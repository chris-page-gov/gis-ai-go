import { createHash } from "node:crypto";
import { lstat, readFile, readdir } from "node:fs/promises";
import { resolve, sep } from "node:path";

export const WEBMCP_GENERATED_MARKER = "gis-ai-go-webmcp-explorer-data.v1\n";
const CHECKSUM_ROW = /^([0-9a-f]{64})  (.+)$/u;

function isMissing(error) {
  return error && typeof error === "object" && "code" in error && error.code === "ENOENT";
}

async function optionalMetadata(path) {
  try {
    return await lstat(path);
  } catch (error) {
    if (isMissing(error)) return null;
    throw error;
  }
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
    throw new Error(`Unsafe catalogue checksum path: ${value}`);
  }
  return value;
}

export async function inventoryRegularTree(root, label, { allowMissing = false } = {}) {
  const rootMetadata = await optionalMetadata(root);
  if (rootMetadata === null) {
    if (allowMissing) return { directories: [], files: [] };
    throw new Error(`${label} root is missing: ${root}`);
  }
  if (rootMetadata.isSymbolicLink()) {
    throw new Error(`${label} root must not be a symbolic link: ${root}`);
  }
  if (!rootMetadata.isDirectory()) {
    throw new Error(`${label} root must be a directory: ${root}`);
  }

  const directories = [];
  const files = [];
  async function visit(directory, relative = "") {
    const names = (await readdir(directory)).sort((left, right) => left.localeCompare(right));
    for (const name of names) {
      const child = relative ? `${relative}/${name}` : name;
      const target = resolve(directory, name);
      const metadata = await lstat(target);
      if (metadata.isSymbolicLink()) {
        throw new Error(`${label} must not contain a symbolic link: ${child}`);
      }
      if (metadata.isDirectory()) {
        directories.push(child);
        await visit(target, child);
      } else if (metadata.isFile()) {
        files.push(child);
      } else {
        throw new Error(`${label} must contain regular files and directories only: ${child}`);
      }
    }
  }
  await visit(root);
  return { directories, files };
}

export function parseCatalogueChecksums(text) {
  if (!text.endsWith("\n")) throw new Error("Catalogue checksums must end with a newline");
  const rows = text.slice(0, -1).split("\n");
  if (rows.length === 0 || rows.some((row) => row.length === 0)) {
    throw new Error("Catalogue checksums must contain non-empty rows");
  }
  const parsed = rows.map((row) => {
    const match = CHECKSUM_ROW.exec(row);
    if (!match) throw new Error(`Invalid catalogue checksum row: ${row}`);
    return { digest: match[1], path: safeRelativePath(match[2]) };
  });
  const paths = parsed.map(({ path }) => path);
  if (
    paths.length !== new Set(paths).size ||
    paths.join("\n") !== [...paths].sort().join("\n")
  ) {
    throw new Error("Catalogue checksum paths must be unique and sorted");
  }
  return parsed;
}

function digest(value) {
  return createHash("sha256").update(value).digest("hex");
}

export async function verifyChecksummedCatalogue(
  root,
  { ignoredFiles = [".okf-generated"] } = {},
) {
  const checksumPath = resolve(root, "CHECKSUMS.sha256");
  const parsed = parseCatalogueChecksums(await readFile(checksumPath, "utf8"));
  for (const row of parsed) {
    const target = resolve(root, row.path);
    if (!target.startsWith(`${root}${sep}`)) {
      throw new Error(`Catalogue checksum path escapes its root: ${row.path}`);
    }
    const metadata = await lstat(target);
    if (!metadata.isFile() || metadata.isSymbolicLink()) {
      throw new Error(`Catalogue checksum target must be a regular file: ${row.path}`);
    }
    const actual = digest(await readFile(target));
    if (actual !== row.digest) {
      throw new Error(
        `Catalogue checksum mismatch for ${row.path}: expected ${row.digest}, found ${actual}`,
      );
    }
  }
  const inventory = await inventoryRegularTree(root, "Generated OKF catalogue");
  const ignored = new Set(ignoredFiles);
  const actual = inventory.files.filter((path) => !ignored.has(path)).sort();
  const expected = [...parsed.map(({ path }) => path), "CHECKSUMS.sha256"].sort();
  if (actual.join("\n") !== expected.join("\n")) {
    throw new Error(
      `Catalogue inventory differs from checksums; expected=${expected.join(",")}; ` +
        `actual=${actual.join(",")}`,
    );
  }
  return parsed;
}
