from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]


def load_script() -> ModuleType:
    path = ROOT / "scripts/check_release_reproducibility.py"
    specification = importlib.util.spec_from_file_location(
        "check_release_reproducibility", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load release reproducibility checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


CHECK = load_script()


class ReleaseReproducibilityContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_outputs(self, root: Path, suffix: bytes = b"") -> None:
        root.mkdir()
        values = {
            "artifact.tar": b"canonical tar bytes" + suffix,
            "artifact.tar.sha256": b"0" * 64 + b"  artifact.tar\n" + suffix,
            "archive-receipt.json": b'{"schema":"fixture"}\n' + suffix,
        }
        for name, value in values.items():
            (root / name).write_bytes(value)

    def test_cleanup_allowlist_is_exact_and_preserves_unrelated_files(self) -> None:
        self.assertEqual(
            tuple(path.as_posix() for path in CHECK.GENERATED_ROOTS),
            (
                "apps/public-explorer/dist",
                "apps/public-explorer/public/catalogue",
                "artifacts/okf",
            ),
        )
        protected = self.root / "docs" / "owner-note.txt"
        protected.parent.mkdir()
        protected.write_text("retain\n", encoding="utf-8")

        removed = CHECK.clean_generated_roots(self.root, "a" * 40, "0.1.0")

        self.assertEqual(removed, [])
        self.assertEqual(protected.read_text(encoding="utf-8"), "retain\n")
        with self.assertRaisesRegex(ValueError, "not allowlisted"):
            CHECK.resolve_cleanup_target(self.root, "docs")
        with self.assertRaisesRegex(ValueError, "not allowlisted"):
            CHECK.resolve_cleanup_target(self.root, "../outside")

    def test_cleanup_rejects_an_unmarked_allowlisted_directory(self) -> None:
        generated = self.root / "artifacts" / "okf"
        generated.mkdir(parents=True)
        owner_file = generated / "owner-note.txt"
        owner_file.write_text("retain\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "generated marker is missing or invalid"):
            CHECK.clean_generated_roots(self.root, "a" * 40, "0.1.0")

        self.assertEqual(owner_file.read_text(encoding="utf-8"), "retain\n")

    def test_compares_exactly_the_three_canonical_release_files(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        self._write_outputs(first)
        self._write_outputs(second)

        digests = CHECK.compare_release_outputs(first, second)

        self.assertEqual(tuple(digests), CHECK.RELEASE_OUTPUTS)
        (second / "unexpected.txt").write_text("not a release output\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exactly the three canonical files"):
            CHECK.compare_release_outputs(first, second)

    def test_rejects_a_byte_difference_in_each_release_output(self) -> None:
        first = self.root / "first"
        self._write_outputs(first)
        for index, name in enumerate(CHECK.RELEASE_OUTPUTS):
            with self.subTest(name=name):
                second = self.root / f"second-{index}"
                self._write_outputs(second)
                (second / name).write_bytes((second / name).read_bytes() + b"changed")
                with self.assertRaisesRegex(
                    ValueError,
                    rf"not byte-identical: {name.replace('.', r'\.')}",
                ):
                    CHECK.compare_release_outputs(first, second)

    def test_build_command_cannot_reinvoke_the_complete_check(self) -> None:
        self.assertEqual(CHECK.BUILD_COMMAND, ("pnpm", "run", "build:explorer"))
        self.assertNotIn("check", CHECK.BUILD_COMMAND)


if __name__ == "__main__":
    unittest.main()
