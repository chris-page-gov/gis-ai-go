// Independent local MCP client: fixed approved data, no model or provider calls.
import assert from "node:assert/strict";
import { createHash, randomBytes } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ENDPOINT = "http://127.0.0.1:8787/mcp";
const PROTOCOL = "2026-07-28";
const OPERATIONS = ["catalogue.search", "catalogue.describe", "selection.resolve", "data.query", "evidence.inspect"];
const RESOURCES = ["catalogue.public", "catalogue.record", "evidence.receipt"];
const PREFIX = "GIS-AI-GO\0canonical-json\0sha256\0v1\0";
const RECEIPT = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const RESULT_CONTRACTS = {
  "catalogue.search": ["gis-ai-go.evidence-receipt.v1", "gis-ai-go.catalogue-result-core.v1"],
  "catalogue.describe": ["gis-ai-go.evidence-receipt.v1", "gis-ai-go.catalogue-result-core.v1"],
  "selection.resolve": ["gis-ai-go.evidence-receipt.v2", "gis-ai-go.selection-resolve-result-core.v1"],
  "data.query": ["gis-ai-go.evidence-receipt.v2", "gis-ai-go.data-query-result-core.v1"],
  "evidence.inspect": ["gis-ai-go.evidence-receipt.v3", "gis-ai-go.evidence-inspect-result-core.v3"],
};
const contentDigest = (domain, value) => createHash("sha256").update(PREFIX).update(domain).update("\0").update(canonical(value)).digest("hex");

// This independent, JSON-only implementation covers the returned receipt values.
export function canonical(value) {
  if (value === null || typeof value !== "object") {
    assert(value === null || ["string", "number", "boolean"].includes(typeof value));
    if (typeof value === "number") assert(Number.isFinite(value));
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  assert.equal(Object.getPrototypeOf(value), Object.prototype);
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
}

export function verifyReceipt(receipt) {
  assert.match(receipt.receipt_id, RECEIPT);
  assert.match(receipt.schema, /^gis-ai-go\.evidence-receipt\.v[123]$/u);
  const { receipt_id, ...core } = receipt;
  const hash = contentDigest(receipt.schema, core);
  assert.equal(receipt_id, `gis-ai-go:evidence-receipt:sha256:${hash}`, "Receipt content identity differs");
  return receipt_id;
}

export function verifyResult(body, operation, source) {
  const receipt = body.evidence_receipt;
  verifyReceipt(receipt);
  const [schema, domain] = RESULT_CONTRACTS[operation];
  assert.equal(receipt.schema, schema);
  assert.equal(receipt.operation.name, operation);
  assert.equal(receipt.request_id, body.request_id, "Receipt must belong to this request");
  assert.equal(receipt.trace_id, body.trace_id, "Receipt must belong to this trace");
  assert.equal(receipt.software.revision, source.source_commit, "Receipt must use the verified local source commit");
  assert.equal(receipt.software.version, source.software_version);
  assert.equal(receipt.result.domain, domain);
  const { evidence_receipt, ...core } = body;
  if (operation !== "evidence.inspect") delete core.evidence_storage;
  assert.equal(receipt.result.sha256, contentDigest(domain, core), "Receipt must bind this complete result core");
}

export function checkToolResult(result, operation, code, source) {
  assert.equal(result.isError === true, code !== undefined);
  const body = result.structuredContent;
  assert(body && typeof body === "object");
  if (code !== undefined && ["catalogue.search", "data.query"].includes(operation)) {
    assert.equal(body.schema, operation === "catalogue.search" ? "gis-ai-go.catalogue-problem.v1" : "gis-ai-go.data-query-reconciliation-problem.v1");
    assert.equal(body.operation, undefined); // This closed problem family has no operation field.
  } else assert.equal(body.operation, operation);
  assert.deepEqual(result.content, [{ type: "text", text: JSON.stringify(body) }], "Plain-text result must be complete");
  if (code !== undefined) assert.equal(body.code, code);
  else verifyResult(body, operation, source);
  return body;
}

export function boundedTransport(fetchImpl = fetch) {
  let requests = 0, bytes = 0;
  const started = Date.now();
  return {
    counts: () => ({ requests, response_bytes: bytes }),
    async fetch(input, init = {}) {
      const url = input instanceof Request ? input.url : String(input);
      assert.equal(url, ENDPOINT, "The demonstration only connects to its fixed loopback MCP endpoint");
      assert(++requests <= 32 && Date.now() - started < 60_000, "Demonstration request/time bound exceeded");
      const response = await fetchImpl(input, {
        ...init, redirect: "error", credentials: "omit",
        signal: AbortSignal.any([AbortSignal.timeout(10_000), ...(init.signal ? [init.signal] : [])]),
      });
      const reader = response.body?.getReader();
      const chunks = [];
      let size = 0;
      try {
        if (reader) for (;;) {
          const item = await reader.read();
          if (item.done) break;
          size += item.value.byteLength; bytes += item.value.byteLength;
          assert(size <= 2_097_152 && bytes <= 4_194_304, "Demonstration response bound exceeded");
          chunks.push(Buffer.from(item.value));
        }
      } finally { if (reader) await reader.cancel(); }
      return new Response(response.body === null ? null : Buffer.concat(chunks), {
        status: response.status, statusText: response.statusText, headers: response.headers,
      });
    },
  };
}

function resourceBody(result, uri) {
  assert.equal(result.contents.length, 1);
  assert.equal(result.contents[0].uri, uri);
  assert.equal(result.contents[0].mimeType, "application/json");
  return JSON.parse(result.contents[0].text);
}

export async function demonstrate(client, source, onPhase = () => {}) {
  assert.match(source.source_commit, /^[0-9a-f]{40}$/u);
  onPhase("discover-tools-and-resources");
  const tools = await client.listTools();
  assert.deepEqual(tools.tools.map(({ name }) => name).sort(), [...OPERATIONS].sort());
  const resources = await client.listResources();
  const templates = await client.listResourceTemplates();
  assert.deepEqual([...resources.resources, ...templates.resourceTemplates].map(({ name }) => name).sort(), [...RESOURCES].sort());
  const catalogueUri = "gis-ai-go://catalogue/public";
  assert(Array.isArray(resourceBody(await client.readResource({ uri: catalogueUri }), catalogueUri).records));
  const recordUri = "gis-ai-go://catalogue/records/PV-ONS-DATA";
  assert.equal(resourceBody(await client.readResource({ uri: recordUri }), recordUri).id, "PV-ONS-DATA");
  const results = [];
  const call = async (name, args, code) => {
    onPhase(code ? `${name}:${code}` : name);
    const result = checkToolResult(await client.callTool({ name, arguments: args }), name, code, source);
    if (code === undefined) results.push(result);
    return result;
  };
  const search = await call("catalogue.search", { query: "ONS Data API", facets: { types: ["provider"] }, limit: 1 });
  assert.equal(search.data.records[0].id, "PV-ONS-DATA");
  assert.equal((await call("catalogue.describe", { record_id: "PV-ONS-DATA" })).data.record.id, "PV-ONS-DATA");
  const selection = {
    question: "Weekly deaths for England in week 24 of 2026, all causes",
    candidate_record_ids: ["PV-ONS-DATA"],
    constraints: {
      profile_ids: ["PV-ONS-DATA"], provider_ids: ["ons-data-api"],
      dataset_ids: ["weekly-deaths-region"], editions: ["time-series"], versions: ["121"],
      dimensions: { time: ["2026"], geography: ["E92000001"], week: ["week-24"], causeofdeath: ["all-causes"] },
    },
  };
  const plan = (await call("selection.resolve", selection)).data.plan;
  assert.deepEqual(plan.data_query, {
    schema: "gis-ai-go.data-query-parameters.v1",
    resource_id: "gis-ai-go:public-read-resource:sha256:c7130712a40d75e71bcf0259792404389bea2e549adf6733f34d491f83e99f68",
    dataset: { id: "weekly-deaths-region", edition: "time-series", version: "121" },
    selections: [{ dimension: "time", option: "2026" }, { dimension: "geography", option: "E92000001" },
      { dimension: "week", option: "week-24" }, { dimension: "causeofdeath", option: "all-causes" }],
    limit: 1,
  });
  // A fresh transport key permits repeat demonstrations; the selected data is fixed.
  const query = { schema: "gis-ai-go.data-query-request.v1", idempotency_key: `gis-ai-go:ik:v1:${randomBytes(32).toString("hex")}`,
    parameters: plan.data_query };
  const data = await call("data.query", query);
  assert.equal(data.data.observations.length, 1);
  assert.equal(data.data.observations[0].value, "10471");
  assert.equal(data.data.cache.status, "approved-current");
  assert.equal(data.data.cache.stale_after, "2027-02-20T20:21:08.947Z");
  assert(data.warnings.some((warning) => /approved cache/u.test(warning)));
  assert(data.evidence_receipt.transformations.some(({ name }) => name === "read-approved-provider-cache"));
  const receiptId = data.evidence_receipt.receipt_id;
  const inspection = await call("evidence.inspect", { receipt_id: receiptId });
  assert.deepEqual(inspection.data.record.receipt, data.evidence_receipt);
  const evidenceUri = `gis-ai-go://evidence/receipts/${encodeURIComponent(receiptId)}`;
  const resource = resourceBody(await client.readResource({ uri: evidenceUri }), evidenceUri);
  assert.deepEqual(resource.data.record.receipt, data.evidence_receipt);
  const distinct = new Set(results.map(({ evidence_receipt }) => evidence_receipt.receipt_id));
  assert.equal(distinct.size, 5);
  const missing = structuredClone(selection);
  delete missing.constraints.dimensions.week;
  await call("selection.resolve", missing, "missing_dimension");
  await call("catalogue.search", { query: "ONS", arbitrary_url: "https://example.invalid/" }, "invalid_request");
  await call("data.query", query, "idempotency_completed");
  return {
    schema: "gis-ai-go.local214-demo-observation.v1", edition: "v0.2.0-local.1",
    source_commit: source.source_commit, source_tree: source.source_tree, software_version: source.software_version,
    outcome: "passed", endpoint: ENDPOINT, tools: OPERATIONS, resource_classes: RESOURCES,
    result: { value: "10471", source: "approved-cache", live: false,
      period: "2026 week 24", geography: "E92000001", retrieved_at: data.data.cache.retrieved_at,
      stale_after: data.data.cache.stale_after },
    receipt_checks: { distinct_current_call_receipts: 5, content_identities_verified: true,
      current_result_digests_verified: true, verified_source_revision: true,
      complete_plain_text: true, query_inspection_and_resource_linked: true },
    // Retain the permitted returned data and receipts before orderly stop removes session state.
    checked_results: results,
    negative_cases: ["missing_dimension", "invalid_request", "idempotency_completed"],
    boundary: { external_ai_observed: false, provider_egress_independently_measured: false,
      process_cleanup_verified: false, supported_public_release: false },
  };
}

async function sourceIdentity() {
  let identity;
  if (existsSync(join(ROOT, "local214-source-identity.json"))) {
    identity = JSON.parse(execFileSync("uv", ["run", "--locked", "--no-sync", "--cache-dir", ".uv-cache",
      "python", "-m", "scripts.local214_package", "verify"], {
      cwd: ROOT, encoding: "utf8", timeout: 30_000, maxBuffer: 1_048_576,
    }));
  } else {
    const git = (...args) => execFileSync("git", args, { cwd: ROOT, encoding: "utf8", timeout: 10_000, maxBuffer: 1_048_576 }).trim();
    assert.equal(git("status", "--porcelain", "--untracked-files=all"), "", "Commit and verify source before retaining a local-edition observation");
    identity = { source_commit: git("rev-parse", "HEAD"), source_tree: git("rev-parse", "HEAD^{tree}") };
  }
  return { source_commit: identity.source_commit, source_tree: identity.source_tree,
    software_version: JSON.parse(await readFile(join(ROOT, "package.json"), "utf8")).version };
}

async function main() {
  let phase = "check-command-and-pinned-sdk";
  try {
  assert.equal(process.argv.length, 2, "Use node scripts/local214_demo.mjs; start the maintained local candidate first");
  phase = "verify-clean-source-identity";
  const source = await sourceIdentity();
  phase = "load-pinned-sdk";
  const require = createRequire(join(ROOT, "apps/mcp-gateway/package.json"));
  const sdkPath = require.resolve("@modelcontextprotocol/client");
  let directory = dirname(sdkPath), sdk;
  while (directory !== dirname(directory)) {
    try {
      const candidate = JSON.parse(await readFile(join(directory, "package.json"), "utf8"));
      if (candidate.name === "@modelcontextprotocol/client") { sdk = candidate; break; }
    } catch (error) { if (error.code !== "ENOENT") throw error; }
    directory = dirname(directory);
  }
  assert.equal(sdk?.version, "2.0.0", "Use the repository's installed pinned MCP SDK");
  const { Client, StreamableHTTPClientTransport } = await import(pathToFileURL(sdkPath).href);
  const transport = boundedTransport();
  const client = new Client({ name: "gis-ai-go-local214-demonstration", version: "0.2.0-local.1" }, {
    capabilities: {}, versionNegotiation: { mode: { pin: PROTOCOL } },
  });
  try {
    phase = "connect-fixed-loopback-endpoint";
    await client.connect(new StreamableHTTPClientTransport(new URL(ENDPOINT), { fetch: transport.fetch }));
    assert.equal(client.getNegotiatedProtocolVersion(), PROTOCOL);
    const observation = await demonstrate(client, source, (value) => { phase = value; });
    phase = "recheck-source-identity";
    assert.deepEqual(await sourceIdentity(), source);
    phase = "close-client";
    await client.close();
    console.log(JSON.stringify({ ...observation, client: { name: sdk.name, version: sdk.version, protocol: PROTOCOL },
      transport: transport.counts() }, null, 2));
  } finally { await client.close(); }
  } catch (error) {
    const code = typeof error.code === "string" && /^[A-Z0-9_]{1,40}$/u.test(error.code) ? error.code : "CHECK_FAILED";
    console.error(JSON.stringify({ schema: "gis-ai-go.local214-demo-failure.v1", outcome: "failed", phase, code,
      message: "Check the candidate terminal and the documented prerequisites, cache validity and demonstration step. No success is claimed." }));
    process.exitCode = 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
