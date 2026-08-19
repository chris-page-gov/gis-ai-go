#!/usr/bin/env node

import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { assertPreparedPublicInventory } from "./build-boundary.mjs";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const files = await assertPreparedPublicInventory({
  publicRoot: resolve(appRoot, "public"),
  distRoot: resolve(appRoot, "dist"),
});

console.log(`Checked ${files.length} allowlisted regular files before the Vite build.`);
