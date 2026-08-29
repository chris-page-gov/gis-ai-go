import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  WEBMCP_GENERATED_MARKER,
  inventoryRegularTree,
  verifyChecksummedCatalogue,
} from "./build-boundary.mjs";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(appRoot, "../..");
const sourceRoot = resolve(repositoryRoot, "artifacts/okf");
const publicRoot = resolve(appRoot, "public");
const destinationRoot = resolve(publicRoot, "catalogue");
const distRoot = resolve(appRoot, "dist");

async function prepareDestination() {
  try {
    const marker = await readFile(resolve(destinationRoot, ".webmcp-explorer-generated"), "utf8");
    if (marker !== WEBMCP_GENERATED_MARKER) {
      throw new Error("Refusing to replace an unmarked WebMCP Explorer catalogue directory");
    }
    await rm(destinationRoot, { recursive: true });
  } catch (error) {
    if (!(error && typeof error === "object" && "code" in error && error.code === "ENOENT")) {
      throw error;
    }
  }
  await mkdir(destinationRoot, { recursive: true });
  await writeFile(
    resolve(destinationRoot, ".webmcp-explorer-generated"),
    WEBMCP_GENERATED_MARKER,
    "utf8",
  );
}

await inventoryRegularTree(publicRoot, "WebMCP Explorer public directory");
await inventoryRegularTree(distRoot, "WebMCP Explorer distribution directory", {
  allowMissing: true,
});
const checksums = await verifyChecksummedCatalogue(sourceRoot);
await prepareDestination();
for (const relative of [...checksums.map(({ path }) => path), "CHECKSUMS.sha256"]) {
  const target = resolve(destinationRoot, relative);
  await mkdir(dirname(target), { recursive: true });
  await cp(resolve(sourceRoot, relative), target, { errorOnExist: true });
}

console.log(`Prepared ${checksums.length + 1} checksum-verified catalogue files.`);
