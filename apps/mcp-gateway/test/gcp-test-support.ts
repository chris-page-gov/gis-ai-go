/** Signed synthetic identities and atomic in-memory backend, only imported by isolated tests. */
import { generateKeyPairSync, sign } from "node:crypto";
import { readFileSync } from "node:fs";
import { createGcpIdentityAdapter, createGcpJwtVerifier, type GcpRole } from "../src/gcp-identity.js";
import type { GcpAtomicDocument, GcpAtomicDocumentStore } from "../src/gcp-firestore.js";
import type { GcpRuntimeConfig } from "../src/gcp-server.js";
import { createGcpKnowledgeService } from "../src/gcp-knowledge.js";
const pair = generateKeyPairSync("rsa", { modulusLength: 2_048 });
export const JWK = { ...pair.publicKey.export({ format: "jwk" }), kid: "synthetic-1", alg: "RS256", use: "sig" };
export const CLOCK = new Date("2026-10-05T12:00:00.000Z").getTime();
export const TRANSPORT_SUBJECT = "123456789012345678901";
export const ORIGIN = "https://synthetic-private.run.app";
export const HUMAN_ISSUER = "https://synthetic.okta.example/oauth2/approved";
export const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
export const EVIDENCE = { storeNonce: "1".repeat(32), createdAt: new Date(CLOCK).toISOString(), sourceRevision: "a".repeat(40) };
export function signed(claims: Record<string, unknown>, header: Record<string, unknown> = { alg: "RS256", kid: "synthetic-1", typ: "JWT" }) {
  const a = Buffer.from(JSON.stringify(header)).toString("base64url"); const b = Buffer.from(JSON.stringify(claims)).toString("base64url");
  return `${a}.${b}.${sign("sha256", Buffer.from(`${a}.${b}`), pair.privateKey).toString("base64url")}`;
}
export function transportToken(clock = CLOCK) {
  return signed({ iss: "https://accounts.google.com", sub: TRANSPORT_SUBJECT, aud: ORIGIN, iat: Math.floor(clock / 1_000), exp: Math.floor(clock / 1_000) + 3_600 });
}
export const jwksFetch: typeof fetch = async () => new Response(JSON.stringify({ keys: [JWK] }), { headers: { "content-type": "application/json" } });
export function runtimeConfig(roles: readonly GcpRole[] = ["analyst"], mode: "personal" | "bduk" = "bduk"): GcpRuntimeConfig {
  return { schema: "gis-ai-go.gcp-runtime.v1", profile: mode, publicOrigin: ORIGIN, transportSubject: TRANSPORT_SUBJECT,
    allowedOrigins: mode === "personal" ? ["http://127.0.0.1:8789"] : [ORIGIN],
    firestore: { projectId: "synthetic-project", databaseId: "(default)", collection: "gis_evidence" }, evidence: EVIDENCE,
    identity: mode === "personal" ? { mode: "single-owner-transport-pilot" } : {
      mode: "oidc", issuer: HUMAN_ISSUER, audience: `${ORIGIN}/mcp`, jwksUri: `${HUMAN_ISSUER}/v1/keys`,
      subjectRoles: { "synthetic-human": roles }, groupRoles: { "approved-viewers": ["viewer"], "approved-analysts": ["analyst"] },
    },
  };
}
export function credentials(config = runtimeConfig(), subject = "synthetic-human", clock = CLOCK) {
  return { "x-gis-invocation-proof": transportToken(clock), ...(config.identity.mode === "oidc" ? { authorization: `Bearer ${signed({
    iss: config.identity.issuer, sub: subject, aud: config.identity.audience, iat: Math.floor(clock / 1_000), exp: Math.floor(clock / 1_000) + 3_600,
  })}` } : {}) };
}
export async function principal(roles: readonly GcpRole[] = ["analyst"], subject = "synthetic-human", clock = CLOCK) {
  const config = runtimeConfig(roles);
  if (config.identity.mode === "oidc") (config.identity as { subjectRoles: Record<string, readonly GcpRole[]> }).subjectRoles = { [subject]: roles };
  const adapter = createGcpIdentityAdapter(config, createGcpJwtVerifier({ fetch: jwksFetch, now: () => clock }));
  return (await adapter.authenticate(new Request(ORIGIN, { headers: credentials(config, subject, clock) }))).principal;
}
export class FakeAtomicStore implements GcpAtomicDocumentStore {
  readonly rows = new Map<string, GcpAtomicDocument>();
  writes = 0; counter = 0;
  beforeSet?: () => Promise<void>;
  afterSet?: () => Promise<void>;
  read = async (id: string) => structuredClone(this.rows.get(id) ?? null);
  compareAndSet = async (id: string, expectedVersion: string | null, fields: Readonly<Record<string, string>>) => {
    await this.beforeSet?.();
    const previous = this.rows.get(id);
    if ((previous?.version ?? null) !== expectedVersion) return false;
    this.rows.set(id, { version: `synthetic-version-${++this.counter}`, fields: structuredClone(fields) }); this.writes += 1;
    await this.afterSet?.(); return true;
  };
}
export function knowledge() {
  const row = (id: string) => ({ id, title: "Captured CPIH index", description: "Maintained L522 series metadata", type: "dataset",
    tags: ["inflation"], temporal: { status: "source-stated", start: "2026-01", end: "2026-07" },
    rights: { executionAdmitted: false }, sources: [{ resource: "https://www.ons.gov.uk/synthetic-source", retrievedAt: "2026-09-01T00:00:00Z" }],
    limitations: ["Synthetic metadata fixture, not live provider data"] });
  return createGcpKnowledgeService([{ id: "okf", revision: "a".repeat(40), inputDigest: "b".repeat(64), records: [row("legacy-1")] },
    { id: "okf-plus", revision: "a".repeat(40), inputDigest: "c".repeat(64), records: [row("expanded-1"), row("expanded-2")] }], "d".repeat(64));
}
