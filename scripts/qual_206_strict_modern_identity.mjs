#!/usr/bin/env node

import { readFileSync } from "node:fs";

import { contentAddress } from "../packages/evidence/dist/src/index.js";

const PREFIX = "gis-ai-go:qual-206-strict-modern-host-evidence";
const DOMAIN = "gis-ai-go.qual-206-strict-modern-host-evidence.v2";

function fail(message) {
  process.stderr.write(`QUAL-206 identity failed: ${message}\n`);
  process.exitCode = 2;
}

function assertSafeIntegers(value, path = "$") {
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) {
      throw new TypeError(`${path} must be an IEEE 754 safe integer`);
    }
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertSafeIntegers(item, `${path}[${index}]`));
    return;
  }
  if (value !== null && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) {
      assertSafeIntegers(item, `${path}.${key}`);
    }
  }
}

if (process.argv.length !== 2) {
  fail("arguments are not accepted");
} else {
  try {
    const input = readFileSync(0, "utf8");
    const value = JSON.parse(input);
    if (value === null || Array.isArray(value) || typeof value !== "object") {
      throw new TypeError("stdin must contain one JSON object");
    }
    assertSafeIntegers(value);
    process.stdout.write(`${contentAddress(PREFIX, DOMAIN, value)}\n`);
  } catch (error) {
    fail(error instanceof Error ? error.message : "identity input was rejected");
  }
}
