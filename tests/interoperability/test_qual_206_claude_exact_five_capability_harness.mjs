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
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  parseClaudeExactFiveCapabilityArguments,
  runClaudeExactFiveCapability,
} from "../../scripts/qual_206_claude_exact_five_capability_harness.mjs";
import { expectedNetworkSandboxProbeEvidence } from
  "../../scripts/qual_206_claude_capability_harness.mjs";
import {
  measureGeneratedRuntimeClosure,
  measureInstalledDependencyClosure,
} from "../../scripts/qual_206_claude_runtime_closure.mjs";

const ROOT = realpathSync(new URL("../../", import.meta.url).pathname);
const FAKE = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_fake_claude_exact_five_client.mjs",
);
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CLAUDE_EXACT_FIVE_CAPABILITY";
const OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const macRuntimeTest = process.platform === "darwin" ? test : test.skip;
const CREDENTIALS = Object.freeze([
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
]);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function currentGit(value) {
  return execFileSync("git", ["-C", ROOT, "rev-parse", value], {
    encoding: "utf8",
  }).trim();
}

function privateRoot(t) {
  const path = mkdtempSync(join(
    realpathSync(tmpdir()),
    "gis-ai-go-claude-exact-five-test-",
  ));
  chmodSync(path, 0o700);
  t.after(() => rmSync(path, { recursive: true, force: true }));
  return path;
}

function identity() {
  const bytes = readFileSync(realpathSync(process.execPath));
  return Object.freeze({ bytes: bytes.length, sha256: sha256(bytes) });
}

function options(root) {
  return Object.freeze({
    authKind: "first-party-login",
    claudeBin: realpathSync(process.execPath),
    maxBudgetUsd: null,
    model: "claude-sonnet-5",
    privateRoot: root,
    sourceCommit: currentGit("HEAD"),
  });
}

function dependencies(scenario = "positive") {
  const executable = identity();
  const environment = { ...process.env };
  for (const credential of CREDENTIALS) delete environment[credential];
  const generated = measureGeneratedRuntimeClosure(ROOT);
  return Object.freeze({
    acceptedIdentity: Object.freeze({ ...executable, version: "2.1.245" }),
    acceptedNodeIdentity: Object.freeze({
      ...executable,
      version: process.versions.node,
    }),
    authStatus: () => ({
      api_provider: "firstParty",
      auth_method: "claude.ai",
      logged_in: true,
      subscription_type: "test-profile",
    }),
    command: [realpathSync(process.execPath), FAKE],
    environment,
    extraEnvironment: {
      QUAL_206_FAKE_CLAUDE_EXACT_FIVE_SCENARIO: scenario,
      ...(scenario === "tampered-receipt"
        ? { GIS_AI_GO_QUAL_206_EXACT_FIVE_TAMPERED_RECEIPT_TEST_ONLY: "1" }
        : {}),
    },
    maximumMilliseconds: 30_000,
    networkSandboxProbe: expectedNetworkSandboxProbeEvidence(),
    parentExecutable: realpathSync(process.execPath),
    runId: randomUUID(),
    runtimeClosureBinding: Object.freeze({
      generated_first_party_closure: Object.freeze({
        ...generated,
        reference_manifest_sha256: generated.manifest_sha256,
        reference_matches_current: true,
      }),
      installed_dependency_closure: measureInstalledDependencyClosure(ROOT),
    }),
    sourceFacts: (commit) => ({
      commit,
      local_origin_main_match: true,
      protected_main_verification: "external-publication-gate",
      repository_origin: "https://github.com/chris-page-gov/gis-ai-go.git",
      tree: currentGit("HEAD^{tree}"),
    }),
    version: "2.1.245 (Claude Code)",
  });
}

test("the exact-five launcher requires its separate explicit authority", () => {
  const root = realpathSync(tmpdir());
  const args = [
    "--auth-kind", "first-party-login",
    "--claude-bin", realpathSync(process.execPath),
    "--model", "claude-sonnet-5",
    "--private-root", root,
    "--source-commit", "a".repeat(40),
  ];
  assert.throws(
    () => parseClaudeExactFiveCapabilityArguments(args, {}),
    new RegExp(`${ENABLE_FLAG}=1`, "u"),
  );
  assert.equal(
    parseClaudeExactFiveCapabilityArguments(args, { [ENABLE_FLAG]: "1" }).model,
    "claude-sonnet-5",
  );
});

macRuntimeTest("fake Claude completes the closed exact-five-v1 journey", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeExactFiveCapability(
    options(root),
    dependencies(),
  );
  assert.equal(manifest.execution.exit_code, 0, JSON.stringify({
    classification: manifest.execution.harness_classification,
    signal: manifest.execution.signal,
    stderr: readFileSync(join(root, "stderr.log"), "utf8"),
    observer: readFileSync(
      join(root, "observer", "session-1", "events.jsonl"),
      "utf8",
    ),
  }));
  assert.equal(manifest.schema,
    "gis-ai-go.qual-206-claude-exact-five-capability-private-run.v1");
  assert.equal(manifest.profile, "exact-five-v1");
  assert.equal(manifest.execution.built_in_tools_available, false);
  assert.equal(manifest.execution.maximum_turns, 6);
  assert.equal(manifest.isolation.mcp_subtree_network_access_allowed, false);
  assert.deepEqual(readdirSync(join(root, "observer")).sort(), [
    "exact-five-v1.claim.json",
    "session-1",
  ]);
  const summary = JSON.parse(readFileSync(
    join(root, "observer", "session-1", "exact-five-capability.json"),
    "utf8",
  ));
  assert.deepEqual(summary.operations.map(({ response }) => response.operation), OPERATIONS);
  assert.equal(summary.operations.length, 5);
  assert.ok(summary.operations.every(({ request, response }) =>
    request.valid === true && response.receipt_present === true &&
    response.receipt_verification_valid === true &&
    response.output_contract_valid === true &&
    response.structured_plain_text_parity === true
  ));
  assert.equal(summary.inspection_relationship.valid, true);
  assert.equal(
    summary.inspection_relationship.inspected_receipt_id,
    summary.inspection_relationship.search_receipt_id,
  );
  const output = JSON.parse(readFileSync(join(root, "stdout.json"), "utf8"));
  assert.deepEqual(output.structured_output.operation_order, OPERATIONS);
  assert.deepEqual(
    output.structured_output.receipt_ids,
    Object.fromEntries(summary.operations.map(({ response }) => [
      response.operation,
      response.receipt_id,
    ])),
  );
  assert.equal(
    output.structured_output.inspected_search_receipt_id,
    summary.inspection_relationship.search_receipt_id,
  );
});

for (const scenario of [
  "wrong-order",
  "wrong-arguments",
  "duplicate-call",
  "wrong-inspection-receipt",
]) {
  macRuntimeTest(`${scenario} fails the exact-five-v1 observer closed`, async (t) => {
    const root = privateRoot(t);
    const { manifest } = await runClaudeExactFiveCapability(
      options(root),
      dependencies(scenario),
    );
    assert.notEqual(manifest.execution.exit_code, 0);
    const events = readFileSync(
      join(root, "observer", "session-1", "events.jsonl"),
      "utf8",
    );
    assert.match(events, /capability-evidence-request-invalid/u);
  });
}

macRuntimeTest("a cryptographically invalid inline receipt fails closed", async (t) => {
  const root = privateRoot(t);
  const { manifest } = await runClaudeExactFiveCapability(
    options(root),
    dependencies("tampered-receipt"),
  );
  assert.notEqual(manifest.execution.exit_code, 0);
  const events = readFileSync(
    join(root, "observer", "session-1", "events.jsonl"),
    "utf8",
  );
  assert.match(events, /response-contract-invalid/u);
  const summary = JSON.parse(readFileSync(
    join(root, "observer", "session-1", "exact-five-capability.json"),
    "utf8",
  ));
  const describe = summary.operations.find(
    ({ response }) => response?.operation === "catalogue.describe",
  );
  assert.equal(describe.response.receipt_present, true);
  assert.equal(describe.response.receipt_verification_valid, false);
});
