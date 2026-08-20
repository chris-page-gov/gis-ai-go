#!/usr/bin/env python3
"""Build and exercise the private execution image under its runtime controls."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "gis-ai-go-execution:exec-202-acceptance"

CONTAINER_CHECK = r"""
import json
import os
import threading
import urllib.request

from gis_ai_go_execution import create_http_server

assert os.getuid() == 65532, os.getuid()
try:
    with open('/app/write-probe', 'w', encoding='utf-8') as handle:
        handle.write('unexpected')
except OSError:
    pass
else:
    raise AssertionError('runtime application files are writable')

server = create_http_server(port=0)
assert server.server_address[0] == '127.0.0.1', server.server_address
worker = threading.Thread(target=server.serve_forever, daemon=True)
worker.start()
try:
    port = server.server_address[1]
    for route, expected in (
        ('/internal/health', 'ok'),
        ('/internal/readiness', 'ready'),
    ):
        with urllib.request.urlopen(f'http://127.0.0.1:{port}{route}', timeout=2) as response:
            value = json.load(response)
        assert value['status'] == expected, value
        assert value['private'] is True, value
        assert value['live_provider_calls'] is False, value
    with urllib.request.urlopen(
        f'http://127.0.0.1:{port}/internal/openapi.json', timeout=2
    ) as response:
        openapi = json.load(response)
    assert openapi['openapi'] == '3.1.0', openapi
finally:
    server.shutdown()
    server.server_close()
    worker.join(timeout=2)
"""


def run(*arguments: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture,
    )


def main() -> None:
    run(
        "docker",
        "build",
        "--file",
        "services/geo-execution/Containerfile",
        "--tag",
        IMAGE,
        ".",
    )
    inspection = json.loads(run("docker", "image", "inspect", IMAGE, capture=True).stdout)[0]
    config = inspection["Config"]
    if config.get("User") != "65532:65532":
        raise AssertionError("execution image must run as the fixed non-root identity")
    if config.get("ExposedPorts"):
        raise AssertionError("execution image must not expose a public port")
    if config.get("Entrypoint") != ["python", "-m", "gis_ai_go_execution"]:
        raise AssertionError("execution image entry point differs from the reviewed module")

    run(
        "docker",
        "run",
        "--rm",
        "--read-only",
        "--network",
        "none",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--pids-limit",
        "64",
        "--memory",
        "128m",
        "--cpus",
        "0.5",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=1m",
        "--entrypoint",
        "python",
        IMAGE,
        "-c",
        CONTAINER_CHECK,
    )
    print(
        "Execution container passed non-root, read-only, network-none and private "
        "health/readiness/OpenAPI acceptance."
    )


if __name__ == "__main__":
    main()
