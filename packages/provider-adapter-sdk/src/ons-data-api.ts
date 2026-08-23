import { createGunzip } from "node:zlib";

import { canonicalJsonBytes, canonicalJsonClone } from "@gis-ai-go/evidence";

import { ProviderAdapterFault, assertFixedEgressTarget, normaliseAdapterError } from "./contract.js";
import {
  FixedHttpsTransportError,
  fixedHttpsTransportErrorKind,
  fixedHttpsGet,
  isExactFixedHttpsTransportError,
  type FixedHttpsResponse,
  type FixedHttpsTelemetry,
  type FixedHttpsTransport,
} from "./fixed-https.js";
import { StrictJsonParseError, parseStrictJson } from "./strict-json.js";
import {
  ADAPTER_OPERATIONS,
  type AdapterDescription,
  type AdapterHealth,
  type AdapterLifecycle,
  type AsyncProviderAdapter,
  type FixedEgressPolicy,
  type NormalisedAdapterError,
  type ProviderAdapterEstimate,
  type ProviderAdapterExecutionOptions,
  type ProviderAdapterProvenance,
  type ProviderAdapterQuery,
  type ProviderAdapterResult,
  type ProviderRights,
  type ProviderSelection,
  type ProviderVersionIdentity,
} from "./types.js";
import { normaliseW3CTraceContext } from "./trace-context.js";

export const ONS_ADAPTER_ID = "gis-ai-go.ons-data-api";
export const ONS_ADAPTER_VERSION = "1";
export const ONS_PROVIDER_ID = "ons-data-api";
export const ONS_DATASET_ID = "weekly-deaths-region";
export const ONS_EDITION = "time-series";
export const ONS_VERSION = "121";
export const ONS_ORIGIN = "https://api.beta.ons.gov.uk";
export const ONS_VERSION_PATH =
  "/v1/datasets/weekly-deaths-region/editions/time-series/versions/121";
export const ONS_OBSERVATION_PATH = `${ONS_VERSION_PATH}/observations`;
export const ONS_OBSERVATION_QUERY =
  "time=2026&geography=E92000001&week=week-24&causeofdeath=all-causes";
export const ONS_OBSERVATION_URI = `${ONS_ORIGIN}${ONS_OBSERVATION_PATH}?${ONS_OBSERVATION_QUERY}`;

const MAX_ATTEMPTS_PER_MINUTE = 30;
const RATE_WINDOW_MS = 60_000;
const DEFAULT_RETRY_DELAY_MS = 100;
/** Maximum wall-clock budget for one fixed ONS adapter call. */
export const ONS_CALL_DEADLINE_MS = 20_000;
const MAX_RETRY_DELAY_MS = 5_000;
const FULL_ATTEMPT_BUDGET_MS = 7_000;

export type OnsApprovedCacheOutage = Readonly<
  | { source: "network"; providerStatus: null; retryable: true }
  | { source: "http-5xx"; providerStatus: number; retryable: boolean }
>;

interface OnsApprovedCacheOutageProof {
  readonly adapter: OnsDataApiAdapter;
  readonly execution: object;
  readonly outage: OnsApprovedCacheOutage;
}

interface OnsApprovedCacheExecutionReservation {
  readonly execution: object;
  readonly claimed: boolean;
}

// Cache eligibility is provenance, not an inference from the public error code.
// Only faults created at the two reviewed provider-failure sites are branded,
// and each proof can be consumed once.
const ONS_APPROVED_CACHE_OUTAGES = new WeakMap<object, OnsApprovedCacheOutageProof>();
const ACTIVE_APPROVED_CACHE_EXECUTIONS = new WeakMap<
  object,
  OnsApprovedCacheExecutionReservation
>();

// Base instances are admitted only after their constructor has validated and
// stored every option. Subclasses, prototype forgeries and proxies are never
// added to this set.
const EXACT_ONS_DATA_API_ADAPTERS = new WeakSet<object>();

function approvedCacheOutage(
  adapter: OnsDataApiAdapter,
  execution: object | undefined,
  fault: ProviderAdapterFault,
  outage: OnsApprovedCacheOutage,
): ProviderAdapterFault {
  if (execution === undefined) return fault;
  ONS_APPROVED_CACHE_OUTAGES.set(
    fault,
    Object.freeze({ adapter, execution, outage: Object.freeze(outage) }),
  );
  return fault;
}

function claimApprovedCacheExecution(adapter: OnsDataApiAdapter): object | undefined {
  const reservation = ACTIVE_APPROVED_CACHE_EXECUTIONS.get(adapter);
  if (reservation === undefined || reservation.claimed) return undefined;
  ACTIVE_APPROVED_CACHE_EXECUTIONS.set(
    adapter,
    Object.freeze({ execution: reservation.execution, claimed: true }),
  );
  return reservation.execution;
}

function takeApprovedCacheEligibleOnsOutage(
  adapter: OnsDataApiAdapter,
  execution: object,
  error: unknown,
  normalised: NormalisedAdapterError,
): OnsApprovedCacheOutage | null {
  if (typeof error !== "object" || error === null) return null;
  const proof = ONS_APPROVED_CACHE_OUTAGES.get(error);
  // A rejected or accepted check exhausts the proof. This prevents the same
  // provider fault from authorising more than one cache decision.
  ONS_APPROVED_CACHE_OUTAGES.delete(error);
  if (
    proof === undefined ||
    proof.adapter !== adapter ||
    proof.execution !== execution ||
    !isPristineOnsDataApiAdapter(adapter) ||
    normalised.code !== "PROVIDER_OUTAGE"
  ) {
    return null;
  }
  const { outage } = proof;
  if (outage.source === "network") {
    return normalised.providerStatus === null &&
      normalised.retryable === outage.retryable
      ? outage
      : null;
  }
  return normalised.providerStatus === outage.providerStatus &&
    normalised.retryable === outage.retryable &&
    Number.isInteger(outage.providerStatus) &&
    outage.providerStatus >= 500 &&
    outage.providerStatus <= 599
    ? outage
    : null;
}

interface OnsProcessAdmissionState {
  inFlight: boolean;
  readonly attemptStarts: number[];
}

// This state is deliberately module-private and shared by every adapter instance.
// Adapter options must not provide a way to replace or reset the provider admission boundary.
const ONS_PROCESS_ADMISSION: OnsProcessAdmissionState = {
  inFlight: false,
  attemptStarts: [],
};

function isAborted(signal: AbortSignal | undefined): boolean {
  return signal?.aborted === true;
}

function acquireOnsProcessCall(): void {
  if (ONS_PROCESS_ADMISSION.inFlight) {
    throw new ProviderAdapterFault("PROVIDER_RATE_LIMITED", { retryable: true });
  }
  ONS_PROCESS_ADMISSION.inFlight = true;
}

function releaseOnsProcessCall(): void {
  ONS_PROCESS_ADMISSION.inFlight = false;
}

function admitOnsProcessAttempt(signal: AbortSignal): void {
  if (signal.aborted) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  const now = Date.now();
  if (!Number.isFinite(now)) throw new ProviderAdapterFault("PROVIDER_OUTAGE");
  while (
    ONS_PROCESS_ADMISSION.attemptStarts[0] !== undefined &&
    ONS_PROCESS_ADMISSION.attemptStarts[0] <= now - RATE_WINDOW_MS
  ) {
    ONS_PROCESS_ADMISSION.attemptStarts.shift();
  }
  if (ONS_PROCESS_ADMISSION.attemptStarts.length >= MAX_ATTEMPTS_PER_MINUTE) {
    throw new ProviderAdapterFault("PROVIDER_RATE_LIMITED", { retryable: true });
  }
  ONS_PROCESS_ADMISSION.attemptStarts.push(now);
}

export const ONS_SELECTIONS: readonly ProviderSelection[] = canonicalJsonClone([
  { dimension: "time", option: "2026" },
  { dimension: "geography", option: "E92000001" },
  { dimension: "week", option: "week-24" },
  { dimension: "causeofdeath", option: "all-causes" },
]);

export const ONS_EGRESS_POLICY: FixedEgressPolicy = canonicalJsonClone({
  mode: "fixed",
  origin: ONS_ORIGIN,
  method: "GET",
  routes: [
    {
      path: "/v1/datasets/weekly-deaths-region/editions/time-series",
      queryParameters: [],
      canonicalRawQuery: "",
    },
    { path: ONS_VERSION_PATH, queryParameters: [], canonicalRawQuery: "" },
    {
      path: ONS_OBSERVATION_PATH,
      queryParameters: ONS_SELECTIONS.map(({ dimension: name, option: value }) => ({ name, value })),
      canonicalRawQuery: ONS_OBSERVATION_QUERY,
    },
  ],
  allowCallerUrl: false,
  allowCredentials: false,
  maxRedirects: 0,
  connectTimeoutMs: 2_000,
  responseTimeoutMs: 5_000,
  maxCompressedBytes: 262_144,
  maxDecompressedBytes: 1_048_576,
  maxAttempts: 2,
  retryableStatuses: [429, 502, 503, 504],
  maxRetryAfterSeconds: 5,
});

const DEFAULT_LIFECYCLE: AdapterLifecycle = Object.freeze({
  discovery: "suspended",
  invocation: "suspended",
  reason: "The live ONS adapter is not activated by the shipped runtime.",
});

const ONS_PROVIDER_VERSION: ProviderVersionIdentity = canonicalJsonClone({
  providerId: ONS_PROVIDER_ID,
  datasetId: ONS_DATASET_ID,
  edition: ONS_EDITION,
  version: ONS_VERSION,
  versionUri: `${ONS_ORIGIN}${ONS_VERSION_PATH}`,
  sourceDate: "2026-07-01",
  dimensionOrder: ONS_SELECTIONS.map(({ dimension }) => dimension),
});

const ONS_RIGHTS: ProviderRights = canonicalJsonClone({
  state: "open-with-conditions",
  licence: "Open Government Licence v3.0",
  licenceUri: "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
  attribution:
    "Source: Office for National Statistics licensed under the Open Government Licence v.3.0",
  obligations: [
    "Acknowledge the source and licence when reproducing the selected ONS content.",
    "Preserve the selected dataset, edition, version and release date.",
    "Do not imply that ONS endorses GIS AI GO or its interpretation.",
  ],
  exceptions: [
    "The ONS logo is excluded and is not retrieved or redistributed.",
    "Any record-level third-party exception overrides this general evidence and must fail closed.",
    "The selected aggregate dataset page stated no additional exception when reviewed.",
  ],
  evidenceUris: [
    "https://www.ons.gov.uk/datasets/weekly-deaths-region/editions/time-series/versions/121",
    "https://www.ons.gov.uk/help/terms-conditions",
    "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
  ],
  reviewedAt: "2026-08-20T17:40:35Z",
});

const ONS_PROVENANCE: ProviderAdapterProvenance = canonicalJsonClone({
  providerVersion: ONS_PROVIDER_VERSION,
  adapter: { id: ONS_ADAPTER_ID, version: ONS_ADAPTER_VERSION },
  transformations: [
    "ons-cmd-single-observation.v1",
    "provider-native-identifiers-preserved.v1",
    "untrusted-provider-links-validated-and-omitted.v1",
    "rfc8785-canonical-json.v1",
  ],
  synthetic: false,
  sourceUri: ONS_OBSERVATION_URI,
});

export interface OnsResponseAttemptTelemetry extends FixedHttpsTelemetry {
  readonly attempt: number;
  readonly outcome: "response";
  readonly status: number;
  readonly decompressedBytes: number | null;
}

export interface OnsFailedAttemptTelemetry {
  readonly attempt: number;
  readonly outcome: "transport-failure";
  readonly status: null;
  readonly code: NormalisedAdapterError["code"];
}

export type OnsAttemptTelemetry = OnsResponseAttemptTelemetry | OnsFailedAttemptTelemetry;

export interface OnsDataApiAdapterOptions {
  readonly lifecycle?: AdapterLifecycle;
  readonly transport?: FixedHttpsTransport;
  readonly now?: () => number;
  readonly sleep?: (milliseconds: number, signal: AbortSignal | undefined) => Promise<void>;
  readonly onAttempt?: (telemetry: OnsAttemptTelemetry) => void;
}

function recordAt(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  return value as Record<string, unknown>;
}

function responseRecordAt(value: unknown): Record<string, unknown> {
  try {
    return recordAt(value);
  } catch {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
}

function exactKeys(
  record: Record<string, unknown>,
  expected: readonly string[],
  code: "INVALID_REQUEST" | "MALFORMED_PROVIDER_RESPONSE" = "MALFORMED_PROVIDER_RESPONSE",
): void {
  const actual = Object.keys(record).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    throw new ProviderAdapterFault(code);
  }
}

function boundedString(
  value: unknown,
  maximum: number,
  code: "INVALID_REQUEST" | "MALFORMED_PROVIDER_RESPONSE" = "MALFORMED_PROVIDER_RESPONSE",
): string {
  if (typeof value !== "string" || Array.from(value).length > maximum) {
    throw new ProviderAdapterFault(code);
  }
  return value;
}

function parseLifecycle(input: unknown): AdapterLifecycle {
  let lifecycle: Record<string, unknown>;
  try {
    lifecycle = recordAt(canonicalJsonClone(input));
    exactKeys(lifecycle, ["discovery", "invocation", "reason"], "INVALID_REQUEST");
  } catch {
    throw new TypeError("ONS adapter lifecycle must be closed canonical JSON");
  }
  if (
    !["active", "suspended"].includes(String(lifecycle.discovery)) ||
    !["active", "suspended"].includes(String(lifecycle.invocation)) ||
    typeof lifecycle.reason !== "string" ||
    lifecycle.reason.length < 1 ||
    Array.from(lifecycle.reason).length > 512
  ) {
    throw new TypeError("ONS adapter lifecycle planes and reason are invalid");
  }
  return canonicalJsonClone({
    discovery: lifecycle.discovery as AdapterLifecycle["discovery"],
    invocation: lifecycle.invocation as AdapterLifecycle["invocation"],
    reason: lifecycle.reason,
  });
}

function parseQuery(input: unknown): ProviderAdapterQuery {
  let request: Record<string, unknown>;
  try {
    request = recordAt(canonicalJsonClone(input));
  } catch {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  exactKeys(request, ["dataset", "selections"], "INVALID_REQUEST");
  const dataset = recordAt(request.dataset);
  exactKeys(dataset, ["edition", "id", "version"], "INVALID_REQUEST");
  const datasetId = boundedString(dataset.id, 128, "INVALID_REQUEST");
  const edition = boundedString(dataset.edition, 128, "INVALID_REQUEST");
  const version = boundedString(dataset.version, 128, "INVALID_REQUEST");
  if (datasetId !== ONS_DATASET_ID || edition !== ONS_EDITION) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  if (version !== ONS_VERSION) throw new ProviderAdapterFault("STALE_PROVIDER_VERSION");
  if (!Array.isArray(request.selections) || request.selections.length !== ONS_SELECTIONS.length) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  const selections = request.selections.map((candidate, index) => {
    const selection = recordAt(candidate);
    exactKeys(selection, ["dimension", "option"], "INVALID_REQUEST");
    const dimension = boundedString(selection.dimension, 128, "INVALID_REQUEST");
    const option = boundedString(selection.option, 128, "INVALID_REQUEST");
    const expected = ONS_SELECTIONS[index];
    if (expected === undefined || dimension !== expected.dimension || option !== expected.option) {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    return { dimension, option };
  });
  return canonicalJsonClone({ dataset: { id: datasetId, edition, version }, selections });
}

function providerUrl(
  value: unknown,
  expectedPath: string,
  expectedQuery: Readonly<Record<string, string>> | null = null,
): void {
  const href = boundedString(value, 2_048);
  let parsed: URL;
  try {
    parsed = new URL(href);
  } catch {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  if (
    !["http:", "https:"].includes(parsed.protocol) ||
    parsed.hostname !== "api.beta.ons.gov.uk" ||
    parsed.username !== "" ||
    parsed.password !== "" ||
    parsed.port !== "" ||
    parsed.pathname !== expectedPath ||
    parsed.hash !== ""
  ) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  if (expectedQuery === null) {
    if (parsed.search !== "") throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
    return;
  }
  const observed = [...parsed.searchParams];
  if (
    observed.length !== Object.keys(expectedQuery).length ||
    new Set(observed.map(([name]) => name)).size !== observed.length ||
    observed.some(([name, option]) => expectedQuery[name] !== option)
  ) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
}

function optionAt(
  dimensions: Record<string, unknown>,
  dimension: string,
  option: string,
  codeList: string,
): void {
  const dimensionRecord = responseRecordAt(dimensions[dimension]);
  exactKeys(dimensionRecord, ["option"]);
  const optionRecord = responseRecordAt(dimensionRecord.option);
  exactKeys(optionRecord, ["href", "id"]);
  if (boundedString(optionRecord.id, 128) !== option) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  providerUrl(optionRecord.href, `/v1/code-lists/${codeList}/codes/${option}`);
}

function parseProviderPayload(payload: unknown, query: ProviderAdapterQuery): ProviderAdapterResult {
  const root = responseRecordAt(payload);
  exactKeys(root, ["dimensions", "limit", "links", "observations", "offset", "total_observations"]);
  if (
    root.limit !== 10_000 ||
    root.offset !== 0 ||
    root.total_observations !== 1 ||
    !Number.isSafeInteger(root.limit) ||
    !Number.isSafeInteger(root.offset) ||
    !Number.isSafeInteger(root.total_observations)
  ) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }

  const dimensions = responseRecordAt(root.dimensions);
  exactKeys(dimensions, ["causeofdeath", "geography", "time", "week"]);
  optionAt(dimensions, "time", "2026", "calendar-years");
  optionAt(dimensions, "geography", "E92000001", "administrative-geography");
  optionAt(dimensions, "week", "week-24", "week-number");
  optionAt(dimensions, "causeofdeath", "all-causes", "cause-of-death");

  const links = responseRecordAt(root.links);
  exactKeys(links, ["dataset_metadata", "self", "version"]);
  const metadataLink = responseRecordAt(links.dataset_metadata);
  exactKeys(metadataLink, ["href"]);
  providerUrl(metadataLink.href, `${ONS_VERSION_PATH}/metadata`);
  const selfLink = responseRecordAt(links.self);
  exactKeys(selfLink, ["href"]);
  providerUrl(
    selfLink.href,
    ONS_OBSERVATION_PATH,
    Object.fromEntries(ONS_SELECTIONS.map(({ dimension, option }) => [dimension, option])),
  );
  const versionLink = responseRecordAt(links.version);
  exactKeys(versionLink, ["href", "id"]);
  if (versionLink.id !== ONS_VERSION) {
    throw new ProviderAdapterFault("STALE_PROVIDER_VERSION");
  }
  providerUrl(versionLink.href, ONS_VERSION_PATH);

  if (!Array.isArray(root.observations) || root.observations.length !== 1) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  const observation = responseRecordAt(root.observations[0]);
  exactKeys(observation, ["metadata", "observation"]);
  const metadata = responseRecordAt(observation.metadata);
  exactKeys(metadata, ["Data Marking"]);
  const dataMarking = boundedString(metadata["Data Marking"], 128);
  if (dataMarking !== "") throw new ProviderAdapterFault("RIGHTS_UNKNOWN");
  const value = boundedString(observation.observation, 32);
  if (!/^(?:0|[1-9][0-9]{0,14})$/u.test(value)) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }

  return canonicalJsonClone({
    schema: "gis-ai-go.provider-adapter-result.v1",
    provider: { id: ONS_PROVIDER_ID, adapterId: ONS_ADAPTER_ID },
    dataset: {
      id: ONS_DATASET_ID,
      edition: ONS_EDITION,
      version: ONS_VERSION,
      versionUri: `${ONS_ORIGIN}${ONS_VERSION_PATH}`,
    },
    dimensions: query.selections,
    observations: [
      {
        value,
        unit: null,
        metadata: [{ name: "Data Marking", value: dataMarking }],
      },
    ],
    rights: ONS_RIGHTS,
    provenance: ONS_PROVENANCE,
  });
}

async function responseBody(
  response: FixedHttpsResponse,
  signal: AbortSignal,
): Promise<Uint8Array> {
  if (signal.aborted) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  const contentType = response.headers["content-type"]?.trim();
  if (
    contentType === undefined ||
    !/^application\/json(?:\s*;\s*charset=utf-8)?$/iu.test(contentType)
  ) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  const declaredLength = response.headers["content-length"];
  if (
    declaredLength !== undefined &&
    (!/^(?:0|[1-9][0-9]*)$/u.test(declaredLength) ||
      Number(declaredLength) !== response.body.byteLength ||
      Number(declaredLength) > ONS_EGRESS_POLICY.maxCompressedBytes)
  ) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  if (response.body.byteLength > ONS_EGRESS_POLICY.maxCompressedBytes) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  const encoding = (response.headers["content-encoding"] ?? "identity").trim().toLowerCase();
  let body: Uint8Array;
  if (encoding === "identity") {
    body = new Uint8Array(response.body);
  } else if (encoding === "gzip") {
    body = await new Promise<Uint8Array>((resolve, reject) => {
      const gunzip = createGunzip();
      const chunks: Buffer[] = [];
      let decompressedBytes = 0;
      let settled = false;
      const finish = (error: ProviderAdapterFault | null, value?: Uint8Array): void => {
        if (settled) return;
        settled = true;
        signal.removeEventListener("abort", onAbort);
        if (error === null) resolve(value!);
        else reject(error);
      };
      const onAbort = (): void => {
        gunzip.destroy();
        finish(new ProviderAdapterFault("PROVIDER_TIMEOUT"));
      };
      signal.addEventListener("abort", onAbort, { once: true });
      gunzip.on("data", (chunk: Buffer | Uint8Array) => {
        const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
        decompressedBytes += bytes.byteLength;
        if (decompressedBytes > ONS_EGRESS_POLICY.maxDecompressedBytes) {
          gunzip.destroy();
          finish(new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE"));
          return;
        }
        chunks.push(bytes);
      });
      gunzip.once("error", () => finish(new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE")));
      gunzip.once("end", () => finish(null, Buffer.concat(chunks, decompressedBytes)));
      if (signal.aborted) onAbort();
      else gunzip.end(response.body);
    });
  } else {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  if (signal.aborted) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  if (body.byteLength > ONS_EGRESS_POLICY.maxDecompressedBytes) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  return body;
}

async function parseSuccessfulResponse(
  response: FixedHttpsResponse,
  query: ProviderAdapterQuery,
  signal: AbortSignal,
): Promise<{ readonly result: ProviderAdapterResult; readonly decompressedBytes: number }> {
  const body = await responseBody(response, signal);
  let text: string;
  let payload: unknown;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(body);
    payload = parseStrictJson(text);
  } catch (error) {
    if (error instanceof ProviderAdapterFault) throw error;
    if (error instanceof StrictJsonParseError || error instanceof TypeError) {
      throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
    }
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  const result = parseProviderPayload(payload, query);
  if (signal.aborted) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  if (canonicalJsonBytes(result).byteLength > 262_144) {
    throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  return { result, decompressedBytes: body.byteLength };
}

function statusFault(
  adapter: OnsDataApiAdapter,
  execution: object | undefined,
  status: number,
): ProviderAdapterFault {
  if (status === 429) {
    return new ProviderAdapterFault("PROVIDER_RATE_LIMITED", {
      providerStatus: status,
      retryable: true,
    });
  }
  if (status === 400 || status === 404 || status === 410) {
    return new ProviderAdapterFault("STALE_PROVIDER_VERSION", { providerStatus: status });
  }
  const fault = new ProviderAdapterFault("PROVIDER_OUTAGE", {
    providerStatus: status,
    retryable: ONS_EGRESS_POLICY.retryableStatuses.includes(status),
  });
  return Number.isInteger(status) && status >= 500 && status <= 599
    ? approvedCacheOutage(adapter, execution, fault, {
      source: "http-5xx",
      providerStatus: status,
      retryable: fault.retryable,
    })
    : fault;
}

function transportFault(
  adapter: OnsDataApiAdapter,
  execution: object | undefined,
  error: unknown,
  aborted: boolean,
  approvedNetworkTransport: boolean,
): ProviderAdapterFault {
  const kind = fixedHttpsTransportErrorKind(error);
  if (kind === null) {
    return new ProviderAdapterFault("PROVIDER_OUTAGE", { retryable: true });
  }
  if (
    kind === "aborted" ||
    kind === "connect-timeout" ||
    kind === "response-timeout"
  ) {
    return new ProviderAdapterFault("PROVIDER_TIMEOUT", { retryable: !aborted });
  }
  if (
    kind === "invalid-response-framing" ||
    kind === "invalid-response-headers" ||
    kind === "response-too-large"
  ) {
    return new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
  }
  const fault = new ProviderAdapterFault("PROVIDER_OUTAGE", {
    retryable: kind === "network",
  });
  return kind === "network" &&
    approvedNetworkTransport &&
    isExactFixedHttpsTransportError(error)
    ? approvedCacheOutage(adapter, execution, fault, {
      source: "network",
      providerStatus: null,
      retryable: true,
    })
    : fault;
}

function retryDelay(response: FixedHttpsResponse, now: number): number | null {
  const header = response.headers["retry-after"];
  if (header === undefined) return DEFAULT_RETRY_DELAY_MS;
  if (/^(?:0|[1-9][0-9]*)$/u.test(header)) {
    const seconds = Number(header);
    const milliseconds = seconds * 1_000;
    return milliseconds <= MAX_RETRY_DELAY_MS ? milliseconds : null;
  }
  const instant = Date.parse(header);
  if (!Number.isFinite(instant)) return null;
  const seconds = Math.max(0, Math.ceil((instant - now) / 1_000));
  const milliseconds = seconds * 1_000;
  return milliseconds <= MAX_RETRY_DELAY_MS ? milliseconds : null;
}

function effectiveDeadline(now: number, supplied: string | undefined): number {
  if (!Number.isFinite(now)) throw new ProviderAdapterFault("PROVIDER_OUTAGE");
  const localDeadline = now + ONS_CALL_DEADLINE_MS;
  if (supplied === undefined) return localDeadline;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(?:Z|([+-])(\d{2}):(\d{2}))$/u.exec(
    supplied,
  );
  if (supplied.length > 64 || match === null) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const offsetHour = match[8] === undefined ? 0 : Number(match[8]);
  const offsetMinute = match[9] === undefined ? 0 : Number(match[9]);
  const leapYear = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const monthDays = [31, leapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (
    year < 1 ||
    month < 1 ||
    month > 12 ||
    day < 1 ||
    day > monthDays[month - 1]! ||
    hour > 23 ||
    minute > 59 ||
    second > 59 ||
    offsetHour > 23 ||
    offsetMinute > 59
  ) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  const parsed = Date.parse(supplied);
  if (!Number.isFinite(parsed)) throw new ProviderAdapterFault("INVALID_REQUEST");
  return Math.min(localDeadline, parsed);
}

async function defaultSleep(milliseconds: number, signal: AbortSignal | undefined): Promise<void> {
  if (signal?.aborted === true) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  await new Promise<void>((resolve, reject) => {
    let settled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const finish = (error: ProviderAdapterFault | null): void => {
      if (settled) return;
      settled = true;
      if (timer !== undefined) clearTimeout(timer);
      signal?.removeEventListener("abort", onAbort);
      if (error === null) resolve();
      else reject(error);
    };
    const onAbort = (): void => {
      finish(new ProviderAdapterFault("PROVIDER_TIMEOUT"));
    };
    timer = setTimeout(() => finish(null), milliseconds);
    signal?.addEventListener("abort", onAbort, { once: true });
    if (signal?.aborted === true) onAbort();
  });
}

function validateOptions(options: OnsDataApiAdapterOptions): void {
  const allowed = new Set(["lifecycle", "transport", "now", "sleep", "onAttempt"]);
  if (Object.keys(options).some((key) => !allowed.has(key))) {
    throw new TypeError("ONS adapter options contain an unexpected property");
  }
  for (const key of ["transport", "now", "sleep", "onAttempt"] as const) {
    if (options[key] !== undefined && typeof options[key] !== "function") {
      throw new TypeError(`ONS adapter ${key} must be a function`);
    }
  }
}

export class OnsDataApiAdapter implements AsyncProviderAdapter {
  public readonly operations = ADAPTER_OPERATIONS;
  readonly #lifecycle: AdapterLifecycle;
  readonly #transport: FixedHttpsTransport;
  readonly #now: () => number;
  readonly #sleep: (milliseconds: number, signal: AbortSignal | undefined) => Promise<void>;
  readonly #onAttempt: ((telemetry: OnsAttemptTelemetry) => void) | undefined;

  public constructor(options: OnsDataApiAdapterOptions = {}) {
    if (new.target !== OnsDataApiAdapter) {
      throw new TypeError("ONS adapter subclassing is not supported");
    }
    validateOptions(options);
    this.#lifecycle = parseLifecycle(options.lifecycle ?? DEFAULT_LIFECYCLE);
    this.#transport = options.transport ?? fixedHttpsGet;
    this.#now = options.now ?? Date.now;
    this.#sleep = options.sleep ?? defaultSleep;
    this.#onAttempt = options.onAttempt;
    assertFixedEgressTarget(ONS_EGRESS_POLICY, {
      method: "GET",
      url: ONS_OBSERVATION_URI,
      redirectCount: 0,
    });
    EXACT_ONS_DATA_API_ADAPTERS.add(this);
  }

  public describe(): AdapterDescription {
    if (this.#lifecycle.discovery !== "active") {
      throw new ProviderAdapterFault("ADAPTER_DISCOVERY_SUSPENDED");
    }
    return canonicalJsonClone({
      adapterId: ONS_ADAPTER_ID,
      adapterVersion: ONS_ADAPTER_VERSION,
      name: "ONS Data API weekly deaths single-observation adapter",
      operations: ADAPTER_OPERATIONS,
      lifecycle: this.#lifecycle,
      providerVersion: ONS_PROVIDER_VERSION,
      egress: ONS_EGRESS_POLICY,
    });
  }

  public health(): AdapterHealth {
    return canonicalJsonClone({
      adapterId: ONS_ADAPTER_ID,
      discovery: this.#lifecycle.discovery,
      invocation: this.#lifecycle.invocation,
      network: "not-checked",
    });
  }

  public estimate(request: unknown): ProviderAdapterEstimate {
    this.#assertInvocation();
    parseQuery(request);
    return canonicalJsonClone({
      confidence: "upper-bound",
      maxObservations: 1,
      maxAttempts: ONS_EGRESS_POLICY.maxAttempts,
      maxCompressedResponseBytes: ONS_EGRESS_POLICY.maxCompressedBytes,
      maxDecompressedResponseBytes: ONS_EGRESS_POLICY.maxDecompressedBytes,
      maxCanonicalResponseBytes: 262_144,
    });
  }

  public async execute(
    request: unknown,
    options: ProviderAdapterExecutionOptions = {},
  ): Promise<ProviderAdapterResult> {
    // Only the canonical call started by executePristineOnsDataApiAdapter can
    // claim its reserved token. Re-entrant or concurrent direct calls receive
    // no approved-cache provenance even while that reservation is active.
    const approvedCacheExecution = claimApprovedCacheExecution(this);
    this.#assertInvocation();
    if (Object.keys(options).some((key) => !["signal", "deadline", "trace"].includes(key))) {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    if (options.signal !== undefined && !(options.signal instanceof AbortSignal)) {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    if (options.deadline !== undefined && typeof options.deadline !== "string") {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    if (options.trace !== undefined) {
      try {
        normaliseW3CTraceContext(options.trace);
      } catch {
        throw new ProviderAdapterFault("INVALID_REQUEST");
      }
    }
    const query = parseQuery(request);
    const startedAt = this.#now();
    const deadline = effectiveDeadline(startedAt, options.deadline);
    if (isAborted(options.signal) || deadline <= startedAt) {
      throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
    }
    acquireOnsProcessCall();
    const controller = new AbortController();
    const onExternalAbort = (): void => controller.abort();
    let deadlineTimer: ReturnType<typeof setTimeout> | undefined;
    try {
      options.signal?.addEventListener("abort", onExternalAbort, { once: true });
      if (isAborted(options.signal)) controller.abort();
      deadlineTimer = setTimeout(
        () => controller.abort(),
        Math.max(1, Math.min(ONS_CALL_DEADLINE_MS, deadline - startedAt)),
      );
      for (let attempt = 1; attempt <= ONS_EGRESS_POLICY.maxAttempts; attempt += 1) {
        if (controller.signal.aborted) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
        admitOnsProcessAttempt(controller.signal);
        let response: FixedHttpsResponse;
        try {
          response = await this.#transport({
            policy: ONS_EGRESS_POLICY,
            url: ONS_OBSERVATION_URI,
            signal: controller.signal,
          });
        } catch (error) {
          const fault = transportFault(
            this,
            approvedCacheExecution,
            error,
            controller.signal.aborted,
            this.#transport === fixedHttpsGet,
          );
          this.#emit({
            attempt,
            outcome: "transport-failure",
            status: null,
            code: fault.code,
          });
          if (fault.retryable && attempt < ONS_EGRESS_POLICY.maxAttempts) continue;
          throw fault;
        }

        if (response.status !== 200) {
          const fault = statusFault(this, approvedCacheExecution, response.status);
          this.#emitResponse(attempt, response, null);
          if (fault.retryable && attempt < ONS_EGRESS_POLICY.maxAttempts) {
            const now = this.#now();
            const delay = retryDelay(response, now);
            if (delay !== null && delay + FULL_ATTEMPT_BUDGET_MS <= deadline - now) {
              await this.#sleep(delay, controller.signal);
              continue;
            }
          }
          throw fault;
        }
        try {
          const parsed = await parseSuccessfulResponse(response, query, controller.signal);
          this.#emitResponse(attempt, response, parsed.decompressedBytes);
          return parsed.result;
        } catch (error) {
          this.#emitResponse(attempt, response, null);
          if (error instanceof ProviderAdapterFault) throw error;
          throw new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE");
        }
      }
      throw new ProviderAdapterFault("PROVIDER_OUTAGE");
    } finally {
      if (deadlineTimer !== undefined) clearTimeout(deadlineTimer);
      options.signal?.removeEventListener("abort", onExternalAbort);
      releaseOnsProcessCall();
    }
  }

  public normalise_error(error: unknown): NormalisedAdapterError {
    return normaliseAdapterError(error);
  }

  public licence_evidence(): ProviderRights {
    return canonicalJsonClone(ONS_RIGHTS);
  }

  public provenance(): ProviderAdapterProvenance {
    return canonicalJsonClone(ONS_PROVENANCE);
  }

  #assertInvocation(): void {
    if (this.#lifecycle.invocation !== "active") {
      throw new ProviderAdapterFault("ADAPTER_INVOCATION_SUSPENDED");
    }
  }

  #emit(telemetry: OnsAttemptTelemetry): void {
    try {
      this.#onAttempt?.(canonicalJsonClone(telemetry));
    } catch {
      // Telemetry is observational and must not change provider execution semantics.
    }
  }

  #emitResponse(
    attempt: number,
    response: FixedHttpsResponse,
    decompressedBytes: number | null,
  ): void {
    this.#emit({
      ...response.telemetry,
      attempt,
      outcome: "response",
      status: response.status,
      decompressedBytes,
    });
  }
}

const ONS_DATA_API_ADAPTER_PROTOTYPE = OnsDataApiAdapter.prototype;
const ONS_DATA_API_ADAPTER_PROTOTYPE_PARENT = Object.getPrototypeOf(
  ONS_DATA_API_ADAPTER_PROTOTYPE,
) as object | null;
const ONS_DATA_API_ADAPTER_PROTOTYPE_DESCRIPTORS = Reflect.ownKeys(
  ONS_DATA_API_ADAPTER_PROTOTYPE,
).map((key) => {
  const descriptor = Object.getOwnPropertyDescriptor(
    ONS_DATA_API_ADAPTER_PROTOTYPE,
    key,
  );
  if (descriptor === undefined) throw new TypeError("ONS adapter prototype is invalid");
  return Object.freeze({ key, descriptor: Object.freeze({ ...descriptor }) });
});
const EXACT_ONS_DATA_API_ADAPTER_EXECUTE = OnsDataApiAdapter.prototype.execute;
const EXACT_ONS_DATA_API_ADAPTER_NORMALISE_ERROR =
  OnsDataApiAdapter.prototype.normalise_error;

function sameDescriptor(
  left: PropertyDescriptor,
  right: PropertyDescriptor | undefined,
): boolean {
  if (right === undefined) return false;
  if (
    left.configurable !== right.configurable ||
    left.enumerable !== right.enumerable
  ) {
    return false;
  }
  if ("value" in left) {
    return (
      "value" in right &&
      left.value === right.value &&
      left.writable === right.writable
    );
  }
  return (
    !("value" in right) &&
    left.get === right.get &&
    left.set === right.set
  );
}

function hasPristineOnsDataApiAdapterPrototype(): boolean {
  try {
    const keys = Reflect.ownKeys(ONS_DATA_API_ADAPTER_PROTOTYPE);
    if (
      keys.length !== ONS_DATA_API_ADAPTER_PROTOTYPE_DESCRIPTORS.length ||
      Object.getPrototypeOf(ONS_DATA_API_ADAPTER_PROTOTYPE) !==
        ONS_DATA_API_ADAPTER_PROTOTYPE_PARENT
    ) {
      return false;
    }
    return ONS_DATA_API_ADAPTER_PROTOTYPE_DESCRIPTORS.every(({ key, descriptor }) =>
      keys.includes(key) &&
      sameDescriptor(
        descriptor,
        Object.getOwnPropertyDescriptor(ONS_DATA_API_ADAPTER_PROTOTYPE, key),
      ));
  } catch {
    return false;
  }
}

/** True only for a fully constructed base adapter, without proxy traversal. */
function isExactOnsDataApiAdapter(value: unknown): value is OnsDataApiAdapter {
  if (
    typeof value !== "object" ||
    value === null ||
    !EXACT_ONS_DATA_API_ADAPTERS.has(value)
  ) {
    return false;
  }
  try {
    return Object.getPrototypeOf(value) === OnsDataApiAdapter.prototype;
  } catch {
    return false;
  }
}

/**
 * True only while an exact adapter has no instance-level method or state
 * substitution. Cache-enabled applications recheck this at every trust
 * boundary around provider execution.
 */
function isPristineOnsDataApiAdapter(value: unknown): value is OnsDataApiAdapter {
  if (
    !isExactOnsDataApiAdapter(value) ||
    !hasPristineOnsDataApiAdapterPrototype()
  ) {
    return false;
  }
  try {
    const keys = Reflect.ownKeys(value);
    if (keys.length !== 1 || keys[0] !== "operations") return false;
    const descriptor = Object.getOwnPropertyDescriptor(value, "operations");
    return (
      descriptor !== undefined &&
      "value" in descriptor &&
      descriptor.value === ADAPTER_OPERATIONS &&
      descriptor.enumerable === true &&
      descriptor.configurable === true &&
      descriptor.writable === true
    );
  } catch {
    return false;
  }
}

/** Admit only a fully constructed base adapter at an application boundary. */
export function requireExactOnsDataApiAdapter(value: unknown): OnsDataApiAdapter {
  if (!isExactOnsDataApiAdapter(value)) {
    throw new TypeError("ONS adapter is not exact");
  }
  return value;
}

/** Admit only an exact adapter without method, state or prototype substitution. */
export function requirePristineOnsDataApiAdapter(value: unknown): OnsDataApiAdapter {
  if (!isPristineOnsDataApiAdapter(value)) {
    throw new TypeError("ONS adapter is not pristine");
  }
  return value;
}

export interface OnsDataApiAdapterExecution {
  readonly result: Promise<ProviderAdapterResult>;
  readonly approvedCacheOutage: (
    error: unknown,
    normalised: NormalisedAdapterError,
  ) => OnsApprovedCacheOutage | null;
}

/**
 * Execute through the captured implementation and return a one-call outage
 * capability bound to this exact invocation.
 */
export function executePristineOnsDataApiAdapter(
  adapter: OnsDataApiAdapter,
  request: unknown,
  options: ProviderAdapterExecutionOptions,
): OnsDataApiAdapterExecution {
  if (!isPristineOnsDataApiAdapter(adapter)) {
    throw new TypeError("ONS adapter is not pristine");
  }
  if (ACTIVE_APPROVED_CACHE_EXECUTIONS.has(adapter)) {
    throw new TypeError("ONS adapter already has an active cache-eligible execution");
  }
  const execution = Object.freeze({});
  ACTIVE_APPROVED_CACHE_EXECUTIONS.set(
    adapter,
    Object.freeze({ execution, claimed: false }),
  );
  let pending: Promise<ProviderAdapterResult>;
  try {
    pending = EXACT_ONS_DATA_API_ADAPTER_EXECUTE.call(adapter, request, options);
  } catch (error) {
    ACTIVE_APPROVED_CACHE_EXECUTIONS.delete(adapter);
    throw error;
  }
  const result = pending.finally(() => {
    if (ACTIVE_APPROVED_CACHE_EXECUTIONS.get(adapter)?.execution === execution) {
      ACTIVE_APPROVED_CACHE_EXECUTIONS.delete(adapter);
    }
  });
  let consumed = false;
  return Object.freeze({
    result,
    approvedCacheOutage: (
      error: unknown,
      normalised: NormalisedAdapterError,
    ): OnsApprovedCacheOutage | null => {
      if (consumed) return null;
      consumed = true;
      return takeApprovedCacheEligibleOnsOutage(
        adapter,
        execution,
        error,
        normalised,
      );
    },
  });
}

/** Normalise through the captured implementation after an integrity check. */
export function normalisePristineOnsDataApiAdapterError(
  adapter: OnsDataApiAdapter,
  error: unknown,
): NormalisedAdapterError {
  if (!isPristineOnsDataApiAdapter(adapter)) {
    throw new TypeError("ONS adapter is not pristine");
  }
  return EXACT_ONS_DATA_API_ADAPTER_NORMALISE_ERROR.call(adapter, error);
}

export function createOnsDataApiAdapter(
  options: OnsDataApiAdapterOptions = {},
): OnsDataApiAdapter {
  return new OnsDataApiAdapter(options);
}

export const ONS_ADAPTER_REQUEST: ProviderAdapterQuery = canonicalJsonClone({
  dataset: { id: ONS_DATASET_ID, edition: ONS_EDITION, version: ONS_VERSION },
  selections: ONS_SELECTIONS,
});
