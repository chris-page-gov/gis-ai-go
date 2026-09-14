import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import test from "node:test";
import { canonicalJson, canonicalJsonBytes } from "../src/canonical-json.js";
import { contentAddress } from "../src/digest.js";
import {
  WEB216_CPIH_CAPTURE,
  WEB216_CPIH_DOMAINS,
  WEB216_CPIH_POLICY_SCOPE,
  Web216CpihReceiptError,
  buildWeb216CpihReceipt,
  buildWeb216CpihResult,
  verifyWeb216CpihReceipt,
  verifyWeb216CpihReceiptStructure,
  type Web216CpihPeriod,
  type Web216CpihReceiptBuildInput,
  type Web216CpihReceiptVerificationMaterial,
} from "../src/web216-cpih-receipt.js";

const PROJECTION = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8")) as Record<string, unknown>;

function fixture(selected: Web216CpihPeriod = "2026-07") {
  const input: Web216CpihReceiptBuildInput = {
    period: selected,
    projection: structuredClone(PROJECTION),
    requestId: "web216-cpih-test-1",
    traceId: "0123456789abcdef0123456789abcdef",
    createdAt: "2026-09-14T16:00:00.000Z",
    software: { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) },
  };
  const receipt = buildWeb216CpihReceipt(input);
  const resultCore = buildWeb216CpihResult(input.projection, selected);
  const material: Web216CpihReceiptVerificationMaterial = {
    projection: input.projection,
    normalisedParameters: { period: selected },
    resultCore,
    expectedSoftware: input.software,
  };
  return { input, receipt, material, resultCore };
}

function reidentify(value: Record<string, unknown>): Record<string, unknown> {
  const { receipt_id: _old, ...core } = value;
  return { ...core, receipt_id: contentAddress("gis-ai-go:evidence-receipt", WEB216_CPIH_DOMAINS.receipt, core) };
}

function rehashProjection(value: Record<string, unknown>): void {
  const { projection_sha256: _old, ...core } = value;
  value.projection_sha256 = createHash("sha256").update(canonicalJsonBytes(core)).digest("hex");
}

test("both admitted months bind exact source-native index text and independently pinned material", () => {
  for (const [selected, expected] of [["2026-01", "139.4"], ["2026-07", "142.7"]] as const) {
    const { input, receipt, material, resultCore } = fixture(selected);
    assert.equal(verifyWeb216CpihReceiptStructure(receipt), true);
    assert.equal(verifyWeb216CpihReceipt(receipt, material).valid, true);
    assert.deepEqual(buildWeb216CpihReceipt(input), receipt);
    assert.equal(resultCore.observation.value, expected);
    assert.equal(typeof resultCore.observation.value, "string");
    assert.equal(resultCore.series.base_year, 2015);
    assert.equal(resultCore.series.base_year_basis, "exact-series-title");
    assert.equal(resultCore.capture.captured_at, PROJECTION.retrieved_at);
    assert.equal(resultCore.capture.release_date, "2026-08-18T23:00:00.000Z");
    assert.equal(resultCore.capture.next_release_validation, "unvalidated-provider-text");
    const sourceData = PROJECTION.data as { months: unknown[] };
    assert.deepEqual(resultCore.observation, sourceData.months[selected === "2026-01" ? 0 : 1]);
    assert.equal(Object.isFrozen(receipt.policy_scope), true);
    assert.equal(Object.isFrozen(resultCore.observation), true);
    assert.equal(receipt.evidence.persistence, "not-persisted");
    assert.equal(receipt.evidence.attestation, "not-attested");
    assert.equal(receipt.policy_scope.provider_egress, false);
    assert.equal(resultCore.capture.source_capture.mcp_executed, false);
    assert.equal(Object.hasOwn(resultCore.series, "edition"), false);
    assert.equal(Object.hasOwn(resultCore.series, "version"), false);
  }
  assert.notEqual(fixture("2026-01").receipt.receipt_id, fixture("2026-07").receipt.receipt_id);
});

test("source hashes are declarations bound by the projection, not a whole-response verification claim", () => {
  const { resultCore } = fixture();
  const description = (PROJECTION.data as { description: Record<string, unknown> }).description;
  assert.deepEqual(WEB216_CPIH_CAPTURE.original_body_sha256, PROJECTION.original_body_sha256);
  assert.equal(WEB216_CPIH_CAPTURE.capture_manifest_sha256, PROJECTION.capture_manifest_sha256);
  assert.equal(WEB216_CPIH_CAPTURE.projection_sha256, PROJECTION.projection_sha256);
  assert.equal(WEB216_CPIH_CAPTURE.fixture_schema, PROJECTION.schema_version);
  assert.deepEqual(WEB216_CPIH_CAPTURE.urls, PROJECTION.source_urls);
  assert.equal(WEB216_CPIH_CAPTURE.original_month_count, PROJECTION.full_captured_month_count);
  assert.deepEqual(WEB216_CPIH_CAPTURE.original_period_range, PROJECTION.full_captured_period_range);
  assert.equal(WEB216_CPIH_CAPTURE.next_release, description.nextRelease);
  assert.equal(resultCore.series.cdid, description.cdid);
  assert.equal(resultCore.series.dataset_id, description.datasetId);
  assert.equal(resultCore.series.title, description.title);
  assert.equal(resultCore.series.unit, description.unit);
  assert.equal(resultCore.capture.validation_scope, "pinned-two-month-projection-not-original-response-bodies");
  assert.equal(resultCore.capture.projected_month_count, 2);
  assert.equal(resultCore.currency, "as-of-recorded-capture-not-always-current");
});

test("substituted fixture material fails even if its own projection hash is recomputed", () => {
  const mutations: ((value: Record<string, unknown>) => void)[] = [
    (p) => { (p.data as { description: Record<string, unknown> }).description.cdid = "D7BT"; },
    (p) => { (p.data as { description: Record<string, unknown> }).description.datasetId = "OTHER"; },
    (p) => { (p.data as { description: Record<string, unknown> }).description.unit = "%"; },
    (p) => { (p.data as { months: Record<string, unknown>[] }).months[0]!.value = "139.40"; },
    (p) => { (p.data as { months: Record<string, unknown>[] }).months[1]!.value = 142.7; },
    (p) => { (p.data as { months: Record<string, unknown>[] }).months[1]!.value = "[suppressed]"; },
    (p) => { (p.original_body_sha256 as Record<string, unknown>).data = "0".repeat(64); },
    (p) => { p.capture_manifest_sha256 = "0".repeat(64); },
    (p) => { p.retrieved_at = "2026-09-14T15:42:57.906632Z"; },
    (p) => { (p.data as { description: Record<string, unknown> }).description.releaseDate = "2026-08-19T00:00:00Z"; },
    (p) => { (p.data as { months: Record<string, unknown>[] }).months[1]!.updateDate = "2026-09-01T00:00:00Z"; },
    (p) => { p.extra = "unknown"; },
    (p) => { (p.data as Record<string, unknown>).permission = "allow-live"; },
  ];
  const { input, receipt, material } = fixture();
  for (const mutate of mutations) {
    const projection = structuredClone(PROJECTION);
    mutate(projection);
    rehashProjection(projection);
    assert.throws(() => buildWeb216CpihReceipt({ ...input, projection }), Web216CpihReceiptError);
    assert.equal(verifyWeb216CpihReceipt(receipt, { ...material, projection }).valid, false);
  }
});

test("unknown or substituted periods and parameter authority fail closed", () => {
  const { input, receipt, material } = fixture();
  for (const selected of ["latest", "2026-02", "2026-08", "2026 JUL", null]) {
    assert.throws(() => buildWeb216CpihReceipt({ ...input, period: selected as Web216CpihPeriod }));
  }
  assert.equal(verifyWeb216CpihReceipt(receipt, {
    ...material, normalisedParameters: { period: "2026-01" },
  }).valid, false);
  assert.equal(verifyWeb216CpihReceipt(receipt, {
    ...material, normalisedParameters: { period: "2026-07", authority: "allow" },
  } as Web216CpihReceiptVerificationMaterial).valid, false);
});

test("full verification rejects changed result values, metadata and unknown nested fields", () => {
  const { receipt, material } = fixture();
  const mutations: ((r: Record<string, unknown>) => void)[] = [
    (r) => { (r.observation as Record<string, unknown>).value = "142.70"; },
    (r) => { (r.observation as Record<string, unknown>).value = ""; },
    (r) => { (r.series as Record<string, unknown>).base_year = 2020; },
    (r) => { (r.series as Record<string, unknown>).edition = "time-series"; },
    (r) => { (r.capture as Record<string, unknown>).captured_at = "2026-09-15T00:00:00Z"; },
    (r) => { r.authority = "allow"; },
  ];
  for (const mutate of mutations) {
    const resultCore = structuredClone(material.resultCore) as unknown as Record<string, unknown>;
    mutate(resultCore);
    assert.equal(verifyWeb216CpihReceipt(receipt, { ...material, resultCore } as unknown as Web216CpihReceiptVerificationMaterial).valid, false);
  }
});

test("rehashed receipts cannot manufacture authority, persistence, attestation or egress", () => {
  const { receipt, material } = fixture();
  const mutations: ((r: Record<string, unknown>) => void)[] = [
    (r) => { (r.policy_scope as Record<string, unknown>).provider_egress = true; },
    (r) => { (r.policy_scope as Record<string, unknown>).authority_profile = "owner-approved"; },
    (r) => { (r.policy_scope as Record<string, unknown>).grants_provider_permission = true; },
    (r) => { (r.evidence as Record<string, unknown>).persistence = "durable"; },
    (r) => { (r.evidence as Record<string, unknown>).attestation = "attested"; },
    (r) => { (r.capture as Record<string, unknown>).projection_sha256 = "1".repeat(64); },
    (r) => { (r.operation as Record<string, unknown>).name = "data.query"; },
    (r) => { (r.operation as Record<string, unknown>).period = "2026-01"; },
    (r) => { (r.result as Record<string, unknown>).sha256 = "0".repeat(64); },
    (r) => { r.authority_context = { grants: "everything" }; },
    (r) => { r.storage = { durable: true }; },
  ];
  for (const mutate of mutations) {
    const altered = structuredClone(receipt) as unknown as Record<string, unknown>;
    mutate(altered);
    const rehashed = reidentify(altered);
    assert.equal(verifyWeb216CpihReceiptStructure(rehashed), false);
    assert.equal(verifyWeb216CpihReceipt(rehashed, material).valid, false);
  }
  assert.deepEqual(receipt.policy_scope, WEB216_CPIH_POLICY_SCOPE);
});

test("caller authority and unknown top-level build or verification fields are refused", () => {
  const { input, receipt, material } = fixture();
  assert.throws(() => buildWeb216CpihReceipt({ ...input, policy: WEB216_CPIH_POLICY_SCOPE } as Web216CpihReceiptBuildInput));
  assert.equal(verifyWeb216CpihReceipt(receipt, { ...material, authority: "allow" } as Web216CpihReceiptVerificationMaterial).valid, false);
  assert.equal(verifyWeb216CpihReceipt(receipt, { ...material, projection: { projection_sha256: WEB216_CPIH_CAPTURE.projection_sha256 } }).valid, false);
  assert.equal(verifyWeb216CpihReceipt(receipt, {
    ...material, expectedSoftware: { ...material.expectedSoftware, revision: "b".repeat(40) },
  }).valid, false);
});

test("timestamps validate calendars and retain microseconds without rounding an earlier receipt", () => {
  const { input } = fixture();
  for (const createdAt of ["2026-02-30T16:00:00Z", "2026-09-14T15:42:57.906632Z", "2026-09-14T15:42:57.906Z", "2026-09-14T16:00:00+01:00"]) {
    assert.throws(() => buildWeb216CpihReceipt({ ...input, createdAt }), Web216CpihReceiptError);
  }
  for (const createdAt of [WEB216_CPIH_CAPTURE.captured_at, "2026-09-14T15:42:57.907Z"]) {
    assert.equal(verifyWeb216CpihReceiptStructure(buildWeb216CpihReceipt({ ...input, createdAt })), true);
  }
});

test("canonical safety rejects accessors, undefined, non-finite values and cyclic material", () => {
  const { input, receipt, material } = fixture();
  let reads = 0;
  const accessor = Object.defineProperty({}, "projection", { enumerable: true, get() { reads++; return PROJECTION; } });
  assert.throws(() => buildWeb216CpihReceipt(accessor as Web216CpihReceiptBuildInput));
  assert.equal(reads, 0);
  for (const projection of [{ ...PROJECTION, extra: undefined }, { ...PROJECTION, extra: NaN }]) {
    assert.equal(verifyWeb216CpihReceipt(receipt, { ...material, projection }).valid, false);
  }
  const cyclic: Record<string, unknown> = {}; cyclic.self = cyclic;
  assert.throws(() => buildWeb216CpihReceipt({ ...input, projection: cyclic }));
  assert.equal(verifyWeb216CpihReceiptStructure(null), false);
  assert.equal(canonicalJson(receipt).includes("durable"), false);
});
