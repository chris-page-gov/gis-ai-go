import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname, sep } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const build = resolve(root, 'apps/public-data-workbench/dist/experience-offline');
const output = resolve(root, 'artifacts/experience');
let html = await readFile(resolve(build, 'experience.html'), 'utf8');
const inputs = [];
async function asset(path) {
  const resolved = resolve(build, path); assert(resolved.startsWith(build + sep), 'Asset must stay inside the build');
  const bytes = await readFile(resolved); assert(bytes.length < 2_097_152, 'Bounded teaching bundle');
  inputs.push({ path, sha256: createHash('sha256').update(bytes).digest('hex') }); return bytes.toString('utf8');
}
const scripts = [...html.matchAll(/<script type="module" crossorigin src="([^"]+)"><\/script>/g)];
assert.equal(scripts.length, 1, 'Use the single-entry experience-offline build');
const code = await asset(scripts[0][1]);
assert(!/\bimport\s*(?:["'{*]|\()/u.test(code), 'Offline entry must have no remaining imports');
html = html.replace(scripts[0][0], `<script type="module">${code.replace(/<\/script/giu, '<\\/script')}</script>`);
for (const match of [...html.matchAll(/<link rel="stylesheet" crossorigin href="([^"]+)">/g)]) {
  const css = await asset(match[1]); html = html.replace(match[0], `<style>${css.replace(/<\/style/giu, '<\\/style')}</style>`);
}
assert(!/<(?:script|link)[^>]+(?:src|href)="\.?\/assets\//u.test(html));
html = html.replace('<a href="./index.html">GIS AI GO</a>', '<span>GIS AI GO · offline activity</span>');
await mkdir(output, { recursive: true });
await writeFile(resolve(output, 'learn-by-trying.html'), html);
const receipt = { schema: 'gis-ai-go.experience-offline-package.v1', inputs, sha256: createHash('sha256').update(html).digest('hex'), bytes: Buffer.byteLength(html), networkRequiredForActivities: false, liveProviderCalls: false };
await writeFile(resolve(output, 'offline-package-receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify({ output: resolve(output, 'learn-by-trying.html'), ...receipt }));
