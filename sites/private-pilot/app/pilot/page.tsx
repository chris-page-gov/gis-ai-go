'use client';

import { useEffect, useRef, useState, type FormEvent } from 'react';

type Operation = 'sites_os_names' | 'sites_os_open_product' | 'sites_ons_areas' | 'sites_ons_cpih' | 'sites_capabilities' | 'sites_evidence_inspect';
type JsonObject = Record<string, unknown>;
const ENDPOINT = '/pilot/mcp';
const PROTOCOL = '2025-11-25';
const operations: readonly { value: Operation; label: string }[] = [
  { value: 'sites_os_names', label: 'Find named places with OS' },
  { value: 'sites_ons_areas', label: 'Find ONS statistical-area names and codes' },
  { value: 'sites_ons_cpih', label: 'Read or compare CPIH index levels' },
  { value: 'sites_os_open_product', label: 'Check an OS open-data product' },
  { value: 'sites_capabilities', label: 'Check this pilot’s capabilities' },
  { value: 'sites_evidence_inspect', label: 'Inspect a saved receipt' },
];
function object(value: unknown): JsonObject | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value) ? value as JsonObject : null;
}
function text(value: unknown): string { return typeof value === 'string' || typeof value === 'number' ? String(value) : 'Not supplied'; }
function rows(value: unknown): JsonObject[] { return Array.isArray(value) ? value.map(object).filter((row): row is JsonObject => row !== null) : []; }
async function readJson(response: Response, signal: AbortSignal): Promise<JsonObject> {
  if (!response.headers.get('content-type')?.toLowerCase().startsWith('application/json')) throw new Error('The server did not return a JSON response.');
  const reader = response.body?.getReader();
  if (!reader) throw new Error('The server returned no result.');
  const chunks: Uint8Array[] = []; let size = 0;
  const cancel = () => { void reader.cancel().catch(() => undefined); };
  signal.addEventListener('abort', cancel, { once: true });
  try {
    for (;;) {
      signal.throwIfAborted(); const item = await reader.read(); signal.throwIfAborted();
      if (item.done) break;
      size += item.value.byteLength; if (size > 1_048_576) throw new Error('The result exceeded this pilot’s display limit.');
      chunks.push(item.value);
    }
    const bytes = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    const parsed: unknown = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes));
    const value = object(parsed); if (!value) throw new Error('The server returned an invalid result.');
    return value;
  } finally { signal.removeEventListener('abort', cancel); void reader.cancel().catch(() => undefined); }
}
async function post(body: JsonObject, signal: AbortSignal): Promise<JsonObject | null> {
  const response = await fetch(ENDPOINT, { method: 'POST', credentials: 'same-origin', redirect: 'error', cache: 'no-store', signal,
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream', 'mcp-protocol-version': PROTOCOL }, body: JSON.stringify(body) });
  if (response.status === 401) throw new Error('Sign in to this private Site to continue.');
  if (response.status === 403) throw new Error('This request is outside the Site’s admitted access boundary.');
  if (response.status === 429) throw new Error('The pilot is at its request limit. No automatic retry was made.');
  if (!response.ok) throw new Error(`The pilot is unavailable (HTTP ${response.status}). No automatic retry was made.`);
  if (body.id === undefined) { void response.body?.cancel().catch(() => undefined); return null; }
  const message = await readJson(response, signal);
  if (message.jsonrpc !== '2.0' || message.id !== body.id || message.error !== undefined) throw new Error('The MCP request was not accepted.');
  const result = object(message.result); if (!result) throw new Error('The MCP response did not contain a result.');
  return result;
}
async function callTool(name: Operation, parameters: JsonObject, signal: AbortSignal): Promise<JsonObject> {
  const initialised = await post({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: PROTOCOL,
    capabilities: {}, clientInfo: { name: 'gis-ai-go-private-pilot-page', version: '0.1.0' } } }, signal);
  if (initialised?.protocolVersion !== PROTOCOL) throw new Error('The server did not agree the expected MCP protocol.');
  await post({ jsonrpc: '2.0', method: 'notifications/initialized' }, signal);
  const response = await post({ jsonrpc: '2.0', id: 2, method: 'tools/call', params: { name, arguments: parameters } }, signal);
  const value = object(response?.structuredContent);
  if (!value) throw new Error('The tool did not return a structured result.');
  if (response?.isError === true) {
    const code = typeof value.code === 'string' && /^[a-z][a-z-]{1,40}$/.test(value.code) ? value.code : 'unavailable';
    throw new Error(`The operation could not be completed (${code}). An upstream attempt may have used the allowance. No automatic retry was made.`);
  }
  if (!['gis-ai-go.sites-pilot-result.v1', 'gis-ai-go.sites-pilot-capabilities.v1'].includes(String(value.schema))) throw new Error('The tool returned an unsupported result format.');
  return value;
}

function Table({ columns, values }: { columns: readonly string[]; values: readonly (readonly string[])[] }) {
  return <div className="pilot-table"><table><thead><tr>{columns.map((column) => <th scope="col" key={column}>{column}</th>)}</tr></thead>
    <tbody>{values.map((row, index) => <tr key={index}>{row.map((cell, column) => <td key={column}>{cell}</td>)}</tr>)}</tbody></table></div>;
}
function Result({ value }: { value: JsonObject }) {
  const provider = object(value.data), data = object(provider?.data), evidence = object(value.evidence);
  const attribution = Array.isArray(provider?.attribution) ? provider.attribution.filter((item): item is string => typeof item === 'string') : [];
  return <section aria-labelledby="pilot-result-heading" className="pilot-result">
    <h2 id="pilot-result-heading">Result</h2>
    {value.schema === 'gis-ai-go.sites-pilot-capabilities.v1' && <><p>This pilot supports open-data queries only. PSGA data remains disabled.</p>
      <dl>{Object.entries(object(provider?.providers) ?? {}).map(([name, state]) => <div key={name}><dt>{name.replaceAll('_', ' ')}</dt><dd>{text(state)}</dd></div>)}</dl></>}
    {provider?.provider === 'os-names' && <><p>{text(data?.interpretation)}</p><p>Coordinate reference system: {text(data?.crs)}. Review the candidates before selecting a place.</p>
      {rows(data?.candidates).length === 0 ? <p>No matching candidates were returned.</p> : <Table columns={['Name', 'Type', 'Native identifier', 'Easting', 'Northing']}
        values={rows(data?.candidates).map((row) => [text(row.NAME1), text(row.LOCAL_TYPE), text(row.ID), text(row.GEOMETRY_X), text(row.GEOMETRY_Y)])} />}
      <p>Provider-reported matches: {text(data?.total_results)}. This page displays at most five candidates.</p></>}
    {provider?.provider === 'ons-geography' && <><p>MSOA names and codes for England and Wales, December 2021. Name-prefix matches do not establish which area contains a point.</p>
      {data?.complete === false && <p className="pilot-notice"><strong>Partial list.</strong> More matches exist. These are not all the areas associated with the place name.</p>}
      {rows(data?.areas).length === 0 ? <p>No matching area names were returned.</p> : <Table columns={['MSOA code', 'Name']}
        values={rows(data?.areas).map((row) => [text(row.MSOA21CD), text(row.MSOA21NM)])} />}</>}
    {provider?.provider === 'ons-cpih' && <><p>{text(data?.title)}. These are index levels, with 2015 = 100, not inflation percentages.</p>
      <Table columns={['Month', 'Index level', 'Source update']} values={rows(data?.observations).map((row) => [text(row.period), text(row.value), text(row.update_date)])} />
      {object(data?.comparison) && <p>Calculated change: {text(object(data?.comparison)?.difference_index_points)} index points; relative change: {object(data?.comparison)?.relative_change_percent === null ? 'undefined because the starting value is zero' : `${text(object(data?.comparison)?.relative_change_percent)}%`}.
        {' '}This compares the selected months and is not a separately published annual inflation rate.</p>}
      <p>Source release: {text(data?.release_date)}. Latest available month at this retrieval: {text(data?.latest_period_at_retrieval)}.</p></>}
    {provider?.provider === 'os-open-data' && <><h3>{text(data?.name)}</h3><p>Product version: {text(data?.version)}. {text(data?.interpretation)}</p>
      <p>Formats: {rows(data?.formats).map((format) => text(format.format)).join(', ')}.</p></>}
    {provider?.source_mode === 'live-provider-response' && <p>Retrieved: {text(provider.retrieved_at)}. Upstream requests: {text(provider.upstream_request_count)}.</p>}
    {typeof evidence?.receipt_id === 'string' && <><h3>Saved evidence</h3><p className="pilot-code">{text(evidence.receipt_id)}</p>
      <p>This receipt records the result returned by the provider. Independent attestation and protection against storage rollback are not established.</p></>}
    {attribution.length > 0 && <div className="pilot-attribution" aria-label="Source attribution">{attribution.map((line) => <p key={line}>{line}</p>)}
      <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/">Open Government Licence v3.0</a></div>}
    <details><summary>View structured result and provenance</summary><pre>{JSON.stringify(value, null, 2)}</pre></details>
  </section>;
}

export default function SitesPilotPage() {
  const [operation, setOperation] = useState<Operation>('sites_os_names');
  const [place, setPlace] = useState('Warwick'); const [product, setProduct] = useState('OpenNames');
  const [firstMonth, setFirstMonth] = useState('2026-01'); const [secondMonth, setSecondMonth] = useState('2026-07');
  const [compare, setCompare] = useState(true); const [receiptId, setReceiptId] = useState('');
  const [busy, setBusy] = useState(false), [status, setStatus] = useState('Choose a question to start.');
  const [failure, setFailure] = useState(''), [result, setResult] = useState<JsonObject | null>(null);
  const active = useRef<AbortController | null>(null);
  useEffect(() => () => { active.current?.abort(); }, []);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (active.current) return;
    const parameters: JsonObject = operation === 'sites_os_names' ? { query: place.trim(), max_results: 5 }
      : operation === 'sites_ons_areas' ? { name_prefix: place.trim(), max_results: 5 }
      : operation === 'sites_os_open_product' ? { product }
      : operation === 'sites_ons_cpih' ? { periods: compare ? [firstMonth, secondMonth] : [firstMonth] }
      : operation === 'sites_evidence_inspect' ? { receipt_id: receiptId.trim() } : {};
    if (operation === 'sites_ons_cpih' && compare && firstMonth === secondMonth) { setFailure('Choose two different months to compare.'); return; }
    if (operation === 'sites_evidence_inspect' && !/^sites-pilot:sha256:[0-9a-f]{64}$/.test(receiptId.trim())) { setFailure('Enter a complete receipt identifier from a successful pilot query.'); return; }
    const controller = new AbortController(); active.current = controller;
    const deadline = setTimeout(() => controller.abort(), 30_000);
    setBusy(true); setFailure(''); setResult(null); setStatus('Request in progress.');
    try {
      const value = await callTool(operation, parameters, controller.signal); setResult(value);
      const receipt = object(value.evidence)?.receipt_id; if (typeof receipt === 'string') setReceiptId(receipt);
      setStatus(operation === 'sites_evidence_inspect' ? 'Stored receipt inspected. No provider refresh was requested.' : 'Result received. Read its source and limitations below.');
    } catch (error) {
      const message = controller.signal.aborted ? 'The request stopped. A provider attempt or evidence write may already have happened. No automatic retry was made.'
        : error instanceof Error ? error.message : 'The request could not be completed.';
      setFailure(message); setStatus('Request not completed.');
    } finally { clearTimeout(deadline); active.current = null; setBusy(false); }
  }
  return <main className="sites-pilot">
    <style>{`
      .sites-pilot{max-width:72rem;margin:auto;padding:2rem 1.25rem 4rem;color:#172b3a;background:#fff;font:1rem/1.55 Arial,Helvetica,sans-serif}
      .sites-pilot *{box-sizing:border-box}.sites-pilot h1{font-size:clamp(2rem,5vw,3rem);line-height:1.15;margin:.6rem 0 1rem}.sites-pilot h2{font-size:1.55rem;margin-top:0}
      .sites-pilot a{color:#07589c;text-decoration:underline}.sites-pilot a:focus-visible,.sites-pilot button:focus-visible,.sites-pilot input:focus-visible,.sites-pilot select:focus-visible,.sites-pilot summary:focus-visible{outline:3px solid #efbd18;outline-offset:3px}
      .pilot-tag{font-weight:bold;color:#34566d;letter-spacing:.04em}.pilot-intro{max-width:52rem}.pilot-notice{padding:1rem;border-left:5px solid #8e6f0c;background:#fff8de}
      .pilot-grid{display:grid;grid-template-columns:minmax(0,3fr) minmax(15rem,2fr);gap:2rem;margin:2rem 0}.pilot-form,.pilot-limits{border:1px solid #b9c8d1;border-radius:.35rem;padding:1.5rem}
      .pilot-form label{display:block;font-weight:bold;margin-top:1rem}.pilot-form input:not([type=checkbox]),.pilot-form select{width:100%;font:inherit;padding:.65rem;border:2px solid #476270;border-radius:.2rem;background:#fff;color:#172b3a;min-height:44px}
      .pilot-form .pilot-checkbox{display:flex;align-items:center;gap:.7rem;font-weight:normal}.pilot-checkbox input{width:22px;height:22px}.pilot-help{font-size:.94rem;color:#425d6d;margin:.4rem 0 1rem}.pilot-actions{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.5rem}
      .pilot-actions button{min-height:44px;font:inherit;font-weight:bold;border:2px solid #075b57;border-radius:.2rem;background:#075b57;color:#fff;padding:.6rem 1.2rem;cursor:pointer}.pilot-actions button.secondary{background:#fff;color:#075b57}.pilot-actions button:disabled{opacity:.6;cursor:wait}
      .pilot-error{padding:1rem;border:3px solid #b52a21;color:#8e211a}.pilot-result{margin-top:2rem;border-top:4px solid #075b57;padding-top:1.5rem}.pilot-table{max-width:100%;overflow-x:auto;margin:1rem 0}.pilot-table table{border-collapse:collapse;width:100%}.pilot-table th,.pilot-table td{text-align:left;vertical-align:top;padding:.7rem;border-bottom:1px solid #b9c8d1;overflow-wrap:anywhere}.pilot-table th{background:#edf3f5}
      .sites-pilot pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf3f5;padding:1rem;max-height:32rem;overflow:auto}.sites-pilot summary{cursor:pointer;font-weight:bold;padding:1rem 0}.pilot-code{overflow-wrap:anywhere;font-family:monospace}.pilot-attribution{font-size:.9rem;margin:1.5rem 0}.pilot-attribution p{margin:.25rem 0}.sites-pilot dt{font-weight:bold}.sites-pilot dd{margin:0 0 .7rem}.sites-pilot li{margin:.4rem 0}
      @media(max-width:48rem){.pilot-grid{grid-template-columns:1fr}.sites-pilot{padding:1.4rem 1rem 3rem}.pilot-form,.pilot-limits{padding:1rem}}
    `}</style>
    <header className="pilot-intro"><p className="pilot-tag">GIS AI GO · private evaluation</p><h1>Ask a bounded question of live public data</h1>
      <p>Find named places, look up statistical-area codes and compare published index levels. This manual page calls the same six MCP tools as an AI client.</p>
      <p className="pilot-notice">Experimental open-data pilot. This is not the supported GIS AI GO release. Private access does not establish permission to use PSGA data.</p></header>
    <div className="pilot-grid"><form className="pilot-form" onSubmit={submit} aria-busy={busy}>
      <h2>Choose your question</h2><label htmlFor="pilot-operation">What do you want to find?</label>
      <select id="pilot-operation" value={operation} onChange={(event) => setOperation(event.target.value as Operation)} disabled={busy}>
        {operations.map((item) => <option value={item.value} key={item.value}>{item.label}</option>)}</select>
      {(operation === 'sites_os_names' || operation === 'sites_ons_areas') && <><label htmlFor="pilot-place">{operation === 'sites_os_names' ? 'Place name' : 'Beginning of an MSOA name'}</label>
        <input id="pilot-place" value={place} onChange={(event) => setPlace(event.target.value)} required minLength={2} maxLength={operation === 'sites_os_names' ? 80 : 60} disabled={busy} aria-describedby="pilot-place-help" />
        <p id="pilot-place-help" className="pilot-help">{operation === 'sites_os_names' ? 'For example, Warwick. A town and a railway station can share a name. Up to five candidates are returned.' : 'For example, Warwick. Results are December 2021 MSOA names and codes, not a point-to-area match or population estimate.'}</p></>}
      {operation === 'sites_os_open_product' && <><label htmlFor="pilot-product">Open-data product</label><select id="pilot-product" value={product} onChange={(event) => setProduct(event.target.value)} disabled={busy}>
        <option value="OpenNames">OS Open Names</option><option value="OpenUPRN">OS Open UPRN</option><option value="LIDS">OS Open Linked Identifiers</option></select><p className="pilot-help">Checks product metadata and available formats. It does not download records.</p></>}
      {operation === 'sites_ons_cpih' && <><label htmlFor="pilot-month-one">First month</label><input type="month" id="pilot-month-one" value={firstMonth} onChange={(event) => setFirstMonth(event.target.value)} required disabled={busy} />
        <label className="pilot-checkbox"><input type="checkbox" checked={compare} onChange={(event) => setCompare(event.target.checked)} disabled={busy} />Compare with a second month</label>
        {compare && <><label htmlFor="pilot-month-two">Second month</label><input type="month" id="pilot-month-two" value={secondMonth} onChange={(event) => setSecondMonth(event.target.value)} required disabled={busy} /></>}
        <p className="pilot-help">CPIH L522/MM23, 2015 = 100. Select one or two published months. Missing months are reported, never substituted.</p></>}
      {operation === 'sites_evidence_inspect' && <><label htmlFor="pilot-receipt">Receipt identifier</label><input id="pilot-receipt" className="pilot-code" value={receiptId} onChange={(event) => setReceiptId(event.target.value)} required maxLength={100} disabled={busy} spellCheck={false} />
        <p className="pilot-help">A successful query fills this field automatically. Inspection reads saved evidence and does not refresh the provider.</p></>}
      {operation === 'sites_capabilities' && <p className="pilot-help">Checks the advertised tools and boundaries without making a provider request.</p>}
      <div className="pilot-actions"><button type="submit" disabled={busy}>{busy ? 'Requesting…' : 'Run question'}</button>
        {busy && <button type="button" className="secondary" onClick={() => active.current?.abort()}>Cancel request</button>}</div>
      <p role="status" aria-live="polite">{status}</p>{failure && <p role="alert" className="pilot-error">{failure}</p>}
    </form><aside className="pilot-limits" aria-labelledby="pilot-limits-heading"><h2 id="pilot-limits-heading">What this can establish</h2>
      <ul><li>OS named-place candidates for Great Britain, preserving ambiguity.</li><li>ONS MSOA names and codes for England and Wales.</li><li>Published CPIH index levels, with deterministic comparison.</li><li>Source metadata, retrieval details and saved receipts.</li></ul>
      <p>It cannot identify occupants, infer property values, retrieve detailed addresses, calculate population or determine which MSOA contains a point.</p>
      <p>Each provider starts with 120 admitted attempts, with at most 20 attempts per minute per provider. A CPIH query uses two upstream requests. Failed attempts count. There are no automatic retries.</p>
      <p>The store holds at most 128 receipts. These application limits do not guarantee a platform billing limit.</p>
      <details><summary>Source contracts</summary><ul><li><a href="https://www.ordnancesurvey.co.uk/products/os-names-api">OS Names API</a></li>
        <li><a href="https://developer.ons.gov.uk/retirement/v0api/">ONS maintained time-series API</a></li><li><a href="https://www.ons.gov.uk/methodology/geography/licences">ONS geography and attribution</a></li></ul></details>
    </aside></div>
    {result && <Result value={result} />}
  </main>;
}
