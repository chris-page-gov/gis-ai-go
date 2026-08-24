import { createHash } from "node:crypto";
import {
  closeSync,
  constants,
  fstatSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  opendirSync,
  readSync,
  realpathSync,
  writeSync,
  type Stats,
} from "node:fs";
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { types as utilTypes } from "node:util";

import { canonicalJson, canonicalJsonClone } from "./canonical-json.js";
import {
  contentAddress,
  domainSeparatedSha256,
  verifyContentAddress,
} from "./digest.js";
import {
  PublicEvidenceLedger,
  type PublicEvidenceLedgerHealth,
} from "./public-ledger.js";
import {
  PublicEvidenceReconciliationIndex,
  type EvidenceReconciliationIndexHealth,
} from "./reconciliation-index.js";
import { isStrictEvidenceDateTime } from "./receipt.js";

const CHECKPOINT_PREFIX = "gis-ai-go:evidence-checkpoint";
const CHECKPOINT_MANIFEST_DOMAIN = "gis-ai-go.evidence-checkpoint-manifest.v1";
const CHECKPOINT_ROOT_DOMAIN = "gis-ai-go.evidence-checkpoint-root.v1";
const CHECKPOINT_ID = /^gis-ai-go:evidence-checkpoint:sha256:[0-9a-f]{64}$/u;
const LEDGER_ID = /^gis-ai-go:public-evidence-ledger:sha256:[0-9a-f]{64}$/u;
const INDEX_ID = /^gis-ai-go:evidence-reconciliation-index:sha256:[0-9a-f]{64}$/u;
const EVENT_ID = /^gis-ai-go:evidence-ledger-event:sha256:[0-9a-f]{64}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const LEDGER_EVENT_FILE = /^\d{16}-[0-9a-f]{64}\.json$/u;
const LEDGER_RECORD_FILE = /^[0-9a-f]{64}\.json$/u;
const INDEX_DOCUMENT_FILE = /^[0-9a-f]{64}\.json$/u;
const INDEX_MARKER_FILE = /^[0-9a-f]{64}$/u;
const MAX_CONFIGURATION_PATH_LENGTH = 4_096;
const MAX_DESCRIPTOR_BYTES = 16_384;
const MAX_LEDGER_EVENT_BYTES = 65_536;
const MAX_LEDGER_RECORD_BYTES = 4_194_304;
const MAX_INDEX_CLAIM_BYTES = 32_768;
const MAX_INDEX_RESOLUTION_BYTES = 16_384;
const MAX_EVIDENCE_FILE_BYTES = MAX_LEDGER_RECORD_BYTES;
const MAX_CHECKPOINT_DOCUMENT_BYTES = 65_536;
const MAX_LEDGER_EVENTS = 1_000_000;
const MAX_INDEX_CLAIMS = 4_096;

const LEDGER_DIRECTORIES = Object.freeze(["events", "records"] as const);
const INDEX_DIRECTORIES = Object.freeze([
  "claim-ownership",
  "claim-ready",
  "claims",
  "resolution-ready",
  "resolutions",
] as const);

const MAX_LEDGER_CHECKPOINT_FILES = 1 + 2 * MAX_LEDGER_EVENTS;
const MAX_LEDGER_CHECKPOINT_ENTRIES = LEDGER_DIRECTORIES.length + MAX_LEDGER_CHECKPOINT_FILES;
const MAX_LEDGER_CHECKPOINT_BYTES =
  MAX_DESCRIPTOR_BYTES +
  MAX_LEDGER_EVENTS * (MAX_LEDGER_EVENT_BYTES + MAX_LEDGER_RECORD_BYTES);
const MAX_INDEX_CHECKPOINT_FILES = 1 + INDEX_DIRECTORIES.length * MAX_INDEX_CLAIMS;
const MAX_INDEX_CHECKPOINT_ENTRIES = INDEX_DIRECTORIES.length + MAX_INDEX_CHECKPOINT_FILES;
const MAX_INDEX_CHECKPOINT_BYTES =
  MAX_DESCRIPTOR_BYTES +
  MAX_INDEX_CLAIMS * (MAX_INDEX_CLAIM_BYTES + MAX_INDEX_RESOLUTION_BYTES);

type EvidenceRootRole = "ledger" | "reconciliation-index";

interface DirectoryInventoryEntry {
  readonly path: string;
  readonly kind: "directory";
  readonly mode: "0700";
}

interface FileInventoryEntry {
  readonly path: string;
  readonly kind: "file";
  readonly mode: "0600";
  readonly bytes: number;
  readonly sha256: string;
}

type InventoryEntry = DirectoryInventoryEntry | FileInventoryEntry;

interface EvidenceRootInventory {
  readonly role: EvidenceRootRole;
  readonly entries: readonly InventoryEntry[];
  readonly summary: EvidenceCheckpointRootSummary;
}

interface EvidenceRootTraversalLimits {
  readonly directoryCount: number;
  readonly maximumChildrenPerDirectory: number;
  readonly maximumEntries: number;
  readonly maximumFiles: number;
  readonly maximumTotalBytes: number;
}

export interface EvidenceCheckpointRootSummary {
  readonly root_sha256: string;
  readonly entry_count: number;
  readonly file_count: number;
  readonly total_bytes: number;
}

export interface EvidenceCheckpointLedgerState {
  readonly ledger_id: string;
  readonly retention_days: number;
  readonly event_count: number;
  readonly record_count: number;
  readonly last_event_id: string | null;
  readonly root: EvidenceCheckpointRootSummary;
}

export interface EvidenceCheckpointIndexState {
  readonly index_id: string;
  readonly ledger_id: string;
  readonly claim_count: number;
  readonly resolution_count: number;
  readonly completed_count: number;
  readonly pending_count: number;
  readonly root: EvidenceCheckpointRootSummary;
}

export interface EvidenceCheckpointManifestCore {
  readonly schema: "gis-ai-go.evidence-checkpoint-manifest.v1";
  readonly created_at: string;
  readonly quiescence: {
    readonly writer: "stopped-single-writer";
    readonly assertion: "operator-supplied";
    readonly source_verification: "complete-before-and-after-copy";
    readonly concurrent_change: "rejected";
  };
  readonly ledger: EvidenceCheckpointLedgerState;
  readonly reconciliation_index: EvidenceCheckpointIndexState;
  readonly recovery: {
    readonly destination_roots: "existing-empty-private-directories";
    readonly verification: "complete-ledger-and-index-after-restore";
    readonly in_place_repair: false;
    readonly disposal_automation: false;
  };
  readonly privacy: {
    readonly source_path: false;
    readonly destination_path: false;
    readonly raw_query: false;
    readonly result_material: false;
    readonly credentials: false;
    readonly personal_data: false;
  };
}

export interface EvidenceCheckpointManifest extends EvidenceCheckpointManifestCore {
  readonly checkpoint_id: string;
}

export interface EvidenceExternalCheckpoint {
  readonly schema: "gis-ai-go.evidence-external-checkpoint.v1";
  readonly created_at: string;
  readonly checkpoint_id: string;
  readonly manifest_sha256: string;
  readonly storage_boundary: "external-to-backup-required";
  readonly ledger: EvidenceCheckpointLedgerState;
  readonly reconciliation_index: EvidenceCheckpointIndexState;
}

export interface CreateEvidenceCheckpointOptions {
  readonly ledgerRootDirectory: string;
  readonly reconciliationIndexRootDirectory: string;
  readonly checkpointDirectory: string;
  readonly externalCheckpointFile: string;
  readonly stoppedSingleWriter: true;
  readonly now?: () => Date;
}

export interface VerifyEvidenceCheckpointOptions {
  readonly checkpointDirectory: string;
  readonly externalCheckpointFile: string;
}

export interface VerifyEvidenceRootsAgainstExternalCheckpointOptions {
  readonly ledgerRootDirectory: string;
  readonly reconciliationIndexRootDirectory: string;
  readonly externalCheckpointFile: string;
}

export interface RestoreEvidenceCheckpointOptions extends VerifyEvidenceCheckpointOptions {
  readonly ledgerDestinationRoot: string;
  readonly reconciliationIndexDestinationRoot: string;
  readonly now?: () => Date;
}

export interface EvidenceCheckpointVerification {
  readonly status: "verified";
  readonly checkpoint_id: string;
  readonly ledger: PublicEvidenceLedgerHealth;
  readonly reconciliation_index: EvidenceReconciliationIndexHealth;
  readonly checks: readonly [
    "external-checkpoint",
    "manifest-content-address",
    "private-modes-and-no-links",
    "complete-root-inventories",
    "ledger-verify",
    "reconciliation-index-verify",
  ];
}

export type EvidenceCheckpointErrorCode =
  | "checkpoint-mismatch"
  | "collision"
  | "corruption"
  | "destination-not-empty"
  | "invalid-configuration"
  | "io-failure"
  | "quiescence-required";

export class EvidenceCheckpointError extends Error {
  public constructor(public readonly code: EvidenceCheckpointErrorCode, message: string) {
    super(message);
    this.name = "EvidenceCheckpointError";
  }
}

function fail(code: EvidenceCheckpointErrorCode, message: string): never {
  throw new EvidenceCheckpointError(code, message);
}

function snapshotClosedOptions(
  value: unknown,
  required: readonly string[],
  optional: readonly string[],
  label: string,
): Readonly<Record<string, unknown>> {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    utilTypes.isProxy(value) ||
    ![Object.prototype, null].includes(Object.getPrototypeOf(value))
  ) {
    fail("invalid-configuration", `${label} are invalid`);
  }
  const allowed = new Set([...required, ...optional]);
  const keys = Reflect.ownKeys(value);
  if (
    keys.some((key) => typeof key !== "string" || !allowed.has(key)) ||
    required.some((key) => !keys.includes(key))
  ) {
    fail("invalid-configuration", `${label} are not closed`);
  }
  const snapshot: Record<string, unknown> = {};
  for (const key of keys as string[]) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (descriptor === undefined || !("value" in descriptor) || descriptor.enumerable !== true) {
      fail("invalid-configuration", `${label} must contain only enumerable data properties`);
    }
    snapshot[key] = descriptor.value;
  }
  return Object.freeze(snapshot);
}

function hasExactPrivateMode(mode: number, expected: 0o600 | 0o700): boolean {
  return process.platform === "win32" || (mode & 0o777) === expected;
}

function assertRealDirectory(path: string, privateMode: boolean): void {
  const stat = lstatSync(path);
  if (
    !stat.isDirectory() ||
    stat.isSymbolicLink() ||
    (privateMode && !hasExactPrivateMode(stat.mode, 0o700))
  ) {
    fail("corruption", "Evidence checkpoint requires a real directory with the required mode");
  }
}

function assertPrivateRegularFile(
  stat: Stats,
  allowEmpty: boolean,
  maximumBytes = MAX_EVIDENCE_FILE_BYTES,
): void {
  if (
    !stat.isFile() ||
    stat.isSymbolicLink() ||
    stat.nlink !== 1 ||
    !hasExactPrivateMode(stat.mode, 0o600) ||
    stat.size > maximumBytes ||
    (!allowEmpty && stat.size < 2)
  ) {
    fail(
      "corruption",
      "Evidence checkpoint requires private, unlinked regular files within the fixed byte bound",
    );
  }
}

function sameFile(left: Stats, right: Stats): boolean {
  return (
    left.isFile() &&
    right.isFile() &&
    left.dev === right.dev &&
    left.ino === right.ino &&
    left.mode === right.mode &&
    left.nlink === right.nlink &&
    left.size === right.size &&
    left.mtimeMs === right.mtimeMs &&
    left.ctimeMs === right.ctimeMs
  );
}

function readPrivateFile(
  path: string,
  allowEmpty: boolean,
  maximumBytes = MAX_EVIDENCE_FILE_BYTES,
): Buffer {
  const scanned = lstatSync(path);
  assertPrivateRegularFile(scanned, allowEmpty, maximumBytes);
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    const before = fstatSync(descriptor);
    if (!sameFile(scanned, before)) {
      fail("corruption", "Evidence checkpoint content changed during inspection");
    }
    const bytes = Buffer.allocUnsafe(scanned.size);
    let offset = 0;
    while (offset < bytes.length) {
      const count = readSync(descriptor, bytes, offset, bytes.length - offset, offset);
      if (count === 0) break;
      offset += count;
    }
    const after = fstatSync(descriptor);
    if (!sameFile(scanned, after) || offset !== scanned.size) {
      fail("corruption", "Evidence checkpoint content changed while it was read");
    }
    return bytes;
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
  }
}

function sha256Bytes(value: Uint8Array): string {
  return createHash("sha256").update(value).digest("hex");
}

function readCanonicalDocument(path: string): { readonly value: unknown; readonly bytes: Buffer } {
  const bytes = readPrivateFile(path, false, MAX_CHECKPOINT_DOCUMENT_BYTES);
  if (bytes.length > MAX_CHECKPOINT_DOCUMENT_BYTES) {
    fail("corruption", "Evidence checkpoint document exceeds its fixed bound");
  }
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    return fail("corruption", "Evidence checkpoint document is not canonical UTF-8");
  }
  if (!Buffer.from(text, "utf8").equals(bytes) || !text.endsWith("\n")) {
    fail("corruption", "Evidence checkpoint document has incomplete or non-canonical bytes");
  }
  let value: unknown;
  try {
    value = JSON.parse(text) as unknown;
  } catch {
    return fail("corruption", "Evidence checkpoint document is not valid JSON");
  }
  if (`${canonicalJson(value)}\n` !== text) {
    fail("corruption", "Evidence checkpoint document is not in its unique canonical form");
  }
  return Object.freeze({ value, bytes });
}

function asRecord(value: unknown, label: string): Record<string, unknown> {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    fail("corruption", `${label} has an invalid shape`);
  }
  return value as Record<string, unknown>;
}

function assertExactKeys(
  value: Record<string, unknown>,
  keys: readonly string[],
  label: string,
): void {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    fail("corruption", `${label} has an unexpected shape`);
  }
}

function assertTimestamp(value: unknown, label: string): asserts value is string {
  const milliseconds = typeof value === "string" ? Date.parse(value) : Number.NaN;
  if (
    typeof value !== "string" ||
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u.test(value) ||
    !isStrictEvidenceDateTime(value) ||
    !Number.isFinite(milliseconds) ||
    new Date(milliseconds).toISOString() !== value
  ) {
    fail("corruption", `${label} is not a canonical UTC timestamp`);
  }
}

function assertBoundedCount(
  value: unknown,
  maximum: number,
  label: string,
): asserts value is number {
  if (!Number.isSafeInteger(value) || (value as number) < 0 || (value as number) > maximum) {
    fail("corruption", `${label} is outside its accepted bound`);
  }
}

function assertRootSummary(
  value: unknown,
  label: string,
  role: EvidenceRootRole,
): asserts value is EvidenceCheckpointRootSummary {
  const record = asRecord(value, label);
  const limits = traversalLimits(role);
  assertExactKeys(record, ["entry_count", "file_count", "root_sha256", "total_bytes"], label);
  if (typeof record.root_sha256 !== "string" || !SHA256.test(record.root_sha256)) {
    fail("corruption", `${label} has an invalid content root`);
  }
  assertBoundedCount(record.entry_count, limits.maximumEntries, `${label} entry count`);
  assertBoundedCount(record.file_count, limits.maximumFiles, `${label} file count`);
  assertBoundedCount(record.total_bytes, limits.maximumTotalBytes, `${label} byte count`);
  if (
    record.file_count < 1 ||
    record.total_bytes < 2 ||
    record.entry_count !== record.file_count + limits.directoryCount
  ) {
    fail("corruption", `${label} counts are inconsistent with its fixed root structure`);
  }
}

function assertLedgerState(value: unknown): asserts value is EvidenceCheckpointLedgerState {
  const record = asRecord(value, "Evidence checkpoint ledger state");
  assertExactKeys(
    record,
    ["event_count", "last_event_id", "ledger_id", "record_count", "retention_days", "root"],
    "Evidence checkpoint ledger state",
  );
  if (typeof record.ledger_id !== "string" || !LEDGER_ID.test(record.ledger_id)) {
    fail("corruption", "Evidence checkpoint ledger identity is invalid");
  }
  assertBoundedCount(record.event_count, MAX_LEDGER_EVENTS, "Evidence checkpoint event count");
  assertBoundedCount(record.record_count, MAX_LEDGER_EVENTS, "Evidence checkpoint record count");
  assertBoundedCount(record.retention_days, 3_650, "Evidence checkpoint retention");
  if ((record.retention_days as number) < 1 || record.event_count !== record.record_count) {
    fail("corruption", "Evidence checkpoint ledger counts or retention are inconsistent");
  }
  if (
    (record.event_count === 0 && record.last_event_id !== null) ||
    (record.event_count !== 0 &&
      (typeof record.last_event_id !== "string" || !EVENT_ID.test(record.last_event_id)))
  ) {
    fail("corruption", "Evidence checkpoint ledger tail identity is inconsistent");
  }
  assertRootSummary(record.root, "Evidence checkpoint ledger root", "ledger");
  const expectedFiles = 1 + record.event_count + record.record_count;
  if (record.root.file_count !== expectedFiles) {
    fail("corruption", "Evidence checkpoint ledger root count does not match its ledger state");
  }
}

function assertIndexState(value: unknown): asserts value is EvidenceCheckpointIndexState {
  const record = asRecord(value, "Evidence checkpoint index state");
  assertExactKeys(
    record,
    [
      "claim_count",
      "completed_count",
      "index_id",
      "ledger_id",
      "pending_count",
      "resolution_count",
      "root",
    ],
    "Evidence checkpoint index state",
  );
  if (
    typeof record.index_id !== "string" ||
    !INDEX_ID.test(record.index_id) ||
    typeof record.ledger_id !== "string" ||
    !LEDGER_ID.test(record.ledger_id)
  ) {
    fail("corruption", "Evidence checkpoint index identities are invalid");
  }
  assertBoundedCount(record.claim_count, MAX_INDEX_CLAIMS, "Evidence checkpoint claim count");
  assertBoundedCount(
    record.resolution_count,
    MAX_INDEX_CLAIMS,
    "Evidence checkpoint resolution count",
  );
  assertBoundedCount(
    record.completed_count,
    MAX_INDEX_CLAIMS,
    "Evidence checkpoint completed count",
  );
  assertBoundedCount(record.pending_count, MAX_INDEX_CLAIMS, "Evidence checkpoint pending count");
  if (
    (record.resolution_count as number) > (record.claim_count as number) ||
    (record.completed_count as number) > (record.resolution_count as number) ||
    (record.pending_count as number) !==
      (record.claim_count as number) - (record.completed_count as number)
  ) {
    fail("corruption", "Evidence checkpoint index counts are inconsistent");
  }
  assertRootSummary(
    record.root,
    "Evidence checkpoint reconciliation root",
    "reconciliation-index",
  );
  const minimumFiles = 1 + record.claim_count + 4 * record.resolution_count;
  const maximumFiles = 1 + INDEX_DIRECTORIES.length * record.claim_count;
  if (record.root.file_count < minimumFiles || record.root.file_count > maximumFiles) {
    fail(
      "corruption",
      "Evidence checkpoint reconciliation root count does not match its index state",
    );
  }
}

function assertManifest(value: unknown): asserts value is EvidenceCheckpointManifest {
  const record = asRecord(value, "Evidence checkpoint manifest");
  assertExactKeys(
    record,
    [
      "checkpoint_id",
      "created_at",
      "ledger",
      "privacy",
      "quiescence",
      "reconciliation_index",
      "recovery",
      "schema",
    ],
    "Evidence checkpoint manifest",
  );
  if (
    record.schema !== "gis-ai-go.evidence-checkpoint-manifest.v1" ||
    typeof record.checkpoint_id !== "string" ||
    !CHECKPOINT_ID.test(record.checkpoint_id)
  ) {
    fail("corruption", "Evidence checkpoint manifest identity is invalid");
  }
  assertTimestamp(record.created_at, "Evidence checkpoint creation time");
  assertLedgerState(record.ledger);
  assertIndexState(record.reconciliation_index);
  if (record.reconciliation_index.ledger_id !== record.ledger.ledger_id) {
    fail("corruption", "Evidence checkpoint roots are not one linked pair");
  }
  const quiescence = asRecord(record.quiescence, "Evidence checkpoint quiescence");
  assertExactKeys(
    quiescence,
    ["assertion", "concurrent_change", "source_verification", "writer"],
    "Evidence checkpoint quiescence",
  );
  if (
    quiescence.writer !== "stopped-single-writer" ||
    quiescence.assertion !== "operator-supplied" ||
    quiescence.source_verification !== "complete-before-and-after-copy" ||
    quiescence.concurrent_change !== "rejected"
  ) {
    fail("corruption", "Evidence checkpoint quiescence claim is invalid");
  }
  const recovery = asRecord(record.recovery, "Evidence checkpoint recovery");
  assertExactKeys(
    recovery,
    ["destination_roots", "disposal_automation", "in_place_repair", "verification"],
    "Evidence checkpoint recovery",
  );
  if (
    recovery.destination_roots !== "existing-empty-private-directories" ||
    recovery.verification !== "complete-ledger-and-index-after-restore" ||
    recovery.in_place_repair !== false ||
    recovery.disposal_automation !== false
  ) {
    fail("corruption", "Evidence checkpoint recovery boundary is invalid");
  }
  const privacy = asRecord(record.privacy, "Evidence checkpoint privacy");
  assertExactKeys(
    privacy,
    [
      "credentials",
      "destination_path",
      "personal_data",
      "raw_query",
      "result_material",
      "source_path",
    ],
    "Evidence checkpoint privacy",
  );
  if (Object.values(privacy).some((entry) => entry !== false)) {
    fail("corruption", "Evidence checkpoint privacy boundary is invalid");
  }
  const { checkpoint_id: checkpointId, ...core } = record;
  if (
    !verifyContentAddress(
      checkpointId as string,
      CHECKPOINT_PREFIX,
      CHECKPOINT_MANIFEST_DOMAIN,
      core,
    )
  ) {
    fail("corruption", "Evidence checkpoint manifest content address does not match");
  }
}

function assertExternalCheckpoint(value: unknown): asserts value is EvidenceExternalCheckpoint {
  const record = asRecord(value, "External evidence checkpoint");
  assertExactKeys(
    record,
    [
      "checkpoint_id",
      "created_at",
      "ledger",
      "manifest_sha256",
      "reconciliation_index",
      "schema",
      "storage_boundary",
    ],
    "External evidence checkpoint",
  );
  if (
    record.schema !== "gis-ai-go.evidence-external-checkpoint.v1" ||
    typeof record.checkpoint_id !== "string" ||
    !CHECKPOINT_ID.test(record.checkpoint_id) ||
    typeof record.manifest_sha256 !== "string" ||
    !SHA256.test(record.manifest_sha256) ||
    record.storage_boundary !== "external-to-backup-required"
  ) {
    fail("corruption", "External evidence checkpoint constants are invalid");
  }
  assertTimestamp(record.created_at, "External evidence checkpoint creation time");
  assertLedgerState(record.ledger);
  assertIndexState(record.reconciliation_index);
  if (record.reconciliation_index.ledger_id !== record.ledger.ledger_id) {
    fail("corruption", "External evidence checkpoint does not bind one linked pair");
  }
  const reconstructed = buildManifest(
    record.created_at,
    record.ledger,
    record.reconciliation_index,
  );
  const reconstructedBytes = Buffer.from(`${canonicalJson(reconstructed)}\n`, "utf8");
  if (
    record.checkpoint_id !== reconstructed.checkpoint_id ||
    record.manifest_sha256 !== sha256Bytes(reconstructedBytes)
  ) {
    fail("corruption", "External evidence checkpoint does not reproduce its manifest identity");
  }
}

function allowedChild(role: EvidenceRootRole, directory: string, name: string): boolean {
  if (role === "ledger") {
    return directory === "events"
      ? LEDGER_EVENT_FILE.test(name)
      : directory === "records" && LEDGER_RECORD_FILE.test(name);
  }
  if (directory === "claims" || directory === "resolutions") {
    return INDEX_DOCUMENT_FILE.test(name);
  }
  return INDEX_MARKER_FILE.test(name);
}

function expectedRootEntries(role: EvidenceRootRole): readonly string[] {
  return role === "ledger"
    ? Object.freeze(["events", "ledger.json", "records"])
    : Object.freeze([
        "claim-ownership",
        "claim-ready",
        "claims",
        "index.json",
        "resolution-ready",
        "resolutions",
      ]);
}

function traversalLimits(role: EvidenceRootRole): EvidenceRootTraversalLimits {
  return role === "ledger"
    ? Object.freeze({
        directoryCount: LEDGER_DIRECTORIES.length,
        maximumChildrenPerDirectory: MAX_LEDGER_EVENTS,
        maximumEntries: MAX_LEDGER_CHECKPOINT_ENTRIES,
        maximumFiles: MAX_LEDGER_CHECKPOINT_FILES,
        maximumTotalBytes: MAX_LEDGER_CHECKPOINT_BYTES,
      })
    : Object.freeze({
        directoryCount: INDEX_DIRECTORIES.length,
        maximumChildrenPerDirectory: MAX_INDEX_CLAIMS,
        maximumEntries: MAX_INDEX_CHECKPOINT_ENTRIES,
        maximumFiles: MAX_INDEX_CHECKPOINT_FILES,
        maximumTotalBytes: MAX_INDEX_CHECKPOINT_BYTES,
      });
}

function maximumInventoryFileBytes(
  role: EvidenceRootRole,
  directory: string | undefined,
): number {
  if (directory === undefined) return MAX_DESCRIPTOR_BYTES;
  if (role === "ledger") {
    return directory === "events" ? MAX_LEDGER_EVENT_BYTES : MAX_LEDGER_RECORD_BYTES;
  }
  if (directory === "claims") return MAX_INDEX_CLAIM_BYTES;
  if (directory === "resolutions") return MAX_INDEX_RESOLUTION_BYTES;
  return 0;
}

function readBoundedDirectoryNames(path: string, maximum: number, label: string): string[] {
  const directory = opendirSync(path);
  const names: string[] = [];
  try {
    for (;;) {
      const entry = directory.readSync();
      if (entry === null) break;
      if (names.length >= maximum) {
        fail("corruption", `${label} exceeds its fixed entry bound`);
      }
      names.push(entry.name);
    }
  } finally {
    directory.closeSync();
  }
  return names.sort();
}

function scanEvidenceRoot(
  root: string,
  role: EvidenceRootRole,
  expectedSummary?: EvidenceCheckpointRootSummary,
): EvidenceRootInventory {
  assertRealDirectory(root, true);
  const expected = expectedRootEntries(role);
  const rootEntries = readBoundedDirectoryNames(root, expected.length, "Evidence root");
  if (
    rootEntries.length !== expected.length ||
    rootEntries.some((entry, index) => entry !== expected[index])
  ) {
    fail("corruption", "Evidence checkpoint source has an unexpected root entry");
  }
  const directories = role === "ledger" ? LEDGER_DIRECTORIES : INDEX_DIRECTORIES;
  const descriptor = role === "ledger" ? "ledger.json" : "index.json";
  const entries: InventoryEntry[] = [];
  const limits = traversalLimits(role);
  const maximumFiles = Math.min(
    limits.maximumFiles,
    expectedSummary?.file_count ?? limits.maximumFiles,
  );
  const maximumTotalBytes = Math.min(
    limits.maximumTotalBytes,
    expectedSummary?.total_bytes ?? limits.maximumTotalBytes,
  );
  let totalBytes = 0;
  let fileCount = 0;

  const addFile = (
    relativePath: string,
    directory: string | undefined,
    allowEmpty: boolean,
  ): void => {
    if (fileCount >= maximumFiles) {
      fail("corruption", "Evidence checkpoint source exceeds its fixed file bound");
    }
    const remainingBytes = maximumTotalBytes - totalBytes;
    const bytes = readPrivateFile(
      join(root, relativePath),
      allowEmpty,
      Math.min(maximumInventoryFileBytes(role, directory), remainingBytes),
    );
    entries.push(
      Object.freeze({
        path: relativePath,
        kind: "file",
        mode: "0600",
        bytes: bytes.length,
        sha256: sha256Bytes(bytes),
      }),
    );
    totalBytes += bytes.length;
    fileCount += 1;
  };

  addFile(descriptor, undefined, false);

  for (const directory of directories) {
    const directoryPath = join(root, directory);
    assertRealDirectory(directoryPath, true);
    entries.push(Object.freeze({ path: directory, kind: "directory", mode: "0700" }));
    const maximumChildren = Math.min(
      limits.maximumChildrenPerDirectory,
      maximumFiles - fileCount,
    );
    for (const name of readBoundedDirectoryNames(
      directoryPath,
      maximumChildren,
      `Evidence ${role} ${directory} directory`,
    )) {
      if (!allowedChild(role, directory, name)) {
        fail("corruption", "Evidence checkpoint source has an unexpected child entry");
      }
      const relativePath = `${directory}/${name}`;
      const allowEmpty =
        role === "reconciliation-index" &&
        directory !== "claims" &&
        directory !== "resolutions";
      addFile(relativePath, directory, allowEmpty);
    }
  }
  entries.sort((left, right) => (left.path < right.path ? -1 : left.path > right.path ? 1 : 0));
  const summary: EvidenceCheckpointRootSummary = Object.freeze({
    root_sha256: domainSeparatedSha256(CHECKPOINT_ROOT_DOMAIN, {
      role,
      entries,
    }),
    entry_count: entries.length,
    file_count: fileCount,
    total_bytes: totalBytes,
  });
  return Object.freeze({ role, entries: Object.freeze(entries), summary });
}

function inventoriesMatch(left: EvidenceRootInventory, right: EvidenceRootInventory): boolean {
  return canonicalJson({ role: left.role, entries: left.entries }) ===
    canonicalJson({ role: right.role, entries: right.entries });
}

function pathsOverlap(left: string, right: string): boolean {
  if (left === right) return true;
  const below = (parent: string, candidate: string): boolean => {
    const candidateFromParent = relative(parent, candidate);
    return (
      candidateFromParent !== "" &&
      candidateFromParent !== ".." &&
      !candidateFromParent.startsWith(`..${sep}`) &&
      !isAbsolute(candidateFromParent)
    );
  };
  return below(left, right) || below(right, left);
}

function configurationPath(value: unknown, label: string): string {
  if (
    typeof value !== "string" ||
    value.length < 1 ||
    value.length > MAX_CONFIGURATION_PATH_LENGTH ||
    value.includes("\0") ||
    value.trim() === ""
  ) {
    fail("invalid-configuration", `${label} is invalid`);
  }
  return resolve(value);
}

function canonicalExistingPath(path: string, privateDirectory: boolean): string {
  assertRealDirectory(path, privateDirectory);
  return realpathSync(path);
}

function canonicalNewPath(path: string): string {
  const parent = dirname(path);
  assertRealDirectory(parent, false);
  return join(realpathSync(parent), basename(path));
}

function entryExists(path: string): boolean {
  try {
    lstatSync(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
}

function syncDirectory(path: string): void {
  const descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    fsyncSync(descriptor);
  } finally {
    closeSync(descriptor);
  }
}

function writeExclusiveFile(path: string, bytes: Uint8Array): void {
  let descriptor: number | undefined;
  try {
    descriptor = openSync(
      path,
      constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW,
      0o600,
    );
    let offset = 0;
    while (offset < bytes.length) {
      const count = writeSync(descriptor, bytes, offset, bytes.length - offset, offset);
      if (count < 1) fail("io-failure", "Evidence checkpoint file write did not complete");
      offset += count;
    }
    fsyncSync(descriptor);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "EEXIST") {
      fail("collision", "Evidence checkpoint refused to overwrite an existing file");
    }
    throw error;
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
  }
}

function writeExclusiveCanonical(path: string, value: unknown): Buffer {
  const bytes = Buffer.from(`${canonicalJson(value)}\n`, "utf8");
  writeExclusiveFile(path, bytes);
  syncDirectory(dirname(path));
  return bytes;
}

function createPrivateDirectory(path: string): void {
  if (entryExists(path)) {
    fail("collision", "Evidence checkpoint refused to overwrite an existing directory");
  }
  mkdirSync(path, { mode: 0o700 });
  syncDirectory(dirname(path));
  assertRealDirectory(path, true);
}

function assertEmptyPrivateRoot(path: string): void {
  assertRealDirectory(path, true);
  const directory = opendirSync(path);
  try {
    if (directory.readSync() !== null) {
      fail("destination-not-empty", "Evidence recovery requires two empty destination roots");
    }
  } finally {
    directory.closeSync();
  }
}

function copyInventory(
  sourceRoot: string,
  destinationRoot: string,
  inventory: EvidenceRootInventory,
): void {
  for (const entry of inventory.entries.filter((candidate) => candidate.kind === "directory")) {
    createPrivateDirectory(join(destinationRoot, entry.path));
  }
  for (const entry of inventory.entries.filter(
    (candidate): candidate is FileInventoryEntry => candidate.kind === "file",
  )) {
    const bytes = readPrivateFile(
      join(sourceRoot, entry.path),
      inventory.role === "reconciliation-index" && entry.bytes === 0,
      entry.bytes,
    );
    if (bytes.length !== entry.bytes || sha256Bytes(bytes) !== entry.sha256) {
      fail("corruption", "Evidence checkpoint source changed during copy");
    }
    writeExclusiveFile(join(destinationRoot, entry.path), bytes);
  }
  const directories = inventory.entries
    .filter((candidate): candidate is DirectoryInventoryEntry => candidate.kind === "directory")
    .map((entry) => join(destinationRoot, entry.path))
    .sort((left, right) => right.length - left.length);
  for (const directory of directories) syncDirectory(directory);
  syncDirectory(destinationRoot);
}

function currentTimestamp(now: (() => Date) | undefined): string {
  const value = (now ?? (() => new Date()))();
  if (!(value instanceof Date) || !Number.isFinite(value.valueOf())) {
    fail("invalid-configuration", "Evidence checkpoint clock must return a valid Date");
  }
  return value.toISOString();
}

function verifyPair(
  ledger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
): {
  readonly ledgerHealth: PublicEvidenceLedgerHealth;
  readonly indexHealth: EvidenceReconciliationIndexHealth;
} {
  if (
    !(ledger instanceof PublicEvidenceLedger) ||
    utilTypes.isProxy(ledger) ||
    !(reconciliationIndex instanceof PublicEvidenceReconciliationIndex) ||
    utilTypes.isProxy(reconciliationIndex) ||
    reconciliationIndex.ledger !== ledger
  ) {
    fail(
      "invalid-configuration",
      "Evidence checkpoint requires one exact linked ledger/index pair",
    );
  }
  const ledgerHealth = PublicEvidenceLedger.prototype.verify.call(ledger);
  const indexHealth = PublicEvidenceReconciliationIndex.prototype.verify.call(reconciliationIndex);
  if (
    indexHealth.ledger_id !== ledgerHealth.ledger_id ||
    reconciliationIndex.descriptor.ledger_id !== ledger.descriptor.ledger_id
  ) {
    fail("corruption", "Evidence checkpoint pair linkage verification failed");
  }
  return Object.freeze({ ledgerHealth, indexHealth });
}

function ledgerRetentionDays(root: string): number {
  const descriptor = asRecord(
    readCanonicalDocument(join(root, "ledger.json")).value,
    "Evidence ledger descriptor",
  );
  assertBoundedCount(descriptor.retention_days, 3_650, "Evidence ledger retention");
  if ((descriptor.retention_days as number) < 1) {
    fail("corruption", "Evidence ledger retention is invalid");
  }
  return descriptor.retention_days as number;
}

function openPairAtRoots(
  ledgerRoot: string,
  indexRoot: string,
): {
  readonly ledger: PublicEvidenceLedger;
  readonly reconciliationIndex: PublicEvidenceReconciliationIndex;
  readonly ledgerHealth: PublicEvidenceLedgerHealth;
  readonly indexHealth: EvidenceReconciliationIndexHealth;
} {
  const ledger = PublicEvidenceLedger.open({
    rootDirectory: ledgerRoot,
    retentionDays: ledgerRetentionDays(ledgerRoot),
  });
  const reconciliationIndex = PublicEvidenceReconciliationIndex.open({
    rootDirectory: indexRoot,
    ledger,
  });
  return Object.freeze({ ledger, reconciliationIndex, ...verifyPair(ledger, reconciliationIndex) });
}

function ledgerState(
  ledger: PublicEvidenceLedger,
  health: PublicEvidenceLedgerHealth,
  inventory: EvidenceRootInventory,
): EvidenceCheckpointLedgerState {
  return Object.freeze({
    ledger_id: health.ledger_id,
    retention_days: ledger.descriptor.retention_days,
    event_count: health.event_count,
    record_count: health.record_count,
    last_event_id: health.last_event_id,
    root: inventory.summary,
  });
}

function indexState(
  health: EvidenceReconciliationIndexHealth,
  inventory: EvidenceRootInventory,
): EvidenceCheckpointIndexState {
  return Object.freeze({
    index_id: health.index_id,
    ledger_id: health.ledger_id,
    claim_count: health.claim_count,
    resolution_count: health.resolution_count,
    completed_count: health.completed_count,
    pending_count: health.pending_count,
    root: inventory.summary,
  });
}

function buildManifest(
  createdAt: string,
  ledger: EvidenceCheckpointLedgerState,
  reconciliationIndex: EvidenceCheckpointIndexState,
): EvidenceCheckpointManifest {
  const core: EvidenceCheckpointManifestCore = {
    schema: "gis-ai-go.evidence-checkpoint-manifest.v1",
    created_at: createdAt,
    quiescence: {
      writer: "stopped-single-writer",
      assertion: "operator-supplied",
      source_verification: "complete-before-and-after-copy",
      concurrent_change: "rejected",
    },
    ledger,
    reconciliation_index: reconciliationIndex,
    recovery: {
      destination_roots: "existing-empty-private-directories",
      verification: "complete-ledger-and-index-after-restore",
      in_place_repair: false,
      disposal_automation: false,
    },
    privacy: {
      source_path: false,
      destination_path: false,
      raw_query: false,
      result_material: false,
      credentials: false,
      personal_data: false,
    },
  };
  return canonicalJsonClone({
    ...core,
    checkpoint_id: contentAddress(
      CHECKPOINT_PREFIX,
      CHECKPOINT_MANIFEST_DOMAIN,
      core,
    ),
  });
}

function buildExternalCheckpoint(
  manifest: EvidenceCheckpointManifest,
  manifestBytes: Uint8Array,
): EvidenceExternalCheckpoint {
  return canonicalJsonClone({
    schema: "gis-ai-go.evidence-external-checkpoint.v1",
    created_at: manifest.created_at,
    checkpoint_id: manifest.checkpoint_id,
    manifest_sha256: sha256Bytes(manifestBytes),
    storage_boundary: "external-to-backup-required",
    ledger: manifest.ledger,
    reconciliation_index: manifest.reconciliation_index,
  });
}

function statesMatch(
  manifest: EvidenceCheckpointManifest,
  external: EvidenceExternalCheckpoint,
): boolean {
  return (
    external.created_at === manifest.created_at &&
    external.checkpoint_id === manifest.checkpoint_id &&
    canonicalJson(external.ledger) === canonicalJson(manifest.ledger) &&
    canonicalJson(external.reconciliation_index) === canonicalJson(manifest.reconciliation_index)
  );
}

function healthMatchesStates(
  ledger: EvidenceCheckpointLedgerState,
  reconciliationIndex: EvidenceCheckpointIndexState,
  ledgerHealth: PublicEvidenceLedgerHealth,
  indexHealth: EvidenceReconciliationIndexHealth,
): boolean {
  return (
    ledgerHealth.ledger_id === ledger.ledger_id &&
    ledgerHealth.event_count === ledger.event_count &&
    ledgerHealth.record_count === ledger.record_count &&
    ledgerHealth.last_event_id === ledger.last_event_id &&
    indexHealth.index_id === reconciliationIndex.index_id &&
    indexHealth.ledger_id === reconciliationIndex.ledger_id &&
    indexHealth.claim_count === reconciliationIndex.claim_count &&
    indexHealth.resolution_count === reconciliationIndex.resolution_count &&
    indexHealth.completed_count === reconciliationIndex.completed_count &&
    indexHealth.pending_count === reconciliationIndex.pending_count
  );
}

function verificationResult(
  checkpointId: string,
  ledger: PublicEvidenceLedgerHealth,
  reconciliationIndex: EvidenceReconciliationIndexHealth,
): EvidenceCheckpointVerification {
  return canonicalJsonClone({
    status: "verified",
    checkpoint_id: checkpointId,
    ledger,
    reconciliation_index: reconciliationIndex,
    checks: [
      "external-checkpoint",
      "manifest-content-address",
      "private-modes-and-no-links",
      "complete-root-inventories",
      "ledger-verify",
      "reconciliation-index-verify",
    ],
  });
}

function assertDisjoint(paths: readonly string[]): void {
  for (let left = 0; left < paths.length; left += 1) {
    for (let right = left + 1; right < paths.length; right += 1) {
      const leftPath = paths[left];
      const rightPath = paths[right];
      if (leftPath === undefined || rightPath === undefined || pathsOverlap(leftPath, rightPath)) {
        fail("invalid-configuration", "Evidence checkpoint paths must be disjoint");
      }
    }
  }
}

function readCheckpointManifest(checkpointRoot: string): {
  readonly manifest: EvidenceCheckpointManifest;
  readonly manifestBytes: Buffer;
} {
  const expected = ["ledger", "manifest.json", "reconciliation-index"];
  const entries = readBoundedDirectoryNames(
    checkpointRoot,
    expected.length,
    "Evidence checkpoint directory",
  );
  if (
    entries.length !== expected.length ||
    entries.some((entry, index) => entry !== expected[index])
  ) {
    fail("corruption", "Evidence checkpoint directory is incomplete or has unrelated entries");
  }
  const manifestDocument = readCanonicalDocument(join(checkpointRoot, "manifest.json"));
  assertManifest(manifestDocument.value);
  return Object.freeze({
    manifest: canonicalJsonClone(manifestDocument.value),
    manifestBytes: manifestDocument.bytes,
  });
}

function readCheckpointDocuments(
  checkpointRoot: string,
  externalFile: string,
): {
  readonly manifest: EvidenceCheckpointManifest;
  readonly manifestBytes: Buffer;
  readonly external: EvidenceExternalCheckpoint;
} {
  const manifestDocument = readCheckpointManifest(checkpointRoot);
  const externalDocument = readCanonicalDocument(externalFile);
  assertExternalCheckpoint(externalDocument.value);
  if (
    !statesMatch(manifestDocument.manifest, externalDocument.value) ||
    sha256Bytes(manifestDocument.manifestBytes) !== externalDocument.value.manifest_sha256
  ) {
    fail("checkpoint-mismatch", "External checkpoint does not match the complete backup manifest");
  }
  return Object.freeze({
    ...manifestDocument,
    external: canonicalJsonClone(externalDocument.value),
  });
}

function verifyCheckpointPayload(
  checkpointRoot: string,
  manifest: EvidenceCheckpointManifest,
): EvidenceCheckpointVerification {
  const ledgerRoot = join(checkpointRoot, "ledger");
  const indexRoot = join(checkpointRoot, "reconciliation-index");
  const ledgerInventoryBefore = scanEvidenceRoot(ledgerRoot, "ledger", manifest.ledger.root);
  const indexInventoryBefore = scanEvidenceRoot(
    indexRoot,
    "reconciliation-index",
    manifest.reconciliation_index.root,
  );
  if (
    canonicalJson(ledgerInventoryBefore.summary) !== canonicalJson(manifest.ledger.root) ||
    canonicalJson(indexInventoryBefore.summary) !==
      canonicalJson(manifest.reconciliation_index.root)
  ) {
    fail("checkpoint-mismatch", "Evidence checkpoint root content does not match its manifest");
  }

  const ledger = PublicEvidenceLedger.open({
    rootDirectory: ledgerRoot,
    retentionDays: manifest.ledger.retention_days,
  });
  const reconciliationIndex = PublicEvidenceReconciliationIndex.open({
    rootDirectory: indexRoot,
    ledger,
  });
  const { ledgerHealth, indexHealth } = verifyPair(ledger, reconciliationIndex);
  const ledgerInventoryAfter = scanEvidenceRoot(ledgerRoot, "ledger", manifest.ledger.root);
  const indexInventoryAfter = scanEvidenceRoot(
    indexRoot,
    "reconciliation-index",
    manifest.reconciliation_index.root,
  );
  if (
    !healthMatchesStates(
      manifest.ledger,
      manifest.reconciliation_index,
      ledgerHealth,
      indexHealth,
    ) ||
    !inventoriesMatch(ledgerInventoryBefore, ledgerInventoryAfter) ||
    !inventoriesMatch(indexInventoryBefore, indexInventoryAfter)
  ) {
    fail("checkpoint-mismatch", "Evidence checkpoint changed or failed complete pair verification");
  }
  return verificationResult(manifest.checkpoint_id, ledgerHealth, indexHealth);
}

function verifyCheckpointInternal(
  options: VerifyEvidenceCheckpointOptions,
): EvidenceCheckpointVerification {
  const checkpointPath = configurationPath(options.checkpointDirectory, "Checkpoint directory");
  const externalPath = configurationPath(
    options.externalCheckpointFile,
    "External checkpoint file",
  );
  const checkpointRoot = canonicalExistingPath(checkpointPath, true);
  const externalStat = lstatSync(externalPath);
  assertPrivateRegularFile(externalStat, false, MAX_CHECKPOINT_DOCUMENT_BYTES);
  const externalFile = realpathSync(externalPath);
  assertDisjoint([checkpointRoot, externalFile]);

  const { manifest } = readCheckpointDocuments(checkpointRoot, externalFile);
  return verifyCheckpointPayload(checkpointRoot, manifest);
}

/**
 * Copy one stopped, linked ledger/index pair into a new private checkpoint and
 * issue its small path-free checkpoint document outside that backup directory.
 */
export function createEvidenceCheckpoint(
  options: CreateEvidenceCheckpointOptions,
): EvidenceCheckpointVerification {
  try {
    const snapshot = snapshotClosedOptions(
      options,
      [
        "checkpointDirectory",
        "externalCheckpointFile",
        "ledgerRootDirectory",
        "reconciliationIndexRootDirectory",
        "stoppedSingleWriter",
      ],
      ["now"],
      "Evidence checkpoint options",
    );
    if (snapshot.stoppedSingleWriter !== true) {
      fail("quiescence-required", "Evidence checkpoint requires the single writer to be stopped");
    }
    if (snapshot.now !== undefined && typeof snapshot.now !== "function") {
      fail("invalid-configuration", "Evidence checkpoint clock is invalid");
    }
    const ledgerPath = configurationPath(
      snapshot.ledgerRootDirectory,
      "Evidence ledger root",
    );
    const indexPath = configurationPath(
      snapshot.reconciliationIndexRootDirectory,
      "Reconciliation index root",
    );
    const ledgerRoot = canonicalExistingPath(ledgerPath, true);
    const indexRoot = canonicalExistingPath(indexPath, true);
    const checkpointPath = configurationPath(snapshot.checkpointDirectory, "Checkpoint directory");
    const externalPath = configurationPath(
      snapshot.externalCheckpointFile,
      "External checkpoint file",
    );
    const checkpointRoot = canonicalNewPath(checkpointPath);
    const externalFile = canonicalNewPath(externalPath);
    if (entryExists(checkpointPath) || entryExists(externalPath)) {
      fail("collision", "Evidence checkpoint outputs must not already exist");
    }
    assertDisjoint([ledgerRoot, indexRoot, checkpointRoot, externalFile]);

    const ledgerInventoryBefore = scanEvidenceRoot(ledgerRoot, "ledger");
    const indexInventoryBefore = scanEvidenceRoot(indexRoot, "reconciliation-index");
    const {
      ledger,
      reconciliationIndex,
      ledgerHealth: healthBefore,
      indexHealth: indexHealthBefore,
    } = openPairAtRoots(ledgerRoot, indexRoot);
    createPrivateDirectory(checkpointPath);
    const checkpointLedgerRoot = join(checkpointPath, "ledger");
    const checkpointIndexRoot = join(checkpointPath, "reconciliation-index");
    createPrivateDirectory(checkpointLedgerRoot);
    createPrivateDirectory(checkpointIndexRoot);
    copyInventory(ledgerRoot, checkpointLedgerRoot, ledgerInventoryBefore);
    copyInventory(indexRoot, checkpointIndexRoot, indexInventoryBefore);

    const { ledgerHealth: healthAfter, indexHealth: indexHealthAfter } = verifyPair(
      ledger,
      reconciliationIndex,
    );
    const ledgerInventoryAfter = scanEvidenceRoot(ledgerRoot, "ledger");
    const indexInventoryAfter = scanEvidenceRoot(indexRoot, "reconciliation-index");
    if (
      canonicalJson(healthBefore) !== canonicalJson(healthAfter) ||
      canonicalJson(indexHealthBefore) !== canonicalJson(indexHealthAfter) ||
      !inventoriesMatch(ledgerInventoryBefore, ledgerInventoryAfter) ||
      !inventoriesMatch(indexInventoryBefore, indexInventoryAfter)
    ) {
      fail("corruption", "Evidence checkpoint source changed during stopped-writer capture");
    }

    const manifest = buildManifest(
      currentTimestamp(snapshot.now as (() => Date) | undefined),
      ledgerState(ledger, healthAfter, ledgerInventoryAfter),
      indexState(indexHealthAfter, indexInventoryAfter),
    );
    const manifestBytes = writeExclusiveCanonical(join(checkpointPath, "manifest.json"), manifest);
    const external = buildExternalCheckpoint(manifest, manifestBytes);
    assertExternalCheckpoint(external);
    const checkpointRootAfterWrites = canonicalExistingPath(checkpointPath, true);
    const storedManifest = readCheckpointManifest(checkpointRootAfterWrites);
    if (
      !storedManifest.manifestBytes.equals(manifestBytes) ||
      canonicalJson(storedManifest.manifest) !== canonicalJson(manifest)
    ) {
      fail("checkpoint-mismatch", "Evidence checkpoint manifest changed after its candidate write");
    }
    const checkpointVerification = verifyCheckpointPayload(
      checkpointRootAfterWrites,
      storedManifest.manifest,
    );
    // This complete source verification is the snapshot linearisation point.
    // Any change visible here leaves the external commit record unpublished.
    const {
      ledgerHealth: healthFinal,
      indexHealth: indexHealthFinal,
    } = verifyPair(ledger, reconciliationIndex);
    const ledgerInventoryFinal = scanEvidenceRoot(ledgerRoot, "ledger", manifest.ledger.root);
    const indexInventoryFinal = scanEvidenceRoot(
      indexRoot,
      "reconciliation-index",
      manifest.reconciliation_index.root,
    );
    if (
      canonicalJson(healthAfter) !== canonicalJson(healthFinal) ||
      canonicalJson(indexHealthAfter) !== canonicalJson(indexHealthFinal) ||
      !inventoriesMatch(ledgerInventoryAfter, ledgerInventoryFinal) ||
      !inventoriesMatch(indexInventoryAfter, indexInventoryFinal)
    ) {
      fail("corruption", "Evidence checkpoint source changed before checkpoint publication");
    }
    // The external checkpoint is the transaction commit record. Until this
    // exclusive, durable write completes, a standalone verifier rejects the
    // candidate even when its copied payload and manifest are otherwise valid.
    // A successful return means the complete canonical bytes, file and parent
    // directory have all been synchronised by writeExclusiveCanonical.
    writeExclusiveCanonical(externalPath, external);
    return checkpointVerification;
  } catch (error) {
    if (error instanceof EvidenceCheckpointError) throw error;
    fail("io-failure", "Evidence checkpoint creation failed closed");
  }
}

/** Verify the complete backup, its external checkpoint and both restored store contracts. */
export function verifyEvidenceCheckpoint(
  options: VerifyEvidenceCheckpointOptions,
): EvidenceCheckpointVerification {
  try {
    const snapshot = snapshotClosedOptions(
      options,
      ["checkpointDirectory", "externalCheckpointFile"],
      [],
      "Evidence checkpoint options",
    );
    return verifyCheckpointInternal({
      checkpointDirectory: snapshot.checkpointDirectory as string,
      externalCheckpointFile: snapshot.externalCheckpointFile as string,
    });
  } catch (error) {
    if (error instanceof EvidenceCheckpointError) throw error;
    fail("io-failure", "Evidence checkpoint verification failed closed");
  }
}

/**
 * Compare a currently verified pair with a separately retained checkpoint. This
 * detects a structurally valid deletion or rollback of the ledger tail.
 */
export function verifyEvidenceRootsAgainstExternalCheckpoint(
  options: VerifyEvidenceRootsAgainstExternalCheckpointOptions,
): EvidenceCheckpointVerification {
  try {
    const snapshot = snapshotClosedOptions(
      options,
      [
        "externalCheckpointFile",
        "ledgerRootDirectory",
        "reconciliationIndexRootDirectory",
      ],
      [],
      "External checkpoint verification options",
    );
    const ledgerPath = configurationPath(
      snapshot.ledgerRootDirectory,
      "Evidence ledger root",
    );
    const indexPath = configurationPath(
      snapshot.reconciliationIndexRootDirectory,
      "Reconciliation index root",
    );
    const ledgerRoot = canonicalExistingPath(ledgerPath, true);
    const indexRoot = canonicalExistingPath(indexPath, true);
    const externalPath = configurationPath(
      snapshot.externalCheckpointFile,
      "External checkpoint file",
    );
    const externalStat = lstatSync(externalPath);
    assertPrivateRegularFile(externalStat, false, MAX_CHECKPOINT_DOCUMENT_BYTES);
    const externalFile = realpathSync(externalPath);
    assertDisjoint([ledgerRoot, indexRoot, externalFile]);
    const externalDocument = readCanonicalDocument(externalFile);
    assertExternalCheckpoint(externalDocument.value);

    const ledgerBefore = scanEvidenceRoot(
      ledgerRoot,
      "ledger",
      externalDocument.value.ledger.root,
    );
    const indexBefore = scanEvidenceRoot(
      indexRoot,
      "reconciliation-index",
      externalDocument.value.reconciliation_index.root,
    );
    const {
      ledger,
      reconciliationIndex,
      ledgerHealth,
      indexHealth,
    } = openPairAtRoots(ledgerRoot, indexRoot);
    const { ledgerHealth: verifiedLedgerHealth, indexHealth: verifiedIndexHealth } = verifyPair(
      ledger,
      reconciliationIndex,
    );
    const ledgerAfter = scanEvidenceRoot(
      ledgerRoot,
      "ledger",
      externalDocument.value.ledger.root,
    );
    const indexAfter = scanEvidenceRoot(
      indexRoot,
      "reconciliation-index",
      externalDocument.value.reconciliation_index.root,
    );
    if (
      canonicalJson(ledgerHealth) !== canonicalJson(verifiedLedgerHealth) ||
      canonicalJson(indexHealth) !== canonicalJson(verifiedIndexHealth) ||
      !inventoriesMatch(ledgerBefore, ledgerAfter) ||
      !inventoriesMatch(indexBefore, indexAfter) ||
      canonicalJson(ledgerAfter.summary) !== canonicalJson(externalDocument.value.ledger.root) ||
      canonicalJson(indexAfter.summary) !==
        canonicalJson(externalDocument.value.reconciliation_index.root) ||
      !healthMatchesStates(
        externalDocument.value.ledger,
        externalDocument.value.reconciliation_index,
        verifiedLedgerHealth,
        verifiedIndexHealth,
      )
    ) {
      fail("checkpoint-mismatch", "Current evidence roots do not match the external checkpoint");
    }
    return verificationResult(
      externalDocument.value.checkpoint_id,
      verifiedLedgerHealth,
      verifiedIndexHealth,
    );
  } catch (error) {
    if (error instanceof EvidenceCheckpointError) throw error;
    fail("io-failure", "External evidence checkpoint verification failed closed");
  }
}

/**
 * Restore a verified checkpoint only into two existing, empty, private and
 * disjoint roots, then run both complete store verifiers on the restored pair.
 */
export function restoreEvidenceCheckpoint(
  options: RestoreEvidenceCheckpointOptions,
): EvidenceCheckpointVerification {
  try {
    const snapshot = snapshotClosedOptions(
      options,
      [
        "checkpointDirectory",
        "externalCheckpointFile",
        "ledgerDestinationRoot",
        "reconciliationIndexDestinationRoot",
      ],
      ["now"],
      "Evidence recovery options",
    );
    if (snapshot.now !== undefined && typeof snapshot.now !== "function") {
      fail("invalid-configuration", "Evidence recovery clock is invalid");
    }
    const checkpointPath = configurationPath(snapshot.checkpointDirectory, "Checkpoint directory");
    const externalPath = configurationPath(
      snapshot.externalCheckpointFile,
      "External checkpoint file",
    );
    verifyCheckpointInternal({
      checkpointDirectory: checkpointPath,
      externalCheckpointFile: externalPath,
    });
    const ledgerDestination = configurationPath(
      snapshot.ledgerDestinationRoot,
      "Ledger destination root",
    );
    const indexDestination = configurationPath(
      snapshot.reconciliationIndexDestinationRoot,
      "Reconciliation destination root",
    );
    const checkpointRoot = canonicalExistingPath(checkpointPath, true);
    const externalFile = realpathSync(externalPath);
    const ledgerRoot = canonicalExistingPath(ledgerDestination, true);
    const indexRoot = canonicalExistingPath(indexDestination, true);
    assertDisjoint([checkpointRoot, externalFile, ledgerRoot, indexRoot]);
    assertEmptyPrivateRoot(ledgerRoot);
    assertEmptyPrivateRoot(indexRoot);

    const { manifest } = readCheckpointDocuments(checkpointRoot, externalFile);
    const sourceLedgerRoot = join(checkpointRoot, "ledger");
    const sourceIndexRoot = join(checkpointRoot, "reconciliation-index");
    const ledgerInventory = scanEvidenceRoot(
      sourceLedgerRoot,
      "ledger",
      manifest.ledger.root,
    );
    const indexInventory = scanEvidenceRoot(
      sourceIndexRoot,
      "reconciliation-index",
      manifest.reconciliation_index.root,
    );
    if (
      canonicalJson(ledgerInventory.summary) !== canonicalJson(manifest.ledger.root) ||
      canonicalJson(indexInventory.summary) !== canonicalJson(manifest.reconciliation_index.root)
    ) {
      fail("checkpoint-mismatch", "Evidence checkpoint changed before recovery copy");
    }
    copyInventory(sourceLedgerRoot, ledgerRoot, ledgerInventory);
    copyInventory(sourceIndexRoot, indexRoot, indexInventory);

    const ledger = PublicEvidenceLedger.open({
      rootDirectory: ledgerRoot,
      retentionDays: manifest.ledger.retention_days,
      ...(snapshot.now === undefined ? {} : { now: snapshot.now as () => Date }),
    });
    const reconciliationIndex = PublicEvidenceReconciliationIndex.open({
      rootDirectory: indexRoot,
      ledger,
      ...(snapshot.now === undefined ? {} : { now: snapshot.now as () => Date }),
    });
    PublicEvidenceLedger.prototype.verify.call(ledger);
    PublicEvidenceReconciliationIndex.prototype.verify.call(reconciliationIndex);
    return verifyEvidenceRootsAgainstExternalCheckpoint({
      ledgerRootDirectory: ledgerRoot,
      reconciliationIndexRootDirectory: indexRoot,
      externalCheckpointFile: externalFile,
    });
  } catch (error) {
    if (error instanceof EvidenceCheckpointError) throw error;
    fail("io-failure", "Evidence checkpoint recovery failed closed");
  }
}
