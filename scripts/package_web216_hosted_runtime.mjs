// Offline packaging only. Does not install, provision, call a provider or deploy.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdir, readFile, readdir, realpath, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
assert(args.length === 4 && args[0] === "--tooling-root" && args[2] === "--output-dir",
  "Use --tooling-root <existing-esbuild-installation> --output-dir <new-output-directory>");
const tooling = await realpath(resolve(args[1]));
const output = resolve(args[3]);
const inside = (base, path) => {
  const part = relative(base, path);
  return part === "" || (!isAbsolute(part) && part !== ".." && !part.startsWith(`..${sep}`));
};
assert(!inside(ROOT, output) && !inside(tooling, output), "Package outside source and tooling checkouts");
const git = (...values) => execFileSync("git", values, { cwd: ROOT, maxBuffer: 8_388_608 });
const head = git("rev-parse", "HEAD").toString().trim();
assert(/^[0-9a-f]{40}$/.test(head));
assert.equal(git("status", "--porcelain", "--untracked-files=all").toString(), "", "Source must be clean");
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const esbuildManifest = JSON.parse(await readFile(join(tooling, "node_modules/esbuild/package.json"), "utf8"));
assert.equal(esbuildManifest.version, "0.28.1", "Use the already pinned compiler; no installation attempted");
const require = createRequire(join(tooling, "package.json"));
const { build } = await import(pathToFileURL(require.resolve("esbuild")).href);
const compiled = await build({
  absWorkingDir: ROOT,
  entryPoints: [join(ROOT, "scripts/web216_hosted_cpih_bundle_entry.ts")],
  bundle: true, write: false, format: "esm", platform: "neutral", target: "es2023",
  conditions: ["workerd"], external: ["node:*"], metafile: true,
  alias: { "@gis-ai-go/evidence/web216-pure": join(ROOT, "packages/evidence/src/web216-pure.ts") },
  nodePaths: [join(ROOT, "apps/mcp-gateway/node_modules")],
});
assert.equal(compiled.outputFiles.length, 1);
const bytes = compiled.outputFiles[0].contents;
assert(bytes.byteLength > 0 && bytes.byteLength <= 4_194_304);
const inputs = Object.keys(compiled.metafile.inputs).sort();
assert(inputs.some((path) => path.endsWith("/shimsWorkerd.mjs")));
assert(!inputs.some((path) => /\/shims(?:Node|Browser)\.mjs$/u.test(path)));
assert(!inputs.some((path) => /apps\/mcp-gateway\/src\/(?:mcp-server|governed-assembly|http-app|openapi)\.ts$/u.test(path)
  || path.includes("packages/tool-registry/") || path.includes("packages/evidence/dist/")
  || /packages\/evidence\/src\/(?:index|checkpoint|public-ledger|reconciliation-index)\.ts$/u.test(path)));
const externalImports = [...new Set(Object.values(compiled.metafile.outputs)
  .flatMap((value) => value.imports.map((item) => item.path)))].sort();
assert(externalImports.every((path) => ["node:async_hooks", "node:crypto", "node:util"].includes(path)),
  "Unreviewed external module in hosted bundle");
const materials = [];
const retained = new Map();
const dependencies = new Map();
for (const path of [...inputs, "pnpm-lock.yaml", "scripts/package_web216_hosted_runtime.mjs"]) {
  const actual = await realpath(resolve(ROOT, path));
  assert(inside(ROOT, actual), "Input escaped source checkout");
  const portable = relative(ROOT, actual).split(sep).join("/");
  const content = await readFile(actual);
  const dependency = portable.startsWith("node_modules/");
  if (!dependency) assert.deepEqual(content, git("show", `${head}:${portable}`),
    "Maintained input is not the exact tracked Git blob");
  if (dependency) {
    let directory = dirname(actual);
    let found = false;
    while (inside(join(ROOT, "node_modules"), directory)) {
      let manifest;
      try { manifest = JSON.parse(await readFile(join(directory, "package.json"), "utf8")); }
      catch (error) { if (error.code !== "ENOENT") throw error; }
      if (typeof manifest?.name === "string" && typeof manifest?.version === "string") {
        if (!dependencies.has(directory)) {
          const notices = [];
          for (const name of (await readdir(directory)).filter((name) => /^(?:licen[sc]e|notice|copying)(?:[.-].*)?$/iu.test(name)).sort()) {
            const notice = await readFile(join(directory, name), "utf8");
            assert(Buffer.byteLength(notice) <= 262_144, "Unexpectedly large licence notice");
            notices.push({ name, text: notice });
          }
          assert(notices.length > 0, `Missing redistribution notice for ${manifest.name}`);
          dependencies.set(directory, { name: manifest.name, version: manifest.version,
            licence: manifest.license ?? null, notices });
        }
        found = true;
        break;
      }
      directory = dirname(directory);
    }
    assert(found, "Dependency has no named package manifest");
  }
  const sha256 = hash(content);
  retained.set(sha256, content);
  materials.push({ path: portable, bytes: content.byteLength, sha256,
    binding: dependency ? "observed-installed-dependency-bytes" : "exact-tracked-git-blob" });
}
assert.equal(git("rev-parse", "HEAD").toString().trim(), head);
assert.equal(git("status", "--porcelain", "--untracked-files=all").toString(), "");
process.umask(0o077);
await mkdir(output, { mode: 0o700 }); // Refuse to replace an existing package.
await mkdir(join(output, "inputs"), { mode: 0o700 });
const save = (path, value) => writeFile(join(output, path), value, { mode: 0o600, flag: "wx" });
for (const [digest, content] of retained) await save(`inputs/${digest}`, content);
await save("web216-runtime.mjs", bytes);
const thirdParty = [...dependencies.values()].sort((a, b) => a.name.localeCompare(b.name));
const notices = thirdParty.map((item) => `${item.name} ${item.version}\n${item.notices.map((notice) => `${notice.name}\n${notice.text}`).join("\n")}`).join("\n\n");
await save("third-party-notices.txt", notices + "\n");
const manifest = {
  schema: "gis-ai-go.web216-hosted-runtime-package.v1", source_commit: head,
  bundle: { path: "web216-runtime.mjs", bytes: bytes.byteLength, sha256: hash(bytes) },
  compiler: { name: "esbuild", version: "0.28.1" },
  conditions: ["workerd"], required_compatibility_flags: ["nodejs_compat"],
  external_imports: externalImports, materials,
  third_party_notices: { path: "third-party-notices.txt", sha256: hash(notices + "\n"),
    dependencies: thirdParty.map(({ name, version, licence }) => ({ name, version, licence })) },
  boundary: { provider_egress: false, deployed: false, attested: false,
    installed_dependencies_attested: false, site_ingress_included: false },
};
await save("bundle-manifest.json", JSON.stringify(manifest, null, 2) + "\n");
await save("bundle-metafile.json", JSON.stringify(compiled.metafile, null, 2) + "\n");
console.log(JSON.stringify({ source_commit: head, bundle_sha256: manifest.bundle.sha256,
  bundle_bytes: bytes.byteLength, material_count: materials.length, output, deployed: false, attested: false }));
