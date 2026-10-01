#!/usr/bin/env node
/** Bounded, opt-in Sites MCP observations. No provider payload or credentials in reports. */
import { createHash } from "node:crypto";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { performance } from "node:perf_hooks";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const REPORT_SCHEMA = "gis-ai-go.sites-mcp-evaluation-run.v1";
export const SUPPORTED_PROTOCOLS = Object.freeze(["2025-06-18", "2025-11-25", "2026-07-28"]);
const TOOLS = Object.freeze(["sites_capabilities", "sites_os_names", "sites_os_open_product", "sites_ons_cpih", "sites_ons_areas", "sites_evidence_inspect"]);
const RECEIPT = /^sites-pilot:sha256:[0-9a-f]{64}$/u;
const sha = value => createHash("sha256").update(typeof value === "string" || Buffer.isBuffer(value) ? value : JSON.stringify(value)).digest("hex");
const object = value => value !== null && typeof value === "object" && !Array.isArray(value);
const finite = value => typeof value === "number" && Number.isFinite(value);
const check = (condition, code) => { if (!condition) throw new Error(code); };
const SAFE_ERRORS = new Set(["target-rejected", "manifest-rejected", "live-not-authorised", "token-rejected", "request-budget-exhausted", "request-too-large", "response-too-large", "redirect-rejected", "deadline", "streaming-not-admitted", "protocol-mismatch", "tool-list-mismatch", "provider-access-required", "rpc-failure", "http-failure", "invalid-json", "connection-failed"]);
const safeError = error => SAFE_ERRORS.has(error?.message) ? error.message : "connection-failed";
// JCS-compatible serialisation for bounded JSON values: UTF-16 key order and
// ECMAScript number/string serialisation. No provider code or getters are evaluated.
function canonical(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
}

export function validateManifest(value) {
  const fields = ["schema", "origin", "path", "deployment_id", "source_revision", "protocol", "credential_kind", "enabled_case_ids", "maximum_requests", "repeats", "concurrency", "deadline_ms", "allow_live"];
  check(object(value) && Object.keys(value).every(key => fields.includes(key)) && fields.every(key => Object.hasOwn(value, key)), "manifest-rejected");
  let url;
  try { url = new URL(value.origin); } catch { throw new Error("target-rejected"); }
  check(url.protocol === "https:" && url.origin === value.origin && url.pathname === "/" && !url.username && !url.password && !url.port &&
    /^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.chatgpt\.site$/u.test(url.hostname), "target-rejected");
  check(["/pilot/mcp"].includes(value.path), "target-rejected");
  check(value.schema === "gis-ai-go.sites-mcp-evaluation-manifest.v1" && typeof value.deployment_id === "string" && /^[A-Za-z0-9_-]{1,128}$/u.test(value.deployment_id) &&
    /^[0-9a-f]{40}$/u.test(value.source_revision) && SUPPORTED_PROTOCOLS.includes(value.protocol) &&
    ["oauth-access-token", "sites-api-bypass-token"].includes(value.credential_kind) && typeof value.allow_live === "boolean", "manifest-rejected");
  for (const [name, low, high] of [["maximum_requests", 3, 100], ["repeats", 1, 20], ["concurrency", 1, 2], ["deadline_ms", 100, 30000]]) {
    check(Number.isInteger(value[name]) && value[name] >= low && value[name] <= high, "manifest-rejected");
  }
  check(Array.isArray(value.enabled_case_ids) && value.enabled_case_ids.length > 0 && value.enabled_case_ids.length <= 13 &&
    value.enabled_case_ids.every(id => /^Q(?:0[1-9]|1[0-3])$/u.test(id)) && new Set(value.enabled_case_ids).size === value.enabled_case_ids.length, "manifest-rejected");
  return structuredClone(value);
}

function representationsAgree(response) {
  if (!object(response?.structuredContent) || !Array.isArray(response?.content)) return true;
  const texts = response.content.filter(item => item?.type === "text" && typeof item.text === "string");
  if (texts.length !== 1) return false;
  try { return canonical(JSON.parse(texts[0].text)) === canonical(response.structuredContent); }
  catch { return false; }
}
function unwrap(response) {
  if (!representationsAgree(response)) return null;
  if (object(response?.structuredContent)) return response.structuredContent;
  if (Array.isArray(response?.content)) {
    const texts = response.content.filter(item => item?.type === "text" && typeof item.text === "string");
    if (texts.length === 1) { try { return JSON.parse(texts[0].text); } catch { return null; } }
  }
  return object(response) ? response : null;
}
function receiptId(envelope) {
  const id = envelope?.evidence?.receipt_id ?? envelope?.evidence?.receipt?.receipt_id ?? envelope?.data?.receipt_id;
  return typeof id === "string" && RECEIPT.test(id) ? id : null;
}
function findField(value, names, depth = 0) {
  if (!object(value) || depth > 3) return undefined;
  for (const name of names) if (Object.hasOwn(value, name)) return value[name];
  for (const child of Object.values(value)) if (object(child)) { const found = findField(child, names, depth + 1); if (found !== undefined) return found; }
  return undefined;
}

/** Stable assertion interface; accepts structuredContent or one complete JSON text result. */
export function evaluateResult(testCase, response, context = {}) {
  const value = unwrap(response);
  const assertions = [];
  const add = (id, passed) => assertions.push({ id, passed: passed === true });
  add("structured-text-parity", representationsAgree(response));
  const problem = response?.isError === true || value?.schema === "gis-ai-go.sites-pilot-problem.v1";
  if (testCase.assertion === "closed-input-denial") {
    const validationText = response?.content?.some(item => item?.type === "text" && typeof item.text === "string" && /^(?:MCP error -32602: )?Input validation error: Invalid arguments for tool sites_os_names:/u.test(item.text));
    add("closed-input-refused", problem && (["invalid-input", "invalid_input", "INVALID_INPUT", "INVALID_PARAMS"].includes(value?.code ?? value?.error?.code) || validationText === true));
    return { passed: assertions.every(a => a.passed), assertions, receipt_id: null };
  }
  const inspection = testCase.assertion === "receipt-inspection";
  const capability = testCase.assertion === "protected-disabled";
  add("successful-pilot-envelope", !problem && value?.schema === (capability ? "gis-ai-go.sites-pilot-capabilities.v1" : "gis-ai-go.sites-pilot-result.v1") &&
    (inspection ? TOOLS.includes(value.tool) && value.tool !== "sites_evidence_inspect" && value.tool !== "sites_capabilities" : value.tool === testCase.tool) && object(value.data) && object(value.evidence));
  const providerData = value?.data;
  const data = providerData?.schema === "gis-ai-go.sites-pilot-provider-result.v1" ? providerData.data : providerData;
  const id = receiptId(value);
  if (testCase.provider_call || testCase.assertion === "receipt-inspection") add("receipt-reference", id !== null);
  if (testCase.provider_call || inspection) {
    let bound = false;
    try {
      const { receipt_id: suppliedId, ...core } = value.evidence;
      bound = core.schema === "gis-ai-go.sites-pilot-evidence.v1" && core.data_sha256 === sha(canonical(providerData)) &&
        suppliedId === `sites-pilot:sha256:${sha(canonical({ tool: value.tool, ...core }))}`;
    } catch { /* Malformed content is a failed assertion, never a success. */ }
    add("evidence-content-bindings", bound);
  }
  if (testCase.provider_call) {
    if (context.source_revision !== undefined) add("declared-software-revision", value?.evidence?.software_revision === context.source_revision);
    add("query-parameter-binding", value?.evidence?.parameters_sha256 === sha(canonical(testCase.arguments)));
    const expectedProvider = { sites_os_names: "os-names", sites_os_open_product: "os-open-data", sites_ons_cpih: "ons-cpih", sites_ons_areas: "ons-geography" }[testCase.tool];
    add("source-provenance", providerData?.schema === "gis-ai-go.sites-pilot-provider-result.v1" &&
      providerData.provider === expectedProvider && Array.isArray(providerData.requests) && providerData.requests.length > 0);
    add("retrieval-mode-explicit", providerData?.source_mode === "live-provider-response");
    add("source-rights", providerData?.licence === "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" && Array.isArray(providerData.attribution) && providerData.attribution.length > 0);
  }
  if (["os-names", "os-point"].includes(testCase.assertion)) {
    const rows = Array.isArray(data?.candidates) ? data.candidates : Array.isArray(data?.results) ? data.results : Array.isArray(data?.features) ? data.features : [];
    add("bounded-names", rows.length > 0 && rows.length <= testCase.arguments.max_results);
    add("native-name-identities", rows.every(row => typeof findField(row, ["ID", "id", "identifier"]) === "string" && typeof findField(row, ["NAME1", "name", "name1"]) === "string"));
    if (testCase.assertion === "os-point") add("explicit-point-and-crs", rows.length > 0 && rows.every(row => {
      const x = findField(row, ["GEOMETRY_X", "easting", "x"]); const y = findField(row, ["GEOMETRY_Y", "northing", "y"]);
      return finite(x) && finite(y);
    }) && findField(data, ["crs", "srs", "srsName"]) !== undefined);
  } else if (testCase.assertion === "os-product") {
    add("requested-product", findField(data, ["id", "product", "productId"]) === testCase.arguments.product);
    add("release-identity", findField(data, ["version", "release", "downloads"]) !== undefined);
  } else if (testCase.assertion === "cpih-periods") {
    const rows = Array.isArray(data?.observations) ? data.observations : [];
    const periods = rows.map(row => row.period);
    add("exact-period-set", JSON.stringify([...periods].sort()) === JSON.stringify([...testCase.arguments.periods].sort()));
    add("numeric-index-values", rows.every(row => (typeof row.value === "string" && /^\d+(?:\.\d+)?$/u.test(row.value)) || finite(row.value)));
    add("index-unit", /index/iu.test(String(findField(data, ["unit", "units"]) ?? "")) && data?.base_year === 2015);
    add("native-series", findField(data, ["cdid", "series_id"]) === "L522" && findField(data, ["datasetId", "dataset_id"]) === "MM23");
    if (rows.length === 2) {
      const from = Number(rows[0].value), to = Number(rows[1].value), comparison = data.comparison;
      add("index-comparison", object(comparison) && comparison.from_period === rows[0].period && comparison.to_period === rows[1].period &&
        Math.abs(Number(comparison.difference_index_points) - (to - from)) <= 0.00000001 &&
        (from === 0 ? comparison.relative_change_percent === null : Math.abs(Number(comparison.relative_change_percent) - (to - from) / from * 100) <= 0.000001) &&
        comparison.rounding === "half-away-from-zero-to-six-decimal-places");
    }
  } else if (testCase.assertion === "ons-area-names") {
    add("geography-and-vintage", data?.geography === "MSOA" && data.vintage === "2021-12" && data.coverage === "England and Wales");
    add("bounded-area-names", Array.isArray(data?.areas) && data.areas.length > 0 && data.areas.length <= testCase.arguments.max_results &&
      data.areas.every(area => /^[EW][0-9]{8}$/u.test(area.MSOA21CD) && typeof area.MSOA21NM === "string" && area.MSOA21NM.toLowerCase().startsWith(testCase.arguments.name_prefix.toLowerCase())));
    add("lookup-not-containment", data?.selection_basis === "name-prefix-not-spatial-containment");
    add("truncation-explicit", typeof data?.complete === "boolean");
  } else if (testCase.assertion === "receipt-inspection") {
    add("same-receipt", typeof context.expected_receipt_id === "string" && id === context.expected_receipt_id);
  } else if (testCase.assertion === "protected-disabled") {
    const protectedValue = findField(data, ["psga_enabled", "protected_data_enabled", "psga"]);
    add("protected-access-disabled", protectedValue === false || protectedValue?.enabled === false || protectedValue === "disabled" || protectedValue === "disabled-rights-not-established");
  } else add("known-assertion", false);
  return { passed: assertions.every(a => a.passed), assertions, receipt_id: id };
}

export function latencySummary(values) {
  const sorted = values.filter(finite).sort((a, b) => a - b); const n = sorted.length;
  return { count: n, minimum_ms: n ? sorted[0] : null, maximum_ms: n ? sorted[n - 1] : null,
    median_ms: n ? (sorted[Math.floor((n - 1) / 2)] + sorted[Math.floor(n / 2)]) / 2 : null,
    p95_ms: n >= 20 ? sorted[Math.ceil(n * 0.95) - 1] : null };
}

async function sdk() {
  const require = createRequire(resolve(ROOT, "apps/mcp-gateway/package.json"));
  const manifest = JSON.parse(await readFile(resolve(ROOT, "apps/mcp-gateway/node_modules/@modelcontextprotocol/client/package.json"), "utf8"));
  check(manifest.version === "2.0.0", "manifest-rejected");
  return import(pathToFileURL(require.resolve("@modelcontextprotocol/client")).href);
}

export async function runEvaluation(manifestInput, { corpus, token, fetch: suppliedFetch, live = false } = {}) {
  const manifest = validateManifest(manifestInput);
  check(object(corpus) && corpus.schema === "gis-ai-go.sites-mcp-pilot-cases.v1" && Array.isArray(corpus.cases), "manifest-rejected");
  check(typeof token === "string" && token.length >= 32 && token.length <= 4096 && !/[\r\n\s]/u.test(token), "token-rejected");
  if (suppliedFetch === undefined) check(live === true && manifest.allow_live === true, "live-not-authorised");
  const fetcher = suppliedFetch ?? globalThis.fetch;
  const cases = manifest.enabled_case_ids.map(id => corpus.cases.find(item => item.id === id));
  check(cases.every(Boolean), "manifest-rejected");
  const endpoint = manifest.origin + manifest.path;
  const wire = []; const results = [];
  const report = { schema: REPORT_SCHEMA, classification: suppliedFetch ? "injected-transport-test" : "bounded-live-observation",
    started_at: new Date().toISOString(), completed_at: "", manifest, manifest_sha256: sha(manifest), corpus_sha256: sha(corpus),
    harness_sha256: sha(await readFile(fileURLToPath(import.meta.url), "utf8")), client_version: "2.0.0", results, wire,
    preflight: "not-run", completion: "partial", error_code: null, latency: latencySummary([]), latency_by_case: [],
    claims: { independent_host_acceptance: false, oauth_flow_verified: false, public_release_acceptance: false,
      protected_data_authority: false, provider_payloads_retained: false, cost_established: false } };
  let requests = 0; let nextRepeat = 0; let stopped = false;
  const { Client, StreamableHTTPClientTransport } = await sdk();
  async function boundedFetch(input, init) {
    const request = new Request(input, init);
    check(request.url === endpoint && ["POST", "GET", "DELETE"].includes(request.method), "target-rejected");
    check(requests < manifest.maximum_requests, "request-budget-exhausted");
    const sequence = ++requests; const start = performance.now();
    const record = { sequence, method: request.method, status: null, elapsed_ms: 0, server_timing_mcp_ms: null, response_bytes: 0, response_sha256: null, error_code: null };
    wire.push(record);
    const headers = new Headers(request.headers);
    for (const name of ["cookie", "proxy-authorization", "authorization", "oai-sites-authorization", "x-sites-pilot-test-token"]) headers.delete(name);
    if (manifest.credential_kind === "sites-api-bypass-token") {
      headers.set("oai-sites-authorization", `Bearer ${token}`); headers.set("x-sites-pilot-test-token", token);
    } else headers.set("authorization", `Bearer ${token}`);
    const controller = new AbortController();
    const abort = () => controller.abort(); request.signal.addEventListener("abort", abort, { once: true });
    if (request.signal.aborted) controller.abort();
    let timer; let reader;
    try {
      return await Promise.race([(async () => {
        const body = request.method === "GET" || request.method === "DELETE" ? undefined : await request.arrayBuffer();
        check(!body || body.byteLength <= 65536, "request-too-large");
        const response = await fetcher(endpoint, { method: request.method, headers, body, redirect: "error", signal: controller.signal });
        record.status = response.status;
        const timing = /(?:^|,)\s*mcp\s*;\s*dur=([0-9]+(?:\.[0-9]+)?)(?:\s*(?:,|$))/u.exec(response.headers.get("server-timing") ?? "");
        if (timing && Number.isFinite(Number(timing[1]))) record.server_timing_mcp_ms = Number(timing[1]);
        check(!response.redirected && (response.url === "" || response.url === endpoint) && !(response.status >= 300 && response.status < 400), "redirect-rejected");
        check(!/text\/event-stream/iu.test(response.headers.get("content-type") ?? ""), "streaming-not-admitted");
        const chunks = []; let count = 0;
        reader = response.body?.getReader();
        if (reader) while (true) {
          const item = await reader.read(); if (item.done) break;
          count += item.value.byteLength; check(count <= 1048576, "response-too-large"); chunks.push(Buffer.from(item.value));
        }
        const bytes = Buffer.concat(chunks); record.response_bytes = count; record.response_sha256 = sha(bytes);
        return new Response(bytes.length ? bytes : null, { status: response.status, headers: response.headers });
      })(), new Promise((_, reject) => { timer = setTimeout(() => { controller.abort(); reject(new Error("deadline")); }, manifest.deadline_ms); })]);
    } catch (error) { record.error_code = safeError(error); throw new Error(record.error_code); }
    finally { clearTimeout(timer); request.signal.removeEventListener("abort", abort); controller.abort(); void reader?.cancel().catch(() => {}); record.elapsed_ms = Math.round((performance.now() - start) * 1000) / 1000; }
  }
  async function worker() {
    while (!stopped && nextRepeat < manifest.repeats) {
      const repetition = ++nextRepeat;
      const client = new Client({ name: "gis-ai-go-sites-evaluation", version: "1.0.0" }, { capabilities: {}, supportedProtocolVersions: [manifest.protocol],
        versionNegotiation: { mode: manifest.protocol === "2026-07-28" ? { pin: manifest.protocol } : "legacy" } });
      const transport = new StreamableHTTPClientTransport(new URL(endpoint), { fetch: boundedFetch });
      let lastReceipt = null;
      try {
        await client.connect(transport);
        check(client.getNegotiatedProtocolVersion() === manifest.protocol, "protocol-mismatch");
        const listed = await client.listTools();
        check(Array.isArray(listed.tools) && listed.tools.length === TOOLS.length && JSON.stringify(listed.tools.map(tool => tool.name).sort()) === JSON.stringify([...TOOLS].sort()), "tool-list-mismatch");
        report.preflight = "passed";
        for (const item of cases) {
          const row = { case_id: item.id, repetition, stage: item.stage, outcome: "not-admitted", elapsed_ms: null,
            reported_upstream_request_count: null, reported_provider_elapsed_ms: null, reported_provider_response_bytes: null,
            assertions: [], receipt_id: null, error_code: null };
          results.push(row);
          if (item.stage === "conditional") continue;
          if (item.assertion === "receipt-inspection" && lastReceipt === null) { row.outcome = "missing-prerequisite"; continue; }
          const args = structuredClone(item.arguments);
          if (args.receipt_id === "$last_receipt_id") args.receipt_id = lastReceipt;
          const start = performance.now();
          try {
            const response = await client.callTool({ name: item.tool, arguments: args });
            const evaluated = evaluateResult(item, response, { expected_receipt_id: lastReceipt, source_revision: manifest.source_revision });
            row.assertions = evaluated.assertions; row.receipt_id = evaluated.receipt_id; row.outcome = evaluated.passed ? "passed" : "failed";
            const provider = unwrap(response)?.data;
            if (item.provider_call && provider?.schema === "gis-ai-go.sites-pilot-provider-result.v1" && Array.isArray(provider.requests) &&
              Number.isInteger(provider.upstream_request_count) && provider.upstream_request_count >= 1 && provider.upstream_request_count <= 2 &&
              provider.upstream_request_count === provider.requests.length && provider.requests.every(request => finite(request.elapsed_ms) && request.elapsed_ms >= 0 &&
                Number.isInteger(request.response_bytes) && request.response_bytes >= 0 && request.response_bytes <= 1048576)) {
              row.reported_upstream_request_count = provider.upstream_request_count;
              row.reported_provider_elapsed_ms = provider.requests.reduce((sum, request) => sum + request.elapsed_ms, 0);
              row.reported_provider_response_bytes = provider.requests.reduce((sum, request) => sum + request.response_bytes, 0);
            }
            if (evaluated.passed && item.provider_call && evaluated.receipt_id) lastReceipt = evaluated.receipt_id;
          } catch (error) {
            if (item.assertion === "closed-input-denial" && error?.code === -32602) {
              row.outcome = "passed"; row.assertions = [{ id: "closed-input-refused", passed: true }];
            } else { row.outcome = "failed"; row.error_code = safeError(error); }
          }
          row.elapsed_ms = Math.round((performance.now() - start) * 1000) / 1000;
          if (requests >= manifest.maximum_requests) { stopped = true; break; }
        }
      } catch (error) { stopped = true; report.preflight = "failed"; report.error_code = safeError(error); }
      finally { await client.close().catch(() => {}); }
    }
  }
  await Promise.all(Array.from({ length: Math.min(manifest.concurrency, manifest.repeats) }, worker));
  report.completed_at = new Date().toISOString();
  report.completion = results.length === manifest.repeats * cases.length ? "complete" : "partial";
  if (report.completion === "partial" && requests >= manifest.maximum_requests) report.error_code = "request-budget-exhausted";
  report.latency = latencySummary(results.filter(row => row.outcome === "passed").map(row => row.elapsed_ms));
  report.latency_by_case = cases.map(item => ({ case_id: item.id, ...latencySummary(results.filter(row => row.case_id === item.id && row.outcome === "passed").map(row => row.elapsed_ms)) }));
  return report;
}

async function main(args) {
  const options = {};
  for (let index = 0; index < args.length; index++) {
    const arg = args[index];
    if (arg === "--live") { check(!options.live, "manifest-rejected"); options.live = true; continue; }
    check(["--manifest", "--token-env", "--output"].includes(arg) && args[index + 1] && !options[arg], "manifest-rejected"); options[arg] = args[++index];
  }
  check(options.live === true && options["--manifest"] && options["--output"] && /^[A-Z][A-Z0-9_]{2,100}$/u.test(options["--token-env"] ?? ""), "live-not-authorised");
  const manifest = JSON.parse(await readFile(options["--manifest"], "utf8"));
  const corpus = JSON.parse(await readFile(resolve(ROOT, "evaluation/sites-mcp-pilot-cases.v1.json"), "utf8"));
  const directory = resolve(options["--output"]); process.umask(0o077);
  await mkdir(directory, { mode: 0o700 });
  const result = await runEvaluation(manifest, { corpus, token: process.env[options["--token-env"]], live: true });
  await writeFile(resolve(directory, "run.json"), JSON.stringify(result, null, 2) + "\n", { flag: "wx", mode: 0o600 });
  process.stdout.write(JSON.stringify({ report: resolve(directory, "run.json"), preflight: result.preflight, observed_cases: result.results.length, wire_requests: result.wire.length }) + "\n");
  if (result.preflight !== "passed" || result.completion !== "complete" || result.results.some(row => ["failed", "missing-prerequisite"].includes(row.outcome))) process.exitCode = 1;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main(process.argv.slice(2)).catch(() => { process.stderr.write("Sites evaluation failed; check the manifest, private output directory and named credential environment variable.\n"); process.exitCode = 1; });
