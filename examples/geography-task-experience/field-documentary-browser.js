/* Selected documentary field links; no provider calls or vocabulary adoption assertion. */
(function(scope){
  'use strict';
  const SCHEMA='gis-ai-go.field-documentary-browser.v1',CAP=4*1024*1024,PAGE=10;
  const STATUS=Object.freeze({
    'explicit-attribute-link-and-exact-version-candidate':'Documentary link candidate',
    'matched-section-without-applicable-code-list-link':'No applicable code-list link',
    'no-exact-document-field-match':'No exact documented field match',
    'version-unresolved-missing-native-components':'Native version unresolved'
  });
  const own=(v,k)=>Object.prototype.hasOwnProperty.call(v,k);
  const fail=()=>{throw new Error('Field reference contract refused');};
  const need=v=>{if(!v)fail();};
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  function closed(v,keys){need(object(v)&&Object.keys(v).length===keys.length&&keys.every(k=>own(v,k)));}
  function bounded(v,max=10000){need(typeof v==='string'&&v.length<=max&&!/[\uD800-\uDFFF]/u.test(v));}
  const hash=v=>need(typeof v==='string'&&/^[a-f0-9]{64}$/u.test(v));
  function url(v,kind){
    bounded(v,2048);let u;try{u=new URL(v);}catch(_){fail();}
    need(u.protocol==='https:'&&!u.username&&!u.password&&!u.port&&!u.search&&!u.hash&&['api.os.uk','docs.os.uk'].includes(u.hostname));
    if(kind==='code')need(u.hostname==='docs.os.uk'&&u.pathname.startsWith('/osngd/code-lists/'));
    return v;
  }
  function reference(v,id){closed(v,['card','bytes','sha256']);bounded(v.card,200);need(v.card===id&&/^[a-zA-Z0-9_.\/-]+$/u.test(id)&&!id.startsWith('/')&&!id.split('/').includes('..'));need(Number.isInteger(v.bytes)&&v.bytes>0&&v.bytes<=16384);hash(v.sha256);}
  function pointer(root,path){
    need(typeof path==='string'&&(path===''||path.startsWith('/'))&&!/~(?:[^01]|$)/u.test(path));let v=root;
    if(path!=='')for(const part of path.slice(1).split('/')){const key=part.replace(/~1/gu,'/').replace(/~0/gu,'~');need(v!==null&&typeof v==='object'&&own(v,key));v=v[key];}
    return v;
  }
  const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  function parse(text){
    bounded(text,CAP);need(new TextEncoder().encode(text).length<=CAP);let data;try{data=JSON.parse(text);}catch(_){fail();}
    closed(data,['schema','globalComplete','basis','counts','statusCounts','limits','resources','documents','sections','fields']);
    need(data.schema===SCHEMA&&data.globalComplete===false);
    closed(data.basis,['candidateManifestSha256','outputManifestSha256','independentReviewSha256','rootReviewSha256']);Object.values(data.basis).forEach(hash);
    closed(data.counts,['collections','documentAttributeSections','explicitAttributeCodeListLinks','nativeConstraintOccurrences','nativeResources','topLevelPropertyOccurrences']);
    closed(data.statusCounts,Object.keys(STATUS));need(Array.isArray(data.limits)&&data.limits.length<=32);data.limits.forEach(v=>bounded(v));
    for(const [k,max]of[['resources',64],['documents',16],['sections',1024],['fields',2048]])need(Array.isArray(data[k])&&data[k].length>0&&data[k].length<=max);
    const resources=new Map(),documents=new Map(),sections=new Map(),ids=new Set();
    for(const r of data.resources){
      closed(r,['id','collectionId','family','kind','url','sha256','bytes','requestStartedAt','requestFinishedAt','versionContext','nativeRootWithoutProperties','propertiesKeyPresent','propertiesType','provenance']);
      bounded(r.id,200);bounded(r.collectionId,160);bounded(r.family,80);need(!resources.has(r.id)&&['schemas','queryables'].includes(r.kind)&&r.id===r.kind+':'+r.collectionId);
      url(r.url);hash(r.sha256);need(Number.isInteger(r.bytes)&&r.bytes>0);for(const key of['requestStartedAt','requestFinishedAt'])if(r[key]!==null)bounded(r[key],80);
      closed(r.versionContext,['basis','schemaSourceId','value']);bounded(r.versionContext.basis);bounded(r.versionContext.schemaSourceId,200);if(r.versionContext.value!==null)bounded(r.versionContext.value,80);
      need(object(r.nativeRootWithoutProperties)&&r.propertiesKeyPresent===true&&r.propertiesType==='dict');reference(r.provenance,`native/${r.collectionId}/${r.kind}-ROOT.json`);resources.set(r.id,r);
    }
    for(const r of resources.values()){need(r.versionContext.schemaSourceId==='schemas:'+r.collectionId&&resources.has(r.versionContext.schemaSourceId));const schema=resources.get(r.versionContext.schemaSourceId);need(schema.kind==='schemas');const root=schema.nativeRootWithoutProperties;const expected=Number.isInteger(root.majorVersion)&&Number.isInteger(root.minorVersion)?root.majorVersion+'.'+root.minorVersion:null;need(r.versionContext.value===expected);}
    for(const d of data.documents){
      closed(d,['id','family','url','sha256','bytes','observedAt','publicationDate','codeListEdition','provenance']);bounded(d.id,100);bounded(d.family,80);need(!documents.has(d.id));url(d.url);hash(d.sha256);
      need(Number.isInteger(d.bytes)&&d.bytes>0&&d.publicationDate===null&&d.codeListEdition===null);bounded(d.observedAt,80);reference(d.provenance,`documents/${d.family}/CONTEXT.json`);documents.set(d.id,d);
    }
    for(const s of data.sections){
      closed(s,['id','provenance','native']);reference(s.provenance,s.id);need(!sections.has(s.id));const n=s.native;
      need(object(n)&&n.schema==='private-ngd-documented-attribute.v1'&&object(n.source)&&documents.has(n.source.id));const d=documents.get(n.source.id);
      need(n.source.sha256===d.sha256&&n.source.url===d.url&&n.source.bytes===d.bytes&&n.source.retrievedAt===d.observedAt);
      bounded(n.nativeSection,16384);bounded(n.nativeHeading);need(object(n.field)&&Array.isArray(n.codeListLinks)&&Array.isArray(n.metadata)&&Array.isArray(n.blocks));
      for(const link of n.codeListLinks){url(link.resolvedUrl,'code');need(link.apiAdoptionEstablished===false&&link.equivalenceEstablished===false);}
      sections.set(s.id,s);
    }
    const counts=Object.fromEntries(Object.keys(STATUS).map(k=>[k,0]));let constraints=0;
    for(const f of data.fields){
      closed(f,['id','provenance','native']);reference(f.provenance,f.id);need(!ids.has(f.id));ids.add(f.id);const n=f.native;
      need(object(n)&&n.schema==='private-ngd-native-attribute-link-candidate.v1'&&resources.has(n.sourceId));const r=resources.get(n.sourceId);
      need(n.collectionId===r.collectionId&&n.resourceKind===r.kind&&n.sourceSha256===r.sha256);bounded(n.nativePropertyName);need(object(n.nativeProperty));
      const base='/properties/'+n.nativePropertyName.replace(/~/gu,'~0').replace(/\//gu,'~1');need(n.nativePointer===base);
      need(n.originalNamePresent===own(n.nativeProperty,'originalName')&&equal(n.nativeOriginalName,n.originalNamePresent?n.nativeProperty.originalName:null));
      need(n.apiConstraintAdoptionEstablished===false&&n.equivalenceEstablished===false&&n.caseFoldingUsed===false&&n.formerlyTextPromotedToAlias===false&&n.codeListValueSetsCompared===false);
      need(own(STATUS,n.status)&&Array.isArray(n.nativeConstraints)&&Array.isArray(n.documentaryCandidates));counts[n.status]++;constraints+=n.nativeConstraints.length;
      for(const con of n.nativeConstraints){need(['enum','const'].includes(con.keyword)&&con.pointer.startsWith(base+'/')&&con.pointer.endsWith('/'+con.keyword));need(equal(pointer(n.nativeProperty,con.pointer.slice(base.length)),con.nativeValue));}
      for(const c of n.documentaryCandidates){
        need(sections.has(c.documentSection)&&c.apiConstraintAdoptionEstablished===false&&c.equivalenceEstablished===false&&c.nativeSchemaVersion===r.versionContext.value);
        const s=sections.get(c.documentSection).native;need(c.documentCurrentName===s.field.currentName&&c.attributeContext===s.attributeContext&&Array.isArray(c.explicitCodeListLinks));
        for(const link of c.explicitCodeListLinks){url(link.resolvedUrl,'code');need(link.apiAdoptionEstablished===false&&link.equivalenceEstablished===false&&typeof link.versionExplicitlyListedInSameMetadataBlock==='boolean');
          need(s.codeListLinks.some(x=>x.resolvedUrl===link.resolvedUrl&&x.blockOrdinal===link.blockOrdinal&&equal(x.sourceSpan,link.sourceSpan)&&equal(x.dataSchemaVersionNativeValues,link.dataSchemaVersionNativeValues)&&equal(x.codeListVersionNativeValues,link.codeListVersionNativeValues)));}
      }
      if(n.status==='version-unresolved-missing-native-components')need(r.versionContext.value===null);
      if(n.status==='no-exact-document-field-match')need(n.documentaryCandidates.length===0);
      if(n.status==='explicit-attribute-link-and-exact-version-candidate')need(n.documentaryCandidates.some(c=>c.explicitCodeListLinks.some(l=>l.versionExplicitlyListedInSameMetadataBlock===true)&&c.versionExplicitlyListed===true));
    }
    need(equal(counts,data.statusCounts));need(data.counts.topLevelPropertyOccurrences===data.fields.length&&data.counts.nativeResources===resources.size&&data.counts.documentAttributeSections===sections.size&&data.counts.nativeConstraintOccurrences===constraints);
    need(data.counts.collections===new Set(data.resources.map(r=>r.collectionId)).size&&data.counts.explicitAttributeCodeListLinks===data.sections.reduce((n,s)=>n+s.native.codeListLinks.length,0));
    // Input is text only: no caller-provided object getters or serialisation hooks run.
    return {data,resources,documents,sections};
  }
  function create(container,text){
    const model=parse(text),data=model.data,doc=container.ownerDocument;
    const el=(tag,value)=>{const n=doc.createElement(tag);if(value!==undefined)n.textContent=value;return n;};
    const labelled=(title,control)=>{const wrap=el('label',title);wrap.append(control);return wrap;};
    const option=(value,title)=>{const n=el('option',title);n.value=value;return n;};
    const details=(title,...children)=>{const d=el('details');d.open=false;d.append(el('summary',title),...children);return d;};
    const link=(title,address)=>{const a=el('a',title);a.href=url(address);a.target='_blank';a.rel='noopener noreferrer';return a;};
    const json=v=>JSON.stringify(v,null,2);
    const filters={query:'',collection:'',kind:'',status:'explicit-attribute-link-and-exact-version-candidate'};let page=0,selected=null;
    const search=el('input');search.type='search';search.maxLength=160;search.autocomplete='off';
    const collection=el('select');collection.append(option('','All selected API collections'));
    for(const id of [...new Set(data.resources.map(r=>r.collectionId))].sort())collection.append(option(id,id));
    const kind=el('select');kind.append(option('','Schemas and queryables'),option('schemas','Schema properties'),option('queryables','Queryable properties'));
    const status=el('select');status.append(option('','All statuses'));
    for(const [id,title]of Object.entries(STATUS))status.append(option(id,title+' ('+data.statusCounts[id]+')'));
    status.append(option('multiple','More than one documentary match'));status.value=filters.status;
    const count=el('p');count.setAttribute('role','status');const list=el('ul'),detail=el('section'),previous=el('button','Previous'),next=el('button','Next');previous.type=next.type='button';
    const scopeNote=details('Scope, terms and interpretation limits',...data.limits.map(x=>el('p',x)),el('p','Search covers these selected field observations. It does not search or change the host vocabulary collections. Schema and queryable occurrences remain separate. Display search ignores letter case and matches substrings; it creates no aliases or field bindings.'));
    // Fixed learning links are separate from the closed supplier-payload URL policy.
    const learningSources=Object.freeze({schema:'https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01',queryables:'https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables'});
    const learningLink=(title,address)=>{need(Object.values(learningSources).includes(address));const a=el('a',title);a.href=address;a.target='_blank';a.rel='noopener noreferrer';return a;};
    scopeNote.append(el('p','Schema: rules describing the allowed structure and values of data. Queryable: a property advertised for use in a filter; returned properties are not necessarily queryable.'),
      learningLink('JSON Schema Draft 7: validation rules',learningSources.schema),learningLink('OS NGD: queryables',learningSources.queryables),
      el('p','Documentary candidate is a project evidence label: a field name and version have a source-linked documentation match. API adoption means evidence that the API field uses that particular list and edition. A documentation link alone does not establish adoption or equivalence.'),
      el('p','Preserved source wording about nullability is historical. A nullable type plus an enum excluding null legitimately rejects null; it is not inherently a contradiction. Read the constraints together, using the declared schema version. Former-name text remains source text, not an inferred alias.'));
    container.append(el('p',data.statusCounts['explicit-attribute-link-and-exact-version-candidate']+' documentary candidates of '+data.fields.length+' field occurrences. API adoption and equivalence are not established. Retained snapshots are not current service status.'),
      labelled('Find a native field name or documentary list label',search),labelled('API collection',collection),labelled('Native resource',kind),labelled('Evidence status',status),count,list,previous,next,detail,scopeNote);
    function matches(){const q=filters.query.toLowerCase();return data.fields.filter(f=>{const n=f.native;return(!filters.collection||n.collectionId===filters.collection)&&(!filters.kind||n.resourceKind===filters.kind)&&(!filters.status||(filters.status==='multiple'?n.documentaryCandidates.length>1:n.status===filters.status))&&(!q||[n.nativePropertyName,n.nativeOriginalName,...n.documentaryCandidates.flatMap(c=>[c.documentCurrentName,...c.explicitCodeListLinks.map(l=>l.labelNative)])].filter(x=>typeof x==='string').some(x=>x.toLowerCase().includes(q)));});}
    function show(f){selected=f.id;const n=f.native,r=model.resources.get(n.sourceId),heading=el('h4',n.nativePropertyName);heading.tabIndex=-1;detail.replaceChildren(heading,
      el('p',STATUS[n.status]+'. '+n.collectionId+' · '+(n.resourceKind==='schemas'?'Schema':'Queryables')),
      el('p','Native originalName: '+(n.originalNamePresent?json(n.nativeOriginalName):'Not supplied (absent)')),
      el('p',(r.kind==='queryables'?'Version from companion feature schema: ':'Full-schema version context: ')+(r.versionContext.value===null?'Unresolved':r.versionContext.value)),
      el('p',r.versionContext.basis),el('p','Recorded request start: '+json(r.requestStartedAt)+'; end: '+json(r.requestFinishedAt)+'. These are not publication or validity dates.'),
      link('Native '+r.kind+' source',r.url),el('p','Native pointer: '+n.nativePointer));
      if(typeof n.nativeProperty.description==='string')detail.append(el('p',n.nativeProperty.description));
      if(n.documentaryCandidates.length===0)detail.append(el('p','No exact current-heading match in the selected retained pages. This does not establish missing data or a supplier error.'));
      for(const c of n.documentaryCandidates){const s=model.sections.get(c.documentSection).native,d=model.documents.get(s.source.id);
        const box=el('section');box.append(el('h5',c.documentCurrentName+' · '+c.attributeContext),el('p','Documentary data-schema versions: '+json(c.dataSchemaVersionNativeValues)),
          el('p','Source observed: '+d.observedAt+'. Publication date and adopted code-list edition remain unknown.'),link('Feature documentation',d.url));
        if(c.documentFormerlyNativeText!==null)box.append(el('p','Formerly text (not an alias): '+json(c.documentFormerlyNativeText)));
        if(!c.explicitCodeListLinks.length)box.append(el('p','No code-list link is admitted for this field/version context.'));
        for(const l of c.explicitCodeListLinks){box.append(link(l.labelNative,l.resolvedUrl),el('p','Explicit Code List Name · native lines '+l.sourceSpan.lineStart+'–'+l.sourceSpan.lineEnd+'; block '+l.blockOrdinal+' '+json(l.blockTitleNative)),
          el('p','Code List Version in this block: '+(l.codeListVersionNativeValues.length?json(l.codeListVersionNativeValues):'Not stated')+'; data-schema versions: '+json(l.dataSchemaVersionNativeValues)),
          el('p',(l.versionExplicitlyListedInSameMetadataBlock?'Documentary link candidate only. ':'Documentary link present; native version eligibility unresolved. ')+'API enum adoption, vocabulary edition and equivalence are not established.'));
        }
        box.append(details('Exact documentary section and source span',el('pre',s.nativeSection),el('pre',json(s.sectionSpan)),el('p','Source SHA-256: '+d.sha256)));detail.append(box);
      }
      detail.append(details('Native property and constraints ('+n.nativeConstraints.length+')',el('pre',json(n.nativeProperty)),el('pre',json(n.nativeConstraints))),
        details('Evidence identity and native resource root',el('pre',json(f.provenance)),el('p','Source SHA-256: '+n.sourceSha256),el('pre',json(r.nativeRootWithoutProperties))));heading.focus();
    }
    function render(){const rows=matches();page=Math.min(page,Math.max(0,Math.ceil(rows.length/PAGE)-1));list.replaceChildren();
      for(const f of rows.slice(page*PAGE,(page+1)*PAGE)){const b=el('button',f.native.nativePropertyName+' · '+f.native.collectionId+' · '+f.native.resourceKind);b.type='button';b.addEventListener('click',()=>show(f));const li=el('li');li.append(b);list.append(li);}
      count.textContent=rows.length+' matching property occurrences / '+data.fields.length+' retained. '+(rows.length?'Showing '+(page*PAGE+1)+'–'+Math.min((page+1)*PAGE,rows.length):'No matches in this selected scope.');previous.disabled=page===0;next.disabled=(page+1)*PAGE>=rows.length;
    }
    function setFilter(input){closed(input,['query','collection','kind','status']);const value={};for(const k of ['query','collection','kind','status']){const d=Object.getOwnPropertyDescriptor(input,k);need(d&&own(d,'value'));bounded(d.value,160);value[k]=d.value;}Object.freeze(value);
      need(value.collection===''||data.resources.some(r=>r.collectionId===value.collection));need(['','schemas','queryables'].includes(value.kind));need(value.status===''||value.status==='multiple'||own(STATUS,value.status));
      Object.assign(filters,value);search.value=filters.query;collection.value=filters.collection;kind.value=filters.kind;status.value=filters.status;page=0;selected=null;detail.replaceChildren();render();
    }
    const change=()=>setFilter({query:search.value,collection:collection.value,kind:kind.value,status:status.value});search.addEventListener('input',change);for(const n of[collection,kind,status])n.addEventListener('change',change);
    previous.addEventListener('click',()=>{if(page>0){page--;render();}});next.addEventListener('click',()=>{if((page+1)*PAGE<matches().length){page++;render();}});render();
    return Object.freeze({setFilter,snapshot:()=>Object.freeze({...filters,page,selected}),elements:{search,collection,kind,status,count,list,detail,previous,next,scopeNote}});
  }
  function mount(disclosure,container,text){let instance=null,failed=false;const load=()=>{if(!disclosure.open||instance||failed)return;
    try{instance=create(container,text);}catch(_){failed=true;container.replaceChildren();const p=container.ownerDocument.createElement('p');p.textContent='Field references could not be loaded. The existing code-list collection remains unchanged.';p.setAttribute('role','alert');container.append(p);}};
    disclosure.addEventListener('toggle',load);load();return Object.freeze({snapshot:()=>instance?instance.snapshot():null});
  }
  const api=Object.freeze({SCHEMA,CAP,PAGE,STATUS,parse,create,mount});scope.FieldDocumentaryBrowser=api;if(typeof module==='object'&&module.exports)module.exports=api;
})(typeof globalThis==='object'?globalThis:this);
