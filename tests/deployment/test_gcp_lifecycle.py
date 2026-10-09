"""Offline lifecycle contract tests; these do not establish hosted acceptance."""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock
import contextlib
import io
import os
import subprocess

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gcp_lifecycle", REPO / "scripts/gcp/lifecycle.py")
gcp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gcp)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = gcp.load_config(REPO / "infra/gcp/environments/personal/config.example.json")

    def test_examples_are_valid_but_unresolved(self):
        for name in ("personal", "bduk-sandpit"):
            config = gcp.load_config(REPO / "infra/gcp/environments" / name / "config.example.json")
            self.assertIn("project.id", gcp.unresolved(config))
            self.assertTrue(gcp.unresolved(config))

    def test_unknown_field_is_rejected(self):
        self.config["network"]["allow_public"] = True
        with self.assertRaisesRegex(gcp.GateError, "unknown fields"):
            gcp.validate_schema(self.config, gcp.read_json(gcp.SCHEMA))

    def test_network_and_data_constraints_cannot_be_weakened(self):
        for section, field in (("network", "public_app_endpoint"), ("network", "vm_external_ip"), ("data", "live_provider_calls"), ("data", "external_model_calls"), ("policy", "mock_identity_allowed_in_deployed_service")):
            with self.subTest(field=field):
                config = copy.deepcopy(self.config)
                config[section][field] = True
                with self.assertRaises(gcp.GateError):
                    gcp.validate_schema(config, gcp.read_json(gcp.SCHEMA))

    def test_bool_does_not_pass_as_number(self):
        with self.assertRaises(gcp.GateError):
            gcp.validate_schema(True, {"type": "integer"})

    def test_resource_sizing_is_bounded(self):
        self.config["operations"]["runtime_sizing"]["max_instances"] = 100
        with self.assertRaises(gcp.GateError):
            gcp.validate_schema(self.config, gcp.read_json(gcp.SCHEMA))

    def cost_config(self):
        config = copy.deepcopy(self.config)
        config["project"]["billing_currency"] = "GBP"
        config["authority"]["pilot_end"] = (gcp.now() + dt.timedelta(days=2)).isoformat()
        config["authority"]["spend_envelope"] = {"currency": "GBP", "maximum_initial": 2, "maximum_monthly": 10, "maximum_total": 20, "pilot_days": 3, "pricing_as_of": gcp.now().date().isoformat(), "pricing_source": "https://cloud.google.com/pricing", "assumptions": ["synthetic test prices; not a quote"], "estimated_initial": 1, "estimated_monthly": 5, "estimated_total": 2, "estimated_retained": 0.2, "budget_is_alert_only": True}
        return config

    def test_cost_requires_verified_currency(self):
        config = self.cost_config()
        config["project"]["billing_currency"] = "USD"
        with self.assertRaisesRegex(gcp.GateError, "currency"):
            gcp.validate_spend(config)

    def test_total_budget_is_not_monthly_budget(self):
        config = self.cost_config()
        config["authority"]["spend_envelope"].update(maximum_total=1, estimated_total=2)
        with self.assertRaisesRegex(gcp.GateError, "spend"):
            gcp.validate_spend(config)

    def test_retained_and_prorated_costs_are_included(self):
        config = self.cost_config()
        config["authority"]["spend_envelope"]["estimated_total"] = 1
        with self.assertRaisesRegex(gcp.GateError, "understates"):
            gcp.validate_spend(config)

    def test_stale_pricing_blocks(self):
        config = self.cost_config()
        config["authority"]["spend_envelope"]["pricing_as_of"] = "2001-01-01"
        with self.assertRaisesRegex(gcp.GateError, "stale"):
            gcp.validate_spend(config)

    def test_current_bounded_test_cost_validates(self):
        gcp.validate_spend(self.cost_config())

    def test_cleanup_remains_authorisable_after_pilot_end(self):
        config = self.cost_config()
        config["authority"]["pilot_end"] = (gcp.now() - dt.timedelta(days=1)).isoformat()
        config["authority"]["spend_envelope"]["pricing_as_of"] = "2001-01-01"
        with self.assertRaises(gcp.GateError):
            gcp.validate_spend(config)
        gcp.validate_spend(config, destructive=True)

    def test_anonymous_and_wildcard_iam_members_rejected(self):
        for member in ("allUsers", "allAuthenticatedUsers", "user:missing-email", "principalSet://iam.googleapis.com/locations/global/workforcePools/pool/*"):
            config = copy.deepcopy(self.config)
            config["network"]["transport_principals"] = [member]
            with self.subTest(member=member), self.assertRaises(gcp.GateError):
                gcp.validate_schema(config, gcp.read_json(gcp.SCHEMA))

    def test_dynamic_role_mappings_and_enrolment_are_bounded(self):
        for values in ({"subject": ["invented-admin"]}, {f"subject-{i}": ["viewer"] for i in range(17)}):
            config = copy.deepcopy(self.config)
            config["identity"]["claims_mapping"] = {"subject_roles": values}
            with self.assertRaises(gcp.GateError):
                gcp.validate_schema(config, gcp.read_json(gcp.SCHEMA))

    def test_reviewed_policy_matches_actual_application_grants(self):
        reviewed = gcp.read_json(gcp.reviewed_policy(self.config))
        self.assertEqual(reviewed["roles"], gcp.concrete_runtime_policy()["roles"])
        self.assertEqual(reviewed["tool_capabilities"], gcp.concrete_runtime_policy()["tool_capabilities"])

    def test_browser_callback_origin_is_exact(self):
        browser = {"callback_url": "https://private.synthetic.invalid/auth/callback"}
        self.assertEqual(gcp.browser_public_origin(browser), "https://private.synthetic.invalid")
        for callback in ("http://private.synthetic.invalid/auth/callback", "https://user:password@private.synthetic.invalid/auth/callback", "https://private.synthetic.invalid/auth/callback?redirect=other", "https://private.synthetic.invalid/arbitrary"):
            with self.subTest(callback=callback), self.assertRaises(gcp.GateError):
                gcp.browser_public_origin({"callback_url": callback})

    def test_output_bound_service_cannot_add_resource_or_delete(self):
        valid = {"changes": [{"address": "module.pilot.google_cloud_run_v2_service.gateway", "actions": ["create"]}]}
        gcp.Lifecycle.service_scope(valid)
        for address, actions in (("google_project.some_project", ["create"]), ("module.pilot.google_cloud_run_v2_service.gateway", ["delete", "create"])):
            with self.assertRaises(gcp.GateError):
                gcp.Lifecycle.service_scope({"changes": [{"address": address, "actions": actions}]})


class OfflineLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".gitignore").write_text("artifacts/\nconfig.private.json\ncurrency.json\n__pycache__/\n*.env\n*.tfstate*\n*.tfplan*\n.devcontainer/image/inputs/\n.devcontainer/platform-approval.json\nscripts/security/receipt.json\nscripts/environment/cache/\n")
        OfflineLifecycleTests.git(self, "init", "--quiet")
        OfflineLifecycleTests.git(self, "add", ".gitignore")
        OfflineLifecycleTests.git(self, "commit", "--quiet", "--no-gpg-sign", "-m", "Synthetic fixture")
        self.config_path = self.root / "config.private.json"
        self.config = gcp.load_config(REPO / "infra/gcp/environments/personal/config.example.json")
        gcp.write_json(self.config_path, self.config)
        self.patch_root = patch.object(gcp, "ROOT", self.root)
        self.patch_root.start()
        self.lifecycle = gcp.Lifecycle(self.config_path)

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=Synthetic Test", "-c", "user.email=test@synthetic.invalid", *args], cwd=self.root, capture_output=True, text=True, check=True).stdout

    def tearDown(self):
        self.patch_root.stop()
        self.temporary.cleanup()

    def test_missing_cli_preserves_unknown_account(self):
        with patch.object(gcp.shutil, "which", return_value=None):
            result = self.lifecycle.preflight()
        self.assertIsNone(result["facts"]["account"])
        self.assertIsNone(result["facts"]["project_id"])
        self.assertIsNone(result["facts"]["billing_enabled"])
        self.assertTrue(all(not line["cloud_mutation"] for line in []))

    def test_preflight_never_runs_mutating_commands(self):
        self.config["project"].update(id="synthetic-project", number="123456", expected_account="owner@synthetic.invalid", billing_account="000000-000000-000000")
        gcp.write_json(self.config_path, self.config)
        lifecycle = gcp.Lifecycle(self.config_path)
        calls = []
        def read_only(args, **kwargs):
            calls.append((args, kwargs))
            payload = [] if "auth" in args or "services" in args else {}
            return {"status": "PASS", "exit_code": 0, "stdout": json.dumps(payload), "stderr": ""}
        with patch.object(gcp.shutil, "which", return_value="synthetic-bin"), patch.object(lifecycle, "run", side_effect=read_only):
            lifecycle.preflight()
        self.assertTrue(calls)
        for args, kwargs in calls:
            self.assertFalse(kwargs.get("mutation", False))
            self.assertNotIn("enable", args)
            self.assertNotIn("create", args)
            self.assertNotIn("set-iam-policy", args)

    def test_browser_api_preflight_requires_exact_service_name(self):
        self.lifecycle.config["project"]["id"] = "synthetic-project"
        self.lifecycle.config["identity"]["browser"] = {
            "client_id": "synthetic-oidc-client", "client_auth_method": "none",
            "callback_url": "https://private.synthetic.invalid/auth/callback",
            "allowed_redirect_uris": ["https://private.synthetic.invalid/auth/callback"],
            "allowed_endpoints": ["https://okta.synthetic.invalid/token"], "scopes": ["openid"], "session_seconds": 300,
            "session_key_secret": {"resource": "projects/synthetic-project/secrets/browser-session", "version": "3"},
            "client_secret": None,
        }
        for names, expected in (([], "BLOCKED"),
            (["prefix-secretmanager.googleapis.com"], "BLOCKED"),
            (["secretmanager.googleapis.com.evil"], "BLOCKED"),
            (["https://secretmanager.googleapis.com"], "BLOCKED"),
            (["Secretmanager.googleapis.com"], "BLOCKED"),
            (["run.googleapis.com", "secretmanager.googleapis.com"], "PASS"),
            (["secretmanager.googleapis.com"] * 2, "PASS")):
            with self.subTest(names=names):
                def read_only(args, **kwargs):
                    payload = ([{"config": {"name": name}} for name in names] if "services" in args
                        else [] if "auth" in args else {"state": "ENABLED"})
                    return {"status": "PASS", "exit_code": 0, "stdout": json.dumps(payload), "stderr": ""}
                with patch.object(gcp.shutil, "which", return_value="synthetic-bin"), patch.object(self.lifecycle, "run", side_effect=read_only):
                    result = self.lifecycle.preflight()
                observed = next(check for check in result["checks"] if check["id"] == "browser-secretmanager-api")
                self.assertEqual(observed["status"], expected)

    def test_unresolved_plan_writes_reviewable_approval_template(self):
        with patch.object(gcp.shutil, "which", return_value=None):
            plan = self.lifecycle.plan()
        self.assertTrue(plan["blockers"])
        template = gcp.read_json(self.lifecycle.directory / "approvals" / (plan["plan_id"] + ".template.json"))
        self.assertEqual(template["status"], "PENDING_OWNER_APPROVAL")
        self.assertIsNone(template["approved_by"])
        self.assertEqual(plan["facts"]["account"], None)

    def test_approval_cannot_authorise_unresolved_plan(self):
        with patch.object(gcp.shutil, "which", return_value=None):
            plan = self.lifecycle.plan()
        approval = {"kind": "deploy", "plan_id": plan["plan_id"], "status": "APPROVED"}
        gcp.write_json(self.lifecycle.directory / "approvals" / (plan["plan_id"] + ".approval.json"), approval)
        with self.assertRaisesRegex(gcp.GateError, "prerequisites"):
            self.lifecycle.approved(plan["plan_id"], "deploy")

    def test_verify_requires_all_catalogue_tests_and_never_reuses_stale_results(self):
        gcp.write_json(self.root / "evaluation/gcp-private-acceptance.v1.json", {"tests": [{"id": f"CHECK{i}", "required_for": ["personal-reference-accepted"]} for i in range(41)]})
        gcp.write_json(self.lifecycle.directory / "hosted-results.json", {"results": [{"id": "CHECK0", "status": "PASS"}]})
        with patch.object(self.lifecycle, "status", return_value={"status": "BLOCKED"}):
            result = self.lifecycle.verify()
        self.assertEqual(len(result["results"]), 41)
        self.assertTrue(all(item["status"] == "BLOCKED" for item in result["results"]))
        self.assertFalse((self.lifecycle.directory / "hosted-results.json").exists())
        self.assertEqual(result["acceptance_level"], "NOT_PREPARED")
        self.assertEqual(result["local_preparation"]["status"], "NOT_PREPARED")

    def test_tampered_image_receipt_is_not_prepared(self):
        gcp.write_json(self.lifecycle.directory / "prepared/manifest.json", {"schema": "gis-ai-go.gcp-prepared.v1"})
        gcp.write_json(self.lifecycle.directory / "image.json", {"manifest_digest": "sha256:" + "a" * 64, "prepared_manifest_sha256": "b" * 64})
        (self.lifecycle.directory / "gateway.oci.tar").write_bytes(b"synthetic tampered archive")
        result = self.lifecycle.prepared_status()
        self.assertEqual(result["status"], "NOT_PREPARED")
        self.assertIn("no longer matches", result["reason"])

    def test_context_digest_binds_file_contents(self):
        context = self.root / "context"
        context.mkdir()
        (context / "file.json").write_text("{}"); before = gcp.digest(gcp.directory_manifest(context))
        (context / "file.json").write_text('{"changed":true}')
        self.assertNotEqual(before, gcp.digest(gcp.directory_manifest(context)))

    def test_symlink_context_rejected(self):
        context = self.root / "context"
        context.mkdir()
        (context / "link").symlink_to(self.config_path)
        with self.assertRaisesRegex(gcp.GateError, "symlink"):
            gcp.directory_manifest(context)

    def test_bduk_default_consumes_foundation_without_new_resources(self):
        gcp.write_json(self.config_path, gcp.load_config(REPO / "infra/gcp/environments/bduk-sandpit/config.example.json"))
        lifecycle = gcp.Lifecycle(self.config_path)
        variables = lifecycle.variables("foundation")
        self.assertFalse(variables["create_foundation"])
        self.assertFalse(variables["create_access_vm"])
        self.assertFalse(variables["create_network"])
        self.assertFalse(variables["enable_apis"])

    def test_browser_secret_configuration_carries_references_only(self):
        browser = {"client_id": "synthetic-oidc-client", "client_auth_method": "client_secret_basic", "callback_url": "https://private.synthetic.invalid/auth/callback", "allowed_redirect_uris": ["https://private.synthetic.invalid/auth/callback"], "allowed_endpoints": ["https://okta.synthetic.invalid/discovery", "https://okta.synthetic.invalid/token", "https://okta.synthetic.invalid/jwks"], "scopes": ["openid"], "session_seconds": 300, "session_key_secret": {"resource": "projects/synthetic-project/secrets/browser-session", "version": "3"}, "client_secret": {"resource": "projects/synthetic-project/secrets/oidc-client", "version": "2"}}
        self.lifecycle.config["identity"]["browser"] = browser
        gcp.validate_schema(self.lifecycle.config, gcp.read_json(gcp.SCHEMA))
        variables = self.lifecycle.variables("service")
        self.assertEqual(variables["browser_secret_references"]["GCP_BROWSER_SESSION_KEY"], browser["session_key_secret"])
        self.assertEqual(variables["browser_secret_references"]["GCP_OIDC_CLIENT_SECRET"], browser["client_secret"])
        browser["session_key_secret"]["version"] = "latest"
        with self.assertRaises(gcp.GateError):
            gcp.validate_schema(self.lifecycle.config, gcp.read_json(gcp.SCHEMA))

    def test_package_created_without_cloud_and_private_inputs_scrubbed(self):
        self.config["project"].update(id="synthetic-private-project", expected_account="synthetic-owner@private.invalid", number="1234567890", billing_account="123ABC-456DEF-789ABC")
        gcp.write_json(self.config_path, self.config)
        lifecycle = gcp.Lifecycle(self.config_path)
        (self.root / "infra/gcp").mkdir(parents=True)
        (self.root / "infra/gcp/readme.md").write_text("ordinary reviewed source")
        with patch.object(gcp.shutil, "which", return_value=None):
            result = lifecycle.package_approval()
        self.assertTrue(Path(result["package"]).exists())
        import zipfile
        with zipfile.ZipFile(result["package"]) as archive:
            content = "\n".join(archive.read(name).decode() for name in archive.namelist())
        self.assertNotIn("synthetic-private-project", content)
        self.assertNotIn("synthetic-owner@private.invalid", content)
        self.assertNotIn("123ABC-456DEF-789ABC", content)
        self.assertNotIn("1234567890", content)
        self.assertIn("NOT_RUN", content)

    def test_package_includes_reviewable_environment_security_source_only(self):
        public = {".devcontainer/local/devcontainer.json": '{}\n',
                  ".devcontainer/image/Containerfile": '# synthetic source\n',
                  "scripts/environment/environment.sh": '#!/bin/sh\nexit 0\n',
                  "scripts/security/image_assurance.py": '#!/usr/bin/env python3\n',
                  "docs/development/DEVELOPMENT_ENVIRONMENTS.md": '# Synthetic guide\n',
                  "docs/security/GCP-223-SECURITY-REVIEW.md": '# Sanitised synthetic audit\n',
                  "SECURITY.md": '# Synthetic source review policy\n',
                  "CONTEXT.md": '# Synthetic authority\n', "PROGRESS.md": '# Synthetic checkpoint\n'}
        private = {".devcontainer/image/inputs/tool.tgz": 'synthetic excluded tooling',
                   ".devcontainer/platform-approval.json": 'synthetic private record',
                   "scripts/security/receipt.json": 'synthetic private receipt',
                   "scripts/environment/cache/image.oci.tar": 'synthetic excluded image'}
        for name, content in (public | private).items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        (self.root / "scripts/environment/environment.sh").chmod(0o755)
        with patch.object(gcp.shutil, "which", return_value=None):
            result = self.lifecycle.package_approval()
        import zipfile
        import hashlib
        with zipfile.ZipFile(result["package"]) as archive:
            self.assertTrue(set(public).issubset(archive.namelist()))
            self.assertFalse(set(private).intersection(archive.namelist()))
            self.assertEqual((archive.getinfo("scripts/environment/environment.sh").external_attr >> 16) & 0o777, 0o755)
            checksums = json.loads(archive.read("package-files.sha256.json"))
            for item in checksums:
                payload = archive.read(item["path"])
                self.assertEqual(item["sha256"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(item["bytes"], len(payload))


class ApprovalTests(unittest.TestCase):
    """Security-sensitive admission tests with synthetic artefacts and no cloud."""
    def setUp(self):
        OfflineLifecycleTests.setUp(self)
        self.config = ConfigTests.cost_config(self)
        self.config["project"].update(id="synthetic-project", number="123456", expected_account="owner@synthetic.invalid", billing_account="000000-000000-000000", billing_currency_evidence=str(self.root / "currency.json"))
        gcp.write_json(self.root / "currency.json", {"currency": "GBP", "billing_account": "000000-000000-000000", "observed_at": gcp.timestamp(), "source": "synthetic evidence fixture"})
        gcp.write_json(self.config_path, self.config)
        self.lifecycle = gcp.Lifecycle(self.config_path)
        directory = self.lifecycle.directory
        gcp.write_json(directory / "prepared/manifest.json", {})
        gcp.write_json(directory / "prepared/context/app/runtime-config.json", {"policy": "synthetic"})
        (directory / "gateway.oci.tar").write_bytes(b"synthetic immutable archive fixture")
        (self.root / "scripts/gcp").mkdir(parents=True)
        (self.root / "scripts/gcp/access_proxy.py").write_text("# synthetic proxy source\n")
        self.source = gcp.source_manifest(self.config_path)
        self.bindings = {"account": self.config["project"]["expected_account"], "config_sha256": gcp.digest(self.config), "source_sha256": gcp.digest(self.source), "prepared_context_sha256": gcp.digest(gcp.directory_manifest(directory / "prepared/context")), "billing_currency_evidence_sha256": gcp.file_digest(self.root / "currency.json"), "prepared_sha256": gcp.file_digest(directory / "prepared/manifest.json"), "image_archive_sha256": gcp.file_digest(directory / "gateway.oci.tar"), "access_proxy_sha256": gcp.file_digest(self.root / "scripts/gcp/access_proxy.py")}
        self.plan = {"kind": "deploy", "blockers": [], "bindings": self.bindings, "cost": self.config["authority"]["spend_envelope"]}
        self.plan_id = gcp.plan_identity(self.plan)
        self.approval = {"kind": "deploy", "plan_id": self.plan_id, "status": "APPROVED", "bindings": self.bindings, "approved_by": self.config["project"]["expected_account"], "approved_at": gcp.timestamp(), "expires_at": (gcp.now() + dt.timedelta(days=1)).isoformat(), "spend": self.plan["cost"]}
        gcp.write_json(directory / "plans" / (self.plan_id + ".json"), self.plan)
        self.persist_approval()

    def tearDown(self):
        OfflineLifecycleTests.tearDown(self)

    def persist_approval(self):
        gcp.write_json(self.lifecycle.directory / "approvals" / (self.plan_id + ".approval.json"), self.approval)

    def approved(self, kind="deploy"):
        with patch.object(self.lifecycle, "assert_cloud_identity", return_value={}):
            return self.lifecycle.approved(self.plan_id, kind)

    def test_synthetic_exact_bound_approval_accepted(self):
        self.assertEqual(self.approved()[0]["bindings"], self.bindings)

    def test_expired_record_rejected(self):
        self.approval["expires_at"] = (gcp.now() - dt.timedelta(minutes=1)).isoformat()
        self.persist_approval()
        with self.assertRaisesRegex(gcp.GateError, "expired"):
            self.approved()

    def test_wrong_approving_account_rejected(self):
        self.approval["approved_by"] = "different@synthetic.invalid"
        self.persist_approval()
        with self.assertRaisesRegex(gcp.GateError, "identity"):
            self.approved()

    def test_destroy_cannot_reuse_deploy_approval(self):
        with self.assertRaisesRegex(gcp.GateError, "operation"):
            self.approved("destroy")

    def test_changed_source_rejected(self):
        (self.root / "scripts/gcp/access_proxy.py").write_text("# changed public source\n")
        with self.assertRaisesRegex(gcp.GateError, "Source/configuration"):
            self.approved()

    def test_source_mode_change_invalidates_approval(self):
        path = self.root / "scripts/gcp/access_proxy.py"
        path.chmod(0o755 if path.stat().st_mode & 0o777 != 0o755 else 0o644)
        with self.assertRaisesRegex(gcp.GateError, "Source/configuration"):
            self.approved()

    def test_source_alias_and_referent_change_after_approval_are_rejected(self):
        path = self.root / "scripts/gcp/access_proxy.py"
        referent = self.root / "synthetic-private.env"
        referent.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(referent)
        for content in ("# original-looking synthetic source\n", "# changed private referent\n"):
            referent.write_text(content)
            with self.assertRaisesRegex(gcp.GateError, "linked"):
                self.approved()

    def test_mutated_runtime_policy_rejected(self):
        gcp.write_json(self.lifecycle.directory / "prepared/context/app/runtime-config.json", {"policy": "changed"})
        with self.assertRaisesRegex(gcp.GateError, "Prepared context"):
            self.approved()

    def test_changed_oci_archive_rejected(self):
        (self.lifecycle.directory / "gateway.oci.tar").write_bytes(b"changed image")
        with self.assertRaisesRegex(gcp.GateError, "image_archive"):
            self.approved()

    def test_changed_currency_evidence_rejected(self):
        gcp.write_json(self.root / "currency.json", {"currency": "USD"})
        with self.assertRaisesRegex(gcp.GateError, "currency evidence"):
            self.approved()

    def test_runtime_and_infrastructure_plan_tampering_rejected(self):
        for field, value in (("runtime_template", {"identity": {"subjectRoles": {"intruder": ["owner"]}}}), ("terraform", {"foundation": {"file": "different.tfplan", "sha256": "f" * 64}}), ("phases", ["unreviewed change"]), ("approval_actions", ["unreviewed-cloud-action"])):
            with self.subTest(field=field):
                plan = copy.deepcopy(self.plan)
                plan[field] = value
                gcp.write_json(self.lifecycle.directory / "plans" / (self.plan_id + ".json"), plan)
                with self.assertRaisesRegex(gcp.GateError, "complete recorded plan"):
                    self.approved()

    def test_unreviewed_approval_action_rejected(self):
        self.approval["actions"] = ["unreviewed-cloud-action"]
        self.persist_approval()
        with self.assertRaisesRegex(gcp.GateError, "exceeds"):
            self.approved()

    def test_saved_plan_cannot_redirect_execution(self):
        with patch.object(self.lifecycle, "iac_root", return_value=self.root):
            with self.assertRaisesRegex(gcp.GateError, "execution path"):
                self.lifecycle.apply_saved("foundation", {"terraform": {"foundation": {"file": str(self.root / "alternate.tfplan"), "sha256": "a" * 64}}})


class SourceBoundaryTests(unittest.TestCase):
    """Real temporary Git inventories, never a physical-filesystem fallback."""
    def setUp(self):
        OfflineLifecycleTests.setUp(self)
        self.source = self.root / "apps/example/source.ts"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("export const synthetic = true;\n")
        OfflineLifecycleTests.git(self, "add", "apps/example/source.ts")
        self.outside = tempfile.TemporaryDirectory()
        self.referent = Path(self.outside.name) / "synthetic-private.ts"
        self.referent.write_text("synthetic private fixture must never enter a package\n")

    def tearDown(self):
        self.outside.cleanup()
        OfflineLifecycleTests.tearDown(self)

    def add_iac(self):
        path = self.root / "infra/gcp/environments/personal/foundation/main.tf"
        path.parent.mkdir(parents=True)
        path.write_text('terraform { required_version = ">= 1.12.2" }\n')
        (path.parent / ".terraform.lock.hcl").write_text("# Synthetic lock source\n")
        return path

    def package(self):
        with patch.object(gcp.shutil, "which", return_value=None):
            return self.lifecycle.package_approval()

    def test_inventory_binds_bytes_and_legitimate_mode(self):
        self.source.chmod(0o755)
        inventory = gcp.source_manifest(self.config_path)
        entry = next(row for row in inventory["files"] if row["path"] == "apps/example/source.ts")
        self.assertEqual(entry["mode"], 0o755)
        self.assertEqual(entry["bytes"], len(self.source.read_bytes()))
        self.assertEqual(entry["sha256"], gcp.file_digest(self.source))

    def test_source_leaf_symlink_fails_instead_of_disappearing(self):
        self.source.unlink()
        self.source.symlink_to(self.referent)
        with self.assertRaisesRegex(gcp.GateError, "linked"):
            gcp.source_manifest(self.config_path)

    def test_source_parent_directory_symlink_fails(self):
        directory = self.source.parent
        directory.rename(Path(self.outside.name) / "directory")
        directory.symlink_to(Path(self.outside.name) / "directory", target_is_directory=True)
        with self.assertRaisesRegex(gcp.GateError, "ancestor"):
            gcp.source_manifest(self.config_path)

    def test_missing_tracked_source_fails(self):
        self.source.unlink()
        with self.assertRaisesRegex(gcp.GateError, "missing"):
            gcp.source_manifest(self.config_path)

    def test_special_tracked_source_fails_without_blocking(self):
        self.source.unlink()
        os.mkfifo(self.source)
        with self.assertRaisesRegex(gcp.GateError, "regular"):
            gcp.source_manifest(self.config_path)

    def test_hardlinked_source_fails(self):
        os.link(self.source, self.root / "synthetic-private.env")
        with self.assertRaisesRegex(gcp.GateError, "one link"):
            gcp.source_manifest(self.config_path)

    def test_exact_private_config_exclusion_does_not_hide_a_link(self):
        selected = self.root / "selected.json"
        selected.write_text("{}")
        self.assertNotIn("selected.json", {row["path"] for row in gcp.source_manifest(selected)["files"]})
        selected.unlink()
        selected.symlink_to(self.referent)
        with self.assertRaisesRegex(gcp.GateError, "linked"):
            gcp.source_manifest(selected)

    def test_changed_bytes_during_read_fail_closed(self):
        read = gcp.os.read
        changed = False
        def replace_after_read(fd, amount):
            nonlocal changed
            block = read(fd, amount)
            if block and not changed:
                changed = True
                self.source.write_text("changed while reading\n")
            return block
        with patch.object(gcp.os, "read", side_effect=replace_after_read), self.assertRaisesRegex(gcp.GateError, "changed during"):
            gcp.read_source_file("apps/example/source.ts")

    def test_ignored_iac_never_materialises(self):
        source = self.add_iac()
        ignored = self.root / "infra/gcp/ignored.auto.tfvars.json"
        ignored.write_text('{"synthetic_unapproved":true}')
        with (self.root / ".gitignore").open("a") as stream:
            stream.write("infra/gcp/ignored.auto.tfvars.json\n")
        target = self.lifecycle.iac_root("foundation")
        self.assertEqual((target / "main.tf").read_bytes(), source.read_bytes())
        self.assertTrue((target / ".terraform.lock.hcl").is_file())
        self.assertFalse((target.parents[2] / "ignored.auto.tfvars.json").exists())

    def test_stale_target_terraform_is_rejected_and_state_preserved(self):
        self.add_iac()
        target = self.lifecycle.iac_root("foundation")
        state = target / "terraform.tfstate.backup"
        state.write_text("synthetic retained state\n")
        (target / "stale.tf").write_text('resource "synthetic" "unapproved" {}\n')
        with self.assertRaisesRegex(gcp.GateError, "stale or unadmitted"):
            self.lifecycle.iac_root("foundation")
        self.assertEqual(state.read_text(), "synthetic retained state\n")
        self.assertTrue((target / "stale.tf").exists())

    def test_removed_previously_admitted_iac_cannot_survive_overlay(self):
        self.add_iac()
        removed = self.root / "infra/gcp/environments/personal/foundation/obsolete.tf"
        removed.write_text("# obsolete synthetic Terraform\n")
        self.lifecycle.iac_root("foundation")
        removed.unlink()
        with self.assertRaisesRegex(gcp.GateError, "stale or unadmitted"):
            self.lifecycle.iac_root("foundation")

    def test_target_source_alias_is_rejected(self):
        self.add_iac()
        target = self.lifecycle.iac_root("foundation")
        (target / "main.tf").unlink()
        (target / "main.tf").symlink_to(self.referent)
        with self.assertRaisesRegex(gcp.GateError, "linked"):
            self.lifecycle.iac_root("foundation")

    def test_target_parent_alias_is_rejected_without_touching_referent(self):
        self.add_iac()
        target = self.lifecycle.iac_root("foundation")
        parent = target.parent
        outside = Path(self.outside.name) / "target-parent"
        parent.rename(outside)
        parent.symlink_to(outside, target_is_directory=True)
        original = (outside / "foundation/main.tf").read_bytes()
        with self.assertRaisesRegex(gcp.GateError, "linked directory"):
            self.lifecycle.iac_root("foundation")
        self.assertEqual((outside / "foundation/main.tf").read_bytes(), original)

    def test_every_terraform_invocation_revalidates_source(self):
        source = self.add_iac()
        self.lifecycle.source_binding = gcp.digest(gcp.source_manifest(self.config_path))
        with patch.object(self.lifecycle, "run", return_value={"status": "PASS"}) as run:
            self.lifecycle.terraform_run("foundation", ["output", "-json"])
            source.write_text("# changed after recorded approval\n")
            with self.assertRaisesRegex(gcp.GateError, "before Terraform"):
                self.lifecycle.terraform_run("foundation", ["output", "-json"])
        self.assertEqual(run.call_count, 1)

    def test_valid_saved_plan_executes_the_exact_bound_path(self):
        self.add_iac()
        root = self.lifecycle.iac_root("foundation")
        saved = root / "deployment.tfplan"
        saved.write_bytes(b"synthetic saved-plan bytes")
        plan = {"terraform": {"foundation": {"file": str(saved), "sha256": gcp.file_digest(saved)}}}
        with patch.object(self.lifecycle, "run", return_value={"status": "PASS", "stdout": ""}) as run, patch.object(self.lifecycle, "terraform_environment", return_value=None):
            self.lifecycle.apply_saved("foundation", plan)
        self.assertEqual(run.call_args.args[0][-1], saved)
        self.assertTrue(run.call_args.kwargs["mutation"])

    def test_package_ignored_private_files_and_state_backups_are_excluded(self):
        public = self.root / "infra/gcp/README.md"
        public.parent.mkdir(parents=True)
        public.write_text("# public synthetic source\n")
        excluded = [public.parent / "private.env", public.parent / "terraform.tfstate.backup", self.root / "artifacts/gcp/costs-illustrative-london-2026-10-05.json"]
        for path in excluded:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic private excluded marker\n")
        import zipfile
        with zipfile.ZipFile(self.package()["package"]) as archive:
            self.assertIn("infra/gcp/README.md", archive.namelist())
            self.assertIn("apps/example/source.ts", archive.namelist())
            self.assertTrue(all(path.relative_to(self.root).as_posix() not in archive.namelist() for path in excluded))
            self.assertFalse(any(b"synthetic private excluded marker" in archive.read(name) for name in archive.namelist()))

    def test_package_public_leaf_alias_is_rejected(self):
        self.source.unlink()
        self.source.symlink_to(self.referent)
        with self.assertRaisesRegex(gcp.GateError, "linked"):
            self.package()

    def test_package_public_parent_alias_is_rejected(self):
        directory = self.source.parent
        directory.rename(Path(self.outside.name) / "package-parent")
        directory.symlink_to(Path(self.outside.name) / "package-parent", target_is_directory=True)
        with self.assertRaisesRegex(gcp.GateError, "ancestor"):
            self.package()

    def test_package_public_hardlink_is_rejected(self):
        os.link(self.source, self.root / "synthetic-private.env")
        with self.assertRaisesRegex(gcp.GateError, "one link"):
            self.package()

    def test_package_revalidates_members_after_inventory(self):
        with patch.object(gcp.shutil, "which", return_value=None):
            self.lifecycle.plan()
        inventory = gcp.source_manifest
        def alias_after_inventory(*args, **kwargs):
            result = inventory(*args, **kwargs)
            self.source.unlink()
            self.source.symlink_to(self.referent)
            return result
        with patch.object(gcp, "source_manifest", side_effect=alias_after_inventory), self.assertRaisesRegex(gcp.GateError, "linked"):
            self.lifecycle.package_approval()

    def test_prepared_sources_require_admitted_regular_files(self):
        inventory = gcp.source_manifest(self.config_path)
        entry = next(row for row in inventory["files"] if row["path"] == "apps/example/source.ts")
        manifest = {"sourceFiles": [{key: entry[key] for key in ("path", "sha256", "bytes")}]}
        gcp.validate_prepared_sources(manifest, inventory)
        self.source.unlink()
        self.source.symlink_to(self.referent)
        with self.assertRaisesRegex(gcp.GateError, "linked"):
            gcp.validate_prepared_sources(manifest, inventory)
        excluded = self.root / "synthetic-private.env"
        excluded.write_text("synthetic ignored source\n")
        with self.assertRaisesRegex(gcp.GateError, "outside the admitted"):
            gcp.validate_prepared_sources({"sourceFiles": [{"path": excluded.name, "sha256": gcp.file_digest(excluded)}]}, inventory)

    def test_reviewed_policy_parent_alias_is_rejected(self):
        directory = self.root / "infra/gcp/policy"
        directory.parent.mkdir(parents=True)
        directory.symlink_to(Path(self.outside.name), target_is_directory=True)
        self.lifecycle.config["policy"]["role_toolsets_manifest"] = "infra/gcp/policy/synthetic-private.ts"
        with self.assertRaisesRegex(gcp.GateError, "ancestor"):
            gcp.reviewed_policy(self.lifecycle.config)


class OnDemandConnectionTests(unittest.TestCase):
    def setUp(self):
        OfflineLifecycleTests.setUp(self)
        self.deployed = {"plan_id": "a" * 24, "service_uri": "https://synthetic.run.app", "foundation": {"access_vm": "gis-ai-go-access"}}
        gcp.write_json(self.lifecycle.directory / "deployed.json", self.deployed)
        self.plan = {"plan_id": self.deployed["plan_id"], "access_vm_operating_scope": {"per_connection_reserved_hours": 1.25, "maximum_tunnel_seconds": 3600}}
        self.approval = {"actions": ["connect-start-stop-owned-vm"]}
        self.process = Mock()
        self.process.wait.return_value = 0
        self.process.poll.return_value = 0
        self.calls = []

    def tearDown(self):
        OfflineLifecycleTests.tearDown(self)

    def cloud(self, args, **kwargs):
        self.calls.append((args, kwargs))
        return {"status": "PASS", "stdout": "", "stderr": "", "exit_code": 0}

    def connect(self):
        with patch.object(self.lifecycle, "approved", return_value=(self.plan, self.approval)), patch.object(self.lifecycle, "gcloud", side_effect=self.cloud), patch.object(gcp.subprocess, "Popen", return_value=self.process), contextlib.redirect_stdout(io.StringIO()):
            return self.lifecycle.connect()

    def test_vm_starts_only_for_approved_connection_and_stops_on_exit(self):
        self.assertEqual(self.connect()["status"], "CLOSED_VM_STOPPED")
        self.assertEqual([args[2] for args, kwargs in self.calls], ["start", "stop"])
        self.assertTrue(all(kwargs["mutation"] for args, kwargs in self.calls))
        self.assertTrue(all(args[3] == "gis-ai-go-access" for args, kwargs in self.calls))

    def test_failed_ssh_still_stops_the_vm(self):
        self.process.wait.return_value = 1
        with self.assertRaisesRegex(gcp.GateError, "SSH tunnel exited"):
            self.connect()
        self.assertEqual(self.calls[-1][0][2], "stop")

    def test_ctrl_c_terminates_ssh_and_stops_the_vm(self):
        self.process.wait.side_effect = [KeyboardInterrupt, 0]
        self.process.poll.return_value = None
        self.assertEqual(self.connect()["status"], "CLOSED_VM_STOPPED")
        self.process.terminate.assert_called_once()
        self.assertEqual(self.calls[-1][0][2], "stop")

    def test_timeout_terminates_ssh_and_stops_the_vm(self):
        self.process.wait.side_effect = [gcp.subprocess.TimeoutExpired("synthetic-ssh", 3600), 0]
        self.process.poll.return_value = None
        self.assertEqual(self.connect()["status"], "CLOSED_VM_STOPPED")
        self.assertEqual(self.calls[-1][0][2], "stop")

    def test_missing_start_stop_authority_never_calls_cloud(self):
        self.approval["actions"] = []
        with self.assertRaisesRegex(gcp.GateError, "starting/stopping"):
            self.connect()
        self.assertEqual(self.calls, [])

    def test_budget_scope_exhaustion_never_starts_vm(self):
        self.lifecycle.config["network"]["access_vm_max_connected_hours"] = 1
        with self.assertRaisesRegex(gcp.GateError, "hours scope is exhausted"):
            self.connect()
        self.assertEqual(self.calls, [])

    def test_unowned_vm_is_rejected_before_cloud_mutation(self):
        self.deployed["foundation"]["access_vm"] = "someone-elses-vm"
        gcp.write_json(self.lifecycle.directory / "deployed.json", self.deployed)
        with self.assertRaisesRegex(gcp.GateError, "target differs"):
            self.connect()
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
