#!/usr/bin/env node

import {
  advertisedToolSchemasExact,
} from "./qual_206_exact_five_event_collector.mjs";

const MAX_INPUT_BYTES = 1_048_576;
const AUTHORITY_ARGUMENT = "--stdin-tools-list-only";

async function main() {
  if (process.argv.length !== 3 || process.argv[2] !== AUTHORITY_ARGUMENT) {
    throw new Error(`Usage: ${AUTHORITY_ARGUMENT}`);
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
