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
        self.config_path = self.root / "config.private.json"
        self.config = gcp.load_config(REPO / "infra/gcp/environments/personal/config.example.json")
        gcp.write_json(self.config_path, self.config)
        self.patch_root = patch.object(gcp, "ROOT", self.root)
        self.patch_root.start()
        self.lifecycle = gcp.Lifecycle(self.config_path)

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

    def test_unresolved_plan_writes_reviewable_approval_template(self):
        with patch.object(gcp.shutil, "which", return_value=None), patch.object(gcp, "source_manifest", return_value={"revision": "a" * 40, "files": []}):
            plan = self.lifecycle.plan()
        self.assertTrue(plan["blockers"])
        template = gcp.read_json(self.lifecycle.directory / "approvals" / (plan["plan_id"] + ".template.json"))
        self.assertEqual(template["status"], "PENDING_OWNER_APPROVAL")
        self.assertIsNone(template["approved_by"])
        self.assertEqual(plan["facts"]["account"], None)

    def test_approval_cannot_authorise_unresolved_plan(self):
        with patch.object(gcp.shutil, "which", return_value=None), patch.object(gcp, "source_manifest", return_value={"revision": "a" * 40, "files": []}):
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
        with patch.object(gcp.shutil, "which", return_value=None), patch.object(gcp, "source_manifest", return_value={"revision": "a" * 40, "files": []}):
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


class ApprovalTests(unittest.TestCase):
    """Security-sensitive admission tests with synthetic artefacts and no cloud."""
    def setUp(self):
        OfflineLifecycleTests.setUp(self)
        self.config = ConfigTests.cost_config(self)
        self.config["project"].update(id="synthetic-project", number="123456", expected_account="owner@synthetic.invalid", billing_account="000000-000000-000000", billing_currency_evidence=str(self.root / "currency.json"))
        gcp.write_json(self.root / "currency.json", {"currency": "GBP", "billing_account": "000000-000000-000000", "observed_at": gcp.timestamp(), "source": "synthetic evidence fixture"})
        gcp.write_json(self.config_path, self.config)
        self.lifecycle = gcp.Lifecycle(self.config_path)
        self.source = {"revision": "a" * 40, "files": []}
        directory = self.lifecycle.directory
        gcp.write_json(directory / "prepared/manifest.json", {})
        gcp.write_json(directory / "prepared/context/app/runtime-config.json", {"policy": "synthetic"})
        (directory / "gateway.oci.tar").write_bytes(b"synthetic immutable archive fixture")
        (self.root / "scripts/gcp").mkdir(parents=True)
        (self.root / "scripts/gcp/access_proxy.py").write_text("# synthetic proxy source\n")
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
        with patch.object(gcp, "source_manifest", return_value=self.source), patch.object(self.lifecycle, "assert_cloud_identity", return_value={}):
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
        self.source["revision"] = "b" * 40
        with self.assertRaisesRegex(gcp.GateError, "Source/configuration"):
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
