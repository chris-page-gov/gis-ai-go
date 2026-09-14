import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import * as legacy from "../src/index.js";
import * as pure from "@gis-ai-go/evidence/web216-pure";

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const PURE_SOURCE = "packages/evidence/src/web216-pure.ts";
const ENTRIES = [PURE_SOURCE,
  "apps/mcp-gateway/src/web216-hosted-cpih-application.ts",
  "apps/mcp-gateway/src/web216-hosted-cpih-mcp.ts",
  "apps/mcp-gateway/src/web216-hosted-cpih-http.ts"];

function admittedSpecifier(specifier: string): void {
  assert.ok(!/^(?:node:)?fs(?:\/|$)/u.test(specifier), "forbidden filesystem import");
  assert.ok(!specifier.startsWith("@gis-ai-go/") || specifier === "@gis-ai-go/evidence/web216-pure",
    "forbidden legacy workspace import");
}
function admittedPath(path: string): void {
  assert.ok(!path.startsWith("../"), "source import escaped the repository");
  assert.ok(!/^packages\/evidence\/(?:dist\/)?src\/(?:index|checkpoint|public-ledger|reconciliation-index)(?:[.-])/u.test(path),
    "forbidden filesystem evidence graph");
  assert.ok(!/^packages\/(?:tool-registry|provider-adapter-sdk|policy-client|authority-context)\//u.test(path),
    "forbidden legacy registry or provider graph");
}

/** Follow maintained literal module declarations, including type-only imports.
 * This is a source-boundary regression, not a general JavaScript security parser.
 * Third-party SDK internals are outside this source check; the actual compiled
 * pure entry is separately imported under a rejecting Node resolution hook below.
 */
function sourceClosure(injections: Record<string, string> = {}): Set<string> {
  const seen = new Set<string>();
  const pending = [...ENTRIES];
  while (pending.length > 0) {
    const path = pending.pop()!;
    if (seen.has(path)) continue;
    admittedPath(path);
    seen.add(path);
    const source = readFileSync(resolve(ROOT, path), "utf8") + (injections[path] ?? "");
    // These modules have static imports only. A future dynamic loader requires a
    // deliberate extension and cannot silently disappear from this check.
    assert.ok(!/\b(?:import|require)\s*\(/u.test(source), "dynamic module loading needs explicit review");
    const specifiers = [
      ...source.matchAll(/^\s*(?:import\s+|export\s+(?:\*|\{))[^;]+?\bfrom\s*["']([^"']+)["']/gmu),
      ...source.matchAll(/^\s*import\s*["']([^"']+)["']/gmu),
    ].map((match) => match[1]!);
    for (const specifier of specifiers) {
      admittedSpecifier(specifier);
      if (specifier === "@gis-ai-go/evidence/web216-pure") pending.push(PURE_SOURCE);
      else if (specifier.startsWith(".")) {
        assert.ok(specifier.endsWith(".js"), "unexpected maintained module extension");
        pending.push(relative(ROOT, resolve(ROOT, dirname(path), specifier.replace(/\.js$/u, ".ts"))));
      } else assert.ok(specifier.startsWith("node:") || specifier === "@modelcontextprotocol/server",
        "unexpected external source dependency");
    }
  }
  return seen;
}

test("the explicit pure export preserves original function, class and regex identities", () => {
  const manifest = JSON.parse(readFileSync(new URL("../../package.json", import.meta.url), "utf8"));
  assert.deepEqual(manifest.exports["."], { types: "./src/index.ts", import: "./dist/src/index.js" });
  assert.deepEqual(manifest.exports["./web216-pure"], { types: "./src/web216-pure.ts", import: "./dist/src/web216-pure.js" });
  for (const [name, value] of Object.entries(pure)) assert.equal(value, legacy[name as keyof typeof legacy], name);
  for (const name of ["openPublicEvidenceLedger", "openEvidenceReconciliationIndex", "createEvidenceCheckpoint", "PublicEvidenceLedger"]) {
    assert.equal(Object.hasOwn(pure, name), false, name);
  }
  assert.equal(pure.PUBLIC_IDEMPOTENCY_KEY.source, "^gis-ai-go:ik:v1:[0-9a-f]{64}$");
  assert.equal(pure.PUBLIC_IDEMPOTENCY_KEY.flags, "u");
});

test("a fresh compiled pure import resolves no filesystem or legacy evidence module", () => {
  const result = spawnSync(process.execPath, ["--input-type=module", "--eval", `
    import assert from "node:assert/strict";
    import { registerHooks } from "node:module";
    registerHooks({ resolve(specifier, context, nextResolve) {
      assert.ok(!/^(?:node:)?fs(?:\\/|$)/u.test(specifier), "forbidden filesystem import");
      assert.ok(!specifier.startsWith("@gis-ai-go/"), "forbidden legacy workspace import");
      const result = nextResolve(specifier, context);
      assert.ok(!/\\/(?:index|checkpoint|public-ledger|reconciliation-index)(?:[.-])/u.test(result.url),
        "forbidden filesystem evidence graph");
      return result;
    }});
    const pure = await import(process.argv[1]);
    assert.equal(typeof pure.createWeb216D1SnapshotStore, "function");
  `, new URL("../src/web216-pure.js", import.meta.url).href], {
    cwd: ROOT, encoding: "utf8", timeout: 5_000, maxBuffer: 65_536,
  });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 0, result.stderr);
});

test("hosted source closure follows the pure selection, schema and storage dependencies", () => {
  const visited = sourceClosure();
  for (const path of [
    ...ENTRIES, "packages/evidence/src/idempotency-constants.ts",
    "packages/evidence/src/web216-transactional-d1.ts", "apps/mcp-gateway/src/web216-cpih-selection.ts",
    "apps/mcp-gateway/src/web216-cpih-input-schemas.ts",
    "apps/mcp-gateway/src/mcp-http-core.ts", "apps/mcp-gateway/src/mcp-wire-guards.ts",
    "apps/mcp-gateway/src/bounded-json.ts",
  ]) assert.ok(visited.has(path), path);
});

test("the closure guard detects nested filesystem, root-barrel, registry and dynamic regressions", () => {
  for (const [path, injection, reason] of [
    ["packages/evidence/src/canonical-json.ts", '\nimport "node:fs/promises";', /forbidden filesystem import/u],
    ["apps/mcp-gateway/src/web216-cpih-selection.ts", '\nimport "@gis-ai-go/evidence";', /forbidden legacy workspace import/u],
    ["packages/evidence/src/web216-transactional-d1.ts", '\nexport * from "./public-ledger.js";', /forbidden filesystem evidence graph/u],
    ["apps/mcp-gateway/src/web216-cpih-input-schemas.ts", '\nimport "@gis-ai-go/tool-registry";', /forbidden legacy workspace import/u],
    ["packages/evidence/src/canonical-json.ts", '\nvoid import("node:fs");', /dynamic module loading needs explicit review/u],
  ] as const) assert.throws(() => sourceClosure({ [path]: injection }), reason);
});
