import { readFileSync } from "node:fs";

import openApiTemplate from "../openapi/catalogue-api.openapi.json" with { type: "json" };

export const CATALOGUE_API_OPERATIONS = Object.freeze([
  "catalogue.describe",
  "catalogue.search",
] as const);
export const EVIDENCE_API_OPERATIONS = Object.freeze([
  "evidence.inspect",
] as const);
export const GATEWAY_API_OPERATIONS = Object.freeze([
  ...CATALOGUE_API_OPERATIONS,
  ...EVIDENCE_API_OPERATIONS,
] as const);

export type CatalogueApiOperation = (typeof CATALOGUE_API_OPERATIONS)[number];
export type EvidenceApiOperation = (typeof EVIDENCE_API_OPERATIONS)[number];
export type GatewayApiOperation = (typeof GATEWAY_API_OPERATIONS)[number];

export interface OpenApiDocument extends Readonly<Record<string, unknown>> {
  readonly paths: Readonly<Record<string, unknown>>;
}

export type CatalogueJsonSchema = Readonly<Record<string, unknown>>;

const OPERATION_PATHS: Readonly<Record<GatewayApiOperation, string>> = Object.freeze({
  "catalogue.describe": "/catalogue/describe",
  "catalogue.search": "/catalogue/search",
  "evidence.inspect": "/evidence/inspect",
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
const evidenceInspectOperationResultSchema = sharedSchema(
  "evidence-inspect-operation-result.schema.json",
);
const evidenceInspectResultSchema = sharedSchema(
  "evidence-inspect-result.schema.json",
);
const evidenceInspectResultV2Schema = sharedSchema(
  "evidence-inspect-result-v2.schema.json",
);
const evidenceLedgerEventSchema = sharedSchema(
  "evidence-ledger-event.schema.json",
);
const evidenceReceiptSchema = sharedSchema("evidence-receipt.schema.json");
const evidenceReceiptV2Schema = sharedSchema("evidence-receipt-v2.schema.json");
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
const publicPolicyDecisionSchema = sharedSchema(
  "public-policy-decision.schema.json",
);
const publicPolicyDecisionV2Schema = sharedSchema(
  "public-policy-decision-v2.schema.json",
);
const publicReadResourceSchema = sharedSchema("public-read-resource.schema.json");

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
  const dispatcher = cloneJson(evidenceInspectOperationResultSchema);
  const rootDefinitions: Record<string, unknown> = {};
  rewriteReferences(dispatcher, "", {
    "urn:gis-ai-go:schema:evidence-inspect-result:v1":
      "#/$defs/evidence_inspect_result_v1",
    "urn:gis-ai-go:schema:evidence-inspect-result:v2":
      "#/$defs/evidence_inspect_result_v2",
  });
  embedSchemaResource(
    evidenceInspectResultSchema,
    "evidence_inspect_result_v1",
    "inspect_v1",
    {
      "urn:gis-ai-go:schema:public-evidence-record:v1":
        "#/$defs/public_evidence_record",
      "urn:gis-ai-go:schema:evidence-ledger-event:v1":
        "#/$defs/evidence_ledger_event",
    },
    rootDefinitions,
  );
  embedSchemaResource(
    evidenceInspectResultV2Schema,
    "evidence_inspect_result_v2",
    "inspect_v2",
    {
      "urn:gis-ai-go:schema:public-evidence-record:v2":
        "#/$defs/public_evidence_record_v2",
      "urn:gis-ai-go:schema:evidence-ledger-event:v1":
        "#/$defs/evidence_ledger_event",
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
    publicReadResourceSchema,
    "public_read_resource",
    "resource",
    {},
    rootDefinitions,
  );
  return deepFreeze({ ...dispatcher, $defs: rootDefinitions });
}

/*
 * These canonical per-version exports remain externally referenced schemas.
 * The operation export below is the separately identified, self-contained
 * dispatcher used by the inactive direct API and MCP advertisements.
 */
export const evidenceInspectResultV1JsonSchema = deepFreeze(
  cloneJson(evidenceInspectResultSchema),
);
export const evidenceInspectResultV2JsonSchema = deepFreeze(
  cloneJson(evidenceInspectResultV2Schema),
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
export const evidenceInspectRequestJsonSchema = deepFreeze(
  cloneJson(evidenceInspectRequestSchema),
);
export const evidenceInspectResultJsonSchema = evidenceOperationResultSchema();
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

export const GATEWAY_OPERATION_JSON_SCHEMAS = deepFreeze({
  ...CATALOGUE_OPERATION_JSON_SCHEMAS,
  ...EVIDENCE_OPERATION_JSON_SCHEMAS,
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
  return GATEWAY_API_OPERATIONS.filter((operation) => selected.has(operation));
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
  schemas.CatalogueProblem = cloneJson(catalogueProblemJsonSchema);
  document["x-gis-ai-go-mounted-candidate-catalogue-operations"] =
    CATALOGUE_API_OPERATIONS.filter((operation) => selected.includes(operation));
  document["x-gis-ai-go-mounted-candidate-operations"] = [...selected];
  return deepFreeze(document as OpenApiDocument);
}

/** The production default remains blocked and mounts no catalogue API operation. */
export const catalogueOpenApiDocument = createCatalogueOpenApiDocument([]);
