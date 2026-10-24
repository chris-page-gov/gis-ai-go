'use strict';
// Fictional data only. Counts and hash-shaped strings are not supplier evidence.
function fixture() {
  const rows = Array.from({length: 9}, (_, i) => ({id: 'fictional-' + i, label: 'Fictional product ' + i,
    scope: i < 7 ? 'included' : i === 7 ? 'excluded' : 'unclassified', sourceUrl: 'https://example.org/fictional/' + i,
    next: 'Review a fictional bounded input.', remaining: 'No actual product or current edition has been assessed.',
    gates: [{id: 'source', status: 'Synthetic source statement only', limit: 'No actual source acceptance.'}, {id: 'meaning', status: 'Unresolved', limit: 'No equivalence established.'}],
    evidence: i ? [] : [{scope: 'Fictional review association', limit: 'Hash-shaped fixture only, not a receipt.', receiptHashes: ['1'.repeat(64)]}]}));
  return {schema: 'gis-ai-go.coverage-navigator.v1', asOf: '2026-01-15', basis: {title: 'Fictional learning basis', scopeNote: 'Synthetic rows and relationships for local tests only.'},
    counts: {rows: 9, included: 7, excluded: 1, unclassified: 1, edges: 2}, fullCoverage: false, percentage: null,
    gates: [{id: 'source', label: 'Source evidence'}, {id: 'meaning', label: 'Meaning'}], rows,
    nodes: [{id: 'fictional-authority', label: 'Fictional authority'}, {id: 'fictional-area', label: 'Fictional area'}, {id: 'fictional-building', label: 'Fictional building'}],
    edges: [{id: 'fictional-assignment', from: 'fictional-authority', to: 'fictional-area', relation: 'A supplied fictional assignment.', limits: 'No geometric containment or current jurisdiction is established.', transitiveIdentityInferred: false},
      {id: 'fictional-reference', from: 'fictional-area', to: 'fictional-building', relation: 'A separate fictional reference.', limits: 'No transitive identity or population membership is established.', transitiveIdentityInferred: false}]};
}
module.exports = {fixture, clone: x => JSON.parse(JSON.stringify(x))};
if (require.main === module) process.stdout.write(JSON.stringify(fixture()));
