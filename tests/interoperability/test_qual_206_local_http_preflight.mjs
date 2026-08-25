import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import {
  assertLocalHttpSourceMaterialsMatchTree,
  bindExecutedLocalHttpSourceMaterials,
  localHttpSourceState,
  runLocalHttpPreflightCapture,
  snapshotLocalHttpSourceMaterials,
} from "../../scripts/qual_206_local_http_preflight.mjs";
import {
  publicIdempotencyKeySha256,
} from "../../packages/evidence/dist/src/index.js";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const SCHEMA_VALIDATION_ID = "gis-ai-go.qual-206-local-http-schema-validation.v1";

function validateAdvertisedToolSchemas(tools) {
  return spawnSync(
    process.execPath,
    ["scripts/qual_206_validate_local_http_schemas.mjs", "--stdin-tools-list-only"],
    {
      cwd: ROOT,
      encoding: "utf8",
      env: { ...process.env, CI: "1", NO_COLOR: "1" },
      input: JSON.stringify(tools),
      stdio: ["pipe", "pipe", "pipe"],
      timeout: 10_000,
    },
  );
}

function assertSchemaValidation(result, valid) {
  assert.equal(result.error, undefined);
  assert.equal(result.signal, null);
  assert.equal(result.status, valid ? 0 : 1, result.stderr);
  assert.equal(result.stderr, "");
  assert.deepEqual(JSON.parse(result.stdout), {
    schema: SCHEMA_VALIDATION_ID,
    valid,
  });
}

function replayPrivateCapture(capture) {
  const programme = [
    "import importlib.util, json, pathlib, sys",
    "path = pathlib.Path('scripts/qual_206_verify_local_http_preflight.py').resolve()",
    "spec = importlib.util.spec_from_file_location('qual_206_http_replay', path)",
    "module = importlib.util.module_from_spec(spec)",
    "spec.loader.exec_module(module)",
    "module.replay_capture(json.load(sys.stdin))",
  ].join("\n");
  return spawnSync(
    "uv",
    [
      "run",
      "--locked",
      "--cache-dir",
      ".uv-cache",
      "python",
      "-c",
      programme,
    ],
    {
      cwd: ROOT,
      encoding: "utf8",
      env: { ...process.env, UV_OFFLINE: "1" },
      input: JSON.stringify(capture),
      stdio: ["pipe", "pipe", "pipe"],
      timeout: 20_000,
    },
  );
}

test(
  "captures the exact-five synthetic capability journey through a real loopback HTTP socket",
  { timeout: 45_000 },
  async (t) => {
    const root = mkdtempSync(join(tmpdir(), "gis-ai-go-local-http-test-"));
    chmodSync(root, 0o700);
    t.after(() => rmSync(root, { recursive: true, force: true }));
    const capturePath = join(root, "private-capture.json");
    const publicPath = join(root, "public-projection.json");

    const capture = await runLocalHttpPreflightCapture(capturePath);
    const state = lstatSync(capturePath);
    assert.equal(state.isFile(), true);
    assert.equal(state.isSymbolicLink(), false);
    assert.equal(state.uid, process.getuid?.());
    assert.equal(state.nlink, 1);
    assert.equal(state.mode & 0o777, 0o600);
    assert.deepEqual(capture, JSON.parse(readFileSync(capturePath, "utf8")));
    assert.equal(capture.schema, "gis-ai-go.qual-206-local-http-private-capture.v1");
    assert.equal(capture.source_materials.length, 12);
    for (const material of capture.source_materials) {
      assert.equal(material.sha256_before_execution, material.sha256_after_execution);
      assert.match(material.sha256_before_execution, /^[0-9a-f]{64}$/u);
    }
    assert.equal(capture.requests.length, 14);
    assert.equal(capture.requests[12].transport_outcome, "client-aborted");
    assert.equal(capture.requests[12].response_json, null);
    assert.equal(capture.requests[13].transport_outcome, "response");
    assert.equal(JSON.parse(capture.requests[13].response_json).error.code, -32601);
    assert.equal(capture.audit_lines.length, 9);
    const auditEvents = capture.audit_lines.map((line) => JSON.parse(line));
    const summary = auditEvents
      .find(({ event }) => event === "session-summary");
    assert.notEqual(summary, undefined);
    assert.deepEqual(summary.operations, EXACT_OPERATIONS);
    assert.equal(summary.provider_transport_calls, 2);
    assert.equal(summary.aborted_provider_calls, 1);
    assert.equal(summary.ledger_event_count, 4);
    assert.equal(summary.reported_error_count, 0);
    assert.equal(summary.guarded_api_invocation_count, 0);
    const idempotencyEvidence = auditEvents.filter(
      ({ event }) => event === "idempotency-evidence-state",
    );
    assert.equal(idempotencyEvidence.length, 2);
    const successfulArguments = JSON.parse(capture.requests[9].request_json)
      .params.arguments;
    const abortedArguments = JSON.parse(capture.requests[12].request_json)
      .params.arguments;
    const successfulReceipt = JSON.parse(capture.requests[9].response_json)
      .result.structuredContent.evidence_receipt.receipt_id;
    assert.equal(idempotencyEvidence[0].role, "successful");
    assert.equal(
      idempotencyEvidence[0].idempotency_key_sha256,
      publicIdempotencyKeySha256(successfulArguments.idempotency_key),
    );
    assert.equal(idempotencyEvidence[0].reconciliation_status, "completed");
    assert.equal(idempotencyEvidence[0].completed_evidence_created, true);
    assert.equal(idempotencyEvidence[0].receipt_id, successfulReceipt);
    assert.equal(idempotencyEvidence[0].ledger_event_sequence, 4);
    assert.equal(idempotencyEvidence[1].role, "aborted");
    assert.equal(
      idempotencyEvidence[1].idempotency_key_sha256,
      publicIdempotencyKeySha256(abortedArguments.idempotency_key),
    );
    assert.equal(idempotencyEvidence[1].reconciliation_status, "pending");
    assert.equal(idempotencyEvidence[1].completed_evidence_created, false);
    assert.equal(idempotencyEvidence[1].resolution_id, null);
    assert.equal(idempotencyEvidence[1].receipt_id, null);
    assert.equal(idempotencyEvidence[1].record_id, null);
    assert.equal(idempotencyEvidence[1].ledger_event_id, null);
    assert.equal(idempotencyEvidence[1].ledger_event_sequence, null);
    assert.equal(
      capture.audit_lines.some((line) =>
        line.includes(successfulArguments.idempotency_key) ||
        line.includes(abortedArguments.idempotency_key)),
      false,
    );
    assert.equal(capture.fixture.host, "127.0.0.1");
    assert.equal(capture.openapi.http_status, 200);
    assert.equal(capture.readiness.http_status, 200);
    assert.equal(capture.child.exit_code, 0);
    assert.equal(capture.child.stdout, "");
    assert.equal(capture.child.stderr, "");

    const advertisedTools = JSON.parse(capture.requests[1].response_json).result.tools;
    assertSchemaValidation(validateAdvertisedToolSchemas(advertisedTools), true);
    await t.test("canonical comparison rejects an advertised input-schema tamper", () => {
      const tampered = structuredClone(advertisedTools);
      const tool = tampered.find(({ name }) => name === "catalogue.search");
      assert.notEqual(tool, undefined);
      tool.inputSchema = { type: "object", additionalProperties: true };
      assertSchemaValidation(validateAdvertisedToolSchemas(tampered), false);
    });
    await t.test("canonical comparison rejects an advertised output-schema tamper", () => {
      const tampered = structuredClone(advertisedTools);
      const tool = tampered.find(({ name }) => name === "catalogue.search");
      assert.notEqual(tool, undefined);
      tool.outputSchema = { type: "object", additionalProperties: true };
      assertSchemaValidation(validateAdvertisedToolSchemas(tampered), false);
    });
    const privateReplay = replayPrivateCapture(capture);
    assert.equal(privateReplay.error, undefined);
    assert.equal(privateReplay.signal, null);
    assert.equal(privateReplay.status, 0, privateReplay.stderr);
    assert.equal(privateReplay.stdout, "");
    assert.equal(privateReplay.stderr, "");

    const verification = spawnSync(
      "uv",
      [
        "run",
        "--locked",
        "--cache-dir",
        ".uv-cache",
        "python",
        "scripts/qual_206_verify_local_http_preflight.py",
        "--capture",
        capturePath,
        "--public-output",
        publicPath,
      ],
      {
        cwd: ROOT,
        encoding: "utf8",
        env: { ...process.env, UV_OFFLINE: "1" },
        stdio: ["ignore", "pipe", "pipe"],
        timeout: 20_000,
      },
    );
    if (capture.source.working_tree_clean) {
      assert.equal(verification.status, 0, verification.stderr);
      const projection = JSON.parse(readFileSync(publicPath, "utf8"));
      assert.equal(projection.evidence_classification, "local-http-transport-preflight");
      assert.equal(projection.source.working_tree_clean, true);
      assert.equal(projection.source.complete_runtime_source_binding, false);
      assert.equal(projection.transport.remote_host_acceptance, false);
      assert.equal(projection.claims.claude_code_capability, "unscored");
      assert.equal(projection.claims.model_capability, "unscored");
      assert.equal(projection.claims.deployment_performed, false);
      assert.equal(projection.verification.private_capture_published, false);
      assert.equal(
        projection.validation.openapi_callable_contract_exact,
        true,
      );
      assert.equal(
        projection.journey.cancellation
          .successful_request_completed_evidence_created,
        true,
      );
      assert.equal(
        projection.journey.cancellation.completed_evidence_created,
        false,
      );
      assert.equal(
        projection.journey.cancellation.private_idempotency_attribution_replayed,
        true,
      );
      const projectionJson = JSON.stringify(projection);
      assert.equal(projectionJson.includes(capturePath), false);
      assert.equal(projectionJson.includes("127.0.0.1"), false);
      assert.equal(projectionJson.includes(successfulArguments.idempotency_key), false);
      assert.equal(projectionJson.includes(abortedArguments.idempotency_key), false);
      assert.equal(
        projectionJson.includes(idempotencyEvidence[0].idempotency_key_sha256),
        false,
      );
      assert.equal(
        projectionJson.includes(idempotencyEvidence[1].idempotency_key_sha256),
        false,
      );
    } else {
      assert.equal(verification.status, 1);
      assert.match(verification.stderr, /requires a clean capture source/u);
      assert.equal(existsSync(publicPath), false);
    }
  },
);

test("refuses capture without the explicit private-capture authority", () => {
  const rejected = spawnSync(
    process.execPath,
    ["scripts/qual_206_local_http_preflight.mjs", "--capture", "/tmp/unused.json"],
    {
      cwd: ROOT,
      encoding: "utf8",
      env: {},
      stdio: ["ignore", "pipe", "pipe"],
      timeout: 5_000,
    },
  );
  assert.notEqual(rejected.status, 0);
  assert.equal(rejected.stdout, "");
  assert.match(rejected.stderr, /Refusing private capture/u);
});

test("fails closed when a runtime material changes between execution snapshots", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-material-race-test-"));
  chmodSync(root, 0o700);
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const relativePath = "ignored-runtime.js";
  const runtimePath = join(root, relativePath);
  writeFileSync(runtimePath, "export const state = 'before';\n", { mode: 0o600 });
  const before = snapshotLocalHttpSourceMaterials(root, [relativePath]);
  writeFileSync(runtimePath, "export const state = 'after';\n", { mode: 0o600 });
  const after = snapshotLocalHttpSourceMaterials(root, [relativePath]);
  assert.throws(
    () => bindExecutedLocalHttpSourceMaterials(before, after),
    /changed during observed execution/u,
  );
});

test("rejects clean-source claims hidden by index flags or changed tree blobs", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-git-source-test-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const git = (...argumentsValue) => execFileSync(
    "/usr/bin/git",
    argumentsValue,
    {
      cwd: root,
      encoding: "utf8",
      env: { LANG: "C", LC_ALL: "C", PATH: "/usr/bin:/bin" },
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  git("init", "--quiet");
  const materialPath = join(root, "material.txt");
  writeFileSync(materialPath, "recorded\n", { mode: 0o600 });
  git("add", "material.txt");
  git(
    "-c",
    "user.name=QUAL-206 test",
    "-c",
    "user.email=qual-206@example.invalid",
    "commit",
    "--quiet",
    "-m",
    "test fixture",
  );
  const source = localHttpSourceState(root);
  git("update-index", "--assume-unchanged", "material.txt");
  writeFileSync(materialPath, "modified but hidden\n", { mode: 0o600 });
  const materials = snapshotLocalHttpSourceMaterials(root, ["material.txt"]);
  assert.throws(() => localHttpSourceState(root), /index state/u);
  assert.throws(
    () => assertLocalHttpSourceMaterialsMatchTree(source, materials, root),
    /recorded Git tree blob/u,
  );
});

test("ignores Git replacement refs when resolving the recorded object graph", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-git-replace-test-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const git = (...argumentsValue) => execFileSync(
    "/usr/bin/git",
    argumentsValue,
    {
      cwd: root,
      encoding: "utf8",
      env: { LANG: "C", LC_ALL: "C", PATH: "/usr/bin:/bin" },
      stdio: ["ignore", "pipe", "pipe"],
    },
  ).trim();
  git("init", "--quiet");
  const materialPath = join(root, "material.txt");
  writeFileSync(materialPath, "recorded\n", { mode: 0o600 });
  git("add", "material.txt");
  git(
    "-c",
    "user.name=QUAL-206 test",
    "-c",
    "user.email=qual-206@example.invalid",
    "commit",
    "--quiet",
    "-m",
    "recorded fixture",
  );
  const recordedCommit = git("rev-parse", "HEAD");
  const recordedTree = git("rev-parse", "HEAD^{tree}");
  writeFileSync(materialPath, "replacement\n", { mode: 0o600 });
  git("add", "material.txt");
  git(
    "-c",
    "user.name=QUAL-206 test",
    "-c",
    "user.email=qual-206@example.invalid",
    "commit",
    "--quiet",
    "-m",
    "replacement fixture",
  );
  const replacementCommit = git("rev-parse", "HEAD");
  git("checkout", "--quiet", "--detach", recordedCommit);
  git("replace", recordedCommit, replacementCommit);
  const source = localHttpSourceState(root);
  assert.equal(source.commit, recordedCommit);
  assert.equal(source.tree, recordedTree);
  assert.equal(source.working_tree_clean, true);
});

test("refuses private capture paths inside the repository, including ignored paths", async (t) => {
  const ignoredRoot = mkdtempSync(join(ROOT, "node_modules/qual-206-private-path-"));
  chmodSync(ignoredRoot, 0o700);
  t.after(() => rmSync(ignoredRoot, { recursive: true, force: true }));
  await assert.rejects(
    runLocalHttpPreflightCapture(join(ignoredRoot, "private-capture.json")),
    /outside the repository/u,
  );
});

test("refuses a symbolic-link capture parent that resolves inside the repository", async (t) => {
  const ignoredRoot = mkdtempSync(join(ROOT, "node_modules/qual-206-private-target-"));
  const externalRoot = mkdtempSync(join(tmpdir(), "gis-ai-go-private-alias-"));
  chmodSync(ignoredRoot, 0o700);
  chmodSync(externalRoot, 0o700);
  t.after(() => rmSync(externalRoot, { recursive: true, force: true }));
  t.after(() => rmSync(ignoredRoot, { recursive: true, force: true }));
  const alias = join(externalRoot, "repository-target");
  symlinkSync(ignoredRoot, alias, "dir");
  await assert.rejects(
    runLocalHttpPreflightCapture(join(alias, "private-capture.json")),
    /must not traverse a symbolic link/u,
  );
});

test("refuses an existing capture symlink that targets a repository file", async (t) => {
  const externalRoot = mkdtempSync(join(tmpdir(), "gis-ai-go-private-file-alias-"));
  chmodSync(externalRoot, 0o700);
  t.after(() => rmSync(externalRoot, { recursive: true, force: true }));
  const alias = join(externalRoot, "private-capture.json");
  symlinkSync(join(ROOT, "scripts/qual_206_local_http_preflight.mjs"), alias, "file");
  await assert.rejects(
    runLocalHttpPreflightCapture(alias),
    /must not link into the repository/u,
  );
});
