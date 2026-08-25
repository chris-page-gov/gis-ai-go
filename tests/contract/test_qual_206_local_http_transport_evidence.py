from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-local-http-transport-preflight.schema.json"
)
EVIDENCE_PATH = (
    ROOT
    / "tests"
    / "interoperability"
    / "evidence"
    / "local-http-transport-preflight-2026-08-25.json"
)
SOURCE_COMMIT = "066a9cb22f719d22e29c95cd99857ddf694c878e"
SOURCE_TREE = "43116491557d53c4c0ad2d3a6768761ccf873df4"
SCHEMA_SHA256 = "f5c0ea1778101db8fd9a301dea163c5ad05d2c1a56ab944addd955738e2b9a22"
EVIDENCE_SHA256 = "c227791068c662c64e14fa9ec354d8d8030e5cc2e3d64b0d8ff93101e1b67274"
OBSERVATION_DOMAIN_PREFIX = (
    b"GIS-AI-GO\0"
    b"gis-ai-go.qual-206-local-http-transport-preflight.observation.v1\0"
    b"v1\0"
)
TRACKED_SOURCE_MATERIALS = {
    "scripts/qual_206_local_http_preflight.mjs": (
        "431cdcd920204739f87dc0be3dd072d78022f541a290db6ca86d8b259056a952"
    ),
    "scripts/qual_206_verify_local_http_preflight.py": (
        "c9ed65df029697690997f4a2c88c59ea43b96ec35e3571eba21adf3b9983728c"
    ),
    "schemas/qual-206-exact-five-tool-schema-digests.v1.json": (
        "f7ac2b507108f01bbb21af6daca31e84da66cc285ccb10e0d329b8e919a79963"
    ),
    "schemas/qual-206-local-http-transport-preflight.schema.json": (
        "f5c0ea1778101db8fd9a301dea163c5ad05d2c1a56ab944addd955738e2b9a22"
    ),
    "schemas/qual-206-local-http-private-capture-v1.schema.json": (
        "047812056e2083e018ee3c880c7e6654a994b41be35df6b42cd1f1be5d8bcfb5"
    ),
    "scripts/qual_206_exact_five_event_collector.mjs": (
        "be45d157c3daed81267e03be34b02eeb8fb006d8889f436ee531e315fba6bdc0"
    ),
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs": (
        "f34757b6c7c555adb37a2d5fffbb164a264a689fe603e12f25703fea8d46eafe"
    ),
    "apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs": (
        "8c901f7e40d40079ac103f065fb907bc55b1ddc7817328517b83c98ace069c1c"
    ),
}
DERIVED_SOURCE_MATERIALS = {
    "artifacts/okf/manifest.json": (
        "f7aa8d35b994f7c1a095fdaf2d9ab82791147ea7baf5e209fe7153e72ca4b2b1"
    ),
    "artifacts/okf/okf-bundle.json": (
        "e9d753c4d44b4566a37c495b3ac092c3767a900d71b245a307967e6cd9457c4b"
    ),
    "apps/mcp-gateway/dist/src/mcp-http.js": (
        "6f58d8950da56d3def292d451e797af60add404c291c45503ba9e04a354bbf01"
    ),
    "apps/mcp-gateway/dist/src/mcp-server.js": (
        "71fdde3b45363d366b62e7c4219c2cc77efbfbfe9d9e5d110f656e76ee9d2ab1"
    ),
}
EXPECTED_MATERIAL_ORDER = [
    "scripts/qual_206_local_http_preflight.mjs",
    "scripts/qual_206_verify_local_http_preflight.py",
    "schemas/qual-206-exact-five-tool-schema-digests.v1.json",
    "schemas/qual-206-local-http-transport-preflight.schema.json",
    "schemas/qual-206-local-http-private-capture-v1.schema.json",
    "artifacts/okf/manifest.json",
    "artifacts/okf/okf-bundle.json",
    "scripts/qual_206_exact_five_event_collector.mjs",
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
    "apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs",
    "apps/mcp-gateway/dist/src/mcp-http.js",
    "apps/mcp-gateway/dist/src/mcp-server.js",
]
PUBLIC_EVIDENCE_FORBIDDEN = re.compile(
    r"(?:"
    r"/Users/|/home/|/Volumes/|/private/tmp/|/var/folders/|file://|"
    r"[A-Za-z]:\\\\Users\\\\|127\.0\.0\.1|\blocalhost\b|"
    r"\bsk-[A-Za-z0-9_-]{8,}|\bgh[opusr]_[A-Za-z0-9]{8,}|"
    r"\bxox[baprs]-[A-Za-z0-9-]{8,}|\bAKIA[0-9A-Z]{16}|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"OPENAI_API_KEY|CODEX_API_KEY|ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN|"
    r"CLAUDE_CODE_OAUTH_TOKEN|"
    r"https?://(?:chatgpt\.com/c/|claude\.ai/chat/)|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}\b"
    r")",
    re.IGNORECASE,
)
FORBIDDEN_FIELD_NAMES = {
    "arguments",
    "command",
    "credentials",
    "endpoint",
    "environment",
    "headers",
    "host",
    "hostname",
    "idempotency_key",
    "log_path",
    "personal_data",
    "port",
    "prompt",
    "raw_command",
    "raw_content",
    "raw_request",
    "raw_response",
    "raw_result",
    "request_json",
    "response_json",
    "session_id",
    "structured_content",
    "tool_arguments",
    "url",
}


def reject_non_standard_number(value: str) -> None:
    raise ValueError(f"Non-standard JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_non_standard_number,
    )
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain one JSON object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_output(*arguments: str, check: bool = True) -> bytes:
    result = subprocess.run(
        ["/usr/bin/git", "--no-replace-objects", *arguments],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(f"git {' '.join(arguments)} failed: {message}")
    return result.stdout


def git_blob(commit: str, path: str) -> bytes:
    return git_output("show", f"{commit}:{path}")


def canonical_json(value: Any) -> str:
    if value is None or isinstance(value, (bool, str)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if not value.is_integer():
            raise ValueError("Canonical projection numbers must be finite integers")
        return str(int(value))
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(member) for member in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_json(key)}:{canonical_json(value[key])}"
            for key in sorted(value)
        ) + "}"
    raise TypeError(f"Unsupported canonical value: {type(value)!r}")


def nested_field_names(node: object) -> set[str]:
    names: set[str] = set()
    if isinstance(node, dict):
        names.update(node)
        for value in node.values():
            names.update(nested_field_names(value))
    elif isinstance(node, list):
        for value in node:
            names.update(nested_field_names(value))
    return names


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


class Qual206LocalHttpTransportPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.document = load_json(EVIDENCE_PATH)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def assert_invalid(self, value: object) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_closed_schema_accepts_exact_canonical_projection(self) -> None:
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
        self.assertEqual(EVIDENCE_PATH.read_bytes(), expected_bytes)
        self.assertEqual(sha256_bytes(SCHEMA_PATH.read_bytes()), SCHEMA_SHA256)
        self.assertEqual(sha256_bytes(EVIDENCE_PATH.read_bytes()), EVIDENCE_SHA256)
        self.assertEqual(
            self.document["schema_contract"],
            {
                "path": "schemas/qual-206-local-http-transport-preflight.schema.json",
                "sha256": SCHEMA_SHA256,
            },
        )

    def test_projection_binds_exact_protected_main_source_and_materials(self) -> None:
        source = self.document["source"]
        self.assertEqual(source["commit"], SOURCE_COMMIT)
        self.assertEqual(source["tree"], SOURCE_TREE)
        self.assertTrue(source["working_tree_clean"])
        self.assertFalse(source["complete_runtime_source_binding"])
        self.assertEqual(
            git_output("rev-parse", f"{SOURCE_COMMIT}^{{tree}}").decode().strip(),
            SOURCE_TREE,
        )
        self.assertEqual(
            git_output("merge-base", "--is-ancestor", SOURCE_COMMIT, "HEAD"),
            b"",
        )

        materials = self.document["verification"]["source_materials"]
        self.assertEqual([item["path"] for item in materials], EXPECTED_MATERIAL_ORDER)
        recorded = {item["path"]: item["sha256"] for item in materials}
        self.assertEqual(
            recorded,
            {**TRACKED_SOURCE_MATERIALS, **DERIVED_SOURCE_MATERIALS},
        )
        for path, expected_digest in TRACKED_SOURCE_MATERIALS.items():
            with self.subTest(path=path):
                self.assertEqual(
                    sha256_bytes(git_blob(SOURCE_COMMIT, path)),
                    expected_digest,
                )
        for path in DERIVED_SOURCE_MATERIALS:
            with self.subTest(path=path):
                result = subprocess.run(
                    [
                        "/usr/bin/git",
                        "--no-replace-objects",
                        "cat-file",
                        "-e",
                        f"{SOURCE_COMMIT}:{path}",
                    ],
                    cwd=ROOT,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.assertNotEqual(result.returncode, 0)

    def test_observation_identity_recomputes_independently(self) -> None:
        verification = self.document["verification"]
        normalised = {
            **self.document,
            "verification": {**verification, "observation_sha256": None},
        }
        expected = sha256_bytes(
            OBSERVATION_DOMAIN_PREFIX + canonical_json(normalised).encode()
        )
        self.assertEqual(verification["observation_sha256"], expected)

    def test_public_projection_is_path_free_minimised_and_withholds_capture(self) -> None:
        rendered = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIsNone(PUBLIC_EVIDENCE_FORBIDDEN.search(rendered))
        self.assertFalse(nested_field_names(self.document) & FORBIDDEN_FIELD_NAMES)
        verification = self.document["verification"]
        self.assertTrue(verification["private_capture_replayed"])
        self.assertFalse(verification["private_capture_published"])
        self.assertTrue(verification["public_projection_path_free"])
        self.assertNotIn('"request_content"', rendered)
        self.assertNotIn('"response_content"', rendered)
        self.assertNotIn('"licensed_payload"', rendered)

    def test_claims_remain_local_unregistered_and_unscored(self) -> None:
        self.assertEqual(
            self.document["status"],
            "loopback-http-transport-pass-capability-unscored",
        )
        self.assertFalse(self.document["transport"]["remote_host_acceptance"])
        self.assertFalse(self.document["transport"]["endpoint_published"])
        claims = self.document["claims"]
        self.assertEqual(claims["claude_code_capability"], "unscored")
        self.assertEqual(claims["model_capability"], "unscored")
        self.assertEqual(claims["live_provider_readiness"], "not-exercised")
        for name in (
            "remote_host_acceptance",
            "registration_performed",
            "activation_performed",
            "deployment_performed",
            "release_performed",
        ):
            self.assertFalse(claims[name])

        mutations: list[tuple[str, dict[str, Any]]] = []
        for name in (
            "remote_host_acceptance",
            "registration_performed",
            "activation_performed",
            "deployment_performed",
            "release_performed",
        ):
            mutated = copy.deepcopy(self.document)
            mutated["claims"][name] = True
            mutations.append((name, mutated))

        capability = copy.deepcopy(self.document)
        capability["claims"]["model_capability"] = "passed"
        mutations.append(("model capability", capability))

        published_capture = copy.deepcopy(self.document)
        published_capture["verification"]["private_capture_published"] = True
        mutations.append(("published private capture", published_capture))

        complete_binding = copy.deepcopy(self.document)
        complete_binding["source"]["complete_runtime_source_binding"] = True
        mutations.append(("complete runtime source binding", complete_binding))

        raw_request = copy.deepcopy(self.document)
        raw_request["journey"]["requests"][0]["raw_request"] = {"secret": True}
        mutations.append(("raw request", raw_request))

        for label, value in mutations:
            with self.subTest(label=label):
                self.assert_invalid(value)
