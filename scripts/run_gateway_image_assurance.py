#!/usr/bin/env python3
"""Run the closed DEPLOY-207 gateway image assurance pipeline."""

from __future__ import annotations

import argparse
import os
import re
import signal
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from gateway_evidence import write_evidence_manifest
from gateway_image import (
    PRIVACY_PHASE_OUTPUT_BOUNDARY,
    ROOT,
    contains_diagnostic_private_path,
    prohibited_text_reason,
)


PHASE_TIMEOUT_SECONDS = 40 * 60
PHASE_DRAIN_TIMEOUT_SECONDS = 10
MAX_PHASE_OUTPUT_BYTES = 1024 * 1024
PHASE_OUTPUT_CHUNK_BYTES = 64 * 1024
PHASE_OUTPUT_BOUNDARY = PRIVACY_PHASE_OUTPUT_BOUNDARY + "\n"
PHASE_NAME = re.compile(r"[a-z][a-z0-9-]{0,63}\Z")


def _contains_reserved_phase_boundary(text: str) -> bool:
    return any(
        line == PRIVACY_PHASE_OUTPUT_BOUNDARY for line in text.splitlines()
    )


def prohibited_phase_transcript_reason(text: str) -> str | None:
    """Classify one trusted, boundary-terminated phase replay transcript."""
    if not text.endswith(PHASE_OUTPUT_BOUNDARY):
        return "malformed-boundary"
    lines = text.splitlines()
    if not lines or lines[-1] != PRIVACY_PHASE_OUTPUT_BOUNDARY:
        return "malformed-boundary"
    frame: list[str] = []
    for line in lines:
        if line == PRIVACY_PHASE_OUTPUT_BOUNDARY:
            reason = prohibited_text_reason("\n".join(frame))
            if reason is not None:
                return reason
            frame = []
        else:
            frame.append(line)
    return None if not frame else "malformed-boundary"


def timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def remove_generated_path(path: Path) -> None:
    """Remove one exact generated path without following symbolic links."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _directory_identity(
    path: Path, *, owner_private: bool = False
) -> tuple[int, int, int, int, int]:
    """Return a non-following identity for one real directory."""
    try:
        metadata = path.lstat()
    except OSError:
        raise ValueError("gateway assurance artefact root is unavailable") from None
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("gateway assurance artefact root must be a real directory")
    mode = stat.S_IMODE(metadata.st_mode)
    if metadata.st_uid != os.getuid():
        raise ValueError("gateway assurance artefact directory must be owner-controlled")
    if owner_private and mode != 0o700:
        raise ValueError("gateway assurance quarantine must remain owner-private")
    if not owner_private and mode & 0o022:
        raise ValueError(
            "gateway assurance artefact root must not be group or world writable"
        )
    return metadata.st_dev, metadata.st_ino, metadata.st_uid, metadata.st_gid, mode


def _require_directory_identity(
    path: Path, identity: tuple[int, int, int, int, int]
) -> None:
    if _directory_identity(path) != identity:
        raise ValueError("gateway assurance artefact root identity changed")


class _PhaseOutput:
    """Count one binary process stream while retaining only a bounded prefix."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.byte_count = 0
        self._prefix = bytearray()
        self.read_failed = False

    def consume(self, stream: Any) -> None:
        try:
            while True:
                chunk = stream.read(PHASE_OUTPUT_CHUNK_BYTES)
                if chunk in (b"", None):
                    break
                if not isinstance(chunk, bytes):
                    self.read_failed = True
                    break
                self.byte_count += len(chunk)
                remaining = MAX_PHASE_OUTPUT_BYTES + 1 - len(self._prefix)
                if remaining > 0:
                    self._prefix.extend(chunk[:remaining])
        except Exception:
            self.read_failed = True
        finally:
            try:
                stream.close()
            except Exception:
                self.read_failed = True

    def classification(self) -> tuple[str, str, str | None]:
        if self.read_failed:
            return "unavailable", "stream-read-failed", None
        if self.byte_count > MAX_PHASE_OUTPUT_BYTES:
            return "withheld", "over-bound", None
        raw = bytes(self._prefix)
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            return "withheld", "invalid-utf8", None
        if any(
            unicodedata.category(character).startswith("C")
            and character not in "\t\n\r"
            for character in text
        ):
            return "withheld", "unsafe-control", None
        if any(line.lstrip().startswith("::") for line in text.splitlines()):
            return "withheld", "workflow-command", None
        if _contains_reserved_phase_boundary(text):
            return "withheld", "reserved-boundary", None
        prohibited_reason = prohibited_text_reason(text)
        normalised = " ".join(text.split())
        if prohibited_reason is not None:
            return "withheld", prohibited_reason, None
        if contains_diagnostic_private_path(normalised):
            return "withheld", "private-path", None
        return "readable", "privacy-safe", text

    def diagnostic(self, classification: tuple[str, str, str | None]) -> str:
        status, reason, _ = classification
        return f"{self.label}_status={status} {self.label}_reason={reason}"


def _unavailable_stream_diagnostic(label: str, reason: str) -> str:
    return f"{label}_status=unavailable {label}_reason={reason}"


def _terminate_process_group(process: subprocess.Popen[bytes]) -> bool:
    """Terminate the isolated phase process group without reflecting failures."""
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
            return True
        except ProcessLookupError:
            return False
        except OSError:
            pass
    try:
        if process.poll() is None:
            process.kill()
            return True
    except OSError:
        pass
    return False


def _prohibited_phase_output_reason(
    outputs: tuple[_PhaseOutput, _PhaseOutput],
    classifications: tuple[tuple[str, str, str | None], ...],
) -> str | None:
    texts: list[str] = []
    for _output, classification in zip(outputs, classifications, strict=True):
        _status, reason, text = classification
        if text is None:
            return reason
        texts.append(text)
    if _contains_reserved_phase_boundary("".join(texts)):
        return "reserved-boundary"
    projection = "".join(texts)
    if any(line.lstrip().startswith("::") for line in projection.splitlines()):
        return "workflow-command"
    prohibited_reason = prohibited_text_reason(projection)
    if prohibited_reason is not None:
        return prohibited_reason
    if contains_diagnostic_private_path(" ".join(projection.split())):
        return "private-path"
    return None


def _emit_phase_output(
    name: str,
    outputs: tuple[_PhaseOutput, _PhaseOutput],
    classifications: tuple[tuple[str, str, str | None], ...],
    *,
    replay: bool,
    reason: str,
) -> None:
    """Replay an entirely safe result or emit fixed status metadata only."""
    if replay:
        for classification, destination in zip(
            classifications, (sys.stdout, sys.stderr), strict=True
        ):
            _status, _reason, text = classification
            if text:
                destination.write(text)
                if not text.endswith("\n"):
                    destination.write("\n")
                destination.write(PHASE_OUTPUT_BOUNDARY)
                destination.flush()
        return
    sys.stderr.write(
        f"gateway image assurance phase {name} output withheld; output_reason={reason}; "
        f"{outputs[0].diagnostic(classifications[0])}; "
        f"{outputs[1].diagnostic(classifications[1])}\n"
    )
    sys.stderr.flush()


def run_checked(
    name: str,
    arguments: list[str],
    *,
    timeout_seconds: float = PHASE_TIMEOUT_SECONDS,
) -> None:
    if PHASE_NAME.fullmatch(name) is None:
        raise ValueError("gateway image assurance phase name is invalid")
    failure: str | None = None
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            tuple(arguments),
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except (OSError, ValueError):
        failure = "could not be started"
    if failure is not None:
        sys.stderr.write(
            f"gateway image assurance phase {name} output unavailable; "
            f"{_unavailable_stream_diagnostic('stdout', 'process-start-failed')}; "
            f"{_unavailable_stream_diagnostic('stderr', 'process-start-failed')}\n"
        )
        sys.stderr.flush()
        raise ValueError(f"gateway image assurance phase {name} {failure}")
    if process is None or process.stdout is None or process.stderr is None:
        raise ValueError(f"gateway image assurance phase {name} could not be started")

    stdout = _PhaseOutput("stdout")
    stderr = _PhaseOutput("stderr")
    threads = (
        threading.Thread(target=stdout.consume, args=(process.stdout,), daemon=True),
        threading.Thread(target=stderr.consume, args=(process.stderr,), daemon=True),
    )
    for thread in threads:
        thread.start()

    timed_out = False
    wait_failed = False
    descendant_group_terminated = False
    return_code: int | None = None
    try:
        return_code = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _terminate_process_group(process)
        try:
            return_code = process.wait(timeout=PHASE_DRAIN_TIMEOUT_SECONDS)
        except (OSError, subprocess.TimeoutExpired):
            wait_failed = True
    except OSError:
        wait_failed = True
        _terminate_process_group(process)
        try:
            return_code = process.wait(timeout=PHASE_DRAIN_TIMEOUT_SECONDS)
        except (OSError, subprocess.TimeoutExpired):
            pass
    if not timed_out and not wait_failed:
        descendant_group_terminated = _terminate_process_group(process)

    drain_failed: set[str] = set()
    drain_deadline = time.monotonic() + PHASE_DRAIN_TIMEOUT_SECONDS
    for output, thread in zip((stdout, stderr), threads, strict=True):
        thread.join(timeout=max(0.0, drain_deadline - time.monotonic()))
        if thread.is_alive():
            drain_failed.add(output.label)

    outputs = (stdout, stderr)
    classifications: tuple[tuple[str, str, str | None], ...] | None = None
    prohibited_output_reason: str | None = None
    if not drain_failed:
        classifications = tuple(output.classification() for output in outputs)
        prohibited_output_reason = _prohibited_phase_output_reason(
            outputs, classifications
        )
    if timed_out:
        failure = "timed out"
    elif (
        wait_failed
        or descendant_group_terminated
        or drain_failed
        or stdout.read_failed
        or stderr.read_failed
    ):
        failure = "could not be completed"
    elif type(return_code) is not int or return_code != 0:
        failure = "exited unsuccessfully"
    elif prohibited_output_reason is not None:
        failure = "emitted prohibited output"
    if drain_failed:
        sys.stderr.write(
            f"gateway image assurance phase {name} output unavailable; "
            f"{_unavailable_stream_diagnostic('stdout', 'stream-drain-timeout')}; "
            f"{_unavailable_stream_diagnostic('stderr', 'stream-drain-timeout')}\n"
        )
        sys.stderr.flush()
    elif failure is None and classifications is not None:
        _emit_phase_output(
            name,
            outputs,
            classifications,
            replay=True,
            reason="privacy-safe",
        )
    else:
        if classifications is None:
            raise ValueError(f"gateway image assurance phase {name} could not be completed")
        _emit_phase_output(
            name,
            outputs,
            classifications,
            replay=False,
            reason=prohibited_output_reason or failure.replace(" ", "-"),
        )
    if failure is not None:
        raise ValueError(f"gateway image assurance phase {name} {failure}")


def run_phase(name: str, arguments: list[str]) -> dict[str, object]:
    started_at = timestamp()
    started = time.monotonic()
    run_checked(name, arguments)
    return {
        "name": name,
        "started_at": started_at,
        "completed_at": timestamp(),
        "duration_ms": round((time.monotonic() - started) * 1000),
        "passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/gateway"))
    parser.add_argument("--platform", default="linux/amd64")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()
    output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    allowed_root = ROOT / "artifacts"
    if output != allowed_root / "gateway":
        raise ValueError("gateway assurance output must be the exact repository artefact directory")
    try:
        allowed_root.mkdir(mode=0o700)
    except FileExistsError:
        pass
    root_identity = _directory_identity(allowed_root)
    _require_directory_identity(allowed_root, root_identity)
    if output.exists() or output.is_symlink():
        remove_generated_path(output)
    quarantine = Path(
        tempfile.mkdtemp(prefix=".gateway-quarantine-", dir=allowed_root)
    )
    quarantine_identity = _directory_identity(quarantine, owner_private=True)
    promoted = False

    python = sys.executable
    dirty = ["--allow-dirty"] if args.allow_dirty else []

    def require_assurance_paths() -> None:
        _require_directory_identity(allowed_root, root_identity)
        _require_directory_identity(quarantine, quarantine_identity)

    def artifact(name: str) -> str:
        require_assurance_paths()
        return str(quarantine / name)

    def checked_phase(name: str, arguments: list[str]) -> dict[str, object]:
        require_assurance_paths()
        result = run_phase(name, arguments)
        require_assurance_paths()
        return result

    try:
        require_assurance_paths()
        phases = [
            checked_phase(
                "okf",
                [python, "scripts/build_okf.py", "--output", "artifacts/okf"],
            ),
            checked_phase(
                "package",
                [
                    python,
                    "scripts/package_gateway_oci.py",
                    "--output-dir",
                    str(quarantine),
                    "--platform",
                    args.platform,
                    *dirty,
                ],
            ),
            checked_phase(
                "verify",
                [
                    python,
                    "scripts/verify_gateway_oci.py",
                    "--archive",
                    artifact("gateway-image.oci.tar"),
                    "--checksum",
                    artifact("gateway-image.oci.tar.sha256"),
                    "--receipt",
                    artifact("image-receipt.json"),
                    "--context-manifest",
                    artifact("build-context.sha256"),
                ],
            ),
            checked_phase(
                "reproducibility",
                [
                    python,
                    "scripts/check_gateway_image_reproducibility.py",
                    "--reference",
                    artifact("gateway-image.oci.tar"),
                    "--receipt",
                    artifact("image-receipt.json"),
                    *dirty,
                ],
            ),
            checked_phase(
                "sbom",
                [
                    python,
                    "scripts/generate_gateway_image_sbom.py",
                    "--archive",
                    artifact("gateway-image.oci.tar"),
                    "--receipt",
                    artifact("image-receipt.json"),
                    "--output",
                    artifact("gateway-image.sbom.cdx.json"),
                ],
            ),
            checked_phase(
                "vulnerability-scan",
                [
                    python,
                    "scripts/scan_gateway_image.py",
                    "--archive",
                    artifact("gateway-image.oci.tar"),
                    "--sbom",
                    artifact("gateway-image.sbom.cdx.json"),
                    "--receipt",
                    artifact("image-receipt.json"),
                    "--output",
                    artifact("gateway-image.vulnerability-scan.json"),
                ],
            ),
            checked_phase(
                "container-acceptance",
                [
                    python,
                    "scripts/check_gateway_container.py",
                    "--archive",
                    artifact("gateway-image.oci.tar"),
                    "--receipt",
                    artifact("image-receipt.json"),
                    "--output",
                    artifact("container-acceptance.json"),
                ],
            ),
        ]
        require_assurance_paths()
        write_evidence_manifest(quarantine, phases)
        require_assurance_paths()
        run_checked(
            "final-verification",
            [
                python,
                "scripts/verify_gateway_image_evidence.py",
                "--directory",
                str(quarantine),
            ],
        )
        require_assurance_paths()
        if output.exists() or output.is_symlink():
            raise ValueError("gateway assurance output appeared before verified promotion")
        quarantine.replace(output)
        promoted = True
    finally:
        if not promoted:
            try:
                _require_directory_identity(allowed_root, root_identity)
            except ValueError:
                pass
            else:
                remove_generated_path(output)
                try:
                    _require_directory_identity(quarantine, quarantine_identity)
                except ValueError:
                    pass
                else:
                    remove_generated_path(quarantine)
    print("Gateway image assurance and offline evidence replay passed.")


if __name__ == "__main__":
    main()
