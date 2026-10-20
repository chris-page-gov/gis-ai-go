"""Synthetic assurance for the isolated GML profiling candidate."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.okf_plus import gml_profile as g

HEAD = ('<os:FeatureCollection xmlns:os="urn:synthetic:os" '
        'xmlns:gml="http://www.opengis.net/gml/3.2" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xsi:schemaLocation="urn:synthetic:os https://example.invalid/os-v1.xsd">')
TAIL = "</os:FeatureCollection>"


class GmlProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "selected.gml"

    def tearDown(self):
        self.temp.cleanup()

    def run_xml(self, text, **kwargs):
        self.source.write_text(text)
        return g.profile(self.source, **kwargs)

    def row(self, snapshot, suffix):
        return next(row for row in snapshot["elements"] if row["xpath"].endswith(suffix))

    def test_complete_traversal_qnames_order_nil_empty_absence_and_privacy(self):
        xml = HEAD + """
<os:feature gml:id="PRIVATE-IDENTIFIER"><os:a>PRIVATE-VALUE</os:a><os:a/>
<os:b xsi:nil="true"/><os:link xlink:href="#PRIVATE-LINK"/></os:feature>
<os:feature><os:b> </os:b><os:a xsi:nil="false">0</os:a></os:feature>
<os:feature><os:a xsi:nil="1"/></os:feature>""" + TAIL
        snapshot = self.run_xml(xml)
        encoded = g.canonical(snapshot)
        for forbidden in (b"PRIVATE-IDENTIFIER", b"PRIVATE-VALUE", b"PRIVATE-LINK"):
            self.assertNotIn(forbidden, encoded)
        self.assertEqual(snapshot["inputSha256"], hashlib.sha256(xml.encode()).hexdigest())
        self.assertEqual(snapshot["counts"]["elements"], 11)
        a = self.row(snapshot, "/Q{urn:synthetic:os}a")
        b = self.row(snapshot, "/Q{urn:synthetic:os}b")
        self.assertEqual(a["occurrences"], 4)
        self.assertEqual(a["absentParentInstances"], 0)
        self.assertEqual(b["absentParentInstances"], 1)
        self.assertEqual(b["nilStates"], {"true": 1, "not-declared": 1})
        self.assertEqual(b["contentStates"], {"empty": 1, "whitespace-only": 1})
        parent = self.row(snapshot, "/Q{urn:synthetic:os}feature")
        self.assertEqual(parent["childCardinality"]["Q{urn:synthetic:os}a"], {"2": 1, "1": 2, "0": 0})
        patterns = [snapshot["structuralPatterns"][key] for key in parent["patterns"]]
        orders = [[token["element"] for token in p["contentOrder"] if "element" in token] for p in patterns]
        self.assertIn(["Q{urn:synthetic:os}a", "Q{urn:synthetic:os}a",
                       "Q{urn:synthetic:os}b", "Q{urn:synthetic:os}link"], orders)
        self.assertIn(["Q{urn:synthetic:os}b", "Q{urn:synthetic:os}a"], orders)
        reference = next(a for a in snapshot["attributes"] if "xlink}href" in a["xpath"])
        self.assertEqual(reference["referenceKinds"], {"fragment": 1})

    def test_namespace_urls_with_slashes_geometry_and_schema_locations_are_inert(self):
        xml = HEAD + '<gml:Point srsName="urn:ogc:def:crs:EPSG::27700" srsDimension="2">' \
              '<gml:pos>12345.67 76543.21</gml:pos></gml:Point>' + TAIL
        with patch("socket.socket", side_effect=AssertionError("Network forbidden")):
            snapshot = self.run_xml(xml)
        point = self.row(snapshot, "}Point")
        self.assertEqual(point["parentInstances"], 1)
        self.assertNotIn(b"12345.67", g.canonical(snapshot))
        srs = next(a for a in snapshot["attributes"] if a["xpath"].endswith("@Q{}srsName"))
        self.assertEqual(srs["semanticValues"], {"urn:ogc:def:crs:EPSG::27700": 1})
        self.assertEqual(snapshot["rootSchemaLocations"][0]["tokens"],
                         ["urn:synthetic:os", "https://example.invalid/os-v1.xsd"])
        self.assertIs(snapshot["rootSchemaLocations"][0]["retrieved"], False)

    def test_legacy_osgb_bng_is_preserved_without_general_scheme_admission(self):
        snapshot = self.run_xml('<a srsName="osgb:BNG"/>')
        self.assertEqual(snapshot["attributes"][0]["semanticValues"], {"osgb:BNG": 1})
        self.assertNotIn("EPSG", g.canonical(snapshot).decode())
        with self.assertRaisesRegex(g.Rejected, "scheme"):
            self.run_xml('<a srsName="osgb:UNREVIEWED"/>')
        with self.assertRaisesRegex(g.Rejected, "scheme"):
            g.inert_reference("osgb:BNG")

    def test_dtd_entity_external_entity_and_parameter_entity_rejected(self):
        inputs = [
            '<!DOCTYPE a><a/>',
            '<!DOCTYPE a [<!ENTITY x "secret">]><a>&x;</a>',
            '<!DOCTYPE a SYSTEM "file:///etc/passwd"><a/>',
            '<!DOCTYPE a [<!ENTITY % x SYSTEM "https://example.invalid/x">%x;]><a/>'
        ]
        for xml in inputs:
            with self.subTest(xml=xml), self.assertRaisesRegex(g.Rejected, "DTD"):
                self.run_xml(xml)
            self.assertEqual(self.source.read_text(), xml)

    def test_builtin_entities_unicode_and_chunked_text_are_redacted(self):
        snapshot = self.run_xml("<a><b>" + ("é&amp;&lt;" * 20000) + "</b></a>")
        b = self.row(snapshot, "/Q{}b")
        self.assertEqual(b["contentStates"], {"text-redacted": 1})
        pattern = snapshot["structuralPatterns"][next(iter(b["patterns"]))]
        self.assertEqual(pattern["contentOrder"], [{"text": True}])
        self.assertNotIn("é", g.canonical(snapshot).decode())

    def test_malformed_xml_and_complete_tail_are_required(self):
        for xml in ("<a><b/></broken>", "<a><b/>", "<a/>trailing", ""):
            with self.subTest(xml=xml), self.assertRaises(g.Rejected):
                self.run_xml(xml)

    def test_byte_depth_element_attribute_path_pattern_and_order_bounds(self):
        cases = [
            ("<a/>", g.Limits(max_bytes=2), "byte"),
            ("<a><b/></a>", g.Limits(max_depth=1), "Depth"),
            ("<a><b/></a>", g.Limits(max_elements=1), "Element"),
            ('<a a="1" b="2"/>', g.Limits(max_attributes=1), "Attribute"),
            ("<a><b/></a>", g.Limits(max_paths=1), "XPath"),
            ("<a><b/></a>", g.Limits(max_patterns=1), "pattern"),
            ("<a><b/><b/></a>", g.Limits(max_sequence_items=1), "sequence"),
            ("<a><b/></a>", g.Limits(max_structure_bytes=1), "metadata byte")
        ]
        for xml, limits, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(g.Rejected, message):
                self.run_xml(xml, limits=limits)

    def test_wall_limit_and_metadata_cardinality_limit(self):
        self.source.write_text("<a/>")
        with patch("scripts.okf_plus.gml_profile.time.monotonic", side_effect=[0, 2]):
            with self.assertRaisesRegex(g.Rejected, "Wall"):
                g.profile(self.source, limits=g.Limits(max_wall_seconds=1))
        with self.assertRaisesRegex(g.Rejected, "cardinality"):
            self.run_xml('<a><b srsName="urn:x:1"/><b srsName="urn:x:2"/></a>',
                         limits=g.Limits(max_metadata_values=1))

    def test_secret_or_unsafe_schema_reference_rejected_without_echo(self):
        for url in ("https://example.invalid/a?key=PRIVATE-SECRET",
                    "file:///etc/passwd", "../private.xsd"):
            xml = '<a xmlns:xsi="' + g.XSI + '" xsi:noNamespaceSchemaLocation="' + url + '"/>'
            with self.assertRaises(g.Rejected) as error:
                self.run_xml(xml)
            self.assertNotIn("PRIVATE-SECRET", str(error.exception))

    def test_symlink_input_and_output_refused_and_existing_output_preserved(self):
        self.source.write_text("<a/>")
        alias = self.root / "alias.gml"
        alias.symlink_to(self.source)
        with self.assertRaisesRegex(g.Rejected, "Symbolic"):
            g.profile(alias)
        snapshot = g.profile(self.source)
        mappings = g.mapping_candidates([], snapshot, self.root)
        existing = self.root / "output"
        existing.mkdir()
        (existing / "user.txt").write_text("keep")
        with self.assertRaisesRegex(g.Rejected, "exists"):
            g.export_bundle(existing, snapshot, mappings)
        self.assertEqual((existing / "user.txt").read_text(), "keep")

    def test_unknown_and_evidence_bound_full_cou_modes(self):
        self.source.write_text("<a/>")
        self.assertEqual(g.profile(self.source)["deliveryMode"]["selected"], "unknown")
        with self.assertRaisesRegex(g.Rejected, "evidence"):
            g.profile(self.source, mode="FULL")
        evidence_file = self.root / "delivery.txt"
        evidence_file.write_text("Synthetic source says delivery FULL.\n")
        checked = g.checked_evidence({"file": "delivery.txt", "sha256": g.sha(evidence_file.read_bytes()),
                                      "lineStart": 1, "lineEnd": 1}, self.root)
        for mode in ("FULL", "COU"):
            result = g.profile(self.source, mode=mode, mode_evidence=checked)
            self.assertFalse(result["deliveryMode"]["couAppliedToBaseline"])
            self.assertFalse(result["deliveryMode"]["evidence"]["meaningIndependentlyValidated"])

    def test_mapping_requires_observed_path_version_and_checked_source_no_inferred_equivalence(self):
        snapshot = self.run_xml("<a><width/></a>")
        evidence_file = self.root / "mapping.txt"
        evidence_file.write_text("Synthetic v1 width becomes width_m in CSV; repetition is lost.\n")
        candidate = {"sourceXpath": "/Q{}a/Q{}width", "productVersion": "synthetic-v1",
                     "targetFormat": "CSV", "targetField": "width_m",
                     "conversionLosses": ["Repeated elements cannot be preserved in one scalar field."],
                     "evidence": {"file": "mapping.txt", "sha256": g.sha(evidence_file.read_bytes()),
                                  "lineStart": 1, "lineEnd": 1}}
        result = g.mapping_candidates([candidate], snapshot, self.root)
        self.assertEqual(result["candidates"][0]["equivalence"], "not-established")
        self.assertEqual(result["automaticallyInventedMappings"], 0)
        for mutation in ("hash", "xpath", "path", "lines"):
            bad = copy.deepcopy(candidate)
            if mutation == "hash":
                bad["evidence"]["sha256"] = "0" * 64
            elif mutation == "xpath":
                bad["sourceXpath"] = "/Q{}unseen"
            elif mutation == "path":
                bad["evidence"]["file"] = "../mapping.txt"
            else:
                bad["evidence"]["lineEnd"] = 3
            with self.subTest(mutation=mutation), self.assertRaises(g.Rejected):
                g.mapping_candidates([bad], snapshot, self.root)
        self.assertEqual(g.mapping_candidates([], snapshot, self.root)["candidates"], [])

    def test_bundle_all_files_bounded_exact_reconstruction_and_mutation_detection(self):
        xml = "<a>" + "".join(f'<f{i}><v/><v nil="false"/></f{i}>' for i in range(400)) + "</a>"
        snapshot = self.run_xml(xml)
        mappings = g.mapping_candidates([], snapshot, self.root)
        output = self.root / "bundle"
        result = g.export_bundle(output, snapshot, mappings)
        self.assertEqual(result["documents"]["profile"], json.loads(g.canonical(snapshot)))
        self.assertGreater(result["files"], 48)
        self.assertLessEqual(result["maxFileBytes"], 16384)
        self.assertEqual(self.source.read_text(), xml)
        victim = next(p for p in output.iterdir() if p.name != "root.json")
        victim.write_bytes(b"[" + victim.read_bytes()[1:])
        with self.assertRaisesRegex(g.Rejected, "checksum"):
            g.verify_bundle(output)

    def test_field_card_lookup_source_binding_and_lossless_oversized_row(self):
        xml = "<a>" + "".join(f'<b srsName="urn:synthetic:crs:{i:03d}"/>'
                              for i in range(200)) + "</a>"
        snapshot = self.run_xml(xml)
        # Make a legitimate semantic metadata row exceed one card's byte budget.
        attr = snapshot["attributes"][0]
        attr["semanticValues"] = {("urn:synthetic:" + str(i) + ":" + "x" * 100): 1 for i in range(200)}
        output = self.root / "cards"
        result = g.export_bundle(output, snapshot, g.mapping_candidates([], snapshot, self.root))
        index = result["documents"]["fieldCardIndex"]
        self.assertEqual(index["fieldCount"], len(snapshot["elements"]) + len(snapshot["attributes"]))
        found = next(row for row in index["fields"] if row["nativeXpath"] == attr["xpath"])
        card = json.loads((output / found["card"]["file"]).read_bytes())
        self.assertEqual(card["sourceSha256"], snapshot["inputSha256"])
        self.assertEqual(card["qname"], "Q{}srsName")
        self.assertIn("detailsReference", card)
        self.assertNotIn("details", card)
        self.assertLessEqual((output / found["card"]["file"]).stat().st_size, 16384)
        self.assertEqual(result["documents"]["profile"]["attributes"][0], attr)
        self.assertFalse(card["schemaValidated"])

    def test_self_consistent_card_hash_cannot_overstate_mode_version_or_claims(self):
        snapshot = self.run_xml("<a/>")
        snapshot["versionEvidence"] = {"status": "source-declared-candidate", "nativeProductVersion": "synthetic-v1"}
        mappings = g.mapping_candidates([], snapshot, self.root)
        original_canonical = g.canonical
        for key, value in (("deliveryModeEvidence", {"selected": "FULL"}),
                           ("versionEvidence", {"status": "schema-validated"}),
                           ("conversionSuccess", True), ("schemaValidated", True),
                           ("occurrences", 99)):
            def changed_canonical(item):
                if isinstance(item, dict) and item.get("@type") == "NativeGmlStructuralFieldCandidate":
                    item = {**item, key: value}
                return original_canonical(item)
            output = self.root / ("tampered-" + key)
            with self.subTest(key=key), patch.object(g, "canonical", side_effect=changed_canonical):
                with self.assertRaisesRegex(g.Rejected, "candidate claim"):
                    g.export_bundle(output, snapshot, mappings)
            self.assertFalse((output / "root.json").exists())

    def test_incomplete_bundle_and_unindexed_file_rejected(self):
        snapshot = self.run_xml("<a/>")
        mappings = g.mapping_candidates([], snapshot, self.root)
        incomplete = self.root / "incomplete"
        incomplete.mkdir()
        with self.assertRaises(FileNotFoundError):
            g.verify_bundle(incomplete)
        output = self.root / "bundle"
        g.export_bundle(output, snapshot, mappings)
        (output / "extra.json").write_text("{}")
        with self.assertRaisesRegex(g.Rejected, "Unindexed"):
            g.verify_bundle(output)

    def test_export_interruption_does_not_delete_source_or_mark_complete(self):
        snapshot = self.run_xml("<a/>")
        mappings = g.mapping_candidates([], snapshot, self.root)
        output = self.root / "interrupted"
        with patch("scripts.okf_plus.gml_profile.os.fsync", side_effect=OSError("synthetic interruption")):
            with self.assertRaises(OSError):
                g.export_bundle(output, snapshot, mappings)
        self.assertTrue(self.source.is_file())
        self.assertFalse((output / "root.json").exists())
        with self.assertRaisesRegex(g.Rejected, "exists"):
            g.export_bundle(output, snapshot, mappings)


    def test_failed_candidate_verification_never_publishes_completion_marker(self):
        snapshot = self.run_xml("<a/>")
        mappings = g.mapping_candidates([], snapshot, self.root)
        output = self.root / "failed-verification"
        with patch.object(g, "verify_bundle", side_effect=g.Rejected("synthetic failed verification")):
            with self.assertRaises(g.Rejected):
                g.export_bundle(output, snapshot, mappings)
        self.assertFalse((output / "root.json").exists())
        self.assertTrue((output / "candidate-root.json").exists())
        self.assertTrue(self.source.exists())


if __name__ == "__main__":
    unittest.main()
