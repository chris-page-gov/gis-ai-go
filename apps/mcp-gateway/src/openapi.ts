import { readFileSync } from "node:fs";

import openApiTemplate from "../openapi/catalogue-api.openapi.json" with { type: "json" };

export const CATALOGUE_API_OPERATIONS = Object.freeze([
  "catalogue.describe",
  "catalogue.search",
] as const);
export const EVIDENCE_API_OPERATIONS = Object.freeze([
  "evidence.inspect",
] as const);
export const PUBLIC_READ_API_OPERATIONS = Object.freeze([
  "selection.resolve",
  "data.query",
] as const);
export const GATEWAY_API_OPERATIONS = Object.freeze([
  ...CATALOGUE_API_OPERATIONS,
  ...EVIDENCE_API_OPERATIONS,
  ...PUBLIC_READ_API_OPERATIONS,
] as const);

export type CatalogueApiOperation = (typeof CATALOGUE_API_OPERATIONS)[number];
export type EvidenceApiOperation = (typeof EVIDENCE_API_OPERATIONS)[number];
export type PublicReadApiOperation = (typeof PUBLIC_READ_API_OPERATIONS)[number];
export type GatewayApiOperation = (typeof GATEWAY_API_OPERATIONS)[number];

export interface OpenApiDocument extends Readonly<Record<string, unknown>> {
  readonly paths: Readonly<Record<string, unknown>>;
}

export type CatalogueJsonSchema = Readonly<Record<string, unknown>>;

const OPERATION_PATHS: Readonly<Record<GatewayApiOperation, string>> = Object.freeze({
  "catalogue.describe": "/catalogue/describe",
  "catalogue.search": "/catalogue/search",
  "evidence.inspect": "/evidence/inspect",
  "selection.resolve": "/selection/resolve",
  "data.query": "/data/query",
});

const OPERATION_RESULT_SCHEMA_IDS: Readonly<Record<CatalogueApiOperation, string>> =
  Object.freeze({
    "catalogue.describe": "urn:gis-ai-go:schema:catalogue-describe-result:v1",
    "catalogue.search": "urn:gis-ai-go:schema:catalogue-search-result:v1",
  });

function sharedSchema(filename: string): unknown {
  const candidates = [
    new URL(`../../../schemas/${filename}`, import.meta.url),
    new URL(`../../../../schemas/${filename}`, import.meta.url),
  ];
  for (const candidate of candidates) {
    let source: string;
    try {
      source = readFileSync(candidate, "utf8");
    } catch (error) {
      if (
        typeof error === "object" &&
        error !== null &&
        "code" in error &&
        error.code === "ENOENT"
      ) {
        continue;
      }
      throw error;
    }
    return JSON.parse(source) as unknown;
  }
  throw new Error("The canonical catalogue schemas are unavailable");
}

const catalogueDescribeRequestSchema = sharedSchema(
  "catalogue-describe-request.schema.json",
);
const catalogueProblemSchema = sharedSchema("catalogue-problem.schema.json");
const catalogueResultSchema = sharedSchema("catalogue-result.schema.json");
const catalogueSearchRequestSchema = sharedSchema(
  "catalogue-search-request.schema.json",
);
const evidenceInspectRequestSchema = sharedSchema(
  "evidence-inspect-request.schema.json",
);
const evidenceInspectRequestV2Schema = sharedSchema(
  "evidence-inspect-request-v2.schema.json",
);
const evidenceInspectOperationRequestSchema = sharedSchema(
  "evidence-inspect-operation-request.schema.json",
);
const evidenceInspectOperationResultV3Schema = sharedSchema(
  "evidence-inspect-operation-result-v3.schema.json",
);
const evidenceInspectResultSchema = sharedSchema(
  "evidence-inspect-result.schema.json",
);
const evidenceInspectResultV2Schema = sharedSchema(
  "evidence-inspect-result-v2.schema.json",
);
const evidenceInspectResultV3Schema = sharedSchema(
  "evidence-inspect-result-v3.schema.json",
);
const evidenceLedgerEventSchema = sharedSchema(
  "evidence-ledger-event.schema.json",
);
const evidenceReceiptSchema = sharedSchema("evidence-receipt.schema.json");
const evidenceReceiptV2Schema = sharedSchema("evidence-receipt-v2.schema.json");
const evidenceReceiptV3Schema = sharedSchema("evidence-receipt-v3.schema.json");
const publicEvidenceRecordSchema = sharedSchema(
  "public-evidence-record.schema.json",
);
const publicEvidenceRecordV2Schema = sharedSchema(
  "public-evidence-record-v2.schema.json",
);
const publicAuthorityContextSchema = sharedSchema(
  "public-authority-context.schema.json",
);
const publicAuthorityContextV2Schema = sharedSchema(
  "public-authority-context-v2.schema.json",
);
const publicAuthorityContextV3Schema = sharedSchema(
  "public-authority-context-v3.schema.json",
);
const publicPolicyDecisionSchema = sharedSchema(
  "public-policy-decision.schema.json",
);
const publicPolicyDecisionV2Schema = sharedSchema(
  "public-policy-decision-v2.schema.json",
);
const publicPolicyDecisionV3Schema = sharedSchema(
  "public-policy-decision-v3.schema.json",
);
const publicReadResourceSchema = sharedSchema("public-read-resource.schema.json");
const selectionResolveRequestSchema = sharedSchema(
  "selection-resolve-request.schema.json",
);
const selectionResolveResultSchema = sharedSchema(
  "selection-resolve-result.schema.json",
);
const selectionResolveProblemSchema = sharedSchema(
  "selection-resolve-problem.schema.json",
);
const selectionPlanSchema = sharedSchema("selection-plan.schema.json");
const dataQueryParametersSchema = sharedSchema(
  "data-query-parameters.schema.json",
);
const dataQueryRequestSchema = sharedSchema("data-query-request.schema.json");
const dataQueryResultSchema = sharedSchema("data-query-result.schema.json");
const dataQueryProblemSchema = sharedSchema("data-query-problem.schema.json");
const dataQueryReconciliationProblemSchema = sharedSchema(
  "data-query-reconciliation-problem.schema.json",
);
const dataQueryOperationProblemSchema = sharedSchema(
  "data-query-operation-problem.schema.json",
);

function deepFreeze<T>(value: T, seen = new WeakSet<object>()): T {
  if (value === null || typeof value !== "object" || seen.has(value)) return value;
  seen.add(value);
  for (const child of Object.values(value as Record<string, unknown>)) {
    deepFreeze(child, seen);
  }
  return Object.freeze(value);
}

function cloneTemplate(): Record<string, unknown> {
  return JSON.parse(JSON.stringify(openApiTemplate)) as Record<string, unknown>;
}

function cloneJson(value: unknown): Record<string, unknown> {
  return JSON.parse(JSON.stringify(value)) as Record<string, unknown>;
}

function objectValue(value: unknown, label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be a JSON object`);
  }
  return value as Record<string, unknown>;
}

function rewriteReferences(
  value: unknown,
  localDefinitionPrefix: string,
  externalReferences: Readonly<Record<string, string>>,
): void {
  if (Array.isArray(value)) {
    value.forEach((item) => rewriteReferences(item, localDefinitionPrefix, externalReferences));
    return;
  }
  if (value === null || typeof value !== "object") return;
  const record = value as Record<string, unknown>;
  if (typeof record.$ref === "string") {
    const external = externalReferences[record.$ref];
    if (external !== undefined) {
      record.$ref = external;
    } else if (localDefinitionPrefix !== "" && record.$ref.startsWith("#/$defs/")) {
      record.$ref = `#/$defs/${localDefinitionPrefix}_${record.$ref.slice(8)}`;
    }
  }
  Object.values(record).forEach((item) =>
    rewriteReferences(item, localDefinitionPrefix, externalReferences));
}

function embedSchemaResource(
  schema: unknown,
  definitionName: string,
  definitionPrefix: string,
  externalReferences: Readonly<Record<string, string>>,
  rootDefinitions: Record<string, unknown>,
): void {
  const resource = cloneJson(schema);
  delete resource.$schema;
  delete resource.$id;
  const nestedDefinitions = resource.$defs === undefined
    ? {}
    : cloneJson(objectValue(resource.$defs, `${definitionName} definitions`));
  delete resource.$defs;
  rewriteReferences(resource, definitionPrefix, externalReferences);
  rootDefinitions[definitionName] = resource;
  for (const [name, definition] of Object.entries(nestedDefinitions)) {
    rewriteReferences(definition, definitionPrefix, externalReferences);
    rootDefinitions[`${definitionPrefix}_${name}`] = definition;
  }
}

function catalogueOperationResultSchema(
  operation: CatalogueApiOperation,
): CatalogueJsonSchema {
  const canonical = cloneJson(catalogueResultSchema);
  const variants = canonical.oneOf;
  if (!Array.isArray(variants)) throw new TypeError("Catalogue result schema must use oneOf");
  const selected = variants.find((candidate) => {
    const schema = objectValue(candidate, "Catalogue result variant");
    const properties = objectValue(schema.properties, "Catalogue result properties");
    const operationSchema = objectValue(properties.operation, "Catalogue result operation");
    return operationSchema.const === operation;
  });
  if (selected === undefined) throw new TypeError(`Catalogue result schema omits ${operation}`);

  const rootDefinitions = cloneJson(
    objectValue(canonical.$defs, "Catalogue result definitions"),
  );
  const receiptReference = {
    "urn:gis-ai-go:schema:evidence-receipt:v1": "#/$defs/evidence_receipt",
  } as const;
  const selectedSchema = cloneJson(selected);
  rewriteReferences(selectedSchema, "", receiptReference);

  const evidenceReferences = {
    "urn:gis-ai-go:schema:public-authority-context:v1":
      "#/$defs/public_authority_context",
    "urn:gis-ai-go:schema:public-policy-decision:v1":
      "#/$defs/public_policy_decision",
  } as const;
  embedSchemaResource(
    evidenceReceiptSchema,
    "evidence_receipt",
    "evidence",
    evidenceReferences,
    rootDefinitions,
  );
  embedSchemaResource(
    publicAuthorityContextSchema,
    "public_authority_context",
    "authority",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicPolicyDecisionSchema,
    "public_policy_decision",
    "policy",
    {},
    rootDefinitions,
  );

  return deepFreeze({
    $schema: canonical.$schema,
    $id: OPERATION_RESULT_SCHEMA_IDS[operation],
    title: `GIS AI GO ${operation} result`,
    description: canonical.description,
    $comment: canonical.$comment,
    ...selectedSchema,
    $defs: rootDefinitions,
  });
}

function evidenceOperationResultSchema(): CatalogueJsonSchema {
  const dispatcher = cloneJson(evidenceInspectOperationResultV3Schema);
  const rootDefinitions: Record<string, unknown> = {};
  rewriteReferences(dispatcher, "", {
    "urn:gis-ai-go:schema:evidence-inspect-result:v3":
      "#/$defs/evidence_inspect_result_v3",
  });
  embedSchemaResource(
    evidenceInspectResultV3Schema,
    "evidence_inspect_result_v3",
    "inspect_v3",
    {
      "urn:gis-ai-go:schema:public-evidence-record:v1":
        "#/$defs/public_evidence_record",
      "urn:gis-ai-go:schema:public-evidence-record:v2":
        "#/$defs/public_evidence_record_v2",
      "urn:gis-ai-go:schema:evidence-ledger-event:v1":
        "#/$defs/evidence_ledger_event",
      "urn:gis-ai-go:schema:evidence-receipt:v3":
        "#/$defs/evidence_receipt_v3",
    },
    rootDefinitions,
  );

  embedSchemaResource(
    publicEvidenceRecordSchema,
    "public_evidence_record",
    "record",
    {
      "urn:gis-ai-go:schema:evidence-receipt:v1": "#/$defs/evidence_receipt",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    publicEvidenceRecordV2Schema,
    "public_evidence_record_v2",
    "record_v2",
    {
      "urn:gis-ai-go:schema:evidence-receipt:v2": "#/$defs/evidence_receipt_v2",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceLedgerEventSchema,
    "evidence_ledger_event",
    "event",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceReceiptSchema,
    "evidence_receipt",
    "evidence",
    {
      "urn:gis-ai-go:schema:public-authority-context:v1":
        "#/$defs/public_authority_context",
      "urn:gis-ai-go:schema:public-policy-decision:v1":
        "#/$defs/public_policy_decision",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceReceiptV2Schema,
    "evidence_receipt_v2",
    "evidence_v2",
    {
      "urn:gis-ai-go:schema:public-authority-context:v2":
        "#/$defs/public_authority_context_v2",
      "urn:gis-ai-go:schema:public-policy-decision:v2":
        "#/$defs/public_policy_decision_v2",
      "urn:gis-ai-go:schema:public-read-resource:v1":
        "#/$defs/public_read_resource",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceReceiptV3Schema,
    "evidence_receipt_v3",
    "evidence_v3",
    {
      "urn:gis-ai-go:schema:public-authority-context:v3":
        "#/$defs/public_authority_context_v3",
      "urn:gis-ai-go:schema:public-policy-decision:v3":
        "#/$defs/public_policy_decision_v3",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    publicAuthorityContextSchema,
    "public_authority_context",
    "authority",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicPolicyDecisionSchema,
    "public_policy_decision",
    "policy",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicAuthorityContextV2Schema,
    "public_authority_context_v2",
    "authority_v2",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicPolicyDecisionV2Schema,
    "public_policy_decision_v2",
    "policy_v2",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicAuthorityContextV3Schema,
    "public_authority_context_v3",
    "authority_v3",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicPolicyDecisionV3Schema,
    "public_policy_decision_v3",
    "policy_v3",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicReadResourceSchema,
    "public_read_resource",
    "resource",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...dispatcher, $defs: rootDefinitions });
}

function evidenceOperationRequestJsonSchema(): CatalogueJsonSchema {
  const dispatcher = cloneJson(evidenceInspectOperationRequestSchema);
  const rootDefinitions: Record<string, unknown> = {};
  rewriteReferences(dispatcher, "", {
    "urn:gis-ai-go:schema:evidence-inspect-request:v1":
      "#/$defs/evidence_inspect_request_v1",
    "urn:gis-ai-go:schema:evidence-inspect-request:v2":
      "#/$defs/evidence_inspect_request_v2",
  });
  embedSchemaResource(
    evidenceInspectRequestSchema,
    "evidence_inspect_request_v1",
    "inspect_request_v1",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceInspectRequestV2Schema,
    "evidence_inspect_request_v2",
    "inspect_request_v2",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...dispatcher, $defs: rootDefinitions });
}

function dataQueryRequestJsonSchema(): CatalogueJsonSchema {
  const request = cloneJson(dataQueryRequestSchema);
  const rootDefinitions: Record<string, unknown> = {};
  rewriteReferences(request, "", {
    "urn:gis-ai-go:schema:data-query-parameters:v1":
      "#/$defs/data_query_parameters_v1",
  });
  embedSchemaResource(
    dataQueryParametersSchema,
    "data_query_parameters_v1",
    "data_query_parameters_v1",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...request, $defs: rootDefinitions });
}

function dataQueryOperationProblemJsonSchema(): CatalogueJsonSchema {
  const dispatcher = cloneJson(dataQueryOperationProblemSchema);
  const rootDefinitions: Record<string, unknown> = {};
  rewriteReferences(dispatcher, "", {
    "urn:gis-ai-go:schema:data-query-problem:v1": "#/$defs/data_query_problem_v1",
    "urn:gis-ai-go:schema:data-query-reconciliation-problem:v1":
      "#/$defs/data_query_reconciliation_problem_v1",
  });
  embedSchemaResource(
    dataQueryProblemSchema,
    "data_query_problem_v1",
    "data_query_problem_v1",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    dataQueryReconciliationProblemSchema,
    "data_query_reconciliation_problem_v1",
    "data_query_reconciliation_problem_v1",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...dispatcher, $defs: rootDefinitions });
}

function publicReadOperationResultSchema(
  schema: unknown,
  operation: PublicReadApiOperation,
): CatalogueJsonSchema {
  const result = cloneJson(schema);
  const rootDefinitions = result.$defs === undefined
    ? {}
    : cloneJson(objectValue(result.$defs, `${operation} result definitions`));
  delete result.$defs;
  rewriteReferences(result, "", {
    "urn:gis-ai-go:schema:evidence-receipt:v2": "#/$defs/evidence_receipt_v2",
    "urn:gis-ai-go:schema:selection-plan:v1": "#/$defs/selection_plan",
  });
  for (const definition of Object.values(rootDefinitions)) {
    rewriteReferences(definition, "", {
      "urn:gis-ai-go:schema:evidence-receipt:v2": "#/$defs/evidence_receipt_v2",
      "urn:gis-ai-go:schema:selection-plan:v1": "#/$defs/selection_plan",
    });
  }
  if (operation === "selection.resolve") {
    embedSchemaResource(
      selectionPlanSchema,
      "selection_plan",
      "selection_plan",
      {},
      rootDefinitions,
    );
  }
  embedSchemaResource(
    evidenceReceiptV2Schema,
    "evidence_receipt_v2",
    "evidence_v2",
    {
      "urn:gis-ai-go:schema:public-authority-context:v2":
        "#/$defs/public_authority_context_v2",
      "urn:gis-ai-go:schema:public-policy-decision:v2":
        "#/$defs/public_policy_decision_v2",
      "urn:gis-ai-go:schema:public-read-resource:v1":
        "#/$defs/public_read_resource",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    publicAuthorityContextV2Schema,
    "public_authority_context_v2",
    "authority_v2",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicPolicyDecisionV2Schema,
    "public_policy_decision_v2",
    "policy_v2",
    {},
    rootDefinitions,
  );
  embedSchemaResource(
    publicReadResourceSchema,
    "public_read_resource",
    "resource",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...result, $defs: rootDefinitions });
}

/*
 * These canonical per-version exports remain externally referenced schemas.
 * The operation export below is the separately identified v3 self-contained
 * dispatcher used by the inactive direct API and MCP advertisements. The
 * historical v1 operation dispatcher remains a frozen repository contract.
 */
export const evidenceInspectResultV1JsonSchema = deepFreeze(
  cloneJson(evidenceInspectResultSchema),
);
export const evidenceInspectResultV2JsonSchema = deepFreeze(
  cloneJson(evidenceInspectResultV2Schema),
);
export const evidenceInspectResultV3JsonSchema = deepFreeze(
  cloneJson(evidenceInspectResultV3Schema),
);

export const catalogueSearchRequestJsonSchema = deepFreeze(
  cloneJson(catalogueSearchRequestSchema),
);
export const catalogueDescribeRequestJsonSchema = deepFreeze(
  cloneJson(catalogueDescribeRequestSchema),
);
export const catalogueSearchResultJsonSchema = catalogueOperationResultSchema(
  "catalogue.search",
);
export const catalogueDescribeResultJsonSchema = catalogueOperationResultSchema(
  "catalogue.describe",
);
export const evidenceInspectRequestV1JsonSchema = deepFreeze(
  cloneJson(evidenceInspectRequestSchema),
);
export const evidenceInspectRequestJsonSchema = deepFreeze(
  evidenceOperationRequestJsonSchema(),
);
export const evidenceInspectResultJsonSchema = evidenceOperationResultSchema();
export const selectionResolveRequestJsonSchema = deepFreeze(
  cloneJson(selectionResolveRequestSchema),
);
export const selectionResolveResultJsonSchema = publicReadOperationResultSchema(
  selectionResolveResultSchema,
  "selection.resolve",
);
export const selectionResolveProblemJsonSchema = deepFreeze(
  cloneJson(selectionResolveProblemSchema),
);
export const dataQueryParametersJsonSchema = deepFreeze(
  cloneJson(dataQueryParametersSchema),
);
export const dataQueryRequestOperationJsonSchema = dataQueryRequestJsonSchema();
export const dataQueryResultJsonSchema = publicReadOperationResultSchema(
  dataQueryResultSchema,
  "data.query",
);
export const dataQueryProblemJsonSchema = deepFreeze(
  cloneJson(dataQueryProblemSchema),
);
export const dataQueryOperationProblemSchemaJson =
  dataQueryOperationProblemJsonSchema();
export const catalogueProblemJsonSchema = deepFreeze(cloneJson(catalogueProblemSchema));

/** Exact canonical schemas shared by direct API and MCP advertisements. */
export const CATALOGUE_OPERATION_JSON_SCHEMAS = deepFreeze({
  "catalogue.describe": {
    inputSchema: catalogueDescribeRequestJsonSchema,
    outputSchema: catalogueDescribeResultJsonSchema,
  },
  "catalogue.search": {
    inputSchema: catalogueSearchRequestJsonSchema,
    outputSchema: catalogueSearchResultJsonSchema,
  },
} as const);

export const EVIDENCE_OPERATION_JSON_SCHEMAS = deepFreeze({
  "evidence.inspect": {
    inputSchema: evidenceInspectRequestJsonSchema,
    outputSchema: evidenceInspectResultJsonSchema,
  },
} as const);

export const PUBLIC_READ_OPERATION_JSON_SCHEMAS = deepFreeze({
  "selection.resolve": {
    inputSchema: selectionResolveRequestJsonSchema,
    outputSchema: selectionResolveResultJsonSchema,
    problemSchema: selectionResolveProblemJsonSchema,
  },
  "data.query": {
    inputSchema: dataQueryRequestOperationJsonSchema,
    outputSchema: dataQueryResultJsonSchema,
    problemSchema: dataQueryOperationProblemSchemaJson,
  },
} as const);

export const GATEWAY_OPERATION_JSON_SCHEMAS = deepFreeze({
  ...CATALOGUE_OPERATION_JSON_SCHEMAS,
  ...EVIDENCE_OPERATION_JSON_SCHEMAS,
  ...PUBLIC_READ_OPERATION_JSON_SCHEMAS,
} as const);

function normaliseOperations(
  operations: readonly GatewayApiOperation[],
): readonly GatewayApiOperation[] {
  if (!Array.isArray(operations)) {
    throw new TypeError("enabled API operations must be an array");
  }
  const selected = new Set<GatewayApiOperation>();
  for (const operation of operations) {
    if (!(GATEWAY_API_OPERATIONS as readonly unknown[]).includes(operation)) {
      throw new TypeError("enabled API operations contain an unknown operation");
    }
    if (selected.has(operation)) {
      throw new TypeError("enabled API operations must be unique");
    }
    selected.add(operation);
  }
  const normalised = GATEWAY_API_OPERATIONS.filter((operation) => selected.has(operation));
  if (
    normalised.includes("data.query") &&
    !normalised.includes("evidence.inspect")
  ) {
    throw new TypeError(
      "data.query OpenAPI mounting requires the exact linked evidence.inspect operation",
    );
  }
  return normalised;
}

/** Build the exact local-candidate contract for the explicitly mounted API set. */
export function createCatalogueOpenApiDocument(
  enabledApiOperations: readonly GatewayApiOperation[],
): OpenApiDocument {
  const selected = normaliseOperations(enabledApiOperations);
  const document = cloneTemplate();
  const paths = document.paths;
  if (paths === null || typeof paths !== "object" || Array.isArray(paths)) {
    throw new TypeError("OpenAPI template paths must be an object");
  }
  const mutablePaths = paths as Record<string, unknown>;
  for (const operation of GATEWAY_API_OPERATIONS) {
    if (!selected.includes(operation)) delete mutablePaths[OPERATION_PATHS[operation]];
  }
  const components = objectValue(document.components, "OpenAPI components");
  const schemas = objectValue(components.schemas, "OpenAPI component schemas");
  schemas.CatalogueSearchRequest = cloneJson(catalogueSearchRequestJsonSchema);
  schemas.CatalogueDescribeRequest = cloneJson(catalogueDescribeRequestJsonSchema);
  schemas.CatalogueSearchResult = cloneJson(catalogueSearchResultJsonSchema);
  schemas.CatalogueDescribeResult = cloneJson(catalogueDescribeResultJsonSchema);
  schemas.EvidenceInspectRequest = cloneJson(evidenceInspectRequestJsonSchema);
  schemas.EvidenceInspectResult = cloneJson(evidenceInspectResultJsonSchema);
  schemas.SelectionResolveRequest = cloneJson(selectionResolveRequestJsonSchema);
  schemas.SelectionResolveResult = cloneJson(selectionResolveResultJsonSchema);
  schemas.SelectionResolveProblem = cloneJson(selectionResolveProblemJsonSchema);
  schemas.DataQueryParameters = cloneJson(dataQueryParametersJsonSchema);
  schemas.DataQueryRequest = cloneJson(dataQueryRequestOperationJsonSchema);
  schemas.DataQueryResult = cloneJson(dataQueryResultJsonSchema);
  schemas.DataQueryProblem = cloneJson(dataQueryProblemJsonSchema);
  schemas.DataQueryOperationProblem = cloneJson(dataQueryOperationProblemSchemaJson);
  schemas.CatalogueProblem = cloneJson(catalogueProblemJsonSchema);
  document["x-gis-ai-go-mounted-candidate-catalogue-operations"] =
    CATALOGUE_API_OPERATIONS.filter((operation) => selected.includes(operation));
  document["x-gis-ai-go-mounted-candidate-operations"] = [...selected];
  return deepFreeze(document as OpenApiDocument);
}

/** Describe one branded candidate assembly without claiming production registration. */
export function createGovernedCandidateOpenApiDocument(
  enabledApiOperations: readonly GatewayApiOperation[],
): OpenApiDocument {
  const selected = normaliseOperations(enabledApiOperations);
  const candidateOperations = Object.freeze([...enabledApiOperations]);
  const document = cloneJson(createCatalogueOpenApiDocument(selected));
  document["x-gis-ai-go-lifecycle"] = "candidate-unregistered";
  document["x-gis-ai-go-production-registration"] = false;
  document["x-gis-ai-go-candidate-operations"] = [...candidateOperations];

  const paths = objectValue(document.paths, "OpenAPI paths");
  const readinessPath = objectValue(paths["/readyz"], "OpenAPI readiness path");
  const readinessGet = objectValue(readinessPath.get, "OpenAPI readiness operation");
  const readinessResponses = objectValue(
    readinessGet.responses,
    "OpenAPI readiness responses",
  );
  readinessResponses["200"] = cloneJson(readinessResponses["503"]);
  objectValue(readinessResponses["200"], "OpenAPI ready response").description =
    "The exact candidate assembly and its evidence and provider dependencies are verified";

  const components = objectValue(document.components, "OpenAPI components");
  const schemas = objectValue(components.schemas, "OpenAPI component schemas");
  const health = objectValue(schemas.Health, "OpenAPI health schema");
  health.required = [
    "status",
    "product",
    "lifecycle",
    "production_registration",
    "catalogue",
  ];
  const healthProperties = objectValue(
    health.properties,
    "OpenAPI health properties",
  );
  healthProperties.lifecycle = { const: "candidate-unregistered" };
  healthProperties.production_registration = { const: false };
  const activeOperationItems = candidateOperations.length === 0
    ? false
    : { enum: [...candidateOperations] };

  schemas.Readiness = {
    type: "object",
    additionalProperties: false,
    required: [
      "status",
      "reason",
      "production_registration",
      "active_tools",
      "active_api_operations",
    ],
    properties: {
      status: { enum: ["ready", "blocked"] },
      reason: {
        enum: [
          "candidate-assembly-verified",
          "evidence-integrity-failed",
          "reconciliation-capacity-exhausted",
          "relevant-capability-suspended",
        ],
      },
      production_registration: { const: false },
      active_tools: {
        type: "array",
        uniqueItems: true,
        maxItems: selected.length,
        items: activeOperationItems,
      },
      active_api_operations: {
        type: "array",
        uniqueItems: true,
        maxItems: selected.length,
        items: activeOperationItems,
      },
    },
  };
  return deepFreeze(document as OpenApiDocument);
}

/** The production default remains blocked and mounts no catalogue API operation. */
export const catalogueOpenApiDocument = createCatalogueOpenApiDocument([]);
