import { lstat, readFile, readdir } from "node:fs/promises";
import { resolve, sep } from "node:path";

export const EXPLORER_GENERATED_MARKER = "gis-ai-go-public-explorer-data.v1\n";

const CHECKSUM_ROW = /^([0-9a-f]{64})  (.+)$/u;

function isMissing(error) {
  return error && typeof error === "object" && "code" in error && error.code === "ENOENT";
}

async function optionalMetadata(path) {
  try {
    return await lstat(path);
  } catch (error) {
    if (isMissing(error)) {
      return null;
    }
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

/**
 * Inventory a directory without following symbolic links.
 *
 * Only directories and regular files are valid build inputs. This check applies
 * to the root itself as well as every descendant so Vite cannot dereference a
 * link while copying its public directory.
 */
export async function inventoryRegularTree(
  root,
  label,
  { allowMissing = false } = {},
) {
  const rootMetadata = await optionalMetadata(root);
  if (rootMetadata === null) {
    if (allowMissing) {
      return { directories: [], files: [] };
    }
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

export async function assertSafeBuildRoots({ publicRoot, distRoot }) {
  const publicTree = await inventoryRegularTree(publicRoot, "Explorer public directory", {
    allowMissing: true,
  });
  const distTree = await inventoryRegularTree(distRoot, "Explorer distribution directory", {
    allowMissing: true,
  });
  return { publicTree, distTree };
}

export function parseCatalogueChecksumPaths(text) {
  if (!text.endsWith("\n")) {
    throw new Error("Catalogue checksums must end with a newline");
  }
  const rows = text.slice(0, -1).split("\n");
  if (rows.length === 0 || rows.some((row) => row.length === 0)) {
    throw new Error("Catalogue checksums must contain non-empty rows");
  }
  const paths = rows.map((row) => {
    const match = CHECKSUM_ROW.exec(row);
    if (!match) {
      throw new Error(`Invalid catalogue checksum row: ${row}`);
    }
    return safeRelativePath(match[2]);
  });
  if (
    paths.length !== new Set(paths).size ||
    paths.join("\n") !== [...paths].sort().join("\n")
  ) {
    throw new Error("Catalogue checksum paths must be unique and sorted");
  }
  return paths;
}

/** Require the complete, generated public input and nothing else. */
export async function assertPreparedPublicInventory({ publicRoot, distRoot }) {
  const { publicTree } = await assertSafeBuildRoots({ publicRoot, distRoot });
  const publicMetadata = await optionalMetadata(publicRoot);
  if (publicMetadata === null) {
    throw new Error(`Explorer public directory root is missing: ${publicRoot}`);
  }

  const catalogueRoot = resolve(publicRoot, "catalogue");
  const markerPath = resolve(catalogueRoot, ".explorer-generated");
  const checksumPath = resolve(catalogueRoot, "CHECKSUMS.sha256");
  const marker = await readFile(markerPath, "utf8");
  if (marker !== EXPLORER_GENERATED_MARKER) {
    throw new Error("Explorer catalogue marker is invalid");
  }
  const checksumPaths = parseCatalogueChecksumPaths(await readFile(checksumPath, "utf8"));
  const expectedFiles = [
    "favicon.svg",
    "catalogue/.explorer-generated",
    "catalogue/CHECKSUMS.sha256",
    ...checksumPaths.map((path) => {
      const target = resolve(catalogueRoot, path);
      if (!target.startsWith(`${catalogueRoot}${sep}`)) {
        throw new Error(`Catalogue checksum path escapes its root: ${path}`);
      }
      return `catalogue/${path}`;
    }),
  ].sort();
  const expectedDirectories = [...new Set(
    expectedFiles.flatMap((path) => {
      const segments = path.split("/");
      return segments.slice(0, -1).map((_, index) => segments.slice(0, index + 1).join("/"));
    }),
  )].sort();
  const actualFiles = [...publicTree.files].sort();
  const actualDirectories = [...publicTree.directories].sort();
  if (
    actualFiles.join("\n") !== expectedFiles.join("\n") ||
    actualDirectories.join("\n") !== expectedDirectories.join("\n")
  ) {
    throw new Error(
      `Explorer public inventory differs from the generated allowlist; ` +
        `expected files=${expectedFiles.join(",")}; actual files=${actualFiles.join(",")}; ` +
        `expected directories=${expectedDirectories.join(",")}; ` +
        `actual directories=${actualDirectories.join(",")}`,
    );
  }
  return actualFiles;
}
