from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from codex_key_quarantine import CodexKeyQuarantine  # noqa: E402


PREFIX = "quarantine-key-span-"


def marker(action: str, label: str = "PRIVATE KEY") -> str:
    return "-----" + action + " " + label + "-----"


def record(text: str, *, kind: str = "event_msg") -> bytes:
    return (json.dumps({"type": kind, "payload": {"message": text}}) + "\n").encode()


def classify(
    scanner: CodexKeyQuarantine, raw: bytes, *, chunk_bytes: int | None = None
) -> str | None:
    scanner.begin_record()
    chunk_bytes = chunk_bytes or max(1, len(raw))
    for offset in range(0, len(raw), chunk_bytes):
        scanner.feed(raw[offset : offset + chunk_bytes])
    return scanner.end_record()


class CodexKeyQuarantineTests(unittest.TestCase):
    def test_clear_record_and_content_free_representation(self) -> None:
        scanner = CodexKeyQuarantine()
        self.assertIsNone(classify(scanner, record("ordinary synthetic evidence")))
        self.assertEqual("clear", scanner.state)
        self.assertEqual("CodexKeyQuarantine(state='clear')", repr(scanner))

    def test_complete_block_preserves_later_safe_record(self) -> None:
        scanner = CodexKeyQuarantine()
        block = marker("BEGIN") + "\nSYNTHETIC-BODY\n" + marker("END")
        self.assertEqual(PREFIX + "single", classify(scanner, record(block)))
        self.assertEqual("clear", scanner.state)
        self.assertIsNone(classify(scanner, record("later safe evidence")))

    def test_block_crosses_records_including_hidden_like_records(self) -> None:
        scanner = CodexKeyQuarantine()
        self.assertEqual(PREFIX + "open", classify(scanner, record(marker("BEGIN"))))
        self.assertEqual("open", scanner.state)
        self.assertEqual(
            PREFIX + "continue", classify(scanner, record("SYNTHETIC", kind="world_state"))
        )
        self.assertEqual(PREFIX + "close", classify(scanner, record(marker("END"))))
        self.assertIsNone(classify(scanner, record("safe after matching terminator")))

    def test_hidden_like_start_cannot_be_skipped_by_projection(self) -> None:
        scanner = CodexKeyQuarantine()
        self.assertEqual(
            PREFIX + "open", classify(scanner, record(marker("BEGIN"), kind="compacted"))
        )
        self.assertEqual(PREFIX + "continue", classify(scanner, record("continuation")))

    def test_every_chunk_boundary_and_one_byte_chunks(self) -> None:
        raw = record(marker("BEGIN", "RSA PRIVATE KEY") + "\n" + marker("END", "RSA PRIVATE KEY"))
        for split in range(len(raw) + 1):
            with self.subTest(split=split):
                scanner = CodexKeyQuarantine()
                scanner.begin_record()
                scanner.feed(raw[:split])
                scanner.feed(raw[split:])
                self.assertEqual(PREFIX + "single", scanner.end_record())
        self.assertEqual(PREFIX + "single", classify(CodexKeyQuarantine(), raw, chunk_bytes=1))

    def test_unicode_ascii_escapes_and_chunk_carry(self) -> None:
        text = marker("BEGIN") + "\n" + marker("END")
        escaped = "".join("\\u" + f"{ord(character):04x}" for character in text)
        raw = ('{"message":"' + escaped + '"}\n').encode()
        for chunk_bytes in (1, 2, 5, 6, 7, 31, len(raw)):
            with self.subTest(chunk_bytes=chunk_bytes):
                self.assertEqual(
                    PREFIX + "single",
                    classify(CodexKeyQuarantine(), raw, chunk_bytes=chunk_bytes),
                )

    def test_escaped_backslash_is_not_decoded_twice(self) -> None:
        literal_escape_text = "".join(
            "\\u" + f"{ord(character):04x}" for character in marker("BEGIN")
        )
        self.assertIsNone(
            classify(CodexKeyQuarantine(), record(literal_escape_text), chunk_bytes=1)
        )

    def test_repeated_complete_blocks_remain_single(self) -> None:
        block = marker("BEGIN") + marker("END")
        self.assertEqual(PREFIX + "single", classify(CodexKeyQuarantine(), record(block * 3)))

    def test_nested_opening_becomes_permanent(self) -> None:
        scanner = CodexKeyQuarantine()
        self.assertEqual(PREFIX + "open", classify(scanner, record(marker("BEGIN"))))
        self.assertEqual(PREFIX + "uncertain", classify(scanner, record(marker("BEGIN"))))
        self.assertEqual("uncertain", scanner.state)
        self.assertEqual(PREFIX + "continue", classify(scanner, record(marker("END"))))
        self.assertEqual(PREFIX + "continue", classify(scanner, record("apparently safe tail")))

    def test_mismatched_and_orphan_closing_markers_become_permanent(self) -> None:
        scanner = CodexKeyQuarantine()
        classify(scanner, record(marker("BEGIN", "RSA PRIVATE KEY")))
        self.assertEqual(PREFIX + "uncertain", classify(scanner, record(marker("END"))))
        self.assertEqual(
            PREFIX + "uncertain", classify(CodexKeyQuarantine(), record(marker("END")))
        )

    def test_incomplete_marker_is_uncertain_and_unclosed_block_stays_open(self) -> None:
        self.assertEqual(
            PREFIX + "uncertain",
            classify(CodexKeyQuarantine(), record("-----" + "BEGIN PRIVATE KEY")),
        )
        scanner = CodexKeyQuarantine()
        self.assertEqual(PREFIX + "open", classify(scanner, record(marker("BEGIN"))))
        self.assertEqual(PREFIX + "continue", classify(scanner, record("no terminator")))
        self.assertEqual("open", scanner.state)

    def test_complete_then_unclosed_block_does_not_resume(self) -> None:
        scanner = CodexKeyQuarantine()
        text = marker("BEGIN") + marker("END") + marker("BEGIN", "EC PRIVATE KEY")
        self.assertEqual(PREFIX + "open", classify(scanner, record(text)))
        self.assertEqual(PREFIX + "continue", classify(scanner, record("continuation")))

    def test_all_supported_framing_labels(self) -> None:
        for label in (
            "PRIVATE KEY", "ENCRYPTED PRIVATE KEY", "PGP PRIVATE KEY BLOCK", "DH PRIVATE KEY"
        ):
            with self.subTest(label=label):
                text = marker("BEGIN", label) + marker("END", label)
                self.assertEqual(PREFIX + "single", classify(CodexKeyQuarantine(), record(text)))
        text = (
            "---- BEGIN SSH2 " + "ENCRYPTED PRIVATE KEY ----\n---- END SSH2 "
            + "ENCRYPTED PRIVATE KEY ----"
        )
        self.assertEqual(
            PREFIX + "single", classify(CodexKeyQuarantine(), record(text), chunk_bytes=1)
        )

    def test_putty_is_permanently_uncertain(self) -> None:
        for version in (1, 2, 3):
            scanner = CodexKeyQuarantine()
            text = "PuTTY-User-Key-File-" + str(version) + ": ssh-rsa"
            self.assertEqual(PREFIX + "uncertain", classify(scanner, record(text), chunk_bytes=1))
            self.assertEqual(PREFIX + "continue", classify(scanner, record("later tail")))

    def test_unknown_private_label_and_overlong_marker_fail_closed(self) -> None:
        for label in ("unknown PRIVATE KEY", "PRIVATE KEY " + "A" * 200, "PRIVATE-KEY"):
            with self.subTest(label=label):
                self.assertEqual(
                    PREFIX + "uncertain",
                    classify(CodexKeyQuarantine(), record(marker("BEGIN", label))),
                )

    def test_public_certificate_is_not_a_private_key_block(self) -> None:
        text = marker("BEGIN", "CERTIFICATE") + marker("END", "CERTIFICATE")
        self.assertIsNone(classify(CodexKeyQuarantine(), record(text), chunk_bytes=1))

    def test_overlapping_marker_dashes_cannot_hide_private_opening(self) -> None:
        scanner = CodexKeyQuarantine()
        text = marker("BEGIN", "CERTIFICATE") + "BEGIN PRIVATE KEY-----"
        self.assertEqual(PREFIX + "open", classify(scanner, record(text), chunk_bytes=1))
        self.assertEqual(PREFIX + "continue", classify(scanner, record("continuation")))

    def test_malformed_public_marker_cannot_swallow_later_private_marker(self) -> None:
        text = "-----" + "BEGIN CERTIFICATE invalid." + marker("BEGIN")
        self.assertEqual(
            PREFIX + "open", classify(CodexKeyQuarantine(), record(text), chunk_bytes=1)
        )

    def test_force_uncertain_during_and_after_record(self) -> None:
        scanner = CodexKeyQuarantine()
        scanner.begin_record()
        scanner.force_uncertain()
        self.assertEqual(PREFIX + "uncertain", scanner.end_record())
        self.assertEqual(PREFIX + "continue", classify(scanner, record("tail")))
        scanner = CodexKeyQuarantine()
        self.assertIsNone(classify(scanner, record("before independent later check")))
        scanner.force_uncertain()
        self.assertEqual(PREFIX + "continue", classify(scanner, record("tail")))

    def test_large_feed_has_bounded_carry_and_does_not_retain_content(self) -> None:
        scanner = CodexKeyQuarantine()
        scanner.begin_record()
        scanner.feed(b'{"message":"' + b"SYNTHETIC-PADDING " * 100_000)
        self.assertLessEqual(len(scanner._escape_carry), 5)
        self.assertLessEqual(len(scanner._marker_carry), 128)
        scanner.feed(b'"}\n')
        self.assertIsNone(scanner.end_record())
        self.assertEqual(b"", scanner._escape_carry)
        self.assertEqual(b"", scanner._marker_carry)
        self.assertNotIn("SYNTHETIC", repr(scanner))

    def test_invalid_escape_without_private_context_does_not_poison_record(self) -> None:
        for raw in (b'{"message":"\\q"}\n', b'{"message":"\\u00xz"}\n', b'{"message":"\\u00'):
            with self.subTest(raw_length=len(raw)):
                # The caller still rejects invalid JSON independently.
                self.assertIsNone(classify(CodexKeyQuarantine(), raw, chunk_bytes=1))

    def test_generic_code_fragments_do_not_poison_record(self) -> None:
        fragments = (
            "-----" + "BEGIN ",
            "-----" + "BEGIN CERTIFICATE",
            "prefix = b'-----" + "BEGIN '",
            "pattern = rb'-----" + "BEGIN (?:(?:RSA )?PRIVATE KEY)-----'",
            "ordinary quote \\\" and backslash \\\\ and braces {}",
        )
        for text in fragments:
            for chunk_bytes in (1, 7, 64_000):
                with self.subTest(chunk_bytes=chunk_bytes):
                    scanner = CodexKeyQuarantine()
                    self.assertIsNone(classify(scanner, record(text), chunk_bytes=chunk_bytes))
                    self.assertEqual("clear", scanner.state)
                    self.assertIsNone(scanner.reason_code)

    def test_non_key_private_tags_are_benign(self) -> None:
        for label in ("PRIVATE_CONTENT", "PRIVATE_SECTION", "PRIVATE"):
            for chunk_bytes in (1, 7, 64_000):
                with self.subTest(label=label, chunk_bytes=chunk_bytes):
                    scanner = CodexKeyQuarantine()
                    text = marker("BEGIN", label) + marker("END", label)
                    self.assertIsNone(classify(scanner, record(text), chunk_bytes=chunk_bytes))
                    self.assertEqual("clear", scanner.state)
                    self.assertIsNone(scanner.reason_code)

    def test_non_key_private_content_tags_do_not_clear_open_key_span(self) -> None:
        for label in ("PRIVATE_CONTENT", "PRIVATE_SECTION"):
            with self.subTest(label=label):
                scanner = CodexKeyQuarantine()
                self.assertEqual(PREFIX + "open", classify(scanner, record(marker("BEGIN"))))
                text = marker("BEGIN", label) + marker("END", label)
                self.assertEqual(PREFIX + "continue", classify(scanner, record(text), chunk_bytes=1))
                self.assertEqual("open", scanner.state)
                self.assertEqual(PREFIX + "close", classify(scanner, record(marker("END"))))

    def test_reason_code_is_fixed_and_first_reason_survives(self) -> None:
        scanner = CodexKeyQuarantine()
        classify(scanner, record(marker("END")))
        self.assertEqual("orphan-private-terminator", scanner.reason_code)
        scanner.force_uncertain()
        self.assertEqual("orphan-private-terminator", scanner.reason_code)
        self.assertNotIn("PRIVATE", scanner.reason_code)

    def test_api_requires_record_boundaries(self) -> None:
        scanner = CodexKeyQuarantine()
        with self.assertRaises(RuntimeError):
            scanner.feed(b"{}")
        with self.assertRaises(RuntimeError):
            scanner.end_record()
        scanner.begin_record()
        with self.assertRaises(RuntimeError):
            scanner.begin_record()
        self.assertIsNone(scanner.end_record())


if __name__ == "__main__":
    unittest.main()
