#!/usr/bin/env node

import {
  advertisedToolSchemasExact,
  expectedToolSchemaDigests,
} from "./qual_206_exact_five_event_collector.mjs";

const MAX_INPUT_BYTES = 1_048_576;
const TOOLS_AUTHORITY_ARGUMENT = "--stdin-tools-list-only";
const DIGESTS_AUTHORITY_ARGUMENT = "--print-schema-digests";

async function main() {
  if (
    process.argv.length !== 3 ||
    ![TOOLS_AUTHORITY_ARGUMENT, DIGESTS_AUTHORITY_ARGUMENT].includes(process.argv[2])
  ) {
    throw new Error(
      `Usage: ${TOOLS_AUTHORITY_ARGUMENT} | ${DIGESTS_AUTHORITY_ARGUMENT}`,
    );
  }
  if (process.argv[2] === DIGESTS_AUTHORITY_ARGUMENT) {
    process.stdout.write(`${JSON.stringify(expectedToolSchemaDigests())}\n`);
    return 0;
  }
  const chunks = [];
  let bytes = 0;
  for await (const chunk of process.stdin) {
    bytes += chunk.length;
    if (bytes > MAX_INPUT_BYTES) throw new Error("Tool schema input exceeded its byte bound");
    chunks.push(chunk);
  }
  if (bytes < 1) throw new Error("Tool schema input is empty");
  const tools = JSON.parse(Buffer.concat(chunks, bytes).toString("utf8"));
  const valid = advertisedToolSchemasExact(tools);
  process.stdout.write(`${JSON.stringify({
    schema: "gis-ai-go.qual-206-local-http-schema-validation.v1",
    valid,
  })}\n`);
  return valid ? 0 : 1;
}

try {
  process.exitCode = await main();
} catch {
  process.stderr.write("QUAL-206 local HTTP schema validation failed closed.\n");
  process.exitCode = 2;
}
