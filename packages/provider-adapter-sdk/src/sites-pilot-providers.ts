/** Experimental open-data Fetch adapters. No production admission or licence is implied. */
import { createHash } from "node:crypto";
import { parseStrictJson } from "./strict-json.js";

export type SitesPilotProvider = "os-names" | "os-open-data" | "ons-cpih" | "ons-geography";
export type SitesPilotProviderErrorCode = "invalid-input" | "credential-unavailable" | "admission-denied" |
  "cancelled" | "timeout" | "upstream-unavailable" | "rate-limited" | "redirect-refused" |
  "response-too-large" | "invalid-response" | "period-unavailable";
export class SitesPilotProviderError extends Error {
  public readonly code: SitesPilotProviderErrorCode;
  public readonly retryAfterSeconds: number | undefined;
  public constructor(code: SitesPilotProviderErrorCode, retryAfterSeconds?: number) {
    super(`The bounded open-data request could not be completed (${code}).`);
    this.name = "SitesPilotProviderError";
    this.code = code;
    this.retryAfterSeconds = retryAfterSeconds;
  }
}
export interface SitesPilotProviderOptions {
  fetch: typeof fetch;
  now?: () => number;
  osApiKey?: string;
  /** Durable quota admission must finish before each individual upstream request. */
  admit: (request: Readonly<{ provider: SitesPilotProvider; endpoint: string }>) => Promise<void>;
  requestTimeoutMs?: number;
  maxResponseBytes?: number;
}
export interface SitesPilotRequestObservation {
  endpoint: string;
  requested_at: string;
  completed_at: string;
  elapsed_ms: number;
  status: 200;
  response_bytes: number;
  body_sha256: string;
}
export interface SitesPilotProviderResult<T> {
  schema: "gis-ai-go.sites-pilot-provider-result.v1";
  provider: SitesPilotProvider;
  source_mode: "live-provider-response";
  retrieved_at: string;
  data: T;
  attribution: readonly string[];
  licence: "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/";
  requests: readonly SitesPilotRequestObservation[];
  upstream_request_count: number;
  boundary: { production_transport: false; independent_attestation: false; receipt_persistence: "not-established-by-adapter" };
}
export type SitesPilotOsLocalType = "City" | "Town" | "Village" | "Hamlet";
export interface SitesPilotOsNamesInput { query: string; maxResults?: number; localType?: SitesPilotOsLocalType }
export interface SitesPilotOsName {
  ID: string; NAMES_URI: string; NAME1: string; NAME2?: string; TYPE: string; LOCAL_TYPE: string;
  GEOMETRY_X: number; GEOMETRY_Y: number; COUNTY_UNITARY?: string; DISTRICT_BOROUGH?: string; COUNTRY: string;
}
export interface SitesPilotOsNamesData {
  crs: "EPSG:27700"; crs_basis: "fixed-os-open-names-source-contract"; coordinate_unit: "metre";
  candidates: readonly SitesPilotOsName[]; total_results: number;
  selection_required: true; interpretation: "Representative named-place points; not addresses or area boundaries.";
}
export type SitesPilotOpenProduct = "OpenNames" | "OpenUPRN" | "LIDS";
export interface SitesPilotOsOpenProductInput { product: SitesPilotOpenProduct }
export interface SitesPilotOsOpenProductData {
  id: SitesPilotOpenProduct; name: string; version: string; areas: readonly string[];
  formats: readonly { format: string; subformat?: string }[];
  source_url: string; downloads_metadata_url: string;
  interpretation: "Live product metadata only; no dataset download or observation query.";
}
export interface SitesPilotOnsCpihInput { periods: readonly string[] }
export interface SitesPilotOnsAreasInput { namePrefix: string; maxResults?: number }
export interface SitesPilotOnsAreasData {
  geography: "MSOA"; vintage: "2021-12"; coverage: "England and Wales";
  areas: readonly { MSOA21CD: string; MSOA21NM: string }[]; complete: boolean;
  selection_basis: "name-prefix-not-spatial-containment"; source_url: string;
}
export interface SitesPilotCpihObservation { period: string; value: string; source_date: string; update_date: string }
export interface SitesPilotOnsCpihData {
  cdid: "L522"; dataset_id: "MM23"; uri: string; title: string; unit: string; base_year: 2015;
  measure_kind: "index-not-inflation-percentage"; release_date: string; next_release: string;
  latest_period_at_retrieval: string; observations: readonly SitesPilotCpihObservation[];
  comparison: null | { from_period: string; to_period: string; difference_index_points: string;
    relative_change_percent: string | null; rounding: "half-away-from-zero-to-six-decimal-places";
    interpretation: "Calculated change between the selected index observations; not a separately published inflation rate." };
}
export interface SitesPilotProviders {
  fetchOsNames(input: SitesPilotOsNamesInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOsNamesData>>;
  fetchOnsCpih(input: SitesPilotOnsCpihInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOnsCpihData>>;
  fetchOsOpenProduct(input: SitesPilotOsOpenProductInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOsOpenProductData>>;
  fetchOnsAreas(input: SitesPilotOnsAreasInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOnsAreasData>>;
}

const OGL = "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" as const;
const ONS_ORIGIN = "https://api.beta.ons.gov.uk";
const CPIH_URI = "/economy/inflationandpriceindices/timeseries/l522/mm23";
const CPIH_TITLE = "CPIH INDEX 00: ALL ITEMS 2015=100";
const CPIH_UNIT = "Index, base year = 100";
const MSOA_TABLE = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services/MSOA_DEC_2021_EW_NC_v3/FeatureServer/0";
const PERIOD = /^[0-9]{4}-(?:0[1-9]|1[0-2])$/u;
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const ROW_FIELDS = ["date", "value", "label", "year", "month", "quarter", "sourceDataset", "updateDate"].sort();
const fail = (code: SitesPilotProviderErrorCode = "invalid-response"): never => { throw new SitesPilotProviderError(code); };
const requireThat = (condition: unknown, code: SitesPilotProviderErrorCode = "invalid-response"): void => { if (!condition) fail(code); };
function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return fail();
  return value as Record<string, unknown>;
}
function boundedText(value: unknown, maximum = 200): string {
  if (typeof value !== "string" || value.length === 0 || value.length > maximum || /[\u0000-\u001f\u007f]/u.test(value)) return fail();
  return value;
}
function timestamp(value: unknown): string {
  const result = boundedText(value, 40);
  requireThat(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})$/u.test(result) && Number.isFinite(Date.parse(result)));
  const year = Number(result.slice(0, 4)), month = Number(result.slice(5, 7)), day = Number(result.slice(8, 10));
  requireThat(year >= 1900 && month >= 1 && month <= 12 && day >= 1 && day <= new Date(Date.UTC(year, month, 0)).getUTCDate());
  return result;
}
function inputObject(input: unknown, fields: readonly string[]): Record<string, unknown> {
  if (input === null || typeof input !== "object" || Array.isArray(input)) return fail("invalid-input");
  const value = input as Record<string, unknown>;
  requireThat(Object.keys(value).every((key) => fields.includes(key)), "invalid-input");
  return value;
}
function unsignedDecimal(value: unknown): string {
  if (typeof value !== "string" || !/^(?:0|[1-9][0-9]{0,14})(?:\.[0-9]{1,10})?$/u.test(value)) return fail();
  return value;
}
function decimalInteger(value: string): bigint {
  const [whole, fraction = ""] = value.split(".");
  return BigInt(whole!) * 10_000_000_000n + BigInt(fraction.padEnd(10, "0"));
}
function decimalString(integer: bigint, digits: number): string {
  const negative = integer < 0n;
  const value = (negative ? -integer : integer).toString().padStart(digits + 1, "0");
  const fractional = value.slice(-digits).replace(/0+$/u, "");
  return `${negative ? "-" : ""}${value.slice(0, -digits)}${fractional ? `.${fractional}` : ""}`;
}
function compareCpih(rows: readonly SitesPilotCpihObservation[]): SitesPilotOnsCpihData["comparison"] {
  if (rows.length !== 2) return null;
  const [from, to] = rows as [SitesPilotCpihObservation, SitesPilotCpihObservation];
  const first = decimalInteger(from.value), difference = decimalInteger(to.value) - first;
  const scaled = difference * 100_000_000n;
  const absolute = scaled < 0n ? -scaled : scaled;
  const rounded = first === 0n ? null : (absolute / first + (absolute % first * 2n >= first ? 1n : 0n)) * (scaled < 0n ? -1n : 1n);
  return { from_period: from.period, to_period: to.period, difference_index_points: decimalString(difference, 10),
    relative_change_percent: rounded === null ? null : decimalString(rounded, 6), rounding: "half-away-from-zero-to-six-decimal-places",
    interpretation: "Calculated change between the selected index observations; not a separately published inflation rate." };
}

/** A separate bounded pilot; caller supplies credentials and durable aggregate quota enforcement. */
export function createSitesPilotProviders(options: SitesPilotProviderOptions): SitesPilotProviders {
  const fetcher = options.fetch, admit = options.admit, now = options.now ?? Date.now, key = options.osApiKey;
  const timeoutMs = options.requestTimeoutMs ?? 10_000, maxBytes = options.maxResponseBytes ?? 1_048_576;
  requireThat(typeof fetcher === "function" && typeof admit === "function" && typeof now === "function", "invalid-input");
  requireThat(Number.isInteger(timeoutMs) && timeoutMs >= 1 && timeoutMs <= 10_000 &&
    Number.isInteger(maxBytes) && maxBytes >= 1 && maxBytes <= 1_048_576, "invalid-input");
  requireThat(key === undefined || (typeof key === "string" && /^[A-Za-z0-9_-]{8,256}$/u.test(key)), "invalid-input");
  const instant = (): number => {
    const value = now();
    requireThat(Number.isFinite(value) && value >= 0 && value <= 8_640_000_000_000_000, "invalid-input");
    return value;
  };
  async function getJson(provider: SitesPilotProvider, url: URL, signal?: AbortSignal): Promise<{ value: unknown; observation: SitesPilotRequestObservation }> {
    if (signal?.aborted) return fail("cancelled");
    // The endpoint contains no credential or caller query; suitable for quota classification.
    const endpoint = `${url.origin}${url.pathname}`;
    try { await admit(Object.freeze({ provider, endpoint })); } catch { return fail("admission-denied"); }
    if (signal?.aborted) return fail("cancelled");
    const started = instant(), controller = new AbortController();
    let timedOut = false;
    let reader: ReadableStreamDefaultReader<Uint8Array> | undefined;
    let received: Response | undefined;
    let rejectAbort: ((error: SitesPilotProviderError) => void) | undefined;
    const aborted = new Promise<never>((_, reject) => { rejectAbort = reject; });
    const abort = (): void => {
      controller.abort();
      rejectAbort!(new SitesPilotProviderError(timedOut ? "timeout" : "cancelled"));
      if (reader) void reader.cancel().catch(() => undefined);
    };
    signal?.addEventListener("abort", abort, { once: true });
    const timer = setTimeout(() => { timedOut = true; abort(); }, timeoutMs);
    try {
      const headers = new Headers({ Accept: "application/json", "User-Agent": "GIS-AI-GO-Sites-Pilot/0.1 (+https://github.com/chris-page-gov/gis-ai-go)" });
      if (provider === "os-names") headers.set("key", key!);
      // Workers supports manual/follow; manual exposes redirects for the refusal below without following them.
      const pending = fetcher(url.toString(), { method: "GET", headers, redirect: "manual", credentials: "omit", cache: "no-store", signal: controller.signal });
      // Even a misbehaving injected transport cannot leave a late body intentionally unread.
      void pending.then((response) => { if (controller.signal.aborted) void response.body?.cancel().catch(() => undefined); }, () => undefined);
      const response = await Promise.race([pending, aborted]);
      received = response;
      requireThat(!response.redirected && !(response.status >= 300 && response.status < 400) && (!response.url || response.url === url.toString()), "redirect-refused");
      if (response.status === 429) {
        const retry = response.headers.get("retry-after");
        const seconds = retry !== null && /^\d{1,4}$/u.test(retry) && Number(retry) <= 3600 ? Number(retry) : undefined;
        void response.body?.cancel().catch(() => undefined);
        throw new SitesPilotProviderError("rate-limited", seconds);
      }
      if (response.status !== 200) { void response.body?.cancel().catch(() => undefined); return fail("upstream-unavailable"); }
      requireThat(/^application\/(?:json|geo\+json)(?:\s*;|$)/iu.test(response.headers.get("content-type") ?? ""));
      const declared = response.headers.get("content-length");
      if (declared !== null) {
        requireThat(/^\d+$/u.test(declared));
        requireThat(Number(declared) <= maxBytes, "response-too-large");
      }
      requireThat(response.body !== null);
      reader = response.body!.getReader();
      const chunks: Uint8Array[] = [];
      let count = 0;
      while (true) {
        const item = await Promise.race([reader.read(), aborted]);
        if (item.done) break;
        count += item.value.byteLength;
        requireThat(count <= maxBytes, "response-too-large");
        chunks.push(item.value);
      }
      const bytes = new Uint8Array(count);
      let offset = 0;
      for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
      let value: unknown;
      try { value = parseStrictJson(new TextDecoder("utf-8", { fatal: true }).decode(bytes)); } catch { return fail("invalid-response"); }
      const completed = instant();
      requireThat(completed >= started, "invalid-response");
      return { value, observation: { endpoint, requested_at: new Date(started).toISOString(), completed_at: new Date(completed).toISOString(),
        elapsed_ms: completed - started, status: 200, response_bytes: count, body_sha256: createHash("sha256").update(bytes).digest("hex") } };
    } catch (error) {
      if (error instanceof SitesPilotProviderError) throw error;
      if (controller.signal.aborted) return fail(timedOut ? "timeout" : "cancelled");
      return fail("upstream-unavailable");
    } finally {
      clearTimeout(timer);
      signal?.removeEventListener("abort", abort);
      if (reader) { void reader.cancel().catch(() => undefined); }
      else { void received?.body?.cancel().catch(() => undefined); }
    }
  }
  function result<T>(provider: SitesPilotProvider, data: T, requests: readonly SitesPilotRequestObservation[], attribution: readonly string[]): SitesPilotProviderResult<T> {
    // An untrusted provider may reflect request material into otherwise valid text fields.
    requireThat(key === undefined || !JSON.stringify(data).includes(key));
    return { schema: "gis-ai-go.sites-pilot-provider-result.v1", provider, source_mode: "live-provider-response",
      retrieved_at: requests.at(-1)!.completed_at, data, attribution, licence: OGL, requests, upstream_request_count: requests.length,
      boundary: { production_transport: false, independent_attestation: false, receipt_persistence: "not-established-by-adapter" } };
  }
  const osAttribution = (retrieved: string): readonly string[] => {
    const year = retrieved.slice(0, 4);
    return [`Contains OS data © Crown copyright and database rights ${year}.`, `Contains Royal Mail data © Royal Mail copyright and database right ${year}.`,
      `Contains National Statistics data © Crown copyright and database right ${year}.`];
  };
  return Object.freeze({
    async fetchOnsAreas(input: SitesPilotOnsAreasInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOnsAreasData>> {
      const params = inputObject(input, ["namePrefix", "maxResults"]), prefix = params.namePrefix, maximum = params.maxResults ?? 5;
      requireThat(typeof prefix === "string" && prefix.length >= 2 && prefix.length <= 60 && prefix === prefix.trim() && /^[\p{L}\p{M}\p{N} .'’()-]+$/u.test(prefix), "invalid-input");
      requireThat(Number.isInteger(maximum) && Number(maximum) >= 1 && Number(maximum) <= 5, "invalid-input");
      // A fixed field/operator and escaped SQL literal; callers cannot submit predicates or wildcards.
      const url = new URL(`${MSOA_TABLE}/query`);
      url.searchParams.set("f", "json"); url.searchParams.set("where", `MSOA21NM LIKE '${(prefix as string).replace(/'/gu, "''")}%'`);
      url.searchParams.set("outFields", "MSOA21CD,MSOA21NM"); url.searchParams.set("returnGeometry", "false");
      url.searchParams.set("resultRecordCount", String(maximum)); url.searchParams.set("orderByFields", "MSOA21CD");
      const response = await getJson("ons-geography", url, signal), body = object(response.value);
      requireThat(body.error === undefined && Array.isArray(body.fields) && body.fields.length === 2 &&
        Array.isArray(body.features) && body.features.length <= Number(maximum) &&
        (body.exceededTransferLimit === undefined || typeof body.exceededTransferLimit === "boolean"));
      const fields = (body.fields as unknown[]).map((raw) => { const field = object(raw); requireThat(field.type === "esriFieldTypeString"); return field.name; });
      requireThat(new Set(fields).size === 2 && fields.includes("MSOA21CD") && fields.includes("MSOA21NM"));
      const seen = new Set<string>();
      const areas = (body.features as unknown[]).map((raw) => {
        const feature = object(raw), attributes = object(feature.attributes);
        requireThat(Object.keys(feature).length === 1 && Object.keys(attributes).length === 2);
        const code = boundedText(attributes.MSOA21CD, 9), name = boundedText(attributes.MSOA21NM, 150);
        requireThat(/^[EW]020[0-9]{5}$/u.test(code) && !seen.has(code) && name.toLocaleLowerCase("en-GB").startsWith((prefix as string).toLocaleLowerCase("en-GB")));
        seen.add(code); return { MSOA21CD: code, MSOA21NM: name };
      });
      return result("ons-geography", { geography: "MSOA", vintage: "2021-12", coverage: "England and Wales", areas,
        complete: body.exceededTransferLimit !== true, selection_basis: "name-prefix-not-spatial-containment", source_url: MSOA_TABLE }, [response.observation],
      ["Source: Office for National Statistics licensed under the Open Government Licence v.3.0."]);
    },
    async fetchOsNames(input: SitesPilotOsNamesInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOsNamesData>> {
      const params = inputObject(input, ["query", "maxResults", "localType"]);
      const query = params.query, maxResults = params.maxResults ?? 5, localType = params.localType;
      requireThat(typeof query === "string" && query.length >= 2 && query.length <= 80 && query === query.trim() &&
        /^[\p{L}\p{M}\p{N} .,'’()\/-]+$/u.test(query), "invalid-input");
      requireThat(Number.isInteger(maxResults) && Number(maxResults) >= 1 && Number(maxResults) <= 5, "invalid-input");
      requireThat(localType === undefined || ["City", "Town", "Village", "Hamlet"].includes(String(localType)), "invalid-input");
      if (!key) return fail("credential-unavailable");
      const url = new URL("https://api.os.uk/search/names/v1/find");
      url.searchParams.set("query", query as string); url.searchParams.set("maxresults", String(maxResults)); url.searchParams.set("format", "JSON");
      if (localType !== undefined) url.searchParams.set("fq", `LOCAL_TYPE:${localType}`);
      const response = await getJson("os-names", url, signal), body = object(response.value), header = object(body.header);
      requireThat(header.query === query && Number.isInteger(header.totalresults) && Number(header.totalresults) >= 0 &&
        (header.format === "JSON" || header.format === "json") && header.maxresults === maxResults && header.offset === 0 && Array.isArray(body.results) && body.results.length <= Number(maxResults));
      const seen = new Set<string>();
      const candidates = (body.results as unknown[]).map((raw) => {
        const entry = object(object(raw).GAZETTEER_ENTRY), id = boundedText(entry.ID, 64), uri = boundedText(entry.NAMES_URI, 150);
        requireThat(/^[A-Za-z0-9._-]{1,64}$/u.test(id) && /^https?:\/\/data\.ordnancesurvey\.co\.uk\/id\/[A-Za-z0-9._~-]+(?:\/[A-Za-z0-9._~-]+)*$/u.test(uri) && !seen.has(id));
        seen.add(id);
        requireThat(typeof entry.GEOMETRY_X === "number" && Number.isFinite(entry.GEOMETRY_X) && entry.GEOMETRY_X >= 0 && entry.GEOMETRY_X <= 700_000 &&
          typeof entry.GEOMETRY_Y === "number" && Number.isFinite(entry.GEOMETRY_Y) && entry.GEOMETRY_Y >= 0 && entry.GEOMETRY_Y <= 1_300_000);
        const actualType = boundedText(entry.LOCAL_TYPE, 80);
        requireThat(localType === undefined || actualType === localType);
        return { ID: id, NAMES_URI: uri, NAME1: boundedText(entry.NAME1), TYPE: boundedText(entry.TYPE, 80), LOCAL_TYPE: actualType,
          GEOMETRY_X: entry.GEOMETRY_X as number, GEOMETRY_Y: entry.GEOMETRY_Y as number, COUNTRY: boundedText(entry.COUNTRY, 80),
          ...(entry.NAME2 === undefined ? {} : { NAME2: boundedText(entry.NAME2) }),
          ...(entry.COUNTY_UNITARY === undefined ? {} : { COUNTY_UNITARY: boundedText(entry.COUNTY_UNITARY) }),
          ...(entry.DISTRICT_BOROUGH === undefined ? {} : { DISTRICT_BOROUGH: boundedText(entry.DISTRICT_BOROUGH) }) };
      });
      requireThat(Number(header.totalresults) >= candidates.length);
      // Names /find has no output CRS parameter or response CRS field. British National Grid metres
      // come from the fixed source contract, not a per-response declaration or range inference:
      // https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-technical-specification
      return result("os-names", { crs: "EPSG:27700", crs_basis: "fixed-os-open-names-source-contract", coordinate_unit: "metre",
        candidates, total_results: Number(header.totalresults), selection_required: true,
        interpretation: "Representative named-place points; not addresses or area boundaries." }, [response.observation], osAttribution(response.observation.completed_at));
    },
    async fetchOsOpenProduct(input: SitesPilotOsOpenProductInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOsOpenProductData>> {
      const params = inputObject(input, ["product"]), product = params.product;
      requireThat(typeof product === "string" && ["OpenNames", "OpenUPRN", "LIDS"].includes(product), "invalid-input");
      const url = new URL(`https://api.os.uk/downloads/v1/products/${product}`);
      const response = await getJson("os-open-data", url, signal), body = object(response.value);
      requireThat(body.id === product && body.url === url.toString() && body.downloadsUrl === `${url}/downloads`);
      requireThat(Array.isArray(body.areas) && body.areas.length > 0 && body.areas.length <= 100 && Array.isArray(body.formats) && body.formats.length > 0 && body.formats.length <= 12);
      const areas = (body.areas as unknown[]).map((area) => { const value = boundedText(area, 2); requireThat(/^[A-Z]{2}$/u.test(value)); return value; });
      const formats = (body.formats as unknown[]).map((item) => { const format = object(item); return { format: boundedText(format.format, 40),
        ...(format.subformat === undefined ? {} : { subformat: boundedText(format.subformat, 40) }) }; });
      const version = boundedText(body.version, 40); requireThat(/^[A-Za-z0-9._-]+$/u.test(version));
      return result("os-open-data", { id: product as SitesPilotOpenProduct, name: boundedText(body.name, 120), version, areas, formats,
        source_url: url.toString(), downloads_metadata_url: `${url}/downloads`, interpretation: "Live product metadata only; no dataset download or observation query." },
      [response.observation], [osAttribution(response.observation.completed_at)[0]!]);
    },
    async fetchOnsCpih(input: SitesPilotOnsCpihInput, signal?: AbortSignal): Promise<SitesPilotProviderResult<SitesPilotOnsCpihData>> {
      const params = inputObject(input, ["periods"]), periods = params.periods;
      requireThat(Array.isArray(periods) && periods.length >= 1 && periods.length <= 2 && periods.every((period) => typeof period === "string" && PERIOD.test(period)) && new Set(periods).size === periods.length, "invalid-input");
      const wanted = [...periods as string[]];
      const searchUrl = new URL(`${ONS_ORIGIN}/v1/search?content_type=timeseries&cdids=L522`);
      const searchResponse = await getJson("ons-cpih", searchUrl, signal), search = object(searchResponse.value);
      requireThat(search.count === 1 && Array.isArray(search.items) && search.items.length === 1);
      const item = object((search.items as unknown[])[0]);
      requireThat(item.cdid === "L522" && item.dataset_id === "MM23" && item.type === "timeseries" && item.uri === CPIH_URI && item.title === CPIH_TITLE);
      const searchRelease = timestamp(item.release_date);
      const dataUrl = new URL(`${ONS_ORIGIN}/v1/data`); dataUrl.searchParams.set("uri", CPIH_URI);
      const dataResponse = await getJson("ons-cpih", dataUrl, signal), data = object(dataResponse.value), description = object(data.description);
      requireThat(data.type === "timeseries" && data.uri === CPIH_URI && description.cdid === "L522" && description.datasetId === "MM23" && description.title === CPIH_TITLE && description.unit === CPIH_UNIT);
      const release = timestamp(description.releaseDate), retrieved = dataResponse.observation.completed_at;
      requireThat(release === searchRelease && Date.parse(release) <= Date.parse(retrieved));
      const releaseMonth = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", year: "numeric", month: "2-digit" }).format(new Date(release)).split("/").reverse().join("-");
      const nextRelease = boundedText(description.nextRelease, 80);
      requireThat(Array.isArray(data.months) && data.months.length > 0 && data.months.length <= 2000);
      const byPeriod = new Map<string, SitesPilotCpihObservation>();
      for (const raw of data.months as unknown[]) {
        const row = object(raw);
        requireThat(JSON.stringify(Object.keys(row).sort()) === JSON.stringify(ROW_FIELDS) && row.sourceDataset === "MM23" && row.quarter === "");
        const sourceDate = boundedText(row.date, 8);
        requireThat(/^[0-9]{4} [A-Z]{3}$/u.test(sourceDate));
        const [year, abbreviation] = sourceDate.split(" "), month = MONTHS.findIndex((name) => name.slice(0, 3).toUpperCase() === abbreviation);
        requireThat(month >= 0 && row.year === year && row.label === sourceDate && row.month === MONTHS[month]);
        const period = `${year}-${String(month + 1).padStart(2, "0")}`, updated = timestamp(row.updateDate);
        requireThat(!byPeriod.has(period) && period <= retrieved.slice(0, 7) && period <= releaseMonth && Date.parse(updated) <= Date.parse(release));
        byPeriod.set(period, { period, value: unsignedDecimal(row.value), source_date: sourceDate, update_date: updated });
      }
      const latestPeriod = [...byPeriod.keys()].sort().at(-1)!, latest = byPeriod.get(latestPeriod)!;
      requireThat(description.date === latest.source_date && description.number === latest.value);
      const observations = wanted.map((period) => byPeriod.get(period) ?? fail("period-unavailable"));
      return result("ons-cpih", { cdid: "L522", dataset_id: "MM23", uri: CPIH_URI, title: CPIH_TITLE, unit: CPIH_UNIT, base_year: 2015,
        measure_kind: "index-not-inflation-percentage", release_date: release, next_release: nextRelease, latest_period_at_retrieval: latestPeriod,
        observations, comparison: compareCpih(observations) }, [searchResponse.observation, dataResponse.observation],
      ["Source: Office for National Statistics licensed under the Open Government Licence v.3.0."]);
    },
  });
}
