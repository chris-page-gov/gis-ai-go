import {
  CanonicalJsonError,
  canonicalJson,
  canonicalJsonClone,
  type CanonicalJsonValue,
} from "./canonical-json.js";
import {
  CANONICAL_DOMAINS,
  canonicalDigest,
  contentAddress,
  verifyContentAddress,
  verifyDomainSeparatedSha256,
  type CanonicalDigest,
} from "./digest.js";

export const CANONICALISATION = "rfc8785-jcs" as const;

const SHA40 = /^[0-9a-f]{40}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const SEMVER = /^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$/u;
const DATE_TIME =
  /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:Z|([+-])(\d{2}):(\d{2}))$/u;

const AUTHORITY_ID_PREFIX = "gis-ai-go:public-authority-context";
const POLICY_ID_PREFIX = "gis-ai-go:public-policy";
const DECISION_ID_PREFIX = "gis-ai-go:public-policy-decision";
const RECEIPT_ID_PREFIX = "gis-ai-go:evidence-receipt";

export const PUBLIC_CATALOGUE_OPERATIONS = ["catalogue.describe", "catalogue.search"] as const;
export type PublicCatalogueOperation = (typeof PUBLIC_CATALOGUE_OPERATIONS)[number];

export const GOVERNED_OPERATIONS = [
  "artefact.export",
  "catalogue.describe",
  "catalogue.search",
  "data.query",
  "evidence.inspect",
  "map.render",
  "route.plan",
  "selection.resolve",
  "spatial.analyse",
  "spatial.locate",
  "statistics.compare",
  "workflow.execute",
] as const;
export type GovernedOperation = (typeof GOVERNED_OPERATIONS)[number];

export const PUBLIC_POLICY_OBLIGATIONS = [
  "inline-evidence-receipt",
  "not-attested",
  "not-persisted",
  "preserve-attribution",
  "preserve-described-resource-licence",
  "preserve-record-licence",
] as const;
export type PublicPolicyObligation = (typeof PUBLIC_POLICY_OBLIGATIONS)[number];

export interface PublicAuthorityContextCore {
  readonly schema: "gis-ai-go.public-authority-context.v1";
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
  readonly permitted_operations: readonly PublicCatalogueOperation[];
  readonly evidence: {
    readonly receipt: "inline-required";
    readonly persistence: "not-persisted";
    readonly attestation: "not-attested";
  };
}

export interface PublicAuthorityContext extends PublicAuthorityContextCore {
  readonly context_id: string;
}

export interface PublicPolicyRule {
  readonly rule_id: "public-catalogue-describe" | "public-catalogue-search";
  readonly operation: PublicCatalogueOperation;
  readonly effect: "allow-with-obligations";
  readonly obligations: readonly PublicPolicyObligation[];
}

export interface PublicPolicyCore {
  readonly schema: "gis-ai-go.public-policy.v1";
  readonly version: string;
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
  readonly rules: readonly PublicPolicyRule[];
}

export interface PublicPolicy extends PublicPolicyCore {
  readonly policy_id: string;
}

export type PublicPolicyReasonCode =
  | "authority-context-not-applicable"
  | "operation-not-allowed"
  | "publication-not-public"
  | "public-catalogue-read-allowed";

export interface PublicPolicyDecisionCore {
  readonly schema: "gis-ai-go.public-policy-decision.v1";
  readonly canonicalisation: typeof CANONICALISATION;
  readonly request_id: string;
  readonly trace_id: string;
  readonly authority_context_id: string;
  readonly policy_id: string;
  readonly policy_version: string;
  readonly policy_default_effect: "deny";
  readonly operation: GovernedOperation;
  readonly effect: "allow-with-obligations" | "deny";
  readonly reason_code: PublicPolicyReasonCode;
  readonly obligations: readonly PublicPolicyObligation[];
}

export interface PublicPolicyDecision extends PublicPolicyDecisionCore {
  readonly decision_id: string;
}

export interface CatalogueIdentity {
  readonly id: string;
  readonly version: string;
  readonly revision: string;
  readonly content_root_sha256: string;
  readonly record_count: number;
  readonly reviewed_at: string;
  readonly stale_after: string;
}

export type EvidenceTransformationName =
  | "filter-catalogue"
  | "load-checksum-verified-catalogue"
  | "normalise-parameters"
  | "project-result-core";

export interface EvidenceTransformation {
  readonly name: EvidenceTransformationName;
  readonly version: "v1";
}

export interface EvidenceSoftwareIdentity {
  readonly name: "gis-ai-go-mcp-gateway";
  readonly version: string;
  readonly revision: string;
}

export interface RecordLicenceObligation {
  readonly record_id: string;
  readonly record_licence: string;
  readonly described_resource_licence: string;
  readonly attribution: string;
}

export const RECEIPT_VERIFICATION_CHECKS = [
  "authority-context",
  "catalogue-integrity",
  "licence-obligations",
  "normalised-parameters-digest",
  "public-policy-decision",
  "result-core-digest",
  "schema",
] as const;
export type ReceiptVerificationCheck = (typeof RECEIPT_VERIFICATION_CHECKS)[number];

export interface InlineEvidenceReceiptCore {
  readonly schema: "gis-ai-go.evidence-receipt.v1";
  readonly created_at: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly operation: {
    readonly name: PublicCatalogueOperation;
    readonly contract_version: "v1";
    readonly normalised_parameters: CanonicalDigest<"gis-ai-go.catalogue-parameters.v1">;
  };
  readonly authority_context: PublicAuthorityContext;
  readonly policy_decision: PublicPolicyDecision;
  readonly catalogue: CatalogueIdentity;
  readonly transformations: readonly EvidenceTransformation[];
  readonly software: EvidenceSoftwareIdentity;
  readonly result: {
    readonly domain: "gis-ai-go.catalogue-result-core.v1";
    readonly sha256: string;
    readonly media_type: "application/json";
    readonly returned_record_count: number;
  };
  readonly licence_obligations: readonly RecordLicenceObligation[];
  readonly verification: {
    readonly status: "passed";
    readonly canonicalisation: typeof CANONICALISATION;
    readonly digest_algorithm: "sha256";
    readonly checks: readonly ReceiptVerificationCheck[];
  };
  readonly evidence_handling: {
    readonly delivery: "inline-only";
    readonly persistence: "not-persisted";
    readonly attestation: "not-attested";
  };
}

export interface InlineEvidenceReceipt extends InlineEvidenceReceiptCore {
  readonly receipt_id: string;
}

export interface InlineReceiptBuildInput {
  readonly createdAt: string;
  readonly requestId: string;
  readonly traceId: string;
  readonly operation: PublicCatalogueOperation;
  /** Normalised application parameters. Only their digest is emitted. */
  readonly normalisedParameters: unknown;
  readonly authorityContext: PublicAuthorityContext;
  /** The compiled policy is verified but is not duplicated in the receipt. */
  readonly publicPolicy: PublicPolicy;
  readonly policyDecision: PublicPolicyDecision;
  readonly catalogue: CatalogueIdentity;
  readonly transformations: readonly EvidenceTransformation[];
  readonly software: EvidenceSoftwareIdentity;
  /** Successful result envelope with `evidence_receipt` omitted. */
  readonly resultCore: unknown;
  readonly licenceObligations: readonly RecordLicenceObligation[];
}

export interface InlineReceiptVerificationMaterial {
  readonly normalisedParameters: unknown;
  readonly resultCore: unknown;
  readonly publicPolicy: PublicPolicy;
  /** Independently derived exact rights for every returned record. */
  readonly licenceObligations: readonly RecordLicenceObligation[];
  readonly expectedAuthorityContext?: PublicAuthorityContext;
  readonly expectedPolicyDecision?: PublicPolicyDecision;
  readonly expectedCatalogue?: CatalogueIdentity;
  readonly expectedSoftware?: EvidenceSoftwareIdentity;
}

export interface InlineReceiptVerificationResult {
  readonly valid: boolean;
  readonly checks: readonly ReceiptVerificationCheck[];
  readonly errors: readonly string[];
}

export class InlineReceiptError extends TypeError {
  public readonly path: string;

  public constructor(path: string, message: string) {
    super(`Inline evidence rejected ${path}: ${message}`);
    this.name = "InlineReceiptError";
    this.path = path;
  }
}

function fail(path: string, message: string): never {
  throw new InlineReceiptError(path, message);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

function recordAt(value: unknown, path: string): Record<string, unknown> {
  if (!isRecord(value)) {
    return fail(path, "must be a plain object");
  }
  return value;
}

function stringAt(value: unknown, path: string, maxLength: number): string {
  if (typeof value !== "string" || value.length === 0 || Array.from(value).length > maxLength) {
    return fail(path, `must be a non-empty string of at most ${maxLength} Unicode characters`);
  }
  return value;
}

function assertExactKeys(value: Record<string, unknown>, expected: readonly string[], path: string): void {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    fail(path, "has an unexpected or missing property");
  }
}

function assertAllowedKeys(
  value: Record<string, unknown>,
  required: readonly string[],
  optional: readonly string[],
  path: string,
): void {
  const allowed = new Set([...required, ...optional]);
  if (
    Object.keys(value).some((key) => !allowed.has(key)) ||
    required.some((key) => !Object.hasOwn(value, key))
  ) {
    fail(path, "has an unexpected or missing property");
  }
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
  if (typeof value !== "string" || value.length > 35) {
    fail(path, "must be a valid RFC 3339 date-time");
  }
  const match = DATE_TIME.exec(value);
  if (match === null) {
    fail(path, "must be a valid RFC 3339 date-time");
  }
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const offsetSign = match[7] === "-" ? -1 : 1;
  const offsetHour = match[8] === undefined ? 0 : Number(match[8]);
  const offsetMinute = match[9] === undefined ? 0 : Number(match[9]);
  const leapYear = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const daysInMonth = [31, leapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (
    year < 1 ||
    month < 1 ||
    month > 12 ||
    day < 1 ||
    day > daysInMonth[month - 1]! ||
    hour > 23 ||
    minute > 59 ||
    second > 60 ||
    offsetHour > 23 ||
    offsetMinute > 59
  ) {
    fail(path, "must contain a real calendar date and bounded time components");
  }
  if (second === 60) {
    const local = new Date(0);
    local.setUTCFullYear(year, month - 1, day);
    local.setUTCHours(hour, minute, 59, 0);
    const offset = offsetSign * (offsetHour * 60 + offsetMinute) * 60_000;
    const utc = new Date(local.getTime() - offset);
    const validLeapPoint =
      utc.getUTCHours() === 23 &&
      utc.getUTCMinutes() === 59 &&
      ((utc.getUTCMonth() === 5 && utc.getUTCDate() === 30) ||
        (utc.getUTCMonth() === 11 && utc.getUTCDate() === 31));
    if (!validLeapPoint) {
      fail(path, "second 60 is valid only at a UTC June or December leap-second boundary");
    }
  }
}

/**
 * Apply the frozen v1 receipt calendar validator without exposing its throwing
 * assertion contract. New evidence surfaces reuse this so runtime date-time
 * acceptance cannot drift from the established receipt boundary.
 */
export function isStrictEvidenceDateTime(value: unknown): value is string {
  try {
    assertDateTime(value, "$.date_time");
    return true;
  } catch {
    return false;
  }
}

function assertSemver(value: unknown, path: string): asserts value is string {
  if (typeof value !== "string" || value.length > 32 || !SEMVER.test(value)) {
    fail(path, "must be a bounded semantic version");
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

function sortedUniqueStrings(
  actual: readonly unknown[],
  expected: readonly string[],
  path: string,
): void {
  if (
    actual.length !== expected.length ||
    actual.some((entry, index) => entry !== expected[index])
  ) {
    fail(path, "must contain the canonical sorted values exactly once");
  }
}

function identityCore(
  value: unknown,
  identityKey: string,
  path: string,
): { readonly identity: string; readonly core: Record<string, unknown> } {
  const record = recordAt(value, path);
  const identity = record[identityKey];
  if (typeof identity !== "string") {
    return fail(`${path}.${identityKey}`, "must be a string");
  }
  const core = Object.fromEntries(Object.entries(record).filter(([key]) => key !== identityKey));
  return { identity, core };
}

function buildIdentity<TCore, TDocument>(
  core: TCore,
  identityKey: string,
  prefix: string,
  domain: string,
): TDocument {
  const detached = canonicalJsonClone(core);
  const identity = contentAddress(prefix, domain, detached);
  return canonicalJsonClone({ ...(detached as object), [identityKey]: identity }) as TDocument;
}

function assertPublicAuthorityContextCore(
  value: unknown,
  path: string,
  expectIdentity: boolean,
): asserts value is PublicAuthorityContextCore | PublicAuthorityContext {
  canonicalJson(value);
  const context = recordAt(value, path);
  const keys = [
    "access",
    "canonicalisation",
    "construction",
    "evidence",
    "permitted_operations",
    "schema",
  ];
  if (expectIdentity) {
    keys.push("context_id");
  }
  assertExactKeys(context, keys, path);
  if (context.schema !== "gis-ai-go.public-authority-context.v1") {
    fail(`${path}.schema`, "must identify the public authority context v1 schema");
  }
  if (context.canonicalisation !== CANONICALISATION) {
    fail(`${path}.canonicalisation`, "must use RFC 8785 JCS");
  }
  if (expectIdentity) {
    assertContentId(context.context_id, AUTHORITY_ID_PREFIX, `${path}.context_id`);
  }

  const construction = recordAt(context.construction, `${path}.construction`);
  assertExactKeys(construction, ["product", "profile", "source"], `${path}.construction`);
  if (
    construction.source !== "server" ||
    construction.profile !== "anonymous-open" ||
    construction.product !== "gis-ai-go-gateway"
  ) {
    fail(`${path}.construction`, "must be the fixed server-constructed anonymous-open profile");
  }

  const access = recordAt(context.access, `${path}.access`);
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
    `${path}.access`,
  );
  if (
    access.authentication !== "none" ||
    access.tier !== "open" ||
    access.publication_classification !== "public" ||
    access.contains_personal_data !== false ||
    access.contains_protected_data !== false ||
    access.read_only !== true
  ) {
    fail(`${path}.access`, "must describe only public, open, read-only, non-personal data");
  }

  if (!Array.isArray(context.permitted_operations)) {
    fail(`${path}.permitted_operations`, "must be an array");
  }
  sortedUniqueStrings(
    context.permitted_operations,
    PUBLIC_CATALOGUE_OPERATIONS,
    `${path}.permitted_operations`,
  );

  const evidence = recordAt(context.evidence, `${path}.evidence`);
  assertExactKeys(evidence, ["attestation", "persistence", "receipt"], `${path}.evidence`);
  if (
    evidence.receipt !== "inline-required" ||
    evidence.persistence !== "not-persisted" ||
    evidence.attestation !== "not-attested"
  ) {
    fail(`${path}.evidence`, "must require non-persisted, non-attested inline evidence");
  }
}

function assertPublicPolicyCore(
  value: unknown,
  path: string,
  expectIdentity: boolean,
): asserts value is PublicPolicyCore | PublicPolicy {
  canonicalJson(value);
  const policy = recordAt(value, path);
  const keys = [
    "applies_to",
    "canonicalisation",
    "compilation",
    "default_effect",
    "rules",
    "schema",
    "version",
  ];
  if (expectIdentity) {
    keys.push("policy_id");
  }
  assertExactKeys(policy, keys, path);
  if (policy.schema !== "gis-ai-go.public-policy.v1") {
    fail(`${path}.schema`, "must identify the public policy v1 schema");
  }
  if (policy.canonicalisation !== CANONICALISATION || policy.default_effect !== "deny") {
    fail(path, "must be RFC 8785 JCS canonicalised and default deny");
  }
  assertSemver(policy.version, `${path}.version`);
  if (expectIdentity) {
    assertContentId(policy.policy_id, POLICY_ID_PREFIX, `${path}.policy_id`);
  }

  const compilation = recordAt(policy.compilation, `${path}.compilation`);
  assertExactKeys(compilation, ["kind", "runtime"], `${path}.compilation`);
  if (compilation.kind !== "compiled-json" || compilation.runtime !== "gis-ai-go-gateway") {
    fail(`${path}.compilation`, "must be compiled JSON for the GIS AI GO gateway");
  }

  const appliesTo = recordAt(policy.applies_to, `${path}.applies_to`);
  assertExactKeys(
    appliesTo,
    [
      "access_tier",
      "authority_profile",
      "contains_personal_data",
      "contains_protected_data",
      "publication_classification",
      "read_only",
    ],
    `${path}.applies_to`,
  );
  if (
    appliesTo.authority_profile !== "anonymous-open" ||
    appliesTo.access_tier !== "open" ||
    appliesTo.publication_classification !== "public" ||
    appliesTo.contains_personal_data !== false ||
    appliesTo.contains_protected_data !== false ||
    appliesTo.read_only !== true
  ) {
    fail(`${path}.applies_to`, "must be limited to anonymous open public read-only data");
  }

  if (!Array.isArray(policy.rules) || policy.rules.length !== PUBLIC_CATALOGUE_OPERATIONS.length) {
    fail(`${path}.rules`, "must contain the two public catalogue rules");
  }
  const ruleOperations: string[] = [];
  for (const [index, ruleValue] of policy.rules.entries()) {
    const rulePath = `${path}.rules[${index}]`;
    const rule = recordAt(ruleValue, rulePath);
    assertExactKeys(rule, ["effect", "obligations", "operation", "rule_id"], rulePath);
    if (!PUBLIC_CATALOGUE_OPERATIONS.includes(rule.operation as PublicCatalogueOperation)) {
      fail(`${rulePath}.operation`, "must be a public catalogue operation");
    }
    const operation = rule.operation as PublicCatalogueOperation;
    const expectedRuleId =
      operation === "catalogue.describe" ? "public-catalogue-describe" : "public-catalogue-search";
    if (rule.rule_id !== expectedRuleId || rule.effect !== "allow-with-obligations") {
      fail(rulePath, "must map the operation to its fixed allow-with-obligations rule");
    }
    if (!Array.isArray(rule.obligations)) {
      fail(`${rulePath}.obligations`, "must be an array");
    }
    sortedUniqueStrings(rule.obligations, PUBLIC_POLICY_OBLIGATIONS, `${rulePath}.obligations`);
    ruleOperations.push(operation);
  }
  sortedUniqueStrings(ruleOperations, PUBLIC_CATALOGUE_OPERATIONS, `${path}.rules`);
}

function assertPublicPolicyDecisionCore(
  value: unknown,
  path: string,
  expectIdentity: boolean,
): asserts value is PublicPolicyDecisionCore | PublicPolicyDecision {
  canonicalJson(value);
  const decision = recordAt(value, path);
  const keys = [
    "authority_context_id",
    "canonicalisation",
    "effect",
    "obligations",
    "operation",
    "policy_default_effect",
    "policy_id",
    "policy_version",
    "reason_code",
    "request_id",
    "schema",
    "trace_id",
  ];
  if (expectIdentity) {
    keys.push("decision_id");
  }
  assertExactKeys(decision, keys, path);
  if (
    decision.schema !== "gis-ai-go.public-policy-decision.v1" ||
    decision.canonicalisation !== CANONICALISATION ||
    decision.policy_default_effect !== "deny"
  ) {
    fail(path, "must be an RFC 8785 JCS default-deny public policy decision");
  }
  if (expectIdentity) {
    assertContentId(decision.decision_id, DECISION_ID_PREFIX, `${path}.decision_id`);
  }
  assertRequestId(decision.request_id, `${path}.request_id`);
  assertTraceId(decision.trace_id, `${path}.trace_id`);
  assertContentId(decision.authority_context_id, AUTHORITY_ID_PREFIX, `${path}.authority_context_id`);
  assertContentId(decision.policy_id, POLICY_ID_PREFIX, `${path}.policy_id`);
  assertSemver(decision.policy_version, `${path}.policy_version`);
  if (!GOVERNED_OPERATIONS.includes(decision.operation as GovernedOperation)) {
    fail(`${path}.operation`, "must be a governed operation");
  }
  if (!Array.isArray(decision.obligations)) {
    fail(`${path}.obligations`, "must be an array");
  }
  if (decision.effect === "allow-with-obligations") {
    if (
      !PUBLIC_CATALOGUE_OPERATIONS.includes(decision.operation as PublicCatalogueOperation) ||
      decision.reason_code !== "public-catalogue-read-allowed"
    ) {
      fail(path, "an allow decision is limited to a named public catalogue rule");
    }
    sortedUniqueStrings(decision.obligations, PUBLIC_POLICY_OBLIGATIONS, `${path}.obligations`);
    return;
  }
  if (decision.effect !== "deny") {
    fail(`${path}.effect`, "must be allow-with-obligations or deny");
  }
  if (
    ![
      "authority-context-not-applicable",
      "operation-not-allowed",
      "publication-not-public",
    ].includes(decision.reason_code as string) ||
    decision.obligations.length !== 0
  ) {
    fail(path, "a deny decision must use a controlled deny reason and no obligations");
  }
}

export function buildPublicAuthorityContext(
  core: PublicAuthorityContextCore,
): PublicAuthorityContext {
  assertPublicAuthorityContextCore(core, "$.authority_context", false);
  return buildIdentity<PublicAuthorityContextCore, PublicAuthorityContext>(
    core,
    "context_id",
    AUTHORITY_ID_PREFIX,
    CANONICAL_DOMAINS.authorityContext,
  );
}

export function verifyPublicAuthorityContext(value: unknown): value is PublicAuthorityContext {
  try {
    assertPublicAuthorityContextCore(value, "$.authority_context", true);
    const { identity, core } = identityCore(value, "context_id", "$.authority_context");
    return verifyContentAddress(
      identity,
      AUTHORITY_ID_PREFIX,
      CANONICAL_DOMAINS.authorityContext,
      core,
    );
  } catch {
    return false;
  }
}

export function buildPublicPolicy(core: PublicPolicyCore): PublicPolicy {
  assertPublicPolicyCore(core, "$.public_policy", false);
  return buildIdentity<PublicPolicyCore, PublicPolicy>(
    core,
    "policy_id",
    POLICY_ID_PREFIX,
    CANONICAL_DOMAINS.publicPolicy,
  );
}

export function verifyPublicPolicy(value: unknown): value is PublicPolicy {
  try {
    assertPublicPolicyCore(value, "$.public_policy", true);
    const { identity, core } = identityCore(value, "policy_id", "$.public_policy");
    return verifyContentAddress(identity, POLICY_ID_PREFIX, CANONICAL_DOMAINS.publicPolicy, core);
  } catch {
    return false;
  }
}

export function buildPublicPolicyDecision(
  core: PublicPolicyDecisionCore,
): PublicPolicyDecision {
  assertPublicPolicyDecisionCore(core, "$.policy_decision", false);
  return buildIdentity<PublicPolicyDecisionCore, PublicPolicyDecision>(
    core,
    "decision_id",
    DECISION_ID_PREFIX,
    CANONICAL_DOMAINS.publicPolicyDecision,
  );
}

export function verifyPublicPolicyDecision(value: unknown): value is PublicPolicyDecision {
  try {
    assertPublicPolicyDecisionCore(value, "$.policy_decision", true);
    const { identity, core } = identityCore(value, "decision_id", "$.policy_decision");
    return verifyContentAddress(
      identity,
      DECISION_ID_PREFIX,
      CANONICAL_DOMAINS.publicPolicyDecision,
      core,
    );
  } catch {
    return false;
  }
}

function assertCatalogue(value: unknown, path: string): asserts value is CatalogueIdentity {
  const catalogue = recordAt(value, path);
  assertExactKeys(
    catalogue,
    ["content_root_sha256", "id", "record_count", "reviewed_at", "revision", "stale_after", "version"],
    path,
  );
  stringAt(catalogue.id, `${path}.id`, 512);
  assertSemver(catalogue.version, `${path}.version`);
  if (typeof catalogue.revision !== "string" || !SHA40.test(catalogue.revision)) {
    fail(`${path}.revision`, "must be a 40-character lower-case Git revision");
  }
  if (typeof catalogue.content_root_sha256 !== "string" || !SHA256.test(catalogue.content_root_sha256)) {
    fail(`${path}.content_root_sha256`, "must be a SHA-256 digest");
  }
  if (
    !Number.isInteger(catalogue.record_count) ||
    (catalogue.record_count as number) < 1 ||
    (catalogue.record_count as number) > 10_000
  ) {
    fail(`${path}.record_count`, "must be an integer from 1 to 10000");
  }
  assertDateTime(catalogue.reviewed_at, `${path}.reviewed_at`);
  assertDateTime(catalogue.stale_after, `${path}.stale_after`);
}

function compareByUnicodeCodePoint(left: string, right: string): number {
  const leftPoints = Array.from(left, (character) => character.codePointAt(0) ?? 0);
  const rightPoints = Array.from(right, (character) => character.codePointAt(0) ?? 0);
  const count = Math.min(leftPoints.length, rightPoints.length);
  for (let index = 0; index < count; index += 1) {
    const difference = leftPoints[index]! - rightPoints[index]!;
    if (difference !== 0) {
      return difference;
    }
  }
  return leftPoints.length - rightPoints.length;
}

function normaliseLicenceObligations(
  obligations: readonly RecordLicenceObligation[],
): readonly RecordLicenceObligation[] {
  if (obligations.length > 100) {
    fail("$.licence_obligations", "must contain at most 100 records");
  }
  const detached = canonicalJsonClone(obligations);
  const seen = new Set<string>();
  for (const [index, obligation] of detached.entries()) {
    const path = `$.licence_obligations[${index}]`;
    const record = recordAt(obligation, path);
    assertExactKeys(
      record,
      ["attribution", "described_resource_licence", "record_id", "record_licence"],
      path,
    );
    const recordId = stringAt(record.record_id, `${path}.record_id`, 512);
    stringAt(record.record_licence, `${path}.record_licence`, 2_048);
    stringAt(record.described_resource_licence, `${path}.described_resource_licence`, 2_048);
    stringAt(record.attribution, `${path}.attribution`, 8_192);
    if (seen.has(recordId)) {
      fail(`${path}.record_id`, "must identify a record only once");
    }
    seen.add(recordId);
  }
  return canonicalJsonClone([...detached].sort((left, right) =>
    compareByUnicodeCodePoint(left.record_id, right.record_id),
  ));
}

interface ResultCoreBinding {
  readonly returnedRecordIds: readonly string[];
}

const RECORD_TYPES = ["bundle", "dataset", "provider", "source", "workflow"] as const;
const AUTHORITY_CLASSES = ["derived", "project-authoritative", "source-authoritative"] as const;
const ACCESS_STATES = ["planned-non-executing", "public", "public-metadata"] as const;
const RIGHTS_STATES = ["metadata-citation", "open-with-conditions", "project-mit"] as const;
const FRESHNESS_STATES = ["current", "review-required"] as const;
const RECORD_STATUSES = [
  "candidate",
  "candidate-metadata",
  "candidate-non-executing",
  "external-source",
] as const;
const SOURCE_NATIVE_STRING_UNSAFE =
  /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SOURCE_NATIVE_KEY_UNSAFE =
  /[\u0000-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SOURCE_NATIVE_DANGEROUS_KEYS = new Set(["__proto__", "constructor", "prototype"]);

function assertInteger(value: unknown, minimum: number, maximum: number, path: string): number {
  if (!Number.isInteger(value) || (value as number) < minimum || (value as number) > maximum) {
    return fail(path, `must be an integer from ${minimum} to ${maximum}`);
  }
  return value as number;
}

function assertVocabulary(
  value: unknown,
  allowed: readonly string[],
  path: string,
): asserts value is string {
  if (typeof value !== "string" || !allowed.includes(value)) {
    fail(path, "must use the closed contract vocabulary");
  }
}

function assertUniqueJson(values: readonly unknown[], path: string): void {
  const seen = new Set<string>();
  for (const [index, value] of values.entries()) {
    const identity = canonicalJson(value);
    if (seen.has(identity)) {
      fail(`${path}[${index}]`, "must be unique");
    }
    seen.add(identity);
  }
}

function assertStringArray(
  value: unknown,
  minimum: number,
  maximum: number,
  itemMaximum: number,
  path: string,
): asserts value is readonly string[] {
  if (!Array.isArray(value) || value.length < minimum || value.length > maximum) {
    fail(path, `must contain from ${minimum} to ${maximum} items`);
  }
  value.forEach((item, index) => stringAt(item, `${path}[${index}]`, itemMaximum));
  assertUniqueJson(value, path);
}

function assertRecordSummary(value: unknown, path: string): string {
  const record = recordAt(value, path);
  assertExactKeys(
    record,
    [
      "access",
      "authority",
      "description",
      "freshness",
      "id",
      "rights",
      "status",
      "tags",
      "title",
      "type",
    ],
    path,
  );
  const id = stringAt(record.id, `${path}.id`, 512);
  assertVocabulary(record.type, RECORD_TYPES, `${path}.type`);
  stringAt(record.title, `${path}.title`, 512);
  stringAt(record.description, `${path}.description`, 4_096);
  assertVocabulary(record.authority, AUTHORITY_CLASSES, `${path}.authority`);
  assertVocabulary(record.access, ACCESS_STATES, `${path}.access`);
  assertVocabulary(record.rights, RIGHTS_STATES, `${path}.rights`);
  assertVocabulary(record.freshness, FRESHNESS_STATES, `${path}.freshness`);
  assertVocabulary(record.status, RECORD_STATUSES, `${path}.status`);
  assertStringArray(record.tags, 0, 50, 128, `${path}.tags`);
  return id;
}

function assertAuthority(value: unknown, path: string): void {
  const authority = recordAt(value, path);
  assertExactKeys(authority, ["class", "source", "statement"], path);
  assertVocabulary(authority.class, AUTHORITY_CLASSES, `${path}.class`);
  stringAt(authority.statement, `${path}.statement`, 4_096);
  stringAt(authority.source, `${path}.source`, 512);
}

function assertPublication(value: unknown, path: string): void {
  const publication = recordAt(value, path);
  assertExactKeys(
    publication,
    ["classification", "contains_personal_data", "contains_protected_data"],
    path,
  );
  if (
    publication.classification !== "public" ||
    publication.contains_personal_data !== false ||
    publication.contains_protected_data !== false
  ) {
    fail(path, "must be the public non-personal, non-protected publication boundary");
  }
}

function assertRecordAccess(value: unknown, path: string): void {
  const access = recordAt(value, path);
  assertExactKeys(access, ["authentication", "state", "tier"], path);
  if (access.tier !== "open") {
    fail(`${path}.tier`, "must be open");
  }
  assertVocabulary(access.state, ACCESS_STATES, `${path}.state`);
  stringAt(access.authentication, `${path}.authentication`, 512);
}

function assertRecordRights(value: unknown, path: string): void {
  const rights = recordAt(value, path);
  assertExactKeys(
    rights,
    ["attribution", "described_resource_licence", "record_licence", "state"],
    path,
  );
  assertVocabulary(rights.state, RIGHTS_STATES, `${path}.state`);
  stringAt(rights.record_licence, `${path}.record_licence`, 2_048);
  stringAt(rights.described_resource_licence, `${path}.described_resource_licence`, 2_048);
  stringAt(rights.attribution, `${path}.attribution`, 8_192);
}

function assertFreshness(value: unknown, path: string): void {
  const freshness = recordAt(value, path);
  assertExactKeys(freshness, ["observed_at", "reviewed_at", "stale_after", "status"], path);
  assertDateTime(freshness.observed_at, `${path}.observed_at`);
  assertDateTime(freshness.reviewed_at, `${path}.reviewed_at`);
  assertDateTime(freshness.stale_after, `${path}.stale_after`);
  assertVocabulary(freshness.status, FRESHNESS_STATES, `${path}.status`);
}

function assertSourceNativeValue(value: unknown, path: string): void {
  if (value === null || typeof value === "boolean") {
    return;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      fail(path, "must be a finite source-native number");
    }
    return;
  }
  if (typeof value === "string") {
    if (Array.from(value).length > 65_536 || SOURCE_NATIVE_STRING_UNSAFE.test(value)) {
      fail(path, "contains unbounded or unsafe source-native text");
    }
    return;
  }
  if (Array.isArray(value)) {
    if (value.length > 10_000) {
      fail(path, "contains too many source-native array items");
    }
    value.forEach((item, index) => assertSourceNativeValue(item, `${path}[${index}]`));
    return;
  }
  const object = recordAt(value, path);
  const keys = Object.keys(object);
  if (keys.length > 256) {
    fail(path, "contains too many source-native object properties");
  }
  for (const key of keys) {
    if (
      Array.from(key).length < 1 ||
      Array.from(key).length > 256 ||
      SOURCE_NATIVE_KEY_UNSAFE.test(key) ||
      SOURCE_NATIVE_DANGEROUS_KEYS.has(key)
    ) {
      fail(path, "contains an unsafe source-native property name");
    }
    assertSourceNativeValue(object[key], `${path}.${key}`);
  }
}

function assertRecordDetail(value: unknown, path: string): string {
  const record = recordAt(value, path);
  assertExactKeys(
    record,
    [
      "access",
      "authority",
      "description",
      "details",
      "freshness",
      "id",
      "limitations",
      "publication",
      "rights",
      "source_refs",
      "status",
      "tags",
      "title",
      "type",
    ],
    path,
  );
  const id = stringAt(record.id, `${path}.id`, 512);
  assertVocabulary(record.type, RECORD_TYPES, `${path}.type`);
  stringAt(record.title, `${path}.title`, 512);
  stringAt(record.description, `${path}.description`, 4_096);
  assertAuthority(record.authority, `${path}.authority`);
  assertPublication(record.publication, `${path}.publication`);
  assertRecordAccess(record.access, `${path}.access`);
  assertRecordRights(record.rights, `${path}.rights`);
  assertFreshness(record.freshness, `${path}.freshness`);
  assertVocabulary(record.status, RECORD_STATUSES, `${path}.status`);
  assertStringArray(record.source_refs, 1, 99, 512, `${path}.source_refs`);
  assertStringArray(record.limitations, 1, 50, 2_048, `${path}.limitations`);
  assertStringArray(record.tags, 0, 50, 128, `${path}.tags`);
  if (!isRecord(record.details)) {
    fail(`${path}.details`, "must be a source-native object");
  }
  assertSourceNativeValue(record.details, `${path}.details`);
  return id;
}

function assertWarnings(value: unknown, path: string): void {
  assertStringArray(value, 0, 20, 1_024, path);
}

function assertFacetGroup(
  value: unknown,
  maximum: number,
  vocabulary: readonly string[] | null,
  path: string,
): void {
  if (!Array.isArray(value) || value.length > maximum) {
    fail(path, `must contain at most ${maximum} facet counts`);
  }
  const seenValues = new Set<string>();
  for (const [index, entryValue] of value.entries()) {
    const entryPath = `${path}[${index}]`;
    const entry = recordAt(entryValue, entryPath);
    assertExactKeys(entry, ["count", "value"], entryPath);
    let facetValue: string;
    if (vocabulary === null) {
      facetValue = stringAt(entry.value, `${entryPath}.value`, 128);
    } else {
      assertVocabulary(entry.value, vocabulary, `${entryPath}.value`);
      facetValue = entry.value as string;
    }
    if (seenValues.has(facetValue)) {
      fail(path, "facet values must be unique");
    }
    seenValues.add(facetValue);
    assertInteger(entry.count, 0, 10_000, `${entryPath}.count`);
  }
  assertUniqueJson(value, path);
}

function assertFacets(value: unknown, path: string): void {
  const facets = recordAt(value, path);
  assertExactKeys(facets, ["access", "authority", "freshness", "rights", "tags", "types"], path);
  assertFacetGroup(facets.types, 5, RECORD_TYPES, `${path}.types`);
  assertFacetGroup(facets.authority, 3, AUTHORITY_CLASSES, `${path}.authority`);
  assertFacetGroup(facets.access, 3, ACCESS_STATES, `${path}.access`);
  assertFacetGroup(facets.rights, 3, RIGHTS_STATES, `${path}.rights`);
  assertFacetGroup(facets.freshness, 2, FRESHNESS_STATES, `${path}.freshness`);
  assertFacetGroup(facets.tags, 100, null, `${path}.tags`);
}

function assertPage(value: unknown, returned: number, path: string): void {
  const page = recordAt(value, path);
  assertExactKeys(page, ["limit", "matched", "next_cursor", "returned"], path);
  const limit = assertInteger(page.limit, 1, 100, `${path}.limit`);
  const declaredReturned = assertInteger(page.returned, 0, 100, `${path}.returned`);
  const matched = assertInteger(page.matched, 0, 10_000, `${path}.matched`);
  if (declaredReturned !== returned || matched < returned || returned > limit) {
    fail(path, "limit, returned and matched counts must agree with the record array");
  }
  if (
    page.next_cursor !== null &&
    (typeof page.next_cursor !== "string" ||
      page.next_cursor.length < 1 ||
      page.next_cursor.length > 1_024)
  ) {
    fail(`${path}.next_cursor`, "must be null or a bounded cursor");
  }
}

function assertRelationship(value: unknown, path: string): void {
  const relationship = recordAt(value, path);
  assertExactKeys(relationship, ["record_id", "relation"], path);
  if (relationship.relation !== "source") {
    fail(`${path}.relation`, "must be source");
  }
  stringAt(relationship.record_id, `${path}.record_id`, 512);
}

function assertSourceSummary(value: unknown, path: string): string {
  const source = recordAt(value, path);
  assertExactKeys(source, ["access", "authority", "freshness", "id", "rights", "title"], path);
  const id = stringAt(source.id, `${path}.id`, 512);
  stringAt(source.title, `${path}.title`, 512);
  assertVocabulary(source.authority, AUTHORITY_CLASSES, `${path}.authority`);
  assertVocabulary(source.access, ACCESS_STATES, `${path}.access`);
  assertVocabulary(source.rights, RIGHTS_STATES, `${path}.rights`);
  assertVocabulary(source.freshness, FRESHNESS_STATES, `${path}.freshness`);
  return id;
}

function inspectResultCore(
  resultCore: unknown,
  operation: PublicCatalogueOperation,
  requestId: string,
  traceId: string,
  catalogue: CatalogueIdentity,
): ResultCoreBinding {
  canonicalJson(resultCore);
  const result = recordAt(resultCore, "$.result_core");
  assertExactKeys(
    result,
    ["catalogue", "data", "operation", "request_id", "schema", "trace_id", "warnings"],
    "$.result_core",
  );
  if (result.schema !== "gis-ai-go.catalogue-result.v1") {
    fail("$.result_core.schema", "must identify the catalogue result v1 schema");
  }
  if (result.operation !== operation || result.request_id !== requestId || result.trace_id !== traceId) {
    fail("$.result_core", "operation, request and trace identifiers must match the receipt");
  }
  if (!sameCanonical(result.catalogue, catalogue)) {
    fail("$.result_core.catalogue", "must match the receipt catalogue identity");
  }
  assertCatalogue(result.catalogue, "$.result_core.catalogue");
  assertWarnings(result.warnings, "$.result_core.warnings");
  const data = recordAt(result.data, "$.result_core.data");
  if (operation === "catalogue.search") {
    assertExactKeys(data, ["facets", "page", "records"], "$.result_core.data");
    if (!Array.isArray(data.records) || data.records.length > 100) {
      fail("$.result_core.data.records", "must be a bounded record array");
    }
    const identifiers = data.records.map((entry, index) =>
      assertRecordSummary(entry, `$.result_core.data.records[${index}]`),
    );
    if (new Set(identifiers).size !== identifiers.length) {
      fail("$.result_core.data.records", "record identifiers must be unique");
    }
    assertUniqueJson(data.records, "$.result_core.data.records");
    assertFacets(data.facets, "$.result_core.data.facets");
    assertPage(data.page, identifiers.length, "$.result_core.data.page");
    return { returnedRecordIds: identifiers };
  }
  assertExactKeys(data, ["included", "record"], "$.result_core.data");
  const identifiers = [assertRecordDetail(data.record, "$.result_core.data.record")];
  const included = recordAt(data.included, "$.result_core.data.included");
  assertAllowedKeys(included, [], ["relationships", "sources"], "$.result_core.data.included");
  if (included.relationships !== undefined) {
    if (!Array.isArray(included.relationships) || included.relationships.length > 100) {
      fail("$.result_core.data.included.relationships", "must contain at most 100 relationships");
    }
    included.relationships.forEach((relationship, index) =>
      assertRelationship(relationship, `$.result_core.data.included.relationships[${index}]`),
    );
    assertUniqueJson(included.relationships, "$.result_core.data.included.relationships");
  }
  if (included.sources !== undefined) {
    if (!Array.isArray(included.sources) || included.sources.length > 99) {
      fail("$.result_core.data.included.sources", "must contain at most 99 source projections");
    }
    for (const [index, source] of included.sources.entries()) {
      identifiers.push(assertSourceSummary(source, `$.result_core.data.included.sources[${index}]`));
    }
    assertUniqueJson(included.sources, "$.result_core.data.included.sources");
  }
  if (new Set(identifiers).size !== identifiers.length) {
    fail("$.result_core.data", "primary and included source record identifiers must be unique");
  }
  return { returnedRecordIds: identifiers };
}

function assertIdentityLinkage(
  authority: PublicAuthorityContext,
  policy: PublicPolicy,
  decision: PublicPolicyDecision,
  operation: PublicCatalogueOperation,
  requestId: string,
  traceId: string,
): void {
  if (!verifyPublicAuthorityContext(authority)) {
    fail("$.authority_context.context_id", "does not match its canonical content");
  }
  if (!verifyPublicPolicy(policy)) {
    fail("$.public_policy.policy_id", "does not match its canonical content");
  }
  if (!verifyPublicPolicyDecision(decision)) {
    fail("$.policy_decision.decision_id", "does not match its canonical content");
  }
  if (
    authority.schema !== "gis-ai-go.public-authority-context.v1" ||
    authority.canonicalisation !== CANONICALISATION ||
    authority.construction.source !== "server" ||
    authority.construction.profile !== "anonymous-open" ||
    authority.access.authentication !== "none" ||
    authority.access.tier !== "open" ||
    authority.access.publication_classification !== "public" ||
    authority.access.contains_personal_data !== false ||
    authority.access.contains_protected_data !== false ||
    authority.access.read_only !== true ||
    authority.evidence.receipt !== "inline-required" ||
    authority.evidence.persistence !== "not-persisted" ||
    authority.evidence.attestation !== "not-attested" ||
    !authority.permitted_operations.includes(operation)
  ) {
    fail("$.authority_context", "is not the applicable anonymous-open public context");
  }
  if (
    policy.schema !== "gis-ai-go.public-policy.v1" ||
    policy.canonicalisation !== CANONICALISATION ||
    policy.default_effect !== "deny" ||
    !SEMVER.test(policy.version)
  ) {
    fail("$.public_policy", "is not the compiled default-deny JCS policy");
  }
  if (
    decision.schema !== "gis-ai-go.public-policy-decision.v1" ||
    decision.canonicalisation !== CANONICALISATION ||
    decision.authority_context_id !== authority.context_id ||
    decision.policy_id !== policy.policy_id ||
    decision.policy_version !== policy.version ||
    decision.policy_default_effect !== "deny" ||
    decision.operation !== operation ||
    decision.request_id !== requestId ||
    decision.trace_id !== traceId ||
    decision.effect !== "allow-with-obligations" ||
    decision.reason_code !== "public-catalogue-read-allowed"
  ) {
    fail("$.policy_decision", "does not authorise this exact public catalogue result");
  }
  sortedUniqueStrings(decision.obligations, PUBLIC_POLICY_OBLIGATIONS, "$.policy_decision.obligations");
}

function assertTransformations(
  value: unknown,
  operation: PublicCatalogueOperation,
  path = "$.transformations",
): asserts value is readonly EvidenceTransformation[] {
  if (!Array.isArray(value) || value.length < 1 || value.length > 4) {
    fail("$.transformations", "must contain between 1 and 4 transformations");
  }
  const transformations = value;
  const seen = new Set<string>();
  for (const [index, transformationValue] of transformations.entries()) {
    const itemPath = `${path}[${index}]`;
    const transformation = recordAt(transformationValue, itemPath);
    assertExactKeys(transformation, ["name", "version"], itemPath);
    if (
      ![
        "filter-catalogue",
        "load-checksum-verified-catalogue",
        "normalise-parameters",
        "project-result-core",
      ].includes(transformation.name as string) ||
      transformation.version !== "v1"
    ) {
      fail(itemPath, "must be a supported versioned transformation");
    }
    const key = `${transformation.name}:${transformation.version}`;
    if (seen.has(key)) {
      fail(itemPath, "must be unique");
    }
    seen.add(key);
  }
  const expectedNames: readonly EvidenceTransformationName[] =
    operation === "catalogue.search"
      ? [
          "load-checksum-verified-catalogue",
          "normalise-parameters",
          "filter-catalogue",
          "project-result-core",
        ]
      : [
          "load-checksum-verified-catalogue",
          "normalise-parameters",
          "project-result-core",
        ];
  if (
    transformations.length !== expectedNames.length ||
    transformations.some((transformation, index) => transformation.name !== expectedNames[index])
  ) {
    fail(path, `must use the exact ordered ${operation} transformation pipeline`);
  }
}

function assertSoftware(value: unknown, path = "$.software"): asserts value is EvidenceSoftwareIdentity {
  const software = recordAt(value, path);
  assertExactKeys(software, ["name", "revision", "version"], path);
  if (
    software.name !== "gis-ai-go-mcp-gateway" ||
    typeof software.version !== "string" ||
    software.version.length > 32 ||
    !SEMVER.test(software.version) ||
    typeof software.revision !== "string" ||
    !SHA40.test(software.revision)
  ) {
    fail(path, "must identify an exact semantic version and Git revision of the gateway");
  }
}

function assertInlineReceiptSchema(value: unknown): asserts value is InlineEvidenceReceipt {
  canonicalJson(value);
  const receipt = recordAt(value, "$");
  assertExactKeys(
    receipt,
    [
      "authority_context",
      "catalogue",
      "created_at",
      "evidence_handling",
      "licence_obligations",
      "operation",
      "policy_decision",
      "receipt_id",
      "request_id",
      "result",
      "schema",
      "software",
      "trace_id",
      "transformations",
      "verification",
    ],
    "$",
  );
  if (receipt.schema !== "gis-ai-go.evidence-receipt.v1") {
    fail("$.schema", "must identify the inline evidence receipt v1 schema");
  }
  assertContentId(receipt.receipt_id, RECEIPT_ID_PREFIX, "$.receipt_id");
  assertDateTime(receipt.created_at, "$.created_at");
  assertRequestId(receipt.request_id, "$.request_id");
  assertTraceId(receipt.trace_id, "$.trace_id");

  const operation = recordAt(receipt.operation, "$.operation");
  assertExactKeys(operation, ["contract_version", "name", "normalised_parameters"], "$.operation");
  if (
    !PUBLIC_CATALOGUE_OPERATIONS.includes(operation.name as PublicCatalogueOperation) ||
    operation.contract_version !== "v1"
  ) {
    fail("$.operation", "must identify a public catalogue v1 operation");
  }
  const parameters = recordAt(operation.normalised_parameters, "$.operation.normalised_parameters");
  assertExactKeys(parameters, ["domain", "sha256"], "$.operation.normalised_parameters");
  if (
    parameters.domain !== CANONICAL_DOMAINS.catalogueParameters ||
    typeof parameters.sha256 !== "string" ||
    !SHA256.test(parameters.sha256)
  ) {
    fail("$.operation.normalised_parameters", "must contain the canonical parameter digest");
  }

  assertPublicAuthorityContextCore(receipt.authority_context, "$.authority_context", true);
  assertPublicPolicyDecisionCore(receipt.policy_decision, "$.policy_decision", true);
  assertCatalogue(receipt.catalogue, "$.catalogue");
  assertTransformations(receipt.transformations, operation.name as PublicCatalogueOperation);
  assertSoftware(receipt.software);

  const result = recordAt(receipt.result, "$.result");
  assertExactKeys(
    result,
    ["domain", "media_type", "returned_record_count", "sha256"],
    "$.result",
  );
  if (
    result.domain !== CANONICAL_DOMAINS.catalogueResultCore ||
    typeof result.sha256 !== "string" ||
    !SHA256.test(result.sha256) ||
    result.media_type !== "application/json" ||
    !Number.isInteger(result.returned_record_count) ||
    (result.returned_record_count as number) < 0 ||
    (result.returned_record_count as number) > 100
  ) {
    fail("$.result", "must contain the bounded canonical result-core digest");
  }

  if (!Array.isArray(receipt.licence_obligations)) {
    fail("$.licence_obligations", "must be an array");
  }
  const obligations = normaliseLicenceObligations(
    receipt.licence_obligations as unknown as readonly RecordLicenceObligation[],
  );
  if (!sameCanonical(obligations, receipt.licence_obligations)) {
    fail("$.licence_obligations", "must be unique and sorted by record identifier code point");
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
    !Array.isArray(verification.checks)
  ) {
    fail("$.verification", "must state the fixed successful JCS and SHA-256 semantics");
  }
  sortedUniqueStrings(verification.checks, RECEIPT_VERIFICATION_CHECKS, "$.verification.checks");

  const handling = recordAt(receipt.evidence_handling, "$.evidence_handling");
  assertExactKeys(handling, ["attestation", "delivery", "persistence"], "$.evidence_handling");
  if (
    handling.delivery !== "inline-only" ||
    handling.persistence !== "not-persisted" ||
    handling.attestation !== "not-attested"
  ) {
    fail("$.evidence_handling", "must state inline-only, non-persisted, non-attested handling");
  }
}

function assertObligationCoverage(
  obligations: readonly RecordLicenceObligation[],
  returnedRecordIds: readonly string[],
): void {
  const expected = [...returnedRecordIds].sort(compareByUnicodeCodePoint);
  const actual = obligations.map((obligation) => obligation.record_id);
  if (new Set(expected).size !== expected.length || !sameCanonical(actual, expected)) {
    fail("$.licence_obligations", "must cover each returned record exactly once in code-point order");
  }
}

function snapshotBuildInput(value: unknown): InlineReceiptBuildInput {
  canonicalJson(value);
  const input = recordAt(value, "$.build_input");
  assertExactKeys(
    input,
    [
      "authorityContext",
      "catalogue",
      "createdAt",
      "licenceObligations",
      "normalisedParameters",
      "operation",
      "policyDecision",
      "publicPolicy",
      "requestId",
      "resultCore",
      "software",
      "traceId",
      "transformations",
    ],
    "$.build_input",
  );
  return canonicalJsonClone(value) as InlineReceiptBuildInput;
}

function snapshotVerificationMaterial(value: unknown): InlineReceiptVerificationMaterial {
  canonicalJson(value);
  const material = recordAt(value, "$.verification_material");
  assertAllowedKeys(
    material,
    ["licenceObligations", "normalisedParameters", "publicPolicy", "resultCore"],
    [
      "expectedAuthorityContext",
      "expectedCatalogue",
      "expectedPolicyDecision",
      "expectedSoftware",
    ],
    "$.verification_material",
  );
  return canonicalJsonClone(value) as InlineReceiptVerificationMaterial;
}

/** Build a detached, immutable, inline-only receipt without retaining raw parameters. */
export function buildInlineReceipt(input: InlineReceiptBuildInput): InlineEvidenceReceipt {
  const snapshot = snapshotBuildInput(input);
  assertDateTime(snapshot.createdAt, "$.created_at");
  assertRequestId(snapshot.requestId, "$.request_id");
  assertTraceId(snapshot.traceId, "$.trace_id");
  if (!PUBLIC_CATALOGUE_OPERATIONS.includes(snapshot.operation)) {
    fail("$.operation.name", "must be a public catalogue operation");
  }
  assertCatalogue(snapshot.catalogue, "$.catalogue");
  assertTransformations(snapshot.transformations, snapshot.operation);
  assertSoftware(snapshot.software);
  assertIdentityLinkage(
    snapshot.authorityContext,
    snapshot.publicPolicy,
    snapshot.policyDecision,
    snapshot.operation,
    snapshot.requestId,
    snapshot.traceId,
  );

  const resultBinding = inspectResultCore(
    snapshot.resultCore,
    snapshot.operation,
    snapshot.requestId,
    snapshot.traceId,
    snapshot.catalogue,
  );
  const obligations = normaliseLicenceObligations(snapshot.licenceObligations);
  assertObligationCoverage(obligations, resultBinding.returnedRecordIds);

  // Canonicalising first also rejects raw material outside the interoperable JSON model.
  canonicalJson(snapshot.normalisedParameters);
  const core: InlineEvidenceReceiptCore = {
    schema: "gis-ai-go.evidence-receipt.v1",
    created_at: snapshot.createdAt,
    request_id: snapshot.requestId,
    trace_id: snapshot.traceId,
    operation: {
      name: snapshot.operation,
      contract_version: "v1",
      normalised_parameters: canonicalDigest(
        CANONICAL_DOMAINS.catalogueParameters,
        snapshot.normalisedParameters,
      ),
    },
    authority_context: snapshot.authorityContext,
    policy_decision: snapshot.policyDecision,
    catalogue: snapshot.catalogue,
    transformations: snapshot.transformations,
    software: snapshot.software,
    result: {
      domain: CANONICAL_DOMAINS.catalogueResultCore,
      sha256: canonicalDigest(CANONICAL_DOMAINS.catalogueResultCore, snapshot.resultCore).sha256,
      media_type: "application/json",
      returned_record_count: resultBinding.returnedRecordIds.length,
    },
    licence_obligations: obligations,
    verification: {
      status: "passed",
      canonicalisation: CANONICALISATION,
      digest_algorithm: "sha256",
      checks: RECEIPT_VERIFICATION_CHECKS,
    },
    evidence_handling: {
      delivery: "inline-only",
      persistence: "not-persisted",
      attestation: "not-attested",
    },
  };
  const receipt = buildIdentity<InlineEvidenceReceiptCore, InlineEvidenceReceipt>(
    core,
    "receipt_id",
    RECEIPT_ID_PREFIX,
    CANONICAL_DOMAINS.evidenceReceipt,
  );
  assertInlineReceiptSchema(receipt);
  return receipt;
}

function assertReceiptIdentity(receipt: InlineEvidenceReceipt): void {
  const { identity, core } = identityCore(receipt, "receipt_id", "$");
  if (!verifyContentAddress(identity, RECEIPT_ID_PREFIX, CANONICAL_DOMAINS.evidenceReceipt, core)) {
    fail("$.receipt_id", "does not match the canonical receipt content");
  }
}

function assertReceiptConstants(receipt: InlineEvidenceReceipt): void {
  if (
    receipt.schema !== "gis-ai-go.evidence-receipt.v1" ||
    receipt.operation.contract_version !== "v1" ||
    receipt.operation.normalised_parameters.domain !== CANONICAL_DOMAINS.catalogueParameters ||
    receipt.result.domain !== CANONICAL_DOMAINS.catalogueResultCore ||
    receipt.result.media_type !== "application/json" ||
    receipt.verification.status !== "passed" ||
    receipt.verification.canonicalisation !== CANONICALISATION ||
    receipt.verification.digest_algorithm !== "sha256" ||
    receipt.evidence_handling.delivery !== "inline-only" ||
    receipt.evidence_handling.persistence !== "not-persisted" ||
    receipt.evidence_handling.attestation !== "not-attested"
  ) {
    fail("$", "fixed inline, verification or digest semantics were changed");
  }
  sortedUniqueStrings(receipt.verification.checks, RECEIPT_VERIFICATION_CHECKS, "$.verification.checks");
}

/**
 * Verify the closed inline receipt envelope and its content identity without
 * claiming that independently supplied parameters or result material were replayed.
 */
export function verifyInlineReceiptStructure(receipt: unknown): boolean {
  try {
    assertInlineReceiptSchema(receipt);
    assertReceiptIdentity(receipt);
    assertReceiptConstants(receipt);
    return true;
  } catch {
    return false;
  }
}

/**
 * Verify the receipt against independently supplied parameters, result core and
 * compiled policy. Errors are bounded and never reflect the raw query material.
 */
export function verifyInlineReceipt(
  receipt: unknown,
  material: InlineReceiptVerificationMaterial,
): InlineReceiptVerificationResult {
  try {
    const snapshot = snapshotVerificationMaterial(material);
    assertInlineReceiptSchema(receipt);
    const candidate = receipt;
    assertReceiptIdentity(candidate);
    assertReceiptConstants(candidate);
    assertDateTime(candidate.created_at, "$.created_at");
    assertRequestId(candidate.request_id, "$.request_id");
    assertTraceId(candidate.trace_id, "$.trace_id");
    if (!PUBLIC_CATALOGUE_OPERATIONS.includes(candidate.operation.name)) {
      fail("$.operation.name", "must be a public catalogue operation");
    }
    assertCatalogue(candidate.catalogue, "$.catalogue");
    assertTransformations(candidate.transformations, candidate.operation.name);
    assertSoftware(candidate.software);
    assertIdentityLinkage(
      candidate.authority_context,
      snapshot.publicPolicy,
      candidate.policy_decision,
      candidate.operation.name,
      candidate.request_id,
      candidate.trace_id,
    );
    const resultBinding = inspectResultCore(
      snapshot.resultCore,
      candidate.operation.name,
      candidate.request_id,
      candidate.trace_id,
      candidate.catalogue,
    );
    const obligations = normaliseLicenceObligations(candidate.licence_obligations);
    if (!sameCanonical(obligations, candidate.licence_obligations)) {
      fail("$.licence_obligations", "must be sorted by record identifier code point");
    }
    assertObligationCoverage(obligations, resultBinding.returnedRecordIds);
    const expectedObligations = normaliseLicenceObligations(snapshot.licenceObligations);
    assertObligationCoverage(expectedObligations, resultBinding.returnedRecordIds);
    if (!sameCanonical(obligations, expectedObligations)) {
      fail("$.licence_obligations", "do not match the independently supplied exact record rights");
    }
    if (candidate.result.returned_record_count !== resultBinding.returnedRecordIds.length) {
      fail("$.result.returned_record_count", "does not match the result core");
    }
    if (
      !verifyDomainSeparatedSha256(
        candidate.operation.normalised_parameters.sha256,
        CANONICAL_DOMAINS.catalogueParameters,
        snapshot.normalisedParameters,
      )
    ) {
      fail("$.operation.normalised_parameters.sha256", "does not match the supplied parameters");
    }
    if (
      !verifyDomainSeparatedSha256(
        candidate.result.sha256,
        CANONICAL_DOMAINS.catalogueResultCore,
        snapshot.resultCore,
      )
    ) {
      fail("$.result.sha256", "does not match the supplied result core");
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
      snapshot.expectedCatalogue !== undefined &&
      !sameCanonical(candidate.catalogue, snapshot.expectedCatalogue)
    ) {
      fail("$.catalogue", "does not match the expected catalogue");
    }
    if (
      snapshot.expectedSoftware !== undefined &&
      !sameCanonical(candidate.software, snapshot.expectedSoftware)
    ) {
      fail("$.software", "does not match the expected software identity");
    }
    return Object.freeze({ valid: true, checks: RECEIPT_VERIFICATION_CHECKS, errors: [] });
  } catch (error) {
    const message = error instanceof InlineReceiptError
      ? error.message
      : error instanceof CanonicalJsonError
        ? `Inline evidence canonical material failed closed (${error.code})`
        : "Inline evidence verification failed closed";
    return Object.freeze({ valid: false, checks: [], errors: Object.freeze([message]) });
  }
}
