import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { evaluatePreflight } from "../scripts/data_agent_kit_preflight.mjs";

function run(args, pathValue = "") {
  return evaluatePreflight(args, { pathValue });
}

function withDirectory(callback) {
  const directory = mkdtempSync(join(tmpdir(), "gis-dak-test-"));
  try { callback(directory); }
  finally { rmSync(directory, { recursive: true, force: true }); }
}

function evidenceArgs(path) {
  return ["--extension-list", path, "--extension-version", "1.2.3"];
}

test("workspace-only success makes no desktop or cloud acceptance claim", () => {
  const result = run(["--workspace-only"]);
  assert.equal(result.exitCode, 0);
  assert.equal(result.report.scope, "workspace-only");
  assert.equal(result.report.cloud_calls, 0);
  assert.equal(result.report.desktop_sign_in, "not-evaluated");
  assert.equal(result.report.project_identity_and_permissions, "not-evaluated");
  assert.equal(result.report.knowledge_catalog_retrieval, "not-evaluated");
});

test("missing local CLIs fail closed without inspecting authentication", () => {
  const result = run([]);
  assert.equal(result.exitCode, 2);
  assert.equal(result.report.checks.code_cli_available, false);
  assert.equal(result.report.checks.gcloud_cli_available, false);
  assert.equal(result.report.checks.exact_extension_version, false);
});

test("version evidence accepts UTF-8 and Windows PowerShell UTF-16LE inventories", () => {
  withDirectory((directory) => {
    for (const encoding of ["utf8", "utf16le"]) {
      const path = join(directory, encoding + ".txt");
      const text = "private.unrelated-publisher@9.9.9\r\ngooglecloudtools.datacloud@1.2.3\r\n";
      writeFileSync(path, (encoding === "utf16le" ? "\uFEFF" : "") + text, encoding);
      const result = run(evidenceArgs(path));
      assert.equal(result.report.checks.exact_extension_version, true);
      assert.equal(result.report.observed_extension_version, "1.2.3");
      assert.equal(result.exitCode, 2); // Version evidence does not replace missing CLIs.
      assert.equal(JSON.stringify(result).includes("private.unrelated-publisher"), false);
      assert.equal(JSON.stringify(result).includes(path), false);
    }
  });
});

test("ambiguous, malformed and mismatched inventories cannot establish a version pin", () => {
  withDirectory((directory) => {
    const path = join(directory, "extensions.txt");
    for (const text of [
      "GoogleCloudTools.datacloud@1.2.4\n",
      "GoogleCloudTools.datacloud@1.2.3\nGoogleCloudTools.datacloud@1.2.3\n",
      "GoogleCloudTools.datacloud@private-invalid-value\n",
      "other.extension@1.2.3\n",
    ]) {
      writeFileSync(path, text);
      const result = run(evidenceArgs(path));
      assert.equal(result.exitCode, 2);
      assert.equal(result.report.checks.exact_extension_version, false);
      assert.equal(JSON.stringify(result).includes("private-invalid-value"), false);
    }
  });
});

test("unreadable, non-file and oversized inventory evidence fails closed", () => {
  withDirectory((directory) => {
    const path = join(directory, "extensions.txt");
    writeFileSync(path, "GoogleCloudTools.datacloud@1.2.3\n" + " ".repeat(262_144));
    for (const candidate of [path, directory, join(directory, "missing.txt")]) {
      const result = run(evidenceArgs(candidate));
      assert.equal(result.exitCode, 2);
      assert.equal(result.report.checks.exact_extension_version, false);
      assert.equal(result.report.observed_extension_version, null);
      assert.equal(JSON.stringify(result).includes(candidate), false);
    }
  });
});

test("invalid arguments do not echo potentially private arguments", () => {
  for (const args of [
    ["--extension-version", "private-invalid-value"],
    ["--unknown-private-value"],
    ["--extension-list", "private-file-path"],
    ["--extension-list", "--workspace-only"],
    ["--extension-version", "1.2.3", "--extension-version", "1.2.4"],
    ["--workspace-only", "--workspace-only"],
    ["--workspace-only", ...evidenceArgs("private-file-path")],
  ]) {
    const result = run(args);
    assert.equal(result.exitCode, 1);
    assert.equal(result.report, null);
    assert.equal(JSON.stringify(result).includes("private-"), false);
  }
});

test("local prerequisite success discovers executable paths without running them", () => {
  withDirectory((directory) => {
    for (const name of ["code", "gcloud"]) {
      const path = join(directory, name + (process.platform === "win32" ? ".cmd" : ""));
      // This deliberately is not a runnable program: preflight must only inspect it.
      writeFileSync(path, "This executable must never be launched by preflight.\n");
      chmodSync(path, 0o700);
    }
    const path = join(directory, "extensions.txt");
    writeFileSync(path, "GoogleCloudTools.datacloud@1.2.3\n");
    const result = run(evidenceArgs(path), directory);
    assert.equal(result.exitCode, 0);
    assert.equal(result.report.status, "passed");
    assert.equal(result.report.checks.code_cli_available, true);
    assert.equal(result.report.checks.gcloud_cli_available, true);
    assert.equal(result.report.checks.exact_extension_version, true);
    assert.equal(result.report.desktop_sign_in, "not-evaluated");
    assert.equal(result.report.cloud_calls, 0);
  });
});
