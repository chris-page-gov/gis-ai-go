import { createHash } from "node:crypto";
import { cp, mkdir, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import {
  EXPLORER_GENERATED_MARKER,
  assertSafeBuildRoots,
} from "./build-boundary.mjs";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(appRoot, "../..");
const sourceRoot = resolve(repositoryRoot, "artifacts/okf");
const publicRoot = resolve(appRoot, "public");
const destinationRoot = resolve(appRoot, "public/catalogue");
const distRoot = resolve(appRoot, "dist");

function digest(value) {
  return createHash("sha256").update(value).digest("hex");
}

function safeRelativePath(value) {
  if (
    !value ||
    value.startsWith("/") ||
    value.includes("\\") ||
    value.split("/").includes("..")
  ) {
    throw new Error(`Unsafe catalogue path: ${value}`);
  }
  return value;
}

async function inventory(root, relative = "") {
  const directory = resolve(root, relative);
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries.sort((left, right) => left.name.localeCompare(right.name))) {
    const child = relative ? `${relative}/${entry.name}` : entry.name;
    if (entry.isSymbolicLink()) {
      throw new Error(`Catalogue input must not contain a symbolic link: ${child}`);
    }
    if (entry.isDirectory()) {
      files.push(...(await inventory(root, child)));
    } else if (entry.isFile()) {
      files.push(child);
    } else {
      throw new Error(`Catalogue input must contain regular files only: ${child}`);
    }
  }
  return files;
}

async function verifySource() {
  const checksumText = await readFile(resolve(sourceRoot, "CHECKSUMS.sha256"), "utf8");
  const rows = checksumText.trimEnd().split("\n");
  const locked = [];
  for (const row of rows) {
    const match = /^([0-9a-f]{64})  (.+)$/.exec(row);
    if (!match) {
      throw new Error(`Invalid checksum row: ${row}`);
    }
    const [, expected, rawPath] = match;
    const relative = safeRelativePath(rawPath);
    const target = resolve(sourceRoot, relative);
    if (!target.startsWith(`${sourceRoot}${sep}`)) {
      throw new Error(`Catalogue path escapes the generated root: ${relative}`);
    }
    const metadata = await stat(target);
    if (!metadata.isFile()) {
      throw new Error(`Catalogue checksum target is not a file: ${relative}`);
    }
    const actual = digest(await readFile(target));
    if (actual !== expected) {
      throw new Error(
        `Catalogue checksum mismatch for ${relative}: expected ${expected}, found ${actual}`,
      );
    }
    locked.push(relative);
  }

  if (locked.length !== new Set(locked).size || locked.join("\n") !== [...locked].sort().join("\n")) {
    throw new Error("Catalogue checksum paths must be unique and sorted");
  }

  const actual = (await inventory(sourceRoot))
    .filter((path) => path !== ".okf-generated")
    .sort();
  const expected = [...locked, "CHECKSUMS.sha256"].sort();
  if (actual.join("\n") !== expected.join("\n")) {
    throw new Error(
      `Catalogue inventory differs from checksums; expected=${expected.join(",")}; ` +
        `actual=${actual.join(",")}`,
    );
  }
  return locked;
}

async function prepareDestination() {
  try {
    const marker = await readFile(resolve(destinationRoot, ".explorer-generated"), "utf8");
    if (marker !== EXPLORER_GENERATED_MARKER) {
      throw new Error("Refusing to replace an unmarked Explorer catalogue directory");
    }
    await rm(destinationRoot, { recursive: true });
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      // A missing generated destination is the normal first-build state.
    } else if (error instanceof Error) {
      throw error;
    }
  }
  await mkdir(destinationRoot, { recursive: true });
  await writeFile(
    resolve(destinationRoot, ".explorer-generated"),
    EXPLORER_GENERATED_MARKER,
    "utf8",
  );
}

await assertSafeBuildRoots({ publicRoot, distRoot });
const locked = await verifySource();
await prepareDestination();
for (const relative of [...locked, "CHECKSUMS.sha256"]) {
  const target = resolve(destinationRoot, relative);
  await mkdir(dirname(target), { recursive: true });
  await cp(resolve(sourceRoot, relative), target, { errorOnExist: true });
}

console.log(`Prepared ${locked.length + 1} checksum-verified catalogue files.`);
