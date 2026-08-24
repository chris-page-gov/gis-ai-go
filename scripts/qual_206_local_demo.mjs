import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import {
  chmodSync,
  existsSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, isAbsolute, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { PUBLIC_ONS_DATA_QUERY_PARAMETERS } from
  "../apps/mcp-gateway/dist/src/data-query-application.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../apps/mcp-gateway/dist/src/mcp-server.js";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const SERVER = fileURLToPath(new URL(
  "../tests/interoperability/fixtures/qual_206_exact_five_stdio_server.mjs",
  import.meta.url,
));
const PROVIDER_EGRESS_GUARD = fileURLToPath(new URL(
  "../tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
  import.meta.url,
));
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUTHORITY_ARGUMENT = "--exact-five-stdio-conformance-only";
const TEMPORARY_ROOT_PREFIX = "gis-ai-go-local-demo-";
const FULL_COMMIT = /^[0-9a-f]{40}$/u;
const RECEIPT_ID = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const PUBLIC_READ_RESOURCE_ID =
  "gis-ai-go:public-read-resource:sha256:" +
  "c7130712a40d75e71bcf0259792404389bea2e549adf6733f34d491f83e99f68";
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const EXACT_RESOURCES = Object.freeze([
  "catalogue.public",
  "catalogue.record",
  "evidence.receipt",
]);
const REQUEST_CONTEXTS = Object.freeze({
  "catalogue.search": Object.freeze({
    requestId: "exact-five-stdio-search-001",
    traceId: "1".repeat(32),
  }),
  "catalogue.describe": Object.freeze({
    requestId: "exact-five-stdio-describe-001",
    traceId: "2".repeat(32),
  }),
  "selection.resolve": Object.freeze({
    requestId: "exact-five-stdio-selection-001",
    traceId: "3".repeat(32),
  }),
  "data.query": Object.freeze({
    requestId: "exact-five-stdio-data-001",
    traceId: "4".repeat(32),
  }),
  "evidence.inspect": Object.freeze({
    requestId: "exact-five-stdio-inspect-001",
    traceId: "5".repeat(32),
  }),
});
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-local-exact-five-demo",
    version: "1.0.0",
  }),
});
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1",
  idempotency_key: `gis-ai-go:ik:v1:${"9".repeat(64)}`,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
});
const SELECTION_REQUEST = Object.freeze({
  question: "Weekly deaths for England in week 24 of 2026, all causes",
  candidate_record_ids: Object.freeze(["PV-ONS-DATA"]),
  constraints: Object.freeze({
    profile_ids: Object.freeze(["PV-ONS-DATA"]),
    provider_ids: Object.freeze(["ons-data-api"]),
    dataset_ids: Object.freeze(["weekly-deaths-region"]),
    editions: Object.freeze(["time-series"]),
    versions: Object.freeze(["121"]),
    dimensions: Object.freeze({
      time: Object.freeze(["2026"]),
      geography: Object.freeze(["E92000001"]),
      week: Object.freeze(["week-24"]),
      causeofdeath: Object.freeze(["all-causes"]),
    }),
  }),
});
const EXPECTED_SELECTION_PLAN = JSON.parse(readFileSync(
  new URL("../providers/fixtures/selection-plan.example.json", import.meta.url),
  "utf8",
));
const EXPECTED_PUBLIC_READ_RESOURCE = JSON.parse(readFileSync(
  new URL("../providers/fixtures/public-read-resource.example.json", import.meta.url),
  "utf8",
));
const EXPECTED_OKF_BUILD_RECEIPT = JSON.parse(readFileSync(
  new URL("../artifacts/okf/build-receipt.json", import.meta.url),
  "utf8",
));
const CONTENT_ROOT = EXPECTED_OKF_BUILD_RECEIPT.contentRootSha256;
if (!/^[0-9a-f]{64}$/u.test(CONTENT_ROOT)) {
  throw new Error("The checked OKF build receipt has an invalid content root");
}

function withTimeout(promise, label, milliseconds = 5_000) {
  let timeout;
  return Promise.race([
    promise,
    new Promise((_resolve, reject) => {
      timeout = setTimeout(
        () => reject(new Error(`Timed out waiting for ${label}`)),
        milliseconds,
      );
    }),
  ]).finally(() => clearTimeout(timeout));
}

function currentSourceState() {
  const commit = execFileSync(
    "git",
    ["-C", ROOT, "rev-parse", "--verify", "HEAD^{commit}"],
    { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] },
  ).trim();
  if (!FULL_COMMIT.test(commit)) {
    throw new Error("The current checkout did not resolve to a full Git commit");
  }
  const changes = execFileSync(
    "git",
    ["-C", ROOT, "status", "--porcelain=v1", "--untracked-files=all"],
    { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] },
  ).trim();
  return Object.freeze({ commit, workingTreeClean: changes.length === 0 });
}

export function isolatedChildEnvironment(sourceCommit, temporaryRoot) {
  if (!FULL_COMMIT.test(sourceCommit)) {
    throw new TypeError("The demo child requires a full lowercase Git commit");
  }
  if (typeof temporaryRoot !== "string" || !isAbsolute(temporaryRoot)) {
    throw new TypeError("The demo child requires an absolute temporary root");
  }
  return {
    [ENABLE_FLAG]: "1",
    [SOURCE_COMMIT_VARIABLE]: sourceCommit,
    TMPDIR: temporaryRoot,
    TMP: temporaryRoot,
    TEMP: temporaryRoot,
  };
}

export function observeChildClose(child) {
  let closeCount = 0;
  let resolveClose;
  const promise = new Promise((resolveValue) => {
    resolveClose = resolveValue;
  });
  child.on("close", (code, signal) => {
    closeCount += 1;
    if (closeCount === 1) resolveClose(Object.freeze({ code, signal }));
  });
  return Object.freeze({
    promise,
    count: () => closeCount,
  });
}

async function closeWithin(closePromise, label, milliseconds) {
  try {
    return await withTimeout(closePromise, label, milliseconds);
  } catch (error) {
    if (error instanceof Error && error.message.startsWith("Timed out waiting for ")) {
      return null;
    }
    throw error;
  }
}

export async function closeChildAndRemoveTemporaryRoot(
  child,
  closeObservation,
  temporaryRoot,
  timings = {},
) {
  const gracefulMilliseconds = timings.gracefulMilliseconds ?? 1_000;
  const terminateMilliseconds = timings.terminateMilliseconds ?? 1_000;
  const killMilliseconds = timings.killMilliseconds ?? 2_000;
  if (child.stdin !== null && !child.stdin.destroyed) child.stdin.end();

  let close = await closeWithin(
    closeObservation.promise,
    "the child to close after EOF",
    gracefulMilliseconds,
  );
  let stage = "graceful-eof";
  if (close === null) {
    child.kill("SIGTERM");
    close = await closeWithin(
      closeObservation.promise,
      "the child to close after SIGTERM",
      terminateMilliseconds,
    );
    stage = "sigterm";
  }
  if (close === null) {
    child.kill("SIGKILL");
    close = await withTimeout(
      closeObservation.promise,
      "the child to close after SIGKILL",
      killMilliseconds,
    );
    stage = "sigkill";
  }
  assert.equal(closeObservation.count(), 1, "The child emitted close more than once");
  const canonicalRoot = realpathSync(temporaryRoot);
  assert.equal(
    dirname(canonicalRoot),
    realpathSync(tmpdir()),
    "Refusing to remove a temporary root outside the operating-system temp directory",
  );
  assert.equal(
    basename(canonicalRoot).startsWith(TEMPORARY_ROOT_PREFIX),
    true,
    "Refusing to remove a temporary root without the local-demo prefix",
  );
  rmSync(temporaryRoot, { recursive: true, force: true });
  assert.equal(existsSync(temporaryRoot), false, "The child temporary root was not removed");
  return Object.freeze({ ...close, stage });
}

function attachJsonLines(stream, label, onValue, onError) {
  let buffer = "";
  stream.setEncoding("utf8");
  stream.on("error", onError);
  stream.on("data", (chunk) => {
    buffer += chunk;
    while (buffer.includes("\n")) {
      const lineEnd = buffer.indexOf("\n");
      const line = buffer.slice(0, lineEnd);
      buffer = buffer.slice(lineEnd + 1);
      if (line.length === 0) continue;
      let value;
      try {
        value = JSON.parse(line);
      } catch (error) {
        onError(new Error(`${label} emitted invalid JSON`, { cause: error }));
        continue;
      }
      try {
        onValue(value);
      } catch (error) {
        onError(error instanceof Error ? error : new Error(`${label} processing failed`));
      }
    }
  });
  return () => buffer;
}

function result(message) {
  assert.equal(message?.jsonrpc, "2.0");
  assert.equal(Object.hasOwn(message, "error"), false, "JSON-RPC result also contained error");
  assert.equal(typeof message.result, "object", JSON.stringify(message));
  assert.notEqual(message.result, null);
  return message.result;
}

function assertToolResult(message, operation, { persisted }) {
  const called = result(message);
  assert.equal(Object.hasOwn(called, "isError"), false, JSON.stringify(called));
  assert.equal(typeof called.structuredContent, "object");
  assert.notEqual(called.structuredContent, null);
  assert.deepEqual(called.content, [{
    type: "text",
    text: JSON.stringify(called.structuredContent),
  }]);
  assert.equal(called.structuredContent.operation, operation);
  const context = REQUEST_CONTEXTS[operation];
  const receipt = called.structuredContent.evidence_receipt;
  assert.equal(called.structuredContent.request_id, context.requestId);
  assert.equal(called.structuredContent.trace_id, context.traceId);
  assert.match(receipt.receipt_id, RECEIPT_ID);
  assert.equal(receipt.operation.name, operation);
  assert.equal(receipt.request_id, context.requestId);
  assert.equal(receipt.trace_id, context.traceId);
  assert.equal(receipt.policy_decision.operation, operation);
  assert.equal(receipt.policy_decision.request_id, context.requestId);
  assert.equal(receipt.policy_decision.trace_id, context.traceId);
  assert.equal(receipt.policy_decision.effect, "allow-with-obligations");
  assert.equal(receipt.policy_decision.policy_default_effect, "deny");
  assert.equal(receipt.verification.status, "passed");
  assert.equal(receipt.verification.digest_algorithm, "sha256");
  if (persisted) {
    assert.equal(called.structuredContent.evidence_storage.status, "persisted");
  } else {
    assert.equal(Object.hasOwn(called.structuredContent, "evidence_storage"), false);
  }
  return called.structuredContent;
}

function assertCatalogueSearch(search, sourceCommit) {
  assert.equal(search.schema, "gis-ai-go.catalogue-result.v1");
  assert.deepEqual(search.warnings, []);
  assert.equal(search.catalogue.content_root_sha256, CONTENT_ROOT);
  assert.equal(search.catalogue.record_count, 36);
  assert.equal(search.catalogue.revision, sourceCommit);
  assert.equal(search.catalogue.version, "0.1.0");
  assert.equal(search.data.records.length, 1);
  const record = search.data.records[0];
  assert.deepEqual({
    id: record.id,
    title: record.title,
    type: record.type,
    authority: record.authority,
    access: record.access,
    rights: record.rights,
    freshness: record.freshness,
    status: record.status,
  }, {
    id: "hmlr:dataset:inspire-index-polygons",
    title: "Index polygons spatial data (INSPIRE)",
    type: "dataset",
    authority: "source-authoritative",
    access: "public",
    rights: "open-with-conditions",
    freshness: "current",
    status: "candidate-metadata",
  });
  assert.equal(record.tags.includes("inspire"), true);
  assert.deepEqual({
    limit: search.data.page.limit,
    matched: search.data.page.matched,
    returned: search.data.page.returned,
  }, { limit: 1, matched: 6, returned: 1 });
  assert.equal(typeof search.data.page.next_cursor, "string");
  assert.notEqual(search.data.page.next_cursor.length, 0);
  assert.equal(search.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v1");
  assert.equal(search.evidence_receipt.result.returned_record_count, 1);
  assert.deepEqual(search.evidence_receipt.catalogue, search.catalogue);
  assert.deepEqual(
    search.evidence_receipt.licence_obligations.map(({ record_id: id }) => id),
    [record.id],
  );
}

function assertCatalogueDescribe(describe) {
  assert.equal(describe.schema, "gis-ai-go.catalogue-result.v1");
  assert.deepEqual(describe.warnings, []);
  assert.equal(describe.catalogue.content_root_sha256, CONTENT_ROOT);
  const record = describe.data.record;
  assert.deepEqual({
    id: record.id,
    title: record.title,
    type: record.type,
    status: record.status,
    authority: {
      class: record.authority.class,
      source: record.authority.source,
    },
    access: {
      state: record.access.state,
      tier: record.access.tier,
    },
    rights: record.rights.state,
    publication: record.publication,
  }, {
    id: "LR-Q003",
    title: "LR-Q003 — Online copy or official copy proof of ownership",
    type: "workflow",
    status: "candidate-non-executing",
    authority: { class: "derived", source: "S-OKF-HMLR-V0.3.0" },
    access: { state: "planned-non-executing", tier: "open" },
    rights: "metadata-citation",
    publication: {
      classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
    },
  });
  const expectedSources = [
    "S-OKF-HMLR-V0.3.0",
    "hmlr-source:7177c8b621ecfc42",
    "hmlr-source:b81206b053b276d5",
  ];
  assert.deepEqual(record.source_refs, expectedSources);
  assert.deepEqual(
    describe.data.included.relationships.map(({ record_id: id }) => id),
    expectedSources,
  );
  assert.deepEqual(
    describe.data.included.sources.map(({ id }) => id),
    expectedSources,
  );
  assert.equal(describe.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v1");
  assert.equal(describe.evidence_receipt.result.returned_record_count, 4);
  assert.deepEqual(describe.evidence_receipt.catalogue, describe.catalogue);
  assert.deepEqual(
    describe.evidence_receipt.licence_obligations
      .map(({ record_id: id }) => id)
      .sort(),
    [record.id, ...expectedSources].sort(),
  );
}

function assertSelection(selection) {
  assert.equal(selection.schema, "gis-ai-go.selection-resolve-result.v1");
  assert.equal(selection.data.status, "resolved");
  assert.equal(selection.data.ambiguity, null);
  assert.deepEqual(selection.data.plan, EXPECTED_SELECTION_PLAN);
  assert.equal(selection.data.resource_id, PUBLIC_READ_RESOURCE_ID);
  assert.deepEqual(selection.data.ranking, {
    algorithm: "weighted-exact-constraints",
    version: "v1",
    selection_profile_id:
      "gis-ai-go:public-selection-profile:sha256:" +
      "344fe6d8cbec7c355735ee711cd19b067be306f4087b30c341efec6c5e819f8e",
    selected_candidate_id: "PV-ONS-DATA:weekly-deaths-region:time-series:121",
    considered_candidates: 1,
    score: 260,
    top_score_tied: false,
    matched_constraints: [
      "candidate_record_ids",
      "constraints.profile_ids",
      "constraints.provider_ids",
      "constraints.dataset_ids",
      "constraints.editions",
      "constraints.versions",
      "constraints.dimensions.time",
      "constraints.dimensions.geography",
      "constraints.dimensions.week",
      "constraints.dimensions.causeofdeath",
    ],
  });
  assert.deepEqual(selection.warnings, [
    "This plan is non-executable and no provider was called.",
    "Question text is untrusted data and was not interpreted.",
  ]);
  assert.equal(selection.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v2");
  assert.equal(selection.evidence_receipt.result.returned_item_count, 1);
  assert.equal(selection.evidence_receipt.resource.resource_id, PUBLIC_READ_RESOURCE_ID);
  assert.deepEqual(selection.evidence_receipt.resource, EXPECTED_PUBLIC_READ_RESOURCE);
  assert.equal(
    selection.evidence_receipt.policy_decision.reason_code,
    "public-read-operation-allowed",
  );
  assert.equal(
    selection.evidence_receipt.policy_decision.obligations.includes("no-provider-execution"),
    true,
  );
}

function assertDataQuery(data, selection) {
  assert.equal(data.schema, "gis-ai-go.data-query-result.v1");
  assert.deepEqual(data.data, {
    status: "succeeded",
    observations: [{ value: "10471", unit: null }],
  });
  assert.deepEqual(data.warnings, []);
  assert.deepEqual(selection.data.plan.data_query, DATA_QUERY_REQUEST.parameters);
  assert.equal(data.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v2");
  assert.equal(data.evidence_receipt.result.returned_item_count, 1);
  assert.deepEqual(data.evidence_receipt.resource, EXPECTED_PUBLIC_READ_RESOURCE);
  assert.equal(data.evidence_receipt.resource.resource_id, selection.data.resource_id);
  assert.equal(
    data.evidence_receipt.policy_decision.reason_code,
    "public-read-operation-allowed",
  );
  assert.equal(
    data.evidence_receipt.policy_decision.obligations.includes("bounded-single-observation"),
    true,
  );
  assert.notEqual(
    data.evidence_receipt.receipt_id,
    selection.evidence_receipt.receipt_id,
  );
}

function assertStoredReceiptRelationships(values) {
  const storage = values.map(({ evidence_storage: reference }) => reference);
  assert.equal(new Set(storage.map(({ ledger_id: id }) => id)).size, 1);
  for (const key of ["record_id", "event_id"]) {
    assert.equal(new Set(storage.map((reference) => reference[key])).size, values.length);
  }
  assert.equal(new Set(values.map(({ evidence_receipt: receipt }) => receipt.receipt_id)).size, 4);
}

function assertInspection(inspection, search) {
  const searchReceipt = search.evidence_receipt.receipt_id;
  assert.equal(inspection.schema, "gis-ai-go.evidence-inspect-result.v3");
  assert.deepEqual(inspection.verification, {
    status: "passed",
    ledger: "restart-verified",
    receipt: "structure-and-content-verified",
    ingest_material: "verified-at-ingest-not-retained",
    attestation: "not-attested",
  });
  assert.equal(inspection.data.record.schema, "gis-ai-go.public-evidence-record.v1");
  assert.deepEqual(inspection.data.record.receipt, search.evidence_receipt);
  assert.deepEqual(inspection.data.storage, search.evidence_storage);
  assert.equal(inspection.data.event.sequence, 1);
  assert.equal(inspection.data.event.event_type, "evidence.stored");
  assert.equal(inspection.data.event.ledger_id, search.evidence_storage.ledger_id);
  assert.equal(inspection.data.event.record_id, search.evidence_storage.record_id);
  assert.equal(inspection.data.event.event_id, search.evidence_storage.event_id);
  assert.equal(inspection.data.event.receipt_id, searchReceipt);
  assert.equal(inspection.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v3");
  assert.equal(inspection.evidence_receipt.operation.contract_version, "v3");
  assert.notEqual(inspection.evidence_receipt.receipt_id, searchReceipt);
  assert.equal(inspection.evidence_receipt.policy_decision.inspected_receipt_id, searchReceipt);
  assert.deepEqual(inspection.evidence_receipt.inspected_evidence, {
    ledger_id: search.evidence_storage.ledger_id,
    receipt_id: searchReceipt,
    record_id: search.evidence_storage.record_id,
    event_id: search.evidence_storage.event_id,
  });
  assert.deepEqual(inspection.evidence_receipt.evidence_handling, {
    delivery: "inline-only",
    persistence: "not-persisted",
    attestation: "not-attested",
    ledger_event: "not-created",
  });
}

function receiptSummary(operation, value) {
  return Object.freeze({
    operation,
    outcome: "succeeded",
    receipt_id: value.evidence_receipt.receipt_id,
    plain_text_parity: true,
  });
}

export async function runLocalExactFiveDemo() {
  const source = currentSourceState();
  const sourceCommit = source.commit;
  const temporaryRoot = mkdtempSync(join(tmpdir(), TEMPORARY_ROOT_PREFIX));
  chmodSync(temporaryRoot, 0o700);
  const child = spawn(
    process.execPath,
    [
      "--import",
      PROVIDER_EGRESS_GUARD,
      SERVER,
      AUTHORITY_ARGUMENT,
      "--scenario=active",
    ],
    {
      cwd: ROOT,
      env: isolatedChildEnvironment(sourceCommit, temporaryRoot),
      stdio: ["pipe", "pipe", "pipe", "pipe"],
    },
  );
  const closeObservation = observeChildClose(child);
  assert.ok(child.stdin);
  assert.ok(child.stdout);
  assert.ok(child.stderr);
  assert.ok(child.stdio[3]);

  const pending = new Map();
  const audits = [];
  const responseIds = [];
  let streamError;
  let spawnError;
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });
  const failStreams = (error) => {
    streamError ??= error;
    for (const request of pending.values()) request.reject(error);
    pending.clear();
  };
  child.once("error", (error) => {
    spawnError = error;
    failStreams(error);
  });
  child.stdin.on("error", failStreams);
  const stdoutRemainder = attachJsonLines(
    child.stdout,
    "The demo fixture",
    (message) => {
      assert.equal(Object.hasOwn(message, "id"), true, "Unexpected JSON-RPC notification");
      assert.equal(Number.isInteger(message.id), true, "Unexpected JSON-RPC response id");
      const request = pending.get(String(message.id));
      assert.notEqual(request, undefined, `Unmatched or duplicate response id ${message.id}`);
      assert.equal(responseIds.includes(message.id), false, `Duplicate response id ${message.id}`);
      pending.delete(String(message.id));
      responseIds.push(message.id);
      request.resolve(message);
    },
    failStreams,
  );
  const auditRemainder = attachJsonLines(
    child.stdio[3],
    "The private audit pipe",
    (message) => audits.push(message),
    failStreams,
  );
  void closeObservation.promise.then(({ code, signal }) => {
    if (pending.size === 0) return;
    failStreams(new Error(
      `The demo fixture closed with ${pending.size} pending request(s); ` +
      `code=${String(code)} signal=${String(signal)}`,
    ));
  });

  async function request(id, method, params) {
    const key = String(id);
    assert.equal(closeObservation.count(), 0, "Cannot send a request after the child closed");
    assert.equal(pending.has(key), false, `Duplicate request id ${key}`);
    assert.equal(responseIds.includes(id), false, `Reused request id ${key}`);
    const response = withTimeout(
      new Promise((resolveResponse, rejectResponse) => {
        pending.set(key, { reject: rejectResponse, resolve: resolveResponse });
      }),
      `STDIO response ${key}`,
    );
    const write = new Promise((resolveWrite, rejectWrite) => {
      child.stdin.write(
        `${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`,
        (error) => {
          if (error === null || error === undefined) resolveWrite();
          else rejectWrite(error);
        },
      );
    });
    const [message] = await Promise.all([response, write]);
    assert.equal(message.id, id);
    return message;
  }

  const metaParams = (value = {}) => ({ _meta: META, ...value });
  let cleanupComplete = false;
  let primaryError;
  try {
    const discovered = result(await request(1, "server/discover", metaParams()));
    assert.deepEqual(discovered.supportedVersions, [MCP_PROTOCOL_VERSION]);

    const tools = result(await request(2, "tools/list", metaParams())).tools;
    const toolNames = tools.map(({ name }) => name);
    assert.equal(toolNames.length, EXACT_OPERATIONS.length);
    assert.deepEqual([...toolNames].sort(), [...EXACT_OPERATIONS].sort());
    for (const tool of tools) {
      for (const schema of [tool.inputSchema, tool.outputSchema]) {
        assert.equal(typeof schema, "object");
        assert.notEqual(schema, null);
        assert.equal(Array.isArray(schema), false);
      }
    }

    const listedResources = result(
      await request(3, "resources/list", metaParams()),
    ).resources;
    assert.deepEqual(
      listedResources.map(({ uri }) => uri),
      [MCP_PUBLIC_CATALOGUE_URI],
    );
    const templates = result(
      await request(4, "resources/templates/list", metaParams()),
    ).resourceTemplates;
    assert.deepEqual(
      templates.map(({ uriTemplate }) => uriTemplate),
      [MCP_CATALOGUE_RECORD_URI_TEMPLATE, MCP_EVIDENCE_RECEIPT_URI_TEMPLATE],
    );

    const publicCatalogue = result(await request(
      5,
      "resources/read",
      metaParams({ uri: MCP_PUBLIC_CATALOGUE_URI }),
    ));
    assert.equal(publicCatalogue.contents.length, 1);
    assert.equal(publicCatalogue.contents[0].uri, MCP_PUBLIC_CATALOGUE_URI);
    const publicCatalogueValue = JSON.parse(publicCatalogue.contents[0].text);
    assert.equal(publicCatalogueValue.recordCount, 36);
    assert.equal(publicCatalogueValue.records.length, 36);

    const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
    const record = result(await request(
      6,
      "resources/read",
      metaParams({ uri: recordUri }),
    ));
    assert.equal(record.contents.length, 1);
    assert.equal(record.contents[0].uri, recordUri);
    const recordValue = JSON.parse(record.contents[0].text);
    assert.equal(recordValue.id, "LR-Q003");
    assert.equal(recordValue.title, "LR-Q003 — Online copy or official copy proof of ownership");

    const search = assertToolResult(await request(
      10,
      "tools/call",
      metaParams({
        name: "catalogue.search",
        arguments: { query: "INSPIRE", limit: 1 },
      }),
    ), "catalogue.search", { persisted: true });
    assertCatalogueSearch(search, sourceCommit);
    const describe = assertToolResult(await request(
      11,
      "tools/call",
      metaParams({
        name: "catalogue.describe",
        arguments: { record_id: "LR-Q003" },
      }),
    ), "catalogue.describe", { persisted: true });
    assertCatalogueDescribe(describe);
    const selection = assertToolResult(await request(
      12,
      "tools/call",
      metaParams({ name: "selection.resolve", arguments: SELECTION_REQUEST }),
    ), "selection.resolve", { persisted: true });
    assertSelection(selection);
    const data = assertToolResult(await request(
      13,
      "tools/call",
      metaParams({ name: "data.query", arguments: DATA_QUERY_REQUEST }),
    ), "data.query", { persisted: true });
    assertDataQuery(data, selection);
    assertStoredReceiptRelationships([search, describe, selection, data]);

    const searchReceipt = search.evidence_receipt.receipt_id;
    const inspection = assertToolResult(await request(
      14,
      "tools/call",
      metaParams({
        name: "evidence.inspect",
        arguments: { receipt_id: searchReceipt },
      }),
    ), "evidence.inspect", { persisted: false });
    assertInspection(inspection, search);

    const evidenceUri =
      `gis-ai-go://evidence/receipts/${encodeURIComponent(searchReceipt)}`;
    const evidence = result(await request(
      15,
      "resources/read",
      metaParams({ uri: evidenceUri }),
    ));
    assert.equal(evidence.contents.length, 1);
    assert.equal(evidence.contents[0].uri, evidenceUri);
    assert.deepEqual(JSON.parse(evidence.contents[0].text), inspection);

    const close = await closeChildAndRemoveTemporaryRoot(
      child,
      closeObservation,
      temporaryRoot,
    );
    cleanupComplete = true;
    assert.equal(close.stage, "graceful-eof");
    assert.equal(close.signal, null);
    assert.equal(close.code, 0, stderr);
    assert.equal(stderr, "");
    assert.equal(spawnError, undefined);
    assert.equal(streamError, undefined);
    assert.equal(stdoutRemainder(), "");
    assert.equal(auditRemainder(), "");
    assert.equal(pending.size, 0);
    assert.deepEqual(responseIds, [1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15]);
    assert.deepEqual(audits.map(({ event }) => event), [
      "provider-egress-guard-ready",
      "provider-transport-started",
      "provider-egress-guard-summary",
      "session-summary",
    ]);
    const guardReady = audits[0];
    const transportStarted = audits[1];
    const guardSummary = audits[2];
    assert.deepEqual(guardReady.guarded_apis, [
      "dns.Resolver.resolve4",
      "dns.Resolver.resolve6",
      "https.request",
    ]);
    assert.equal(transportStarted.scenario, "active");
    assert.equal(transportStarted.ordinal, 1);
    assert.equal(guardSummary.guarded_api_invocation_count, 0);
    assert.deepEqual(guardSummary.guarded_apis, guardReady.guarded_apis);
    const summaries = audits.filter(({ event }) => event === "session-summary");
    assert.equal(summaries.length, 1);
    const summary = summaries[0];
    assert.equal(summary.source_commit, sourceCommit);
    assert.equal(summary.state, "candidate-unregistered");
    assert.equal(summary.production_registration, false);
    assert.deepEqual(summary.operations, EXACT_OPERATIONS);
    assert.deepEqual(summary.resources, EXACT_RESOURCES);
    assert.deepEqual(summary.suspensions, []);
    assert.equal(summary.provider_transport_calls, 1);
    assert.equal(summary.aborted_provider_calls, 0);
    assert.equal(summary.ledger_event_count, 4);
    assert.equal(summary.reported_error_count, 0);

    return Object.freeze({
      format: "gis-ai-go.local-exact-five-demo.v1",
      status: "passed",
      source_commit: sourceCommit,
      source: Object.freeze({
        commit: sourceCommit,
        working_tree_clean: source.workingTreeClean,
        binding: source.workingTreeClean
          ? "exact-clean-head"
          : "head-with-local-changes",
      }),
      protocol_version: MCP_PROTOCOL_VERSION,
      transport: "operating-system-stdio-pipes",
      network_boundary: Object.freeze({
        operating_system_isolation_enforced: false,
        guarded_provider_egress_apis_invoked:
          guardSummary.guarded_api_invocation_count,
        claim_scope: "guarded-node-provider-egress-apis",
      }),
      discovery: Object.freeze({
        tools: EXACT_OPERATIONS,
        resources: EXACT_RESOURCES,
        resource_uris: Object.freeze([MCP_PUBLIC_CATALOGUE_URI]),
        resource_templates: Object.freeze([
          MCP_CATALOGUE_RECORD_URI_TEMPLATE,
          MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
        ]),
      }),
      journey: Object.freeze([
        receiptSummary("catalogue.search", search),
        receiptSummary("catalogue.describe", describe),
        receiptSummary("selection.resolve", selection),
        Object.freeze({
          ...receiptSummary("data.query", data),
          observation_value: "10471",
          observation_source: "deterministic-fixed-ons-shaped-fixture",
        }),
        Object.freeze({
          ...receiptSummary("evidence.inspect", inspection),
          inspected_receipt_id: searchReceipt,
        }),
      ]),
      evidence: Object.freeze({
        ledger_event_count: summary.ledger_event_count,
        inspection_created_ledger_event: false,
      }),
      provider: Object.freeze({
        mode: "deterministic-fixed-response",
        audited_injected_transport_calls: summary.provider_transport_calls,
      }),
      credential_environment: Object.freeze({
        parent_environment_forwarded: false,
        allowed_names: Object.freeze([
          ENABLE_FLAG,
          SOURCE_COMMIT_VARIABLE,
          "TMPDIR",
          "TMP",
          "TEMP",
        ]),
      }),
      boundary: Object.freeze({
        state: summary.state,
        production_registration: summary.production_registration,
        public_listener: false,
        registry_modified: false,
        production_entrypoint_used: false,
        activation: false,
        deployment: false,
        release: false,
      }),
    });
  } catch (error) {
    primaryError = error;
    throw error;
  } finally {
    if (!cleanupComplete) {
      try {
        await closeChildAndRemoveTemporaryRoot(child, closeObservation, temporaryRoot);
      } catch (cleanupError) {
        if (primaryError !== undefined) {
          throw new AggregateError(
            [primaryError, cleanupError],
            "The local demonstration and its child cleanup both failed",
          );
        }
        throw cleanupError;
      }
    }
  }
}

function shortReceipt(receiptId) {
  return `${receiptId.slice(0, 47)}…`;
}

export function formatHumanDemo(report) {
  const lines = [
    "GIS AI GO local exact-five demonstration",
    `Source commit: ${report.source_commit} (` +
      `${report.source.working_tree_clean ? "clean" : "with local changes"})`,
    `Transport: MCP ${report.protocol_version} over private STDIO pipes`,
    "Provider: one injected fixed-response call; no guarded provider-egress API invoked",
    "OS network isolation: not enforced; this demonstration is not a network sandbox",
    `1. Discovery — exactly ${report.discovery.tools.length} tools verified`,
    `2. Resources — ${report.discovery.resources.length} governed resources verified`,
  ];
  for (const [index, step] of report.journey.entries()) {
    const observation = step.operation === "data.query"
      ? `; fixture observation ${step.observation_value}`
      : "";
    lines.push(
      `${index + 3}. ${step.operation} — passed; ${shortReceipt(step.receipt_id)}` +
        observation,
    );
  }
  lines.push(
    `Boundary: ${report.boundary.state}; ` +
      `production_registration=${String(report.boundary.production_registration)}`,
    "No public listener, registry change, live provider call, activation, deployment " +
      "or release occurred.",
    "Result: PASS",
  );
  return `${lines.join("\n")}\n`;
}

function parseMode(argumentsValue) {
  if (argumentsValue.length === 0) return "human";
  if (argumentsValue.length === 1 && argumentsValue[0] === "--json") return "json";
  throw new Error("Usage: node scripts/qual_206_local_demo.mjs [--json]");
}

async function main() {
  const mode = parseMode(process.argv.slice(2));
  const report = await runLocalExactFiveDemo();
  process.stdout.write(
    mode === "json" ? `${JSON.stringify(report, null, 2)}\n` : formatHumanDemo(report),
  );
}

const entryPath = process.argv[1];
if (
  entryPath !== undefined &&
  import.meta.url === pathToFileURL(resolve(entryPath)).href
) {
  try {
    await main();
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown local demo failure";
    process.stderr.write(`GIS AI GO local exact-five demo failed: ${message}\n`);
    process.exitCode = 1;
  }
}
