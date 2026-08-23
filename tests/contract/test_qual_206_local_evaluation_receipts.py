from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "qual-206-local-evaluation-receipt-set.schema.json"
RECEIPT_PATH = ROOT / "evaluation" / "qual-206-local-evaluation-receipts.v1.json"
EVALUATION_PATH = ROOT / "evaluation" / "evaluation-cases.json"
PACKAGE_PATH = ROOT / "package.json"
EXPECTED_CASE_IDS = ["E01", "E02", "E09", "E13", "E15", "E17", "E20"]
EXPECTED_SUITE_LABELS = [
    "catalogue-snapshot",
    "catalogue-application",
    "selection-application",
    "data-query-application",
    "evidence-application",
    "public-read-transport",
    "http-application",
    "readiness-integrity",
    "blocked-container",
    "interoperability-stdio",
    "tool-registry",
    "trace-context",
    "provider-adapter",
    "approved-provider-cache",
    "fixed-https-parser-boundary",
    "public-explorer",
]
BOUNDARY = (
    "Repository-only deterministic evidence. It is non-live and unscored, does not "
    "complete the research case, and does not authorise activation, deployment, "
    "registration or release."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> str:
    if value is None or isinstance(value, (bool, str)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, int):
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise ValueError("Canonical numbers must be JavaScript-safe integers")
        return str(value)
    if isinstance(value, list):
        return f"[{','.join(canonical(item) for item in value)}]"
    if isinstance(value, dict):
        members = (
            f"{json.dumps(key, ensure_ascii=False)}:{canonical(value[key])}"
            for key in sorted(value)
        )
        return f"{{{','.join(members)}}}"
    raise TypeError(f"Unsupported canonical value: {type(value)!r}")


def identity(domain: str, value: dict[str, Any]) -> str:
    prefix = f"GIS-AI-GO\0{domain}\0v1\0".encode()
    return hashlib.sha256(prefix + canonical(value).encode()).hexdigest()


def assert_contract_objects_are_closed(
    test_case: unittest.TestCase,
    node: object,
    path: str = "$",
) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            test_case.assertIs(
                node.get("additionalProperties"),
                False,
                f"{path} must reject unknown properties",
            )
        for key, value in node.items():
            assert_contract_objects_are_closed(test_case, value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_contract_objects_are_closed(test_case, value, f"{path}[{index}]")


class Qual206LocalEvaluationReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.document = load_json(RECEIPT_PATH)
        cls.evaluation = load_json(EVALUATION_PATH)
        cls.validator = Draft202012Validator(cls.schema)

    def assert_invalid(self, value: object) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_closed_schema_accepts_the_committed_receipt_set(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        assert_contract_objects_are_closed(self, self.schema)
        errors = sorted(
            self.validator.iter_errors(self.document),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(
            [],
            [
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
                for error in errors
            ],
        )
        expected_bytes = (
            json.dumps(self.document, ensure_ascii=False, indent=2) + "\n"
        ).encode()
        self.assertEqual(RECEIPT_PATH.read_bytes(), expected_bytes)

    def test_receipts_cover_exactly_the_bounded_local_cases(self) -> None:
        manifest_cases = {
            case["id"]: (index, case)
            for index, case in enumerate(self.evaluation["cases"])
        }
        self.assertEqual(
            [receipt["case"]["id"] for receipt in self.document["receipts"]],
            EXPECTED_CASE_IDS,
        )
        self.assertEqual(
            [suite["label"] for suite in self.document["suites"]],
            EXPECTED_SUITE_LABELS,
        )
        self.assertEqual(
            self.document["evaluation_manifest"],
            {
                "path": "evaluation/evaluation-cases.json",
                "sha256": sha256(EVALUATION_PATH),
                "case_count": len(self.evaluation["cases"]),
            },
        )

        suite_ids = {suite["suite_id"] for suite in self.document["suites"]}
        self.assertEqual(len(suite_ids), len(EXPECTED_SUITE_LABELS))
        referenced_suite_ids: set[str] = set()
        for receipt in self.document["receipts"]:
            case_id = receipt["case"]["id"]
            manifest_index, manifest_case = manifest_cases[case_id]
            with self.subTest(case=case_id):
                self.assertEqual(receipt["case"]["title"], manifest_case["title"])
                self.assertEqual(
                    receipt["case"]["manifest_pointer"],
                    f"/cases/{manifest_index}",
                )
                self.assertEqual(receipt["outcome"]["case_complete"], False)
                self.assertEqual(receipt["outcome"]["scoring"], "unscored")
                self.assertEqual(receipt["boundary"], BOUNDARY)
                self.assertTrue(set(receipt["evidence_suite_ids"]) <= suite_ids)
                referenced_suite_ids.update(receipt["evidence_suite_ids"])
                self.assertEqual(
                    len(receipt["local_assertions"]),
                    len({item["id"] for item in receipt["local_assertions"]}),
                )
        self.assertEqual(referenced_suite_ids, suite_ids)

    def test_material_and_content_identities_bind_exact_repository_bytes(self) -> None:
        schema_contract = self.document["schema_contract"]
        self.assertEqual(
            schema_contract,
            {
                "path": "schemas/qual-206-local-evaluation-receipt-set.schema.json",
                "sha256": sha256(SCHEMA_PATH),
            },
        )
        generator = self.document["generator"]
        self.assertEqual(generator["sha256"], sha256(ROOT / generator["path"]))
        self.assertEqual(generator["package_json_sha256"], sha256(PACKAGE_PATH))
        self.assertEqual(
            generator["pnpm_lock_sha256"],
            sha256(ROOT / "pnpm-lock.yaml"),
        )

        for suite in self.document["suites"]:
            with self.subTest(suite=suite["label"]):
                material_paths = [item["path"] for item in suite["materials"]]
                self.assertEqual(material_paths, sorted(set(material_paths)))
                for item in suite["materials"]:
                    path = (ROOT / item["path"]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT.resolve()))
                    self.assertTrue(path.is_file(), item["path"])
                    self.assertEqual(item["sha256"], sha256(path))
                core = {key: value for key, value in suite.items() if key != "suite_id"}
                expected_id = (
                    "gis-ai-go:qual-206-local-suite-evidence:sha256:"
                    f"{identity('qual-206-local-suite-evidence', core)}"
                )
                self.assertEqual(suite["suite_id"], expected_id)

        for receipt in self.document["receipts"]:
            core = {key: value for key, value in receipt.items() if key != "receipt_id"}
            expected_id = (
                "gis-ai-go:qual-206-local-evaluation-receipt:sha256:"
                f"{identity('qual-206-local-evaluation-receipt', core)}"
            )
            self.assertEqual(receipt["receipt_id"], expected_id)

        core = {key: value for key, value in self.document.items() if key != "set_id"}
        expected_set_id = (
            "gis-ai-go:qual-206-local-evaluation-set:sha256:"
            f"{identity('qual-206-local-evaluation-set', core)}"
        )
        self.assertEqual(self.document["set_id"], expected_set_id)

    def test_receipts_make_no_live_host_or_release_claim(self) -> None:
        self.assertEqual(self.document["boundary"], BOUNDARY)
        self.assertEqual(set(self.document["claims"].values()), {False})
        for suite in self.document["suites"]:
            self.assertEqual(set(suite["controls"].values()), {False})
            self.assertIn(suite["command"][0], {"node", "pnpm"})
            for forbidden in ("curl", "docker", "gh", "git", "--write"):
                self.assertNotIn(forbidden, suite["command"])

        serialised = json.dumps(self.document, ensure_ascii=False)
        for private_prefix in ("/Users/", "/private/", "file://"):
            self.assertNotIn(private_prefix, serialised)

        scripts = load_json(PACKAGE_PATH)["scripts"]
        self.assertIn(
            "node scripts/qual_206_local_evaluations.mjs --check",
            scripts["test:qual-206-local-evaluations"],
        )
        self.assertIn(
            "node scripts/qual_206_local_evaluations.mjs --write",
            scripts["generate:qual-206-local-evaluations"],
        )
        for name in (
            "test:qual-206-local-evaluations",
            "generate:qual-206-local-evaluations",
        ):
            self.assertTrue(
                scripts[name].endswith(
                    "python -m unittest "
                    "tests.contract.test_qual_206_local_evaluation_receipts"
                )
            )

    def test_schema_rejects_claim_inflation_drift_and_extra_cases(self) -> None:
        unknown = copy.deepcopy(self.document)
        unknown["receipts"][0]["unexpected"] = True
        self.assert_invalid(unknown)

        complete = copy.deepcopy(self.document)
        complete["receipts"][0]["outcome"]["case_complete"] = True
        self.assert_invalid(complete)

        live = copy.deepcopy(self.document)
        live["claims"]["live_host_session"] = True
        self.assert_invalid(live)

        extra_case = copy.deepcopy(self.document)
        extra_case["receipts"].append(copy.deepcopy(extra_case["receipts"][0]))
        self.assert_invalid(extra_case)

        duplicate_case = copy.deepcopy(self.document)
        duplicate_case["receipts"][1]["case"] = copy.deepcopy(
            duplicate_case["receipts"][0]["case"]
        )
        self.assert_invalid(duplicate_case)

        reordered_suites = copy.deepcopy(self.document)
        reordered_suites["suites"][0:2] = reversed(reordered_suites["suites"][0:2])
        self.assert_invalid(reordered_suites)

        absolute_material = copy.deepcopy(self.document)
        absolute_material["suites"][0]["materials"][0]["path"] = "/tmp/result.json"
        self.assert_invalid(absolute_material)


if __name__ == "__main__":
    unittest.main()
