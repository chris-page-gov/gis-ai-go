import dns from "node:dns/promises";
import { fstatSync, writeSync } from "node:fs";
import https from "node:https";
import { syncBuiltinESMExports } from "node:module";

const GUARDED_APIS = Object.freeze([
  "dns.Resolver.resolve4",
  "dns.Resolver.resolve6",
  "https.request",
]);
const ERROR_CODE = "GIS_AI_GO_TEST_PROVIDER_EGRESS_BLOCKED";
const STATE_SYMBOL = Symbol.for("gis-ai-go.qual-206-provider-egress-guard");
const guardedApiInvocations = [];
Object.defineProperty(globalThis, STATE_SYMBOL, {
  configurable: false,
  enumerable: false,
  writable: false,
  value: Object.freeze({
    snapshot: () => Object.freeze([...guardedApiInvocations]),
  }),
});

function writeAudit(value) {
  try {
    fstatSync(3);
    writeSync(3, `${JSON.stringify(value)}\n`, undefined, "utf8");
  } catch {
    // The negative-control probe intentionally has no private audit pipe.
  }
}

function blocked(api) {
  return function providerEgressBlocked() {
    guardedApiInvocations.push(api);
    writeAudit(Object.freeze({
      schema: "gis-ai-go.qual-206-provider-egress-guard.v1",
      event: "provider-egress-guard-blocked",
      api,
      ordinal: guardedApiInvocations.length,
    }));
    const error = new Error(`${ERROR_CODE}: ${api}`);
    Object.defineProperty(error, "code", { value: ERROR_CODE });
    throw error;
  };
}

dns.Resolver.prototype.resolve4 = blocked("dns.Resolver.resolve4");
dns.Resolver.prototype.resolve6 = blocked("dns.Resolver.resolve6");
https.request = blocked("https.request");
syncBuiltinESMExports();

writeAudit(Object.freeze({
  schema: "gis-ai-go.qual-206-provider-egress-guard.v1",
  event: "provider-egress-guard-ready",
  guarded_apis: GUARDED_APIS,
}));

process.once("exit", () => {
  writeAudit(Object.freeze({
    schema: "gis-ai-go.qual-206-provider-egress-guard.v1",
    event: "provider-egress-guard-summary",
    guarded_apis: GUARDED_APIS,
    guarded_api_invocation_count: guardedApiInvocations.length,
  }));
});
