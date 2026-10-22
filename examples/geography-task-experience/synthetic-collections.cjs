'use strict';
const {fixture} = require('./synthetic-fixture.cjs');
// Every source, entry and collection in this fixture is fictional.
const IDS = ['selected-journey-example', 'ngd-batch-example-1', 'ngd-batch-example-2', 'ngd-batch-example-3', 'ngd-batch-example-4'];
function payload(id) {
  if (!IDS.includes(id)) throw Error('Unknown synthetic collection');
  const p = fixture();
  for (const s of p.schemes) {
    s.title = id + ' / ' + s.title;
    s.edition = 'Fictional edition for ' + id;
    s.entries[0].label = 'Distinct fictional label for ' + id;
    s.entries[0].native.collectionFixture = id;
  }
  return p;
}
function catalogue() {
  return {schema: 'gis-ai-go.classification-collections.v1', globalComplete: false,
    collections: IDS.map((id, i) => ({id,
      title: i === 0 ? 'Selected journey — fictional example' : 'NGD batch ' + i + ' — fictional example',
      scopeNote: 'Fictional fixture only. No supplier list or payload is admitted.',
      schemeCount: 2, entryCount: 26, coverage: 'selected-sources-only'}))};
}
module.exports = {IDS, payload, catalogue};
