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
const LEGACY_SERVER = join(
  ROOT,
  "scripts",
  "qual_206_legacy_conformance_server.mjs",
);
const PROXY = join(ROOT, "scripts", "qual_206_telemetry_proxy.mjs");
const CASES = join(ROOT, "tests", "interoperability", "qual_206_cases.json");
const CASES_EXPANSION = join(
  ROOT,
  "tests",
  "interoperability",
  "qual_206_cases_expansion.json",
);
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
const LEGACY_FALLBACK_EVIDENCE = join(
  ROOT,
  "tests",
  "interoperability",
  "evidence",
  "legacy-fallback-exploratory-2026-08-20.json",
);
const SOURCE_COMMIT = "66507f9a6e6c0da23a8af4682268f9362d93bc06";
const LEGACY_CANDIDATE_BASE = "b798a40b940e135b933c3b757cb5a9f9ff6aa2ae";
const LEGACY_FALLBACK_EVIDENCE_SHA256 =
  "5d2c22c17b7a0c65bd3957f9d23057ab7a5d522d223ed432642250b997823537";
const LEGACY_RUNTIME_FILES = [
  {
    path: "apps/mcp-gateway/src/mcp-server.ts",
    sha256: "ee39e4cc99c8ed082f790f2eba3df908a8b4bf0830dd5ee7a8cc770206b657d9",
  },
  {
    path: "apps/mcp-gateway/src/mcp-stdio.ts",
    sha256: "68c229a0252064f630a5c2d5c057e5348b1e4ce6974aecd48b291cd05db6a794",
  },
  {
    path: "scripts/qual_206_legacy_conformance_server.mjs",
    sha256: "bf87bec24357d5fd6d419bd8b4374642ab46a2f3dfa6d9baebde46f7498edb9c",
  },
  {
    path: "scripts/qual_206_telemetry_proxy.mjs",
    sha256: "3800e4458932ee1324ad03d64007f23f76f49682a6eabdc191ecf6eaccb501d5",
  },
];
const LEGACY_COMPILED_RUNTIME = [
  {
    source_path: "apps/mcp-gateway/dist/src/mcp-server.js",
    sha256: "860e466d5ab7215cec0dde4e67260fd1bd33f1166b21aa2d092d8e6dcad49018",
  },
  {
    source_path: "apps/mcp-gateway/dist/src/mcp-stdio.js",
    sha256: "035d8260308479133537ba5fa07a7bbf2affbc4ed6072859a924f01089ce95ef",
  },
];
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

function gitBlobSha1(value) {
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value);
  return createHash("sha1")
    .update(`blob ${bytes.length}\0`)
    .update(bytes)
    .digest("hex");
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

test("legacy conformance server fails closed without both explicit authorities", async () => {
  const missingArgument = run(process.execPath, [LEGACY_SERVER], {
    env: {
      GIS_AI_GO_QUAL_206_CONFORMANCE: "1",
      GIS_AI_GO_QUAL_206_SOURCE_COMMIT: LEGACY_CANDIDATE_BASE,
    },
    input: "",
  });
  const [argumentCode] = await once(missingArgument.child, "exit");
  assert.notEqual(argumentCode, 0);
  assert.equal(missingArgument.output().stdout, "");
  assert.match(
    missingArgument.output().stderr,
    /--legacy-stdio-conformance-only/u,
  );

  const missingEnvironment = run(
    process.execPath,
    [LEGACY_SERVER, "--legacy-stdio-conformance-only"],
    {
      env: {
        GIS_AI_GO_QUAL_206_CONFORMANCE: "",
        GIS_AI_GO_QUAL_206_SOURCE_COMMIT: LEGACY_CANDIDATE_BASE,
      },
      input: "",
    },
  );
  const [environmentCode] = await once(missingEnvironment.child, "exit");
  assert.notEqual(environmentCode, 0);
  assert.equal(missingEnvironment.output().stdout, "");
  assert.match(
    missingEnvironment.output().stderr,
    /GIS_AI_GO_QUAL_206_CONFORMANCE=1/u,
  );
});

test("legacy conformance journey keeps the existing minimised telemetry boundary", async () => {
  const directory = await mkdtemp(join(tmpdir(), "gis-ai-go-qual-206-legacy-"));
  const telemetry = join(directory, "telemetry.jsonl");
  const messages = [
    {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2025-06-18",
        capabilities: {},
        clientInfo: { name: "legacy-telemetry-test", version: "1.0.0" },
      },
    },
    {
      jsonrpc: "2.0",
      method: "notifications/initialized",
      params: {},
    },
    { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} },
    {
      jsonrpc: "2.0",
      id: 3,
      method: "tools/call",
      params: {
        name: "catalogue.describe",
        arguments: { record_id: "LR-Q003" },
      },
    },
    { jsonrpc: "2.0", id: 4, method: "resources/list", params: {} },
    {
      jsonrpc: "2.0",
      id: 5,
      method: "resources/templates/list",
      params: {},
    },
    {
      jsonrpc: "2.0",
      id: 6,
      method: "resources/read",
      params: { uri: "gis-ai-go://catalogue/public" },
    },
  ];
  const invocation = run(
    process.execPath,
    [
      PROXY,
      "--log",
      telemetry,
      "--client",
      "legacy-node-test",
      "--",
      process.execPath,
      LEGACY_SERVER,
      "--legacy-stdio-conformance-only",
    ],
    {
      env: {
        GIS_AI_GO_QUAL_206_CONFORMANCE: "1",
        GIS_AI_GO_QUAL_206_SOURCE_COMMIT: LEGACY_CANDIDATE_BASE,
      },
      input: `${messages.map((value) => JSON.stringify(value)).join("\n")}\n`,
    },
  );
  const [code] = await once(invocation.child, "exit");
  const { stderr, stdout } = invocation.output();
  assert.equal(code, 0, stderr);
  assert.equal(stderr, "");
  const replies = stdout.trim().split("\n").map((line) => JSON.parse(line));
  assert.equal(replies.length, 6);
  const repliesById = new Map(replies.map((reply) => [reply.id, reply]));
  assert.equal(repliesById.get(1).result.protocolVersion, "2025-06-18");
  assert.deepEqual(
    repliesById.get(2).result.tools.map((tool) => tool.name),
    ["catalogue.describe", "catalogue.search"],
  );
  assert.equal(
    repliesById.get(3).result.structuredContent.operation,
    "catalogue.describe",
  );
  assert.equal(
    repliesById.get(6).result.contents[0].uri,
    "gis-ai-go://catalogue/public",
  );

  const logText = await readFile(telemetry, "utf8");
  const events = logText.trim().split("\n").map((line) => JSON.parse(line));
  assert.equal(events[0].source_commit, LEGACY_CANDIDATE_BASE);
  assert.equal(events.at(-1).event, "session_end");
  assert.equal(events.filter((event) => event.event === "request").length, 7);
  assert.equal(events.filter((event) => event.event === "response").length, 6);
  assert.deepEqual(
    events.filter((event) => event.event === "request").map((event) => event.method),
    [
      "other",
      "other",
      "tools/list",
      "tools/call",
      "resources/list",
      "resources/templates/list",
      "resources/read",
    ],
  );
  assert.doesNotMatch(logText, /legacy-telemetry-test|LR-Q003|catalogue\/public/u);
  assert.equal((await stat(telemetry)).mode & 0o777, 0o600);
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

test("evaluation expansion preserves the frozen corpus and provenance", async () => {
  const corpusBytes = await readFile(CASES);
  const corpus = JSON.parse(corpusBytes);
  const expansion = JSON.parse(await readFile(CASES_EXPANSION, "utf8"));
  assert.equal(
    sha256(corpusBytes),
    "23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389",
  );
  assert.equal(
    gitBlobSha1(corpusBytes),
    "728c9902b98c45f0a123127cb0756e86ba7a1113",
  );
  assert.equal(expansion.schema, "gis-ai-go.qual-206-evaluation-expansion.v1");
  assert.equal(expansion.base_corpus.sha256, sha256(corpusBytes));
  assert.equal(expansion.base_corpus.git_blob, gitBlobSha1(corpusBytes));
  assert.deepEqual(
    expansion.base_corpus.case_ids,
    corpus.cases.map((value) => value.id),
  );
  assert.equal(
    expansion.source_repository.commit,
    "56683b33c0cd02842b7f3ee465414c68a1f3f2a6",
  );

  const expectedExpansionIds = [
    "QUAL-206-HOST-011",
    "QUAL-206-HOST-012",
    "QUAL-206-HOST-013",
    "QUAL-206-HOST-014",
    "QUAL-206-HOST-015",
    "QUAL-206-HOST-017",
    "QUAL-206-HOST-018",
  ];
  assert.deepEqual(expansion.cases.map((value) => value.id), expectedExpansionIds);
  const combinedIds = [
    ...corpus.cases.map((value) => value.id),
    ...expansion.cases.map((value) => value.id),
  ];
  assert.equal(combinedIds.length, 17);
  assert.equal(new Set(combinedIds).size, combinedIds.length);
  assert.equal(combinedIds.includes("QUAL-206-HOST-016"), false);

  assert.equal(expansion.sources.length, 8);
  const sourceIds = new Set(expansion.sources.map((source) => source.id));
  assert.equal(sourceIds.size, expansion.sources.length);
  for (const source of expansion.sources) {
    assert.match(source.commit, /^[0-9a-f]{40}$/u);
    assert.match(source.git_blob, /^[0-9a-f]{40}$/u);
    assert.match(source.sha256, /^[0-9a-f]{64}$/u);
    assert.equal(source.path.startsWith("/"), false);
    assert.equal(source.pointers.length > 0, true);
    assert.equal(new Set(source.pointers).size, source.pointers.length);
  }
  for (const source of expansion.sources.filter(
    (value) => value.repository === "chris-page-gov/mcp-geo",
  )) {
    assert.equal(source.commit, expansion.source_repository.commit);
  }
  const submoduleSource = expansion.sources.find(
    (value) => value.repository === "chris-page-gov/os-mcp",
  );
  assert.equal(
    submoduleSource.commit,
    "584cb6d0c2ded52b7e5f27b89be5c7a4eb1f2365",
  );
  assert.equal(
    submoduleSource.parent_repository_commit,
    expansion.source_repository.commit,
  );
  assert.equal(submoduleSource.submodule_path, "submodules/os-mcp");

  for (const evaluationCase of expansion.cases) {
    assert.equal(evaluationCase.provenance.kind, "historical-derived");
    assert.ok(evaluationCase.provenance.source_refs.length > 0);
    for (const sourceRef of evaluationCase.provenance.source_refs) {
      assert.equal(sourceIds.has(sourceRef), true, sourceRef);
    }
    for (const extendedCase of evaluationCase.extends_cases ?? []) {
      assert.equal(expansion.base_corpus.case_ids.includes(extendedCase), true);
    }
    assert.equal(
      new Set(evaluationCase.fixture.variants.map((value) => value.id)).size,
      evaluationCase.fixture.variants.length,
    );
    assert.equal(
      new Set(evaluationCase.assertions.map((value) => value.id)).size,
      evaluationCase.assertions.length,
    );
  }
});

test("evaluation expansion keeps HOST-015 locally passing but non-live and unscored", async () => {
  const expansion = JSON.parse(await readFile(CASES_EXPANSION, "utf8"));
  const statuses = expansion.cases.map((value) => value.status);
  assert.equal(statuses.filter((value) => value === "pending").length, 6);
  assert.equal(statuses.filter((value) => value === "expected-failing").length, 0);
  assert.equal(statuses.filter((value) => value === "passing").length, 1);
  for (const evaluationCase of expansion.cases) {
    assert.equal(evaluationCase.execution_mode, "non-live");
    assert.equal(evaluationCase.scoring, "unscored");
    assert.equal(evaluationCase.live_capability_evidence, false);
    assert.equal(
      evaluationCase.activation_boundary,
      evaluationCase.id === "QUAL-206-HOST-015"
        ? "local-runtime-wired-production-unactivated"
        : "design-only-no-runtime-wiring",
    );
    assert.equal(
      ["pending", "passing"].includes(evaluationCase.status),
      true,
    );
    assert.equal(evaluationCase.classification, "non-live-pre-activation");
    assert.equal(evaluationCase.known_gap, undefined);
    assert.equal(evaluationCase.observed_result, undefined);
    assert.equal(evaluationCase.host_result, undefined);
    assert.equal(evaluationCase.telemetry, undefined);
  }

  const reconciled = expansion.cases.find(
    (value) => value.id === "QUAL-206-HOST-015",
  );
  assert.equal(reconciled.status, "passing");
  assert.equal(reconciled.classification, "non-live-pre-activation");
  assert.equal(
    reconciled.activation_boundary,
    "local-runtime-wired-production-unactivated",
  );
  assert.deepEqual(reconciled.provenance.source_refs, ["MCPGEO-SOURCE-05"]);
  assert.deepEqual(
    reconciled.assertions.map(({ id }) => id),
    [
      "at-most-once-side-effects",
      "completed-retry-fails-closed",
      "receipt-only-recovery",
    ],
  );

  assert.equal(expansion.deferred_cases.length, 1);
  const deferred = expansion.deferred_cases[0];
  assert.equal(deferred.id, "QUAL-206-HOST-016");
  assert.equal(deferred.status, "deferred");
  assert.equal(deferred.classification, "not-runnable-no-governed-cache");
  assert.equal(deferred.live_capability_evidence, false);
  assert.equal(deferred.scoring, "unscored");
  assert.deepEqual(deferred.source_refs, ["MCPGEO-SOURCE-06"]);
  assert.match(deferred.rationale, /no governed runtime cache/u);
  assert.match(deferred.activation_condition, /expected and ingested shard counts/u);

  const sourceIds = new Set(expansion.sources.map((source) => source.id));
  for (const sourceRef of deferred.source_refs) {
    assert.equal(sourceIds.has(sourceRef), true, sourceRef);
  }
  const referencedSources = new Set([
    ...expansion.cases.flatMap((value) => value.provenance.source_refs),
    ...expansion.deferred_cases.flatMap((value) => value.source_refs),
  ]);
  assert.deepEqual([...referencedSources].sort(), [...sourceIds].sort());
  assert.doesNotMatch(JSON.stringify(expansion.cases), /"status":"(?:failed|passed)"/u);
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

test("legacy fallback evidence is new, source-bound and explicitly exploratory", async () => {
  const evidenceBytes = await readFile(LEGACY_FALLBACK_EVIDENCE);
  assert.equal(sha256(evidenceBytes), LEGACY_FALLBACK_EVIDENCE_SHA256);
  const evidence = JSON.parse(evidenceBytes.toString("utf8"));
  const runbook = await readFile(
    join(ROOT, "docs", "operations", "QUAL-206_INTEROPERABILITY.md"),
    "utf8",
  );
  assert.equal(
    evidence.schema,
    "gis-ai-go.qual-206-legacy-fallback-exploratory.v1",
  );
  assert.equal(evidence.status, "exploratory-connectivity-pass");
  assert.equal(evidence.source.base_commit, LEGACY_CANDIDATE_BASE);
  assert.equal(evidence.source.candidate_commit, null);
  assert.equal(evidence.source.worktree_changes_uncommitted, true);
  assert.equal(evidence.source.production_activation, false);
  assert.equal(evidence.source.public_endpoint_created, false);
  assert.deepEqual(evidence.source.runtime_files, LEGACY_RUNTIME_FILES);
  assert.deepEqual(evidence.source.compiled_runtime, LEGACY_COMPILED_RUNTIME);
  assert.equal(evidence.limitations.accepted_evidence, false);
  assert.equal(evidence.limitations.candidate_commit_missing, true);
  assert.match(
    runbook,
    /retains base commit `b798a40`, a null\s+candidate commit and its original runtime hashes/u,
  );
  assert.equal(evidence.claude.version, "2.1.204");
  assert.equal(evidence.claude.model_authentication_supplied, false);
  assert.equal(evidence.claude.model_task_requested, false);
  assert.equal(evidence.claude.transport_readiness, "ready");
  assert.equal(evidence.claude.capability, "unscored");
  assert.equal(evidence.claude.initialize_success, true);
  assert.equal(evidence.claude.tools_list_success, true);
  assert.equal(evidence.telemetry.source_commit, LEGACY_CANDIDATE_BASE);
  assert.equal(evidence.telemetry.event_count, 7);
  assert.deepEqual(evidence.telemetry.event_counts, {
    session_start: 1,
    request: 3,
    response: 2,
    session_end: 1,
  });
  assert.equal(evidence.telemetry.initialize_response.outcome, "success");
  assert.equal(evidence.telemetry.tools_list_response.outcome, "success");
  assert.equal(evidence.telemetry.exit_code, 0);
  assert.equal(evidence.telemetry.pending_request_count, 0);
  assert.equal(evidence.telemetry.raw_content_published, false);
  assert.equal(evidence.codex.version, "0.146.1");
  assert.equal(evidence.codex.configuration_validation, "pass");
  assert.equal(evidence.codex.normal_registry_mutated, false);
  assert.equal(evidence.codex.model_task_requested, false);
  assert.equal(evidence.codex.mcp_process_started, false);
  assert.equal(evidence.codex.transport_readiness, "not_tested");
  assert.equal(evidence.codex.capability, "unscored");
  assert.equal(evidence.isolation.parent_openai_key_variables_removed, true);
  assert.equal(evidence.isolation.mcp_child_openai_key_variables_removed, true);
  assert.equal(evidence.isolation.token_pattern_matches, 0);
  assert.equal(evidence.limitations.accepted_evidence, false);
  assert.equal(evidence.limitations.repeat_from_exact_committed_source_required, true);
  assert.equal(evidence.limitations.chatgpt_tunnel_touched, false);
  assert.doesNotMatch(
    JSON.stringify(evidence),
    /\/Users\/|\/private\/tmp|sk-|device[_ -]?id|access[_ -]?token/iu,
  );
});
