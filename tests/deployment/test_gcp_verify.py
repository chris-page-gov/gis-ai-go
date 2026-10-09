"""Verifier control/evidence tests; these never claim hosted GCP acceptance."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import threading
import tempfile
import unittest
import subprocess
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gcp_hosted_verify", ROOT / "scripts/gcp/verify_hosted.py")
verify_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_module)



class HostedVerificationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.tmp_path = Path(temporary.name)

    def test_full_catalogue_remains_blocked_without_deployment(self):
        tmp_path = self.tmp_path
        calls = []
        report = verify_module.verify({"profile": "personal-network-private"}, {}, tmp_path / "results.json", environment={},
                                      probe=lambda *args, **kwargs: calls.append(args), read_cloud=lambda *args: None)
        assert len(report["results"]) == 41
        assert len({row["id"] for row in report["results"]}) == 41
        assert {row["status"] for row in report["results"]} == {"BLOCKED"}
        assert report["local_mock"] is False
        assert report["hosted_acceptance"] == "NOT_ACCEPTED"
        assert calls == []


    def test_arbitrary_private_target_rejected_before_network(self):
        tmp_path = self.tmp_path
        calls = []
        report = verify_module.verify({"profile": "personal-network-private"}, {"service_uri": "https://pilot.run.app"},
                                      tmp_path / "results.json", environment={"GIS_GCP_PRIVATE_BASE_URL": "http://192.168.1.1:8789"},
                                      probe=lambda *args, **kwargs: calls.append(args))
        assert calls == []
        assert next(row for row in report["results"] if row["id"] == "NET01")["status"] == "BLOCKED"


    def test_http_200_homepage_is_never_exact_knowledge_release(self):
        deployment = {"release_id": "a" * 64}
        assert not verify_module.exact_release({"status": "OBSERVED", "http_status": 200, "content_type": "text/html"}, deployment)
        response = {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
            "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "b" * 64}}
        assert not verify_module.exact_release(response, deployment)
        response["json"]["release_sha256"] = "a" * 64
        assert verify_module.exact_release(response, deployment)


    def test_revision_replacement_requires_sole_observed_serving_revision(self):
        assert verify_module.observed_revision(None) == (None, False)
        latest = "pilot-00002-abc"
        assert verify_module.observed_revision({"status": {"latestReadyRevisionName": latest}}) == (latest, False)
        assert verify_module.observed_revision({"status": {"latestReadyRevisionName": latest, "traffic": [
            {"revisionName": latest, "percent": 99}, {"revisionName": "pilot-00001-def", "percent": 1}]}}) == (latest, False)
        assert verify_module.observed_revision({"status": {"latestReadyRevisionName": latest, "traffic": [
            {"revisionName": "pilot-00001-def", "percent": 100}]}}) == (latest, False)
        assert verify_module.observed_revision({"status": {"latestReadyRevisionName": latest, "traffic": [
            {"revisionName": latest, "percent": 100}]}}) == (latest, True)

    def test_hosted_target_requires_exact_uri_image_revision_readiness_and_traffic(self):
        deployment = {"service_uri": "https://pilot.run.app", "revision": "pilot-00002-abc",
                      "image_reference": "europe-west2-docker.pkg.dev/synthetic/pilot/gateway@sha256:" + "a" * 64}
        service = {"status": {"url": deployment["service_uri"], "latestReadyRevisionName": deployment["revision"],
                   "conditions": [{"type": "Ready", "status": "True"}],
                   "traffic": [{"revisionName": deployment["revision"], "percent": 100}]},
                   "spec": {"template": {"spec": {"containers": [{"image": deployment["image_reference"]}]}}}}
        assert verify_module.exact_cloud_deployment(service, deployment)
        import copy
        for field in ("uri", "image", "revision", "ready", "traffic"):
            with self.subTest(field=field):
                modified = copy.deepcopy(service)
                if field == "uri": modified["status"]["url"] = "https://different.run.app"
                if field == "image": modified["spec"]["template"]["spec"]["containers"][0]["image"] = "unapproved:tag"
                if field == "revision": modified["status"]["latestReadyRevisionName"] = "pilot-00003-def"
                if field == "ready": modified["status"]["conditions"][0]["status"] = "False"
                if field == "traffic": modified["status"]["traffic"][0]["percent"] = 99
                assert not verify_module.exact_cloud_deployment(modified, deployment)


    def test_real_local_http_probe_never_follows_token_bearing_redirect(self):
        observed = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_GET(self):
                observed.append((self.path, self.headers.get("Authorization")))
                self.send_response(302)
                self.send_header("Location", "/stolen")
                self.send_header("Content-Length", "0")
                self.end_headers()
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = verify_module.http_probe("http://127.0.0.1:" + str(server.server_port), "/start", token="synthetic-never-real")
            assert result["http_status"] == 302
            assert observed == [("/start", "Bearer synthetic-never-real")]
            assert "synthetic-never-real" not in json.dumps(result)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


    def test_response_payload_and_token_never_written_to_evidence(self):
        tmp_path = self.tmp_path
        secret = "synthetic-secret-value-never-a-real-token"
        config = {"profile": "personal-network-private"}
        def fixture_probe(*args, **kwargs):
            return {"status": "OBSERVED", "http_status": 200, "content_type": "text/html", "json": {"untrusted": secret}}
        report = verify_module.verify(config, {"service_uri": "https://pilot.run.app", "release_id": "a" * 64}, tmp_path / "results.json",
                                      environment={"GIS_GCP_ALLOWED_IDENTITY_TOKEN": secret}, probe=fixture_probe)
        assert secret not in json.dumps(report)
        assert secret not in (tmp_path / "results.json").read_text()
        assert report["credential_bindings_present"]["GIS_GCP_ALLOWED_IDENTITY_TOKEN"] is True
        assert report["results"][6]["status"] != "PASS"


    def test_missing_transport_verification_never_sends_public_credential(self):
        tmp_path = self.tmp_path
        config = {"profile": "personal-network-private", "project": {"region": "europe-west2"},
                  "operations": {"name_prefix": "pilot"}, "network": {"access_vm_zone": "europe-west2-a"}}
        deployment = {"service_uri": "https://pilot.run.app", "release_id": "a" * 64, "foundation": {"access_vm": "pilot-access"}}
        targets = []
        def fixture_probe(base, path, **kwargs):
            targets.append(base)
            if path == "/api/release" and not kwargs.get("extra_headers"):
                return {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
                    "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "a" * 64,
                    "bundles": [{"grain": "catalogue-representations-not-unique-datasets"}]}}
            return {"status": "OBSERVED", "http_status": 400, "content_type": "application/json", "json": {}}
        with mock.patch.object(verify_module, "validate_transport_token", return_value=False), mock.patch.object(verify_module.subprocess, "run", side_effect=OSError("fixture")):
            report = verify_module.verify(config, deployment, tmp_path / "results.json", environment={"GIS_GCP_TRANSPORT_TOKEN": "synthetic-invalid"},
                                          probe=fixture_probe, read_cloud=lambda *args: None)
        assert all(target == "http://127.0.0.1:8789" for target in targets)
        assert next(row for row in report["results"] if row["id"] == "NET02")["status"] == "BLOCKED"
        assert next(row for row in report["results"] if row["id"] == "MCP01")["status"] == "BLOCKED"


    def test_forbidden_403_is_not_network_privacy_pass(self):
        tmp_path = self.tmp_path
        config = {"profile": "personal-network-private", "project": {"region": "europe-west2"},
                  "operations": {"name_prefix": "pilot"}, "network": {"access_vm_zone": "europe-west2-a"}}
        deployment = {"service_uri": "https://pilot.run.app", "release_id": "a" * 64, "foundation": {"access_vm": "pilot-access"}}
        def fixture_probe(base, path, **kwargs):
            if base.startswith("https:"):
                return {"status": "OBSERVED", "http_status": 403, "content_type": "text/html"}
            if path == "/api/release" and not kwargs.get("extra_headers"):
                return {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
                    "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "a" * 64,
                    "bundles": [{"grain": "catalogue-representations-not-unique-datasets"}]}}
            return {"status": "OBSERVED", "http_status": 400, "content_type": "application/json", "json": {}}
        with mock.patch.object(verify_module, "validate_transport_token", return_value=True), mock.patch.object(verify_module.subprocess, "run", side_effect=OSError("fixture")):
            report = verify_module.verify(config, deployment, tmp_path / "results.json", environment={"GIS_GCP_TRANSPORT_TOKEN": "synthetic-valid-for-fixture"},
                                          probe=fixture_probe, read_cloud=lambda *args: None)
        network = next(row for row in report["results"] if row["id"] == "NET02")
        assert network["status"] == "BLOCKED"
        assert "403 alone" in network["reason"]

    def test_invalid_token_refusal_does_not_pass_real_forbidden_identity(self):
        config = {"profile": "personal-network-private", "project": {"region": "europe-west2"},
                  "operations": {"name_prefix": "pilot"}, "network": {"access_vm_zone": "europe-west2-a"}}
        identity = {"mode": "oidc", "issuer": "https://synthetic.invalid", "audience": "synthetic-audience",
                    "jwksUri": "https://synthetic.invalid/keys", "subjectRoles": {}, "groupRoles": {}}
        deployment = {"service_uri": "https://pilot.run.app", "release_id": "a" * 64,
                      "variables": {"runtime_config_json": json.dumps({"identity": identity})},
                      "foundation": {"access_vm": "pilot-access"}}
        environment = {**os.environ, "GIS_GCP_FORBIDDEN_IDENTITY_TOKEN": "not-a-signed-token"}
        # The actual native verifier rejects malformed JWT before a JWKS request.
        verified = verify_module.validate_forbidden_identity(deployment, self.tmp_path, environment)
        assert verified == {"valid": False, "has_granted_roles": False}
        def fixture_probe(base, path, **kwargs):
            if kwargs.get("token") == "not-a-signed-token":
                return {"status": "OBSERVED", "http_status": 401, "content_type": "application/json", "json": {}}
            if path == "/api/release" and not kwargs.get("extra_headers"):
                return {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
                    "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "a" * 64,
                    "bundles": [{"grain": "catalogue-representations-not-unique-datasets"}]}}
            return {"status": "OBSERVED", "http_status": 400, "content_type": "application/json", "json": {}}
        with mock.patch.object(verify_module, "validate_forbidden_identity", return_value=verified), mock.patch.object(verify_module.subprocess, "run", side_effect=OSError("fixture")):
            report = verify_module.verify(config, deployment, self.tmp_path / "results.json", environment=environment,
                                          probe=fixture_probe, read_cloud=lambda *args: None)
        gate = next(row for row in report["results"] if row["id"] == "AUTH02")
        assert gate["status"] == "BLOCKED"
        assert "invalid" in gate["reason"]

    def test_forbidden_identity_pass_requires_verified_no_roles_and_policy_403(self):
        config = {"profile": "personal-network-private", "project": {"region": "europe-west2"},
                  "operations": {"name_prefix": "pilot"}, "network": {"access_vm_zone": "europe-west2-a"}}
        deployment = {"service_uri": "https://pilot.run.app", "release_id": "a" * 64, "foundation": {"access_vm": "pilot-access"},
                      "revision": "pilot-00002-abc", "image_reference": "europe-west2-docker.pkg.dev/synthetic/pilot/gateway@sha256:" + "a" * 64}
        service = {"status": {"url": deployment["service_uri"], "latestReadyRevisionName": deployment["revision"],
                   "conditions": [{"type": "Ready", "status": "True"}],
                   "traffic": [{"revisionName": deployment["revision"], "percent": 100}]},
                   "spec": {"template": {"spec": {"containers": [{"image": deployment["image_reference"]}]}}}}
        for verified, expected in (({"valid": False, "has_granted_roles": False}, "BLOCKED"),
                                   ({"valid": True, "has_granted_roles": True}, "BLOCKED"),
                                   ({"valid": True, "has_granted_roles": False}, "PASS")):
            with self.subTest(verified=verified):
                def fixture_probe(base, path, **kwargs):
                    if kwargs.get("token") == "synthetic-forbidden-binding":
                        return {"status": "OBSERVED", "http_status": 403, "content_type": "application/json", "json": {}}
                    if path == "/api/release" and not kwargs.get("extra_headers"):
                        return {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
                            "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "a" * 64,
                            "bundles": [{"grain": "catalogue-representations-not-unique-datasets"}]}}
                    return {"status": "OBSERVED", "http_status": 400, "content_type": "application/json", "json": {}}
                with mock.patch.object(verify_module, "validate_forbidden_identity", return_value=verified), mock.patch.object(verify_module.subprocess, "run", side_effect=OSError("fixture")):
                    report = verify_module.verify(config, deployment, self.tmp_path / "results.json", environment={"GIS_GCP_FORBIDDEN_IDENTITY_TOKEN": "synthetic-forbidden-binding"},
                                                  probe=fixture_probe, read_cloud=lambda *args: service)
                assert next(row for row in report["results"] if row["id"] == "AUTH02")["status"] == expected

    def test_successful_local_wire_probes_cannot_claim_hosted_pass_without_cloud_observation(self):
        config = {"profile": "personal-network-private", "project": {"region": "europe-west2"},
                  "operations": {"name_prefix": "pilot"}, "network": {"access_vm_zone": "europe-west2-a"}}
        deployment = {"service_uri": "https://pilot.run.app", "release_id": "a" * 64,
                      "verification_evidence_writes_authorised": True, "foundation": {"access_vm": "pilot-access"}}
        def fixture_probe(base, path, **kwargs):
            if path == "/api/release" and not kwargs.get("extra_headers"):
                return {"status": "OBSERVED", "http_status": 200, "content_type": "application/json", "json": {
                    "schema": "gis-ai-go.gcp-knowledge-release.v1", "release_sha256": "a" * 64,
                    "bundles": [{"grain": "catalogue-representations-not-unique-datasets"}]}}
            if path == "/":
                return {"status": "OBSERVED", "http_status": 200, "content_type": "text/html"}
            return {"status": "OBSERVED", "http_status": 400, "content_type": "application/json", "json": {}}
        def fixture_sdk(command, **kwargs):
            Path(command[command.index("--output") + 1]).write_text(json.dumps({"observations": {
                name: {"status": "PASS"} for name in ("negotiation", "discovery", "evidence", "both_bundles", "reader_discovery", "reader_direct_refusal", "persisted_receipt")}}))
            return subprocess.CompletedProcess(command, 0, "", "")
        with mock.patch.object(verify_module.subprocess, "run", side_effect=fixture_sdk):
            report = verify_module.verify(config, deployment, self.tmp_path / "results.json", environment={},
                                          probe=fixture_probe, read_cloud=lambda *args: None)
        assert len(report["results"]) == 41
        assert not any(row["status"] == "PASS" for row in report["results"])
        assert report["observations"]["sdk"]["negotiation"]["status"] == "PASS"
        assert report["observations"]["service"]["exact_deployment_verified"] is False
        assert json.loads((self.tmp_path / "hosted-probe-input.json").read_text())["evidence_writes_authorised"] is False

    def test_actual_sdk_probe_against_signed_synthetic_runtime(self):
        """Real HTTP/SDK, mocked JWKS/store: deliberately not hosted acceptance."""
        fixture = self.tmp_path / "signed-runtime.mjs"
        fixture.write_text('''
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const root = process.argv[2];
const local = (path) => import(pathToFileURL(root + path).href);
const support = await local("/apps/mcp-gateway/dist/test/gcp-test-support.js");
const { createGcpFetchHandler } = await local("/apps/mcp-gateway/dist/src/gcp-server.js");
const { createGcpJwtVerifier } = await local("/apps/mcp-gateway/dist/src/gcp-identity.js");
const { provisionGcpCpihPrincipal } = await local("/apps/mcp-gateway/dist/src/gcp-application.js");
const require = createRequire(root + "/apps/mcp-gateway/package.json");
const { toNodeHandler } = await import(pathToFileURL(require.resolve("@modelcontextprotocol/node")).href);
const config = support.runtimeConfig(["owner"]);
config.identity.subjectRoles["synthetic-reader"] = ["viewer"];
const backend = new support.FakeAtomicStore();
const owner = await support.principal(["owner"]);
await provisionGcpCpihPrincipal({ backend, principalScope: owner.scope, projection: support.PROJECTION, evidence: support.EVIDENCE });
const handler = createGcpFetchHandler({ config, projection: support.PROJECTION, knowledge: support.knowledge(), assets: new Map(), backend,
  verifier: createGcpJwtVerifier({ fetch: support.jwksFetch, now: () => support.CLOCK }), now: () => new Date(support.CLOCK) });
const node = toNodeHandler({ fetch: async (request) => {
  const headers = new Headers(request.headers);
  headers.set("host", new URL(support.ORIGIN).host);
  headers.set("x-gis-invocation-proof", support.transportToken());
  return handler.fetch(new Request(support.ORIGIN + new URL(request.url).pathname, {
    method: request.method, headers, ...(request.body ? { body: request.body, duplex: "half" } : {}) }));
} });
const server = createServer((request, response) => { void node(request, response).catch(() => { response.writeHead(503); response.end(); }); });
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
console.log(JSON.stringify({ endpoint: "http://127.0.0.1:" + server.address().port + "/mcp",
  allowed: support.credentials(config).authorization.slice(7), reader: support.credentials(config, "synthetic-reader").authorization.slice(7) }));
process.on("SIGTERM", () => { server.closeAllConnections(); server.close(() => process.exit(0)); });
''')
        server = subprocess.Popen(["node", str(fixture), str(ROOT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            ready = json.loads(server.stdout.readline())
            input_path, output_path = self.tmp_path / "input.json", self.tmp_path / "sdk.json"
            input_path.write_text(json.dumps({"endpoint": ready["endpoint"], "release_id": "d" * 64,
                "known_records": [{"bundle": "okf", "id": "legacy-1"}, {"bundle": "okf-plus", "id": "expanded-1"}],
                "observed_revision": None, "single_current_revision_verified": False, "evidence_writes_authorised": True}))
            environment = {**os.environ, "GIS_GCP_ALLOWED_IDENTITY_TOKEN": ready["allowed"], "GIS_GCP_READER_IDENTITY_TOKEN": ready["reader"]}
            completed = subprocess.run(["node", str(ROOT / "scripts/gcp/verify_mcp.mjs"), "--input", str(input_path), "--output", str(output_path)],
                                       capture_output=True, text=True, env=environment, timeout=30, check=False)
            report = json.loads(output_path.read_text())
            assert completed.returncode == 0, report
            observed = report["observations"]
            for name in ("negotiation", "discovery", "selection", "both_bundles", "reader_discovery", "reader_direct_refusal", "malformed_input", "evidence", "concurrent_idempotency"):
                assert observed[name]["status"] == "PASS", (name, observed)
            assert ready["allowed"] not in output_path.read_text()
            assert ready["reader"] not in output_path.read_text()
            # Repeat against the same fake process: receipt read is not restart proof.
            again = subprocess.run(["node", str(ROOT / "scripts/gcp/verify_mcp.mjs"), "--input", str(input_path), "--output", str(output_path)],
                                   capture_output=True, text=True, env=environment, timeout=30, check=False)
            assert again.returncode == 0
            assert json.loads(output_path.read_text())["observations"]["persisted_receipt"]["status"] == "BLOCKED"
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
            server.stdout.close()
            server.stderr.close()

if __name__ == "__main__":
    unittest.main()
