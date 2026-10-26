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
