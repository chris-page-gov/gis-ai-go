"""Independent Reader routing, complete context, integrity and learning checks."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.okf_plus.context_projection import project as context_project, sha, canonical
from scripts.okf_plus.explorer_projection import install, project, token_bucket
from tests.contract.test_okf_plus_context import fixture, BASE, CAPTURED


def inputs(count=41):
    search, bundle = fixture(count)
    context, _ = context_project(search, bundle, base_url=BASE, captured_at=CAPTURED)
    return search, bundle, context


class ExplorerProjectionTests(unittest.TestCase):
    def test_record_source_reference_locators_select_only_the_requested_record(self):
        search, bundle, context = inputs(41)
        outputs, _ = project(search, bundle, context, captured_at=CAPTURED)
        descriptor = json.loads(outputs['okf-explorer.json'])
        manifest = json.loads(outputs['data-manifest.json'])
        index_ref = descriptor['entrypoints']['record_resources']
        self.assertEqual(index_ref, manifest['indexes']['record_resources'])
        index = json.loads(outputs[index_ref['path']])
        self.assertEqual(index['schema'], 'okf-record-resource-index.v1')
        self.assertEqual(index['snapshot'], descriptor['snapshot'])
        self.assertEqual(index['algorithm'], 'fnv1a32-prefix-2')
        projected_ids = set()
        chunk_routes = {}
        for row in search['records']:
            bucket_ref = index['buckets'][token_bucket(row['route'])]
            self.assertEqual(bucket_ref['sha256'], sha(outputs[bucket_ref['path']]))
            entry = json.loads(outputs[bucket_ref['path']])[row['route']]
            self.assertEqual(entry['dataset'], row['route'].removeprefix('records/'))
            selected = []
            for ref in entry['chunks']:
                self.assertEqual(ref['bytes'], len(outputs[ref['path']]))
                self.assertEqual(ref['sha256'], sha(outputs[ref['path']]))
                chunk = json.loads(outputs[ref['path']])
                self.assertEqual(len(ref['rows']), len(set(ref['rows'])))
                selected.extend(chunk[index] for index in ref['rows'])
                chunk_routes.setdefault(ref['path'], set()).add(row['route'])
            self.assertEqual(len(selected), entry['count'])
            self.assertEqual({item['dataset'] for item in selected}, {entry['dataset']})
            self.assertTrue(projected_ids.isdisjoint(item['id'] for item in selected))
            projected_ids.update(item['id'] for item in selected)
        self.assertEqual(len(projected_ids), descriptor['counts']['resources'])
        # Adjacent records share one bounded transport, but have distinct selectors.
        self.assertEqual(sorted(map(len, chunk_routes.values())), [9, 32])

    def test_source_facets_links_and_citations_are_available_without_full_record_loading(self):
        search, bundle, _ = inputs(3)
        first, second, third = bundle['records']
        first['skos:related'] = [{'@id': second['@id']}, {'@id': third['@id']}]
        first['dcterms:publisher'] = {'@id': 'https://example.test/publisher', 'rdfs:label': 'Fixture publisher'}
        context, _ = context_project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        outputs, report = project(search, bundle, context, captured_at=CAPTURED)
        descriptor = json.loads(outputs['okf-explorer.json'])
        manifest = json.loads(outputs['data-manifest.json'])
        coverage = json.loads(outputs['discovery-coverage.json'])
        self.assertEqual(descriptor['counts']['relationships'], 2)
        self.assertEqual(descriptor['counts']['publishers'], 1)
        self.assertEqual(descriptor['counts']['resources'], 6)
        self.assertEqual(descriptor['vocabulary']['resource_plural'], 'source references')
        facets = json.loads(outputs['search/facets.json'])
        self.assertEqual(facets['source_publisher'], {'https://example.test/publisher': [0]})
        self.assertEqual(facets['review_status'], {'synthetic': [0, 1, 2]})
        self.assertEqual(facets['update_frequency'], {'Monthly': [0, 1, 2]})
        self.assertEqual(coverage['facets']['source_publisher']['nonemptyRecords'], 1)
        self.assertEqual(coverage['relationships']['retained_record_reference_occurrences'], 2)
        self.assertEqual(coverage['relationships']['projected_assertions'], 2)
        docs = json.loads(outputs['search/results/00000.json'])
        self.assertEqual(docs[0]['publisher'], 'https://example.test/publisher')
        self.assertEqual(docs[1]['publisher'], '')
        self.assertEqual(docs[0]['source_publishers'], [{'name': 'https://example.test/publisher', 'title': 'Fixture publisher'}])
        self.assertEqual(docs[0]['review_status'], ['synthetic'])
        # Compact discovery rows do not duplicate complete retained semantics.
        self.assertNotIn('okf_plus', docs[0])
        relationships = [edge for ref in manifest['chunks']['relationships'] for edge in json.loads(outputs[ref['path']])]
        self.assertEqual({edge['target'] for edge in relationships}, {search['records'][1]['route'], search['records'][2]['route']})
        adjacency = json.loads(outputs['relationship-adjacency.json'])
        bucket = adjacency['buckets'][token_bucket(search['records'][0]['route'])]
        incident = json.loads(outputs[bucket['path']])[search['records'][0]['route']]
        self.assertEqual({edge['id'] for edge in incident}, {edge['id'] for edge in relationships})
        for name in ('resources', 'publishers', 'relationships'):
            for ref in manifest['chunks'][name]:
                self.assertEqual(ref['bytes'], len(outputs[ref['path']]))
                self.assertEqual(ref['sha256'], sha(outputs[ref['path']]))
        self.assertNotIn('endpoint_labels', descriptor['entrypoints'])
        self.assertNotIn('endpoint_labels', manifest['indexes'])
        analysis = json.loads(outputs['analysis-overview.json'])
        self.assertEqual({entry['route'] for entry in analysis['graph_overview']['nodes']}, {row['route'] for row in search['records']})
        self.assertEqual({entry['label'] for entry in analysis['graph_overview']['nodes']}, {row['title'] for row in search['records']})
        self.assertEqual(analysis['summary']['relationship_count'], 2)
        self.assertEqual(len(analysis['graph_overview']['edges']), 2)
        self.assertEqual(report['discovery']['relationships'], 2)
        record = json.loads(outputs['records/00000.json'])[0]
        self.assertEqual(record['okf_plus']['metadata'], first)

    def test_tail_route_loads_one_whole_chunk_and_metadata_is_not_rewritten(self):
        search, bundle, context = inputs()
        outputs, report = project(search, bundle, context, captured_at=CAPTURED)
        locator = json.loads(outputs['record-locator.json'])
        tail = search['records'][-1]
        bucket = json.loads(outputs[locator['buckets'][token_bucket(tail['route'])]['path']])
        chunk_index, row_index = bucket[tail['route']]
        chunk = json.loads(outputs[locator['record_chunks'][chunk_index]['path']])
        record = chunk[row_index]
        self.assertEqual(record['route'], tail['route'])
        self.assertEqual(record['id'], tail['id'])
        self.assertEqual(record['narrative']['body'], tail['text'])
        self.assertEqual(record['okf_plus']['metadata'], bundle['records'][-1])
        self.assertIsNone(record['okf_plus']['metadata']['details']['nullField'])
        self.assertEqual(record['provenance']['sources'], tail['sources'])
        self.assertEqual(report['readerRecords'], 41)
        self.assertEqual(report['omittedRecordIds'], [])
        self.assertLessEqual(len(chunk), locator['chunk_size'])
        self.assertGreater(chunk_index, 0)

    def test_complete_search_tail_is_indexed_without_reader_record_loading(self):
        search, bundle, context = inputs()
        outputs, _ = project(search, bundle, context, captured_at=CAPTURED)
        manifest = json.loads(outputs['search/manifest.json'])
        lexicon = json.loads(outputs[manifest['entrypoints']['lexicon']['ta']])
        entry = next(row for row in lexicon if row['token'] == 'tail999')
        posting = json.loads(outputs[entry['postings']])['tokens']['tail999']
        self.assertEqual([row[0] for row in posting], [40])
        result = json.loads(outputs[manifest['entrypoints']['result_docs'][0]])[40]
        self.assertEqual(result['record_id'], search['records'][-1]['id'])
        # Explorer's route helper gives `open` precedence over `route`.
        self.assertEqual(result['open'], result['route'])
        self.assertNotIn('okf_plus', result)
        self.assertNotIn('narrative', result)
        self.assertEqual(manifest['counts']['documents'], 41)
        for row in json.loads(outputs['overview.json'])['recent_datasets']:
            self.assertEqual(row['open'], row['route'])
        shards = json.loads(outputs[manifest['shard_metadata']])['shards']
        self.assertEqual(manifest['shard_manifest_sha256'], sha(canonical(shards) + b'\n'))
        for row in shards['search']:
            self.assertEqual(row['sha256'], sha(outputs[row['path']]))

    def test_context_snapshot_and_all_entrypoints_remain_exactly_bound(self):
        search, bundle, context = inputs(3)
        outputs, report = project(search, bundle, context, captured_at=CAPTURED)
        descriptor = json.loads(outputs['okf-explorer.json'])
        context_manifest = json.loads(outputs['context/manifest.json'])
        self.assertEqual(descriptor['snapshot'], context_manifest['semantic_source_snapshot'])
        self.assertEqual(report['snapshot'], descriptor['snapshot'])
        references = list(descriptor['entrypoint_integrity'].values())
        references += [value for value in descriptor['entrypoints'].values() if isinstance(value, dict)]
        for reference in references:
            self.assertEqual(reference['bytes'], len(outputs[reference['path']]))
            self.assertEqual(reference['sha256'], sha(outputs[reference['path']]))
        for reference in report['outputs']:
            self.assertEqual(reference['bytes'], len(outputs[reference['path']]))
            self.assertEqual(reference['sha256'], sha(outputs[reference['path']]))
        self.assertEqual(outputs, project(search, bundle, context, captured_at=CAPTURED)[0])

    def test_foreign_snapshot_or_tampered_context_fails_closed(self):
        search, bundle, context = inputs(3)
        bad = deepcopy(bundle); bad['records'][0]['description'] = 'Different input'
        with self.assertRaisesRegex(ValueError, 'field mismatch'):
            project(search, bad, context, captured_at=CAPTURED)
        bad = dict(context); bad['base-index.json'] += b' '
        with self.assertRaisesRegex(ValueError, 'byte binding mismatch'):
            project(search, bundle, bad, captured_at=CAPTURED)
        other = deepcopy(search); other['revision'] = 'd' * 40
        bad_bundle = deepcopy(bundle); bad_bundle['revision'] = 'd' * 40
        with self.assertRaisesRegex(ValueError, 'input snapshot'):
            project(other, bad_bundle, context, captured_at=CAPTURED)

    def test_distinct_semantic_ids_cannot_overwrite_one_reader_route(self):
        search, bundle, _ = inputs(2)
        search['records'][1]['route'] = search['records'][0]['route']
        # A valid upstream context binding does not prove unique Reader routes.
        context, _ = context_project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        with self.assertRaisesRegex(ValueError, 'unique Reader route'):
            project(search, bundle, context, captured_at=CAPTURED)

    def test_authored_learning_order_and_semantic_references_are_preserved(self):
        search, bundle, _ = inputs(3)
        for number, (row, parent) in enumerate(zip(search['records'], bundle['records'])):
            row['id'] = parent['@id'] = f'https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/synthetic/{number}'
        path = {'schema': 'gis-ai-go.okf-plus-learning-path.v1', 'id': 'check-a-field',
                'title': 'Check a field', 'description': 'Clearly synthetic exercise.',
                'objectives': ['Explain the evidence boundary.'], 'prerequisites': [],
                'prerequisiteConcepts': [{'recordId': search['records'][0]['id'], 'purpose': 'Read first.'}],
                'steps': [{'recordId': search['records'][2]['id'], 'title': 'Inspect the later record',
                           'outcome': 'State the gap.', 'practice': 'Find the unknown.', 'minutes': 5,
                           'conceptRefs': [search['records'][0]['id']], 'sourceRefs': ['https://example.test/catalogue']},
                          {'recordId': search['records'][1]['id'], 'title': 'Compare the earlier record',
                           'outcome': 'Explain the date.', 'conceptRefs': [search['records'][0]['id']],
                           'practice': 'Compare the date.', 'minutes': 4, 'sourceRefs': ['https://example.test/catalogue']}],
                'relationshipScope': 'learning-navigation-only'}
        for row in (search['records'][0], bundle['records'][0]):
            row['details']['learningPath'] = deepcopy(path)
        context, _ = context_project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        outputs, _ = project(search, bundle, context, captured_at=CAPTURED)
        descriptor = json.loads(outputs['okf-explorer.json'])
        learning = descriptor['learning_presentation']
        self.assertEqual(learning['schema'], 'okf-large-learning-presentation.v1')
        self.assertEqual([step['route'] for step in learning['paths'][0]['steps']],
                         [search['records'][2]['route'], search['records'][1]['route']])
        self.assertEqual(learning['paths'][0]['steps'][0]['evidence_routes'], [search['records'][0]['route']])
        self.assertNotIn('programme', learning)
        self.assertNotIn('assessment', learning['paths'][0])
        for row in (search['records'][0], bundle['records'][0]):
            row['details']['learningPath']['steps'][0]['recordId'] = 'https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/synthetic/absent'
        context, _ = context_project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        with self.assertRaisesRegex(ValueError, 'absent record'):
            project(search, bundle, context, captured_at=CAPTURED)

    def test_install_never_replaces_an_existing_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'new-candidate'
            install({'hello.json': b'{}'}, output)
            with self.assertRaisesRegex(ValueError, 'existing output'):
                install({'hello.json': b'changed'}, output)
            self.assertEqual((output / 'hello.json').read_bytes(), b'{}')


if __name__ == '__main__':
    unittest.main()
