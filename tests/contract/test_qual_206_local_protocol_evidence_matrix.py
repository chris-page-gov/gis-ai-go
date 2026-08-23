from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-local-protocol-evidence-matrix.schema.json"
)
MATRIX_PATH = (
    ROOT / "evaluation" / "qual-206-local-protocol-evidence-matrix.v1.json"
)
GATEWAY_MANIFEST_PATH = ROOT / "apps" / "mcp-gateway" / "package.json"
LOCKFILE_PATH = ROOT / "pnpm-lock.yaml"
RUNTIME_BASE_COMMIT = "7fa8b720d3cbaa3e0a1ebfadf0fb355a7330a04c"
BOUNDARY = (
    "Repository-material-bound deterministic source matrix. It is repository-only, "
    "non-live and unscored; coverage rows bind source declarations but do not record "
    "test execution, the suspension regression uses in-process STDIO server wiring, "
    "and the matrix does not complete host interoperability or authorise activation, "
    "deployment, registration or release."
)
EXPECTED_RUNTIME_PATHS = [
    "apps/mcp-gateway/src/governed-assembly.ts",
    "apps/mcp-gateway/src/mcp-http.ts",
    "apps/mcp-gateway/src/mcp-request-signal.ts",
    "apps/mcp-gateway/src/mcp-server.ts",
    "apps/mcp-gateway/src/mcp-stdio.ts",
]
EXPECTED_COVERAGE = [
    (
        "official-http",
        "official-client",
        "http",
        "in-process-fetch-and-loopback",
        {
            "protocol_2026_07_28": True,
            "cancellation": False,
            "unsupported_traffic": False,
        },
    ),
    (
        "official-stdio",
        "official-client",
        "stdio",
        "real-process-stdio",
        {
            "protocol_2026_07_28": True,
            "cancellation": False,
            "unsupported_traffic": False,
        },
    ),
    (
        "raw-http",
        "raw-transcript",
        "http",
        "in-process-fetch",
        {
            "protocol_2026_07_28": True,
            "cancellation": True,
            "unsupported_traffic": True,
        },
    ),
    (
        "raw-stdio",
        "raw-transcript",
        "stdio",
        "in-process-and-real-process-stdio",
        {
            "protocol_2026_07_28": True,
            "cancellation": True,
            "unsupported_traffic": True,
        },
    ),
]
EXPECTED_SOURCE_TEST_NAMES = {
    "official-http": [
        (
            "apps/mcp-gateway/test/mcp-transport.test.ts",
            (
                "interoperates with the pinned v2 SDK client for tools and resources",
                "interoperates through the real bounded loopback Node ingress",
            ),
        )
    ],
    "official-stdio": [
        (
            "apps/mcp-gateway/test/mcp-stdio.test.ts",
            (
                "interoperates with the pinned official STDIO client in an enabled "
                "subprocess",
            ),
        )
    ],
    "raw-http": [
        (
            "apps/mcp-gateway/test/mcp-transport.test.ts",
            (
                "requires both HTTP Accept media types before entering the SDK",
                "rejects every unsafe JSON-RPC request ID before SDK dispatch",
                "guards the SDK 2.0.0 missing protocol-version header defect narrowly",
                "leaves unsupported revisions and cross-header mismatches to the pinned "
                "SDK",
            ),
        ),
        (
            "apps/mcp-gateway/test/public-read-transport.test.ts",
            (
                "propagates modern MCP HTTP cancellation with no receipt or ledger event",
            ),
        ),
    ],
    "raw-stdio": [
        (
            "apps/mcp-gateway/test/mcp-stdio.test.ts",
            (
                "serves a raw modern STDIO transcript through the same registered factory",
                "rejects every unsafe STDIO request ID before application dispatch",
                "rejects a legacy STDIO opening without pinning the connection to it",
                "bounds the reply to an exactly 1 MiB subprocess request with a huge ID",
                "keeps the executable stdout protocol-clean with frozen zero activation",
            ),
        ),
        (
            "apps/mcp-gateway/test/public-read-transport.test.ts",
            (
                "honours STDIO cancellation without a response, receipt or ledger event",
            ),
        ),
    ],
}
EXPECTED_SUSPENSION_SOURCE = (
    "apps/mcp-gateway/test/qual-206-local-protocol-matrix.test.ts",
    ("keeps every governed suspension absent and uncallable over in-process STDIO",),
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob(commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(f"Unable to read {path} from {commit}: {message}")
    return result.stdout


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


def identity(value: dict[str, Any]) -> str:
    prefix = b"GIS-AI-GO\0qual-206-local-protocol-evidence-matrix\0v1\0"
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


class Qual206LocalProtocolEvidenceMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.document = load_json(MATRIX_PATH)
        cls.validator = Draft202012Validator(cls.schema)

    def assert_invalid(self, value: object) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_closed_schema_accepts_canonical_matrix(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        assert_contract_objects_are_closed(self, self.schema)
        errors = sorted(
            self.validator.iter_errors(self.document),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(
            [],
            [
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: "
                f"{error.message}"
                for error in errors
            ],
        )
        expected_bytes = (
            json.dumps(self.document, ensure_ascii=False, indent=2) + "\n"
        ).encode()
        self.assertEqual(MATRIX_PATH.read_bytes(), expected_bytes)

    def test_matrix_binds_exact_base_git_materials_and_source_labels(self) -> None:
        self.assertEqual(
            self.document["schema_contract"],
            {
                "path": (
                    "schemas/qual-206-local-protocol-evidence-matrix.schema.json"
                ),
                "sha256": sha256(SCHEMA_PATH),
            },
        )
        binding = self.document["repository_binding"]
        self.assertEqual(binding["runtime_base_commit"], RUNTIME_BASE_COMMIT)
        self.assertEqual(
            [material["path"] for material in binding["runtime_materials"]],
            EXPECTED_RUNTIME_PATHS,
        )

        base_materials = [
            *binding["runtime_materials"],
            self.document["official_client"]["manifest"],
            self.document["official_client"]["lockfile"],
        ]
        coverage_sources = [
            source
            for row in self.document["coverage"]
            for source in row["test_sources"]
        ]
        base_scoped = [*base_materials, *coverage_sources]
        for material in base_scoped:
            with self.subTest(path=material["path"]):
                path = (ROOT / material["path"]).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                self.assertTrue(path.is_file())
                self.assertEqual(material["sha256"], sha256(path))
                self.assertEqual(
                    material["sha256"],
                    sha256_bytes(git_blob(RUNTIME_BASE_COMMIT, material["path"])),
                )

        actual_source_names = {
            row["id"]: [
                (source["path"], tuple(source["source_test_names"]))
                for source in row["test_sources"]
            ]
            for row in self.document["coverage"]
        }
        self.assertEqual(actual_source_names, EXPECTED_SOURCE_TEST_NAMES)

        suspension_source = self.document["suspension_stdio"]["test_source"]
        self.assertEqual(
            (
                suspension_source["path"],
                tuple(suspension_source["source_test_names"]),
            ),
            EXPECTED_SUSPENSION_SOURCE,
        )
        suspension_path = (ROOT / suspension_source["path"]).resolve()
        self.assertTrue(suspension_path.is_relative_to(ROOT.resolve()))
        self.assertTrue(suspension_path.is_file())
        self.assertEqual(suspension_source["sha256"], sha256(suspension_path))

        for source_entry in [*coverage_sources, suspension_source]:
            source = (ROOT / source_entry["path"]).read_text(encoding="utf-8")
            for name in source_entry["source_test_names"]:
                with self.subTest(path=source_entry["path"], source_test=name):
                    self.assertRegex(
                        source,
                        rf"(?m)^[ \t]*test\([ \t]*{re.escape(json.dumps(name))}[ \t]*,",
                    )

        core = {
            key: value for key, value in self.document.items() if key != "matrix_id"
        }
        self.assertEqual(
            self.document["matrix_id"],
            "gis-ai-go:qual-206-local-protocol-evidence-matrix:sha256:"
            f"{identity(core)}",
        )

    def test_official_client_and_lock_are_exactly_pinned(self) -> None:
        official = self.document["official_client"]
        self.assertEqual(official["package"], "@modelcontextprotocol/client")
        self.assertEqual(official["version"], "2.0.0")
        self.assertEqual(official["manifest"]["path"], "apps/mcp-gateway/package.json")
        self.assertEqual(official["lockfile"]["path"], "pnpm-lock.yaml")

        manifest = load_json(GATEWAY_MANIFEST_PATH)
        self.assertEqual(
            manifest["devDependencies"]["@modelcontextprotocol/client"],
            "2.0.0",
        )
        lockfile = LOCKFILE_PATH.read_text(encoding="utf-8")
        importer = re.search(
            r"^  apps/mcp-gateway:\n(?P<body>.*?)(?=^  [^ ].*:\n|\Z)",
            lockfile,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(importer)
        importer_body = importer.group("body") if importer is not None else ""
        self.assertRegex(
            importer_body,
            (
                r"'@modelcontextprotocol/client':\n"
                r"\s+specifier: 2\.0\.0\n"
                r"\s+version: 2\.0\.0"
            ),
        )

    def test_matrix_distinguishes_driver_transport_and_coverage(self) -> None:
        actual = [
            (
                row["id"],
                row["driver"],
                row["transport"],
                row["wiring"],
                row["covers"],
            )
            for row in self.document["coverage"]
        ]
        self.assertEqual(actual, EXPECTED_COVERAGE)
        self.assertEqual(
            {
                (row["driver"], row["transport"])
                for row in self.document["coverage"]
            },
            {
                ("official-client", "http"),
                ("official-client", "stdio"),
                ("raw-transcript", "http"),
                ("raw-transcript", "stdio"),
            },
        )

        for transport in ("http", "stdio"):
            raw = next(
                row
                for row in self.document["coverage"]
                if row["driver"] == "raw-transcript"
                and row["transport"] == transport
            )
            self.assertEqual(set(raw["covers"].values()), {True})

    def test_suspension_evidence_is_in_process_and_not_host_acceptance(self) -> None:
        suspension = self.document["suspension_stdio"]
        self.assertEqual(suspension["wiring"], "in-process-stdio-server")
        self.assertEqual(suspension["scenario_count"], 7)
        self.assertEqual(suspension["resulting_suspension_count"], 9)
        self.assertFalse(suspension["production_registration"])
        self.assertEqual(suspension["provider_network_calls"], 0)
        self.assertFalse(suspension["operating_system_pipe_framing"])
        source = (ROOT / suspension["test_source"]["path"]).read_text(
            encoding="utf-8"
        )
        self.assertIn("startGovernedCandidateStdio", source)
        self.assertIn("InMemoryTransport.createLinkedPair", source)
        self.assertNotIn("spawn(", source)

        self.assertEqual(self.document["boundary"], BOUNDARY)
        self.assertEqual(set(self.document["claims"].values()), {False})
        serialised = json.dumps(self.document, ensure_ascii=False)
        for private_prefix in ("/Users/", "/private/", "file://"):
            self.assertNotIn(private_prefix, serialised)

    def test_schema_rejects_claim_and_provenance_inflation(self) -> None:
        unknown = copy.deepcopy(self.document)
        unknown["unexpected"] = True
        self.assert_invalid(unknown)

        live = copy.deepcopy(self.document)
        live["claims"]["live_host_session"] = True
        self.assert_invalid(live)

        activated = copy.deepcopy(self.document)
        activated["suspension_stdio"]["production_registration"] = True
        self.assert_invalid(activated)

        pipe_framing = copy.deepcopy(self.document)
        pipe_framing["suspension_stdio"]["operating_system_pipe_framing"] = True
        self.assert_invalid(pipe_framing)

        unpinned = copy.deepcopy(self.document)
        unpinned["official_client"]["version"] = "2.0.1"
        self.assert_invalid(unpinned)

        rebased = copy.deepcopy(self.document)
        rebased["repository_binding"]["runtime_base_commit"] = "a" * 40
        self.assert_invalid(rebased)

        executed = copy.deepcopy(self.document)
        executed["claims"]["test_execution_recorded"] = True
        self.assert_invalid(executed)

        duplicate = copy.deepcopy(self.document)
        duplicate["coverage"][1] = copy.deepcopy(duplicate["coverage"][0])
        self.assert_invalid(duplicate)

        contradictory = copy.deepcopy(self.document)
        contradictory["coverage"][0]["driver"] = "raw-transcript"
        contradictory["coverage"][0]["transport"] = "stdio"
        contradictory["coverage"][0]["wiring"] = "real-process-stdio"
        self.assert_invalid(contradictory)

        inflated = copy.deepcopy(self.document)
        inflated["coverage"][0]["covers"]["cancellation"] = True
        self.assert_invalid(inflated)


if __name__ == "__main__":
    unittest.main()
