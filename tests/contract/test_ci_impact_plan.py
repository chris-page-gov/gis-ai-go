from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from plan_ci_impact import (  # noqa: E402
    ImpactPlanError,
    canonical_json_bytes,
    changed_paths_between,
    load_impact_map,
    plan_for_paths,
    write_new_output,
)


MAP_PATH = ROOT / ".github" / "ci" / "verification-impact-map.v1.json"
SOURCE_LOCK_PATH = ROOT / "okf" / "source-lock.json"
BASE = "1" * 40
HEAD = "2" * 40
REQUIRED_OKF_PR_LANES = {"gateway_image", "repository_assurance"}
RESEARCH_OKF_INPUTS = (
    "docs/research/2026-08-19/research-pack/data/providers.json",
    "docs/research/2026-08-19/research-pack/data/sources.json",
    "docs/research/2026-08-19/research-pack/data/workflows.json",
)
LOCKED_OKF_INPUTS = tuple(
    item["path"]
    for item in json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))["inputs"]
)


class CiImpactPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.impact_map = load_impact_map(MAP_PATH)

    def plan(self, *paths: str) -> dict[str, object]:
        return plan_for_paths(
            self.impact_map,
            paths,
            base_commit=BASE,
            head_commit=HEAD,
            event="pull_request",
        )

    def assert_locked_okf_inputs_select_image_assurance(self, impact_map: object) -> None:
        for path in LOCKED_OKF_INPUTS:
            plan = plan_for_paths(
                impact_map,
                [path],
                base_commit=BASE,
                head_commit=HEAD,
                event="pull_request",
            )
            self.assertTrue(
                REQUIRED_OKF_PR_LANES.issubset(set(plan["selected_lanes"])),
                f"locked OKF input {path!r} did not select repository and image assurance",
            )

    def test_qual_harness_change_selects_repository_assurance_only(self) -> None:
        plan = self.plan("scripts/qual_206_claude_capability_harness.mjs")
        self.assertFalse(plan["force_full"])
        self.assertEqual(plan["reason"], "matched-rules")
        self.assertEqual(plan["selected_lanes"], ["repository_assurance"])
        self.assertEqual(
            plan["matched_rule_ids"],
            ["qual-206-evidence", "repository-tests-and-tooling"],
        )

    def test_qual_schema_also_selects_the_gateway_derivation_chain(self) -> None:
        plan = self.plan("schemas/qual-206-claude-capability-evidence-v1.schema.json")
        self.assertFalse(plan["force_full"])
        self.assertEqual(
            plan["selected_lanes"],
            [
                "gateway_image",
                "repository_assurance",
            ],
        )
        self.assertEqual(plan["matched_rule_ids"], ["gateway-build-context"])

    def test_documentation_change_selects_repository_assurance_only(self) -> None:
        plan = self.plan("docs/implementation/ROADMAP.md")
        self.assertFalse(plan["force_full"])
        self.assertEqual(plan["selected_lanes"], ["repository_assurance"])
        self.assertEqual(plan["matched_rule_ids"], ["documentation-and-governance"])

    def test_locked_research_inputs_select_okf_image_assurance(self) -> None:
        for path in RESEARCH_OKF_INPUTS:
            with self.subTest(path=path):
                plan = self.plan(path)
                self.assertFalse(plan["force_full"])
                self.assertEqual(
                    plan["selected_lanes"],
                    ["gateway_image", "repository_assurance"],
                )
                self.assertEqual(
                    plan["matched_rule_ids"],
                    ["documentation-and-governance", "governed-okf-publication"],
                )

    def test_every_locked_okf_input_selects_repository_and_image_assurance(self) -> None:
        self.assert_locked_okf_inputs_select_image_assurance(self.impact_map)

    def test_nearby_unlocked_research_document_remains_repository_only(self) -> None:
        plan = self.plan(
            "docs/research/2026-08-19/research-pack/data/decisions.json"
        )
        self.assertFalse(plan["force_full"])
        self.assertEqual(plan["selected_lanes"], ["repository_assurance"])
        self.assertEqual(plan["matched_rule_ids"], ["documentation-and-governance"])

    def test_locked_research_inputs_force_full_exact_commit_on_main(self) -> None:
        for path in RESEARCH_OKF_INPUTS:
            with self.subTest(path=path):
                plan = plan_for_paths(
                    self.impact_map,
                    [path],
                    base_commit=BASE,
                    head_commit=HEAD,
                    event="push_main",
                )
                self.assertTrue(plan["force_full"])
                self.assertEqual(plan["reason"], "protected-main-exact-commit")
                self.assertEqual(
                    plan["selected_lanes"], list(self.impact_map.full_lanes)
                )

    def test_source_lock_coverage_fails_if_a_locked_mapping_is_removed(self) -> None:
        document = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        rule = next(
            item
            for item in document["rules"]
            if item["id"] == "governed-okf-publication"
        )
        rule["patterns"].remove(RESEARCH_OKF_INPUTS[0])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            mutated_map = load_impact_map(path)
            with self.assertRaises(AssertionError):
                self.assert_locked_okf_inputs_select_image_assurance(mutated_map)

    def test_global_workflow_change_selects_every_lane(self) -> None:
        plan = self.plan(".github/workflows/ci.yml")
        self.assertTrue(plan["force_full"])
        self.assertEqual(plan["reason"], "force-full-rule")
        self.assertEqual(
            plan["selected_lanes"], ["gateway_image", "repository_assurance"]
        )
        self.assertEqual(plan["force_full_rule_ids"], ["global-assurance-control"])

    def test_unknown_path_fails_closed_to_every_lane(self) -> None:
        plan = self.plan("future-component/source/new-runtime.ts")
        self.assertTrue(plan["force_full"])
        self.assertEqual(plan["reason"], "unmatched-path")
        self.assertEqual(plan["unmatched_paths"], ["future-component/source/new-runtime.ts"])
        self.assertEqual(
            plan["selected_lanes"], ["gateway_image", "repository_assurance"]
        )

    def test_empty_change_set_fails_closed_to_every_lane(self) -> None:
        plan = self.plan()
        self.assertTrue(plan["force_full"])
        self.assertEqual(plan["reason"], "empty-change-set")
        self.assertEqual(
            plan["selected_lanes"], ["gateway_image", "repository_assurance"]
        )

    def test_gateway_dependency_closure_is_expanded_deterministically(self) -> None:
        plan = self.plan("apps/mcp-gateway/src/server.ts")
        self.assertEqual(
            plan["selected_lanes"],
            [
                "gateway_image",
                "repository_assurance",
            ],
        )
        self.assertEqual(
            canonical_json_bytes(plan),
            canonical_json_bytes(self.plan("apps/mcp-gateway/src/server.ts")),
        )

    def test_push_main_gateway_plan_expands_the_provenance_chain(self) -> None:
        plan = plan_for_paths(
            self.impact_map,
            ["apps/mcp-gateway/src/server.ts"],
            base_commit=BASE,
            head_commit=HEAD,
            event="push_main",
        )
        self.assertEqual(
            plan["selected_lanes"],
            [
                "gateway-provenance",
                "gateway_attestation_verification",
                "gateway_image",
                "gateway_independent_image",
                "provenance",
                "repository_assurance",
            ],
        )
        self.assertEqual(plan["reason"], "protected-main-exact-commit")
        self.assertTrue(plan["force_full"])

    def test_push_main_documentation_plan_retains_full_exact_commit_evidence(self) -> None:
        plan = plan_for_paths(
            self.impact_map,
            ["docs/implementation/ROADMAP.md"],
            base_commit=BASE,
            head_commit=HEAD,
            event="push_main",
        )
        self.assertEqual(plan["reason"], "protected-main-exact-commit")
        self.assertEqual(plan["selected_lanes"], list(self.impact_map.full_lanes))

    def test_unsafe_changed_path_is_rejected(self) -> None:
        with self.assertRaisesRegex(ImpactPlanError, "unsafe path component"):
            self.plan("../outside")
        with self.assertRaisesRegex(ImpactPlanError, "control character"):
            self.plan("docs/forged\nheading.md")

    def test_map_rejects_a_non_full_unknown_path_policy(self) -> None:
        document = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        document["unknown_path_policy"] = "none"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ImpactPlanError, "must select full assurance"):
                load_impact_map(path)

    def test_map_rejects_duplicate_keys_and_non_standard_constants(self) -> None:
        source = MAP_PATH.read_text(encoding="utf-8")
        invalid_documents = (
            (
                source.replace(
                    '"mode": "shadow",',
                    '"mode": "shadow",\n  "mode": "shadow",',
                    1,
                ),
                "duplicate JSON key",
            ),
            (
                source.replace('"mode": "shadow"', '"mode": NaN', 1),
                "non-standard JSON constant",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            for index, (content, message) in enumerate(invalid_documents):
                with self.subTest(message=message):
                    path = Path(directory) / f"invalid-{index}.json"
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaisesRegex(ImpactPlanError, message):
                        load_impact_map(path)

    def test_map_rejects_an_event_incompatible_dependency(self) -> None:
        document = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        lane = next(
            item
            for item in document["lanes"]
            if item["id"] == "gateway_attestation_verification"
        )
        lane["events"] = ["pull_request", "push_main"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ImpactPlanError, "not available"):
                load_impact_map(path)

    def test_git_rename_inventory_includes_old_and_new_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(("git", "init", "-q"), cwd=root, check=True)
            subprocess.run(
                ("git", "config", "user.email", "ci-impact@example.invalid"),
                cwd=root,
                check=True,
            )
            subprocess.run(
                ("git", "config", "user.name", "CI impact test"),
                cwd=root,
                check=True,
            )
            old = root / "docs" / "old.md"
            old.parent.mkdir()
            old.write_text("bounded\n", encoding="utf-8")
            subprocess.run(("git", "add", "docs/old.md"), cwd=root, check=True)
            subprocess.run(("git", "commit", "-qm", "first"), cwd=root, check=True)
            base = subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=root).decode(
                "ascii"
            ).strip()
            subprocess.run(
                ("git", "mv", "docs/old.md", "docs/new.md"), cwd=root, check=True
            )
            subprocess.run(("git", "commit", "-qm", "rename"), cwd=root, check=True)
            head = subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=root).decode(
                "ascii"
            ).strip()
            self.assertEqual(
                changed_paths_between(root, base, head),
                ("docs/new.md", "docs/old.md"),
            )

    def test_locked_input_rename_evaluates_old_and_new_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(("git", "init", "-q"), cwd=root, check=True)
            subprocess.run(
                ("git", "config", "user.email", "ci-impact@example.invalid"),
                cwd=root,
                check=True,
            )
            subprocess.run(
                ("git", "config", "user.name", "CI impact test"),
                cwd=root,
                check=True,
            )
            old = root / RESEARCH_OKF_INPUTS[0]
            old.parent.mkdir(parents=True)
            old.write_text("{}\n", encoding="utf-8")
            subprocess.run(("git", "add", RESEARCH_OKF_INPUTS[0]), cwd=root, check=True)
            subprocess.run(("git", "commit", "-qm", "first"), cwd=root, check=True)
            base = subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=root).decode(
                "ascii"
            ).strip()
            new_path = "docs/research/2026-08-19/research-pack/data/decisions.json"
            subprocess.run(
                ("git", "mv", RESEARCH_OKF_INPUTS[0], new_path), cwd=root, check=True
            )
            subprocess.run(("git", "commit", "-qm", "rename"), cwd=root, check=True)
            head = subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=root).decode(
                "ascii"
            ).strip()
            changed_paths = changed_paths_between(root, base, head)
            self.assertEqual(changed_paths, (new_path, RESEARCH_OKF_INPUTS[0]))
            plan = plan_for_paths(
                self.impact_map,
                changed_paths,
                base_commit=base,
                head_commit=head,
                event="pull_request",
            )
            self.assertTrue(REQUIRED_OKF_PR_LANES.issubset(set(plan["selected_lanes"])))

    def test_output_is_new_and_repository_relative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_new_output(root, Path("artifacts/ci/plan.json"), b"{}\n")
            self.assertEqual(target.read_bytes(), b"{}\n")
            with self.assertRaisesRegex(ImpactPlanError, "already exists"):
                write_new_output(root, Path("artifacts/ci/plan.json"), b"{}\n")
            with self.assertRaisesRegex(ImpactPlanError, "repository relative"):
                write_new_output(root, Path("/tmp/plan.json"), b"{}\n")


if __name__ == "__main__":
    unittest.main()
