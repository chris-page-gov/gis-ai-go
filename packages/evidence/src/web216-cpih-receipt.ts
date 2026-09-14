/**
 * Experimental, provider-free read of one admitted CPIH capture observation.
 * This family is deliberately not an activated gateway operation. Its separately
 * identified ledger wrapper supplies storage evidence without altering this body.
 * A content hash proves equality, not authority, execution, attestation or storage.
 */
import { createHash } from "node:crypto";
import { canonicalJson, canonicalJsonBytes, canonicalJsonClone } from "./canonical-json.js";
import { canonicalDigest, contentAddress } from "./digest.js";
import {
  CANONICALISATION,
  isStrictEvidenceDateTime,
  type EvidenceSoftwareIdentity,
} from "./receipt.js";

export const WEB216_CPIH_DOMAINS = Object.freeze({
  receipt: "gis-ai-go.web216-cpih-receipt.v1",
  parameters: "gis-ai-go.web216-cpih-parameters.v1",
  result: "gis-ai-go.web216-cpih-result-core.v1",
} as const);

export type Web216CpihPeriod = "2026-01" | "2026-07";

// Reviewed constants from tests/fixtures/web216/current-cpih-projection.json.
// The projection hash is plain SHA-256 of its canonical body WITHOUT its own
// projection_sha256 field. Original response bodies are not in this fixture.
export const WEB216_CPIH_CAPTURE = canonicalJsonClone({
  fixture_schema: "web216.public-cpih-projection.v1",
  projection_sha256: "0e04a627e98d356ddf295a584e7a2d9e9c5a8110c509a6762561ff2b796ab667",
  capture_manifest_sha256: "571af13a50ca4d93b364bb4cf63d46af7655d56b16b8275bd4fe1b461d857a6b",
  original_body_sha256: {
    data: "7f9af141727981a21d040febcb8a71db9299455e910583ed3eefad446a50a3b9",
    search: "802ced2b6077c4ab5f96d84415e53cb400b53ee81dffdf577c12daddb721db99",
  },
  captured_at: "2026-09-14T15:42:57.906633Z",
  release_date: "2026-08-18T23:00:00.000Z",
  next_release: "16 September 2026",
  next_release_validation: "unvalidated-provider-text",
  original_month_count: 463,
  original_period_range: { first: "1988-01", last: "2026-07" },
  projected_month_count: 2,
  validation_scope: "pinned-two-month-projection-not-original-response-bodies",
  source_capture: { mcp_executed: false, production_transport: false },
  urls: {
    data: "https://api.beta.ons.gov.uk/v1/data?uri=%2Feconomy%2Finflationandpriceindices%2Ftimeseries%2Fl522%2Fmm23",
    public_page: "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l522/mm23",
    search: "https://api.beta.ons.gov.uk/v1/search?content_type=timeseries&cdids=L522",
  },
} as const);

export const WEB216_CPIH_POLICY_SCOPE = canonicalJsonClone({
  construction: "compile-time-pinned-experimental-capture-scope",
  authority_profile: "anonymous-open",
  authentication: "none",
  publication_classification: "public",
  contains_personal_data: false,
  contains_protected_data: false,
  read_only: true,
  operation: "read-validated-cpih-capture",
  admitted_periods: ["2026-01", "2026-07"],
  max_observations: 1,
  provider_egress: false,
  grants_provider_permission: false,
  default_effect: "deny",
  effect: "allow-pinned-capture-read-only",
} as const);

const SERIES = canonicalJsonClone({
  cdid: "L522",
  dataset_id: "MM23",
  type: "timeseries",
  uri: "/economy/inflationandpriceindices/timeseries/l522/mm23",
  title: "CPIH INDEX 00: ALL ITEMS 2015=100",
  unit: "Index, base year = 100",
  base_year: 2015,
  base_year_basis: "exact-series-title",
} as const);

const OBSERVATIONS = canonicalJsonClone({
  "2026-01": {
    date: "2026 JAN", label: "2026 JAN", month: "January", quarter: "",
    sourceDataset: "MM23", updateDate: "2026-02-18T00:00:00.000Z",
    value: "139.4", year: "2026",
  },
  "2026-07": {
    date: "2026 JUL", label: "2026 JUL", month: "July", quarter: "",
    sourceDataset: "MM23", updateDate: "2026-08-18T23:00:00.000Z",
    value: "142.7", year: "2026",
  },
} as const);

const CHECKS = Object.freeze([
  "schema-and-content", "compile-time-capture-admission", "full-projection-material",
  "fixed-no-egress-policy", "normalised-parameters", "exact-result-core", "software-identity",
] as const);

export class Web216CpihReceiptError extends TypeError {
  public constructor(message: string) {
    super(message);
    this.name = "Web216CpihReceiptError";
  }
}

function fail(message: string): never { throw new Web216CpihReceiptError(message); }

function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    fail("Expected a closed JSON object");
  }
  return value as Record<string, unknown>;
}

function exactKeys(value: Record<string, unknown>, keys: readonly string[]): void {
  if (Object.keys(value).length !== keys.length || keys.some((key) => !Object.hasOwn(value, key))) {
    fail("Unexpected or missing property");
  }
}

function period(value: unknown): Web216CpihPeriod {
  if (value !== "2026-01" && value !== "2026-07") fail("Period is not compile-time admitted");
  return value;
}

function assertProjection(value: unknown): void {
  const projection = object(canonicalJsonClone(value));
  const { projection_sha256: expected, ...body } = projection;
  const bytes = canonicalJsonBytes(body);
  if (bytes.length > 16_384 || expected !== WEB216_CPIH_CAPTURE.projection_sha256 ||
      createHash("sha256").update(bytes).digest("hex") !== WEB216_CPIH_CAPTURE.projection_sha256) {
    fail("Projection does not match the compile-time admitted complete material");
  }
  // Equality with a pinned whole-projection digest also closes every nested shape;
  // a caller cannot admit a substituted series, value, URL, hash or metadata field
  // by recomputing its own hash. The original raw-body hash declarations remain
  // provenance, not a claim that absent original bodies were verified here.
}

function resultFor(selected: Web216CpihPeriod) {
  return canonicalJsonClone({
    schema: "gis-ai-go.web216-cpih-result-core.v1",
    state: "validated-captured-observation",
    series: SERIES,
    period: selected,
    observation: OBSERVATIONS[selected],
    capture: WEB216_CPIH_CAPTURE,
    currency: "as-of-recorded-capture-not-always-current",
    provider_egress: false,
    attribution: "Source: Office for National Statistics",
    rights_basis: {
      terms_uri: "https://www.ons.gov.uk/help/terms-conditions",
      scope: "general-ONS-terms-not-a-record-specific-legal-audit",
    },
  } as const);
}

export type Web216CpihResultCore = ReturnType<typeof resultFor>;

/** Schema constants only, not evidence that a query or source retrieval occurred. */
export const WEB216_CPIH_RESULT_CORES = canonicalJsonClone({
  "2026-01": resultFor("2026-01"),
  "2026-07": resultFor("2026-07"),
} as const);

/** Project one exact admitted row; decimal text and source-native dates stay intact. */
export function buildWeb216CpihResult(projection: unknown, selected: Web216CpihPeriod): Web216CpihResultCore {
  const admitted = period(selected);
  assertProjection(projection);
  return resultFor(admitted);
}

export interface Web216CpihReceiptBuildInput {
  readonly projection: unknown;
  readonly period: Web216CpihPeriod;
  readonly requestId: string;
  readonly traceId: string;
  readonly createdAt: string;
  readonly software: EvidenceSoftwareIdentity;
}

/** Only UTC timestamps are emitted here; preserve up to nanosecond source precision. */
function epochNanoseconds(value: unknown): bigint {
  if (!isStrictEvidenceDateTime(value)) fail("Invalid evidence date-time");
  const match = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z$/u.exec(value);
  if (match === null) fail("Evidence date-time must be UTC with bounded precision");
  const milliseconds = Date.parse(`${match[1]}Z`);
  if (!Number.isFinite(milliseconds)) fail("Evidence date-time is not representable");
  return BigInt(milliseconds) * 1_000_000n + BigInt((match[2] ?? "").padEnd(9, "0"));
}

function assertSoftware(value: unknown): asserts value is EvidenceSoftwareIdentity {
  const software = object(value);
  exactKeys(software, ["name", "version", "revision"]);
  if (software.name !== "gis-ai-go-mcp-gateway" || typeof software.version !== "string" ||
      software.version.length > 32 ||
      !/^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$/u.test(software.version) ||
      typeof software.revision !== "string" || !/^[0-9a-f]{40}$/u.test(software.revision)) {
    fail("Software must identify an exact gateway semantic version and Git revision");
  }
}

function receiptFor(input: Omit<Web216CpihReceiptBuildInput, "projection">) {
  const selected = period(input.period);
  if (typeof input.requestId !== "string" || input.requestId.length > 128 ||
      !/^[A-Za-z0-9][A-Za-z0-9._:-]*$/u.test(input.requestId) ||
      typeof input.traceId !== "string" || !/^[0-9a-f]{32}$/u.test(input.traceId)) {
    fail("Invalid bounded request or trace identifier");
  }
  if (epochNanoseconds(input.createdAt) < epochNanoseconds(WEB216_CPIH_CAPTURE.captured_at)) {
    fail("Receipt cannot precede the admitted capture");
  }
  assertSoftware(input.software);
  const core = {
    schema: "gis-ai-go.web216-cpih-receipt.v1",
    canonicalisation: CANONICALISATION,
    created_at: input.createdAt,
    request_id: input.requestId,
    trace_id: input.traceId,
    operation: {
      name: "read-validated-cpih-capture",
      contract_version: "v1",
      period: selected,
      normalised_parameters: canonicalDigest(WEB216_CPIH_DOMAINS.parameters, { period: selected }),
    },
    result: canonicalDigest(WEB216_CPIH_DOMAINS.result, resultFor(selected)),
    capture: WEB216_CPIH_CAPTURE,
    policy_scope: WEB216_CPIH_POLICY_SCOPE,
    software: input.software,
    outcome: "success",
    execution_scope: "experimental-pinned-capture-read-not-live-provider-evidence",
    evidence: {
      delivery: "inline-only", persistence: "not-persisted", attestation: "not-attested",
    },
  } as const;
  return canonicalJsonClone({
    ...core,
    receipt_id: contentAddress("gis-ai-go:evidence-receipt", WEB216_CPIH_DOMAINS.receipt, core),
  });
}

export type Web216CpihReceipt = ReturnType<typeof receiptFor>;

export function buildWeb216CpihReceipt(input: Web216CpihReceiptBuildInput): Web216CpihReceipt {
  const snapshot = canonicalJsonClone(input);
  exactKeys(object(snapshot), ["projection", "period", "requestId", "traceId", "createdAt", "software"]);
  assertProjection(snapshot.projection);
  return receiptFor(snapshot);
}

/**
 * Reconstruct the entire allowed receipt, including nested fields and its ID.
 * This structural check cannot prove possession of the captured source material.
 */
export function verifyWeb216CpihReceiptStructure(value: unknown): boolean {
  try {
    const receipt = object(canonicalJsonClone(value));
    const operation = object(receipt.operation);
    const expected = receiptFor({
      period: period(operation.period),
      requestId: receipt.request_id as string,
      traceId: receipt.trace_id as string,
      createdAt: receipt.created_at as string,
      software: receipt.software as EvidenceSoftwareIdentity,
    });
    return canonicalJson(receipt) === canonicalJson(expected);
  } catch { return false; }
}

export interface Web216CpihReceiptVerificationMaterial {
  readonly projection: unknown;
  readonly normalisedParameters: { readonly period: Web216CpihPeriod };
  readonly resultCore: Web216CpihResultCore;
  readonly expectedSoftware: EvidenceSoftwareIdentity;
}

export interface Web216CpihReceiptVerificationResult {
  readonly valid: boolean;
  readonly checks: readonly string[];
  readonly errors: readonly string[];
}

/** Full material equality, not an attestation, durable reference or permission grant. */
export function verifyWeb216CpihReceipt(
  value: unknown,
  material: Web216CpihReceiptVerificationMaterial,
): Web216CpihReceiptVerificationResult {
  try {
    const receipt = canonicalJsonClone(value) as Web216CpihReceipt;
    const snapshot = canonicalJsonClone(material);
    exactKeys(object(snapshot), ["projection", "normalisedParameters", "resultCore", "expectedSoftware"]);
    if (!verifyWeb216CpihReceiptStructure(receipt)) fail("Receipt structure or content is invalid");
    assertProjection(snapshot.projection);
    if (canonicalJson(snapshot.normalisedParameters) !== canonicalJson({ period: receipt.operation.period })) {
      fail("Normalised parameters differ from the admitted receipt selection");
    }
    if (canonicalJson(snapshot.resultCore) !== canonicalJson(resultFor(receipt.operation.period))) {
      fail("Result core differs from the exact admitted observation and metadata");
    }
    assertSoftware(snapshot.expectedSoftware);
    if (canonicalJson(snapshot.expectedSoftware) !== canonicalJson(receipt.software)) {
      fail("Software identity differs from the expected build");
    }
    return canonicalJsonClone({ valid: true, checks: CHECKS, errors: [] });
  } catch (error) {
    const message = error instanceof Web216CpihReceiptError
      ? error.message : "CPIH receipt verification failed closed";
    return canonicalJsonClone({ valid: false, checks: [], errors: [message] });
  }
}
