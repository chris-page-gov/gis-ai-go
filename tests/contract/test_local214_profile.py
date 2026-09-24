"""Local prerelease policy cannot silently promote pending or duplicate gates."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import ValidationError
from scripts.check_local214_profile import PROFILE, validate_profile, validate_record


class Local214ProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(PROFILE.read_text())
        self.record = {
            "schema": "gis-ai-go.local-edition-acceptance.v1",
            "edition": "0.2.0-local.1", "source_commit": "a" * 40,
            "source_tree": "b" * 40,
            "artefacts": {name: "c" * 64 for name in (
                "gis-ai-go-v0.2.0-local.1-source.tar.gz", "local214-package-manifest.json",
                "SHA256SUMS", "gis-ai-go-local214-walkthrough.pdf", "guide-manifest.json")},
            "checks": [{"id": gate, "status": "pending", "evidence": [], "scope": "Synthetic test only"}
                       for gate in self.profile["required_gates"]]
        }

    def test_current_profile_preserves_runtime_and_version_boundaries(self):
        validate_profile(self.profile)

    def test_pending_record_is_valid_but_not_a_pass(self):
        validate_record(self.record, self.profile)
        with self.assertRaises(ValueError):
            validate_record(self.record, self.profile, require_pass=True)

    def test_all_gates_need_evidence_and_unique_identity(self):
        for check in self.record["checks"]:
            check.update(status="passed", evidence=["Synthetic fixture, not acceptance evidence"])
        validate_record(self.record, self.profile, require_pass=True)
        duplicate = copy.deepcopy(self.record)
        duplicate["checks"][-1] = duplicate["checks"][0]
        with self.assertRaises(ValueError):
            validate_record(duplicate, self.profile, require_pass=True)
        self.record["checks"][0]["evidence"] = []
        with self.assertRaises(ValidationError):
            validate_record(self.record, self.profile, require_pass=True)

    def test_human_gate_cannot_be_omitted_or_marked_unavailable_as_pass(self):
        for check in self.record["checks"]:
            check.update(status="passed", evidence=["Synthetic fixture"])
        human = next(c for c in self.record["checks"] if c["id"] == "unaided-colleague-walkthrough")
        human["status"] = "unavailable"
        with self.assertRaises(ValueError):
            validate_record(self.record, self.profile, require_pass=True)

    def test_no_stable_release_or_expiry_extension(self):
        for field, value in [("edition", "0.2.0"), ("latest_supported_release", "0.2.0"),
                             ("provider_egress", 0),
                             ("approved_cache_expires_at", "2099-01-01T00:00:00Z"),
                             ("publication", {"prerelease": False, "make_latest": True, "requires_all_gates": True})]:
            changed = copy.deepcopy(self.profile)
            changed[field] = value
            with self.assertRaises(ValueError):
                validate_profile(changed)

    def test_required_distribution_artefacts_cannot_be_replaced_by_unrelated_hash(self):
        self.record["artefacts"] = {"unrelated.txt": "c" * 64}
        with self.assertRaises(ValidationError):
            validate_record(self.record, self.profile)

    def test_canonical_ci_includes_archive_and_independent_client_lanes(self):
        root = Path(__file__).resolve().parents[2]
        workflow = (root / ".github/workflows/ci.yml").read_text()
        for command in ("scripts.local214_package package", "sha256sum -c SHA256SUMS",
                        "scripts.local214_package verify", "GIS_AI_GO_LOCAL214_ARCHIVE_TEST_ROOT",
                        "local-candidate-launcher.acceptance.js"):
            self.assertIn(command, workflow)
        package = json.loads((root / "package.json").read_text())
        self.assertIn("test:local-edition-client", package["scripts"]["test"])
        self.assertEqual(package["scripts"]["test:local-edition-client"], "node --test tests/test_local214_demo.mjs")
