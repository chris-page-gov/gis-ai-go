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
  realpathSync,
  readdirSync,
  writeSync,
  type Stats,
} from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { types as utilTypes } from "node:util";

import { canonicalJson, canonicalJsonClone } from "./canonical-json.js";
import {
  CANONICAL_DOMAINS,
  contentAddress,
  domainSeparatedSha256,
  verifyContentAddress,
} from "./digest.js";
import {
  PublicEvidenceLedger,
  type PublicEvidenceLedgerDescriptor,
  type StoredPublicEvidence,
} from "./public-ledger.js";
import {
  verifyPublicReadReceiptStructure,
  type PublicReadEvidenceReceipt,
} from "./public-read-receipt.js";
import { evidenceReconciliationClaimAdmissionLimit } from "./reconciliation-index-capacity.js";

const INDEX_PREFIX = "gis-ai-go:evidence-reconciliation-index";
const CLAIM_PREFIX = "gis-ai-go:evidence-reconciliation-claim";
const RESOLUTION_PREFIX = "gis-ai-go:evidence-reconciliation-resolution";
const INDEX_ID = /^gis-ai-go:evidence-reconciliation-index:sha256:[0-9a-f]{64}$/u;
const CLAIM_ID = /^gis-ai-go:evidence-reconciliation-claim:sha256:[0-9a-f]{64}$/u;
const RESOLUTION_ID =
  /^gis-ai-go:evidence-reconciliation-resolution:sha256:[0-9a-f]{64}$/u;
const RECEIPT_ID = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const RESOURCE_ID = /^gis-ai-go:public-read-resource:sha256:[0-9a-f]{64}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const DOCUMENT_FILE = /^([0-9a-f]{64})\.json$/u;
const MARKER_FILE = /^([0-9a-f]{64})$/u;
const MAX_DESCRIPTOR_BYTES = 16_384;
const MAX_CLAIM_BYTES = 32_768;
const MAX_RESOLUTION_BYTES = 16_384;
const MAX_DOCUMENTS = 1_000_000;
const MIN_RETENTION_DAYS = 1;
const MAX_RETENTION_DAYS = 3_650;
const ZERO_KEY = `gis-ai-go:ik:v1:${"0".repeat(64)}`;
const RAW_IDEMPOTENCY_KEY_TEXT = /gis-ai-go:ik:v1:[0-9a-f]{64}/u;
const PRIVATE_TEXT =
  /(?:^\/(?:Users|home)\/|^[A-Za-z]:\\Users\\|\bBearer\s+|-----BEGIN [^-]*PRIVATE KEY-----)/u;

/** A non-secret, caller-generated 256-bit correlation identity. */
export const PUBLIC_IDEMPOTENCY_KEY = /^gis-ai-go:ik:v1:[0-9a-f]{64}$/u;

export type EvidenceReconciliationIndexErrorCode =
  | "capacity"
  | "collision"
  | "conflict"
  | "corruption"
  | "invalid-configuration"
  | "invalid-input"
  | "io-failure"
  | "retention-mismatch"
  | "truncation";

export class EvidenceReconciliationIndexError extends Error {
  public constructor(
    public readonly code: EvidenceReconciliationIndexErrorCode,
    message: string,
  ) {
    super(message);
    this.name = "EvidenceReconciliationIndexError";
  }
}

export interface EvidenceReconciliationIndexDescriptorCore {
  readonly schema: "gis-ai-go.evidence-reconciliation-index.v1";
  readonly created_at: string;
  readonly ledger_id: string;
  readonly retention_days: number;
  readonly scope: {
    readonly authority_profile: "anonymous-open";
    readonly source_operations: readonly ["data.query"];
    readonly lookup_operation: "evidence.inspect";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
  };
  readonly storage: {
    readonly model: "exclusive-content-addressed-claims-and-resolutions";
    readonly overwrite: "forbidden";
    readonly raw_idempotency_key: "not-retained";
    readonly result_material: "not-retained";
    readonly attestation: "not-attested";
  };
}

export interface EvidenceReconciliationIndexDescriptor
  extends EvidenceReconciliationIndexDescriptorCore {
  readonly index_id: string;
}

export interface EvidenceReconciliationClaimCore {
  readonly schema: "gis-ai-go.evidence-reconciliation-claim.v1";
  readonly index_id: string;
  readonly ledger_id: string;
  readonly claimed_at: string;
  readonly retain_until: string;
  readonly operation: "data.query";
  readonly idempotency_key_sha256: string;
  readonly request_fingerprint_sha256: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly resource_id: string;
  readonly normalised_parameters: {
    readonly domain: "gis-ai-go.data-query-parameters.v1";
    readonly sha256: string;
  };
  readonly privacy: {
    readonly raw_idempotency_key: false;
    readonly raw_query: false;
    readonly result_material: false;
    readonly credentials: false;
    readonly personal_data: false;
    readonly machine_path: false;
  };
}

export interface EvidenceReconciliationClaim extends EvidenceReconciliationClaimCore {
  readonly claim_id: string;
}

export interface EvidenceReconciliationResolutionCore {
  readonly schema: "gis-ai-go.evidence-reconciliation-resolution.v1";
  readonly index_id: string;
  readonly ledger_id: string;
  readonly resolved_at: string;
  readonly retain_until: string;
  readonly claim_id: string;
  readonly idempotency_key_sha256: string;
  readonly request_fingerprint_sha256: string;
  readonly receipt_id: string;
}

export interface EvidenceReconciliationResolution
  extends EvidenceReconciliationResolutionCore {
  readonly resolution_id: string;
}

export interface EvidenceReconciliationClaimInput {
  readonly idempotencyKey: string;
  readonly operation: "data.query";
  readonly requestId: string;
  readonly traceId: string;
  readonly resourceId: string;
  readonly normalisedParametersSha256: string;
}

export interface OpenEvidenceReconciliationIndexOptions {
  readonly rootDirectory: string;
  readonly ledger: PublicEvidenceLedger;
  readonly now?: () => Date;
}

export interface EvidenceReconciliationIndexHealth {
  readonly status: "verified";
  readonly index_id: string;
  readonly ledger_id: string;
  readonly claim_count: number;
  readonly resolution_count: number;
  readonly completed_count: number;
  readonly pending_count: number;
  readonly checks: readonly [
    "descriptor",
    "canonical-files",
    "content-identities",
    "exclusive-key-bindings",
    "receipt-linkage",
    "retention",
    "privacy",
  ];
}

export type EvidenceReconciliationClaimOutcome =
  | {
      readonly status: "claimed";
      readonly claim: EvidenceReconciliationClaim;
    }
  | {
      readonly status: "pending";
      readonly claim?: EvidenceReconciliationClaim;
      readonly resolution?: EvidenceReconciliationResolution;
    }
  | {
      readonly status: "completed";
      readonly claim: EvidenceReconciliationClaim;
      readonly resolution: EvidenceReconciliationResolution;
      readonly stored: StoredPublicEvidence;
    };

export type EvidenceReconciliationLookup =
  | { readonly status: "not-found" }
  | {
      readonly status: "pending";
      readonly claim?: EvidenceReconciliationClaim;
      readonly resolution?: EvidenceReconciliationResolution;
    }
  | {
      readonly status: "completed";
      readonly claim: EvidenceReconciliationClaim;
      readonly resolution: EvidenceReconciliationResolution;
      readonly stored: StoredPublicEvidence;
    };

interface IndexState {
  readonly ownershipKeys: ReadonlySet<string>;
  readonly claimsByKey: ReadonlyMap<string, EvidenceReconciliationClaim>;
  readonly resolutionsByKey: ReadonlyMap<string, EvidenceReconciliationResolution>;
}

interface VerifiedIndexState {
  readonly state: IndexState;
  readonly health: EvidenceReconciliationIndexHealth;
  readonly storedByKey: ReadonlyMap<string, StoredPublicEvidence | null>;
}

function fail(code: EvidenceReconciliationIndexErrorCode, message: string): never {
  throw new EvidenceReconciliationIndexError(code, message);
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

function snapshotDataObject(
  value: unknown,
  expectedKeys: readonly string[],
  code: "invalid-configuration" | "invalid-input",
  label: string,
): Readonly<Record<string, unknown>> {
  try {
    if (!isPlainObject(value)) fail(code, `${label} must be a plain object`);
    const keys = Reflect.ownKeys(value);
    if (
      keys.some((key) => typeof key !== "string") ||
      keys.length !== expectedKeys.length ||
      [...(keys as string[])].sort().some(
        (key, index) => key !== [...expectedKeys].sort()[index],
      )
    ) {
      fail(code, `${label} has an unexpected shape`);
    }
    const descriptors = Object.getOwnPropertyDescriptors(value);
    const snapshot: Record<string, unknown> = {};
    for (const key of expectedKeys) {
      const descriptor = descriptors[key];
      if (descriptor === undefined || !("value" in descriptor) || !descriptor.enumerable) {
        fail(code, `${label} must use enumerable data properties`);
      }
      snapshot[key] = descriptor.value;
    }
    return Object.freeze(snapshot);
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    fail(code, `${label} could not be inspected safely`);
  }
}

function asRecord(value: unknown, label: string): Record<string, unknown> {
  if (!isPlainObject(value)) fail("corruption", `${label} must be a plain object`);
  return value;
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

function assertTimestamp(value: unknown, label: string): asserts value is string {
  if (
    typeof value !== "string" ||
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u.test(value) ||
    !Number.isFinite(Date.parse(value))
  ) {
    fail("corruption", `${label} must be a canonical UTC timestamp`);
  }
}

function currentTimestamp(now: () => Date): string {
  let value: unknown;
  try {
    value = now();
  } catch {
    return fail("invalid-configuration", "Reconciliation index clock failed");
  }
  if (!(value instanceof Date) || utilTypes.isProxy(value)) {
    return fail("invalid-configuration", "Reconciliation index clock must return a Date");
  }
  let milliseconds: number;
  try {
    milliseconds = Date.prototype.getTime.call(value);
  } catch {
    return fail("invalid-configuration", "Reconciliation index clock returned an invalid Date");
  }
  if (!Number.isFinite(milliseconds)) {
    return fail("invalid-configuration", "Reconciliation index clock returned an invalid Date");
  }
  return new Date(milliseconds).toISOString();
}

function retainUntil(timestamp: string, retentionDays: number): string {
  const value = new Date(timestamp);
  value.setUTCDate(value.getUTCDate() + retentionDays);
  return value.toISOString();
}

function hasExactPrivateMode(mode: number, expected: 0o600 | 0o700): boolean {
  return process.platform === "win32" || (mode & 0o777) === expected;
}

function regularDirectory(path: string): void {
  try {
    const stat = lstatSync(path);
    if (!stat.isDirectory() || stat.isSymbolicLink() || !hasExactPrivateMode(stat.mode, 0o700)) {
      fail("corruption", "Reconciliation storage must use private real directories");
    }
    if (realpathSync(path) !== path) {
      fail("corruption", "Reconciliation storage must not traverse symbolic links");
    }
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    fail("io-failure", "Reconciliation storage directory could not be inspected");
  }
}

function regularFile(path: string, maximum: number): Stats {
  try {
    const stat = lstatSync(path);
    if (!stat.isFile() || stat.isSymbolicLink() || !hasExactPrivateMode(stat.mode, 0o600)) {
      fail("corruption", "Reconciliation storage contains a non-private regular file");
    }
    if (stat.size < 2 || stat.size > maximum) {
      fail("truncation", "Reconciliation storage file is truncated or over its bound");
    }
    return stat;
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    fail("io-failure", "Reconciliation storage file could not be inspected");
  }
}

function regularMarker(path: string): void {
  try {
    const stat = lstatSync(path);
    if (
      !stat.isFile() ||
      stat.isSymbolicLink() ||
      !hasExactPrivateMode(stat.mode, 0o600) ||
      stat.size !== 0
    ) {
      fail("corruption", "Reconciliation storage contains an invalid publication marker");
    }
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    fail("io-failure", "Reconciliation publication marker could not be inspected");
  }
}

function assertRealDirectory(path: string, label: string): void {
  try {
    const stat = lstatSync(path);
    if (!stat.isDirectory() || stat.isSymbolicLink() || realpathSync(path) !== path) {
      fail("invalid-configuration", `${label} must be a real directory`);
    }
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    fail("invalid-configuration", `${label} could not be inspected`);
  }
}

function pathsOverlap(left: string, right: string): boolean {
  if (left === right) return true;
  const leftFromRight = relative(right, left);
  const rightFromLeft = relative(left, right);
  const below = (candidate: string): boolean =>
    candidate !== "" && candidate !== ".." && !candidate.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`) && !isAbsolute(candidate);
  return below(leftFromRight) || below(rightFromLeft);
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
      return fail("corruption", "Reconciliation storage changed during inspection");
    }
    const buffer = Buffer.allocUnsafe(scanned.size + 1);
    let bytesRead = 0;
    while (bytesRead < buffer.length) {
      const count = readSync(descriptor, buffer, bytesRead, buffer.length - bytesRead, bytesRead);
      if (count === 0) break;
      bytesRead += count;
    }
    const after = fstatSync(descriptor);
    if (!sameFile(scanned, after) || bytesRead !== scanned.size) {
      return fail("corruption", "Reconciliation storage changed while being read");
    }
    bytes = buffer.subarray(0, bytesRead);
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    return fail("io-failure", "Reconciliation storage file could not be read");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The verified read remains authoritative.
      }
    }
  }
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    return fail("corruption", "Reconciliation storage is not canonical UTF-8");
  }
  if (!Buffer.from(text, "utf8").equals(bytes) || !text.endsWith("\n")) {
    return fail("truncation", "Reconciliation storage is missing canonical complete bytes");
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(text) as unknown;
  } catch {
    return fail("corruption", "Reconciliation storage is not valid JSON");
  }
  let canonical: string;
  try {
    canonical = `${canonicalJson(parsed)}\n`;
  } catch {
    return fail("corruption", "Reconciliation storage is outside canonical JSON");
  }
  if (canonical !== text) fail("corruption", "Reconciliation storage is not canonical JSON");
  return parsed;
}

function syncDirectory(path: string): void {
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, "r");
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
  } catch {
    fail("io-failure", "Reconciliation storage could not synchronise a directory entry");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The controlled failure remains authoritative.
      }
    }
  }
}

/** Return true only when this call created and synchronised the immutable file. */
function writeExclusiveCanonical(path: string, value: unknown): boolean {
  const bytes = Buffer.from(`${canonicalJson(value)}\n`, "utf8");
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, "wx", 0o600);
    const written = writeSync(descriptor, bytes, 0, bytes.length, null);
    if (written !== bytes.length) fail("io-failure", "Reconciliation write was incomplete");
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
  } catch (error) {
    if (error instanceof EvidenceReconciliationIndexError) throw error;
    if ((error as NodeJS.ErrnoException).code === "EEXIST") return false;
    fail("io-failure", "Reconciliation storage could not create immutable content");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The controlled failure remains authoritative.
      }
    }
  }
  syncDirectory(dirname(path));
  return true;
}

/** Return true only when this call created and durably published an empty marker. */
function writeExclusiveMarker(path: string): boolean {
  let descriptor: number | undefined;
  try {
    descriptor = openSync(path, "wx", 0o600);
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "EEXIST") return false;
    fail("io-failure", "Reconciliation storage could not create a publication marker");
  } finally {
    if (descriptor !== undefined) {
      try {
        closeSync(descriptor);
      } catch {
        // The controlled failure remains authoritative.
      }
    }
  }
  syncDirectory(dirname(path));
  return true;
}

function assertPublicIdempotencyKey(value: unknown): asserts value is string {
  if (typeof value !== "string" || !PUBLIC_IDEMPOTENCY_KEY.test(value) || value === ZERO_KEY) {
    fail("invalid-input", "Idempotency key must be one non-zero 256-bit public identity");
  }
}

export function publicIdempotencyKeySha256(
  idempotencyKey: string,
  operation: "data.query" = "data.query",
): string {
  assertPublicIdempotencyKey(idempotencyKey);
  if (operation !== "data.query") fail("invalid-input", "Idempotency operation is unsupported");
  return domainSeparatedSha256(CANONICAL_DOMAINS.idempotencyKey, {
    operation,
    key: idempotencyKey,
  });
}

function snapshotClaimInput(value: unknown): EvidenceReconciliationClaimInput {
  const expected = [
    "idempotencyKey",
    "normalisedParametersSha256",
    "operation",
    "requestId",
    "resourceId",
    "traceId",
  ] as const;
  const snapshot = snapshotDataObject(
    value,
    expected,
    "invalid-input",
    "Reconciliation claim",
  );
  assertPublicIdempotencyKey(snapshot.idempotencyKey);
  if (
    snapshot.operation !== "data.query" ||
    typeof snapshot.requestId !== "string" ||
    !REQUEST_ID.test(snapshot.requestId) ||
    typeof snapshot.traceId !== "string" ||
    !TRACE_ID.test(snapshot.traceId) ||
    typeof snapshot.resourceId !== "string" ||
    !RESOURCE_ID.test(snapshot.resourceId) ||
    typeof snapshot.normalisedParametersSha256 !== "string" ||
    !SHA256.test(snapshot.normalisedParametersSha256)
  ) {
    fail("invalid-input", "Reconciliation claim identifiers are invalid");
  }
  if (
    RAW_IDEMPOTENCY_KEY_TEXT.test(snapshot.requestId) ||
    PRIVATE_TEXT.test(snapshot.requestId)
  ) {
    fail("invalid-input", "Reconciliation request identity contains prohibited material");
  }
  return Object.freeze({
    idempotencyKey: snapshot.idempotencyKey,
    operation: "data.query",
    requestId: snapshot.requestId,
    traceId: snapshot.traceId,
    resourceId: snapshot.resourceId,
    normalisedParametersSha256: snapshot.normalisedParametersSha256,
  });
}

export function evidenceReconciliationRequestFingerprint(
  value: Pick<
    EvidenceReconciliationClaimInput,
    "operation" | "resourceId" | "normalisedParametersSha256"
  >,
): string {
  const snapshot = snapshotDataObject(
    value,
    ["normalisedParametersSha256", "operation", "resourceId"],
    "invalid-input",
    "Reconciliation fingerprint material",
  );
  if (
    snapshot.operation !== "data.query" ||
    typeof snapshot.resourceId !== "string" ||
    !RESOURCE_ID.test(snapshot.resourceId) ||
    typeof snapshot.normalisedParametersSha256 !== "string" ||
    !SHA256.test(snapshot.normalisedParametersSha256)
  ) {
    fail("invalid-input", "Reconciliation fingerprint material is invalid");
  }
  return domainSeparatedSha256(CANONICAL_DOMAINS.idempotencyRequestFingerprint, {
    schema: "gis-ai-go.idempotency-request-fingerprint.v1",
    operation: "data.query",
    contract_version: "v1",
    authority_profile: "anonymous-open",
    resource_id: snapshot.resourceId,
    normalised_parameters: {
      domain: CANONICAL_DOMAINS.dataQueryParameters,
      sha256: snapshot.normalisedParametersSha256,
    },
  });
}

function descriptorCore(
  ledger: PublicEvidenceLedgerDescriptor,
  createdAt: string,
): EvidenceReconciliationIndexDescriptorCore {
  return {
    schema: "gis-ai-go.evidence-reconciliation-index.v1",
    created_at: createdAt,
    ledger_id: ledger.ledger_id,
    retention_days: ledger.retention_days,
    scope: {
      authority_profile: "anonymous-open",
      source_operations: ["data.query"],
      lookup_operation: "evidence.inspect",
      contains_personal_data: false,
      contains_protected_data: false,
    },
    storage: {
      model: "exclusive-content-addressed-claims-and-resolutions",
      overwrite: "forbidden",
      raw_idempotency_key: "not-retained",
      result_material: "not-retained",
      attestation: "not-attested",
    },
  };
}

function buildDescriptor(
  ledger: PublicEvidenceLedgerDescriptor,
  createdAt: string,
): EvidenceReconciliationIndexDescriptor {
  const core = descriptorCore(ledger, createdAt);
  return canonicalJsonClone({
    ...core,
    index_id: contentAddress(
      INDEX_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationIndex,
      core,
    ),
  });
}

function assertDescriptor(
  value: unknown,
  ledger: PublicEvidenceLedgerDescriptor,
): asserts value is EvidenceReconciliationIndexDescriptor {
  const descriptor = asRecord(value, "Reconciliation index descriptor");
  assertExactKeys(
    descriptor,
    ["created_at", "index_id", "ledger_id", "retention_days", "schema", "scope", "storage"],
    "Reconciliation index descriptor",
  );
  assertTimestamp(descriptor.created_at, "Reconciliation index creation time");
  if (
    descriptor.schema !== "gis-ai-go.evidence-reconciliation-index.v1" ||
    typeof descriptor.index_id !== "string" ||
    !INDEX_ID.test(descriptor.index_id) ||
    descriptor.ledger_id !== ledger.ledger_id ||
    descriptor.retention_days !== ledger.retention_days ||
    !Number.isInteger(descriptor.retention_days) ||
    (descriptor.retention_days as number) < MIN_RETENTION_DAYS ||
    (descriptor.retention_days as number) > MAX_RETENTION_DAYS
  ) {
    fail("corruption", "Reconciliation index descriptor constants are invalid");
  }
  const scope = asRecord(descriptor.scope, "Reconciliation index scope");
  assertExactKeys(
    scope,
    [
      "authority_profile",
      "contains_personal_data",
      "contains_protected_data",
      "lookup_operation",
      "source_operations",
    ],
    "Reconciliation index scope",
  );
  if (
    scope.authority_profile !== "anonymous-open" ||
    scope.contains_personal_data !== false ||
    scope.contains_protected_data !== false ||
    scope.lookup_operation !== "evidence.inspect" ||
    !Array.isArray(scope.source_operations) ||
    scope.source_operations.length !== 1 ||
    scope.source_operations[0] !== "data.query"
  ) {
    fail("corruption", "Reconciliation index scope is invalid");
  }
  const storage = asRecord(descriptor.storage, "Reconciliation index storage");
  assertExactKeys(
    storage,
    ["attestation", "model", "overwrite", "raw_idempotency_key", "result_material"],
    "Reconciliation index storage",
  );
  if (
    storage.model !== "exclusive-content-addressed-claims-and-resolutions" ||
    storage.overwrite !== "forbidden" ||
    storage.raw_idempotency_key !== "not-retained" ||
    storage.result_material !== "not-retained" ||
    storage.attestation !== "not-attested"
  ) {
    fail("corruption", "Reconciliation index storage semantics are invalid");
  }
  const { index_id: identity, ...core } = descriptor;
  if (
    !verifyContentAddress(
      identity as string,
      INDEX_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationIndex,
      core,
    )
  ) {
    fail("corruption", "Reconciliation index identity does not match its content");
  }
}

function assertPrivacy(value: unknown): void {
  if (typeof value === "string") {
    if (PRIVATE_TEXT.test(value) || RAW_IDEMPOTENCY_KEY_TEXT.test(value)) {
      fail("corruption", "Reconciliation storage contains private text");
    }
    return;
  }
  if (value === null || typeof value !== "object") return;
  if (Array.isArray(value)) {
    value.forEach(assertPrivacy);
    return;
  }
  for (const [key, child] of Object.entries(asRecord(value, "Reconciliation document"))) {
    if (["idempotency_key", "query", "result", "observation", "value"].includes(key)) {
      fail("corruption", "Reconciliation storage contains prohibited material");
    }
    assertPrivacy(child);
  }
}

function buildClaim(
  descriptor: EvidenceReconciliationIndexDescriptor,
  input: EvidenceReconciliationClaimInput,
  claimedAt: string,
): EvidenceReconciliationClaim {
  const core: EvidenceReconciliationClaimCore = {
    schema: "gis-ai-go.evidence-reconciliation-claim.v1",
    index_id: descriptor.index_id,
    ledger_id: descriptor.ledger_id,
    claimed_at: claimedAt,
    retain_until: retainUntil(claimedAt, descriptor.retention_days),
    operation: "data.query",
    idempotency_key_sha256: publicIdempotencyKeySha256(input.idempotencyKey),
    request_fingerprint_sha256: evidenceReconciliationRequestFingerprint({
      operation: input.operation,
      resourceId: input.resourceId,
      normalisedParametersSha256: input.normalisedParametersSha256,
    }),
    request_id: input.requestId,
    trace_id: input.traceId,
    resource_id: input.resourceId,
    normalised_parameters: {
      domain: CANONICAL_DOMAINS.dataQueryParameters,
      sha256: input.normalisedParametersSha256,
    },
    privacy: {
      raw_idempotency_key: false,
      raw_query: false,
      result_material: false,
      credentials: false,
      personal_data: false,
      machine_path: false,
    },
  };
  return canonicalJsonClone({
    ...core,
    claim_id: contentAddress(
      CLAIM_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationClaim,
      core,
    ),
  });
}

function assertClaim(
  value: unknown,
  descriptor: EvidenceReconciliationIndexDescriptor,
): asserts value is EvidenceReconciliationClaim {
  const claim = asRecord(value, "Reconciliation claim");
  assertExactKeys(
    claim,
    [
      "claim_id",
      "claimed_at",
      "idempotency_key_sha256",
      "index_id",
      "ledger_id",
      "normalised_parameters",
      "operation",
      "privacy",
      "request_fingerprint_sha256",
      "request_id",
      "resource_id",
      "retain_until",
      "schema",
      "trace_id",
    ],
    "Reconciliation claim",
  );
  assertTimestamp(claim.claimed_at, "Reconciliation claim time");
  assertTimestamp(claim.retain_until, "Reconciliation claim retention time");
  if (
    claim.schema !== "gis-ai-go.evidence-reconciliation-claim.v1" ||
    typeof claim.claim_id !== "string" ||
    !CLAIM_ID.test(claim.claim_id) ||
    claim.index_id !== descriptor.index_id ||
    claim.ledger_id !== descriptor.ledger_id ||
    claim.retain_until !== retainUntil(claim.claimed_at as string, descriptor.retention_days) ||
    claim.operation !== "data.query" ||
    typeof claim.idempotency_key_sha256 !== "string" ||
    !SHA256.test(claim.idempotency_key_sha256) ||
    typeof claim.request_fingerprint_sha256 !== "string" ||
    !SHA256.test(claim.request_fingerprint_sha256) ||
    typeof claim.request_id !== "string" ||
    !REQUEST_ID.test(claim.request_id) ||
    typeof claim.trace_id !== "string" ||
    !TRACE_ID.test(claim.trace_id) ||
    typeof claim.resource_id !== "string" ||
    !RESOURCE_ID.test(claim.resource_id)
  ) {
    fail("corruption", "Reconciliation claim constants are invalid");
  }
  const parameters = asRecord(claim.normalised_parameters, "Reconciliation parameters");
  assertExactKeys(parameters, ["domain", "sha256"], "Reconciliation parameters");
  if (
    parameters.domain !== CANONICAL_DOMAINS.dataQueryParameters ||
    typeof parameters.sha256 !== "string" ||
    !SHA256.test(parameters.sha256)
  ) {
    fail("corruption", "Reconciliation parameter digest is invalid");
  }
  const expectedFingerprint = evidenceReconciliationRequestFingerprint({
    operation: "data.query",
    resourceId: claim.resource_id as string,
    normalisedParametersSha256: parameters.sha256,
  });
  if (claim.request_fingerprint_sha256 !== expectedFingerprint) {
    fail("corruption", "Reconciliation request fingerprint is invalid");
  }
  const privacy = asRecord(claim.privacy, "Reconciliation privacy claims");
  assertExactKeys(
    privacy,
    [
      "credentials",
      "machine_path",
      "personal_data",
      "raw_idempotency_key",
      "raw_query",
      "result_material",
    ],
    "Reconciliation privacy claims",
  );
  if (Object.values(privacy).some((item) => item !== false)) {
    fail("corruption", "Reconciliation privacy claims are invalid");
  }
  assertPrivacy(claim);
  const { claim_id: identity, ...core } = claim;
  if (
    !verifyContentAddress(
      identity as string,
      CLAIM_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationClaim,
      core,
    )
  ) {
    fail("corruption", "Reconciliation claim identity does not match its content");
  }
}

function receiptMatchesClaim(
  receipt: PublicReadEvidenceReceipt,
  claim: EvidenceReconciliationClaim,
): boolean {
  return (
    receipt.operation.name === claim.operation &&
    receipt.request_id === claim.request_id &&
    receipt.trace_id === claim.trace_id &&
    receipt.resource.resource_id === claim.resource_id &&
    receipt.operation.normalised_parameters.domain === claim.normalised_parameters.domain &&
    receipt.operation.normalised_parameters.sha256 === claim.normalised_parameters.sha256
  );
}

function buildResolution(
  descriptor: EvidenceReconciliationIndexDescriptor,
  claim: EvidenceReconciliationClaim,
  receipt: PublicReadEvidenceReceipt,
  resolvedAt: string,
): EvidenceReconciliationResolution {
  const core: EvidenceReconciliationResolutionCore = {
    schema: "gis-ai-go.evidence-reconciliation-resolution.v1",
    index_id: descriptor.index_id,
    ledger_id: descriptor.ledger_id,
    resolved_at: resolvedAt,
    retain_until: claim.retain_until,
    claim_id: claim.claim_id,
    idempotency_key_sha256: claim.idempotency_key_sha256,
    request_fingerprint_sha256: claim.request_fingerprint_sha256,
    receipt_id: receipt.receipt_id,
  };
  return canonicalJsonClone({
    ...core,
    resolution_id: contentAddress(
      RESOLUTION_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationResolution,
      core,
    ),
  });
}

function assertResolution(
  value: unknown,
  descriptor: EvidenceReconciliationIndexDescriptor,
  claim: EvidenceReconciliationClaim,
): asserts value is EvidenceReconciliationResolution {
  const resolution = asRecord(value, "Reconciliation resolution");
  assertExactKeys(
    resolution,
    [
      "claim_id",
      "idempotency_key_sha256",
      "index_id",
      "ledger_id",
      "receipt_id",
      "request_fingerprint_sha256",
      "resolution_id",
      "resolved_at",
      "retain_until",
      "schema",
    ],
    "Reconciliation resolution",
  );
  assertTimestamp(resolution.resolved_at, "Reconciliation resolution time");
  assertTimestamp(resolution.retain_until, "Reconciliation resolution retention time");
  if (
    resolution.schema !== "gis-ai-go.evidence-reconciliation-resolution.v1" ||
    typeof resolution.resolution_id !== "string" ||
    !RESOLUTION_ID.test(resolution.resolution_id) ||
    resolution.index_id !== descriptor.index_id ||
    resolution.ledger_id !== descriptor.ledger_id ||
    resolution.claim_id !== claim.claim_id ||
    resolution.idempotency_key_sha256 !== claim.idempotency_key_sha256 ||
    resolution.request_fingerprint_sha256 !== claim.request_fingerprint_sha256 ||
    resolution.retain_until !== claim.retain_until ||
    typeof resolution.receipt_id !== "string" ||
    !RECEIPT_ID.test(resolution.receipt_id)
  ) {
    fail("corruption", "Reconciliation resolution constants are invalid");
  }
  assertPrivacy(resolution);
  const { resolution_id: identity, ...core } = resolution;
  if (
    !verifyContentAddress(
      identity as string,
      RESOLUTION_PREFIX,
      CANONICAL_DOMAINS.evidenceReconciliationResolution,
      core,
    )
  ) {
    fail("corruption", "Reconciliation resolution identity does not match its content");
  }
}

function normaliseOptions(value: unknown): OpenEvidenceReconciliationIndexOptions {
  if (!isPlainObject(value) || utilTypes.isProxy(value)) {
    fail("invalid-configuration", "Reconciliation index options must be a plain object");
  }
  let snapshot: Readonly<Record<string, unknown>>;
  const keys = Reflect.ownKeys(value);
  const allowed = ["ledger", "now", "rootDirectory"];
  if (
    keys.length < 2 ||
    keys.length > 3 ||
    keys.some((key) => typeof key !== "string" || !allowed.includes(key)) ||
    !keys.includes("ledger") ||
    !keys.includes("rootDirectory")
  ) {
    fail("invalid-configuration", "Reconciliation index options are invalid");
  }
  snapshot = snapshotDataObject(
    value,
    (keys as string[]).sort(),
    "invalid-configuration",
    "Reconciliation index options",
  );
  if (
    typeof snapshot.rootDirectory !== "string" ||
    snapshot.rootDirectory.length < 1 ||
    snapshot.rootDirectory.length > 4_096 ||
    snapshot.rootDirectory.includes("\0") ||
    snapshot.rootDirectory.trim() === "" ||
    RAW_IDEMPOTENCY_KEY_TEXT.test(snapshot.rootDirectory) ||
    !(snapshot.ledger instanceof PublicEvidenceLedger) ||
    utilTypes.isProxy(snapshot.ledger) ||
    (snapshot.now !== undefined && typeof snapshot.now !== "function")
  ) {
    fail("invalid-configuration", "Reconciliation index options are invalid");
  }
  return Object.freeze({
    rootDirectory: snapshot.rootDirectory,
    ledger: snapshot.ledger,
    ...(snapshot.now === undefined ? {} : { now: snapshot.now as () => Date }),
  });
}

export class PublicEvidenceReconciliationIndex {
  public readonly descriptor: EvidenceReconciliationIndexDescriptor;
  public readonly ledger: PublicEvidenceLedger;
  readonly #root: string;
  readonly #claimOwnershipDirectory: string;
  readonly #claimReadyDirectory: string;
  readonly #claimsDirectory: string;
  readonly #resolutionReadyDirectory: string;
  readonly #resolutionsDirectory: string;
  readonly #now: () => Date;
  readonly #maximumClaims: number;

  private constructor(
    root: string,
    ledger: PublicEvidenceLedger,
    descriptor: EvidenceReconciliationIndexDescriptor,
    now: () => Date,
    maximumClaims: number,
  ) {
    this.#root = root;
    this.#claimOwnershipDirectory = join(root, "claim-ownership");
    this.#claimReadyDirectory = join(root, "claim-ready");
    this.#claimsDirectory = join(root, "claims");
    this.#resolutionReadyDirectory = join(root, "resolution-ready");
    this.#resolutionsDirectory = join(root, "resolutions");
    this.ledger = ledger;
    this.descriptor = descriptor;
    this.#now = now;
    this.#maximumClaims = maximumClaims;
  }

  public static open(value: OpenEvidenceReconciliationIndexOptions): PublicEvidenceReconciliationIndex {
    const maximumClaims = evidenceReconciliationClaimAdmissionLimit(value);
    const options = normaliseOptions(value);
    options.ledger.verify();
    const root = resolve(options.rootDirectory);
    const ledgerRoot = options.ledger.storageRootDirectory();
    if (RAW_IDEMPOTENCY_KEY_TEXT.test(ledgerRoot)) {
      fail("invalid-configuration", "Evidence ledger root contains prohibited material");
    }
    const now = options.now ?? (() => new Date());
    try {
      assertRealDirectory(ledgerRoot, "Evidence ledger root");
      const ledgerRealRoot = realpathSync(ledgerRoot);
      if (existsSync(root)) {
        assertRealDirectory(root, "Reconciliation index root");
      } else {
        assertRealDirectory(dirname(root), "Reconciliation index parent");
      }
      const candidateRealRoot = existsSync(root)
        ? realpathSync(root)
        : join(realpathSync(dirname(root)), root.slice(dirname(root).length + 1));
      if (pathsOverlap(candidateRealRoot, ledgerRealRoot)) {
        fail(
          "invalid-configuration",
          "Evidence ledger and reconciliation index roots must be disjoint",
        );
      }
      if (!existsSync(root)) {
        mkdirSync(root, { mode: 0o700 });
        syncDirectory(dirname(root));
      }
      regularDirectory(root);
      const descriptorPath = join(root, "index.json");
      const directoryNames = [
        "claim-ownership",
        "claim-ready",
        "claims",
        "resolution-ready",
        "resolutions",
      ] as const;
      if (!existsSync(descriptorPath)) {
        const existing = readdirSync(root);
        if (existing.some((name) => !directoryNames.includes(name as never))) {
          fail("corruption", "Reconciliation storage is non-empty without a descriptor");
        }
        for (const name of directoryNames) {
          const path = join(root, name);
          if (!existsSync(path)) mkdirSync(path, { mode: 0o700 });
          regularDirectory(path);
        }
        syncDirectory(root);
        const descriptor = buildDescriptor(options.ledger.descriptor, currentTimestamp(now));
        if (!writeExclusiveCanonical(descriptorPath, descriptor)) {
          fail("collision", "Reconciliation descriptor already exists");
        }
      }
      for (const name of directoryNames) regularDirectory(join(root, name));
      const descriptor = readCanonicalDocument(descriptorPath, MAX_DESCRIPTOR_BYTES);
      assertDescriptor(descriptor, options.ledger.descriptor);
      const index = new PublicEvidenceReconciliationIndex(
        root,
        options.ledger,
        canonicalJsonClone(descriptor),
        now,
        maximumClaims,
      );
      index.verify();
      return index;
    } catch (error) {
      if (error instanceof EvidenceReconciliationIndexError) throw error;
      fail("io-failure", "Reconciliation index could not be opened");
    }
  }

  public verify(): EvidenceReconciliationIndexHealth {
    return this.#verifyState().health;
  }

  #verifyState(): VerifiedIndexState {
    regularDirectory(this.#root);
    regularDirectory(this.#claimOwnershipDirectory);
    regularDirectory(this.#claimReadyDirectory);
    regularDirectory(this.#claimsDirectory);
    regularDirectory(this.#resolutionReadyDirectory);
    regularDirectory(this.#resolutionsDirectory);
    let rootEntries: string[];
    try {
      rootEntries = readdirSync(this.#root).sort();
    } catch {
      return fail("io-failure", "Reconciliation storage root could not be enumerated");
    }
    if (
      rootEntries.length !== 6 ||
      rootEntries[0] !== "claim-ownership" ||
      rootEntries[1] !== "claim-ready" ||
      rootEntries[2] !== "claims" ||
      rootEntries[3] !== "index.json" ||
      rootEntries[4] !== "resolution-ready" ||
      rootEntries[5] !== "resolutions"
    ) {
      fail("corruption", "Reconciliation storage root contains an unexpected entry");
    }
    const descriptor = readCanonicalDocument(join(this.#root, "index.json"), MAX_DESCRIPTOR_BYTES);
    assertDescriptor(descriptor, this.ledger.descriptor);
    if (canonicalJson(descriptor) !== canonicalJson(this.descriptor)) {
      fail("corruption", "Reconciliation descriptor changed after opening");
    }
    const state = this.#loadState();
    const resolutionEntries = [...state.resolutionsByKey.entries()];
    const storedReceipts = this.ledger.inspectReceipts(
      resolutionEntries.map(([, resolution]) => resolution.receipt_id),
    );
    const storedByKey = new Map<string, StoredPublicEvidence | null>();
    let completedCount = 0;
    for (const [index, [key]] of resolutionEntries.entries()) {
      const claim = state.claimsByKey.get(key);
      if (claim === undefined) fail("truncation", "Reconciliation resolution has no claim");
      const stored = storedReceipts[index];
      if (stored === undefined) fail("corruption", "Evidence bulk inspection was incomplete");
      storedByKey.set(key, stored);
      if (stored !== null) {
        if (
          stored.record.schema !== "gis-ai-go.public-evidence-record.v2" ||
          !receiptMatchesClaim(stored.record.receipt, claim)
        ) {
          fail("corruption", "Reconciliation resolution does not match its durable receipt");
        }
        completedCount += 1;
      }
    }
    const health: EvidenceReconciliationIndexHealth = Object.freeze({
      status: "verified",
      index_id: this.descriptor.index_id,
      ledger_id: this.descriptor.ledger_id,
      claim_count: state.ownershipKeys.size,
      resolution_count: state.resolutionsByKey.size,
      completed_count: completedCount,
      pending_count: state.ownershipKeys.size - completedCount,
      checks: [
        "descriptor",
        "canonical-files",
        "content-identities",
        "exclusive-key-bindings",
        "receipt-linkage",
        "retention",
        "privacy",
      ] as const,
    });
    return Object.freeze({ state, health, storedByKey });
  }

  public claim(value: EvidenceReconciliationClaimInput): EvidenceReconciliationClaimOutcome {
    const input = snapshotClaimInput(value);
    const key = publicIdempotencyKeySha256(input.idempotencyKey, input.operation);
    const fingerprint = evidenceReconciliationRequestFingerprint({
      operation: input.operation,
      resourceId: input.resourceId,
      normalisedParametersSha256: input.normalisedParametersSha256,
    });
    let verified = this.#verifyState();
    let state = verified.state;
    const existing = state.claimsByKey.get(key);
    if (existing !== undefined) {
      return this.#existingClaim(existing, fingerprint, state, verified.storedByKey);
    }
    if (state.ownershipKeys.has(key)) return Object.freeze({ status: "pending" });
    if (state.ownershipKeys.size >= this.#maximumClaims) {
      fail("capacity", "Reconciliation index reached its fixed local claim limit");
    }

    const claim = buildClaim(this.descriptor, input, currentTimestamp(this.#now));
    assertPrivacy(claim);
    const owns = writeExclusiveMarker(join(this.#claimOwnershipDirectory, key));
    if (!owns) {
      verified = this.#verifyState();
      state = verified.state;
      const competing = state.claimsByKey.get(key);
      if (competing === undefined) return Object.freeze({ status: "pending" });
      return this.#existingClaim(competing, fingerprint, state, verified.storedByKey);
    }
    const created = writeExclusiveCanonical(join(this.#claimsDirectory, `${key}.json`), claim);
    if (!created) {
      fail("collision", "Reconciliation claim content existed before ownership publication");
    }
    if (!writeExclusiveMarker(join(this.#claimReadyDirectory, key))) {
      fail("collision", "Reconciliation claim publication marker already exists");
    }
    this.verify();
    return canonicalJsonClone({ status: "claimed", claim });
  }

  public resolve(
    claimValue: EvidenceReconciliationClaim,
    receiptValue: PublicReadEvidenceReceipt,
  ): EvidenceReconciliationResolution {
    const state = this.#verifyAndLoadState();
    let claim: EvidenceReconciliationClaim;
    let receipt: PublicReadEvidenceReceipt;
    try {
      claim = canonicalJsonClone(claimValue);
      receipt = canonicalJsonClone(receiptValue);
    } catch {
      return fail("invalid-input", "Reconciliation resolution input is unsafe");
    }
    assertClaim(claim, this.descriptor);
    if (!verifyPublicReadReceiptStructure(receipt) || !receiptMatchesClaim(receipt, claim)) {
      fail("invalid-input", "Reconciliation receipt does not match its claim");
    }
    const storedClaim = state.claimsByKey.get(claim.idempotency_key_sha256);
    if (storedClaim === undefined || canonicalJson(storedClaim) !== canonicalJson(claim)) {
      fail("conflict", "Reconciliation claim is not the accepted immutable claim");
    }
    const existing = state.resolutionsByKey.get(claim.idempotency_key_sha256);
    if (existing !== undefined) {
      if (existing.receipt_id !== receipt.receipt_id) {
        fail("conflict", "Reconciliation claim is already bound to another receipt");
      }
      return canonicalJsonClone(existing);
    }
    if (this.ledger.inspect(receipt.receipt_id) !== null) {
      fail(
        "conflict",
        "Reconciliation resolution must be published before ledger persistence",
      );
    }
    const resolution = buildResolution(
      this.descriptor,
      claim,
      receipt,
      currentTimestamp(this.#now),
    );
    const created = writeExclusiveCanonical(
      join(this.#resolutionsDirectory, `${claim.idempotency_key_sha256}.json`),
      resolution,
    );
    if (!created) {
      const competing = this.#verifyAndLoadState().resolutionsByKey.get(
        claim.idempotency_key_sha256,
      );
      if (competing === undefined) {
        fail("io-failure", "Reconciliation resolution publication is still pending");
      }
      if (competing.receipt_id !== receipt.receipt_id) {
        fail("conflict", "Reconciliation resolution collision is invalid");
      }
      return canonicalJsonClone(competing);
    }
    if (
      !writeExclusiveMarker(
        join(this.#resolutionReadyDirectory, claim.idempotency_key_sha256),
      )
    ) {
      fail("collision", "Reconciliation resolution publication marker already exists");
    }
    this.verify();
    return canonicalJsonClone(resolution);
  }

  public lookup(
    idempotencyKey: string,
    operation: "data.query" = "data.query",
  ): EvidenceReconciliationLookup {
    const key = publicIdempotencyKeySha256(idempotencyKey, operation);
    const verified = this.#verifyState();
    const state = verified.state;
    if (!state.ownershipKeys.has(key)) return Object.freeze({ status: "not-found" });
    const claim = state.claimsByKey.get(key);
    if (claim === undefined) return Object.freeze({ status: "pending" });
    const resolution = state.resolutionsByKey.get(key);
    if (resolution === undefined) {
      return canonicalJsonClone({ status: "pending", claim });
    }
    const stored = verified.storedByKey.get(key);
    if (stored === undefined) {
      fail("corruption", "Reconciliation lookup has no verified receipt state");
    }
    if (stored === null) {
      return canonicalJsonClone({ status: "pending", claim, resolution });
    }
    if (
      stored.record.schema !== "gis-ai-go.public-evidence-record.v2" ||
      !receiptMatchesClaim(stored.record.receipt, claim)
    ) {
      fail("corruption", "Reconciliation lookup does not match its durable receipt");
    }
    return canonicalJsonClone({ status: "completed", claim, resolution, stored });
  }

  #existingClaim(
    claim: EvidenceReconciliationClaim,
    fingerprint: string,
    state: IndexState,
    storedByKey: ReadonlyMap<string, StoredPublicEvidence | null>,
  ): EvidenceReconciliationClaimOutcome {
    if (claim.request_fingerprint_sha256 !== fingerprint) {
      fail("conflict", "Idempotency key is bound to another semantic request");
    }
    const resolution = state.resolutionsByKey.get(claim.idempotency_key_sha256);
    if (resolution === undefined) {
      return canonicalJsonClone({ status: "pending", claim });
    }
    const stored = storedByKey.get(claim.idempotency_key_sha256);
    if (stored === undefined) {
      fail("corruption", "Idempotency completion has no verified receipt state");
    }
    if (stored === null) {
      return canonicalJsonClone({ status: "pending", claim, resolution });
    }
    if (
      stored.record.schema !== "gis-ai-go.public-evidence-record.v2" ||
      !receiptMatchesClaim(stored.record.receipt, claim)
    ) {
      fail("corruption", "Idempotency completion does not match its durable receipt");
    }
    return canonicalJsonClone({ status: "completed", claim, resolution, stored });
  }

  #verifyAndLoadState(): IndexState {
    return this.#verifyState().state;
  }

  #loadState(): IndexState {
    let ownershipNames: string[];
    let claimReadyNames: string[];
    let claimNames: string[];
    let resolutionReadyNames: string[];
    let resolutionNames: string[];
    try {
      ownershipNames = readdirSync(this.#claimOwnershipDirectory).sort();
      claimReadyNames = readdirSync(this.#claimReadyDirectory).sort();
      claimNames = readdirSync(this.#claimsDirectory).sort();
      resolutionReadyNames = readdirSync(this.#resolutionReadyDirectory).sort();
      resolutionNames = readdirSync(this.#resolutionsDirectory).sort();
    } catch {
      return fail("io-failure", "Reconciliation storage could not be enumerated");
    }
    if (
      ownershipNames.length > MAX_DOCUMENTS ||
      claimReadyNames.length > MAX_DOCUMENTS ||
      claimNames.length > MAX_DOCUMENTS ||
      resolutionReadyNames.length > MAX_DOCUMENTS ||
      resolutionNames.length > MAX_DOCUMENTS
    ) {
      fail("corruption", "Reconciliation storage exceeds its bounded capacity");
    }
    if (ownershipNames.some((name) => !MARKER_FILE.test(name))) {
      fail("corruption", "Reconciliation ownership contains an unexpected entry");
    }
    if (claimReadyNames.some((name) => !MARKER_FILE.test(name))) {
      fail("corruption", "Reconciliation claim publication contains an unexpected entry");
    }
    if (claimNames.some((name) => !DOCUMENT_FILE.test(name))) {
      fail("corruption", "Reconciliation claims contain an unexpected entry");
    }
    if (resolutionNames.some((name) => !DOCUMENT_FILE.test(name))) {
      fail("corruption", "Reconciliation resolutions contain an unexpected entry");
    }
    if (resolutionReadyNames.some((name) => !MARKER_FILE.test(name))) {
      fail("corruption", "Reconciliation resolution publication contains an unexpected entry");
    }
    for (const name of ownershipNames) {
      regularMarker(join(this.#claimOwnershipDirectory, name));
    }
    for (const name of claimReadyNames) regularMarker(join(this.#claimReadyDirectory, name));
    for (const name of resolutionReadyNames) {
      regularMarker(join(this.#resolutionReadyDirectory, name));
    }
    const ownershipKeys = new Set(ownershipNames);
    const claimReadyKeys = new Set(claimReadyNames);
    const resolutionReadyKeys = new Set(resolutionReadyNames);
    const claimDocuments = new Set(
      claimNames.map((name) => {
        const match = DOCUMENT_FILE.exec(name);
        if (match?.[1] === undefined) fail("corruption", "Reconciliation claim filename is invalid");
        return match[1];
      }),
    );
    const resolutionDocuments = new Set(
      resolutionNames.map((name) => {
        const match = DOCUMENT_FILE.exec(name);
        if (match?.[1] === undefined) {
          fail("corruption", "Reconciliation resolution filename is invalid");
        }
        return match[1];
      }),
    );
    for (const key of claimDocuments) {
      if (!ownershipKeys.has(key)) fail("corruption", "Reconciliation claim has no owner");
    }
    for (const key of claimReadyKeys) {
      if (!ownershipKeys.has(key) || !claimDocuments.has(key)) {
        fail("truncation", "Published reconciliation claim is incomplete");
      }
    }
    for (const key of resolutionDocuments) {
      if (!claimReadyKeys.has(key)) {
        fail("corruption", "Reconciliation resolution has no published claim");
      }
    }
    for (const key of resolutionReadyKeys) {
      if (!resolutionDocuments.has(key)) {
        fail("truncation", "Published reconciliation resolution is incomplete");
      }
    }
    const claimsByKey = new Map<string, EvidenceReconciliationClaim>();
    for (const key of claimReadyKeys) {
      const name = `${key}.json`;
      const value = readCanonicalDocument(join(this.#claimsDirectory, name), MAX_CLAIM_BYTES);
      assertClaim(value, this.descriptor);
      if (value.idempotency_key_sha256 !== key || claimsByKey.has(key)) {
        fail("collision", "Reconciliation claim is duplicated or misplaced");
      }
      claimsByKey.set(key, canonicalJsonClone(value));
    }
    const resolutionsByKey = new Map<string, EvidenceReconciliationResolution>();
    for (const key of resolutionReadyKeys) {
      const name = `${key}.json`;
      const claim = claimsByKey.get(key);
      if (claim === undefined) fail("truncation", "Reconciliation resolution has no claim");
      const value = readCanonicalDocument(
        join(this.#resolutionsDirectory, name),
        MAX_RESOLUTION_BYTES,
      );
      assertResolution(value, this.descriptor, claim);
      if (value.idempotency_key_sha256 !== key || resolutionsByKey.has(key)) {
        fail("collision", "Reconciliation resolution is duplicated or misplaced");
      }
      resolutionsByKey.set(key, canonicalJsonClone(value));
    }
    return Object.freeze({ ownershipKeys, claimsByKey, resolutionsByKey });
  }
}

export function openEvidenceReconciliationIndex(
  options: OpenEvidenceReconciliationIndexOptions,
): PublicEvidenceReconciliationIndex {
  return PublicEvidenceReconciliationIndex.open(options);
}
