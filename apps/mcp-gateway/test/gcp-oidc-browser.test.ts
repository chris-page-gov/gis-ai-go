import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";
import { createGcpBrowserOidc, GcpBrowserIdentityError, type GcpBrowserOidcConfig } from "../src/gcp-oidc-browser.js";
import { createGcpFetchHandler, type GcpReleaseAsset } from "../src/gcp-server.js";
import { createGcpJwtVerifier } from "../src/gcp-identity.js";
import { CLOCK, credentials, FakeAtomicStore, HUMAN_ISSUER, JWK, knowledge, ORIGIN, PROJECTION, runtimeConfig, signed } from "./gcp-test-support.js";
const DISCOVERY = `${HUMAN_ISSUER}/.well-known/openid-configuration`;
const AUTHORISE = `${HUMAN_ISSUER}/v1/authorize`; const TOKEN = `${HUMAN_ISSUER}/v1/token`; const JWKS = `${HUMAN_ISSUER}/v1/keys`;
const CLIENT_ID = "synthetic-browser-client";
const BROWSER: GcpBrowserOidcConfig = { clientId: CLIENT_ID, clientAuthMethod: "none", callbackUrl: ORIGIN + "/auth/callback",
  allowedRedirectUris: [ORIGIN + "/auth/callback"], allowedEndpoints: [DISCOVERY, AUTHORISE, TOKEN, JWKS], scopes: ["openid", "groups"], sessionSeconds: 300 };
const cookieValue = (response: Response, name: string) => response.headers.getSetCookie().find((cookie) => cookie.startsWith(name + "="))!.split(";")[0]!;
function fixture(overrides: { idNonce?: string; idAudience?: string; idIssuer?: string; idSignatureBad?: boolean; accessLifetime?: number; accessAudience?: string; metadataIssuer?: string; tokenEndpoint?: string } = {}) {
  const backend = new FakeAtomicStore(); let clock = CLOCK; let nonce = ""; let challenge = ""; let exchanges = 0; const destinations: string[] = [];
  const config = runtimeConfig(["analyst"]);
  assert.equal(config.identity.mode, "oidc");
  const identity = config.identity as Extract<typeof config.identity, { mode: "oidc" }>;
  const fetcher: typeof fetch = async (input, init) => {
    const url = String(input); destinations.push(url); assert.equal(init?.redirect, "error");
    if (url === DISCOVERY) return new Response(JSON.stringify({ issuer: overrides.metadataIssuer ?? HUMAN_ISSUER,
      authorization_endpoint: AUTHORISE, token_endpoint: overrides.tokenEndpoint ?? TOKEN, jwks_uri: JWKS,
      response_types_supported: ["code"], subject_types_supported: ["public"], id_token_signing_alg_values_supported: ["RS256"],
      code_challenge_methods_supported: ["S256"], token_endpoint_auth_methods_supported: ["none"] }), { headers: { "content-type": "application/json" } });
    if (url === JWKS) return new Response(JSON.stringify({ keys: [JWK] }), { headers: { "content-type": "application/json" } });
    if (url === TOKEN) {
      exchanges += 1;
      const body = new URLSearchParams(init?.body as URLSearchParams); assert.equal(body.get("client_id"), CLIENT_ID);
      assert.equal(body.get("redirect_uri"), BROWSER.callbackUrl);
      assert.equal(createHash("sha256").update(body.get("code_verifier")!).digest("base64url"), challenge);
      const base = { iss: overrides.idIssuer ?? HUMAN_ISSUER, sub: "synthetic-human", iat: clock / 1_000, exp: clock / 1_000 + 300 };
      let idToken = signed({ ...base, aud: overrides.idAudience ?? CLIENT_ID, nonce: overrides.idNonce ?? nonce });
      if (overrides.idSignatureBad) { const index = idToken.lastIndexOf(".") + 1; idToken = idToken.slice(0, index) + (idToken[index] === "A" ? "B" : "A") + idToken.slice(index + 1); }
      return new Response(JSON.stringify({ token_type: "Bearer", expires_in: 300,
        id_token: idToken,
        access_token: signed({ ...base, iss: HUMAN_ISSUER, exp: clock / 1_000 + (overrides.accessLifetime ?? 300), aud: overrides.accessAudience ?? identity.audience }),
      }), { headers: { "content-type": "application/json" } });
    }
    throw Error("Synthetic issuer requested an unapproved endpoint");
  };
  const options = { browser: BROWSER, identity, publicOrigin: ORIGIN, environment: "bduk" as const,
    secrets: { sessionKey: Buffer.alloc(32, 1).toString("base64url") }, backend, fetch: fetcher, now: () => clock,
    verifier: createGcpJwtVerifier({ fetch: fetcher, now: () => clock }) };
  const adapter = createGcpBrowserOidc(options);
  async function login() {
    const response = await adapter.handle(new Request(ORIGIN + "/auth/login")); assert.equal(response!.status, 302);
    const redirect = new URL(response!.headers.get("location")!); nonce = redirect.searchParams.get("nonce")!; challenge = redirect.searchParams.get("code_challenge")!;
    const state = redirect.searchParams.get("state")!;
    return { response: response!, redirect, state, cookie: cookieValue(response!, "__Host-gis-login") };
  }
  async function callback(flow: Awaited<ReturnType<typeof login>>, state = flow.state, selectedAdapter = adapter) {
    nonce = flow.redirect.searchParams.get("nonce")!; challenge = flow.redirect.searchParams.get("code_challenge")!;
    return selectedAdapter.handle(new Request(`${BROWSER.callbackUrl}?code=synthetic-code&state=${state}&iss=${encodeURIComponent(HUMAN_ISSUER)}`, { headers: { cookie: flow.cookie } }));
  }
  return { adapter, backend, options, config, login, callback, get exchanges() { return exchanges; }, destinations,
    advance: (milliseconds: number) => { clock += milliseconds; } };
}

test("private callers cannot reserve shared storage by starting or failing browser logins", async () => {
  const s = fixture(); const victim = await s.login();
  for (let index = 0; index < 400; index += 1) await s.login();
  assert.equal(s.backend.rows.size, 0); assert.equal(s.backend.writes, 0);
  assert.equal((await s.callback(victim))!.status, 303);
  const rejected = fixture({ idNonce: "wrong" }); const badFlow = await rejected.login();
  assert.equal((await rejected.callback(badFlow))!.status, 400);
  assert.equal(rejected.backend.rows.size, 0); assert.equal(rejected.backend.writes, 0);
});

test("concurrent verified callbacks accept one session and retain original replay state across fresh adapters", async () => {
  const s = fixture(); const flow = await s.login();
  const results = await Promise.all([s.callback(flow), s.callback(flow)]);
  assert.deepEqual(results.map((response) => response!.status).sort(), [303, 400]);
  assert.equal([...s.backend.rows.values()].filter((row) => row.fields.status === "active").length, 1);
  const fresh = createGcpBrowserOidc(s.options); const exchanges = s.exchanges;
  assert.equal((await fresh.handle(new Request(`${BROWSER.callbackUrl}?code=synthetic-code&state=${flow.state}`, { headers: { cookie: flow.cookie } })))!.status, 400);
  assert.equal(s.exchanges, exchanges);
  const successful = results.find((response) => response!.status === 303)!;
  const cookie = cookieValue(successful!, "__Host-gis-browser");
  assert.equal((await fresh.handle(new Request(ORIGIN + "/auth/logout", { method: "POST", headers: { cookie, origin: ORIGIN } })))!.status, 303);
  assert.equal((await s.callback(flow))!.status, 400); assert.equal(s.exchanges, exchanges);
});

test("distinct verified flows admitted concurrently do not exhaust replay-ledger retry rounds", async () => {
  const shared = new FakeAtomicStore(); const cases = Array.from({ length: 8 }, () => fixture());
  const adapters = cases.map((entry) => createGcpBrowserOidc({ ...entry.options, backend: shared }));
  const flows = await Promise.all(cases.map((entry) => entry.login()));
  const original = shared.compareAndSet;
  let expected = 8; let waiting: (() => void)[] = [];
  shared.compareAndSet = async (id, version, fields) => {
    if (fields.schema === "gis-ai-go.gcp-browser-consumed-flows.v2") {
      await new Promise<void>((resolve) => {
        waiting.push(resolve);
        if (waiting.length === expected) {
          const ready = waiting; waiting = []; expected -= 1;
          for (const release of ready) release();
        }
      });
    }
    return original(id, version, fields);
  };
  const responses = await Promise.all(cases.map((entry, index) => entry.callback(flows[index]!, flows[index]!.state, adapters[index])));
  assert.deepEqual(responses.map((response) => response!.status), Array(8).fill(303));
  assert.equal([...shared.rows.values()].filter((row) => row.fields.status === "active").length, 8);
});

test("accepted flow tombstone survives session failure; expiry during verification cannot commit a flow", async () => {
  const s = fixture(); const flow = await s.login();
  const original = s.backend.compareAndSet;
  s.backend.compareAndSet = async (id, version, fields) => fields.schema === "gis-ai-go.gcp-browser-session.v1" ? false : original(id, version, fields);
  assert.equal((await s.callback(flow))!.status, 400); const exchanges = s.exchanges;
  assert.equal((await s.callback(flow))!.status, 400); assert.equal(s.exchanges, exchanges);
  const expired = fixture(); const expiredFlow = await expired.login();
  const verifier = { verify: async (token: string, config: Parameters<typeof expired.options.verifier.verify>[1]) => {
    const claims = await expired.options.verifier.verify(token, config); expired.advance(300_001); return claims;
  } };
  const adapter = createGcpBrowserOidc({ ...expired.options, verifier });
  assert.equal((await adapter.handle(new Request(`${BROWSER.callbackUrl}?code=synthetic-code&state=${expiredFlow.state}`, { headers: { cookie: expiredFlow.cookie } })))!.status, 400);
  assert.equal(expired.backend.writes, 0);
});

test("maintained OIDC performs exact issuer/client ID/signature/nonce validation with state and S256 PKCE; encrypted session rechecks signed access", async () => {
  const s = fixture(); const flow = await s.login();
  assert.equal(flow.redirect.origin + flow.redirect.pathname, AUTHORISE); assert.equal(flow.redirect.searchParams.get("response_type"), "code");
  assert.equal(flow.redirect.searchParams.get("code_challenge_method"), "S256"); assert.equal(flow.redirect.searchParams.get("redirect_uri"), BROWSER.callbackUrl);
  assert.match(flow.response.headers.get("set-cookie")!, /HttpOnly; Secure; SameSite=Lax; Max-Age=300/u);
  assert.equal((await s.callback(flow, "wrong-state"))!.status, 400); assert.equal(s.exchanges, 0);
  const callback = (await s.callback(flow))!; assert.equal(callback.status, 303); assert.equal(callback.headers.get("location"), ORIGIN + "/");
  const cookie = cookieValue(callback, "__Host-gis-browser"); assert.equal(cookie.includes("synthetic-human"), false); assert.equal(cookie.includes("Bearer"), false);
  const authenticated = await s.adapter.authenticateRequest(new Request(ORIGIN + "/api/release", { headers: { cookie } }));
  assert.match(authenticated.headers.get("authorization")!, /^Bearer /u);
  assert.equal(JSON.stringify([...s.backend.rows.values()]).includes(authenticated.headers.get("authorization")!.slice(7)), false);
  assert.equal((await s.callback(flow))!.status, 400); assert.equal(s.exchanges, 1); // Consumed state cannot replay a code.
  s.advance(300_001); await assert.rejects(s.adapter.authenticateRequest(new Request(ORIGIN, { headers: { cookie } })), GcpBrowserIdentityError);
});

test("wrong nonce, client audience, issuer or access resource audience rejects the signed mock response", async () => {
  for (const overrides of [{ idNonce: "other-nonce" }, { idAudience: "other-client" }, { idIssuer: HUMAN_ISSUER + "/wrong" }, { accessAudience: "wrong-resource" }, { idSignatureBad: true }, { accessLifetime: 301 }]) {
    const s = fixture(overrides); assert.equal((await s.callback(await s.login()))!.status, 400);
    assert.equal([...s.backend.rows.values()].some((doc) => doc.fields.schema === "gis-ai-go.gcp-browser-session.v1"), false);
  }
});

test("discovery issuer/endpoint mismatch, redirect injection and altered encrypted cookies fail without external requests", async () => {
  for (const overrides of [{ metadataIssuer: "https://attacker.example" }, { tokenEndpoint: "https://attacker.example/token" }]) {
    const s = fixture(overrides); assert.equal((await s.adapter.handle(new Request(ORIGIN + "/auth/login")))!.status, 400);
    assert.deepEqual(s.destinations, [DISCOVERY]);
  }
  const s = fixture(); assert.equal((await s.adapter.handle(new Request(ORIGIN + "/auth/login?next=https://attacker.example")))!.status, 400);
  assert.equal(s.destinations.length, 0);
  const flow = await s.login();
  const bad = flow.cookie.slice(0, -1) + (flow.cookie.endsWith("A") ? "B" : "A");
  assert.equal((await s.adapter.handle(new Request(`${BROWSER.callbackUrl}?code=synthetic&state=${flow.state}`, { headers: { cookie: bad } })))!.status, 400);
  assert.equal(s.exchanges, 0);
});

test("cookie POST requires exact Origin; logout revokes opaque session across fresh adapters and rejects replay", async () => {
  const s = fixture(); const response = (await s.callback(await s.login()))!; const cookie = cookieValue(response, "__Host-gis-browser");
  for (const origin of [undefined, "null", "https://attacker.example"]) {
    await assert.rejects(s.adapter.authenticateRequest(new Request(ORIGIN + "/mcp", { method: "POST", headers: { cookie, ...(origin ? { origin } : {}) }, body: "{}" })), GcpBrowserIdentityError);
  }
  const authorised = await s.adapter.authenticateRequest(new Request(ORIGIN + "/mcp", { method: "POST", headers: { cookie, origin: ORIGIN }, body: "{}" }));
  assert.ok(authorised.headers.get("authorization"));
  assert.equal((await s.adapter.handle(new Request(ORIGIN + "/auth/logout", { headers: { cookie } })))!.status, 400);
  const logout = await s.adapter.handle(new Request(ORIGIN + "/auth/logout", { method: "POST", headers: { cookie, origin: ORIGIN } }));
  assert.equal(logout!.status, 303); assert.match(logout!.headers.getSetCookie().join(";"), /__Host-gis-browser=;.*Max-Age=0/u);
  await assert.rejects(createGcpBrowserOidc(s.options).authenticateRequest(new Request(ORIGIN, { headers: { cookie } })), GcpBrowserIdentityError);
});

test("server browser flow keeps transport separate, applies current role policy on each cookie request and preserves direct bearer MCP", async () => {
  const s = fixture();
  const config = { ...s.config, identity: { ...s.config.identity, browser: BROWSER } };
  const assets = new Map<string, GcpReleaseAsset>([["/", { bytes: Buffer.from("Existing governed website"), contentType: "text/html", kind: "website" }]]);
  const options = { config, assets, backend: s.backend, projection: PROJECTION, knowledge: knowledge(),
    browserSecrets: s.options.secrets, browserFetch: s.options.fetch, now: () => new Date(CLOCK),
    verifier: createGcpJwtVerifier({ now: () => CLOCK, fetch: async (input, init) => String(input) === "https://www.googleapis.com/oauth2/v3/certs"
      ? new Response(JSON.stringify({ keys: [JWK] }), { headers: { "content-type": "application/json" } }) : s.options.fetch(input, init) }),
  };
  const handler = createGcpFetchHandler(options); const proof = credentials(s.config)["x-gis-invocation-proof"];
  const headers = { "x-gis-invocation-proof": proof, accept: "text/html" };
  assert.equal((await handler.fetch(new Request(ORIGIN, { headers }))).status, 302);
  const response = (await s.callback(await s.login()))!; const cookie = cookieValue(response, "__Host-gis-browser");
  assert.equal((await handler.fetch(new Request(ORIGIN, { headers: { ...headers, cookie } }))).status, 200);
  assert.equal((await handler.fetch(new Request(ORIGIN, { headers: { cookie } }))).status, 401);
  const noRole = { ...config, identity: { ...config.identity, subjectRoles: { "synthetic-human": [] } } } as typeof config;
  const revoked = createGcpFetchHandler({ ...options, config: noRole });
  assert.equal((await revoked.fetch(new Request(ORIGIN, { headers: { ...headers, cookie } }))).status, 403);
  const direct = await handler.fetch(new Request(ORIGIN + "/api/release", { headers: credentials(s.config) })); assert.equal(direct.status, 200);
  const { browserSecrets: _secrets, ...withoutSecrets } = options; const unavailable = createGcpFetchHandler(withoutSecrets);
  assert.equal((await unavailable.fetch(new Request(ORIGIN + "/auth/login", { headers }))).status, 503);
});

test("verified-flow ledger and sessions stay bounded and expired markers can be reclaimed after restart", async () => {
  const s = fixture();
  for (let index = 0; index < 256; index += 1) {
    const response = await s.callback(await s.login()); assert.ok([303, 400].includes(response!.status));
  }
  assert.ok(s.backend.rows.size <= 257);
  const ledger = [...s.backend.rows.values()].find((row) => row.fields.schema === "gis-ai-go.gcp-browser-consumed-flows.v2")!;
  assert.equal(JSON.parse(ledger.fields.entries_json!).length, 256);
  const writes = s.backend.writes;
  assert.equal((await s.callback(await s.login()))!.status, 400); assert.equal(s.backend.writes, writes);
  s.advance(301_000);
  const fresh = createGcpBrowserOidc(s.options); const flow = await s.login();
  assert.equal((await s.callback(flow, flow.state, fresh))!.status, 303);
  const renewed = [...s.backend.rows.values()].find((row) => row.fields.schema === "gis-ai-go.gcp-browser-consumed-flows.v2")!;
  assert.equal(JSON.parse(renewed.fields.entries_json!).length, 1);
  assert.equal([...s.backend.rows.values()].some((row) => "token" in row.fields || "verifier" in row.fields || "nonce" in row.fields), false);
});
