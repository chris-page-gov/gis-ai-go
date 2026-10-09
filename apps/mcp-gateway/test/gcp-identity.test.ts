import assert from "node:assert/strict";
import test from "node:test";
import { createGcpIdentityAdapter, createGcpJwtVerifier, gcpAuthorise, GcpIdentityError } from "../src/gcp-identity.js";
import { CLOCK, credentials, HUMAN_ISSUER, JWK, jwksFetch, ORIGIN, principal, runtimeConfig, signed, TRANSPORT_SUBJECT } from "./gcp-test-support.js";

test("synthetic signed verification enforces signature, exact issuer/audience, lifetime, key source and algorithm", async () => {
  const verifier = createGcpJwtVerifier({ fetch: jwksFetch, now: () => CLOCK });
  const config = { issuer: HUMAN_ISSUER, audience: `${ORIGIN}/mcp`, jwksUri: `${HUMAN_ISSUER}/v1/keys` };
  const valid = { iss: config.issuer, aud: config.audience, sub: "synthetic-human", iat: CLOCK / 1_000, exp: CLOCK / 1_000 + 300 };
  assert.equal((await verifier.verify(signed(valid), config)).sub, "synthetic-human");
  for (const change of [
    { iss: `${config.issuer}.attacker` }, { aud: ORIGIN }, { aud: [config.audience, "other"] }, { exp: CLOCK / 1_000 },
    { exp: CLOCK / 1_000 + 3_601 }, { iat: undefined }, { iat: CLOCK / 1_000 + 60 }, { nbf: CLOCK / 1_000 + 1 }, { sub: "" },
  ]) await assert.rejects(verifier.verify(signed({ ...valid, ...change }), config), GcpIdentityError);
  for (const header of [{ alg: "none", kid: "synthetic-1" }, { alg: "HS256", kid: "synthetic-1" },
    { alg: "RS256", kid: "synthetic-1", jku: "https://attacker.example/keys" }, { alg: "RS256", kid: "other" },
    { alg: "RS256", kid: "synthetic-1", crit: ["anything"] }]) await assert.rejects(verifier.verify(signed(valid, header), config), GcpIdentityError);
  const token = signed(valid); const signature = token.slice(token.lastIndexOf(".") + 1);
  await assert.rejects(verifier.verify(token.slice(0, token.lastIndexOf(".") + 1) + (signature[0] === "A" ? "B" : "A") + signature.slice(1), config), GcpIdentityError);
});

test("JWKS lookup is bounded and fail-closed after cache expiry, redirects and duplicate key IDs", async () => {
  let calls = 0; let clock = CLOCK; let unavailable = false;
  const fetcher: typeof fetch = async (_url, init) => {
    calls += 1; assert.equal(init?.redirect, "error");
    if (unavailable) throw Error("synthetic outage"); return new Response(JSON.stringify({ keys: [JWK] }), { headers: { "content-type": "application/json" } });
  };
  const verifier = createGcpJwtVerifier({ fetch: fetcher, now: () => clock });
  const config = { issuer: HUMAN_ISSUER, audience: ORIGIN, jwksUri: `${HUMAN_ISSUER}/v1/keys` };
  const token = () => signed({ iss: config.issuer, aud: config.audience, sub: "human", iat: clock / 1_000, exp: clock / 1_000 + 300 });
  await verifier.verify(token(), config); await verifier.verify(token(), config); assert.equal(calls, 1);
  clock += 301_000; unavailable = true;
  await assert.rejects(verifier.verify(token(), config), GcpIdentityError); assert.equal(calls, 2);
  const duplicate = createGcpJwtVerifier({ now: () => CLOCK, fetch: async () => new Response(JSON.stringify({ keys: [JWK, JWK] }), { headers: { "content-type": "application/json" } }) });
  await assert.rejects(duplicate.verify(signed({ iss: config.issuer, aud: config.audience, sub: "human", iat: CLOCK / 1_000, exp: CLOCK / 1_000 + 300 }), config), GcpIdentityError);
});

test("transport workload is distinct from signed human identity; spoofed roles, email suffixes and bare headers grant nothing", async () => {
  const config = runtimeConfig(["analyst"]);
  const adapter = createGcpIdentityAdapter(config, createGcpJwtVerifier({ fetch: jwksFetch, now: () => CLOCK }));
  const verified = await adapter.authenticate(new Request(ORIGIN, { headers: credentials(config) }));
  assert.equal(verified.transport.subject, TRANSPORT_SUBJECT); assert.equal(verified.principal.subject, "synthetic-human");
  assert.equal(verified.principal.kind, "human-oidc"); assert.deepEqual(verified.principal.roles, ["analyst"]);
  for (const key of ["x-roles", "x-user-email", "x-goog-authenticated-user-email", "x-gis-role"]) {
    await assert.rejects(adapter.authenticate(new Request(ORIGIN, { headers: { ...credentials(config), [key]: "owner@bduk.gov.uk" } })), GcpIdentityError);
  }
  const unknown = await principal([], "unapproved@bduk.gov.uk"); assert.deepEqual(unknown.roles, []);
  assert.equal(gcpAuthorise(unknown, "knowledge.read", { classification: "public-metadata", environment: "bduk" }, CLOCK), false);
  await assert.rejects(adapter.authenticate(new Request(ORIGIN, { headers: { authorization: credentials(config).authorization! } })), GcpIdentityError);
});

test("single-owner transport pilot never claims human sign-in; strict RBAC/ABAC rejects scope/classification/environment/expiry", async () => {
  const config = runtimeConfig([], "personal");
  const adapter = createGcpIdentityAdapter(config, createGcpJwtVerifier({ fetch: jwksFetch, now: () => CLOCK }));
  const { principal: owner } = await adapter.authenticate(new Request(ORIGIN, { headers: credentials(config) }));
  assert.equal(owner.kind, "single-owner-transport-pilot"); assert.equal(owner.subject, TRANSPORT_SUBJECT);
  const viewer = await principal(["viewer"]); const analyst = await principal(["analyst"]); const auditor = await principal(["evidence-auditor"]); const operator = await principal(["platform-operator"]);
  const resource = { classification: "public-metadata", environment: "bduk" };
  assert.equal(gcpAuthorise(viewer, "cpih.query", resource, CLOCK), false);
  assert.equal(gcpAuthorise(analyst, "cpih.query", resource, CLOCK), true);
  assert.equal(gcpAuthorise(auditor, "evidence.inspect", resource, CLOCK), true);
  assert.equal(gcpAuthorise(auditor, "cpih.query", resource, CLOCK), false);
  assert.equal(gcpAuthorise(operator, "operations.status", resource, CLOCK), true);
  assert.equal(gcpAuthorise(operator, "knowledge.read", resource, CLOCK), false);
  assert.equal(gcpAuthorise(analyst, "knowledge.read", { ...resource, classification: "protected" }, CLOCK), false);
  assert.equal(gcpAuthorise(analyst, "knowledge.read", { ...resource, environment: "personal" }, CLOCK), false);
  assert.equal(gcpAuthorise(analyst, "evidence.inspect", { ...resource, principalScope: "f".repeat(64) }, CLOCK), false);
  assert.equal(gcpAuthorise(analyst, "knowledge.read", resource, CLOCK + 3_600_001), false);
  assert.equal(gcpAuthorise({ ...analyst }, "knowledge.read", resource, CLOCK), false);
});
