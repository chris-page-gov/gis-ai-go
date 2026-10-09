#!/usr/bin/env node
/** Independent pinned SDK probe. Tokens remain in process memory, never argv or output. */
import { createHash, randomBytes } from "node:crypto";
import { createRequire } from "node:module";
import { readFile, writeFile, mkdir, rename } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const sha = (value) => createHash("sha256").update(JSON.stringify(value)).digest("hex");
function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  return value;
}
const recordDigest = (value) => sha(canonical(value));
async function jsonFile(path) { return JSON.parse(await readFile(path, "utf8")); }
async function save(path, value) {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  await writeFile(path + ".tmp", JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  await rename(path + ".tmp", path);
}
const options = {};
for (let i = 2; i < process.argv.length; i += 2) {
  const key = process.argv[i];
  if (!["--input", "--output"].includes(key) || !process.argv[i + 1]) throw Error("Invalid probe arguments");
  options[key.slice(2)] = process.argv[i + 1];
}
if (!options.input || !options.output) throw Error("--input and --output required");
const input = await jsonFile(options.input);
if (["transport-token-validation", "application-identity-validation"].includes(input.mode)) {
  let valid = false; let hasGrantedRoles = false;
  try {
    const { createGcpJwtVerifier } = await import(pathToFileURL(resolve(ROOT, "apps/mcp-gateway/dist/src/gcp-identity.js")).href);
    const transport = input.mode === "transport-token-validation";
    const token = process.env[transport ? "GIS_GCP_TRANSPORT_TOKEN" : "GIS_GCP_FORBIDDEN_IDENTITY_TOKEN"];
    if (!token || (transport && !/^\d{10,32}$/u.test(input.expected_subject ?? "")) ||
        (!transport && input.identity?.mode !== "oidc")) throw Error("Missing verified identity binding");
    const config = transport ? { issuer: "https://accounts.google.com", audience: input.audience,
      jwksUri: "https://www.googleapis.com/oauth2/v3/certs" } : input.identity;
    const claims = await createGcpJwtVerifier().verify(token, config);
    if (transport) valid = claims.sub === input.expected_subject;
    else {
      const groups = claims[config.groupClaim ?? "groups"];
      if (groups !== undefined && (!Array.isArray(groups) || groups.length > 128 || groups.some((group) => typeof group !== "string"))) throw Error("Invalid signed attributes");
      const roles = new Set(config.subjectRoles?.[claims.sub] ?? []);
      for (const group of groups ?? []) for (const role of config.groupRoles?.[group] ?? []) roles.add(role);
      hasGrantedRoles = roles.size !== 0;
      valid = true;
    }
  } catch {}
  await save(options.output, { schema: "gis-ai-go.gcp-signed-identity-observation.v1", valid,
    has_granted_roles: hasGrantedRoles, signature_verification: valid ? "PASS" : "BLOCKED", values_logged: false });
  process.exit(valid ? 0 : 2);
}
const observations = {};
const fail = (name, reason) => { observations[name] = { status: "BLOCKED", reason }; };
const pass = (name, details = {}) => { observations[name] = { status: "PASS", ...details }; };
const tokens = {
  allowed: process.env.GIS_GCP_ALLOWED_IDENTITY_TOKEN,
  forbidden: process.env.GIS_GCP_FORBIDDEN_IDENTITY_TOKEN,
  reader: process.env.GIS_GCP_READER_IDENTITY_TOKEN,
};
let sdk, validatedResult, protocol;
const clients = [];
async function connect(token) {
  const client = new sdk.Client({ name: "gis-ai-go-gcp-independent-acceptance", version: "1.0.0" }, {
    capabilities: {}, versionNegotiation: { mode: { pin: protocol } },
  });
  clients.push(client);
  const boundedFetch = async (value, init) => {
    const req = new Request(value, init);
    const target = new URL(req.url);
    if (target.origin !== new URL(input.endpoint).origin || target.pathname !== "/mcp") throw Error("SDK escaped fixed MCP target");
    const headers = new Headers(req.headers);
    if (token) headers.set("authorization", "Bearer " + token);
    const signals = [AbortSignal.timeout(15_000), ...(req.signal ? [req.signal] : [])];
    const response = await fetch(new Request(req, { headers, signal: AbortSignal.any(signals), redirect: "error" }));
    const length = Number(response.headers.get("content-length") ?? 0);
    if (length > 1_100_000) throw Error("MCP response limit exceeded");
    // Stream consumption is bounded before the SDK parses untrusted response text.
    const reader = response.body?.getReader();
    if (!reader) return response;
    let size = 0; const chunks = [];
    for (;;) { const part = await reader.read(); if (part.done) break; size += part.value.byteLength;
      if (size > 1_100_000) { await reader.cancel(); throw Error("MCP response limit exceeded"); } chunks.push(part.value); }
    return new Response(Buffer.concat(chunks), { status: response.status, headers: response.headers });
  };
  await client.connect(new sdk.StreamableHTTPClientTransport(new URL(input.endpoint), { fetch: boundedFetch }));
  if (client.getProtocolEra() !== "modern" || client.getNegotiatedProtocolVersion() !== protocol) throw Error("Unexpected protocol negotiation");
  return client;
}
function value(result) {
  if (result.isError || result.content?.length !== 1 || result.content[0]?.type !== "text" ||
      recordDigest(JSON.parse(result.content[0].text)) !== recordDigest(result.structuredContent)) throw Error("Invalid tool envelope");
  return result.structuredContent;
}
async function call(client, name, args) { return value(await client.callTool({ name, arguments: args })); }
async function denied(client, name, args) {
  try {
    const result = await client.callTool({ name, arguments: args });
    return result.isError === true && result.structuredContent?.code === "unavailable";
  } catch (error) {
    // An HTTP error or broken route is not a policy refusal. Only a parsed MCP
    // unknown-method/tool refusal counts, using otherwise valid tool arguments.
    return [-32601, -32602].includes(error?.code);
  }
}
try {
  const req = createRequire(resolve(ROOT, "apps/mcp-gateway/package.json"));
  sdk = await import(pathToFileURL(req.resolve("@modelcontextprotocol/client")).href);
  const gateway = resolve(ROOT, "apps/mcp-gateway/dist/src");
  ({ validateWeb216HostedCpihMcpResult: validatedResult } = await import(pathToFileURL(resolve(gateway, "web216-hosted-cpih-mcp.js")).href));
  ({ MCP_PROTOCOL_VERSION: protocol } = await import(pathToFileURL(resolve(gateway, "mcp-constants.js")).href));
  const client = await connect(tokens.allowed);
  pass("negotiation", { client: "@modelcontextprotocol/client@2.0.0", protocol, era: client.getProtocolEra(), wire_model: "modern SDK negotiation (server/discover); not a legacy initialize claim" });
  const tools = (await client.listTools()).tools.map(({ name }) => name).sort();
  pass("discovery", { tools });
  const selected = await call(client, "web216_cpih_select", { period: "2026-07" });
  if (selected.authority?.grants_execution !== false || !selected.plan_id) throw Error("Invalid captured-data selection");
  pass("selection", { plan_id: selected.plan_id, live_provider: false });
  const described = [];
  for (const expected of input.known_records ?? []) {
    const result = await call(client, "okf_describe", { bundle: expected.bundle, id: expected.id });
    const id = result.record?.id ?? result.record?.["@id"];
    if (result.bundle !== expected.bundle || id !== expected.id || result.provenance?.release_sha256 !== input.release_id) throw Error("Hosted metadata release mismatch");
    described.push({ bundle: expected.bundle, id, record_sha256: recordDigest(result.record),
      rights_present: Object.hasOwn(result.record, "rights"), source_citations_present: Array.isArray(result.record.sources) && result.record.sources.length > 0,
      temporal_present: Object.hasOwn(result.record, "temporal") || Object.hasOwn(result.record, "freshness") });
  }
  if (described.length === 2 && new Set(described.map((row) => row.bundle)).size === 2) pass("both_bundles", { records: described });
  else fail("both_bundles", "Prepared known-record inventory unavailable; no corpus inferred from homepage");
  if (tokens.reader) {
    const reader = await connect(tokens.reader);
    const readerTools = (await reader.listTools()).tools.map(({ name }) => name).sort();
    const excluded = ["web216_cpih_query", "web216_cpih_inspect", "okf_export"];
    if (excluded.some((name) => readerTools.includes(name)) || !readerTools.includes("okf_describe")) observations.reader_discovery = { status: "FAIL", reason: "Supplied reader identity does not have the reviewed viewer toolset" };
    else {
      pass("reader_discovery", { tools: readerTools });
      const key = "gis-ai-go:ik:v1:" + "0".repeat(64);
      const outcomes = await Promise.all(excluded.map(async (name) => [name, await denied(reader, name,
        name === "okf_export" ? {} : name === "web216_cpih_query"
          ? { period: "2026-07", selection_plan_id: selected.plan_id, idempotency_key: key } : { idempotency_key: key })]));
      // Confirm the route still works, so a disconnected client cannot pass the refusals.
      await call(reader, "web216_cpih_select", { period: "2026-07" });
      if (outcomes.every(([, refusal]) => refusal)) pass("reader_direct_refusal", { tools: excluded });
      else observations.reader_direct_refusal = { status: "FAIL", reason: "A forbidden direct tool call succeeded" };
    }
  } else fail("reader_discovery", "GIS_GCP_READER_IDENTITY_TOKEN binding absent; real role comparison unavailable");
  let malformed = false;
  try { malformed = (await client.callTool({ name: "web216_cpih_select", arguments: { period: "2026-07", role: "owner" } })).isError === true; }
  catch (error) { malformed = [-32601, -32602].includes(error?.code); }
  await call(client, "web216_cpih_select", { period: "2026-07" });
  observations.malformed_input = { status: malformed ? "PASS" : "FAIL", reason: "Closed selection schema rejects an extra self-asserted role" };
  const priorPath = resolve(dirname(options.output), "mcp-persistence-anchor.json");
  let prior;
  try { prior = await jsonFile(priorPath); } catch {}
  if (prior) {
    const restored = await call(client, "web216_cpih_inspect", { receipt_id: prior.receipt_id });
    if (!await validatedResult(restored) || recordDigest(restored.evidence.record) !== prior.record_sha256) observations.persisted_receipt = { status: "FAIL", reason: "Previously observed receipt changed or is unavailable" };
    else if (input.observed_revision && input.observed_revision !== prior.observed_revision && input.single_current_revision_verified &&
        prior.single_current_revision_verified === true && prior.observed_revision) {
      pass("persisted_receipt", { prior_revision: prior.observed_revision, observed_revision: input.observed_revision, receipt_id: prior.receipt_id, record_sha256: prior.record_sha256 });
    } else fail("persisted_receipt", "Receipt inspection succeeded; actual sole-serving revision replacement has not been observed");
  }
  if (!input.evidence_writes_authorised) fail("evidence", "Approval scope does not include bounded verification evidence writes; no query issued");
  else {
    const key = prior?.idempotency_key ?? "gis-ai-go:ik:v1:" + randomBytes(32).toString("hex");
    const proposal = { period: "2026-07", selection_plan_id: selected.plan_id, idempotency_key: key };
    const other = await connect(tokens.allowed);
    const concurrent = await Promise.allSettled([call(client, "web216_cpih_query", proposal), call(other, "web216_cpih_query", proposal)]);
    const successful = concurrent.filter((result) => result.status === "fulfilled").map((result) => result.value);
    if (!successful.length || !await validatedResult(successful[0])) throw Error("No valid durable evidence returned");
    const first = successful[0];
    const replay = await call(client, "web216_cpih_query", proposal);
    const inspection = await call(other, "web216_cpih_inspect", { receipt_id: first.evidence.receipt.receipt_id });
    if (!await validatedResult(replay) || !await validatedResult(inspection) ||
        recordDigest(replay.evidence.record) !== recordDigest(first.evidence.record) || recordDigest(inspection.evidence.record) !== recordDigest(first.evidence.record) ||
        successful.some((result) => recordDigest(result.evidence.record) !== recordDigest(first.evidence.record))) throw Error("Duplicate/replay evidence identity differs");
    pass("evidence", { receipt_id: first.evidence.receipt.receipt_id, record_sha256: recordDigest(first.evidence.record), result_origin: "pinned-capture-not-live-provider", inspection_from_separate_sdk_client: true });
    const january = await call(client, "web216_cpih_select", { period: "2026-01" });
    const conflict = await client.callTool({ name: "web216_cpih_query", arguments: { ...proposal, period: "2026-01", selection_plan_id: january.plan_id } });
    if (conflict.isError !== true || conflict.structuredContent?.code !== "conflict") throw Error("Conflicting request fingerprint was not refused");
    pass("concurrent_idempotency", { successful_initial_responses: successful.length, calls: 2, fingerprint_conflict_refused: true, principal_ownership: "separate-real-principal-test-still-required" });
    if (!prior) await save(priorPath, { schema: "gis-ai-go.gcp-verification-anchor.v1", observed_at: new Date().toISOString(),
      observed_revision: input.observed_revision ?? null, single_current_revision_verified: input.single_current_revision_verified === true,
      release_id: input.release_id, idempotency_key: key,
      receipt_id: first.evidence.receipt.receipt_id, record_sha256: recordDigest(first.evidence.record) });
    observations.anchor = { status: "PASS", path: priorPath, revision_replacement_proved: false };
  }
} catch {
  // SDK/HTTP errors may contain credentials or untrusted record strings. Preserve only bounded diagnostic classes.
  fail("probe_incomplete", "Independent hosted MCP probe could not complete; check private route, signed identity, principal provisioning and exact release");
} finally {
  await Promise.allSettled(clients.map((client) => client.close()));
}
await save(options.output, { schema: "gis-ai-go.gcp-sdk-observations.v1", observed_at: new Date().toISOString(), local_mock: false, observations });
console.log(JSON.stringify({ status: observations.probe_incomplete ? "BLOCKED" : "OBSERVED", output: options.output }));
process.exitCode = observations.probe_incomplete ? 2 : 0;
