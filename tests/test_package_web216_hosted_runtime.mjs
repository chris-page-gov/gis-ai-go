import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdir, mkdtemp, readFile, rm, symlink, unlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  createVerifiedFileLoader, planOutputDirectory, createOutputDirectory,
} from "../scripts/package_web216_hosted_runtime.mjs";

const ROOT = "/web216-fixture-root";
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
function fixtureLoader(content, expected = content) {
  let reads = 0; let load;
  const loader = createVerifiedFileLoader({ root: ROOT, resolvePath: async (path) => path,
    readBytes: async () => { reads += 1; return content; }, trackedBytes: async () => expected });
  loader.plugin.setup({ onLoad(options, callback) {
    assert.equal(options.namespace, "file"); load = callback;
  } });
  return { loader, load, reads: () => reads };
}

test("onLoad supplies the verified bytes and later file or compiler-buffer changes cannot rewrite their evidence", async () => {
  const bytes = Buffer.from("export const value = 1;");
  const expected = Buffer.from(bytes);
  const { loader, load, reads } = fixtureLoader(bytes, expected);
  const loaded = await load({ path: `${ROOT}/source.ts` });
  assert.equal(loaded.loader, "ts"); assert.deepEqual(Buffer.from(loaded.contents), expected);
  bytes.fill(0); loaded.contents.fill(1);
  const retained = loader.entry("source.ts");
  assert.deepEqual(retained.content, expected); assert.equal(retained.material.sha256, sha256(expected));
  retained.content.fill(2);
  assert.deepEqual(loader.entry("source.ts").content, expected);
  assert.deepEqual(Buffer.from((await load({ path: `${ROOT}/source.ts` })).contents), expected);
  assert.equal(reads(), 1);
});

test("changed maintained bytes fail before esbuild receives any source", async () => {
  const { loader, load } = fixtureLoader(Buffer.from("transient changed input"), Buffer.from("tracked input"));
  await assert.rejects(load({ path: `${ROOT}/source.ts` }), /exact tracked Git blob/u);
  assert.throws(() => loader.entry("source.ts"), /not captured/u);
});

test("the loader is closed to unsupported extensions, escaped paths and over-limit input", async () => {
  await assert.rejects(fixtureLoader(Buffer.from("text")).load({ path: `${ROOT}/source.css` }), /Unsupported/u);
  await assert.rejects(fixtureLoader(Buffer.alloc(8_388_609)).load({ path: `${ROOT}/large.js` }), /bounded byte limit/u);
  let called = false; let load;
  const loader = createVerifiedFileLoader({ root: ROOT, resolvePath: async () => "/outside-fixture/source.js",
    readBytes: async () => { called = true; return Buffer.from("text"); }, trackedBytes: async () => Buffer.from("text") });
  loader.plugin.setup({ onLoad(_options, callback) { load = callback; } });
  await assert.rejects(load({ path: `${ROOT}/source.js` }), /escaped source checkout/u);
  assert.equal(called, false);
});

test("all supported loaders retain declared dependency uncertainty and root licence bytes", async () => {
  for (const [extension, expectedLoader] of [["ts", "ts"], ["js", "js"], ["mjs", "js"], ["cjs", "js"], ["json", "json"]]) {
    const { loader, load } = fixtureLoader(Buffer.from("{}"));
    const path = `${ROOT}/node_modules/example/source.${extension}`;
    assert.equal((await load({ path })).loader, expectedLoader);
    assert.equal(loader.entry(path).material.binding, "observed-installed-dependency-bytes");
  }
  const licence = await readFile(new URL("../LICENSE", import.meta.url));
  const { loader } = fixtureLoader(licence);
  await loader.capture("LICENSE");
  assert.deepEqual(loader.entry("LICENSE").content, licence);
  assert.equal(loader.entry("LICENSE").material.sha256, sha256(licence));
  assert.equal(loader.entry("LICENSE").material.binding, "exact-tracked-git-blob");
});

async function directories(t) {
  const base = await mkdtemp(join(tmpdir(), "web216-packager-test-"));
  t.after(() => rm(base, { recursive: true, force: true })); // Only this test's new directory.
  const source = join(base, "source"); const tooling = join(base, "tooling"); const outside = join(base, "outside");
  await Promise.all([source, tooling, outside].map((path) => mkdir(path, { mode: 0o700 })));
  return { base, source, tooling, outside };
}
test("symlinked parents into either protected checkout are rejected before creating output", async (t) => {
  const { base, source, tooling } = await directories(t);
  for (const [label, target] of [["source-link", source], ["tooling-link", tooling]]) {
    const link = join(base, label); await symlink(target, link, "dir");
    await assert.rejects(planOutputDirectory(join(link, "new-package"), [source, tooling]), /outside source and tooling/u);
  }
});

test("parent retargeting between planning and creation is rejected", async (t) => {
  const { base, source, tooling, outside } = await directories(t);
  const link = join(base, "destination-link"); await symlink(outside, link, "dir");
  const plan = await planOutputDirectory(join(link, "new-package"), [source, tooling]);
  await unlink(link); await symlink(source, link, "dir");
  await assert.rejects(createOutputDirectory(plan), /parent changed/u);
});

test("fresh output resolves canonically and an existing package is never replaced", async (t) => {
  const { base, source, tooling, outside } = await directories(t);
  const link = join(base, "safe-link"); await symlink(outside, link, "dir");
  const plan = await planOutputDirectory(join(link, "new-package"), [source, tooling]);
  assert.equal(await createOutputDirectory(plan), join(outside, "new-package"));
  await assert.rejects(createOutputDirectory(plan), { code: "EEXIST" });
});
