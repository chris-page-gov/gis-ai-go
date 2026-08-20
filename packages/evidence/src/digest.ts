import { createHash, timingSafeEqual } from "node:crypto";

import { canonicalJsonBytes } from "./canonical-json.js";

export const DOMAIN_SEPARATION_PREFIX = "GIS-AI-GO\u0000canonical-json\u0000sha256\u0000v1\u0000";

const DOMAIN_PATTERN = /^[a-z0-9](?:[a-z0-9.-]{0,126}[a-z0-9])?\.v[1-9][0-9]*$/u;
const CONTENT_ID_PREFIX_PATTERN = /^gis-ai-go:[a-z0-9]+(?:-[a-z0-9]+)*$/u;
const SHA256_PATTERN = /^[0-9a-f]{64}$/u;

export const CANONICAL_DOMAINS = Object.freeze({
  authorityContext: "gis-ai-go.public-authority-context.v1",
  catalogueParameters: "gis-ai-go.catalogue-parameters.v1",
  catalogueResultCore: "gis-ai-go.catalogue-result-core.v1",
  evidenceLedgerDescriptor: "gis-ai-go.public-evidence-ledger.v1",
  evidenceLedgerEvent: "gis-ai-go.evidence-ledger-event.v1",
  evidenceReplayKey: "gis-ai-go.evidence-replay-key.v1",
  evidenceReceipt: "gis-ai-go.evidence-receipt.v1",
  publicEvidenceRecord: "gis-ai-go.public-evidence-record.v1",
  executionParameters: "gis-ai-go.execution-parameters.v1",
  executionResultData: "gis-ai-go.execution-result-data.v1",
  providerAdapterResult: "gis-ai-go.provider-adapter-result.v1",
  publicPolicy: "gis-ai-go.public-policy.v1",
  publicPolicyDecision: "gis-ai-go.public-policy-decision.v1",
} as const);

export interface CanonicalDigest<D extends string = string> {
  readonly domain: D;
  readonly sha256: string;
}

function assertDomain(domain: string): void {
  if (!DOMAIN_PATTERN.test(domain)) {
    throw new TypeError(
      "Canonical digest domain must be a bounded lower-case ASCII name ending in a non-zero .v version",
    );
  }
}

function assertContentIdPrefix(prefix: string): void {
  if (!CONTENT_ID_PREFIX_PATTERN.test(prefix)) {
    throw new TypeError("Content identity prefix must be a lower-case gis-ai-go namespace");
  }
}

/** Hash canonical JSON in an unambiguous product/version/domain envelope. */
export function domainSeparatedSha256(domain: string, value: unknown): string {
  assertDomain(domain);
  return createHash("sha256")
    .update(DOMAIN_SEPARATION_PREFIX, "utf8")
    .update(domain, "utf8")
    .update("\u0000", "utf8")
    .update(canonicalJsonBytes(value))
    .digest("hex");
}

export function canonicalDigest<const D extends string>(
  domain: D,
  value: unknown,
): CanonicalDigest<D> {
  return Object.freeze({ domain, sha256: domainSeparatedSha256(domain, value) });
}

export function contentAddress(prefix: string, domain: string, value: unknown): string {
  assertContentIdPrefix(prefix);
  return `${prefix}:sha256:${domainSeparatedSha256(domain, value)}`;
}

export function verifyDomainSeparatedSha256(
  expectedSha256: string,
  domain: string,
  value: unknown,
): boolean {
  if (!SHA256_PATTERN.test(expectedSha256)) {
    return false;
  }
  const actual = domainSeparatedSha256(domain, value);
  return timingSafeEqual(Buffer.from(expectedSha256, "hex"), Buffer.from(actual, "hex"));
}

export function verifyContentAddress(
  expectedId: string,
  prefix: string,
  domain: string,
  value: unknown,
): boolean {
  assertContentIdPrefix(prefix);
  const marker = `${prefix}:sha256:`;
  if (!expectedId.startsWith(marker)) {
    return false;
  }
  return verifyDomainSeparatedSha256(expectedId.slice(marker.length), domain, value);
}
