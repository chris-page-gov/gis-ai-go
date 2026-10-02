/** Offline authored-coverage and source-drift checks; never executes prompts or provider calls. */
import { createHash } from 'node:crypto';
import { readFile, lstat, realpath, mkdir, writeFile } from 'node:fs/promises';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { isDeepStrictEqual } from 'node:util';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const CATALOGUE_PATH = 'evaluation/experience/catalogue.v1.json';
export const LOCAL_FIXTURES_PATH = 'evaluation/experience/local-fixtures.v1.json';
export const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const requireThat = (condition, message) => { if (!condition) throw new Error(message); };
const isObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const text = (value) => typeof value === 'string' && value.trim().length > 0;
const array = (value) => Array.isArray(value) && value.length > 0;
const unique = (values) => new Set(values).size === values.length;
const safePath = (value) => text(value) && !isAbsolute(value) && !value.includes('\\') && !value.split('/').some((part) => part === '..' || part === '.' || part === '');
const setEqual = (a, b) => a.length === b.length && [...a].sort().every((v, i) => v === [...b].sort()[i]);
function collection(doc, key) {
  requireThat(array(doc[key]), `${key}: expected a non-empty array`);
  requireThat(doc[key].every((row) => isObject(row) && text(row.id)), `${key}: missing identifier`);
  requireThat(unique(doc[key].map((row) => row.id)), `${key}: duplicate identifier`);
  return new Map(doc[key].map((row) => [row.id, row]));
}
function refs(row, key, target, context) {
  requireThat(array(row[key]) && unique(row[key]) && row[key].every((id) => target.has(id)), `${context}: invalid ${key}`);
}
export function validateCatalogue(doc) {
  requireThat(isObject(doc) && doc.schema === 'gis-ai-go.experience-catalogue.v1', 'Unsupported catalogue schema');
  requireThat(/^\d{4}-\d{2}-\d{2}$/u.test(doc.statusDate), 'Missing status date');
  requireThat(/^[a-f0-9]{40}$/u.test(doc.baselineCommit), 'Missing baseline commit');
  const keys = ['personas', 'sources', 'concepts', 'presentationForms', 'features', 'stories', 'questions'];
  const maps = Object.fromEntries(keys.map((key) => [key, collection(doc, key)]));
  for (const p of doc.personas) requireThat(text(p.languageStyle) && text(p.need) && p.researchStatus === 'authored-hypothesis', `${p.id}: persona research boundary missing`);
  for (const source of doc.sources) {
    requireThat(text(source.apiOrData) && text(source.rightsBoundary) && array(source.repositoryPaths), `${source.id}: source binding missing`);
    requireThat(source.repositoryPaths.every(safePath), `${source.id}: unsafe repository path`);
    requireThat(Array.isArray(source.urls) && source.urls.every((url) => /^https:\/\//u.test(url)), `${source.id}: source URL must use HTTPS`);
  }
  for (const row of [...doc.concepts, ...doc.presentationForms, ...doc.features, ...doc.stories, ...doc.questions]) {
    requireThat(text(row.jitSummary) && row.jitSummary.length <= 520, `${row.id}: missing or oversized JIT summary`);
  }
  for (const concept of doc.concepts) refs(concept, 'sourceIds', maps.sources, concept.id);
  for (const row of [...doc.features, ...doc.stories, ...doc.questions]) {
    refs(row, 'sourceIds', maps.sources, row.id);
    refs(row, 'conceptIds', maps.concepts, row.id);
    refs(row, 'presentationFormIds', maps.presentationForms, row.id);
  }
  for (const feature of doc.features) {
    requireThat(['current', 'planned'].includes(feature.status) && text(feature.operation) && text(feature.boundary), `${feature.id}: capability boundary missing`);
    requireThat(array(feature.implementationPaths) && feature.implementationPaths.every(safePath), `${feature.id}: implementation binding missing`);
    if (feature.status === 'current') requireThat(['accepted-baseline-source-declaration', 'local-increment-unaccepted'].includes(feature.maturity), `${feature.id}: implementation maturity missing`);
    if (feature.status === 'planned') requireThat(array(feature.acceptanceQuestions) && feature.acceptanceQuestions.every((q) => q.executionStatus === 'not-run'), `${feature.id}: planned acceptance must remain unassessed`);
    if (feature.parentFeatureId !== undefined) requireThat(maps.features.has(feature.parentFeatureId) && feature.parentFeatureId !== feature.id, `${feature.id}: invalid parent feature`);
  }
  for (const story of doc.stories) {
    refs(story, 'featureIds', maps.features, story.id); refs(story, 'personaIds', maps.personas, story.id);
    requireThat(story.personaIds.includes(story.primaryPersonaId) && array(story.completionCriteria) && array(story.componentNeeds), `${story.id}: user need or outcome missing`);
  }
  const variantIds = [];
  for (const q of doc.questions) {
    requireThat(maps.stories.has(q.storyId), `${q.id}: unknown story`);
    refs(q, 'featureIds', maps.features, q.id);
    const story = maps.stories.get(q.storyId);
    requireThat(q.featureIds.every((id) => story.featureIds.includes(id)), `${q.id}: story/feature mismatch`);
    requireThat(text(q.prompt) && ['positive', 'clarification', 'negative'].includes(q.caseType), `${q.id}: invalid question`);
    requireThat(q.executionStatus === 'not-run' && q.providerCallsAuthorisedByThisCase === false && q.executionPlane === 'human-or-ai-client', `${q.id}: authored material cannot claim execution or authority`);
    requireThat(array(q.variants) && q.variants.every((v) => text(v.id) && text(v.text) && maps.personas.has(v.personaId)), `${q.id}: missing language variant`);
    requireThat(unique(q.variants.map((v) => v.personaId)), `${q.id}: repeated persona variant`);
    variantIds.push(...q.variants.map((v) => v.id));
    if (q.caseType === 'positive') requireThat(setEqual(q.variants.map((v) => v.personaId), [...maps.personas.keys()]), `${q.id}: positive question lacks a persona variant`);
    requireThat(array(q.assertions) && q.assertions.every((a) => text(a.id) && text(a.description)) && unique(q.assertions.map((a) => a.id)), `${q.id}: assertion contract missing`);
    requireThat(setEqual(q.expected, q.assertions.map((a) => a.description)), `${q.id}: expected/assertion mismatch`);
    for (const fid of q.featureIds) {
      const f = maps.features.get(fid);
      requireThat(f.sourceIds.every((id) => q.sourceIds.includes(id)) && f.conceptIds.every((id) => q.conceptIds.includes(id)), `${q.id}: feature source or concept omitted`);
    }
    if (q.typedCall !== undefined) {
      requireThat(q.caseType === 'positive' && q.featureIds.every((id) => maps.features.get(id).surface === 'private-sites'), `${q.id}: typed recipe outside private Site positive cases`);
      requireThat(isObject(q.typedCall) && isObject(q.typedCall.arguments) && q.featureIds.some((id) => maps.features.get(id).operation === q.typedCall.name) && text(q.typedCallBoundary), `${q.id}: invalid typed recipe`);
    }
  }
  requireThat(unique(variantIds), 'Duplicate language-variant identifier');
  const current = doc.features.filter((f) => f.status === 'current');
  for (const f of current) {
    requireThat(doc.stories.some((s) => s.featureIds.includes(f.id)), `${f.id}: missing story`);
    for (const type of ['positive', 'clarification', 'negative']) requireThat(doc.questions.some((q) => q.featureIds.includes(f.id) && q.caseType === type), `${f.id}: missing ${type} case`);
  }
  for (const activity of doc.eventActivities ?? []) {
    refs(activity, 'featureIds', maps.features, activity.id);
    requireThat(maps.personas.has(activity.personaId) && text(activity.prompt) && text(activity.jitSummary) && text(activity.output), `${activity.id}: incomplete event activity`);
  }
  return { currentFeatures: current.length, baselineFeatures: current.filter((f) => f.maturity === 'accepted-baseline-source-declaration').length,
    newLocalFeatures: current.filter((f) => f.maturity === 'local-increment-unaccepted').length, plannedFeatures: doc.features.length - current.length,
    personas: doc.personas.length, concepts: doc.concepts.length, stories: doc.stories.length, questions: doc.questions.length,
    languageVariants: variantIds.length, authoredCurrentFeatureCoveragePercent: 100, authoredPositivePersonaCoveragePercent: 100 };
}

async function boundedLocal(root, name, maximum = 8_388_608) {
  requireThat(safePath(name), `Unsafe evidence path: ${name}`);
  const path = resolve(root, name), canonical = await realpath(path), rel = relative(await realpath(root), canonical);
  requireThat(rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel), `Path escapes repository: ${name}`);
  const stat = await lstat(path);
  requireThat(!stat.isSymbolicLink() && stat.isFile() && stat.size <= maximum, `Not a bounded regular file: ${name}`);
  return readFile(path);
}
export async function verifySourceBindings(doc, root = ROOT) {
  const paths = new Set([...doc.sources.flatMap((s) => s.repositoryPaths), ...doc.features.flatMap((f) => f.implementationPaths)]);
  for (const path of paths) {
    requireThat(safePath(path), `Unsafe source path: ${path}`);
    const stat = await lstat(resolve(root, path));
    requireThat(stat.isFile() || stat.isDirectory(), `Source path missing: ${path}`);
  }
  const read = async (path) => (await boundedLocal(root, path)).toString('utf8');
  const pilot = await read('apps/mcp-gateway/src/sites-pilot-http.ts');
  const local = await read('scripts/local214_demo.mjs');
  const page = await read('apps/webmcp-explorer/src/webmcp-adapter.ts');
  const workbench = await read('apps/public-data-workbench/src/webmcp.ts');
  const experience = await read('apps/public-data-workbench/src/experience-tools.ts');
  const capture = await read('apps/mcp-gateway/src/web216-cpih-mcp.ts');
  const publicUi = await read('apps/public-explorer/src/main.ts');
  const constantStrings = (source, name) => {
    const match = source.match(new RegExp(`const ${name} = (?:Object\\.freeze\\()?\\[([\\s\\S]*?)\\]`));
    requireThat(match, `Cannot discover ${name}`); return [...match[1].matchAll(/"([^"]+)"/gu)].map((m) => m[1]);
  };
  const inventories = [
    ['private-sites', [...pilot.slice(pilot.indexOf('SITES_PILOT_INPUTS'), pilot.indexOf('export type SitesPilotTool')).matchAll(/^  (sites_[a-z_]+): object/gmu)].map((m) => m[1])],
    ['local-mcp', constantStrings(local, 'OPERATIONS')], ['local-mcp-resource', constantStrings(local, 'RESOURCES')],
    ['explorer-page-tools', constantStrings(page, 'WEBMCP_TOOL_NAMES')],
    ['local-workbench', [...workbench.matchAll(/\{ name: "(workbench_[a-z_]+)"/gu)].map((m) => m[1])],
    ['captured-cpih-mcp', constantStrings(capture, 'WEB216_CPIH_MCP_TOOLS')],
    ['local-learning-workbench', constantStrings(experience, 'EXPERIENCE_TOOL_NAMES')],
  ];
  for (const [surface, operations] of inventories) {
    const declared = doc.features.filter((f) => f.status === 'current' && f.surface === surface && (surface !== 'local-learning-workbench' || f.operation.startsWith('experience_'))).map((f) => f.operation);
    requireThat(operations.length > 0 && setEqual(declared, operations), `${surface}: source operation inventory differs from authored feature denominator`);
  }
  const facets = [...publicUi.matchAll(/facetGroup\("([^"]+)"/gu)].map((m) => `filter-${m[1].toLowerCase()}`);
  const declaredFacets = doc.features.filter((f) => f.surface === 'public-explorer' && f.operation.startsWith('filter-')).map((f) => f.operation);
  requireThat(setEqual(facets, declaredFacets), 'Public Explorer facet inventory drift');
  const oldCases = JSON.parse(await read('evaluation/sites-mcp-pilot-cases.v1.json')).cases;
  for (const q of doc.questions.filter((q) => q.typedCall)) {
    requireThat(oldCases.some((c) => c.tool === q.typedCall.name && JSON.stringify(c.arguments) === JSON.stringify(q.typedCall.arguments)) || (q.typedCall.name === 'sites_capabilities' && Object.keys(q.typedCall.arguments).length === 0), `${q.id}: typed recipe has no existing bounded corpus anchor`);
  }
  return { checkedPaths: paths.size, exactOperationInventories: inventories.map(([surface, ops]) => ({ surface, count: ops.length })), publicFacets: facets.length, networkRequests: 0 };
}

export function validateLocalFixtures(doc, fixtures) {
  requireThat(fixtures?.schema === 'gis-ai-go.experience-local-fixtures.v1' && array(fixtures.cases), 'Unsupported local fixture schema');
  requireThat(unique(fixtures.cases.map((c) => c.id)), 'Duplicate local fixture identifier');
  const features = new Map(doc.features.map((f) => [f.id, f])), sources = new Map(doc.sources.map((s) => [s.id, s]));
  for (const c of fixtures.cases) {
    requireThat(text(c.id) && text(c.question) && text(c.jitSummary) && c.executionPlane === 'deterministic-local-fixture', 'Incomplete deterministic fixture');
    refs(c, 'featureIds', features, c.id); refs(c, 'sourceIds', sources, c.id);
    requireThat(['plan', 'zip'].includes(c.operation) && isObject(c.input) && array(c.checks), `${c.id}: unsupported fixture operation`);
    requireThat(c.checks.every((check) => /^\/(?:[A-Za-z0-9_-]+\/)*[A-Za-z0-9_-]+$/u.test(check.path) && (Object.hasOwn(check, 'equals') !== Object.hasOwn(check, 'absent')) && (check.absent === undefined || check.absent === true)), `${c.id}: invalid fixture assertion`);
    if (c.input.fixture !== undefined) requireThat(safePath(c.input.fixture) && c.input.fixture.startsWith('packages/experience-intake/examples/'), `${c.id}: fixture must use a retained synthetic example`);
  }
  return { cases: fixtures.cases.length, featureIds: [...new Set(fixtures.cases.flatMap((c) => c.featureIds))].sort(), executionPlane: 'deterministic-local-fixture', naturalLanguageEvaluations: 0 };
}

// Synthetic stored ZIP with empty members. It tests inventory, never real map data.
function emptyMemberZip(names) {
  requireThat(Array.isArray(names) && names.length <= 64 && names.every((n) => text(n) && n.length <= 1024), 'Invalid synthetic ZIP members');
  const locals = [], central = []; let offset = 0;
  for (const name of names) {
    const label = Buffer.from(name), local = Buffer.alloc(30), entry = Buffer.alloc(46);
    local.writeUInt32LE(0x04034b50); local.writeUInt16LE(20, 4); local.writeUInt16LE(0x0800, 6); local.writeUInt16LE(label.length, 26);
    entry.writeUInt32LE(0x02014b50); entry.writeUInt16LE(0x0314, 4); entry.writeUInt16LE(20, 6); entry.writeUInt16LE(0x0800, 8); entry.writeUInt16LE(label.length, 28); entry.writeUInt32LE(offset, 42);
    locals.push(local, label); central.push(entry, label); offset += local.length + label.length;
  }
  const directory = Buffer.concat(central), end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50); end.writeUInt16LE(names.length, 8); end.writeUInt16LE(names.length, 10); end.writeUInt32LE(directory.length, 12); end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, directory, end]);
}

export async function runLocalFixtures(doc, fixtures, root = ROOT) {
  const inventory = validateLocalFixtures(doc, fixtures);
  const modulePath = 'packages/experience-intake/dist/src/index.js';
  const sourcePaths = ['index', 'previews', 'strict-json', 'types', 'zip'].map((name) => `packages/experience-intake/src/${name}.ts`);
  const runtimePaths = ['index', 'previews', 'strict-json', 'zip'].map((name) => `packages/experience-intake/dist/src/${name}.js`);
  const bindings = await Promise.all([...sourcePaths, ...runtimePaths].map(async (path) => ({ path, sha256: sha256(await boundedLocal(root, path)) })));
  const api = await import(pathToFileURL(resolve(root, modulePath)).href);
  const results = [];
  for (const c of fixtures.cases) {
    let request = structuredClone(c.input), result;
    if (c.operation === 'zip') result = api.inspectZipArchive('synthetic.zip', emptyMemberZip(request.members));
    else {
      if (request.fixture) {
        const content = await boundedLocal(root, request.fixture, 262144);
        request = { files: [{ name: request.fixture.split('/').at(-1), size: content.byteLength, text: content.toString('utf8') }] };
      } else if (request.files) request.files = request.files.map((f) => ({ ...f, size: f.size ?? Buffer.byteLength(f.text ?? '') }));
      result = api.planIntake(request);
    }
    const readPointer = (pointer) => {
      let value = result;
      for (const key of pointer.slice(1).split('/')) {
        if (value === null || typeof value !== 'object' || !Object.hasOwn(value, key)) return { present: false };
        value = value[key];
      }
      return { present: true, value };
    };
    const checks = c.checks.map((check) => { const found = readPointer(check.path); return { path: check.path, passed: check.absent === true ? !found.present : found.present && isDeepStrictEqual(found.value, check.equals) }; });
    const policyPassed = result.policy.networkRequests === 0 && result.policy.persistedFiles === 0 && result.policy.executesContent === false;
    results.push({ id: c.id, featureIds: c.featureIds, outcome: checks.every((c) => c.passed) && policyPassed ? 'passed' : 'failed', checks, policyPassed, resultSha256: sha256(JSON.stringify(result)) });
  }
  return { ...inventory, executed: true, sourceAndRuntimeBindings: bindings, nodeVersion: process.version,
    passed: results.filter((r) => r.outcome === 'passed').length, failed: results.filter((r) => r.outcome === 'failed').length,
    providerCalls: 0, modelCalls: 0, results,
    limitation: 'Direct deterministic calls against synthetic inputs. Not a browser interaction, independent participant result, AI interpretation or voice evaluation. Build the package immediately before this run; source and runtime digests are both retained.' };
}

/** Checks evidence integrity and aggregates declared reviewer outcomes, not answer truth. */
export async function evaluateObservations(doc, observations, catalogueDigest, root = ROOT) {
  requireThat(isObject(observations) && observations.schema === 'gis-ai-go.experience-observations.v1' && Array.isArray(observations.observations), 'Unsupported observation schema');
  requireThat(observations.catalogueSha256 === catalogueDigest, 'Observation catalogue digest mismatch');
  requireThat(/^[a-f0-9]{40}$/u.test(observations.runtimeRevision), 'Observation runtime revision required');
  const questions = new Map(doc.questions.map((q) => [q.id, q]));
  const runs = [], seen = new Set();
  for (const o of observations.observations) {
    const q = questions.get(o.questionId);
    requireThat(q && q.variants.some((v) => v.id === o.variantId), 'Unknown question or variant in observation');
    requireThat(['typed-client', 'ai-text', 'ai-voice', 'participant'].includes(o.plane), 'Unknown observation plane');
    requireThat(text(o.reviewerRole) && text(o.client) && text(o.observedAt) && Number.isFinite(Date.parse(o.observedAt)), 'Reviewer role, client and date required');
    const status = o.status ?? 'completed';
    requireThat(['completed', 'blocked'].includes(status), 'Unknown observation status');
    if (status === 'blocked') {
      requireThat(['authentication', 'client-unavailable', 'unsupported', 'input-not-available', 'timeout', 'permission', 'other-reviewed'].includes(o.blockReasonCode), 'Blocked observation needs a reason code');
      requireThat(Array.isArray(o.assertionResults) && o.assertionResults.length === 0, 'Blocked observation cannot claim assertion results');
    } else {
      requireThat(Array.isArray(o.assertionResults) && setEqual(o.assertionResults.map((r) => r.id), q.assertions.map((a) => a.id)), 'Observation must account for every expected assertion');
      requireThat(o.assertionResults.every((r) => typeof r.passed === 'boolean' && text(r.evidencePointer)), 'Assertion result needs explicit verdict and evidence pointer');
    }
    if (o.rubric !== undefined) {
      requireThat(isObject(o.rubric) && Object.keys(o.rubric).every((k) => ['taskCompletion', 'comprehension', 'sourceCorrectness', 'latencyMs'].includes(k)), 'Unknown rubric field');
      requireThat(o.rubric.taskCompletion === undefined || ['independent', 'one-hint', 'repeated-help', 'not-completed', 'not-assessed'].includes(o.rubric.taskCompletion), 'Unknown task-completion rating');
      requireThat(o.rubric.comprehension === undefined || ['own-words', 'partial', 'not-yet', 'not-assessed'].includes(o.rubric.comprehension), 'Unknown comprehension rating');
      requireThat(o.rubric.sourceCorrectness === undefined || ['correct', 'incorrect', 'not-assessed'].includes(o.rubric.sourceCorrectness), 'Unknown source-correctness rating');
      requireThat(o.rubric.latencyMs === undefined || Number.isSafeInteger(o.rubric.latencyMs) && o.rubric.latencyMs >= 0 && o.rubric.latencyMs <= 3_600_000, 'Invalid latency observation');
    }
    requireThat(/^[a-f0-9]{64}$/u.test(o.evidenceSha256), 'Evidence SHA-256 required');
    const bytes = await boundedLocal(root, o.evidencePath);
    requireThat(sha256(bytes) === o.evidenceSha256, 'Observation evidence digest mismatch');
    const key = `${o.questionId}/${o.variantId}/${o.plane}`;
    requireThat(!seen.has(key), 'Duplicate observation'); seen.add(key);
    runs.push({ questionId: o.questionId, variantId: o.variantId, plane: o.plane, status,
      recordedOutcome: status === 'blocked' ? 'blocked' : o.assertionResults.every((r) => r.passed) ? 'reviewer-reported-pass' : 'reviewer-reported-fail',
      ...(status === 'blocked' ? { blockReasonCode: o.blockReasonCode } : {}), ...(o.rubric === undefined ? {} : { rubric: o.rubric }), evidenceSha256: o.evidenceSha256 });
  }
  const completed = runs.filter((r) => r.status === 'completed');
  return { schema: observations.schema, runtimeRevision: observations.runtimeRevision, integrityChecked: true,
    verdictAuthority: 'Supplied reviewer judgements; this aggregator does not assess meaning, independence or factual correctness.',
    runs, recordedRuns: runs.length, reportedPasses: runs.filter((r) => r.recordedOutcome === 'reviewer-reported-pass').length,
    blockedRuns: runs.length - completed.length,
    typedClientRuns: completed.filter((r) => r.plane === 'typed-client').length,
    naturalLanguageRuns: completed.filter((r) => r.plane !== 'typed-client').length,
    unobservedQuestionCount: doc.questions.length - new Set(completed.map((r) => r.questionId)).size,
    unobservedNaturalLanguageQuestionCount: doc.questions.length - new Set(completed.filter((r) => r.plane !== 'typed-client').map((r) => r.questionId)).size };
}

export async function evaluate({ root = ROOT, observationsPath, localFixtures = false } = {}) {
  const bytes = await boundedLocal(root, CATALOGUE_PATH), doc = JSON.parse(bytes);
  const authored = validateCatalogue(doc), sourceBindings = await verifySourceBindings(doc, root), digest = sha256(bytes);
  const fixtureBytes = await boundedLocal(root, LOCAL_FIXTURES_PATH), fixtureDoc = JSON.parse(fixtureBytes);
  const fixtureInventory = validateLocalFixtures(doc, fixtureDoc);
  const deterministicFixtures = localFixtures ? await runLocalFixtures(doc, fixtureDoc, root) : { ...fixtureInventory, executed: false, reason: 'Use --run-local-fixtures after building the intake package. No deterministic execution is claimed by a coverage check.' };
  const observations = observationsPath ? await evaluateObservations(doc, JSON.parse(await boundedLocal(root, observationsPath)), digest, root) : {
    recordedRuns: 0, naturalLanguageRuns: 0, typedClientRuns: 0, unobservedQuestionCount: doc.questions.length,
    unobservedNaturalLanguageQuestionCount: doc.questions.length,
    verdictAuthority: 'No observations supplied. Authored questions, existing-test anchors and source checks are not execution results.' };
  return { schema: 'gis-ai-go.experience-evaluation-report.v1', catalogueSha256: digest, baselineCommit: doc.baselineCommit,
    authored, sourceBindings, observations, deterministicFixtures: { ...deterministicFixtures, fixtureSha256: sha256(fixtureBytes) }, providerCalls: 0, modelCalls: 0,
    limits: ['Source inventory and authored coverage only; no participant comprehension or reading-age claim.',
      '100% uses the declared current-feature denominator, including separately labelled new local facilities.',
      'Planned file formats, hosted/client access and voice acceptance remain separate gates.',
      'All questions are developer-authored; no independent hold-out result is claimed.'] };
}
async function main(args) {
  const options = {};
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === '--observations' || args[i] === '--output') {
      requireThat(text(args[i + 1]), `Missing argument for ${args[i]}`); options[args[i].slice(2)] = args[++i];
    } else if (args[i] === '--run-local-fixtures') options.localFixtures = true;
    else requireThat(args[i] === '--check', `Unknown option: ${args[i]}`);
  }
  const report = await evaluate({ observationsPath: options.observations, localFixtures: options.localFixtures });
  const body = `${JSON.stringify(report, null, 2)}\n`;
  if (options.output) {
    requireThat(safePath(options.output) && options.output.startsWith('artifacts/experience/'), 'Report output must be under artifacts/experience/');
    const path = resolve(ROOT, options.output); await mkdir(dirname(path), { recursive: true });
    const canonicalParent = await realpath(dirname(path)), rel = relative(await realpath(ROOT), canonicalParent);
    requireThat(!rel.startsWith('..') && !isAbsolute(rel), 'Report output escapes repository');
    try { requireThat(!(await lstat(path)).isSymbolicLink(), 'Report output may not be a symbolic link'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
    await writeFile(path, body, { mode: 0o600 });
  }
  process.stdout.write(body);
  requireThat(!report.deterministicFixtures.executed || report.deterministicFixtures.failed === 0, 'One or more deterministic local fixtures failed');
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).catch((error) => { process.stderr.write(`Experience evaluation failed: ${error.message}\n`); process.exitCode = 1; });
}
