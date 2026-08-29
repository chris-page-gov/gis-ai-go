#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { homedir, platform } from "node:os";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";

export const CHROME_WEBMCP_FLAGS = Object.freeze([
  {
    id: "enable-webmcp-testing",
    label: "WebMCP for testing",
    url: "chrome://flags/#enable-webmcp-testing",
    defaultEnabledFromMajor: null,
    plane: "native_page_api",
  },
  {
    id: "devtools-webmcp-support",
    label: "DevTools WebMCP support",
    url: "chrome://flags/#devtools-webmcp-support",
    defaultEnabledFromMajor: 152,
    plane: "devtools_panel",
  },
]);

export const VALIDATED_CHROME_MAJORS = Object.freeze([152]);

export function defaultChromeDataRoot(options = {}) {
  const operatingSystem = options.platform ?? platform();
  const homeDirectory = options.homeDirectory ?? homedir();
  if (operatingSystem === "darwin") {
    return join(homeDirectory, "Library", "Application Support", "Google", "Chrome");
  }
  if (operatingSystem === "linux") {
    return join(homeDirectory, ".config", "google-chrome");
  }
  if (operatingSystem === "win32" && options.localAppData) {
    return join(options.localAppData, "Google", "Chrome", "User Data");
  }
  throw new Error(`Google Chrome data location is not known for ${operatingSystem}.`);
}

function persistedFlagValue(experiments, id) {
  return experiments.find((value) => value === id || value.startsWith(`${id}@`)) ?? null;
}

function chromeMajor(version) {
  const match = /^(\d+)\./.exec(version);
  return match === null ? null : Number.parseInt(match[1], 10);
}

export function inspectChromeLocalState(localState, version = "unknown") {
  const experiments = localState?.browser?.enabled_labs_experiments;
  if (!Array.isArray(experiments) || !experiments.every((value) => typeof value === "string")) {
    throw new Error("Chrome Local State has no valid enabled_labs_experiments list.");
  }

  const profileMajorVersion = chromeMajor(version);
  const versionValidated =
    profileMajorVersion !== null && VALIDATED_CHROME_MAJORS.includes(profileMajorVersion);
  const flags = CHROME_WEBMCP_FLAGS.map((flag) => {
    const persistedValue = persistedFlagValue(experiments, flag.id);
    const explicitlyEnabled =
      persistedValue === flag.id || persistedValue === `${flag.id}@1`;
    const explicitlyDisabled = persistedValue === `${flag.id}@2`;
    const enabledByVersionDefault =
      persistedValue === null &&
      flag.defaultEnabledFromMajor !== null &&
      profileMajorVersion !== null &&
      profileMajorVersion >= flag.defaultEnabledFromMajor;
    return {
      id: flag.id,
      label: flag.label,
      url: flag.url,
      plane: flag.plane,
      expectedFromPersistedState:
        explicitlyEnabled || (!explicitlyDisabled && enabledByVersionDefault),
      state: explicitlyEnabled
        ? "enabled_override"
        : explicitlyDisabled
          ? "disabled_override"
          : enabledByVersionDefault
            ? "default_enabled_for_profile_version"
            : "default_or_unknown",
      persistedValue,
    };
  });
  const nativePageFlag = flags.find((flag) => flag.plane === "native_page_api");
  const devtoolsPanelFlag = flags.find((flag) => flag.plane === "devtools_panel");
  const planes = {
    nativePageApi: {
      persistedConfigurationObserved:
        versionValidated && nativePageFlag?.expectedFromPersistedState === true,
    },
    devtoolsPanel: {
      persistedConfigurationObserved:
        versionValidated && devtoolsPanelFlag?.expectedFromPersistedState === true,
    },
  };
  return {
    schema: "gis-ai-go.chrome-webmcp-preflight.v1",
    browser: {
      name: "Google Chrome",
      profileLastVersion: version,
      profileMajorVersion,
      validatedMajorVersions: VALIDATED_CHROME_MAJORS,
      versionValidated,
    },
    flags,
    planes,
    boundary: {
      changes_settings: false,
      proves_active_api: false,
      proves_browser_relaunched: false,
      reads_running_binary_version: false,
      native_manual_validation_requires_remote_debugging: false,
      external_devtools_automation_checked: false,
    },
  };
}

export async function readChromePreflight(options = {}) {
  const chromeDataRoot =
    options.chromeDataRoot ??
    defaultChromeDataRoot({
      localAppData: process.env.LOCALAPPDATA,
    });
  const localStatePath = options.localStatePath ?? join(chromeDataRoot, "Local State");
  const versionPath = options.versionPath ?? join(dirname(localStatePath), "Last Version");
  const [localStateText, versionText] = await Promise.all([
    readFile(localStatePath, "utf8"),
    readFile(versionPath, "utf8"),
  ]);
  return inspectChromeLocalState(JSON.parse(localStateText), versionText.trim());
}

export function parseArguments(argv) {
  const options = { json: false };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--json") {
      options.json = true;
    } else if (argument === "--local-state") {
      const value = argv.at(index + 1);
      if (value === undefined || value.startsWith("--")) {
        throw new Error("--local-state requires a file path.");
      }
      options.localStatePath = value;
      index += 1;
    } else if (argument === "--last-version") {
      const value = argv.at(index + 1);
      if (value === undefined || value.startsWith("--")) {
        throw new Error("--last-version requires a file path.");
      }
      options.versionPath = value;
      index += 1;
    } else {
      throw new Error(`Unknown or incomplete argument: ${argument}`);
    }
  }
  return options;
}

function formatHuman(result) {
  const lines = [
    "GIS AI GO Chrome WebMCP preflight",
    `Chrome profile Last Version: ${result.browser.profileLastVersion}`,
  ];
  if (!result.browser.versionValidated) {
    lines.push(
      `REVIEW REQUIRED: this procedure currently records evidence for Chrome ${
        result.browser.validatedMajorVersions.join(", ")
      } only.`,
    );
  }
  for (const flag of result.flags) {
    if (flag.state === "enabled_override") {
      lines.push(`PASS (persisted override): ${flag.label}`);
    } else if (flag.state === "default_enabled_for_profile_version") {
      lines.push(`INFO (enabled by this Chrome version's default): ${flag.label}`);
    } else {
      lines.push(`ACTION REQUIRED: ${flag.label}`);
      lines.push(`  Open ${flag.url}, choose Enabled, then relaunch Chrome.`);
    }
  }
  lines.push(
    `Native page API: ${
      result.planes.nativePageApi.persistedConfigurationObserved
        ? "PERSISTED CONFIGURATION OBSERVED; RUN THE LIVE PAGE PROBE"
        : "ACTION REQUIRED"
    }`,
  );
  lines.push(
    `DevTools WebMCP panel: ${
      result.planes.devtoolsPanel.persistedConfigurationObserved
        ? "PERSISTED CONFIGURATION OBSERVED; VERIFY THE LIVE PANEL"
        : "ACTION REQUIRED FOR PANEL VALIDATION"
    }`,
  );
  lines.push(
    "This read-only check does not inspect the running binary, prove a relaunch or " +
      "prove the active WebMCP API.",
  );
  return lines.join("\n");
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const result = await readChromePreflight(options);
  process.stdout.write(`${options.json ? JSON.stringify(result, null, 2) : formatHuman(result)}\n`);
  if (
    !result.planes.nativePageApi.persistedConfigurationObserved ||
    !result.planes.devtoolsPanel.persistedConfigurationObserved
  ) {
    process.exitCode = 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    process.stderr.write(
      `Chrome WebMCP preflight failed: ${
        error instanceof Error ? error.message : String(error)
      }\n`,
    );
    process.exitCode = 1;
  });
}
