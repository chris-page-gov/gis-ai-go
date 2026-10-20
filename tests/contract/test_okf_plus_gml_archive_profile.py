"""Synthetic ZIP/gzip admission, processing and preservation tests."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
import warnings
import zipfile

from scripts.okf_plus import gml_archive_profile as a
from scripts.okf_plus import gml_profile as g

XML = (b'<os:FeatureCollection xmlns:os="http://www.ordnancesurvey.co.uk/xml/namespaces/osgb" '
       b'xmlns:gml="http://www.opengis.net/gml/3.2"><gml:featureMember>'
       b'<os:TopographicArea><os:value>PRIVATE-VALUE</os:value></os:TopographicArea>'
       b'</gml:featureMember><gml:featureMembers><os:TopographicLine/>'
       b'<os:TopographicPoint/></gml:featureMembers></os:FeatureCollection>')


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.raw = self.root / "payload.bin"
        self.receipt = self.root / "receipt.json"
        self.work = self.root / "work"
        self.output = self.root / "output"

    def tearDown(self):
        self.temp.cleanup()

    def zip(self, members):
        with zipfile.ZipFile(self.raw, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, raw in members:
                archive.writestr(name, raw)

    def descriptor(self, classifications=(), mode="COU_FEATURES"):
        selection = {"id": "synthetic-selection", "deliveryMode": mode}
        evidence = self.root / "selection.json"
        evidence.write_bytes(g.canonical(selection))
        self.receipt.write_bytes(g.canonical({
            "schema": a.SCHEMA,
            "payload": {"file": str(self.raw), "bytes": self.raw.stat().st_size,
                        "sha256": g.sha(self.raw.read_bytes()),
                        "md5": hashlib.md5(self.raw.read_bytes()).hexdigest()},
            "selection": selection,
            "selectionEvidence": {"file": str(evidence), "sha256": g.sha(evidence.read_bytes()),
                                  "jsonPointer": ""},
            "classifications": list(classifications)}))

    def process(self, **kwargs):
        return a.process(self.receipt, self.raw, self.work, self.output, **kwargs)

    def test_complete_zip_nested_gzip_profile_crc_and_independent_feature_count(self):
        self.zip([("directory/", b""), ("directory/one.gml", XML),
                  ("second.gml.gz", gzip.compress(XML))])
        self.descriptor()
        result = self.process()
        self.assertEqual(result["xmlProfiles"], 2)
        self.assertEqual(result["independentFeatureElements"], 6)
        self.assertFalse(result["conversionSuccess"])
        self.assertTrue(self.raw.exists())
        self.assertEqual(a.verify_archive(self.output, self.work, True), result)
        summary = g.verify_bundle(self.output / "summary")["documents"]["profile"]
        self.assertEqual(summary["selection"]["deliveryMode"], "COU_FEATURES")
        self.assertFalse(summary["schemaMappingComplete"])
        self.assertEqual(summary["selectionEvidence"]["labelNormalisedTo"], "COU")
        self.assertNotIn(b"PRIVATE-VALUE", g.canonical(summary))
        self.assertTrue(all(p.stat().st_size <= 16384 for p in self.output.rglob("*.json")))

    def test_completion_marker_cannot_claim_conversion_disposal_or_extra_authority(self):
        self.raw.write_bytes(gzip.compress(XML))
        self.descriptor()
        self.process()
        path = self.output / "complete.json"
        original = json.loads(path.read_bytes())
        for key in ("conversionSuccess", "rawPayloadDisposed", "schemaMappingComplete", "providerAuthorised"):
            path.write_bytes(g.canonical({**original, key: True}))
            with self.subTest(key=key), self.assertRaisesRegex(g.Rejected, "completion marker"):
                a.verify_archive(self.output, self.work, True)
        path.write_bytes(g.canonical(original))
        self.assertEqual(a.verify_archive(self.output, self.work, True)["status"], "verified")
        self.assertTrue(self.raw.exists())

    def test_gzip_magic_not_extension_and_trailer_verified(self):
        self.raw.write_bytes(gzip.compress(XML))
        self.descriptor(mode="Full")
        result = self.process()
        self.assertEqual(result["independentFeatureElements"], 3)
        summary = g.verify_bundle(self.output / "summary")["documents"]["profile"]
        self.assertTrue(summary["members"][0]["gzipTrailerVerified"])
        self.assertEqual(summary["selectionEvidence"]["labelNormalisedTo"], "FULL")

    def test_unsafe_zip_paths_types_unicode_case_and_implicit_directory_collisions(self):
        cases = [
            [("../a.gml", XML)], [("/a.gml", XML)], [("a\\b.gml", XML)],
            [("a.gml", XML), ("A.gml", XML)],
            [("é.gml", XML), ("e\u0301.gml", XML)],
            [("a", XML), ("a/b.gml", XML)],
            [("A/b.gml", XML), ("a/c.gml", XML)],
            [("a.gml", XML), ("a.gml", XML)],
        ]
        for members in cases:
            with self.subTest(members=[m[0] for m in members]), warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.zip(members)
                self.descriptor()
                with self.assertRaises(g.Rejected):
                    self.process()
                self.assertFalse(self.work.exists())
                self.assertTrue(self.raw.exists())
        symlink = zipfile.ZipInfo("link.gml")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.zip([(symlink, b"target")])
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "special"):
            self.process()

    def test_raw_hash_size_and_selection_evidence_must_match_before_extraction(self):
        self.raw.write_bytes(gzip.compress(XML))
        self.descriptor()
        for key in ("bytes", "sha256", "md5"):
            self.descriptor()
            value = json.loads(self.receipt.read_bytes())
            value["payload"][key] = 1 if key == "bytes" else "0" * (32 if key == "md5" else 64)
            self.receipt.write_bytes(g.canonical(value))
            with self.subTest(key=key), self.assertRaises(g.Rejected):
                self.process()
            self.assertFalse(self.work.exists())
        self.descriptor()
        (self.root / "selection.json").write_text("{}")
        with self.assertRaisesRegex(g.Rejected, "evidence checksum"):
            self.process()

    def test_declared_and_streamed_expansion_bounds_preserve_raw(self):
        self.zip([("one.gml", XML)])
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "ceiling"):
            self.process(limits=a.ArchiveLimits(max_member_bytes=5))
        self.assertFalse(self.work.exists())
        self.raw.write_bytes(gzip.compress(XML))
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "ceiling"):
            self.process(limits=a.ArchiveLimits(max_expanded_bytes=20))
        self.assertTrue(self.raw.exists())
        self.assertTrue((self.output / "failure.json").exists())
        self.assertFalse((self.output / "complete.json").exists())

    def test_non_xml_member_needs_explicit_hash_bound_retained_classification(self):
        doc = b"Bounded synthetic product documentation.\n"
        self.zip([("one.gml", XML), ("README.txt", doc)])
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "classification"):
            self.process()
        self.assertFalse((self.output / "complete.json").exists())
        self.assertTrue(self.raw.exists())

    def test_explicit_bounded_document_retention(self):
        doc = b"Bounded synthetic product documentation.\n"
        self.zip([("one.gml", XML), ("README.txt", doc)])
        self.descriptor([{"path": "README.txt", "kind": "documentation", "sha256": g.sha(doc)}])
        self.process()
        summary = g.verify_bundle(self.output / "summary")["documents"]["profile"]
        self.assertEqual(summary["members"][1]["processing"], "retained-bounded-documentation")
        self.assertEqual((self.work / summary["members"][1]["transientFile"]).read_bytes(), doc)

    def test_gzip_corrupt_trailer_fails_without_completion_and_retains_raw(self):
        raw = bytearray(gzip.compress(XML))
        raw[-8] ^= 1
        self.raw.write_bytes(raw)
        self.descriptor()
        with self.assertRaises((gzip.BadGzipFile, EOFError)):
            self.process()
        self.assertTrue(self.raw.exists())
        self.assertFalse((self.output / "complete.json").exists())

    def test_zip_crc_corruption_and_malformed_xml_failure(self):
        with zipfile.ZipFile(self.raw, "w", zipfile.ZIP_STORED) as archive:
            archive.writestr("a.gml", XML)
        raw = self.raw.read_bytes().replace(b"PRIVATE-VALUE", b"CHANGED-VALUE")
        self.raw.write_bytes(raw)
        self.descriptor()
        with self.assertRaises(zipfile.BadZipFile):
            self.process()
        self.assertFalse((self.output / "complete.json").exists())

    def test_dtd_inside_archive_fails_preserving_raw_and_finished_extractions(self):
        self.zip([("a.gml", b'<!DOCTYPE a [<!ENTITY x "no">]><a>&x;</a>')])
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "DTD"):
            self.process()
        self.assertTrue(self.raw.exists())
        self.assertTrue((self.work / "member-00000.bin").exists())
        self.assertFalse((self.output / "complete.json").exists())

    def test_existing_work_output_and_symlinks_refused(self):
        self.raw.write_bytes(gzip.compress(XML))
        self.descriptor()
        self.work.mkdir()
        sentinel = self.work / "user.txt"
        sentinel.write_text("keep")
        with self.assertRaisesRegex(g.Rejected, "Fresh"):
            self.process()
        self.assertEqual(sentinel.read_text(), "keep")

    def test_member_and_nested_expanded_count_ceiling(self):
        self.zip([("one.gml", XML), ("two.gml", XML)])
        self.descriptor()
        with self.assertRaisesRegex(g.Rejected, "member count"):
            self.process(limits=a.ArchiveLimits(max_members=1))
        self.assertFalse(self.work.exists())

    def test_explicit_sequence_cap_preserves_default_failure_and_records_reviewed_bound(self):
        # Whitespace and child elements both count as ordered items.
        xml = b"<root> " + b"<feature/> " * 10_000 + b"</root>"
        self.raw.write_bytes(gzip.compress(xml))
        self.descriptor()
        self.assertEqual(a.ArchiveLimits.max_sequence_items, 20_000)
        with self.assertRaisesRegex(g.Rejected, "order sequence"):
            self.process()
        self.assertFalse((self.output / "complete.json").exists())
        self.assertTrue(self.raw.exists())
        success = self.root / "reviewed-output"
        result = a.process(self.receipt, self.raw, self.root / "reviewed-work", success,
                           limits=a.ArchiveLimits(max_sequence_items=30_000))
        self.assertEqual(result["xmlProfiles"], 1)
        summary = g.verify_bundle(success / "summary")["documents"]["profile"]
        self.assertEqual(summary["limits"]["max_sequence_items"], 30_000)
        profile = g.verify_bundle(success / "profiles/member-00000")["documents"]["profile"]
        self.assertEqual(profile["limits"]["max_sequence_items"], 30_000)
        self.assertEqual(profile["counts"]["elements"], 10_001)
        for value in (0, -1, True, 1.5):
            with self.subTest(value=value), self.assertRaisesRegex(g.Rejected, "positive integers"):
                a.ArchiveLimits(max_sequence_items=value).validate()

    def test_product_transaction_actions_and_child_candidates_remain_separate(self):
        xml = (b'<os:Transaction xmlns:os="http://namespaces.os.uk/product/1.0" '
               b'xmlns:f="urn:synthetic:feature" xmlns:other="urn:synthetic:not-os">'
               b'<os:insert><f:Feature><os:delete><f:Nested/></os:delete></f:Feature></os:insert>'
               b'<os:replace><f:Feature/><f:Another/></os:replace>'
               b'<os:delete/><os:delete><f:Feature/></os:delete>'
               b'<other:insert><f:Excluded/></other:insert></os:Transaction>')
        self.raw.write_bytes(gzip.compress(xml))
        self.descriptor()
        result = self.process()
        self.assertEqual(result["independentFeatureElements"], 0)
        self.assertEqual(result["independentTransactionActionChildren"], 4)
        summary = g.verify_bundle(self.output / "summary")["documents"]["profile"]
        count = summary["profiles"][0]["independentFeatureCount"]
        prefix = "{" + a.OS_PRODUCT_NAMESPACE + "}"
        self.assertEqual(count["transactionActionCounts"], {
            prefix + "insert": 1, prefix + "replace": 1, prefix + "delete": 2})
        self.assertEqual(count["transactionActionChildQNames"][prefix + "replace"],
                         {"{urn:synthetic:feature}Feature": 1, "{urn:synthetic:feature}Another": 1})
        self.assertFalse(count["schemaValidated"])
        self.assertFalse(count["conversionSuccess"])
        self.assertIn("{urn:synthetic:not-os}insert", count["unclassifiedRootChildQNames"])
        wrong_root = self.root / "wrong-root.xml"
        wrong_root.write_bytes(xml.replace(b"os:Transaction", b"os:Other"))
        self.assertEqual(a.feature_count(wrong_root, lambda: None)["transactionActionCounts"], {})

    def test_os_member_and_direct_os_feature_counts_not_conversion(self):
        xml = (b'<os:FeatureCollection xmlns:os="http://www.ordnancesurvey.co.uk/xml/namespaces/osgb">'
               b'<os:topographicAreaMember><os:TopographicArea/></os:topographicAreaMember>'
               b'<os:TopographicLine/><os:Unknown/></os:FeatureCollection>')
        self.raw.write_bytes(gzip.compress(xml))
        self.descriptor()
        result = self.process()
        self.assertEqual(result["independentFeatureElements"], 2)
        summary = g.verify_bundle(self.output / "summary")["documents"]["profile"]
        self.assertTrue(summary["profiles"][0]["independentFeatureCount"]["unclassifiedRootChildQNames"])


if __name__ == "__main__":
    unittest.main()
