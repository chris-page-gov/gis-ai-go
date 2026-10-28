/** Principal-scoped GCP assembly over maintained CPIH selection/result/evidence contracts. */
import { createHash } from "node:crypto";
import {
  createWeb216TransactionalSnapshot, lookupWeb216TransactionalRecord, type EvidenceSoftwareIdentity,
} from "@gis-ai-go/evidence/web216-pure";
import { createGcpFirestoreCpihStore, type GcpAtomicDocumentStore } from "./gcp-firestore.js";
import {
  createWeb216HostedCpihApplication, Web216HostedCpihApplicationError, type Web216HostedCpihApplication,
  type Web216HostedCpihCallContext, type Web216HostedCpihSignalContext,
} from "./web216-hosted-cpih-application.js";
import { normaliseWeb216CpihQueryProposal } from "./web216-cpih-selection.js";
import { gcpAuthorise, type GcpVerifiedPrincipal } from "./gcp-identity.js";

export interface GcpEvidenceConfig {
  /** Immutable provisioning values, retained across revisions/rollback. */
  readonly storeNonce: string;
  readonly createdAt: string;
  readonly sourceRevision: string;
}
export function createGcpEvidenceSeed(options: { readonly projection: unknown; readonly evidence: GcpEvidenceConfig; readonly principalScope: string }) {
  const software: EvidenceSoftwareIdentity = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: options.evidence.sourceRevision };
  if (!/^(?!0{32}$)[0-9a-f]{32}$/u.test(options.evidence.storeNonce) || !/^[0-9a-f]{64}$/u.test(options.principalScope)) throw Error("Invalid evidence provisioning seed");
  const storeNonce = createHash("sha256").update(JSON.stringify(["gis-ai-go.gcp-scoped-store.v1", options.evidence.storeNonce, options.principalScope])).digest("hex").slice(0, 32);
  const initialSnapshot = createWeb216TransactionalSnapshot({ projection: options.projection, software,
    createdAt: options.evidence.createdAt, storeNonce, maximumRecords: 128 });
  const material = { projection: options.projection, expectedSoftware: software, expectedStoreId: initialSnapshot.descriptor.store_id };
  return { initialSnapshot, material, software };
}
/** Explicit deployment/platform provisioning only; never called by an HTTP request. */
export async function provisionGcpCpihPrincipal(options: {
  readonly backend: GcpAtomicDocumentStore; readonly principalScope: string;
  readonly projection: unknown; readonly evidence: GcpEvidenceConfig;
}) {
  const seed = createGcpEvidenceSeed(options);
  const store = createGcpFirestoreCpihStore({ backend: options.backend, principalScope: options.principalScope, ...seed });
  return store.initialiseIfAbsent();
}
export function createGcpCpihApplication(options: {
  readonly backend: GcpAtomicDocumentStore; readonly principal: GcpVerifiedPrincipal;
  readonly projection: unknown; readonly evidence: GcpEvidenceConfig; readonly now?: () => Date;
}): Web216HostedCpihApplication {
  const now = options.now ?? (() => new Date());
  const principal = options.principal;
  const resource = { classification: "public-metadata", environment: principal.environment, principalScope: principal.scope };
  const { software, initialSnapshot, material } = createGcpEvidenceSeed({ projection: options.projection, evidence: options.evidence, principalScope: principal.scope });
  const store = createGcpFirestoreCpihStore({ backend: options.backend, principalScope: principal.scope, initialSnapshot, material });
  const maintained = createWeb216HostedCpihApplication({ store, projection: options.projection, software,
    expectedStoreId: initialSnapshot.descriptor.store_id, now });
  function require(capability: "cpih.select" | "cpih.query" | "evidence.inspect") {
    if (!gcpAuthorise(principal, capability, resource, now().getTime())) throw new Web216HostedCpihApplicationError("unavailable");
  }
  function retained(value: { readonly retain_until: string }) {
    if (Date.parse(value.retain_until) <= now().getTime()) throw new Web216HostedCpihApplicationError("not-found");
  }
  // This wrapper is deliberately not passed into the old branded MCP constructor.
  // The GCP face calls these maintained methods through this policy/retention seam.
  return Object.freeze({
    resolve: async (input: unknown, context?: Web216HostedCpihSignalContext) => {
      require("cpih.select"); return maintained.resolve(input, context);
    },
    readiness: (context?: Web216HostedCpihSignalContext) => maintained.readiness(context),
    query: async (input: unknown, context: Web216HostedCpihCallContext) => {
      require("cpih.query"); const proposal = normaliseWeb216CpihQueryProposal(input);
      if (context.signal?.aborted) throw new Web216HostedCpihApplicationError("cancelled");
      // Missing/deleted state is a blocked prerequisite. HTTP requests never create or replace a history.
      const snapshot = await store.readSnapshot();
      const existing = lookupWeb216TransactionalRecord(snapshot, proposal.idempotency_key, material);
      if (existing.status === "found-model-record") retained(existing.record);
      const result = await maintained.query(proposal, context); retained(result.evidence.record); return result;
    },
    inspect: async (input: unknown, context?: Web216HostedCpihSignalContext) => {
      require("evidence.inspect");
      const result = await maintained.inspect(input, context); retained(result.evidence.record); return result;
    },
  });
}
