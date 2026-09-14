import type { RequestId } from "@modelcontextprotocol/server";

export const MCP_REQUEST_ID_MAX_CODE_POINTS = 128;
export const MCP_RESOURCE_URI_MAX_CODE_POINTS = 2_048;

const MCP_REQUEST_ID_CONTROL_CHARACTER = /[\u0000-\u001f\u007f]/u;
const RAW_IDEMPOTENCY_KEY_TEXT = /gis-ai-go:ik:v1:[0-9a-f]{64}/u;
const NESTED_PERCENT_ESCAPE = /%(?:25)*([0-9a-f]{2})/giu;

function containsRawIdempotencyKeyAfterPercentDecoding(value: string): boolean {
  let candidate = value;
  for (let remaining = 32; remaining > 0; remaining -= 1) {
    if (RAW_IDEMPOTENCY_KEY_TEXT.test(candidate)) return true;
    const decoded = candidate.replace(
      NESTED_PERCENT_ESCAPE,
      (_escape, octet: string) => String.fromCharCode(Number.parseInt(octet, 16)),
    );
    if (decoded === candidate) return false;
    candidate = decoded;
  }
  return RAW_IDEMPOTENCY_KEY_TEXT.test(candidate);
}

/** Detect a raw reconciliation key in any caller-controlled MCP text field. */
export function containsRawIdempotencyKeyInMcpText(
  value: unknown,
): value is string {
  return (
    typeof value === "string" &&
    containsRawIdempotencyKeyAfterPercentDecoding(value)
  );
}

/** Shared HTTP/STDIO request-ID boundary applied before SDK dispatch. */
export function isBoundedMcpRequestId(value: unknown): value is RequestId {
  if (typeof value === "number") return Number.isSafeInteger(value);
  return (
    typeof value === "string" &&
    Array.from(value).length <= MCP_REQUEST_ID_MAX_CODE_POINTS &&
    !MCP_REQUEST_ID_CONTROL_CHARACTER.test(value) &&
    !containsRawIdempotencyKeyInMcpText(value)
  );
}

/** Shared bound applied before any MCP resource URI parsing or decoding. */
export function isBoundedMcpResourceUri(value: unknown): value is string {
  return (
    typeof value === "string" &&
    Array.from(value).length >= 1 &&
    Array.from(value).length <= MCP_RESOURCE_URI_MAX_CODE_POINTS &&
    !MCP_REQUEST_ID_CONTROL_CHARACTER.test(value)
  );
}

/**
 * Detect a raw reconciliation key in an MCP resource URI before SDK dispatch.
 * Valid percent escapes are decoded independently and repeatedly so malformed
 * unrelated escapes cannot conceal a raw, encoded or multiply encoded key.
 */
export function containsRawIdempotencyKeyInMcpResourceUri(
  value: unknown,
): value is string {
  if (!isBoundedMcpResourceUri(value)) return false;
  return containsRawIdempotencyKeyInMcpText(value);
}
