import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import { boundedTransport, canonical, checkToolResult, verifyReceipt, verifyResult } from "../scripts/local214_demo.mjs";

const SOURCE = { source_commit: "1".repeat(40), software_version: "0.1.0" };
const hash = (domain, value) => createHash("sha256").update("GIS-AI-GO\0canonical-json\0sha256\0v1\0")
  .update(domain).update("\0").update(canonical(value)).digest("hex");
function fixture(operation = "catalogue.search", suffix = "1") {
  const [version, domain] = {
    "catalogue.search": [1, "gis-ai-go.catalogue-result-core.v1"],
    "data.query": [2, "gis-ai-go.data-query-result-core.v1"],
    "evidence.inspect": [3, "gis-ai-go.evidence-inspect-result-core.v3"],
  }[operation];
  const body = { operation, request_id: `request-${suffix}`, trace_id: suffix.repeat(32), data: { value: suffix } };
  const receiptCore = { schema: `gis-ai-go.evidence-receipt.v${version}`,
    request_id: body.request_id, trace_id: body.trace_id, operation: { name: operation },
    software: { revision: SOURCE.source_commit, version: SOURCE.software_version },
    result: { domain, sha256: hash(domain, body) } };
  const receipt = { ...receiptCore, receipt_id: `gis-ai-go:evidence-receipt:sha256:${hash(receiptCore.schema, receiptCore)}` };
  return { ...body, evidence_receipt: receipt };
}

test("independent receipt check rejects changed evidence and incomplete plain text", () => {
  const body = fixture();
  const receipt = body.evidence_receipt;
  assert.equal(verifyReceipt(receipt), receipt.receipt_id);
  assert.throws(() => verifyReceipt({ ...receipt, data: { z: 2, a: "fixed" } }), /content identity/u);
  const result = { structuredContent: body, content: [{ type: "text", text: JSON.stringify(body) }] };
  assert.equal(checkToolResult(result, "catalogue.search", undefined, SOURCE), body);
  assert.throws(() => checkToolResult({ ...result, content: [{ type: "text", text: "Summary only" }] }, "catalogue.search", undefined, SOURCE), /Plain-text/u);
});

test("otherwise-valid receipts cannot be swapped or detached from result and source", () => {
  for (const operation of ["catalogue.search", "data.query", "evidence.inspect"]) {
    const first = fixture(operation), second = fixture(operation, "2");
    verifyResult(first, operation, SOURCE);
    verifyResult(second, operation, SOURCE);
    assert.throws(() => verifyResult({ ...first, evidence_receipt: second.evidence_receipt }, operation, SOURCE), /this request/u);
    assert.throws(() => verifyResult({ ...first, data: { value: "changed" } }, operation, SOURCE), /result core/u);
    assert.throws(() => verifyResult(first, operation, { ...SOURCE, source_commit: "2".repeat(40) }), /source commit/u);
    assert.throws(() => verifyResult({ ...first, trace_id: "2".repeat(32) }, operation, SOURCE), /this trace/u);
  }
});

test("bounded client rejects changed endpoints before any network call", async () => {
  let calls = 0;
  const transport = boundedTransport(async () => { calls += 1; return new Response("{}"); });
  for (const target of ["https://example.invalid/mcp", "http://localhost:8787/mcp", "http://127.0.0.1:8787/mcp?target=other"]) {
    await assert.rejects(() => transport.fetch(target), /fixed loopback/u);
  }
  assert.equal(calls, 0);
  const response = await transport.fetch("http://127.0.0.1:8787/mcp");
  assert.equal(await response.text(), "{}");
  assert.deepEqual(transport.counts(), { requests: 1, response_bytes: 2 });
});

test("bounded client refuses excessive response bodies and request counts", async () => {
  const oversized = boundedTransport(async () => new Response("x".repeat(2_097_153)));
  await assert.rejects(() => oversized.fetch("http://127.0.0.1:8787/mcp"), /response bound/u);
  const many = boundedTransport(async () => new Response("{}"));
  for (let i = 0; i < 32; i++) await many.fetch("http://127.0.0.1:8787/mcp");
  await assert.rejects(() => many.fetch("http://127.0.0.1:8787/mcp"), /request\/time bound/u);
});

test("negative cases require the precise server outcome", () => {
  const body = { operation: "selection.resolve", code: "missing_dimension" };
  const result = { isError: true, structuredContent: body, content: [{ type: "text", text: JSON.stringify(body) }] };
  assert.equal(checkToolResult(result, "selection.resolve", "missing_dimension"), body);
  assert.throws(() => checkToolResult(result, "selection.resolve", "idempotency_completed"));
  const catalogue = { schema: "gis-ai-go.catalogue-problem.v1", code: "invalid_request" };
  assert.equal(checkToolResult({ isError: true, structuredContent: catalogue,
    content: [{ type: "text", text: JSON.stringify(catalogue) }] }, "catalogue.search", "invalid_request"), catalogue);
  const completed = { schema: "gis-ai-go.data-query-reconciliation-problem.v1", code: "idempotency_completed" };
  assert.equal(checkToolResult({ isError: true, structuredContent: completed,
    content: [{ type: "text", text: JSON.stringify(completed) }] }, "data.query", "idempotency_completed"), completed);
});
