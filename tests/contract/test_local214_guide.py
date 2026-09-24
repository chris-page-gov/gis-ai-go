"""Focused scope, escaping and print-contract checks for the local learning guide."""
import json
import unittest

from scripts import build_local214_guide as guide


class Local214GuideTests(unittest.TestCase):
    def test_maintained_figure_bytes_and_markdown_agree(self):
        data = guide.snapshot(guide.ROOT)
        self.assertEqual(len(json.loads(data[guide.FIGURES])), 3)
        self.assertEqual(sum(kind == "figure" for kind, _ in guide.parse(data[guide.GUIDE].decode())), 3)

    def test_shared_parser_retains_page_boundary_and_command(self):
        self.assertEqual(list(guide.parse("<!-- page -->\n\n```bash\nnode scripts/local214_demo.mjs\n```")),
                         [("paragraph", "<!-- page -->"), ("code", "node scripts/local214_demo.mjs")])

    def test_inline_content_is_escaped(self):
        self.assertEqual(guide.inline("<script> `A&B`", "a" * 40),
                         '&lt;script&gt; <font face="Courier">A&amp;B</font>')

    def test_links_are_source_revision_bound(self):
        self.assertEqual(guide.link("../../VERSION", "a" * 40),
                         f"{guide.PUBLIC}/blob/{'a' * 40}/VERSION")

    def test_unsafe_and_outside_links_are_rejected(self):
        for target in ("javascript:alert(1)", "file:///private/path", "http://example.org/",
                       "../../../../outside.md", "//example.org/", "missing.md"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                guide.link(target, "a" * 40)

    def test_expiry_and_vintage_are_not_invented(self):
        text = (guide.ROOT / guide.GUIDE).read_text()
        cache = json.loads((guide.ROOT / "providers/ons/data-query-approved-cache.v1.json").read_bytes())
        self.assertIn(cache["freshness"]["stale_after"], text)
        self.assertIn(cache["observation"]["value"], text)
        self.assertIn("20 August 2026", text)
        self.assertIn("not a current statistic", text)

    def test_claims_keep_local_and_unperformed_acceptance_separate(self):
        text = (guide.ROOT / guide.GUIDE).read_text()
        for boundary in ("not a supported public MCP service", "not an unaided human",
                         "does not certify", "Receipts do not survive", "not screenshots"):
            self.assertIn(boundary, text)

    def test_no_wide_unbroken_commands(self):
        text = (guide.ROOT / guide.GUIDE).read_text()
        for kind, value in guide.parse(text):
            if kind == "code":
                self.assertTrue(all(len(line) <= 90 for line in value.splitlines()))

    def test_software_and_package_manager_match_maintained_source(self):
        text = (guide.ROOT / guide.GUIDE).read_text()
        package = json.loads((guide.ROOT / "package.json").read_text())
        self.assertIn(f"Software version: `{package['version']}`", text)
        self.assertIn("pnpm `" + package["packageManager"].split("@")[1] + "`", text)


if __name__ == "__main__":
    unittest.main()
