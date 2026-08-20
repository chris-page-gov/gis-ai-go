export const CATALOGUE_PROBLEM_CODES = [
  "invalid_request",
  "invalid_cursor",
  "record_not_found",
  "evidence_not_found",
  "evidence_unavailable",
  "not_acceptable",
  "rate_limited",
  "complexity_limit_exceeded",
  "service_unavailable",
  "internal_error",
] as const;

export type CatalogueProblemCode = (typeof CATALOGUE_PROBLEM_CODES)[number];

export const CATALOGUE_PROBLEM_FIELD_CODES = [
  "required",
  "invalid_type",
  "invalid_value",
  "out_of_range",
  "not_unique",
  "unknown_property",
] as const;

export type CatalogueProblemFieldCode = (typeof CATALOGUE_PROBLEM_FIELD_CODES)[number];

export interface CatalogueProblemFieldError {
  readonly path: string;
  readonly code: CatalogueProblemFieldCode;
  readonly message: string;
}

export interface CatalogueProblem {
  readonly schema: "gis-ai-go.catalogue-problem.v1";
  readonly type: string;
  readonly title: string;
  readonly status: number;
  readonly code: CatalogueProblemCode;
  readonly detail?: string;
  readonly instance?: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly retry_after_seconds?: number;
  readonly errors?: readonly CatalogueProblemFieldError[];
}

export interface CatalogueProblemContext {
  readonly requestId: string;
  readonly traceId: string;
  readonly instance?: string;
}

export interface CatalogueProblemOptions {
  readonly detail?: string;
  readonly retryAfterSeconds?: number;
  readonly errors?: readonly CatalogueProblemFieldError[];
}

interface ProblemDefinition {
  readonly type: string;
  readonly title: string;
  readonly status: number;
}

const DEFINITIONS: Readonly<Record<CatalogueProblemCode, ProblemDefinition>> = Object.freeze({
  invalid_request: {
    type: "urn:gis-ai-go:problem:invalid-request",
    title: "Invalid request",
    status: 400,
  },
  invalid_cursor: {
    type: "urn:gis-ai-go:problem:invalid-cursor",
    title: "Invalid cursor",
    status: 400,
  },
  record_not_found: {
    type: "urn:gis-ai-go:problem:record-not-found",
    title: "Catalogue record not found",
    status: 404,
  },
  evidence_not_found: {
    type: "urn:gis-ai-go:problem:evidence-not-found",
    title: "Public evidence not found",
    status: 404,
  },
  evidence_unavailable: {
    type: "urn:gis-ai-go:problem:evidence-unavailable",
    title: "Public evidence unavailable",
    status: 503,
  },
  not_acceptable: {
    type: "urn:gis-ai-go:problem:not-acceptable",
    title: "Representation not acceptable",
    status: 406,
  },
  rate_limited: {
    type: "urn:gis-ai-go:problem:rate-limited",
    title: "Rate limit exceeded",
    status: 429,
  },
  complexity_limit_exceeded: {
    type: "urn:gis-ai-go:problem:complexity-limit-exceeded",
    title: "Complexity limit exceeded",
    status: 422,
  },
  service_unavailable: {
    type: "urn:gis-ai-go:problem:service-unavailable",
    title: "Service unavailable",
    status: 503,
  },
  internal_error: {
    type: "urn:gis-ai-go:problem:internal-error",
    title: "Internal error",
    status: 500,
  },
});

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const CONTROL_CHARACTER = /[\u0000-\u001f\u007f]/u;
const INSTANCE_PATH = /^\/(?:[A-Za-z0-9._~:/-]|%[0-9A-F]{2})*$/u;

function codePointLength(value: string): number {
  return Array.from(value).length;
}

function isBoundedText(
  value: unknown,
  minimum: number,
  maximum: number,
): value is string {
  return (
    typeof value === "string" &&
    codePointLength(value) >= minimum &&
    codePointLength(value) <= maximum &&
    !CONTROL_CHARACTER.test(value)
  );
}

function assertBoundedText(
  value: unknown,
  field: string,
  minimum: number,
  maximum: number,
): asserts value is string {
  if (!isBoundedText(value, minimum, maximum)) {
    throw new TypeError(
      `${field} must contain ${minimum} to ${maximum} Unicode characters without controls`,
    );
  }
}

/** Check the exact canonical path invariant used by catalogue problem instances. */
export function isCanonicalCatalogueProblemInstance(value: unknown): value is string {
  if (!isBoundedText(value, 1, 2_048)) return false;

  let canonicalPath: string;
  try {
    canonicalPath = decodeURIComponent(value)
      .split("/")
      .map((segment) => encodeURIComponent(segment).replaceAll("%3A", ":"))
      .join("/");
  } catch {
    return false;
  }
  return INSTANCE_PATH.test(value) && canonicalPath === value;
}

/** Validate the request and trace identity shared by success and problem envelopes. */
export function assertCatalogueProblemContext(context: CatalogueProblemContext): void {
  if (
    typeof context.requestId !== "string" ||
    codePointLength(context.requestId) > 128 ||
    !REQUEST_ID.test(context.requestId)
  ) {
    throw new TypeError("requestId does not match the catalogue problem contract");
  }
  if (typeof context.traceId !== "string" || !TRACE_ID.test(context.traceId)) {
    throw new TypeError("traceId must contain exactly 32 lowercase hexadecimal characters");
  }
  if (
    context.instance !== undefined &&
    !isCanonicalCatalogueProblemInstance(context.instance)
  ) {
    throw new TypeError(
      "instance must be a bounded canonical absolute path without a query or fragment",
    );
  }
}

function assertErrors(errors: readonly CatalogueProblemFieldError[]): void {
  if (!Array.isArray(errors) || errors.length < 1 || errors.length > 20) {
    throw new TypeError("errors must contain from 1 to 20 field errors");
  }
  const identities = new Set<string>();
  for (const [index, error] of errors.entries()) {
    if (typeof error !== "object" || error === null || Array.isArray(error)) {
      throw new TypeError(`errors[${index}] must be a field error object`);
    }
    const keys = Object.keys(error).sort();
    if (keys.length !== 3 || keys[0] !== "code" || keys[1] !== "message" || keys[2] !== "path") {
      throw new TypeError(`errors[${index}] has an unexpected shape`);
    }
    assertBoundedText(error.path, `errors[${index}].path`, 1, 256);
    assertBoundedText(error.message, `errors[${index}].message`, 1, 512);
    if (!(CATALOGUE_PROBLEM_FIELD_CODES as readonly unknown[]).includes(error.code)) {
      throw new TypeError(`errors[${index}].code is not controlled`);
    }
    const identity = JSON.stringify([error.path, error.code, error.message]);
    if (identities.has(identity)) {
      throw new TypeError("errors must be unique");
    }
    identities.add(identity);
  }
}

function assertOptions(options: CatalogueProblemOptions): void {
  if (options.detail !== undefined) {
    assertBoundedText(options.detail, "detail", 1, 1_024);
  }
  if (
    options.retryAfterSeconds !== undefined &&
    (!Number.isInteger(options.retryAfterSeconds) ||
      options.retryAfterSeconds < 1 ||
      options.retryAfterSeconds > 3_600)
  ) {
    throw new TypeError("retryAfterSeconds must be an integer from 1 to 3600");
  }
  if (options.errors !== undefined) {
    assertErrors(options.errors);
  }
}

function optionalFields(
  context: CatalogueProblemContext,
  options: CatalogueProblemOptions,
): Partial<CatalogueProblem> {
  return {
    ...(options.detail === undefined ? {} : { detail: options.detail }),
    ...(context.instance === undefined ? {} : { instance: context.instance }),
    ...(options.retryAfterSeconds === undefined
      ? {}
      : { retry_after_seconds: options.retryAfterSeconds }),
    ...(options.errors === undefined ? {} : { errors: options.errors }),
  };
}

/** Create the one RFC 9457-compatible problem shape used by every transport. */
export function createCatalogueProblem(
  code: CatalogueProblemCode,
  context: CatalogueProblemContext,
  options: CatalogueProblemOptions = {},
): CatalogueProblem {
  if (!(CATALOGUE_PROBLEM_CODES as readonly unknown[]).includes(code)) {
    throw new TypeError("code is not a controlled catalogue problem code");
  }
  assertCatalogueProblemContext(context);
  assertOptions(options);
  const definition = DEFINITIONS[code];
  return {
    schema: "gis-ai-go.catalogue-problem.v1",
    type: definition.type,
    title: definition.title,
    status: definition.status,
    code,
    request_id: context.requestId,
    trace_id: context.traceId,
    ...optionalFields(context, options),
  };
}

export class CatalogueProblemError extends Error {
  public readonly problem: CatalogueProblem;

  public constructor(problem: CatalogueProblem) {
    super(problem.detail ?? problem.title);
    this.name = "CatalogueProblemError";
    this.problem = problem;
  }
}

export function isCatalogueProblemError(error: unknown): error is CatalogueProblemError {
  return error instanceof CatalogueProblemError;
}

export function throwCatalogueProblem(
  code: CatalogueProblemCode,
  context: CatalogueProblemContext,
  options: CatalogueProblemOptions = {},
): never {
  throw new CatalogueProblemError(createCatalogueProblem(code, context, options));
}
