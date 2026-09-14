// Optional development experiment. Installs nothing and never deploys a Worker.
// Build @gis-ai-go/evidence first; supply a pre-existing, trusted local tooling root.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtemp, readFile, realpath, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const FIXTURE = join(ROOT, "scripts/web216_worker_storage_fixture.ts");
const VERSIONS = { miniflare: "5.20260911.1-alpha", workerd: "1.20260911.1", esbuild: "0.28.1" };
const usage = "node scripts/web216_worker_storage_probe.mjs --tooling-root <existing-installation-root>";
const args = process.argv.slice(2);
if (args.length !== 2 || args[0] !== "--tooling-root" || !args[1]) throw Error(usage);
const toolingRoot = await realpath(resolve(args[1]));
const temporaryRoot = await realpath(tmpdir());
const inside = (root, path) => { const part = relative(root, path); return part === "" || (!isAbsolute(part) && part !== ".." && !part.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`)); };
assert(!inside(ROOT, temporaryRoot) && !inside(toolingRoot, temporaryRoot), "Temporary output must be outside repository and tooling");
process.umask(0o077);
const directory = await mkdtemp(join(temporaryRoot, "gis-ai-go-web216-worker-d1-"));
const startedAt = new Date().toISOString();
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const save = async (name, value) => writeFile(join(directory, name),
  Buffer.isBuffer(value) || typeof value === "string" ? value : JSON.stringify(value, null, 2) + "\n",
  { mode: 0o600, flag: "wx" });
console.log(JSON.stringify({ directory, started_at: startedAt }));
let phase = "preflight";
let outboundAttempts = 0;
const runtimeErrors = [];
const plan = { experiment: "local-workerd-d1-not-hosted", started_at: startedAt,
  tooling_root: toolingRoot, expected_versions: VERSIONS, source_hashes: {},
  provider_egress: false, telemetry: false, deployment: false,
  persistence_option: "resourcePersistencePath", response_deadline_ms: 20_000,
  response_byte_limit: 1_048_576,
  limitation: "Local dispose/recreate compatibility only; no crash recovery, cloud durability or accepted-build attestation." };

async function deadline(operation) {
  let timer;
  try { return await Promise.race([operation(), new Promise((_, reject) => {
    timer = setTimeout(() => reject(Error("Local probe response deadline exceeded")), 20_000);
  })]); } finally { clearTimeout(timer); }
}
async function observe(worker, path, label) {
  const record = { requested_at: new Date().toISOString(), path, status: null, body_complete: false };
  const chunks = [];
  let size = 0;
  try {
    await deadline(async () => {
      const response = await (await worker.getWorker("web216-d1-probe")).fetch(`http://localhost/${path}`);
      record.status = response.status;
      const reader = response.body?.getReader();
      if (reader) {
        while (true) {
          const item = await reader.read();
          if (item.done) break;
          size += item.value.byteLength;
          if (size > plan.response_byte_limit) { void reader.cancel().catch(() => {}); throw Error("Response exceeds probe limit"); }
          chunks.push(Buffer.from(item.value));
        }
      }
      record.body_complete = true;
    });
  } catch (error) {
    record.error = { name: error?.name ?? "unknown", message: String(error?.message ?? error) };
  }
  const body = Buffer.concat(chunks);
  Object.assign(record, { completed_at: new Date().toISOString(), body_bytes: body.length,
    body_sha256: sha256(body), body_file: `${label}-response.body.json` });
  await save(record.body_file, body);
  await save(`${label}-response.json`, record);
  assert.equal(record.error, undefined, "See preserved response failure");
  assert.equal(record.status, 200, "See preserved non-200 response");
  return JSON.parse(body.toString("utf8"));
}

try {
  for (const [name, path] of [["runner", fileURLToPath(import.meta.url)], ["fixture", FIXTURE]]) {
    const bytes = await readFile(path);
    plan.source_hashes[name] = sha256(bytes);
    await save(name === "runner" ? "runner-source.mjs" : "fixture-source.ts", bytes);
  }
  const require = createRequire(join(toolingRoot, "package.json"));
  const entries = {};
  for (const [name, version] of Object.entries(VERSIONS)) {
    const packageRoot = await realpath(join(toolingRoot, "node_modules", name));
    const manifest = JSON.parse(await readFile(join(packageRoot, "package.json"), "utf8"));
    assert.equal(manifest.version, version, `Pre-existing ${name} must be exactly ${version}; no installation attempted`);
    entries[name] = await realpath(require.resolve(name));
    assert(inside(packageRoot, entries[name]), `${name} must resolve inside its verified package`);
  }
  await readFile(join(ROOT, "packages/evidence/dist/src/index.js"));
  const { build } = await import(pathToFileURL(entries.esbuild).href);
  const { Miniflare, convertV4MiniflareOptions, NoOpLog } = await import(pathToFileURL(entries.miniflare).href);
  const compiled = await build({ absWorkingDir: ROOT, entryPoints: [FIXTURE], bundle: true, write: false,
    format: "esm", platform: "neutral", target: "es2023", external: ["node:*"], metafile: true });
  const script = compiled.outputFiles[0].text;
  await save("worker.mjs", script);
  plan.bundle_sha256 = sha256(script);
  plan.bundle_bytes = Buffer.byteLength(script);
  plan.compiled_input_hashes = [];
  for (const path of Object.keys(compiled.metafile.inputs).sort()) {
    assert(inside(ROOT, resolve(ROOT, path)), "Bundle inputs must remain repository-local");
    plan.compiled_input_hashes.push({ path, sha256: sha256(await readFile(resolve(ROOT, path))) });
  }
  // Inputs are trusted local compiled prerequisites; the exact executed bundle is
  // retained. These hashes are a source inventory, not build-process attestation.
  const options = () => ({ ...convertV4MiniflareOptions({ name: "web216-d1-probe", modules: true, script,
    host: "127.0.0.1", cf: false, compatibilityDate: "2026-09-14", compatibilityFlags: ["nodejs_compat"],
    d1Databases: { DB: "web216-public-fixture" }, resourcePersistencePath: join(directory, "database"),
    log: new NoOpLog(), outboundService: () => { outboundAttempts += 1; return new Response("Provider egress refused", { status: 503 }); },
  }), telemetry: { enabled: false }, handleUncaughtError: (error) => runtimeErrors.push(String(error)) });
  assert.equal(options().resourcePersistencePath, join(directory, "database"));
  await save("attempt-plan.json", plan);
  phase = "fresh-exercise";
  let worker = new Miniflare(options());
  let first;
  try { first = await observe(worker, "exercise", "first"); }
  finally { await worker.dispose(); }
  phase = "restart-inspect";
  worker = new Miniflare(options());
  let reopened;
  try { reopened = await observe(worker, "inspect", "reopened"); }
  finally { await worker.dispose(); }
  assert.equal(first.canonical, reopened.canonical);
  assert.equal(reopened.snapshot.records.length, 2);
  assert.equal(reopened.snapshot.events.length, 2);
  assert.deepEqual(reopened.snapshot.records.map((record) => record.period), ["2026-01", "2026-07"]);
  assert.equal(outboundAttempts, 0);
  assert.deepEqual(runtimeErrors, []);
  const outcome = { outcome: "local-d1-restart-pass", started_at: startedAt, completed_at: new Date().toISOString(),
    restart_exact_match: true, record_count: 2, canonical_snapshot_sha256: sha256(reopened.canonical),
    local_measurements: first.measurements, outbound_attempts: outboundAttempts, runtime_errors: runtimeErrors,
    bundle_sha256: plan.bundle_sha256, source_hashes: plan.source_hashes,
    hosted_deployment: false, crash_recovery_established: false, attested: false };
  await save("outcome.json", outcome);
  console.log(JSON.stringify({ directory, ...outcome }));
} catch (error) {
  await save("failure.json", { outcome: "failed-or-unavailable", phase, completed_at: new Date().toISOString(),
    error: { name: error?.name ?? "unknown", message: String(error?.message ?? error) },
    plan, outbound_attempts: outboundAttempts, runtime_errors: runtimeErrors });
  console.error(JSON.stringify({ directory, phase, outcome: "failed-or-unavailable", message: String(error?.message ?? error) }));
  process.exitCode = 1;
}
