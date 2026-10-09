#!/usr/bin/env python3
"""Private GCP pilot lifecycle. Cloud reads are separated from approved mutations.

All subprocesses use argument arrays; private config, state and cloud evidence stay
under ignored artifacts. No credential value is persisted. The approval file is
an owner/platform record, never automatically completed by this program.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import urllib.parse
import zipfile
import uuid

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "infra/gcp/config.schema.json"
PHASES = ("foundation", "service")
COMMANDS = ("preflight", "prepare", "plan", "apply", "connect", "verify", "status", "package-approval", "rollback", "destroy")
TIMEOUT = 180
SOURCE_FILE_LIMIT = 64 * 1024 * 1024
SOURCE_TOTAL_LIMIT = 4 * 1024 * 1024 * 1024
SOURCE_FILE_COUNT_LIMIT = 100000


class GateError(RuntimeError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def plan_identity(plan):
    return digest({key: value for key, value in plan.items() if key not in ("created_at", "facts", "plan_id")})[:24]


def file_digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def _source_name(name):
    """A Git name is a lexical repository path, never a resolved alias."""
    name = str(name)
    path = Path(name)
    if not name or "\0" in name or path.is_absolute() or any(part in ("", ".", "..") for part in name.split("/")) or path.as_posix() != name:
        raise GateError("Source inventory contains an invalid repository path")
    return name


def _open_regular_source(name, root):
    """Open every component without following links, including the root."""
    name = _source_name(name)
    descriptors = []
    try:
        descriptors.append(os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))
        for part in Path(name).parts[:-1]:
            descriptors.append(os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptors[-1]))
        directories = [(os.fstat(fd).st_dev, os.fstat(fd).st_ino) for fd in descriptors]
        descriptors.append(os.open(Path(name).name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptors[-1]))
        metadata = os.fstat(descriptors[-1])
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise GateError("Source must be a regular file with one link: " + name)
        return descriptors, directories, metadata
    except (OSError, GateError) as error:
        for fd in reversed(descriptors):
            os.close(fd)
        if isinstance(error, GateError):
            raise
        raise GateError("Source is missing, linked or has an invalid ancestor: " + name) from error


def _file_identity(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns,
            metadata.st_ctime_ns, metadata.st_mode, metadata.st_nlink)


def read_source_file(name, *, root=None, expected=None, include_bytes=True, validate_only=False, limit=SOURCE_FILE_LIMIT):
    """Read bounded stable bytes from a regular repository-contained file.

    Directory descriptors prevent traversal through parent links. Reopening the
    lexical path after the read detects replacement of a file or an ancestor.
    The same reader is used for inventory, policy, IaC and review ZIP payloads.
    """
    root = ROOT if root is None else Path(root)
    name = _source_name(name)
    descriptors, directories, before = _open_regular_source(name, root)
    try:
        if before.st_size > limit:
            raise GateError("Source exceeds its bounded file limit: " + name)
        sha = hashlib.sha256()
        content = bytearray() if include_bytes else None
        count = 0
        if not validate_only:
            while block := os.read(descriptors[-1], 1024 * 1024):
                count += len(block)
                if count > limit:
                    raise GateError("Source exceeds its bounded file limit: " + name)
                sha.update(block)
                if content is not None:
                    content.extend(block)
        after = os.fstat(descriptors[-1])
        if _file_identity(before) != _file_identity(after) or (not validate_only and count != before.st_size):
            raise GateError("Source changed during its bounded read: " + name)
        reopened, current_directories, current = _open_regular_source(name, root)
        try:
            if directories != current_directories or _file_identity(before) != _file_identity(current):
                raise GateError("Source or its ancestor changed during its bounded read: " + name)
        finally:
            for fd in reversed(reopened):
                os.close(fd)
        entry = {"path": name, "sha256": sha.hexdigest(), "bytes": count, "mode": stat.S_IMODE(before.st_mode)}
        if expected is not None and entry != expected:
            raise GateError("Admitted source bytes or mode changed: " + name)
        return entry, bytes(content) if content is not None else None
    finally:
        for fd in reversed(descriptors):
            os.close(fd)


def source_path_name(path):
    path = Path(path)
    if not path.is_absolute():
        return _source_name(path.as_posix())
    try:
        return _source_name(path.relative_to(ROOT).as_posix())
    except ValueError as error:
        raise GateError("Reviewed source must be contained in the repository") from error


def validate_prepared_sources(manifest, source):
    admitted = {entry["path"]: entry for entry in source["files"]}
    for declared in manifest.get("sourceFiles", []):
        name = _source_name(declared["path"])
        if name not in admitted:
            raise GateError("Prepared build source is outside the admitted Git inventory: " + name)
        actual, _ = read_source_file(name, expected=admitted[name], include_bytes=False)
        if declared.get("sha256") != actual["sha256"] or ("bytes" in declared and declared["bytes"] != actual["bytes"]):
            raise GateError("Prepared build source changed: " + name)


def _directory_descriptors(root, name, *, create=False):
    descriptors = []
    try:
        descriptors.append(os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))
        for part in Path(_source_name(name)).parts:
            if create:
                try:
                    os.mkdir(part, mode=0o700, dir_fd=descriptors[-1])
                except FileExistsError:
                    pass
            descriptors.append(os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptors[-1]))
        return descriptors
    except (OSError, GateError) as error:
        for fd in reversed(descriptors):
            os.close(fd)
        if isinstance(error, GateError):
            raise
        raise GateError("IaC destination has a linked or invalid ancestor") from error


def write_admitted_source(root, name, content, mode):
    """Replace only a normal destination leaf; never follow a target alias."""
    name = _source_name(name)
    parent = Path(name).parent.as_posix()
    descriptors = _directory_descriptors(root, parent, create=True) if parent != "." else [os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)]
    temporary = ".source-" + uuid.uuid4().hex + ".tmp"
    leaf = Path(name).name
    try:
        try:
            existing = os.stat(leaf, dir_fd=descriptors[-1], follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None and (not stat.S_ISREG(existing.st_mode) or existing.st_nlink != 1):
            raise GateError("IaC destination is linked or is not a regular file: " + name)
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=descriptors[-1])
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(content)
                stream.flush()
                os.fchmod(stream.fileno(), mode)
                os.fsync(stream.fileno())
            os.replace(temporary, leaf, src_dir_fd=descriptors[-1], dst_dir_fd=descriptors[-1])
            os.fsync(descriptors[-1])
        finally:
            try:
                os.unlink(temporary, dir_fd=descriptors[-1])
            except FileNotFoundError:
                pass
    finally:
        for fd in reversed(descriptors):
            os.close(fd)


def private_source_name(name):
    parts = Path(name).parts
    leaf = parts[-1]
    return (any(part in (".terraform", "__pycache__", "node_modules", "artifacts", "inputs") for part in parts)
            or leaf == ".env" or leaf.startswith(".env.") or leaf.endswith(".env")
            or bool(re.search(r"(?:\.tfstate|\.tfplan)(?:\.|$)|\.private\.json$|(?:^|[-.])(?:credentials|credential|secrets?)(?:\.|$)", leaf)))


def terraform_input_name(name):
    return name.endswith((".tf", ".tf.json", ".tfvars", ".tfvars.json")) or Path(name).name == ".terraform.lock.hcl"


def directory_manifest(path):
    path = Path(path)
    if not path.is_dir():
        return []
    files = []
    for item in sorted(path.rglob("*")):
        if item.is_symlink():
            raise GateError("Prepared context contains a symlink")
        if item.is_file():
            files.append({"path": item.relative_to(path).as_posix(), "sha256": file_digest(item), "bytes": item.stat().st_size})
    return files


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.chmod(0o600)
    temporary.replace(path)


def now():
    return dt.datetime.now(dt.timezone.utc)


def timestamp():
    return now().isoformat()


def execute(args, *, cwd=ROOT, timeout=TIMEOUT, input_text=None, env=None):
    try:
        result = subprocess.run([str(a) for a in args], cwd=cwd, text=True, input=input_text,
                                capture_output=True, timeout=timeout, check=False, env=env)
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {"status": "BLOCKED", "exit_code": None, "reason": str(error), "stdout": "", "stderr": ""}
    return {"status": "PASS" if result.returncode == 0 else "BLOCKED", "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def require(result, purpose):
    if result["status"] != "PASS":
        # Error text is private; never print an entire cloud response/configuration.
        raise GateError(f"{purpose}: {result['status']} (exit {result.get('exit_code')}); inspect the private command evidence")
    return result["stdout"]


def validate_schema(value, schema, path="config"):
    """Small fail-closed validator for the checked-in schema; no pip/network dependency."""
    if "anyOf" in schema:
        for alternative in schema["anyOf"]:
            try:
                validate_schema(value, alternative, path)
                return
            except GateError:
                pass
        raise GateError(f"{path}: does not match an allowed shape")
    if "const" in schema and value != schema["const"]:
        raise GateError(f"{path}: required constant differs")
    if "enum" in schema and value not in schema["enum"]:
        raise GateError(f"{path}: unsupported value")
    types = schema.get("type", [])
    types = [types] if isinstance(types, str) else types
    actual = "null" if value is None else "boolean" if isinstance(value, bool) else "integer" if isinstance(value, int) else "number" if isinstance(value, float) else "string" if isinstance(value, str) else "array" if isinstance(value, list) else "object" if isinstance(value, dict) else "invalid"
    if types and actual not in types and not (actual == "integer" and "number" in types):
        raise GateError(f"{path}: expected {'/'.join(types)}")
    if value is None:
        return
    if isinstance(value, dict):
        if len(value) > schema.get("maxProperties", sys.maxsize):
            raise GateError(f"{path}: too many properties")
        fields = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(fields):
            raise GateError(f"{path}: unknown fields {sorted(set(value) - set(fields))}")
        for name in schema.get("required", []):
            if name not in value:
                raise GateError(f"{path}.{name}: required")
        for name, child in value.items():
            if name in fields:
                validate_schema(child, fields[name], f"{path}.{name}")
            elif isinstance(schema.get("additionalProperties"), dict):
                validate_schema(child, schema["additionalProperties"], f"{path}.{name}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise GateError(f"{path}: too few items")
        if len(value) > schema.get("maxItems", sys.maxsize):
            raise GateError(f"{path}: too many items")
        if schema.get("uniqueItems") and len({digest(item) for item in value}) != len(value):
            raise GateError(f"{path}: duplicate items")
        for index, item in enumerate(value):
            validate_schema(item, schema.get("items", {}), f"{path}[{index}]")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or (schema.get("pattern") and not re.search(schema["pattern"], value)):
            raise GateError(f"{path}: invalid string")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", float("-inf")) or value > schema.get("maximum", float("inf")):
            raise GateError(f"{path}: out of bounds")


def load_config(path):
    config = read_json(path)
    validate_schema(config, read_json(SCHEMA))
    return config


def concrete_runtime_policy():
    """Read the deliberately static reviewed grants; fail if source shape changes."""
    identity = read_source_file("apps/mcp-gateway/src/gcp-identity.ts")[1].decode()
    match = re.search(r"const GRANTS:[\s\S]*?Object\.freeze\(\{([\s\S]*?)\n\}\);", identity)
    if not match:
        raise GateError("Static application grants could not be inspected")
    roles = {}
    for quoted, bare, values in re.findall(r'(?:"([^\"]+)"|([a-zA-Z_][a-zA-Z0-9_-]*)):\s*(\[[^\]]+\])', match.group(1)):
        roles[quoted or bare] = json.loads(values)
    mcp = read_source_file("apps/mcp-gateway/src/gcp-mcp.ts")[1].decode()
    match = re.search(r"GCP_TOOL_CAPABILITIES:[\s\S]*?Object\.freeze\(\{([\s\S]*?)\n\}\);", mcp)
    if not match or len(roles) != 5:
        raise GateError("Static tool capability mapping could not be inspected")
    tools = dict(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*):\s*"([^\"]+)"', match.group(1)))
    if len(tools) != 6:
        raise GateError("The reviewed custom MCP tool inventory changed")
    return {"schema": "gis-ai-go.gcp-policy.v1", "policy_release": "gis-ai-go.gcp-public-metadata.v1", "roles": roles,
            "tool_capabilities": tools, "constraints": {"default_decision": "deny", "classification": "public-metadata", "environment": "exact-match", "evidence_ownership": "principal-scope", "token_expiry": "enforced", "unknown_roles": "deny"}}


def reviewed_policy(config):
    name = config["policy"]["role_toolsets_manifest"]
    if not name:
        raise GateError("A concrete reviewed policy manifest is required")
    path = Path(name)
    path = path if path.is_absolute() else ROOT / path
    relative = source_path_name(path)
    if not relative.startswith("infra/gcp/policy/"):
        raise GateError("Policy manifest must be a repository-owned reviewed policy file")
    policy = json.loads(read_source_file(relative)[1])
    concrete = concrete_runtime_policy()
    expected_toolsets = {role: [tool for tool, capability in concrete["tool_capabilities"].items() if capability in capabilities] for role, capabilities in concrete["roles"].items()}
    if policy.get("schema") != "gis-ai-go.gcp-role-toolsets.v1" or policy.get("id") != config["policy"]["policy_release"] or policy.get("id") != concrete["policy_release"] or policy.get("roles") != concrete["roles"] or policy.get("tool_capabilities") != concrete["tool_capabilities"] or policy.get("role_toolsets") != expected_toolsets or policy.get("default_decision") != "deny" or policy.get("classifications") != ["public-metadata"]:
        raise GateError("Policy manifest differs from the application's actual grants/tool capabilities")
    source_paths = {"apps/mcp-gateway/src/gcp-identity.ts", "apps/mcp-gateway/src/gcp-mcp.ts"}
    if {binding.get("path") for binding in policy.get("source_bindings", [])} != source_paths:
        raise GateError("Policy manifest must bind both actual authorisation/tool sources")
    for binding in policy["source_bindings"]:
        if read_source_file(binding["path"], include_bytes=False)[0]["sha256"] != binding.get("sha256"):
            raise GateError("Policy source changed after manifest review")
    return path


def browser_public_origin(browser):
    parsed = urllib.parse.urlsplit(browser["callback_url"])
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.path != "/auth/callback" or parsed.query or parsed.fragment:
        raise GateError("Browser callback must be one exact approved HTTPS origin followed by /auth/callback")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))


def source_manifest(config_path=None):
    result = execute(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT)
    paths = require(result, "source inventory").split("\0")
    # Exact selected config is the only authorised omission. Validate its lexical
    # components before exclusion; a link to it can never hide a source entry.
    private = Path(config_path).absolute() if config_path else None
    files = []
    total = 0
    for item in sorted(set(filter(None, paths))):
        item = _source_name(item)
        if ROOT / item == private:
            read_source_file(item, include_bytes=False, validate_only=True)
            continue
        entry, _ = read_source_file(item, include_bytes=False)
        files.append(entry)
        total += entry["bytes"]
        if len(files) > SOURCE_FILE_COUNT_LIMIT or total > SOURCE_TOTAL_LIMIT:
            raise GateError("Source inventory exceeds its bounded count or byte limit")
    return {"revision": require(execute(["git", "rev-parse", "HEAD"], cwd=ROOT), "revision").strip(), "files": files}


def placeholders(value):
    if isinstance(value, str):
        return bool(re.search(r"(?i)(<[^>]+>|REPLACE_ME|YOUR_PROJECT|TODO|example\.com|CHANGEME)", value))
    if isinstance(value, dict):
        return any(placeholders(child) for child in value.values())
    if isinstance(value, list):
        return any(placeholders(child) for child in value)
    return False


def unresolved(config):
    missing = []
    for key in ("id", "number", "expected_account", "billing_account", "region", "billing_currency", "billing_currency_evidence"):
        if not config["project"].get(key):
            missing.append("project." + key)
    if not config["authority"]["spend_envelope"]:
        missing.append("authority.spend_envelope (dated, currency-bound prices and approved spending limits)")
    if not config["authority"]["pilot_end"]:
        missing.append("authority.pilot_end")
    for key in ("policy_release", "role_toolsets_manifest"):
        if not config["policy"][key]:
            missing.append("policy." + key)
    if not config["state"]["retention_policy"]:
        missing.append("state.retention_policy")
    for key in ("store_nonce", "created_at", "software_revision"):
        if not config["state"].get(key):
            missing.append("state." + key)
    if config["network"]["create_access_vm"]:
        if not config["network"].get("access_vm_on_demand"):
            missing.append("personal access VM must be on demand")
        for key in ("access_vm_image", "access_vm_zone"):
            if not config["network"][key]:
                missing.append("network." + key)
        if not config["network"]["access_principals"]:
            missing.append("network.access_principals")
    if config["profile"] == "bduk-sandpit-network-private":
        if not config["identity"].get("browser"):
            missing.append("identity.browser (approved Okta browser registration/endpoints/secret references)")
        for section, keys in (("network", ("vpc_id", "subnet_id", "shared_vpc_host_project", "transport_principals")), ("identity", ("oidc_issuer", "client_id", "resource_audience", "jwks_uri", "claims_mapping", "group_attribute_mapping", "runtime_service_account", "transport_service_account", "transport_subject")), ("authority", ("platform_approval_reference",)), ("operations", ("image_repository",))):
            for key in keys:
                if not config[section].get(key):
                    missing.append(section + "." + key)
        if not (config["state"]["bundle_store"] or {}).get("backup_bucket_name"):
            missing.append("state.bundle_store.backup_bucket_name")
        if config["network"]["create_access_vm"]:
            missing.append("BDUK profile consumes approved platform networking; no personal VM")
    if placeholders({k: v for k, v in config.items() if k != "_status"}):
        missing.append("unresolved placeholder value")
    browser = config["identity"].get("browser")
    if browser:
        try:
            browser_public_origin(browser)
        except GateError as error:
            missing.append(str(error))
        if config["profile"] != "bduk-sandpit-network-private":
            missing.append("personal transport milestone cannot silently enable enterprise browser SSO")
        if browser["callback_url"] not in browser["allowed_redirect_uris"] or not browser["callback_url"].endswith("/auth/callback"):
            missing.append("identity.browser exact approved callback /auth/callback")
        if "openid" not in browser["scopes"]:
            missing.append("identity.browser.scopes requires openid")
        if browser["client_auth_method"] == "client_secret_basic" and browser["client_secret"] is None:
            missing.append("identity.browser.client_secret reference")
        if browser["client_auth_method"] == "none" and browser["client_secret"] is not None:
            missing.append("identity.browser public client cannot carry a client secret")
    return missing


def validate_spend(config, *, destructive=False, within_approved_scope=False):
    spend = config["authority"]["spend_envelope"]
    if not spend:
        raise GateError("No budget or pricing authority; supply the dated costed envelope")
    if spend["currency"] != config["project"].get("billing_currency"):
        raise GateError("Cost currency differs from verified billing currency")
    if destructive:
        # An expired pilot must still permit explicitly approved removal of its
        # resources. Deployment duration/new-compute limits are not cleanup gates.
        return
    planning_budget = config["authority"].get("planning_budget_total")
    planning_currency = config["authority"].get("planning_budget_currency")
    if planning_budget is not None and (spend["maximum_total"] > planning_budget or spend["currency"] != planning_currency):
        raise GateError("Spend scope exceeds the owner's total planning envelope")
    if spend["estimated_initial"] > spend["maximum_initial"] or spend["estimated_monthly"] > spend["maximum_monthly"] or spend["estimated_total"] > spend["maximum_total"]:
        raise GateError("Cost estimate exceeds approved spend scope")
    minimum_total = spend["estimated_initial"] + spend["estimated_monthly"] * spend["pilot_days"] / 30.0 + spend["estimated_retained"]
    if spend["estimated_total"] < minimum_total:
        raise GateError("Total cost estimate understates initial, pilot-duration and retained costs")
    if not str(spend["pricing_source"]).startswith("https://"):
        raise GateError("Pricing provenance must identify the verified official source")
    pricing_date = dt.date.fromisoformat(spend["pricing_as_of"])
    if not within_approved_scope and abs((now().date() - pricing_date).days) > 31:
        raise GateError("Pricing evidence is stale; revalidate rates and assumptions")
    end = dt.datetime.fromisoformat(config["authority"]["pilot_end"].replace("Z", "+00:00"))
    if end <= now() or end > now() + dt.timedelta(days=spend["pilot_days"]):
        raise GateError("Pilot end is expired or exceeds approved duration")


class Lifecycle:
    def __init__(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.config = load_config(self.config_path)
        self.config_digest = digest(self.config)
        self.directory = ROOT / "artifacts/gcp" / self.config_digest[:16]
        self.directory.mkdir(parents=True, exist_ok=True)
        self.journal_path = self.directory / "commands.jsonl"
        self.source_binding = None

    def run(self, args, *, mutation=False, **kwargs):
        result = execute(args, **kwargs)
        evidence = {"timestamp": timestamp(), "command": [str(a) for a in args], "cloud_mutation": mutation,
                    "status": result["status"], "exit_code": result.get("exit_code")}
        # Subprocess outputs can contain principal/resource names. Keep them private.
        write_json(self.directory / "command-results" / f"{now().strftime('%Y%m%dT%H%M%S%f')}.json", result)
        with self.journal_path.open("a") as stream:
            stream.write(json.dumps(evidence) + "\n")
        return result

    def gcloud(self, args, *, mutation=False, **kwargs):
        project = self.config["project"]["id"]
        command = ["gcloud", *args, "--quiet"]
        if project:
            command.extend(["--project", project])
        if self.config["project"].get("expected_account"):
            command.extend(["--account", self.config["project"]["expected_account"]])
        return self.run(command, mutation=mutation, **kwargs)

    def terraform_environment(self):
        # Terraform ADC may differ from the gcloud active account. Bind its
        # provider to a short-lived token minted for the exact approved account.
        account = self.config["project"]["expected_account"]
        token = require(execute(["gcloud", "auth", "print-access-token", "--account", account]), "account-bound Terraform authentication").strip()
        return {**os.environ, "GOOGLE_OAUTH_ACCESS_TOKEN": token, "GOOGLE_PROJECT": self.config["project"]["id"]}

    def preflight(self):
        config = self.config
        checks = []
        facts = {"account": None, "project_id": None, "project_number": None, "billing_account": None,
                 "billing_enabled": None, "billing_currency": config["project"].get("billing_currency")}
        tools = {name: shutil.which(name) for name in ("git", "node", "pnpm", "python3", "docker", "skopeo", "terraform", "gcloud")}
        for name, path in tools.items():
            checks.append({"id": "tool-" + name, "status": "PASS" if path else "BLOCKED", "reason": path or "executable unavailable"})
        if tools["gcloud"]:
            auth = self.gcloud(["auth", "list", "--filter=status:ACTIVE", "--format=json(account)"])
            if auth["status"] == "PASS":
                accounts = json.loads(auth["stdout"])
                if len(accounts) == 1:
                    facts["account"] = accounts[0]["account"]
            checks.append({"id": "active-account", "status": "PASS" if facts["account"] == config["project"]["expected_account"] and facts["account"] else "BLOCKED", "reason": "exact configured identity must be observed"})
            if config["project"]["id"]:
                for args, identifier in ((["projects", "describe", config["project"]["id"], "--format=json(projectId,projectNumber,lifecycleState)"], "project"), (["billing", "projects", "describe", config["project"]["id"], "--format=json"], "billing"), (["services", "list", "--enabled", "--format=json(config.name)"], "enabled-apis")):
                    observed = self.gcloud(args)
                    checks.append({"id": identifier, "status": observed["status"], "reason": "read-only observation" if observed["status"] == "PASS" else "unknown or denied; absence not established"})
                    if observed["status"] == "PASS":
                        data = json.loads(observed["stdout"])
                        if identifier == "project":
                            facts.update(project_id=data.get("projectId"), project_number=str(data.get("projectNumber")))
                        if identifier == "billing":
                            facts.update(billing_account=data.get("billingAccountName", "").removeprefix("billingAccounts/"), billing_enabled=data.get("billingEnabled"))
                        if identifier == "enabled-apis":
                            facts["enabled_apis"] = [item["config"]["name"] for item in data]
                browser = config["identity"].get("browser")
                if browser:
                    api_status = "PASS" if any(api == "secretmanager.googleapis.com" for api in facts.get("enabled_apis", [])) else "BLOCKED"
                    checks.append({"id": "browser-secretmanager-api", "status": api_status, "reason": "Existing API required; preflight never enables it"})
                    references = [browser["session_key_secret"]] + ([browser["client_secret"]] if browser["client_secret"] else [])
                    for index, reference in enumerate(references):
                        parts = reference["resource"].split("/")
                        result = self.run(["gcloud", "secrets", "versions", "describe", reference["version"], "--secret", parts[3], "--project", parts[1], "--account", config["project"]["expected_account"], "--format=json(name,state)", "--quiet"])
                        enabled = result["status"] == "PASS" and json.loads(result["stdout"]).get("state") == "ENABLED"
                        checks.append({"id": "browser-secret-version-" + str(index), "status": "PASS" if enabled else "BLOCKED", "reason": "Version metadata only; no credential value read"})
                network = config["network"]
                for key, group in (("vpc_id", "networks"), ("subnet_id", "networks subnets")):
                    if network.get(key):
                        args = ["compute", *group.split(), "describe", network[key].split("/")[-1], "--format=json(name,network,privateIpGoogleAccess,ipCidrRange)"]
                        if key == "subnet_id":
                            args.extend(["--region", config["project"]["region"]])
                        if network.get("shared_vpc_host_project"):
                            args.extend(["--project", network["shared_vpc_host_project"]])
                        result = self.run(["gcloud", *args, "--quiet", *([] if network.get("shared_vpc_host_project") else ["--project", config["project"]["id"]])])
                        checks.append({"id": key, "status": result["status"], "reason": "platform topology needs separate inside-source verification"})
        else:
            checks.append({"id": "cloud-identity-project-billing", "status": "BLOCKED", "reason": "gcloud unavailable; account/project/billing remain UNKNOWN"})
        for name in unresolved(config):
            checks.append({"id": "input-" + name, "status": "BLOCKED", "reason": "owner or platform input unresolved"})
        checks.extend([{"id": "mutation-permissions", "status": "NOT_RUN", "reason": "Terraform saved planning and approved apply establish permissions; read access is insufficient"},
                       {"id": "private-source-topology", "status": "NOT_RUN", "reason": "requires approved in-VPC runner"}])
        result = {"timestamp": timestamp(), "read_only": True, "facts": facts, "tools": tools, "checks": checks}
        write_json(self.directory / "preflight.json", result)
        return result

    def assert_cloud_identity(self, *, destructive=False, within_approved_scope=False):
        observed = self.preflight()
        facts = observed["facts"]
        if not destructive and any(check["id"].startswith("browser-") and check["status"] != "PASS" for check in observed["checks"]):
            raise GateError("Browser identity API/secret-version prerequisites remain unresolved")
        expected = self.config["project"]
        if facts["account"] != expected["expected_account"] or facts["project_id"] != expected["id"] or facts["project_number"] != expected["number"]:
            raise GateError("Observed account/project does not exactly match approved configuration")
        if (not destructive and not facts["billing_enabled"]) or facts["billing_account"] != expected["billing_account"]:
            raise GateError("Billing attachment is unknown, disabled or differs from approved scope")
        evidence = Path(expected["billing_currency_evidence"])
        if not evidence.is_file():
            raise GateError("Verified billing currency evidence is unavailable")
        currency = read_json(evidence)
        if currency.get("billing_account") != expected["billing_account"] or currency.get("currency") != expected["billing_currency"] or not currency.get("source"):
            raise GateError("Billing currency evidence does not bind the selected account/currency/source")
        observed = dt.datetime.fromisoformat(currency["observed_at"].replace("Z", "+00:00"))
        if observed > now() or (not destructive and not within_approved_scope and observed < now() - dt.timedelta(days=31)):
            raise GateError("Billing currency evidence is stale or dated in the future")
        return facts

    def prepare(self):
        source = source_manifest(self.config_path)
        write_json(self.directory / "source-manifest.json", source)
        prepare_command = ["node", "scripts/gcp/prepare.mjs", "--config", self.config_path, "--output", self.directory / "prepared"]
        if os.environ.get("GIS_AI_GO_VERIFIED_OKF_PLUS"):
            prepare_command.extend(["--verified-okf-plus", os.environ["GIS_AI_GO_VERIFIED_OKF_PLUS"]])
        result = self.run(prepare_command, timeout=1800)
        require(result, "admitted bundle/application preparation")
        manifest = read_json(self.directory / "prepared/manifest.json")
        context = self.directory / "prepared/context"
        # An OCI archive exposes its real manifest digest before registry publication.
        image_path = self.directory / "gateway.oci.tar"
        if shutil.which("docker"):
            build_command = ["docker", "buildx", "build"]
            if os.environ.get("GIS_AI_GO_BUILDX_BUILDER"):
                build_command.extend(["--builder", os.environ["GIS_AI_GO_BUILDX_BUILDER"]])
            build_command.extend(["--platform=linux/amd64", "--provenance=false", "--sbom=false", "--output", f"type=oci,dest={image_path}", "--file", context / "Containerfile", context])
            image = self.run(build_command, timeout=1800)
            if image["status"] == "PASS":
                with tarfile.open(image_path) as archive:
                    index = json.load(archive.extractfile("index.json"))
                manifests = index["manifests"]
                if len(manifests) != 1 or not re.fullmatch(r"sha256:[0-9a-f]{64}", manifests[0]["digest"]):
                    raise GateError("OCI export must have one immutable Linux image manifest")
                write_json(self.directory / "image.json", {"manifest_digest": manifests[0]["digest"], "archive_sha256": file_digest(image_path), "bytes": image_path.stat().st_size, "platform": "linux/amd64", "status": "LOCAL_BUILD_ONLY", "prepared_manifest_sha256": file_digest(self.directory / "prepared/manifest.json"), "prepared_context_sha256": digest(directory_manifest(context)), "build_source_sha256": manifest.get("sourceSha256")})
            else:
                write_json(self.directory / "image.json", {"status": "BLOCKED", "reason": "local OCI image build failed; inspect private command evidence"})
        else:
            write_json(self.directory / "image.json", {"status": "BLOCKED", "reason": "docker unavailable"})
        return {"prepared_manifest_sha256": file_digest(self.directory / "prepared/manifest.json"), "release_id": manifest.get("releaseId"), "image": read_json(self.directory / "image.json")}

    def variables(self, phase, image_digest=None, invoker_unique_id="OUTPUT_BOUND_AFTER_FOUNDATION", runtime_config=None):
        cfg = self.config
        project = cfg["project"]["id"] or "UNRESOLVED_PROJECT"
        region = cfg["project"]["region"] or "UNRESOLVED_REGION"
        name = cfg["operations"]["name_prefix"]
        create_network = cfg["profile"] == "personal-network-private" and not cfg["network"]["vpc_id"]
        network = cfg["network"]["vpc_id"] or f"projects/{project}/global/networks/{name}-private"
        subnet = cfg["network"]["subnet_id"] or f"projects/{project}/regions/{region}/subnetworks/{name}-private"
        common = dict(project_id=project, region=region, profile=cfg["profile"], name_prefix=name, network_id=network, subnet_id=subnet)
        if phase == "foundation":
            common.update(enable_apis=cfg["profile"] == "personal-network-private", publisher_member="user:" + (cfg["project"]["expected_account"] or "UNRESOLVED_ACCOUNT"), create_network=create_network, subnet_cidr=cfg["network"]["subnet_cidr"], backup_bucket_name=(cfg["state"]["bundle_store"] or {}).get("backup_bucket_name") or f"{project}-{name}-backup", database_id=(cfg["state"]["evidence_store"] or {}).get("database_id", "UNRESOLVED_DATABASE"), create_access_vm=cfg["network"]["create_access_vm"], access_vm_zone=cfg["network"]["access_vm_zone"] or "UNRESOLVED_ZONE", access_vm_image=cfg["network"]["access_vm_image"] or "UNRESOLVED_PINNED_IMAGE", access_vm_machine_type=cfg["network"]["access_vm_machine_type"], access_principals=cfg["network"]["access_principals"])
            common.update(create_foundation=cfg["profile"] == "personal-network-private", existing_runtime_email=cfg["identity"].get("runtime_service_account") or "", existing_invoker_email=cfg["identity"].get("transport_service_account") or "", existing_invoker_unique_id=cfg["identity"].get("transport_subject") or "", existing_image_repository=cfg["operations"].get("image_repository") or "")
            common.update(project_number=cfg["project"].get("number") or "UNRESOLVED_PROJECT_NUMBER", access_vm_on_demand=cfg["network"]["access_vm_on_demand"])
        else:
            prepared = self.directory / "prepared/manifest.json"
            manifest = read_json(prepared) if prepared.exists() else {}
            repository = cfg["operations"].get("image_repository") or f"{region}-docker.pkg.dev/{project}/{name}-images/gateway"
            common.update(runtime_email=cfg["identity"].get("runtime_service_account") or f"{name}-runtime@{project}.iam.gserviceaccount.com", invoker_unique_id=invoker_unique_id, image_reference=f"{repository}@{image_digest or 'UNRESOLVED_IMAGE'}", release_id=manifest.get("releaseId", "UNRESOLVED_RELEASE"), transport_principals=cfg["network"]["transport_principals"] or [f"serviceAccount:{name}-invoker@{project}.iam.gserviceaccount.com"], runtime_config_json=json.dumps(runtime_config or {}, separators=(",", ":")), deletion_protection=True)
            common.update(cfg["operations"]["runtime_sizing"] or {})
            common.pop("min_instances", None)
            browser = cfg["identity"].get("browser")
            common["browser_secret_references"] = {}
            if browser:
                common["browser_secret_references"]["GCP_BROWSER_SESSION_KEY"] = browser["session_key_secret"]
                if browser["client_secret"]:
                    common["browser_secret_references"]["GCP_OIDC_CLIENT_SECRET"] = browser["client_secret"]
        return common

    def iac_root(self, phase):
        if phase not in PHASES:
            raise GateError("Unknown IaC phase")
        environment = "personal" if self.config["profile"] == "personal-network-private" else "bduk-sandpit"
        owner = digest({"profile": self.config["profile"], "project": self.config["project"]["id"], "name": self.config["operations"]["name_prefix"]})[:16]
        source = source_manifest(self.config_path)
        if self.source_binding and digest(source) != self.source_binding:
            raise GateError("Source changed before Terraform invocation")
        entries = {entry["path"][len("infra/gcp/"):]: entry for entry in source["files"] if entry["path"].startswith("infra/gcp/")}
        if not entries or f"environments/{environment}/{phase}/main.tf" not in entries:
            raise GateError("Admitted Git inventory has no executable IaC phase")
        if any(private_source_name(name) for name in entries):
            raise GateError("Private/generated IaC cannot be admitted as public source")
        target_name = f"artifacts/gcp/state/{owner}/iac"
        descriptors = _directory_descriptors(ROOT, target_name, create=True)
        for fd in reversed(descriptors):
            os.close(fd)
        target = ROOT / target_name
        generated_inputs = {f"environments/{profile}/{part}/inputs.auto.tfvars.json" for profile in ("personal", "bduk-sandpit") for part in PHASES}
        # Old overlay copies must not leave executable configuration behind. Keep
        # state, saved plans and provider cache intact; report rather than remove it.
        for current, directories, filenames in os.walk(target, followlinks=False):
            for directory in directories:
                if (Path(current) / directory).is_symlink():
                    raise GateError("IaC target contains a linked directory")
            directories[:] = [name for name in directories if name != ".terraform"]
            for filename in filenames:
                relative = (Path(current) / filename).relative_to(target).as_posix()
                if terraform_input_name(relative):
                    read_source_file(relative, root=target, include_bytes=False)
                    if relative not in entries and relative not in generated_inputs:
                        raise GateError("IaC target contains stale or unadmitted Terraform input: " + relative)
        for relative, entry in sorted(entries.items()):
            _actual, content = read_source_file(entry["path"], expected=entry)
            write_admitted_source(target, relative, content, entry["mode"])
            read_source_file(relative, root=target, expected={**entry, "path": relative}, include_bytes=False)
        return target / "environments" / environment / phase

    def terraform_run(self, phase, args, **kwargs):
        # Revalidate/re-materialise immediately before every Terraform process;
        # a previous root copy is not an authority for later invocations.
        root = self.iac_root(phase)
        return self.run(["terraform", f"-chdir={root}", *args], **kwargs)

    def terraform_plan(self, phase, variables, *, destroy=False, targets=()):
        root = self.iac_root(phase)
        write_json(root / "inputs.auto.tfvars.json", variables)
        require(self.terraform_run(phase, ["init", "-input=false", "-backend=false", "-lockfile=readonly"], timeout=600), "Terraform provider initialisation")
        plan_path = root / ("destroy.tfplan" if destroy else "deployment.tfplan")
        args = ["plan", "-input=false", "-lock-timeout=30s", "-out", plan_path]
        if destroy:
            args.append("-destroy")
        for address in targets:
            args.extend(["-target", address])
        require(self.terraform_run(phase, args, timeout=600, env=self.terraform_environment()), "Terraform saved plan")
        shown = require(self.terraform_run(phase, ["show", "-json", plan_path]), "Terraform plan inspection")
        write_json(root / ("destroy-plan.json" if destroy else "deployment-plan.json"), json.loads(shown))
        return {"sha256": file_digest(plan_path), "file": str(plan_path), "changes": [{"address": r["address"], "actions": r["change"]["actions"]} for r in json.loads(shown).get("resource_changes", [])]}

    def plan(self, destructive=False):
        preflight = self.preflight()
        source = source_manifest(self.config_path)
        self.source_binding = digest(source)
        prepared_path = self.directory / "prepared/manifest.json"
        image_path = self.directory / "image.json"
        blockers = unresolved(self.config)
        if not prepared_path.exists() and not destructive:
            blockers.append("prepare has not produced admitted inventory")
        image = read_json(image_path) if image_path.exists() else {"status": "BLOCKED"}
        try:
            policy_path = reviewed_policy(self.config)
        except (GateError, OSError, ValueError) as error:
            policy_path = None
            blockers.append(str(error))
        if not image.get("manifest_digest") and not destructive:
            blockers.append("immutable OCI image digest unavailable")
        if prepared_path.exists() and not destructive:
            verified = self.run(["node", "--input-type=module", "-e", "import {verifyPrepared} from './scripts/gcp/prepare.mjs'; await verifyPrepared(process.argv[1]);", prepared_path.parent], timeout=600)
            if verified["status"] != "PASS":
                blockers.append("prepared admitted inventory verification failed")
            manifest = read_json(prepared_path)
            if image.get("prepared_manifest_sha256") != file_digest(prepared_path) or image.get("prepared_context_sha256") != digest(directory_manifest(prepared_path.parent / "context")) or image.get("build_source_sha256") != manifest.get("sourceSha256"):
                blockers.append("image build receipt does not bind this exact admitted context/source manifest")
            try:
                validate_prepared_sources(manifest, source)
            except GateError as error:
                blockers.append(str(error))
        if not shutil.which("terraform"):
            blockers.append("terraform unavailable")
        if not shutil.which("gcloud"):
            blockers.append("gcloud unavailable; cloud identity UNKNOWN")
        if not shutil.which("skopeo") and not destructive:
            blockers.append("skopeo unavailable for authenticated digest-preserving publication")
        try:
            validate_spend(self.config, destructive=destructive)
        except (GateError, ValueError, TypeError) as error:
            blockers.append(str(error))
        context_path = self.directory / "prepared/context"
        runtime_path = context_path / "app/runtime-config.json"
        runtime_template = read_json(runtime_path) if runtime_path.exists() else None
        if runtime_template:
            runtime_template["firestore"] = {"projectId": self.config["project"]["id"], "databaseId": (self.config["state"]["evidence_store"] or {}).get("database_id"), "collection": (self.config["state"]["evidence_store"] or {}).get("collection")}
            runtime_template["evidence"] = {"storeNonce": self.config["state"].get("store_nonce"), "createdAt": self.config["state"].get("created_at"), "sourceRevision": self.config["state"].get("software_revision")}
            if self.config["profile"] == "bduk-sandpit-network-private":
                identity = self.config["identity"]
                runtime_template["identity"] = {"mode": "oidc", "issuer": identity["oidc_issuer"], "audience": identity["resource_audience"], "jwksUri": identity.get("jwks_uri"), "groupClaim": (identity.get("group_attribute_mapping") or {}).get("claim", "groups"), "groupRoles": (identity.get("group_attribute_mapping") or {}).get("roles", {}), "subjectRoles": (identity.get("claims_mapping") or {}).get("subject_roles", {})}
                if identity.get("browser"):
                    browser = identity["browser"]
                    runtime_template["identity"]["browser"] = {"clientId": browser["client_id"], "clientAuthMethod": browser["client_auth_method"], "callbackUrl": browser["callback_url"], "allowedRedirectUris": browser["allowed_redirect_uris"], "allowedEndpoints": browser["allowed_endpoints"], "scopes": browser["scopes"], "sessionSeconds": browser["session_seconds"]}
        bindings = {"config_sha256": self.config_digest, "source_sha256": digest(source), "prepared_sha256": file_digest(prepared_path) if prepared_path.exists() else None,
                    "prepared_context_sha256": digest(directory_manifest(context_path)),
                    "policy_manifest_sha256": file_digest(policy_path) if policy_path else None,
                    "image_digest": image.get("manifest_digest"), "image_archive_sha256": image.get("archive_sha256"), "access_proxy_sha256": file_digest(ROOT / "scripts/gcp/access_proxy.py") if (ROOT / "scripts/gcp/access_proxy.py").exists() else None,
                    "account": self.config["project"]["expected_account"], "project": self.config["project"]["id"], "project_number": self.config["project"]["number"], "spend_sha256": digest(self.config["authority"]["spend_envelope"])}
        currency_path = self.config["project"].get("billing_currency_evidence")
        bindings["billing_currency_evidence_sha256"] = file_digest(currency_path) if currency_path and Path(currency_path).is_file() else None
        plan = {"schema_version": "1", "created_at": timestamp(), "kind": "destroy" if destructive else "deploy", "bindings": bindings, "blockers": blockers,
                "runtime_template": runtime_template,
                "facts": preflight["facts"], "desired_variables": {phase: self.variables(phase, image.get("manifest_digest")) for phase in PHASES},
                "cost": self.config["authority"]["spend_envelope"], "upload_inventory": read_json(prepared_path) if prepared_path.exists() else {"status": "NOT_RUN"},
                "phases": ["apply approved foundation saved plan", "publish locally built immutable OCI image only", "plan/apply Cloud Run with output-bound invoker subject", "read actual service URI, bind transport audience, plan/apply configuration", "provision one principal-scoped synthetic evidence snapshot explicitly", "install reviewed proxy over IAP; no internet software bootstrap"],
                "output_bound_fields": ["invoker_unique_id from the newly approved service account", "runtime_config.transportSubject", "runtime_config.transportAudience from actual service URI", "runtime_config.publicOrigin from actual service URI"],
                "rollback": "previous recorded compatible image/bundle/policy; initial deployment disable/delete service with separate destructive approval", "retention": self.config["operations"]["retention_on_destroy"], "terraform": {}}
        if not blockers:
            self.assert_cloud_identity(destructive=destructive)
            if destructive:
                for phase in reversed(PHASES):
                    state = require(self.terraform_run(phase, ["state", "list"]), "owned state inventory").splitlines()
                    targets = [s for s in state if not re.search(r"google_(storage_bucket\.backup|firestore_database\.evidence)", s)]
                    if targets:
                        current_variables = read_json(self.iac_root(phase) / "inputs.auto.tfvars.json")
                        plan["desired_variables"][phase] = current_variables
                        plan["terraform"][phase] = self.terraform_plan(phase, current_variables, destroy=True, targets=targets)
            else:
                plan["terraform"]["foundation"] = self.terraform_plan("foundation", plan["desired_variables"]["foundation"])
                # Service identity/audience are output-bound, not guessed. Its complete
                # intended configuration is reviewed now, its concrete plan after foundation.
        plan["approval_actions"] = ["foundation", "publish-image", "deploy-service", "bind-observed-identity", "provision-synthetic-evidence", "bootstrap-access-proxy", "verify-bounded-evidence", "rollback-compatible-release"] if not destructive else ["destroy-owned-pilot-retain-evidence"]
        if self.config["identity"].get("browser") and not destructive:
            plan["approval_actions"].append("bind-browser-secret-access")
        if self.config["network"]["create_access_vm"] and not destructive:
            plan["approval_actions"].append("connect-start-stop-owned-vm")
            plan["access_vm_operating_scope"] = {"mode": "on-demand", "maximum_reserved_connected_hours": self.config["network"]["access_vm_max_connected_hours"], "maximum_tunnel_seconds": 3600, "per_connection_reserved_hours": 1.25, "automatic_stop_cron": "0 * * * *", "automatic_start": False, "scheduler_delay_minutes": 15, "hard_budget_cap": False, "retained_charges": ["stopped VM boot disk", "private DNS", "Firestore/PITR", "backup objects", "image storage", "retained logs"], "authority": "Exact owned VM start/stop only; reserved-hours ledger is a cooperative client safeguard"}
        plan_id = plan_identity(plan)
        plan["plan_id"] = plan_id
        write_json(self.directory / "plans" / f"{plan_id}.json", plan)
        write_json(self.directory / "latest-plan.json", plan)
        template = {"status": "PENDING_OWNER_APPROVAL", "plan_id": plan_id, "bindings": bindings, "kind": plan["kind"], "approved_by": None, "approved_at": None, "expires_at": None, "actions": plan["approval_actions"], "spend": plan["cost"], "platform_approval_reference": self.config["authority"].get("platform_approval_reference")}
        write_json(self.directory / "approvals" / f"{plan_id}.template.json", template)
        return plan

    def approved(self, plan_id, kind, *, connection=False):
        if not re.fullmatch(r"[0-9a-f]{24}", plan_id or ""):
            raise GateError("An exact recorded plan ID is required")
        plan = read_json(self.directory / "plans" / f"{plan_id}.json")
        approval = read_json(self.directory / "approvals" / f"{plan_id}.approval.json")
        if plan_identity(plan) != plan_id:
            raise GateError("The complete recorded plan changed after review")
        if not set(approval.get("actions", [])) <= set(plan.get("approval_actions", [])):
            raise GateError("Approval action exceeds the reviewed plan scope")
        if plan["kind"] != kind or approval.get("kind") != kind or approval.get("plan_id") != plan_id or approval.get("status") != "APPROVED":
            raise GateError("Approval does not authorise this exact operation")
        if plan["blockers"]:
            raise GateError("Unresolved prerequisites block cloud mutations")
        if not approval.get("approved_at"):
            raise GateError("Approval has no recorded decision time")
        approved_time = dt.datetime.fromisoformat(approval["approved_at"].replace("Z", "+00:00"))
        if approved_time > now():
            raise GateError("Approval decision time is in the future")
        expiry = dt.datetime.fromisoformat(approval["expires_at"].replace("Z", "+00:00"))
        if kind == "destroy":
            latest_expiry = approved_time + dt.timedelta(days=7)
        else:
            pilot_end = dt.datetime.fromisoformat(self.config["authority"]["pilot_end"].replace("Z", "+00:00"))
            latest_expiry = min(approved_time + dt.timedelta(days=90), pilot_end)
        if expiry <= now() or expiry > latest_expiry:
            raise GateError("Approval expired or exceeds its explicit pilot/cleanup validity scope")
        expected = plan["bindings"]
        if approval.get("bindings") != expected or approval.get("approved_by") != expected["account"] or approval.get("spend") != plan["cost"]:
            raise GateError("Approval identity, immutable inputs or spend scope differs")
        if self.config["profile"] == "bduk-sandpit-network-private" and approval.get("platform_approval_reference") != self.config["authority"]["platform_approval_reference"]:
            raise GateError("BDUK platform approval reference differs")
        if digest(self.config) != expected["config_sha256"] or digest(source_manifest(self.config_path)) != expected["source_sha256"]:
            raise GateError("Source/configuration changed after the approved plan")
        self.source_binding = expected["source_sha256"]
        if kind != "destroy" and not connection and digest(directory_manifest(self.directory / "prepared/context")) != expected["prepared_context_sha256"]:
            raise GateError("Prepared context changed after the approved plan")
        if file_digest(self.config["project"]["billing_currency_evidence"]) != expected["billing_currency_evidence_sha256"]:
            raise GateError("Verified billing currency evidence changed after approval")
        if expected.get("policy_manifest_sha256") and file_digest(reviewed_policy(self.config)) != expected["policy_manifest_sha256"]:
            raise GateError("Reviewed application policy changed after approval")
        for path, field in ((self.directory / "prepared/manifest.json", "prepared_sha256"), (self.directory / "gateway.oci.tar", "image_archive_sha256"), (ROOT / "scripts/gcp/access_proxy.py", "access_proxy_sha256")):
            if kind == "destroy" or (connection and field in ("prepared_sha256", "image_archive_sha256")):
                continue
            if file_digest(path) != expected[field]:
                raise GateError(f"Approved {field} changed")
        validate_spend(self.config, destructive=kind == "destroy", within_approved_scope=connection)
        self.assert_cloud_identity(destructive=kind == "destroy", within_approved_scope=connection)
        return plan, approval

    def apply_saved(self, phase, plan, key="deployment.tfplan"):
        root = self.iac_root(phase)
        selected_path = root / key
        if phase in plan.get("terraform", {}):
            bound = plan["terraform"][phase]
            bound_path = Path(bound["file"])
            if not bound_path.is_absolute() or bound_path != selected_path:
                raise GateError("Saved plan path differs from the approved execution path")
            bound_name = bound_path.relative_to(ROOT).as_posix()
            if read_source_file(bound_name, include_bytes=False, limit=128 * 1024 * 1024)[0]["sha256"] != bound["sha256"]:
                raise GateError("Saved Terraform plan changed")
            selected_path = bound_path
        else:
            raise GateError("No saved Terraform plan was approved for this phase")
        require(self.terraform_run(phase, ["apply", "-input=false", "-lock-timeout=30s", selected_path], mutation=True, timeout=1200, env=self.terraform_environment()), "approved Terraform apply")

    @staticmethod
    def service_scope(concrete_plan, *, deleting=False):
        for change in concrete_plan["changes"]:
            address = change["address"]
            if not (address == "module.pilot.google_cloud_run_v2_service.gateway" or address.startswith("module.pilot.google_cloud_run_v2_service_iam_member.private_transport[") or address.startswith("module.pilot.google_secret_manager_secret_iam_member.browser[")):
                raise GateError("Unapproved resource appeared in the output-bound service plan")
            if "delete" in change["actions"] and not deleting:
                raise GateError("Output-bound deployment would delete or replace a resource outside approval")

    def outputs(self, phase):
        data = json.loads(require(self.terraform_run(phase, ["output", "-json"]), "actual Terraform outputs"))
        return {name: item["value"] for name, item in data.items()}

    def apply(self, plan_id):
        plan, approval = self.approved(plan_id, "deploy")
        required = {"foundation", "publish-image", "deploy-service", "bind-observed-identity", "bootstrap-access-proxy", "provision-synthetic-evidence"}
        if self.config["identity"].get("browser"):
            required.add("bind-browser-secret-access")
        if not required <= set(approval.get("actions", [])):
            raise GateError("Approval lacks required phase authority")
        progress_path = self.directory / "plans" / f"{plan_id}.progress.json"
        progress = read_json(progress_path) if progress_path.exists() else {"plan_id": plan_id}
        if progress.get("foundation"):
            foundation = self.outputs("foundation")
            if foundation != progress["foundation"]:
                raise GateError("Foundation outputs changed during resumption; review drift before continuing")
        else:
            self.apply_saved("foundation", plan)
            foundation = self.outputs("foundation")
            progress["foundation"] = foundation
            write_json(progress_path, progress)
        image = plan["bindings"]["image_digest"]
        repository = foundation["image_repository"]
        # Token exists only in memory and is supplied on stdin, never journalled.
        token = execute(["gcloud", "auth", "print-access-token", "--account", plan["bindings"]["account"]])
        access_token = require(token, "short-lived registry authentication").strip()
        authfile = self.directory / ".registry-auth.json"
        host = repository.split("/")[0]
        try:
            require(self.run(["skopeo", "login", "--authfile", authfile, "--username", "oauth2accesstoken", "--password-stdin", host], mutation=False, input_text=access_token + "\n"), "private registry login")
            destination = repository + ":approved-" + plan_id
            require(self.run(["skopeo", "copy", "--preserve-digests", "--authfile", authfile, "oci-archive:" + str(self.directory / "gateway.oci.tar"), "docker://" + destination], mutation=True, timeout=1200), "approved immutable image publication")
            observed = json.loads(require(self.run(["skopeo", "inspect", "--authfile", authfile, "docker://" + destination]), "published image inspection"))
            if observed["Digest"] != image:
                raise GateError("Published registry digest differs from the approved local OCI digest")
        finally:
            authfile.unlink(missing_ok=True)
            access_token = None
        base = json.loads(json.dumps(plan["runtime_template"]))
        base["transportSubject"] = foundation["invoker_unique_id"]
        # URI is unknown before the first deployment. Startup health may run but
        # application identity must deny while this audience is unresolved.
        base["transportAudience"] = None
        variables = self.variables("service", image, foundation["invoker_unique_id"], base)
        phase_plan = self.terraform_plan("service", variables)
        self.service_scope(phase_plan)
        self.apply_saved("service", {"terraform": {"service": phase_plan}})
        service = self.outputs("service")
        uri = service["service_uri"]
        if not re.fullmatch(r"https://[a-z0-9-]+(?:\.[a-z0-9-]+)*\.run\.app", uri):
            raise GateError("Observed service URI is outside the reviewed fixed target class")
        base["transportAudience"] = uri
        if self.config["profile"] == "personal-network-private":
            base["publicOrigin"] = uri
            base["allowedOrigins"] = ["http://127.0.0.1:8789"]
        else:
            origin = browser_public_origin(self.config["identity"]["browser"])
            base["publicOrigin"] = origin
            base["allowedOrigins"] = [origin]
        variables = self.variables("service", image, foundation["invoker_unique_id"], base)
        phase_plan = self.terraform_plan("service", variables)
        self.service_scope(phase_plan)
        self.apply_saved("service", {"terraform": {"service": phase_plan}})
        service = self.outputs("service")
        # Provisioning is an explicit bounded cloud write, never request-side
        # history recreation. The immutable image supplies the seed implementation.
        runtime_json = json.dumps(base, separators=(",", ":"))
        provisioning_env = {**os.environ, "GCP_RUNTIME_CONFIG_JSON": runtime_json}
        local_image = "gis-ai-go-gcp-approved:" + plan_id
        require(self.run(["skopeo", "copy", "oci-archive:" + str(self.directory / "gateway.oci.tar"), "docker-daemon:" + local_image], timeout=600), "import approved local image without registry authentication")
        provisioning_token = require(execute(["gcloud", "auth", "print-access-token", "--account", plan["bindings"]["account"]]), "provisioning authentication").strip()
        subjects = [None] if self.config["profile"] == "personal-network-private" else sorted(base["identity"]["subjectRoles"])
        for subject in subjects:
            subject_args = ["--subject", subject] if subject else []
            require(self.run(["docker", "run", "--rm", "--network=none", "--env", "GCP_RUNTIME_CONFIG_JSON", "--entrypoint", "node", local_image, "/app/gateway/dist/src/gcp-provision.js", *subject_args], env=provisioning_env), "seed preview")
            require(self.run(["docker", "run", "--rm", "-i", "--env", "GCP_RUNTIME_CONFIG_JSON", "--entrypoint", "node", local_image, "/app/gateway/dist/src/gcp-provision.js", *subject_args, "--apply"], mutation=True, env=provisioning_env, input_text=provisioning_token + "\n", timeout=180), "approved bounded evidence provisioning")
        provisioning_token = None
        if foundation.get("access_vm"):
            vm = foundation["access_vm"]
            zone = self.config["network"]["access_vm_zone"]
            try:
                require(self.gcloud(["compute", "instances", "start", vm, "--zone", zone], mutation=True), "approved access VM bootstrap start")
                self.bootstrap_proxy(vm, uri)
            finally:
                require(self.gcloud(["compute", "instances", "stop", vm, "--zone", zone], mutation=True), "approved access VM idle stop")
        release = {"release_id": service["release_id"], "timestamp": timestamp(), "plan_id": plan_id, "config_sha256": self.config_digest,
                   "image_reference": service["image_reference"], "service_uri": uri, "revision": service["latest_revision"], "foundation": foundation,
                   "variables": variables, "policy_release": self.config["policy"]["policy_release"], "evidence_schema": "gcp-evidence-v1", "acceptance": "DEPLOYED_NOT_VERIFIED", "verification_evidence_writes_authorised": "verify-bounded-evidence" in approval.get("actions", [])}
        write_json(self.directory / "releases" / f"{release['release_id']}.json", release)
        write_json(self.directory / "deployed.json", release)
        progress["completed_release"] = release["release_id"]
        progress["completed_at"] = timestamp()
        write_json(progress_path, progress)
        return release

    def bootstrap_proxy(self, vm, uri):
        zone = self.config["network"]["access_vm_zone"]
        # The exact script hash is bound in the owner-approved plan. The VM image
        # must already provide Python 3; there is no apt/NAT bootstrap.
        require(self.gcloud(["compute", "scp", ROOT / "scripts/gcp/access_proxy.py", f"{vm}:/tmp/gis-access-proxy.py", "--zone", zone, "--tunnel-through-iap"], mutation=True), "reviewed access proxy staging")
        unit = "[Unit]\nDescription=GIS AI GO fixed private invocation proxy\nAfter=network-online.target\n[Service]\nUser=nobody\nExecStart=/usr/bin/python3 /opt/gis-ai-go/access_proxy.py --upstream " + uri + " --allowed-origin http://127.0.0.1:8789 --port 8081\nRestart=on-failure\nNoNewPrivileges=true\nPrivateTmp=true\nProtectSystem=strict\nProtectHome=true\n[Install]\nWantedBy=multi-user.target\n"
        unit_path = self.directory / "gis-access-proxy.service"
        unit_path.write_text(unit)
        require(self.gcloud(["compute", "scp", unit_path, f"{vm}:/tmp/gis-access-proxy.service", "--zone", zone, "--tunnel-through-iap"], mutation=True), "reviewed unit staging")
        # Constant script with no unchecked interpolated values.
        command = "set -eu; test -x /usr/bin/python3; sudo install -d -m 0755 /opt/gis-ai-go; sudo install -m 0644 /tmp/gis-access-proxy.py /opt/gis-ai-go/access_proxy.py; sudo install -m 0644 /tmp/gis-access-proxy.service /etc/systemd/system/gis-access-proxy.service; sudo systemctl daemon-reload; sudo systemctl enable --now gis-access-proxy.service"
        require(self.gcloud(["compute", "ssh", vm, "--zone", zone, "--tunnel-through-iap", "--command", command], mutation=True), "approved proxy installation")

    def connect(self, approved_plan=None):
        deployed = read_json(self.directory / "deployed.json")
        if self.config["profile"] != "personal-network-private":
            raise GateError("Join the platform-approved BDUK private network; no personal bastion is created")
        plan, approval = self.approved(approved_plan or deployed["plan_id"], "deploy", connection=True)
        if "connect-start-stop-owned-vm" not in approval.get("actions", []):
            raise GateError("Recorded approval does not cover starting/stopping the owned access VM")
        vm = deployed["foundation"]["access_vm"]
        if vm != self.config["operations"]["name_prefix"] + "-access" or not self.config["network"]["access_vm_on_demand"]:
            raise GateError("The connection target differs from the approved on-demand owned VM")
        zone = self.config["network"]["access_vm_zone"]
        owner = digest({"profile": self.config["profile"], "project": self.config["project"]["id"], "name": self.config["operations"]["name_prefix"]})[:16]
        ledger_path = ROOT / "artifacts/gcp/access-ledger" / f"{owner}.json"
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with ledger_path.with_suffix(".lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise GateError("Another local session owns this private VM tunnel") from error
            ledger = read_json(ledger_path) if ledger_path.exists() else {"reserved_hours": 0, "sessions": []}
            reservation = plan["access_vm_operating_scope"]["per_connection_reserved_hours"]
            ceiling = self.config["network"]["access_vm_max_connected_hours"]
            if ledger["reserved_hours"] + reservation > ceiling:
                raise GateError("The recorded maximum connection-hours scope is exhausted; review the actual usage/costs")
            session = {"started_at": timestamp(), "plan_id": plan["plan_id"], "reserved_hours": reservation, "status": "STARTING"}
            ledger["reserved_hours"] += reservation
            ledger["sessions"].append(session)
            write_json(ledger_path, ledger)
            process = None
            failure = None
            try:
                require(self.gcloud(["compute", "instances", "start", vm, "--zone", zone], mutation=True), "approved on-demand VM start")
                print(json.dumps({"browser_url": "http://127.0.0.1:8789/", "mcp_url": "http://127.0.0.1:8789/mcp", "canonical_transport_audience": deployed["service_uri"], "connection": "foreground IAP SSH tunnel; exit/Ctrl-C stops the VM; maximum session one hour", "automatic_stop_safeguard": "hourly schedule, possible 15-minute scheduler delay; no hard spend cap", "identity": "transport service account; human identity remains separate"}, indent=2))
                command = ["gcloud", "compute", "ssh", vm, "--project", self.config["project"]["id"], "--account", self.config["project"]["expected_account"], "--zone", zone, "--tunnel-through-iap", "--quiet", "--", "-N", "-o", "ExitOnForwardFailure=yes", "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3", "-L", "127.0.0.1:8789:127.0.0.1:8081"]
                process = subprocess.Popen(command)
                returncode = process.wait(timeout=plan["access_vm_operating_scope"]["maximum_tunnel_seconds"])
                if returncode:
                    failure = f"IAP SSH tunnel exited {returncode}"
            except (KeyboardInterrupt, subprocess.TimeoutExpired):
                session["exit_reason"] = "owner exit or approved maximum session duration"
            except (GateError, OSError) as error:
                failure = str(error)
            finally:
                try:
                    if process is not None and process.poll() is None:
                        try:
                            process.terminate()
                            process.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait(timeout=10)
                        except ProcessLookupError:
                            pass
                finally:
                    stopped = self.gcloud(["compute", "instances", "stop", vm, "--zone", zone], mutation=True)
                    session.update(ended_at=timestamp(), status="STOPPED" if stopped["status"] == "PASS" else "STOP_BLOCKED")
                    write_json(ledger_path, ledger)
                    if stopped["status"] != "PASS":
                        failure = "VM stop failed; inspect status immediately; automatic schedule is an unproven fallback"
            if failure:
                raise GateError(failure)
        return {"status": "CLOSED_VM_STOPPED", "local_listener": "127.0.0.1:8789", "evidence": str(ledger_path), "retained_costs": "Boot disk/private DNS/images/evidence/backups/logs remain; stopped does not mean free"}

    def status(self):
        if not self.config["project"]["id"] or not shutil.which("gcloud"):
            return {"status": "BLOCKED", "reason": "No cloud observation possible; project/account are UNKNOWN", "deployed_url": None}
        results = {}
        for name, args in (("service", ["run", "services", "describe", self.config["operations"]["name_prefix"], "--region", self.config["project"]["region"], "--format=json"]), ("vm", ["compute", "instances", "describe", self.config["operations"]["name_prefix"] + "-access", "--zone", self.config["network"]["access_vm_zone"] or "UNRESOLVED", "--format=json(name,status,networkInterfaces)" ])):
            if name == "vm" and not self.config["network"]["create_access_vm"]:
                continue
            result = self.gcloud(args)
            results[name] = {"status": result["status"], "observed": json.loads(result["stdout"]) if result["status"] == "PASS" else None}
        write_json(self.directory / "status.json", {"timestamp": timestamp(), "resources": results})
        return {"status": "PASS" if all(item["status"] == "PASS" for item in results.values()) else "BLOCKED", "evidence": str(self.directory / "status.json")}

    def prepared_status(self):
        """Classify actual current local material, independent of cloud health."""
        manifest_path = self.directory / "prepared/manifest.json"
        image_path = self.directory / "image.json"
        archive_path = self.directory / "gateway.oci.tar"
        if not all(path.is_file() for path in (manifest_path, image_path, archive_path)):
            return {"status": "NOT_PREPARED", "reason": "Exact admitted context/source and immutable OCI image material are not all present"}
        try:
            manifest, image = read_json(manifest_path), read_json(image_path)
            if image.get("prepared_manifest_sha256") != file_digest(manifest_path) or image.get("prepared_context_sha256") != digest(directory_manifest(manifest_path.parent / "context")) or image.get("build_source_sha256") != manifest.get("sourceSha256") or image.get("archive_sha256") != file_digest(archive_path):
                raise GateError("Prepared context/source/image receipt no longer matches the actual files")
            verified = self.run(["node", "scripts/gcp/prepare.mjs", "--verify-prepared", manifest_path.parent], timeout=600)
            if verified["status"] != "PASS":
                raise GateError("Admitted context validation did not pass")
            validate_prepared_sources(manifest, source_manifest(self.config_path))
            if not manifest.get("sourceFiles") or manifest.get("schema") != "gis-ai-go.gcp-prepared.v1":
                raise GateError("Prepared source inventory is incomplete")
            with tarfile.open(archive_path) as archive:
                stream = archive.extractfile("index.json")
                if stream is None:
                    raise GateError("OCI index is missing")
                index = json.load(stream)
            if len(index.get("manifests", [])) != 1 or index["manifests"][0].get("digest") != image.get("manifest_digest") or not re.fullmatch(r"sha256:[0-9a-f]{64}", image.get("manifest_digest", "")):
                raise GateError("Observed OCI image digest differs from the build receipt")
            return {"status": "PASS", "reason": "Current admitted context/source and immutable OCI archive were verified", "release_id": manifest.get("releaseId"), "image_digest": image["manifest_digest"]}
        except (GateError, OSError, ValueError, KeyError, tarfile.TarError) as error:
            return {"status": "NOT_PREPARED", "reason": str(error)}

    def verify(self):
        catalogue = read_json(ROOT / "evaluation/gcp-private-acceptance.v1.json")
        gates = catalogue.get("tests", catalogue.get("checks", catalogue.get("gates", [])))
        if isinstance(gates, dict):
            gates = list(gates.values())
        if len(gates) != 41 or len({gate.get("id") for gate in gates}) != 41:
            raise GateError("The pinned catalogue must contain exactly 41 distinct acceptance tests")
        results = []
        for gate in gates:
            results.append({"id": gate.get("id"), "status": "NOT_RUN", "reason": "Requires observed hosted execution; local/mock tests do not establish this gate", "required_for": gate.get("required_for", [])})
        status = self.status()
        if status["status"] == "BLOCKED":
            for result in results:
                result.update(status="BLOCKED", reason="Hosted prerequisites unavailable; cloud deployment and actual private identity/network/persistence not observed")
        verify_helper = ROOT / "scripts/gcp/verify_hosted.py"
        (self.directory / "hosted-results.json").unlink(missing_ok=True)
        if status["status"] == "PASS" and verify_helper.exists():
            observed = self.run([sys.executable, verify_helper, "--config", self.config_path, "--deployment", self.directory / "deployed.json", "--output", self.directory / "hosted-results.json"], timeout=600)
            if (self.directory / "hosted-results.json").exists():
                actual = read_json(self.directory / "hosted-results.json")
                indexed = {r["id"]: r for r in actual["results"]}
                results = [indexed.get(result["id"], result) for result in results]
        prepared = self.prepared_status()
        indexed = {result["id"]: result for result in results}
        by_level = {}
        for level in ("private-transport-smoke-tested", "personal-reference-accepted", "bduk-sandpit-accepted"):
            required_ids = [gate["id"] for gate in gates if level in gate.get("required_for", [])]
            required = [indexed[identifier]["status"] for identifier in required_ids]
            if not required:
                by_level[level] = "NOT_RUN"
            elif "FAIL" in required:
                by_level[level] = "FAIL"
            elif "BLOCKED" in required:
                by_level[level] = "BLOCKED"
            elif "NOT_RUN" in required:
                by_level[level] = "NOT_RUN"
            elif all(outcome == "PASS" for outcome in required):
                by_level[level] = "PASS"
            else:
                # Architecture-specific NOT_APPLICABLE is reviewable evidence,
                # never an implicit waiver of the selected required level.
                by_level[level] = "NOT_RUN"
        acceptance = "prepared-only" if prepared["status"] == "PASS" else "NOT_PREPARED"
        if prepared["status"] == "PASS":
            for level in ("private-transport-smoke-tested", "personal-reference-accepted", "bduk-sandpit-accepted"):
                if by_level[level] == "PASS" and (level != "bduk-sandpit-accepted" or self.config["profile"] == "bduk-sandpit-network-private"):
                    acceptance = level
        selected = "bduk-sandpit-accepted" if self.config["profile"] == "bduk-sandpit-network-private" else "personal-reference-accepted"
        evidence = {"timestamp": timestamp(), "acceptance_level": acceptance, "local_preparation": prepared, "hosted_acceptance": by_level[selected], "hosted_levels": by_level, "results": results}
        write_json(self.directory / "verification.json", evidence)
        return evidence

    def package_approval(self):
        if not (self.directory / "latest-plan.json").exists():
            self.plan()
        plan = read_json(self.directory / "latest-plan.json")
        source = source_manifest(self.config_path)
        if plan.get("bindings", {}).get("source_sha256") != digest(source):
            raise GateError("Review plan source changed; create a current plan before packaging")
        package = self.directory / "platform-review.zip"
        # Membership is exclusively the admitted Git inventory. No filesystem
        # fallback can discover ignored credentials, state or generated tooling.
        root_files = {"evaluation/gcp-private-acceptance.v1.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "package.json", "uv.lock", "pyproject.toml", "docs/decisions/ADR-0019-network-private-gcp-pilot.md", "AGENTS.md", "README.md", "SECURITY.md", "CONTEXT.md", "PROGRESS.md", "LICENSE", "tsconfig.base.json", ".nvmrc", ".node-version", ".python-version", "scripts/build_okf.py", "scripts/okf_plus/build.py", "scripts/okf_plus/verify.py"}
        def reviewable(name):
            if private_source_name(name):
                return False
            if name in root_files or name.startswith(("infra/gcp/", "scripts/gcp/", "docs/deployment/gcp/")):
                return True
            path = Path(name)
            if name.startswith("docs/security/"):
                return path.suffix == ".md"
            if name.startswith((".devcontainer/", "scripts/environment/", "scripts/security/", "docs/development/")):
                return path.suffix in (".py", ".sh", ".md") or path.name in ("Containerfile", ".dockerignore", "devcontainer.json", "toolchain.lock.json") or path.name.endswith(".example.json")
            return (name.startswith(("apps/", "packages/", "tests/deployment/"))
                    and path.suffix in (".ts", ".tsx", ".mjs", ".js", ".py", ".json", ".html", ".css")
                    and not any(part in ("dist", "dist-hosted", "public", "playwright-report", "test-results") for part in path.parts))
        files = [entry for entry in source["files"] if reviewable(entry["path"])]
        redactions = [self.config["project"].get(k) for k in ("id", "number", "expected_account", "billing_account")]
        redactions.extend([self.config.get("identity", {}).get(k) for k in ("oidc_issuer", "client_id", "resource_audience", "secret_reference", "federation_resource")])
        redactions.extend(self.config["network"]["access_principals"] + self.config["network"]["transport_principals"])
        redactions.extend((self.config["identity"].get("claims_mapping") or {}).get("subject_roles", {}))
        redactions.extend((self.config["identity"].get("group_attribute_mapping") or {}).get("roles", {}))
        browser = self.config["identity"].get("browser")
        if browser:
            redactions.extend([browser["client_id"], browser["callback_url"], *browser["allowed_redirect_uris"], *browser["allowed_endpoints"]])
            redactions.append(browser["session_key_secret"]["resource"])
            if browser["client_secret"]:
                redactions.append(browser["client_secret"]["resource"])
        redactions = sorted(set(filter(None, redactions)), key=lambda value: (-len(value), value))
        def sanitise(value):
            if isinstance(value, str):
                for index, secret in enumerate(filter(None, redactions)):
                    value = value.replace(secret, f"REDACTED_INPUT_{index}")
                value = value.replace(str(ROOT), "REPOSITORY")
                return re.sub(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "REDACTED_PRINCIPAL", value)
            if isinstance(value, dict):
                return {sanitise(key): sanitise(child) for key, child in value.items()}
            if isinstance(value, list):
                return [sanitise(child) for child in value]
            return value
        review = {"status": "bduk-ready-for-review; not platform approval or hosted acceptance", "source_revision": source["revision"], "source_manifest_sha256": digest(source), "plan": sanitise(plan), "required_inputs": unresolved(self.config), "cloud_mutations_performed_by_packaging": False, "no_data_payloads_or_credentials": True}
        package_checksums = []
        with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            def add_review_file(name, content, mode=None):
                if not isinstance(content, bytes):
                    content = content.encode()
                info = zipfile.ZipInfo(name)
                info.external_attr = ((mode or 0o100644) & 0xFFFF) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content)
                package_checksums.append({"path": name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
            for entry in files:
                _actual, raw = read_source_file(entry["path"], expected=entry)
                content = raw.decode()
                # Code includes clearly synthetic identity fixtures. Preserve them;
                # redact exact known private inputs only, not arbitrary addresses.
                for index, private_input in enumerate(filter(None, redactions)):
                    content = content.replace(private_input, f"REDACTED_INPUT_{index}")
                add_review_file(entry["path"], content, stat.S_IFREG | entry["mode"])
            add_review_file("review-manifest.json", json.dumps(review, indent=2) + "\n")
            for name in ("verification.json", "local-tests.json", "image.json", "prepared/manifest.json"):
                path = self.directory / name
                if os.path.lexists(path):
                    _entry, raw = read_source_file(path.relative_to(ROOT).as_posix())
                    add_review_file("evidence/" + name, json.dumps(sanitise(json.loads(raw)), indent=2) + "\n")
            add_review_file("SOURCE_REPLAY.md", "# Source replay\n\nThis review package includes the changed application code, deployment code and tests.\nObtain the public repository at source revision `" + source["revision"] + "` in a separate approved workspace, then overlay these reviewed files.\nUse the pinned pnpm/uv tools and frozen lockfiles. Admitted public OKF+ build inputs are a separately validated prerequisite; private original archives are excluded.\nRun prepare only after the source-lock verification and public metadata input inventory succeed.\nThe image/bundle manifest identifies exact payload bytes; no cloud upload or acceptance is implied by this ZIP.\n")
            archive.writestr("package-files.sha256.json", json.dumps(package_checksums, indent=2) + "\n")
        checksum = file_digest(package)
        (package.parent / "platform-review.zip.sha256").write_text(checksum + "  platform-review.zip\n")
        return {"status": "PACKAGE_CREATED", "package": str(package), "sha256": checksum, "hosted_acceptance": "NOT_PROVED"}

    def rollback(self, release_id):
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,100}", release_id or ""):
            raise GateError("Exact recorded release ID required")
        candidates = list((ROOT / "artifacts/gcp").glob(f"*/releases/{release_id}.json"))
        if len(candidates) != 1:
            raise GateError("Recorded compatible release is unavailable or ambiguous")
        release = read_json(candidates[0])
        original_directory = candidates[0].parent.parent
        original_plan = read_json(original_directory / "plans" / f"{release['plan_id']}.json")
        original_approval = read_json(original_directory / "approvals" / f"{release['plan_id']}.approval.json")
        if plan_identity(original_plan) != release["plan_id"] or original_approval.get("status") != "APPROVED" or original_approval.get("bindings") != original_plan["bindings"]:
            raise GateError("Historical release has no intact approved source plan")
        if original_approval.get("kind") != "deploy" or original_approval.get("plan_id") != release["plan_id"] or original_approval.get("approved_by") != original_plan["bindings"]["account"]:
            raise GateError("Historical release approval identity/operation does not match its plan")
        original_approved_at = dt.datetime.fromisoformat(original_approval["approved_at"].replace("Z", "+00:00"))
        original_expiry = dt.datetime.fromisoformat(original_approval["expires_at"].replace("Z", "+00:00"))
        if not original_approved_at < original_expiry <= original_approved_at + dt.timedelta(days=90):
            raise GateError("Historical release approval validity scope is invalid")
        expected_variables = original_plan["desired_variables"]["service"]
        if {key: value for key, value in release["variables"].items() if key not in ("runtime_config_json", "invoker_unique_id")} != {key: value for key, value in expected_variables.items() if key not in ("runtime_config_json", "invoker_unique_id")}:
            raise GateError("Historical service resource/IAM/secret scope differs from its approved plan")
        expected_image = original_plan["desired_variables"]["service"]["image_reference"]
        expected_release = original_plan["upload_inventory"].get("releaseId")
        if release["image_reference"] != expected_image or release["variables"]["image_reference"] != expected_image or release["release_id"] != expected_release or release["variables"]["release_id"] != expected_release:
            raise GateError("Historical release image/bundle identity differs from its approved plan")
        original_runtime = json.loads(json.dumps(original_plan["runtime_template"]))
        recorded_runtime = json.loads(release["variables"]["runtime_config_json"])
        for key in ("transportSubject", "transportAudience", "publicOrigin", "allowedOrigins"):
            original_runtime.pop(key, None)
            recorded_runtime.pop(key, None)
        if original_runtime != recorded_runtime:
            raise GateError("Historical release policy/runtime configuration differs from its approved plan")
        current = read_json(self.directory / "deployed.json")
        if release["service_uri"] != current["service_uri"] or release["variables"]["invoker_unique_id"] != release["foundation"]["invoker_unique_id"]:
            raise GateError("Historical transport target/subject differs from the compatible deployment")
        # Restore immutable released artefacts under current recorded authority;
        # do not require the checkout to become the older source revision.
        plan, approval = self.approved(current["plan_id"], "deploy")
        if "rollback-compatible-release" not in approval.get("actions", []):
            raise GateError("Recorded approval does not cover restoring this release")
        if release["evidence_schema"] != current["evidence_schema"]:
            raise GateError("Evidence migration compatibility is unproved; rollback blocked")
        old_runtime = json.loads(release["variables"]["runtime_config_json"])
        new_runtime = json.loads(current["variables"]["runtime_config_json"])
        expected_origin = browser_public_origin({"callback_url": old_runtime["identity"]["browser"]["callbackUrl"]}) if old_runtime["profile"] == "bduk" else current["service_uri"]
        expected_origins = [expected_origin] if old_runtime["profile"] == "bduk" else ["http://127.0.0.1:8789"]
        if old_runtime.get("transportSubject") != release["foundation"]["invoker_unique_id"] or old_runtime.get("transportAudience") != current["service_uri"] or old_runtime.get("publicOrigin") != expected_origin or old_runtime.get("allowedOrigins") != expected_origins:
            raise GateError("Historical output-bound runtime identity/origin is incompatible")
        if old_runtime.get("evidence") != new_runtime.get("evidence") or release["foundation"] != current["foundation"]:
            raise GateError("Rollback would change evidence identity or platform ownership")
        actual = self.terraform_plan("service", release["variables"])
        self.service_scope(actual)
        self.apply_saved("service", {"terraform": {"service": actual}})
        observed = self.outputs("service")
        release["revision"] = observed["latest_revision"]
        release["rollback_authority_plan_id"] = current["plan_id"]
        write_json(self.directory / "deployed.json", release)
        return {"status": "ROLLED_BACK_NOT_VERIFIED", "release_id": release_id, "evidence_retained": True}

    def destroy(self, plan_id):
        plan, approval = self.approved(plan_id, "destroy")
        if "destroy-owned-pilot-retain-evidence" not in approval.get("actions", []):
            raise GateError("Approval lacks explicit destructive authority")
        # Cloud Run deletion protection is removed only inside this explicitly
        # approved destructive operation; retained storage is never targeted.
        if "service" in plan["terraform"]:
            variables = read_json(self.iac_root("service") / "inputs.auto.tfvars.json")
            variables["deletion_protection"] = False
            unlock = self.terraform_plan("service", variables)
            self.service_scope(unlock)
            self.apply_saved("service", {"terraform": {"service": unlock}})
            destroy_plan = self.terraform_plan("service", variables, destroy=True)
            self.service_scope(destroy_plan, deleting=True)
            self.apply_saved("service", {"terraform": {"service": destroy_plan}}, "destroy.tfplan")
        if "foundation" in plan["terraform"]:
            self.apply_saved("foundation", plan, "destroy.tfplan")
        result = {"status": "OWNED_RUNTIME_DESTROYED_NOT_VERIFIED", "retained": ["Firestore evidence and PITR", "private backup bucket and object versions", "enabled APIs", "logs according to platform retention"], "residual_costs": "Firestore storage/PITR, backup objects and retained logs; inspect actual billing", "whole_project_deleted": False}
        write_json(self.directory / "destroy-results.json", result)
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="ignored private JSON config")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("--approved-plan")
    parser.add_argument("--release")
    parser.add_argument("--destroy", action="store_true", help="plan an explicit destructive operation")
    args = parser.parse_args(argv)
    try:
        lifecycle = Lifecycle(args.config)
        method = getattr(lifecycle, args.command.replace("-", "_"))
        if args.command in ("apply", "destroy"):
            result = method(args.approved_plan)
        elif args.command == "rollback":
            result = method(args.release)
        elif args.command == "plan":
            result = method(args.destroy)
        elif args.command == "connect":
            result = method(args.approved_plan)
        else:
            result = method()
        # Keep rich principal/resource details in private evidence; the owner gets
        # exact scoped plans via the plan artifact and URLs only after deployment.
        if args.command == "plan":
            result = {"plan_id": result["plan_id"], "kind": result["kind"], "blockers": result["blockers"], "cost": result["cost"], "plan_path": str(lifecycle.directory / "latest-plan.json"), "approval_template": str(lifecycle.directory / "approvals" / (result["plan_id"] + ".template.json"))}
        print(json.dumps(result, indent=2))
        if args.command == "verify" and any(item["status"] in ("FAIL", "BLOCKED", "NOT_RUN") for item in result["results"]):
            return 2
        if args.command == "preflight" and any(item["status"] == "BLOCKED" for item in result["checks"]):
            return 2
        if args.command == "plan" and result["blockers"]:
            return 2
        return 0
    except (GateError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "BLOCKED", "reason": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
