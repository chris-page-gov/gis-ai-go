from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_changelog_fragments import (
    collect_fragment_errors,
    fragment_errors,
    render_release_preview,
)


class ChangelogFragmentTests(unittest.TestCase):
    def test_allows_a_release_tree_with_no_pending_fragments(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            directory = root / "changelog.d"
            directory.mkdir()
            (directory / "README.md").write_text("Instructions\n", encoding="utf-8")

            self.assertEqual(collect_fragment_errors(root), [])

    def test_rejects_headings_multiple_bullets_and_unsupported_categories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            directory = root / "changelog.d"
            directory.mkdir()
            (directory / "README.md").write_text("Instructions\n", encoding="utf-8")
            bad = directory / "QUAL-206.docs.md"
            bad.write_text("# Changed\n\n- First.\n- Second.\n", encoding="utf-8")

            errors = fragment_errors(bad)
            self.assertIn("filename must end in a supported change category", errors)
            self.assertIn("fragment must not contain a heading", errors)
            self.assertIn(
                "fragment must contain exactly one top-level Markdown bullet",
                errors,
            )

    def test_rejects_unindented_continuations_and_missing_final_lf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "DEPLOY-207.changed.md"
            path.write_text("- First line.\nContinuation.", encoding="utf-8")
            errors = fragment_errors(path)
            self.assertIn("fragment must end with exactly one LF", errors)
            self.assertIn("continuation lines must be indented by two spaces", errors)

    def test_rejects_multiple_terminal_lfs_multiple_paragraphs_and_long_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            multiple_lfs = root / "MULTIPLE.fixed.md"
            multiple_lfs.write_text("- First paragraph.\n\n", encoding="utf-8")
            self.assertIn(
                "fragment must end with exactly one LF",
                fragment_errors(multiple_lfs),
            )
            self.assertIn(
                "fragment must contain exactly one paragraph",
                fragment_errors(multiple_lfs),
            )

            multiple_paragraphs = root / "PARAGRAPHS.changed.md"
            multiple_paragraphs.write_text(
                "- First paragraph.\n\n  Second paragraph.\n",
                encoding="utf-8",
            )
            self.assertIn(
                "fragment must contain exactly one paragraph",
                fragment_errors(multiple_paragraphs),
            )

            too_long = root / "LONG.added.md"
            too_long.write_text(f"- {'x' * 1022}\n", encoding="utf-8")
            self.assertIn("fragment exceeds 1024 bytes", fragment_errors(too_long))

    def test_renders_a_deterministic_non_release_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            directory = root / "changelog.d"
            directory.mkdir()
            (directory / "README.md").write_text("Instructions\n", encoding="utf-8")
            (directory / "B.fixed.md").write_text("- Fix B.\n", encoding="utf-8")
            (directory / "A.added.md").write_text(
                "- Add A with a wrapped\n  continuation.\n",
                encoding="utf-8",
            )

            self.assertEqual(collect_fragment_errors(root), [])
            preview = render_release_preview(root, "0.2.0")
            self.assertIn("# GIS AI GO v0.2.0 release preview", preview)
            self.assertIn("This is preparation, not release", preview)
            self.assertLess(preview.index("## Added"), preview.index("## Fixed"))
            self.assertNotIn("2026-", preview)


if __name__ == "__main__":
    unittest.main()
