import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
// Local assembled-Site UI check. Provider requests are intercepted, never forwarded.
const root=resolve(import.meta.dirname,'..'), require=createRequire(root+'/apps/public-data-workbench/package.json');
assert.equal(process.argv.length,2,'This check uses only the fixed localhost:4177 preview');
const {chromium}=require('@playwright/test');
const {default:AxeBuilder}=require('@axe-core/playwright');
const origin='http://localhost:4177';
const report={schema:'gis-ai-go.experience-pilot-page-observation.v1',at:new Date().toISOString(),scope:'Local assembled Site; MCP responses intercepted with synthetic data; no hosted identity or live-provider acceptance.',requests:[],tests:[],pageErrors:[],httpErrors:[]};
await mkdir(root+'/artifacts/experience',{recursive:true});await mkdir(root+'/output/playwright/experience',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true,timeout:15000});
const deadline=setTimeout(()=>{report.status='deadline-exceeded';process.exitCode=1;void browser.close();},90000);deadline.unref();
try {
 const context=await browser.newContext({viewport:{width:1280,height:900}});const page=await context.newPage();page.setDefaultTimeout(10000);page.setDefaultNavigationTimeout(15000);page.on('pageerror',e=>report.pageErrors.push(e.message));page.on('response',response=>{if(response.status()>=400)report.httpErrors.push({status:response.status(),path:new URL(response.url()).pathname});});
 await page.route('**/*',async route=>{const request=route.request(),u=new URL(request.url());if(u.origin!==origin){report.requests.push({kind:'blocked-external',origin:u.origin,path:u.pathname});await route.abort();return;}
  if(u.pathname!=='/pilot/mcp'){await route.continue();return;}
  const body=request.postDataJSON();report.requests.push({kind:'mock-mcp',method:body.method,tool:body.params?.name??null});
  if(body.id===undefined){await route.fulfill({status:202,body:''});return;}
  const result=body.method==='initialize'?{protocolVersion:'2025-11-25',capabilities:{tools:{}},serverInfo:{name:'synthetic-page-check',version:'1'}}:{content:[],structuredContent:{schema:'gis-ai-go.sites-pilot-capabilities.v1',tool:'sites_capabilities',data:{providers:{psga:'disabled-rights-not-established'}},evidence:{provider_egress:false}}};
  await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({jsonrpc:'2.0',id:body.id,result})});
 });
 await page.goto(origin+'/pilot',{waitUntil:'networkidle',timeout:30000});await page.locator('#pilot-operation').waitFor();
 const features={sites_os_names:'pilot-names',sites_ons_areas:'pilot-areas',sites_ons_cpih:'pilot-cpih',sites_os_open_product:'pilot-product',sites_capabilities:'pilot-capabilities',sites_evidence_inspect:'pilot-inspect'};
 const choices=await page.locator('#pilot-operation option').evaluateAll(xs=>xs.map(x=>x.value));assert.equal(choices.length,6);
 for(const value of choices){await page.locator('#pilot-operation').selectOption(value);const panel=page.locator('.pilot-learning');assert((await panel.innerText()).length>100);const href=await panel.locator('a').getAttribute('href');assert.equal(href,'/experience/experience.html#feature='+features[value]+'&view=cards');report.tests.push({id:value+'-learning',passed:true});}
 await page.locator('#pilot-operation').selectOption('sites_capabilities');await page.getByRole('button',{name:'Run question',exact:true}).click();await page.getByRole('heading',{name:'Result',exact:true}).waitFor();assert((await page.locator('.pilot-result').innerText()).includes('PSGA data remains disabled'));report.tests.push({id:'synthetic-capability-journey',passed:true});
 for(const width of [390,1280]){await page.setViewportSize({width,height:900});const scan=await new AxeBuilder({page}).analyze();assert.equal(scan.violations.length,0);const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);assert.equal(overflow,false);await page.locator('#pilot-operation').focus();for(let i=0;i<6;i++){await page.keyboard.press('Tab');const focus=await page.evaluate(()=>{const e=document.activeElement;if(!e||e===document.body)return true;const r=e.getBoundingClientRect();if(r.width===0||r.height===0)return false;const x=Math.min(innerWidth-1,Math.max(0,r.left+r.width/2)),y=Math.min(innerHeight-1,Math.max(0,r.top+r.height/2));const hit=document.elementFromPoint(x,y);return {visible:e===hit||e.contains(hit),id:e.id,tag:e.tagName,rect:{x:r.x,y:r.y,width:r.width,height:r.height},hit:hit?.tagName,hitClass:hit?.className};});if(focus!==true&&!focus.visible){report.focusFailure=focus;await page.screenshot({path:root+'/output/playwright/experience/pilot-focus-failure.png'});}assert(focus===true||focus.visible,'Pilot keyboard focus must remain visible');}report.tests.push({id:'layout-'+width,passed:true,axeViolations:0});await page.screenshot({path:root+'/output/playwright/experience/pilot-'+width+'.png'});}
 await page.locator('.pilot-learning a').click();await page.locator('#example-choice').waitFor();assert(['/experience/experience.html','/experience/experience'].includes(new URL(page.url()).pathname));report.tests.push({id:'learning-link-and-assets',passed:true});
 assert.equal(report.requests.filter(x=>x.kind==='blocked-external').length,0);assert.equal(report.pageErrors.length,0);assert.equal(report.httpErrors.length,0);assert.equal(report.requests.filter(x=>x.kind==='mock-mcp').length,3);
 report.sourceSha256=createHash('sha256').update(await readFile(root+'/artifacts/sites-source/app/pilot/page.tsx')).digest('hex');report.status='passed';
} catch(e){report.status='failed';report.error=String(e).replaceAll(root,'<repository>');process.exitCode=1;}
finally{clearTimeout(deadline);await browser.close();await writeFile(root+'/artifacts/experience/pilot-page-report.json',JSON.stringify(report,(_key,value)=>typeof value==='string'?value.replaceAll(root,'<repository>').replace(/\u001b\[[0-9;]*m/gu,''):value,2)+'\n');console.log(JSON.stringify(report));}
