import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { once } from "node:events";
import { chmodSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import test from "node:test";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import {
  closeChildAndRemoveTemporaryRoot,
  formatHumanDemo,
  isolatedChildEnvironment,
  observeChildClose,
  runLocalExactFiveDemo,
} from "../../scripts/qual_206_local_demo.mjs";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const PROVIDER_EGRESS_GUARD = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_provider_egress_guard.mjs",
);
const UNRESPONSIVE_CHILD = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_unresponsive_child.mjs",
);
const PROVIDER_MODULE_URL = pathToFileURL(join(
  ROOT,
  "packages",
  "provider-adapter-sdk",
  "dist",
  "src",
  "index.js",
)).href;
const CREDENTIAL_VARIABLES = Object.freeze([
  "OPENAI_API_KEY",
  "CODEX_API_KEY",
  "ANTHROPIC_API_KEY",
  "ANTHROPIC_AUTH_TOKEN",
  "CLAUDE_CODE_OAUTH_TOKEN",
]);
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);

function currentCommit() {
  return execFileSync(
    "git",
    ["-C", ROOT, "rev-parse", "--verify", "HEAD^{commit}"],
    { encoding: "utf8" },
  ).trim();
}

test("runs the exact-five journey as an unregistered report", { timeout: 20_000 }, async () => {
  const report = await runLocalExactFiveDemo();

  assert.equal(report.format, "gis-ai-go.local-exact-five-demo.v1");
  assert.equal(report.status, "passed");
  assert.equal(report.source_commit, currentCommit());
  assert.equal(report.source.commit, currentCommit());
  assert.equal(typeof report.source.working_tree_clean, "boolean");
  assert.equal(
    report.source.binding,
    report.source.working_tree_clean
      ? "exact-clean-head"
      : "head-with-local-changes",
  );
  assert.equal(report.protocol_version, "2026-07-28");
  assert.equal(report.transport, "operating-system-stdio-pipes");
  assert.deepEqual(report.network_boundary, {
    operating_system_isolation_enforced: false,
    guarded_provider_egress_apis_invoked: 0,
    claim_scope: "guarded-node-provider-egress-apis",
  });
  assert.deepEqual(report.discovery.tools, EXACT_OPERATIONS);
  assert.deepEqual(report.discovery.resources, [
    "catalogue.public",
    "catalogue.record",
    "evidence.receipt",
  ]);
  assert.deepEqual(
    report.journey.map(({ operation }) => operation),
    EXACT_OPERATIONS,
  );
  assert.equal(report.journey.every(({ plain_text_parity }) => plain_text_parity), true);
  assert.equal(report.journey[3].observation_value, "10471");
  assert.equal(
    report.journey[3].observation_source,
    "deterministic-fixed-ons-shaped-fixture",
  );
  assert.equal(report.evidence.ledger_event_count, 4);
  assert.equal(report.evidence.inspection_created_ledger_event, false);
  assert.deepEqual(report.provider, {
    mode: "deterministic-fixed-response",
    audited_injected_transport_calls: 1,
  });
  assert.deepEqual(report.credential_environment, {
    parent_environment_forwarded: false,
    allowed_names: [
      "GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO",
      "GIS_AI_GO_QUAL_206_SOURCE_COMMIT",
      "TMPDIR",
      "TMP",
      "TEMP",
    ],
  });
  assert.deepEqual(report.boundary, {
    state: "candidate-unregistered",
    production_registration: false,
    public_listener: false,
    registry_modified: false,
    production_entrypoint_used: false,
    activation: false,
    deployment: false,
    release: false,
  });

  const human = formatHumanDemo(report);
  assert.match(human, /exactly 5 tools verified/u);
  for (const operation of EXACT_OPERATIONS) assert.match(human, new RegExp(operation, "u"));
  assert.match(human, /candidate-unregistered/u);
  assert.match(human, /production_registration=false/u);
  assert.match(human, /no guarded provider-egress API invoked/u);
  assert.match(human, /OS network isolation: not enforced/u);
  assert.match(human, /No public listener, registry change, live provider call/u);
  assert.match(human, /Result: PASS/u);
});

test("passes only fixed controls and parent-owned temporary paths to the child", () => {
  const environment = isolatedChildEnvironment("a".repeat(40), "/tmp/gis-ai-go-demo-test");
  for (const name of CREDENTIAL_VARIABLES) {
    assert.equal(Object.hasOwn(environment, name), false);
  }
  assert.deepEqual(Object.keys(environment).sort(), [
    "GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO",
    "GIS_AI_GO_QUAL_206_SOURCE_COMMIT",
    "TEMP",
    "TMP",
    "TMPDIR",
  ]);
  assert.equal(environment.GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO, "1");
  assert.equal(environment.GIS_AI_GO_QUAL_206_SOURCE_COMMIT, "a".repeat(40));
  assert.equal(environment.TMPDIR, "/tmp/gis-ai-go-demo-test");
  assert.equal(environment.TMP, environment.TMPDIR);
  assert.equal(environment.TEMP, environment.TMPDIR);
  assert.throws(
    () => isolatedChildEnvironment("not-a-commit", "/tmp/gis-ai-go-demo-test"),
    TypeError,
  );
  assert.throws(() => isolatedChildEnvironment("a".repeat(40), "relative"), TypeError);
});

test("binds every provider-egress guard to the live transport", { timeout: 5_000 }, async () => {
  const probeSource = `
    import { Resolver } from "node:dns/promises";
    import { request as httpsRequest } from "node:https";
    import {
      ONS_EGRESS_POLICY,
      ONS_OBSERVATION_URI,
      fixedHttpsGet,
    } from ${JSON.stringify(PROVIDER_MODULE_URL)};

    try {
      await fixedHttpsGet({ policy: ONS_EGRESS_POLICY, url: ONS_OBSERVATION_URI });
    } catch {}
    const state = globalThis[Symbol.for("gis-ai-go.qual-206-provider-egress-guard")];
    const afterTransport = state.snapshot();
    const direct = [];
    for (const [name, invoke] of [
      ["dns.Resolver.resolve4", () => new Resolver().resolve4("example.invalid")],
      ["dns.Resolver.resolve6", () => new Resolver().resolve6("example.invalid")],
      ["https.request", () => httpsRequest({ hostname: "example.invalid" })],
    ]) {
      try {
        invoke();
        direct.push({ name, code: "not-blocked" });
      } catch (error) {
        direct.push({ name, code: error.code });
      }
    }
    process.stdout.write(JSON.stringify({
      afterTransport,
      direct,
      afterAll: state.snapshot(),
    }));
  `;
  const probe = spawn(
    process.execPath,
    [
      "--import",
      PROVIDER_EGRESS_GUARD,
      "--input-type=module",
      "-e",
      probeSource,
    ],
    { cwd: ROOT, env: {}, stdio: ["ignore", "pipe", "pipe"] },
  );
  const closeObservation = observeChildClose(probe);
  let stdout = "";
  let stderr = "";
  probe.stdout.setEncoding("utf8");
  probe.stderr.setEncoding("utf8");
  probe.stdout.on("data", (chunk) => { stdout += chunk; });
  probe.stderr.on("data", (chunk) => { stderr += chunk; });
  const close = await closeObservation.promise;
  assert.equal(close.signal, null);
  assert.equal(close.code, 0, stderr);
  assert.equal(closeObservation.count(), 1);
  assert.equal(stderr, "");
  const observed = JSON.parse(stdout);
  assert.deepEqual(observed.afterTransport, ["dns.Resolver.resolve4"]);
  assert.deepEqual(observed.direct, [
    { name: "dns.Resolver.resolve4", code: "GIS_AI_GO_TEST_PROVIDER_EGRESS_BLOCKED" },
    { name: "dns.Resolver.resolve6", code: "GIS_AI_GO_TEST_PROVIDER_EGRESS_BLOCKED" },
    { name: "https.request", code: "GIS_AI_GO_TEST_PROVIDER_EGRESS_BLOCKED" },
  ]);
  assert.deepEqual(observed.afterAll, [
    "dns.Resolver.resolve4",
    "dns.Resolver.resolve4",
    "dns.Resolver.resolve6",
    "https.request",
  ]);
});

test("escalates an unresponsive child to SIGKILL and removes its state", {
  timeout: 5_000,
}, async (t) => {
  const temporaryRoot = mkdtempSync(join(tmpdir(), "gis-ai-go-local-demo-cleanup-test-"));
  chmodSync(temporaryRoot, 0o700);
  const child = spawn(process.execPath, [UNRESPONSIVE_CHILD], {
    cwd: ROOT,
    env: { TMPDIR: temporaryRoot, TMP: temporaryRoot, TEMP: temporaryRoot },
    stdio: ["pipe", "ignore", "pipe", "pipe"],
  });
  const closeObservation = observeChildClose(child);
  t.after(async () => {
    if (closeObservation.count() === 0) {
      child.kill("SIGKILL");
      await Promise.race([
        closeObservation.promise,
        new Promise((resolveValue) => setTimeout(resolveValue, 1_000)),
      ]);
    }
    rmSync(temporaryRoot, { recursive: true, force: true });
  });

  const [ready] = await once(child.stdio[3], "data");
  assert.match(ready.toString("utf8"), /"event":"ready"/u);
  assert.equal(existsSync(join(
    temporaryRoot,
    "state-that-requires-parent-cleanup",
    "marker",
  )), true);

  const close = await closeChildAndRemoveTemporaryRoot(
    child,
    closeObservation,
    temporaryRoot,
    { gracefulMilliseconds: 50, terminateMilliseconds: 50, killMilliseconds: 1_000 },
  );
  assert.equal(close.stage, "sigkill");
  assert.equal(close.code, null);
  assert.equal(close.signal, "SIGKILL");
  assert.equal(closeObservation.count(), 1);
  assert.equal(existsSync(temporaryRoot), false);
});
