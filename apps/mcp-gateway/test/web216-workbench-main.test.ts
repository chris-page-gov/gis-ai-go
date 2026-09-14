import assert from "node:assert/strict";
import { chmodSync, lstatSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { assertWeb216WorkbenchArguments, openWeb216WorkbenchState, WEB216_WORKBENCH_ORIGIN, web216WorkbenchLifecycle } from "../src/web216-workbench-main.js";
import { WEB216_WORKBENCH_HOST, WEB216_WORKBENCH_PORT } from "../src/web216-workbench-server.js";
const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");

test("launcher fixes port 8788, refuses configuration arguments and emits bounded non-authorising lifecycle records", () => {
  assert.equal(WEB216_WORKBENCH_HOST, "127.0.0.1"); assert.equal(WEB216_WORKBENCH_PORT, 8788);
  assert.equal(WEB216_WORKBENCH_ORIGIN, "http://127.0.0.1:8788");
  assert.doesNotThrow(() => assertWeb216WorkbenchArguments(["node", "launcher.js"]));
  for (const argument of ["--port=8787", "--host=0.0.0.0", "--provider=https://example.org", "--state=/tmp"]) {
    assert.throws(() => assertWeb216WorkbenchArguments(["node", "launcher.js", argument]), /no arguments/u);
  }
  const record = web216WorkbenchLifecycle("started", SOFTWARE.revision, "b".repeat(64));
  assert.equal(record.provider_egress, false); assert.equal(record.activated_supported_release, false);
  assert.equal(record.runtime_build_attestation, "not-attested");
  assert.equal(record.storage, "private-local-durable-retained-after-shutdown");
  assert.equal(JSON.stringify(record).includes(tmpdir()), false);
});

test("private store identity binds the capture, ledger and reconciliation index and preserves completed receipts on reopen", (t) => {
  const parent = mkdtempSync(join(tmpdir(), "web216-state-")); t.after(() => rmSync(parent, { recursive: true, force: true }));
  const first = openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW);
  const root = join(parent, "web216-public-data-workbench-v1");
  assert.deepEqual(readdirSync(root).sort(), ["identity.json", "ledger", "reconciliation"]);
  assert.equal(lstatSync(root).mode & 0o777, 0o700); assert.equal(lstatSync(join(root, "identity.json")).mode & 0o777, 0o600);
  const selection = first.application.resolve({ period: "2026-01" });
  const query = first.application.query({ period: "2026-01", selection_plan_id: selection.plan_id, idempotency_key: KEY }, { requestId: "persisted-query", traceId: "c".repeat(32) });
  const second = openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW);
  assert.deepEqual(second.identity, first.identity);
  assert.deepEqual(second.application.inspect({ idempotency_key: KEY }), query);
  assert.equal(second.ledger.verify().event_count, 1);
  assert.equal(JSON.stringify(second.identity).includes(KEY), false);
});

test("missing, tampered, public-permission and linked state cannot be adopted", (t) => {
  const parent = mkdtempSync(join(tmpdir(), "web216-state-invalid-")); t.after(() => rmSync(parent, { recursive: true, force: true }));
  openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW);
  const root = join(parent, "web216-public-data-workbench-v1"); const marker = join(root, "identity.json");
  const original = readFileSync(marker);
  writeFileSync(marker, JSON.stringify({ ...JSON.parse(original.toString()) as object, provider_egress: true }));
  assert.throws(() => openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW), /identity mismatch/u);
  writeFileSync(marker, original); chmodSync(marker, 0o644);
  assert.throws(() => openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW), /validation/u);
  chmodSync(marker, 0o600); rmSync(marker);
  assert.throws(() => openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW), /incomplete/u);
  const outside = join(parent, "outside.json"); writeFileSync(outside, original, { mode: 0o600 }); symlinkSync(outside, marker);
  assert.throws(() => openWeb216WorkbenchState(parent, PROJECTION, SOFTWARE, NOW), /validation/u);
});
