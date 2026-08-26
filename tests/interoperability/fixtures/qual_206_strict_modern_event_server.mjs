import { fstatSync, mkdtempSync, realpathSync, rmSync, writeSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "../../../packages/evidence/dist/src/index.js";
import {
  FixedHttpsTransportError,
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  createOnsDataApiAdapter,
} from "../../../packages/provider-adapter-sdk/dist/src/index.js";
import { loadCatalogueSnapshot } from
  "../../../apps/mcp-gateway/dist/src/catalogue-snapshot.js";
import {
  createGovernedCandidateAssembly,
  governedCandidateAssemblyBindings,
  verifyGovernedCandidateOperation,
} from
  "../../../apps/mcp-gateway/dist/src/governed-assembly.js";
import { startCatalogueStdio, startGovernedCandidateStdio } from
  "../../../apps/mcp-gateway/dist/src/mcp-stdio.js";

// This additive fixture leaves the accepted exact-five fixture byte-exact because
// the existing non-live local evaluation receipts bind that historical source.

const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUTHORITY_ARGUMENT = "--exact-five-stdio-conformance-only";
const FULL_COMMIT = /^[0-9a-f]{40}$/u;
const SCENARIO_ARGUMENT = /^--scenario=([a-z0-9.\-]+)$/u;
const FIXED_ASSEMBLY_TIME = new Date("2026-08-24T08:00:00.000Z");
const FIXED_LEDGER_TIME = new Date("2026-08-24T08:00:01.000Z");
const FIXED_RECONCILIATION_TIME = new Date("2026-08-24T08:00:02.000Z");

const ACTIVE_LIFECYCLE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Exact-five deterministic subprocess conformance fixture.",
});

const SCENARIOS = Object.freeze({
  active: Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  cancellation: Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  "independent-host": Object.freeze({ lifecycle: ACTIVE_LIFECYCLE }),
  "claude-host-002": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: Object.freeze([
      "catalogue.describe",
      "selection.resolve",
      "data.query",
      "evidence.inspect",
    ]),
  }),
  "claude-exact-five-v1": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    toolsOnly: true,
  }),
  "claude-exact-five-v1-tampered-receipt": Object.freeze({
    lifecycle: ACTIVE_LIFECYCLE,
    toolsOnly: true,
    tamperedReceiptOperation: "catalogue.describe",
  }),
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
    requestId: "exact-five-stdio-search-001",
    traceId: "1".repeat(32),
    instance: "/catalogue/search",
  }),
  "catalogue.describe": Object.freeze({
    requestId: "exact-five-stdio-describe-001",
    traceId: "2".repeat(32),
    instance: "/catalogue/describe",
  }),
  "selection.resolve": Object.freeze({
    requestId: "exact-five-stdio-selection-001",
    traceId: "3".repeat(32),
    instance: "/selection/resolve",
  }),
  "data.query": Object.freeze({
    requestId: "exact-five-stdio-data-001",
    traceId: "4".repeat(32),
    instance: "/data/query",
  }),
  "evidence.inspect": Object.freeze({
    requestId: "exact-five-stdio-inspect-001",
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
    `Refusing to expose the exact-five STDIO fixture without ${ENABLE_FLAG}=1`,
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
    "Exact-five STDIO conformance requires its exact authority and closed scenario",
  );
}
const scenarioName = scenarioMatch[1];
const scenario = SCENARIOS[scenarioName];

try {
  fstatSync(3);
} catch {
  throw new Error("Exact-five STDIO conformance requires its private audit pipe");
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
    schema: "gis-ai-go.qual-206-exact-five-stdio-audit.v1",
    event: "provider-transport-started",
    scenario: scenarioName,
    ordinal: providerTransportCalls,
  }));
  const awaitsCancellation =
    scenarioName === "cancellation" ||
    (scenarioName === "independent-host" && providerTransportCalls === 2);
  if (!awaitsCancellation) return fixedResponse();

  return await new Promise((_resolve, reject) => {
    let complete = false;
    const abort = () => {
      if (complete) return;
      complete = true;
      abortedProviderCalls += 1;
      signal.removeEventListener("abort", abort);
      writeAudit(Object.freeze({
        schema: "gis-ai-go.qual-206-exact-five-stdio-audit.v1",
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
  "gis-ai-go-exact-five-stdio-",
));
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
  fileURLToPath(new URL("../../../artifacts/okf/", import.meta.url)),
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

const stdioOptions = {
  createRequestContext: (operation) => REQUEST_CONTEXTS[operation],
  onerror: () => {
    reportedErrors += 1;
  },
};
const handle = scenario.toolsOnly === true
  ? (() => {
      const bindings = governedCandidateAssemblyBindings(assembly);
      const catalogueApplication = scenario.tamperedReceiptOperation === undefined
        ? bindings.catalogueApplication
        : Object.freeze({
            search: bindings.catalogueApplication.search,
            describe: (...parameters) => {
              const result = structuredClone(
                bindings.catalogueApplication.describe(...parameters),
              );
              result.evidence_receipt.receipt_id =
                `gis-ai-go:evidence-receipt:sha256:${"0".repeat(64)}`;
              return result;
            },
          });
      return startCatalogueStdio({
        ...stdioOptions,
        application: catalogueApplication,
        evidenceApplication: bindings.evidenceApplication,
        selectionApplication: bindings.selectionApplication,
        dataQueryApplication: bindings.dataQueryApplication,
        snapshot: bindings.snapshot,
        enabledOperations: assembly.mcpOperations,
        enabledResources: [],
        readinessGuard: (operation) => verifyGovernedCandidateOperation(assembly, operation),
      });
    })()
  : startGovernedCandidateStdio(assembly, stdioOptions);

let closing = false;
async function close() {
  if (closing) return;
  closing = true;
  await handle.close();
}

process.once("SIGINT", () => void close());
process.once("SIGTERM", () => void close());
process.once("exit", () => {
  try {
    writeAudit(Object.freeze({
      schema: "gis-ai-go.qual-206-exact-five-stdio-audit.v1",
      event: "session-summary",
      scenario: scenarioName,
      source_commit: sourceCommit,
      transport: "operating-system-stdio-pipes",
      state: assembly.state,
      production_registration: assembly.productionRegistration,
      operations: assembly.operations,
      resources: scenario.toolsOnly === true ? [] : assembly.mcpResources,
      suspensions: assembly.suspensions,
      provider_transport_calls: providerTransportCalls,
      aborted_provider_calls: abortedProviderCalls,
      ledger_event_count: ledger.verify().event_count,
      reported_error_count: reportedErrors,
    }));
  } finally {
    rmSync(stateRoot, { recursive: true, force: true });
  }
});
