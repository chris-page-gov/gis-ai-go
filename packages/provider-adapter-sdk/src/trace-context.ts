import { types as utilTypes } from "node:util";

import type { W3CTraceContext } from "./types.js";

const TRACEPARENT = /^00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}$/u;
const TRACESTATE_KEY = /^[a-z0-9][a-z0-9_\-*\/@]{0,255}$/u;
const ZERO_TRACE_ID = "0".repeat(32);
const ZERO_PARENT_ID = "0".repeat(16);

/** Repository input ceiling; W3C member syntax and counts remain authoritative within it. */
export const MAX_W3C_TRACESTATE_CHARACTERS = 512;

function isPlainDataObject(value: unknown): value is Record<string, unknown> {
  if (
    typeof value !== "object" ||
    value === null ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  if (prototype !== Object.prototype && prototype !== null) return false;
  let keys: readonly PropertyKey[];
  let descriptors: PropertyDescriptorMap;
  try {
    keys = Reflect.ownKeys(value);
    descriptors = Object.getOwnPropertyDescriptors(value);
  } catch {
    return false;
  }
  if (
    keys.some((key) => typeof key !== "string") ||
    keys.some((key) => key !== "traceparent" && key !== "tracestate") ||
    !Object.hasOwn(descriptors, "traceparent")
  ) {
    return false;
  }
  return Object.values(descriptors).every(
    (descriptor) => "value" in descriptor && descriptor.enumerable === true,
  );
}

function validTracestateValue(value: string): boolean {
  if (value.length < 1 || value.length > 256 || value.endsWith(" ")) return false;
  return [...value].every((character) => {
    const code = character.codePointAt(0) ?? 0;
    return (
      (code >= 0x20 && code <= 0x2b) ||
      (code >= 0x2d && code <= 0x3c) ||
      (code >= 0x3e && code <= 0x7e)
    );
  });
}

function validTracestate(value: string): boolean {
  const members = value.split(",");
  if (members.length < 1 || members.length > 32) return false;
  const keys = new Set<string>();
  for (const rawMember of members) {
    const member = rawMember.replace(/^[\t ]+|[\t ]+$/gu, "");
    if (member === "") continue;
    const separator = member.indexOf("=");
    if (separator < 1 || separator !== member.lastIndexOf("=")) return false;
    const key = member.slice(0, separator);
    const memberValue = member.slice(separator + 1);
    if (
      !TRACESTATE_KEY.test(key) ||
      !validTracestateValue(memberValue) ||
      keys.has(key)
    ) {
      return false;
    }
    keys.add(key);
  }
  return true;
}

/**
 * Validate and copy W3C Trace Context Level 2 at the
 * gateway-to-provider-adapter invocation boundary.
 *
 * Only version `00` traceparent values are accepted. Trace and parent identifiers
 * must be non-zero. All two-hex-digit flags and the Level 2 tracestate grammar are
 * accepted within the repository input ceiling. The returned object has no shared
 * caller-controlled container state.
 */
export function normaliseW3CTraceContext(
  value: unknown,
  expectedTraceId?: string,
): W3CTraceContext {
  if (!isPlainDataObject(value)) {
    throw new TypeError("Trace Context must be a closed plain data object");
  }
  const traceparent = value.traceparent;
  if (typeof traceparent !== "string") {
    throw new TypeError("traceparent is invalid");
  }
  const match = TRACEPARENT.exec(traceparent);
  if (
    match === null ||
    match[1] === ZERO_TRACE_ID ||
    match[2] === ZERO_PARENT_ID ||
    (expectedTraceId !== undefined && match[1] !== expectedTraceId)
  ) {
    throw new TypeError("traceparent is invalid");
  }
  if (value.tracestate !== undefined) {
    if (typeof value.tracestate !== "string") {
      throw new TypeError("tracestate is invalid");
    }
    if (value.tracestate.length > MAX_W3C_TRACESTATE_CHARACTERS) {
      throw new TypeError("tracestate exceeds the repository input ceiling");
    }
    if (!validTracestate(value.tracestate)) {
      throw new TypeError("tracestate is invalid");
    }
  }
  return Object.freeze({
    traceparent,
    ...(value.tracestate === undefined ? {} : { tracestate: value.tracestate }),
  });
}

/** Return the validated W3C trace identifier without retaining the input object. */
export function w3cTraceId(value: unknown): string {
  return normaliseW3CTraceContext(value).traceparent.slice(3, 35);
}
