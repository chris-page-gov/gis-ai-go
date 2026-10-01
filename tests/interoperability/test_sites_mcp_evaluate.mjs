import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { evaluateResult, latencySummary, runEvaluation, validateManifest } from "../../scripts/sites_mcp_evaluate.mjs";

const corpus = JSON.parse(await readFile(new URL("../../evaluation/sites-mcp-pilot-cases.v1.json", import.meta.url), "utf8"));
const secret = "synthetic-test-token-never-report-this";
const names = ["sites_capabilities", "sites_os_names", "sites_os_open_product", "sites_ons_cpih", "sites_ons_areas", "sites_evidence_inspect"];
const manifest = (changes = {}) => ({ schema: "gis-ai-go.sites-mcp-evaluation-manifest.v1", origin: "https://gis-pilot.example.chatgpt.site", path: "/pilot/mcp",
  deployment_id: "synthetic-deployment", source_revision: "a".repeat(40), protocol: "2025-06-18", credential_kind: "sites-api-bypass-token",
  enabled_case_ids: ["Q04", "Q10", "Q11", "Q12", "Q06"], maximum_requests: 20, repeats: 1, concurrency: 1, deadline_ms: 1000, allow_live: false, ...changes });
const canonical = value => value === null || typeof value !== "object" ? JSON.stringify(value) : Array.isArray(value) ? `[${value.map(canonical).join(",")}]` : `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
const hash = value => createHash("sha256").update(canonical(value)).digest("hex");
const envelope = (tool, data, args = tool === "sites_os_open_product" ? { product: "OpenNames" } : { query: "Warwick", max_results: 1 }) => {
  const payload = { schema: "gis-ai-go.sites-pilot-provider-result.v1", provider: tool === "sites_ons_cpih" ? "ons-cpih" : tool === "sites_ons_areas" ? "ons-geography" : tool === "sites_os_names" ? "os-names" : "os-open-data", source_mode: "live-provider-response", requests: [{ elapsed_ms: 2, response_bytes: 100 }], upstream_request_count: 1, licence: "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/", attribution: ["Synthetic test attribution"], data };
  const core = { schema: "gis-ai-go.sites-pilot-evidence.v1", software_revision: "a".repeat(40), parameters_sha256: hash(args), data_sha256: hash(payload) };
  return { schema: "gis-ai-go.sites-pilot-result.v1", tool, data: payload, evidence: { ...core, receipt_id: `sites-pilot:sha256:${hash({ tool, ...core })}` } };
};
const cpih = periods => envelope("sites_ons_cpih", { cdid: "L522", datasetId: "MM23", unit: "index (2015=100)", base_year: 2015,
  observations: periods.map(period => ({ period, value: "142.7" })), comparison: periods.length === 2 ? { from_period: periods[0], to_period: periods[1],
    difference_index_points: "0", relative_change_percent: "0", rounding: "half-away-from-zero-to-six-decimal-places" } : null }, { periods });
const result = value => ({ content: [{ type: "text", text: JSON.stringify(value) }], structuredContent: value });

function fakeProvider(observed, options = {}) {
  return async (url, init) => {
    assert.equal(url, manifest().origin + "/pilot/mcp");
    assert.equal(init.redirect, "error");
    assert.equal(init.headers.get("oai-sites-authorization"), `Bearer ${secret}`);
    assert.equal(init.headers.get("x-sites-pilot-test-token"), secret);
    if (init.method !== "POST") return new Response(null, { status: 405 });
    const request = JSON.parse(Buffer.from(init.body).toString("utf8"));
    observed.push(request);
    if (request.method === "notifications/initialized") return new Response(null, { status: 202 });
    let response;
    if (request.method === "initialize") response = { protocolVersion: request.params.protocolVersion, capabilities: { tools: {} }, serverInfo: { name: "fixture", version: "1" } };
    else if (request.method === "server/discover") response = { supportedVersions: ["2026-07-28"], capabilities: { tools: {} }, ttlMs: 0, cacheScope: "private" };
    else if (request.method === "tools/list") response = { tools: (options.tools ?? names).map(name => ({ name, inputSchema: { type: "object" } })), ttlMs: 0, cacheScope: "private" };
    else if (request.method === "tools/call") {
      const { name, arguments: args } = request.params;
      if (name === "sites_ons_cpih") response = result(cpih(args.periods));
      else if (name === "sites_evidence_inspect") { assert.equal(args.receipt_id, cpih(["2026-07"]).evidence.receipt_id); response = result(cpih(["2026-07"])); }
      else if (name === "sites_capabilities") response = result({ schema: "gis-ai-go.sites-pilot-capabilities.v1", tool: name, data: { providers: { psga: "disabled-rights-not-established" } }, evidence: {} });
      else if (name === "sites_os_names" && args.psga_entitled) response = { ...result({ schema: "gis-ai-go.sites-pilot-problem.v1", code: "invalid-input" }), isError: true };
      else throw Error("Unexpected fixture call");
      if (options.mismatchText === true) response.content = [{ type: "text", text: JSON.stringify({ conflicting_text: secret }) }];
    } else throw Error("Unexpected protocol method");
    return new Response(JSON.stringify({ jsonrpc: "2.0", id: request.id, result: { resultType: "complete", ...response } }), { headers: { "content-type": "application/json" } });
  };
}

test("target and manifest reject authority drift, credentials in URL and expanded budgets", () => {
  assert.equal(validateManifest(manifest()).path, "/pilot/mcp");
  for (const change of [{ origin: "https://localhost" }, { origin: "https://u:p@gis-pilot.example.chatgpt.site" }, { origin: "https://gis-pilot.example.chatgpt.site:8443" },
    { origin: "https://gis-pilot.example.chatgpt.site/" }, { origin: "https://gis-pilot.example.chatgpt.site.evil.test" }, { path: "/mcp?key=secret" },
    { maximum_requests: 101 }, { concurrency: 3 }, { allow_live: "yes" }, { extra: true }, { enabled_case_ids: ["Q04", "Q04"] }]) assert.throws(() => validateManifest(manifest(change)));
});

test("assertions distinguish valid CPIH, period mismatch, percentages and absent lineage", () => {
  const question = corpus.cases.find(item => item.id === "Q04");
  assert.equal(evaluateResult(question, result(cpih(["2026-07"]))).passed, true);
  for (const broken of [cpih(["2026-01"]), { ...cpih(["2026-07"]), evidence: {} }, { ...cpih(["2026-07"]), data: { ...cpih(["2026-07"]).data, data: { ...cpih(["2026-07"]).data.data, unit: "percent" } } }]) {
    assert.equal(evaluateResult(question, result(broken)).passed, false);
  }
  assert.equal(evaluateResult(question, { content: [{ type: "text", text: "not JSON" }] }).passed, false);
});

test("named-place and product assertions require native identities, bounds and CRS", () => {
  const q = id => corpus.cases.find(item => item.id === id);
  const value = envelope("sites_os_names", { crs: "EPSG:27700", results: [{ ID: "osgb-test", NAME1: "Warwick", GEOMETRY_X: 428119, GEOMETRY_Y: 265114 }] });
  assert.equal(evaluateResult(q("Q02"), result(value)).passed, true);
  assert.equal(evaluateResult(q("Q02"), result({ ...value, data: { ...value.data, data: { ...value.data.data, crs: undefined } } })).passed, false);
  assert.equal(evaluateResult(q("Q03"), result(envelope("sites_os_open_product", { id: "OpenNames", version: "2026-07" }))).passed, true);
  assert.equal(evaluateResult(q("Q03"), result(envelope("sites_os_open_product", { id: "OpenUPRN", version: "2026-07" }))).passed, false);
});

test("ONS area names retain geography vintage and lookup/truncation boundaries", () => {
  const question = corpus.cases.find(item => item.id === "Q13");
  const data = { geography: "MSOA", vintage: "2021-12", coverage: "England and Wales", areas: [{ MSOA21CD: "E02000001", MSOA21NM: "Warwick 001" }], complete: false, selection_basis: "name-prefix-not-spatial-containment" };
  assert.equal(evaluateResult(question, result(envelope(question.tool, data, question.arguments))).passed, true);
  for (const change of [{ vintage: "2011-12" }, { selection_basis: "point-containment" }, { complete: undefined }, { areas: [{ MSOA21CD: "Warwick", MSOA21NM: "Warwick 001" }] }]) {
    assert.equal(evaluateResult(question, result(envelope(question.tool, { ...data, ...change }, question.arguments))).passed, false);
  }
});

test("CPIH comparison rejects a derived value that disagrees with the observations", () => {
  const question = corpus.cases.find(item => item.id === "Q05"); const value = cpih(question.arguments.periods);
  assert.equal(evaluateResult(question, result(value)).passed, true);
  value.data.data.comparison.relative_change_percent = "5";
  const evaluated = evaluateResult(question, result(value));
  assert.equal(evaluated.passed, false);
  assert.equal(evaluated.assertions.find(assertion => assertion.id === "index-comparison").passed, false);
});

test("structured and text representations must agree without relying on JSON key order", () => {
  const question = corpus.cases.find(item => item.id === "Q04"), value = cpih(["2026-07"]);
  const reordered = Object.fromEntries(Object.entries(value).reverse());
  assert.equal(evaluateResult(question, { structuredContent: value, content: [{ type: "text", text: JSON.stringify(reordered, null, 2) }] }).passed, true);
  for (const content of [
    [{ type: "text", text: JSON.stringify({ ...value, tool: "sites_capabilities" }) }],
    [{ type: "text", text: "malformed JSON" }],
    [{ type: "text", text: JSON.stringify(value) }, { type: "text", text: "Unreviewed contradictory explanation" }],
    [],
  ]) {
    const evaluated = evaluateResult(question, { structuredContent: value, content });
    assert.equal(evaluated.passed, false);
    assert.equal(evaluated.assertions.find(assertion => assertion.id === "structured-text-parity").passed, false);
    assert.equal(evaluated.receipt_id, null);
  }
});

test("wire-level parity failure is retained without leaking conflicting text or credentials", async () => {
  const report = await runEvaluation(manifest({ enabled_case_ids: ["Q04"] }), { corpus, token: secret, fetch: fakeProvider([], { mismatchText: true }) });
  assert.equal(report.preflight, "passed");
  assert.equal(report.results[0].outcome, "failed");
  assert.equal(report.results[0].assertions.find(assertion => assertion.id === "structured-text-parity").passed, false);
  assert.equal(report.results[0].receipt_id, null);
  assert(!JSON.stringify(report).includes(secret));
  assert(!JSON.stringify(report).includes("conflicting_text"));
  assert(!JSON.stringify(report).includes("142.7"));
});

for (const protocol of ["2025-06-18", "2025-11-25", "2026-07-28"]) test(`official client exercises ${protocol} over injected Fetch without network`, async () => {
  const observed = [];
  const report = await runEvaluation(manifest({ protocol }), { corpus, token: secret, fetch: fakeProvider(observed) });
  assert.equal(report.preflight, "passed", JSON.stringify(report));
  assert.equal(report.error_code, null);
  assert.equal(report.results.filter(row => row.outcome === "passed").length, 4, JSON.stringify(report.results));
  assert.equal(report.results.find(row => row.case_id === "Q06").outcome, "not-admitted");
  assert.equal(observed[0].method, protocol === "2026-07-28" ? "server/discover" : "initialize");
  assert.equal(observed.some(item => item.method === "notifications/initialized"), protocol !== "2026-07-28");
  const calls = observed.filter(item => item.method === "tools/call");
  assert.equal(calls.length, 4);
  assert(!JSON.stringify(report).includes(secret));
  assert(!JSON.stringify(report).includes("142.7"));
  assert(!JSON.stringify(report).includes("authorization"));
  assert.equal(report.claims.oauth_flow_verified, false);
  assert.equal(report.classification, "injected-transport-test");
  execFileSync(fileURLToPath(new URL("../../.venv/bin/python", import.meta.url)), ["-c", "import json,sys; from jsonschema import Draft202012Validator,FormatChecker; s=json.load(open('schemas/sites-mcp-evaluation-run.schema.json')); Draft202012Validator.check_schema(s); Draft202012Validator(s,format_checker=FormatChecker()).validate(json.load(sys.stdin))"],
    { cwd: new URL("../../", import.meta.url), input: JSON.stringify(report), stdio: ["pipe", "pipe", "pipe"] });
});

test("live transport is opt-in even with a well-formed manifest and token", async () => {
  await assert.rejects(runEvaluation(manifest(), { corpus, token: secret }), /live-not-authorised/u);
  await assert.rejects(runEvaluation(manifest({ allow_live: true }), { corpus, token: secret }), /live-not-authorised/u);
  await assert.rejects(runEvaluation(manifest(), { corpus, token: "bad\nsecret", fetch: fakeProvider([]) }), /token-rejected/u);
});

test("unexpected advertised tools stop before provider calls", async () => {
  const observed = [];
  const report = await runEvaluation(manifest(), { corpus, token: secret, fetch: fakeProvider(observed, { tools: [...names, "unsafe"] }) });
  assert.equal(report.preflight, "failed"); assert.equal(report.error_code, "tool-list-mismatch");
  assert.equal(observed.some(item => item.method === "tools/call"), false);
});

test("redirect, streaming, excessive bytes and timeout fail closed and minimise errors", async () => {
  for (const [code, fetcher] of [
    ["redirect-rejected", async () => new Response(null, { status: 302, headers: { location: "https://evil.test" } })],
    ["streaming-not-admitted", async () => new Response("data: private", { headers: { "content-type": "text/event-stream" } })],
    ["response-too-large", async () => new Response("x".repeat(1048577))],
    ["deadline", async () => new Promise(() => {})],
  ]) {
    const report = await runEvaluation(manifest({ deadline_ms: 100 }), { corpus, token: secret, fetch: fetcher });
    assert.equal(report.preflight, "failed"); assert(report.wire.some(row => row.error_code === code), JSON.stringify(report));
    assert(!JSON.stringify(report).includes("private"));
  }
});

test("global wire budget holds with two parallel evaluation sequences", async () => {
  const observed = [];
  const report = await runEvaluation(manifest({ repeats: 3, concurrency: 2, maximum_requests: 8 }), { corpus, token: secret, fetch: fakeProvider(observed) });
  assert(report.wire.length <= 8); assert(observed.length <= 8);
  assert.equal(report.completion, "partial");
  assert.equal(report.error_code, "request-budget-exhausted");
});

test("percentile is withheld for small exploratory samples", () => {
  assert.deepEqual(latencySummary([3, 1, 2]), { count: 3, minimum_ms: 1, maximum_ms: 3, median_ms: 2, p95_ms: null });
  assert.equal(latencySummary(Array.from({ length: 20 }, (_, i) => i + 1)).p95_ms, 19);
  assert.equal(latencySummary([]).median_ms, null);
});
