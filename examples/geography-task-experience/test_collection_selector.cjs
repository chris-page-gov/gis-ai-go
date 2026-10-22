'use strict';
const assert = require('node:assert/strict'), fs = require('node:fs'), vm = require('node:vm'), path = require('node:path');
const fixture = require('./synthetic-collections.cjs');
const [A, B, C, D, E] = fixture.IDS;
const local = x => JSON.parse(JSON.stringify(x));
const tree = n => [n, ...n.children.flatMap(tree)], text = n => tree(n).map(x => x.textContent).join(' ');
const tick = async () => { await Promise.resolve(); await Promise.resolve(); };
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return {promise, resolve, reject}; };
let checks = 0;
async function check(name, fn) { await fn(); checks++; process.stdout.write('PASS ' + name + '\n'); }
function environment(loader, transformCatalogue, transformInitial) {
  let now = 0, timerId = 0, focused = null, network = 0;
  const timers = new Map(), nodes = {}, events = {};
  class Element {
    constructor(tag) { this.tag = tag; this.children = []; this.attrs = {}; this.listeners = {}; this.textContent = ''; this.value = ''; this.dataset = {}; this.hidden = false; this.ownerDocument = doc; this.classList = {add(){}, toggle(){}}; }
    set id(v) { this._id = v; nodes[v] = this; } get id() { return this._id; }
    append(...n) { this.children.push(...n); }
    replaceChildren(...n) { if (this.refuseReplacement) throw Error('synthetic host refusal'); this.children = n; }
    setAttribute(k, v) { this.attrs[k] = String(v); }
    addEventListener(k, fn) { this.listeners[k] = fn; }
    focus() { focused = this; }
    set innerHTML(_) { throw Error('HTML forbidden'); }
  }
  const doc = {createElement: tag => new Element(tag), body: {dataset: {}}};
  const context = vm.createContext({TextEncoder, URL, AbortController, AbortSignal,
    performance: {now: () => now}, setTimeout(fn, delay) { const id = ++timerId; timers.set(id, {fn, at: now + delay}); return id; }, clearTimeout(id) { timers.delete(id); },
    document: doc, fetch() { network++; throw Error('Network forbidden'); },
    location: {hash: ''}, history: {pushState(_a, _b, hash) { context.location.hash = hash; }},
    window: {addEventListener(k, fn) { events[k] = fn; }, matchMedia: () => ({matches: false})}});
  for (const file of ['classification-browser.js', 'collection-selector.js']) vm.runInContext(fs.readFileSync(path.join(__dirname, file), 'utf8'), context, {timeout: 5000});
  const calls = [], api = context.ClassificationCollections;
  const book = fixture.catalogue(), initial = fixture.payload(A);
  if (transformCatalogue) transformCatalogue(book);
  if (transformInitial) transformInitial(initial);
  const root = doc.createElement('section');
  const ui = api.create(root, JSON.stringify(book), A, JSON.stringify(initial), {document: doc, loadCollection(id, options) { calls.push({id, signal: options.signal}); return loader ? loader(id, options) : JSON.stringify(fixture.payload(id)); }});
  function advance(ms, runTimers = true) { now += ms; if (runTimers) for (const [id, t] of [...timers]) if (t.at <= now) { timers.delete(id); t.fn(); } }
  function overlay() {
    const contract = JSON.parse(fs.readFileSync(path.join(__dirname, 'OVERLAY-CONTRACT.v1.json'), 'utf8'));
    for (const id of contract.requiredHostIds) { nodes[id] = doc.createElement('div'); nodes[id].id = id; }
    const panels = contract.taskIds.map(id => { nodes['task-' + id] = doc.createElement('section'); nodes['task-' + id].id = 'task-' + id; nodes['title-' + id] = doc.createElement('h2'); return nodes['task-' + id]; });
    const nav = contract.taskIds.map(id => { const n = doc.createElement('button'); n.dataset.task = id; return n; });
    const tabs = contract.referenceIds.map(id => { const n = nodes['ref-tab-' + id] = doc.createElement('button'); n.dataset.reference = id; nodes['ref-panel-' + id] = doc.createElement('section'); return n; });
    const skip = doc.createElement('a');
    doc.querySelectorAll = s => ({'.task-panel': panels, '[data-task]': nav, '#task-navigator [data-task]': nav, '[data-reference]': tabs, '.skip-link[href="#reference-heading"]': [skip]}[s] || []);
    context.$ = id => { assert.ok(nodes[id], id); return nodes[id]; };
    context.el = (tag, value, cls) => { const n = doc.createElement(tag); if (value !== undefined) n.textContent = value; n.className = cls; return n; };
    vm.runInContext(fs.readFileSync(path.join(__dirname, 'shared_actions.js'), 'utf8'), context);
    const source = fs.readFileSync(path.join(__dirname, 'experience.js'), 'utf8').replace('__VOCABULARY_REGISTRY__', JSON.stringify({sources: [], terms: []}));
    vm.runInContext(source, context); nodes['learning-persona'].value = 'resident'; vm.runInContext('initialiseExperience()', context);
    nodes['ref-panel-codelists'].append(root);
    return {run: s => vm.runInContext(s, context), nodes, events, nav, tabs, skip};
  }
  return {ui, api, root, doc, context, calls, timers, nodes, advance, overlay, focused: () => focused, network: () => network};
}
(async () => {
  await check('five explicit fictional collections, counts and active-search scope', () => {
    const e = environment(); assert.equal(e.ui.elements.select.children.length, 5); assert.equal(e.calls.length, 0);
    assert.match(text(e.root), /Search covers the active collection/); assert.match(text(e.root), /26 retained entry occurrences/);
    assert.match(text(e.root), /global search.*not provided/); assert.equal(e.ui.elements.select.attrs['aria-describedby'], e.ui.elements.scopeNote.id);
    assert.equal(e.ui.elements.status.attrs['aria-live'], 'polite'); assert.equal(e.ui.elements.cancel.type, 'button');
  });
  await check('exact-ID loader receives only an AbortSignal and no arbitrary route', async () => {
    const e = environment(); const r = await e.ui.selectCollection(B); assert.equal(r.ok, true); assert.equal(r.code, 'selected');
    assert.equal(e.calls.length, 1); assert.equal(e.calls[0].id, B); assert.equal(e.calls[0].signal.aborted, false);
    assert.equal(e.ui.snapshot().activeCollectionId, B); assert.match(text(e.root), /Fictional edition for ngd-batch-example-1/); assert.equal(e.network(), 0);
  });
  await check('unknown and prototype-like IDs refuse before loader', async () => {
    const e = environment(); for (const id of ['constructor', '__proto__', 'toString', 'https://example.invalid/list', {}, null]) assert.equal((await e.ui.selectCollection(id)).code, 'unknown-collection');
    assert.equal(e.calls.length, 0); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('load failure preserves exact displayed widget, selected entry and open disclosure', async () => {
    const e = environment(() => Promise.reject(Error('private host text'))); e.ui.setFilter(A, '001');
    const leaf = e.ui.elements.display.children[0], list = tree(leaf).find(n => n.className === 'classification-results');
    list.children[0].children[0].listeners.click(); const disclosure = tree(leaf).find(n => n.tag === 'details'); disclosure.open = true;
    const before = local(e.ui.snapshot()); assert.equal((await e.ui.selectCollection(B)).code, 'load-refused');
    assert.equal(e.ui.elements.display.children[0], leaf); assert.deepEqual(local(e.ui.snapshot()), before); assert.equal(disclosure.open, true);
    assert.ok(!text(e.root).includes('private host text')); assert.equal(e.ui.elements.select.value, A);
  });
  await check('invalid schema and count mismatch leave old collection unchanged', async () => {
    for (const [change, code] of [[p => { p.globalComplete = true; }, 'invalid-payload'], [p => { p.schemes.pop(); }, 'count-mismatch']]) {
      const p = fixture.payload(B); change(p); const e = environment(() => JSON.stringify(p)), old = e.ui.elements.display.children[0];
      assert.equal((await e.ui.selectCollection(B)).code, code); assert.equal(e.ui.elements.display.children[0], old); assert.equal(e.ui.snapshot().activeCollectionId, A);
    }
  });
  await check('raw UTF-8 byte cap refuses multi-byte text below character cap', async () => {
    const e = environment(() => 'é'.repeat(8388609)); assert.equal((await e.ui.selectCollection(B)).code, 'oversize-payload'); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('malformed JSON and non-string loader returns refuse without evaluating getters', async () => {
    let reads = 0; for (const value of ['{', {get schema() { reads++; throw Error('private'); }}, new Uint8Array(4)]) {
      const e = environment(() => value); assert.equal((await e.ui.selectCollection(B)).code, 'invalid-payload');
    } assert.equal(reads, 0);
  });
  await check('64 scheme limit is unchanged and 65 refuses', async () => {
    const p = fixture.payload(B), base = p.schemes[0]; p.schemes = Array.from({length: 65}, (_, i) => ({...base, id: 'scheme-' + i}));
    const e = environment(() => JSON.stringify(p)); assert.equal((await e.ui.selectCollection(B)).code, 'invalid-payload');
    assert.throws(() => environment(null, c => { c.collections[1].schemeCount = 65; }));
  });
  await check('stale async success cannot overwrite newer successful selection', async () => {
    const b = deferred(), c = deferred(); const e = environment(id => id === B ? b.promise : c.promise);
    const first = e.ui.selectCollection(B), second = e.ui.selectCollection(C); assert.equal((await first).code, 'superseded'); assert.equal(e.calls[0].signal.aborted, true);
    c.resolve(JSON.stringify(fixture.payload(C))); assert.equal((await second).ok, true); b.resolve(JSON.stringify(fixture.payload(B))); await tick();
    assert.equal(e.ui.snapshot().activeCollectionId, C); assert.match(e.ui.elements.scopeNote.textContent, /NGD batch 2/);
  });
  await check('stale rejection does not replace latest status', async () => {
    const b = deferred(); const e = environment(id => id === B ? b.promise : JSON.stringify(fixture.payload(id)));
    const first = e.ui.selectCollection(B); await e.ui.selectCollection(C); b.reject(Error('stale private failure')); await tick(); await first;
    assert.equal(e.ui.elements.status.textContent, 'Collection ready. Search covers the active collection.'); assert.equal(e.ui.snapshot().activeCollectionId, C);
  });
  await check('cancel is immediate even if host ignores abort; late result is discarded', async () => {
    const b = deferred(), e = environment(() => b.promise), old = e.ui.elements.display.children[0]; const promise = e.ui.selectCollection(B);
    e.ui.elements.cancel.listeners.click(); assert.equal((await promise).code, 'cancelled'); assert.equal(e.calls[0].signal.aborted, true);
    b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal(e.ui.elements.display.children[0], old); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('same active choice cancels pending and preserves existing filters', async () => {
    const b = deferred(), e = environment(() => b.promise); e.ui.setFilter(A, '001'); const first = e.ui.selectCollection(B);
    assert.equal((await e.ui.selectCollection(A)).code, 'already-active'); assert.equal((await first).code, 'superseded'); assert.equal(e.ui.snapshot().widget.query, '001'); assert.equal(e.calls.length, 1);
    b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('timeout closes UI request, aborts signal and retains current collection', async () => {
    const b = deferred(), e = environment(() => b.promise), promise = e.ui.selectCollection(B); e.advance(30000);
    assert.equal((await promise).code, 'load-timeout'); assert.equal(e.calls[0].signal.aborted, true); assert.equal(e.ui.snapshot().activeCollectionId, A); assert.equal(e.timers.size, 0);
    b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('late synchronous host work refuses even before timer callback runs', async () => {
    let e; e = environment(() => { e.advance(30000, false); return JSON.stringify(fixture.payload(B)); });
    assert.equal((await e.ui.selectCollection(B)).code, 'load-timeout'); assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('at most two unsettled host loads; capacity reopens only after settlement', async () => {
    const b = deferred(), c = deferred(), e = environment(id => id === B ? b.promise : id === C ? c.promise : JSON.stringify(fixture.payload(id)));
    const first = e.ui.selectCollection(B), second = e.ui.selectCollection(C); assert.equal((await e.ui.selectCollection(D)).code, 'load-capacity'); assert.equal(e.calls.length, 2);
    await first; await second; b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal((await e.ui.selectCollection(D)).ok, true);
    c.resolve(JSON.stringify(fixture.payload(C))); await tick(); assert.equal(e.ui.snapshot().activeCollectionId, D);
  });
  await check('dispose settles outstanding request and prevents later loader/effects', async () => {
    const b = deferred(), e = environment(() => b.promise); const p = e.ui.selectCollection(B); e.ui.dispose();
    assert.equal((await p).code, 'disposed'); assert.equal((await e.ui.selectCollection(C)).code, 'disposed'); assert.equal(e.calls.length, 1); assert.equal(e.ui.elements.select.disabled, true);
    b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal(e.ui.snapshot().activeCollectionId, A); assert.equal(e.ui.snapshot().disposed, true);
  });
  await check('same scheme/entry/code IDs in other collections remain separate', async () => {
    const e = environment(); function pick() { e.ui.setFilter(e.ui.snapshot().activeCollectionId, '000', 'fictional-a'); const list = tree(e.ui.elements.display).find(n => n.className === 'classification-results'); list.children[0].children[0].listeners.click(); }
    pick(); const first = local(e.ui.snapshot().widget.selected); await e.ui.selectCollection(B); pick(); const second = local(e.ui.snapshot().widget.selected);
    assert.equal(first.schemeId, second.schemeId); assert.equal(first.entryId, second.entryId); assert.equal(first.collectionId, A); assert.equal(second.collectionId, B);
    assert.ok(text(e.ui.elements.display).includes('Distinct fictional label for ' + B)); assert.ok(!text(e.ui.elements.display).includes('Distinct fictional label for ' + A));
  });
  await check('contextual search requires active collection identity', async () => {
    const e = environment(); assert.equal(e.ui.setFilter(B, '001').code, 'inactive-collection'); assert.equal(e.ui.snapshot().widget.query, '');
    assert.equal(e.ui.setFilter(A, '001').ok, true); assert.equal(e.ui.focusSearch(B), false); assert.equal(e.ui.focusSearch(A), true); assert.equal(e.focused().type, 'search');
    assert.equal(e.ui.setFilter(A, '001', 'unknown-scheme').code, 'invalid-filter'); assert.equal(e.ui.snapshot().widget.query, '001');
  });
  await check('non-string contextual query or scheme refuses without changing the active widget', () => {
    const e = environment(); e.ui.setFilter(A, '001', 'fictional-a'); const before = JSON.stringify(e.ui.snapshot());
    for (const value of [false, null, 0, {}, [], undefined]) {
      // Explicit undefined follows JavaScript's documented default scheme argument; test query only for it.
      if (value !== undefined) assert.equal(e.ui.setFilter(A, '002', value).code, 'invalid-filter');
      assert.equal(e.ui.setFilter(A, value, 'fictional-a').code, 'invalid-filter');
      assert.equal(JSON.stringify(e.ui.snapshot()), before);
    }
  });
  await check('closed catalogue refuses extra URLs, duplicate IDs and false completeness', () => {
    for (const mutate of [c => { c.collections[0].url = 'https://example.invalid'; }, c => { c.collections[1].id = c.collections[0].id; }, c => { c.globalComplete = true; }, c => { c.collections[0].entryCount = -1; }, c => { c.collections = Array(9).fill(c.collections[0]); }]) assert.throws(() => environment(null, mutate));
  });
  await check('invalid initial input does not mutate supplied root', () => {
    const e = environment(), root = e.doc.createElement('section'), old = e.doc.createElement('p'); root.append(old);
    assert.throws(() => e.api.create(root, JSON.stringify(fixture.catalogue()), A, '{}', {document: e.doc, loadCollection() { throw Error('unused'); }})); assert.equal(root.children[0], old);
  });
  await check('refused final DOM replacement leaves original display and closes loading state', async () => {
    const e = environment(), old = e.ui.elements.display.children[0]; e.ui.elements.display.refuseReplacement = true;
    assert.equal((await e.ui.selectCollection(B)).code, 'display-refused'); assert.equal(e.ui.elements.display.children[0], old);
    assert.equal(e.ui.snapshot().pendingCollectionId, null); assert.equal(e.ui.snapshot().activeCollectionId, A); assert.equal(e.ui.elements.cancel.disabled, true);
  });
  await check('a pending load leaves existing search and paging usable', async () => {
    const b = deferred(), e = environment(() => b.promise), old = e.ui.elements.display.children[0]; const p = e.ui.selectCollection(B);
    const next = tree(old).find(n => n.attrs['aria-label'] === 'Next page of code-list results'); next.listeners.click(); assert.equal(e.ui.snapshot().widget.page, 1);
    assert.equal(e.ui.setFilter(A, '001').ok, true); assert.equal(e.ui.snapshot().widget.query, '001'); assert.match(e.ui.elements.status.textContent, /Search still covers the displayed collection/);
    e.ui.cancel(); await p; b.resolve(JSON.stringify(fixture.payload(B))); await tick(); assert.equal(e.ui.snapshot().widget.query, '001');
  });
  await check('catalogue byte cap is separate and invalid input is never treated as URL', () => {
    const e = environment(); assert.throws(() => e.api.catalogue(' '.repeat(32769)));
    assert.throws(() => e.api.catalogue('https://example.invalid/catalogue.json')); assert.equal(e.network(), 0);
  });
  await check('catalogue snapshot is immutable; options accessors are not called', () => {
    const e = environment(), book = e.api.catalogue(JSON.stringify(fixture.catalogue())); assert.ok(Object.isFrozen(book.collections)); assert.ok(Object.isFrozen(book.collections[0]));
    let reads = 0; assert.throws(() => e.api.create(e.doc.createElement('section'), JSON.stringify(fixture.catalogue()), A, JSON.stringify(fixture.payload(A)), {get loadCollection() { reads++; return () => ''; }})); assert.equal(reads, 0);
  });
  await check('host exception getters and text never reach UI or escape', async () => {
    let reads = 0; const error = {get selectorCode() { reads++; throw Error('private'); }, get message() { reads++; throw Error('private'); }};
    const e = environment(() => { throw error; }); assert.equal((await e.ui.selectCollection(B)).code, 'load-refused'); assert.equal(reads, 0); assert.ok(!text(e.root).includes('private'));
  });
  await check('native select change starts the exact chosen collection', async () => {
    const e = environment(); e.ui.elements.select.value = E; e.ui.elements.select.listeners.change(); await tick(); assert.equal(e.ui.snapshot().activeCollectionId, E); assert.equal(e.calls[0].id, E);
  });
  await check('no focus steal after async selection', async () => {
    const b = deferred(), e = environment(() => b.promise), other = e.doc.createElement('button'); const p = e.ui.selectCollection(B); other.focus(); b.resolve(JSON.stringify(fixture.payload(B))); await p; assert.equal(e.focused(), other);
  });
  await check('host abort callback reentrancy cannot overwrite a newer request', async () => {
    const b = deferred(); let e, nested;
    e = environment((id, options) => { if (id === B) { options.signal.addEventListener('abort', () => { nested = e.ui.selectCollection(D); }, {once: true}); return b.promise; } return JSON.stringify(fixture.payload(id)); });
    const first = e.ui.selectCollection(B); assert.equal((await e.ui.selectCollection(C)).code, 'superseded'); await nested; await first;
    assert.equal(e.ui.snapshot().activeCollectionId, D); assert.deepEqual(e.calls.map(c => c.id), [B, D]); b.resolve(JSON.stringify(fixture.payload(B))); await tick();
  });
  await check('real overlay pin/fold/task/history controls coexist with collection switching', async () => {
    const e = environment(), o = e.overlay(); o.run("experienceReferenceTab('codelists'); experienceSetPinned(true); experienceShow('areas',false)");
    e.ui.setFilter(A, '001'); const old = e.ui.elements.display.children[0]; o.run("experienceFold('reference',false); experienceShow('groups',false); experienceFold('reference',true)");
    assert.equal(e.ui.elements.display.children[0], old); assert.equal(e.ui.snapshot().widget.query, '001'); const route = e.context.location.hash;
    await e.ui.selectCollection(B); assert.equal(o.run('experiencePinned'), true); assert.equal(o.run('experienceReference'), 'codelists'); assert.equal(o.run('experienceTask'), 'groups'); assert.equal(e.context.location.hash, route);
    o.nodes['ref-tab-codelists'].listeners.keydown({key: 'ArrowRight', preventDefault(){}}); assert.equal(e.focused(), o.nodes['ref-tab-context']);
    e.context.location.hash = '#task/areas'; o.events.popstate(); assert.equal(o.run('experienceTask'), 'areas'); assert.equal(e.ui.snapshot().activeCollectionId, B); assert.equal(e.network(), 0);
  });
  await check('text remains inert and module has no fetch/HTML/storage/route facility', async () => {
    const p = fixture.payload(B); p.schemes[0].entries[0].label = '<img src=x onerror=bad>';
    const e = environment(() => JSON.stringify(p)); await e.ui.selectCollection(B); assert.ok(text(e.root).includes('<img src=x onerror=bad>')); assert.equal(tree(e.root).filter(n => ['img', 'script'].includes(n.tag)).length, 0);
    const source = fs.readFileSync(path.join(__dirname, 'collection-selector.js'), 'utf8'); assert.ok(!/\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage|innerHTML|insertAdjacentHTML|pushState)\s*[.(=]/u.test(source));
  });
  await check('scope line stays visible with active identity/counts while complete caveats are in native details', () => {
    const e = environment(), d = e.root.children.find(n => n.className === 'classification-collection-scope');
    assert.equal(d.tag, 'details'); assert.equal(d.children[0].tag, 'summary'); assert.equal(d.children[0].textContent, 'Scope and search limits');
    assert.notEqual(d.open, true); assert.equal(Object.hasOwn(d.attrs, 'open'), false);
    assert.match(e.ui.elements.scopeNote.textContent, /^Active collection: Selected journey/);
    assert.match(e.ui.elements.scopeNote.textContent, /2 supplied schemes; 26 retained entry occurrences/);
    assert.match(e.ui.elements.scopeNote.textContent, /Search covers the active collection\.$/);
    assert.ok(!e.ui.elements.scopeNote.textContent.includes('Fictional fixture only'));
    assert.equal(d.children[1].textContent, fixture.catalogue().collections[0].scopeNote);
    assert.equal(d.children[2].textContent, 'Coverage is limited to selected sources; global search and overall vocabulary completeness are not provided.');
    assert.equal(e.ui.elements.select.attrs['aria-describedby'], e.ui.elements.scopeNote.id);
    assert.equal(e.root.children.indexOf(d), e.root.children.indexOf(e.ui.elements.scopeNote) + 1);
  });
  await check('native summary keeps browser keyboard ownership with no custom role or toggle handlers', () => {
    const e = environment(), d = e.root.children.find(n => n.className === 'classification-collection-scope'), summary = d.children[0];
    assert.deepEqual(summary.listeners, {}); assert.deepEqual(d.listeners, {});
    for (const a of ['role', 'tabindex', 'aria-expanded']) assert.equal(Object.hasOwn(summary.attrs, a), false);
    summary.focus(); assert.equal(e.focused(), summary); assert.equal(e.calls.length, 0);
    assert.equal(e.ui.snapshot().activeCollectionId, A);
  });
  await check('successful selection updates exact context without replacing disclosure or stealing its focus', async () => {
    const e = environment(undefined, c => { c.collections[1].scopeNote = 'Distinct fictional scope. Native edition remains separate.'; });
    const d = e.root.children.find(n => n.className === 'classification-collection-scope'); d.open = true; d.children[0].focus();
    assert.equal((await e.ui.selectCollection(B)).ok, true);
    assert.equal(e.root.children.find(n => n.className === 'classification-collection-scope'), d);
    assert.equal(d.open, true); assert.equal(e.focused(), d.children[0]);
    assert.equal(d.children[1].textContent, 'Distinct fictional scope. Native edition remains separate.');
    assert.match(e.ui.elements.scopeNote.textContent, /Active collection: NGD batch 1/);
  });
  await check('failed selection keeps original exact scope, native disclosure state and widget', async () => {
    const e = environment(() => Promise.reject(Error('unretained host text')));
    const d = e.root.children.find(n => n.className === 'classification-collection-scope'), old = e.ui.elements.display.children[0];
    d.open = true; const before = text(d), line = e.ui.elements.scopeNote.textContent;
    assert.equal((await e.ui.selectCollection(B)).code, 'load-refused');
    assert.equal(text(d), before); assert.equal(e.ui.elements.scopeNote.textContent, line); assert.equal(d.open, true);
    assert.equal(e.ui.elements.display.children[0], old); assert.ok(!text(e.root).includes('unretained host text'));
  });
  await check('pending and cancelled stale loads never publish the candidate scope', async () => {
    const pending = deferred(), e = environment(() => pending.promise, c => { c.collections[1].scopeNote = 'Not yet accepted scope'; });
    const d = e.root.children.find(n => n.className === 'classification-collection-scope'), before = text(d), line = e.ui.elements.scopeNote.textContent;
    const result = e.ui.selectCollection(B); assert.equal(text(d), before); assert.equal(e.ui.elements.scopeNote.textContent, line);
    e.ui.cancel(); assert.equal((await result).code, 'cancelled'); pending.resolve(JSON.stringify(fixture.payload(B))); await tick();
    assert.equal(text(d), before); assert.equal(e.ui.elements.scopeNote.textContent, line); assert.ok(!text(d).includes('Not yet accepted scope'));
  });
  await check('full permitted scope text remains exact and inert without length-driven truncation', () => {
    const native = '<script>fictional</script> ' + 'x'.repeat(1973);
    assert.equal(native.length, 2000);
    const e = environment(undefined, c => { c.collections[0].scopeNote = native; });
    const d = e.root.children.find(n => n.className === 'classification-collection-scope');
    assert.equal(d.children[1].textContent, native); assert.equal(tree(d).some(n => ['script', 'img'].includes(n.tag)), false);
    assert.ok(e.ui.elements.scopeNote.textContent.length < 250); assert.equal(e.network(), 0);
  });
  await check('same active collection and task/pin/fold history preserve disclosure state', async () => {
    const e = environment(), d = e.root.children.find(n => n.className === 'classification-collection-scope'); d.open = true;
    const o = e.overlay(); o.run("experienceReferenceTab('codelists'); experienceSetPinned(true); experienceShow('areas',false)");
    o.run("experienceFold('reference',false); experienceShow('groups',false); experienceFold('reference',true)");
    assert.equal((await e.ui.selectCollection(A)).code, 'already-active');
    assert.equal(d.open, true); assert.equal(e.root.children.find(n => n.className === 'classification-collection-scope'), d);
    assert.equal(o.run('experiencePinned'), true); assert.equal(o.run('experienceReference'), 'codelists');
    e.context.location.hash = '#task/areas'; o.events.popstate(); assert.equal(o.run('experienceTask'), 'areas'); assert.equal(d.open, true);
  });
  console.log(JSON.stringify({passed: true, checks, actualSupplierPayloads: 0, networkRequests: 0, renderedBrowserAcceptance: false}));
})().catch(error => { console.error(error); process.exitCode = 1; });
