import { createHash, timingSafeEqual } from "node:crypto";

const SHA256 = /^[0-9a-f]{64}$/u;
const BASE64URL = /^[A-Za-z0-9_-]+$/u;

export const CATALOGUE_CURSOR_VERSION = 1 as const;

export interface CatalogueCursorPayload {
  readonly content_root_sha256: string;
  readonly criteria_sha256: string;
  readonly offset: number;
  readonly v: typeof CATALOGUE_CURSOR_VERSION;
}

export interface CatalogueCursorBinding {
  readonly contentRootSha256: string;
  readonly criteriaSha256: string;
  readonly limit: number;
}

export class InvalidCatalogueCursorError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "InvalidCatalogueCursorError";
  }
}

/**
 * Serialise the bounded JSON values used for cursor criteria deterministically.
 *
 * The cursor payload itself contains only strings and integers. Supporting arrays
 * and plain objects here lets the application hash its semantic search criteria
 * without depending on property insertion order.
 */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value === "string" || typeof value === "boolean") {
    return JSON.stringify(value);
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new TypeError("Canonical JSON does not support non-finite numbers");
    }
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => canonicalJson(item)).join(",")}]`;
  }
  if (typeof value === "object") {
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) {
      throw new TypeError("Canonical JSON requires a plain object");
    }
    const object = value as Record<string, unknown>;
    const members = Object.keys(object)
      .sort()
      .map((key) => {
        const member = object[key];
        if (member === undefined) {
          throw new TypeError("Canonical JSON does not support undefined values");
        }
        return `${JSON.stringify(key)}:${canonicalJson(member)}`;
      });
    return `{${members.join(",")}}`;
  }
  throw new TypeError(`Canonical JSON does not support ${typeof value}`);
}

export function sha256CanonicalJson(value: unknown): string {
  return createHash("sha256").update(canonicalJson(value), "utf8").digest("hex");
}

function assertSha256(value: string, field: string): void {
  if (!SHA256.test(value)) {
    throw new TypeError(`${field} must be a lowercase SHA-256 digest`);
  }
}

function cursorPayload(
  binding: Omit<CatalogueCursorBinding, "limit">,
  offset: number,
): CatalogueCursorPayload {
  assertSha256(binding.contentRootSha256, "contentRootSha256");
  assertSha256(binding.criteriaSha256, "criteriaSha256");
  if (!Number.isSafeInteger(offset) || offset <= 0) {
    throw new TypeError("Cursor offset must be a positive safe integer");
  }
  return {
    content_root_sha256: binding.contentRootSha256,
    criteria_sha256: binding.criteriaSha256,
    offset,
    v: CATALOGUE_CURSOR_VERSION,
  };
}

/** Encode a page boundary as an opaque deterministic cursor. */
export function encodeCatalogueCursor(
  binding: Omit<CatalogueCursorBinding, "limit">,
  offset: number,
): string {
  const json = canonicalJson(cursorPayload(binding, offset));
  const body = Buffer.from(json, "utf8").toString("base64url");
  const digest = createHash("sha256").update(json, "utf8").digest("hex");
  return `${body}.${digest}`;
}

function invalid(message: string): never {
  throw new InvalidCatalogueCursorError(message);
}

function parsePayload(value: unknown, canonical: string): CatalogueCursorPayload {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    invalid("The cursor payload is not an object");
  }
  const object = value as Record<string, unknown>;
  const actualKeys = Object.keys(object).sort();
  const expectedKeys = ["content_root_sha256", "criteria_sha256", "offset", "v"];
  if (
    actualKeys.length !== expectedKeys.length ||
    actualKeys.some((key, index) => key !== expectedKeys[index])
  ) {
    invalid("The cursor payload has an unexpected shape");
  }
  if (canonicalJson(object) !== canonical) {
    invalid("The cursor payload is not canonical JSON");
  }
  if (object.v !== CATALOGUE_CURSOR_VERSION) {
    invalid("The cursor version is not supported");
  }
  if (typeof object.content_root_sha256 !== "string" || !SHA256.test(object.content_root_sha256)) {
    invalid("The cursor content root is invalid");
  }
  if (typeof object.criteria_sha256 !== "string" || !SHA256.test(object.criteria_sha256)) {
    invalid("The cursor criteria digest is invalid");
  }
  if (!Number.isSafeInteger(object.offset) || (object.offset as number) <= 0) {
    invalid("The cursor offset is invalid");
  }
  return {
    content_root_sha256: object.content_root_sha256,
    criteria_sha256: object.criteria_sha256,
    offset: object.offset as number,
    v: CATALOGUE_CURSOR_VERSION,
  };
}

/**
 * Decode and verify a cursor against the exact catalogue and semantic criteria.
 *
 * The digest is deliberately a corruption check rather than an authentication
 * mechanism. All payload fields are server-validated and the cursor conveys no
 * authority.
 */
export function decodeCatalogueCursor(token: string, binding: CatalogueCursorBinding): number {
  assertSha256(binding.contentRootSha256, "contentRootSha256");
  assertSha256(binding.criteriaSha256, "criteriaSha256");
  if (!Number.isSafeInteger(binding.limit) || binding.limit < 1 || binding.limit > 100) {
    throw new TypeError("Cursor page limit must be an integer from 1 to 100");
  }

  const parts = token.split(".");
  const body = parts[0];
  const suppliedDigest = parts[1];
  if (
    parts.length !== 2 ||
    body === undefined ||
    suppliedDigest === undefined ||
    !BASE64URL.test(body) ||
    !SHA256.test(suppliedDigest)
  ) {
    invalid("The cursor encoding is invalid");
  }

  let bytes: Buffer;
  let json: string;
  try {
    bytes = Buffer.from(body, "base64url");
    if (bytes.toString("base64url") !== body) {
      invalid("The cursor base64url encoding is not canonical");
    }
    json = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch (error) {
    if (error instanceof InvalidCatalogueCursorError) throw error;
    invalid("The cursor payload is not valid UTF-8");
  }

  const expectedDigest = createHash("sha256").update(bytes).digest();
  const actualDigest = Buffer.from(suppliedDigest, "hex");
  if (
    actualDigest.length !== expectedDigest.length ||
    !timingSafeEqual(actualDigest, expectedDigest)
  ) {
    invalid("The cursor corruption digest does not match");
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(json) as unknown;
  } catch {
    invalid("The cursor payload is not valid JSON");
  }
  const payload = parsePayload(parsed, json);
  if (payload.content_root_sha256 !== binding.contentRootSha256) {
    invalid("The cursor belongs to a different catalogue revision");
  }
  if (payload.criteria_sha256 !== binding.criteriaSha256) {
    invalid("The cursor belongs to different search criteria");
  }
  if (payload.offset % binding.limit !== 0) {
    invalid("The cursor offset is not aligned to the page size");
  }
  return payload.offset;
}
