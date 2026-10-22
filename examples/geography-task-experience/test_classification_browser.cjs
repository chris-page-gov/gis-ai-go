'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs'), vm = require('node:vm'), path = require('node:path');
const browserModule = {module: {exports: {}}, TextEncoder, URL};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'classification-browser.js'), 'utf8'), browserModule, {filename: 'classification-browser.js', timeout: 5000});
const api = browserModule.module.exports;
const localValue = value => JSON.parse(JSON.stringify(value));
const {fixture} = require('./synthetic-fixture.cjs');
let focused = null, checks = 0;
class Element {
  constructor(tag, doc) { this.tag = tag; this.ownerDocument = doc; this.children = []; this.attrs = {}; this.listeners = {}; this.textContent = ''; this.value = ''; this.classList = {add() {}}; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  addEventListener(k, fn) { this.listeners[k] = fn; }
  focus() { focused = this; }
  set innerHTML(_) { throw new Error('HTML interpretation is forbidden'); }
}
const document = {createElement: tag => new Element(tag, document)};
const tree = e => [e, ...e.children.flatMap(tree)];
const text = e => tree(e).map(n => n.textContent).join(' ');
const mount = (data = fixture()) => { const root = new Element('section', document); return {root, ui: api.create(root, data)}; };
function check(name, fn) { fn(); checks++; console.log('ok ' + name); }
const mutate = fn => { const data = fixture(); fn(data); return data; };
check('source rows remain immutable', () => { const data = fixture(), before = JSON.stringify(data); mount(data); assert.equal(JSON.stringify(data), before); });
check('bounded first page', () => { const {ui} = mount(); assert.equal(ui.elements.list.children.length, 20); assert.match(ui.elements.count.textContent, /26 matching entries \/ 26 retained/); assert.equal(ui.elements.previous.disabled, true); });
check('all-scheme summaries occupy one folded disclosure before results', () => { const {ui} = mount(); assert.equal(ui.elements.scopeBox.children.length, 1); const group=ui.elements.scopeBox.children[0]; assert.equal(group.tag,'details'); assert.equal(group.open,false); assert.match(group.children[0].textContent,/Coverage, sources and limits for 2 supplied schemes/); assert.match(text(group),/Fictional scheme A/); assert.match(text(group),/Fictional scheme B/); });
check('paging preserves an opened scope disclosure', () => { const {ui} = mount(); const group=ui.elements.scopeBox.children[0]; group.open=true; ui.elements.next.listeners.click(); assert.equal(ui.elements.scopeBox.children[0],group); assert.equal(group.open,true); });
check('scheme selection keeps results ahead of optional scope detail', () => { const {ui} = mount(); ui.setFilter('','fictional-b'); const card=ui.elements.scopeBox.children[0]; assert.equal(card.tag,'details'); assert.equal(card.open,false); assert.match(card.children[0].textContent,/Fictional scheme B/); ui.elements.list.children[0].children[0].listeners.click(); assert.match(text(ui.elements.detail),/Limits for this entry/); assert.match(text(ui.elements.detail),/Different meaning/); });
check('last page and exact counts', () => { const {ui} = mount(); ui.elements.next.listeners.click(); assert.equal(ui.elements.list.children.length, 6); assert.equal(ui.elements.next.disabled, true); assert.match(ui.elements.count.textContent, /Showing 21–26/); ui.elements.previous.listeners.click(); assert.equal(ui.snapshot().page, 0); });
check('search includes source code and preserves leading zeros', () => { const {ui} = mount(); ui.setFilter('001'); assert.equal(ui.elements.list.children.length, 1); assert.match(text(ui.elements.list), /001/); });
check('equal codes across schemes stay separate', () => { const {ui} = mount(); ui.setFilter('000'); assert.equal(ui.elements.list.children.length, 2); assert.match(text(ui.elements.list), /Fictional scheme A/); assert.match(text(ui.elements.list), /Fictional scheme B/); });
check('scheme filter narrows denominator', () => { const {ui} = mount(); ui.setFilter('000', 'fictional-b'); assert.match(ui.elements.count.textContent, /1 matching entries \/ 1 retained in this scheme/); });
check('scheme title is searchable', () => { const {ui} = mount(); ui.setFilter('scheme B'); assert.equal(ui.elements.list.children.length, 1); });
check('source alias searchable with authority intact', () => { const {ui} = mount(); ui.setFilter('shortcut'); ui.elements.list.children[0].children[0].listeners.click(); assert.match(text(ui.elements.detail), /search-variant; project-search-variant/); });
check('search resets page and selection', () => { const {ui} = mount(); ui.elements.next.listeners.click(); ui.elements.search.value = 'not-found'; ui.elements.search.listeners.input(); assert.equal(ui.snapshot().page, 0); assert.equal(ui.elements.list.children.length, 0); assert.match(ui.elements.count.textContent, /No matching/); });
check('scheme selection uses native change and keeps search', () => { const {ui} = mount(); ui.setFilter('000'); ui.elements.select.value = 'fictional-b'; ui.elements.select.listeners.change(); assert.equal(ui.snapshot().query, '000'); assert.equal(ui.elements.list.children.length, 1); });
check('source dates remain separate and uncoerced', () => { const {ui} = mount(); const t = text(ui.elements.scopeBox); for (const x of ['Reference date 2020-04', 'Publication date 2021-01-02', 'Retrieved at 2026-10-21T10:00:00Z', 'Edition or release Synthetic edition 1']) assert.ok(t.includes(x)); });
check('unknown expected count has no percentage or full-scope claim', () => { const {root, ui} = mount(); ui.setFilter('', 'fictional-b'); assert.match(text(ui.elements.scopeBox), /unknown expected count/); assert.ok(!text(root).includes('%')); assert.match(text(root), /Overall vocabulary coverage remains incomplete/); });
check('list completeness and definition completeness separate', () => { const {ui} = mount(); assert.match(text(ui.elements.scopeBox), /Complete selected source list/); assert.match(text(ui.elements.scopeBox), /Mixed or partial source definitions/); });
check('null and empty definition remain distinct', () => { const {ui} = mount(); ui.setFilter('001'); ui.elements.list.children[0].children[0].listeners.click(); assert.match(text(ui.elements.detail), /No definition supplied \(null\)/); ui.setFilter('002'); ui.elements.list.children[0].children[0].listeners.click(); assert.match(text(ui.elements.detail), /Empty string \(supplied\)/); });
check('missing definition refuses rather than becoming null', () => assert.throws(() => mount(mutate(d => delete d.schemes[0].entries[0].definition)), /missing definition/));
check('full native JSON preserves scalar types', () => { const {ui} = mount(); ui.setFilter('001'); ui.elements.list.children[0].children[0].listeners.click(); const pre = tree(ui.elements.detail).find(x => x.tag === 'pre'); assert.deepEqual(JSON.parse(pre.textContent), fixture().schemes[0].entries[1].native); });
check('native markup is inert text including property names', () => { const attack = '<img src=x onerror=alert(1)>'; const {root, ui} = mount(mutate(d => { d.schemes[0].entries[0].label = attack; d.schemes[0].entries[0].native[attack] = '</script><script>alert(1)</script>'; })); ui.setFilter('000', 'fictional-a'); ui.elements.list.children[0].children[0].listeners.click(); assert.ok(text(root).includes(attack)); assert.equal(tree(root).filter(x => ['img', 'script'].includes(x.tag)).length, 0); });
check('unsafe source links are not anchor targets', () => { for (const url of ['javascript:alert(1)', 'http://example.invalid/', 'https://user:pass@example.invalid/', 'https://example.invalid/?sig=secret', 'https://example.invalid/?X-Amz-Signature=secret']) { const {root} = mount(mutate(d => { d.schemes[0].sources[0].url = url; })); assert.equal(tree(root).filter(x => x.tag === 'a' && x.href === url).length, 0); assert.match(text(root), /link withheld/); } });
check('safe links only follow explicit anchors', () => { const {root} = mount(); const links = tree(root).filter(x => x.tag === 'a'); assert.ok(links.length); for (const a of links) { assert.equal(a.href, 'https://example.invalid/source'); assert.equal(a.rel, 'noopener noreferrer'); assert.equal(a.target, '_blank'); } });
check('sourced parent only and keyboard focus on details', () => { const {ui} = mount(); ui.setFilter('001'); ui.elements.list.children[0].children[0].listeners.click(); assert.equal(focused.tag, 'h4'); assert.match(text(ui.elements.detail), /Source-supplied parent: 000/); const button = tree(ui.elements.detail).find(x => x.tag === 'button' && x.textContent === 'Inspect source-supplied parent'); button.listeners.click(); assert.deepEqual(localValue(ui.snapshot().selected), {schemeId: 'fictional-a', entryId: 'entry-0'}); });
check('other exact-code occurrences are lexical comparisons with source identity', () => { const {ui} = mount(); ui.setFilter('000', 'fictional-a'); ui.elements.list.children[0].children[0].listeners.click(); assert.match(text(ui.elements.detail), /Equal codes do not establish equivalent concepts/); const button = tree(ui.elements.detail).find(x => x.tag === 'button' && x.textContent.startsWith('Fictional scheme B:')); button.listeners.click(); assert.deepEqual(localValue(ui.snapshot().selected), {schemeId:'fictional-b',entryId:'entry-0'}); assert.match(text(ui.elements.detail), /Different meaning/); });
check('entry limits and code comparisons start folded with visible counts and caveat', () => {
  const {ui}=mount();ui.setFilter('000','fictional-a');ui.elements.list.children[0].children[0].listeners.click();
  const disclosures=ui.elements.detail.children.filter(x=>x.tag==='details');
  const limits=disclosures.find(x=>x.children[0].textContent.startsWith('Limits for this'));
  const comparisons=disclosures.find(x=>x.children[0].textContent.startsWith('Other occurrences'));
  assert.equal(limits.open,false);assert.match(limits.children[0].textContent,/\(1\)/);assert.ok(text(limits).includes(fixture().schemes[0].gaps[0]));
  assert.equal(comparisons.open,false);assert.match(comparisons.children[0].textContent,/\(1\) — equivalence not established/);
  assert.ok(ui.elements.detail.children.some(x=>x.tag==='dl'&&text(x).includes('Source definition')));
  assert.ok(ui.elements.detail.children.some(x=>x.tag==='a'&&x.href==='https://example.invalid/source'));
});
check('paging preserves an opened entry disclosure and its selected term', () => {
  const {ui}=mount();ui.elements.list.children[0].children[0].listeners.click();const limits=ui.elements.detail.children.find(x=>x.tag==='details');limits.open=true;const selected=localValue(ui.snapshot().selected);
  ui.elements.next.listeners.click();assert.equal(ui.elements.detail.children.find(x=>x.tag==='details'),limits);assert.equal(limits.open,true);assert.deepEqual(localValue(ui.snapshot().selected),selected);
});
check('following a comparison resets disclosures for the new entry and focuses its title', () => {
  const {ui}=mount();ui.setFilter('000','fictional-a');ui.elements.list.children[0].children[0].listeners.click();const comparisons=ui.elements.detail.children.find(x=>x.tag==='details'&&x.children[0].textContent.startsWith('Other occurrences'));comparisons.open=true;
  tree(comparisons).find(x=>x.tag==='button').listeners.click();assert.deepEqual(localValue(ui.snapshot().selected),{schemeId:'fictional-b',entryId:'entry-0'});assert.equal(focused.tag,'h4');assert.match(focused.textContent,/Different meaning/);assert.equal(ui.elements.detail.children.find(x=>x.tag==='details').open,false);
});
check('no prefix hierarchy inferred', () => { const s = fixture().schemes[0]; assert.equal(api.parentOf(s, s.entries[0]).state, 'not-supplied'); assert.equal(api.parentOf(s, s.entries[2]).state, 'unresolved'); });
check('ambiguous and self parent unresolved', () => { const s = fixture().schemes[0]; s.entries[2].code = '000'; assert.equal(api.parentOf(s, s.entries[1]).state, 'unresolved'); s.entries[0].parentCode = '000'; assert.equal(api.parentOf(s, s.entries[0]).state, 'unresolved'); });
check('empty parent is explicit, not null or root', () => { const s = fixture().schemes[0]; s.entries[0].parentCode = ''; assert.equal(api.parentOf(s, s.entries[0]).state, 'empty'); });
check('duplicate scheme identity refuses', () => assert.throws(() => mount(mutate(d => { d.schemes[1].id = d.schemes[0].id; })), /duplicate scheme/));
check('duplicate entry identity within scheme refuses', () => assert.throws(() => mount(mutate(d => { d.schemes[0].entries[1].id = d.schemes[0].entries[0].id; })), /duplicate entry/));
check('stale retained count refuses', () => assert.throws(() => mount(mutate(d => { d.schemes[0].coverage.retainedEntries = 24; })), /retained count/));
check('unknown denominator cannot claim complete selected list', () => assert.throws(() => mount(mutate(d => { d.schemes[0].coverage.expectedEntries = null; })), /denominator/));
check('unresolved entry or alias sources refuse', () => { assert.throws(() => mount(mutate(d => { d.schemes[0].entries[0].sourceId = 'missing'; })), /entry source/); assert.throws(() => mount(mutate(d => { d.schemes[0].entries[1].aliases[0].sourceId = 'missing'; })), /alias source/); });
check('project alias authority cannot imply source-stated synonym', () => assert.throws(() => mount(mutate(d => { d.schemes[0].entries[1].aliases[0].kind = 'source-alternative-label'; })), /alias authority/));
check('oversized native object refuses with visible alert', () => { const root = new Element('section', document); assert.throws(() => api.create(root, mutate(d => { d.schemes[0].entries[0].native = {large: 'x'.repeat(131073)}; })), /128 KiB/); assert.equal(root.children[0].attrs.role, 'alert'); });
check('non-JSON native values refuse', () => { for (const value of [undefined, NaN, Infinity, () => 0]) assert.throws(() => mount(mutate(d => { d.schemes[0].entries[0].native.bad = value; })), /not JSON/); });
check('deep native structures refuse', () => assert.throws(() => mount(mutate(d => { let x = {}; d.schemes[0].entries[0].native = x; for (let i=0;i<18;i++) { x.n = {}; x=x.n; } })), /bound/));
check('not captured empty list is honest', () => { const d = fixture(); d.schemes = [d.schemes[1]]; d.schemes[0].entries = []; d.schemes[0].coverage = {status:'not-captured',expectedEntries:null,retainedEntries:0,definitionsStatus:'labels-only'}; const {ui} = mount(d); assert.match(ui.elements.count.textContent, /0 matching entries \/ 0 retained/); assert.equal(ui.elements.next.disabled, true); });
check('accessible controls and live count', () => { const {root, ui} = mount(); assert.equal(ui.elements.count.attrs['aria-live'], 'polite'); const labels = tree(root).filter(x=>x.tag==='label'); assert.equal(labels[0].htmlFor, ui.elements.select.id); assert.equal(labels[1].htmlFor, ui.elements.search.id); assert.equal(ui.elements.previous.type, 'button'); });
check('null and empty codes stay visible without numeric inference', () => { const {ui} = mount(mutate(d=>{d.schemes[0].entries[0].code=null;d.schemes[0].entries[1].code='';})); assert.match(text(ui.elements.list), /Code role not specified/); assert.match(text(ui.elements.list), /Empty string \(supplied\)/); });
check('context filter rejects unknown scheme', () => { const {ui} = mount(); assert.throws(()=>ui.setFilter('', 'not-present'), /contextual/); });
check('closed contract rejects extra properties at every contract level', () => {
  for (const locate of [d=>d,d=>d.schemes[0],d=>d.schemes[0].sources[0],d=>d.schemes[0].coverage,d=>d.schemes[0].entries[0],d=>d.schemes[0].entries[1].aliases[0]]) assert.throws(()=>mount(mutate(d=>{locate(d).unexpected=true;})), /unexpected property/);
});
check('native nested arbitrary fields are intentionally retained', () => { const d=fixture();d.schemes[0].entries[0].native.extra={unknown:{nested:[null,'',false,0]}};assert.deepEqual(JSON.parse(api.validate(d).rows[0].nativeDisplay),d.schemes[0].entries[0].native); });
check('scheme source entry and source-reference identities are bounded', () => {
  for (const locate of [d=>d.schemes[0],d=>d.schemes[0].sources[0],d=>d.schemes[0].entries[0]]) assert.throws(()=>mount(mutate(d=>{locate(d).id='bad/id';})), /identity/);
  assert.throws(()=>mount(mutate(d=>{d.schemes[0].entries[0].sourceId=' bad ';})), /identity/);
});
check('nonempty source definitions required for definition-complete status', () => { for(const definition of [null,'','  ']) assert.throws(()=>mount(mutate(d=>{d.schemes[1].coverage.definitionsStatus='source-definitions-retained';d.schemes[1].entries[0].definition=definition;})), /definition coverage/); });
check('labels-only rejects substantive definitions but preserves whitespace-only values', () => { assert.throws(()=>mount(mutate(d=>{d.schemes[1].entries[0].definition='Definition';})), /labels-only/);const {ui}=mount(mutate(d=>{d.schemes[1].entries[0].definition=' \t ';}));ui.setFilter('000','fictional-b');ui.elements.list.children[0].children[0].listeners.click();assert.ok(text(ui.elements.detail).includes('Whitespace-only string (supplied): " \\t "')); });
check('aliases cannot be empty or whitespace', () => { for(const value of ['', '  ']) assert.throws(()=>mount(mutate(d=>{d.schemes[0].entries[1].aliases[0].text=value;})), /alias text/); });
check('nested encoding and punctuation cannot hide credential query names', () => {
  for (const name of ['api.key', '%2561pi_key', 'X%252dAmz%252dCredential', 'x.goog.signature', '%25252561pi_key']) assert.equal(api.safeSourceURL('https://example.invalid/?'+name+'=synthetic'),null);
  assert.equal(api.safeSourceURL('https://example.invalid/?page=2'),'https://example.invalid/?page=2');
});
check('password and secret query names are withheld in real rendered anchors', () => {
  for(const name of ['password','secret','%2570assword','s.e.c.r.e.t']){const url='https://example.invalid/?'+name+'=synthetic';assert.equal(api.safeSourceURL(url),null);const {root}=mount(mutate(d=>{d.schemes[0].sources[0].url=url;}));assert.equal(tree(root).filter(x=>x.tag==='a'&&x.href===url).length,0);assert.match(text(root),/link withheld/);}
});
check('optional source label language stays explicit without inference', () => {
  for(const language of ['en-GB',null,'x'.repeat(80)]){const {ui}=mount(mutate(d=>{d.schemes[0].entries[0].labelLanguage=language;}));ui.setFilter('000','fictional-a');ui.elements.list.children[0].children[0].listeners.click();assert.match(text(ui.elements.detail),/Source-declared label language/);assert.ok(text(ui.elements.detail).includes(api.display(language,'Not supplied (explicit null)')));}
  const {ui}=mount();ui.setFilter('000','fictional-a');ui.elements.list.children[0].children[0].listeners.click();assert.ok(!text(ui.elements.detail).includes('Source-declared label language'));
});
check('source label language enforces the optional 1-to-80 contract', () => {for(const value of ['', 'x'.repeat(81), 1])assert.throws(()=>mount(mutate(d=>{d.schemes[0].entries[0].labelLanguage=value;})),/labelLanguage/);});
check('oversized native property names are charged before formatting', () => assert.throws(()=>api.nativeText({['x'.repeat(131073)]:null}),/128 KiB/));
check('aggregate native text bound refuses before whole payload retention', () => {
  const d=fixture(),s=d.schemes[0],base=s.entries[0];s.entries=Array.from({length:180},(_,i)=>({...base,id:'large-'+i,native:{value:'x'.repeat(100000)}}));s.coverage.expectedEntries=180;s.coverage.retainedEntries=180;
  assert.throws(()=>api.validate(d),/total native display exceeds 16 MiB/);
});
check('no network, HTML parser, storage or fetch facility in module', () => { const source = require('node:fs').readFileSync(require.resolve('./classification-browser.js'), 'utf8'); assert.ok(!/\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage|innerHTML|insertAdjacentHTML)\s*[.(=]/u.test(source)); });

function withNativeForm() {
  const d=fixture(),e=d.schemes[0].entries[0];e.code=null;e.aliases=[];e.codeRole='unresolved-native-value';e.native.value='🆕ZZ13SA';
  e.nativeSearchForms=[{text:e.native.value,kind:'source-native-value',authority:'source-stated',sourceId:e.sourceId,sourceLocator:e.sourceLocator,nativePointer:'/native/value',language:null}];return d;
}
check('full source-native string supports substring discovery without alias or code promotion',()=>{
  const d=withNativeForm(),before=JSON.stringify(d),{ui}=mount(d);ui.setFilter('ZZ13SA');assert.equal(ui.elements.list.children.length,1);assert.match(text(ui.elements.list),/Code interpretation unresolved/);ui.elements.list.children[0].children[0].listeners.click();assert.match(text(ui.elements.detail),/🆕ZZ13SA/);assert.match(text(ui.elements.detail),/Exact source-native search forms/);assert.equal(JSON.stringify(d),before);assert.equal(d.schemes[0].entries[0].code,null);assert.deepEqual(d.schemes[0].entries[0].aliases,[]);
});
check('native values are not searched without a declared form',()=>{const d=withNativeForm();delete d.schemes[0].entries[0].nativeSearchForms;const{ui}=mount(d);ui.setFilter('ZZ13SA');assert.equal(ui.elements.list.children.length,0);});
check('stripping source markers refuses',()=>{const d=withNativeForm();d.schemes[0].entries[0].nativeSearchForms[0].text='ZZ13SA';assert.throws(()=>mount(d),/native search string/);});
check('native pointer and source locator cannot be rebound',()=>{for(const field of ['nativePointer','sourceLocator','sourceId']){const d=withNativeForm();d.schemes[0].entries[0].nativeSearchForms[0][field]='missing';assert.throws(()=>mount(d),/native/);}});
check('pointer escapes and empty native key are preserved',()=>{for(const [key,pointer]of [['','/native/'],['a/b~c','/native/a~1b~0c']]){const d=withNativeForm(),e=d.schemes[0].entries[0];e.native={[key]:'🆕ZZ13SA'};e.nativeSearchForms[0].nativePointer=pointer;const{ui}=mount(d);ui.setFilter('ZZ13SA');assert.equal(ui.elements.list.children.length,1);}});
check('inherited and accessor native values cannot resolve',()=>{for(const accessor of [false,true]){const d=withNativeForm(),e=d.schemes[0].entries[0];let reads=0;e.native=Object.create({value:'🆕ZZ13SA'});if(accessor)Object.defineProperty(e.native,'value',{enumerable:true,get(){reads++;return'🆕ZZ13SA';}});assert.throws(()=>mount(d),/own data property/);assert.equal(reads,0);}});
check('native form accessors are refused without evaluation',()=>{const d=withNativeForm(),f=d.schemes[0].entries[0].nativeSearchForms[0];let reads=0;Object.defineProperty(f,'text',{enumerable:true,get(){reads++;return'🆕ZZ13SA';}});assert.throws(()=>mount(d),/own data property/);assert.equal(reads,0);});
check('array pointer leading zeros and traversal outside native are refused',()=>{for(const pointer of ['/label','/native/values/01','/native/values/-','/native/a~2b']){const d=withNativeForm(),e=d.schemes[0].entries[0];e.native.values=['🆕ZZ13SA'];e.nativeSearchForms[0].nativePointer=pointer;assert.throws(()=>mount(d),/native/);}});
check('null roles are distinct without interpreting legacy absence',()=>{for(const[role,wording]of [['unresolved-native-value','Code interpretation unresolved'],['no-separate-code-assertion','No separate code assertion'],['unknown','Code role not specified']]){const d=withNativeForm();d.schemes[0].entries[0].codeRole=role;const{ui}=mount(d);ui.setFilter('ZZ13SA');assert.match(text(ui.elements.list),new RegExp(wording));ui.elements.list.children[0].children[0].listeners.click();assert.match(text(ui.elements.detail),new RegExp(wording));}});
check('code role conflicts refuse instead of changing code',()=>{for(const[role,code]of [['source-code-retained',null],['explicit-empty-code',null],['unresolved-native-value','ZZ13SA'],['no-separate-code-assertion','']]){const d=withNativeForm();Object.assign(d.schemes[0].entries[0],{codeRole:role,code});assert.throws(()=>mount(d),/code role conflict/);}});
check('native forms retain null-language and bounded exact role',()=>{for(const[field,value]of [['language','en'],['authority','project-search-variant'],['kind','notation']]){const d=withNativeForm();d.schemes[0].entries[0].nativeSearchForms[0][field]=value;assert.throws(()=>mount(d),/native search role/);}});
check('native forms preserve field snapshot after caller changes declared form',()=>{const d=withNativeForm(),{ui}=mount(d);d.schemes[0].entries[0].nativeSearchForms[0].text='changed';ui.setFilter('ZZ13SA');assert.equal(ui.elements.list.children.length,1);ui.elements.list.children[0].children[0].listeners.click();assert.match(text(ui.elements.detail),/🆕ZZ13SA/);});
check('native pointer count and duplicate limits refuse',()=>{for(const count of [2,9]){const d=withNativeForm(),e=d.schemes[0].entries[0];e.nativeSearchForms=Array.from({length:count},()=>({...e.nativeSearchForms[0]}));assert.throws(()=>mount(d),/native search/);}});
check('native form Unicode character ceiling preserves supplementary characters',()=>{const d=withNativeForm(),e=d.schemes[0].entries[0];e.native.value=e.nativeSearchForms[0].text='🆕'.repeat(1000);api.validate(d);e.native.value=e.nativeSearchForms[0].text+='🆕';assert.throws(()=>api.validate(d),/text bound/);});
check('unrelated native accessors refuse before callback or context mutation',()=>{const d=withNativeForm(),e=d.schemes[0].entries[0];let calls=0;Object.defineProperty(e.native,'other',{enumerable:true,get(){calls++;e.native.value='changed';return 'effect';}});assert.throws(()=>api.validate(d),/own data property/);assert.equal(calls,0);assert.equal(e.native.value,'🆕ZZ13SA');});
check('own and inherited custom serialisation never executes',()=>{for(const inherited of [false,true]){const d=withNativeForm(),e=d.schemes[0].entries[0];let calls=0;const hook={toJSON(){calls++;return {value:'changed'};}};if(inherited)e.native=Object.assign(Object.create(hook),e.native);else Object.defineProperty(e.native,'toJSON',{value:hook.toJSON,enumerable:false});assert.throws(()=>api.validate(d),/custom serialisation/);assert.equal(calls,0);}});
check('inert native snapshot keeps display and search pointer identical',()=>{const d=withNativeForm(),e=d.schemes[0].entries[0],before=JSON.stringify(d),row=api.validate(d).rows[0];assert.equal(JSON.stringify(d),before);e.native.value='changed';e.nativeSearchForms[0].text='changed';assert.equal(row.entry.native.value,'🆕ZZ13SA');assert.equal(row.nativeSearchForms[0].text,row.entry.native.value);assert.equal(JSON.parse(row.nativeDisplay).value,row.entry.native.value);assert.ok(Object.isFrozen(row.entry.native));assert.equal(api.matchRows([row],'','ZZ13SA').length,1);});
check('escaped lone surrogate values and native keys refuse at UTF-8 boundary',()=>{for(const bad of ['\ud800','\udfff']){const d=withNativeForm(),e=d.schemes[0].entries[0];e.native.value=e.nativeSearchForms[0].text=bad;assert.throws(()=>api.validate(d),/unpaired surrogate/);const k=withNativeForm();k.schemes[0].entries[0].native[bad]='value';assert.throws(()=>api.validate(k),/unpaired surrogate/);}});
check('literal native toJSON string is retained without being a hook',()=>{const d=withNativeForm();d.schemes[0].entries[0].native.toJSON='source-owned text';const row=api.validate(d).rows[0];assert.equal(JSON.parse(row.nativeDisplay).toJSON,'source-owned text');});
console.log(JSON.stringify({passed:true,syntheticChecks:checks,privateModelUsed:false,limits:['Synthetic DOM and contract checks; rendered browser and human evaluation are separate.']}));
