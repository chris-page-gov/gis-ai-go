"""Closed synthetic contracts; no provider authority is granted."""
import copy
import gzip
import json
from pathlib import Path
import tempfile
import unittest
from jsonschema import Draft202012Validator
from scripts.okf_plus import gml_profile as g, gml_archive_profile as a

ROOT = Path(__file__).resolve().parents[2]

class GmlLocalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "okf-plus/schemas/gml-local-processing.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def test_actual_descriptor_and_completion_and_refused_authority_mutations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            raw = root / "sample.gz"
            raw.write_bytes(gzip.compress(b"<synthetic/>"))
            evidence = root / "selection.json"
            selected = {"id": "synthetic-input", "deliveryMode": "unknown"}
            evidence.write_bytes(g.canonical(selected))
            descriptor = {"schema": a.SCHEMA,
                          "payload": {"bytes": raw.stat().st_size, "sha256": g.sha(raw.read_bytes())},
                          "selection": selected,
                          "selectionEvidence": {"file": "selection.json", "sha256": g.sha(evidence.read_bytes()),
                                                "jsonPointer": ""}}
            path = root / "descriptor.json"
            path.write_bytes(g.canonical(descriptor))
            self.validator.validate(descriptor)
            a.process(path, raw, root / "work", root / "output")
            completion = json.loads((root / "output/complete.json").read_bytes())
            self.validator.validate(completion)
            for key in ("conversionSuccess", "rawPayloadDisposed", "schemaMappingComplete"):
                changed = copy.deepcopy(completion)
                changed[key] = True
                self.assertTrue(list(self.validator.iter_errors(changed)), key)
            bad = copy.deepcopy(descriptor)
            bad["providerAuthorised"] = True
            self.assertTrue(list(self.validator.iter_errors(bad)))

    def test_descriptor_rejects_missing_digest_boolean_size_and_unknown_fields(self):
        descriptor = {"payload": {"bytes": 1, "sha256": "a" * 64},
                      "selection": {"id": "synthetic", "deliveryMode": "unknown"},
                      "selectionEvidence": {"file": "source.json", "sha256": "b" * 64, "jsonPointer": ""}}
        for mutation in ("digest", "size", "unknown"):
            bad = copy.deepcopy(descriptor)
            if mutation == "digest": del bad["payload"]["sha256"]
            elif mutation == "size": bad["payload"]["bytes"] = True
            else: bad["selection"]["authority"] = "granted"
            self.assertTrue(list(self.validator.iter_errors(bad)), mutation)
