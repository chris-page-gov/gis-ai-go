import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, symlink, rm } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { assertAllowlistedContext, contentRoot, inventoryTree, safeRelative, sha256, verifyPrepared } from "./prepare.mjs";

test("build context rejects archive, credential, source map, research and state injection", () => {
  for (const path of ["app/bundles/capture/x.json", "app/bundles/private/x.json", "app/.env", "app/credentials.json", "app/bundles/credentials.json", "app/node_modules/fake/application_default_credentials.json", "app/static/research/x.md", "app/bundles/a.zip", "app/runtime/a.map", "app/bundles/state.tfstate", "app/schemas/private/record.schema.json", "app/schemas/arbitrary.json", "../../secret", "app/runtime/a\\b.js", "app/runtime/a\n.js"]) {
    assert.throws(() => assertAllowlistedContext([{ path, bytes: 1, sha256: "0".repeat(64) }]), undefined, path);
  }
  assertAllowlistedContext([{ path: "Containerfile" }, { path: "app/runtime/gcp-main.mjs" }, { path: "app/bundles/okf-plus/search-index.json" }, { path: "app/schemas/catalogue-result.schema.json" }]);
});

test("content root binds exact bytes, paths and sizes independently of traversal order", () => {
  const rows = [{ path: "app/runtime/a.js", bytes: 1, sha256: sha256("x") }, { path: "Containerfile", bytes: 2, sha256: sha256("zz") }];
  assert.equal(contentRoot(rows), contentRoot([...rows].reverse()));
  assert.notEqual(contentRoot(rows), contentRoot([{ ...rows[0], bytes: 2 }, rows[1]]));
  assert.notEqual(contentRoot(rows), contentRoot([{ ...rows[0], path: "app/runtime/b.js" }, rows[1]]));
  assert.notEqual(contentRoot(rows), contentRoot([{ ...rows[0], sha256: sha256("y") }, rows[1]]));
});

test("regular-file inventory rejects links before reading their targets", async () => {
  const root = await mkdtemp(join(tmpdir(), "gcp-inventory-test-"));
  try {
    await writeFile(join(root, "safe.json"), "{}\n");
    const rows = await inventoryTree(root);
    assert.deepEqual(rows, [{ path: "safe.json", bytes: 3, sha256: sha256("{}\n") }]);
    await symlink("/etc/passwd", join(root, "linked.json"));
    await assert.rejects(inventoryTree(root), /Symbolic/);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("prepared verification refuses changed bytes and added allowed payloads", async () => {
  const root = await mkdtemp(join(tmpdir(), "gcp-prepared-test-"));
  try {
    await mkdir(join(root, "context/app/runtime"), { recursive: true });
    const runtime = join(root, "context/app/runtime/gcp-main.mjs");
    await writeFile(runtime, "export {};\n");
    const files = await inventoryTree(join(root, "context"));
    await writeFile(join(root, "manifest.json"), JSON.stringify({ schema: "gis-ai-go.gcp-prepared.v1", files, contextSha256: contentRoot(files) }));
    assert.equal((await verifyPrepared(root)).schema, "gis-ai-go.gcp-prepared.v1");
    await writeFile(runtime, "export default 1;\n");
    await assert.rejects(verifyPrepared(root), /changed/);
    await writeFile(runtime, "export {};\n");
    await writeFile(join(root, "context/app/runtime/extra.js"), "");
    await assert.rejects(verifyPrepared(root), /changed/);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("safe paths are closed to URL and filesystem substitution", () => {
  for (const path of ["", "/tmp/x", "file:///tmp/x", "../x", "a/../x", "a//x", "a/./x", "a\0b"]) assert.throws(() => safeRelative(path));
  assert.equal(safeRelative("app/bundles/okf-plus/source-lock.json"), "app/bundles/okf-plus/source-lock.json");
});
