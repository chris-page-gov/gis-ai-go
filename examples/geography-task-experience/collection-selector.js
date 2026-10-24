/* Source-only collection selection. Host supplies reviewed JSON by an exact ID. */
(function (scope) {
  'use strict';
  const SCHEMA = 'gis-ai-go.classification-collections.v1';
  const MAX_BYTES = 16 * 1024 * 1024, CATALOGUE_BYTES = 32768;
  const TIMEOUT_MS = 30000, MAX_UNSETTLED = 2;
  const ERROR_TEXT = Object.freeze({
    'unknown-collection': 'That collection is not in the supplied catalogue.',
    'load-refused': 'The host could not supply this collection.',
    'oversize-payload': 'The collection exceeds the 16 MiB display-input limit.',
    'invalid-payload': 'The collection does not satisfy the code-list contract.',
    'count-mismatch': 'The supplied collection counts differ from its catalogue entry.',
    'display-refused': 'The collection could not be prepared for display.',
    'load-timeout': 'The collection was not ready within 30 seconds.',
    'load-capacity': 'Earlier host loads have not settled. Wait before selecting another collection.',
    cancelled: 'Collection selection cancelled.',
    disposed: 'Collection selection is stopped.',
    'inactive-collection': 'Choose this collection before applying its contextual search.',
    'invalid-filter': 'The contextual search was refused.'
  });
  const throwCode = code => { throw Object.freeze({selectorCode: code}); };
  const own = (x, k) => Object.prototype.hasOwnProperty.call(x, k);
  function closed(value, required, optional = []) {
    if (value === null || typeof value !== 'object' || Array.isArray(value)) throwCode('invalid-payload');
    // Use each own data descriptor once: callbacks cannot change values after validation.
    const descriptors = Object.getOwnPropertyDescriptors(value), snapshot = Object.create(null);
    for (const key of Reflect.ownKeys(descriptors)) {
      if (typeof key !== 'string' || (!required.includes(key) && !optional.includes(key))) throwCode('invalid-payload');
      const d = descriptors[key];
      if (!own(d, 'value')) throwCode('invalid-payload');
      snapshot[key] = d.value;
    }
    for (const key of required) if (!own(snapshot, key)) throwCode('invalid-payload');
    return Object.freeze(snapshot);
  }
  function jsonText(text, cap) {
    if (typeof text !== 'string') throwCode('invalid-payload');
    if (text.length > cap || new TextEncoder().encode(text).length > cap) throwCode('oversize-payload');
    try { return JSON.parse(text); } catch (_) { throwCode('invalid-payload'); }
  }
  function catalogue(text) {
    const p = closed(jsonText(text, CATALOGUE_BYTES), ['schema', 'globalComplete', 'collections']);
    if (p.schema !== SCHEMA || p.globalComplete !== false || !Array.isArray(p.collections) || p.collections.length < 1 || p.collections.length > 8) throwCode('invalid-payload');
    const seen = new Set();
    const collections = p.collections.map(raw => {
      const c = closed(raw, ['id', 'title', 'scopeNote', 'schemeCount', 'entryCount', 'coverage']);
      if (typeof c.id !== 'string' || !/^[a-z][a-z0-9-]{0,47}$/u.test(c.id) || seen.has(c.id)) throwCode('invalid-payload');
      for (const [key, max] of [['title', 200], ['scopeNote', 2000]]) {
        if (typeof c[key] !== 'string' || !c[key].trim() || c[key].length > max) throwCode('invalid-payload');
      }
      if (!Number.isSafeInteger(c.schemeCount) || c.schemeCount < 1 || c.schemeCount > 64 || !Number.isSafeInteger(c.entryCount) || c.entryCount < 0 || c.entryCount > 1280000 || c.coverage !== 'selected-sources-only') throwCode('invalid-payload');
      seen.add(c.id); return c;
    });
    return Object.freeze({schema: SCHEMA, globalComplete: false, collections: Object.freeze(collections)});
  }
  function finiteCode(error, fallback) {
    try {
      const d = Object.getOwnPropertyDescriptor(error, 'selectorCode');
      if (d && own(d, 'value') && typeof d.value === 'string' && own(ERROR_TEXT, d.value)) return d.value;
    } catch (_) { /* Host exception text and accessors are never displayed. */ }
    return fallback;
  }
  function create(root, catalogueText, initialId, initialText, options) {
    const config = closed(options, ['loadCollection'], ['document', 'idPrefix']);
    if (typeof config.loadCollection !== 'function') throwCode('invalid-payload');
    const load = config.loadCollection, doc = config.document || root.ownerDocument;
    const prefix = config.idPrefix === undefined ? 'classification-collections' : config.idPrefix;
    if (typeof prefix !== 'string' || !/^[a-z][a-z0-9-]{0,59}$/u.test(prefix)) throwCode('invalid-payload');
    const book = catalogue(catalogueText), byId = new Map(book.collections.map(c => [c.id, c]));
    if (typeof initialId !== 'string' || !byId.has(initialId)) throwCode('unknown-collection');
    const widget = scope.ClassificationBrowser;
    if (!widget || typeof widget.create !== 'function' || typeof widget.validate !== 'function') throwCode('display-refused');
    const el = (tag, text) => { const n = doc.createElement(tag); if (text !== undefined) n.textContent = text; return n; };
    function prepare(id, text) {
      const payload = jsonText(text, MAX_BYTES);
      try { widget.validate(payload); } catch (_) { throwCode('invalid-payload'); }
      const expected = byId.get(id);
      if (payload.schemes.length !== expected.schemeCount || payload.schemes.reduce((n, s) => n + s.entries.length, 0) !== expected.entryCount) throwCode('count-mismatch');
      const node = el('section'); node.setAttribute('aria-label', 'Active collection code lists');
      let api;
      try { api = widget.create(node, payload, {document: doc, idPrefix: prefix + '-data'}); }
      catch (_) { throwCode('display-refused'); }
      return {node, api};
    }
    // Complete initial validation and detached rendering before touching the supplied root.
    let activeId = initialId, active = prepare(initialId, initialText);
    let pending = null, serial = 0, unsettled = 0, disposed = false;
    const label = el('label', 'Collection'), select = el('select');
    label.htmlFor = prefix + '-select'; select.id = label.htmlFor;
    for (const c of book.collections) { const o = el('option', c.title + ' — ' + c.schemeCount + ' schemes, ' + c.entryCount + ' entries'); o.value = c.id; select.append(o); }
    select.value = activeId;
    const scopeNote = el('p'), status = el('p'), cancelButton = el('button', 'Cancel selection');
    const scopeDetails = el('details'), scopeSummary = el('summary', 'Scope and search limits'), scopeContext = el('p');
    scopeDetails.className = 'classification-collection-scope';
    scopeDetails.append(scopeSummary, scopeContext, el('p', 'Coverage is limited to selected sources; global search and overall vocabulary completeness are not provided.'));
    scopeNote.id = prefix + '-scope'; select.setAttribute('aria-describedby', scopeNote.id);
    status.id = prefix + '-status'; status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite'); status.setAttribute('aria-atomic', 'true');
    cancelButton.type = 'button'; cancelButton.disabled = true;
    const display = el('div'); display.append(active.node);
    function describe() {
      const c = byId.get(activeId);
      scopeNote.textContent = 'Active collection: ' + c.title + '. ' + c.schemeCount + ' supplied schemes; ' + c.entryCount + ' retained entry occurrences. Search covers the active collection.';
      scopeContext.textContent = c.scopeNote;
    }
    function announce(code) {
      status.textContent = ERROR_TEXT[code] + ' The displayed collection remains ' + byId.get(activeId).title + '.';
    }
    const result = (ok, code, id) => Object.freeze({ok, code, collectionId: id, activeCollectionId: activeId});
    function settle(job, code, ok = false) {
      if (job.settled) return;
      job.settled = true; clearTimeout(job.timer); job.resolve(result(ok, code, job.id));
    }
    function retire(code) {
      const old = pending; pending = null;
      if (old) { settle(old, code); old.abort.abort(); }
    }
    function failCurrent(job, code) {
      if (pending !== job || disposed) return;
      const version = serial;
      retire(code);
      // An abort listener is host code and may have requested a newer selection.
      if (serial !== version || disposed) return;
      cancelButton.disabled = true; select.value = activeId; announce(code);
    }
    function expired(job) { return performance.now() - job.started >= TIMEOUT_MS; }
    function selectCollection(id) {
      if (disposed) return Promise.resolve(result(false, 'disposed', null));
      if (typeof id !== 'string' || !byId.has(id)) { announce('unknown-collection'); select.value = pending ? pending.id : activeId; return Promise.resolve(result(false, 'unknown-collection', null)); }
      const version = ++serial;
      retire('superseded');
      if (serial !== version || disposed) return Promise.resolve(result(false, disposed ? 'disposed' : 'superseded', id));
      if (id === activeId) { cancelButton.disabled = true; select.value = activeId; status.textContent = 'The selected collection is already displayed.'; return Promise.resolve(result(true, 'already-active', id)); }
      if (unsettled >= MAX_UNSETTLED) { cancelButton.disabled = true; select.value = activeId; announce('load-capacity'); return Promise.resolve(result(false, 'load-capacity', id)); }
      let resolve;
      const promise = new Promise(r => { resolve = r; });
      const job = {id, resolve, settled: false, abort: new AbortController(), started: performance.now(), timer: null};
      pending = job; select.value = id; cancelButton.disabled = false;
      status.textContent = 'Loading ' + byId.get(id).title + '. Search still covers the displayed collection: ' + byId.get(activeId).title + '.';
      job.timer = setTimeout(() => failCurrent(job, 'load-timeout'), TIMEOUT_MS);
      unsettled++;
      let supplied;
      try { supplied = load(id, Object.freeze({signal: job.abort.signal})); }
      catch (_) { unsettled--; failCurrent(job, 'load-refused'); return promise; }
      Promise.resolve(supplied).then(text => {
        unsettled--;
        if (pending !== job || disposed) return;
        if (expired(job)) { failCurrent(job, 'load-timeout'); return; }
        let next;
        try { next = prepare(id, text); } catch (error) { failCurrent(job, finiteCode(error, 'invalid-payload')); return; }
        if (pending !== job || disposed) return;
        if (expired(job)) { failCurrent(job, 'load-timeout'); return; }
        // Only the widget leaf is replaced; task, pin, fold, route and glossary owners are untouched.
        try { display.replaceChildren(next.node); } catch (_) { failCurrent(job, 'display-refused'); return; }
        activeId = id; active = next; pending = null; cancelButton.disabled = true; select.value = id;
        describe(); status.textContent = 'Collection ready. Search covers the active collection.';
        settle(job, 'selected', true);
      }, () => { unsettled--; failCurrent(job, 'load-refused'); });
      return promise;
    }
    function cancel() {
      if (disposed) return result(false, 'disposed', null);
      const version = ++serial; retire('cancelled');
      if (serial === version && !disposed) { cancelButton.disabled = true; select.value = activeId; announce('cancelled'); }
      return result(false, 'cancelled', null);
    }
    function snapshot() {
      const w = active.api.snapshot();
      return Object.freeze({activeCollectionId: activeId, pendingCollectionId: pending ? pending.id : null, disposed,
        widget: Object.freeze({schemeId: w.schemeId, query: w.query, page: w.page,
          selected: w.selected ? Object.freeze({collectionId: activeId, schemeId: w.selected.schemeId, entryId: w.selected.entryId}) : null})});
    }
    function setFilter(collectionId, query, schemeId = '') {
      if (disposed) return result(false, 'disposed', null);
      if (collectionId !== activeId) { announce('inactive-collection'); return result(false, 'inactive-collection', null); }
      if (typeof query !== 'string' || typeof schemeId !== 'string') { announce('invalid-filter'); return result(false, 'invalid-filter', activeId); }
      try { active.api.setFilter(query, schemeId); } catch (_) { announce('invalid-filter'); return result(false, 'invalid-filter', activeId); }
      return result(true, 'filter-applied', activeId);
    }
    function focusSearch(collectionId) {
      if (disposed || collectionId !== activeId) return false;
      active.api.elements.search.focus(); return true;
    }
    function dispose() {
      if (disposed) return;
      disposed = true; serial++; retire('disposed'); select.disabled = true; cancelButton.disabled = true; announce('disposed');
    }
    select.addEventListener('change', () => { void selectCollection(select.value); });
    cancelButton.addEventListener('click', cancel);
    describe(); status.textContent = 'Collection ready. Search covers the active collection.';
    root.replaceChildren(label, select, scopeNote, scopeDetails, status, cancelButton, display);
    return Object.freeze({selectCollection, cancel, setFilter, focusSearch, snapshot, dispose,
      elements: Object.freeze({select, scopeNote, status, cancel: cancelButton, display})});
  }
  const api = Object.freeze({SCHEMA, MAX_BYTES, CATALOGUE_BYTES, TIMEOUT_MS, MAX_UNSETTLED, catalogue, create});
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else scope.ClassificationCollections = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
