import assert from "node:assert/strict";
import test from "node:test";

import {
  VALIDATED_CHROME_MAJORS,
  defaultChromeDataRoot,
  inspectChromeLocalState,
  parseArguments,
} from "../../scripts/chrome-preflight.mjs";

test("reports persisted native WebMCP configuration without requiring a DevTools override", () => {
  const result = inspectChromeLocalState(
    {
      browser: {
        enabled_labs_experiments: ["enable-webmcp-testing@1"],
      },
    },
    "152.0.7977.64",
  );

  assert.equal(result.browser.profileLastVersion, "152.0.7977.64");
  assert.deepEqual(result.browser.validatedMajorVersions, VALIDATED_CHROME_MAJORS);
  assert.equal(result.browser.versionValidated, true);
  assert.equal(result.planes.nativePageApi.persistedConfigurationObserved, true);
  assert.equal(result.planes.devtoolsPanel.persistedConfigurationObserved, true);
  assert.deepEqual(
    result.flags.map(({ expectedFromPersistedState, state }) => ({
      expectedFromPersistedState,
      state,
    })),
    [
      { expectedFromPersistedState: true, state: "enabled_override" },
      {
        expectedFromPersistedState: true,
        state: "default_enabled_for_profile_version",
      },
    ],
  );
  assert.equal(result.boundary.changes_settings, false);
  assert.equal(result.boundary.proves_active_api, false);
  assert.equal(result.boundary.proves_browser_relaunched, false);
});

test("distinguishes disabled, default and unrelated experiment values", () => {
  const result = inspectChromeLocalState(
    {
      browser: {
        enabled_labs_experiments: [
          "enable-webmcp-testing@2",
          "some-unrelated-flag@1",
        ],
      },
    },
    "152.0.7977.64",
  );

  assert.equal(result.planes.nativePageApi.persistedConfigurationObserved, false);
  assert.equal(result.planes.devtoolsPanel.persistedConfigurationObserved, true);
  assert.deepEqual(
    result.flags.map(({ expectedFromPersistedState, persistedValue }) => ({
      expectedFromPersistedState,
      persistedValue,
    })),
    [
      { expectedFromPersistedState: false, persistedValue: "enable-webmcp-testing@2" },
      { expectedFromPersistedState: true, persistedValue: null },
    ],
  );
});

test("detects an explicit DevTools WebMCP disable override", () => {
  const result = inspectChromeLocalState(
    {
      browser: {
        enabled_labs_experiments: [
          "enable-webmcp-testing@1",
          "devtools-webmcp-support@2",
        ],
      },
    },
    "152.0.7977.64",
  );

  assert.equal(result.planes.nativePageApi.persistedConfigurationObserved, true);
  assert.equal(result.planes.devtoolsPanel.persistedConfigurationObserved, false);
  assert.equal(result.flags[1].state, "disabled_override");
});

test("does not claim a validated configuration outside the exact observed major", () => {
  for (const version of ["151.0.0.0", "153.0.0.0"]) {
    const result = inspectChromeLocalState(
      { browser: { enabled_labs_experiments: ["enable-webmcp-testing@1"] } },
      version,
    );

    assert.equal(result.browser.versionValidated, false);
    assert.equal(result.planes.nativePageApi.persistedConfigurationObserved, false);
    assert.equal(result.planes.devtoolsPanel.persistedConfigurationObserved, false);
  }
});

test("fails closed when Chrome's experiment list is malformed", () => {
  assert.throws(
    () => inspectChromeLocalState({ browser: { enabled_labs_experiments: "enabled" } }),
    /no valid enabled_labs_experiments list/,
  );
});

test("resolves the documented macOS Chrome data root", () => {
  assert.equal(
    defaultChromeDataRoot({ platform: "darwin", homeDirectory: "/tmp/example-home" }),
    "/tmp/example-home/Library/Application Support/Google/Chrome",
  );
});

test("rejects incomplete path overrides instead of reading the default profile", () => {
  assert.throws(() => parseArguments(["--local-state"]), /requires a file path/);
  assert.throws(
    () => parseArguments(["--last-version", "--json"]),
    /requires a file path/,
  );
});
