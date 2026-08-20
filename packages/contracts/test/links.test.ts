import assert from "node:assert/strict";
import test from "node:test";

import { isSafeNavigableHref, safeNavigableHref } from "../src/index.js";

const PUBLIC_BASE = "https://chris-page-gov.github.io/gis-ai-go/";
const LOCAL_BASE = "http://127.0.0.1:4173/gis-ai-go/";

test("accepts HTTPS and deployment-relative catalogue destinations", () => {
  assert.equal(
    safeNavigableHref("https://example.org/catalogue?id=one", PUBLIC_BASE),
    "https://example.org/catalogue?id=one",
  );
  assert.equal(
    safeNavigableHref("catalogue/records/dataset/record.md", PUBLIC_BASE),
    "catalogue/records/dataset/record.md",
  );
  assert.ok(isSafeNavigableHref("catalogue/okf-bundle.json", LOCAL_BASE));
});

test("rejects active, credentialled, protocol-relative and cross-base destinations", () => {
  for (const value of [
    "javascript:alert(1)",
    "data:text/html,unsafe",
    "http://example.org/plaintext",
    "https://user:secret@example.org/",
    "//example.org/path",
    "/absolute/path",
    "../outside",
    "%2e%2e/outside",
    "catalogue%2frecord",
    "catalogue\\record",
  ]) {
    assert.equal(safeNavigableHref(value, PUBLIC_BASE), null, value);
  }
});

test("rejects malformed encoding, controls, bidi and whitespace disguises", () => {
  for (const value of [
    "%",
    " catalogue/record",
    "catalogue/record ",
    "catalogue/\u0000record",
    "catalogue/\u202erecord",
  ]) {
    assert.equal(safeNavigableHref(value, PUBLIC_BASE), null, value);
  }
});

test("allows local HTTP only for relative same-origin development links", () => {
  assert.equal(safeNavigableHref("catalogue/record", LOCAL_BASE), "catalogue/record");
  assert.equal(safeNavigableHref("http://127.0.0.1:4173/catalogue/record", LOCAL_BASE), null);
  assert.equal(safeNavigableHref("../outside", LOCAL_BASE), null);
});
