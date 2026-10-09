#!/usr/bin/env python3
"""Read-only hosted observations and approval-scoped public-capture MCP checks.

This never opens a tunnel, publishes a revision, modifies IAM or replaces state.
Real cloud prerequisites and identity bindings remain necessary. Public metadata
responses are bounded and hashed; tokens and response payloads are not journalled.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "evaluation/gcp-private-acceptance.v1.json"
MAX_RESPONSE = 1_100_000
TOKEN_BINDINGS = ("GIS_GCP_ALLOWED_IDENTITY_TOKEN", "GIS_GCP_FORBIDDEN_IDENTITY_TOKEN",
                  "GIS_GCP_READER_IDENTITY_TOKEN", "GIS_GCP_TRANSPORT_TOKEN")


def read_json(path):
    return json.loads(Path(path).read_text())


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temp.chmod(0o600)
    temp.replace(path)


def origin(value, *, personal=False):
    parsed = urlsplit(value)
    if parsed.username or parsed.password or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError("Private probe URL must be one fixed origin")
    if personal:
        if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.port != 8789:
            raise ValueError("Personal verification requires the reviewed 127.0.0.1:8789 tunnel")
    elif parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Platform verification requires an approved HTTPS origin")
    return value.rstrip("/")


def http_probe(base, path, *, token=None, extra_headers=None, method="GET", body=None):
    """Never follow redirects or log bearer credentials and response contents."""
    target = urlsplit(base)
    headers = {"accept": "application/json", **(extra_headers or {})}
    if token:
        headers["authorization"] = "Bearer " + token
    if body is not None:
        headers["content-type"] = "application/json"
    cls = http.client.HTTPSConnection if target.scheme == "https" else http.client.HTTPConnection
    connection = cls(target.hostname, target.port, timeout=15,
                     **({"context": ssl.create_default_context()} if target.scheme == "https" else {}))
    try:
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        raw = response.read(MAX_RESPONSE + 1)
        if len(raw) > MAX_RESPONSE:
            return {"status": "FAIL", "reason": "Hosted response exceeds verifier bound"}
        content_type = response.getheader("content-type", "").split(";")[0].lower()
        result = {"status": "OBSERVED", "http_status": response.status, "content_type": content_type,
                  "body_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        if content_type == "application/json":
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    result["json"] = parsed
            except (UnicodeDecodeError, ValueError):
                result.update(status="FAIL", reason="Malformed JSON hosted response")
        return result
    except (OSError, http.client.HTTPException):
        return {"status": "BLOCKED", "reason": "Private route unavailable or TLS/HTTP request failed; establish reviewed connection"}
    finally:
        connection.close()


def cloud_read(config, args):
    if not shutil.which("gcloud"):
        return None
    project = config.get("project", {})
    if not project.get("id") or not project.get("expected_account"):
        return None
    try:
        result = subprocess.run(["gcloud", *args, "--project", project["id"], "--account", project["expected_account"], "--quiet"],
                                capture_output=True, text=True, timeout=45, check=False)
        return json.loads(result.stdout) if result.returncode == 0 else None
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def catalogue_results():
    tests = read_json(CATALOGUE)["tests"]
    ids = [item["id"] for item in tests]
    if len(ids) != 41 or len(set(ids)) != 41:
        raise ValueError("Canonical 41-gate acceptance catalogue missing or duplicated")
    return {item["id"]: {"id": item["id"], "status": "BLOCKED", "required_for": item["required_for"],
                         "reason": "Required observed acceptance evidence is unavailable", "evidence": []} for item in tests}


def public_observation(value):
    return {key: item for key, item in value.items() if key != "json"}


def exact_release(probe, deployment):
    return (probe.get("status") == "OBSERVED" and probe.get("http_status") == 200
            and probe.get("content_type") == "application/json"
            and probe.get("json", {}).get("schema") == "gis-ai-go.gcp-knowledge-release.v1"
            and probe["json"].get("release_sha256") == deployment.get("release_id"))


def observed_revision(service):
    if not isinstance(service, dict):
        return None, False
    status = service.get("status", {})
    latest = status.get("latestReadyRevisionName") or service.get("latestReadyRevision")
    traffic = status.get("traffic", service.get("trafficStatuses", []))
    sole = len(traffic) == 1 and traffic[0].get("percent") == 100 and (
        traffic[0].get("revisionName") == latest or traffic[0].get("revision") == latest)
    return latest, bool(latest and sole)


def exact_cloud_deployment(service, deployment):
    """A loopback response alone cannot establish a hosted Cloud Run result."""
    if not isinstance(service, dict):
        return False
    status = service.get("status", {})
    uri = status.get("url", service.get("uri"))
    revision, sole = observed_revision(service)
    expected_revision = deployment.get("revision")
    containers = service.get("spec", {}).get("template", {}).get("spec", {}).get("containers")
    if containers is None:
        containers = service.get("template", {}).get("containers", [])
    image = containers[0].get("image") if isinstance(containers, list) and len(containers) == 1 else None
    expected_image = deployment.get("image_reference", "")
    ready = any(item.get("type") == "Ready" and item.get("status") == "True" for item in status.get("conditions", []))
    if not status:
        ready = service.get("terminalCondition", {}).get("state") == "CONDITION_SUCCEEDED"
    return bool(uri == deployment.get("service_uri") and isinstance(expected_image, str)
                and re.fullmatch(r"[a-z0-9.-]+/[A-Za-z0-9._/-]+@sha256:[0-9a-f]{64}", expected_image)
                and image == expected_image and revision and expected_revision
                and revision.split("/")[-1] == expected_revision.split("/")[-1] and sole and ready)


def known_records(directory):
    rows = []
    try:
        for bundle in ("okf", "okf-plus"):
            body = read_json(directory / "prepared/context/app/bundles" / bundle / "okf-bundle.json")
            record = body["records"][0]
            rows.append({"bundle": bundle, "id": record.get("id", record.get("@id"))})
    except (OSError, ValueError, KeyError, IndexError):
        return []
    return rows


def validate_transport_token(deployment, canonical, directory, environment):
    input_path, result_path = directory / "transport-probe-input.json", directory / "transport-token-observation.json"
    save_json(input_path, {"mode": "transport-token-validation", "audience": canonical,
                           "expected_subject": deployment.get("foundation", {}).get("invoker_unique_id")})
    result_path.unlink(missing_ok=True)
    try:
        result = subprocess.run(["node", str(ROOT / "scripts/gcp/verify_mcp.mjs"), "--input", str(input_path), "--output", str(result_path)],
                                capture_output=True, text=True, timeout=15, check=False, env=environment)
        return result.returncode == 0 and read_json(result_path).get("valid") is True
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def validate_forbidden_identity(deployment, directory, environment):
    """Distinguish a real unadmitted principal from an invalid credential."""
    try:
        runtime = json.loads(deployment["variables"]["runtime_config_json"])
        identity = runtime["identity"]
        if identity.get("mode") != "oidc":
            return {"valid": False, "has_granted_roles": False}
    except (KeyError, TypeError, ValueError):
        return {"valid": False, "has_granted_roles": False}
    input_path, result_path = directory / "forbidden-probe-input.json", directory / "forbidden-identity-observation.json"
    save_json(input_path, {"mode": "application-identity-validation", "identity": identity})
    result_path.unlink(missing_ok=True)
    try:
        result = subprocess.run(["node", str(ROOT / "scripts/gcp/verify_mcp.mjs"), "--input", str(input_path), "--output", str(result_path)],
                                capture_output=True, text=True, timeout=15, check=False, env=environment)
        verified = read_json(result_path)
        return {"valid": result.returncode == 0 and verified.get("valid") is True,
                "has_granted_roles": verified.get("has_granted_roles") is not False}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return {"valid": False, "has_granted_roles": False}


def verify(config, deployment, output, *, environment=None, probe=http_probe, read_cloud=cloud_read):
    environment = os.environ if environment is None else environment
    output = Path(output)
    results = catalogue_results()
    observations = {}
    def record(identifier, status, reason, *evidence):
        results[identifier].update(status=status, reason=reason, evidence=list(evidence))
    personal = config.get("profile") == "personal-network-private"
    try:
        base = origin(environment.get("GIS_GCP_PRIVATE_BASE_URL", "http://127.0.0.1:8789" if personal else deployment.get("service_uri", "")), personal=personal)
        canonical = origin(deployment.get("service_uri", ""))
        if not re.fullmatch(r"https://[a-z0-9-]+(?:\.[a-z0-9-]+)*\.run\.app", canonical):
            raise ValueError("Actual canonical Cloud Run service URI required")
    except ValueError:
        record("NET01", "BLOCKED", "No observed deployment URI and approved private connection; no network request issued")
        return finish(results, observations, config, deployment, output, environment)
    allowed = environment.get("GIS_GCP_ALLOWED_IDENTITY_TOKEN")
    release = probe(base, "/api/release", token=allowed)
    observations["release"] = public_observation(release)
    homepage = probe(base, "/", token=allowed, extra_headers={"accept": "text/html"})
    observations["homepage"] = public_observation(homepage)
    release_ok = exact_release(release, deployment)
    if not release_ok:
        record("NET01", "BLOCKED" if release.get("status") == "BLOCKED" else "FAIL", "Private route did not return the exact approved application release", "observations.release")
        return finish(results, observations, config, deployment, output, environment)
    if homepage.get("http_status") != 200 or homepage.get("content_type") != "text/html":
        record("NET01", "FAIL", "Approved knowledge responds but current website does not", "observations.homepage")
    record("KNOW04", "PASS" if release["json"].get("bundles") and all(row.get("grain") == "catalogue-representations-not-unique-datasets" for row in release["json"]["bundles"]) else "FAIL", "Hosted release explicitly distinguishes catalogue representations and refuses live-provider claims", "observations.release")
    forbidden = environment.get("GIS_GCP_FORBIDDEN_IDENTITY_TOKEN")
    if forbidden:
        denied = probe(base, "/api/release", token=forbidden)
        observations["forbidden_identity"] = public_observation(denied)
        verified = validate_forbidden_identity(deployment, output.parent, environment)
        observations["forbidden_identity_validation"] = verified
        if verified["valid"] and not verified["has_granted_roles"]:
            record("AUTH02", "PASS" if denied.get("http_status") == 403 else "FAIL", "Allowed principal and independently verified signed principal with no granted roles were exercised", "observations.release", "observations.forbidden_identity", "observations.forbidden_identity_validation")
        else:
            record("AUTH02", "BLOCKED", "Supplied token is invalid, unverifiable or maps to a granted role; refusal does not prove a forbidden real identity", "observations.forbidden_identity", "observations.forbidden_identity_validation")
    else:
        record("AUTH02", "BLOCKED", "Allowed identity observed; separately supplied forbidden real identity binding absent")
    spoofed = probe(base, "/api/release", token=allowed, extra_headers={"x-gis-role": "owner", "x-user-email": "synthetic@example.invalid"})
    observations["spoofed_headers"] = public_observation(spoofed)
    record("AUTH03", "BLOCKED", "Spoofed-header refusal observed; separately signed wrong-issuer/audience/expired identity samples remain required", "observations.spoofed_headers")
    if spoofed.get("http_status") not in (400, 401, 403):
        record("AUTH03", "FAIL", "Spoofed identity headers were not refused", "observations.spoofed_headers")
    service = read_cloud(config, ["run", "services", "describe", config["operations"]["name_prefix"], "--region", config["project"]["region"], "--format=json"])
    revision, sole_revision = observed_revision(service)
    cloud_verified = exact_cloud_deployment(service, deployment)
    observations["service"] = {"read_observed": service is not None, "revision": revision, "sole_revision_traffic_verified": sole_revision,
                               "exact_deployment_verified": cloud_verified}
    if service is None:
        record("NET03", "BLOCKED", "Cloud Run actual ingress, approved source DNS/routing and platform topology require read access and in-VPC observations")
    else:
        annotations = service.get("metadata", {}).get("annotations", {})
        ingress = annotations.get("run.googleapis.com/ingress", service.get("ingress"))
        observations["service"]["ingress"] = ingress
        record("NET03", "FAIL" if ingress not in ("internal", "INGRESS_TRAFFIC_INTERNAL_ONLY") else "BLOCKED", "Actual ingress checked; effective in-VPC DNS/routing and unauthorised other-project source still require independent observations", "observations.service")
    if personal:
        vm = read_cloud(config, ["compute", "instances", "describe", deployment.get("foundation", {}).get("access_vm", ""), "--zone", config["network"].get("access_vm_zone") or "UNRESOLVED", "--format=json(networkInterfaces,tags.items,status)"])
        observations["access_vm"] = {"read_observed": vm is not None, "has_external_ip": any(interface.get("accessConfigs") for interface in (vm or {}).get("networkInterfaces", []))}
        record("NET04", "FAIL" if observations["access_vm"]["has_external_ip"] else "BLOCKED", "No-external-IP observation does not establish effective firewall or remote loopback-only proxy listener", "observations.access_vm")
    else:
        for identifier in ("NET04", "NET05"):
            record(identifier, "NOT_APPLICABLE", "BDUK consumes approved platform private networking and creates no personal access VM or IAP tunnel")
    # Never pass generic public 403 as network privacy. A valid invocation token
    # needs independent signature/subject/audience verification and an observed
    # outside-source topology; their absence remains an explicit blocked gate.
    if environment.get("GIS_GCP_TRANSPORT_TOKEN"):
        transport_valid = validate_transport_token(deployment, canonical, output.parent, environment)
        observations["outside_transport"] = {"signature_issuer_audience_expiry_subject_verified": transport_valid}
        if transport_valid:
            outside = probe(canonical, "/api/release", token=allowed, extra_headers={
                "x-serverless-authorization": "Bearer " + environment["GIS_GCP_TRANSPORT_TOKEN"],
                "x-gis-invocation-proof": environment["GIS_GCP_TRANSPORT_TOKEN"]})
            observations["outside"] = public_observation(outside)
            if outside.get("http_status") == 200:
                record("NET02", "FAIL", "Outside canonical path returned content with a verified valid invocation credential", "observations.outside")
            else:
                record("NET02", "BLOCKED", "Valid invocation credential and no content observed outside; independent outside-source topology and IAM-versus-ingress denial evidence still required. A 403 alone cannot prove network privacy", "observations.outside", "observations.outside_transport")
        else:
            record("NET02", "BLOCKED", "Supplied transport token signature/issuer/audience/expiry/exact subject could not be verified; no public request issued", "observations.outside_transport")
    else:
        record("NET02", "BLOCKED", "GIS_GCP_TRANSPORT_TOKEN binding absent; valid-credential outside-path test not possible")
    probe_input = {"endpoint": base + "/mcp", "release_id": deployment.get("release_id"), "known_records": known_records(output.parent),
                   "observed_revision": revision, "single_current_revision_verified": sole_revision,
                   "evidence_writes_authorised": cloud_verified and deployment.get("verification_evidence_writes_authorised") is True}
    input_path, sdk_path = output.parent / "hosted-probe-input.json", output.parent / "hosted-sdk-observations.json"
    save_json(input_path, probe_input)
    sdk_path.unlink(missing_ok=True)
    try:
        completed = subprocess.run(["node", str(ROOT / "scripts/gcp/verify_mcp.mjs"), "--input", str(input_path), "--output", str(sdk_path)],
                                   capture_output=True, text=True, timeout=180, check=False, env=environment)
        sdk = read_json(sdk_path).get("observations", {}) if sdk_path.exists() else {}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        sdk = {}
    observations["sdk"] = sdk
    if sdk.get("negotiation", {}).get("status") == "PASS":
        record("MCP01", "PASS", "Independent pinned SDK negotiated the actual modern protocol through the private route", "observations.sdk.negotiation")
        record("MCP04", "PASS", "Protocol evidence comes from SDK negotiation and discovery, separate from HTTP health/homepage", "observations.sdk.negotiation", "observations.sdk.discovery")
        if homepage.get("http_status") == 200:
            record("NET01", "PASS", "Exact approved release, current website and actual SDK MCP respond through the selected private connection", "observations.release", "observations.homepage", "observations.sdk.negotiation")
    if sdk.get("evidence", {}).get("status") == "PASS":
        record("MCP02", "PASS", "Discovered and invoked captured-data tool; separately inspected structurally verified linked receipt", "observations.sdk.evidence")
    if sdk.get("both_bundles", {}).get("status") == "PASS":
        record("KNOW01", "BLOCKED", "Known record from both bundles observed via MCP; record-specific browser/UI interaction remains unobserved", "observations.sdk.both_bundles")
        record("KNOW02", "BLOCKED", "Exact release and source records observed; full source/rights/freshness/gap interpretation remains a required acceptance check", "observations.sdk.both_bundles")
    for identifier, name in (("POL01", "reader_discovery"), ("POL02", "reader_direct_refusal"), ("STATE01", "persisted_receipt")):
        item = sdk.get(name)
        if item:
            record(identifier, item["status"], item.get("reason", "Actual independent hosted probe observed"), "observations.sdk." + name)
    if sdk.get("concurrent_idempotency", {}).get("status") == "PASS":
        record("STATE02", "BLOCKED", "Concurrent duplicate/replay and conflicting fingerprint observed; separate authorised principal ownership test still required", "observations.sdk.concurrent_idempotency")
    if personal:
        record("AUTH05", "NOT_APPLICABLE", "Personal reference profile makes no BDUK Okta claim; actual sandpit claims/revocation remain required for BDUK acceptance")
    record("AUTH01", "BLOCKED", "Transport and application identity modes are distinct in configuration; human identity verification is not inferred from access VM transport")
    record("MCP03", "BLOCKED", "Malformed input subcheck available; real in-flight cancellation and all unsupported protocol/streaming cases remain required", "observations.sdk.malformed_input")
    if not cloud_verified:
        # Retain wire observations, but never promote a local/mock endpoint to a
        # hosted acceptance gate while the real cloud target remains unverified.
        for item in results.values():
            if item["status"] == "PASS":
                item.update(status="BLOCKED", reason="Probe succeeded, but actual Cloud Run URI, immutable image, ready revision and sole 100% traffic do not match the recorded deployment; hosted result unproved")
    return finish(results, observations, config, deployment, output, environment)


def finish(results, observations, config, deployment, output, environment):
    value = {"schema": "gis-ai-go.gcp-hosted-verification.v1", "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
             "local_mock": False, "acceptance_level": "prepared-only", "hosted_acceptance": "NOT_ACCEPTED",
             "profile": config.get("profile"), "deployment_release": deployment.get("release_id"),
             "credential_bindings_present": {name: bool(environment.get(name)) for name in TOKEN_BINDINGS},
             "results": list(results.values()), "observations": observations,
             "limits": ["No cloud resource mutation, automatic tunnel or restart performed by verifier.",
                        "Optional captured-data query writes require recorded approval scope.",
                        "Partial subchecks do not pass a wider required gate.",
                        "Local fixture tests never establish hosted authentication, persistence or BDUK acceptance."]}
    save_json(output, value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("config", "deployment", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    try:
        evidence = verify(read_json(args.config), read_json(args.deployment), args.output)
    except (OSError, ValueError, KeyError):
        evidence = finish(catalogue_results(), {}, {}, {}, args.output, os.environ)
    print(json.dumps({"status": "OBSERVED_NOT_ACCEPTED", "evidence": str(Path(args.output)), "gate_count": len(evidence["results"])}))
    return 2 if any(item["status"] in ("FAIL", "BLOCKED", "NOT_RUN") for item in evidence["results"] if item["required_for"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
