import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUTPUT_PATH = join(
  ROOT,
  "evaluation",
  "qual-206-local-evaluation-receipts.v1.json",
);
const EVALUATION_PATH = "evaluation/evaluation-cases.json";
const SCHEMA_PATH = "schemas/qual-206-local-evaluation-receipt-set.schema.json";
const BOUNDARY =
  "Repository-only deterministic evidence. It is non-live and unscored, does not " +
  "complete the research case, and does not authorise activation, deployment, " +
  "registration or release.";
const CASE_IDS = ["E01", "E02", "E09", "E13", "E15", "E17", "E20"];
const MAX_OUTPUT_BYTES = 4 * 1024 * 1024;

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function canonical(value) {
  if (value === null || typeof value === "boolean" || typeof value === "string") {
    return JSON.stringify(value);
  }
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new Error("Canonical numbers must be safe integers");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (typeof value !== "object") throw new Error("Unsupported canonical value");
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`)
    .join(",")}}`;
}

function identity(domain, value) {
  const prefix = `GIS-AI-GO\0${domain}\0v1\0`;
  return sha256(Buffer.concat([Buffer.from(prefix, "utf8"), Buffer.from(canonical(value))]));
}

function escapePattern(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
}

function material(path) {
  const bytes = readFileSync(join(ROOT, path));
  return { path, sha256: sha256(bytes) };
}

function localOnlyEnvironment() {
  const env = { CI: "1", NO_COLOR: "1", UV_OFFLINE: "1" };
  for (const name of ["HOME", "LANG", "LC_ALL", "PATH", "TMPDIR", "TZ"]) {
    if (process.env[name] !== undefined) env[name] = process.env[name];
  }
  return env;
}

const SUITE_DEFINITIONS = [
  {
    label: "catalogue-snapshot",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/catalogue-snapshot.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/catalogue-snapshot.test.js",
    testNames: [
      "loads the checksum-verified catalogue as a deeply immutable snapshot",
      "rejects checksum corruption",
      "rejects a checksum-valid receipt whose manifest cross-link is false",
    ],
    materials: [
      "apps/mcp-gateway/src/catalogue-snapshot.ts",
      "okf/source-lock.json",
      "okf/source/publication.json",
    ],
  },
  {
    label: "catalogue-application",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/catalogue-application.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/catalogue-application.test.js",
    testNames: [
      "search returns governed Price Paid and INSPIRE summaries with controlled facets",
      "inline receipt verification rejects parameter replay and result or rights tampering",
      "semantically equivalent search criteria produce byte-equivalent values",
      "describe preserves full governed fields and stable source expansions",
    ],
    materials: [
      "apps/mcp-gateway/src/catalogue-application.ts",
      "apps/mcp-gateway/src/problem.ts",
      "packages/evidence/src/receipt.ts",
    ],
  },
  {
    label: "selection-application",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/selection-application.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/selection-application.test.js",
    testNames: [
      "resolves exact ranked constraints to one content-addressed non-executable plan",
      "normalises ordering deterministically without interpreting question text",
      "returns explicit ambiguity, missing, contradiction and no-provider outcomes",
      "has no provider adapter, transport, registry or activation dependency",
    ],
    materials: [
      "apps/mcp-gateway/src/selection-application.ts",
      "profiles/public-selection-profile.v1.json",
      "providers/fixtures/public-read-resource.example.json",
      "providers/fixtures/selection-plan.example.json",
    ],
  },
  {
    label: "data-query-application",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/data-query-application.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/data-query-application.test.js",
    testNames: [
      "requires an explicitly injected exact ONS adapter and closed options",
      "executes one fixed query with discovery suspended and verified evidence",
      "propagates exact validated Trace Context to the adapter without provider headers",
      "creates a random-ID-flagged provider trace for a trusted legacy context",
      "rejects a mismatched provider trace before egress",
      "uses exact approved cache after a classified HTTP 500 to 599 response",
      "uses exact approved cache after an internally classified network failure",
      "does not use cache for stale, suspended or rate-limited provider states",
      "keeps 3xx, 4xx, timeout, unsafe, malformed, opaque and unbranded failures receipt-free",
      "keeps discovery and invocation lifecycle planes independent",
      "rejects every deviation from the exact five-key request before execution",
      "independently rejects result and evidence drift",
      "maps adapter failures to fixed non-reflective receipt-free problems",
    ],
    materials: [
      "apps/mcp-gateway/src/data-query-application.ts",
      "apps/mcp-gateway/src/problem.ts",
      "apps/mcp-gateway/src/reconciliation-applications.ts",
      "packages/evidence/src/digest.ts",
      "packages/evidence/src/public-read-receipt.ts",
      "packages/provider-adapter-sdk/src/fixed-https.ts",
      "packages/provider-adapter-sdk/src/ons-approved-cache.ts",
      "packages/provider-adapter-sdk/src/ons-data-api.ts",
      "packages/provider-adapter-sdk/src/trace-context.ts",
      "packages/provider-adapter-sdk/src/types.ts",
      "providers/fixtures/data-query-parameters.example.json",
      "providers/fixtures/data-query-result.example.json",
      "providers/ons/data-query-approved-cache.v1.json",
      "schemas/approved-provider-cache.schema.json",
      "schemas/data-query-result.schema.json",
      "schemas/evidence-receipt-v2.schema.json",
    ],
  },
  {
    label: "evidence-application",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/evidence-application.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/evidence-application.test.js",
    testNames: [
      "inspects one authorised open receipt without activating a transport",
      "inspects a durable public-read v2 receipt with its distinct result version",
    ],
    materials: [
      "apps/mcp-gateway/src/evidence-application.ts",
      "packages/evidence/src/public-ledger.ts",
      "packages/evidence/src/public-read-receipt.ts",
      "packages/evidence/src/reconciliation-index.ts",
    ],
  },
  {
    label: "public-read-transport",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/public-read-transport.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/public-read-transport.test.js",
    testNames: [
      "keeps public-read capabilities absent by default and requires explicit applications",
      "propagates exact Trace Context across direct, MCP HTTP and STDIO boundaries",
      "publishes self-contained OpenAPI and identical MCP schemas with every status",
      "keeps direct and MCP HTTP success and problem JSON exactly equivalent",
      "persists selection and data evidence and inspects both through direct and STDIO",
      "keeps the legacy conformance factory structurally catalogue-only",
    ],
    materials: [
      "apps/mcp-gateway/src/activation.ts",
      "apps/mcp-gateway/src/data-query-application.ts",
      "apps/mcp-gateway/src/http-app.ts",
      "apps/mcp-gateway/src/mcp-http.ts",
      "apps/mcp-gateway/src/mcp-server.ts",
      "apps/mcp-gateway/src/mcp-stdio.ts",
      "apps/mcp-gateway/src/openapi.ts",
      "apps/mcp-gateway/src/problem.ts",
      "packages/provider-adapter-sdk/src/fixed-https.ts",
      "packages/provider-adapter-sdk/src/ons-data-api.ts",
      "packages/provider-adapter-sdk/src/trace-context.ts",
      "packages/provider-adapter-sdk/src/types.ts",
    ],
  },
  {
    label: "http-application",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/http-app.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/http-app.test.js",
    testNames: [
      "readiness is deliberately blocked with zero active operations",
      "serves an OpenAPI candidate with no catalogue operation paths",
      "direct search returns evidenced Price Paid and INSPIRE results",
      "direct API material is byte-equivalent to the shared application result",
      "implemented routes remain absent unless explicitly selected",
    ],
    materials: [
      "apps/mcp-gateway/src/activation.ts",
      "apps/mcp-gateway/src/http-app.ts",
      "apps/mcp-gateway/src/openapi.ts",
    ],
  },
  {
    label: "readiness-integrity",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/readiness-integrity.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/readiness-integrity.test.js",
    testNames: [
      "re-verifies configured evidence storage on every readiness evaluation",
      "accepts only the branded exact linked evidence pair",
    ],
    materials: [
      "apps/mcp-gateway/src/http-app.ts",
      "apps/mcp-gateway/src/readiness-integrity.ts",
      "packages/evidence/src/public-ledger.ts",
      "packages/evidence/src/reconciliation-index.ts",
    ],
  },
  {
    label: "blocked-container",
    kind: "node-test",
    sourceTest: "apps/mcp-gateway/test/container-main.test.ts",
    compiledTest: "apps/mcp-gateway/dist/test/container-main.test.js",
    testNames: [
      "keeps the container entry point fixed and production authority blocked",
      "rejects command-line configuration for the server and health check",
      "maps readiness corruption and hostile errors to fixed path-free events",
    ],
    materials: [
      "apps/mcp-gateway/src/activation.ts",
      "apps/mcp-gateway/src/container-healthcheck.ts",
      "apps/mcp-gateway/src/container-main.ts",
      "apps/mcp-gateway/src/http-app.ts",
      "apps/mcp-gateway/src/http-server.ts",
      "apps/mcp-gateway/src/metadata.ts",
      "apps/mcp-gateway/src/readiness-integrity.ts",
    ],
  },
  {
    label: "interoperability-stdio",
    kind: "node-test",
    sourceTest: "tests/interoperability/test_qual_206_harness.mjs",
    compiledTest: "tests/interoperability/test_qual_206_harness.mjs",
    testNames: [
      "conformance server fails closed without the explicit test flag",
      "legacy conformance journey keeps the existing minimised telemetry boundary",
      "proxy records minimised telemetry for a real deterministic tool call",
    ],
    materials: [
      "scripts/qual_206_conformance_server.mjs",
      "scripts/qual_206_legacy_conformance_server.mjs",
      "scripts/qual_206_telemetry_proxy.mjs",
      "tests/interoperability/qual_206_cases.json",
    ],
  },
  {
    label: "tool-registry",
    kind: "node-test",
    sourceTest: "packages/tool-registry/test/tool-registry.test.ts",
    compiledTest: "packages/tool-registry/dist/test/tool-registry.test.js",
    testNames: [
      "keeps target lifecycle metadata separate from an empty current callable set",
      "rejects lifecycle, mutability, schema and target substitutions",
      "rejects substitutions in the implemented public-read slice metadata",
      "rejects active input properties without invoking them",
    ],
    materials: [
      "packages/tool-registry/src/registry.ts",
      "profiles/tool-registry.v1.json",
      "schemas/tool-registry.schema.json",
    ],
  },
  {
    label: "trace-context",
    kind: "node-test",
    sourceTest: "packages/provider-adapter-sdk/test/trace-context.test.ts",
    compiledTest: "packages/provider-adapter-sdk/dist/test/trace-context.test.js",
    testNames: [
      "validates and copies bounded W3C Trace Context Level 2",
      "rejects invalid, ambiguous and hostile Trace Context",
    ],
    materials: [
      "packages/provider-adapter-sdk/src/index.ts",
      "packages/provider-adapter-sdk/src/trace-context.ts",
      "packages/provider-adapter-sdk/src/types.ts",
    ],
  },
  {
    label: "provider-adapter",
    kind: "node-test",
    sourceTest: "packages/provider-adapter-sdk/test/ons-data-api.test.ts",
    compiledTest: "packages/provider-adapter-sdk/dist/test/ons-data-api.test.js",
    testNames: [
      "is default-suspended on both independent lifecycle planes",
      "constructs only the fixed URL and returns deterministic native evidence",
      "keeps the checked-in live evidence privacy-safe and deterministically bound",
      "rejects caller URL/query, stale versions, wrong selection order and alternate options",
      "rejects malformed trace and arbitrary headers before provider transport",
      "brands only network and HTTP 500 to 599 faults for approved-cache use",
      "fails closed on schema, version, native-ID, link and rights drift",
    ],
    materials: [
      "packages/provider-adapter-sdk/src/fixed-https.ts",
      "packages/provider-adapter-sdk/src/ons-data-api.ts",
      "packages/provider-adapter-sdk/src/strict-json.ts",
      "packages/provider-adapter-sdk/src/trace-context.ts",
      "packages/provider-adapter-sdk/src/types.ts",
      "providers/ons/data-api-adapter-live-probe.v1.json",
      "providers/ons/data-api-adapter-preflight.v1.json",
    ],
  },
  {
    label: "approved-provider-cache",
    kind: "node-test",
    sourceTest: "packages/provider-adapter-sdk/test/ons-approved-cache.test.ts",
    compiledTest: "packages/provider-adapter-sdk/dist/test/ons-approved-cache.test.js",
    testNames: [
      "reads only the exact current policy-approved ONS cache",
      "brands only constructor-validated exact cache instances",
      "rejects cache content, coverage, approval and rebuild drift after re-signing",
      "fails closed for stale, pre-retrieval, pre-approval or unauthorised reads",
    ],
    materials: [
      "packages/evidence/src/digest.ts",
      "packages/evidence/src/public-read-receipt.ts",
      "packages/provider-adapter-sdk/src/ons-approved-cache.ts",
      "providers/ons/data-api-adapter-live-probe.v1.json",
      "providers/ons/data-query-approved-cache.v1.json",
      "schemas/approved-provider-cache.schema.json",
      "schemas/data-query-result.schema.json",
      "schemas/evidence-receipt-v2.schema.json",
    ],
  },
  {
    label: "fixed-https-parser-boundary",
    kind: "node-test",
    sourceTest: "packages/provider-adapter-sdk/test/fixed-https.test.ts",
    compiledTest: "packages/provider-adapter-sdk/dist/test/fixed-https.test.js",
    testNames: [
      "classifies real Node parser and DNS failures at the fixed transport boundary",
    ],
    materials: [
      "packages/provider-adapter-sdk/src/index.ts",
      "packages/provider-adapter-sdk/src/fixed-https.ts",
      "packages/provider-adapter-sdk/src/ons-data-api.ts",
    ],
  },
  {
    label: "public-explorer",
    kind: "vitest",
    sourceTests: [
      "apps/public-explorer/test/unit/catalogue.test.ts",
      "apps/public-explorer/test/unit/links.test.ts",
      "apps/public-explorer/test/component/cards.test.ts",
    ],
    testNames: [
      "accepts the bounded public fixture and preserves the legal-boundary caveat",
      "searches only controlled fields with NFKC normalisation and ten terms",
      "allows HTTPS destinations and deployment-relative paths",
      "renders untrusted catalogue text without creating markup",
      "links each explicit source reference without inventing a provider",
      "shows reviewed worked-question findings as governed, non-executing detail",
      "shows bounded ONS capabilities and mixed, per-record LandIS conditions",
    ],
    materials: [
      "apps/public-explorer/src/catalogue.ts",
      "apps/public-explorer/src/links.ts",
      "apps/public-explorer/src/views/cards.ts",
      "okf/source-lock.json",
      "okf/source/publication.json",
    ],
  },
];

const CASE_ASSERTIONS = {
  E01: {
    suites: [
      "catalogue-snapshot",
      "catalogue-application",
      "data-query-application",
      "approved-provider-cache",
      "public-read-transport",
    ],
    assertions: [
      ["bounded-discovery", "Only explicitly constructed read-only operations are discoverable; production remains empty and not ready."],
      ["deterministic-statistic", "The fixed ONS fixture returns one bounded observation with a verified evidence receipt and no live provider call."],
      ["catalogue-integrity", "Catalogue discovery reads only the checksum-verified public snapshot and preserves governed source metadata."],
      ["approved-cache-boundary", "Only the current execution of an exact, pristine ONS adapter can consume its owner-bound proof once after an internally classified network failure or HTTP 500 to 599 response and use the exact current approved cache; forged or substituted instances, replayed proofs, 3xx and 4xx responses, local timeouts, unsafe addresses, malformed responses, opaque or externally constructed failures, stale content and suspended states fail closed."],
    ],
    limitations: [
      "No independent host or live provider was exercised, so factual freshness, latency and host interoperability remain unscored.",
    ],
  },
  E02: {
    suites: ["public-explorer"],
    assertions: [
      ["bounded-public-data", "The static Explorer accepts the bounded public catalogue fixture and searches only controlled fields."],
      ["source-backed-links", "Visible records retain safe source links, rights distinctions and reviewed HMLR, ONS and LandIS context without scraping."],
      ["untrusted-text", "Instruction-like catalogue content is rendered as text rather than executable markup."],
    ],
    limitations: [
      "This receipt covers local unit and component behaviour, not a deployed browser journey or an AI host session.",
    ],
  },
  E09: {
    suites: [
      "catalogue-application",
      "data-query-application",
      "evidence-application",
      "approved-provider-cache",
      "public-explorer",
    ],
    assertions: [
      ["open-catalogue-provenance", "Public HMLR, ONS and LandIS catalogue material retains source links, rights and reviewed context."],
      ["ons-query-evidence", "The fixed ONS adapter fixture returns one exact observation and a verified public-read evidence receipt."],
      ["receipt-inspection", "Persisted public-read evidence can be inspected through the transport-neutral application without activating a service."],
      ["approved-cache-provenance", "The approved ONS cache binds its exact query, source probe, result, rights, complete coverage, approval and freshness evidence."],
    ],
    limitations: [
      "Only ONS has a deterministic provider-result fixture; HMLR and LandIS coverage is catalogue metadata, not a live provider query.",
    ],
  },
  E13: {
    suites: ["public-read-transport", "interoperability-stdio", "evidence-application"],
    assertions: [
      ["non-app-parity", "Direct, modern MCP and STDIO results expose the same complete structured value and JSON text fallback."],
      ["legacy-journey", "The constructor-only legacy STDIO seam completes initialise, list, call and resource operations with minimised telemetry."],
      ["evidence-completeness", "The non-App result retains the complete evidence receipt identity and inspection material."],
    ],
    limitations: [
      "No independent third-party host consumed the fallback, so host capability remains unscored.",
    ],
  },
  E15: {
    suites: ["public-explorer", "http-application", "catalogue-snapshot"],
    assertions: [
      ["linked-machine-data", "The static product exposes safe source and machine-data links over a checksum-verified catalogue."],
      ["direct-api-parity", "The explicit local direct API returns the same evidenced catalogue application result."],
      ["no-default-service", "Implemented direct routes remain absent unless explicitly selected for local conformance."],
    ],
    limitations: [
      "No WebMCP-incapable browser agent or deployed direct API was exercised; navigation capability remains unscored.",
    ],
  },
  E17: {
    suites: [
      "catalogue-application",
      "selection-application",
      "tool-registry",
      "public-explorer",
    ],
    assertions: [
      ["metadata-is-data", "Instruction-like catalogue text and question text remain quoted data and cannot alter deterministic selection."],
      ["registry-drift-closed", "Lifecycle, schema and implemented-slice registry substitutions fail closed without becoming callable."],
      ["no-poisoning-side-effect", "Rejected or ignored poisoning material has no provider, activation or evidence side effect."],
    ],
    limitations: [
      "No model or independent host was asked to follow malicious instructions, so host-level resistance remains unscored.",
    ],
  },
  E20: {
    suites: [
      "tool-registry",
      "trace-context",
      "provider-adapter",
      "fixed-https-parser-boundary",
      "data-query-application",
      "http-application",
      "public-read-transport",
      "readiness-integrity",
      "blocked-container",
    ],
    assertions: [
      ["empty-callable-set", "The current callable registry and production operation arrays remain empty with readiness blocked."],
      ["provider-suspension", "The ONS adapter keeps discovery and invocation independently suspended by default, and the approved cache cannot bypass suspension."],
      ["explicit-local-only", "Capabilities appear only through explicit local construction and cannot be enabled through runtime input."],
      ["trace-context-boundary", "Trusted W3C Trace Context is correlated exactly across the application and adapter boundaries without widening the fixed ONS egress request."],
      ["readiness-integrity", "An explicitly configured readiness ledger and reconciliation pair is re-verified on each readiness evaluation and reports only a fixed path-free event while production remains blocked."],
    ],
    limitations: [
      "No deployed provider, registry entry, operator alert or emergency rollback was exercised.",
    ],
  },
};

function runSuite(definition) {
  const sourceTests = definition.sourceTests ?? [definition.sourceTest];
  const sources = sourceTests.map((path) => ({
    path,
    source: readFileSync(join(ROOT, path), "utf8"),
  }));
  for (const { path, source } of sources) {
    if (source.length === 0) throw new Error(`${path} is empty`);
  }
  for (const name of definition.testNames) {
    if (!sources.some(({ source }) => source.includes(name))) {
      throw new Error(`${definition.label} cannot find exact test name: ${name}`);
    }
  }

  let command;
  let invocation;
  if (definition.kind === "node-test") {
    const pattern = `^(?:${definition.testNames.map(escapePattern).join("|")})$`;
    command = [
      "node",
      "--test",
      "--test-reporter=tap",
      `--test-name-pattern=${pattern}`,
      definition.compiledTest,
    ];
    invocation = spawnSync(process.execPath, command.slice(1), {
      cwd: ROOT,
      encoding: "utf8",
      env: localOnlyEnvironment(),
      maxBuffer: MAX_OUTPUT_BYTES,
    });
    if (invocation.status === 0) {
      const match = invocation.stdout.match(/# tests (\d+)[\s\S]*# pass (\d+)[\s\S]*# fail (\d+)/u);
      if (
        match === null ||
        Number(match[1]) !== definition.testNames.length ||
        Number(match[2]) !== definition.testNames.length ||
        Number(match[3]) !== 0
      ) {
        throw new Error(`${definition.label} did not run its exact selected tests`);
      }
    }
  } else {
    const testFiles = sourceTests.map((path) => path.replace("apps/public-explorer/", ""));
    const pattern = `(?:^| )(?:${definition.testNames.map(escapePattern).join("|")})$`;
    command = [
      "pnpm",
      "--filter",
      "@gis-ai-go/public-explorer",
      "exec",
      "vitest",
      "run",
      ...testFiles,
      `--testNamePattern=${pattern}`,
      "--reporter=json",
    ];
    invocation = spawnSync(command[0], command.slice(1), {
      cwd: ROOT,
      encoding: "utf8",
      env: localOnlyEnvironment(),
      maxBuffer: MAX_OUTPUT_BYTES,
    });
    if (invocation.status === 0) {
      const report = JSON.parse(invocation.stdout);
      const passedNames = report.testResults.flatMap((result) =>
        result.assertionResults
          .filter((assertion) => assertion.status === "passed")
          .map((assertion) => assertion.title),
      );
      if (
        report.success !== true ||
        report.numPassedTests !== definition.testNames.length ||
        report.numFailedTests !== 0 ||
        JSON.stringify(passedNames.sort()) !== JSON.stringify([...definition.testNames].sort())
      ) {
        throw new Error(`${definition.label} did not run its exact selected tests`);
      }
    }
  }
  if (invocation.error !== undefined) throw invocation.error;
  if (invocation.status !== 0) {
    const output = `${invocation.stdout ?? ""}\n${invocation.stderr ?? ""}`.slice(
      -16_384,
    );
    throw new Error(`${definition.label} failed with status ${invocation.status}\n${output}`);
  }

  const materialPaths = [
    ...sourceTests,
    ...definition.materials,
  ];
  const core = {
    label: definition.label,
    command,
    result: "passed",
    test_count: definition.testNames.length,
    test_names: definition.testNames,
    materials: [...new Set(materialPaths)].sort().map(material),
    controls: {
      external_network_required: false,
      live_provider_enabled: false,
      host_session_required: false,
    },
  };
  return {
    suite_id: `gis-ai-go:qual-206-local-suite-evidence:sha256:${identity(
      "qual-206-local-suite-evidence",
      core,
    )}`,
    ...core,
  };
}

function buildReceiptSet() {
  const evaluationBytes = readFileSync(join(ROOT, EVALUATION_PATH));
  const evaluation = JSON.parse(evaluationBytes.toString("utf8"));
  const cases = new Map(evaluation.cases.map((value, index) => [value.id, { ...value, index }]));
  if (CASE_IDS.some((id) => !cases.has(id))) {
    throw new Error("The evaluation manifest is missing a required local case");
  }

  const suites = SUITE_DEFINITIONS.map(runSuite);
  const suitesByLabel = new Map(suites.map((suite) => [suite.label, suite]));
  const receipts = CASE_IDS.map((caseId) => {
    const evaluationCase = cases.get(caseId);
    const definition = CASE_ASSERTIONS[caseId];
    const core = {
      case: {
        id: caseId,
        title: evaluationCase.title,
        manifest_pointer: `/cases/${evaluationCase.index}`,
      },
      outcome: {
        status: "local-preflight-pass",
        classification: "repository-only-non-live",
        scoring: "unscored",
        case_complete: false,
      },
      evidence_suite_ids: definition.suites.map((label) => {
        const suite = suitesByLabel.get(label);
        if (suite === undefined) throw new Error(`${caseId} references unknown suite ${label}`);
        return suite.suite_id;
      }),
      local_assertions: definition.assertions.map(([id, statement]) => ({ id, statement })),
      limitations: definition.limitations,
      boundary: BOUNDARY,
    };
    return {
      receipt_id: `gis-ai-go:qual-206-local-evaluation-receipt:sha256:${identity(
        "qual-206-local-evaluation-receipt",
        core,
      )}`,
      ...core,
    };
  });

  const core = {
    schema: "gis-ai-go.qual-206-local-evaluation-receipt-set.v1",
    classification: "repository-only-non-live-unscored",
    schema_contract: {
      path: SCHEMA_PATH,
      sha256: sha256(readFileSync(join(ROOT, SCHEMA_PATH))),
    },
    generator: {
      path: "scripts/qual_206_local_evaluations.mjs",
      sha256: sha256(readFileSync(fileURLToPath(import.meta.url))),
      package_json_sha256: sha256(readFileSync(join(ROOT, "package.json"))),
      pnpm_lock_sha256: sha256(readFileSync(join(ROOT, "pnpm-lock.yaml"))),
      verification_command: "pnpm run test:qual-206-local-evaluations",
    },
    evaluation_manifest: {
      path: EVALUATION_PATH,
      sha256: sha256(evaluationBytes),
      case_count: evaluation.cases.length,
    },
    suites,
    receipts,
    claims: {
      live_provider_call: false,
      live_host_session: false,
      public_deployment: false,
      production_activation: false,
      release_ready: false,
      complete_case_evaluation: false,
    },
    boundary: BOUNDARY,
  };
  return {
    ...core,
    set_id: `gis-ai-go:qual-206-local-evaluation-set:sha256:${identity(
      "qual-206-local-evaluation-set",
      core,
    )}`,
  };
}

const mode = process.argv[2] ?? "--check";
if (!["--check", "--write"].includes(mode) || process.argv.length !== 3) {
  throw new Error("Usage: node scripts/qual_206_local_evaluations.mjs --check|--write");
}
const output = `${JSON.stringify(buildReceiptSet(), null, 2)}\n`;
if (mode === "--write") {
  writeFileSync(OUTPUT_PATH, output, { encoding: "utf8", mode: 0o644 });
  process.stdout.write(`Wrote ${CASE_IDS.length} deterministic local QUAL-206 receipts.\n`);
} else {
  const current = readFileSync(OUTPUT_PATH, "utf8");
  if (current !== output) {
    throw new Error(
      "Committed local QUAL-206 receipts differ from the passing deterministic run",
    );
  }
  process.stdout.write(
    `Verified ${CASE_IDS.length} deterministic local QUAL-206 receipts; all remain non-live and unscored.\n`,
  );
}
