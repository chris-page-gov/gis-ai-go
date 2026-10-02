import assert from 'node:assert/strict';
import { readFile, mkdtemp, writeFile, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { CATALOGUE_PATH, evaluate, evaluateObservations, sha256, validateCatalogue, verifySourceBindings, validateLocalFixtures, runLocalFixtures } from '../scripts/experience_evaluate.mjs';

const catalogueBytes = await readFile(new URL(`../${CATALOGUE_PATH}`, import.meta.url));
const catalogue = JSON.parse(catalogueBytes);
const digest = sha256(catalogueBytes);
const clone = () => structuredClone(catalogue);

test('coverage separates baseline, new local facilities, planned scope and unobserved execution', async () => {
  const report = await evaluate();
  assert.equal(report.authored.baselineFeatures, 45);
  assert.equal(report.authored.newLocalFeatures, 29);
  assert.equal(report.authored.plannedFeatures, 8);
  assert.equal(report.authored.currentFeatures, 74);
  assert.equal(report.authored.questions, 222);
  assert.equal(report.authored.personas, 9);
  assert.equal(report.authored.authoredCurrentFeatureCoveragePercent, 100);
  assert.equal(report.observations.naturalLanguageRuns, 0);
  assert.equal(report.observations.unobservedNaturalLanguageQuestionCount, 222);
  assert.equal(report.providerCalls, 0); assert.equal(report.modelCalls, 0);
  assert.equal(report.sourceBindings.networkRequests, 0);
  assert.equal(report.catalogueSha256, digest);
});

test('every positive case has all role variants while non-positive cases remain real test contracts', () => {
  validateCatalogue(catalogue);
  for (const q of catalogue.questions) {
    assert(q.assertions.length >= 2);
    assert(q.jitSummary.length > 15);
    if (q.caseType === 'positive') assert.deepEqual(q.variants.map((v) => v.personaId).sort(), catalogue.personas.map((p) => p.id).sort());
  }
  const expert = catalogue.questions.find((q) => q.featureIds.includes('pilot-names') && q.caseType === 'positive').variants.find((v) => v.personaId === 'geospatial-specialist');
  assert(expert.text.includes('toponym') && expert.text.includes('polygon centroid'));
  assert(catalogue.eventContext.accessPlan.includes('facilitator-led'));
});

test('removing a refusal, persona, JIT explanation or source binding fails closed', () => {
  for (const [mutate, expected] of [
    [(d) => { d.questions = d.questions.filter((q) => q.id !== 'EX-Q001-negative'); }, /missing negative case/u],
    [(d) => { d.questions[0].variants.pop(); }, /lacks a persona variant/u],
    [(d) => { d.questions[0].jitSummary = ''; }, /JIT summary/u],
    [(d) => { d.questions[0].sourceIds = ['not-real']; }, /sourceIds/u],
    [(d) => { d.features[0].conceptIds = ['not-real']; }, /conceptIds/u],
    [(d) => { d.sources[0].repositoryPaths = ['../secret']; }, /unsafe repository path/u],
  ]) { const d = clone(); mutate(d); assert.throws(() => validateCatalogue(d), expected); }
});

test('authored data cannot claim passes, grant provider authority or smuggle an unbound typed call', () => {
  const passed = clone(); passed.questions[0].executionStatus = 'passed';
  assert.throws(() => validateCatalogue(passed), /cannot claim execution/u);
  const authority = clone(); authority.questions[0].providerCallsAuthorisedByThisCase = true;
  assert.throws(() => validateCatalogue(authority), /cannot claim execution or authority/u);
  const recipe = clone(); const q = recipe.questions.find((q) => q.typedCall); q.typedCall.name = 'execute_arbitrary_code';
  assert.throws(() => validateCatalogue(recipe), /invalid typed recipe/u);
});

test('source-bound denominator catches removed or invented tool operations', async () => {
  const missing = clone(); missing.features = missing.features.filter((f) => f.id !== 'pilot-areas');
  await assert.rejects(verifySourceBindings(missing), /source operation inventory differs/u);
  const invented = clone(); invented.features.find((f) => f.id === 'pilot-areas').operation = 'sites_any_sql';
  await assert.rejects(verifySourceBindings(invented), /source operation inventory differs/u);
  const facet = clone(); facet.features = facet.features.filter((f) => f.id !== 'public-filter-topic');
  await assert.rejects(verifySourceBindings(facet), /facet inventory drift/u);
});

test('typed recipe cannot widen existing provider bounds', async () => {
  const d = clone(); d.questions.find((q) => q.typedCall?.name === 'sites_os_names').typedCall.arguments.max_results = 10000;
  await assert.rejects(verifySourceBindings(d), /no existing bounded corpus anchor/u);
});

async function observationFixture(action) {
  const root = await mkdtemp(join(tmpdir(), 'gis-experience-evidence-'));
  try {
    const evidence = JSON.stringify({ synthetic: true, outcome: 'Fixture for aggregator integrity tests, not a real participant result.' });
    await writeFile(join(root, 'result.json'), evidence);
    const q = catalogue.questions[0];
    const observation = { questionId: q.id, variantId: q.variants[0].id, plane: 'typed-client', reviewerRole: 'test-fixture', client: 'synthetic test client', observedAt: '2026-10-02T12:00:00Z', evidencePath: 'result.json', evidenceSha256: sha256(evidence), assertionResults: q.assertions.map((a) => ({ id: a.id, passed: true, evidencePointer: 'result.json: synthetic' })) };
    const input = { schema: 'gis-ai-go.experience-observations.v1', catalogueSha256: digest, runtimeRevision: catalogue.baselineCommit, observations: [observation] };
    await action({ root, input, observation });
  } finally { await rm(root, { recursive: true, force: true }); }
}

test('recorded typed checks do not become natural-language or participant acceptance', async () => {
  await observationFixture(async ({ root, input }) => {
    const result = await evaluateObservations(catalogue, input, digest, root);
    assert.equal(result.recordedRuns, 1); assert.equal(result.typedClientRuns, 1);
    assert.equal(result.naturalLanguageRuns, 0); assert.equal(result.unobservedNaturalLanguageQuestionCount, 222);
    assert.equal(result.runs[0].recordedOutcome, 'reviewer-reported-pass');
    assert.match(result.verdictAuthority, /does not assess meaning/u);
  });
});

test('observation must bind exact catalogue, runtime and all assertions', async () => {
  await observationFixture(async ({ root, input }) => {
    const wrongDigest = structuredClone(input); wrongDigest.catalogueSha256 = '0'.repeat(64);
    await assert.rejects(evaluateObservations(catalogue, wrongDigest, digest, root), /catalogue digest mismatch/u);
    const wrongVariant = structuredClone(input); wrongVariant.observations[0].variantId = 'unknown';
    await assert.rejects(evaluateObservations(catalogue, wrongVariant, digest, root), /Unknown question or variant/u);
    const incomplete = structuredClone(input); incomplete.observations[0].assertionResults.pop();
    await assert.rejects(evaluateObservations(catalogue, incomplete, digest, root), /every expected assertion/u);
    const duplicate = structuredClone(input); duplicate.observations.push(duplicate.observations[0]);
    await assert.rejects(evaluateObservations(catalogue, duplicate, digest, root), /Duplicate observation/u);
    const failed = structuredClone(input); failed.observations[0].assertionResults[0].passed = false;
    assert.equal((await evaluateObservations(catalogue, failed, digest, root)).runs[0].recordedOutcome, 'reviewer-reported-fail');
  });
});

test('tampered, missing, traversal and linked evidence fail integrity validation', async () => {
  await observationFixture(async ({ root, input }) => {
    await writeFile(join(root, 'result.json'), 'changed');
    await assert.rejects(evaluateObservations(catalogue, input, digest, root), /evidence digest mismatch/u);
    const traversal = structuredClone(input); traversal.observations[0].evidencePath = '../result.json';
    await assert.rejects(evaluateObservations(catalogue, traversal, digest, root), /Unsafe evidence path/u);
    const missing = structuredClone(input); missing.observations[0].evidencePath = 'missing.json';
    await assert.rejects(evaluateObservations(catalogue, missing, digest, root), /ENOENT/u);
    await symlink(join(root, 'result.json'), join(root, 'linked.json'));
    const linked = structuredClone(input); linked.observations[0].evidencePath = 'linked.json';
    await assert.rejects(evaluateObservations(catalogue, linked, digest, root), /bounded regular file/u);
  });
});

test('granular intake cases reference current child facilities and concrete bounded checks', async () => {
  const fixture = JSON.parse(await readFile(new URL('../evaluation/experience/local-fixtures.v1.json', import.meta.url)));
  const coverage = validateLocalFixtures(catalogue, fixture);
  assert.equal(coverage.cases, 30);
  assert(coverage.featureIds.includes('intake-zip') && coverage.featureIds.includes('intake-presentation'));
  assert.equal(coverage.naturalLanguageEvaluations, 0);
  const unknown = structuredClone(fixture); unknown.cases[0].featureIds.push('invented');
  assert.throws(() => validateLocalFixtures(catalogue, unknown), /featureIds/u);
  const unsafe = structuredClone(fixture); unsafe.cases[0].input.fixture = '../private-file';
  assert.throws(() => validateLocalFixtures(catalogue, unsafe), /retained synthetic example/u);
});

test('setup blocks remain unassessed rather than becoming wrong answers or passes', async () => {
  await observationFixture(async ({ root, input }) => {
    const blocked = input.observations[0]; blocked.status = 'blocked'; blocked.blockReasonCode = 'client-unavailable'; blocked.assertionResults = [];
    blocked.rubric = { taskCompletion: 'not-assessed', comprehension: 'not-assessed', sourceCorrectness: 'not-assessed', latencyMs: 1200 };
    const report = await evaluateObservations(catalogue, input, digest, root);
    assert.equal(report.blockedRuns, 1); assert.equal(report.reportedPasses, 0); assert.equal(report.typedClientRuns, 0);
    assert.equal(report.unobservedQuestionCount, catalogue.questions.length);
    assert.equal(report.runs[0].recordedOutcome, 'blocked');
    blocked.assertionResults = [{ id: 'task-outcome', passed: true, evidencePointer: 'unjustified' }];
    await assert.rejects(evaluateObservations(catalogue, input, digest, root), /cannot claim assertion results/u);
  });
});
