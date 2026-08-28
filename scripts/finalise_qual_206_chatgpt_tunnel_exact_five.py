#!/usr/bin/env python3
"""Finalise allowlisted private metadata for a completed ChatGPT tunnel capture."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Any

import verify_qual_206_chatgpt_tunnel_exact_five as verifier


def private_file_facts(path: Path, *, maximum: int, label: str) -> dict[str, Any]:
    raw = verifier.read_private(path, maximum=maximum, label=label)
    return {
        "name": path.name,
        "bytes": len(raw),
        "sha256": verifier.sha256_bytes(raw),
        "mode": "0600",
    }


def build_manifest(arguments: argparse.Namespace) -> dict[str, Any]:
    private_root = arguments.private_root
    node_path = verifier.locate_verified_node(arguments.node)
    pnpm_path = Path(verifier.require_explicit_pnpm_path(arguments.pnpm))
    verifier.require_directory(private_root, label="private root")
    if (private_root.lstat().st_mode & 0o777) != 0o700:
        verifier.fail("private root mode is not 0700")
    if (private_root / "run-manifest.json").exists():
        verifier.fail("private run manifest already exists")
    claim_raw = verifier.read_private(
        private_root / verifier.CLAIM_NAME,
        maximum=2_048,
        label="global exact-five claim",
    )
    claim = verifier.strict_canonical_object(claim_raw, label="global exact-five claim")
    session_names = sorted(
        name for name in os.listdir(private_root) if re.fullmatch(r"session-[1-8]", name)
    )
    if session_names != [f"session-{index}" for index in range(1, len(session_names) + 1)]:
        verifier.fail("capture sessions are not a contiguous session-1 to session-8 set")
    expected_names = {
        verifier.CLAIM_NAME,
        verifier.STATUS_BEFORE_NAME,
        verifier.STATUS_AFTER_NAME,
        verifier.STATUS_STOPPED_NAME,
        *session_names,
    }
    if set(os.listdir(private_root)) != expected_names:
        verifier.fail("private root contains material outside the finaliser allowlist")
    commit = verifier._host_call(verifier.host002.git_output, "rev-parse", "HEAD")
    tree = verifier._host_call(verifier.host002.git_output, "rev-parse", "HEAD^{tree}")
    source = {
        "commit": commit,
        "tree": tree,
        "repository_origin": verifier.host002.CANONICAL_REPOSITORY_ORIGIN,
        "local_origin_main_match": True,
        "clean_detached_checkout": True,
        "protected_main_verification": "external-publication-gate",
    }
    verifier.verify_source({"source": source})
    runtime = verifier.independently_reproduce_runtime_closure(
        commit,
        node_path=node_path,
        pnpm_path=pnpm_path,
    )
    manifest = {
        "schema": "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-private-run.v1",
        "run_id": claim.get("run_id"),
        "scenario": verifier.SCENARIO,
        "source": source,
        "runtime": runtime,
        "tunnel_client": {
            "version": "0.0.13",
            "build_sha": "4b5267f823be0b046bb883aacb51603cfde3a0ea",
            "reported_version": verifier.TUNNEL_CLIENT_VERSION,
            "binary_bytes": verifier.TUNNEL_CLIENT_BYTES,
            "binary_sha256": verifier.TUNNEL_CLIENT_SHA256,
            "archive_sha256": (
                "15abf165f06050af642c948ba6bd6c905191dc5420a9422dadde2b49d892e2c6"
            ),
            "sha256sums_sha256": (
                "e6495395e8f5d952b0edc34a0b552426e38472973a7602f94b3868fbcd9aceb4"
            ),
            "release_url": (
                "https://github.com/openai/tunnel-client/releases/tag/v0.0.13"
            ),
            "release_verified": True,
        },
        "tunnel": {
            "local_alias": "gis-ai-go-v0-2-exact-five-v1",
            "remote_name": "gis-ai-go-v0-2-interoperability",
            "remote_id": "tunnel_6a873e7214308191bfe27240c1c03f68",
            "connection_kind": "openai-secure-tunnel",
            "authenticated": True,
            "local_mcp_child_transport": "stdio",
            "direct_public_streamable_http_tls": False,
        },
        "host": {
            "name": "ChatGPT",
            "app_name": "GIS AI GO v0.2 interoperability",
            "app_id": "asdk_app_6a873f853628819184bccb4a9b961576",
            "app_version_id": arguments.app_version_id,
            "displayed_model": arguments.displayed_model,
            "displayed_model_operator_observed": True,
            "conversation_id_sha256": arguments.conversation_id_sha256,
        },
        "execution": {
            "started_at": arguments.started_at,
            "finished_at": arguments.finished_at,
            "exit_code": None,
            "signal": None,
            "classification": "complete",
            "session_count": len(session_names),
        },
        "private_files": {
            "claim": private_file_facts(
                private_root / verifier.CLAIM_NAME,
                maximum=2_048,
                label="global exact-five claim",
            ),
            "status_before": private_file_facts(
                private_root / verifier.STATUS_BEFORE_NAME,
                maximum=65_536,
                label="tunnel status before",
            ),
            "status_after": private_file_facts(
                private_root / verifier.STATUS_AFTER_NAME,
                maximum=65_536,
                label="tunnel status after",
            ),
            "status_stopped": private_file_facts(
                private_root / verifier.STATUS_STOPPED_NAME,
                maximum=65_536,
                label="tunnel status stopped",
            ),
        },
        "isolation": {
            "private_root_mode": "0700",
            "private_file_mode": "0600",
            "observer_credentials_observed": False,
            "mcp_child_recognised_credentials_forwarded": False,
            "mcp_child_network_access_allowed": False,
            "mcp_child_network_sandbox": verifier.NETWORK_SANDBOX,
            "provider_egress_guard_ready": True,
            "guarded_live_provider_api_invocations": 0,
            "raw_material_published": False,
        },
        "claims": dict(verifier.EXPECTED_CLAIMS),
    }
    verifier.validate(
        verifier.schema_validator(verifier.PRIVATE_SCHEMA),
        manifest,
        label="finalised private run manifest",
    )
    if claim.get("source_commit") != commit:
        verifier.fail("global claim is not bound to the current source commit")
    before_raw = verifier.read_private(
        private_root / verifier.STATUS_BEFORE_NAME,
        maximum=65_536,
        label="tunnel status before",
    )
    after_raw = verifier.read_private(
        private_root / verifier.STATUS_AFTER_NAME,
        maximum=65_536,
        label="tunnel status after",
    )
    stopped_raw = verifier.read_private(
        private_root / verifier.STATUS_STOPPED_NAME,
        maximum=65_536,
        label="tunnel status stopped",
    )
    verifier.verify_statuses(
        before_raw,
        after_raw,
        stopped_raw,
        manifest,
        verifier.schema_validator(verifier.STATUS_SCHEMA),
    )
    return manifest


def write_manifest(private_root: Path, manifest: dict[str, Any]) -> None:
    output = private_root / "run-manifest.json"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(output, flags, 0o600)
    try:
        raw = verifier.canonical_line(manifest)
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                verifier.fail("private run-manifest write made no progress")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    if (output.lstat().st_mode & 0o777) != 0o600:
        verifier.fail("finalised private run manifest mode is not 0600")
    directory_descriptor = os.open(private_root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_descriptor)
    finally:
        os.close(directory_descriptor)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Finalise the closed private metadata for a completed tunnel capture."
    )
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--node", required=True, type=Path)
    parser.add_argument("--pnpm", required=True, type=Path)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--finished-at", required=True)
    parser.add_argument("--displayed-model", required=True)
    parser.add_argument("--app-version-id", required=True)
    parser.add_argument("--conversation-id-sha256", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        manifest = build_manifest(arguments)
        write_manifest(arguments.private_root, manifest)
    except (OSError, verifier.TunnelExactFiveVerificationError) as error:
        print(f"QUAL-206 private capture finalisation failed: {error}", file=sys.stderr)
        return 1
    print("QUAL-206 private ChatGPT tunnel capture finalised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
