// Offline packaging only. Does not install, provision, call a provider or deploy.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { lstat, mkdir, open, readFile, readdir, realpath, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { basename, dirname, extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const MAX_INPUT_BYTES = 8_388_608;
const MAX_CAPTURE_BYTES = 33_554_432;
const LOADERS = Object.freeze({ ".ts": "ts", ".js": "js", ".mjs": "js", ".cjs": "js", ".json": "json" });
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const inside = (base, path) => {
  const part = relative(base, path);
  return part === "" || (!isAbsolute(part) && part !== ".." && !part.startsWith(`..${sep}`));
};
async function readBoundedFile(path, maximum = MAX_INPUT_BYTES) {
  const handle = await open(path, "r");
  try {
    assert((await handle.stat()).isFile(), "Input must be a regular file");
    const chunks = []; let length = 0;
    while (true) {
      const chunk = Buffer.alloc(Math.min(65_536, maximum + 1 - length));
      const { bytesRead } = await handle.read(chunk);
      if (bytesRead === 0) break;
      length += bytesRead; assert(length <= maximum, "Input exceeds bounded byte limit");
      chunks.push(chunk.subarray(0, bytesRead));
    }
    return Buffer.concat(chunks, length);
  } finally { await handle.close(); }
}

/** Captured bytes stay private; the compiler and output writer receive copies. */
export function createVerifiedFileLoader({ root, trackedBytes, readBytes = readBoundedFile, resolvePath = realpath }) {
  const captured = new Map(); const requestedPaths = new Map(); let totalBytes = 0;
  async function capture(path) {
    const requested = resolve(root, path);
    const actual = await resolvePath(requested);
    assert(inside(root, actual), "Input escaped source checkout");
    requestedPaths.set(requested, actual);
    if (captured.has(actual)) return captured.get(actual);
    const portable = relative(root, actual).split(sep).join("/");
    const content = Buffer.from(await readBytes(actual));
    assert(content.byteLength <= MAX_INPUT_BYTES, "Input exceeds bounded byte limit");
    const dependency = portable.startsWith("node_modules/");
    if (!dependency) assert.deepEqual(content, await trackedBytes(portable),
      "Maintained input is not the exact tracked Git blob");
    totalBytes += content.byteLength;
    assert(totalBytes <= MAX_CAPTURE_BYTES, "Captured inputs exceed total byte limit");
    const entry = { actual, content, material: Object.freeze({ path: portable, bytes: content.byteLength,
      sha256: hash(content), binding: dependency ? "observed-installed-dependency-bytes" : "exact-tracked-git-blob" }) };
    captured.set(actual, entry); return entry;
  }
  return {
    plugin: { name: "web216-verified-file-bytes", setup(build) {
      build.onLoad({ filter: /.*/, namespace: "file" }, async ({ path }) => {
        const loader = LOADERS[extname(path)]; assert(loader, "Unsupported compiler input loader");
        const entry = await capture(path);
        return { contents: Uint8Array.from(entry.content), loader, resolveDir: dirname(entry.actual) };
      });
    } },
    capture: async (path) => (await capture(path)).material,
    entry(path) {
      const requested = resolve(root, path);
      const entry = captured.get(requestedPaths.get(requested) ?? requested);
      assert(entry, "Compiler input was not captured by the verified loader");
      return { actual: entry.actual, material: entry.material, content: Buffer.from(entry.content) };
    },
  };
}

/** Existing parents must resolve outside protected roots before creating output. */
export async function planOutputDirectory(requestedPath, protectedDirectories) {
  const requested = resolve(requestedPath);
  const parent = await realpath(dirname(requested));
  const protectedRoots = await Promise.all(protectedDirectories.map((path) => realpath(path)));
  const output = join(parent, basename(requested));
  assert(protectedRoots.every((root) => !inside(root, output)), "Package outside source and tooling checkouts");
  return Object.freeze({ requested, parent, output, protectedRoots: Object.freeze(protectedRoots) });
}
export async function createOutputDirectory(plan) {
  assert.equal(await realpath(dirname(plan.requested)), plan.parent, "Destination parent changed after validation");
  await mkdir(plan.output, { mode: 0o700 }); // Refuse existing packages and symlinks.
  const actual = await realpath(plan.output); const identity = await lstat(plan.output);
  assert.equal(actual, plan.output, "Created destination resolved elsewhere");
  assert(identity.isDirectory() && !identity.isSymbolicLink(), "Destination must be a new real directory");
  assert(plan.protectedRoots.every((root) => !inside(root, actual)), "Destination entered a protected checkout");
  return actual;
}

async function main(args) {
assert(args.length === 4 && args[0] === "--tooling-root" && args[2] === "--output-dir",
  "Use --tooling-root <existing-esbuild-installation> --output-dir <new-output-directory>");
const tooling = await realpath(resolve(args[1]));
const destination = await planOutputDirectory(args[3], [ROOT, tooling]);
const git = (...values) => execFileSync("git", values, { cwd: ROOT, maxBuffer: 8_388_608 });
const head = git("rev-parse", "HEAD").toString().trim();
assert(/^[0-9a-f]{40}$/.test(head));
assert.equal(git("status", "--porcelain", "--untracked-files=all").toString(), "", "Source must be clean");
const loader = createVerifiedFileLoader({ root: await realpath(ROOT), trackedBytes: (path) => git("show", `${head}:${path}`) });
const supporting = ["pnpm-lock.yaml", "scripts/package_web216_hosted_runtime.mjs", "LICENSE"];
for (const path of supporting) await loader.capture(path);
const esbuildManifest = JSON.parse(await readFile(join(tooling, "node_modules/esbuild/package.json"), "utf8"));
assert.equal(esbuildManifest.version, "0.28.1", "Use the already pinned compiler; no installation attempted");
const require = createRequire(join(tooling, "package.json"));
const { build } = await import(pathToFileURL(require.resolve("esbuild")).href);
const compiled = await build({
  absWorkingDir: ROOT,
  entryPoints: [join(ROOT, "scripts/web216_hosted_cpih_bundle_entry.ts")],
  bundle: true, write: false, format: "esm", platform: "neutral", target: "es2023",
  conditions: ["workerd"], external: ["node:*"], metafile: true, plugins: [loader.plugin],
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
for (const path of [...new Set([...inputs, ...supporting])]) {
  // These are the captured buffers supplied to the compiler, never file rereads.
  const { actual, content, material } = loader.entry(path);
  const dependency = material.binding === "observed-installed-dependency-bytes";
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
  materials.push(material);
}
assert.equal(git("rev-parse", "HEAD").toString().trim(), head);
assert.equal(git("status", "--porcelain", "--untracked-files=all").toString(), "");
process.umask(0o077);
const output = await createOutputDirectory(destination);
await mkdir(join(output, "inputs"), { mode: 0o700 });
const save = (path, value) => writeFile(join(output, path), value, { mode: 0o600, flag: "wx" });
for (const [digest, content] of retained) await save(`inputs/${digest}`, content);
await save("web216-runtime.mjs", bytes);
const projectLicence = loader.entry("LICENSE");
await save("LICENSE", projectLicence.content);
const thirdParty = [...dependencies.values()].sort((a, b) => a.name.localeCompare(b.name));
const notices = thirdParty.map((item) => `${item.name} ${item.version}\n${item.notices.map((notice) => `${notice.name}\n${notice.text}`).join("\n")}`).join("\n\n");
await save("third-party-notices.txt", notices + "\n");
const manifest = {
  schema: "gis-ai-go.web216-hosted-runtime-package.v1", source_commit: head,
  bundle: { path: "web216-runtime.mjs", bytes: bytes.byteLength, sha256: hash(bytes) },
  compiler: { name: "esbuild", version: "0.28.1" },
  conditions: ["workerd"], required_compatibility_flags: ["nodejs_compat"],
  external_imports: externalImports, materials,
  project_licence: { path: "LICENSE", bytes: projectLicence.material.bytes, sha256: projectLicence.material.sha256 },
  third_party_notices: { path: "third-party-notices.txt", sha256: hash(notices + "\n"),
    dependencies: thirdParty.map(({ name, version, licence }) => ({ name, version, licence })) },
  boundary: { provider_egress: false, deployed: false, attested: false,
    installed_dependencies_attested: false, site_ingress_included: false },
};
await save("bundle-metafile.json", JSON.stringify(compiled.metafile, null, 2) + "\n");
await save("bundle-manifest.json", JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify({ source_commit: head, bundle_sha256: manifest.bundle.sha256,
  bundle_bytes: bytes.byteLength, material_count: materials.length, output, deployed: false, attested: false }));
}

if (process.argv[1] !== undefined && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main(process.argv.slice(2));
}
