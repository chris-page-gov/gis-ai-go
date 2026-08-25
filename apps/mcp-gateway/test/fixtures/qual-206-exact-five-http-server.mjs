import {
  chmodSync,
  fstatSync,
  mkdtempSync,
  realpathSync,
  rmSync,
  statSync,
  writeSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  publicIdempotencyKeySha256,
} from "../../../../packages/evidence/dist/src/index.js";
import {
  FixedHttpsTransportError,
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  createOnsDataApiAdapter,
} from "../../../../packages/provider-adapter-sdk/dist/src/index.js";
import { loadCatalogueSnapshot } from "../../dist/src/catalogue-snapshot.js";
import { createGovernedCandidateAssembly } from "../../dist/src/governed-assembly.js";
import { createGovernedCandidateNodeServer } from "../../dist/src/http-server.js";

const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_HTTP";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUDIT_FD_VARIABLE = "GIS_AI_GO_QUAL_206_PRIVATE_AUDIT_FD";
const AUTHORITY_ARGUMENT = "--exact-five-http-conformance-only";
const FULL_COMMIT = /^[0-9a-f]{40}$/u;
const SCENARIO_ARGUMENT = /^--scenario=([a-z.\-]+)$/u;
const AUDIT_SCHEMA = "gis-ai-go.qual-206-exact-five-http-audit.v1";
const GUARD_STATE_SYMBOL = Symbol.for("gis-ai-go.qual-206-provider-egress-guard");
const FIXED_ASSEMBLY_TIME = new Date("2026-08-25T08:00:00.000Z");
const FIXED_LEDGER_TIME = new Date("2026-08-25T08:00:01.000Z");
const FIXED_RECONCILIATION_TIME = new Date("2026-08-25T08:00:02.000Z");
const SUCCESSFUL_DATA_QUERY_IDEMPOTENCY_KEY =
  `gis-ai-go:ik:v1:${"9".repeat(64)}`;
const ABORTED_DATA_QUERY_IDEMPOTENCY_KEY =
  `gis-ai-go:ik:v1:${"8".repeat(64)}`;

const ACTIVE_LIFECYCLE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Exact-five deterministic real-socket HTTP conformance fixture.",
});

const SCENARIOS = Object.freeze({
  active: Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  "capability-pack": Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  cancellation: Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  unsupported: Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  "provider-discovery": Object.freeze({
    lifecycle: Object.freeze({
      discovery: "suspended",
      invocation: "active",
      reason: "Deterministic provider-discovery suspension fixture.",
    }),
  }),
  "provider-invocation": Object.freeze({
    lifecycle: Object.freeze({
      discovery: "active",
      invocation: "suspended",
      reason: "Deterministic provider-invocation suspension fixture.",
    }),
  }),
  "explicit-catalogue.search": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze(["catalogue.search"]),
  }),
  "explicit-catalogue.describe": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze(["catalogue.describe"]),
  }),
  "explicit-selection.resolve": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze(["selection.resolve"]),
  }),
  "explicit-data.query": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze(["data.query"]),
  }),
  "explicit-evidence.inspect": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze(["evidence.inspect"]),
  }),
});

const REQUEST_CONTEXTS = Object.freeze({
  "catalogue.search": Object.freeze({
    requestId: "exact-five-http-search-001",
    traceId: "1".repeat(32),
    instance: "/catalogue/search",
  }),
  "catalogue.describe": Object.freeze({
    requestId: "exact-five-http-describe-001",
    traceId: "2".repeat(32),
    instance: "/catalogue/describe",
  }),
  "selection.resolve": Object.freeze({
    requestId: "exact-five-http-selection-001",
    traceId: "3".repeat(32),
    instance: "/selection/resolve",
  }),
  "data.query": Object.freeze({
    requestId: "exact-five-http-data-001",
    traceId: "4".repeat(32),
    instance: "/data/query",
  }),
  "evidence.inspect": Object.freeze({
    requestId: "exact-five-http-inspect-001",
    traceId: "5".repeat(32),
    instance: "/evidence/inspect",
  }),
});

const VALID_ONS_PAYLOAD = Object.freeze({
  dimensions: {
    causeofdeath: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/cause-of-death/codes/all-causes",
        id: "all-causes",
      },
    },
    geography: {
      option: {
        href:
          "http://api.beta.ons.gov.uk/v1/code-lists/administrative-geography/" +
          "codes/E92000001",
        id: "E92000001",
      },
    },
    time: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/calendar-years/codes/2026",
        id: "2026",
      },
    },
    week: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/week-number/codes/week-24",
        id: "week-24",
      },
    },
  },
  limit: 10_000,
  links: {
    dataset_metadata: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121/metadata",
    },
    self: { href: ONS_OBSERVATION_URI },
    version: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121",
      id: "121",
    },
  },
  observations: [{ metadata: { "Data Marking": "" }, observation: "10471" }],
  offset: 0,
  total_observations: 1,
});

if (process.env[ENABLE_FLAG] !== "1") {
  throw new Error(
    `Refusing to expose the exact-five HTTP fixture without ${ENABLE_FLAG}=1`,
  );
}

const sourceCommit = process.env[SOURCE_COMMIT_VARIABLE] ?? "";
if (!FULL_COMMIT.test(sourceCommit)) {
  throw new Error(`${SOURCE_COMMIT_VARIABLE} must be a full lowercase Git commit`);
}

const argumentsValue = process.argv.slice(2);
const scenarioMatch = SCENARIO_ARGUMENT.exec(argumentsValue[1] ?? "");
if (
  argumentsValue.length !== 2 ||
  argumentsValue[0] !== AUTHORITY_ARGUMENT ||
  scenarioMatch === null ||
  !Object.hasOwn(SCENARIOS, scenarioMatch[1])
) {
  throw new Error(
    "Exact-five HTTP conformance requires its exact authority and closed scenario",
  );
}
const scenarioName = scenarioMatch[1];
const scenario = SCENARIOS[scenarioName];

if (process.env[AUDIT_FD_VARIABLE] !== "3") {
  throw new Error(`Exact-five HTTP conformance requires ${AUDIT_FD_VARIABLE}=3`);
}
try {
  const auditPipe = fstatSync(3);
  if (!auditPipe.isFIFO() && !auditPipe.isSocket()) throw new Error("not a pipe");
} catch {
  throw new Error("Exact-five HTTP conformance requires its private audit pipe");
}

const guardState = globalThis[GUARD_STATE_SYMBOL];
if (
  typeof guardState !== "object" ||
  guardState === null ||
  typeof guardState.snapshot !== "function"
) {
  throw new Error("Exact-five HTTP conformance requires its provider egress guard");
}

function writeAudit(value) {
  writeSync(3, `${JSON.stringify(value)}\n`, undefined, "utf8");
}

function fixedResponse() {
  const body = Buffer.from(JSON.stringify(VALID_ONS_PAYLOAD), "utf8");
  return Object.freeze({
    status: 200,
    headers: Object.freeze({ "content-type": "application/json" }),
    body,
    telemetry: Object.freeze({
      dnsMs: 1,
      resolvedAddressCount: 1,
      selectedAddressFamily: 4,
      connectMs: 2,
      responseMs: 3,
      totalMs: 6,
      compressedBytes: body.byteLength,
      tlsProtocol: "TLSv1.3",
      tlsCipher: "TLS_AES_256_GCM_SHA384",
    }),
  });
}

let providerTransportCalls = 0;
let abortedProviderCalls = 0;
let reportedErrors = 0;

async function deterministicTransport({ policy, url, signal }) {
  if (
    policy !== ONS_EGRESS_POLICY ||
    url !== ONS_OBSERVATION_URI ||
    !(signal instanceof AbortSignal)
  ) {
    throw new TypeError("The deterministic provider request escaped its fixed contract");
  }
  providerTransportCalls += 1;
  writeAudit(Object.freeze({
    schema: AUDIT_SCHEMA,
    event: "provider-transport-started",
    scenario: scenarioName,
    ordinal: providerTransportCalls,
  }));
  const mustAwaitCancellation = scenarioName === "cancellation" ||
    (scenarioName === "capability-pack" && providerTransportCalls === 2);
  if (!mustAwaitCancellation) return fixedResponse();

  return await new Promise((_resolve, reject) => {
    let complete = false;
    const abort = () => {
      if (complete) return;
      complete = true;
      abortedProviderCalls += 1;
      signal.removeEventListener("abort", abort);
      writeAudit(Object.freeze({
        schema: AUDIT_SCHEMA,
        event: "provider-transport-aborted",
        scenario: scenarioName,
        ordinal: providerTransportCalls,
      }));
      reject(new FixedHttpsTransportError("aborted"));
    };
    signal.addEventListener("abort", abort, { once: true });
    if (signal.aborted) abort();
  });
}

const stateRoot = mkdtempSync(join(
  realpathSync(tmpdir()),
  "gis-ai-go-exact-five-http-",
));
let writeSessionSummary;
process.once("exit", () => {
  try {
    writeSessionSummary?.();
  } finally {
    rmSync(stateRoot, { recursive: true, force: true });
  }
});
chmodSync(stateRoot, 0o700);
const privateStateRootMode = statSync(stateRoot).mode & 0o777;
if (privateStateRootMode !== 0o700) {
  rmSync(stateRoot, { recursive: true, force: true });
  throw new Error("Exact-five HTTP conformance state root is not private");
}

const ledger = openPublicEvidenceLedger({
  rootDirectory: join(stateRoot, "ledger"),
  retentionDays: 365,
  now: () => FIXED_LEDGER_TIME,
});
const reconciliationIndex = openEvidenceReconciliationIndex({
  rootDirectory: join(stateRoot, "reconciliation"),
  ledger,
  now: () => FIXED_RECONCILIATION_TIME,
});
const snapshot = await loadCatalogueSnapshot(
  fileURLToPath(new URL("../../../../artifacts/okf/", import.meta.url)),
  { now: FIXED_ASSEMBLY_TIME },
);
const adapter = createOnsDataApiAdapter({
  lifecycle: scenario.lifecycle,
  transport: deterministicTransport,
  now: () => Date.parse("2030-01-01T00:00:00.000Z"),
});
const assembly = createGovernedCandidateAssembly({
  snapshot,
  evidenceLedger: ledger,
  reconciliationIndex,
  adapter,
  now: () => FIXED_ASSEMBLY_TIME,
  ...(scenario.suspendedTools === undefined
    ? {}
    : { suspendedTools: scenario.suspendedTools }),
});

const server = createGovernedCandidateNodeServer(assembly, {
  createMcpRequestContext: (operation) => REQUEST_CONTEXTS[operation],
  directAllowedHosts: Object.freeze(["127.0.0.1"]),
  directAllowedOrigins: Object.freeze(["http://127.0.0.1"]),
  onerror: () => {
    reportedErrors += 1;
  },
});

await new Promise((resolve, reject) => {
  const onError = (error) => reject(error);
  server.once("error", onError);
  server.listen(0, "127.0.0.1", () => {
    server.removeListener("error", onError);
    resolve();
  });
});
const address = server.address();
if (
  address === null ||
  typeof address !== "object" ||
  address.address !== "127.0.0.1" ||
  !Number.isSafeInteger(address.port) ||
  address.port < 1 ||
  address.port > 65_535
) {
  await server.closeGateway();
  rmSync(stateRoot, { recursive: true, force: true });
  throw new Error("Exact-five HTTP conformance did not bind its closed loopback address");
}

writeAudit(Object.freeze({
  schema: AUDIT_SCHEMA,
  event: "server-listening",
  scenario: scenarioName,
  source_commit: sourceCommit,
  transport: "operating-system-loopback-http",
  host: "127.0.0.1",
  port: address.port,
  state: assembly.state,
  production_registration: assembly.productionRegistration,
}));

let closing = false;
async function close() {
  if (closing) return;
  closing = true;
  await server.closeGateway();
}

function closeFromSignal() {
  void close().catch(() => {
    reportedErrors += 1;
    process.exitCode = 1;
  });
}

process.once("SIGINT", closeFromSignal);
process.once("SIGTERM", closeFromSignal);

function idempotencyEvidenceEvent(role, idempotencyKey) {
  const digest = publicIdempotencyKeySha256(idempotencyKey);
  const lookup = reconciliationIndex.lookup(idempotencyKey);
  if (
    lookup.status !== (role === "successful" ? "completed" : "pending") ||
    lookup.claim.idempotency_key_sha256 !== digest
  ) {
    throw new Error(`The ${role} idempotency evidence state is not exact`);
  }
  if (lookup.status === "completed") {
    if (
      lookup.resolution.idempotency_key_sha256 !== digest ||
      lookup.resolution.receipt_id !== lookup.stored.record.receipt.receipt_id ||
      lookup.stored.event.receipt_id !== lookup.resolution.receipt_id ||
      lookup.stored.event.record_id !== lookup.stored.record.record_id
    ) {
      throw new Error("The successful idempotency evidence linkage is not exact");
    }
    return Object.freeze({
      schema: AUDIT_SCHEMA,
      event: "idempotency-evidence-state",
      role,
      idempotency_key_sha256: digest,
      reconciliation_status: lookup.status,
      claim_id: lookup.claim.claim_id,
      resolution_id: lookup.resolution.resolution_id,
      receipt_id: lookup.resolution.receipt_id,
      record_id: lookup.stored.record.record_id,
      ledger_event_id: lookup.stored.event.event_id,
      ledger_event_sequence: lookup.stored.event.sequence,
      completed_evidence_created: true,
    });
  }
  if ("resolution" in lookup || "stored" in lookup) {
    throw new Error("The aborted idempotency key acquired completed evidence");
  }
  return Object.freeze({
    schema: AUDIT_SCHEMA,
    event: "idempotency-evidence-state",
    role,
    idempotency_key_sha256: digest,
    reconciliation_status: lookup.status,
    claim_id: lookup.claim.claim_id,
    resolution_id: null,
    receipt_id: null,
    record_id: null,
    ledger_event_id: null,
    ledger_event_sequence: null,
    completed_evidence_created: false,
  });
}

writeSessionSummary = () => {
  if (scenarioName === "capability-pack") {
    writeAudit(idempotencyEvidenceEvent(
      "successful",
      SUCCESSFUL_DATA_QUERY_IDEMPOTENCY_KEY,
    ));
    writeAudit(idempotencyEvidenceEvent(
      "aborted",
      ABORTED_DATA_QUERY_IDEMPOTENCY_KEY,
    ));
  }
  writeAudit(Object.freeze({
    schema: AUDIT_SCHEMA,
    event: "session-summary",
    scenario: scenarioName,
    source_commit: sourceCommit,
    transport: "operating-system-loopback-http",
    host: "127.0.0.1",
    state: assembly.state,
    production_registration: assembly.productionRegistration,
    operations: assembly.operations,
    resources: assembly.mcpResources,
    suspensions: assembly.suspensions,
    provider_transport_calls: providerTransportCalls,
    aborted_provider_calls: abortedProviderCalls,
    ledger_event_count: ledger.verify().event_count,
    reported_error_count: reportedErrors,
    private_state_root_mode: privateStateRootMode.toString(8).padStart(4, "0"),
    guarded_api_invocation_count: guardState.snapshot().length,
  }));
};
