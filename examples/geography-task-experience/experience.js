/* Authored presentation v12. Learning progress is in memory, not an assessment. */
const experienceTasks = {
 learn:{title:'Start with a question',help:'Choose a goal and practise one small task. Use the check and safeguard before marking it tried.',check:'Can you explain the result and one limit in your own words?',concept:'Learning paths organise activities. They do not add data, execute queries or award a qualification.'},
 areas:{title:'Explore statistical areas',help:'Choose an area level, then a polygon or its code. Follow published membership to a smaller statistical area and inspect its retained UPRNs.',check:'Which link is exact-fit statistical membership, and which authority allocation is best-fit?',concept:'OA, LSOA and MSOA are statistical areas. A local authority is an organisation; its administrative area is a separate geography. Published memberships do not prove geometric containment.'},
 groups:{title:'Compare lookup groupings',help:'Choose a dimension and the cohort to count. Use the table for exact labels and the chart for a comparison of counts.',check:'Are you counting retained UPRNs, people, categories or measurements? Check the method and date beside the chart.',concept:'RUC and OAC are classifications. IMD rank is not an amount of deprivation. Category labels and search aliases are not numerical measures.'},
 features:{title:'Follow identifier links',help:'Choose an earlier road or building-part query, or an added native reference. Follow only the loaded source-owned links; an unloaded target stays an evidence gap.',check:'Which identifier type and source version establish this association? Is there an actual match, no match, or no response?',concept:'UPRN, USRN, TOID and OSID have different roles. A Site reference, Building-owned part reference or Street reference does not alone prove containment, access or a usable route.'},
 settlements:{title:'Compare settlements',help:'Compare the dated BUA assignments and the selected historical boundaries. The table works without drawing a map.',check:'What is the join field and which editions differ? What does the not-covered pseudo-code mean?',concept:'Built-up areas describe settlements rather than administrative authorities. Not covered is not rurality and is not a geometric complement.'},
 history:{title:'Inspect code dates',help:'Choose a code and compare its recorded instances. Keep the native source date meaning separate from the date of a drawn boundary.',check:'Does a date describe code use, a boundary, a publication or retrieval? A repeated code does not establish unchanged geometry.',concept:'The Register of Geographic Codes describes codes and instances. Code history and statistical allocation need their own evidence; no successor or crosswalk is inferred here.'},
 sources:{title:'Check methods and limits',help:'Compare the explanation routes, inspect the historical research note and follow its named sources. Proposal previews are labelled separately from observed views.',check:'Which statement is observed, which is a documented method, and which remains proposed?',concept:'Task groups are conceptual organisation for learning. Docker containers and storage directories are technical infrastructure, not geographic relationships.'}
};
const experienceCombinations={
 learn:{groups:[['Question and activity','JIT'],['Concept definitions','ontology'],['Source evidence','provenance']],relation:'A learning sequence connects a goal, activity, check and source; it does not add a data relationship.'},
 areas:{groups:[['Dated geography','OA'],['Published membership','MSOA'],['UPRN lookup','NSUL'],['Source evidence','provenance']],relation:'Published membership links selected statistical areas. The authority allocation and UPRN lookup retain their separate methods and dates.'},
 groups:{groups:[['Selected UPRNs','UPRN'],['Administrative allocation','ONSUD'],['Classifications','classification'],['Source evidence','provenance']],relation:'A declared cohort and lookup dimension produce category counts. The category is not a quantity, and the allocation method stays visible.'},
 features:{groups:[['Typed identifiers','UPRN'],['Identifier relationships','Linked Identifiers'],['Native features','OSID'],['Source evidence','provenance']],relation:'Source-owned identifier links lead to separately selected native observations. A link is not universal containment or a connected network.'},
 settlements:{groups:[['BUA assignment','BUA'],['Dated boundary','geography'],['Selected geography','OA'],['Source evidence','provenance']],relation:'An exact dated BUA code joins the supplied lookup and historical comparison. The map supplies context; no current-edition crosswalk is inferred.'},
 history:{groups:[['Native codes','GSS'],['Register instances','RGC'],['Distinct dates','epoch'],['Source evidence','provenance']],relation:'Native code instances and source-defined date fields support a history display. They do not establish boundary equivalence or succession.'},
 sources:{groups:[['Source claims','provenance'],['Definitions','ontology'],['Interpretations and gaps','JIT']],relation:'Evidence, interpretation and unresolved questions are shown separately. A proposed view is not another acquired dataset.'}
};
const experienceStages=[
 {id:'orient',task:'areas',title:'1. Identify the area',goal:'Know which area the question concerns.',activity:'Choose a level and an area code; follow one published membership.',outcome:'Name the area type and its edition.',safeguard:'Do not read containment from the picture.',source:'Published membership and boundary sources in Methods and limits.'},
 {id:'compare',task:'groups',title:'2. Compare like with like',goal:'Understand what a grouping chart counts.',activity:'Choose a classification and compare the table with its chart.',outcome:'State the denominator and the source meaning of a category.',safeguard:'UPRNs are not people; ranks and nominal classes are not quantities.',source:'ONSUD method, source labels and classification definitions beside the view.'},
 {id:'follow',task:'features',title:'3. Follow a typed link',goal:'Use identifier evidence before unnecessary spatial work.',activity:'Inspect a selected native observation and follow one loaded reference.',outcome:'Name its source, identifier type, version and outcome.',safeguard:'Association does not establish containment, accessibility or road access.',source:'Native reference, version fields and source-bound diagnostics in observation detail.'},
 {id:'contrast',task:'settlements',title:'4. Test a different geography',goal:'Distinguish a settlement from an authority.',activity:'Compare a dated BUA code assignment with its boundary evidence.',outcome:'Explain the date mismatch and the not-covered category.',safeguard:'Use the exact BUA24CD join only; no current-product crosswalk is inferred.',source:'ONS historical boundary source and separate lookup edition.'},
 {id:'verify',task:'history',title:'5. Check the dates and evidence',goal:'Make a defensible explanation.',activity:'Inspect a code instance, then check the methods and source links.',outcome:'Give one supported finding and one unresolved limit.',safeguard:'Code validity is not boundary validity. A practice tick is not proof.',source:'Register source fields and the dated source list.'}
];
const experiencePersonaPrompts={
 resident:'Try: “Which area is this, and what does its evidence mean?”',
 planner:'Try: “Which dated area and evidence would support a service question, and what would I need before a decision?”',
 analyst:'Try: “What is the denominator, and are these categories, ranks and dates suitable for comparison?”',
 specialist:'Try: “Which typed references, cardinality, versions and geometry limits support this route?”',
 steward:'Try: “Can I trace this native field, null and identifier to its source and preserved interpretation?”',
 teacher:'Try: “Can a learner explain one supported finding and one safeguard in their own words?”',
 reviewer:'Try: “Which claims are observed, proposed or unresolved, and what evidence would change that judgement?”'
};
// The small source-reviewed registry is embedded by the builder; no separate network request.
const experienceVocabulary = __VOCABULARY_REGISTRY__;
let experienceReady=false,experienceTask='learn',experienceReference='context',experiencePinned=false;
const experiencePractised=new Set();
let experienceLearningStep=0;
function experienceFeatureView(which){
 const added=which==='added';$('earlier-feature-view').hidden=added;$('added-feature-view').hidden=!added;
 $('show-earlier').setAttribute('aria-pressed',String(!added));$('show-added').setAttribute('aria-pressed',String(added));
}
function experienceFold(kind,open,focusReturn=false){
 const nav=kind==='navigator',panel=$(nav?'task-navigator':'reference-inspector'),button=$(nav?'navigator-toggle':'reference-toggle');
 panel.hidden=!open;button.setAttribute('aria-expanded',String(open));button.textContent=(open?'Hide ':'Show ')+(nav?'tasks':'reference');
 $('app-shell').classList.toggle(nav?'tasks-folded':'reference-folded',!open);if(focusReturn)button.focus();
}
function experienceReferenceTab(id,focus=false){
 if(!['context','glossary','dates'].includes(id))return;experienceReference=id;
 for(const tab of document.querySelectorAll('[data-reference]')){const active=tab.dataset.reference===id;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;$('ref-panel-'+tab.dataset.reference).hidden=!active;}
 if(focus)$('ref-tab-'+id).focus();
}
function experienceContext(task){
 const t=experienceTasks[task],box=$('context-help');box.replaceChildren(el('h3',t.title),el('p',t.help),el('h4','Check your interpretation'),el('p',t.check),el('h4','Keep this distinction'),el('p',t.concept));
 const combination=experienceCombinations[task];box.append(el('h4','What this task combines'));const badges=el('div',undefined,'concept-badges');for(const [label,query]of combination.groups){const button=el('button',label);button.type='button';button.setAttribute('aria-label','Find definitions for '+label);button.onclick=()=>{experienceReferenceTab('glossary');$('glossary-search').value=query;experienceSearch();$('glossary-search').focus();};badges.append(button);}box.append(badges,el('p',combination.relation,'muted'),el('p','These are conceptual evidence groups. The three UI panes organise the screen; Docker containers and storage folders are separate technical infrastructure.','muted'));
}
function experienceShow(task,focus=true,updateRoute=true){
 if(!experienceReady)return;if(!experienceTasks[task])task='learn';experienceTask=task;
 for(const panel of document.querySelectorAll('.task-panel'))panel.hidden=panel.id!=='task-'+task;
 for(const button of document.querySelectorAll('#task-navigator [data-task]'))button.setAttribute('aria-current',button.dataset.task===task?'page':'false');
 if(task==='areas'||task==='features')$(task==='areas'?'area-map-slot':'feature-map-slot').append($('map-workbench'));
 $('active-task-label').textContent=experienceTasks[task].title;
 if(!experiencePinned){experienceContext(task);experienceReferenceTab('context');}
 if(updateRoute&&location.hash!=='#task/'+task)history.pushState({task},'', '#task/'+task);
 if(focus){$('workspace').scrollTop=0;$('title-'+task).focus();}
}
function experienceRenderLearning(){
 $('persona-prompt').textContent=experiencePersonaPrompts[$('learning-persona').value];
 const stepper=$('learning-stepper');stepper.replaceChildren();experienceStages.forEach((stage,i)=>{const button=el('button',stage.title);button.type='button';button.setAttribute('aria-pressed',String(i===experienceLearningStep));button.onclick=()=>{experienceLearningStep=i;experienceRenderLearning();$('learning-stage-title').focus();};stepper.append(button);});
 const stage=experienceStages[experienceLearningStep],box=$('learning-stages');box.replaceChildren();const article=el('article',undefined,'learning-stage'),title=el('h3',stage.title);title.id='learning-stage-title';title.tabIndex=-1;article.append(title,el('p',stage.goal));const d=el('dl');for(const [name,value]of [['Try',stage.activity],['Observable outcome',stage.outcome],['Safeguard',stage.safeguard],['Evidence',stage.source]])d.append(el('dt',name),el('dd',value));article.append(d);const button=el('button','Try this activity');button.type='button';button.onclick=()=>experienceShow(stage.task);const label=el('label',undefined,'practice-tick'),check=document.createElement('input');check.type='checkbox';check.checked=experiencePractised.has(stage.id);check.onchange=()=>{if(check.checked)experiencePractised.add(stage.id);else experiencePractised.delete(stage.id);experienceProgress();};label.append(check,el('span','I tried this activity'));article.append(button,label);box.append(article);
 $('learning-previous').disabled=experienceLearningStep===0;$('learning-next').disabled=experienceLearningStep===experienceStages.length-1;experienceProgress();
}
function experienceProgress(){$('learning-progress').textContent=`${experiencePractised.size} of ${experienceStages.length} practice activities marked as tried. Stored in memory for this page only; not an assessment.`;}
function experienceSources(parent,refs){
 const list=el('ul');for(const id of refs||[]){const source=experienceVocabulary.sources.find(x=>x.id===id);if(!source)continue;let url;try{url=new URL(source.url);}catch{continue;}if(url.protocol!=='https:')continue;const li=el('li'),a=el('a',source.title);a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';li.append(a);if(source.reviewState){const reviews={'opened-primary-source-text':'Official primary source text reviewed','official-page-opened-text-reviewed':'Official page text reviewed','official-search-result-extract-reviewed':'Official search extract reviewed; full page not reviewed','local-pinned-project-file-read':'Pinned project source reviewed','source-reviewed-project-record-reused':'Source-reviewed project explanation reused','retained-guide-excerpt-reviewed':'Retained official guide excerpt reviewed'};li.append(el('span',' · '+(reviews[source.reviewState]||'Review scope recorded in the source registry'),'muted'));}list.append(li);}parent.append(list);
}
function experienceSearch(){
 const query=$('glossary-search').value.trim().toLocaleLowerCase('en-GB'),all=experienceVocabulary.terms;
 const terms=all.filter(t=>[t.label,t.definition,t.scopeNote,...(t.aliases||[]).map(a=>a.value)].filter(Boolean).some(x=>x.toLocaleLowerCase('en-GB').includes(query)));
 $('glossary-count').textContent=`${terms.length} ${terms.length===1?'entry':'entries'}${query?' matching your search':''}.`;
 const box=$('glossary-results');box.replaceChildren();
 if(!terms.length){box.append(el('p','No matching definition. Try a shorter term or an identifier such as UPRN. Search does not query a provider.'));return;}
 for(const term of terms){const d=el('details',undefined,'definition');d.open=terms.length===1;d.append(el('summary',term.label+(term.helpStatus==='source-only'?' · source guidance':'')),el('p',term.definition));if(term.domainContext)d.append(el('p','Context: '+term.domainContext,'muted'));if(term.scopeNote)d.append(el('p',term.scopeNote,'scope-note'));if(term.example?.kind==='authored-synthetic-example')d.append(el('h4','Illustrative example'),el('p',term.example.text));if(term.aliases?.length){const list=el('ul');for(const alias of term.aliases)list.append(el('li',`${alias.value} — ${alias.kind||'search variant'}${alias.authority?' · '+alias.authority:''}${alias.language?' · '+alias.language:''}`));d.append(el('h4','Labels and search variants'),list);}experienceSources(d,term.sourceRefs);box.append(d);}
}
function initialiseExperience(){
 experienceReady=true;$('journey-slot').append($('journey'));
 for(const button of document.querySelectorAll('[data-task]'))button.addEventListener('click',()=>experienceShow(button.dataset.task));
 for(const button of document.querySelectorAll('[data-reference]')){button.addEventListener('click',()=>experienceReferenceTab(button.dataset.reference));button.addEventListener('keydown',event=>{const ids=['context','glossary','dates'],i=ids.indexOf(button.dataset.reference);let next;if(event.key==='ArrowRight')next=(i+1)%3;else if(event.key==='ArrowLeft')next=(i+2)%3;else if(event.key==='Home')next=0;else if(event.key==='End')next=2;else return;event.preventDefault();experienceReferenceTab(ids[next],true);});}
 const navButtons=[...document.querySelectorAll('#task-navigator [data-task]')];navButtons.forEach((button,i)=>button.addEventListener('keydown',event=>{let next;if(event.key==='ArrowDown')next=(i+1)%navButtons.length;else if(event.key==='ArrowUp')next=(i+navButtons.length-1)%navButtons.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=navButtons.length-1;else return;event.preventDefault();navButtons[next].focus();}));
 $('navigator-toggle').onclick=()=>experienceFold('navigator',$('task-navigator').hidden);
 $('reference-toggle').onclick=()=>experienceFold('reference',$('reference-inspector').hidden);
 $('reference-pin').onclick=()=>{experiencePinned=!experiencePinned;$('reference-pin').setAttribute('aria-pressed',String(experiencePinned));$('reference-pin').textContent=experiencePinned?'Unpin reference':'Pin this reference';$('reference-pin-status').textContent=experiencePinned?'Pinned: changing tasks keeps this reference. You can still choose another reference tab.':'Follows the current task until pinned.';if(!experiencePinned){experienceContext(experienceTask);experienceReferenceTab('context');}};
 $('reference-inspector').addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();experienceFold('reference',false,true);}});
 $('task-navigator').addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();experienceFold('navigator',false,true);}});
 $('task-help').onclick=()=>{experienceFold('reference',true);experienceContext(experienceTask);experienceReferenceTab('context',true);};
 $('learning-previous').onclick=()=>{experienceLearningStep=Math.max(0,experienceLearningStep-1);experienceRenderLearning();$('learning-stage-title').focus();};$('learning-next').onclick=()=>{experienceLearningStep=Math.min(experienceStages.length-1,experienceLearningStep+1);experienceRenderLearning();$('learning-stage-title').focus();};
 $('glossary-search').oninput=experienceSearch;$('learning-persona').onchange=experienceRenderLearning;$('reset-learning').onclick=()=>{experiencePractised.clear();experienceRenderLearning();};
 $('show-earlier').onclick=()=>experienceFeatureView('earlier');$('show-added').onclick=()=>experienceFeatureView('added');
 const restoreTaskRoute=()=>{if(location.hash.startsWith('#task/'))experienceShow(location.hash.slice(6),false,false);else if(!location.hash)experienceShow('learn',false,false);};
 window.addEventListener('popstate',restoreTaskRoute);
 window.addEventListener('hashchange',restoreTaskRoute);
 for(const link of document.querySelectorAll('.skip-link[href="#reference-heading"]'))link.addEventListener('click',()=>experienceFold('reference',true));
 experienceRenderLearning();experienceSearch();experienceContext('learn');
 const initial=location.hash.startsWith('#task/')?location.hash.slice(6):'learn';experienceShow(initial,false,false);
 if(window.matchMedia('(max-width: 900px)').matches){experienceFold('navigator',false);experienceFold('reference',false);}
 document.body.dataset.ready='true';
}
