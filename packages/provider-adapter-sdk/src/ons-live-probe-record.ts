import { canonicalJsonClone } from "@gis-ai-go/evidence";

import {
  ONS_ADAPTER_ID,
  ONS_ADAPTER_VERSION,
  ONS_DATASET_ID,
  ONS_EDITION,
  ONS_EGRESS_POLICY,
  ONS_ORIGIN,
  ONS_PROVIDER_ID,
  ONS_VERSION,
  ONS_VERSION_PATH,
  type OnsAttemptTelemetry,
} from "./ons-data-api.js";
import {
  digestProviderAdapterResult,
  serialiseProviderAdapterResult,
} from "./synthetic-fixture.js";
import type {
  AdapterDescription,
  ProviderAdapterResult,
  ProviderRights,
} from "./types.js";

const MAX_DURATION_MS = 20_000;
const MAX_CANONICAL_BYTES = 262_144;
const ONS_VERSION_URI = `${ONS_ORIGIN}${ONS_VERSION_PATH}`;
const UTC_DATE_TIME = new RegExp(
  "^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])" +
    "T(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d{3})?Z$",
  "u",
);

export interface OnsLiveProbeRecordInput {
  readonly observedAt: string;
  readonly durationMs: number;
  readonly description: AdapterDescription;
  readonly rights: ProviderRights;
  readonly result: ProviderAdapterResult;
  readonly attempts: readonly OnsAttemptTelemetry[];
}

function boundedNumber(
  value: number,
  minimum: number,
  maximum: number,
  label: string,
): void {
  if (!Number.isFinite(value) || value < minimum || value > maximum) {
    throw new TypeError(`${label} is outside the live-probe bound`);
  }
}

function boundedInteger(
  value: number,
  minimum: number,
  maximum: number,
  label: string,
): void {
  boundedNumber(value, minimum, maximum, label);
  if (!Number.isInteger(value)) throw new TypeError(`${label} must be an integer`);
}

function canonicalUtcDateTime(value: string, label: string): void {
  if (!UTC_DATE_TIME.test(value)) throw new TypeError(`${label} must be a UTC date-time string`);
  const parsed = Date.parse(value);
  const normalised = value.includes(".") ? value : value.replace("Z", ".000Z");
  if (!Number.isFinite(parsed) || new Date(parsed).toISOString() !== normalised) {
    throw new TypeError(`${label} must be a real UTC date-time`);
  }
}

function validateResponseAttempt(attempt: OnsAttemptTelemetry): void {
  if (attempt.outcome !== "response") return;
  boundedInteger(attempt.status, 100, 599, "attempt status");
  boundedInteger(
    attempt.compressedBytes,
    0,
    ONS_EGRESS_POLICY.maxCompressedBytes,
    "attempt compressedBytes",
  );
  boundedNumber(attempt.dnsMs, 0, ONS_EGRESS_POLICY.connectTimeoutMs, "attempt dnsMs");
  boundedInteger(attempt.resolvedAddressCount, 1, 64, "attempt resolvedAddressCount");
  if (attempt.selectedAddressFamily !== 4 && attempt.selectedAddressFamily !== 6) {
    throw new TypeError("attempt selectedAddressFamily is invalid");
  }
  boundedNumber(attempt.connectMs, 0, ONS_EGRESS_POLICY.connectTimeoutMs, "attempt connectMs");
  boundedNumber(attempt.responseMs, 0, ONS_EGRESS_POLICY.responseTimeoutMs, "attempt responseMs");
  boundedNumber(
    attempt.totalMs,
    0,
    ONS_EGRESS_POLICY.connectTimeoutMs + ONS_EGRESS_POLICY.responseTimeoutMs,
    "attempt totalMs",
  );
  for (const [label, value, maximum] of [
    ["attempt tlsProtocol", attempt.tlsProtocol, 32],
    ["attempt tlsCipher", attempt.tlsCipher, 128],
  ] as const) {
    if (value !== null && (value.length < 1 || value.length > maximum)) {
      throw new TypeError(`${label} is outside the live-probe bound`);
    }
  }
  if (attempt.status === 200) {
    if (attempt.decompressedBytes === null) {
      throw new TypeError("successful response telemetry must include decompressedBytes");
    }
    boundedInteger(
      attempt.decompressedBytes,
      0,
      ONS_EGRESS_POLICY.maxDecompressedBytes,
      "attempt decompressedBytes",
    );
  } else if (attempt.decompressedBytes !== null) {
    throw new TypeError("non-200 response telemetry must not invent decompressedBytes");
  }
}

function validateSuccessfulAttempts(attempts: readonly OnsAttemptTelemetry[]): void {
  if (attempts.length < 1 || attempts.length > ONS_EGRESS_POLICY.maxAttempts) {
    throw new TypeError("live-probe attempts are outside the provider bound");
  }
  attempts.forEach((attempt, index) => {
    if (attempt.attempt !== index + 1) {
      throw new TypeError("live-probe attempt numbers must be contiguous");
    }
    validateResponseAttempt(attempt);
  });

  const finalAttempt = attempts.at(-1);
  if (finalAttempt?.outcome !== "response" || finalAttempt.status !== 200) {
    throw new TypeError("a passed live probe must end with a successful response");
  }
  if (attempts.length === 2) {
    const firstAttempt = attempts[0]!;
    if (firstAttempt.outcome === "response") {
      if (!ONS_EGRESS_POLICY.retryableStatuses.includes(firstAttempt.status)) {
        throw new TypeError("a passed live probe may retain only a retryable response");
      }
    } else if (
      firstAttempt.code !== "PROVIDER_OUTAGE" &&
      firstAttempt.code !== "PROVIDER_TIMEOUT"
    ) {
      throw new TypeError("a passed live probe may retain only a retryable transport failure");
    }
  }
}

export function buildOnsLiveProbeRecord(input: OnsLiveProbeRecordInput) {
  if (
    input.description.adapterId !== ONS_ADAPTER_ID ||
    input.description.adapterVersion !== ONS_ADAPTER_VERSION ||
    input.description.providerVersion.providerId !== ONS_PROVIDER_ID ||
    input.description.providerVersion.datasetId !== ONS_DATASET_ID ||
    input.description.providerVersion.edition !== ONS_EDITION ||
    input.description.providerVersion.version !== ONS_VERSION ||
    input.description.providerVersion.versionUri !== ONS_VERSION_URI ||
    input.description.providerVersion.sourceDate !== "2026-07-01"
  ) {
    throw new TypeError("live-probe description is not the fixed ONS adapter");
  }
  if (
    input.rights.state !== "open-with-conditions" ||
    input.rights.licence !== "Open Government Licence v3.0" ||
    input.rights.licenceUri !==
      "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
  ) {
    throw new TypeError("live-probe rights are not the reviewed ONS rights");
  }
  if (
    input.result.provider.id !== ONS_PROVIDER_ID ||
    input.result.provider.adapterId !== ONS_ADAPTER_ID ||
    input.result.dataset.id !== ONS_DATASET_ID ||
    input.result.dataset.edition !== ONS_EDITION ||
    input.result.dataset.version !== ONS_VERSION ||
    input.result.dataset.versionUri !== ONS_VERSION_URI ||
    input.result.provenance.synthetic !== false
  ) {
    throw new TypeError("live-probe result is not the fixed ONS result");
  }
  canonicalUtcDateTime(input.observedAt, "live-probe observedAt");
  canonicalUtcDateTime(input.rights.reviewedAt, "live-probe rights reviewedAt");
  boundedNumber(input.durationMs, 0, MAX_DURATION_MS, "live-probe durationMs");
  validateSuccessfulAttempts(input.attempts);
  const canonicalBytes = serialiseProviderAdapterResult(input.result).byteLength;
  boundedInteger(canonicalBytes, 1, MAX_CANONICAL_BYTES, "live-probe canonicalBytes");

  return canonicalJsonClone({
    schema: "gis-ai-go.provider-live-probe.v1",
    observedAt: input.observedAt,
    status: "passed",
    bounded: true,
    credentialsUsed: false,
    payloadStored: false,
    adapter: {
      id: input.description.adapterId,
      version: input.description.adapterVersion,
    },
    providerVersion: {
      providerId: input.description.providerVersion.providerId,
      datasetId: input.description.providerVersion.datasetId,
      edition: input.description.providerVersion.edition,
      version: input.description.providerVersion.version,
      versionUri: input.description.providerVersion.versionUri,
      sourceDate: input.description.providerVersion.sourceDate,
    },
    rights: {
      state: input.rights.state,
      licence: input.rights.licence,
      licenceUri: input.rights.licenceUri,
      reviewedAt: input.rights.reviewedAt,
    },
    result: {
      digest: digestProviderAdapterResult(input.result),
      canonicalBytes,
    },
    durationMs: input.durationMs,
    attempts: input.attempts,
  });
}
