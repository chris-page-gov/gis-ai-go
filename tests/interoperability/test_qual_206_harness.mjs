import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { once } from "node:events";
import { mkdtemp, readFile, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const SERVER = join(ROOT, "scripts", "qual_206_conformance_server.mjs");
const PROXY = join(ROOT, "scripts", "qual_206_telemetry_proxy.mjs");
const CASES = join(ROOT, "tests", "interoperability", "qual_206_cases.json");
const CHATGPT_EVIDENCE = join(
  ROOT,
  "tests",
  "interoperability",
  "evidence",
  "chatgpt-tunnel-2026-08-20.json",
);
const INDEPENDENT_HOST_EVIDENCE = join(
  ROOT,
  "tests",
  "interoperability",
  "evidence",
  "independent-host-readiness-2026-08-20.json",
);
const CODEX_HOST_EVIDENCE = join(
  ROOT,
  "tests",
  "interoperability",
  "evidence",
  "codex-cli-2026-08-20.json",
);
const SOURCE_COMMIT = "66507f9a6e6c0da23a8af4682268f9362d93bc06";
const META = {
  "io.modelcontextprotocol/protocolVersion": "2026-07-28",
  "io.modelcontextprotocol/clientCapabilities": {},
  "io.modelcontextprotocol/clientInfo": {
    name: "gis-ai-go-qual-206-test",
    version: "1.0.0",
  },
};

function run(command, args, options = {}) {
  const child = spawn(command, args, {
    cwd: ROOT,
    env: { ...process.env, ...options.env },
    stdio: ["pipe", "pipe", "pipe"],
  });
  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });
  if (options.input !== undefined) child.stdin.end(options.input);
  return { child, output: () => ({ stderr, stdout }) };
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

test("conformance server fails closed without the explicit test flag", async () => {
  const invocation = run(process.execPath, [SERVER], {
    env: { GIS_AI_GO_QUAL_206_SOURCE_COMMIT: SOURCE_COMMIT },
    input: "",
  });
  const [code] = await once(invocation.child, "exit");
  const { stderr, stdout } = invocation.output();
  assert.notEqual(code, 0);
  assert.equal(stdout, "");
  assert.match(stderr, /GIS_AI_GO_QUAL_206_CONFORMANCE=1/u);
});

test("proxy records minimised telemetry for a real deterministic tool call", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const requests = [
    {
      jsonrpc: "2.0",
      id: 1,
      method: "server/discover",
      params: { _meta: META },
    },
    {
      jsonrpc: "2.0",
      id: 2,
      method: "tools/call",
      params: {
        _meta: META,
        name: "catalogue.search",
        arguments: { query: "INSPIRE", limit: 20 },
      },
    },
  ];
  const input = `${requests.map((value) => JSON.stringify(value)).join("\n")}\n`;
  const invocation = run(
    process.execPath,
    [
      PROXY,
      "--log",
      telemetry,
      "--client",
      "node-test",
      "--",
      process.execPath,
      SERVER,
    ],
    {
      env: {
        GIS_AI_GO_QUAL_206_CONFORMANCE: "1",
        GIS_AI_GO_QUAL_206_SOURCE_COMMIT: SOURCE_COMMIT,
        QUAL_206_UNRELATED_ENV: "sentinel-value-must-not-be-recorded",
      },
      input,
    },
  );
  const [code] = await once(invocation.child, "exit");
  const { stderr, stdout } = invocation.output();
  assert.equal(code, 0, stderr);
  assert.equal(stderr, "");

  const replies = stdout.trim().split("\n").map((line) => JSON.parse(line));
  assert.equal(replies.length, 2);
  assert.deepEqual(replies[0].result.supportedVersions, ["2026-07-28"]);
  const structured = replies[1].result.structuredContent;
  assert.equal(
    structured.data.records[0].id,
    "hmlr:dataset:inspire-index-polygons",
  );
  assert.match(
    structured.evidence_receipt.receipt_id,
    /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
  );

  const logText = await readFile(telemetry, "utf8");
  const events = logText.trim().split("\n").map((line) => JSON.parse(line));
  assert.equal(events[0].event, "session_start");
  assert.equal(events[0].source_commit, SOURCE_COMMIT);
  assert.equal(events.at(-1).event, "session_end");
  assert.deepEqual(
    events.filter((event) => event.event === "request").map((event) => event.method),
    ["server/discover", "tools/call"],
  );
  assert.equal(
    events.find((event) => event.operation === "catalogue.search")?.parameters_sha256
      ?.length,
    64,
  );
  assert.equal(events.filter((event) => event.event === "response").length, 2);
  assert.doesNotMatch(logText, /INSPIRE/u);
  assert.doesNotMatch(logText, /inspire-index-polygons/u);
  assert.doesNotMatch(logText, /sentinel-value/u);
  assert.equal((await stat(telemetry)).mode & 0o777, 0o600);
});

test("proxy does not reflect malformed source identity into telemetry", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-source-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const invocation = run(
    process.execPath,
    [
      PROXY,
      "--log",
      telemetry,
      "--client",
      "source-test",
      "--",
      process.execPath,
      "--eval",
      "",
    ],
    {
      env: {
        GIS_AI_GO_QUAL_206_SOURCE_COMMIT: "not-a-commit\nsecret-looking-text",
      },
      input: "",
    },
  );
  const [code] = await once(invocation.child, "exit");
  assert.equal(code, 0);
  const events = (await readFile(telemetry, "utf8"))
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
  assert.equal(events[0].source_commit, "unknown");
  assert.doesNotMatch(JSON.stringify(events), /secret-looking-text/u);
});

test("proxy isolates the child environment and digests stderr", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-env-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const childProgram = [
    "process.stdout.write(JSON.stringify({jsonrpc:'2.0',id:1,result:{",
    "inherited:process.env.QUAL_206_UNRELATED_ENV??null}})+'\\n');",
    "process.stderr.write('private-child-diagnostic');",
  ].join("");
  const invocation = run(
    process.execPath,
    [
      PROXY,
      "--log",
      telemetry,
      "--client",
      "environment-test",
      "--",
      process.execPath,
      "--eval",
      childProgram,
    ],
    {
      env: { QUAL_206_UNRELATED_ENV: "sentinel-value-must-not-cross" },
      input: "",
    },
  );
  const [code] = await once(invocation.child, "exit");
  const { stderr, stdout } = invocation.output();
  assert.equal(code, 0);
  assert.equal(JSON.parse(stdout).result.inherited, null);
  assert.match(stderr, /^\[qual-206\] child stderr bytes=24 sha256=[0-9a-f]{64}\n$/u);
  assert.doesNotMatch(stderr, /private-child-diagnostic/u);
  const logText = await readFile(telemetry, "utf8");
  assert.doesNotMatch(logText, /sentinel-value|private-child-diagnostic/u);
  assert.equal(
    logText.trim().split("\n").map((line) => JSON.parse(line))
      .filter((event) => event.event === "server_stderr").length,
    1,
  );
});

test("proxy records unterminated input and output fragments without changing bytes", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-framing-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const completeFrame = Buffer.from(`${JSON.stringify({
    jsonrpc: "2.0",
    method: "tools/list",
    params: {},
  })}\r\n`);
  const trailing = Buffer.from("unterminated-🙂-fragment");
  const input = Buffer.concat([completeFrame, trailing]);
  const invocation = run(
    process.execPath,
    [
      PROXY,
      "--log",
      telemetry,
      "--client",
      "framing-test",
      "--",
      process.execPath,
      "--eval",
      "process.stdin.pipe(process.stdout)",
    ],
  );
  const emojiOffset = input.indexOf(Buffer.from("🙂"));
  invocation.child.stdin.write(input.subarray(0, emojiOffset + 2));
  invocation.child.stdin.end(input.subarray(emojiOffset + 2));
  const [code] = await once(invocation.child, "exit");
  const { stderr, stdout } = invocation.output();
  assert.equal(code, 0, stderr);
  assert.equal(stderr, "");
  assert.equal(stdout, input.toString("utf8"));
  const events = (await readFile(telemetry, "utf8"))
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
  const fragments = events.filter((event) => event.event === "truncated_frame");
  assert.deepEqual(
    fragments.map((event) => event.direction),
    ["client_to_server", "server_to_client"],
  );
  assert.deepEqual(
    fragments.map((event) => [event.frame_bytes, event.frame_sha256]),
    [
      [trailing.length, sha256(trailing)],
      [trailing.length, sha256(trailing)],
    ],
  );
  assert.doesNotMatch(JSON.stringify(fragments), /unterminated|🙂/u);
});

test("proxy allowlists method and operation labels", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-label-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const privateLabel = "private-label-must-not-be-recorded";
  const input = `${JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: privateLabel,
    params: { name: privateLabel },
  })}\n`;
  const invocation = run(
    process.execPath,
    [PROXY, "--log", telemetry, "--client", "label-test", "--", process.execPath, "--eval", ""],
    { input },
  );
  const [code] = await once(invocation.child, "exit");
  assert.equal(code, 0);
  const logText = await readFile(telemetry, "utf8");
  const request = logText.trim().split("\n").map((line) => JSON.parse(line))
    .find((event) => event.event === "request");
  assert.equal(request.method, "other");
  assert.equal(request.operation, undefined);
  assert.doesNotMatch(logText, /private-label/u);
});

test("derived evaluation corpus is bounded and provenance-addressed", async () => {
  const corpus = JSON.parse(await readFile(CASES, "utf8"));
  assert.equal(corpus.schema, "gis-ai-go.qual-206-evaluation-corpus.v1");
  assert.match(corpus.derived_from.commit, /^[0-9a-f]{40}$/u);
  assert.equal(corpus.derived_from.sources.length, 6);
  assert.equal(corpus.cases.length, 10);
  assert.equal(new Set(corpus.cases.map((value) => value.id)).size, 10);
  const sourcePaths = new Set(corpus.derived_from.sources.map((source) => source.path));
  for (const source of corpus.derived_from.sources) {
    assert.match(source.sha256, /^[0-9a-f]{64}$/u);
    assert.equal(source.path.startsWith("/"), false);
  }
  const candidateCases = corpus.cases
    .filter((value) => value.provenance.kind === "candidate-assurance")
    .map((value) => value.id);
  assert.deepEqual(candidateCases, [
    "QUAL-206-HOST-002",
    "QUAL-206-HOST-006",
    "QUAL-206-HOST-009",
  ]);
  for (const evaluationCase of corpus.cases) {
    if (evaluationCase.provenance.kind === "historical-derived") {
      assert.ok(evaluationCase.provenance.source_refs.length > 0);
      for (const sourceRef of evaluationCase.provenance.source_refs) {
        assert.equal(sourcePaths.has(sourceRef), true, sourceRef);
      }
    } else {
      assert.equal(evaluationCase.provenance.kind, "candidate-assurance");
      assert.equal(typeof evaluationCase.provenance.basis, "string");
      assert.ok(evaluationCase.provenance.basis.length > 0);
      assert.equal(evaluationCase.provenance.source_refs, undefined);
    }
  }
});

test("reviewed ChatGPT evidence is path-free and binds the harness bytes", async () => {
  const evidence = JSON.parse(await readFile(CHATGPT_EVIDENCE, "utf8"));
  assert.equal(evidence.schema, "gis-ai-go.qual-206-live-host-evidence.v1");
  assert.equal(evidence.status, "local-live-candidate-pass");
  assert.equal(evidence.source.commit, SOURCE_COMMIT);
  assert.equal(evidence.host.name, "ChatGPT");
  assert.equal(evidence.request.operation, "catalogue.search");
  assert.equal(
    evidence.result.record_id,
    "hmlr:dataset:inspire-index-polygons",
  );
  assert.match(
    evidence.result.receipt_id,
    /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
  );
  assert.equal(evidence.telemetry.raw_content_retained, false);
  assert.equal(evidence.telemetry.event_count, 6);
  assert.deepEqual(evidence.telemetry.event_counts, {
    session_start: 3,
    session_end: 1,
    request: 1,
    response: 1,
  });
  assert.equal(evidence.telemetry.retained_copy_mode, "0600");
  assert.match(evidence.telemetry.retained_copy_sha256, /^[0-9a-f]{64}$/u);
  assert.equal(evidence.result.outcome, "success");
  assert.equal(evidence.tunnel.queue_length, 0);
  assert.equal(evidence.tunnel.worker_occupancy, 0);
  for (const entry of evidence.harness.files) {
    assert.equal(entry.path.startsWith("/"), false);
    assert.equal(
      sha256(await readFile(join(ROOT, entry.path))),
      entry.sha256,
      entry.path,
    );
  }
  assert.equal(
    evidence.harness.evaluation_corpus.role,
    "Reviewed current assurance corpus; not a live-session runtime input.",
  );
  assert.equal(
    sha256(await readFile(join(ROOT, evidence.harness.evaluation_corpus.path))),
    evidence.harness.evaluation_corpus.sha256,
  );
  assert.doesNotMatch(JSON.stringify(evidence), /\/Users\/|\/private\/tmp|sk-/u);
});

test("independent-host readiness evidence is bounded, path-free and unscored", async () => {
  const evidence = JSON.parse(await readFile(INDEPENDENT_HOST_EVIDENCE, "utf8"));
  const runbook = await readFile(
    join(ROOT, "docs", "operations", "QUAL-206_INTEROPERABILITY.md"),
    "utf8",
  );
  assert.equal(
    evidence.schema,
    "gis-ai-go.qual-206-independent-host-readiness.v1",
  );
  assert.equal(evidence.status, "readiness-attempts-not-ready");
  assert.equal(evidence.source.commit, SOURCE_COMMIT);
  assert.equal(evidence.source.production_activation, false);
  assert.equal(evidence.hosts.length, 3);
  assert.deepEqual(
    evidence.hosts.map((host) => host.name),
    ["Claude Code", "Antigravity IDE", "VS Code"],
  );
  for (const host of evidence.hosts) {
    assert.equal(host.readiness, "not_ready");
    assert.equal(host.capability, "unscored");
  }
  assert.equal(
    evidence.hosts[0].mcp_list_health_attempt.response_error_code,
    -32022,
  );
  assert.equal(evidence.hosts[1].mcp_requests, 0);
  assert.equal(evidence.hosts[2].mcp_requests, 0);
  assert.equal(
    evidence.evidence_limitations.current_telemetry_wrapper_exercised,
    false,
  );
  assert.equal(
    evidence.evidence_limitations.historical_parent_process_api_key_absence_proved,
    false,
  );
  assert.equal(
    evidence.evidence_limitations.retained_file_credential_scan_completed,
    true,
  );
  assert.equal(
    evidence.evidence_limitations.repeat_procedure_removes_openai_key_variables,
    true,
  );
  assert.equal(evidence.evidence_limitations.raw_host_logs_published, false);
  assert.equal(evidence.evidence_limitations.capability_result_claimed, false);
  assert.match(runbook, /"-u","OPENAI_API_KEY","-u","CODEX_API_KEY"/u);
  assert.ok(
    (runbook.match(/\/usr\/bin\/env -u OPENAI_API_KEY -u CODEX_API_KEY/gu) ?? [])
      .length >= 4,
  );
  for (const digest of JSON.stringify(evidence).matchAll(/[0-9a-f]{64}/gu)) {
    assert.equal(digest[0].length, 64);
  }
  assert.doesNotMatch(
    JSON.stringify(evidence),
    /\/Users\/|\/private\/tmp|sk-|device[_ -]?id|access[_ -]?token/iu,
  );
});

test("Codex CLI readiness evidence binds the exact case and remains unscored", async () => {
  const evidence = JSON.parse(await readFile(CODEX_HOST_EVIDENCE, "utf8"));
  const runbook = await readFile(
    join(ROOT, "docs", "operations", "QUAL-206_INTEROPERABILITY.md"),
    "utf8",
  );
  const corpusBytes = await readFile(CASES);
  const corpus = JSON.parse(corpusBytes);
  const evaluationCase = corpus.cases.find(
    (value) => value.id === "QUAL-206-HOST-002",
  );
  assert.equal(evidence.schema, "gis-ai-go.qual-206-codex-host-evidence.v1");
  assert.equal(evidence.status, "not_ready");
  assert.equal(evidence.source.commit, SOURCE_COMMIT);
  assert.equal(evidence.source.production_activation, false);
  assert.equal(evidence.host.name, "Codex CLI");
  assert.equal(evidence.host.version, "0.146.1");
  assert.equal(evidence.host.reported_commit, null);
  assert.equal(evidence.host.model_requested, "gpt-5.6-luna");
  assert.equal(evidence.host.model_response_observed, false);
  assert.equal(evidence.case.id, evaluationCase.id);
  assert.equal(evidence.case.corpus_sha256, sha256(corpusBytes));
  assert.equal(evidence.case.prompt_bytes, Buffer.byteLength(evaluationCase.prompt));
  assert.equal(evidence.case.prompt_sha256, sha256(evaluationCase.prompt));
  assert.equal(evidence.case.stdin_bytes, Buffer.byteLength(`${evaluationCase.prompt}\n`));
  assert.equal(evidence.case.stdin_sha256, sha256(`${evaluationCase.prompt}\n`));
  assert.equal(evidence.case.raw_prompt_published, false);
  assert.equal(evidence.result.readiness, "not_ready");
  assert.equal(evidence.result.capability, "unscored");
  assert.equal(evidence.result.classification, "protocol-negotiation-failure");
  assert.equal(evidence.result.exit_code, 1);
  assert.equal(evidence.result.host_requested_protocol_version, "2025-06-18");
  assert.deepEqual(evidence.result.server_supported_protocol_versions, ["2026-07-28"]);
  assert.equal(evidence.result.mcp_error_code, -32022);
  assert.equal(evidence.result.task_level_tool_calls, 0);
  assert.equal(evidence.telemetry.current_wrapper_exercised, true);
  assert.equal(evidence.telemetry.event_count, 3);
  assert.equal(evidence.telemetry.request_count, 1);
  assert.equal(evidence.telemetry.response_count, 1);
  assert.equal(evidence.telemetry.invalid_frame_count, 0);
  assert.equal(evidence.telemetry.non_json_frame_count, 0);
  assert.equal(evidence.telemetry.truncated_frame_count, 0);
  assert.equal(evidence.telemetry.server_stderr_event_count, 0);
  assert.equal(evidence.telemetry.session_end_observed, false);
  assert.equal(evidence.telemetry.request.method_label, "other");
  assert.equal(evidence.telemetry.response.error_code, -32022);
  assert.equal(evidence.telemetry.raw_content_published, false);
  assert.equal(evidence.output.stdout.bytes, 0);
  assert.equal(evidence.output.stdout.sha256, sha256(""));
  assert.equal(evidence.output.stderr.published, false);
  assert.equal(evidence.output.exact_api_key_matches, 0);
  assert.equal(evidence.output.token_pattern_matches, 0);
  assert.equal(evidence.isolation.directory_mode, "0700");
  assert.equal(evidence.isolation.raw_file_mode, "0600");
  assert.equal(evidence.isolation.normal_profile_mutation_observed, false);
  assert.equal(evidence.isolation.remaining_isolated_processes_after_probe, 0);
  assert.equal(evidence.isolation.mcp_child_received_api_credentials, false);
  assert.match(
    runbook,
    /-c 'shell_environment_policy\.ignore_default_excludes=false'/u,
  );
  for (const entry of evidence.harness.files) {
    assert.equal(entry.path.startsWith("/"), false);
    assert.equal(sha256(await readFile(join(ROOT, entry.path))), entry.sha256);
  }
  for (const digest of JSON.stringify(evidence).matchAll(/[0-9a-f]{64}/gu)) {
    assert.equal(digest[0].length, 64);
  }
  assert.doesNotMatch(
    JSON.stringify(evidence),
    /\/Users\/|\/private\/tmp|sk-|device[_ -]?id|access[_ -]?token/iu,
  );
});
