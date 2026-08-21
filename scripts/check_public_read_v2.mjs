import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  PUBLIC_READ_ONS_RESOURCE,
  PUBLIC_READ_ONS_RESOURCE_CORE,
  PUBLIC_READ_ONS_SELECTION_PLAN,
  PUBLIC_READ_SELECTION_PROFILE,
} from "../packages/evidence/dist/src/public-read-receipt.js";
import {
  PUBLIC_READ_AUTHORITY_CONTEXT,
} from "../packages/authority-context/dist/src/public-read-v2.js";
import {
  PUBLIC_READ_POLICY,
  PUBLIC_READ_POLICY_CORE,
} from "../packages/policy-client/dist/src/public-read-v2.js";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DOMAIN_PREFIX = "GIS-AI-GO\u0000canonical-json\u0000sha256\u0000v1\u0000";
const ADAPTER_PREFLIGHT_PATH = "providers/ons/data-api-adapter-preflight.v1.json";
const PROFILE_REGISTER_PATH = "docs/research/2026-08-19/research-pack/data/providers.json";
const ACCEPTED_PROFILE_ID = "PV-ONS-DATA";
const ACCEPTED_PROFILE_POINTER = "/providers/1";
const ACCEPTED_PROFILE_SHA256 =
  "535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622";
const ACCEPTED_ADAPTER_PREFLIGHT_GIT_BLOB = "fc511965db5d575ef4c2165aa40e6bf5ed3cae34";
const ACCEPTED_ADAPTER_PREFLIGHT_SHA256 =
  "552bed362c6c01252a5251238815819f9966af04d675a62b6479e723f040e7b7";
const SELECTION_RANKING_BRANCH_DOMAIN =
  "gis-ai-go.selection-ranking-schema-branches.v1";

function fail(message) {
  throw new Error(`Public-read v2 identity check failed: ${message}`);
}

function load(relativePath) {
  const parsed = JSON.parse(readFileSync(join(ROOT, relativePath), "utf8"));
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
    fail(`${relativePath} must contain one JSON object`);
  }
  return parsed;
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function gitBlobSha1(bytes) {
  return createHash("sha1")
    .update(`blob ${bytes.byteLength}\u0000`, "utf8")
    .update(bytes)
    .digest("hex");
}

function canonical(value) {
  if (value === null || typeof value === "boolean" || typeof value === "string") {
    return JSON.stringify(value);
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) fail("canonical material contains a non-finite number");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map(canonical).join(",")}]`;
  }
  if (typeof value !== "object") {
    fail(`canonical material contains unsupported ${typeof value}`);
  }
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) {
    fail("canonical material contains a non-plain object");
  }
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`)
    .join(",")}}`;
}

function digest(domain, value) {
  return createHash("sha256")
    .update(DOMAIN_PREFIX, "utf8")
    .update(domain, "utf8")
    .update("\u0000", "utf8")
    .update(canonical(value), "utf8")
    .digest("hex");
}

function identity(value, key, prefix, domain) {
  const { [key]: claimed, ...core } = value;
  const expected = `${prefix}:sha256:${digest(domain, core)}`;
  if (claimed !== expected) fail(`${key} does not match ${domain} canonical content`);
  return expected;
}

function equal(actual, expected, label) {
  if (canonical(actual) !== canonical(expected)) fail(`${label} differs`);
}

function deriveSelectionRankingBranches(profile) {
  const fieldOrder = profile.ranking.field_order;
  const weights = profile.ranking.weights;
  const anchors = profile.grammar.anchor_fields;
  const dimensions = profile.grammar.required_dimension_fields;
  if (
    !Array.isArray(fieldOrder) ||
    !Array.isArray(anchors) ||
    !Array.isArray(dimensions) ||
    new Set(fieldOrder).size !== fieldOrder.length ||
    anchors.length !== 4 ||
    dimensions.length !== 4 ||
    [...anchors, ...dimensions].some((field) => !fieldOrder.includes(field))
  ) {
    fail("selection profile cannot generate the closed ranking branches");
  }
  const fixedFields = new Set([...anchors, ...dimensions]);
  const optional = fieldOrder.filter((field) => !fixedFields.has(field));
  if (optional.length !== 2) {
    fail("selection profile must leave exactly edition and version optional");
  }
  for (const field of fieldOrder) {
    if (!Number.isSafeInteger(weights[field]) || weights[field] <= 0) {
      fail(`selection profile has an invalid weight for ${field}`);
    }
  }

  const branches = [];
  for (let anchorMask = 1; anchorMask < 2 ** anchors.length; anchorMask += 1) {
    for (let optionalMask = 0; optionalMask < 2 ** optional.length; optionalMask += 1) {
      const selected = new Set(dimensions);
      anchors.forEach((field, index) => {
        if ((anchorMask & (1 << index)) !== 0) selected.add(field);
      });
      optional.forEach((field, index) => {
        if ((optionalMask & (1 << index)) !== 0) selected.add(field);
      });
      const matched = fieldOrder.filter((field) => selected.has(field));
      branches.push({
        required: ["matched_constraints", "score"],
        properties: {
          matched_constraints: { const: matched },
          score: {
            const: matched.reduce((total, field) => total + weights[field], 0),
          },
        },
      });
    }
  }
  if (branches.length !== 60) {
    fail(`selection profile generated ${branches.length} ranking branches, not 60`);
  }
  return branches;
}

const resource = load("providers/fixtures/public-read-resource.example.json");
const authority = load("providers/fixtures/public-authority-context-v2.example.json");
const policy = load("packages/policy-client/src/public-read-v2.json");
const decision = load("providers/fixtures/public-policy-decision-v2.example.json");
const receipt = load("providers/fixtures/evidence-receipt-v2.example.json");
const selectionPlan = load("providers/fixtures/selection-plan.example.json");
const selectionProfile = load("profiles/public-selection-profile.v1.json");
const resourceSchema = load("schemas/public-read-resource.schema.json");
const selectionPlanSchema = load("schemas/selection-plan.schema.json");
const selectionProfileSchema = load("schemas/public-selection-profile.schema.json");
const selectionResultSchema = load("schemas/selection-resolve-result.schema.json");
const authoritySchema = load("schemas/public-authority-context-v2.schema.json");
const policySchema = load("schemas/public-policy-v2.schema.json");
const decisionSchema = load("schemas/public-policy-decision-v2.schema.json");
const publication = load("okf/source/publication.json");
const researchProviders = load(PROFILE_REGISTER_PATH);
const adapterPreflightBytes = readFileSync(join(ROOT, ADAPTER_PREFLIGHT_PATH));
if (sha256(adapterPreflightBytes) !== ACCEPTED_ADAPTER_PREFLIGHT_SHA256) {
  fail("adapter preflight does not match the accepted SHA-256");
}
if (gitBlobSha1(adapterPreflightBytes) !== ACCEPTED_ADAPTER_PREFLIGHT_GIT_BLOB) {
  fail("adapter preflight does not match the accepted Git blob");
}
const adapterPreflight = JSON.parse(adapterPreflightBytes.toString("utf8"));
if (
  adapterPreflight === null ||
  typeof adapterPreflight !== "object" ||
  Array.isArray(adapterPreflight)
) {
  fail(`${ADAPTER_PREFLIGHT_PATH} must contain one JSON object`);
}

const resourceId = identity(
  resource,
  "resource_id",
  "gis-ai-go:public-read-resource",
  "gis-ai-go.public-read-resource.v1",
);
const authorityId = identity(
  authority,
  "context_id",
  "gis-ai-go:public-authority-context",
  "gis-ai-go.public-authority-context.v2",
);
const policyId = identity(
  policy,
  "policy_id",
  "gis-ai-go:public-policy",
  "gis-ai-go.public-policy.v2",
);
const decisionId = identity(
  decision,
  "decision_id",
  "gis-ai-go:public-policy-decision",
  "gis-ai-go.public-policy-decision.v2",
);
const receiptId = identity(
  receipt,
  "receipt_id",
  "gis-ai-go:evidence-receipt",
  "gis-ai-go.evidence-receipt.v2",
);
const selectionPlanId = identity(
  selectionPlan,
  "plan_id",
  "gis-ai-go:selection-plan",
  "gis-ai-go.selection-plan.v1",
);
const selectionProfileId = identity(
  selectionProfile,
  "selection_profile_id",
  "gis-ai-go:public-selection-profile",
  "gis-ai-go.public-selection-profile.v1",
);

equal(resourceSchema.const, resource, "resource schema and fixture");
equal(selectionPlanSchema.const, selectionPlan, "selection plan schema and fixture");
equal(
  selectionProfileSchema.const,
  selectionProfile,
  "selection profile schema and checked JSON",
);
equal(PUBLIC_READ_ONS_SELECTION_PLAN, selectionPlan, "compiled selection plan and fixture");
equal(
  PUBLIC_READ_SELECTION_PROFILE,
  selectionProfile,
  "compiled selection profile and checked JSON",
);
equal(selectionProfile.candidates[0].plan, selectionPlan, "selection profile candidate plan");
if (
  selectionPlan.plan_id !== selectionPlanId ||
  selectionProfile.selection_profile_id !== selectionProfileId ||
  selectionPlan.resource_id !== resourceId ||
  selectionPlan.data_query.resource_id !== resourceId ||
  selectionProfile.resource_id !== resourceId ||
  selectionProfile.candidates[0].resource_id !== resourceId
) {
  fail("selection plan or profile identity is not bound to the reviewed resource");
}
equal(
  selectionPlan,
  {
    schema: "gis-ai-go.selection-plan.v1",
    plan_id: selectionPlanId,
    operation: "data.query",
    execution: "forbidden",
    resource_id: resourceId,
    profile: { id: resource.profile.id, sha256: resource.profile.sha256 },
    provider: resource.provider,
    data_query: {
      schema: "gis-ai-go.data-query-parameters.v1",
      resource_id: resourceId,
      dataset: {
        id: resource.dataset.id,
        edition: resource.dataset.edition,
        version: resource.dataset.version,
      },
      selections: resource.selections,
      limit: resource.limits.max_observations,
    },
    rights_sha256: digest("gis-ai-go.provider-rights.v1", resource.rights),
    controls: {
      provider_execution: false,
      caller_url: false,
      credentials: false,
      network: "not-used",
    },
  },
  "selection plan and reviewed resource projection",
);
equal(
  selectionProfile.grammar,
  {
    maximum_request_bytes: 16384,
    maximum_question_code_points: 512,
    maximum_values_per_field: 4,
    anchor_fields: [
      "candidate_record_ids",
      "constraints.profile_ids",
      "constraints.provider_ids",
      "constraints.dataset_ids",
    ],
    required_dimension_fields: [
      "constraints.dimensions.time",
      "constraints.dimensions.geography",
      "constraints.dimensions.week",
      "constraints.dimensions.causeofdeath",
    ],
  },
  "selection profile closed grammar",
);
equal(
  selectionProfile.ranking,
  {
    algorithm: "weighted-exact-constraints",
    version: "v1",
    field_order: [
      "candidate_record_ids",
      "constraints.profile_ids",
      "constraints.provider_ids",
      "constraints.dataset_ids",
      "constraints.editions",
      "constraints.versions",
      "constraints.dimensions.time",
      "constraints.dimensions.geography",
      "constraints.dimensions.week",
      "constraints.dimensions.causeofdeath",
    ],
    weights: {
      candidate_record_ids: 128,
      "constraints.profile_ids": 64,
      "constraints.provider_ids": 32,
      "constraints.dataset_ids": 16,
      "constraints.editions": 8,
      "constraints.versions": 4,
      "constraints.dimensions.time": 2,
      "constraints.dimensions.geography": 2,
      "constraints.dimensions.week": 2,
      "constraints.dimensions.causeofdeath": 2,
    },
    tie_handling: "ambiguous-no-plan",
  },
  "selection profile deterministic ranking",
);
equal(
  selectionProfile.candidates[0].accepted_values,
  {
    profile_id: resource.profile.id,
    provider_id: resource.provider.id,
    dataset_id: resource.dataset.id,
    edition: resource.dataset.edition,
    version: resource.dataset.version,
    dimensions: Object.fromEntries(
      resource.selections.map(({ dimension, option }) => [dimension, option]),
    ),
  },
  "selection candidate accepted values and reviewed resource",
);
const selectionRankingBranches = deriveSelectionRankingBranches(selectionProfile);
const selectionRankingSchema = selectionResultSchema.$defs.success_ranking;
equal(
  selectionResultSchema.$defs.constraint_field.enum,
  selectionProfile.ranking.field_order,
  "selection result constraint field order and checked profile",
);
equal(
  selectionRankingSchema.oneOf,
  selectionRankingBranches,
  "selection result generated ranking branches and checked profile",
);
const branchScores = selectionRankingBranches.map(
  (branch) => branch.properties.score.const,
);
const branchLengths = selectionRankingBranches.map(
  (branch) => branch.properties.matched_constraints.const.length,
);
equal(
  selectionRankingSchema.properties.score.minimum,
  Math.min(...branchScores),
  "selection result minimum generated score",
);
equal(
  selectionRankingSchema.properties.score.maximum,
  Math.max(...branchScores),
  "selection result maximum generated score",
);
equal(
  selectionRankingSchema.properties.matched_constraints.minItems,
  Math.min(...branchLengths),
  "selection result minimum generated field count",
);
equal(
  selectionRankingSchema.properties.matched_constraints.maxItems,
  Math.max(...branchLengths),
  "selection result maximum generated field count",
);
const selectionRankingBranchesSha256 = digest(
  SELECTION_RANKING_BRANCH_DOMAIN,
  selectionRankingBranches,
);
equal(authoritySchema.const, authority, "authority schema and fixture");
equal(policy.resources, [resource], "checked policy resource and fixture");
equal(PUBLIC_READ_ONS_RESOURCE, resource, "compiled resource and fixture");
const { resource_id: ignoredResourceId, ...resourceCore } = resource;
equal(PUBLIC_READ_ONS_RESOURCE_CORE, resourceCore, "compiled resource core and fixture");
equal(PUBLIC_READ_AUTHORITY_CONTEXT, authority, "compiled authority and fixture");
equal(PUBLIC_READ_POLICY, policy, "compiled policy and checked JSON");
const { policy_id: ignoredPolicyId, ...policyCore } = policy;
equal(PUBLIC_READ_POLICY_CORE, policyCore, "compiled policy core and checked JSON");
equal(policySchema.properties.policy_id.const, policyId, "policy schema identity");
equal(policySchema.properties.rules.prefixItems[0].const, policy.rules[0], "query rule");
equal(policySchema.properties.rules.prefixItems[1].const, policy.rules[1], "selection rule");
equal(decisionSchema.properties.schema.const, decision.schema, "decision schema discriminator");
equal(
  decisionSchema.properties.canonicalisation.const,
  decision.canonicalisation,
  "decision schema canonicalisation",
);
equal(
  decisionSchema.properties.policy_version.const,
  policy.version,
  "decision schema policy version",
);
equal(
  decisionSchema.properties.policy_default_effect.const,
  policy.default_effect,
  "decision schema policy default",
);
equal(
  decisionSchema.properties.resource_id.oneOf[1].const,
  resourceId,
  "decision schema approved resource",
);

for (const [index, rule] of policy.rules.entries()) {
  const branch = decisionSchema.oneOf[index].properties;
  equal(branch.operation.const, rule.operation, `decision schema rule ${index} operation`);
  equal(branch.resource_id.const, rule.resource_id, `decision schema rule ${index} resource`);
  equal(branch.effect.const, rule.effect, `decision schema rule ${index} effect`);
  equal(
    branch.reason_code.const,
    "public-read-operation-allowed",
    `decision schema rule ${index} reason`,
  );
  equal(branch.obligations.const, rule.obligations, `decision schema rule ${index} obligations`);
}

for (const [actual, expected, label] of [
  [decision.authority_context_id, authorityId, "decision authority identity"],
  [decision.policy_id, policyId, "decision policy identity"],
  [decision.resource_id, resourceId, "decision resource identity"],
  [decisionSchema.properties.authority_context_id.const, authorityId, "decision schema authority"],
  [decisionSchema.properties.policy_id.const, policyId, "decision schema policy"],
  [receipt.authority_context.context_id, authorityId, "receipt authority identity"],
  [receipt.policy_decision.policy_id, policyId, "receipt policy identity"],
  [receipt.resource.resource_id, resourceId, "receipt resource identity"],
]) {
  if (actual !== expected) fail(`${label} differs`);
}

equal(receipt.authority_context, authority, "receipt authority and fixture");
equal(receipt.resource, resource, "receipt resource and fixture");
equal(receipt.policy_decision, decision, "receipt decision and fixture");

if (resource.profile.source_path !== PROFILE_REGISTER_PATH) {
  fail("resource profile source path is not the immutable providers register");
}
if (
  resource.profile.id !== ACCEPTED_PROFILE_ID ||
  resource.profile.source_pointer !== ACCEPTED_PROFILE_POINTER ||
  resource.profile.sha256 !== ACCEPTED_PROFILE_SHA256
) {
  fail("resource profile does not match the accepted immutable provider record");
}
const pointerMatch = /^\/providers\/(0|[1-9][0-9]*)$/u.exec(resource.profile.source_pointer);
if (pointerMatch === null || !Array.isArray(researchProviders.providers)) {
  fail("resource profile pointer is not a providers-array JSON pointer");
}
const profileIndex = Number(pointerMatch[1]);
const researchProfile = researchProviders.providers[profileIndex];
if (researchProfile === undefined || researchProfile.id !== resource.profile.id) {
  fail("resource profile pointer does not select the claimed provider");
}
const researchProfileDigest = sha256(Buffer.from(`${canonical(researchProfile)}\n`, "utf8"));
if (researchProfileDigest !== ACCEPTED_PROFILE_SHA256) {
  fail("immutable provider record does not match the accepted SHA-256");
}
if (resource.profile.sha256 !== researchProfileDigest) {
  fail("resource profile digest does not match the immutable provider record");
}
if (
  !Array.isArray(publication.selected?.research_provider_ids) ||
  !publication.selected.research_provider_ids.includes(resource.profile.id) ||
  publication.selected?.research_provider_sha256_by_id?.[ACCEPTED_PROFILE_ID] !==
    ACCEPTED_PROFILE_SHA256
) {
  fail("resource profile is not bound by the publication selection inventory");
}

const observationRoute = adapterPreflight.egressPolicy.routes.find(
  (route) => route.path.endsWith("/observations"),
);
if (observationRoute === undefined) fail("adapter preflight has no observation route");
equal(
  resource.provider,
  {
    id: adapterPreflight.provider.id,
    adapter_id: adapterPreflight.adapterId,
    adapter_version: "1",
  },
  "resource provider and accepted adapter preflight",
);
equal(
  resource.dataset,
  {
    id: adapterPreflight.providerVersion.datasetId,
    edition: adapterPreflight.providerVersion.edition,
    version: adapterPreflight.providerVersion.versionId,
    version_uri: adapterPreflight.providerVersion.versionUri,
    source_date: adapterPreflight.providerVersion.sourceDate,
    dimension_order: adapterPreflight.providerVersion.dimensionOrder,
  },
  "resource dataset and accepted adapter preflight",
);
equal(
  resource.selections,
  observationRoute.queryParameters.map(({ name, value }) => ({ dimension: name, option: value })),
  "resource selections and accepted adapter route",
);
equal(resource.selections, adapterPreflight.probe.selection, "resource selections and probe");
equal(
  resource.rights,
  {
    state: adapterPreflight.rights.state,
    licence: adapterPreflight.rights.licence,
    licence_uri: adapterPreflight.rights.licenceUri,
    attribution: adapterPreflight.rights.attribution,
    obligations: adapterPreflight.rights.obligations,
    exceptions: adapterPreflight.rights.exceptions,
    evidence_uris: adapterPreflight.rights.evidenceUris,
    reviewed_at: adapterPreflight.rights.reviewedAt,
  },
  "resource rights and accepted adapter preflight",
);
equal(
  resource.limits,
  {
    max_observations: adapterPreflight.estimate.maxObservations,
    max_attempts: adapterPreflight.estimate.maxAttempts,
    max_compressed_response_bytes: adapterPreflight.estimate.maxCompressedResponseBytes,
    max_decompressed_response_bytes: adapterPreflight.estimate.maxDecompressedResponseBytes,
    max_canonical_response_bytes: adapterPreflight.estimate.maxCanonicalResponseBytes,
  },
  "resource limits and accepted adapter estimate",
);

console.log(
  `Verified public-read v2 identities: resource ${resourceId.slice(-64)}, ` +
    `authority ${authorityId.slice(-64)}, policy ${policyId.slice(-64)}, ` +
    `decision ${decisionId.slice(-64)}, receipt ${receiptId.slice(-64)}, ` +
    `selection plan ${selectionPlanId.slice(-64)}, ` +
    `selection profile ${selectionProfileId.slice(-64)}, ` +
    `60 ranking branches ${selectionRankingBranchesSha256}.`,
);
