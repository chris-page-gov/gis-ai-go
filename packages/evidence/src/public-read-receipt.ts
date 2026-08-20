import {
  CanonicalJsonError,
  canonicalJson,
  canonicalJsonClone,
} from "./canonical-json.js";
import {
  CANONICAL_DOMAINS,
  canonicalDigest,
  contentAddress,
  domainSeparatedSha256,
  verifyContentAddress,
  verifyDomainSeparatedSha256,
  type CanonicalDigest,
} from "./digest.js";
import {
  CANONICALISATION,
  GOVERNED_OPERATIONS,
  type EvidenceSoftwareIdentity,
  type GovernedOperation,
} from "./receipt.js";

const SHA40 = /^[0-9a-f]{40}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const SEMVER = /^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$/u;
const DATE_TIME =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/u;

const AUTHORITY_ID_PREFIX = "gis-ai-go:public-authority-context";
const POLICY_ID_PREFIX = "gis-ai-go:public-policy";
const DECISION_ID_PREFIX = "gis-ai-go:public-policy-decision";
const RECEIPT_ID_PREFIX = "gis-ai-go:evidence-receipt";
const RESOURCE_ID_PREFIX = "gis-ai-go:public-read-resource";
const MAX_NORMALISED_PARAMETERS_BYTES = 16_384;
const MAX_RESULT_CORE_BYTES = 262_144;

export const PUBLIC_READ_AUTHORITY_CONTEXT_ID =
  "gis-ai-go:public-authority-context:sha256:5d97a93aaa9c8fcbf9f02d2812275cf59b4c0e0e923de89ac975035c741bc1f1";
export const PUBLIC_READ_POLICY_ID =
  "gis-ai-go:public-policy:sha256:b1a37b2ebf6900e2b5d62dfa20bcdaa1232e1c4c9f9630f90ac9d3dde738624a";

export const PUBLIC_READ_OPERATIONS = Object.freeze([
  "data.query",
  "selection.resolve",
] as const);
export type PublicReadOperation = (typeof PUBLIC_READ_OPERATIONS)[number];

export const SELECTION_RESOLVE_OBLIGATIONS = Object.freeze([
  "inline-evidence-receipt",
  "no-provider-execution",
  "not-attested",
  "not-persisted",
  "preserve-attribution",
  "preserve-provider-identifiers",
  "preserve-provider-rights",
  "preserve-provider-version",
] as const);

export const DATA_QUERY_OBLIGATIONS = Object.freeze([
  "bounded-single-observation",
  "inline-evidence-receipt",
  "not-attested",
  "not-persisted",
  "preserve-attribution",
  "preserve-provider-identifiers",
  "preserve-provider-rights",
  "preserve-provider-version",
] as const);

export type PublicReadPolicyObligation =
  | (typeof SELECTION_RESOLVE_OBLIGATIONS)[number]
  | (typeof DATA_QUERY_OBLIGATIONS)[number];

export interface PublicReadResourceCore {
  readonly schema: "gis-ai-go.public-read-resource.v1";
  readonly publication: {
    readonly classification: "public";
    readonly access_tier: "open";
    readonly authentication: "none";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
    readonly read_only: true;
  };
  readonly profile: {
    readonly id: "PV-ONS-DATA";
    readonly sha256: "535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622";
    readonly source_path: "docs/research/2026-08-19/research-pack/data/providers.json";
    readonly source_pointer: "/providers/1";
  };
  readonly provider: {
    readonly id: "ons-data-api";
    readonly adapter_id: "gis-ai-go.ons-data-api";
    readonly adapter_version: "1";
  };
  readonly dataset: {
    readonly id: "weekly-deaths-region";
    readonly edition: "time-series";
    readonly version: "121";
    readonly version_uri: "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121";
    readonly source_date: "2026-07-01";
    readonly dimension_order: readonly ["time", "geography", "week", "causeofdeath"];
  };
  readonly selections: readonly [
    { readonly dimension: "time"; readonly option: "2026" },
    { readonly dimension: "geography"; readonly option: "E92000001" },
    { readonly dimension: "week"; readonly option: "week-24" },
    { readonly dimension: "causeofdeath"; readonly option: "all-causes" },
  ];
  readonly rights: {
    readonly state: "open-with-conditions";
    readonly licence: "Open Government Licence v3.0";
    readonly licence_uri: "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/";
    readonly attribution: "Source: Office for National Statistics licensed under the Open Government Licence v.3.0";
    readonly obligations: readonly [
      "Acknowledge the source and licence when reproducing the selected ONS content.",
      "Preserve the selected dataset, edition, version and release date.",
      "Do not imply that ONS endorses GIS AI GO or its interpretation.",
    ];
    readonly exceptions: readonly [
      "The ONS logo is excluded and is not retrieved or redistributed.",
      "Any record-level third-party exception overrides this general evidence and must fail closed.",
      "The selected aggregate dataset page stated no additional exception when reviewed.",
    ];
    readonly evidence_uris: readonly [
      "https://www.ons.gov.uk/datasets/weekly-deaths-region/editions/time-series/versions/121",
      "https://www.ons.gov.uk/help/terms-conditions",
      "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    ];
    readonly reviewed_at: "2026-08-20T17:40:35Z";
  };
  readonly limits: {
    readonly max_observations: 1;
    readonly max_attempts: 2;
    readonly max_compressed_response_bytes: 262144;
    readonly max_decompressed_response_bytes: 1048576;
    readonly max_canonical_response_bytes: 262144;
  };
  readonly output: {
    readonly media_type: "application/json";
    readonly spatial: false;
    readonly crs: null;
    readonly axis_order: null;
  };
}

export interface PublicReadResource extends PublicReadResourceCore {
  readonly resource_id: string;
}

export interface PublicReadAuthorityContextCore {
  readonly schema: "gis-ai-go.public-authority-context.v2";
  readonly canonicalisation: typeof CANONICALISATION;
  readonly construction: {
    readonly source: "server";
    readonly profile: "anonymous-open";
    readonly product: "gis-ai-go-gateway";
  };
  readonly access: {
    readonly authentication: "none";
    readonly tier: "open";
    readonly publication_classification: "public";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
    readonly read_only: true;
  };
  readonly permitted_operations: readonly ["data.query", "selection.resolve"];
  readonly evidence: {
    readonly receipt: "inline-required";
    readonly persistence: "not-persisted";
    readonly attestation: "not-attested";
  };
}

export interface PublicReadAuthorityContext extends PublicReadAuthorityContextCore {
  readonly context_id: string;
}

export interface PublicReadPolicyRule {
  readonly rule_id:
    | "public-data-query-ons-v121"
    | "public-selection-resolve-ons-v121";
  readonly operation: PublicReadOperation;
  readonly resource_id: string;
  readonly effect: "allow-with-obligations";
  readonly obligations: readonly PublicReadPolicyObligation[];
}

export interface PublicReadPolicyCore {
  readonly schema: "gis-ai-go.public-policy.v2";
  readonly version: "2.0.0";
  readonly canonicalisation: typeof CANONICALISATION;
  readonly compilation: {
    readonly kind: "compiled-json";
    readonly runtime: "gis-ai-go-gateway";
  };
  readonly default_effect: "deny";
  readonly applies_to: {
    readonly authority_profile: "anonymous-open";
    readonly access_tier: "open";
    readonly publication_classification: "public";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
    readonly read_only: true;
  };
  readonly resources: readonly [PublicReadResource];
  readonly rules: readonly [PublicReadPolicyRule, PublicReadPolicyRule];
}

export interface PublicReadPolicy extends PublicReadPolicyCore {
  readonly policy_id: string;
}

export type PublicReadPolicyReasonCode =
  | "authority-context-not-applicable"
  | "operation-not-allowed"
  | "public-read-operation-allowed"
  | "resource-not-approved";

export interface PublicReadPolicyDecisionCore {
  readonly schema: "gis-ai-go.public-policy-decision.v2";
  readonly canonicalisation: typeof CANONICALISATION;
  readonly request_id: string;
  readonly trace_id: string;
  readonly authority_context_id: string;
  readonly policy_id: string;
  readonly policy_version: "2.0.0";
  readonly policy_default_effect: "deny";
  readonly operation: GovernedOperation;
  readonly resource_id: string | null;
  readonly effect: "allow-with-obligations" | "deny";
  readonly reason_code: PublicReadPolicyReasonCode;
  readonly obligations: readonly PublicReadPolicyObligation[];
}

export interface PublicReadPolicyDecision extends PublicReadPolicyDecisionCore {
  readonly decision_id: string;
}

export type PublicReadTransformationName =
  | "execute-fixed-provider-query"
  | "normalise-public-read-parameters"
  | "project-public-read-result-core"
  | "resolve-fixed-selection-profile";

export interface PublicReadTransformation {
  readonly name: PublicReadTransformationName;
  readonly version: "v1";
}

export interface PublicReadResultEvidenceBinding {
  readonly resource_id: string;
  readonly profile_sha256: string;
  readonly provider_id: string;
  readonly adapter_id: string;
  readonly dataset_id: string;
  readonly edition: string;
  readonly version: string;
  readonly rights_sha256: string;
  readonly returned_item_count: 1;
}

export const PUBLIC_READ_RECEIPT_VERIFICATION_CHECKS = Object.freeze([
  "authority-context",
  "normalised-parameters-digest",
  "profile-binding",
  "provider-binding",
  "provider-rights",
  "public-policy-decision",
  "result-core-digest",
  "schema",
] as const);
export type PublicReadReceiptVerificationCheck =
  (typeof PUBLIC_READ_RECEIPT_VERIFICATION_CHECKS)[number];

export interface PublicReadEvidenceReceiptCore {
  readonly schema: "gis-ai-go.evidence-receipt.v2";
  readonly created_at: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly operation: {
    readonly name: PublicReadOperation;
    readonly contract_version: "v1";
    readonly normalised_parameters:
      | CanonicalDigest<"gis-ai-go.data-query-parameters.v1">
      | CanonicalDigest<"gis-ai-go.selection-resolve-parameters.v1">;
  };
  readonly authority_context: PublicReadAuthorityContext;
  readonly policy_decision: PublicReadPolicyDecision;
  readonly resource: PublicReadResource;
  readonly transformations: readonly PublicReadTransformation[];
  readonly software: EvidenceSoftwareIdentity;
  readonly result: {
    readonly domain:
      | "gis-ai-go.data-query-result-core.v1"
      | "gis-ai-go.selection-resolve-result-core.v1";
    readonly sha256: string;
    readonly media_type: "application/json";
    readonly returned_item_count: 1;
  };
  readonly verification: {
    readonly status: "passed";
    readonly canonicalisation: typeof CANONICALISATION;
    readonly digest_algorithm: "sha256";
    readonly checks: readonly PublicReadReceiptVerificationCheck[];
  };
  readonly evidence_handling: {
    readonly delivery: "inline-only";
    readonly persistence: "not-persisted";
    readonly attestation: "not-attested";
  };
}

export interface PublicReadEvidenceReceipt extends PublicReadEvidenceReceiptCore {
  readonly receipt_id: string;
}

export interface PublicReadReceiptBuildInput {
  readonly createdAt: string;
  readonly requestId: string;
  readonly traceId: string;
  readonly operation: PublicReadOperation;
  /** Only the operation-specific digest is retained. */
  readonly normalisedParameters: unknown;
  readonly authorityContext: PublicReadAuthorityContext;
  readonly publicPolicy: PublicReadPolicy;
  readonly policyDecision: PublicReadPolicyDecision;
  readonly resource: PublicReadResource;
  readonly transformations: readonly PublicReadTransformation[];
  readonly software: EvidenceSoftwareIdentity;
  /** Successful receipt-free result. Denials and ambiguity are not success material. */
  readonly resultCore: unknown;
}

export interface PublicReadReceiptVerificationMaterial {
  readonly normalisedParameters: unknown;
  readonly resultCore: unknown;
  readonly publicPolicy: PublicReadPolicy;
  readonly expectedAuthorityContext?: PublicReadAuthorityContext;
  readonly expectedPolicyDecision?: PublicReadPolicyDecision;
  readonly expectedResource?: PublicReadResource;
  readonly expectedSoftware?: EvidenceSoftwareIdentity;
}

export interface PublicReadReceiptVerificationResult {
  readonly valid: boolean;
  readonly checks: readonly PublicReadReceiptVerificationCheck[];
  readonly errors: readonly string[];
}

export class PublicReadReceiptError extends TypeError {
  public constructor(public readonly path: string, message: string) {
    super(`Public-read evidence rejected ${path}: ${message}`);
    this.name = "PublicReadReceiptError";
  }
}

function fail(path: string, message: string): never {
  throw new PublicReadReceiptError(path, message);
}

function snapshotAt<T>(value: unknown, path: string): T {
  try {
    return canonicalJsonClone(value) as T;
  } catch {
    return fail(path, "must be detached canonical JSON without proxies or accessors");
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

function recordAt(value: unknown, path: string): Record<string, unknown> {
  if (!isRecord(value)) return fail(path, "must be a plain object");
  return value;
}

function assertExactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
  path: string,
): void {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    fail(path, "has an unexpected or missing property");
  }
}

function stringAt(value: unknown, path: string, maximum: number): string {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    Array.from(value).length > maximum
  ) {
    return fail(path, `must be a non-empty string of at most ${maximum} Unicode characters`);
  }
  return value;
}

function assertRequestId(value: unknown, path: string): asserts value is string {
  if (typeof value !== "string" || value.length > 128 || !REQUEST_ID.test(value)) {
    fail(path, "must be a valid bounded request identifier");
  }
}

function assertTraceId(value: unknown, path: string): asserts value is string {
  if (typeof value !== "string" || !TRACE_ID.test(value)) {
    fail(path, "must be 32 lower-case hexadecimal characters");
  }
}

function assertDateTime(value: unknown, path: string): asserts value is string {
  if (
    typeof value !== "string" ||
    value.length > 35 ||
    !DATE_TIME.test(value) ||
    !Number.isFinite(Date.parse(value))
  ) {
    fail(path, "must be a valid bounded RFC 3339 date-time");
  }
}

function assertContentId(value: unknown, prefix: string, path: string): asserts value is string {
  const marker = `${prefix}:sha256:`;
  if (
    typeof value !== "string" ||
    !value.startsWith(marker) ||
    !SHA256.test(value.slice(marker.length))
  ) {
    fail(path, "must be a content-addressed SHA-256 identifier in the expected domain");
  }
}

function sameCanonical(left: unknown, right: unknown): boolean {
  return canonicalJson(left) === canonicalJson(right);
}

function identityCore(
  value: unknown,
  identityKey: string,
  path: string,
): { readonly identity: string; readonly core: Record<string, unknown> } {
  const record = recordAt(value, path);
  const identity = record[identityKey];
  if (typeof identity !== "string") return fail(`${path}.${identityKey}`, "must be a string");
  return {
    identity,
    core: Object.fromEntries(Object.entries(record).filter(([key]) => key !== identityKey)),
  };
}

function buildIdentity<TCore, TDocument>(
  core: TCore,
  identityKey: string,
  prefix: string,
  domain: string,
): TDocument {
  const canonicalCore = canonicalJsonClone(core);
  return canonicalJsonClone({
    ...canonicalCore,
    [identityKey]: contentAddress(prefix, domain, canonicalCore),
  }) as TDocument;
}

function expectedObligations(operation: PublicReadOperation): readonly PublicReadPolicyObligation[] {
  return operation === "data.query"
    ? DATA_QUERY_OBLIGATIONS
    : SELECTION_RESOLVE_OBLIGATIONS;
}

function expectedRule(operation: PublicReadOperation, resourceId: string): PublicReadPolicyRule {
  return {
    rule_id:
      operation === "data.query"
        ? "public-data-query-ons-v121"
        : "public-selection-resolve-ons-v121",
    operation,
    resource_id: resourceId,
    effect: "allow-with-obligations",
    obligations: expectedObligations(operation),
  };
}

export const PUBLIC_READ_ONS_RESOURCE_CORE: PublicReadResourceCore = canonicalJsonClone({
  schema: "gis-ai-go.public-read-resource.v1",
  publication: {
    classification: "public",
    access_tier: "open",
    authentication: "none",
    contains_personal_data: false,
    contains_protected_data: false,
    read_only: true,
  },
  profile: {
    id: "PV-ONS-DATA",
    sha256: "535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622",
    source_path: "docs/research/2026-08-19/research-pack/data/providers.json",
    source_pointer: "/providers/1",
  },
  provider: {
    id: "ons-data-api",
    adapter_id: "gis-ai-go.ons-data-api",
    adapter_version: "1",
  },
  dataset: {
    id: "weekly-deaths-region",
    edition: "time-series",
    version: "121",
    version_uri:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
    source_date: "2026-07-01",
    dimension_order: ["time", "geography", "week", "causeofdeath"],
  },
  selections: [
    { dimension: "time", option: "2026" },
    { dimension: "geography", option: "E92000001" },
    { dimension: "week", option: "week-24" },
    { dimension: "causeofdeath", option: "all-causes" },
  ],
  rights: {
    state: "open-with-conditions",
    licence: "Open Government Licence v3.0",
    licence_uri: "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
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
    evidence_uris: [
      "https://www.ons.gov.uk/datasets/weekly-deaths-region/editions/time-series/versions/121",
      "https://www.ons.gov.uk/help/terms-conditions",
      "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    ],
    reviewed_at: "2026-08-20T17:40:35Z",
  },
  limits: {
    max_observations: 1,
    max_attempts: 2,
    max_compressed_response_bytes: 262_144,
    max_decompressed_response_bytes: 1_048_576,
    max_canonical_response_bytes: 262_144,
  },
  output: {
    media_type: "application/json",
    spatial: false,
    crs: null,
    axis_order: null,
  },
});

export function buildPublicReadResource(core: PublicReadResourceCore): PublicReadResource {
  const snapshot = snapshotAt<PublicReadResourceCore>(core, "$.resource");
  if (!sameCanonical(snapshot, PUBLIC_READ_ONS_RESOURCE_CORE)) {
    fail("$.resource", "must be the exact reviewed ONS public-read resource");
  }
  return buildIdentity<PublicReadResourceCore, PublicReadResource>(
    snapshot,
    "resource_id",
    RESOURCE_ID_PREFIX,
    CANONICAL_DOMAINS.publicReadResource,
  );
}

export const PUBLIC_READ_ONS_RESOURCE = buildPublicReadResource(PUBLIC_READ_ONS_RESOURCE_CORE);

export function verifyPublicReadResource(value: unknown): value is PublicReadResource {
  try {
    const snapshot = snapshotAt<PublicReadResource>(value, "$.resource");
    const { identity, core } = identityCore(snapshot, "resource_id", "$.resource");
    assertContentId(identity, RESOURCE_ID_PREFIX, "$.resource.resource_id");
    if (!sameCanonical(core, PUBLIC_READ_ONS_RESOURCE_CORE)) {
      fail("$.resource", "does not match the exact reviewed ONS boundary");
    }
    if (
      !verifyContentAddress(
        identity,
        RESOURCE_ID_PREFIX,
        CANONICAL_DOMAINS.publicReadResource,
        core,
      )
    ) {
      fail("$.resource.resource_id", "does not match the canonical resource content");
    }
    return true;
  } catch {
    return false;
  }
}

function assertAuthorityCore(value: unknown, includeIdentity: boolean): void {
  const authority = recordAt(value, "$.authority_context");
  assertExactKeys(
    authority,
    [
      "access",
      "canonicalisation",
      "construction",
      ...(includeIdentity ? ["context_id"] : []),
      "evidence",
      "permitted_operations",
      "schema",
    ],
    "$.authority_context",
  );
  if (
    authority.schema !== "gis-ai-go.public-authority-context.v2" ||
    authority.canonicalisation !== CANONICALISATION ||
    !sameCanonical(authority.permitted_operations, PUBLIC_READ_OPERATIONS)
  ) {
    fail("$.authority_context", "must identify the closed public-read v2 authority");
  }
  const construction = recordAt(authority.construction, "$.authority_context.construction");
  assertExactKeys(construction, ["product", "profile", "source"], "$.authority_context.construction");
  const access = recordAt(authority.access, "$.authority_context.access");
  assertExactKeys(
    access,
    [
      "authentication",
      "contains_personal_data",
      "contains_protected_data",
      "publication_classification",
      "read_only",
      "tier",
    ],
    "$.authority_context.access",
  );
  const evidence = recordAt(authority.evidence, "$.authority_context.evidence");
  assertExactKeys(evidence, ["attestation", "persistence", "receipt"], "$.authority_context.evidence");
  if (
    construction.source !== "server" ||
    construction.profile !== "anonymous-open" ||
    construction.product !== "gis-ai-go-gateway" ||
    access.authentication !== "none" ||
    access.tier !== "open" ||
    access.publication_classification !== "public" ||
    access.contains_personal_data !== false ||
    access.contains_protected_data !== false ||
    access.read_only !== true ||
    evidence.receipt !== "inline-required" ||
    evidence.persistence !== "not-persisted" ||
    evidence.attestation !== "not-attested"
  ) {
    fail("$.authority_context", "contains an unsupported authority or evidence claim");
  }
  if (includeIdentity) {
    assertContentId(authority.context_id, AUTHORITY_ID_PREFIX, "$.authority_context.context_id");
  }
}

export function buildPublicReadAuthorityContext(
  core: PublicReadAuthorityContextCore,
): PublicReadAuthorityContext {
  const snapshot = snapshotAt<PublicReadAuthorityContextCore>(core, "$.authority_context");
  assertAuthorityCore(snapshot, false);
  return buildIdentity<PublicReadAuthorityContextCore, PublicReadAuthorityContext>(
    snapshot,
    "context_id",
    AUTHORITY_ID_PREFIX,
    CANONICAL_DOMAINS.authorityContextV2,
  );
}

export function verifyPublicReadAuthorityContext(
  value: unknown,
): value is PublicReadAuthorityContext {
  try {
    const snapshot = snapshotAt<PublicReadAuthorityContext>(value, "$.authority_context");
    assertAuthorityCore(snapshot, true);
    const { identity, core } = identityCore(snapshot, "context_id", "$.authority_context");
    return verifyContentAddress(
      identity,
      AUTHORITY_ID_PREFIX,
      CANONICAL_DOMAINS.authorityContextV2,
      core,
    );
  } catch {
    return false;
  }
}

function assertRule(value: unknown, operation: PublicReadOperation, resourceId: string): void {
  const rule = recordAt(value, `$.public_policy.rules.${operation}`);
  assertExactKeys(
    rule,
    ["effect", "obligations", "operation", "resource_id", "rule_id"],
    `$.public_policy.rules.${operation}`,
  );
  if (!sameCanonical(rule, expectedRule(operation, resourceId))) {
    fail(`$.public_policy.rules.${operation}`, "must be the exact operation-specific allow rule");
  }
}

function assertPolicyCore(value: unknown, includeIdentity: boolean): void {
  const policy = recordAt(value, "$.public_policy");
  assertExactKeys(
    policy,
    [
      "applies_to",
      "canonicalisation",
      "compilation",
      "default_effect",
      ...(includeIdentity ? ["policy_id"] : []),
      "resources",
      "rules",
      "schema",
      "version",
    ],
    "$.public_policy",
  );
  if (
    policy.schema !== "gis-ai-go.public-policy.v2" ||
    policy.version !== "2.0.0" ||
    policy.canonicalisation !== CANONICALISATION ||
    policy.default_effect !== "deny"
  ) {
    fail("$.public_policy", "must be the compiled default-deny public-read v2 policy");
  }
  const compilation = recordAt(policy.compilation, "$.public_policy.compilation");
  assertExactKeys(compilation, ["kind", "runtime"], "$.public_policy.compilation");
  const applies = recordAt(policy.applies_to, "$.public_policy.applies_to");
  assertExactKeys(
    applies,
    [
      "access_tier",
      "authority_profile",
      "contains_personal_data",
      "contains_protected_data",
      "publication_classification",
      "read_only",
    ],
    "$.public_policy.applies_to",
  );
  if (
    compilation.kind !== "compiled-json" ||
    compilation.runtime !== "gis-ai-go-gateway" ||
    applies.authority_profile !== "anonymous-open" ||
    applies.access_tier !== "open" ||
    applies.publication_classification !== "public" ||
    applies.contains_personal_data !== false ||
    applies.contains_protected_data !== false ||
    applies.read_only !== true
  ) {
    fail("$.public_policy", "contains unsupported compilation or publication semantics");
  }
  if (
    !Array.isArray(policy.resources) ||
    policy.resources.length !== 1 ||
    !verifyPublicReadResource(policy.resources[0])
  ) {
    fail("$.public_policy.resources", "must contain only the reviewed ONS resource");
  }
  if (!Array.isArray(policy.rules) || policy.rules.length !== 2) {
    fail("$.public_policy.rules", "must contain exactly two ordered allow rules");
  }
  assertRule(policy.rules[0], "data.query", PUBLIC_READ_ONS_RESOURCE.resource_id);
  assertRule(policy.rules[1], "selection.resolve", PUBLIC_READ_ONS_RESOURCE.resource_id);
  if (includeIdentity) {
    assertContentId(policy.policy_id, POLICY_ID_PREFIX, "$.public_policy.policy_id");
  }
}

export function buildPublicReadPolicy(core: PublicReadPolicyCore): PublicReadPolicy {
  const snapshot = snapshotAt<PublicReadPolicyCore>(core, "$.public_policy");
  assertPolicyCore(snapshot, false);
  return buildIdentity<PublicReadPolicyCore, PublicReadPolicy>(
    snapshot,
    "policy_id",
    POLICY_ID_PREFIX,
    CANONICAL_DOMAINS.publicPolicyV2,
  );
}

export function verifyPublicReadPolicy(value: unknown): value is PublicReadPolicy {
  try {
    const snapshot = snapshotAt<PublicReadPolicy>(value, "$.public_policy");
    assertPolicyCore(snapshot, true);
    const { identity, core } = identityCore(snapshot, "policy_id", "$.public_policy");
    return verifyContentAddress(identity, POLICY_ID_PREFIX, CANONICAL_DOMAINS.publicPolicyV2, core);
  } catch {
    return false;
  }
}

function assertDecisionCore(value: unknown, includeIdentity: boolean): void {
  const decision = recordAt(value, "$.policy_decision");
  assertExactKeys(
    decision,
    [
      "authority_context_id",
      "canonicalisation",
      ...(includeIdentity ? ["decision_id"] : []),
      "effect",
      "obligations",
      "operation",
      "policy_default_effect",
      "policy_id",
      "policy_version",
      "reason_code",
      "request_id",
      "resource_id",
      "schema",
      "trace_id",
    ],
    "$.policy_decision",
  );
  if (
    decision.schema !== "gis-ai-go.public-policy-decision.v2" ||
    decision.canonicalisation !== CANONICALISATION ||
    decision.policy_version !== "2.0.0" ||
    decision.policy_default_effect !== "deny" ||
    !GOVERNED_OPERATIONS.includes(decision.operation as GovernedOperation)
  ) {
    fail("$.policy_decision", "must identify a governed public-read v2 decision");
  }
  assertRequestId(decision.request_id, "$.policy_decision.request_id");
  assertTraceId(decision.trace_id, "$.policy_decision.trace_id");
  if (decision.authority_context_id !== PUBLIC_READ_AUTHORITY_CONTEXT_ID) {
    fail("$.policy_decision.authority_context_id", "must identify the exact public-read authority");
  }
  if (decision.policy_id !== PUBLIC_READ_POLICY_ID) {
    fail("$.policy_decision.policy_id", "must identify the exact checked public-read policy");
  }
  if (!Array.isArray(decision.obligations)) {
    fail("$.policy_decision.obligations", "must be an array");
  }
  if (decision.effect === "allow-with-obligations") {
    if (
      !PUBLIC_READ_OPERATIONS.includes(decision.operation as PublicReadOperation) ||
      decision.reason_code !== "public-read-operation-allowed" ||
      decision.resource_id !== PUBLIC_READ_ONS_RESOURCE.resource_id ||
      !sameCanonical(
        decision.obligations,
        expectedObligations(decision.operation as PublicReadOperation),
      )
    ) {
      fail("$.policy_decision", "does not express an exact allowed public-read operation");
    }
  } else {
    if (
      decision.effect !== "deny" ||
      decision.obligations.length !== 0 ||
      decision.resource_id !== null
    ) {
      fail("$.policy_decision", "must be a closed default-deny decision without obligations");
    }
    const isPublicRead = PUBLIC_READ_OPERATIONS.includes(
      decision.operation as PublicReadOperation,
    );
    const validReason =
      decision.reason_code === "authority-context-not-applicable" ||
      (decision.reason_code === "operation-not-allowed" && !isPublicRead) ||
      (decision.reason_code === "resource-not-approved" && isPublicRead);
    if (!validReason) {
      fail("$.policy_decision.reason_code", "contradicts the denied operation and resource");
    }
  }
  if (includeIdentity) {
    assertContentId(decision.decision_id, DECISION_ID_PREFIX, "$.policy_decision.decision_id");
  }
}

export function buildPublicReadPolicyDecision(
  core: PublicReadPolicyDecisionCore,
): PublicReadPolicyDecision {
  const snapshot = snapshotAt<PublicReadPolicyDecisionCore>(core, "$.policy_decision");
  assertDecisionCore(snapshot, false);
  return buildIdentity<PublicReadPolicyDecisionCore, PublicReadPolicyDecision>(
    snapshot,
    "decision_id",
    DECISION_ID_PREFIX,
    CANONICAL_DOMAINS.publicPolicyDecisionV2,
  );
}

export function verifyPublicReadPolicyDecision(
  value: unknown,
): value is PublicReadPolicyDecision {
  try {
    const snapshot = snapshotAt<PublicReadPolicyDecision>(value, "$.policy_decision");
    assertDecisionCore(snapshot, true);
    const { identity, core } = identityCore(snapshot, "decision_id", "$.policy_decision");
    return verifyContentAddress(
      identity,
      DECISION_ID_PREFIX,
      CANONICAL_DOMAINS.publicPolicyDecisionV2,
      core,
    );
  } catch {
    return false;
  }
}

function assertSoftware(value: unknown): asserts value is EvidenceSoftwareIdentity {
  const software = recordAt(value, "$.software");
  assertExactKeys(software, ["name", "revision", "version"], "$.software");
  if (
    software.name !== "gis-ai-go-mcp-gateway" ||
    typeof software.version !== "string" ||
    !SEMVER.test(software.version) ||
    typeof software.revision !== "string" ||
    !SHA40.test(software.revision)
  ) {
    fail("$.software", "must identify an exact gateway semantic version and Git revision");
  }
}

function expectedTransformations(
  operation: PublicReadOperation,
): readonly PublicReadTransformation[] {
  return operation === "data.query"
    ? [
        { name: "normalise-public-read-parameters", version: "v1" },
        { name: "execute-fixed-provider-query", version: "v1" },
        { name: "project-public-read-result-core", version: "v1" },
      ]
    : [
        { name: "normalise-public-read-parameters", version: "v1" },
        { name: "resolve-fixed-selection-profile", version: "v1" },
        { name: "project-public-read-result-core", version: "v1" },
      ];
}

function assertTransformations(value: unknown, operation: PublicReadOperation): void {
  if (!Array.isArray(value) || !sameCanonical(value, expectedTransformations(operation))) {
    fail("$.transformations", `must use the exact ordered ${operation} transformation pipeline`);
  }
}

function parameterDomain(operation: PublicReadOperation):
  | "gis-ai-go.data-query-parameters.v1"
  | "gis-ai-go.selection-resolve-parameters.v1" {
  return operation === "data.query"
    ? CANONICAL_DOMAINS.dataQueryParameters
    : CANONICAL_DOMAINS.selectionResolveParameters;
}

function resultDomain(operation: PublicReadOperation):
  | "gis-ai-go.data-query-result-core.v1"
  | "gis-ai-go.selection-resolve-result-core.v1" {
  return operation === "data.query"
    ? CANONICAL_DOMAINS.dataQueryResultCore
    : CANONICAL_DOMAINS.selectionResolveResultCore;
}

export function publicReadResultEvidenceBinding(
  resource: PublicReadResource = PUBLIC_READ_ONS_RESOURCE,
): PublicReadResultEvidenceBinding {
  const snapshot = snapshotAt<PublicReadResource>(resource, "$.resource");
  if (!verifyPublicReadResource(snapshot)) {
    fail("$.resource", "must be the exact reviewed ONS resource");
  }
  return canonicalJsonClone({
    resource_id: snapshot.resource_id,
    profile_sha256: snapshot.profile.sha256,
    provider_id: snapshot.provider.id,
    adapter_id: snapshot.provider.adapter_id,
    dataset_id: snapshot.dataset.id,
    edition: snapshot.dataset.edition,
    version: snapshot.dataset.version,
    rights_sha256: domainSeparatedSha256(CANONICAL_DOMAINS.providerRights, snapshot.rights),
    returned_item_count: 1,
  });
}

function assertFixedDataset(value: unknown, path: string, resource: PublicReadResource): void {
  const dataset = recordAt(value, path);
  assertExactKeys(dataset, ["edition", "id", "version"], path);
  if (
    dataset.id !== resource.dataset.id ||
    dataset.edition !== resource.dataset.edition ||
    dataset.version !== resource.dataset.version
  ) {
    fail(path, "must identify the exact reviewed dataset, edition and version");
  }
}

function assertFixedSelections(value: unknown, path: string, resource: PublicReadResource): void {
  if (!Array.isArray(value) || !sameCanonical(value, resource.selections)) {
    fail(path, "must contain the exact four provider-ordered selections");
  }
}

function assertNormalisedParameters(
  value: unknown,
  operation: PublicReadOperation,
  resource: PublicReadResource,
): void {
  const canonical = canonicalJson(value);
  if (new TextEncoder().encode(canonical).length > MAX_NORMALISED_PARAMETERS_BYTES) {
    fail("$.normalised_parameters", "exceeds the 16384-byte canonical parameter bound");
  }
  const parameters = recordAt(value, "$.normalised_parameters");
  if (operation === "data.query") {
    assertExactKeys(
      parameters,
      ["dataset", "limit", "resource_id", "schema", "selections"],
      "$.normalised_parameters",
    );
    if (
      parameters.schema !== "gis-ai-go.data-query-parameters.v1" ||
      parameters.resource_id !== resource.resource_id ||
      parameters.limit !== 1
    ) {
      fail("$.normalised_parameters", "must be the exact bounded data.query parameters");
    }
  } else {
    assertExactKeys(
      parameters,
      ["dataset", "profile_id", "provider_id", "schema", "selections"],
      "$.normalised_parameters",
    );
    if (
      parameters.schema !== "gis-ai-go.selection-resolve-parameters.v1" ||
      parameters.profile_id !== resource.profile.id ||
      parameters.provider_id !== resource.provider.id
    ) {
      fail("$.normalised_parameters", "must be the exact fixed selection parameters");
    }
  }
  assertFixedDataset(parameters.dataset, "$.normalised_parameters.dataset", resource);
  assertFixedSelections(parameters.selections, "$.normalised_parameters.selections", resource);
}

function assertObservation(value: unknown, path: string): void {
  const observation = recordAt(value, path);
  const keys = Object.keys(observation).sort();
  if (
    !(
      (keys.length === 1 && keys[0] === "value") ||
      (keys.length === 2 && keys[0] === "unit" && keys[1] === "value")
    )
  ) {
    fail(path, "must contain only value and the optional unit");
  }
  if (typeof observation.value !== "string" || Array.from(observation.value).length > 2_048) {
    fail(`${path}.value`, "must be a string of at most 2048 Unicode characters");
  }
  if (
    "unit" in observation &&
    observation.unit !== null &&
    (typeof observation.unit !== "string" ||
      observation.unit.length === 0 ||
      Array.from(observation.unit).length > 256)
  ) {
    fail(`${path}.unit`, "must be null or a non-empty string of at most 256 characters");
  }
}

function inspectResultCore(
  resultCore: unknown,
  operation: PublicReadOperation,
  requestId: string,
  traceId: string,
  resource: PublicReadResource,
): 1 {
  const canonical = canonicalJson(resultCore);
  if (new TextEncoder().encode(canonical).length > MAX_RESULT_CORE_BYTES) {
    fail("$.result_core", "exceeds the 262144-byte canonical result bound");
  }
  const result = recordAt(resultCore, "$.result_core");
  assertExactKeys(
    result,
    ["data", "evidence_binding", "operation", "request_id", "schema", "trace_id", "warnings"],
    "$.result_core",
  );
  const expectedSchema = operation === "data.query"
    ? "gis-ai-go.data-query-result.v1"
    : "gis-ai-go.selection-resolve-result.v1";
  if (
    result.schema !== expectedSchema ||
    result.operation !== operation ||
    result.request_id !== requestId ||
    result.trace_id !== traceId
  ) {
    fail("$.result_core", "schema, operation, request and trace must match the receipt");
  }
  const data = recordAt(result.data, "$.result_core.data");
  if (operation === "data.query") {
    assertExactKeys(data, ["observations", "status"], "$.result_core.data");
    if (data.status !== "succeeded") {
      fail("$.result_core.data.status", "must identify a successful data query");
    }
    if (!Array.isArray(data.observations) || data.observations.length !== 1) {
      fail("$.result_core.data.observations", "must contain exactly one observation");
    }
    assertObservation(data.observations[0], "$.result_core.data.observations[0]");
  } else {
    assertExactKeys(data, ["ambiguity", "resource_id", "status"], "$.result_core.data");
    if (
      data.status !== "resolved" ||
      data.ambiguity !== null ||
      data.resource_id !== resource.resource_id
    ) {
      fail("$.result_core.data", "must contain one unambiguous exact resource resolution");
    }
  }
  if (!sameCanonical(result.evidence_binding, publicReadResultEvidenceBinding(resource))) {
    fail("$.result_core.evidence_binding", "does not match the exact profile, provider and rights");
  }
  if (!Array.isArray(result.warnings) || result.warnings.length > 20) {
    fail("$.result_core.warnings", "must be a bounded warning array");
  }
  result.warnings.forEach((warning, index) =>
    stringAt(warning, `$.result_core.warnings[${index}]`, 1_024),
  );
  return 1;
}

function assertIdentityLinkage(
  authority: PublicReadAuthorityContext,
  policy: PublicReadPolicy,
  decision: PublicReadPolicyDecision,
  resource: PublicReadResource,
  operation: PublicReadOperation,
  requestId: string,
  traceId: string,
): void {
  if (!verifyPublicReadAuthorityContext(authority)) {
    fail("$.authority_context", "does not have a valid public-read v2 identity");
  }
  if (!verifyPublicReadPolicy(policy)) {
    fail("$.public_policy", "does not have a valid public-read v2 identity");
  }
  if (!verifyPublicReadPolicyDecision(decision)) {
    fail("$.policy_decision", "does not have a valid public-read v2 identity");
  }
  if (!verifyPublicReadResource(resource)) {
    fail("$.resource", "does not have the exact reviewed resource identity");
  }
  const rule = policy.rules.find((candidate) => candidate.operation === operation);
  if (
    !authority.permitted_operations.includes(operation) ||
    rule === undefined ||
    rule.resource_id !== resource.resource_id ||
    !sameCanonical(policy.resources[0], resource) ||
    decision.authority_context_id !== authority.context_id ||
    decision.policy_id !== policy.policy_id ||
    decision.policy_version !== policy.version ||
    decision.operation !== operation ||
    decision.resource_id !== resource.resource_id ||
    decision.request_id !== requestId ||
    decision.trace_id !== traceId ||
    decision.effect !== "allow-with-obligations" ||
    decision.reason_code !== "public-read-operation-allowed" ||
    !sameCanonical(decision.obligations, expectedObligations(operation))
  ) {
    fail("$.policy_decision", "does not authorise this exact successful public-read result");
  }
}

function snapshotBuildInput(value: unknown): PublicReadReceiptBuildInput {
  const snapshot = snapshotAt<Record<string, unknown>>(value, "$.build_input");
  const input = recordAt(snapshot, "$.build_input");
  assertExactKeys(
    input,
    [
      "authorityContext",
      "createdAt",
      "normalisedParameters",
      "operation",
      "policyDecision",
      "publicPolicy",
      "requestId",
      "resource",
      "resultCore",
      "software",
      "traceId",
      "transformations",
    ],
    "$.build_input",
  );
  return snapshot as unknown as PublicReadReceiptBuildInput;
}

function snapshotVerificationMaterial(value: unknown): PublicReadReceiptVerificationMaterial {
  const snapshot = snapshotAt<Record<string, unknown>>(value, "$.verification_material");
  const material = recordAt(snapshot, "$.verification_material");
  const keys = Object.keys(material);
  const allowed = new Set([
    "expectedAuthorityContext",
    "expectedPolicyDecision",
    "expectedResource",
    "expectedSoftware",
    "normalisedParameters",
    "publicPolicy",
    "resultCore",
  ]);
  if (
    !["normalisedParameters", "publicPolicy", "resultCore"].every((key) => keys.includes(key)) ||
    keys.some((key) => !allowed.has(key))
  ) {
    fail("$.verification_material", "has an unexpected or missing property");
  }
  return snapshot as unknown as PublicReadReceiptVerificationMaterial;
}

function assertReceiptSchema(value: unknown): asserts value is PublicReadEvidenceReceipt {
  canonicalJson(value);
  const receipt = recordAt(value, "$");
  assertExactKeys(
    receipt,
    [
      "authority_context",
      "created_at",
      "evidence_handling",
      "operation",
      "policy_decision",
      "receipt_id",
      "request_id",
      "resource",
      "result",
      "schema",
      "software",
      "trace_id",
      "transformations",
      "verification",
    ],
    "$",
  );
  if (receipt.schema !== "gis-ai-go.evidence-receipt.v2") {
    fail("$.schema", "must identify the public-read evidence receipt v2 schema");
  }
  assertContentId(receipt.receipt_id, RECEIPT_ID_PREFIX, "$.receipt_id");
  assertDateTime(receipt.created_at, "$.created_at");
  assertRequestId(receipt.request_id, "$.request_id");
  assertTraceId(receipt.trace_id, "$.trace_id");
  const operation = recordAt(receipt.operation, "$.operation");
  assertExactKeys(operation, ["contract_version", "name", "normalised_parameters"], "$.operation");
  if (
    !PUBLIC_READ_OPERATIONS.includes(operation.name as PublicReadOperation) ||
    operation.contract_version !== "v1"
  ) {
    fail("$.operation", "must identify a supported public-read v1 operation contract");
  }
  const operationName = operation.name as PublicReadOperation;
  const parameters = recordAt(operation.normalised_parameters, "$.operation.normalised_parameters");
  assertExactKeys(parameters, ["domain", "sha256"], "$.operation.normalised_parameters");
  if (
    parameters.domain !== parameterDomain(operationName) ||
    typeof parameters.sha256 !== "string" ||
    !SHA256.test(parameters.sha256)
  ) {
    fail("$.operation.normalised_parameters", "must contain the operation-specific digest");
  }
  if (!verifyPublicReadAuthorityContext(receipt.authority_context)) {
    fail("$.authority_context", "must be a valid public-read v2 authority context");
  }
  if (!verifyPublicReadPolicyDecision(receipt.policy_decision)) {
    fail("$.policy_decision", "must be a valid public-read v2 policy decision");
  }
  if (!verifyPublicReadResource(receipt.resource)) {
    fail("$.resource", "must be the exact reviewed ONS resource");
  }
  assertTransformations(receipt.transformations, operationName);
  assertSoftware(receipt.software);
  const result = recordAt(receipt.result, "$.result");
  assertExactKeys(result, ["domain", "media_type", "returned_item_count", "sha256"], "$.result");
  if (
    result.domain !== resultDomain(operationName) ||
    typeof result.sha256 !== "string" ||
    !SHA256.test(result.sha256) ||
    result.media_type !== "application/json" ||
    result.returned_item_count !== 1
  ) {
    fail("$.result", "must contain the bounded operation-specific result digest");
  }
  const verification = recordAt(receipt.verification, "$.verification");
  assertExactKeys(
    verification,
    ["canonicalisation", "checks", "digest_algorithm", "status"],
    "$.verification",
  );
  if (
    verification.status !== "passed" ||
    verification.canonicalisation !== CANONICALISATION ||
    verification.digest_algorithm !== "sha256" ||
    !sameCanonical(verification.checks, PUBLIC_READ_RECEIPT_VERIFICATION_CHECKS)
  ) {
    fail("$.verification", "must state the exact successful public-read verification checks");
  }
  const handling = recordAt(receipt.evidence_handling, "$.evidence_handling");
  assertExactKeys(handling, ["attestation", "delivery", "persistence"], "$.evidence_handling");
  if (
    handling.delivery !== "inline-only" ||
    handling.persistence !== "not-persisted" ||
    handling.attestation !== "not-attested"
  ) {
    fail("$.evidence_handling", "must remain inline-only, non-persisted and non-attested");
  }
}

export function buildPublicReadReceipt(
  input: PublicReadReceiptBuildInput,
): PublicReadEvidenceReceipt {
  const snapshot = snapshotBuildInput(input);
  assertDateTime(snapshot.createdAt, "$.created_at");
  assertRequestId(snapshot.requestId, "$.request_id");
  assertTraceId(snapshot.traceId, "$.trace_id");
  if (!PUBLIC_READ_OPERATIONS.includes(snapshot.operation)) {
    fail("$.operation.name", "must be a supported public-read operation");
  }
  assertTransformations(snapshot.transformations, snapshot.operation);
  assertSoftware(snapshot.software);
  assertIdentityLinkage(
    snapshot.authorityContext,
    snapshot.publicPolicy,
    snapshot.policyDecision,
    snapshot.resource,
    snapshot.operation,
    snapshot.requestId,
    snapshot.traceId,
  );
  const returnedItemCount = inspectResultCore(
    snapshot.resultCore,
    snapshot.operation,
    snapshot.requestId,
    snapshot.traceId,
    snapshot.resource,
  );
  assertNormalisedParameters(
    snapshot.normalisedParameters,
    snapshot.operation,
    snapshot.resource,
  );
  const core: PublicReadEvidenceReceiptCore = {
    schema: "gis-ai-go.evidence-receipt.v2",
    created_at: snapshot.createdAt,
    request_id: snapshot.requestId,
    trace_id: snapshot.traceId,
    operation: {
      name: snapshot.operation,
      contract_version: "v1",
      normalised_parameters: canonicalDigest(
        parameterDomain(snapshot.operation),
        snapshot.normalisedParameters,
      ),
    },
    authority_context: snapshot.authorityContext,
    policy_decision: snapshot.policyDecision,
    resource: snapshot.resource,
    transformations: snapshot.transformations,
    software: snapshot.software,
    result: {
      domain: resultDomain(snapshot.operation),
      sha256: canonicalDigest(resultDomain(snapshot.operation), snapshot.resultCore).sha256,
      media_type: "application/json",
      returned_item_count: returnedItemCount,
    },
    verification: {
      status: "passed",
      canonicalisation: CANONICALISATION,
      digest_algorithm: "sha256",
      checks: PUBLIC_READ_RECEIPT_VERIFICATION_CHECKS,
    },
    evidence_handling: {
      delivery: "inline-only",
      persistence: "not-persisted",
      attestation: "not-attested",
    },
  };
  const receipt = buildIdentity<PublicReadEvidenceReceiptCore, PublicReadEvidenceReceipt>(
    core,
    "receipt_id",
    RECEIPT_ID_PREFIX,
    CANONICAL_DOMAINS.evidenceReceiptV2,
  );
  assertReceiptSchema(receipt);
  return receipt;
}

function assertReceiptIdentity(receipt: PublicReadEvidenceReceipt): void {
  const { identity, core } = identityCore(receipt, "receipt_id", "$");
  if (
    !verifyContentAddress(
      identity,
      RECEIPT_ID_PREFIX,
      CANONICAL_DOMAINS.evidenceReceiptV2,
      core,
    )
  ) {
    fail("$.receipt_id", "does not match the canonical v2 receipt content");
  }
}

/** Verify only the closed v2 envelope and content identities retained by the ledger. */
export function verifyPublicReadReceiptStructure(receipt: unknown): receipt is PublicReadEvidenceReceipt {
  try {
    const candidate = snapshotAt<PublicReadEvidenceReceipt>(receipt, "$");
    assertReceiptSchema(candidate);
    assertReceiptIdentity(candidate);
    assertIdentityLinkage(
      candidate.authority_context,
      buildPublicReadPolicy({
        schema: "gis-ai-go.public-policy.v2",
        version: "2.0.0",
        canonicalisation: CANONICALISATION,
        compilation: { kind: "compiled-json", runtime: "gis-ai-go-gateway" },
        default_effect: "deny",
        applies_to: {
          authority_profile: "anonymous-open",
          access_tier: "open",
          publication_classification: "public",
          contains_personal_data: false,
          contains_protected_data: false,
          read_only: true,
        },
        resources: [PUBLIC_READ_ONS_RESOURCE],
        rules: [
          expectedRule("data.query", PUBLIC_READ_ONS_RESOURCE.resource_id),
          expectedRule("selection.resolve", PUBLIC_READ_ONS_RESOURCE.resource_id),
        ],
      }),
      candidate.policy_decision,
      candidate.resource,
      candidate.operation.name,
      candidate.request_id,
      candidate.trace_id,
    );
    return true;
  } catch {
    return false;
  }
}

export function verifyPublicReadReceipt(
  receipt: unknown,
  material: PublicReadReceiptVerificationMaterial,
): PublicReadReceiptVerificationResult {
  try {
    const snapshot = snapshotVerificationMaterial(material);
    const candidate = snapshotAt<PublicReadEvidenceReceipt>(receipt, "$");
    assertReceiptSchema(candidate);
    assertReceiptIdentity(candidate);
    assertIdentityLinkage(
      candidate.authority_context,
      snapshot.publicPolicy,
      candidate.policy_decision,
      candidate.resource,
      candidate.operation.name,
      candidate.request_id,
      candidate.trace_id,
    );
    const returnedItemCount = inspectResultCore(
      snapshot.resultCore,
      candidate.operation.name,
      candidate.request_id,
      candidate.trace_id,
      candidate.resource,
    );
    assertNormalisedParameters(
      snapshot.normalisedParameters,
      candidate.operation.name,
      candidate.resource,
    );
    if (candidate.result.returned_item_count !== returnedItemCount) {
      fail("$.result.returned_item_count", "does not match the validated result material");
    }
    if (
      !verifyDomainSeparatedSha256(
        candidate.operation.normalised_parameters.sha256,
        parameterDomain(candidate.operation.name),
        snapshot.normalisedParameters,
      )
    ) {
      fail("$.operation.normalised_parameters.sha256", "does not match supplied parameters");
    }
    if (
      !verifyDomainSeparatedSha256(
        candidate.result.sha256,
        resultDomain(candidate.operation.name),
        snapshot.resultCore,
      )
    ) {
      fail("$.result.sha256", "does not match the supplied successful result core");
    }
    if (
      snapshot.expectedAuthorityContext !== undefined &&
      !sameCanonical(candidate.authority_context, snapshot.expectedAuthorityContext)
    ) {
      fail("$.authority_context", "does not match the expected authority context");
    }
    if (
      snapshot.expectedPolicyDecision !== undefined &&
      !sameCanonical(candidate.policy_decision, snapshot.expectedPolicyDecision)
    ) {
      fail("$.policy_decision", "does not match the expected policy decision");
    }
    if (
      snapshot.expectedResource !== undefined &&
      !sameCanonical(candidate.resource, snapshot.expectedResource)
    ) {
      fail("$.resource", "does not match the expected resource");
    }
    if (
      snapshot.expectedSoftware !== undefined &&
      !sameCanonical(candidate.software, snapshot.expectedSoftware)
    ) {
      fail("$.software", "does not match the expected software identity");
    }
    return Object.freeze({
      valid: true,
      checks: PUBLIC_READ_RECEIPT_VERIFICATION_CHECKS,
      errors: [],
    });
  } catch (error) {
    const message = error instanceof PublicReadReceiptError
      ? error.message
      : error instanceof CanonicalJsonError
        ? `Public-read evidence canonical material failed closed (${error.code})`
        : "Public-read evidence verification failed closed";
    return Object.freeze({ valid: false, checks: [], errors: Object.freeze([message]) });
  }
}
