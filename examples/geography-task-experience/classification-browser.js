/* Offline, source-owned code lists. No acquisition, equivalence or inferred hierarchy. */
(function (scope) {
  'use strict';
  const SCHEMA = 'gis-ai-go.classification-browser.v1';
  const PAGE_SIZE = 20;
  const has = (x, k) => Object.prototype.hasOwnProperty.call(x, k);
  const plain = x => x !== null && typeof x === 'object' && !Array.isArray(x);
  const fail = message => { throw new Error('Code-list contract: ' + message); };
  const text = (x, name, nullable = false) => {
    if (nullable && x === null) return;
    if (typeof x !== 'string' || x.length > 10000) fail(name + ' must be a bounded string' + (nullable ? ' or null' : ''));
  };
  function fields(x, required, name, optional = []) {
    if (!plain(x)) fail(name + ' must be an object');
    for (const k of required) if (!has(x, k)) fail(name + ' is missing ' + k);
    for (const k of Object.keys(x)) if (!required.includes(k) && !optional.includes(k)) fail(name + ' has an unexpected property');
  }
  const identity = (value, name) => { if (typeof value !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}$/u.test(value)) fail(name + ' identity'); };
  function nativeText(value) {
    let nodes = 0, scalarBytes = 0;
    const seen = new Set();
    const charge = x => { if (x.length > 131072) fail('native field display exceeds 128 KiB'); scalarBytes += new TextEncoder().encode(x).length; if (scalarBytes > 131072) fail('native field display exceeds 128 KiB'); };
    function visit(x, depth) {
      if (++nodes > 4096 || depth > 16) fail('native field display bound exceeded');
      if (typeof x === 'string') { charge(x); return; }
      if (x === null || typeof x === 'boolean') return;
      if (typeof x === 'number' && Number.isFinite(x)) return;
      if (!plain(x) && !Array.isArray(x)) fail('native value is not JSON');
      if (seen.has(x)) fail('native value contains a cycle');
      seen.add(x);
      for (const [key, child] of Object.entries(x)) { charge(key); visit(child, depth + 1); }
      seen.delete(x);
    }
    if (!plain(value)) fail('native must be an object');
    visit(value, 0);
    const encoded = JSON.stringify(value, null, 2);
    if (new TextEncoder().encode(encoded).length > 131072) fail('native field display exceeds 128 KiB');
    return encoded;
  }
  function safeSourceURL(value) {
    try {
      if (typeof value !== 'string' || value.length > 2048 || /[\s\\]/u.test(value)) return null;
      const u = new URL(value);
      if (u.protocol !== 'https:' || u.username || u.password || (u.port && u.port !== '443')) return null;
      const forbidden = /^(?:key|apikey|accesstoken|token|authorization|clientsecret|password|secret|sig|signature|sas|auth|xamz.*|xgoog.*)$/iu;
      for (let name of u.searchParams.keys()) {
        for (let i = 0; i < 2; i++) name = decodeURIComponent(name);
        if (decodeURIComponent(name) !== name || forbidden.test(name.replace(/[^a-z0-9]/giu, ''))) return null;
      }
      return u.href;
    } catch (_) { return null; }
  }
  function validate(payload) {
    fields(payload, ['schema', 'reviewedOn', 'globalComplete', 'schemes'], 'payload');
    if (payload.schema !== SCHEMA || payload.globalComplete !== false) fail('version or global scope is unsupported');
    text(payload.reviewedOn, 'reviewedOn');
    if (!/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/u.test(payload.reviewedOn)) fail('reviewedOn format');
    if (!Array.isArray(payload.schemes) || !payload.schemes.length || payload.schemes.length > 64) fail('scheme count is unsupported');
    const schemeIds = new Set(), rows = [];
    let displayBytes = 0;
    for (const s of payload.schemes) {
      fields(s, ['id', 'title', 'edition', 'referenceDate', 'publishedDate', 'retrievedAt', 'jurisdiction', 'description', 'sources', 'coverage', 'gaps', 'entries'], 'scheme');
      for (const k of ['id', 'title', 'retrievedAt', 'jurisdiction', 'description']) text(s[k], 'scheme.' + k);
      identity(s.id, 'scheme');
      for (const k of ['edition', 'referenceDate', 'publishedDate']) text(s[k], 'scheme.' + k, true);
      if (schemeIds.has(s.id)) fail('duplicate scheme identity');
      schemeIds.add(s.id);
      if (!Array.isArray(s.sources) || !s.sources.length || s.sources.length > 32) fail('source count');
      const sources = new Map();
      for (const src of s.sources) {
        fields(src, ['id', 'title', 'url', 'sha256'], 'source');
        for (const k of ['id', 'title', 'url', 'sha256']) text(src[k], 'source.' + k);
        identity(src.id, 'source');
        if (!/^[a-f0-9]{64}$/u.test(src.sha256) || sources.has(src.id)) fail('invalid or duplicate source identity');
        sources.set(src.id, src);
      }
      fields(s.coverage, ['status', 'expectedEntries', 'retainedEntries', 'definitionsStatus'], 'coverage');
      const c = s.coverage;
      if (!['complete-selected-list', 'partial', 'not-captured'].includes(c.status)) fail('coverage status');
      if (!['source-definitions-retained', 'labels-only', 'mixed-or-partial'].includes(c.definitionsStatus)) fail('definition status');
      for (const k of ['expectedEntries', 'retainedEntries']) {
        if (k === 'expectedEntries' && c[k] === null) continue;
        if (!Number.isSafeInteger(c[k]) || c[k] < 0 || c[k] > 20000) fail('coverage count');
      }
      if (!Array.isArray(s.entries) || s.entries.length > 20000 || c.retainedEntries !== s.entries.length) fail('retained count differs from supplied entries');
      if (c.status === 'complete-selected-list' && c.expectedEntries !== s.entries.length) fail('complete selected-list denominator is unproved');
      if (!Array.isArray(s.gaps) || !s.gaps.length || s.gaps.length > 100) fail('explicit scope gaps are required');
      s.gaps.forEach(gap => text(gap, 'gap'));
      const ids = new Set();
      for (const e of s.entries) {
        fields(e, ['id', 'code', 'label', 'definition', 'level', 'parentCode', 'aliases', 'sourceId', 'sourceLocator', 'native'], 'entry', ['labelLanguage']);
        if (has(e, 'labelLanguage')) { text(e.labelLanguage, 'entry.labelLanguage', true); if (e.labelLanguage !== null && (e.labelLanguage.length < 1 || e.labelLanguage.length > 80)) fail('labelLanguage length'); }
        for (const k of ['id', 'label', 'sourceId', 'sourceLocator']) text(e[k], 'entry.' + k);
        identity(e.id, 'entry'); identity(e.sourceId, 'entry source');
        for (const k of ['code', 'definition', 'level', 'parentCode']) text(e[k], 'entry.' + k, true);
        if (c.definitionsStatus === 'source-definitions-retained' && (e.definition === null || !e.definition.trim())) fail('source definition coverage is unsupported');
        if (c.definitionsStatus === 'labels-only' && e.definition !== null && e.definition.trim()) fail('labels-only definition coverage conflicts with entry');
        if (ids.has(e.id)) fail('duplicate entry identity within a scheme');
        ids.add(e.id);
        if (!sources.has(e.sourceId)) fail('unresolved entry source');
        if (!Array.isArray(e.aliases) || e.aliases.length > 100) fail('alias count');
        for (const a of e.aliases) {
          fields(a, ['text', 'kind', 'authority', 'sourceId'], 'alias');
          for (const k of ['text', 'kind', 'authority', 'sourceId']) text(a[k], 'alias.' + k);
          if (!a.text.trim()) fail('alias text is empty');
          identity(a.sourceId, 'alias source');
          if (!['abbreviation', 'search-variant', 'native-field-form', 'native-type-form', 'historical-label', 'source-alternative-label', 'notation', 'full-iri', 'compact-iri'].includes(a.kind)) fail('alias kind');
          if (!['source-stated', 'project-search-variant'].includes(a.authority) || (a.authority === 'project-search-variant' && a.kind !== 'search-variant')) fail('alias authority');
          if (!sources.has(a.sourceId)) fail('unresolved alias source');
        }
        const nativeDisplay = nativeText(e.native);
        displayBytes += new TextEncoder().encode(nativeDisplay).length;
        if (displayBytes > 16777216) fail('total native display exceeds 16 MiB');
        rows.push({scheme: s, entry: e, sources, nativeDisplay});
      }
    }
    return {payload, rows};
  }
  function display(value, nullLabel = 'Not supplied (null)') {
    if (value === null) return nullLabel;
    if (value === '') return 'Empty string (supplied)';
    if (typeof value === 'string' && /^\s+$/u.test(value)) return 'Whitespace-only string (supplied): ' + JSON.stringify(value);
    return value;
  }
  function matchRows(rows, schemeId, query) {
    const q = query.trim().toLocaleLowerCase('en-GB');
    return rows.filter(({scheme: s, entry: e}) => (!schemeId || schemeId === s.id) &&
      (!q || [s.id, s.title, e.code, e.label, ...e.aliases.map(a => a.text)]
        .some(v => v !== null && v.toLocaleLowerCase('en-GB').includes(q))));
  }
  function parentOf(scheme, entry) {
    if (entry.parentCode === null) return {state: 'not-supplied', label: 'No parent relationship supplied (null). This does not prove a top-level concept.'};
    if (entry.parentCode === '') return {state: 'empty', label: 'An explicit empty parent code was supplied; no parent is inferred.'};
    const candidates = scheme.entries.filter(e => e.code === entry.parentCode);
    if (candidates.length !== 1 || candidates[0].id === entry.id) return {state: 'unresolved', label: 'Unresolved parent code: ' + entry.parentCode + '. It has no unique separate entry in this supplied scheme.'};
    return {state: 'resolved', entry: candidates[0], label: 'Source-supplied parent: ' + display(candidates[0].code) + ' — ' + display(candidates[0].label)};
  }
  function create(root, payload, options = {}) {
    const doc = options.document || root.ownerDocument;
    const prefix = options.idPrefix || 'classification-browser';
    if (!/^[a-z][a-z0-9-]{0,79}$/u.test(prefix)) fail('invalid DOM prefix');
    const el = (tag, value, cls) => {
      const n = doc.createElement(tag);
      if (value !== undefined) n.textContent = value;
      if (cls) n.className = cls;
      return n;
    };
    root.classList.add('classification-browser');
    let admitted;
    try { admitted = validate(payload); } catch (error) {
      const message = el('p', 'This code-list payload could not be displayed: ' + error.message, 'classification-error');
      message.setAttribute('role', 'alert'); root.replaceChildren(message); throw error;
    }
    const {rows} = admitted;
    const state = {schemeId: '', query: '', page: 0, selected: null};
    const heading = el('h3', 'Source code lists');
    const intro = el('p', 'These selected lists are separate from the learning glossary. Matching codes or labels across schemes do not establish equivalence. Overall vocabulary coverage remains incomplete.');
    const review = el('p', 'Projection reviewed on: ' + payload.reviewedOn + '. This is not the supplier release date.', 'muted');
    const controls = el('div', undefined, 'classification-controls');
    const schemeLabel = el('label', 'Scheme'); schemeLabel.htmlFor = prefix + '-scheme';
    const select = el('select'); select.id = schemeLabel.htmlFor;
    const all = el('option', 'All supplied schemes'); all.value = ''; select.append(all);
    for (const s of payload.schemes) { const option = el('option', s.title + ' — ' + display(s.edition, 'edition not supplied')); option.value = s.id; select.append(option); }
    const searchLabel = el('label', 'Find a code, label or alias'); searchLabel.htmlFor = prefix + '-search';
    const search = el('input'); search.id = searchLabel.htmlFor; search.type = 'search'; search.maxLength = 500; search.autocomplete = 'off';
    search.setAttribute('aria-describedby', prefix + '-search-help');
    const help = el('p', 'Search includes scheme names. Search is text matching; it does not infer equivalent concepts.', 'muted'); help.id = prefix + '-search-help';
    controls.append(schemeLabel, select, searchLabel, search, help);
    const scopeBox = el('div', undefined, 'classification-scope');
    const count = el('p'); count.id = prefix + '-count'; count.setAttribute('role', 'status'); count.setAttribute('aria-live', 'polite'); count.setAttribute('aria-atomic', 'true');
    const list = el('ol', undefined, 'classification-results'); list.setAttribute('aria-label', 'Matching source entries');
    const pagination = el('div', undefined, 'classification-pagination');
    const previous = el('button', 'Previous page'), next = el('button', 'Next page'), page = el('span');
    previous.type = next.type = 'button'; previous.setAttribute('aria-label', 'Previous page of code-list results'); next.setAttribute('aria-label', 'Next page of code-list results'); pagination.append(previous, page, next);
    const detail = el('section', undefined, 'classification-detail'); detail.setAttribute('aria-label', 'Selected source entry');
    root.replaceChildren(heading, intro, review, controls, scopeBox, count, list, pagination, detail);
    function pair(dl, label, value) { dl.append(el('dt', label), el('dd', value)); }
    function sourceLink(src) {
      const link = safeSourceURL(src.url);
      if (!link) return el('span', src.title + ' — link withheld: unsupported or credential-bearing URL.');
      const a = el('a', src.title); a.href = link; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a;
    }
    function scopeCard(s) {
      const card = el('details', undefined, 'classification-scheme');
      card.open = Boolean(state.schemeId);
      const c = s.coverage;
      const status = {'complete-selected-list': 'Complete selected source list', partial: 'Partial selected list', 'not-captured': 'List not captured'}[c.status];
      card.append(el('summary', s.title + ': ' + status + ' — ' + c.retainedEntries + ' retained / ' + (c.expectedEntries === null ? 'unknown expected count' : c.expectedEntries + ' expected') + '; ' + s.gaps.length + ' scope notes'));
      const dl = el('dl');
      pair(dl, 'Scope', s.description); pair(dl, 'Jurisdiction', s.jurisdiction);
      pair(dl, 'Edition or release', display(s.edition, 'Unknown (null)'));
      pair(dl, 'Reference date', display(s.referenceDate, 'Unknown (null)'));
      pair(dl, 'Publication date', display(s.publishedDate, 'Unknown (null)'));
      pair(dl, 'Retrieved at', display(s.retrievedAt));
      pair(dl, 'Definition coverage', {'source-definitions-retained': 'Source definitions retained', 'labels-only': 'Labels only; definitions are not supplied', 'mixed-or-partial': 'Mixed or partial source definitions'}[c.definitionsStatus]);
      card.append(dl, el('h4', 'Remaining gaps and limits'));
      const gaps = el('ul'); s.gaps.forEach(gap => gaps.append(el('li', gap))); card.append(gaps);
      const sources = el('ul'); for (const src of s.sources) { const li = el('li'); li.append(sourceLink(src), el('small', 'Source SHA-256: ' + src.sha256)); sources.append(li); } card.append(sources);
      return card;
    }
    function showDetail(row, moveFocus) {
      state.selected = row;
      detail.replaceChildren();
      if (!row) { detail.append(el('p', 'Choose a source entry to inspect its definition, relationships and native fields.')); return; }
      const {scheme: s, entry: e} = row;
      const title = el('h4', display(e.code, 'No code supplied') + ' — ' + display(e.label)); title.tabIndex = -1;
      const dl = el('dl'); pair(dl, 'Scheme', s.title); pair(dl, 'Entry identity within scheme', e.id);
      pair(dl, 'Code', display(e.code)); pair(dl, 'Label', display(e.label));
      if (has(e, 'labelLanguage')) pair(dl, 'Source-declared label language', display(e.labelLanguage, 'Not supplied (explicit null)'));
      pair(dl, 'Source definition', display(e.definition, 'No definition supplied (null); a label is not a definition.'));
      pair(dl, 'Source level', display(e.level, 'No level supplied (null); none is inferred.'));
      pair(dl, 'Source locator', display(e.sourceLocator));
      detail.append(title, dl);
      const limits = el('ul'); s.gaps.forEach(gap => limits.append(el('li', gap))); detail.append(el('h5', 'Limits for this entry’s scheme'), limits);
      if (e.code !== null && e.code !== '') {
        const other = rows.filter(r => r.entry.code === e.code && !(r.scheme.id === s.id && r.entry.id === e.id));
        detail.append(el('h5', 'Other occurrences of this code'), el('p', 'Exact text comparison only. Equal codes do not establish equivalent concepts, and different labels must remain source-owned.', 'muted'));
        if (!other.length) detail.append(el('p', 'No other occurrence in these supplied lists. This is not a global absence claim.'));
        else {
          detail.append(el('p', other.length + ' other occurrence' + (other.length === 1 ? '' : 's') + (other.length > 20 ? '; showing the first 20.' : '.')));
          const occurrences = el('ul');
          for (const r of other.slice(0, 20)) { const item = el('li'), button = el('button', r.scheme.title + ': ' + display(r.entry.code) + ' — ' + display(r.entry.label)); button.type = 'button'; button.addEventListener('click', () => showDetail(r, true)); item.append(button); occurrences.append(item); }
          detail.append(occurrences);
        }
      }
      const relationship = parentOf(s, e);
      detail.append(el('p', relationship.label));
      if (relationship.state === 'resolved') {
        const button = el('button', 'Inspect source-supplied parent'); button.type = 'button';
        button.addEventListener('click', () => showDetail(rows.find(r => r.scheme.id === s.id && r.entry.id === relationship.entry.id), true));
        detail.append(button);
      }
      detail.append(el('p', 'Only the supplied parent relationship is shown. Code prefixes, field order and matching labels do not establish hierarchy or equivalence.', 'muted'));
      const aliases = el('ul');
      for (const a of e.aliases) { const item = el('li', display(a.text) + ' — ' + a.kind + '; ' + a.authority + '. '); item.append(sourceLink(row.sources.get(a.sourceId))); aliases.append(item); }
      detail.append(el('h5', 'Aliases and search forms'), e.aliases.length ? aliases : el('p', 'No aliases supplied.'));
      detail.append(el('h5', 'Source'), sourceLink(row.sources.get(e.sourceId)));
      const native = el('details'); native.append(el('summary', 'All native fields for this entry'), el('p', 'Exact supplied JSON types are retained: null, an empty string, zero and false remain different. Native field names are source-owned; their presence does not prove their complete meaning.', 'muted'), el('pre', row.nativeDisplay)); detail.append(native);
      if (moveFocus) title.focus();
    }
    function render(resetSelection) {
      const matches = matchRows(rows, state.schemeId, state.query);
      const total = rows.filter(r => !state.schemeId || r.scheme.id === state.schemeId).length;
      const pages = Math.max(1, Math.ceil(matches.length / PAGE_SIZE)); state.page = Math.min(state.page, pages - 1);
      const start = state.page * PAGE_SIZE, visible = matches.slice(start, start + PAGE_SIZE);
      count.textContent = matches.length + ' matching entries / ' + total + ' retained in ' + (state.schemeId ? 'this scheme' : 'the supplied schemes') + '. ' + (matches.length ? 'Showing ' + (start + 1) + '–' + (start + visible.length) + '.' : 'No matching source entries.');
      scopeBox.replaceChildren(...payload.schemes.filter(s => !state.schemeId || s.id === state.schemeId).map(scopeCard));
      list.replaceChildren(); list.start = start + 1;
      for (const row of visible) {
        const item = el('li'), button = el('button', display(row.entry.code, 'No code supplied') + ' — ' + display(row.entry.label)); button.type = 'button';
        button.addEventListener('click', () => showDetail(row, true));
        item.append(button, el('small', row.scheme.title + ' · ' + display(row.scheme.edition, 'edition unknown'))); list.append(item);
      }
      previous.disabled = state.page === 0; next.disabled = state.page >= pages - 1; page.textContent = 'Page ' + (state.page + 1) + ' of ' + pages;
      if (resetSelection || !state.selected) showDetail(null, false);
    }
    select.addEventListener('change', () => { state.schemeId = select.value; state.page = 0; render(true); });
    search.addEventListener('input', () => { state.query = search.value.slice(0, 500); state.page = 0; render(true); });
    previous.addEventListener('click', () => { if (state.page > 0) { state.page--; render(false); } });
    next.addEventListener('click', () => { const pages = Math.ceil(matchRows(rows, state.schemeId, state.query).length / PAGE_SIZE); if (state.page + 1 < pages) { state.page++; render(false); } });
    render(true);
    return Object.freeze({elements: {select, search, count, list, previous, next, page, detail, scopeBox}, setFilter: (query, schemeId = '') => {
      if (typeof query !== 'string' || query.length > 500 || (schemeId && !payload.schemes.some(s => s.id === schemeId))) fail('unsupported contextual filter');
      search.value = query; select.value = schemeId; state.query = query; state.schemeId = schemeId; state.page = 0; render(true);
    }, snapshot: () => ({schemeId: state.schemeId, query: state.query, page: state.page, selected: state.selected ? {schemeId: state.selected.scheme.id, entryId: state.selected.entry.id} : null})});
  }
  const api = Object.freeze({SCHEMA, PAGE_SIZE, validate, nativeText, safeSourceURL, display, matchRows, parentOf, create});
  if (typeof module === 'object' && module.exports) module.exports = api;
  else scope.ClassificationBrowser = api;
})(typeof globalThis === 'object' ? globalThis : this);
