/** Bounded browser OIDC over maintained openid-client. Secrets and tokens never enter the release manifest. */
import { createCipheriv, createDecipheriv, createHash, randomBytes, timingSafeEqual } from "node:crypto";
import { parseBoundedJsonBytes } from "./bounded-json.js";
import { type GcpAtomicDocumentStore } from "./gcp-firestore.js";
import { createGcpJwtVerifier, gcpPrincipalScope, type GcpJwtVerifier, type GcpOidcConfig } from "./gcp-identity.js";

export interface GcpBrowserOidcConfig {
  readonly clientId: string;
  readonly clientAuthMethod: "client_secret_basic" | "none";
  readonly callbackUrl: string;
  readonly allowedRedirectUris: readonly string[];
  /** Exact approved HTTPS destinations, including discovery, authorisation, token and JWKS URLs. */
  readonly allowedEndpoints: readonly string[];
  readonly scopes: readonly string[];
  readonly sessionSeconds: 300;
}
export interface GcpBrowserSecrets { readonly sessionKey: string; readonly clientSecret?: string }
export class GcpBrowserIdentityError extends Error {
  constructor() { super("Browser identity could not be verified"); this.name = "GcpBrowserIdentityError"; }
}
const SESSION = "__Host-gis-browser"; const FLOW = "__Host-gis-login";
function fail(): never { throw new GcpBrowserIdentityError(); }
/** openid-client 6.8.8's declaration getter currently conflicts with exactOptionalPropertyTypes.
 * This narrow facade avoids changing repository assurance flags; all protocol/crypto work still runs in the pinned library.
 * Real signed-issuer tests cover this facade against the installed maintained implementation. */
interface MaintainedConfiguration { serverMetadata(): { issuer: string; authorization_endpoint?: string; token_endpoint?: string; jwks_uri?: string; code_challenge_methods_supported?: string[] } }
interface MaintainedOidcClient {
  customFetch: symbol; clockTolerance: symbol; clockSkew: symbol;
  discovery(issuer: URL, clientId: string, metadata: Record<PropertyKey, unknown>, auth: unknown, options: Record<PropertyKey, unknown>): Promise<MaintainedConfiguration>;
  ClientSecretBasic(secret: string | undefined): unknown; None(): unknown; enableNonRepudiationChecks(config: unknown): void;
  randomPKCECodeVerifier(): string; randomState(): string; randomNonce(): string; calculatePKCECodeChallenge(verifier: string): Promise<string>;
  buildAuthorizationUrl(config: MaintainedConfiguration, parameters: Record<string, string>): URL;
  authorizationCodeGrant(config: MaintainedConfiguration, url: URL, checks: { expectedState: string; expectedNonce: string; pkceCodeVerifier: string; idTokenExpected: true }): Promise<{
    id_token?: string; access_token: string; claims(): { sub: string } | undefined;
  }>;
}
const libraryName: string = "openid-client";
const maintainedLibrary = () => import(libraryName) as Promise<MaintainedOidcClient>;
const hash = (purpose: string, sid: string) => createHash("sha256").update(JSON.stringify(["gis-ai-go.gcp-browser.v1", purpose, sid])).digest("hex");
/** 256 fixed slots per purpose: expired authentication documents are reused, never accumulated indefinitely. */
const slot = (purpose: string, sid: string) => hash(purpose + "-slot", sid.slice(0, 2));
const equal = (a: string, b: string) => Buffer.byteLength(a) === Buffer.byteLength(b) && timingSafeEqual(Buffer.from(a), Buffer.from(b));
function https(value: string) {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.hash || url.search) fail();
  return url;
}
export function validateGcpBrowserConfig(browser: GcpBrowserOidcConfig, publicOrigin: string) {
  if (!browser.clientId || browser.clientId.length > 256 || !["client_secret_basic", "none"].includes(browser.clientAuthMethod) ||
      browser.sessionSeconds !== 300 || browser.callbackUrl !== `${publicOrigin}/auth/callback` ||
      !Array.isArray(browser.allowedRedirectUris) || browser.allowedRedirectUris.length !== 1 || browser.allowedRedirectUris[0] !== browser.callbackUrl ||
      !Array.isArray(browser.allowedEndpoints) || browser.allowedEndpoints.length < 3 || browser.allowedEndpoints.length > 12 ||
      !Array.isArray(browser.scopes) || !browser.scopes.includes("openid") || browser.scopes.includes("offline_access") ||
      browser.scopes.length > 8 || browser.scopes.some((scope) => !/^[A-Za-z0-9:._-]{1,64}$/u.test(scope))) fail();
  https(publicOrigin); https(browser.callbackUrl);
  for (const endpoint of browser.allowedEndpoints) https(endpoint);
}
type Flow = { v: 1; kind: "login"; sid: string; state: string; nonce: string; verifier: string; exp: number };
type Session = { v: 1; kind: "session"; sid: string; token: string; exp: number };
export function createGcpBrowserOidc(options: {
  readonly browser: GcpBrowserOidcConfig; readonly identity: GcpOidcConfig;
  readonly publicOrigin: string; readonly environment: "personal" | "bduk";
  readonly secrets: GcpBrowserSecrets; readonly backend: GcpAtomicDocumentStore;
  readonly fetch?: typeof fetch; readonly verifier?: GcpJwtVerifier; readonly now?: () => number;
}) {
  const browser = options.browser; validateGcpBrowserConfig(browser, options.publicOrigin);
  const now = options.now ?? Date.now; const seconds = () => Math.floor(now() / 1_000);
  const key = Buffer.from(options.secrets.sessionKey, "base64url");
  if (key.length !== 32 || key.toString("base64url") !== options.secrets.sessionKey ||
      (browser.clientAuthMethod === "client_secret_basic" && !options.secrets.clientSecret)) fail();
  const fetcher = options.fetch ?? fetch; const verifier = options.verifier ?? createGcpJwtVerifier({ fetch: fetcher, now });
  const allowed = new Set(browser.allowedEndpoints);
  async function allocate(purpose: "flow" | "session", fields: Readonly<Record<string, string>>) {
    // At most four strong reads and CAS attempts. Occupied unexpired slots are never overwritten.
    for (let attempt = 0; attempt < 4; attempt += 1) {
      const sid = randomBytes(32).toString("hex"); const id = slot(purpose, sid); const previous = await options.backend.read(id);
      if (previous && Number(previous.fields.expires_at) > seconds() && !["consumed", "revoked"].includes(previous.fields.status ?? "")) continue;
      if (previous && previous.fields.schema !== `gis-ai-go.gcp-browser-${purpose}.v1`) fail();
      if (await options.backend.compareAndSet(id, previous?.version ?? null, { ...fields, sid_hash: hash(purpose, sid) })) return sid;
    }
    fail();
  }
  function cookie(name: string, value: string, age: number) { return `${name}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${age}`; }
  function seal(name: string, value: Flow | Session) {
    const iv = randomBytes(12); const cipher = createCipheriv("aes-256-gcm", key, iv); cipher.setAAD(Buffer.from(name));
    const encrypted = Buffer.concat([cipher.update(JSON.stringify(value)), cipher.final()]);
    const result = Buffer.concat([iv, encrypted, cipher.getAuthTag()]).toString("base64url");
    if (result.length > 3_800) fail(); return result;
  }
  function unseal<T extends Flow | Session>(request: Request, name: string, kind: T["kind"]): T | null {
    const cookies = (request.headers.get("cookie") ?? "").split(";").map((part) => part.trim()).filter((part) => part.startsWith(name + "="));
    if (!cookies.length) return null;
    try {
      if (cookies.length !== 1) fail();
      const encoded = cookies[0]!.slice(name.length + 1);
      if (encoded.length > 3_800 || !/^[A-Za-z0-9_-]+$/u.test(encoded)) fail();
      const bytes = Buffer.from(encoded, "base64url"); if (bytes.length < 29 || bytes.toString("base64url") !== encoded) fail();
      const decipher = createDecipheriv("aes-256-gcm", key, bytes.subarray(0, 12)); decipher.setAAD(Buffer.from(name)); decipher.setAuthTag(bytes.subarray(-16));
      const value = parseBoundedJsonBytes(Buffer.concat([decipher.update(bytes.subarray(12, -16)), decipher.final()]), 4_096) as T;
      if (value.v !== 1 || value.kind !== kind || !/^[0-9a-f]{64}$/u.test(value.sid) || !Number.isSafeInteger(value.exp) || value.exp <= seconds()) fail();
      return value;
    } catch { return fail(); }
  }
  let configured: Promise<MaintainedConfiguration> | undefined;
  async function configuration() {
    configured ??= (async () => {
      const oidc = await maintainedLibrary();
      const guardedFetch = async (url: string, init: { method: string; headers: Record<string, string>; body?: BodyInit }) => {
        if (!allowed.has(url)) fail();
        const response = await fetcher(url, { method: init.method, headers: init.headers, ...(init.body === undefined ? {} : { body: init.body }),
          redirect: "error", signal: AbortSignal.timeout(5_000) });
        if (response.status >= 300 && response.status < 400) fail();
        const reader = response.body?.getReader(); if (!reader) return response;
        let size = 0; const chunks: Uint8Array[] = [];
        for (;;) { const part = await reader.read(); if (part.done) break; size += part.value.byteLength;
          if (size > 65_536) { void reader.cancel(); fail(); } chunks.push(part.value); }
        return new Response(Buffer.concat(chunks), { status: response.status, headers: response.headers });
      };
      const client = await oidc.discovery(new URL(options.identity.issuer), browser.clientId,
        { id_token_signed_response_alg: "RS256", [oidc.clockTolerance]: 0,
          [oidc.clockSkew]: Math.floor(now() / 1_000) - Math.floor(Date.now() / 1_000) },
        browser.clientAuthMethod === "client_secret_basic" ? oidc.ClientSecretBasic(options.secrets.clientSecret) : oidc.None(),
        { [oidc.customFetch]: guardedFetch, timeout: 5, execute: [oidc.enableNonRepudiationChecks] });
      const metadata = client.serverMetadata();
      if (metadata.issuer !== options.identity.issuer || !metadata.authorization_endpoint || !metadata.token_endpoint || !metadata.jwks_uri ||
          [metadata.authorization_endpoint, metadata.token_endpoint, metadata.jwks_uri].some((endpoint) => !allowed.has(endpoint)) ||
          metadata.jwks_uri !== options.identity.jwksUri || !metadata.code_challenge_methods_supported?.includes("S256")) fail();
      return client;
    })().catch((error) => { configured = undefined; throw error; });
    return configured;
  }
  function csrf(request: Request) { if (request.headers.get("origin") !== options.publicOrigin) fail(); }
  async function session(request: Request): Promise<Session | null> {
    const value = unseal<Session>(request, SESSION, "session"); if (!value) return null;
    const stored = await options.backend.read(slot("session", value.sid));
    if (stored?.fields.schema !== "gis-ai-go.gcp-browser-session.v1" || stored.fields.status !== "active" ||
        stored.fields.sid_hash !== hash("session", value.sid) || Number(stored.fields.expires_at) !== value.exp || value.exp > seconds() + 300) fail();
    const claims = await verifier.verify(value.token, options.identity);
    if ((claims.exp as number) - (claims.iat as number) > 300 || value.exp > (claims.exp as number) ||
        stored.fields.principal_scope !== gcpPrincipalScope(options.identity.issuer, claims.sub as string, options.environment)) fail();
    return value;
  }
  return Object.freeze({
    cookieAuthenticated: (request: Request) => !request.headers.has("authorization") && (request.headers.get("cookie") ?? "").includes(SESSION + "="),
    authenticateRequest: async (request: Request): Promise<Request> => {
      if (request.headers.has("authorization")) return request;
      const value = await session(request); if (!value) return request;
      if (!["GET", "HEAD"].includes(request.method)) csrf(request);
      const headers = new Headers(request.headers); headers.set("authorization", `Bearer ${value.token}`);
      return new Request(request, { headers });
    },
    handle: async (request: Request): Promise<Response | null> => {
      const url = new URL(request.url);
      try {
        if (url.pathname === "/auth/login" && request.method === "GET") {
          if (url.search) fail();
          const oidc = await maintainedLibrary();
          const client = await configuration(); const verifierValue = oidc.randomPKCECodeVerifier();
          const flow: Flow = { v: 1, kind: "login", sid: randomBytes(32).toString("hex"), state: oidc.randomState(), nonce: oidc.randomNonce(),
            verifier: verifierValue, exp: seconds() + 300 };
          flow.sid = await allocate("flow", { schema: "gis-ai-go.gcp-browser-flow.v1", status: "pending", expires_at: String(flow.exp) });
          const target = oidc.buildAuthorizationUrl(client, { redirect_uri: browser.callbackUrl, scope: browser.scopes.join(" "), response_type: "code",
            state: flow.state, nonce: flow.nonce, code_challenge: await oidc.calculatePKCECodeChallenge(flow.verifier), code_challenge_method: "S256" });
          if (!allowed.has(target.origin + target.pathname)) fail();
          return new Response(null, { status: 302, headers: { location: target.href, "set-cookie": cookie(FLOW, seal(FLOW, flow), 300), "cache-control": "no-store" } });
        }
        if (url.pathname === "/auth/callback" && request.method === "GET") {
          if ([...url.searchParams.keys()].some((name) => !["code", "state", "iss", "error", "error_description"].includes(name)) ||
              [...new Set(url.searchParams.keys())].some((name) => url.searchParams.getAll(name).length !== 1)) fail();
          const flow = unseal<Flow>(request, FLOW, "login");
          if (!flow || !url.searchParams.get("state") || !equal(flow.state, url.searchParams.get("state")!)) fail();
          const stored = await options.backend.read(slot("flow", flow.sid));
          if (stored?.fields.schema !== "gis-ai-go.gcp-browser-flow.v1" || stored.fields.status !== "pending" || stored.fields.sid_hash !== hash("flow", flow.sid) || Number(stored.fields.expires_at) !== flow.exp ||
              !await options.backend.compareAndSet(slot("flow", flow.sid), stored.version, { ...stored.fields, status: "consumed" })) fail();
          const callback = new URL(browser.callbackUrl); callback.search = url.search;
          const oidc = await maintainedLibrary();
          const tokens = await oidc.authorizationCodeGrant(await configuration(), callback, { expectedState: flow.state, expectedNonce: flow.nonce,
            pkceCodeVerifier: flow.verifier, idTokenExpected: true });
          if (!tokens.id_token || !tokens.access_token || tokens.access_token.length > 2_500) fail();
          const claims = await verifier.verify(tokens.access_token, options.identity);
          if ((claims.exp as number) - (claims.iat as number) > 300 || tokens.claims()?.sub !== claims.sub) fail();
          const value: Session = { v: 1, kind: "session", sid: randomBytes(32).toString("hex"), token: tokens.access_token,
            exp: Math.min(seconds() + 300, claims.exp as number) };
          value.sid = await allocate("session", { schema: "gis-ai-go.gcp-browser-session.v1", status: "active",
            expires_at: String(value.exp), principal_scope: gcpPrincipalScope(options.identity.issuer, claims.sub as string, options.environment) });
          const encrypted = seal(SESSION, value);
          const headers = new Headers({ location: options.publicOrigin + "/", "cache-control": "no-store" });
          headers.append("set-cookie", cookie(SESSION, encrypted, value.exp - seconds())); headers.append("set-cookie", cookie(FLOW, "", 0));
          return new Response(null, { status: 303, headers });
        }
        if (url.pathname === "/auth/logout") {
          if (request.method !== "POST" || url.search) fail(); csrf(request);
          const value = await session(request);
          if (value) {
            const id = slot("session", value.sid); const stored = await options.backend.read(id);
            if (!stored || stored.fields.sid_hash !== hash("session", value.sid) || !await options.backend.compareAndSet(id, stored.version, { ...stored.fields, status: "revoked" })) fail();
          }
          const headers = new Headers({ location: options.publicOrigin + "/", "cache-control": "no-store" });
          headers.append("set-cookie", cookie(SESSION, "", 0)); headers.append("set-cookie", cookie(FLOW, "", 0));
          return new Response(null, { status: 303, headers });
        }
        return null;
      } catch { return new Response('{"code":"browser-authentication-rejected"}', { status: 400, headers: {
        "content-type": "application/json", "cache-control": "no-store", "set-cookie": cookie(FLOW, "", 0) } }); }
    },
  });
}
