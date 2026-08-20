import { createHash } from "node:crypto";
import {
  closeSync,
  constants,
  existsSync,
  fstatSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  readSync,
  readdirSync,
  writeSync,
  type Stats,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { types as utilTypes } from "node:util";

import { canonicalJson, canonicalJsonClone } from "./canonical-json.js";
import {
  CANONICAL_DOMAINS,
  contentAddress,
  domainSeparatedSha256,
  verifyContentAddress,
} from "./digest.js";
import {
  verifyInlineReceipt,
  verifyInlineReceiptStructure,
  type InlineEvidenceReceipt,
  type InlineReceiptVerificationMaterial,
} from "./receipt.js";
import {
  verifyPublicReadReceipt,
  verifyPublicReadReceiptStructure,
  type PublicReadEvidenceReceipt,
  type PublicReadReceiptVerificationMaterial,
} from "./public-read-receipt.js";

const LEDGER_PREFIX = "gis-ai-go:public-evidence-ledger";
const RECORD_PREFIX = "gis-ai-go:public-evidence-record";
const EVENT_PREFIX = "gis-ai-go:evidence-ledger-event";
const LEDGER_ID = /^gis-ai-go:public-evidence-ledger:sha256:[0-9a-f]{64}$/u;
const RECORD_ID = /^gis-ai-go:public-evidence-record:sha256:[0-9a-f]{64}$/u;
const EVENT_ID = /^gis-ai-go:evidence-ledger-event:sha256:[0-9a-f]{64}$/u;
const RECEIPT_ID = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const EVENT_FILE = /^(\d{16})-([0-9a-f]{64})\.json$/u;
const RECORD_FILE = /^([0-9a-f]{64})\.json$/u;
const MAX_DESCRIPTOR_BYTES = 16_384;
const MAX_EVENT_BYTES = 65_536;
const MAX_RECORD_BYTES = 4_194_304;
const MAX_EVENTS = 1_000_000;
const MIN_RETENTION_DAYS = 1;
const MAX_RETENTION_DAYS = 3_650;
const LEDGER_HEALTH_CHECKS = Object.freeze([
  "descriptor",
  "canonical-files",
  "content-identities",
  "event-sequence",
  "hash-chain",
  "receipt-boundary",
  "replay-keys",
  "retention",
  "privacy",
] as const);
const FORBIDDEN_PRIVATE_KEYS = new Set([
  "access_token",
  "credential",
  "credentials",
  "cursor",
  "geometry",
  "machine_path",
  "password",
  "prompt",
  "query",
  "raw_query",
  "rawquery",
  "secret",
  "token",
]);
const FORBIDDEN_PRIVATE_TEXT =
  /(?:^\/(?:Users|home)\/|^[A-Za-z]:\\Users\\|\bBearer\s+|-----BEGIN [^-]*PRIVATE KEY-----)/u;

export type PublicEvidenceLedgerErrorCode =
  | "collision"
  | "corruption"
  | "invalid-configuration"
  | "invalid-receipt"
  | "io-failure"
  | "replay"
  | "retention-mismatch"
  | "truncation";

export class PublicEvidenceLedgerError extends Error {
  public constructor(public readonly code: PublicEvidenceLedgerErrorCode, message: string) {
    super(message);
    this.name = "PublicEvidenceLedgerError";
  }
}

export interface PublicEvidenceLedgerDescriptorCore {
  readonly schema: "gis-ai-go.public-evidence-ledger.v1";
  readonly created_at: string;
  readonly retention_days: number;
  readonly scope: {
    readonly authority_profile: "anonymous-open";
    readonly publication_classification: "public";
    readonly access_tier: "open";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
    readonly permitted_operations: readonly ["evidence.inspect"];
  };
  readonly storage: {
    readonly model: "append-only-content-addressed-files";
    readonly overwrite: "forbidden";
    readonly attestation: "not-attested";
  };
}

export interface PublicEvidenceLedgerDescriptor extends PublicEvidenceLedgerDescriptorCore {
  readonly ledger_id: string;
}

export type PublicEvidenceReceipt = InlineEvidenceReceipt | PublicReadEvidenceReceipt;
export type PublicEvidenceReceiptVerificationMaterial =
  | InlineReceiptVerificationMaterial
  | PublicReadReceiptVerificationMaterial;

export interface PublicEvidenceRecordV1Core {
  readonly schema: "gis-ai-go.public-evidence-record.v1";
  readonly ledger_id: string;
  readonly persisted_at: string;
  readonly retain_until: string;
  readonly receipt: InlineEvidenceReceipt;
  readonly verification: {
    readonly receipt: "full-material-verified-at-ingest";
    readonly restart: "structure-and-content-verified";
    readonly attestation: "not-attested";
  };
  readonly privacy: {
    readonly raw_query: false;
    readonly prompt: false;
    readonly geometry: false;
    readonly credentials: false;
    readonly personal_data: false;
    readonly machine_path: false;
  };
}

export interface PublicEvidenceRecordV1 extends PublicEvidenceRecordV1Core {
  readonly record_id: string;
}

/**
 * A parallel record identity for public-read v2 receipts. The v1 record schema
 * and content-address domain remain byte-for-byte unchanged.
 */
export interface PublicEvidenceRecordV2Core {
  readonly schema: "gis-ai-go.public-evidence-record.v2";
  readonly ledger_id: string;
  readonly persisted_at: string;
  readonly retain_until: string;
  readonly receipt: PublicReadEvidenceReceipt;
  readonly verification: PublicEvidenceRecordV1Core["verification"];
  readonly privacy: PublicEvidenceRecordV1Core["privacy"];
}

export interface PublicEvidenceRecordV2 extends PublicEvidenceRecordV2Core {
  readonly record_id: string;
}

export type PublicEvidenceRecordCore =
  | PublicEvidenceRecordV1Core
  | PublicEvidenceRecordV2Core;
export type PublicEvidenceRecord = PublicEvidenceRecordV1 | PublicEvidenceRecordV2;

export interface PublicEvidenceLedgerEventCore {
  readonly schema: "gis-ai-go.evidence-ledger-event.v1";
  readonly ledger_id: string;
  readonly sequence: number;
  readonly event_type: "evidence.stored";
  readonly recorded_at: string;
  readonly previous_event_id: string | null;
  readonly record_id: string;
  readonly receipt_id: string;
  readonly replay_key_sha256: string;
  readonly retain_until: string;
}

export interface PublicEvidenceLedgerEvent extends PublicEvidenceLedgerEventCore {
  readonly event_id: string;
}

export interface PublicEvidenceStorageReference {
  readonly status: "persisted";
  readonly ledger_id: string;
  readonly record_id: string;
  readonly event_id: string;
  readonly persisted_at: string;
  readonly retain_until: string;
}

export interface StoredPublicEvidence {
  readonly record: PublicEvidenceRecord;
  readonly event: PublicEvidenceLedgerEvent;
  readonly reference: PublicEvidenceStorageReference;
}

export interface PublicEvidenceLedgerHealth {
  readonly status: "verified";
  readonly ledger_id: string;
  readonly event_count: number;
  readonly record_count: number;
  readonly last_event_id: string | null;
  readonly checks: readonly [
    "descriptor",
    "canonical-files",
    "content-identities",
    "event-sequence",
    "hash-chain",
    "receipt-boundary",
    "replay-keys",
    "retention",
    "privacy",
  ];
}

export interface OpenPublicEvidenceLedgerOptions {
  readonly rootDirectory: string;
  readonly retentionDays?: number;
  readonly now?: () => Date;
}

interface LedgerState {
  readonly recordsById: ReadonlyMap<string, PublicEvidenceRecord>;
  readonly eventsByRecordId: ReadonlyMap<string, PublicEvidenceLedgerEvent>;
  readonly eventsByReceiptId: ReadonlyMap<string, PublicEvidenceLedgerEvent>;
  readonly replayKeys: ReadonlySet<string>;
  readonly lastEvent: PublicEvidenceLedgerEvent | null;
}

function fail(code: PublicEvidenceLedgerErrorCode, message: string): never {
  throw new PublicEvidenceLedgerError(code, message);
}

function asRecord(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return fail("corruption", "Evidence storage contains a non-object document");
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  if (prototype !== Object.prototype && prototype !== null) {
    return fail("corruption", "Evidence storage contains a non-plain document");
  }
  return value as Record<string, unknown>;
}

function normaliseOpenOptions(value: unknown): OpenPublicEvidenceLedgerOptions {
  try {
    if (
      value === null ||
      typeof value !== "object" ||
      Array.isArray(value) ||
      utilTypes.isProxy(value) ||
      Object.getPrototypeOf(value) !== Object.prototype
    ) {
      return fail("invalid-configuration", "Evidence storage options must be a plain object");
    }
    const descriptors = Object.getOwnPropertyDescriptors(value);
    const keys = Reflect.ownKeys(value);
    if (
      keys.some((key) => typeof key !== "string") ||
      keys.some((key) => !["now", "retentionDays", "rootDirectory"].includes(key as string)) ||
      !("rootDirectory" in descriptors)
    ) {
      return fail("invalid-configuration", "Evidence storage options have an unexpected shape");
    }
    for (const descriptor of Object.values(descriptors)) {
      if (!("value" in descriptor) || descriptor.enumerable !== true) {
        return fail("invalid-configuration", "Evidence storage options must use data properties");
      }
    }
    return Object.freeze({
      rootDirectory: descriptors.rootDirectory?.value as string,
      ...(descriptors.retentionDays === undefined
        ? {}
        : { retentionDays: descriptors.retentionDays.value as number }),
      ...(descriptors.now === undefined ? {} : { now: descriptors.now.value as () => Date }),
    });
  } catch (error) {
    if (error instanceof PublicEvidenceLedgerError) throw error;
    return fail("invalid-configuration", "Evidence storage options could not be inspected");
  }
}

function assertExactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
  label: string,
): void {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    fail("corruption", `${label} has an unexpected shape`);
  }
}

function currentTimestamp(now: () => Date): string {
  const value = now();
  if (!(value instanceof Date) || !Number.isFinite(value.valueOf())) {
    return fail("invalid-configuration", "Evidence storage clock must return a valid Date");
  }
  return value.toISOString();
}

function assertTimestamp(value: unknown, label: string): asserts value is string {
  if (
    typeof value !== "string" ||
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u.test(value) ||
    !Number.isFinite(Date.parse(value))
  ) {
    fail("corruption", `${label} must be a canonical UTC timestamp`);
  }
}

function retainUntil(persistedAt: string, retentionDays: number): string {
  const value = new Date(persistedAt);
  value.setUTCDate(value.getUTCDate() + retentionDays);
  return value.toISOString();
}

function digestFromId(value: string): string {
  return value.slice(value.lastIndexOf(":") + 1);
}

function isGroupOrWorldWritable(mode: number): boolean {
  return process.platform !== "win32" && (mode & 0o022) !== 0;
}

function regularDirectory(path: string): void {
  try {
    const stat = lstatSync(path);
    if (
      !stat.isDirectory() ||
      stat.isSymbolicLink() ||
      isGroupOrWorldWritable(stat.mode)
    ) {
      fail(
        "corruption",
        "Evidence storage must use private real directories, not symbolic links",
      );
    }
  } catch (error) {
    if (error instanceof PublicEvidenceLedgerError) throw error;
    fail("io-failure", "Evidence storage directory could not be inspected");
  }
}

function regularFile(path: string, maximum: number): Stats {
  try {
    const stat = lstatSync(path);
    if (!stat.isFile() || stat.isSymbolicLink() || isGroupOrWorldWritable(stat.mode)) {
      fail("corruption", "Evidence storage contains a non-regular file");
    }
    if (stat.size < 2 || stat.size > maximum) {
      fail("truncation", "Evidence storage file is empty, truncated or over its bound");
    }
    return stat;
  } catch (error) {
    if (error instanceof PublicEvidenceLedgerError) throw error;
    fail("io-failure", "Evidence storage file could not be inspected");
  }
}

function sameFile(left: Stats, right: Stats): boolean {
  return (
    left.isFile() &&
    right.isFile() &&
    left.dev === right.dev &&
    left.ino === right.ino &&
    left.mode === right.mode &&
    left.size === right.size &&
    left.mtimeMs === right.mtimeMs &&
    left.ctimeMs === right.ctimeMs
  );
}

function readCanonicalDocument(path: string, maximum: number): unknown {
  const scanned = regularFile(path, maximum);
  let descriptor: number | undefined;
  let bytes: Buffer;
  try {
    descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    const before = fstatSync(descriptor);
    if (!sameFile(scanned, before)) {
      return fail("corruption", "Evidence storage changed while it was being inspected");
    }
    const capacity = scanned.size + 1;
    if (!Number.isSafeInteger(capacity) || capacity > maximum + 1) {
      return fail("truncation", "Evidence storage file exceeds its safe read bound");
    }
    const buffer = Buffer.allocUnsafe(capacity);
    let bytesRead = 0;
    while (bytesRead < buffer.length) {
      const count = readSync(
        descriptor,
        buffer,
        bytesRead,
        buffer.length - bytesRead,
        bytesRead,
      );
      if (count === 0) break;
      bytesRead += count;
    }
    const after = fstatSync(descriptor);
    if (!sameFile(scanned, after) || bytesRead !== scanned.size) {
      return fail("corruption", "Evidence storage changed while it was being read");
    }
    bytes = buffer.subarray(0, bytesRead);
  } catch (error) {
    if (error instanceof PublicEvidenceLedgerError) throw error;
    return fail("io-failure", "Evidence storage file could not be read");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // A completed read is verified below without disclosing the path.
      }
    }
  }
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    return fail("corruption", "Evidence storage file is not canonical UTF-8");
  }
  if (!Buffer.from(text, "utf8").equals(bytes)) {
    return fail("corruption", "Evidence storage file has a non-canonical byte encoding");
  }
  if (!text.endsWith("\n")) {
    return fail("truncation", "Evidence storage file is missing its complete record terminator");
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(text) as unknown;
  } catch {
    return fail("corruption", "Evidence storage file is not valid JSON");
  }
  let canonical: string;
  try {
    canonical = `${canonicalJson(parsed)}\n`;
  } catch {
    return fail("corruption", "Evidence storage file is outside canonical JSON");
  }
  if (canonical !== text) {
    return fail("corruption", "Evidence storage file is not in its unique canonical form");
  }
  return parsed;
}

function writeExclusiveCanonical(path: string, value: unknown): void {
  const bytes = Buffer.from(`${canonicalJson(value)}\n`, "utf8");
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, "wx", 0o600);
    const written = writeSync(descriptor, bytes, 0, bytes.length, null);
    if (written !== bytes.length) {
      fail("io-failure", "Evidence storage could not complete an immutable write");
    }
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
  } catch (error) {
    if (error instanceof PublicEvidenceLedgerError) throw error;
    const code = (error as NodeJS.ErrnoException).code;
    if (code === "EEXIST") {
      fail("collision", "Evidence storage refused to overwrite existing content");
    }
    fail("io-failure", "Evidence storage could not create immutable content");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The write and sync result remains authoritative; verification follows.
      }
    }
  }
  syncDirectory(dirname(path));
}

function syncDirectory(path: string): void {
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, "r");
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
  } catch {
    fail("io-failure", "Evidence storage could not synchronise an immutable directory entry");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The controlled failure above remains the client-safe outcome.
      }
    }
  }
}

function rawSha256(value: unknown): string {
  return createHash("sha256").update(canonicalJson(value), "utf8").digest("hex");
}

function assertPrivacy(value: unknown): void {
  if (typeof value === "string") {
    if (FORBIDDEN_PRIVATE_TEXT.test(value)) {
      fail("invalid-receipt", "Evidence receipt contains prohibited private material");
    }
    return;
  }
  if (value === null || typeof value !== "object") return;
  if (Array.isArray(value)) {
    value.forEach(assertPrivacy);
    return;
  }
  for (const [key, member] of Object.entries(asRecord(value))) {
    if (FORBIDDEN_PRIVATE_KEYS.has(key.toLowerCase())) {
      fail("invalid-receipt", "Evidence receipt contains a prohibited private field");
    }
    assertPrivacy(member);
  }
}

function descriptorCore(
  createdAt: string,
  retentionDays: number,
): PublicEvidenceLedgerDescriptorCore {
  return {
    schema: "gis-ai-go.public-evidence-ledger.v1",
    created_at: createdAt,
    retention_days: retentionDays,
    scope: {
      authority_profile: "anonymous-open",
      publication_classification: "public",
      access_tier: "open",
      contains_personal_data: false,
      contains_protected_data: false,
      permitted_operations: ["evidence.inspect"],
    },
    storage: {
      model: "append-only-content-addressed-files",
      overwrite: "forbidden",
      attestation: "not-attested",
    },
  };
}

function buildDescriptor(
  createdAt: string,
  retentionDays: number,
): PublicEvidenceLedgerDescriptor {
  const core = descriptorCore(createdAt, retentionDays);
  return canonicalJsonClone({
    ...core,
    ledger_id: contentAddress(
      LEDGER_PREFIX,
      CANONICAL_DOMAINS.evidenceLedgerDescriptor,
      core,
    ),
  });
}

function assertDescriptor(value: unknown): asserts value is PublicEvidenceLedgerDescriptor {
  const descriptor = asRecord(value);
  assertExactKeys(
    descriptor,
    ["created_at", "ledger_id", "retention_days", "schema", "scope", "storage"],
    "Evidence ledger descriptor",
  );
  assertTimestamp(descriptor.created_at, "Evidence ledger creation time");
  if (
    descriptor.schema !== "gis-ai-go.public-evidence-ledger.v1" ||
    typeof descriptor.ledger_id !== "string" ||
    !LEDGER_ID.test(descriptor.ledger_id) ||
    !Number.isInteger(descriptor.retention_days) ||
    (descriptor.retention_days as number) < MIN_RETENTION_DAYS ||
    (descriptor.retention_days as number) > MAX_RETENTION_DAYS
  ) {
    fail("corruption", "Evidence ledger descriptor constants are invalid");
  }
  const scope = asRecord(descriptor.scope);
  assertExactKeys(
    scope,
    [
      "access_tier",
      "authority_profile",
      "contains_personal_data",
      "contains_protected_data",
      "permitted_operations",
      "publication_classification",
    ],
    "Evidence ledger scope",
  );
  if (
    scope.authority_profile !== "anonymous-open" ||
    scope.publication_classification !== "public" ||
    scope.access_tier !== "open" ||
    scope.contains_personal_data !== false ||
    scope.contains_protected_data !== false ||
    !Array.isArray(scope.permitted_operations) ||
    scope.permitted_operations.length !== 1 ||
    scope.permitted_operations[0] !== "evidence.inspect"
  ) {
    fail("corruption", "Evidence ledger scope is not anonymous open public evidence");
  }
  const storage = asRecord(descriptor.storage);
  assertExactKeys(storage, ["attestation", "model", "overwrite"], "Evidence ledger storage");
  if (
    storage.model !== "append-only-content-addressed-files" ||
    storage.overwrite !== "forbidden" ||
    storage.attestation !== "not-attested"
  ) {
    fail("corruption", "Evidence ledger storage semantics are invalid");
  }
  const { ledger_id: identity, ...core } = descriptor;
  if (
    !verifyContentAddress(
      identity as string,
      LEDGER_PREFIX,
      CANONICAL_DOMAINS.evidenceLedgerDescriptor,
      core,
    )
  ) {
    fail("corruption", "Evidence ledger descriptor identity does not match its content");
  }
}

function replayKey(receipt: PublicEvidenceReceipt): string {
  return domainSeparatedSha256(CANONICAL_DOMAINS.evidenceReplayKey, {
    request_id: receipt.request_id,
    trace_id: receipt.trace_id,
    operation: receipt.operation.name,
    normalised_parameters_sha256: receipt.operation.normalised_parameters.sha256,
    result_sha256: receipt.result.sha256,
  });
}

function recordCore(
  descriptor: PublicEvidenceLedgerDescriptor,
  receipt: PublicEvidenceReceipt,
  persistedAt: string,
): PublicEvidenceRecordCore {
  const shared = {
    ledger_id: descriptor.ledger_id,
    persisted_at: persistedAt,
    retain_until: retainUntil(persistedAt, descriptor.retention_days),
    verification: {
      receipt: "full-material-verified-at-ingest",
      restart: "structure-and-content-verified",
      attestation: "not-attested",
    },
    privacy: {
      raw_query: false,
      prompt: false,
      geometry: false,
      credentials: false,
      personal_data: false,
      machine_path: false,
    },
  } as const;
  return receipt.schema === "gis-ai-go.evidence-receipt.v1"
    ? {
        ...shared,
        schema: "gis-ai-go.public-evidence-record.v1",
        receipt,
      }
    : {
        ...shared,
        schema: "gis-ai-go.public-evidence-record.v2",
        receipt,
      };
}

function buildRecord(
  descriptor: PublicEvidenceLedgerDescriptor,
  receipt: PublicEvidenceReceipt,
  persistedAt: string,
): PublicEvidenceRecord {
  const core = recordCore(descriptor, receipt, persistedAt);
  const domain =
    core.schema === "gis-ai-go.public-evidence-record.v1"
      ? CANONICAL_DOMAINS.publicEvidenceRecord
      : CANONICAL_DOMAINS.publicEvidenceRecordV2;
  return canonicalJsonClone({
    ...core,
    record_id: contentAddress(RECORD_PREFIX, domain, core),
  }) as PublicEvidenceRecord;
}

function assertRecord(
  value: unknown,
  descriptor: PublicEvidenceLedgerDescriptor,
): asserts value is PublicEvidenceRecord {
  const record = asRecord(value);
  assertExactKeys(
    record,
    [
      "ledger_id",
      "persisted_at",
      "privacy",
      "receipt",
      "record_id",
      "retain_until",
      "schema",
      "verification",
    ],
    "Public evidence record",
  );
  assertTimestamp(record.persisted_at, "Evidence persistence time");
  assertTimestamp(record.retain_until, "Evidence retention time");
  const v1Record = record.schema === "gis-ai-go.public-evidence-record.v1";
  const v2Record = record.schema === "gis-ai-go.public-evidence-record.v2";
  const receiptBoundaryValid =
    (v1Record && verifyInlineReceiptStructure(record.receipt)) ||
    (v2Record && verifyPublicReadReceiptStructure(record.receipt));
  if (
    (!v1Record && !v2Record) ||
    record.ledger_id !== descriptor.ledger_id ||
    typeof record.record_id !== "string" ||
    !RECORD_ID.test(record.record_id) ||
    record.retain_until !== retainUntil(record.persisted_at, descriptor.retention_days) ||
    !receiptBoundaryValid
  ) {
    fail("corruption", "Public evidence record constants or receipt boundary are invalid");
  }
  const verification = asRecord(record.verification);
  assertExactKeys(
    verification,
    ["attestation", "receipt", "restart"],
    "Evidence record verification",
  );
  if (
    verification.receipt !== "full-material-verified-at-ingest" ||
    verification.restart !== "structure-and-content-verified" ||
    verification.attestation !== "not-attested"
  ) {
    fail("corruption", "Evidence record verification claims are invalid");
  }
  const privacy = asRecord(record.privacy);
  assertExactKeys(
    privacy,
    ["credentials", "geometry", "machine_path", "personal_data", "prompt", "raw_query"],
    "Evidence record privacy",
  );
  if (Object.values(privacy).some((item) => item !== false)) {
    fail("corruption", "Evidence record privacy claims are invalid");
  }
  assertPrivacy(record.receipt);
  const { record_id: identity, ...core } = record;
  const domain = v1Record
    ? CANONICAL_DOMAINS.publicEvidenceRecord
    : CANONICAL_DOMAINS.publicEvidenceRecordV2;
  if (
    !verifyContentAddress(
      identity as string,
      RECORD_PREFIX,
      domain,
      core,
    )
  ) {
    fail("corruption", "Public evidence record identity does not match its content");
  }
}

function buildEvent(
  descriptor: PublicEvidenceLedgerDescriptor,
  record: PublicEvidenceRecord,
  sequence: number,
  previousEventId: string | null,
): PublicEvidenceLedgerEvent {
  const core: PublicEvidenceLedgerEventCore = {
    schema: "gis-ai-go.evidence-ledger-event.v1",
    ledger_id: descriptor.ledger_id,
    sequence,
    event_type: "evidence.stored",
    recorded_at: record.persisted_at,
    previous_event_id: previousEventId,
    record_id: record.record_id,
    receipt_id: record.receipt.receipt_id,
    replay_key_sha256: replayKey(record.receipt),
    retain_until: record.retain_until,
  };
  return canonicalJsonClone({
    ...core,
    event_id: contentAddress(EVENT_PREFIX, CANONICAL_DOMAINS.evidenceLedgerEvent, core),
  });
}

function assertEvent(
  value: unknown,
  descriptor: PublicEvidenceLedgerDescriptor,
  record: PublicEvidenceRecord,
  expectedSequence: number,
  previousEventId: string | null,
): asserts value is PublicEvidenceLedgerEvent {
  const event = asRecord(value);
  assertExactKeys(
    event,
    [
      "event_id",
      "event_type",
      "ledger_id",
      "previous_event_id",
      "receipt_id",
      "record_id",
      "recorded_at",
      "replay_key_sha256",
      "retain_until",
      "schema",
      "sequence",
    ],
    "Evidence ledger event",
  );
  assertTimestamp(event.recorded_at, "Evidence event time");
  assertTimestamp(event.retain_until, "Evidence event retention time");
  if (
    event.schema !== "gis-ai-go.evidence-ledger-event.v1" ||
    event.ledger_id !== descriptor.ledger_id ||
    event.sequence !== expectedSequence ||
    event.event_type !== "evidence.stored" ||
    event.recorded_at !== record.persisted_at ||
    event.previous_event_id !== previousEventId ||
    event.record_id !== record.record_id ||
    event.receipt_id !== record.receipt.receipt_id ||
    event.replay_key_sha256 !== replayKey(record.receipt) ||
    event.retain_until !== record.retain_until ||
    typeof event.event_id !== "string" ||
    !EVENT_ID.test(event.event_id) ||
    typeof event.replay_key_sha256 !== "string" ||
    !SHA256.test(event.replay_key_sha256)
  ) {
    fail("corruption", "Evidence ledger event does not match its sequence and record");
  }
  const { event_id: identity, ...core } = event;
  if (
    !verifyContentAddress(
      identity as string,
      EVENT_PREFIX,
      CANONICAL_DOMAINS.evidenceLedgerEvent,
      core,
    )
  ) {
    fail("corruption", "Evidence ledger event identity does not match its content");
  }
}

export class PublicEvidenceLedger {
  public readonly descriptor: PublicEvidenceLedgerDescriptor;
  readonly #root: string;
  readonly #recordsDirectory: string;
  readonly #eventsDirectory: string;
  readonly #now: () => Date;

  private constructor(
    root: string,
    descriptor: PublicEvidenceLedgerDescriptor,
    now: () => Date,
  ) {
    this.#root = root;
    this.#recordsDirectory = join(root, "records");
    this.#eventsDirectory = join(root, "events");
    this.descriptor = descriptor;
    this.#now = now;
  }

  public static open(options: OpenPublicEvidenceLedgerOptions): PublicEvidenceLedger {
    const snapshot = normaliseOpenOptions(options);
    if (
      typeof snapshot.rootDirectory !== "string" ||
      snapshot.rootDirectory.includes("\0") ||
      snapshot.rootDirectory.trim() === ""
    ) {
      fail("invalid-configuration", "Evidence storage requires a bounded root directory");
    }
    const retentionDays = snapshot.retentionDays ?? 365;
    if (
      !Number.isInteger(retentionDays) ||
      retentionDays < MIN_RETENTION_DAYS ||
      retentionDays > MAX_RETENTION_DAYS ||
      (snapshot.now !== undefined && typeof snapshot.now !== "function")
    ) {
      fail("invalid-configuration", "Evidence retention or clock configuration is invalid");
    }
    const root = resolve(snapshot.rootDirectory);
    const now = snapshot.now ?? (() => new Date());
    try {
      if (existsSync(root)) {
        regularDirectory(root);
        const existingEntries = readdirSync(root);
        if (
          existingEntries.some((name) => !["events", "ledger.json", "records"].includes(name))
        ) {
          fail("invalid-configuration", "Evidence storage root contains unrelated entries");
        }
      } else {
        mkdirSync(root, { recursive: true, mode: 0o700 });
        syncDirectory(dirname(root));
      }
      regularDirectory(root);
      const recordsDirectory = join(root, "records");
      const eventsDirectory = join(root, "events");
      if (!existsSync(recordsDirectory)) mkdirSync(recordsDirectory, { mode: 0o700 });
      if (!existsSync(eventsDirectory)) mkdirSync(eventsDirectory, { mode: 0o700 });
      syncDirectory(root);
      regularDirectory(recordsDirectory);
      regularDirectory(eventsDirectory);
    } catch (error) {
      if (error instanceof PublicEvidenceLedgerError) throw error;
      fail("io-failure", "Evidence storage directories could not be prepared");
    }

    const descriptorPath = join(root, "ledger.json");
    if (!existsSync(descriptorPath)) {
      writeExclusiveCanonical(
        descriptorPath,
        buildDescriptor(currentTimestamp(now), retentionDays),
      );
    }
    const descriptor = readCanonicalDocument(descriptorPath, MAX_DESCRIPTOR_BYTES);
    assertDescriptor(descriptor);
    if (descriptor.retention_days !== retentionDays) {
      fail("retention-mismatch", "Evidence retention cannot change for an existing ledger");
    }
    const ledger = new PublicEvidenceLedger(root, canonicalJsonClone(descriptor), now);
    ledger.verify();
    return ledger;
  }

  public verify(): PublicEvidenceLedgerHealth {
    regularDirectory(this.#root);
    regularDirectory(this.#recordsDirectory);
    regularDirectory(this.#eventsDirectory);
    let rootEntries: string[];
    try {
      rootEntries = readdirSync(this.#root).sort();
    } catch {
      return fail("io-failure", "Evidence storage root could not be enumerated");
    }
    if (
      rootEntries.length !== 3 ||
      rootEntries[0] !== "events" ||
      rootEntries[1] !== "ledger.json" ||
      rootEntries[2] !== "records"
    ) {
      fail("corruption", "Evidence storage root contains an unexpected entry");
    }
    const descriptor = readCanonicalDocument(join(this.#root, "ledger.json"), MAX_DESCRIPTOR_BYTES);
    assertDescriptor(descriptor);
    if (canonicalJson(descriptor) !== canonicalJson(this.descriptor)) {
      fail("corruption", "Evidence ledger descriptor changed after opening");
    }

    let eventNames: string[];
    let recordNames: string[];
    try {
      eventNames = readdirSync(this.#eventsDirectory).sort();
      recordNames = readdirSync(this.#recordsDirectory).sort();
    } catch {
      return fail("io-failure", "Evidence storage could not enumerate immutable content");
    }
    if (eventNames.length > MAX_EVENTS || recordNames.length > MAX_EVENTS) {
      fail("corruption", "Evidence storage exceeds its bounded event capacity");
    }
    if (eventNames.some((name) => !EVENT_FILE.test(name))) {
      fail("corruption", "Evidence event directory contains an unexpected entry");
    }
    if (recordNames.some((name) => !RECORD_FILE.test(name))) {
      fail("corruption", "Evidence record directory contains an unexpected entry");
    }

    const recordsById = new Map<string, PublicEvidenceRecord>();
    for (const name of recordNames) {
      const match = RECORD_FILE.exec(name);
      if (match === null) fail("corruption", "Evidence record name is invalid");
      const value = readCanonicalDocument(join(this.#recordsDirectory, name), MAX_RECORD_BYTES);
      assertRecord(value, this.descriptor);
      if (digestFromId(value.record_id) !== match[1]) {
        fail("collision", "Evidence record file name does not match its content identity");
      }
      if (recordsById.has(value.record_id)) {
        fail("collision", "Evidence storage contains a duplicate record identity");
      }
      recordsById.set(value.record_id, canonicalJsonClone(value));
    }

    const eventsByRecordId = new Map<string, PublicEvidenceLedgerEvent>();
    const eventsByReceiptId = new Map<string, PublicEvidenceLedgerEvent>();
    const replayKeys = new Set<string>();
    let previous: PublicEvidenceLedgerEvent | null = null;
    for (const [index, name] of eventNames.entries()) {
      const match = EVENT_FILE.exec(name);
      if (match === null) fail("corruption", "Evidence event name is invalid");
      const expectedSequence = index + 1;
      if (Number(match[1]) !== expectedSequence) {
        fail("truncation", "Evidence event sequence has a gap or reordered entry");
      }
      const value = readCanonicalDocument(join(this.#eventsDirectory, name), MAX_EVENT_BYTES);
      const recordValue = asRecord(value).record_id;
      if (typeof recordValue !== "string" || !RECORD_ID.test(recordValue)) {
        fail("corruption", "Evidence event has an invalid record identity");
      }
      const record = recordsById.get(recordValue);
      if (record === undefined) {
        fail("truncation", "Evidence event refers to a missing record");
      }
      assertEvent(
        value,
        this.descriptor,
        record,
        expectedSequence,
        previous?.event_id ?? null,
      );
      if (digestFromId(value.event_id) !== match[2]) {
        fail("collision", "Evidence event file name does not match its content identity");
      }
      if (
        eventsByRecordId.has(value.record_id) ||
        eventsByReceiptId.has(value.receipt_id) ||
        replayKeys.has(value.replay_key_sha256)
      ) {
        fail("replay", "Evidence storage contains a duplicate or replayed receipt");
      }
      eventsByRecordId.set(value.record_id, canonicalJsonClone(value));
      eventsByReceiptId.set(value.receipt_id, canonicalJsonClone(value));
      replayKeys.add(value.replay_key_sha256);
      previous = canonicalJsonClone(value);
    }
    if (recordsById.size !== eventsByRecordId.size) {
      fail("truncation", "Evidence storage contains an orphaned or unsequenced record");
    }

    return Object.freeze({
      status: "verified",
      ledger_id: this.descriptor.ledger_id,
      event_count: eventNames.length,
      record_count: recordNames.length,
      last_event_id: previous?.event_id ?? null,
      checks: LEDGER_HEALTH_CHECKS,
    });
  }

  public persistReceipt(
    receipt: PublicEvidenceReceipt,
    material: PublicEvidenceReceiptVerificationMaterial,
  ): StoredPublicEvidence {
    const health = this.verify();
    let receiptSnapshot: PublicEvidenceReceipt;
    let materialSnapshot: PublicEvidenceReceiptVerificationMaterial;
    try {
      receiptSnapshot = canonicalJsonClone(receipt) as PublicEvidenceReceipt;
      materialSnapshot = canonicalJsonClone(material) as PublicEvidenceReceiptVerificationMaterial;
    } catch {
      return fail("invalid-receipt", "Evidence storage rejected unsafe receipt material");
    }
    const v2Receipt = receiptSnapshot.schema === "gis-ai-go.evidence-receipt.v2";
    const verification = v2Receipt
      ? verifyPublicReadReceipt(
          receiptSnapshot,
          materialSnapshot as PublicReadReceiptVerificationMaterial,
        )
      : verifyInlineReceipt(
          receiptSnapshot,
          materialSnapshot as InlineReceiptVerificationMaterial,
        );
    const structureValid = v2Receipt
      ? verifyPublicReadReceiptStructure(receiptSnapshot)
      : verifyInlineReceiptStructure(receiptSnapshot);
    if (!verification.valid || !structureValid) {
      fail("invalid-receipt", "Evidence storage rejected an unverifiable public receipt");
    }
    assertPrivacy(receiptSnapshot);
    const state = this.#loadState();
    const key = replayKey(receiptSnapshot);
    if (
      state.replayKeys.has(key) ||
      state.eventsByReceiptId.has(receiptSnapshot.receipt_id)
    ) {
      fail("replay", "Evidence storage rejected a repeated evidence binding");
    }
    const persistedAt = currentTimestamp(this.#now);
    const record = buildRecord(this.descriptor, receiptSnapshot, persistedAt);
    const event = buildEvent(
      this.descriptor,
      record,
      health.event_count + 1,
      health.last_event_id,
    );
    writeExclusiveCanonical(
      join(this.#recordsDirectory, `${digestFromId(record.record_id)}.json`),
      record,
    );
    writeExclusiveCanonical(
      join(
        this.#eventsDirectory,
        `${String(event.sequence).padStart(16, "0")}-${digestFromId(event.event_id)}.json`,
      ),
      event,
    );
    this.verify();
    return canonicalJsonClone({
      record,
      event,
      reference: {
        status: "persisted",
        ledger_id: this.descriptor.ledger_id,
        record_id: record.record_id,
        event_id: event.event_id,
        persisted_at: record.persisted_at,
        retain_until: record.retain_until,
      },
    });
  }

  public inspect(identity: string): StoredPublicEvidence | null {
    if (!RECEIPT_ID.test(identity) && !RECORD_ID.test(identity)) {
      return null;
    }
    this.verify();
    const state = this.#loadState();
    const event = RECEIPT_ID.test(identity)
      ? state.eventsByReceiptId.get(identity)
      : state.eventsByRecordId.get(identity);
    if (event === undefined) return null;
    const record = state.recordsById.get(event.record_id);
    if (record === undefined) {
      fail("corruption", "Evidence inspection found a missing immutable record");
    }
    return canonicalJsonClone({
      record,
      event,
      reference: {
        status: "persisted",
        ledger_id: this.descriptor.ledger_id,
        record_id: record.record_id,
        event_id: event.event_id,
        persisted_at: record.persisted_at,
        retain_until: record.retain_until,
      },
    });
  }

  #loadState(): LedgerState {
    const recordsById = new Map<string, PublicEvidenceRecord>();
    const eventsByRecordId = new Map<string, PublicEvidenceLedgerEvent>();
    const eventsByReceiptId = new Map<string, PublicEvidenceLedgerEvent>();
    const replayKeys = new Set<string>();
    const recordNames = readdirSync(this.#recordsDirectory).sort();
    for (const name of recordNames) {
      const match = RECORD_FILE.exec(name);
      if (match === null) fail("corruption", "Evidence state record name is invalid");
      const record = readCanonicalDocument(
        join(this.#recordsDirectory, name),
        MAX_RECORD_BYTES,
      );
      assertRecord(record, this.descriptor);
      if (digestFromId(record.record_id) !== match[1] || recordsById.has(record.record_id)) {
        fail("collision", "Evidence state record identity is duplicated or misplaced");
      }
      recordsById.set(record.record_id, canonicalJsonClone(record));
    }
    let lastEvent: PublicEvidenceLedgerEvent | null = null;
    const eventNames = readdirSync(this.#eventsDirectory).sort();
    for (const [index, name] of eventNames.entries()) {
      const match = EVENT_FILE.exec(name);
      if (match === null || Number(match[1]) !== index + 1) {
        fail("truncation", "Evidence state event sequence is incomplete");
      }
      const event = readCanonicalDocument(join(this.#eventsDirectory, name), MAX_EVENT_BYTES);
      const eventRecord = asRecord(event);
      const record = recordsById.get(String(eventRecord.record_id));
      if (record === undefined) fail("corruption", "Evidence state has a missing record");
      assertEvent(
        event,
        this.descriptor,
        record,
        index + 1,
        lastEvent?.event_id ?? null,
      );
      if (
        digestFromId(event.event_id) !== match[2] ||
        eventsByRecordId.has(event.record_id) ||
        eventsByReceiptId.has(event.receipt_id) ||
        replayKeys.has(event.replay_key_sha256)
      ) {
        fail("replay", "Evidence state contains a duplicate or misplaced event");
      }
      eventsByRecordId.set(event.record_id, canonicalJsonClone(event));
      eventsByReceiptId.set(event.receipt_id, canonicalJsonClone(event));
      replayKeys.add(event.replay_key_sha256);
      lastEvent = canonicalJsonClone(event);
    }
    return {
      recordsById,
      eventsByRecordId,
      eventsByReceiptId,
      replayKeys,
      lastEvent,
    };
  }
}

/** Open or create a portable, append-only public evidence ledger. */
export function openPublicEvidenceLedger(
  options: OpenPublicEvidenceLedgerOptions,
): PublicEvidenceLedger {
  return PublicEvidenceLedger.open(options);
}

/** Raw canonical SHA-256 for independent file-byte comparisons in tests and tooling. */
export function publicEvidenceDocumentSha256(value: unknown): string {
  return rawSha256(value);
}
