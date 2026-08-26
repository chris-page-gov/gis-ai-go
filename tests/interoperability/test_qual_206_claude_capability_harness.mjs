import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import {
  chmodSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  statSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import {
  buildClaudePermissionAliasMap,
  expectedNetworkSandboxProbeEvidence,
  parseClaudeCapabilityArguments,
  runClaudeCapability,
  verifyNetworkSandboxCompatibility,
} from "../../scripts/qual_206_claude_capability_harness.mjs";
import {
  capabilitySearchRequest,
} from "../../scripts/qual_206_claude_stdio_observer.mjs";
import {
  dependencyLinkTargetAllowed,
  measureGeneratedRuntimeClosure,
  measureInstalledDependencyClosure,
} from "../../scripts/qual_206_claude_runtime_closure.mjs";

const ROOT = realpathSync(new URL("../../", import.meta.url).pathname);
const FAKE = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_fake_claude_capability_client.mjs",
);
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CLAUDE_CAPABILITY";
const macRuntimeTest = process.platform === "darwin" ? test : test.skip;
const POSITIVE_TEST_NAME =
  "fake Claude completes one bounded HOST-002 call with a verified receipt";
const NO_CALL_TEST_NAME =
  "matching final text without an MCP call cannot create a capability claim";
const WRONG_OUTPUT_TEST_NAME =
  "a model answer with a changed receipt cannot match the observed MCP result";
const CREDENTIALS = [
  "OPENAI_API_KEY",
  "CODEX_API_KEY",
  "ANTHROPIC_API_KEY",
  "ANTHROPIC_AUTH_TOKEN",
  "CLAUDE_CODE_OAUTH_TOKEN",
  "AWS_ACCESS_KEY_ID",
  "AWS_SECRET_ACCESS_KEY",
  "AWS_SESSION_TOKEN",
  "GOOGLE_APPLICATION_CREDENTIALS",
  "AZURE_CLIENT_SECRET",
];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function currentCommit() {
  return execFileSync("git", ["-C", ROOT, "rev-parse", "HEAD"], {
    encoding: "utf8",
  }).trim();
}

function currentTree() {
  return execFileSync("git", ["-C", ROOT, "rev-parse", "HEAD^{tree}"], {
    encoding: "utf8",
  }).trim();
}

function privateRoot(t) {
  const path = mkdtempSync(join(realpathSync(tmpdir()), "gis-ai-go-claude-capability-test-"));
  chmodSync(path, 0o700);
  t.after(() => rmSync(path, { recursive: true, force: true }));
  return path;
}

function nodeIdentity() {
  const path = realpathSync(process.execPath);
  const bytes = readFileSync(path);
  return Object.freeze({
    bytes: bytes.length,
    sha256: sha256(bytes),
    version: "2.1.245",
  });
}

function closedEnvironment() {
  const environment = { ...process.env };
  for (const name of CREDENTIALS) delete environment[name];
  return environment;
}

function options(root) {
  return Object.freeze({
    authKind: "first-party-login",
    claudeBin: realpathSync(process.execPath),
    maxBudgetUsd: null,
    model: "claude-sonnet-5",
    privateRoot: root,
    sourceCommit: currentCommit(),
  });
}

function dependencies(scenario = "positive") {
  return Object.freeze({
    acceptedIdentity: nodeIdentity(),
    acceptedNodeIdentity: Object.freeze({
      ...nodeIdentity(),
      version: process.versions.node,
    }),
    authStatus: (_command, environment) => {
      assert.equal(environment.CLAUDE_CODE_SIMPLE, undefined);
      assert.equal(environment.CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC, "1");
      assert.equal(environment.MCP_PROTOCOL_NEGOTIATION, "auto");
      assert.equal(environment.MCP_SDK_GENERATION, "v2");
      return {
        api_provider: "firstParty",
        auth_method: "claude.ai",
        logged_in: true,
        subscription_type: "test-profile",
      };
    },
    command: [realpathSync(process.execPath), FAKE],
    environment: closedEnvironment(),
    extraEnvironment: { QUAL_206_FAKE_CLAUDE_SCENARIO: scenario },
    maximumMilliseconds: 30_000,
    networkSandboxProbe: expectedNetworkSandboxProbeEvidence(),
    parentExecutable: realpathSync(process.execPath),
    runId: randomUUID(),
    runtimeClosureBinding: Object.freeze({
      generated_first_party_closure: Object.freeze({
        ...measureGeneratedRuntimeClosure(ROOT),
        reference_manifest_sha256: measureGeneratedRuntimeClosure(ROOT).manifest_sha256,
        reference_matches_current: true,
      }),
      installed_dependency_closure: measureInstalledDependencyClosure(ROOT),
    }),
    sourceFacts: (commit) => ({
      commit,
      local_origin_main_match: true,
      protected_main_verification: "external-publication-gate",
      repository_origin: "https://github.com/chris-page-gov/gis-ai-go.git",
      tree: currentTree(),
    }),
    version: "2.1.245 (Claude Code)",
  });
}

test("production arguments distinguish first-party login from API spend", () => {
  const root = realpathSync(tmpdir());
  const binary = realpathSync(process.execPath);
  const base = [
    "--auth-kind", "first-party-login",
    "--claude-bin", binary,
    "--model", "claude-sonnet-5",
    "--private-root", root,
    "--source-commit", "a".repeat(40),
  ];
  const parsed = parseClaudeCapabilityArguments(base, { [ENABLE_FLAG]: "1" });
  assert.equal(parsed.authKind, "first-party-login");
  assert.equal(parsed.maxBudgetUsd, null);
  assert.throws(
    () => parseClaudeCapabilityArguments(
      [...base, "--max-budget-usd", "1.00"],
      { [ENABLE_FLAG]: "1" },
    ),
    /invalid argument set/u,
  );
  assert.throws(
    () => parseClaudeCapabilityArguments(
      base.map((value) => value === "claude-sonnet-5" ? "sonnet" : value),
      { [ENABLE_FLAG]: "1" },
    ),
    /pinned capability profile/u,
  );
  assert.throws(() => parseClaudeCapabilityArguments(base, {}), /refusing/u);
});

test("Claude permission aliases preserve canonical MCP names and reject collisions", () => {
  assert.deepEqual(
    buildClaudePermissionAliasMap("gis-ai-go", ["catalogue.search", "data.query"]),
    {
      "catalogue.search": "mcp__gis-ai-go__catalogue_search",
      "data.query": "mcp__gis-ai-go__data_query",
    },
  );
  assert.throws(
    () => buildClaudePermissionAliasMap(
      "gis-ai-go",
      ["catalogue.search", "catalogue_search"],
    ),
    /permission alias collision/u,
  );
  assert.throws(
    () => buildClaudePermissionAliasMap("gis-ai-go", ["catalogue/search"]),
    /MCP 2026-07-28 naming guidance/u,
  );
  const prototypeName = buildClaudePermissionAliasMap("gis-ai-go", ["__proto__"]);
  assert.equal(Object.hasOwn(prototypeName, "__proto__"), true);
  assert.equal(prototypeName["__proto__"], "mcp__gis-ai-go____proto__");
});

test("Claude capability calls accept bounded extension metadata", () => {
  const request = capabilitySearchRequest({
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {
      name: "catalogue.search",
      arguments: { query: "INSPIRE", limit: 1 },
      _meta: {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
          name: "Claude Code",
          version: "2.1.245",
          title: "Claude Code",
        },
        "com.anthropic/toolUseId": "bounded-test-value",
      },
    },
  });
  assert.equal(request.valid, true);
  assert.equal(request.protocol_valid, true);
  assert.equal(request.client_attribution_valid, true);
  assert.equal(request.evidence_request_valid, true);
  assert.equal(
    capabilitySearchRequest({
      method: "tools/call",
      params: {
        name: "catalogue.search",
        arguments: { query: "INSPIRE", limit: 1 },
        _meta: {
          "io.modelcontextprotocol/clientCapabilities": {},
          "io.modelcontextprotocol/clientInfo": { name: "Claude Code", version: "2.1.245" },
        },
      },
    }).valid,
    false,
  );
  const unattributed = capabilitySearchRequest({
    method: "tools/call",
    params: {
      name: "catalogue.search",
      arguments: { query: "INSPIRE", limit: 1 },
      _meta: {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
      },
    },
  });
  assert.equal(unattributed.protocol_valid, true);
  assert.equal(unattributed.client_attribution_valid, false);
  assert.equal(unattributed.valid, false);

  const invalidMetaKey = capabilitySearchRequest({
    method: "tools/call",
    params: {
      name: "catalogue.search",
      arguments: { query: "INSPIRE", limit: 1 },
      _meta: {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": { name: "Claude Code", version: "2.1.245" },
        "not a valid meta key": "rejected",
      },
    },
  });
  assert.equal(invalidMetaKey.protocol_valid, false);
  assert.equal(invalidMetaKey.valid, false);

  const unexpectedParams = capabilitySearchRequest({
    method: "tools/call",
    params: {
      name: "catalogue.search",
      arguments: { query: "INSPIRE", limit: 1 },
      requestState: "unbound-state",
      _meta: {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": { name: "Claude Code", version: "2.1.245" },
      },
    },
  });
  assert.equal(unexpectedParams.protocol_valid, true);
  assert.equal(unexpectedParams.evidence_request_valid, false);
  assert.equal(unexpectedParams.valid, false);
});

test("dependency links stay inside measured dependencies or exact workspaces", () => {
  const root = "/private/tmp/gis-ai-go-dependency-link-rule";
  assert.equal(
    dependencyLinkTargetAllowed(root, join(root, "node_modules", ".pnpm", "zod")),
    true,
  );
  assert.equal(
    dependencyLinkTargetAllowed(root, join(root, "packages", "evidence")),
    true,
  );
  assert.equal(
    dependencyLinkTargetAllowed(root, join(root, "packages", "evidence", "ignored.js")),
    false,
  );
  assert.equal(
    dependencyLinkTargetAllowed(root, join(root, "ignored-runtime", "payload.js")),
    false,
  );
  assert.equal(
    dependencyLinkTargetAllowed(root, resolve(root, "..", "outside-root")),
    false,
  );
});

macRuntimeTest("the exact macOS sandbox preserves durable writes and denies loopback", async () => {
  assert.deepEqual(
    await verifyNetworkSandboxCompatibility(),
    expectedNetworkSandboxProbeEvidence(),
  );
});

macRuntimeTest(POSITIVE_TEST_NAME, async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), dependencies());
  assert.equal(
    manifest.execution.exit_code,
    0,
    readFileSync(join(root, "stderr.log"), "utf8"),
  );
  assert.equal(manifest.execution.harness_classification, null);
  assert.equal(manifest.execution.built_in_tools_available, false);
  assert.equal(manifest.execution.allowed_mcp_tool,
    "mcp__gis-ai-go-qual-206-host-002__catalogue_search");
  assert.equal(manifest.host.auth_preflight.auth_method, "claude.ai");
  assert.equal(manifest.host.api_budget_usd, null);
  assert.deepEqual(readdirSync(join(root, "observer")).sort(), [
    "catalogue-search.claim.json",
    "session-1",
    "session-2",
  ]);
  const capability = JSON.parse(
    readFileSync(join(root, "observer", "session-2", "capability.json"), "utf8"),
  );
  assert.equal(capability.request.observed, true);
  assert.equal(capability.request.valid, true);
  assert.equal(capability.response.contract_valid, true);
  assert.equal(capability.response.receipt_verification_valid, true);
  assert.equal(capability.response.record_id, "hmlr:dataset:inspire-index-polygons");
  assert.equal(capability.response.title, "Index polygons spatial data (INSPIRE)");
  assert.match(
    capability.response.receipt_id,
    /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
  );
  const output = JSON.parse(readFileSync(join(root, "stdout.json"), "utf8"));
  assert.equal(output.structured_output.receipt_id, capability.response.receipt_id);
  assert.deepEqual(readdirSync(join(root, "workspace")), []);
  for (const name of [
    "mcp.json",
    "settings.json",
    "stdout.json",
    "stderr.log",
    "run-manifest.json",
  ]) {
    assert.equal(statSync(join(root, name)).mode & 0o777, 0o600, name);
  }
  const mcp = JSON.parse(readFileSync(join(root, "mcp.json"), "utf8"));
  const server = mcp.mcpServers["gis-ai-go-qual-206-host-002"];
  assert.equal(Object.keys(mcp.mcpServers).length, 1);
  for (const credential of CREDENTIALS) {
    const index = server.args.indexOf(credential);
    assert.ok(index > 0 && server.args[index - 1] === "-u", credential);
  }
  for (const clientOnlyVariable of [
    "MCP_PROTOCOL_NEGOTIATION",
    "MCP_SDK_GENERATION",
  ]) {
    const index = server.args.indexOf(clientOnlyVariable);
    assert.ok(
      index > 0 && server.args[index - 1] === "-u",
      clientOnlyVariable,
    );
  }
});

macRuntimeTest(NO_CALL_TEST_NAME, async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), dependencies("no-call"));
  assert.equal(manifest.execution.exit_code, 0);
  assert.deepEqual(readdirSync(join(root, "observer")), ["session-1"]);
  const capability = JSON.parse(
    readFileSync(join(root, "observer", "session-1", "capability.json"), "utf8"),
  );
  assert.equal(capability.request.observed, false);
  assert.equal(capability.response.observed, false);
});

macRuntimeTest(WRONG_OUTPUT_TEST_NAME, async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), dependencies("wrong-output"));
  assert.equal(manifest.execution.exit_code, 0);
  const capability = JSON.parse(
    readFileSync(join(root, "observer", "session-2", "capability.json"), "utf8"),
  );
  const output = JSON.parse(readFileSync(join(root, "stdout.json"), "utf8"));
  assert.equal(capability.response.receipt_verification_valid, true);
  assert.notEqual(output.structured_output.receipt_id, capability.response.receipt_id);
});

macRuntimeTest("a second tool call is rejected by the global one-call claim", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), dependencies("second-call"));
  assert.notEqual(manifest.execution.exit_code, 0);
  assert.ok(readdirSync(join(root, "observer")).includes("catalogue-search.claim.json"));
  const events = readFileSync(
    join(root, "observer", "session-2", "events.jsonl"),
    "utf8",
  );
  assert.match(events, /capability-second-call-in-session/u);
});

macRuntimeTest("a valid call in a later MCP session is rejected by the global claim", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(
    options(root),
    dependencies("cross-session-second-call"),
  );
  assert.notEqual(manifest.execution.exit_code, 0);
  assert.deepEqual(readdirSync(join(root, "observer")).sort(), [
    "catalogue-search.claim.json",
    "session-1",
    "session-2",
    "session-3",
  ]);
  const events = readFileSync(
    join(root, "observer", "session-3", "events.jsonl"),
    "utf8",
  );
  assert.match(events, /capability-call-already-claimed/u);
});

for (const [scenario, anomaly] of [
  ["wrong-query", "capability-evidence-request-invalid"],
  ["wrong-operation", "capability-evidence-request-invalid"],
]) {
  macRuntimeTest(`${scenario} cannot create a valid capability observation`, async (t) => {
    const root = privateRoot(t);
    const { manifest } = await runClaudeCapability(options(root), dependencies(scenario));
    assert.notEqual(manifest.execution.exit_code, 0);
    const events = readFileSync(
      join(root, "observer", "session-2", "events.jsonl"),
      "utf8",
    );
    assert.match(events, new RegExp(anomaly, "u"));
  });
}

macRuntimeTest("a surviving descendant is terminated when the bounded run expires", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), {
    ...dependencies("hanging-descendant"),
    maximumMilliseconds: 200,
  });
  assert.equal(manifest.execution.harness_classification, "run-timeout");
  assert.equal(manifest.execution.process_group_absent, true);
});

macRuntimeTest("a capture write failure terminates the detached process group", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), {
    ...dependencies(),
    captureWriter: () => {
      const error = new Error("synthetic full disk");
      error.code = "ENOSPC";
      throw error;
    },
  });
  assert.equal(manifest.execution.harness_classification, "stdout-capture-write-failed");
  assert.equal(manifest.execution.process_group_absent, true);
  assert.equal(manifest.execution.stdout.limit_exceeded, true);
});

macRuntimeTest("a signal received before spawn is applied to the new process group", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), {
    ...dependencies(),
    beforeSpawn: () => process.emit("SIGTERM"),
  });
  assert.equal(manifest.execution.interrupted_signal, "SIGTERM");
  assert.equal(manifest.execution.harness_classification, "launcher-sigterm");
  assert.equal(manifest.execution.process_group_absent, true);
});

macRuntimeTest("a prompt-stream failure terminates the detached process group", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeCapability(options(root), {
    ...dependencies(),
    beforePrompt: (child) => {
      const error = new Error("synthetic broken input pipe");
      error.code = "EPIPE";
      child.stdin.emit("error", error);
    },
  });
  assert.equal(manifest.execution.harness_classification, "stdin-stream-failed");
  assert.equal(manifest.execution.process_group_absent, true);
});
