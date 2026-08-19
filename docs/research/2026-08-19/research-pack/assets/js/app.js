(() => {
  'use strict';
  const D = window.RESEARCH_PACK_DATA;
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];
  const state = { view: 'overview', selected: null, compare: new Set(), query: '', topic: '', type: '', access: '', maturity: '' };
  const collections = {
    findings: D.findings, decisions: D.decisions, providers: D.providers, tools: D.tools,
    risks: D.risks, sources: D.sources, standards: D.standards, workflows: D.workflows,
    hosting: D.hosting, names: D.names, evaluations: D.evaluations, controls: D.controls
  };
  const recordType = (r) => {
    if (r.statement) return r.type || 'finding';
    if (r.recommendation && r.options_considered) return 'decision';
    if (r.authority && r.datasets_services) return 'provider';
    if (r.namespace && r.input_schema) return 'tool';
    if (r.attack_path) return 'risk';
    if (r.url && r.organisation) return 'source';
    return 'record';
  };
  const text = (r) => JSON.stringify(r).toLowerCase();
  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const arr = (v) => Array.isArray(v) ? v : (v ? [v] : []);
  const title = (r) => r.title || r.name || r.id || 'Untitled';
  const summary = (r) => r.statement || r.recommendation || r.purpose || r.description || r.authority || r.attack_path || r.notes || '';
  const status = (r) => r.status || r.maturity || r.confidence || r.type || '';
  const topic = (r) => r.topic || r.namespace || (r.provider_dependencies ? 'tools' : recordType(r));
  const tiers = (r) => arr(r.access_tiers || r.access_tier || r.tiers || (recordType(r)==='finding' ? [] : null));
  function matches(r) {
    if (state.query && !text(r).includes(state.query.toLowerCase())) return false;
    if (state.topic && topic(r) !== state.topic) return false;
    if (state.type && recordType(r) !== state.type) return false;
    if (state.access && !tiers(r).map(String).includes(state.access)) return false;
    if (state.maturity && !String(status(r)).includes(state.maturity)) return false;
    return true;
  }
  function badge(label, cls='') { return `<span class="badge ${cls}">${esc(label)}</span>`; }
  function findingBadge(t) {
    if (t === 'verified-fact') return badge('Verified fact','fact');
    if (t === 'recommendation') return badge('Recommendation','rec');
    if (t === 'assumption') return badge('Assumption','assumption');
    if (t === 'unresolved-question') return badge('Unresolved','unresolved');
    return badge(t || 'record');
  }
  function setDetail(r) {
    state.selected = r;
    const sources = arr(r.source_ids || r.evidence).map(id => D.sources.find(s => s.id === id)).filter(Boolean);
    $('#detail-content').innerHTML = `
      <h3>${esc(title(r))}</h3>
      <p>${esc(summary(r))}</p>
      <p>${badge(recordType(r))} ${status(r) ? badge(status(r)) : ''}</p>
      ${sources.length ? `<h4>Evidence</h4><ul>${sources.map(s => `<li><a href="${esc(s.url)}">${esc(s.id)} — ${esc(s.title)}</a> <span class="meta">(${esc(s.maturity)})</span></li>`).join('')}</ul>` : ''}
      <h4>Complete record</h4><pre>${esc(JSON.stringify(r,null,2))}</pre>`;
    $('#export-selected').disabled = false;
    $('.detail').scrollIntoView({behavior:'smooth',block:'nearest'});
  }
  function card(r, opts={}) {
    const rid = `${recordType(r)}:${r.id || title(r)}`;
    const selected = state.compare.has(rid);
    return `<article class="result">
      <p>${recordType(r)==='finding' ? findingBadge(r.type) : badge(recordType(r))} ${status(r) ? badge(status(r), recordType(r)==='risk'?'risk':'') : ''}</p>
      <h3>${esc(title(r))}</h3><p>${esc(summary(r))}</p>
      <p class="meta">${esc(r.id || '')}${topic(r) ? ` · ${esc(topic(r))}` : ''}${tiers(r).length ? ` · ${esc(tiers(r).join(', '))}` : ''}</p>
      <div class="result-actions"><button data-inspect="${esc(rid)}">Inspect</button>
      ${opts.compare ? `<label><input type="checkbox" data-compare="${esc(rid)}" ${selected?'checked':''}> Compare</label>` : ''}</div>
    </article>`;
  }
  function currentRecords() {
    const key = state.view;
    if (collections[key]) return collections[key].filter(matches);
    return Object.values(collections).flat().filter(matches);
  }
  function bindInspect(records) {
    const map = new Map(records.map(r => [`${recordType(r)}:${r.id || title(r)}`,r]));
    $$('[data-inspect]').forEach(b => b.addEventListener('click',() => setDetail(map.get(b.dataset.inspect))));
    $$('[data-compare]').forEach(c => c.addEventListener('change',() => { c.checked ? state.compare.add(c.dataset.compare) : state.compare.delete(c.dataset.compare); render(); }));
  }
  function overview() {
    const counts = [['Decisions',D.decisions.length],['Requirements',50],['Tools',D.tools.length],['Workflows',D.workflows.length],['Threats',D.risks.length],['Evaluation cases',D.evaluations.length],['Sources',D.sources.length],['Repositories',D.repositories.length]];
    const html = `<h2>Executive overview</h2>
      <div class="callout"><strong>Recommendation:</strong> start a new platform called <strong>Locus Accord</strong> as a working codename. Use a static OKF presentation plane, a TypeScript MCP/control gateway, Python deterministic geospatial execution, physically isolated data tiers and a dedicated evidence plane.</div>
      <div class="callout warning"><strong>Boundary:</strong> this pack authorises research and a Codex hand-off only. It does not create, modify, implement or deploy a repository or protected service.</div>
      <div class="cards">${counts.map(([k,v])=>`<article class="card"><div class="kpi">${v}</div><h3>${k}</h3></article>`).join('')}</div>
      <h2>Accepted architecture</h2><div class="cards">${D.planes.map(p=>`<article class="card"><h3>${esc(p.name)}</h3><p>${esc(p.contains.join(', '))}</p><p class="meta">${esc(p.trust_boundary)}</p></article>`).join('')}</div>
      <h2>Reports</h2><div class="cards">${D.reports.map(r=>`<article class="card"><h3>${esc(r.title)}</h3><p><a href="${esc(r.href)}">Open report</a></p></article>`).join('')}</div>`;
    return html;
  }
  function listView(key) {
    const records = collections[key].filter(matches);
    const compare = key === 'decisions' || key === 'providers' || key === 'hosting';
    let extra='';
    if (key==='decisions' && state.compare.size) {
      const chosen=D.decisions.filter(r=>state.compare.has(`decision:${r.id}`));
      extra=`<h3>Side-by-side comparison</h3><div class="compare-grid">${chosen.map(r=>`<article class="card"><h4>${esc(r.id)} — ${esc(r.title)}</h4><p><strong>Recommendation:</strong> ${esc(r.recommendation)}</p><p><strong>Benefits:</strong> ${esc(r.benefits.join('; '))}</p><p><strong>Disadvantages:</strong> ${esc(r.disadvantages.join('; '))}</p><p><strong>Conditions:</strong> ${esc(r.conditions_that_change_decision.join('; '))}</p></article>`).join('')}</div>`;
    }
    return `<div class="results-header"><h2>${esc(key[0].toUpperCase()+key.slice(1))}</h2><strong>${records.length} records</strong></div>${extra}<div class="result-list">${records.map(r=>card(r,{compare})).join('') || '<div class="empty">No records match the filters.</div>'}</div>`;
  }
  function timeline() {
    const events=[];
    D.sources.forEach(s=>{ if(s.published) events.push({date:s.published,title:s.title,kind:'source',record:s}); });
    D.repositories.forEach(r=>events.push({date:r.retrieved,title:`Pinned ${r.repository}`,kind:'repository',record:r}));
    D.decisions.forEach(r=>events.push({date:r.decided_on,title:`Decision ${r.id}: ${r.title}`,kind:'decision',record:r}));
    const filtered=events.filter(e=>matches(e.record)).sort((a,b)=>String(b.date).localeCompare(String(a.date)));
    return `<h2>Evidence and decision timeline</h2><div class="timeline">${filtered.map((e,i)=>`<div class="timeline-item"><strong>${esc(e.date)}</strong><h3>${esc(e.title)}</h3><p>${badge(e.kind)} <button data-time="${i}">Inspect</button></p></div>`).join('')}</div>`;
  }
  function bindTimeline() {
    const events=[];
    D.sources.forEach(s=>{ if(s.published) events.push({date:s.published,title:s.title,kind:'source',record:s}); });
    D.repositories.forEach(r=>events.push({date:r.retrieved,title:`Pinned ${r.repository}`,kind:'repository',record:r}));
    D.decisions.forEach(r=>events.push({date:r.decided_on,title:`Decision ${r.id}: ${r.title}`,kind:'decision',record:r}));
    const filtered=events.filter(e=>matches(e.record)).sort((a,b)=>String(b.date).localeCompare(String(a.date)));
    $$('[data-time]').forEach(b=>b.addEventListener('click',()=>setDetail(filtered[Number(b.dataset.time)].record)));
  }
  function graph() {
    const nodes=[...D.controls.slice(0,6),...D.providers.slice(0,7),...D.decisions.slice(0,8)];
    const width=980,height=650,cx=490,cy=325;
    const positions=new Map(nodes.map((n,i)=>{const a=(i/nodes.length)*Math.PI*2;const r=i<6?150:270;return [n.id,{x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r}];}));
    const edges=[];
    D.decisions.slice(0,8).forEach((d,i)=>edges.push([d.id,D.controls[i%6].id]));
    D.providers.forEach((p,i)=>edges.push([p.id,D.controls[(i+4)%6].id]));
    return `<h2>Decision, provider and control graph</h2><p>Select a node to inspect the source record. This is a bounded relationship view, not an ontology inference.</p><div class="graph-wrap"><svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="graph-title"><title id="graph-title">Relationship graph of controls, providers and decisions</title>${edges.map(([a,b])=>{const p=positions.get(a),q=positions.get(b);return p&&q?`<line class="edge" x1="${p.x}" y1="${p.y}" x2="${q.x}" y2="${q.y}"></line>`:''}).join('')}${nodes.map(n=>{const p=positions.get(n.id);return `<g class="node" tabindex="0" role="button" data-node="${esc(n.id)}" aria-label="Inspect ${esc(title(n))}"><rect x="${p.x-55}" y="${p.y-22}" width="110" height="44" rx="8"></rect><text x="${p.x}" y="${p.y-3}" text-anchor="middle">${esc(n.id)}</text><text x="${p.x}" y="${p.y+13}" text-anchor="middle">${esc(title(n).slice(0,16))}</text></g>`}).join('')}</svg></div>`;
  }
  function bindGraph() {
    const map=new Map([...D.controls,...D.providers,...D.decisions].map(r=>[r.id,r]));
    $$('[data-node]').forEach(n=>{const go=()=>setDetail(map.get(n.dataset.node));n.addEventListener('click',go);n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});});
  }
  function mapView() {
    const p = D.providers.filter(matches);
    const items=[
      {id:'PV-OS',x:260,y:90,w:300,h:440,label:'Great Britain'},
      {id:'PV-ONS-DATA',x:210,y:60,w:400,h:500,label:'UK statistics'},
      {id:'PV-ONS-GEO',x:300,y:150,w:230,h:330,label:'England and Wales / product-specific UK'},
      {id:'PV-NOMIS',x:180,y:50,w:450,h:520,label:'UK datasets'},
      {id:'PV-LANDIS',x:320,y:180,w:200,h:300,label:'England and Wales soils'},
      {id:'PV-HMLR-OPEN',x:335,y:190,w:180,h:285,label:'England and Wales land registration'},
      {id:'PV-HMLR-PROTECTED',x:350,y:205,w:150,h:255,label:'Protected HMLR services'}
    ].filter(i=>p.some(v=>v.id===i.id));
    return `<h2>Provider geographic-scope view</h2><p>This diagram is schematic. It communicates jurisdiction/product scope and must not be used as an authoritative boundary.</p><div class="map-wrap"><svg viewBox="0 0 800 620" role="img" aria-labelledby="map-title"><title id="map-title">Schematic provider coverage map</title><path d="M390 40 C340 80 365 130 320 170 C290 210 330 260 300 310 C260 370 310 430 280 500 C350 560 470 570 520 510 C500 450 550 400 515 340 C550 280 520 220 550 165 C510 120 470 90 450 45 Z" fill="none" stroke="currentColor" stroke-width="4"></path>${items.map((i,k)=>`<g class="node" tabindex="0" role="button" data-map-node="${i.id}"><rect x="${i.x}" y="${i.y}" width="${i.w}" height="${i.h}" rx="18" fill="none" stroke="currentColor" stroke-dasharray="${4+k} ${3+k}" opacity=".65"></rect><text x="${i.x+10}" y="${i.y+22}">${esc(i.id)} — ${esc(i.label)}</text></g>`).join('')}</svg></div>`;
  }
  function bindMap() { const map=new Map(D.providers.map(r=>[r.id,r])); $$('[data-map-node]').forEach(n=>{const go=()=>setDetail(map.get(n.dataset.mapNode));n.addEventListener('click',go);n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});}); }
  function architecture() {
    return `<h2>Architecture diagrams</h2><div class="diagram-grid">${D.diagrams.map(d=>`<figure><a href="${esc(d.href)}"><img src="${esc(d.href)}" alt="${esc(d.title)} diagram"></a><figcaption>${esc(d.title)}</figcaption></figure>`).join('')}</div>`;
  }
  function render() {
    let out='';
    if(state.view==='overview') out=overview();
    else if(state.view==='timeline') out=timeline();
    else if(state.view==='graph') out=graph();
    else if(state.view==='map') out=mapView();
    else if(state.view==='architecture') out=architecture();
    else out=listView(state.view);
    $('#view-content').innerHTML=out;
    if(collections[state.view]) bindInspect(collections[state.view].filter(matches));
    if(state.view==='timeline') bindTimeline();
    if(state.view==='graph') bindGraph();
    if(state.view==='map') bindMap();
    const count=currentRecords().length;
    $('#filter-summary').textContent=`${count} matching record${count===1?'':'s'} in the current scope.`;
  }
  function initFilters() {
    const all=Object.values(collections).flat();
    [...new Set(all.map(topic).filter(Boolean))].sort().forEach(v=>$('#topic').insertAdjacentHTML('beforeend',`<option value="${esc(v)}">${esc(v)}</option>`));
    [...new Set(all.map(recordType))].sort().forEach(v=>$('#record-type').insertAdjacentHTML('beforeend',`<option value="${esc(v)}">${esc(v)}</option>`));
    [...new Set(all.map(status).filter(Boolean).map(String))].sort().forEach(v=>$('#maturity').insertAdjacentHTML('beforeend',`<option value="${esc(v)}">${esc(v)}</option>`));
    $('#search').addEventListener('input',e=>{state.query=e.target.value;render();});
    $('#topic').addEventListener('change',e=>{state.topic=e.target.value;render();});
    $('#record-type').addEventListener('change',e=>{state.type=e.target.value;render();});
    $('#access').addEventListener('change',e=>{state.access=e.target.value;render();});
    $('#maturity').addEventListener('change',e=>{state.maturity=e.target.value;render();});
    $('#clear-filters').addEventListener('click',()=>{state.query=state.topic=state.type=state.access=state.maturity='';['search','topic','record-type','access','maturity'].forEach(id=>$('#'+id).value='');render();});
  }
  $$('.tabs [role="tab"]').forEach(b=>b.addEventListener('click',()=>{state.view=b.dataset.view;$$('.tabs [role="tab"]').forEach(x=>x.setAttribute('aria-selected',String(x===b)));render();$('#main-content').focus();}));
  $('#export-selected').addEventListener('click',()=>{if(!state.selected)return;const blob=new Blob([JSON.stringify(state.selected,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${state.selected.id||'selected-record'}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);});
  initFilters(); render();
})();
