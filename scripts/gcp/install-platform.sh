#!/usr/bin/env bash
# BDUK operator entrypoint. Requires the reviewed repository/package, not curl | bash.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 - "$SCRIPT_DIR" "$@" <<'PY'
"""Orchestrate the existing approval-bound lifecycle; never manufacture approval."""
import argparse
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid


PROFILE = "bduk-sandpit-network-private"
DEFAULT_CONFIG = "artifacts/gcp/bduk-sandpit.json"
COMMANDS = ("init", "inputs", "review", "install", "preflight", "prepare", "plan",
            "apply", "connect", "verify", "status", "package-approval", "rollback", "destroy")


class Installer:
    def __init__(self, script_dir, config):
        self.root = Path(script_dir).resolve().parents[1]
        spec = importlib.util.spec_from_file_location("platform_gcp_lifecycle", self.root / "scripts/gcp/lifecycle.py")
        self.gcp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gcp)
        path = Path(config)
        self.config_path = path if path.is_absolute() else self.root / path
        self.steps = []
        self.run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]

    def private_path(self):
        # Private inputs belong outside the tracked source and must not redirect
        # writes through a symlink. Do not read credential files to discover values.
        base = self.root / "artifacts/gcp"
        path = self.config_path.absolute()
        if ".." in path.parts:
            raise self.gcp.GateError("Use a direct private path under artifacts/gcp")
        try:
            path.relative_to(base)
        except ValueError as error:
            raise self.gcp.GateError("Private configuration must be under artifacts/gcp") from error
        for item in (path, *path.parents):
            if item.is_symlink():
                raise self.gcp.GateError("Private configuration path contains a symlink")
            if item == self.root:
                break
        return path

    def initialise(self):
        path = self.private_path()
        config = self.gcp.load_config(self.root / "infra/gcp/environments/bduk-sandpit/config.example.json")
        config["_status"] = "Unapproved BDUK configuration; platform inputs required; no credentials or cloud approval."
        # New store identity is a local draft, not permission to initialise an
        # existing evidence store. Explicit provisioning still checks approval.
        config["state"]["store_nonce"] = uuid.uuid4().hex
        config["state"]["created_at"] = self.gcp.timestamp()
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root,
                                  capture_output=True, text=True, check=False)
        if revision.returncode == 0 and re.fullmatch(r"[0-9a-f]{40,64}", revision.stdout.strip()):
            config["state"]["software_revision"] = revision.stdout.strip()
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # O_EXCL also refuses an existing file; never truncate owner work.
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, "w") as stream:
            stream.write(json.dumps(config, indent=2) + "\n")
        return {"status": "DRAFT_CREATED", "config": str(path), "profile": PROFILE,
                "next": "Fill approved platform inputs; run inputs, then review. No secret values."}

    def load(self):
        path = self.private_path()
        if path.stat().st_mode & 0o077:
            raise self.gcp.GateError("Configuration must be owner-private: chmod 600 the selected file")
        config = self.gcp.load_config(path)
        if config["profile"] != PROFILE:
            raise self.gcp.GateError("This installer requires the BDUK sandpit profile; personal authority cannot be reused")
        if config["network"]["create_access_vm"] or config["network"]["access_vm_on_demand"]:
            raise self.gcp.GateError("BDUK must use the approved platform network, without a personal access VM")
        if config["network"]["access_mode"] != "platform-approved-private-network":
            raise self.gcp.GateError("BDUK access_mode must be platform-approved-private-network")
        self.lifecycle = self.gcp.Lifecycle(path)
        self.evidence = self.lifecycle.directory / "installer-runs" / self.run_id
        self.evidence.mkdir(parents=True, mode=0o700)
        return config

    def step(self, action, *extra):
        command = [str(self.root / "scripts/gcp/deploy.sh"), "--config", str(self.config_path), action, *extra]
        try:
            completed = subprocess.run(command, cwd=self.root, capture_output=True, text=True,
                                       timeout=5400 if action == "prepare" else 2400, check=False)
            observed = {"exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
        except (OSError, subprocess.TimeoutExpired) as error:
            observed = {"exit_code": 2, "stdout": "", "stderr": str(error)}
        path = self.evidence / f"{len(self.steps):02d}-{action}.json"
        self.gcp.write_json(path, observed)
        code = observed["exit_code"]
        try:
            result = json.loads(observed["stdout"])
        except ValueError:
            result = {}
        # The underlying status CLI can exit zero while reporting BLOCKED.
        if code == 0 and result.get("status") == "BLOCKED":
            code = 2
        if code == 0 and action == "prepare" and self.lifecycle.prepared_status()["status"] != "PASS":
            code = 2
        self.steps.append({"action": action, "exit_code": code, "evidence": str(path)})
        print(f"{action}: {'PASS' if code == 0 else 'BLOCKED'}; private evidence: {path}", file=sys.stderr)
        return code

    def review(self, skip_prepare=False):
        codes = [self.step("preflight")]
        if not skip_prepare:
            prepared = self.lifecycle.prepared_status()
            if prepared["status"] == "PASS":
                self.steps.append({"action": "reuse-verified-preparation", "exit_code": 0})
            elif any((self.lifecycle.directory / name).exists() for name in ("prepared", "image.json", "gateway.oci.tar")):
                # Preserve incomplete/stale/approved material; do not delete it
                # to make a new build pass or break a historical rollback.
                codes.append(2)
                self.steps.append({"action": "prepare", "exit_code": 2,
                                   "reason": "Existing unverified preparation preserved; use a new reviewed configuration/release scope"})
            else:
                codes.append(self.step("prepare"))
        codes.append(self.step("plan"))
        # Missing login or a failed local build must not prevent the independent
        # platform package. No review operation invokes apply or writes approval.
        codes.append(self.step("package-approval"))
        return 0 if all(code == 0 for code in codes) else 2

    def finish(self, code):
        result = {"status": "PASS" if code == 0 else "BLOCKED", "profile": PROFILE,
                  "steps": self.steps, "evidence": str(self.evidence / "summary.json"),
                  "acceptance": "Consult verification.json; script completion is not BDUK acceptance",
                  "approval_created": False}
        self.gcp.write_json(self.evidence / "summary.json", result)
        return result


def main(script_dir, argv=None):
    parser = argparse.ArgumentParser(description="Install GIS AI GO on an approved BDUK GCP sandpit; default is non-mutating review.")
    parser.add_argument("command", choices=COMMANDS, nargs="?", default="review")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="owner-private config under artifacts/gcp")
    parser.add_argument("--approved-plan", help="existing exact 24-hex approved plan ID; never generated here")
    parser.add_argument("--release", help="existing recorded compatible release for rollback")
    parser.add_argument("--destroy", action="store_true", help="request a read-only destructive plan")
    parser.add_argument("--skip-prepare", action="store_true", help="review existing/absent material without a local image build")
    args = parser.parse_args(argv)
    if args.command in ("install", "apply", "destroy") and not re.fullmatch(r"[0-9a-f]{24}", args.approved_plan or ""):
        parser.error("install/apply/destroy require --approved-plan from the existing reviewed approval record")
    if args.command == "rollback" and not re.fullmatch(r"[A-Za-z0-9._-]{1,100}", args.release or ""):
        parser.error("rollback requires --release from an existing approved compatible release")
    if args.destroy and args.command != "plan":
        parser.error("--destroy is only valid with plan")
    if args.skip_prepare and args.command != "review":
        parser.error("--skip-prepare is only valid with review")
    # Own all newly created private config, command results and local state.
    os.umask(0o077)
    installer = Installer(script_dir, args.config)
    try:
        if args.command == "init":
            print(json.dumps(installer.initialise(), indent=2))
            return 0
        config = installer.load()
        if args.command == "inputs":
            missing = installer.gcp.unresolved(config)
            print(json.dumps({"status": "BLOCKED" if missing else "INPUTS_FILLED_NOT_APPROVED", "required_inputs": missing}, indent=2))
            return 2 if missing else 0
        if args.command == "review":
            code = installer.review(args.skip_prepare)
        elif args.command in ("install", "apply"):
            # Approval verification, identity readback and bound saved plan apply
            # remain in the existing lifecycle. Never reprepare/replan first.
            code = installer.step("apply", "--approved-plan", args.approved_plan)
            if code == 0:
                verification = installer.step("verify")
                status = installer.step("status")
                code = 0 if verification == status == 0 else 2
        elif args.command == "destroy":
            code = installer.step("destroy", "--approved-plan", args.approved_plan)
        elif args.command == "rollback":
            code = installer.step("rollback", "--release", args.release)
        elif args.command == "connect":
            raise installer.gcp.GateError("Join the approved BDUK private network; this profile has no personal tunnel VM")
        else:
            code = installer.step(args.command, *( ["--destroy"] if args.destroy else [] ))
        print(json.dumps(installer.finish(code), indent=2))
        return code
    except (installer.gcp.GateError, OSError, ValueError) as error:
        # Config and lifecycle errors contain field names/paths, not secret values.
        print(json.dumps({"status": "BLOCKED", "reason": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2:]))
PY
