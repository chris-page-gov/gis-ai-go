#!/usr/bin/env node
/** Offline release preparation. Only the enumerated context is a build input. */
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { lstat, mkdir, readFile, readdir, realpath, stat, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, extname, join, relative, resolve, sep } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const BASE_IMAGE = "node:24.19.0-bookworm-slim@sha256:3638d9a6fe4030bd716be989438248074489337ba3275657f93595428be4fc03";
const EXCLUDED_PARTS = new Set([".git", ".env", "capture", "private", "secrets", "research", "__pycache__", ".terraform", "test", "tests",
  "credentials.json", "application_default_credentials.json", "id_rsa", "id_ed25519"]);
const RUNTIME_SUFFIXES = new Set([".js", ".mjs", ".cjs", ".json", ".node", ".wasm", ".md", ".txt"]);
const SOURCE_SUFFIXES = new Set([".ts", ".js", ".mjs", ".cjs", ".json", ".jsonld", ".md", ".html", ".css", ".svg", ".py", ".yaml", ".yml", ".toml"]);
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const serialise = (value) => JSON.stringify(value, null, 2) + "\n";
const within = (base, path) => path === base || path.startsWith(base + sep);

export function safeRelative(value) {
  if (typeof value !== "string" || !value || value.includes("\\") || /[\x00-\x1f\x7f:]/u.test(value) ||
      value.startsWith("/") || value.split("/").some((part) => !part || part === "." || part === "..")) {
    throw new Error("Unsafe release path");
  }
  return value;
}

export async function inventoryTree(base, prefix = "") {
  const root = resolve(base);
  if ((await lstat(root)).isSymbolicLink()) throw new Error("Symbolic release root is forbidden");
  const rows = [];
  async function walk(directory, path) {
    for (const item of (await readdir(directory, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      const child = path ? path + "/" + item.name : item.name;
      safeRelative(child);
      if (item.isSymbolicLink()) throw new Error("Symbolic release input is forbidden: " + child);
      if (item.isDirectory()) await walk(join(directory, item.name), child);
      else if (item.isFile()) {
        const bytes = await readFile(join(directory, item.name));
        rows.push({ path: prefix ? prefix + "/" + child : child, bytes: bytes.length, sha256: sha256(bytes) });
      } else throw new Error("Release inputs must be regular files");
    }
  }
  await walk(root, "");
  return rows.sort((a, b) => a.path.localeCompare(b.path));
}

export function contentRoot(files) {
  return sha256(files.map(({ path, bytes, sha256: digest }) => `${digest} ${bytes} ${safeRelative(path)}\n`).sort().join(""));
}

export function assertAllowlistedContext(files) {
  for (const row of files) {
    const path = safeRelative(row.path), parts = path.split("/");
    if (parts.some((part) => EXCLUDED_PARTS.has(part) || part.startsWith(".env")) ||
        /(?:\.tfstate(?:\..*)?|\.pem|\.key|\.p12|\.zip|\.tar(?:\.gz)?|\.map|\.d\.(?:ts|mts|cts))$/u.test(path)) {
      throw new Error("Forbidden build input: " + path);
    }
    if (path !== "Containerfile" && !/^app\/(?:runtime|gateway|node_modules|static|bundles|licences)\//u.test(path) &&
        !/^app\/schemas\/[a-z0-9-]+\.schema\.json$/u.test(path) &&
        !["app/package.json", "app/runtime-config.json", "app/release-manifest.json"].includes(path)) {
      throw new Error("Input is outside the deliberate build allowlist: " + path);
    }
  }
  return true;
}

function run(command, args, label, output) {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: "utf8", maxBuffer: 16 * 1024 * 1024,
    timeout: 30 * 60 * 1000, env: { ...process.env, CI: "1" } });
  if (result.error || result.status !== 0) {
    if (output) {
      const diagnostic = join(output, "diagnostics-" + label.replace(/[^a-z0-9-]/giu, "-") + ".txt");
      // Local diagnostics are outside the upload context and have no publication authority.
      spawnSync("python3", ["-c", "import os,sys; fd=os.open(sys.argv[1],os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600);os.write(fd,sys.stdin.buffer.read());os.close(fd)", diagnostic],
        { input: `${result.stdout ?? ""}\n${result.stderr ?? ""}\n${result.error?.message ?? ""}` });
    }
    throw new Error(label + " failed; inspect local diagnostics; no upload occurred");
  }
  console.log(label + ": passed");
  return result.stdout;
}

async function copyFile(source, target) {
  if ((await lstat(source)).isSymbolicLink()) throw new Error("Symbolic payload input is forbidden");
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, await readFile(source), { mode: 0o644 });
}

async function copyRegularTree(source, target, admitted = () => true) {
  for (const row of await inventoryTree(source)) {
    if (admitted(row.path)) await copyFile(join(source, row.path), join(target, row.path));
  }
}

function findDependency(directory, name) {
  const require = createRequire(join(directory, "package.json"));
  for (const modules of require.resolve.paths(name) ?? []) {
    const candidate = join(modules, name, "package.json");
    if (existsSync(candidate)) return dirname(candidate);
  }
  throw new Error("Production dependency is missing: " + name);
}

/** Materialise the installed production closure without pnpm deploy or network access. */
export async function stageDependencyClosure(gateway, app) {
  const queue = [await realpath(gateway)], visited = new Set(), names = new Map(), packages = [];
  while (queue.length) {
    const directory = queue.shift();
    if (visited.has(directory)) continue;
    visited.add(directory);
    const pkg = JSON.parse(await readFile(join(directory, "package.json"), "utf8"));
    if (!/^(@[a-z0-9._-]+\/)?[a-z0-9._-]+$/iu.test(pkg.name) || typeof pkg.version !== "string") throw new Error("Invalid production package identity");
    if (names.has(pkg.name) && names.get(pkg.name) !== pkg.version) throw new Error("Conflicting package versions require a nested closure: " + pkg.name);
    names.set(pkg.name, pkg.version);
    const workspace = within(ROOT, directory) && !within(join(ROOT, "node_modules"), directory);
    if (!workspace && !within(join(ROOT, "node_modules"), directory)) throw new Error("Dependency escapes the installed lockfile closure");
    const target = directory === await realpath(gateway) ? join(app, "gateway") : join(app, "node_modules", pkg.name);
    await copyFile(join(directory, "package.json"), join(target, "package.json"));
    if (workspace) {
      await copyRegularTree(join(directory, "dist"), join(target, "dist"), (path) => !path.split("/").includes("test") &&
        !/(?:\.map|\.d\.ts)$/u.test(path));
    } else {
      await copyRegularTree(directory, target, (path) => !path.split("/").some((part) => ["node_modules", "test", "tests", "src"].includes(part)) &&
        !/(?:\.map|\.d\.(?:ts|mts|cts))$/u.test(path) && (RUNTIME_SUFFIXES.has(extname(path)) || /(?:^|\/)(?:licen[sc]e|notice|copying)(?:[.-]|$)/iu.test(path)));
    }
    const notices = [];
    for (const name of (await readdir(directory)).filter((name) => /^(?:licen[sc]e|notice|copying)(?:[.-].*)?$/iu.test(name)).sort()) {
      if ((await stat(join(directory, name))).isFile()) notices.push({ name, sha256: sha256(await readFile(join(directory, name))) });
    }
    if (workspace && !notices.length) {
      await copyFile(join(ROOT, "LICENSE"), join(target, "LICENSE"));
      notices.push({ name: "LICENSE", sha256: sha256(await readFile(join(ROOT, "LICENSE"))) });
    }
    if (!notices.length) throw new Error("Production dependency is missing its licence notice: " + pkg.name);
    packages.push({ name: pkg.name, version: pkg.version, licence: pkg.license ?? null, notices, workspace });
    const required = new Set([...Object.keys(pkg.dependencies ?? {}), ...Object.keys(pkg.peerDependencies ?? {})]);
    for (const name of required) {
      try { queue.push(await realpath(findDependency(directory, name))); }
      catch (error) { if (!pkg.peerDependenciesMeta?.[name]?.optional) throw error; }
    }
  }
  return packages.sort((a, b) => a.name.localeCompare(b.name));
}

async function sourceInventory(extraInputs = []) {
  const paths = new Set(["LICENSE", "VERSION", ".nvmrc", "package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "pyproject.toml", "uv.lock", "tsconfig.base.json",
    "scripts/build_okf.py", "infra/gcp/container/Containerfile", "infra/gcp/container/index.html", "infra/gcp/container/portal.css", ...extraInputs]);
  for (const folder of ["apps/mcp-gateway/src", "apps/mcp-gateway/openapi", "apps/public-explorer/src", "apps/public-explorer/scripts", "apps/public-explorer/public",
    "apps/webmcp-explorer/src", "apps/webmcp-explorer/scripts", "apps/webmcp-explorer/public", "apps/public-data-workbench/src", "scripts/gcp", "infra/gcp/container"]) {
    if (!existsSync(join(ROOT, folder))) continue;
    for (const row of await inventoryTree(join(ROOT, folder))) {
      if (!row.path.startsWith("catalogue/") && SOURCE_SUFFIXES.has(extname(row.path))) paths.add(folder + "/" + row.path);
    }
  }
  for (const folder of ["authority-context", "contracts", "evidence", "policy-client", "provider-adapter-sdk", "tool-registry", "experience-intake"]) {
    for (const row of await inventoryTree(join(ROOT, "packages", folder, "src"))) if (SOURCE_SUFFIXES.has(extname(row.path))) paths.add(`packages/${folder}/src/${row.path}`);
    paths.add(`packages/${folder}/package.json`); paths.add(`packages/${folder}/tsconfig.json`);
  }
  paths.add("evaluation/experience/catalogue.v1.json");
  paths.add("packages/tool-registry/scripts/copy-profile.mjs");
  for (const app of ["mcp-gateway", "public-explorer", "webmcp-explorer", "public-data-workbench"]) {
    for (const file of ["package.json", "tsconfig.json", "vite.config.ts", "index.html", "experience.html"]) {
      if (existsSync(join(ROOT, "apps", app, file))) paths.add(`apps/${app}/${file}`);
    }
  }
  const rows = [];
  for (const path of [...paths].sort()) {
    safeRelative(path);
    if (!within(ROOT, resolve(ROOT, path))) throw new Error("Source input escapes checkout");
    const info = await lstat(join(ROOT, path));
    if (!info.isFile() || info.isSymbolicLink()) throw new Error("Source input is not a regular file");
    const bytes = await readFile(join(ROOT, path));
    rows.push({ path, bytes: bytes.length, sha256: sha256(bytes) });
  }
  return rows;
}

export async function verifyPrepared(output) {
  const manifest = JSON.parse(await readFile(join(output, "manifest.json"), "utf8"));
  if (manifest.schema !== "gis-ai-go.gcp-prepared.v1") throw new Error("Unknown prepared manifest");
  const files = await inventoryTree(join(output, "context"));
  assertAllowlistedContext(files);
  if (serialise(files) !== serialise(manifest.files.map(({ classification, ...row }) => row)) || contentRoot(files) !== manifest.contextSha256) {
    throw new Error("Prepared context changed after manifest creation");
  }
  return manifest;
}

/** Reuse requires the complete existing public-export digest chain, never a status label alone. */
export async function verifyOkfPlus(directory, { revision, uv = process.env.GIS_AI_GO_UV ?? "uv", diagnostics } = {}) {
  directory = resolve(directory);
  if (![join(ROOT, "artifacts/gcp"), join(ROOT, "artifacts/okf-plus")].some((base) => within(base, directory))) {
    throw new Error("Reusable verification must be a local admitted OKF+ artefact");
  }
  revision ??= spawnSync("git", ["rev-parse", "HEAD"], { cwd: ROOT, encoding: "utf8" }).stdout.trim();
  if (!/^[0-9a-f]{40}$/u.test(revision)) throw new Error("Missing source revision");
  run(uv, ["run", "--locked", "--cache-dir", ".uv-cache", "python", "-c", `import sys\nfrom pathlib import Path\nsys.path.insert(0,'scripts/okf_plus')\nfrom export import source_paths,verified_generated\nroot=Path.cwd(); _,report=verified_generated(root,Path(sys.argv[1]),set(source_paths(root)))\nif report['sourceRevision']!=sys.argv[2]: raise ValueError('Verified source revision differs')\nprint('Reused complete verifier result after exact source/bundle/context digest-chain checks')`, directory, revision], "expanded-okf-verified-output-reuse", diagnostics);
  return JSON.parse(await readFile(join(directory, "verification.json"), "utf8"));
}

export async function prepare({ output, configPath, verifiedOkfPlus } = {}) {
  if (!output) throw new Error("--output is required");
  output = resolve(output);
  if (!within(join(ROOT, "artifacts", "gcp"), output) || output === join(ROOT, "artifacts", "gcp")) {
    throw new Error("Preparation output must be an isolated directory under artifacts/gcp");
  }
  if (existsSync(output) && (await readdir(output)).length) throw new Error("Use a new empty preparation directory");
  await mkdir(output, { recursive: true, mode: 0o700 });
  const config = configPath ? JSON.parse(await readFile(resolve(configPath), "utf8")) : undefined;
  if (config && !["personal-network-private", "bduk-sandpit-network-private"].includes(config.profile)) {
    throw new Error("Unknown deployment profile; preparation will not choose a personal fallback");
  }
  const git = (args) => spawnSync("git", args, { cwd: ROOT, encoding: "utf8" });
  const revision = git(["rev-parse", "HEAD"]).stdout.trim();
  if (!/^[0-9a-f]{40}$/u.test(revision)) throw new Error("Missing source revision");
  const sourceStatus = git(["status", "--porcelain=v1", "--untracked-files=all"]).stdout;
  const pnpm = process.env.GIS_AI_GO_PNPM ?? "pnpm";
  const uv = process.env.GIS_AI_GO_UV ?? "uv";
  const pnpmVersion = spawnSync(pnpm, ["--version"], { encoding: "utf8" }).stdout.trim();
  if (pnpmVersion !== "10.33.2") throw new Error("Pinned pnpm 10.33.2 is required; installation is separate and never mutates lockfiles");
  if (process.version !== "v24.19.0") throw new Error("Use the repository's pinned Node 24.19.0");
  const python = (args, label) => run(uv, ["run", "--locked", "--cache-dir", ".uv-cache", "python", ...args], label, output);
  const legacy = join(output, "checks", "okf"), expanded = verifiedOkfPlus ? resolve(verifiedOkfPlus) : join(output, "checks", "okf-plus");
  python(["scripts/build_okf.py", "--output", legacy, "--revision", revision], "legacy-okf-build");
  if (verifiedOkfPlus) {
    await verifyOkfPlus(expanded, { revision, uv, diagnostics: output });
  } else python(["scripts/okf_plus/verify.py", "--output", expanded, "--revision", revision], "expanded-okf-offline-verification");
  // Existing UI builders deliberately read the conventional public OKF path.
  python(["scripts/build_okf.py", "--output", "artifacts/okf", "--revision", revision], "ui-okf-input");
  for (const pkg of ["contracts", "evidence", "authority-context", "policy-client", "provider-adapter-sdk", "tool-registry", "mcp-gateway"]) {
    run(pnpm, ["--filter", "@gis-ai-go/" + pkg, "run", "build"], "typescript-" + pkg, output);
  }
  for (const pkg of ["public-explorer", "webmcp-explorer"]) run(pnpm, ["--filter", "@gis-ai-go/" + pkg, "run", "build"], "ui-" + pkg, output);
  run(pnpm, ["--filter", "@gis-ai-go/public-data-workbench", "run", "prepare:data"], "workbench-data", output);
  run(pnpm, ["--filter", "@gis-ai-go/public-data-workbench", "exec", "vite", "build", "--mode", "gcp"], "ui-private-workbench", output);
  run(pnpm, ["--filter", "@gis-ai-go/public-data-workbench", "run", "test:unit"], "workbench-tests", output);
  if (!existsSync(join(ROOT, "apps/mcp-gateway/dist/src/gcp-main.js"))) throw new Error("GCP runtime entrypoint has not been built");
  const legacyReceipt = JSON.parse(await readFile(join(legacy, "build-receipt.json"), "utf8"));
  const expandedReport = JSON.parse(await readFile(join(expanded, "verification.json"), "utf8"));
  const expandedCoverage = JSON.parse(await readFile(join(expanded, "bundle/coverage.json"), "utf8"));
  if (legacyReceipt.recordCount !== 36 || expandedCoverage.recordCount !== 30833 || expandedReport.status !== "passed-automated-checks") {
    throw new Error("The admitted legacy and expanded corpus gate changed; review before packaging");
  }
  const legacyLock = JSON.parse(await readFile(join(ROOT, "okf/source-lock.json"), "utf8"));
  const expandedLock = JSON.parse(await readFile(join(expanded, "bundle/source-lock.json"), "utf8"));
  const inputs = [...legacyLock.inputs, ...expandedLock.inputs].map(({ path }) => path);
  inputs.push("tests/fixtures/web216/current-cpih-projection.json", "scripts/web216_build_workbench_data.py", "scripts/web216_corpus.py", "scripts/web216_experiments.py", "tests/fixtures/web216/story-corpus.json", "profiles/tool-registry.v1.json");
  // The maintained HTTP assembly loads these canonical contracts on import.
  // Retain exactly its declared schema files, never the checkout or fixtures.
  const schemaSource = await readFile(join(ROOT, "apps/mcp-gateway/src/openapi.ts"), "utf8");
  const runtimeSchemas = [...new Set([...schemaSource.matchAll(/sharedSchema\(\s*"([a-z0-9-]+\.schema\.json)"/gu)].map((match) => match[1]))].sort();
  if (runtimeSchemas.length < 1) throw new Error("Canonical runtime schema declaration is missing");
  inputs.push(...runtimeSchemas.map((file) => "schemas/" + file));
  const sourceFiles = await sourceInventory(inputs), context = join(output, "context"), app = join(context, "app");
  await mkdir(app, { recursive: true });
  await copyFile(join(ROOT, "infra/gcp/container/Containerfile"), join(context, "Containerfile"));
  if (!(await readFile(join(context, "Containerfile"), "utf8")).includes("FROM " + BASE_IMAGE + "\n")) throw new Error("Base pin changed without manifest update");
  await copyRegularTree(legacy, join(app, "bundles/okf"));
  await copyRegularTree(join(expanded, "bundle"), join(app, "bundles/okf-plus"));
  await copyRegularTree(join(expanded, "context"), join(app, "bundles/okf-plus-context"));
  await copyFile(join(expanded, "verification.json"), join(app, "bundles/okf-plus-verification.json"));
  await copyFile(join(ROOT, "tests/fixtures/web216/current-cpih-projection.json"), join(app, "bundles/cpih-projection.json"));
  await copyRegularTree(join(ROOT, "apps/public-explorer/dist"), join(app, "static/explorer"));
  await copyRegularTree(join(ROOT, "apps/webmcp-explorer/dist"), join(app, "static/webmcp"));
  await copyRegularTree(join(ROOT, "apps/public-data-workbench/dist/gcp"), join(app, "static/workbench"));
  await copyFile(join(ROOT, "infra/gcp/container/index.html"), join(app, "static/index.html"));
  await copyFile(join(ROOT, "infra/gcp/container/portal.css"), join(app, "static/portal.css"));
  await copyRegularTree(join(ROOT, "infra/gcp/container/knowledge"), join(app, "static/knowledge"));
  const dependencies = await stageDependencyClosure(join(ROOT, "apps/mcp-gateway"), app);
  for (const file of runtimeSchemas) await copyFile(join(ROOT, "schemas", file), join(app, "schemas", file));
  run(process.execPath, ["--input-type=module", "-e", `import { createRequire } from 'node:module'; import { pathToFileURL } from 'node:url';\nawait import(${JSON.stringify(pathToFileURL(join(app, "gateway/dist/src/gcp-main.js")).href)});\nconst require=createRequire(${JSON.stringify(join(app, "gateway/package.json"))});\nawait import(pathToFileURL(require.resolve('openid-client')).href);\nconsole.log('Actual packaged runtime and maintained OIDC dependency imports passed without network calls');`], "packaged-runtime-import", output);
  await mkdir(join(app, "runtime"), { recursive: true });
  await writeFile(join(app, "runtime/gcp-main.mjs"), 'import { runGcpMain } from "../gateway/dist/src/gcp-main.js";\nawait runGcpMain().catch(() => { process.stderr.write("Private runtime startup failed; no readiness is claimed.\\n"); process.exitCode = 1; });\n');
  await writeFile(join(app, "package.json"), serialise({ name: "gis-ai-go-private-gcp-pilot", version: "0.1.0", private: true, type: "module" }));
  await copyFile(join(ROOT, "LICENSE"), join(app, "licences/LICENSE"));
  await copyFile(join(ROOT, "THIRD_PARTY.md"), join(app, "licences/THIRD_PARTY.md"));
  for (const file of ["LICENSE.md", "LICENSE-CODE.md"]) {
    await copyFile(join(ROOT, "okf-plus/vendor/explorer-context", file), join(app, "licences", "okf-plus-explorer-" + file));
  }
  await writeFile(join(app, "licences/runtime-dependencies.json"), serialise(dependencies));
  const bduk = config?.profile === "bduk-sandpit-network-private";
  const runtimeConfig = { schema: "gis-ai-go.gcp-runtime.v1", profile: bduk ? "bduk" : "personal",
    publicOrigin: null, allowedOrigins: bduk ? [] : ["http://127.0.0.1:8789"],
    transportSubject: null, transportAudience: null,
    firestore: { projectId: null, databaseId: null, collection: null },
    identity: bduk ? { mode: "oidc", issuer: null, audience: null, jwksUri: null, claimMappings: null }
      : { mode: "single-owner-transport-pilot" },
    evidence: null };
  await writeFile(join(app, "runtime-config.json"), serialise(runtimeConfig));
  const payloadFiles = await inventoryTree(app);
  const releaseSha256 = contentRoot(payloadFiles), bundles = [
    { id: "okf", path: "bundles/okf", record_count: 36, profile: legacyReceipt.profile,
      source_lock_sha256: legacyReceipt.sourceLockSha256, content_root_sha256: legacyReceipt.contentRootSha256, producer: { name: "scripts/build_okf.py", version: legacyReceipt.builderVersion } },
    { id: "okf-plus", path: "bundles/okf-plus", context_path: "bundles/okf-plus-context", record_count: 30833,
      profile: JSON.parse(await readFile(join(expanded, "bundle/okf-bundle.json"), "utf8")).profile,
      source_lock_sha256: sha256(await readFile(join(expanded, "bundle/source-lock.json"))), input_digest: expandedLock.sha256,
      content_root_sha256: contentRoot(await inventoryTree(join(expanded, "bundle"))),
      verifier: { name: "scripts/okf_plus/verify.py", sha256: expandedReport.implementationSha256, status: expandedReport.status },
      limitations: expandedReport.limitations, record_grain: "Source-native catalogue representations; not deduplicated products", source_vintage: expandedCoverage.catalogues.map(({ family, retrievedAt }) => ({ family, retrievedAt })) },
  ];
  const release = { schema: "gis-ai-go.gcp-release.v1", source_revision: revision, release_sha256: releaseSha256,
    source_inputs_sha256: contentRoot(sourceFiles), bundles, files: payloadFiles,
    consumers: { "/": { kind: "navigation-to-release-backed-surfaces", overview: ["okf", "okf-plus", "cpih-projection"] },
      "/knowledge": "okf-plus", "/api/knowledge": ["okf", "okf-plus"], "/workbench": "cpih-projection", "/explorer": "okf", "/webmcp": "okf", "/mcp": ["okf", "okf-plus", "cpih-projection"] },
    boundary: { content: ["admitted-public-metadata", "redistributable-projections"], provider_egress: false, external_model_calls: false,
      private_original_archives: false, credentials: false, bduk_secure_data: false, licensed_feature_payloads: false,
      hosted_authentication: "not-observed", durable_hosted_acceptance: "not-observed", bduk_acceptance: "not-observed" } };
  await writeFile(join(app, "release-manifest.json"), serialise(release));
  // Reuse the reviewed public-export scanner on actual outgoing metadata and
  // browser assets. Installed code has its own locked dependency/notice closure.
  python(["-c", `import sys\nfrom pathlib import Path\nsys.path.insert(0,'scripts/okf_plus')\nfrom export import check_public, public_patterns\nroot=Path.cwd(); context=Path(sys.argv[1]); patterns=public_patterns(root); count=0\nfor base in ('app/bundles','app/static'):\n for path in sorted((context/base).rglob('*')):\n  if path.is_file():\n   raw=path.read_bytes()\n   try: raw.decode('utf-8') if path.suffix!='.gz' else None\n   except UnicodeDecodeError: continue\n   check_public(raw,path.relative_to(context).as_posix(),patterns); count+=1\nprint('Scanned',count,'outgoing public data and browser assets; no secret/machine-path match')`, context], "outgoing-public-content-scan");
  const files = await inventoryTree(context);
  assertAllowlistedContext(files);
  // Ensure preparation never silently bound a moving working tree.
  for (const row of sourceFiles) if (sha256(await readFile(join(ROOT, row.path))) !== row.sha256) throw new Error("Source changed during packaging: " + row.path);
  if (git(["rev-parse", "HEAD"]).stdout.trim() !== revision) throw new Error("Source revision changed during packaging");
  const changedPaths = new Set(sourceStatus.split("\n").filter(Boolean).map((row) => row.slice(3)));
  const includedUncommitted = sourceFiles.filter(({ path }) => changedPaths.has(path));
  const manifest = { schema: "gis-ai-go.gcp-prepared.v1", sourceCommit: revision, sourceSha256: contentRoot(sourceFiles),
    workingTree: { statusSha256: sha256(sourceStatus), includedUncommitted, authority: "Actual local source; no public checkpoint reset" },
    sourceFiles, releaseId: releaseSha256, releaseSha256, contextSha256: contentRoot(files), baseImage: BASE_IMAGE,
    containerfile: "context/Containerfile", contextPath: "context", imageBuild: { command: "docker build --network=none --platform linux/amd64 -f context/Containerfile context", network: "Pinned base image registry pull only; RUN has no network" },
    bundles, dependencies, installedDependencyEvidence: { status: "observed-installed-dependency-bytes", attested: false,
      lockfile: "pnpm-lock.yaml", lockfileSha256: sha256(await readFile(join(ROOT, "pnpm-lock.yaml"))) },
    tests: { expanded_okf: expandedReport.status, workbench_unit: "passed", ui_boundary: "passed", typescript_build: "passed", packaged_runtime_import: "passed" },
    files: files.map((row) => ({ ...row, classification: row.path.startsWith("app/bundles/") || row.path.includes("/catalogue/") ? "admitted-public-metadata" : "application-code-and-local-assets" })),
    uploadInventory: { fileCount: files.length, totalBytes: files.reduce((sum, row) => sum + row.bytes, 0), credentials: 0,
      protectedBdukData: 0, licensedFeaturePayloads: 0, privateOriginalArchives: 0, stateFiles: 0 },
    runtimeConfiguration: { path: "app/runtime-config.json", readiness: "unresolved-template-requires-approved-runtime-binding", secretsIncluded: false },
    acceptance: { localOffline: true, containerBuild: false, hostedAuthentication: false, hostedPersistence: false, bduk: false } };
  await writeFile(join(output, "source-manifest.json"), serialise({ schema: "gis-ai-go.gcp-source.v1", sourceCommit: revision, sourceSha256: manifest.sourceSha256, files: sourceFiles, includedUncommitted }));
  await writeFile(join(output, "manifest.json"), serialise(manifest));
  await verifyPrepared(output);
  return manifest;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), options = {};
  while (args.length) {
    const argument = args.shift();
    if (argument === "--output") options.output = args.shift();
    else if (argument === "--config") options.configPath = args.shift();
    else if (argument === "--verified-okf-plus") options.verifiedOkfPlus = args.shift();
    else if (argument === "--verify-prepared") options.verifyPrepared = args.shift();
    else if (argument === "--verify-okf-plus") options.verifyOkfPlus = args.shift();
    else throw new Error("Unknown prepare option: " + argument);
  }
  try {
    if (options.verifyPrepared) {
      const result = await verifyPrepared(resolve(options.verifyPrepared));
      console.log(JSON.stringify({ status: "verified-prepared-local-only", sourceCommit: result.sourceCommit, releaseId: result.releaseId,
        contextSha256: result.contextSha256, uploadInventory: result.uploadInventory, hosted: false }));
    } else if (options.verifyOkfPlus) {
      const result = await verifyOkfPlus(options.verifyOkfPlus);
      console.log(JSON.stringify({ status: "verified-okf-plus-local-only", sourceRevision: result.sourceRevision, inputDigest: result.inputDigest,
        hosted: false }));
    } else {
      const result = await prepare(options);
      console.log(JSON.stringify({ status: "prepared-local-only", sourceCommit: result.sourceCommit, releaseId: result.releaseId,
        contextSha256: result.contextSha256, uploadInventory: result.uploadInventory, hosted: false }));
    }
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
