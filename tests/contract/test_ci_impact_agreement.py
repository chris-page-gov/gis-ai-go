from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agree_ci_impact import MAX_PLAN_BYTES, agree, canonical_bytes, write_receipt  # noqa: E402
from plan_ci_impact import changed_paths_between, load_impact_map, plan_for_paths  # noqa: E402


MAP = Path(".github/ci/verification-impact-map.v2.json")


class CiImpactAgreementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name).resolve()
        self.root = self.directory / "candidate"
        self.root.mkdir()
        self.trusted = self.directory / "trusted"
        self.trusted.mkdir()
        for name in ("agree_ci_impact.py", "plan_ci_impact.py"):
            (self.trusted / name).write_bytes((SCRIPTS / name).read_bytes())
        self.git("init", "-q")
        self.git("config", "user.email", "ci-agreement@example.invalid")
        self.git("config", "user.name", "CI agreement fixture")
        self.write(MAP.as_posix(), (ROOT / MAP).read_text())
        self.write("docs/example.md", "base\n")
        self.write("apps/mcp-gateway/src/example.ts", "export const value = 1;\n")
        self.write("scripts/plan_ci_impact.py", (SCRIPTS / "plan_ci_impact.py").read_text())
        self.base = self.commit("base")
        self.write("docs/example.md", "candidate\n")
        self.head = self.commit("candidate")
        self.candidate = self.directory / "candidate-plan.json"
        self.make_plan()

    def git(self, *arguments: str) -> bytes:
        return subprocess.check_output(("git", *arguments), cwd=self.root, stderr=subprocess.DEVNULL)

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, message: str) -> str:
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD").decode().strip()

    def make_plan(self, event: str = "pull_request") -> dict[str, object]:
        result = plan_for_paths(
            load_impact_map(self.root / MAP),
            changed_paths_between(self.root, self.base, self.head),
            base_commit=self.base, head_commit=self.head, event=event,
        )
        self.candidate.write_bytes(canonical_bytes(result))
        return result

    def receipt(self, **overrides: object) -> dict[str, object]:
        arguments = dict(
            repository_root=self.root, base=self.base, head=self.head,
            event="pull_request", candidate_plan=self.candidate, candidate_result="success",
        )
        arguments.update(overrides)
        return agree(**arguments)

    def assert_full(self, receipt: dict[str, object]) -> None:
        self.assertIs(receipt["gateway_image_required"], True)
        self.assertIs(receipt["force_full"], True)
        self.assertIs(receipt["enforced"], False)
        self.assertEqual(receipt["mode"], "shadow")

    def test_documentation_agreement_binds_both_policies_and_inventory(self) -> None:
        receipt = self.receipt()
        self.assertIs(receipt["gateway_image_required"], False)
        self.assertIs(receipt["force_full"], False)
        self.assertIs(receipt["enforced"], False)
        self.assertEqual(receipt["reason"], "both-policies-omit-image")
        self.assertEqual(receipt["changed_paths"], ["docs/example.md"])
        self.assertEqual(receipt["base_commit"], self.base)
        self.assertEqual(receipt["head_commit"], self.head)
        self.assertEqual(receipt["policy_source_commit"], self.base)
        self.assertEqual(receipt["base_map_sha256"], receipt["candidate_map_sha256"])
        self.assertEqual(receipt["candidate_plan_sha256"], receipt["expected_candidate_plan_sha256"])
        self.assertEqual(receipt["base_decision"], receipt["candidate_decision"])
        for field in ("agreement_sha256", "planner_sha256", "base_plan_sha256"):
            self.assertRegex(receipt[field], r"^[0-9a-f]{64}$")

    def test_gateway_change_requires_image_from_both_policies(self) -> None:
        self.write("apps/mcp-gateway/src/example.ts", "export const value = 2;\n")
        self.head = self.commit("gateway")
        self.make_plan()
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "both-policies-require-image")

    def test_counterfeit_false_recommendation_cannot_hide_gateway_change(self) -> None:
        self.write("apps/mcp-gateway/src/example.ts", "export const value = 2;\n")
        self.head = self.commit("gateway")
        counterfeit = self.make_plan()
        counterfeit["gateway_image_required"] = False
        counterfeit["selected_lanes"] = ["repository_assurance"]
        counterfeit["lane_decisions"]["gateway_image"] = False
        self.candidate.write_bytes(canonical_bytes(counterfeit))
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "candidate-plan-mismatch")

    def test_policy_is_read_from_exact_git_blobs_not_dirty_checkout_files(self) -> None:
        self.write(MAP.as_posix(), "not JSON; uncommitted candidate preparation\n")
        self.write("scripts/plan_ci_impact.py", "raise RuntimeError('untrusted Python')\n")
        receipt = self.receipt()
        self.assertIs(receipt["gateway_image_required"], False)
        self.assertEqual(receipt["reason"], "both-policies-omit-image")

    def test_missing_or_linked_base_policy_cannot_authorise_reduction(self) -> None:
        self.git("rm", MAP.as_posix())
        self.base = self.commit("missing base map")
        self.write("docs/example.md", "another candidate\n")
        self.head = self.commit("candidate")
        self.assert_full(self.receipt())
        target = self.root / "docs" / "map.json"
        target.write_bytes((ROOT / MAP).read_bytes())
        (self.root / MAP).parent.mkdir(parents=True, exist_ok=True)
        (self.root / MAP).symlink_to("../../docs/map.json")
        self.base = self.commit("linked base map")
        self.write("docs/example.md", "last candidate\n")
        self.head = self.commit("candidate")
        self.assert_full(self.receipt())

    def test_candidate_control_map_mutation_cannot_govern_itself(self) -> None:
        mapping = json.loads((self.root / MAP).read_text())
        control = next(rule for rule in mapping["rules"] if rule["id"] == "global-assurance-control")
        documentation = next(rule for rule in mapping["rules"] if rule["id"] == "documentation-and-governance")
        for pattern in (".github/**", "scripts/plan_ci_impact.py"):
            control["patterns"].remove(pattern)
            documentation["patterns"].append(pattern)
        documentation["patterns"].sort()
        self.write(MAP.as_posix(), json.dumps(mapping))
        self.head = self.commit("weaken candidate map")
        self.assertIs(self.make_plan()["gateway_image_required"], False)
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "control-path-change")
        self.assertIs(receipt["base_decision"]["force_full"], True)
        self.assertIs(receipt["candidate_decision"]["gateway_image_required"], False)
        self.assertNotEqual(receipt["base_map_sha256"], receipt["candidate_map_sha256"])

    def test_control_changes_remain_full_even_if_base_mapping_is_weakened(self) -> None:
        mapping = json.loads((self.root / MAP).read_text())
        control = next(rule for rule in mapping["rules"] if rule["id"] == "global-assurance-control")
        control["patterns"].remove(".github/**")
        documentation = next(rule for rule in mapping["rules"] if rule["id"] == "documentation-and-governance")
        documentation["patterns"] = sorted([*documentation["patterns"], ".github/**"])
        self.write(MAP.as_posix(), json.dumps(mapping))
        self.base = self.commit("weak base")
        self.write(".github/workflows/ci.yml", "name: changed\n")
        self.head = self.commit("workflow")
        self.make_plan()
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "trusted-control-route-not-full")

    def test_every_agreement_control_path_requires_full(self) -> None:
        from agree_ci_impact import CONTROL_PATHS
        for name in sorted(CONTROL_PATHS):
            with self.subTest(path=name):
                self.write(name, "candidate control bytes\n")
                self.head = self.commit("control change")
                self.make_plan()
                receipt = self.receipt()
                self.assert_full(receipt)
                self.assertIn(receipt["reason"], ("control-path-change", "trusted-control-route-not-full"))

    def test_candidate_python_is_never_executed_by_trusted_cli(self) -> None:
        marker = self.directory / "executed"
        malicious = f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\nraise SystemExit(99)\n"
        self.write("scripts/plan_ci_impact.py", malicious)
        self.write("json.py", malicious)
        self.write("sitecustomize.py", malicious)
        self.head = self.commit("hostile candidate Python")
        # An attacker can supply any bytes; only the trusted job reads them.
        self.candidate.write_text('{"gateway_image_required":false}\n')
        output = self.directory / "receipt.json"
        result = subprocess.run(
            (sys.executable, "-I", str(self.trusted / "agree_ci_impact.py"),
             "--repository-root", str(self.root), "--base", self.base, "--head", self.head,
             "--event", "pull_request", "--candidate-result", "success",
             "--candidate-plan", str(self.candidate), "--output", str(output)),
            cwd=self.root, capture_output=True, check=True,
        )
        self.assertEqual(result.stdout, output.read_bytes())
        self.assert_full(json.loads(result.stdout))
        self.assertFalse(marker.exists())

    def test_wrong_identity_inventory_or_boolean_type_fails_full(self) -> None:
        original = self.make_plan()
        mutations = {
            "base_commit": "1" * 40, "head_commit": "2" * 40,
            "event": "push_main", "map_sha256": "0" * 64,
            "changed_paths": [], "changed_path_count": 0, "matches": [],
            "gateway_image_required": 0, "force_full": 0, "enforced": 0,
            "always_run": [], "applicable_lanes": [], "selected_lanes": [],
            "schema": "future", "unexpected": False,
        }
        for key, value in mutations.items():
            with self.subTest(field=key):
                candidate = {**original, key: value}
                self.candidate.write_bytes(canonical_bytes(candidate))
                self.assert_full(self.receipt())
        candidate = dict(original)
        candidate["lane_decisions"] = {**candidate["lane_decisions"], "gateway_image": 0}
        self.candidate.write_bytes(canonical_bytes(candidate))
        self.assert_full(self.receipt())

    def test_missing_and_malformed_artifact_fail_full(self) -> None:
        self.candidate.unlink()
        self.assert_full(self.receipt())
        for raw in (b"", b"not JSON", b"null", b"[]", b"{}", b"\xff", b'{"x":NaN}', b'{"x":Infinity}'):
            with self.subTest(raw=raw):
                self.candidate.write_bytes(raw)
                self.assert_full(self.receipt())

    def test_duplicate_json_keys_are_rejected_even_when_final_value_is_correct(self) -> None:
        original = self.make_plan()
        raw = canonical_bytes(original)
        self.candidate.write_bytes(b'{"gateway_image_required":true,' + raw[1:])
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "candidate-plan-invalid")

    def test_artifact_links_and_oversized_files_fail_full(self) -> None:
        target = self.directory / "target.json"
        target.write_bytes(self.candidate.read_bytes())
        self.candidate.unlink()
        self.candidate.symlink_to(target)
        self.assert_full(self.receipt())
        self.candidate.unlink()
        with self.candidate.open("wb") as handle:
            handle.truncate(MAX_PLAN_BYTES + 1)
        self.assert_full(self.receipt())

    def test_unsuccessful_candidate_job_cannot_supply_permission(self) -> None:
        for result in ("failure", "cancelled", "skipped", "missing", ""):
            with self.subTest(result=result):
                receipt = self.receipt(candidate_result=result)
                self.assert_full(receipt)
                self.assertEqual(receipt["reason"], "candidate-job-not-successful")

    def test_push_main_always_requires_full(self) -> None:
        receipt = self.receipt(event="push_main")
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "protected-main-exact-commit")

    def test_rename_keeps_original_gateway_path_in_both_inventories(self) -> None:
        self.git("mv", "apps/mcp-gateway/src/example.ts", "docs/renamed.ts")
        self.head = self.commit("rename gateway into documentation")
        self.make_plan()
        receipt = self.receipt()
        self.assert_full(receipt)
        self.assertIn("apps/mcp-gateway/src/example.ts", receipt["changed_paths"])
        self.assertIn("docs/renamed.ts", receipt["changed_paths"])

    def test_wrong_checkout_missing_base_and_empty_inventory_fail_full(self) -> None:
        for overrides in ({"head": self.base}, {"base": "1" * 40}, {"base": self.head}, {"base": "--invalid"}):
            with self.subTest(overrides=overrides):
                self.assert_full(self.receipt(**overrides))

    def test_missing_base_evaluator_fails_full(self) -> None:
        with patch("agree_ci_impact._load_base_evaluator", side_effect=FileNotFoundError):
            self.assert_full(self.receipt())

    def test_policy_disagreement_fails_full(self) -> None:
        # A future evaluator version can change a decision; equal false scalars
        # alone must never hide differing lane or force-full recommendations.
        import agree_ci_impact
        evaluator = agree_ci_impact._load_base_evaluator()
        evaluate = evaluator.plan_for_paths
        calls = 0

        def changed_decision(*args: object, **kwargs: object) -> dict[str, object]:
            nonlocal calls
            calls += 1
            result = evaluate(*args, **kwargs)
            if calls == 1:
                result["always_run"] = [*result["always_run"], "additional-check"]
            return result

        with patch("agree_ci_impact._load_base_evaluator", return_value=evaluator), patch.object(
            evaluator, "plan_for_paths", side_effect=changed_decision,
        ):
            receipt = self.receipt()
        self.assert_full(receipt)
        self.assertEqual(receipt["reason"], "policy-disagreement")

    def test_receipt_write_is_exclusive_and_rejects_parent_aliases(self) -> None:
        output = self.directory / "receipt.json"
        write_receipt(output, b"{}\n")
        with self.assertRaises(FileExistsError):
            write_receipt(output, b"changed")
        alias = self.directory / "alias"
        alias.symlink_to(self.trusted, target_is_directory=True)
        with self.assertRaises(ValueError):
            write_receipt(alias / "receipt.json", b"{}\n")
        self.assertEqual(output.read_bytes(), b"{}\n")


if __name__ == "__main__":
    unittest.main()
