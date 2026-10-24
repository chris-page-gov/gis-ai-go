/* Optional local navigation over a dated, host-reviewed coverage statement. */
(function (scope) {
  'use strict';
  const CAP = 1024 * 1024, PAGE = 5, SCHEMA = 'gis-ai-go.coverage-navigator.v1';
  const FAILURE = 'Coverage navigation could not be loaded.';
  const require = ok => { if (!ok) throw new Error(FAILURE); };
  const own = (v, keys) => {
    require(v !== null && typeof v === 'object' && !Array.isArray(v));
    require(Object.keys(v).length === keys.length && keys.every(k => Object.hasOwn(v, k)));
    return v;
  };
  const string = (v, max, empty = false) => {
    require(typeof v === 'string' && (empty || v.length > 0) && Array.from(v).length <= max);
    for (const c of v) require(c.codePointAt(0) < 0xd800 || c.codePointAt(0) > 0xdfff);
    return v;
  };
  const id = v => { string(v, 80); require(/^[A-Za-z][A-Za-z0-9_.:-]{0,79}$/u.test(v)); return v; };
  const array = (v, max, min = 0) => { require(Array.isArray(v) && v.length >= min && v.length <= max); return v; };
  const safeUrl = v => {
    if (v === null) return true;
    try {
      string(v, 2048); const u = new URL(v);
      return u.protocol === 'https:' && !u.username && !u.password && !u.search && !u.port && u.href === v &&
        ['docs.os.uk', 'www.ordnancesurvey.co.uk', 'os.uk', 'www.ons.gov.uk', 'www.nomisweb.co.uk', 'example.org'].includes(u.hostname);
    } catch (_) { return false; }
  };
  const freeze = v => { if (v && typeof v === 'object') { Object.values(v).forEach(freeze); Object.freeze(v); } return v; };
  function parse(text) {
    require(typeof text === 'string' && new TextEncoder().encode(text).length <= CAP);
    let p; try { p = JSON.parse(text); } catch (_) { throw new Error(FAILURE); }
    own(p, ['schema', 'asOf', 'basis', 'counts', 'fullCoverage', 'percentage', 'gates', 'rows', 'nodes', 'edges']);
    require(p.schema === SCHEMA && p.fullCoverage === false && p.percentage === null);
    string(p.asOf, 10); require(/^\d{4}-\d{2}-\d{2}$/u.test(p.asOf) && !p.asOf.startsWith('0000'));
    const day = new Date(p.asOf + 'T00:00:00Z'); require(Number.isFinite(day.getTime()) && day.toISOString().slice(0, 10) === p.asOf);
    own(p.basis, ['title', 'scopeNote']); string(p.basis.title, 200); string(p.basis.scopeNote, 2000);
    own(p.counts, ['rows', 'included', 'excluded', 'unclassified', 'edges']);
    Object.values(p.counts).forEach(n => require(Number.isSafeInteger(n) && n >= 0 && n <= 256));
    const gates = new Map();
    for (const g of array(p.gates, 16, 1)) { own(g, ['id', 'label']); id(g.id); string(g.label, 120); require(!gates.has(g.id)); gates.set(g.id, g.label); }
    const ids = new Set(), scopes = {included: 0, excluded: 0, unclassified: 0};
    for (const r of array(p.rows, 256)) {
      own(r, ['id', 'label', 'scope', 'sourceUrl', 'next', 'remaining', 'gates', 'evidence']);
      id(r.id); require(!ids.has(r.id)); ids.add(r.id); string(r.label, 240); string(r.next, 2000); string(r.remaining, 2000);
      require(typeof r.scope === 'string' && Object.hasOwn(scopes, r.scope)); scopes[r.scope]++; require(safeUrl(r.sourceUrl));
      require(array(r.gates, 16).length === gates.size); const seen = new Set();
      for (const g of r.gates) { own(g, ['id', 'status', 'limit']); require(gates.has(g.id) && !seen.has(g.id)); seen.add(g.id); string(g.status, 120); string(g.limit, 2000); }
      for (const e of array(r.evidence, 32)) {
        own(e, ['scope', 'limit', 'receiptHashes']); string(e.scope, 500); string(e.limit, 2000);
        array(e.receiptHashes, 16).forEach(h => require(typeof h === 'string' && /^[a-f0-9]{64}$/u.test(h)));
      }
    }
    const nodes = new Set();
    for (const n of array(p.nodes, 64)) { own(n, ['id', 'label']); id(n.id); string(n.label, 160); require(!nodes.has(n.id)); nodes.add(n.id); }
    const edges = new Set();
    for (const e of array(p.edges, 128)) {
      own(e, ['id', 'from', 'to', 'relation', 'limits', 'transitiveIdentityInferred']); id(e.id);
      require(!edges.has(e.id) && nodes.has(e.from) && nodes.has(e.to) && e.transitiveIdentityInferred === false); edges.add(e.id);
      string(e.relation, 2000); string(e.limits, 2000);
    }
    require(p.counts.rows === p.rows.length && p.counts.edges === p.edges.length);
    for (const k of Object.keys(scopes)) require(p.counts[k] === scopes[k]);
    return freeze(p);
  }
  function create(root, text, prefix = 'coverage-navigator') {
    require(typeof prefix === 'string' && /^[a-z][a-z0-9-]{0,59}$/u.test(prefix));
    const p = parse(text), doc = root.ownerDocument;
    const gateNames = new Map(p.gates.map(g => [g.id, g.label])), nodeNames = new Map(p.nodes.map(n => [n.id, n.label]));
    let page = 0, query = '', filterScope = 'included', selected = null, disposed = false;
    const make = (tag, value) => { const e = doc.createElement(tag); if (value !== undefined) e.textContent = value; return e; };
    const button = (title, fn) => { const b = make('button', title); b.type = 'button'; b.addEventListener('click', () => { if (!disposed) fn(); }); return b; };
    const label = (title, control, suffix) => { const e = make('label', title); control.id = prefix + '-' + suffix; e.htmlFor = control.id; return e; };
    const note = make('p', `${p.asOf}: ${p.counts.rows} supplied basis rows — ${p.counts.included} included, ${p.counts.excluded} excluded and ${p.counts.unclassified} unclassified. Full coverage is not established. No completion percentage is provided.`);
    const help = make('details'); help.append(make('summary', 'Basis, dates and relationship limits'), make('h4', p.basis.title), make('p', p.basis.scopeNote),
      make('p', 'Documentary denominator: the basis rows count entries in a selected catalogue or scope statement. They do not count processed payloads or passing tests.'),
      make('p', 'Tested evidence: a check or processed selection supports only its recorded input, method and result. A completed selection does not mean a whole product, every current edition or all jurisdictions are covered.'),
      make('p', 'Scoped status: read each gate status with its stated limit. It is not a whole-product verdict, and inclusion in the basis is not technical acceptance.'),
      make('p', 'Directed relationship: an arrow follows the supplied evidence and direction. It is not automatically identity, containment, a spatial test or a transitive chain.'),
      make('p', 'Publication, reference period, code validity, boundary vintage, feature version and retrieval date have distinct roles. A difference alone is not an error.'),
      make('p', 'Displayed review hashes are host-provided references. This widget does not verify receipts, source authenticity, rights or current service behaviour.'));
    const choose = make('select'); for (const [value, title] of [['products', 'Rows and next actions'], ['routes', 'Relationships']]) { const o = make('option', title); o.value = value; choose.append(o); } choose.value = 'products';
    const modeLabel = label('Coverage view', choose, 'mode'), products = make('section'), routes = make('section'); routes.hidden = true;
    const search = make('input'); search.type = 'search'; search.maxLength = 160;
    const searchLabel = label('Find a row or remaining gap', search, 'search'), filter = make('select');
    for (const [value, title] of [['included', 'Included rows'], ['all', 'All supplied rows'], ['excluded', 'Excluded rows'], ['unclassified', 'Unclassified rows']]) { const o = make('option', title); o.value = value; filter.append(o); } filter.value = filterScope;
    const filterLabel = label('Scope', filter, 'scope'), status = make('p'), list = make('ul'), detail = make('section');
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite'); detail.setAttribute('aria-label', 'Selected coverage row');
    const previous = button('Previous rows', () => { page = Math.max(0, page - 1); render(); }), next = button('Next rows', () => { page++; render(); });
    function show(r) {
      selected = r.id; detail.replaceChildren(); const heading = make('h4', r.label); heading.tabIndex = -1;
      const meaning = r.scope === 'included' ? 'Included in this supplied dated basis; full technical coverage is not established.' : r.scope === 'excluded' ? 'Excluded from this supplied dated basis.' : 'Unclassified in this supplied dated basis.';
      detail.append(heading, make('p', meaning), make('h5', 'Next bounded action'), make('p', r.next), make('h5', 'Remaining dependency'), make('p', r.remaining));
      if (r.sourceUrl) { const a = make('a', 'Supplied source documentation'); a.href = r.sourceUrl; a.target = '_blank'; a.rel = 'noopener noreferrer'; detail.append(a); }
      const checks = make('details'); checks.append(make('summary', `Inspect ${r.gates.length} separate evidence gates`));
      for (const g of r.gates) checks.append(make('h5', gateNames.get(g.id)), make('p', g.status), make('p', g.limit)); detail.append(checks);
      const evidence = make('details'); evidence.append(make('summary', `${r.evidence.length} supplied review associations`));
      if (!r.evidence.length) evidence.append(make('p', 'No review association is supplied here; no complete input or acceptance is implied.'));
      for (const e of r.evidence) { evidence.append(make('p', e.scope), make('p', e.limit)); const hashes = make('details'); hashes.append(make('summary', 'Supplied review hashes')); for (const h of e.receiptHashes) hashes.append(make('code', h)); evidence.append(hashes); } detail.append(evidence);
      heading.focus(); render();
    }
    function render() {
      const matched = p.rows.filter(r => (filterScope === 'all' || r.scope === filterScope) && (!query || [r.label, r.remaining, r.next].join(' ').toLocaleLowerCase('en-GB').includes(query)));
      const last = Math.max(0, Math.ceil(matched.length / PAGE) - 1); page = Math.min(page, last); list.replaceChildren();
      for (const r of matched.slice(page * PAGE, page * PAGE + PAGE)) { const li = make('li'), b = button(r.label, () => show(r)); b.setAttribute('aria-pressed', String(selected === r.id)); li.append(b); list.append(li); }
      status.textContent = matched.length ? `${page * PAGE + 1}–${Math.min(page * PAGE + PAGE, matched.length)} of ${matched.length} matching rows. Search covers these supplied rows, not other collections.` : 'No matching row in this supplied dated basis.';
      previous.disabled = page === 0; next.disabled = page >= last;
    }
    function setFilter(q, s = 'included') {
      if (disposed) return false;
      string(q, 160, true); require(typeof s === 'string' && ['included', 'all', 'excluded', 'unclassified'].includes(s));
      query = q.toLocaleLowerCase('en-GB'); filterScope = s; search.value = q; filter.value = s; page = 0; selected = null; detail.replaceChildren(); render(); return true;
    }
    search.addEventListener('input', () => setFilter(search.value, filter.value)); filter.addEventListener('change', () => setFilter(search.value, filter.value));
    products.append(searchLabel, search, filterLabel, filter, status, list, previous, next, detail);
    const edgeChoice = make('select'), edgeLabel = label('Relationship to inspect', edgeChoice, 'edge'), edgeDetail = make('section');
    for (const e of p.edges) { const o = make('option', `${nodeNames.get(e.from)} → ${nodeNames.get(e.to)}`); o.value = e.id; edgeChoice.append(o); }
    edgeChoice.value = p.edges.length ? p.edges[0].id : ''; edgeChoice.disabled = !p.edges.length;
    function showEdge() {
      if (disposed) return;
      const e = p.edges.find(e => e.id === edgeChoice.value); edgeDetail.replaceChildren();
      if (!e) { edgeDetail.append(make('p', 'No supplied relationship selected.')); return; }
      const diagram = make('div'); diagram.className = 'coverage-route'; diagram.append(make('strong', nodeNames.get(e.from)), make('span', '→'), make('strong', nodeNames.get(e.to)));
      edgeDetail.append(diagram, make('p', e.relation), make('h4', 'What this does not establish'), make('p', e.limits));
    }
    edgeChoice.addEventListener('change', showEdge); routes.append(make('p', `${p.edges.length} supplied directed relationships. They do not establish a universal containment chain or common snapshot.`), edgeLabel, edgeChoice, edgeDetail); showEdge();
    choose.addEventListener('change', () => { if (disposed) return; require(['products', 'routes'].includes(choose.value)); products.hidden = choose.value !== 'products'; routes.hidden = choose.value !== 'routes'; });
    root.replaceChildren(note, help, modeLabel, choose, products, routes); render();
    return Object.freeze({elements: Object.freeze({search, filter, list, detail, previous, next, status, help, mode: choose, products, routes, edgeChoice, edgeDetail}),
      setFilter, snapshot: () => Object.freeze({query, scope: filterScope, page, selected}), dispose: () => { disposed = true; }});
  }
  function mount(disclosure, root, text, prefix) {
    let instance = null, disposed = false;
    const initialise = () => { if (!disposed && disclosure.open && !instance) { try { instance = create(root, text, prefix); } catch (_) { root.textContent = FAILURE + ' Existing host panels remain available.'; } } };
    disclosure.addEventListener('toggle', initialise);
    initialise();
    return Object.freeze({snapshot: () => instance && instance.snapshot(), dispose: () => { disposed = true; if (instance) instance.dispose(); }});
  }
  const api = Object.freeze({parse, create, mount, CAP, PAGE, SCHEMA});
  if (typeof module === 'object' && module.exports) module.exports = api; else scope.CoverageNavigator = api;
})(typeof globalThis === 'object' ? globalThis : this);
