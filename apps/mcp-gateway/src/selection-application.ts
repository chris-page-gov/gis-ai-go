import { types as utilTypes } from "node:util";

import {
  PUBLIC_READ_ONS_RESOURCE,
  PUBLIC_READ_ONS_SELECTION_PLAN,
  PUBLIC_READ_SELECTION_PROFILE,
  PUBLIC_SELECTION_WARNINGS,
  PublicEvidenceLedger,
  PublicEvidenceLedgerError,
  buildPublicReadReceipt,
  canonicalJson,
  canonicalJsonClone,
  publicReadResultEvidenceBinding,
  verifyPublicReadReceipt,
  verifyPublicSelectionProfile,
  type EvidenceSoftwareIdentity,
  type PublicEvidenceStorageReference,
  type PublicReadEvidenceReceipt,
  type PublicReadReceiptVerificationMaterial,
  type PublicSelectionConstraintField,
  type PublicSelectionPlan,
} from "@gis-ai-go/evidence";
import {
  evaluatePublicReadPolicy,
  isAllowedPublicReadOperation,
} from "@gis-ai-go/policy-client";

import {
  assertCatalogueProblemContext,
  type CatalogueProblemContext,
} from "./problem.js";

const REQUEST_KEYS = ["candidate_record_ids", "constraints", "question"] as const;
const CONSTRAINT_KEYS = [
  "dataset_ids",
  "dimensions",
  "editions",
  "profile_ids",
  "provider_ids",
  "versions",
] as const;
const DIMENSION_KEYS = ["causeofdeath", "geography", "time", "week"] as const;
const IDENTIFIER = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const UNSAFE_TEXT =
  /[\u0000-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const MAX_REQUEST_BYTES =
  PUBLIC_READ_SELECTION_PROFILE.grammar.maximum_request_bytes;
const MAX_VALUES =
  PUBLIC_READ_SELECTION_PROFILE.grammar.maximum_values_per_field;

type SelectionDimension = (typeof DIMENSION_KEYS)[number];

export interface SelectionResolveConstraints {
  readonly profile_ids?: readonly string[];
  readonly provider_ids?: readonly string[];
  readonly dataset_ids?: readonly string[];
  readonly editions?: readonly string[];
  readonly versions?: readonly string[];
  readonly dimensions?: Readonly<
    Partial<Record<SelectionDimension, readonly string[]>>
  >;
}

export interface SelectionResolveRequest {
  readonly question: string;
  readonly candidate_record_ids?: readonly string[];
  readonly constraints: SelectionResolveConstraints;
}

export interface SelectionResolveNormalisedParameters {
  readonly schema: "gis-ai-go.selection-resolve-parameters.v1";
  readonly profile_id: "PV-ONS-DATA";
  readonly provider_id: "ons-data-api";
  readonly dataset: {
    readonly id: "weekly-deaths-region";
    readonly edition: "time-series";
    readonly version: "121";
  };
  readonly selections: typeof PUBLIC_READ_ONS_RESOURCE.selections;
}

export interface SelectionResolveRanking {
  readonly algorithm: "weighted-exact-constraints";
  readonly version: "v1";
  readonly selection_profile_id: string;
  readonly selected_candidate_id: string;
  readonly considered_candidates: 1;
  readonly score: number;
  readonly matched_constraints: readonly PublicSelectionConstraintField[];
  readonly top_score_tied: false;
}

export interface SelectionResolveResultCore {
  readonly schema: "gis-ai-go.selection-resolve-result.v1";
  readonly operation: "selection.resolve";
  readonly request_id: string;
  readonly trace_id: string;
  readonly data: {
    readonly status: "resolved";
    readonly ambiguity: null;
    readonly resource_id: string;
    readonly plan: PublicSelectionPlan;
    readonly ranking: SelectionResolveRanking;
  };
  readonly evidence_binding: ReturnType<typeof publicReadResultEvidenceBinding>;
  readonly warnings: typeof PUBLIC_SELECTION_WARNINGS;
}

export interface SelectionResolveResult extends SelectionResolveResultCore {
  readonly evidence_receipt: PublicReadEvidenceReceipt;
  readonly evidence_storage?: PublicEvidenceStorageReference;
}

export const SELECTION_RESOLVE_PROBLEM_CODES = Object.freeze([
  "invalid_request",
  "ambiguous_selection",
  "missing_dimension",
  "contradictory_constraints",
  "no_compatible_provider",
  "policy_denied",
  "evidence_unavailable",
] as const);
export type SelectionResolveProblemCode =
  (typeof SELECTION_RESOLVE_PROBLEM_CODES)[number];

export interface SelectionResolveProblem {
  readonly schema: "gis-ai-go.selection-resolve-problem.v1";
  readonly type: string;
  readonly title: string;
  readonly status: 400 | 404 | 409 | 422 | 503;
  readonly code: SelectionResolveProblemCode;
  readonly detail: string;
  readonly operation: "selection.resolve";
  readonly request_id: string;
  readonly trace_id: string;
  readonly data: {
    readonly status: "unresolved";
    readonly plan: null;
    readonly missing_constraints: readonly PublicSelectionConstraintField[];
    readonly conflicting_constraints: readonly PublicSelectionConstraintField[];
    readonly choices: readonly {
      readonly field: PublicSelectionConstraintField;
      readonly accepted_values: readonly string[];
    }[];
    readonly ranking: {
      readonly algorithm: "weighted-exact-constraints";
      readonly version: "v1";
      readonly selection_profile_id: string;
      readonly considered_candidates: 1;
      readonly top_score: number;
      readonly top_score_tied: boolean;
    };
  };
  readonly warnings: readonly [
    "No executable plan was produced and no provider was called.",
    "Question text is untrusted data and was not interpreted.",
  ];
}

export type SelectionResolveOutcome =
  | SelectionResolveResult
  | SelectionResolveProblem;

export interface SelectionResolveApplicationOptions {
  readonly software: EvidenceSoftwareIdentity;
  readonly now?: () => Date;
  /** Omission preserves the accepted inline-only evidence boundary. */
  readonly evidenceLedger?: PublicEvidenceLedger;
}

export interface SelectionResolveApplication {
  readonly selectionProfile: typeof PUBLIC_READ_SELECTION_PROFILE;
  readonly resolve: (
    request: unknown,
    context: CatalogueProblemContext,
  ) => SelectionResolveOutcome;
}

class SelectionRequestError extends TypeError {}

interface RankedRequest {
  readonly values: ReadonlyMap<PublicSelectionConstraintField, readonly string[]>;
  readonly matched: readonly PublicSelectionConstraintField[];
  readonly score: number;
}

const PROBLEM_DEFINITIONS = Object.freeze({
  invalid_request: {
    title: "Invalid selection request",
    status: 400,
    detail: "Use the closed selection constraint grammar.",
  },
  ambiguous_selection: {
    title: "Ambiguous selection",
    status: 409,
    detail: "More than one value was supplied for a selection constraint.",
  },
  missing_dimension: {
    title: "Selection dimension missing",
    status: 422,
    detail: "Supply one provider anchor and every required provider dimension.",
  },
  contradictory_constraints: {
    title: "Selection constraints contradict",
    status: 422,
    detail: "The supplied constraints do not describe one reviewed selection.",
  },
  no_compatible_provider: {
    title: "No compatible provider",
    status: 404,
    detail: "No reviewed public provider matches the supplied constraints.",
  },
  policy_denied: {
    title: "Selection policy denied",
    status: 503,
    detail: "The public-read policy did not authorise this selection.",
  },
  evidence_unavailable: {
    title: "Selection evidence unavailable",
    status: 503,
    detail: "Durable evidence could not be verified for this selection.",
  },
} as const satisfies Readonly<
  Record<
    SelectionResolveProblemCode,
    {
      readonly title: string;
      readonly status: 400 | 404 | 409 | 422 | 503;
      readonly detail: string;
    }
  >
>);

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

function assertExactKeys(
  value: Record<string, unknown>,
  allowed: readonly string[],
  required: readonly string[],
): void {
  const keys = Object.keys(value).sort();
  if (
    keys.some((key) => !allowed.includes(key)) ||
    required.some((key) => !Object.hasOwn(value, key))
  ) {
    throw new SelectionRequestError();
  }
}

function normaliseIdentifierArray(value: unknown): readonly string[] {
  if (!Array.isArray(value) || value.length < 1 || value.length > MAX_VALUES) {
    throw new SelectionRequestError();
  }
  const normalised = value.map((item) => {
    if (
      typeof item !== "string" ||
      Array.from(item).length > 128 ||
      !IDENTIFIER.test(item) ||
      item.normalize("NFC") !== item
    ) {
      throw new SelectionRequestError();
    }
    return item;
  });
  if (new Set(normalised).size !== normalised.length) {
    throw new SelectionRequestError();
  }
  return Object.freeze([...normalised].sort());
}

function normaliseRequest(value: unknown): SelectionResolveRequest {
  let snapshot: unknown;
  try {
    snapshot = canonicalJsonClone(value);
  } catch {
    throw new SelectionRequestError();
  }
  if (
    new TextEncoder().encode(canonicalJson(snapshot)).byteLength > MAX_REQUEST_BYTES ||
    !isPlainObject(snapshot)
  ) {
    throw new SelectionRequestError();
  }
  assertExactKeys(snapshot, REQUEST_KEYS, ["constraints", "question"]);
  if (
    typeof snapshot.question !== "string" ||
    Array.from(snapshot.question).length < 1 ||
    Array.from(snapshot.question).length >
      PUBLIC_READ_SELECTION_PROFILE.grammar.maximum_question_code_points ||
    snapshot.question.trim().length === 0 ||
    snapshot.question.normalize("NFC") !== snapshot.question ||
    UNSAFE_TEXT.test(snapshot.question)
  ) {
    throw new SelectionRequestError();
  }
  if (!isPlainObject(snapshot.constraints)) {
    throw new SelectionRequestError();
  }
  assertExactKeys(snapshot.constraints, CONSTRAINT_KEYS, []);
  if (Object.keys(snapshot.constraints).length < 1) {
    throw new SelectionRequestError();
  }
  const constraints: Record<string, unknown> = {};
  for (const key of CONSTRAINT_KEYS.filter((key) => key !== "dimensions")) {
    if (Object.hasOwn(snapshot.constraints, key)) {
      constraints[key] = normaliseIdentifierArray(snapshot.constraints[key]);
    }
  }
  if (Object.hasOwn(snapshot.constraints, "dimensions")) {
    const dimensions = snapshot.constraints.dimensions;
    if (!isPlainObject(dimensions)) throw new SelectionRequestError();
    assertExactKeys(dimensions, DIMENSION_KEYS, []);
    if (Object.keys(dimensions).length < 1) throw new SelectionRequestError();
    constraints.dimensions = Object.fromEntries(
      DIMENSION_KEYS.filter((key) => Object.hasOwn(dimensions, key)).map((key) => [
        key,
        normaliseIdentifierArray(dimensions[key]),
      ]),
    );
  }
  return canonicalJsonClone({
    question: snapshot.question,
    ...(Object.hasOwn(snapshot, "candidate_record_ids")
      ? { candidate_record_ids: normaliseIdentifierArray(snapshot.candidate_record_ids) }
      : {}),
    constraints,
  }) as SelectionResolveRequest;
}

function requestValues(
  request: SelectionResolveRequest,
): ReadonlyMap<PublicSelectionConstraintField, readonly string[]> {
  const values = new Map<PublicSelectionConstraintField, readonly string[]>();
  if (request.candidate_record_ids !== undefined) {
    values.set("candidate_record_ids", request.candidate_record_ids);
  }
  const fields = [
    ["profile_ids", "constraints.profile_ids"],
    ["provider_ids", "constraints.provider_ids"],
    ["dataset_ids", "constraints.dataset_ids"],
    ["editions", "constraints.editions"],
    ["versions", "constraints.versions"],
  ] as const;
  for (const [key, field] of fields) {
    const selected = request.constraints[key];
    if (selected !== undefined) values.set(field, selected);
  }
  for (const dimension of DIMENSION_KEYS) {
    const selected = request.constraints.dimensions?.[dimension];
    if (selected !== undefined) {
      values.set(`constraints.dimensions.${dimension}`, selected);
    }
  }
  return values;
}

function acceptedValue(field: PublicSelectionConstraintField): string {
  const candidate = PUBLIC_READ_SELECTION_PROFILE.candidates[0];
  const accepted = candidate.accepted_values;
  const values: Readonly<Record<PublicSelectionConstraintField, string>> = {
    candidate_record_ids: candidate.record_id,
    "constraints.profile_ids": accepted.profile_id,
    "constraints.provider_ids": accepted.provider_id,
    "constraints.dataset_ids": accepted.dataset_id,
    "constraints.editions": accepted.edition,
    "constraints.versions": accepted.version,
    "constraints.dimensions.time": accepted.dimensions.time,
    "constraints.dimensions.geography": accepted.dimensions.geography,
    "constraints.dimensions.week": accepted.dimensions.week,
    "constraints.dimensions.causeofdeath": accepted.dimensions.causeofdeath,
  };
  return values[field];
}

function rankRequest(request: SelectionResolveRequest): RankedRequest {
  const values = requestValues(request);
  const matched = PUBLIC_READ_SELECTION_PROFILE.ranking.field_order.filter((field) =>
    values.get(field)?.includes(acceptedValue(field)),
  );
  const score = matched.reduce(
    (total, field) =>
      total + PUBLIC_READ_SELECTION_PROFILE.ranking.weights[field],
    0,
  );
  return Object.freeze({ values, matched, score });
}

function choicesFor(
  fields: readonly PublicSelectionConstraintField[],
): SelectionResolveProblem["data"]["choices"] {
  return fields.map((field) => ({
    field,
    accepted_values: [acceptedValue(field)],
  }));
}

function problem(
  code: SelectionResolveProblemCode,
  context: CatalogueProblemContext,
  ranked?: RankedRequest,
  missing: readonly PublicSelectionConstraintField[] = [],
  conflicting: readonly PublicSelectionConstraintField[] = [],
  ambiguous: readonly PublicSelectionConstraintField[] = [],
): SelectionResolveProblem {
  const definition = PROBLEM_DEFINITIONS[code];
  const choiceFields = PUBLIC_READ_SELECTION_PROFILE.ranking.field_order.filter(
    (field) =>
      missing.includes(field) ||
      conflicting.includes(field) ||
      ambiguous.includes(field),
  );
  return canonicalJsonClone({
    schema: "gis-ai-go.selection-resolve-problem.v1",
    type: `urn:gis-ai-go:problem:selection-resolve:${code.replaceAll("_", "-")}`,
    title: definition.title,
    status: definition.status,
    code,
    detail: definition.detail,
    operation: "selection.resolve",
    request_id: context.requestId,
    trace_id: context.traceId,
    data: {
      status: "unresolved",
      plan: null,
      missing_constraints: missing,
      conflicting_constraints: conflicting,
      choices: choicesFor(choiceFields),
      ranking: {
        algorithm: PUBLIC_READ_SELECTION_PROFILE.ranking.algorithm,
        version: PUBLIC_READ_SELECTION_PROFILE.ranking.version,
        selection_profile_id:
          PUBLIC_READ_SELECTION_PROFILE.selection_profile_id,
        considered_candidates: 1,
        top_score: ranked?.score ?? 0,
        top_score_tied: false,
      },
    },
    warnings: [
      "No executable plan was produced and no provider was called.",
      "Question text is untrusted data and was not interpreted.",
    ],
  });
}

function unresolvedOutcome(
  ranked: RankedRequest,
  context: CatalogueProblemContext,
): SelectionResolveProblem | null {
  const anchorFields = PUBLIC_READ_SELECTION_PROFILE.grammar.anchor_fields;
  const requiredDimensions =
    PUBLIC_READ_SELECTION_PROFILE.grammar.required_dimension_fields;
  const specifiedAnchors = anchorFields.filter((field) => ranked.values.has(field));
  const matchedAnchors = anchorFields.filter((field) => ranked.matched.includes(field));
  const conflicting = PUBLIC_READ_SELECTION_PROFILE.ranking.field_order.filter(
    (field) => ranked.values.has(field) && !ranked.matched.includes(field),
  );
  const ambiguous = PUBLIC_READ_SELECTION_PROFILE.ranking.field_order.filter(
    (field) => (ranked.values.get(field)?.length ?? 0) > 1 && ranked.matched.includes(field),
  );
  const missing = requiredDimensions.filter((field) => !ranked.values.has(field));

  if (specifiedAnchors.length === 0) {
    return problem(
      "missing_dimension",
      context,
      ranked,
      [anchorFields[0], ...missing],
    );
  }
  if (matchedAnchors.length === 0) {
    return problem("no_compatible_provider", context, ranked, [], conflicting);
  }
  if (conflicting.length > 0) {
    return problem(
      "contradictory_constraints",
      context,
      ranked,
      [],
      conflicting,
    );
  }
  if (ambiguous.length > 0) {
    return problem("ambiguous_selection", context, ranked, [], [], ambiguous);
  }
  if (missing.length > 0) {
    return problem("missing_dimension", context, ranked, missing);
  }
  return null;
}

function receiptTimestamp(now: () => Date): string {
  const timestamp = now();
  if (!(timestamp instanceof Date) || !Number.isFinite(timestamp.valueOf())) {
    throw new TypeError("Selection application clock must return a valid Date");
  }
  return timestamp.toISOString();
}

function normalisedParameters(): SelectionResolveNormalisedParameters {
  return canonicalJsonClone({
    schema: "gis-ai-go.selection-resolve-parameters.v1",
    profile_id: PUBLIC_READ_ONS_RESOURCE.profile.id,
    provider_id: PUBLIC_READ_ONS_RESOURCE.provider.id,
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
    },
    selections: PUBLIC_READ_ONS_RESOURCE.selections,
  });
}

function resultCore(
  ranked: RankedRequest,
  context: CatalogueProblemContext,
): SelectionResolveResultCore {
  return canonicalJsonClone({
    schema: "gis-ai-go.selection-resolve-result.v1",
    operation: "selection.resolve",
    request_id: context.requestId,
    trace_id: context.traceId,
    data: {
      status: "resolved",
      ambiguity: null,
      resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
      plan: PUBLIC_READ_ONS_SELECTION_PLAN,
      ranking: {
        algorithm: PUBLIC_READ_SELECTION_PROFILE.ranking.algorithm,
        version: PUBLIC_READ_SELECTION_PROFILE.ranking.version,
        selection_profile_id:
          PUBLIC_READ_SELECTION_PROFILE.selection_profile_id,
        selected_candidate_id:
          PUBLIC_READ_SELECTION_PROFILE.candidates[0].candidate_id,
        considered_candidates: 1,
        score: ranked.score,
        matched_constraints: ranked.matched,
        top_score_tied: false,
      },
    },
    evidence_binding: publicReadResultEvidenceBinding(),
    warnings: PUBLIC_SELECTION_WARNINGS,
  });
}

function assertConstructorOptions(
  options: SelectionResolveApplicationOptions,
): void {
  if (!isPlainObject(options)) {
    throw new TypeError("Selection application options must be a closed plain object");
  }
  const ownKeys = Reflect.ownKeys(options);
  const keys = ownKeys.filter((key): key is string => typeof key === "string").sort();
  const allowed = ["evidenceLedger", "now", "software"];
  if (
    ownKeys.length !== keys.length ||
    keys.some((key) => !allowed.includes(key)) ||
    !Object.hasOwn(options, "software") ||
    keys.some((key) => {
      const descriptor = Object.getOwnPropertyDescriptor(options, key);
      return descriptor === undefined || !("value" in descriptor) || !descriptor.enumerable;
    }) ||
    (options.now !== undefined && typeof options.now !== "function") ||
    (options.evidenceLedger !== undefined &&
      !(options.evidenceLedger instanceof PublicEvidenceLedger))
  ) {
    throw new TypeError("Selection application options are invalid");
  }
}

/**
 * Create the inactive deterministic resolver. It has no adapter, network,
 * execution, transport, registry or lifecycle activation dependency.
 */
export function createSelectionResolveApplication(
  options: SelectionResolveApplicationOptions,
): SelectionResolveApplication {
  assertConstructorOptions(options);
  if (!verifyPublicSelectionProfile(PUBLIC_READ_SELECTION_PROFILE)) {
    throw new Error("The reviewed public selection profile failed closed");
  }
  const software = canonicalJsonClone(options.software);
  const now = options.now ?? (() => new Date());
  const ledger = options.evidenceLedger;
  if (ledger !== undefined) ledger.verify();

  return Object.freeze({
    selectionProfile: PUBLIC_READ_SELECTION_PROFILE,
    resolve(request: unknown, suppliedContext: CatalogueProblemContext) {
      let context: CatalogueProblemContext;
      try {
        context = canonicalJsonClone(suppliedContext);
      } catch {
        throw new TypeError("Selection context must be detached canonical JSON");
      }
      assertCatalogueProblemContext(context);

      let normalisedRequest: SelectionResolveRequest;
      try {
        normalisedRequest = normaliseRequest(request);
      } catch (error) {
        if (error instanceof SelectionRequestError) {
          return problem("invalid_request", context);
        }
        throw error;
      }
      const ranked = rankRequest(normalisedRequest);
      const unresolved = unresolvedOutcome(ranked, context);
      if (unresolved !== null) return unresolved;

      const policy = evaluatePublicReadPolicy({
        requestId: context.requestId,
        traceId: context.traceId,
        operation: "selection.resolve",
        resource: PUBLIC_READ_ONS_RESOURCE,
      });
      if (!isAllowedPublicReadOperation(policy, "selection.resolve")) {
        return problem("policy_denied", context, ranked);
      }

      const parameters = normalisedParameters();
      const core = resultCore(ranked, context);
      const receipt = buildPublicReadReceipt({
        createdAt: receiptTimestamp(now),
        requestId: context.requestId,
        traceId: context.traceId,
        operation: "selection.resolve",
        normalisedParameters: parameters,
        authorityContext: policy.authorityContext,
        publicPolicy: policy.policy,
        policyDecision: policy.decision,
        resource: PUBLIC_READ_ONS_RESOURCE,
        transformations: [
          { name: "normalise-public-read-parameters", version: "v1" },
          { name: "resolve-fixed-selection-profile", version: "v1" },
          { name: "project-public-read-result-core", version: "v1" },
        ],
        software,
        resultCore: core,
      });
      const verificationMaterial: PublicReadReceiptVerificationMaterial = {
        normalisedParameters: parameters,
        resultCore: core,
        publicPolicy: policy.policy,
        expectedAuthorityContext: policy.authorityContext,
        expectedPolicyDecision: policy.decision,
        expectedResource: PUBLIC_READ_ONS_RESOURCE,
        expectedSoftware: software,
      };
      if (!verifyPublicReadReceipt(receipt, verificationMaterial).valid) {
        throw new Error("Selection application produced unverifiable public evidence");
      }

      let storage: PublicEvidenceStorageReference | undefined;
      if (ledger !== undefined) {
        try {
          storage = ledger.persistReceipt(receipt, verificationMaterial).reference;
        } catch (error) {
          if (error instanceof PublicEvidenceLedgerError) {
            return problem("evidence_unavailable", context, ranked);
          }
          throw error;
        }
      }
      return canonicalJsonClone({
        ...core,
        evidence_receipt: receipt,
        ...(storage === undefined ? {} : { evidence_storage: storage }),
      });
    },
  });
}
