#!/usr/bin/env python3
"""Exercise the exact blocked gateway OCI image through its local Compose boundary."""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import os
import re
import socket
import stat
import subprocess
import tempfile
import threading
import time
import unicodedata
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Iterator

from jsonschema import Draft202012Validator, FormatChecker

from gateway_image import (
    EXPECTED_ENVIRONMENT,
    EXPECTED_ENTRYPOINT,
    EXPECTED_HEALTHCHECK,
    EXPECTED_HEALTH_CONFIGURATION,
    EXPECTED_PORT,
    EXPECTED_USER,
    EXPECTED_WORKING_DIRECTORY,
    LEDGER_ROOT,
    MAX_JSON_BYTES,
    OCI_MANIFEST_MEDIA_TYPE,
    RECONCILIATION_ROOT,
    RECEIPT_SCHEMA,
    contains_diagnostic_private_path,
    ROOT,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    inspect_oci_archive,
    prohibited_text_reason,
    sha256_file,
)

COMPOSE_RELATIVE = "deploy/gateway/compose.candidate.yaml"
COMPOSE_FILE = ROOT / COMPOSE_RELATIVE
ACCEPTANCE_SCHEMA = ROOT / "schemas" / "gateway-container-acceptance.schema.json"
HOST = "127.0.0.1"
PORT = 8_787
MCP_VERSION = "2026-07-28"
RAW_KEY_SENTINEL = "gis-ai-go:ik:v1:" + "a" * 64
EXPECTED_TMPFS = {
    "/tmp": "rw,noexec,nosuid,nodev,size=1m,mode=0700,uid=65532,gid=65532"
}
EXPECTED_CHECKS = [
    "exact-oci-load",
    "closed-compose-topology",
    "exact-image-runtime-identity",
    "closed-compose-labels",
    "non-root-read-only-runtime",
    "loopback-only-internal-network",
    "blocked-health-readiness",
    "zero-tools-routes-resources",
    "private-disjoint-storage",
    "runtime-resource-bounds",
    "restart-persistence",
    "log-minimisation",
    "service-suspension",
    "exact-image-restore",
    "closed-acceptance-receipt",
]
DOCKER_LOAD_TIMEOUT_SECONDS = 10 * 60
MAX_DOCKER_LOAD_DIAGNOSTIC_BYTES = 4 * 1024
_DOCKER_LOAD_SENSITIVE = re.compile(
    r"(?i)(?:"
    r"bearer|auth|oauth|credentials?|api[ _-]?keys?|"
    r"(?:access|refresh)[ _-]?tokens?|tokens?|"
    r"passwords?|passwd|pwd|client[ _-]?secrets?|secrets?"
    r")"
)
COMPOSE_CONTAINER_LABELS = frozenset(
    {
        "com.docker.compose.config-hash",
        "com.docker.compose.container-number",
        "com.docker.compose.depends_on",
        "com.docker.compose.image",
        "com.docker.compose.oneoff",
        "com.docker.compose.project",
        "com.docker.compose.project.config_files",
        "com.docker.compose.project.working_dir",
        "com.docker.compose.service",
        "com.docker.compose.version",
    }
)
CONTAINER_HTTP_SCRIPT = r"""
import http from 'node:http';
const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const input = JSON.parse(Buffer.concat(chunks).toString('utf8'));
const requestBody = input.body === null ? null : Buffer.from(input.body, 'base64');
const requestHeaders = {...input.headers};
if (requestBody !== null) requestHeaders['content-length'] = String(requestBody.length);
const reply = await new Promise((resolve, reject) => {
  const request = http.request({
    host: '127.0.0.1', port: 8787, method: input.method, path: input.path,
    headers: requestHeaders,
  }, (response) => {
    const body = [];
    response.on('data', (chunk) => body.push(chunk));
    response.on('end', () => resolve({
      status: response.statusCode,
      body: Buffer.concat(body).toString('base64'),
    }));
  });
  request.on('error', reject);
  if (requestBody !== null) request.write(requestBody);
  request.end();
});
process.stdout.write(JSON.stringify(reply));
"""


def run(
    arguments: Iterable[str],
    *,
    capture: bool = False,
    discard_output: bool = False,
    check: bool = True,
    environment: dict[str, str] | None = None,
    input_text: str | None = None,
    timeout: int = 10 * 60,
) -> subprocess.CompletedProcess[str]:
    if capture and discard_output:
        raise ValueError("command output cannot be captured and discarded")
    return subprocess.run(
        tuple(arguments), cwd=ROOT, check=check, capture_output=capture,
        stdout=subprocess.DEVNULL if discard_output else None,
        stderr=subprocess.DEVNULL if discard_output else None,
        text=True, env=environment, input=input_text, timeout=timeout,
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class _DockerLoadStream:
    """Incrementally count one process stream while retaining a bounded prefix."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.byte_count = 0
        self._prefix = bytearray()
        self.read_failed = False

    def consume(self, stream: Any) -> None:
        try:
            while True:
                chunk = stream.read(64 * 1024)
                if chunk in (b"", None):
                    break
                if not isinstance(chunk, bytes):
                    self.read_failed = True
                    break
                self.byte_count += len(chunk)
                remaining = MAX_DOCKER_LOAD_DIAGNOSTIC_BYTES + 1 - len(self._prefix)
                if remaining > 0:
                    self._prefix.extend(chunk[:remaining])
        except Exception:
            self.read_failed = True
        finally:
            try:
                stream.close()
            except Exception:
                self.read_failed = True

    def _classification(self) -> tuple[str, str, str | None]:
        if self.read_failed:
            return "unavailable", "stream-read-failed", None
        if self.byte_count > MAX_DOCKER_LOAD_DIAGNOSTIC_BYTES:
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
        prohibited_reason = prohibited_text_reason(text)
        normalised = " ".join(text.split())
        if prohibited_reason is None:
            prohibited_reason = prohibited_text_reason(normalised)
        if prohibited_reason is not None:
            return "withheld", prohibited_reason, None
        if contains_diagnostic_private_path(normalised):
            return "withheld", "private-path", None
        if _DOCKER_LOAD_SENSITIVE.search(normalised):
            return "withheld", "sensitive", None
        return "withheld", "privacy-safe", text

    def diagnostic(self) -> str:
        status, reason, _ = self._classification()
        return f"{self.label}_status={status} {self.label}_reason={reason}"

    def success_text(self) -> str | None:
        _, reason, text = self._classification()
        return text if reason == "privacy-safe" else None


def _docker_load_unavailable_stream(
    label: str, *, reason: str = "no-captured-output"
) -> str:
    return f"{label}_status=unavailable {label}_reason={reason}"


def load_docker_archive(archive: Path) -> subprocess.CompletedProcess[str]:
    """Load one archive with bounded binary streaming and detached diagnostics."""
    arguments = ("docker", "load", "--input", str(archive))
    process: subprocess.Popen[bytes] | None = None
    failure: ValueError | None = None
    try:
        process = subprocess.Popen(
            arguments,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        failure = ValueError(
            f"gateway image load failed; process_status=start-failed; "
            f"{_docker_load_unavailable_stream('stdout')}; "
            f"{_docker_load_unavailable_stream('stderr')}"
        )
    if failure is not None:
        raise failure
    if process is None or process.stdout is None or process.stderr is None:
        raise ValueError("gateway image load completed without a process result")

    stdout = _DockerLoadStream("stdout")
    stderr = _DockerLoadStream("stderr")
    threads = (
        threading.Thread(target=stdout.consume, args=(process.stdout,), daemon=True),
        threading.Thread(target=stderr.consume, args=(process.stderr,), daemon=True),
    )
    for thread in threads:
        thread.start()

    timed_out = False
    wait_failed = False
    return_code: int | None = None
    try:
        return_code = process.wait(timeout=DOCKER_LOAD_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            process.kill()
            return_code = process.wait(timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            wait_failed = True
    except OSError:
        wait_failed = True
        try:
            process.kill()
            return_code = process.wait(timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            pass

    drain_failed: set[str] = set()
    for collector, stream, thread in zip(
        (stdout, stderr), (process.stdout, process.stderr), threads, strict=True
    ):
        thread.join(timeout=10)
        if thread.is_alive():
            try:
                stream.close()
            except OSError:
                pass
            thread.join(timeout=1)
        if thread.is_alive():
            drain_failed.add(collector.label)
    wait_failed = wait_failed or bool(drain_failed)
    stdout_diagnostic = (
        _docker_load_unavailable_stream("stdout", reason="stream-drain-timeout")
        if "stdout" in drain_failed
        else stdout.diagnostic()
    )
    stderr_diagnostic = (
        _docker_load_unavailable_stream("stderr", reason="stream-drain-timeout")
        if "stderr" in drain_failed
        else stderr.diagnostic()
    )

    if timed_out:
        failure = ValueError(
            f"gateway image load failed; process_status=timed-out "
            f"timeout_seconds={DOCKER_LOAD_TIMEOUT_SECONDS}; "
            f"{stdout_diagnostic}; {stderr_diagnostic}"
        )
    elif wait_failed or stdout.read_failed or stderr.read_failed:
        failure = ValueError(
            f"gateway image load failed; process_status=stream-failed; "
            f"{stdout_diagnostic}; {stderr_diagnostic}"
        )
    elif type(return_code) is not int or return_code != 0:
        exit_code = return_code if type(return_code) is int else "unknown"
        failure = ValueError(
            f"gateway image load failed; process_status=exit-code "
            f"process_exit_code={exit_code}; {stdout_diagnostic}; {stderr_diagnostic}"
        )
    else:
        stdout_text = stdout.success_text()
        stderr_text = stderr.success_text()
        if stdout_text is None or stderr_text is None:
            failure = ValueError(
                f"gateway image load failed; process_status=invalid-success-output; "
                f"{stdout_diagnostic}; {stderr_diagnostic}"
            )
        else:
            return subprocess.CompletedProcess(
                arguments,
                return_code,
                stdout=stdout_text,
                stderr=stderr_text,
            )
    if failure is not None:
        raise failure
    raise ValueError("gateway image load completed without a process result")


def load_json_object(path: Path, *, maximum: int = MAX_JSON_BYTES) -> dict[str, Any]:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError("acceptance input must be one real regular file")
    if metadata.st_size > maximum:
        raise ValueError("acceptance JSON input exceeds its byte bound")
    try:
        value = json.loads(path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("acceptance JSON input is invalid") from error
    if not isinstance(value, dict):
        raise ValueError("acceptance JSON input must be an object")
    return value


def validate_schema_instance(schema_path: Path, value: dict[str, Any]) -> None:
    schema = load_json_object(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


@contextmanager
def record_phase(phases: list[dict[str, Any]], name: str) -> Iterator[None]:
    started_at = utc_now()
    started_ns = time.monotonic_ns()
    yield
    phases.append(
        {
            "name": name,
            "started_at": started_at,
            "ended_at": utc_now(),
            "duration_ms": max(0, (time.monotonic_ns() - started_ns) // 1_000_000),
            "status": "passed",
        }
    )


def compose(
    project: str, environment: dict[str, str], *arguments: str,
    capture: bool = False, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return run(
        ("docker", "compose", "--project-name", project, "--file", str(COMPOSE_FILE),
         *arguments),
        capture=capture, discard_output=not capture, check=check,
        environment=environment,
    )


def expected_rendered_compose(project: str, image: str) -> dict[str, Any]:
    return {
        "name": project,
        "networks": {
            "offline": {
                "name": f"{project}_offline", "driver": "bridge", "ipam": {},
                "internal": True,
            }
        },
        "services": {
            "gateway": {
                "cap_drop": ["ALL"], "cpus": 0.5, "command": None,
                "deploy": {
                    "replicas": 1,
                    "resources": {
                        "limits": {"cpus": 0.5, "memory": "268435456", "pids": 64}
                    },
                    "placement": {},
                },
                "entrypoint": None, "image": image,
                "logging": {
                    "driver": "json-file",
                    "options": {"max-file": "1", "max-size": "1m"},
                },
                "mem_limit": "268435456", "memswap_limit": "268435456",
                "networks": {"offline": None}, "pids_limit": 64,
                "ports": [{
                    "mode": "ingress", "host_ip": HOST, "target": PORT,
                    "published": str(PORT), "protocol": "tcp",
                }],
                "pull_policy": "never", "read_only": True, "restart": "no",
                "security_opt": ["no-new-privileges:true"],
                "stop_grace_period": "35s",
                "tmpfs": [f"/tmp:{EXPECTED_TMPFS['/tmp']}"],
                "ulimits": {"nofile": {"soft": 1024, "hard": 1024}},
                "user": EXPECTED_USER,
                "volumes": [
                    {"type": "volume", "source": "evidence-ledger", "target": LEDGER_ROOT},
                    {"type": "volume", "source": "reconciliation-index",
                     "target": RECONCILIATION_ROOT},
                ],
            }
        },
        "volumes": {
            "evidence-ledger": {"name": f"{project}_evidence-ledger"},
            "reconciliation-index": {"name": f"{project}_reconciliation-index"},
        },
    }


def validate_rendered_compose(
    configuration: dict[str, Any], project: str, image: str
) -> str:
    if configuration != expected_rendered_compose(project, image):
        raise AssertionError("rendered Compose configuration differs from its closed shape")
    return sha256_bytes(canonical_json_bytes(configuration))


def _normalised_compose_version(value: str) -> str:
    return value[1:] if value.startswith("v") else value


def normalise_container_labels(
    labels: dict[str, str], *, image_labels: dict[str, str], project: str,
    image_id: str, compose_version: str,
) -> dict[str, str]:
    if not isinstance(labels, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
    ):
        raise AssertionError("running container labels are invalid")
    actual_image_labels = {
        key: value for key, value in labels.items()
        if not key.startswith("com.docker.compose.")
    }
    if actual_image_labels != image_labels:
        raise AssertionError(
            "running container image labels differ from the exact OCI image"
        )
    compose_labels = {
        key: value for key, value in labels.items()
        if key.startswith("com.docker.compose.")
    }
    if set(compose_labels) != COMPOSE_CONTAINER_LABELS:
        raise AssertionError("running container has an incomplete or extra Compose label")
    config_hash = compose_labels["com.docker.compose.config-hash"]
    if re.fullmatch(r"[0-9a-f]{64}", config_hash) is None:
        raise AssertionError("Compose container configuration hash is invalid")
    expected = {
        "com.docker.compose.container-number": "1",
        "com.docker.compose.depends_on": "",
        "com.docker.compose.image": image_id,
        "com.docker.compose.oneoff": "False",
        "com.docker.compose.project": project,
        "com.docker.compose.service": "gateway",
        "com.docker.compose.version": _normalised_compose_version(compose_version),
    }
    if any(compose_labels.get(key) != value for key, value in expected.items()):
        raise AssertionError("running container Compose ownership labels differ")
    config_files = Path(compose_labels["com.docker.compose.project.config_files"])
    working_directory = Path(compose_labels["com.docker.compose.project.working_dir"])
    if (config_files.resolve() != COMPOSE_FILE.resolve()
            or working_directory.resolve() != COMPOSE_FILE.parent.resolve()):
        raise AssertionError("running container Compose source labels differ")
    return {
        "config_hash": config_hash, "container_number": "1", "depends_on": "",
        "image": image_id, "oneoff": "False", "project": "ephemeral-project",
        "project_config_file": COMPOSE_RELATIVE,
        "project_working_directory": "deploy/gateway", "service": "gateway",
        "version": _normalised_compose_version(compose_version),
    }


def normalise_resource_labels(
    labels: dict[str, str], *, project: str, compose_version: str,
    resource_kind: str, logical_name: str,
) -> dict[str, str]:
    identity_key = f"com.docker.compose.{resource_kind}"
    expected_keys = {
        "com.docker.compose.config-hash", "com.docker.compose.project",
        "com.docker.compose.version", identity_key,
    }
    if not isinstance(labels, dict) or set(labels) != expected_keys:
        raise AssertionError(f"Compose {resource_kind} labels are incomplete or extra")
    config_hash = labels["com.docker.compose.config-hash"]
    if re.fullmatch(r"[0-9a-f]{64}", config_hash) is None:
        raise AssertionError(f"Compose {resource_kind} configuration hash is invalid")
    if labels != {
        "com.docker.compose.config-hash": config_hash,
        "com.docker.compose.project": project,
        "com.docker.compose.version": _normalised_compose_version(compose_version),
        identity_key: logical_name,
    }:
        raise AssertionError(f"Compose {resource_kind} ownership labels differ")
    return {
        "config_hash": config_hash, "project": "ephemeral-project",
        "version": _normalised_compose_version(compose_version),
        resource_kind: logical_name,
    }


def classify_transport(port_map: Any) -> dict[str, Any]:
    declared = [{
        "container_port": PORT, "protocol": "tcp", "host_ip": HOST,
        "host_port": PORT,
    }]
    if not isinstance(port_map, dict):
        raise AssertionError("gateway engine port inventory differs from its closed shape")
    if port_map == {}:
        realised = None
    elif set(port_map) == {EXPECTED_PORT}:
        realised = port_map[EXPECTED_PORT]
    else:
        raise AssertionError("gateway engine port inventory differs from its closed shape")
    if realised == [{"HostIp": HOST, "HostPort": str(PORT)}]:
        return {
            "mode": "host-loopback", "declared": declared,
            "realised": [{"host_ip": HOST, "host_port": PORT}],
            "probe_origin": "host-loopback", "host_reachable": True,
            "network_internal": True,
        }
    if realised is None or realised == []:
        return {
            "mode": "container-loopback-internal-engine-fallback", "declared": declared,
            "realised": [], "probe_origin": "container-loopback",
            "host_reachable": False, "network_internal": True,
        }
    raise AssertionError("gateway engine realised an unreviewed port mapping")


def assert_transport_unchanged(
    inspection: Any, expected_transport: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(inspection, dict):
        raise AssertionError("gateway restart inspection is invalid")
    network_settings = inspection.get("NetworkSettings")
    if not isinstance(network_settings, dict):
        raise AssertionError("gateway restart network settings are incomplete")
    config = inspection.get("Config")
    host = inspection.get("HostConfig")
    if (
        not isinstance(config, dict)
        or config.get("ExposedPorts") != {EXPECTED_PORT: {}}
        or not isinstance(host, dict)
        or host.get("PortBindings") != {
            EXPECTED_PORT: [{"HostIp": HOST, "HostPort": str(PORT)}]
        }
    ):
        raise AssertionError("gateway restart port declaration changed")
    transport = classify_transport(network_settings.get("Ports"))
    if transport != expected_transport:
        raise AssertionError("gateway transport changed after restart")
    if transport["mode"] == "container-loopback-internal-engine-fallback":
        assert_host_unreachable()
    return transport


def docker_versions() -> dict[str, Any]:
    version = json.loads(
        run(("docker", "version", "--format", "{{json .}}"), capture=True).stdout
    )
    compose_version = json.loads(
        run(("docker", "compose", "version", "--format", "json"), capture=True).stdout
    )
    client, server = version.get("Client"), version.get("Server")
    if not isinstance(client, dict) or not isinstance(server, dict):
        raise AssertionError("Docker client and server identities are unavailable")
    if not isinstance(compose_version, dict) or set(compose_version) != {"version"}:
        raise AssertionError("Docker Compose version identity is invalid")
    platform = server.get("Platform")
    if not isinstance(platform, dict) or not isinstance(platform.get("Name"), str):
        raise AssertionError("Docker server platform identity is invalid")
    projection = {
        "client": {
            "version": client.get("Version"), "api_version": client.get("ApiVersion"),
            "os": client.get("Os"), "architecture": client.get("Arch"),
        },
        "server": {
            "version": server.get("Version"), "api_version": server.get("ApiVersion"),
            "os": server.get("Os"), "architecture": server.get("Arch"),
            "platform_name": platform["Name"],
        },
        "compose": {"version": compose_version["version"]},
    }
    if not all(
        isinstance(value, str) and 0 < len(value) <= 128
        for group in projection.values() for value in group.values()
    ):
        raise AssertionError("Docker or Compose version identity is incomplete")
    return projection


def request(
    method: str, path: str, *, body: bytes | None = None,
    headers: dict[str, str] | None = None, container: str | None = None,
) -> tuple[int, bytes]:
    request_headers = {"accept": "application/json", **(headers or {})}
    if container is not None:
        payload = json.dumps(
            {
                "method": method, "path": path, "headers": request_headers,
                "body": None if body is None else base64.b64encode(body).decode("ascii"),
            },
            separators=(",", ":"),
        )
        result = run(
            ("docker", "exec", "--interactive", container, "node",
             "--input-type=module", "--eval", CONTAINER_HTTP_SCRIPT),
            capture=True, input_text=payload,
        )
        response = json.loads(result.stdout)
        if (not isinstance(response, dict) or set(response) != {"status", "body"}
                or not isinstance(response["status"], int)
                or not isinstance(response["body"], str)):
            raise AssertionError("container-local HTTP probe returned an invalid envelope")
        return response["status"], base64.b64decode(response["body"], validate=True)
    connection = http.client.HTTPConnection(HOST, PORT, timeout=3)
    try:
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        return response.status, response.read()
    finally:
        connection.close()


def wait_for_health(container: str | None = None, timeout: float = 30.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    failure: Exception | None = None
    while time.monotonic() < deadline:
        try:
            status, body = request("GET", "/healthz", container=container)
            value = json.loads(body)
            if status == 200 and isinstance(value, dict):
                return value
        except (OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
            failure = error
        time.sleep(0.2)
    raise AssertionError("blocked gateway did not become healthy") from failure


def wait_for_container_health(container: str, timeout: float = 30.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        inspection = json.loads(
            run(("docker", "inspect", container), capture=True).stdout
        )[0]
        state = inspection.get("State")
        if isinstance(state, dict) and state.get("Health", {}).get("Status") == "healthy":
            return inspection
        time.sleep(0.2)
    raise AssertionError("Docker did not report the gateway container healthy")


def assert_host_unreachable(observation_seconds: float = 1.0) -> None:
    if not 0.2 <= observation_seconds <= 10.0:
        raise ValueError("host-unreachable observation interval is outside its bound")
    deadline = time.monotonic() + observation_seconds
    while True:
        try:
            connection = socket.create_connection((HOST, PORT), timeout=0.5)
        except ConnectionRefusedError:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            time.sleep(min(0.2, remaining))
            continue
        except OSError:
            raise AssertionError(
                "gateway host port closure probe did not receive a refusal"
            ) from None
        try:
            connection.close()
        except OSError:
            pass
        raise AssertionError("gateway host port became reachable")


def assert_container_stopped(container: str) -> dict[str, Any]:
    inspection = json.loads(run(("docker", "inspect", container), capture=True).stdout)[0]
    state = inspection.get("State")
    actual = {
        "status": state.get("Status") if isinstance(state, dict) else None,
        "running": state.get("Running") if isinstance(state, dict) else None,
        "paused": state.get("Paused") if isinstance(state, dict) else None,
        "restarting": state.get("Restarting") if isinstance(state, dict) else None,
        "oom_killed": state.get("OOMKilled") if isinstance(state, dict) else None,
        "dead": state.get("Dead") if isinstance(state, dict) else None,
        "exit_code": state.get("ExitCode") if isinstance(state, dict) else None,
        "error": state.get("Error") if isinstance(state, dict) else None,
    }
    if actual != {
        "status": "exited", "running": False, "paused": False, "restarting": False,
        "oom_killed": False, "dead": False, "exit_code": 0, "error": "",
    }:
        raise AssertionError("Compose stop did not cleanly suspend the exact gateway container")
    probe = run(("docker", "exec", container, "node", "--version"),
                capture=True, check=False)
    if probe.returncode == 0:
        raise AssertionError("the stopped gateway container still accepted an exec probe")
    return {"status": "exited", "running": False, "exit_code": 0,
            "exec_rejected": True}


def json_from_exec(container: str, expression: str) -> dict[str, Any]:
    result = run(
        ("docker", "exec", container, "node", "--input-type=module", "--eval", expression),
        capture=True,
    )
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise AssertionError("container inspection did not return an object")
    return value


def storage_identity(container: str) -> dict[str, Any]:
    expression = f"""
      import {{ createHash }} from 'node:crypto';
      import {{ readFileSync, statSync }} from 'node:fs';
      const values = {{}};
      for (const [name, path] of [
        ['ledger', '{LEDGER_ROOT}/ledger.json'],
        ['reconciliation', '{RECONCILIATION_ROOT}/index.json'],
      ]) {{
        const bytes = readFileSync(path);
        values[name] = {{
          sha256: createHash('sha256').update(bytes).digest('hex'),
          mode: statSync(path).mode & 0o777,
        }};
      }}
      for (const [name, path] of [
        ['ledger_root', '{LEDGER_ROOT}'],
        ['reconciliation_root', '{RECONCILIATION_ROOT}'],
      ]) values[name] = {{ mode: statSync(path).mode & 0o777 }};
      console.log(JSON.stringify(values));
    """
    return json_from_exec(container, expression)


def assert_http_boundary(
    expected_revision: str, expected_version: str, *, container: str | None,
) -> dict[str, Any]:
    health = wait_for_health(container)
    if (health.get("status") != "ok" or health.get("lifecycle") != "candidate-blocked"
            or health.get("catalogue", {}).get("revision") != expected_revision
            or health.get("catalogue", {}).get("version") != expected_version):
        raise AssertionError("gateway health identity differs from the exact image")
    status, body = request("GET", "/readyz", container=container)
    ready = json.loads(body)
    expected_ready = {
        "status": "blocked",
        "reason": "transport-and-interoperability-unverified",
        "active_tools": [],
        "active_api_operations": [],
    }
    if status != 503 or ready != expected_ready:
        raise AssertionError("gateway readiness is not the exact blocked boundary")
    status, body = request("GET", "/openapi.json", container=container)
    paths = sorted(json.loads(body).get("paths", {}))
    if status != 200 or paths != ["/healthz", "/openapi.json", "/readyz"]:
        raise AssertionError("gateway OpenAPI advertises an operation while blocked")
    status, body = request(
        "POST", "/data/query",
        body=json.dumps({"idempotency_key": RAW_KEY_SENTINEL}).encode(),
        headers={"content-type": "application/json"}, container=container,
    )
    direct_code = json.loads(body).get("code")
    if status != 400 or direct_code != "invalid_request":
        raise AssertionError("blocked direct data route became callable")
    direct_status = status
    mcp_body = json.dumps(
        {
            "jsonrpc": "2.0", "id": 1, "method": "server/discover",
            "params": {"_meta": {
                "io.modelcontextprotocol/protocolVersion": MCP_VERSION,
                "io.modelcontextprotocol/clientCapabilities": {},
                "io.modelcontextprotocol/clientInfo": {
                    "name": "gis-ai-go-container-check", "version": "1.0.0",
                },
            }},
        }, separators=(",", ":"),
    ).encode()
    status, body = request(
        "POST", "/mcp", body=mcp_body,
        headers={
            "accept": "application/json, text/event-stream",
            "content-type": "application/json", "mcp-protocol-version": MCP_VERSION,
            "mcp-method": "server/discover",
        }, container=container,
    )
    capabilities = json.loads(body).get("result", {}).get("capabilities")
    if status != 200 or capabilities != {}:
        raise AssertionError("blocked MCP discovery advertised a capability")
    mcp_status = status
    status, body = request(
        "GET", "/healthz", headers={"host": "attacker.invalid"}, container=container,
    )
    if status != 400 or json.loads(body).get("code") != "invalid_request":
        raise AssertionError("gateway direct face accepted a hostile Host header")
    direct_host_status = status
    status, _ = request(
        "POST", "/mcp", body=mcp_body,
        headers={
            "accept": "application/json, text/event-stream",
            "content-type": "application/json", "host": "attacker.invalid",
            "mcp-protocol-version": MCP_VERSION, "mcp-method": "server/discover",
        }, container=container,
    )
    if status != 403:
        raise AssertionError("gateway MCP face accepted a hostile Host header")
    return {
        "health": health,
        "readiness": {"http_status": 503, **expected_ready},
        "openapi_paths": paths,
        "direct_operation": {"http_status": direct_status, "code": direct_code},
        "mcp_discovery": {"http_status": mcp_status, "capabilities": capabilities},
        "host_filter": {"direct_http_status": direct_host_status, "mcp_http_status": status},
    }


def inspect_loaded_image(
    image: dict[str, Any], tag: str, oci: Any,
) -> tuple[str, dict[str, Any] | None, dict[str, str]]:
    image_id = image.get("Id")
    if (not isinstance(image_id, str)
            or re.fullmatch(r"sha256:[0-9a-f]{64}", image_id) is None):
        raise AssertionError("loaded Docker image identity is invalid")
    if tag not in image.get("RepoTags", []):
        raise AssertionError("loaded Docker image did not retain the exact local tag")
    config = image.get("Config")
    if not isinstance(config, dict):
        raise AssertionError("loaded Docker image configuration is invalid")
    expected = {
        "User": EXPECTED_USER, "ExposedPorts": {EXPECTED_PORT: {}},
        "Env": EXPECTED_ENVIRONMENT, "Entrypoint": EXPECTED_ENTRYPOINT, "Cmd": None,
        "WorkingDir": EXPECTED_WORKING_DIRECTORY, "StopSignal": "SIGTERM",
        "Healthcheck": EXPECTED_HEALTH_CONFIGURATION,
    }
    if any(config.get(key) != value for key, value in expected.items()):
        raise AssertionError("loaded Docker image runtime configuration differs from the OCI image")
    labels = config.get("Labels")
    if labels != oci.labels:
        raise AssertionError("loaded Docker image labels differ from the OCI archive")
    if f"{image.get('Os')}/{image.get('Architecture')}" != oci.platform:
        raise AssertionError("loaded Docker image platform differs from the OCI archive")
    descriptor = image.get("Descriptor")
    if descriptor is None:
        if image_id != oci.config_digest:
            raise AssertionError("classic Docker image ID differs from the OCI config digest")
        descriptor_projection = None
    else:
        expected_annotations = {
            "io.containerd.image.name": f"docker.io/library/{tag}",
            "org.opencontainers.image.created": labels["org.opencontainers.image.created"],
            "org.opencontainers.image.ref.name": tag.split(":", 1)[1],
        }
        if (
            not isinstance(descriptor, dict)
            or set(descriptor) != {"mediaType", "digest", "size", "annotations"}
            or descriptor.get("mediaType") != OCI_MANIFEST_MEDIA_TYPE
            or descriptor.get("digest") != oci.manifest_digest
            or descriptor.get("annotations") != expected_annotations
            or not isinstance(descriptor.get("size"), int)
            or not 1 <= descriptor["size"] <= MAX_JSON_BYTES
            or image_id != descriptor["digest"]
        ):
            raise AssertionError("containerd image descriptor differs from the OCI manifest")
        descriptor_projection = {
            "media_type": descriptor["mediaType"],
            "digest": descriptor["digest"],
            "bytes": descriptor["size"],
        }
    return image_id, descriptor_projection, labels


def _inspect_resource(command: tuple[str, ...]) -> dict[str, Any]:
    value = json.loads(run(command, capture=True).stdout)
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], dict):
        raise AssertionError("Docker resource inspection returned an invalid envelope")
    return value[0]


def assert_runtime_configuration(
    container: str, *, project: str, tag: str, image_id: str,
    image_labels: dict[str, str], compose_version: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    inspection = wait_for_container_health(container)
    config, host, state = (
        inspection.get("Config"), inspection.get("HostConfig"), inspection.get("State")
    )
    if not isinstance(config, dict) or not isinstance(host, dict) or not isinstance(state, dict):
        raise AssertionError("running container inspection is incomplete")
    if inspection.get("Image") != image_id or config.get("Image") != tag:
        raise AssertionError("running container does not use the exact loaded image")
    expected_config = {
        "User": EXPECTED_USER, "Entrypoint": EXPECTED_ENTRYPOINT, "Cmd": None,
        "Env": EXPECTED_ENVIRONMENT, "WorkingDir": EXPECTED_WORKING_DIRECTORY,
        "ExposedPorts": {EXPECTED_PORT: {}},
        "Healthcheck": EXPECTED_HEALTH_CONFIGURATION, "StopSignal": "SIGTERM",
        "StopTimeout": 35, "Volumes": None, "AttachStdin": False, "Tty": False,
        "OpenStdin": False, "StdinOnce": False,
    }
    if any(config.get(key) != value for key, value in expected_config.items()):
        raise AssertionError("running container command, environment or image boundary differs")
    normalised_labels = normalise_container_labels(
        config.get("Labels"), image_labels=image_labels, project=project,
        image_id=image_id, compose_version=compose_version,
    )
    expected_host = {
        "ReadonlyRootfs": True, "CapAdd": None, "CapDrop": ["ALL"],
        "SecurityOpt": ["no-new-privileges:true"], "Privileged": False,
        "PublishAllPorts": False, "AutoRemove": False, "PidsLimit": 64,
        "Memory": 256 * 1024 * 1024, "MemorySwap": 256 * 1024 * 1024,
        "MemoryReservation": 0, "NanoCpus": 500_000_000, "Tmpfs": EXPECTED_TMPFS,
        "Ulimits": [{"Name": "nofile", "Hard": 1024, "Soft": 1024}],
        "RestartPolicy": {"Name": "no", "MaximumRetryCount": 0},
        "LogConfig": {
            "Type": "json-file", "Config": {"max-file": "1", "max-size": "1m"},
        },
        "NetworkMode": f"{project}_offline",
        "PortBindings": {EXPECTED_PORT: [{"HostIp": HOST, "HostPort": str(PORT)}]},
    }
    if any(host.get(key) != value for key, value in expected_host.items()):
        raise AssertionError("running container privilege, resource or lifecycle controls differ")
    expected_binds = {
        f"{project}_evidence-ledger:{LEDGER_ROOT}:rw",
        f"{project}_reconciliation-index:{RECONCILIATION_ROOT}:rw",
    }
    binds = host.get("Binds") or []
    if set(binds) != expected_binds or len(binds) != 2:
        raise AssertionError("running container bind inventory differs")

    state_projection = {
        "status": state.get("Status"), "running": state.get("Running"),
        "paused": state.get("Paused"), "restarting": state.get("Restarting"),
        "oom_killed": state.get("OOMKilled"), "dead": state.get("Dead"),
        "exit_code": state.get("ExitCode"), "error": state.get("Error"),
        "health": state.get("Health", {}).get("Status"),
        "health_failing_streak": state.get("Health", {}).get("FailingStreak"),
    }
    if state_projection != {
        "status": "running", "running": True, "paused": False, "restarting": False,
        "oom_killed": False, "dead": False, "exit_code": 0, "error": "",
        "health": "healthy", "health_failing_streak": 0,
    }:
        raise AssertionError("running container health or process state differs")
    container_id = inspection.get("Id")
    if (not isinstance(container_id, str)
            or re.fullmatch(r"[0-9a-f]{64}", container_id) is None):
        raise AssertionError("running container identity is invalid")

    network_name = f"{project}_offline"
    network_settings = inspection.get("NetworkSettings")
    if not isinstance(network_settings, dict):
        raise AssertionError("gateway network settings are incomplete")
    networks = network_settings.get("Networks")
    if not isinstance(networks, dict) or set(networks) != {network_name}:
        raise AssertionError("gateway must join exactly the isolated Compose network")
    network = _inspect_resource(("docker", "network", "inspect", network_name))
    expected_network = {
        "Name": network_name, "Scope": "local", "Driver": "bridge",
        "Internal": True, "Attachable": False, "Ingress": False, "ConfigOnly": False,
    }
    if any(network.get(key) != value for key, value in expected_network.items()):
        raise AssertionError("gateway network is not the exact internal local bridge")
    network_members = network.get("Containers")
    if not isinstance(network_members, dict) or set(network_members) != {container_id}:
        raise AssertionError("gateway internal network has an unexpected member")
    if network_members[container_id].get("Name") != f"{project}-gateway-1":
        raise AssertionError("gateway internal network member identity differs")
    network_labels = normalise_resource_labels(
        network.get("Labels"), project=project, compose_version=compose_version,
        resource_kind="network", logical_name="offline",
    )

    mount_specs = {
        "evidence-ledger": LEDGER_ROOT,
        "reconciliation-index": RECONCILIATION_ROOT,
    }
    mounts = inspection.get("Mounts")
    if not isinstance(mounts, list) or len(mounts) != 2:
        raise AssertionError("gateway must have exactly two durable mounts")
    mount_by_destination = {mount.get("Destination"): mount for mount in mounts}
    if set(mount_by_destination) != set(mount_specs.values()):
        raise AssertionError("gateway durable mount destinations differ")
    volume_projection: list[dict[str, Any]] = []
    seen_sources: set[str] = set()
    for logical_name, destination in mount_specs.items():
        expected_name = f"{project}_{logical_name}"
        mount = mount_by_destination[destination]
        expected_mount = {
            "Type": "volume", "Name": expected_name, "Destination": destination,
            "Driver": "local", "Mode": "rw", "RW": True, "Propagation": "",
        }
        if any(mount.get(key) != value for key, value in expected_mount.items()):
            raise AssertionError("gateway durable mount differs from its closed shape")
        source = mount.get("Source")
        if not isinstance(source, str) or not source or source in seen_sources:
            raise AssertionError("gateway durable mount sources are not distinct")
        seen_sources.add(source)
        volume = _inspect_resource(("docker", "volume", "inspect", expected_name))
        if (volume.get("Name") != expected_name or volume.get("Driver") != "local"
                or volume.get("Scope") != "local" or volume.get("Options") is not None):
            raise AssertionError("gateway volume differs from its project-owned local shape")
        if volume.get("Mountpoint") != source:
            raise AssertionError("gateway mount source differs from the named local volume")
        volume_labels = normalise_resource_labels(
            volume.get("Labels"), project=project, compose_version=compose_version,
            resource_kind="volume", logical_name=logical_name,
        )
        volume_projection.append({
            "logical_name": logical_name, "destination": destination,
            "driver": "local", "scope": "local", "mount_read_write": True,
            "labels": volume_labels,
        })

    transport = classify_transport(network_settings.get("Ports"))
    if transport["mode"] == "container-loopback-internal-engine-fallback":
        assert_host_unreachable()
    identity = json_from_exec(
        container, "console.log(JSON.stringify({uid:process.getuid(),gid:process.getgid()}));"
    )
    if identity != {"uid": 65532, "gid": 65532}:
        raise AssertionError("gateway process does not use the fixed non-root identity")
    write_probe = run(
        ("docker", "exec", container, "node", "--input-type=module", "--eval",
         "import{writeFileSync}from'node:fs';writeFileSync('/app/write-probe','x');"),
        capture=True, check=False,
    )
    if write_probe.returncode == 0:
        raise AssertionError("gateway application filesystem accepted a write")
    egress = run(
        ("docker", "exec", container, "node", "--input-type=module", "--eval",
         "await fetch('http://192.0.2.1:9',{signal:AbortSignal.timeout(1000)})"
         ".then(()=>process.exit(2),()=>process.exit(0));"),
        capture=True, check=False, timeout=30,
    )
    if egress.returncode != 0:
        raise AssertionError("gateway offline network did not reject the egress probe")

    projection = {
        "container": {
            "container_id": container_id, "name": "gateway-1", "image_id": image_id,
            "user": EXPECTED_USER, "entrypoint": EXPECTED_ENTRYPOINT, "cmd": None,
            "environment": EXPECTED_ENVIRONMENT,
            "working_directory": EXPECTED_WORKING_DIRECTORY,
            "exposed_ports": [EXPECTED_PORT], "stop_signal": "SIGTERM",
            "stop_timeout_seconds": 35,
            "healthcheck": {
                "test": EXPECTED_HEALTHCHECK, "interval_ns": 10_000_000_000,
                "timeout_ns": 3_000_000_000, "start_period_ns": 5_000_000_000,
                "retries": 3,
            },
            "labels": normalised_labels, "read_only_root": True, "cap_add": [],
            "cap_drop": ["ALL"], "security_options": ["no-new-privileges:true"],
            "privileged": False, "publish_all_ports": False, "auto_remove": False,
            "tmpfs": EXPECTED_TMPFS, "nofile": {"soft": 1024, "hard": 1024},
            "restart": {"name": "no", "maximum_retry_count": 0},
            "logging": {
                "driver": "json-file", "options": {"max-file": "1", "max-size": "1m"},
            },
            "resources": {
                "cpus": 0.5, "memory_bytes": 256 * 1024 * 1024,
                "memory_swap_bytes": 256 * 1024 * 1024,
                "memory_reservation_bytes": 0, "pids": 64,
            },
            "state": state_projection,
        },
        "network": {
            "logical_name": "offline", "driver": "bridge", "scope": "local",
            "internal": True, "attachable": False, "ingress": False,
            "config_only": False, "member_count": 1, "labels": network_labels,
        },
        "volumes": volume_projection,
    }
    return projection, transport


def comparable_runtime(value: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(canonical_json_bytes(value))
    copy["container"].pop("container_id")
    return copy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/gateway/container-acceptance.json"),
    )
    args = parser.parse_args()
    archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    output = args.output if args.output.is_absolute() else ROOT / args.output
    compose_metadata = COMPOSE_FILE.lstat()
    if (
        stat.S_ISLNK(compose_metadata.st_mode)
        or not stat.S_ISREG(compose_metadata.st_mode)
        or compose_metadata.st_nlink != 1
    ):
        raise ValueError("Compose candidate must be one real regular file")
    compose_file_sha256 = sha256_file(COMPOSE_FILE)
    oci = inspect_oci_archive(archive)
    receipt_bytes = receipt_path.read_bytes()
    receipt = load_json_object(receipt_path)
    validate_schema_instance(RECEIPT_SCHEMA, receipt)
    if receipt_bytes != canonical_json_bytes(receipt):
        raise ValueError("gateway image receipt is not canonical JSON")
    source = receipt["source"]
    if (
        receipt["image"]["archive_sha256"] != oci.archive_sha256
        or receipt["image"]["archive_bytes"] != oci.archive_size
        or receipt["image"]["manifest_digest"] != oci.manifest_digest
        or receipt["image"]["config_digest"] != oci.config_digest
        or receipt["build"]["platform"] != oci.platform
    ):
        raise ValueError("container check archive differs from its image receipt")
    expected_source_labels = {
        "org.opencontainers.image.revision": source["revision"],
        "org.opencontainers.image.version": source["version"],
        "org.opencontainers.image.created": source["created"],
        "io.gis-ai-go.source-tree-clean": str(source["clean"]).lower(),
    }
    if any(oci.labels.get(key) != value for key, value in expected_source_labels.items()):
        raise ValueError("container check source differs from the exact OCI labels")
    tag = f"gis-ai-go-gateway:deploy-207-{source['revision'][:12]}"
    project = f"gis-ai-go-deploy207-{os.getpid()}"
    environment = dict(os.environ)
    environment["GIS_AI_GO_GATEWAY_IMAGE"] = tag
    environment["DOCKER_DEFAULT_PLATFORM"] = oci.platform
    phases: list[dict[str, Any]] = []
    checks: list[str] = []
    image_id = ""
    loaded_image_descriptor: dict[str, Any] | None = None
    restored_image_id = ""
    saved_sha256 = ""
    rendered_sha256 = ""
    runtime: dict[str, Any] = {}
    suspended_state: dict[str, Any] = {}
    storage_before: dict[str, Any] = {}
    transport: dict[str, Any] = {}
    boundary: dict[str, Any] = {}

    with record_phase(phases, "engine-identity"):
        engine = docker_versions()

    with tempfile.TemporaryDirectory(prefix="gis-ai-go-gateway-restore-") as temporary:
        saved = Path(temporary) / "gateway-image.tar"
        try:
            with record_phase(phases, "exact-oci-load"):
                loaded = load_docker_archive(archive)
                if tag not in loaded.stdout and tag not in loaded.stderr:
                    raise AssertionError("loaded OCI archive did not retain its exact local tag")
                image = _inspect_resource(("docker", "image", "inspect", tag))
                image_id, loaded_image_descriptor, image_labels = inspect_loaded_image(
                    image, tag, oci
                )
                checks.append("exact-oci-load")

            with record_phase(phases, "compose-render"):
                configuration = json.loads(
                    compose(
                        project, environment, "config", "--format", "json", capture=True
                    ).stdout
                )
                if not isinstance(configuration, dict):
                    raise AssertionError("rendered Compose configuration is not an object")
                rendered_sha256 = validate_rendered_compose(configuration, project, tag)
                checks.append("closed-compose-topology")

            with record_phase(phases, "compose-start-and-probe"):
                compose(project, environment, "up", "--detach", "--no-build",
                        "--pull", "never")
                container = compose(
                    project, environment, "ps", "--quiet", "gateway", capture=True
                ).stdout.strip()
                if re.fullmatch(r"[0-9a-f]{12,64}", container) is None:
                    raise AssertionError("Compose did not return one gateway container identity")
                runtime, transport = assert_runtime_configuration(
                    container, project=project, tag=tag, image_id=image_id,
                    image_labels=image_labels,
                    compose_version=engine["compose"]["version"],
                )
                http_container = None if transport["mode"] == "host-loopback" else container
                boundary = assert_http_boundary(
                    source["revision"], source["version"], container=http_container
                )
                if transport["mode"] == (
                    "container-loopback-internal-engine-fallback"
                ):
                    assert_host_unreachable()
                storage_before = storage_identity(container)
                if (storage_before["ledger"]["mode"] != 0o600
                        or storage_before["reconciliation"]["mode"] != 0o600):
                    raise AssertionError("gateway descriptor files are not mode 0600")
                if (storage_before["ledger_root"]["mode"] != 0o700
                        or storage_before["reconciliation_root"]["mode"] != 0o700):
                    raise AssertionError("gateway durable roots are not mode 0700")
                checks.extend([
                    "exact-image-runtime-identity", "closed-compose-labels",
                    "non-root-read-only-runtime", "loopback-only-internal-network",
                    "blocked-health-readiness", "zero-tools-routes-resources",
                    "private-disjoint-storage", "runtime-resource-bounds",
                ])

            with record_phase(phases, "restart-and-persistence"):
                compose(project, environment, "restart", "gateway")
                restart_inspection = wait_for_container_health(container)
                restart_transport = assert_transport_unchanged(
                    restart_inspection, transport
                )
                assert_http_boundary(
                    source["revision"], source["version"], container=http_container
                )
                if restart_transport["mode"] == (
                    "container-loopback-internal-engine-fallback"
                ):
                    assert_host_unreachable()
                if storage_identity(container) != storage_before:
                    raise AssertionError("gateway durable identities changed across restart")
                checks.append("restart-persistence")
                logs = compose(
                    project, environment, "logs", "--no-color", "gateway", capture=True
                ).stdout
                try:
                    assert_no_private_text(logs, "gateway logs")
                except ValueError:
                    raise AssertionError(
                        "gateway logs contain prohibited request or machine material"
                    ) from None
                checks.append("log-minimisation")

            with record_phase(phases, "service-suspension"):
                compose(project, environment, "stop", "gateway")
                suspended_state = assert_container_stopped(container)
                if transport["mode"] == "host-loopback":
                    assert_host_unreachable()
                checks.append("service-suspension")
                compose(project, environment, "down", "--remove-orphans")

            with record_phase(phases, "exact-image-restore"):
                run(
                    ("docker", "image", "save", "--output", str(saved), tag),
                    discard_output=True,
                )
                saved_sha256 = sha256_file(saved)
                run(("docker", "image", "rm", tag), discard_output=True)
                restored = load_docker_archive(saved)
                if tag not in restored.stdout and tag not in restored.stderr:
                    raise AssertionError("saved image did not restore its exact local tag")
                restored_image = _inspect_resource(("docker", "image", "inspect", tag))
                restored_image_id, restored_descriptor, restored_labels = inspect_loaded_image(
                    restored_image, tag, oci
                )
                if (
                    restored_image_id != image_id
                    or restored_descriptor != loaded_image_descriptor
                    or restored_labels != image_labels
                ):
                    raise AssertionError("saved image restored a different exact identity")
                compose(project, environment, "up", "--detach", "--no-build",
                        "--pull", "never")
                container = compose(
                    project, environment, "ps", "--quiet", "gateway", capture=True
                ).stdout.strip()
                restored_runtime, restored_transport = assert_runtime_configuration(
                    container, project=project, tag=tag, image_id=image_id,
                    image_labels=image_labels,
                    compose_version=engine["compose"]["version"],
                )
                if comparable_runtime(restored_runtime) != comparable_runtime(runtime):
                    raise AssertionError("gateway runtime shape changed after exact-image restore")
                if restored_transport != transport:
                    raise AssertionError("gateway transport changed after exact-image restore")
                http_container = None if transport["mode"] == "host-loopback" else container
                assert_http_boundary(
                    source["revision"], source["version"], container=http_container
                )
                if restored_transport["mode"] == (
                    "container-loopback-internal-engine-fallback"
                ):
                    assert_host_unreachable()
                if storage_identity(container) != storage_before:
                    raise AssertionError(
                        "gateway durable identities changed after exact-image restore"
                    )
                checks.append("exact-image-restore")
        finally:
            compose(
                project, environment, "down", "--volumes", "--remove-orphans",
                capture=True, check=False,
            )

    checks.append("closed-acceptance-receipt")
    if checks != EXPECTED_CHECKS:
        raise AssertionError("gateway container checks did not complete in reviewed order")
    if sha256_file(COMPOSE_FILE) != compose_file_sha256:
        raise AssertionError("Compose candidate changed during its acceptance rehearsal")
    evidence = {
        "schema": "gis-ai-go.gateway-container-acceptance.v1",
        "classification": "local-mechanism-rehearsal",
        "source": {
            "repository": source["repository"], "revision": source["revision"],
            "version": source["version"], "created": source["created"],
            "source_date_epoch": source["source_date_epoch"],
            "tree_clean": source["clean"],
        },
        "image": {
            "archive_sha256": oci.archive_sha256,
            "manifest_digest": oci.manifest_digest,
            "config_digest": oci.config_digest, "platform": oci.platform, "tag": tag,
            "loaded_image_descriptor": loaded_image_descriptor,
            "loaded_image_id": image_id, "restored_image_id": restored_image_id,
            "saved_archive_sha256": saved_sha256,
        },
        "compose": {
            "file": COMPOSE_RELATIVE, "file_sha256": compose_file_sha256,
            "rendered_sha256": rendered_sha256,
        },
        "engine": engine, "phases": phases,
        "runtime": {**runtime, "suspended_state": suspended_state},
        "transport": transport,
        "storage": {**storage_before, "distinct_volumes": True},
        "boundary": boundary, "checks": checks,
        "claims": {
            "public_deployment": False, "production_activation": False,
            "live_provider_call": False, "production_rollback": False,
            "static_explorer_dependency": False,
        },
    }
    canonical = canonical_json_bytes(evidence)
    if len(canonical) > MAX_JSON_BYTES:
        raise ValueError("gateway container acceptance receipt exceeds its byte bound")
    assert_no_private_json(evidence, "gateway container acceptance receipt")
    assert_no_private_text(canonical, "gateway container acceptance receipt")
    validate_schema_instance(ACCEPTANCE_SCHEMA, evidence)
    if canonical_json_bytes(json.loads(canonical)) != canonical:
        raise AssertionError("gateway container acceptance receipt is not canonical JSON")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical)
    print(
        "Gateway container passed closed Compose, runtime, persistence, suspension "
        "and exact-image restore acceptance."
    )


if __name__ == "__main__":
    main()
