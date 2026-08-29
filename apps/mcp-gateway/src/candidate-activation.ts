import {
  type PublicEvidenceLedger,
  type PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  createApprovedOnsDataQueryCache,
  createOnsDataApiAdapter,
  type ApprovedOnsDataQueryCacheRecord,
} from "@gis-ai-go/provider-adapter-sdk";
import { V02_TARGET_ACTIVE_TOOL_NAMES } from "@gis-ai-go/tool-registry";

import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  GOVERNED_CANDIDATE_MCP_RESOURCES,
  assessGovernedCandidateReadiness,
  createGovernedCandidateAssembly,
  governedCandidateAssemblyBindings,
  type GovernedCandidateAssembly,
} from "./governed-assembly.js";

export const CANDIDATE_ACTIVATION_LIFECYCLE = "candidate-unregistered" as const;
export const CANDIDATE_ACTIVATION_PROVIDER_REASON =
  "The fixed local unregistered v0.2.0 candidate permits the reviewed public ONS operation." as const;
export const CANDIDATE_ACTIVATION_OPERATIONS = Object.freeze([
  ...V02_TARGET_ACTIVE_TOOL_NAMES,
]);
export const CANDIDATE_ACTIVATION_RESOURCES = GOVERNED_CANDIDATE_MCP_RESOURCES;

/**
 * Build the only shipped exact-five candidate activation.
 *
 * The caller can supply only the already verified catalogue snapshot, exact linked
 * evidence stores and the repository-approved T04 record. The provider lifecycle,
 * adapter transport, cache parser and operation projection are fixed here. There is
 * no path, environment, command-line, clock, suspension or arbitrary option seam.
 * Production registration deliberately remains false.
 */
export function createCandidateActivation(
  snapshot: CatalogueSnapshot,
  evidenceLedger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
  approvedCacheRecord: ApprovedOnsDataQueryCacheRecord,
): GovernedCandidateAssembly {
  if (arguments.length !== 4) {
    throw new TypeError("Candidate activation requires the exact fixed input tuple");
  }
  const adapter = createOnsDataApiAdapter({
    lifecycle: Object.freeze({
      discovery: "active",
      invocation: "active",
      reason: CANDIDATE_ACTIVATION_PROVIDER_REASON,
    }),
  });
  const approvedCache = createApprovedOnsDataQueryCache(approvedCacheRecord);
  const assembly = createGovernedCandidateAssembly({
    snapshot,
    evidenceLedger,
    reconciliationIndex,
    adapter,
    approvedCache,
  });
  const readiness = assessGovernedCandidateReadiness(assembly);

  if (
    assembly.state !== CANDIDATE_ACTIVATION_LIFECYCLE ||
    assembly.productionRegistration !== false ||
    assembly.suspensions.length !== 0 ||
    assembly.operations.length !== CANDIDATE_ACTIVATION_OPERATIONS.length ||
    assembly.operations.some(
      (operation, index) => operation !== CANDIDATE_ACTIVATION_OPERATIONS[index],
    ) ||
    assembly.apiOperations !== assembly.operations ||
    assembly.mcpOperations !== assembly.operations ||
    assembly.mcpResources.length !== CANDIDATE_ACTIVATION_RESOURCES.length ||
    assembly.mcpResources.some(
      (resource, index) => resource !== CANDIDATE_ACTIVATION_RESOURCES[index],
    ) ||
    !(
      (readiness.status === "ready" &&
        readiness.reason === "candidate-assembly-verified") ||
      (readiness.status === "blocked" &&
        readiness.reason === "reconciliation-capacity-exhausted")
    ) ||
    readiness.productionRegistration !== false ||
    readiness.activeTools !== assembly.operations ||
    readiness.activeApiOperations !== assembly.operations
  ) {
    throw new Error("The fixed candidate activation failed closed");
  }

  // Repeat the private brand check immediately before returning the assembly.
  governedCandidateAssemblyBindings(assembly);
  return assembly;
}
