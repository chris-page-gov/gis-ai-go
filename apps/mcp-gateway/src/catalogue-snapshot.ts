import { createHash } from "node:crypto";
import { constants, type Stats } from "node:fs";
import { lstat, open, opendir, realpath } from "node:fs/promises";
import { dirname, isAbsolute, join, posix, relative, resolve, sep } from "node:path";
import { types as utilTypes } from "node:util";

import {
  parseCatalogueJson,
  type CatalogueBundle,
  type CatalogueRecord,
} from "@gis-ai-go/contracts";

const GENERATED_MARKER = "gis-ai-go-okf-builder.v1\n";
const MARKER_PATH = ".okf-generated";
const CHECKSUM_PATH = "CHECKSUMS.sha256";
const BUNDLE_PATH = "okf-bundle.json";
const MANIFEST_PATH = "manifest.json";
const RECEIPT_PATH = "build-receipt.json";
const EXPECTED_BUNDLE_ID =
  "https://chris-page-gov.github.io/gis-ai-go/id/bundle/public-discovery";

const MAX_FILES = 1_000;
const MAX_DIRECTORIES = 1_000;
const MAX_TOTAL_BYTES = 64 * 1024 * 1024;
const MAX_BUNDLE_BYTES = 8 * 1024 * 1024;
const MAX_CONTROL_FILE_BYTES = 8 * 1024 * 1024;
const MAX_CHECKSUM_BYTES = 2 * 1024 * 1024;
const MAX_RELATIVE_PATH_LENGTH = 1_024;

const SHA256 = /^[0-9a-f]{64}$/u;
const SHA40 = /^[0-9a-f]{40}$/u;
const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/u;
const SAFE_PATH_SEGMENT = /^[A-Za-z0-9][A-Za-z0-9._-]*$/u;
const VERIFIED_CATALOGUE_SNAPSHOTS = new WeakSet<object>();

interface ScannedFile {
  readonly absolutePath: string;
  readonly size: number;
  readonly device: number;
  readonly inode: number;
  readonly mode: number;
  readonly modifiedAtMilliseconds: number;
  readonly changedAtMilliseconds: number;
}

interface Inventory {
  readonly files: ReadonlyMap<string, ScannedFile>;
  readonly directories: ReadonlySet<string>;
  readonly totalBytes: number;
}

interface ChecksumEntry {
  readonly path: string;
  readonly sha256: string;
}

interface ManifestFile {
  readonly path: string;
  readonly bytes: number;
  readonly sha256: string;
}

interface ParsedManifest {
  readonly version: string;
  readonly revision: string;
  readonly recordCount: number;
  readonly recordIds: readonly string[];
  readonly files: readonly ManifestFile[];
}

interface ParsedReceipt {
  readonly version: string;
  readonly revision: string;
  readonly profile: string;
  readonly profileStatus: string;
  readonly recordCount: number;
  readonly outputCount: number;
  readonly contentRootSha256: string;
  readonly manifestSha256: string;
}

export interface CatalogueSnapshot {
  readonly root: string;
  readonly bundle: CatalogueBundle;
  readonly recordsById: ReadonlyMap<string, CatalogueRecord>;
  readonly version: string;
  readonly revision: string;
  readonly contentRootSha256: string;
  readonly manifestSha256: string;
  readonly recordCount: number;
  readonly stale: boolean;
  readonly stalenessWarning: string | null;
  readonly warnings: readonly string[];
}

export interface LoadCatalogueSnapshotOptions {
  readonly now?: Date;
}

class FrozenRecordMap implements ReadonlyMap<string, CatalogueRecord> {
  readonly #records: Map<string, CatalogueRecord>;

  constructor(records: readonly CatalogueRecord[]) {
    this.#records = new Map(records.map((record) => [record.id, record]));
    Object.freeze(this);
  }

  get size(): number {
    return this.#records.size;
  }

  get(key: string): CatalogueRecord | undefined {
    return this.#records.get(key);
  }

  has(key: string): boolean {
    return this.#records.has(key);
  }

  entries(): MapIterator<[string, CatalogueRecord]> {
    return this.#records.entries();
  }

  keys(): MapIterator<string> {
    return this.#records.keys();
  }

  values(): MapIterator<CatalogueRecord> {
    return this.#records.values();
  }

  forEach(
    callbackfn: (
      value: CatalogueRecord,
      key: string,
      map: ReadonlyMap<string, CatalogueRecord>,
    ) => void,
    thisArg?: unknown,
  ): void {
    for (const [key, value] of this.#records) {
      callbackfn.call(thisArg, value, key, this);
    }
  }

  [Symbol.iterator](): MapIterator<[string, CatalogueRecord]> {
    return this.entries();
  }
}

// Calls read through this map after asynchronous transport boundaries. Keep its
// private dispatch surface immutable before any verified instance is exposed.
Object.freeze(FrozenRecordMap.prototype);

function sha256(bytes: Uint8Array): string {
  return createHash("sha256").update(bytes).digest("hex");
}

function fail(message: string): never {
  throw new Error(`Catalogue snapshot rejected: ${message}`);
}

function safeRelativePath(value: string, label: string): string {
  if (
    value.length === 0 ||
    value.length > MAX_RELATIVE_PATH_LENGTH ||
    value.includes("\\") ||
    value.startsWith("/") ||
    posix.normalize(value) !== value
  ) {
    fail(`${label} is not a canonical safe relative path`);
  }
  const segments = value.split("/");
  if (segments.some((segment) => !SAFE_PATH_SEGMENT.test(segment))) {
    fail(`${label} contains an unsafe path segment`);
  }
  return value;
}

function decodeUtf8(bytes: Uint8Array, label: string): string {
  let value: string;
  try {
    value = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch (error) {
    throw new Error(`Catalogue snapshot rejected: ${label} is not valid UTF-8`, {
      cause: error,
    });
  }
  if (!Buffer.from(value, "utf8").equals(Buffer.from(bytes))) {
    fail(`${label} is not canonical UTF-8`);
  }
  return value;
}

function expectObject(value: unknown, label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    fail(`${label} must be an object`);
  }
  return value as Record<string, unknown>;
}

function expectExactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
  label: string,
): void {
  const actual = Object.keys(value).sort();
  const canonical = [...expected].sort();
  if (actual.length !== canonical.length || actual.some((key, index) => key !== canonical[index])) {
    fail(`${label} has missing or unexpected fields`);
  }
}

function expectString(value: unknown, label: string): string {
  if (typeof value !== "string" || value.length === 0) {
    fail(`${label} must be a non-empty string`);
  }
  return value;
}

function expectDigest(value: unknown, label: string): string {
  const digest = expectString(value, label);
  if (!SHA256.test(digest)) {
    fail(`${label} must be a lowercase SHA-256 digest`);
  }
  return digest;
}

function expectInteger(value: unknown, label: string, minimum = 0): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < minimum) {
    fail(`${label} must be an integer of at least ${minimum}`);
  }
  return value;
}

function parseJsonObject(bytes: Uint8Array, label: string): Record<string, unknown> {
  let value: unknown;
  try {
    value = JSON.parse(decodeUtf8(bytes, label)) as unknown;
  } catch (error) {
    if (error instanceof Error && error.message.startsWith("Catalogue snapshot rejected:")) {
      throw error;
    }
    throw new Error(`Catalogue snapshot rejected: ${label} is not valid JSON`, { cause: error });
  }
  return expectObject(value, label);
}

async function assertCanonicalRoot(inputRoot: string): Promise<string> {
  if (!isAbsolute(inputRoot)) {
    fail("catalogue root must be an absolute path");
  }
  const root = resolve(inputRoot);
  let cursor = root;
  while (true) {
    let stats;
    try {
      stats = await lstat(cursor);
    } catch (error) {
      throw new Error("Catalogue snapshot rejected: catalogue root or ancestor is inaccessible", {
        cause: error,
      });
    }
    if (stats.isSymbolicLink()) {
      fail("catalogue root and its ancestors must not be symbolic links");
    }
    if (!stats.isDirectory()) {
      fail("catalogue root and its ancestors must be directories");
    }
    const parent = dirname(cursor);
    if (parent === cursor) {
      break;
    }
    cursor = parent;
  }
  if ((await realpath(root)) !== root) {
    fail("catalogue root must resolve without aliases or symbolic links");
  }
  return root;
}

function relativeFromRoot(root: string, absolutePath: string): string {
  return relative(root, absolutePath).split(sep).join("/");
}

async function scanInventory(root: string): Promise<Inventory> {
  const files = new Map<string, ScannedFile>();
  const directories = new Set<string>();
  const pendingDirectories = [root];
  let totalBytes = 0;

  while (pendingDirectories.length > 0) {
    const directory = pendingDirectories.pop()!;
    const directoryHandle = await opendir(directory);
    try {
      while (true) {
        const entry = await directoryHandle.read();
        if (entry === null) {
          break;
        }
        if (entry.name !== MARKER_PATH && !SAFE_PATH_SEGMENT.test(entry.name)) {
          fail("catalogue inventory contains an unsafe entry name");
        }
        const absolutePath = join(directory, entry.name);
        const entryPath = relativeFromRoot(root, absolutePath);
        const stats = await lstat(absolutePath);
        if (stats.isSymbolicLink()) {
          fail("catalogue inventory contains a symbolic link");
        }
        if (stats.isDirectory()) {
          directories.add(entryPath);
          if (directories.size > MAX_DIRECTORIES) {
            fail(`catalogue inventory exceeds ${MAX_DIRECTORIES} directories`);
          }
          pendingDirectories.push(absolutePath);
          continue;
        }
        if (!stats.isFile()) {
          fail("catalogue inventory contains a non-regular entry");
        }
        files.set(entryPath, {
          absolutePath,
          size: stats.size,
          device: stats.dev,
          inode: stats.ino,
          mode: stats.mode,
          modifiedAtMilliseconds: stats.mtimeMs,
          changedAtMilliseconds: stats.ctimeMs,
        });
        if (files.size > MAX_FILES) {
          fail(`catalogue inventory exceeds ${MAX_FILES} files`);
        }
        totalBytes += stats.size;
        if (!Number.isSafeInteger(totalBytes) || totalBytes > MAX_TOTAL_BYTES) {
          fail(`catalogue inventory exceeds ${MAX_TOTAL_BYTES} bytes`);
        }
      }
    } finally {
      await directoryHandle.close();
    }
  }
  return { files, directories, totalBytes };
}

function hasStableScannedMetadata(
  stats: Stats,
  file: ScannedFile,
): boolean {
  return (
    stats.isFile() &&
    stats.size === file.size &&
    stats.dev === file.device &&
    stats.ino === file.inode &&
    stats.mode === file.mode &&
    stats.mtimeMs === file.modifiedAtMilliseconds &&
    stats.ctimeMs === file.changedAtMilliseconds
  );
}

async function readScannedFile(file: ScannedFile, maximumBytes: number): Promise<Buffer> {
  if (file.size > maximumBytes) {
    fail(`catalogue control file exceeds ${maximumBytes} bytes`);
  }
  let handle;
  try {
    handle = await open(file.absolutePath, constants.O_RDONLY | constants.O_NOFOLLOW);
    const beforeRead = await handle.stat();
    if (!hasStableScannedMetadata(beforeRead, file)) {
      fail("catalogue inventory changed while it was being verified");
    }
    const readCapacity = file.size + 1;
    if (!Number.isSafeInteger(readCapacity) || readCapacity > maximumBytes + 1) {
      fail(`catalogue control file exceeds ${maximumBytes} bytes`);
    }
    const bytes = Buffer.allocUnsafe(readCapacity);
    let bytesRead = 0;
    while (bytesRead < bytes.byteLength) {
      const result = await handle.read(
        bytes,
        bytesRead,
        bytes.byteLength - bytesRead,
        bytesRead,
      );
      if (result.bytesRead === 0) {
        break;
      }
      bytesRead += result.bytesRead;
    }
    const afterRead = await handle.stat();
    if (!hasStableScannedMetadata(afterRead, file)) {
      fail("catalogue inventory changed while it was being verified");
    }
    if (bytesRead !== file.size) {
      fail("catalogue file size changed while it was being verified");
    }
    return bytes.subarray(0, bytesRead);
  } catch (error) {
    if (error instanceof Error && error.message.startsWith("Catalogue snapshot rejected:")) {
      throw error;
    }
    throw new Error("Catalogue snapshot rejected: catalogue file could not be read safely", {
      cause: error,
    });
  } finally {
    await handle?.close();
  }
}

function requireInventoryFile(inventory: Inventory, path: string): ScannedFile {
  const file = inventory.files.get(path);
  if (!file) {
    fail(`catalogue inventory is missing ${path}`);
  }
  return file;
}

function parseChecksums(text: string): readonly ChecksumEntry[] {
  if (!text.endsWith("\n") || text.length === 0) {
    fail(`${CHECKSUM_PATH} must end with one canonical newline`);
  }
  const lines = text.slice(0, -1).split("\n");
  if (lines.length > MAX_FILES - 2) {
    fail(`${CHECKSUM_PATH} contains too many entries`);
  }
  const entries = lines.map((line, index): ChecksumEntry => {
    const match = /^([0-9a-f]{64})  (.+)$/u.exec(line);
    if (!match?.[1] || !match[2]) {
      fail(`${CHECKSUM_PATH} row ${index + 1} is malformed`);
    }
    const path = safeRelativePath(match[2], `${CHECKSUM_PATH} row ${index + 1}`);
    if (path === MARKER_PATH || path === CHECKSUM_PATH) {
      fail(`${CHECKSUM_PATH} must not checksum itself or the generated marker`);
    }
    return { sha256: match[1], path };
  });
  const sortedPaths = entries.map((entry) => entry.path).toSorted();
  if (
    entries.some((entry, index) => entry.path !== sortedPaths[index]) ||
    new Set(sortedPaths).size !== sortedPaths.length
  ) {
    fail(`${CHECKSUM_PATH} paths must be sorted and unique`);
  }
  const canonical = entries.map((entry) => `${entry.sha256}  ${entry.path}\n`).join("");
  if (canonical !== text) {
    fail(`${CHECKSUM_PATH} is not in canonical form`);
  }
  return entries;
}

function expectedDirectories(paths: readonly string[]): ReadonlySet<string> {
  const expected = new Set<string>();
  for (const path of paths) {
    let parent = posix.dirname(path);
    while (parent !== ".") {
      expected.add(parent);
      parent = posix.dirname(parent);
    }
  }
  return expected;
}

function assertExactInventory(inventory: Inventory, entries: readonly ChecksumEntry[]): void {
  const expectedFiles = new Set([
    MARKER_PATH,
    CHECKSUM_PATH,
    ...entries.map((entry) => entry.path),
  ]);
  if (
    expectedFiles.size !== inventory.files.size ||
    [...inventory.files.keys()].some((path) => !expectedFiles.has(path))
  ) {
    fail("catalogue inventory has missing or unexpected files");
  }
  const expectedDirs = expectedDirectories([...expectedFiles]);
  if (
    expectedDirs.size !== inventory.directories.size ||
    [...inventory.directories].some((path) => !expectedDirs.has(path))
  ) {
    fail("catalogue inventory has missing or unexpected directories");
  }
}

function parseManifest(bytes: Uint8Array): ParsedManifest {
  const value = parseJsonObject(bytes, MANIFEST_PATH);
  expectExactKeys(
    value,
    ["schema", "version", "revision", "recordCount", "recordIds", "files"],
    MANIFEST_PATH,
  );
  if (value.schema !== "gis-ai-go-okf-manifest.v1") {
    fail(`${MANIFEST_PATH}.schema is not supported`);
  }
  const version = expectString(value.version, `${MANIFEST_PATH}.version`);
  if (!SEMVER.test(version)) {
    fail(`${MANIFEST_PATH}.version must be semantic`);
  }
  const revision = expectString(value.revision, `${MANIFEST_PATH}.revision`);
  if (!SHA40.test(revision)) {
    fail(`${MANIFEST_PATH}.revision must be a lowercase Git SHA`);
  }
  const recordCount = expectInteger(value.recordCount, `${MANIFEST_PATH}.recordCount`, 1);
  if (!Array.isArray(value.recordIds) || value.recordIds.length !== recordCount) {
    fail(`${MANIFEST_PATH}.recordIds must match recordCount`);
  }
  const recordIds = value.recordIds.map((item, index) =>
    expectString(item, `${MANIFEST_PATH}.recordIds[${index}]`),
  );
  if (new Set(recordIds).size !== recordIds.length) {
    fail(`${MANIFEST_PATH}.recordIds must be unique`);
  }
  if (!Array.isArray(value.files) || value.files.length > MAX_FILES) {
    fail(`${MANIFEST_PATH}.files must be a bounded array`);
  }
  const files = value.files.map((item, index): ManifestFile => {
    const file = expectObject(item, `${MANIFEST_PATH}.files[${index}]`);
    expectExactKeys(file, ["path", "bytes", "sha256"], `${MANIFEST_PATH}.files[${index}]`);
    return {
      path: safeRelativePath(
        expectString(file.path, `${MANIFEST_PATH}.files[${index}].path`),
        `${MANIFEST_PATH}.files[${index}].path`,
      ),
      bytes: expectInteger(file.bytes, `${MANIFEST_PATH}.files[${index}].bytes`),
      sha256: expectDigest(file.sha256, `${MANIFEST_PATH}.files[${index}].sha256`),
    };
  });
  const paths = files.map((file) => file.path);
  if (
    paths.some((path, index) => path !== paths.toSorted()[index]) ||
    new Set(paths).size !== paths.length
  ) {
    fail(`${MANIFEST_PATH}.files must be sorted and unique`);
  }
  return { version, revision, recordCount, recordIds, files };
}

function parseReceipt(bytes: Uint8Array): ParsedReceipt {
  const value = parseJsonObject(bytes, RECEIPT_PATH);
  expectExactKeys(
    value,
    [
      "schema",
      "builder",
      "builderVersion",
      "version",
      "revision",
      "profile",
      "profileStatus",
      "sourceLockSha256",
      "inputRootSha256",
      "inputs",
      "recordCount",
      "outputCount",
      "checksumScope",
      "contentRootScope",
      "contentRootSha256",
      "manifestSha256",
      "determinism",
    ],
    RECEIPT_PATH,
  );
  if (value.schema !== "gis-ai-go-okf-build-receipt.v1") {
    fail(`${RECEIPT_PATH}.schema is not supported`);
  }
  if (value.builder !== "scripts/build_okf.py") {
    fail(`${RECEIPT_PATH}.builder is not supported`);
  }
  const builderVersion = expectString(value.builderVersion, `${RECEIPT_PATH}.builderVersion`);
  if (!SEMVER.test(builderVersion)) {
    fail(`${RECEIPT_PATH}.builderVersion must be semantic`);
  }
  const version = expectString(value.version, `${RECEIPT_PATH}.version`);
  if (!SEMVER.test(version)) {
    fail(`${RECEIPT_PATH}.version must be semantic`);
  }
  const revision = expectString(value.revision, `${RECEIPT_PATH}.revision`);
  if (!SHA40.test(revision)) {
    fail(`${RECEIPT_PATH}.revision must be a lowercase Git SHA`);
  }
  const profile = expectString(value.profile, `${RECEIPT_PATH}.profile`);
  const profileStatus = expectString(value.profileStatus, `${RECEIPT_PATH}.profileStatus`);
  expectDigest(value.sourceLockSha256, `${RECEIPT_PATH}.sourceLockSha256`);
  const inputRootSha256 = expectDigest(value.inputRootSha256, `${RECEIPT_PATH}.inputRootSha256`);
  if (!Array.isArray(value.inputs) || value.inputs.length > MAX_FILES) {
    fail(`${RECEIPT_PATH}.inputs must be a bounded array`);
  }
  const inputRows = value.inputs.map((item, index) => {
    const input = expectObject(item, `${RECEIPT_PATH}.inputs[${index}]`);
    expectExactKeys(
      input,
      ["bytes", "path", "role", "sha256"],
      `${RECEIPT_PATH}.inputs[${index}]`,
    );
    return {
      bytes: expectInteger(input.bytes, `${RECEIPT_PATH}.inputs[${index}].bytes`),
      path: safeRelativePath(
        expectString(input.path, `${RECEIPT_PATH}.inputs[${index}].path`),
        `${RECEIPT_PATH}.inputs[${index}].path`,
      ),
      role: expectString(input.role, `${RECEIPT_PATH}.inputs[${index}].role`),
      sha256: expectDigest(input.sha256, `${RECEIPT_PATH}.inputs[${index}].sha256`),
    };
  });
  const inputPaths = inputRows.map((input) => input.path);
  if (
    inputPaths.some((path, index) => path !== inputPaths.toSorted()[index]) ||
    new Set(inputPaths).size !== inputPaths.length
  ) {
    fail(`${RECEIPT_PATH}.inputs must be sorted and unique`);
  }
  const computedInputRoot = sha256(
    Buffer.from(inputRows.map((input) => `${input.sha256}  ${input.path}\n`).join(""), "utf8"),
  );
  if (computedInputRoot !== inputRootSha256) {
    fail(`${RECEIPT_PATH}.inputRootSha256 does not match its input inventory`);
  }
  if (
    value.checksumScope !==
    "All generated files except .okf-generated and CHECKSUMS.sha256, including build-receipt.json."
  ) {
    fail(`${RECEIPT_PATH}.checksumScope is not supported`);
  }
  if (
    value.contentRootScope !==
    "All generated payload files except .okf-generated, CHECKSUMS.sha256 and build-receipt.json."
  ) {
    fail(`${RECEIPT_PATH}.contentRootScope is not supported`);
  }
  const determinism = expectObject(value.determinism, `${RECEIPT_PATH}.determinism`);
  expectExactKeys(
    determinism,
    ["canonicalJson", "pathOrder", "wallClockIncluded", "checkoutPathIncluded"],
    `${RECEIPT_PATH}.determinism`,
  );
  if (
    determinism.canonicalJson !== "sorted-key UTF-8 JSON with two-space indent and final newline" ||
    determinism.pathOrder !== "lexicographic" ||
    determinism.wallClockIncluded !== false ||
    determinism.checkoutPathIncluded !== false
  ) {
    fail(`${RECEIPT_PATH}.determinism does not describe the supported builder`);
  }
  return {
    version,
    revision,
    profile,
    profileStatus,
    recordCount: expectInteger(value.recordCount, `${RECEIPT_PATH}.recordCount`, 1),
    outputCount: expectInteger(value.outputCount, `${RECEIPT_PATH}.outputCount`, 1),
    contentRootSha256: expectDigest(
      value.contentRootSha256,
      `${RECEIPT_PATH}.contentRootSha256`,
    ),
    manifestSha256: expectDigest(value.manifestSha256, `${RECEIPT_PATH}.manifestSha256`),
  };
}

function assertManifestInventory(
  manifest: ParsedManifest,
  entries: readonly ChecksumEntry[],
  inventory: Inventory,
  verifiedDigests: ReadonlyMap<string, string>,
): void {
  const ledgerPaths = new Set(entries.map((entry) => entry.path));
  const expectedManifestPaths = new Set(
    entries
      .map((entry) => entry.path)
      .filter((path) => path !== MANIFEST_PATH && path !== RECEIPT_PATH),
  );
  if (
    manifest.files.length !== expectedManifestPaths.size ||
    manifest.files.some((file) => !expectedManifestPaths.has(file.path)) ||
    !ledgerPaths.has(MANIFEST_PATH) ||
    !ledgerPaths.has(RECEIPT_PATH)
  ) {
    fail(`${MANIFEST_PATH}.files does not match the checksum-locked payload inventory`);
  }
  for (const file of manifest.files) {
    const scanned = requireInventoryFile(inventory, file.path);
    if (scanned.size !== file.bytes || verifiedDigests.get(file.path) !== file.sha256) {
      fail(`${MANIFEST_PATH}.files metadata does not match the verified payload`);
    }
  }
}

function deepFreeze<T>(value: T, seen = new WeakSet<object>()): T {
  if (value === null || typeof value !== "object" || seen.has(value)) {
    return value;
  }
  seen.add(value);
  for (const child of Object.values(value as Record<string, unknown>)) {
    deepFreeze(child, seen);
  }
  return Object.freeze(value);
}

/**
 * Load one checksum-locked public catalogue without following filesystem links.
 *
 * Any ambiguity in the root, inventory, integrity ledgers or publication
 * contract rejects the complete snapshot. No partial catalogue is returned.
 */
export async function loadCatalogueSnapshot(
  inputRoot: string,
  options: LoadCatalogueSnapshotOptions = {},
): Promise<CatalogueSnapshot> {
  const now = options.now ?? new Date();
  if (!Number.isFinite(now.getTime())) {
    fail("load time must be a valid Date");
  }
  const root = await assertCanonicalRoot(inputRoot);
  const inventory = await scanInventory(root);

  const markerBytes = await readScannedFile(
    requireInventoryFile(inventory, MARKER_PATH),
    Buffer.byteLength(GENERATED_MARKER),
  );
  if (!markerBytes.equals(Buffer.from(GENERATED_MARKER, "utf8"))) {
    fail("generated marker is missing or invalid");
  }
  const checksumBytes = await readScannedFile(
    requireInventoryFile(inventory, CHECKSUM_PATH),
    MAX_CHECKSUM_BYTES,
  );
  const entries = parseChecksums(decodeUtf8(checksumBytes, CHECKSUM_PATH));
  assertExactInventory(inventory, entries);

  const required = new Set([BUNDLE_PATH, MANIFEST_PATH, RECEIPT_PATH]);
  const controlBytes = new Map<string, Buffer>();
  const verifiedDigests = new Map<string, string>();
  for (const entry of entries) {
    const scanned = requireInventoryFile(inventory, entry.path);
    const maximum =
      entry.path === BUNDLE_PATH
        ? MAX_BUNDLE_BYTES
        : required.has(entry.path)
          ? MAX_CONTROL_FILE_BYTES
          : MAX_TOTAL_BYTES;
    const bytes = await readScannedFile(scanned, maximum);
    const actualDigest = sha256(bytes);
    if (actualDigest !== entry.sha256) {
      fail(`checksum mismatch for ${entry.path}`);
    }
    verifiedDigests.set(entry.path, actualDigest);
    if (required.has(entry.path)) {
      controlBytes.set(entry.path, bytes);
    }
  }
  for (const path of required) {
    if (!controlBytes.has(path)) {
      fail(`${CHECKSUM_PATH} is missing required control file ${path}`);
    }
  }

  const manifest = parseManifest(controlBytes.get(MANIFEST_PATH)!);
  const receipt = parseReceipt(controlBytes.get(RECEIPT_PATH)!);
  assertManifestInventory(manifest, entries, inventory, verifiedDigests);

  const manifestSha256 = verifiedDigests.get(MANIFEST_PATH)!;
  if (receipt.manifestSha256 !== manifestSha256) {
    fail(`${RECEIPT_PATH}.manifestSha256 does not match ${MANIFEST_PATH}`);
  }
  const computedContentRoot = sha256(
    Buffer.from(
      entries
        .filter((entry) => entry.path !== RECEIPT_PATH)
        .map((entry) => `${entry.sha256}  ${entry.path}\n`)
        .join(""),
      "utf8",
    ),
  );
  if (receipt.contentRootSha256 !== computedContentRoot) {
    fail(`${RECEIPT_PATH}.contentRootSha256 does not match the canonical payload inventory`);
  }
  if (receipt.outputCount !== entries.length) {
    fail(`${RECEIPT_PATH}.outputCount does not match the checksum inventory`);
  }

  const bundle = parseCatalogueJson(decodeUtf8(controlBytes.get(BUNDLE_PATH)!, BUNDLE_PATH));
  if (bundle.id !== EXPECTED_BUNDLE_ID) {
    fail(`${BUNDLE_PATH}.id is not the GIS AI GO public discovery bundle`);
  }
  if (
    bundle.version !== manifest.version ||
    bundle.version !== receipt.version ||
    bundle.revision !== manifest.revision ||
    bundle.revision !== receipt.revision ||
    bundle.recordCount !== manifest.recordCount ||
    bundle.recordCount !== receipt.recordCount ||
    bundle.profile !== receipt.profile ||
    bundle.profileStatus !== receipt.profileStatus
  ) {
    fail("bundle, manifest and receipt identity fields do not agree");
  }
  const recordIds = bundle.records.map((record) => record.id);
  if (
    recordIds.length !== manifest.recordIds.length ||
    recordIds.some((recordId, index) => recordId !== manifest.recordIds[index])
  ) {
    fail(`${MANIFEST_PATH}.recordIds does not match ${BUNDLE_PATH}`);
  }

  const frozenBundle = deepFreeze(bundle);
  const recordsById = new FrozenRecordMap(frozenBundle.records);
  const stale = now.getTime() >= Date.parse(frozenBundle.staleAfter);
  const stalenessWarning = stale
    ? `Catalogue freshness review expired at ${frozenBundle.staleAfter}; ` +
      "results are a governed snapshot, not current source authority."
    : null;
  const warnings = deepFreeze(stalenessWarning === null ? [] : [stalenessWarning]);

  const snapshot = Object.freeze({
    root,
    bundle: frozenBundle,
    recordsById,
    version: frozenBundle.version,
    revision: frozenBundle.revision,
    contentRootSha256: computedContentRoot,
    manifestSha256,
    recordCount: frozenBundle.recordCount,
    stale,
    stalenessWarning,
    warnings,
  });
  VERIFIED_CATALOGUE_SNAPSHOTS.add(snapshot);
  return snapshot;
}

/** Admit only the exact immutable value returned by the checksum-verifying loader. */
export function requireExactCatalogueSnapshot(value: unknown): CatalogueSnapshot {
  if (
    typeof value !== "object" ||
    value === null ||
    utilTypes.isProxy(value) ||
    !VERIFIED_CATALOGUE_SNAPSHOTS.has(value)
  ) {
    throw new TypeError("Catalogue snapshot is not an exact verified snapshot");
  }
  return value as CatalogueSnapshot;
}
