#!/usr/bin/env node
/** Offline workspace/prerequisite checks; never installs, authenticates or calls Google. */
import { accessSync, constants, readFileSync, statSync } from "node:fs";
import { delimiter, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const extensionId = "GoogleCloudTools.datacloud";
const usage = "Use --workspace-only, or --extension-list FILE --extension-version X.Y.Z.\n";

function available(name, pathValue) {
  const suffixes = process.platform === "win32" ? ["", ".exe", ".cmd", ".bat"] : [""];
  return pathValue.split(delimiter).filter(Boolean).some((directory) =>
    suffixes.some((suffix) => {
      try {
        const candidate = join(directory, name + suffix);
        if (!statSync(candidate).isFile()) return false;
        accessSync(candidate, process.platform === "win32" ? constants.F_OK : constants.X_OK);
        return true;
      } catch { return false; }
    }));
}

function checkJson(relativePath, predicate) {
  try { return predicate(JSON.parse(readFileSync(join(root, relativePath), "utf8"))); }
  catch { return false; }
}

/** Evaluate local evidence without writing output, launching processes or changing state. */
export function evaluatePreflight(args = [], { pathValue = process.env.PATH ?? "" } = {}) {
  let workspaceOnly = false;
  let inventory;
  let expectedVersion;
  try {
    for (let index = 0; index < args.length; index += 1) {
      const argument = args[index];
      const value = args[index + 1];
      const hasValue = typeof value === "string" && value.length > 0 && !value.startsWith("--");
      if (argument === "--workspace-only" && !workspaceOnly) workspaceOnly = true;
      else if (argument === "--extension-list" && !inventory && hasValue) inventory = args[++index];
      else if (argument === "--extension-version" && !expectedVersion && hasValue) expectedVersion = args[++index];
      else throw Error("Invalid arguments");
    }
    if (expectedVersion && !/^\d+\.\d+\.\d+$/u.test(expectedVersion)) throw Error("Invalid version");
    if (Boolean(inventory) !== Boolean(expectedVersion)) throw Error("Incomplete evidence arguments");
    if (workspaceOnly && (inventory || expectedVersion)) throw Error("Choose one scope");
  } catch {
    return { exitCode: 1, report: null, error: usage };
  }

  const checks = {
    extension_recommended: checkJson(".vscode/extensions.json", (value) =>
      Array.isArray(value.recommendations) && value.recommendations.some((id) => id.toLowerCase() === extensionId.toLowerCase())),
    notebook_execution_disabled: checkJson(".vscode/settings.json", (value) =>
      value["google.datacloud.executeCellToolForNotebookMCP"] === false),
  };
  let observedVersion = null;
  if (!workspaceOnly) {
    checks.code_cli_available = available("code", pathValue);
    checks.gcloud_cli_available = available("gcloud", pathValue);
    checks.exact_extension_version = false;
    if (inventory && expectedVersion) {
      try {
        const path = resolve(inventory);
        const stat = statSync(path);
        if (!stat.isFile() || stat.size > 262_144) throw Error("Invalid inventory");
        // Windows PowerShell 5 redirection writes UTF-16LE; PS7 and POSIX use UTF-8.
        const bytes = readFileSync(path);
        if (bytes.length > 262_144) throw Error("Invalid inventory");
        const text = bytes[0] === 0xff && bytes[1] === 0xfe
          ? bytes.subarray(2).toString("utf16le") : bytes.toString("utf8").replace(/^\uFEFF/u, "");
        const rows = text.split(/\r?\n/u).map((line) => line.trim()).filter((line) =>
          line.toLowerCase().startsWith(extensionId.toLowerCase() + "@"));
        const version = rows.length === 1 ? rows[0].slice(extensionId.length + 1) : "";
        if (/^\d+\.\d+\.\d+$/u.test(version)) observedVersion = version;
        checks.exact_extension_version = observedVersion === expectedVersion;
      } catch { /* Only emit the closed check result, never private file contents. */ }
    }
  }
  const passed = Object.values(checks).every((value) => value === true);
  return {
    exitCode: passed ? 0 : 2,
    report: {
      schema: "gis-ai-go.data-agent-kit-preflight.v1",
      scope: workspaceOnly ? "workspace-only" : "local-prerequisites",
      status: passed ? "passed" : "blocked",
      extension_id: extensionId,
      observed_extension_version: observedVersion,
      checks,
      cloud_calls: 0,
      desktop_sign_in: "not-evaluated",
      project_identity_and_permissions: "not-evaluated",
      knowledge_catalog_retrieval: "not-evaluated",
    },
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = evaluatePreflight(process.argv.slice(2));
  if (result.report) process.stdout.write(JSON.stringify(result.report, null, 2) + "\n");
  else process.stderr.write(result.error);
  process.exitCode = result.exitCode;
}
