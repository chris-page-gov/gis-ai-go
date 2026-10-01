import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { createSitesPilotProviders, SitesPilotProviderError, type SitesPilotProviderOptions, type SitesPilotProviderErrorCode } from "../src/sites-pilot-providers.js";

const NOW = Date.parse("2026-10-01T12:00:00Z");
const KEY = "synthetic-os-key-not-a-credential";
const fixture = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8")) as { search: unknown; data: unknown };
const clone = <T>(value: T): T => JSON.parse(JSON.stringify(value)) as T;
const json = (value: unknown, init: ResponseInit = {}): Response => new Response(JSON.stringify(value), { ...init, headers: { "content-type": "application/json", ...init.headers } });
const names = () => ({ header: { query: "Warwick", format: "JSON", maxresults: 5, offset: 0, totalresults: 1 }, results: [{ GAZETTEER_ENTRY: {
  ID: "osgb4000000074555874", NAMES_URI: "http://data.ordnancesurvey.co.uk/id/4000000074555874", NAME1: "Warwick", TYPE: "populatedPlace", LOCAL_TYPE: "Town",
  GEOMETRY_X: 428119, GEOMETRY_Y: 265114, COUNTRY: "England", COUNTY_UNITARY: "Warwickshire",
} }] });
const product = () => ({ id: "OpenNames", name: "OS Open Names", version: "2026-07", areas: ["GB"], formats: [{ format: "CSV" }],
  url: "https://api.os.uk/downloads/v1/products/OpenNames", downloadsUrl: "https://api.os.uk/downloads/v1/products/OpenNames/downloads" });
const areas = () => ({ fields: [{ name: "MSOA21CD", type: "esriFieldTypeString" }, { name: "MSOA21NM", type: "esriFieldTypeString" }],
  exceededTransferLimit: true, features: [{ attributes: { MSOA21CD: "E02006519", MSOA21NM: "Warwick 001" } }] });
function options(fetcher: typeof fetch, extra: Partial<SitesPilotProviderOptions> = {}): SitesPilotProviderOptions {
  return { fetch: fetcher, now: () => NOW, admit: async () => undefined, ...extra };
}
async function rejects(promise: Promise<unknown>, code: SitesPilotProviderErrorCode): Promise<void> {
  await assert.rejects(promise, (error: unknown) => error instanceof SitesPilotProviderError && error.code === code && !error.message.includes(KEY));
}

test("ONS area names preserve native codes, date and incomplete page without claiming spatial containment", async () => {
  const api = createSitesPilotProviders(options(async (value, init) => {
    const url = new URL(String(value)); assert.equal(url.origin, "https://services1.arcgis.com");
    assert.equal(url.searchParams.get("where"), "MSOA21NM LIKE 'Warwick%'"); assert.equal(url.searchParams.get("resultRecordCount"), "5");
    assert.equal(url.searchParams.get("returnGeometry"), "false"); assert.equal(new Headers(init?.headers).get("key"), null); return json(areas());
  }, { osApiKey: KEY, admit: async ({ provider }) => { assert.equal(provider, "ons-geography"); } }));
  const output = await api.fetchOnsAreas({ namePrefix: "Warwick" });
  assert.equal(output.data.complete, false); assert.equal(output.data.vintage, "2021-12");
  assert.equal(output.data.selection_basis, "name-prefix-not-spatial-containment"); assert.deepEqual(output.data.areas, [{ MSOA21CD: "E02006519", MSOA21NM: "Warwick 001" }]);
});

test("ONS names escape apostrophes while predicates, wildcards and excessive limits never reach admission", async () => {
  let calls = 0;
  const api = createSitesPilotProviders(options(async (value) => { calls++; assert.equal(new URL(String(value)).searchParams.get("where"), "MSOA21NM LIKE 'King''s%'");
    return json({ ...areas(), exceededTransferLimit: false, features: [] }); }));
  assert.equal((await api.fetchOnsAreas({ namePrefix: "King's" })).data.complete, true);
  for (const namePrefix of ["x' OR 1=1 --", "Warwick%", "Warwick_", "Warwick;", "x\nDROP", "x".repeat(61)]) await rejects(api.fetchOnsAreas({ namePrefix }), "invalid-input");
  await rejects(api.fetchOnsAreas({ namePrefix: "Warwick", maxResults: 6 }), "invalid-input"); assert.equal(calls, 1);
});

test("ONS names reject duplicate or invalid GSS codes, changed fields and HTTP200 ArcGIS errors", async () => {
  const duplicate = areas(); duplicate.features.push(duplicate.features[0]!);
  const invalid = areas(); invalid.features[0]!.attributes.MSOA21CD = "S02000001";
  const wrongField = areas(); wrongField.fields[0]!.name = "LSOA21CD";
  const wrongName = areas(); wrongName.features[0]!.attributes.MSOA21NM = "Elsewhere 001";
  for (const body of [duplicate, invalid, wrongField, wrongName, { error: { code: 400, message: KEY } }]) {
    await rejects(createSitesPilotProviders(options(async () => json(body))).fetchOnsAreas({ namePrefix: "Warwick" }), "invalid-response");
  }
});

test("OS Names admits before fetch, sends server-side key and returns bounded native evidence", async () => {
  const order: string[] = [];
  const api = createSitesPilotProviders(options(async (url, init) => {
    order.push("fetch"); assert.equal(String(url), "https://api.os.uk/search/names/v1/find?query=Warwick&maxresults=5&format=JSON&fq=LOCAL_TYPE%3ATown");
    assert.equal(new Headers(init?.headers).get("key"), KEY); assert.equal(init?.redirect, "error"); assert.equal(init?.credentials, "omit");
    return json(names());
  }, { osApiKey: KEY, admit: async (request) => { await Promise.resolve(); order.push("admit"); assert.deepEqual(request, { provider: "os-names", endpoint: "https://api.os.uk/search/names/v1/find" }); } }));
  const output = await api.fetchOsNames({ query: "Warwick", localType: "Town" });
  assert.deepEqual(order, ["admit", "fetch"]); assert.equal(output.data.candidates[0]?.GEOMETRY_X, 428119);
  assert.equal(output.data.crs, "EPSG:27700"); assert.equal(output.data.crs_basis, "fixed-os-open-names-source-contract");
  assert.equal(output.data.coordinate_unit, "metre");
  assert.equal(output.source_mode, "live-provider-response"); assert.equal(output.upstream_request_count, 1);
  assert.match(output.requests[0]!.body_sha256, /^[a-f0-9]{64}$/u); assert.equal(JSON.stringify(output).includes(KEY), false);
  assert.equal(output.boundary.receipt_persistence, "not-established-by-adapter");
});

test("OS Names accepts the observed lowercase JSON format label but refuses another format", async () => {
  const body = names(); body.header.format = "json";
  const api = createSitesPilotProviders(options(async () => json(body), { osApiKey: KEY }));
  assert.equal((await api.fetchOsNames({ query: "Warwick" })).data.candidates.length, 1);
  body.header.format = "xml";
  await rejects(api.fetchOsNames({ query: "Warwick" }), "invalid-response");
});

test("missing key, malformed query and excessive requested results consume no admission or fetch", async () => {
  let called = 0;
  const api = createSitesPilotProviders(options(async () => { called++; return json(names()); }, { admit: async () => { called++; } }));
  await rejects(api.fetchOsNames({ query: "Warwick" }), "credential-unavailable");
  for (const query of ["", "a", " Warwick", "x".repeat(81), "https://elsewhere/?key=secret", "Warwick\nInjected"]) await rejects(api.fetchOsNames({ query }), "invalid-input");
  await rejects(api.fetchOsNames({ query: "Warwick", maxResults: 6 }), "invalid-input");
  assert.equal(called, 0);
});

test("OS Names rejects returned identity links, inconsistent selection, duplicate IDs and invalid geometry", async () => {
  const mutations = [
    (value: ReturnType<typeof names>) => { value.results[0]!.GAZETTEER_ENTRY.NAMES_URI = "https://evil.example/id/1"; },
    (value: ReturnType<typeof names>) => { value.results[0]!.GAZETTEER_ENTRY.LOCAL_TYPE = "Railway_Station"; },
    (value: ReturnType<typeof names>) => { value.results[0]!.GAZETTEER_ENTRY.GEOMETRY_X = -1; },
    (value: ReturnType<typeof names>) => { value.results.push(value.results[0]!); },
    (value: ReturnType<typeof names>) => { value.header.query = "Wrong place"; },
    (value: ReturnType<typeof names>) => { value.results[0]!.GAZETTEER_ENTRY.NAME1 = KEY; },
  ];
  for (const mutate of mutations) { const body = names(); mutate(body); const api = createSitesPilotProviders(options(async () => json(body), { osApiKey: KEY }));
    await rejects(api.fetchOsNames({ query: "Warwick", localType: "Town" }), "invalid-response"); }
});

test("keyless OS product fetch projects only fixed metadata URLs and never forwards the configured key", async () => {
  const body = { ...product(), hostile: { key: KEY, url: "https://untrusted.example" } };
  const api = createSitesPilotProviders(options(async (url, init) => { assert.equal(String(url), product().url); assert.equal(new Headers(init?.headers).get("key"), null); return json(body); }, { osApiKey: KEY }));
  const output = await api.fetchOsOpenProduct({ product: "OpenNames" });
  assert.equal(output.data.version, "2026-07"); assert.equal(JSON.stringify(output).includes("untrusted"), false); assert.equal(JSON.stringify(output).includes(KEY), false);
  await rejects(api.fetchOsOpenProduct({ product: "Premium" as "OpenNames" }), "invalid-input");
});

test("OpenData metadata rejects source identity and download URL substitution", async () => {
  for (const body of [{ ...product(), id: "Other" }, { ...product(), downloadsUrl: "https://evil.example" }, { ...product(), areas: [] }]) {
    await rejects(createSitesPilotProviders(options(async () => json(body))).fetchOsOpenProduct({ product: "OpenNames" }), "invalid-response");
  }
});

test("CPIH independently admits two exact calls, validates full monthly material and calculates exact change", async () => {
  const urls: string[] = [], admitted: string[] = [];
  const api = createSitesPilotProviders(options(async (url, init) => { urls.push(String(url)); assert.equal(new Headers(init?.headers).get("key"), null); return json(urls.length === 1 ? fixture.search : fixture.data); },
    { osApiKey: KEY, admit: async (request) => { admitted.push(request.endpoint); } }));
  const output = await api.fetchOnsCpih({ periods: ["2026-01", "2026-07"] });
  assert.deepEqual(urls, ["https://api.beta.ons.gov.uk/v1/search?content_type=timeseries&cdids=L522", "https://api.beta.ons.gov.uk/v1/data?uri=%2Feconomy%2Finflationandpriceindices%2Ftimeseries%2Fl522%2Fmm23"]);
  assert.equal(admitted.length, 2); assert.equal(output.upstream_request_count, 2); assert.equal(output.data.latest_period_at_retrieval, "2026-07");
  assert.equal(output.data.comparison?.difference_index_points, "3.3"); assert.equal(output.data.comparison?.relative_change_percent, "2.367288");
  assert.deepEqual(output.data.observations.map((row) => row.value), ["139.4", "142.7"]);
});

test("CPIH reverse comparison, zero denominator and absent period preserve their meanings", async () => {
  const run = (data: unknown, periods: string[]) => { let calls = 0; return createSitesPilotProviders(options(async () => json(++calls === 1 ? fixture.search : data))).fetchOnsCpih({ periods }); };
  assert.equal((await run(fixture.data, ["2026-07", "2026-01"])).data.comparison?.difference_index_points, "-3.3");
  const zero = clone(fixture.data) as { months: { value: string }[] }; zero.months[0]!.value = "0";
  assert.equal((await run(zero, ["2026-01", "2026-07"])).data.comparison?.relative_change_percent, null);
  await rejects(run(fixture.data, ["2025-01"]), "period-unavailable");
});

test("CPIH search identity is checked before a second request or admission", async () => {
  let calls = 0, admissions = 0;
  const search = clone(fixture.search) as { items: { uri: string }[] }; search.items[0]!.uri = "https://evil.example/";
  const api = createSitesPilotProviders(options(async () => { calls++; return json(search); }, { admit: async () => { admissions++; } }));
  await rejects(api.fetchOnsCpih({ periods: ["2026-07"] }), "invalid-response"); assert.equal(calls, 1); assert.equal(admissions, 1);
});

test("CPIH rejects drift, duplicate periods, suppression, future updates and headline mismatch", async () => {
  type Data = { description: Record<string, unknown>; months: Record<string, unknown>[] };
  const mutations = [
    (d: Data) => { d.description.releaseDate = "2026-09-01T00:00:00Z"; },
    (d: Data) => { d.months.push(d.months[0]!); },
    (d: Data) => { d.months[0]!.suppression = "missing"; },
    (d: Data) => { d.months[0]!.value = ".."; },
    (d: Data) => { d.months[0]!.updateDate = "2026-12-01T00:00:00Z"; },
    (d: Data) => { d.months[0]!.updateDate = "2026-02-30T00:00:00Z"; },
    (d: Data) => { d.description.number = "999"; },
    (d: Data) => { d.description.unit = "Percent"; },
  ];
  for (const mutate of mutations) { const data = clone(fixture.data) as Data; mutate(data); let calls = 0;
    await rejects(createSitesPilotProviders(options(async () => json(++calls === 1 ? fixture.search : data))).fetchOnsCpih({ periods: ["2026-07"] }), "invalid-response"); }
});

test("CPIH input is bounded before provider admission", async () => {
  let admissions = 0;
  const api = createSitesPilotProviders(options(async () => { throw new Error("must not fetch"); }, { admit: async () => { admissions++; } }));
  for (const periods of [[], ["latest"], ["2026-13"], ["2026-01", "2026-01"], ["2026-01", "2026-02", "2026-03"]]) await rejects(api.fetchOnsCpih({ periods }), "invalid-input");
  assert.equal(admissions, 0);
});

test("admission denial blocks fetch and removes private failure details", async () => {
  let calls = 0;
  const api = createSitesPilotProviders(options(async () => { calls++; return json(product()); }, { admit: async () => { throw new Error(KEY); } }));
  await rejects(api.fetchOsOpenProduct({ product: "OpenNames" }), "admission-denied"); assert.equal(calls, 0);
});

test("redirects,429 and provider failure do not retry or expose bodies", async () => {
  for (const [status, code] of [[302, "redirect-refused"], [429, "rate-limited"], [503, "upstream-unavailable"]] as const) {
    let calls = 0;
    const api = createSitesPilotProviders(options(async () => { calls++; return new Response(KEY, { status, headers: { location: "https://evil.example", "retry-after": "60" } }); }));
    await rejects(api.fetchOsOpenProduct({ product: "OpenNames" }), code); assert.equal(calls, 1);
  }
  await rejects(createSitesPilotProviders(options(async () => { throw new TypeError(`Network failure ${KEY}`); })).fetchOsOpenProduct({ product: "OpenNames" }), "upstream-unavailable");
});

test("strict JSON, UTF-8, content type and byte ceilings are enforced", async () => {
  const responses = [
    new Response('{"id":"OpenNames","id":"Other"}', { headers: { "content-type": "application/json" } }),
    new Response(new Uint8Array([0xff]), { headers: { "content-type": "application/json" } }),
    new Response("<html>not data</html>", { headers: { "content-type": "text/html" } }),
  ];
  for (const response of responses) await rejects(createSitesPilotProviders(options(async () => response)).fetchOsOpenProduct({ product: "OpenNames" }), "invalid-response");
  for (const headers of [{}, { "content-length": "99999" }]) {
    await rejects(createSitesPilotProviders(options(async () => json(product(), { headers }), { maxResponseBytes: 16 })).fetchOsOpenProduct({ product: "OpenNames" }), "response-too-large");
  }
});

test("deadline bounds a never-resolving fetch and a stalled response body", async () => {
  const never: typeof fetch = async () => new Promise<Response>(() => undefined);
  await rejects(createSitesPilotProviders(options(never, { requestTimeoutMs: 5 })).fetchOsOpenProduct({ product: "OpenNames" }), "timeout");
  let cancelled = false;
  const body = new ReadableStream<Uint8Array>({ pull: () => new Promise<void>(() => undefined), cancel: () => { cancelled = true; } });
  await rejects(createSitesPilotProviders(options(async () => new Response(body, { headers: { "content-type": "application/json" } }), { requestTimeoutMs: 5 })).fetchOsOpenProduct({ product: "OpenNames" }), "timeout");
  assert.equal(cancelled, true);
});

test("caller cancellation before or during fetch consumes no extra upstream calls", async () => {
  const before = new AbortController(); before.abort(); let calls = 0;
  const api = createSitesPilotProviders(options(async () => { calls++; return new Promise<Response>(() => undefined); }, { requestTimeoutMs: 500 }));
  await rejects(api.fetchOsOpenProduct({ product: "OpenNames" }, before.signal), "cancelled"); assert.equal(calls, 0);
  const during = new AbortController(); const pending = api.fetchOsOpenProduct({ product: "OpenNames" }, during.signal);
  await Promise.resolve(); during.abort(); await rejects(pending, "cancelled"); assert.equal(calls, 1);
});
