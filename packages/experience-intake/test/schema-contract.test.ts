import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { inspectZipArchive, planIntake, type IntakeFile } from "../src/index.js";

interface ContractCase {
  label: string;
  schema: "request" | "result";
  value: unknown;
  valid: boolean;
}

const REPOSITORY_ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const UV_CACHE_DIRECTORY = fileURLToPath(new URL("../../../../.uv-cache", import.meta.url));
const DRAFT_2020_12_CHECK = [
  "import json, sys",
  "from jsonschema import Draft202012Validator, FormatChecker",
  "batch = json.load(sys.stdin)",
  "validators = {}",
  "for name in ('request', 'result'):",
  "    schema = batch['schemas'][name]",
  "    Draft202012Validator.check_schema(schema)",
  "    validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())",
  "results = []",
  "for case in batch['cases']:",
  "    error = next(validators[case['schema']].iter_errors(case['value']), None)",
  "    results.append({'label': case['label'], 'valid': error is None,",
  "                    'error': None if error is None else error.json_path + ': ' + error.message[:300]})",
  "json.dump(results, sys.stdout)",
].join("\n");

function schema(name: "request" | "result"): unknown {
  return JSON.parse(readFileSync(new URL(`../../schema/${name}.v1.schema.json`, import.meta.url), "utf8"));
}

function checkContracts(cases: readonly ContractCase[]): void {
  // Reuse the repository's pinned test-only validator. The planner retains its
  // independent runtime checks and gains no Python or JSON Schema dependency.
  const validation = spawnSync("uv", [
    "run", "--locked", "--cache-dir", UV_CACHE_DIRECTORY, "--project", REPOSITORY_ROOT,
    "python", "-c", DRAFT_2020_12_CHECK,
  ], {
    cwd: REPOSITORY_ROOT,
    encoding: "utf8",
    input: JSON.stringify({ schemas: { request: schema("request"), result: schema("result") }, cases }),
    maxBuffer: 1_048_576,
    timeout: 30_000,
  });
  assert.equal(validation.error, undefined, `Schema validator failed to start: ${validation.error?.message}`);
  assert.equal(validation.status, 0, `Schema definitions or validator failed: ${validation.stderr}`);
  const results = JSON.parse(validation.stdout) as { label: string; valid: boolean; error: string | null }[];
  assert.equal(results.length, cases.length, "Every contract case must be checked");
  for (const [index, expected] of cases.entries()) {
    const actual = results[index]!;
    assert.equal(actual.label, expected.label, "The validator must preserve case identity");
    assert.equal(actual.valid, expected.valid,
      `${expected.schema}: ${expected.label}: ${actual.error ?? "unexpectedly accepted"}`);
  }
}

function file(name: string, text?: string): IntakeFile {
  return { name, size: text === undefined ? 20 : Buffer.byteLength(text, "utf8"),
    ...(text === undefined ? {} : { text }) };
}

test("published intake schemas check real producer outputs and reject contract drift", () => {
  const requests = [
    { label: "empty", value: { files: [] } },
    { label: "text preview", value: { files: [file("notes.txt", "Synthetic note\n" + "x".repeat(1_300))] } },
    { label: "table preview", value: { files: [file("counts.csv", "place,count\n" + "Example,2\n".repeat(12))] } },
    { label: "geographic preview", value: { files: [file("place.geojson",
      '{"type":"Feature","geometry":{"type":"Point","coordinates":[-1.58,52.28]},"properties":{"name":"Synthetic place"}}')] } },
    { label: "malformed geography needs input", value: { files: [file("bad.geojson", "{}")] } },
    { label: "missing text needs input", value: { files: [file("notes.txt")] } },
    { label: "grouped Shapefile planned only", value: { files: ["shp", "shx", "dbf", "prj", "cpg"].map(ext => file(`places.${ext}`)) } },
    { label: "URL companion suggestions", value: { files: [], urls: ["https://example.org/places.shp"] } },
    { label: "oversize file blocked", value: { files: [{ name: "large.csv", size: 21 * 1_024 * 1_024 }] } },
    { label: "maximum descriptor counts", value: { files: Array.from({ length: 64 }, () => file("note.txt")),
      urls: Array.from({ length: 8 }, () => "https://example.org/data.csv") } },
  ];
  const plans = requests.map(({ value }) => planIntake(value));
  assert.deepEqual(new Set(plans.map(plan => plan.status)), new Set(["empty", "ready", "attention", "blocked"]));
  assert.deepEqual(new Set(plans.flatMap(plan => plan.items.map(item => item.status))),
    new Set(["preview-ready", "needs-input", "planned-only", "blocked"]));
  assert.deepEqual(new Set(plans.flatMap(plan => plan.items.flatMap(item => item.preview ? [item.preview.kind] : []))),
    new Set(["text", "table", "geojson"]));

  // A valid empty ZIP exercises the optional archive-evidence contract without
  // inventing an archive result or extracting any contents.
  const emptyZip = Buffer.alloc(22);
  emptyZip.writeUInt32LE(0x06054b50);
  const archive = inspectZipArchive("empty.zip", emptyZip);
  assert.equal(archive.evidence.archive?.memberCount, 0);
  const textPlan = plans[1]!;
  const textItem = textPlan.items[0]!;
  const { policy: _omittedPolicy, ...missingPolicy } = textPlan;
  const cases: ContractCase[] = requests.flatMap(({ label, value }, index) => [
    { label, schema: "request", value, valid: true },
    { label, schema: "result", value: plans[index], valid: true },
  ]);
  cases.push(
    { label: "real ZIP inventory", schema: "result", value: archive, valid: true },
    { label: "real invalid-request refusal", schema: "result", value: planIntake(null), valid: true },
    { label: "real malformed-ZIP refusal", schema: "result", value: inspectZipArchive("bad.zip", new Uint8Array()), valid: true },
    { label: "unknown request property", schema: "request", value: { files: [], fetch: true }, valid: false },
    { label: "missing file size", schema: "request", value: { files: [{ name: "note.txt" }] }, valid: false },
    { label: "unknown file property", schema: "request", value: { files: [{ ...file("note.txt"), secret: "synthetic" }] }, valid: false },
    { label: "negative file size", schema: "request", value: { files: [{ name: "note.txt", size: -1 }] }, valid: false },
    { label: "fractional file size", schema: "request", value: { files: [{ name: "note.txt", size: 1.5 }] }, valid: false },
    { label: "unsafe integer size", schema: "request", value: { files: [{ name: "note.txt", size: Number.MAX_SAFE_INTEGER + 1 }] }, valid: false },
    { label: "too many files", schema: "request", value: { files: Array.from({ length: 65 }, () => file("note.txt")) }, valid: false },
    { label: "too many URLs", schema: "request", value: { files: [], urls: Array.from({ length: 9 }, () => "https://example.org/") }, valid: false },
    { label: "unknown result property", schema: "result", value: { ...textPlan, hosted: true }, valid: false },
    { label: "missing policy", schema: "result", value: missingPolicy, valid: false },
    { label: "invented result status", schema: "result", value: { ...textPlan, status: "imported" }, valid: false },
    { label: "network authority must stay zero", schema: "result", value: { ...textPlan, policy: { ...textPlan.policy, networkRequests: 1 } }, valid: false },
    { label: "unknown item property", schema: "result", value: { ...textPlan, items: [{ ...textItem, published: true }] }, valid: false },
    { label: "invented preview kind", schema: "result", value: { ...textPlan, items: [{ ...textItem, preview: { ...textItem.preview, kind: "binary-import" } }] }, valid: false },
    { label: "oversize published excerpt", schema: "result", value: { ...textPlan, items: [{ ...textItem, preview: { ...textItem.preview, excerpt: "x".repeat(1_201) } }] }, valid: false },
    { label: "archive cannot claim extraction", schema: "result", value: { ...archive, evidence: { ...archive.evidence,
      archive: { ...archive.evidence.archive, contentExtracted: true } } }, valid: false },
  );
  checkContracts(cases);
});

test("schema-valid descriptors remain subject to stricter path and UTF-8 runtime rules", () => {
  const unsafePath = { files: [{ name: "note.txt", relativePath: "../note.txt", size: 20 }] };
  // The JSON Schema counts characters; the runtime independently limits bytes.
  const excessiveBytes = { files: [file("note.txt", "é".repeat(140_000))] };
  const pathResult = planIntake(unsafePath);
  const byteResult = planIntake(excessiveBytes);
  assert.equal(pathResult.status, "blocked");
  assert.equal(pathResult.issues[0]?.code, "invalid-request");
  assert.equal(byteResult.status, "blocked");
  assert.equal(byteResult.items[0]?.issues[0]?.code, "preview-size-limit");
  checkContracts([
    { label: "traversal is structurally valid", schema: "request", value: unsafePath, valid: true },
    { label: "UTF-8 excess is structurally valid", schema: "request", value: excessiveBytes, valid: true },
    { label: "path refusal remains a valid result", schema: "result", value: pathResult, valid: true },
    { label: "byte-budget refusal remains a valid result", schema: "result", value: byteResult, valid: true },
  ]);
});
