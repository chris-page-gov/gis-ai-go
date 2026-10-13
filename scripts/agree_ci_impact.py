#!/usr/bin/env python3
"""Compare CI recommendations using only an independently extracted base evaluator.

This module and its sibling plan_ci_impact.py must come from the exact trusted
base commit. The candidate supplies data only; no candidate Python is executed.
The result remains shadow evidence and cannot itself authorise skipping a job.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence


MAP_PATH = ".github/ci/verification-impact-map.v2.json"
SCHEMA = "gis-ai-go.ci-impact-agreement.v1"
MAX_PLAN_BYTES = 64 * 1024 * 1024
CONTROL_PATHS = frozenset(
    {
        "scripts/plan_ci_impact.py",
        "scripts/agree_ci_impact.py",
        "tests/contract/test_ci_impact_plan.py",
        "tests/contract/test_ci_impact_agreement.py",
        "tests/contract/test_pages_workflows.py",
    }
)
DECISION_FIELDS = (
    "force_full",
    "gateway_image_required",
    "selected_lanes",
    "applicable_lanes",
    "always_run",
    "lane_decisions",
)
CANDIDATE_RESULTS = ("success", "failure", "cancelled", "skipped", "missing", "")


class AgreementError(ValueError):
    """A required piece of agreement evidence could not be established."""


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _closed_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AgreementError("candidate plan has duplicate JSON keys")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise AgreementError("candidate plan has a non-finite JSON number")


def _regular_bytes(path: Path, maximum: int) -> bytes:
    # O_NOFOLLOW also prevents a link substitution between inspection and open.
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as handle:
        metadata = os.fstat(handle.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > maximum:
            raise AgreementError("evidence must be a bounded regular file")
        raw = handle.read(maximum + 1)
    if len(raw) > maximum:
        raise AgreementError("evidence exceeds its byte limit")
    return raw


def _load_base_evaluator() -> Any:
    # An isolated Python invocation excludes candidate directories. Loading only
    # this sibling additionally avoids resolving an import through candidate code.
    source = Path(__file__).resolve().with_name("plan_ci_impact.py")
    _regular_bytes(source, 1024 * 1024)
    spec = importlib.util.spec_from_file_location("_trusted_ci_impact", source)
    if spec is None or spec.loader is None:
        raise AgreementError("base evaluator is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclass resolves its defining module here.
    spec.loader.exec_module(module)
    return module


def _git_blob(root: Path, commit: str, path: str, maximum: int) -> bytes:
    # commit has already passed the base evaluator's full-commit validation.
    listing = subprocess.run(
        ("git", "ls-tree", "-z", commit, "--", path),
        cwd=root,
        check=True,
        capture_output=True,
        timeout=30,
    ).stdout
    entries = listing.rstrip(b"\0").split(b"\0")
    if len(entries) != 1 or b"\t" not in entries[0]:
        raise AgreementError("policy blob is missing")
    metadata, name = entries[0].split(b"\t", 1)
    fields = metadata.split(b" ")
    if len(fields) != 3 or fields[0] not in {b"100644", b"100755"} or fields[1] != b"blob":
        raise AgreementError("policy source must be a regular Git blob")
    if name.decode("utf-8") != path:
        raise AgreementError("policy source identity differs")
    identity = fields[2].decode("ascii")
    size = int(subprocess.run(
        ("git", "cat-file", "-s", identity), cwd=root, check=True,
        capture_output=True, timeout=30,
    ).stdout)
    if size > maximum:
        raise AgreementError("policy blob exceeds its byte limit")
    raw = subprocess.run(
        ("git", "cat-file", "blob", identity), cwd=root, check=True,
        capture_output=True, timeout=30,
    ).stdout
    if len(raw) != size:
        raise AgreementError("policy blob size differs")
    return raw


def _decision(plan: dict[str, object]) -> dict[str, object]:
    return {key: plan[key] for key in DECISION_FIELDS}


def _is_control(path: str) -> bool:
    return path.startswith(".github/") or path in CONTROL_PATHS


def agree(
    *, repository_root: Path, base: str, head: str, event: str,
    candidate_plan: Path, candidate_result: str,
) -> dict[str, object]:
    receipt: dict[str, object] = {
        "schema": SCHEMA,
        "mode": "shadow",
        "enforced": False,
        "event": event,
        "base_commit": base,
        "head_commit": head,
        "policy_source_commit": base,
        "candidate_result": candidate_result,
        "force_full": True,
        "gateway_image_required": True,
        "reason": "trusted-evaluation-failed",
        "agreement_sha256": digest(Path(__file__).read_bytes()),
        "planner_sha256": None,
        "base_map_sha256": None,
        "candidate_map_sha256": None,
        "changed_path_count": None,
        "changed_paths": None,
        "base_plan_sha256": None,
        "candidate_plan_sha256": None,
        "expected_candidate_plan_sha256": None,
        "base_decision": None,
        "candidate_decision": None,
    }
    try:
        evaluator = _load_base_evaluator()
        receipt["planner_sha256"] = digest(Path(evaluator.__file__).read_bytes())
        root = evaluator.resolve_repository_root(repository_root)
        paths = evaluator.changed_paths_between(root, base, head)
        receipt["changed_paths"] = list(paths)
        receipt["changed_path_count"] = len(paths)
        with tempfile.TemporaryDirectory(prefix="ci-impact-base-") as directory:
            map_file = Path(directory) / "map.json"
            raw_base = _git_blob(root, base, MAP_PATH, evaluator.MAX_MAP_BYTES)
            receipt["base_map_sha256"] = digest(raw_base)
            map_file.write_bytes(raw_base)
            base_map = evaluator.load_impact_map(map_file)
            base_plan = evaluator.plan_for_paths(
                base_map, paths, base_commit=base, head_commit=head, event=event,
            )
            receipt["base_plan_sha256"] = digest(canonical_bytes(base_plan))
            receipt["base_decision"] = _decision(base_plan)

            if event == "push_main":
                receipt["reason"] = "protected-main-exact-commit"
                return receipt
            if candidate_result != "success":
                receipt["reason"] = "candidate-job-not-successful"
                return receipt

            raw_candidate_map = _git_blob(root, head, MAP_PATH, evaluator.MAX_MAP_BYTES)
            receipt["candidate_map_sha256"] = digest(raw_candidate_map)
            map_file.write_bytes(raw_candidate_map)
            candidate_map = evaluator.load_impact_map(map_file)
            expected = evaluator.plan_for_paths(
                candidate_map, paths, base_commit=base, head_commit=head, event=event,
            )
            expected_raw = canonical_bytes(expected)
            receipt["expected_candidate_plan_sha256"] = digest(expected_raw)

        receipt["reason"] = "candidate-plan-invalid"
        raw_candidate = _regular_bytes(candidate_plan, MAX_PLAN_BYTES)
        receipt["candidate_plan_sha256"] = digest(raw_candidate)
        candidate = json.loads(
            raw_candidate.decode("utf-8"), object_pairs_hook=_closed_pairs,
            parse_constant=_reject_constant,
        )
        # Canonical byte comparison distinguishes false from 0, true from 1,
        # binds the complete closed schema and every source/inventory identity,
        # and refuses a plausible-looking false recommendation from changed code.
        if canonical_bytes(candidate) != expected_raw:
            receipt["reason"] = "candidate-plan-mismatch"
            return receipt
        receipt["candidate_decision"] = _decision(candidate)
        # Never let a candidate redefine what counts as control-plane code.
        # Retain both valid decisions first, so a weakened candidate map is
        # visible in the diagnostic evidence even though it cannot take effect.
        if any(_is_control(path) for path in paths):
            receipt["reason"] = (
                "control-path-change" if base_plan["force_full"] is True
                else "trusted-control-route-not-full"
            )
            return receipt
        if canonical_bytes(_decision(base_plan)) != canonical_bytes(_decision(candidate)):
            receipt["reason"] = "policy-disagreement"
            return receipt
        if base_plan["gateway_image_required"] is not False or candidate["gateway_image_required"] is not False:
            receipt["reason"] = "both-policies-require-image"
            return receipt
        if base_plan["force_full"] is not False or candidate["force_full"] is not False:
            receipt["reason"] = "full-assurance-required"
            return receipt
        receipt["reason"] = "both-policies-omit-image"
        receipt["gateway_image_required"] = False
        receipt["force_full"] = False
    except (ValueError, OSError, subprocess.SubprocessError, ImportError, RecursionError):
        # No exception detail or untrusted artifact text is echoed into logs.
        # An absent/invalid base or candidate is a positive full-assurance result.
        pass
    return receipt


def write_receipt(path: Path, payload: bytes) -> None:
    if not path.is_absolute():
        raise AgreementError("receipt output must be absolute")
    if path.parent.resolve(strict=True) != path.parent:
        raise AgreementError("receipt parent must not use a symbolic-link alias")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--event", choices=("pull_request", "push_main"), required=True)
    parser.add_argument("--candidate-plan", type=Path, required=True)
    parser.add_argument("--candidate-result", choices=CANDIDATE_RESULTS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    if not arguments.candidate_plan.is_absolute():
        parser.error("candidate plan must use an absolute path")
    receipt = agree(
        repository_root=arguments.repository_root, base=arguments.base,
        head=arguments.head, event=arguments.event,
        candidate_plan=arguments.candidate_plan, candidate_result=arguments.candidate_result,
    )
    payload = canonical_bytes(receipt)
    try:
        write_receipt(arguments.output, payload)
    except (OSError, AgreementError) as error:
        raise SystemExit("CI impact agreement could not write a new receipt") from error
    print(payload.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
