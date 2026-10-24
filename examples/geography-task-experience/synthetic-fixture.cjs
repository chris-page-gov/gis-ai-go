'use strict';
// Fictional data only. No supplier code, jurisdiction or source is asserted.
function fixture() {
  const source = {id: 'synthetic-source', title: 'Fictional source', url: 'https://example.invalid/source', sha256: 'a'.repeat(64)};
  const entry = (i, override = {}) => ({id: 'entry-' + i, code: String(i).padStart(3, '0'), label: 'Fictional label ' + i, definition: 'Fictional definition ' + i, level: null, parentCode: null, aliases: [], sourceId: source.id, sourceLocator: 'Synthetic row ' + (i + 1), native: {code: String(i).padStart(3, '0'), empty: '', absentMeaning: null, number: 0, boolean: false}, ...override});
  const entries = Array.from({length: 25}, (_, i) => entry(i));
  entries[1] = entry(1, {parentCode: '000', level: 'Source level A', definition: null, aliases: [{text: 'Fictional search shortcut', kind: 'search-variant', authority: 'project-search-variant', sourceId: source.id}]});
  entries[2] = entry(2, {definition: '', parentCode: 'not-retained'});
  return {schema: 'gis-ai-go.classification-browser.v1', reviewedOn: '2026-10-21', globalComplete: false, schemes: [
    {id: 'fictional-a', title: 'Fictional scheme A', edition: 'Synthetic edition 1', referenceDate: '2020-04', publishedDate: '2021-01-02', retrievedAt: '2026-10-21T10:00:00Z', jurisdiction: 'Fictional scope', description: 'A complete selected fictional list for tests only.', sources: [source], coverage: {status: 'complete-selected-list', expectedEntries: 25, retainedEntries: 25, definitionsStatus: 'mixed-or-partial'}, gaps: ['This fixture is not a supplier list or global vocabulary.'], entries},
    {id: 'fictional-b', title: 'Fictional scheme B', edition: null, referenceDate: null, publishedDate: null, retrievedAt: '2026-10-21T10:00:01Z', jurisdiction: 'Different fictional scope', description: 'A partial fictional list with duplicate codes across schemes.', sources: [{...source}], coverage: {status: 'partial', expectedEntries: null, retainedEntries: 1, definitionsStatus: 'labels-only'}, gaps: ['The source denominator is unknown.'], entries: [entry(0, {label: 'Different meaning', definition: null})]}
  ]};
}
module.exports = {fixture};
