#!/usr/bin/env node

import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  CLAUDE_EXACT_FIVE_CAPABILITY_PROFILE,
  parseClaudeCapabilityArguments,
  runClaudeCapability,
} from "./qual_206_claude_capability_harness.mjs";
import { canonicalJson } from "./qual_206_claude_runtime_closure.mjs";

const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CLAUDE_EXACT_FIVE_CAPABILITY";
const SHARED_ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CLAUDE_CAPABILITY";

export function parseClaudeExactFiveCapabilityArguments(
  argv,
  environment = process.env,
) {
  if (environment[ENABLE_FLAG] !== "1") {
    throw new Error(`refusing exact-five capability execution without ${ENABLE_FLAG}=1`);
  }
  return parseClaudeCapabilityArguments(argv, {
    ...environment,
    [SHARED_ENABLE_FLAG]: "1",
  });
}

export async function runClaudeExactFiveCapability(options, dependencies = {}) {
  if (Object.hasOwn(dependencies, "capabilityProfile")) {
    throw new Error("the exact-five launcher does not accept a caller-supplied profile");
  }
  return await runClaudeCapability(options, {
    ...dependencies,
    capabilityProfile: CLAUDE_EXACT_FIVE_CAPABILITY_PROFILE,
  });
}

async function main() {
  const options = parseClaudeExactFiveCapabilityArguments(process.argv.slice(2));
  const { manifest } = await runClaudeExactFiveCapability(options);
  process.stdout.write(`${canonicalJson({
    schema: manifest.schema,
    profile: manifest.profile,
    run_id: manifest.run_id,
    exit_code: manifest.execution.exit_code,
    harness_classification: manifest.execution.harness_classification,
    private_manifest_written: true,
  })}\n`);
  process.exitCode = manifest.execution.exit_code === 0 &&
    manifest.execution.harness_classification === null ? 0 : 2;
}

const entry = process.argv[1];
if (entry !== undefined && import.meta.url === pathToFileURL(resolve(entry)).href) {
  try {
    await main();
  } catch {
    process.stderr.write("QUAL-206 Claude exact-five capability harness failed closed\n");
    process.exitCode = 2;
  }
}
