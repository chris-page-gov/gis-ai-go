/** Explicit initial evidence provisioning. Preview is offline; --apply is a cloud mutation approval gate. */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { canonicalJson } from "@gis-ai-go/evidence/web216-pure";
import { createGcpEvidenceSeed, provisionGcpCpihPrincipal } from "./gcp-application.js";
import { gcpPrincipalScope } from "./gcp-identity.js";
import { createGcpFirestoreRestStore } from "./gcp-firestore.js";
import type { GcpRuntimeConfig } from "./gcp-server.js";
import { readGcpRuntimeConfig } from "./gcp-main.js";

export function gcpProvisionPreview(config: GcpRuntimeConfig, projection: unknown, subject: string) {
  if (config.schema !== "gis-ai-go.gcp-runtime.v1" || !subject || subject.length > 512) throw Error("Invalid provisioning configuration");
  const issuer = config.identity.mode === "single-owner-transport-pilot" ? "https://accounts.google.com" : config.identity.issuer;
  if (config.identity.mode === "single-owner-transport-pilot") {
    if (config.profile !== "personal" || subject !== config.transportSubject) throw Error("Personal provisioning must use the approved exact transport subject");
  } else if (!Object.hasOwn(config.identity.subjectRoles ?? {}, subject)) {
    throw Error("Human evidence enrolment requires an explicitly approved subject binding");
  }
  const scope = gcpPrincipalScope(issuer, subject, config.profile);
  const { initialSnapshot } = createGcpEvidenceSeed({ projection, evidence: config.evidence, principalScope: scope });
  const fields = { schema: "gis-ai-go.gcp-firestore-cpih.v1", principal_scope: scope,
    snapshot_json: canonicalJson(initialSnapshot), store_id: initialSnapshot.descriptor.store_id,
    checkpoint_id: initialSnapshot.head.checkpoint_id, sequence: "0" };
  return { schema: "gis-ai-go.gcp-provision-preview.v1", project_id: config.firestore.projectId,
    database_id: config.firestore.databaseId, collection: config.firestore.collection, principal_scope: scope,
    store_id: initialSnapshot.descriptor.store_id, fields,
    precondition: "absent-document-only-existing-history-must-verify", operation: "provision-empty-principal-scoped-evidence",
    data_inventory: ["approved capture identity and software descriptor", "empty receipt/event arrays", "one content-addressed initial head"],
    uploaded_credentials: false, contains_protected_data: false, cloud_mutation: false };
}
export async function runGcpProvision(argv: readonly string[]) {
  const apply = argv.includes("--apply");
  const args = argv.filter((arg) => arg !== "--apply");
  let config: GcpRuntimeConfig; let projection: unknown; let subject: string;
  if (args.length === 0 || (args.length === 2 && args[0] === "--subject")) {
    const bound = readGcpRuntimeConfig(); if (bound === null || (args.length === 0 && bound.identity.mode !== "single-owner-transport-pilot")) throw Error("An exact approved provisioning subject is required");
    config = bound; projection = JSON.parse(readFileSync("/app/bundles/cpih-projection.json", "utf8")); subject = args[1] ?? config.transportSubject;
  } else {
    if (args.length !== 6 || args[0] !== "--config" || args[2] !== "--projection" || args[4] !== "--subject") throw Error("Usage: gcp-provision --config FILE --projection FILE --subject EXACT_SUBJECT [--apply]");
    config = JSON.parse(readFileSync(args[1]!, "utf8")) as GcpRuntimeConfig;
    projection = JSON.parse(readFileSync(args[3]!, "utf8")); subject = args[5]!;
  }
  const preview = gcpProvisionPreview(config, projection, subject);
  if (!apply) { process.stdout.write(canonicalJson(preview) + "\n"); return; }
  // Operator supplies a short-lived gcloud access token on stdin, never arguments/env/files/logs.
  // The lifecycle command must check its recorded plan approval before invoking this mutation.
  const token = readFileSync(0, "utf8").trim();
  if (!/^[A-Za-z0-9._~-]{20,8192}$/u.test(token)) throw Error("A short-lived operator access token is required on stdin");
  const backend = createGcpFirestoreRestStore(config.firestore, { accessToken: async () => token });
  const snapshot = await provisionGcpCpihPrincipal({ backend, principalScope: preview.principal_scope,
    projection, evidence: config.evidence });
  process.stdout.write(canonicalJson({ schema: "gis-ai-go.gcp-provision-result.v1", status: "initialised-or-existing-history-verified",
    principal_scope: preview.principal_scope, store_id: snapshot.descriptor.store_id, checkpoint_id: snapshot.head.checkpoint_id,
    record_count: snapshot.records.length, cloud_mutation: true, deployment_acceptance: "not-established-by-provisioning" }) + "\n");
}
const entry = process.argv[1];
if (entry && pathToFileURL(resolve(entry)).href === import.meta.url) await runGcpProvision(process.argv.slice(2)).catch(() => {
  process.stderr.write('{"schema":"gis-ai-go.gcp-provision-result.v1","status":"failed"}\n'); process.exitCode = 1;
});
