#!/usr/bin/env node

import { createHash } from "node:crypto";
import { lstat, readFile, readdir } from "node:fs/promises";
import { dirname, extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import {
  inspectHtmlDocument,
  requireExactInventory,
} from "./dist-policy.mjs";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(appRoot, "../..");
const distRoot = resolve(appRoot, "dist");
const catalogueRoot = resolve(distRoot, "catalogue");
const sourceCatalogueRoot = resolve(repositoryRoot, "artifacts/okf");
const CHECKSUM_ROW = /^([0-9a-f]{64})  (.+)$/;

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function safeRelativePath(value) {
  const segments = value.split("/");
  if (
    !value ||
    value.startsWith("/") ||
    value.includes("\\") ||
    value.includes("\0") ||
    segments.includes("") ||
    segments.includes(".") ||
    segments.includes("..")
  ) {
    throw new Error(`Unsafe distribution path: ${value}`);
  }
  return value;
}

function containedPath(root, relative) {
  const target = resolve(root, safeRelativePath(relative));
  if (!target.startsWith(`${root}${sep}`)) {
    throw new Error(`Distribution path escapes its root: ${relative}`);
  }
  return target;
}

async function inventory(root, relative = "") {
  const directory = relative ? containedPath(root, relative) : root;
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries.sort((left, right) => left.name.localeCompare(right.name))) {
    const child = relative ? `${relative}/${entry.name}` : entry.name;
    if (entry.isSymbolicLink()) {
      throw new Error(`Distribution must not contain a symbolic link: ${child}`);
    }
    if (entry.isDirectory()) {
      files.push(...(await inventory(root, child)));
    } else if (entry.isFile()) {
      files.push(child);
    } else {
      throw new Error(`Distribution must contain regular files only: ${child}`);
    }
  }
  return files;
}

function parseChecksums(text) {
  if (!text.endsWith("\n")) {
    throw new Error("Catalogue checksums must end with a newline");
  }
  const rows = text.slice(0, -1).split("\n");
  if (rows.length === 0 || rows.some((row) => row.length === 0)) {
    throw new Error("Catalogue checksums must contain non-empty rows");
  }
  const parsed = rows.map((row) => {
    const match = CHECKSUM_ROW.exec(row);
    if (!match) throw new Error(`Invalid catalogue checksum row: ${row}`);
    return { digest: match[1], path: safeRelativePath(match[2]) };
  });
  const paths = parsed.map((row) => row.path);
  if (
    paths.length !== new Set(paths).size ||
    paths.join("\n") !== [...paths].sort().join("\n")
  ) {
    throw new Error("Catalogue checksum paths must be unique and sorted");
  }
  return parsed;
}

async function requireRegularFile(path, label) {
  const metadata = await lstat(path);
  if (!metadata.isFile() || metadata.isSymbolicLink()) {
    throw new Error(`${label} must be a regular file`);
  }
}

async function verifyHtml(distFiles) {
  const indexPath = resolve(distRoot, "index.html");
  await requireRegularFile(indexPath, "Explorer index");
  const html = await readFile(indexPath, "utf8");
  const referenced = [];
  for (const value of inspectHtmlDocument(html)) {
    const path = decodeURIComponent(value.split(/[?#]/u, 1)[0]).replace(/^\.\//u, "");
    if (path) referenced.push(safeRelativePath(path));
  }
  for (const path of referenced) {
    if (!distFiles.includes(path)) {
      throw new Error(`Built HTML references a missing local file: ${path}`);
    }
  }
  return [...new Set(referenced)].sort();
}

async function verifyCatalogue() {
  const sourceChecksumPath = resolve(sourceCatalogueRoot, "CHECKSUMS.sha256");
  const distChecksumPath = resolve(catalogueRoot, "CHECKSUMS.sha256");
  await requireRegularFile(sourceChecksumPath, "Canonical OKF checksums");
  await requireRegularFile(distChecksumPath, "Distributed OKF checksums");
  const sourceChecksumBytes = await readFile(sourceChecksumPath);
  const distChecksumBytes = await readFile(distChecksumPath);
  if (!sourceChecksumBytes.equals(distChecksumBytes)) {
    throw new Error("Distributed catalogue checksums differ from the canonical OKF build");
  }
  const checksums = parseChecksums(distChecksumBytes.toString("utf8"));
  for (const row of checksums) {
    const sourcePath = containedPath(sourceCatalogueRoot, row.path);
    const distPath = containedPath(catalogueRoot, row.path);
    await requireRegularFile(sourcePath, `Canonical catalogue file ${row.path}`);
    await requireRegularFile(distPath, `Distributed catalogue file ${row.path}`);
    const sourceBytes = await readFile(sourcePath);
    const distBytes = await readFile(distPath);
    if (sha256(sourceBytes) !== row.digest || sha256(distBytes) !== row.digest) {
      throw new Error(`Catalogue checksum mismatch for ${row.path}`);
    }
    if (!sourceBytes.equals(distBytes)) {
      throw new Error(`Distributed catalogue file differs byte-for-byte: ${row.path}`);
    }
  }
  const catalogueFiles = (await inventory(catalogueRoot)).sort();
  const expected = [
    ".explorer-generated",
    "CHECKSUMS.sha256",
    ...checksums.map((row) => row.path),
  ].sort();
  if (catalogueFiles.join("\n") !== expected.join("\n")) {
    throw new Error(
      `Distributed catalogue inventory differs from checksums; ` +
        `expected=${expected.join(",")}; actual=${catalogueFiles.join(",")}`,
    );
  }
  const bundle = JSON.parse(
    await readFile(resolve(catalogueRoot, "okf-bundle.json"), "utf8"),
  );
  const jsonld = JSON.parse(
    await readFile(resolve(catalogueRoot, "okf-bundle.jsonld"), "utf8"),
  );
  if (
    bundle.recordCount !== bundle.records?.length ||
    bundle.recordCount !== jsonld["@graph"]?.length
  ) {
    throw new Error("Distributed JSON and JSON-LD record counts differ");
  }
  const identifiers = new Set(bundle.records.map((record) => record.id));
  const jsonldIdentifiers = new Set(
    jsonld["@graph"].map((record) => record.identifier),
  );
  if (
    identifiers.size !== jsonldIdentifiers.size ||
    [...identifiers].some((identifier) => !jsonldIdentifiers.has(identifier))
  ) {
    throw new Error("Distributed JSON and JSON-LD identifiers differ");
  }
  return expected.map((path) => `catalogue/${path}`);
}

await requireRegularFile(resolve(distRoot, "favicon.svg"), "Explorer favicon");
const distFiles = (await inventory(distRoot)).sort();
for (const path of distFiles) {
  if (extname(path) === ".map") {
    throw new Error(`Production distribution must not contain a source map: ${path}`);
  }
  if (path.includes("docs/research/") || path.includes("research-pack")) {
    throw new Error(`Distribution contains historical research material: ${path}`);
  }
}
const referencedFiles = await verifyHtml(distFiles);
const catalogueFiles = await verifyCatalogue();
requireExactInventory(distFiles, [
  "favicon.svg",
  "index.html",
  ...referencedFiles,
  ...catalogueFiles,
]);
console.log(
  `Checked ${distFiles.length} static Explorer files, relative Vite assets, CSP and ` +
    "byte-exact catalogue checksums.",
);
