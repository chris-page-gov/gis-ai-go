'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path'),root=__dirname;
const contract=JSON.parse(fs.readFileSync(path.join(root,'OVERLAY-CONTRACT.v1.json'),'utf8'));
let focused=null,requests=0;const events={},nodes={};
class E{
 constructor(tag='div'){this.tag=tag;this.children=[];this.attributes={};this.dataset={};this.hidden=false;this.value='';this.textContent='';this.classList={toggle(){}};this.listeners={};}
 set id(value){this._id=value;nodes[value]=this} get id(){return this._id}
 append(...x){this.children.push(...x)} replaceChildren(...x){this.children=x}
 setAttribute(k,v){this.attributes[k]=String(v)} addEventListener(k,fn){this.listeners[k]=fn} focus(){focused=this}
}
for(const id of contract.requiredHostIds)nodes[id]=new E();
const skipReference=new E('a');
const panels=contract.taskIds.map(t=>{const e=nodes['task-'+t]=new E();e.id='task-'+t;nodes['title-'+t]=new E();return e});
const nav=contract.taskIds.map(t=>{const e=new E('button');e.dataset.task=t;return e});
const tabs=contract.referenceIds.map(t=>{const e=nodes['ref-tab-'+t]=new E('button');e.dataset.reference=t;nodes['ref-panel-'+t]=new E();return e});
const get=id=>{assert.ok(nodes[id],'Required host ID: '+id);return nodes[id]};
const el=(tag,text,cls)=>{const e=new E(tag);if(text!==undefined)e.textContent=text;e.className=cls;return e};
const tree=e=>[e,...e.children.flatMap(tree)],text=e=>tree(e).map(x=>x.textContent).join(' ');
const registry={terms:[{id:'synthetic-a',label:'Example area',definition:'A synthetic area definition.',aliases:[{value:'EA','kind':'project-search-variant','authority':'project','language':'en-GB'}],sourceRefs:['safe','unsafe']},{id:'synthetic-b',label:'Source term',definition:'Definition still to be reviewed.',domainContext:'Synthetic test context',example:{kind:'authored-synthetic-example',text:'Fictional example, not a native data observation.'},helpStatus:'source-only',sourceRefs:['safe']}],sources:[{id:'safe',title:'Synthetic reference',url:'https://example.invalid/reference',reviewState:'official-search-result-extract-reviewed'},{id:'unsafe',title:'Unsafe scheme',url:'javascript:alert(1)'}]};
const doc={body:{dataset:{}},createElement:t=>new E(t),querySelectorAll:s=>({'.task-panel':panels,'[data-task]':nav,'#task-navigator [data-task]':nav,'[data-reference]':tabs,'.skip-link[href="#reference-heading"]':[skipReference]}[s]||[])};
const context=vm.createContext({$:get,el,document:doc,URL,Set,window:{addEventListener:(k,v)=>events[k]=v,matchMedia:()=>({matches:false})},location:{hash:''},history:{pushState(_a,_b,h){context.location.hash=h}},fetch(){requests++;throw Error('No request admitted')}});
let source=fs.readFileSync(path.join(root,'experience.js'),'utf8');assert.equal(source.split('__VOCABULARY_REGISTRY__').length,2);source=source.replace('__VOCABULARY_REGISTRY__',JSON.stringify(registry));vm.runInContext(source,context);
const run=s=>vm.runInContext(s,context);nodes['learning-persona'].value='resident';run('initialiseExperience()');
let checks=0;function check(fn){fn();checks++}
check(()=>assert.equal(panels.filter(x=>!x.hidden).length,1));
check(()=>{run("experienceShow('areas')");assert.equal(focused,nodes['title-areas']);assert.equal(context.location.hash,'#task/areas')});
check(()=>{nodes['ref-tab-glossary'].listeners.click();nodes['glossary-search'].value='EA';run('experienceSearch()');assert.equal(nodes['glossary-results'].children.length,1);assert.ok(text(nodes['glossary-results']).includes('project-search-variant'))});
check(()=>{const links=tree(nodes['glossary-results']).filter(x=>x.tag==='a');assert.equal(links.length,1);assert.equal(links[0].href,'https://example.invalid/reference');assert.ok(text(nodes['glossary-results']).includes('full page not reviewed'))});
check(()=>{nodes['reference-pin'].onclick();run("experienceShow('groups')");assert.equal(nodes['ref-tab-glossary'].attributes['aria-selected'],'true');assert.equal(nodes['glossary-search'].value,'EA')});
check(()=>{run("experienceFold('reference',false,true)");assert.equal(focused,nodes['reference-toggle']);assert.equal(nodes['reference-inspector'].hidden,true);run("experienceFold('reference',true)");assert.equal(nodes['glossary-search'].value,'EA')});
check(()=>{nodes['reference-pin'].onclick();assert.equal(nodes['ref-tab-context'].attributes['aria-selected'],'true')});
check(()=>{let prevented=false;nodes['ref-tab-context'].listeners.keydown({key:'ArrowRight',preventDefault(){prevented=true}});assert.equal(focused,nodes['ref-tab-glossary']);assert.ok(prevented)});
check(()=>{nodes['reference-inspector'].listeners.keydown({key:'Escape',preventDefault(){}});assert.equal(nodes['reference-inspector'].hidden,true);assert.equal(focused,nodes['reference-toggle'])});
check(()=>{nodes['glossary-search'].value='unmatched';run('experienceSearch()');assert.ok(text(nodes['glossary-results']).includes('No matching definition'))});
check(()=>{nodes['glossary-search'].value='Source term';run('experienceSearch()');assert.ok(text(nodes['glossary-results']).includes('source guidance'))});
check(()=>assert.ok(text(nodes['glossary-results']).includes('Illustrative example')&&text(nodes['glossary-results']).includes('Fictional example, not a native data observation.')));
check(()=>{nodes['learning-next'].onclick();assert.ok(text(nodes['learning-stages']).includes('Compare like with like'));assert.equal(nodes['learning-stages'].children.length,1)});
check(()=>{run("experienceFeatureView('added')");assert.ok(nodes['earlier-feature-view'].hidden);assert.equal(nodes['added-feature-view'].hidden,false)});
check(()=>{run("experienceShow('unknown')");assert.equal(nodes['task-learn'].hidden,false)});
check(()=>{for(const task of contract.taskIds){run(`experienceContext('${task}')`);assert.ok(text(nodes['context-help']).includes('conceptual evidence groups'));assert.ok(tree(nodes['context-help']).some(x=>x.tag==='button'))}});
check(()=>{run("experienceShow('groups')");nodes.workspace.focus();context.location.hash='#workspace';events.hashchange();assert.equal(run('experienceTask'),'groups');assert.equal(focused,nodes.workspace)});
check(()=>{run("experienceFold('reference',false)");skipReference.listeners.click();nodes['reference-heading'].focus();context.location.hash='#reference-heading';events.hashchange();assert.equal(run('experienceTask'),'groups');assert.equal(nodes['reference-inspector'].hidden,false);assert.equal(focused,nodes['reference-heading'])});
check(()=>{context.location.hash='#task/areas';events.popstate();assert.equal(run('experienceTask'),'areas');context.location.hash='';events.popstate();assert.equal(run('experienceTask'),'learn')});
check(()=>assert.equal(requests,0));
console.log(JSON.stringify({passed:true,syntheticChecks:checks,networkRequests:requests,privateModelUsed:false,limits:['Synthetic DOM contract checks, not rendered browser or human evaluation.']},null,2));
