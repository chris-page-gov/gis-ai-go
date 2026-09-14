"""Bounded, content-free quarantine decisions for original Codex JSONL records.

This is a conservative lexical classifier, not a JSON or private-key validator.
The caller must still validate the source and redact and verify every retained
projection. JSON escapes are decoded once so ASCII marker spelling cannot bypass
the classifier. No source value is exposed; only a small incomplete escape/marker
carry and a recognised framing label survive a feed call.
"""

from __future__ import annotations

import re


_CHUNK_BYTES = 64 * 1024
_MAX_MARKER_BYTES = 128
_PREFIX = "quarantine-key-span-"
_STARTS = (
    b"-----BEGIN ",
    b"-----END ",
    b"---- BEGIN SSH2 ",
    b"---- END SSH2 ",
    b"PuTTY-User-Key-File-",
)
_START_PATTERN = re.compile(b"|".join(re.escape(value) for value in _STARTS))
_MAX_START_BYTES = max(map(len, _STARTS))
_ESCAPE_PATTERN = re.compile(rb"\\(?:u[0-9a-fA-F]{0,4}|[\s\S]?)")
_PRIVATE_LABEL = re.compile(
    rb"(?:(?:[A-Z0-9][A-Z0-9 -]{0,62} )?PRIVATE KEY|PGP PRIVATE KEY BLOCK)"
)
_LABEL_CHARACTERS = re.compile(rb"[A-Za-z0-9 -]*")
_PRIVATE_HINT = re.compile(rb"\bPRIVATE[ -]+KEY\b", re.IGNORECASE)
_ESCAPES = {
    b'"': b'"',
    b"\\": b"\\",
    b"/": b"/",
    b"b": b"\b",
    b"f": b"\f",
    b"n": b"\n",
    b"r": b"\r",
    b"t": b"\t",
}


class CodexKeyQuarantine:
    """Classify complete records without retaining their content.

    ``begin_record`` and ``end_record`` delimit one original JSONL record;
    ``feed`` accepts arbitrary chunk boundaries within it. An open recognised
    block survives record boundaries. Uncertain framing never clears, including
    at an apparent later terminator. ``force_uncertain`` also works between
    records for a caller's later independent marker check.
    """

    def __init__(self) -> None:
        self._active = False
        self._uncertain = False
        self._open_label: tuple[bytes, bytes] | None = None
        self._escape_carry = b""
        self._marker_carry = b""
        self._record_initial_state = "clear"
        self._record_saw_marker = False
        self._reason_code: str | None = None

    @property
    def state(self) -> str:
        if self._uncertain:
            return "uncertain"
        return "open" if self._open_label is not None else "clear"

    def __repr__(self) -> str:
        return f"CodexKeyQuarantine(state={self.state!r})"

    @property
    def reason_code(self) -> str | None:
        """Return only a fixed reason code, never an observed marker or value."""

        return self._reason_code

    def begin_record(self) -> None:
        if self._active:
            raise RuntimeError("a quarantine record is already active")
        self._active = True
        self._record_initial_state = self.state
        self._record_saw_marker = False
        self._escape_carry = b""
        self._marker_carry = b""

    def force_uncertain(self) -> None:
        """Permanently quarantine this record and all later records."""

        self._mark_uncertain("external-marker")

    def _mark_uncertain(self, reason_code: str) -> None:
        if not self._uncertain:
            self._reason_code = reason_code
        self._uncertain = True
        self._open_label = None
        self._escape_carry = b""
        self._marker_carry = b""

    def feed(self, raw: bytes) -> None:
        if not self._active:
            raise RuntimeError("begin_record must precede quarantine input")
        if not isinstance(raw, bytes):
            raise TypeError("quarantine input must be bytes")
        if self._uncertain:
            return
        for offset in range(0, len(raw), _CHUNK_BYTES):
            chunk = self._escape_carry + raw[offset : offset + _CHUNK_BYTES]
            self._escape_carry = b""

            def decode_escape(match: re.Match[bytes]) -> bytes:
                token = match.group()
                if token == b"\\" or (token.startswith(b"\\u") and len(token) < 6):
                    if match.end() == len(chunk):
                        self._escape_carry = token
                        return b""
                    elif self._open_label is not None:
                        self._mark_uncertain("invalid-escape-in-open-span")
                    return b"\x00"
                if token.startswith(b"\\u"):
                    codepoint = int(token[2:], 16)
                    # Non-ASCII code points cannot be ASCII marker characters.
                    # A separator prevents accidental joining across them.
                    return bytes((codepoint,)) if codepoint < 128 else b"\x00"
                decoded = _ESCAPES.get(token[1:])
                if decoded is None:
                    if self._open_label is not None:
                        self._mark_uncertain("invalid-escape-in-open-span")
                    return b"\x00"
                return decoded

            decoded = _ESCAPE_PATTERN.sub(decode_escape, chunk)
            if self._uncertain:
                self._escape_carry = b""
                return
            self._scan_markers(decoded)
            if self._uncertain:
                return

    def _scan_markers(self, decoded: bytes) -> None:
        value = self._marker_carry + decoded
        self._marker_carry = b""
        cursor = 0
        while match := _START_PATTERN.search(value, cursor):
            prefix = match.group()
            if prefix == _STARTS[4]:
                # PuTTY containers use counted sections rather than one matching
                # end marker. No format parser is claimed by this classifier.
                self._mark_uncertain("unframed-putty-container")
                return
            family = b"pem" if prefix.startswith(b"-----") else b"ssh2"
            closing = b"END" in prefix
            terminator = b"-----" if family == b"pem" else b" ----"
            label_start = match.end()
            marker_limit = match.start() + _MAX_MARKER_BYTES
            marker_end = value.find(terminator, label_start, marker_limit)
            if marker_end == -1:
                candidate = value[match.start() : marker_limit]
                label_tail = value[label_start:marker_limit]
                plausible_label = _LABEL_CHARACTERS.fullmatch(label_tail) is not None
                label_prefix = _LABEL_CHARACTERS.match(label_tail).group()
                if len(value) - match.start() >= _MAX_MARKER_BYTES:
                    if plausible_label and _PRIVATE_HINT.search(label_tail):
                        self._mark_uncertain("oversized-private-marker")
                        return
                elif plausible_label:
                    self._marker_carry = candidate
                    return
                if _PRIVATE_HINT.search(label_prefix):
                    self._mark_uncertain("incomplete-private-marker")
                    return
                # Quoted code and regular expressions can contain generic BEGIN
                # fragments. They are not private-key markers. Do not swallow a
                # later independently recognisable marker in the same chunk.
                cursor = match.start() + 1
                continue
            label = value[label_start:marker_end]
            # A malformed neighbouring marker can reuse these closing dashes as
            # its own opening. Search from the terminator, not beyond it.
            cursor = marker_end
            recognised = (
                _PRIVATE_LABEL.fullmatch(label) is not None
                if family == b"pem"
                else label == b"ENCRYPTED PRIVATE KEY"
            )
            if not recognised:
                label_prefix = _LABEL_CHARACTERS.match(label).group()
                if _PRIVATE_HINT.search(label_prefix):
                    self._mark_uncertain("malformed-private-marker")
                    return
                if (
                    _LABEL_CHARACTERS.fullmatch(label) is not None
                    and self._open_label is not None
                ):
                    self._mark_uncertain("mismatched-marker")
                    return
                continue
            framing = (family, label)
            self._record_saw_marker = True
            if closing:
                if self._open_label != framing:
                    self._mark_uncertain(
                        "mismatched-private-terminator"
                        if self._open_label
                        else "orphan-private-terminator"
                    )
                    return
                self._open_label = None
            elif self._open_label is not None:
                self._mark_uncertain("nested-private-marker")
                return
            else:
                self._open_label = framing
        # Preserve only a suffix which can become a recognised marker prefix.
        # Ordinary source chunks remain on the native regex fast path.
        tail = value[max(cursor, len(value) - _MAX_START_BYTES + 1) :]
        for size in range(len(tail), 0, -1):
            suffix = tail[-size:]
            if any(prefix.startswith(suffix) for prefix in _STARTS):
                self._marker_carry = suffix
                break

    def end_record(self) -> str | None:
        if not self._active:
            raise RuntimeError("no quarantine record is active")
        if self._escape_carry and self._open_label is not None:
            self._mark_uncertain("invalid-escape-in-open-span")
        if _PRIVATE_HINT.search(self._marker_carry):
            # An incomplete plausible PRIVATE KEY label is unsafe, unlike an
            # ordinary quote, escape or non-private BEGIN fragment in code.
            self._mark_uncertain("incomplete-private-marker")
        self._active = False
        self._escape_carry = b""
        self._marker_carry = b""
        if self._record_initial_state == "uncertain":
            return _PREFIX + "continue"
        if self._uncertain:
            return _PREFIX + "uncertain"
        if self._record_initial_state == "open":
            return _PREFIX + ("continue" if self.state == "open" else "close")
        if self.state == "open":
            return _PREFIX + "open"
        if self._record_saw_marker:
            return _PREFIX + "single"
        return None
