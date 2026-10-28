"""Installer orchestration/approval tests: no GCP calls or hosted acceptance."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/gcp/install-platform.sh"
source = SCRIPT.read_text().split("<<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
installer = types.ModuleType("platform_installer_under_test")
exec(compile(source, str(SCRIPT), "exec"), installer.__dict__)


class PlatformInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.operator = installer.Installer(ROOT / "scripts/gcp", "artifacts/gcp/bduk.json")
        self.operator.root = self.root
        self.operator.config_path = self.root / "artifacts/gcp/bduk.json"
        self.config = self.operator.gcp.load_config(ROOT / "infra/gcp/environments/bduk-sandpit/config.example.json")
        self.output = self.root / "artifacts/gcp/synthetic-output"
        self.output.mkdir(parents=True)
        self.operator.evidence = self.output / "installer"
        self.operator.evidence.mkdir()
        self.operator.lifecycle = Mock(directory=self.output)
        self.operator.lifecycle.prepared_status.return_value = {"status": "NOT_PREPARED"}

    def tearDown(self):
        self.temporary.cleanup()

    def write_config(self, config=None, mode=0o600):
        self.operator.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.operator.config_path.write_text(json.dumps(config or self.config))
        self.operator.config_path.chmod(mode)

    def review(self, result=0, skip=False):
        with patch.object(self.operator, "step", return_value=result) as step:
            code = self.operator.review(skip)
        return code, [call.args[0] for call in step.call_args_list]

    def test_init_is_exclusive_private_and_does_not_grant_authority(self):
        with patch.object(self.operator.gcp, "load_config", return_value=self.config), patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "a" * 40 + "\n", "")):
            result = self.operator.initialise()
            original = self.operator.config_path.read_bytes()
            with self.assertRaises(FileExistsError):
                self.operator.initialise()
        self.assertEqual(original, self.operator.config_path.read_bytes())
        self.assertEqual(self.operator.config_path.stat().st_mode & 0o777, 0o600)
        generated = json.loads(original)
        self.assertEqual(result["profile"], "bduk-sandpit-network-private")
        self.assertFalse(generated["authority"]["cloud_mutations_approved"])
        self.assertIsNone(generated["authority"]["spend_envelope"])
        self.assertIsNone(generated["authority"]["pilot_end"])
        self.assertFalse(generated["network"]["create_access_vm"])
        self.assertEqual(len(generated["state"]["store_nonce"]), 32)
        self.assertEqual(generated["state"]["software_revision"], "a" * 40)

    def test_private_path_rejects_source_file_and_symlink(self):
        self.operator.config_path = self.root / "source.json"
        with self.assertRaisesRegex(self.operator.gcp.GateError, "artifacts/gcp"):
            self.operator.private_path()
        target = self.root / "actual"
        target.mkdir()
        (self.root / "artifacts/gcp/redirect").symlink_to(target, target_is_directory=True)
        self.operator.config_path = self.root / "artifacts/gcp/redirect/bduk.json"
        with self.assertRaisesRegex(self.operator.gcp.GateError, "symlink"):
            self.operator.private_path()

    def test_public_readable_config_is_refused(self):
        self.write_config(mode=0o644)
        with self.assertRaisesRegex(self.operator.gcp.GateError, "owner-private"):
            self.operator.load()

    def test_personal_profile_cannot_use_bduk_installer(self):
        config = self.operator.gcp.load_config(ROOT / "infra/gcp/environments/personal/config.example.json")
        self.write_config(config)
        with self.assertRaisesRegex(self.operator.gcp.GateError, "personal authority"):
            self.operator.load()

    def test_personal_vm_flags_refused_before_any_lifecycle(self):
        for flag in ("create_access_vm", "access_vm_on_demand"):
            config = json.loads(json.dumps(self.config))
            config["network"][flag] = True
            self.write_config(config)
            with patch.object(self.operator.gcp, "Lifecycle") as lifecycle, self.assertRaisesRegex(self.operator.gcp.GateError, "without a personal"):
                self.operator.load()
            lifecycle.assert_not_called()

    def test_personal_access_mode_refused_even_without_vm(self):
        self.config["network"]["access_mode"] = "iap-ssh-to-private-vpc"
        self.write_config()
        with patch.object(self.operator.gcp, "Lifecycle") as lifecycle, self.assertRaisesRegex(self.operator.gcp.GateError, "access_mode"):
            self.operator.load()
        lifecycle.assert_not_called()

    def test_review_never_applies_and_attempts_independent_package(self):
        code, actions = self.review(result=2)
        self.assertEqual(code, 2)
        self.assertEqual(actions, ["preflight", "prepare", "plan", "package-approval"])

    def test_verified_preparation_is_reused(self):
        self.operator.lifecycle.prepared_status.return_value = {"status": "PASS"}
        code, actions = self.review()
        self.assertEqual(code, 0)
        self.assertEqual(actions, ["preflight", "plan", "package-approval"])
        self.assertEqual(self.operator.steps[0]["action"], "reuse-verified-preparation")

    def test_unverified_existing_preparation_is_never_removed(self):
        directory = self.output / "prepared"
        directory.mkdir()
        marker = directory / "retain.txt"
        marker.write_text("previous review material")
        code, actions = self.review()
        self.assertEqual(code, 2)
        self.assertEqual(actions, ["preflight", "plan", "package-approval"])
        self.assertEqual(marker.read_text(), "previous review material")

    def test_skip_prepare_can_package_without_image(self):
        code, actions = self.review(result=2, skip=True)
        self.assertEqual(code, 2)
        self.assertEqual(actions, ["preflight", "plan", "package-approval"])
        self.operator.lifecycle.prepared_status.assert_not_called()

    def test_zero_exit_blocked_status_propagates_and_output_remains_private(self):
        with patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"status":"BLOCKED","principal":"synthetic-private-value"}', "")), contextlib.redirect_stderr(io.StringIO()) as stderr:
            code = self.operator.step("status")
        self.assertEqual(code, 2)
        self.assertNotIn("synthetic-private-value", stderr.getvalue())
        output = Path(self.operator.steps[0]["evidence"])
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_prepare_cannot_pass_without_verified_image_material(self):
        with patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"image":{"status":"BLOCKED"}}', "")), contextlib.redirect_stderr(io.StringIO()):
            code = self.operator.step("prepare")
        self.assertEqual(code, 2)
        self.operator.lifecycle.prepared_status.assert_called_once()

    def run_main(self, args, returns=None):
        fake = Mock(gcp=self.operator.gcp)
        fake.step.side_effect = returns or [0, 0, 0]
        fake.finish.return_value = {"status": "synthetic-orchestration-only"}
        with patch.object(installer, "Installer", return_value=fake), patch.object(installer.os, "umask"), contextlib.redirect_stdout(io.StringIO()):
            code = installer.main(ROOT / "scripts/gcp", args)
        return code, fake

    def test_install_requires_explicit_existing_plan_before_loading_config(self):
        with patch.object(installer, "Installer") as factory, contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            installer.main(ROOT / "scripts/gcp", ["install"])
        self.assertEqual(error.exception.code, 2)
        factory.assert_not_called()

    def test_install_only_applies_exact_plan_then_verifies_and_observes(self):
        plan = "b" * 24
        code, fake = self.run_main(["install", "--approved-plan", plan])
        self.assertEqual(code, 0)
        self.assertEqual([call.args for call in fake.step.call_args_list], [("apply", "--approved-plan", plan), ("verify",), ("status",)])
        fake.initialise.assert_not_called()
        fake.review.assert_not_called()

    def test_failed_apply_stops_without_reprepare_or_verification(self):
        code, fake = self.run_main(["install", "--approved-plan", "b" * 24], [2])
        self.assertEqual(code, 2)
        self.assertEqual(fake.step.call_count, 1)
        fake.review.assert_not_called()

    def test_unproved_hosted_verification_still_observes_status_and_stays_blocked(self):
        code, fake = self.run_main(["install", "--approved-plan", "b" * 24], [0, 2, 0])
        self.assertEqual(code, 2)
        self.assertEqual(fake.step.call_count, 3)

    def test_destroy_requires_own_explicit_plan_and_is_not_automatic(self):
        code, fake = self.run_main(["destroy", "--approved-plan", "c" * 24])
        self.assertEqual(code, 0)
        fake.step.assert_called_once_with("destroy", "--approved-plan", "c" * 24)

    def test_rollback_preserves_existing_release_contract(self):
        code, fake = self.run_main(["rollback", "--release", "previous-approved-release"])
        self.assertEqual(code, 0)
        fake.step.assert_called_once_with("rollback", "--release", "previous-approved-release")

    def test_bduk_connect_does_not_invoke_personal_tunnel(self):
        code, fake = self.run_main(["connect"])
        self.assertEqual(code, 2)
        fake.step.assert_not_called()

    def test_actual_shell_entrypoint_runs_help_from_another_directory(self):
        result = subprocess.run([str(SCRIPT), "--help"], cwd=self.root, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("BDUK GCP sandpit", result.stdout)


if __name__ == "__main__":
    unittest.main()
