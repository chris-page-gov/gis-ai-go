/** Private Cloud Run identity seam. No unsigned identity, email suffix or role header is authority. */
import { createHash, createPublicKey, verify, type JsonWebKey } from "node:crypto";
import { parseBoundedJsonBytes } from "./bounded-json.js";
import type { GcpBrowserOidcConfig } from "./gcp-oidc-browser.js";

export type GcpRole = "viewer" | "analyst" | "evidence-auditor" | "platform-operator" | "owner";
export interface GcpVerifiedPrincipal {
  readonly kind: "human-oidc" | "single-owner-transport-pilot";
  readonly issuer: string;
  readonly subject: string;
  /** An irreversible namespace for principal-scoped evidence; never an email. */
  readonly scope: string;
  readonly roles: readonly GcpRole[];
  readonly environment: "personal" | "bduk";
  readonly classification: "public-metadata";
  readonly expiresAt: number;
}
export interface GcpOidcConfig {
  readonly issuer: string;
  readonly audience: string;
  readonly jwksUri: string;
  readonly groupClaim?: string;
  readonly groupRoles?: Readonly<Record<string, readonly GcpRole[]>>;
  readonly subjectRoles?: Readonly<Record<string, readonly GcpRole[]>>;
  readonly browser?: GcpBrowserOidcConfig | null;
}
export class GcpIdentityError extends Error {
  constructor() { super("The signed identity could not be verified"); this.name = "GcpIdentityError"; }
}
const PRINCIPALS = new WeakSet<object>();
export function isGcpVerifiedPrincipal(value: unknown): value is GcpVerifiedPrincipal {
  return typeof value === "object" && value !== null && PRINCIPALS.has(value);
}
function reject(): never { throw new GcpIdentityError(); }
function object(value: unknown): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) reject();
  return value as Record<string, unknown>;
}
function jsonSegment(value: string): Record<string, unknown> {
  if (!/^[A-Za-z0-9_-]+$/u.test(value)) reject();
  const bytes = Buffer.from(value, "base64url");
  if (bytes.toString("base64url") !== value) reject();
  try { return object(parseBoundedJsonBytes(bytes, 16_384)); } catch { return reject(); }
}
export function gcpPrincipalScope(issuer: string, subject: string, environment: string): string {
  return createHash("sha256").update(JSON.stringify(["gis-ai-go.gcp-principal.v1", environment, issuer, subject])).digest("hex");
}
const ROLES = new Set<GcpRole>(["viewer", "analyst", "evidence-auditor", "platform-operator", "owner"]);
export function validateGcpOidcConfig(config: GcpOidcConfig): void {
  const issuer = new URL(config.issuer); const jwks = new URL(config.jwksUri);
  if (issuer.protocol !== "https:" || jwks.protocol !== "https:" || issuer.username || issuer.password ||
      issuer.search || issuer.hash || jwks.username || jwks.password || jwks.hash ||
      !config.audience || config.audience.length > 2_048 || !/^[a-zA-Z0-9_]+$/u.test(config.groupClaim ?? "groups")) reject();
  // Config is operator-authored. JWKS redirects, token-selected jku/x5u and issuer suffix matching are never accepted.
  for (const mapping of [config.groupRoles, config.subjectRoles]) for (const values of Object.values(mapping ?? {})) {
    if (!Array.isArray(values) || values.some((role) => !ROLES.has(role))) reject();
  }
}
export interface GcpJwtVerifier {
  verify(token: string, config: GcpOidcConfig): Promise<Readonly<Record<string, unknown>>>;
}
/** Native Node verification against pinned configuration. Fetch and clock are trusted constructor seams only. */
export function createGcpJwtVerifier(options: { readonly fetch?: typeof fetch; readonly now?: () => number } = {}): GcpJwtVerifier {
  const fetcher = options.fetch ?? fetch; const now = options.now ?? Date.now;
  const cache = new Map<string, { until: number; keys: readonly Record<string, unknown>[] }>();
  async function keys(uri: string): Promise<readonly Record<string, unknown>[]> {
    const previous = cache.get(uri);
    if (previous && now() < previous.until) return previous.keys;
    const response = await fetcher(uri, { redirect: "error", signal: AbortSignal.timeout(5_000), headers: { accept: "application/json" } });
    if (!response.ok || !response.headers.get("content-type")?.toLowerCase().startsWith("application/json")) reject();
    if (Number(response.headers.get("content-length") ?? 0) > 65_536) reject();
    const reader = response.body?.getReader(); if (!reader) reject();
    let size = 0; const chunks: Uint8Array[] = [];
    for (;;) { const part = await reader.read(); if (part.done) break; size += part.value.byteLength;
      if (size > 65_536) { void reader.cancel(); reject(); } chunks.push(part.value); }
    const value = object(parseBoundedJsonBytes(Buffer.concat(chunks), 65_536));
    if (!Array.isArray(value.keys) || value.keys.length < 1 || value.keys.length > 64) reject();
    const admitted = value.keys.map(object);
    cache.set(uri, { until: now() + 300_000, keys: admitted }); return admitted;
  }
  return Object.freeze({ verify: async (token: string, config: GcpOidcConfig) => {
    try {
      validateGcpOidcConfig(config);
      if (typeof token !== "string" || token.length > 24_576) reject();
      const segments = token.split("."); if (segments.length !== 3) reject();
      const [encodedHeader, encodedClaims, signature] = segments as [string, string, string];
      const header = jsonSegment(encodedHeader); const claims = jsonSegment(encodedClaims);
      if ((header.alg !== "RS256" && header.alg !== "ES256") || typeof header.kid !== "string" || !header.kid ||
          header.kid.length > 256 || header.crit !== undefined || header.jku !== undefined || header.x5u !== undefined ||
          header.jwk !== undefined || (header.typ !== undefined && !["JWT", "at+jwt"].includes(header.typ as string))) reject();
      const candidates = (await keys(config.jwksUri)).filter((key) => key.kid === header.kid);
      if (candidates.length !== 1) reject();
      const jwk = candidates[0]!;
      if ((jwk.use !== undefined && jwk.use !== "sig") || (jwk.alg !== undefined && jwk.alg !== header.alg) ||
          (jwk.key_ops !== undefined && (!Array.isArray(jwk.key_ops) || !jwk.key_ops.includes("verify"))) ||
          Object.hasOwn(jwk, "d") || (header.alg === "RS256" && jwk.kty !== "RSA") ||
          (header.alg === "ES256" && (jwk.kty !== "EC" || jwk.crv !== "P-256"))) reject();
      const key = createPublicKey({ key: jwk as JsonWebKey, format: "jwk" });
      if (header.alg === "RS256" && (key.asymmetricKeyDetails?.modulusLength ?? 0) < 2_048) reject();
      const signed = Buffer.from(`${encodedHeader}.${encodedClaims}`);
      const sig = Buffer.from(signature, "base64url");
      if (!/^[A-Za-z0-9_-]+$/u.test(signature) || sig.toString("base64url") !== signature ||
          !verify("sha256", signed, header.alg === "ES256" ? { key, dsaEncoding: "ieee-p1363" } : key, sig)) reject();
      const seconds = Math.floor(now() / 1_000);
      if (claims.iss !== config.issuer || claims.aud !== config.audience ||
          typeof claims.sub !== "string" || !claims.sub || claims.sub.length > 512 ||
          !Number.isSafeInteger(claims.exp) || (claims.exp as number) <= seconds ||
          !Number.isSafeInteger(claims.iat) || (claims.iat as number) > seconds + 30 ||
          (claims.exp as number) <= (claims.iat as number) || (claims.exp as number) - (claims.iat as number) > 3_600 ||
          (claims.nbf !== undefined && (!Number.isSafeInteger(claims.nbf) || (claims.nbf as number) > seconds)) ||
          (claims.iat as number) < seconds - 3_600) reject();
      return Object.freeze(claims);
    } catch { return reject(); }
  } });
}
export interface GcpIdentityConfig {
  readonly profile: "personal" | "bduk";
  readonly publicOrigin: string;
  readonly transportAudience?: string;
  readonly transportSubject: string;
  readonly identity: { readonly mode: "single-owner-transport-pilot" } | ({ readonly mode: "oidc" } & GcpOidcConfig);
}
export interface GcpIdentityEnvelope {
  readonly transport: { readonly issuer: string; readonly subject: string; readonly verified: true };
  readonly principal: GcpVerifiedPrincipal;
}
export function createGcpIdentityAdapter(config: GcpIdentityConfig, verifier = createGcpJwtVerifier()) {
  const audience = config.transportAudience ?? config.publicOrigin;
  if (!/^\d{10,32}$/u.test(config.transportSubject) || new URL(audience).origin !== audience ||
      !audience.startsWith("https://") || (config.profile === "bduk" && config.identity.mode !== "oidc")) reject();
  const transportConfig = { issuer: "https://accounts.google.com", audience,
    jwksUri: "https://www.googleapis.com/oauth2/v3/certs" };
  if (config.identity.mode === "oidc") validateGcpOidcConfig(config.identity);
  async function authenticateTransport(request: Request) {
    // Edge IAM verifies X-Serverless-Authorization. Cloud Run strips its signature.
    // The narrow proxy preserves a *separate full signed copy*; this app verifies it independently.
    for (const key of ["x-user-email", "x-user-id", "x-roles", "x-gis-user", "x-goog-authenticated-user-email",
      "x-goog-authenticated-user-id", "x-forwarded-user", "x-gis-role"]) if (request.headers.has(key)) reject();
    const proof = request.headers.get("x-gis-invocation-proof"); if (!proof) reject();
    const transportClaims = await verifier.verify(proof, transportConfig);
    if (transportClaims.sub !== config.transportSubject) reject();
    const transport = Object.freeze({ issuer: transportConfig.issuer, subject: config.transportSubject, verified: true as const });
    return { transport, transportClaims };
  }
  return Object.freeze({ authenticateTransport: async (request: Request) => (await authenticateTransport(request)).transport,
    authenticate: async (request: Request): Promise<GcpIdentityEnvelope> => {
    const { transport, transportClaims } = await authenticateTransport(request);
    let principal: GcpVerifiedPrincipal;
    if (config.identity.mode === "single-owner-transport-pilot") {
      if (request.headers.has("authorization")) reject();
      principal = Object.freeze({ kind: "single-owner-transport-pilot", issuer: transport.issuer,
        subject: transport.subject, scope: gcpPrincipalScope(transport.issuer, transport.subject, config.profile),
        roles: Object.freeze(["owner"] as const), environment: config.profile,
        classification: "public-metadata", expiresAt: transportClaims.exp as number });
    } else {
      const match = /^Bearer ([A-Za-z0-9_.-]+)$/u.exec(request.headers.get("authorization") ?? ""); if (!match) reject();
      const claims = await verifier.verify(match[1]!, config.identity);
      const groups = claims[config.identity.groupClaim ?? "groups"];
      if (groups !== undefined && (!Array.isArray(groups) || groups.length > 128 || groups.some((group) => typeof group !== "string"))) reject();
      const roles = new Set<GcpRole>();
      for (const role of config.identity.subjectRoles?.[claims.sub as string] ?? []) roles.add(role);
      for (const group of (groups ?? []) as string[]) for (const role of config.identity.groupRoles?.[group] ?? []) roles.add(role);
      principal = Object.freeze({ kind: "human-oidc", issuer: config.identity.issuer, subject: claims.sub as string,
        scope: gcpPrincipalScope(config.identity.issuer, claims.sub as string, config.profile), roles: Object.freeze([...roles].sort()),
        environment: config.profile, classification: "public-metadata", expiresAt: claims.exp as number });
    }
    PRINCIPALS.add(principal); return Object.freeze({ transport, principal });
  } });
}

export type GcpCapability = "website" | "knowledge.read" | "knowledge.export" | "knowledge.search" |
  "cpih.select" | "cpih.query" | "evidence.inspect" | "operations.status";
const GRANTS: Readonly<Record<GcpRole, readonly GcpCapability[]>> = Object.freeze({
  viewer: ["website", "knowledge.read", "knowledge.search", "cpih.select"],
  analyst: ["website", "knowledge.read", "knowledge.search", "cpih.select", "cpih.query", "evidence.inspect"],
  "evidence-auditor": ["website", "knowledge.read", "knowledge.search", "evidence.inspect"],
  "platform-operator": ["operations.status"],
  owner: ["website", "knowledge.read", "knowledge.export", "knowledge.search", "cpih.select", "cpih.query", "evidence.inspect", "operations.status"],
});
/** One deny-by-default ABAC decision used for lists, invocations, resources, HTTP and exports. */
export function gcpAuthorise(principal: GcpVerifiedPrincipal, capability: GcpCapability,
  resource: { readonly classification: string; readonly environment: string; readonly principalScope?: string }, now = Date.now()): boolean {
  return isGcpVerifiedPrincipal(principal) && principal.expiresAt * 1_000 > now &&
    principal.environment === resource.environment && resource.classification === "public-metadata" &&
    (resource.principalScope === undefined || resource.principalScope === principal.scope) &&
    principal.roles.some((role) => GRANTS[role]?.includes(capability));
}
