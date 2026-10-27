"""Source-reference and publisher projection preserve evidence boundaries."""
from copy import deepcopy
import unittest

from scripts.okf_plus.explorer_resources import project_resources


def fixture():
    rows = [{'id': 'https://example.test/id/a', 'route': 'records/example/a.md'},
            {'id': 'https://example.test/id/b', 'route': 'records/example/b.md'}]
    semantic = {
        rows[0]['id']: {'@id': rows[0]['id'], 'resource': 'https://example.test/source/a.pdf',
            'sourceFamily': 'not-a-publisher',
            'sources': [{'resource': 'https://example.test/source/a.pdf', 'referenceTitle': 'Source A'},
                        {'resource': 'https://example.test/api/a.json'}],
            'rights': {'executionAdmitted': False, 'describedData': 'Not established.'},
            'dcterms:publisher': {'@id': 'https://publisher.test/', 'rdfs:label': 'Source publisher'}},
        rows[1]['id']: {'@id': rows[1]['id'], 'resource': 'https://example.test/source/b',
            'sourceFamily': 'not-a-publisher', 'sources': [],
            'rights': {'executionAdmitted': False}},
    }
    return rows, semantic


class ExplorerResourcesTests(unittest.TestCase):
    def test_source_references_are_deduplicated_per_record_with_exact_pointers(self):
        rows, semantic = fixture()
        before = deepcopy(semantic)
        resources, publishers, records, coverage = project_resources(rows, semantic)
        self.assertEqual(semantic, before)
        self.assertEqual(len(resources), 3)
        source = next(item for item in resources if item['url'].endswith('a.pdf'))
        self.assertEqual(source['dataset'], 'example/a.md')
        self.assertEqual(source['route'], 'resource/' + source['id'])
        self.assertEqual(source['name'], 'Source A')
        self.assertEqual(source['provenance']['source_fields'], ['/resource', '/sources/0/resource'])
        self.assertEqual(source['provenance']['reference_roles'], ['evidence-citation', 'landing-page'])
        self.assertEqual(records[rows[0]['id']]['resource_count'], 2)
        self.assertEqual(coverage['projected_source_field_occurrences'], 4)
        self.assertEqual(coverage['source_reference_associations'], 3)

    def test_pdf_or_json_url_does_not_invent_a_media_type_download_or_fetch(self):
        rows, semantic = fixture()
        resources, _, _, _ = project_resources(rows, semantic)
        for item in resources:
            self.assertEqual(item['resource_type'], 'source-reference')
            self.assertEqual(item['source_access']['display_mode'], 'link')
            self.assertEqual(item['source_access']['media_type'], 'not-established')
            self.assertEqual(item['downloadability'], 'not-established')
            self.assertFalse(item['execution_admitted'])
            for absent in ('format', 'source_format', 'size', 'download_url'):
                self.assertNotIn(absent, item)

    def test_publisher_requires_explicit_identity_and_never_uses_source_family(self):
        rows, semantic = fixture()
        _, publishers, records, coverage = project_resources(rows, semantic)
        self.assertEqual(len(publishers), 1)
        self.assertEqual(publishers[0]['name'], 'https://publisher.test/')
        self.assertEqual(publishers[0]['title'], 'Source publisher')
        self.assertEqual(publishers[0]['route'], 'publisher/https%3A%2F%2Fpublisher.test%2F')
        self.assertEqual(records[rows[0]['id']]['publisher'], 'https://publisher.test/')
        self.assertEqual(records[rows[1]['id']]['publisher'], '')
        self.assertEqual(records[rows[1]['id']]['source_publishers'], [])
        self.assertEqual(coverage['records_with_projected_publishers'], 1)

    def test_co_publishers_remain_multiple_without_inventing_a_primary(self):
        rows, semantic = fixture()
        semantic[rows[0]['id']]['dcterms:publisher'] = [
            {'@id': 'https://publisher.test/'}, {'@id': 'https://other.test/'}]
        _, publishers, records, coverage = project_resources(rows, semantic)
        self.assertEqual(len(publishers), 2)
        self.assertEqual(records[rows[0]['id']]['publisher'], '')
        self.assertEqual({item['name'] for item in records[rows[0]['id']]['source_publishers']},
                         {'https://publisher.test/', 'https://other.test/'})
        self.assertEqual(coverage['records_with_multiple_publishers'], 1)

    def test_conflicting_publisher_labels_do_not_acquire_an_arbitrary_preferred_label(self):
        rows, semantic = fixture()
        semantic[rows[1]['id']]['dcterms:publisher'] = {
            '@id': 'https://publisher.test/', 'rdfs:label': 'Different source label'}
        _, publishers, _, _ = project_resources(rows, semantic)
        self.assertEqual(publishers[0]['title'], 'https://publisher.test/')
        self.assertEqual(publishers[0]['source_labels'], ['Different source label', 'Source publisher'])
        self.assertEqual(publishers[0]['provenance']['label_status'], 'conflicting-source-labels')

    def test_identical_url_on_distinct_records_keeps_distinct_association_ids(self):
        rows, semantic = fixture()
        semantic[rows[1]['id']]['resource'] = semantic[rows[0]['id']]['resource']
        resources, _, _, coverage = project_resources(rows, semantic)
        same_url = [item for item in resources if item['url'].endswith('a.pdf')]
        self.assertEqual(len(same_url), 2)
        self.assertEqual(len({item['id'] for item in same_url}), 2)
        self.assertEqual(coverage['distinct_source_urls'], 2)
        self.assertEqual(project_resources(rows, semantic), project_resources(list(reversed(rows)), semantic))

    def test_a_later_record_cannot_hide_a_conflict_within_an_earlier_record(self):
        rows, semantic = fixture()
        semantic[rows[0]['id']]['dcterms:publisher'] = [
            {'@id': 'https://publisher.test/', 'rdfs:label': 'A'},
            {'@id': 'https://publisher.test/', 'rdfs:label': 'B'}]
        semantic[rows[1]['id']]['dcterms:publisher'] = {'@id': 'https://publisher.test/', 'rdfs:label': 'A'}
        _, publishers, _, _ = project_resources(rows, semantic)
        self.assertEqual(publishers[0]['title'], 'https://publisher.test/')
        self.assertEqual(publishers[0]['source_labels'], ['A', 'B'])
        self.assertEqual(publishers[0]['provenance']['label_status'], 'conflicting-source-labels')

    def test_absent_and_literal_publishers_are_counted_without_minted_identities(self):
        rows, semantic = fixture()
        semantic[rows[0]['id']]['dcterms:publisher'] = 'Publisher literal without an IRI'
        _, publishers, records, coverage = project_resources(rows, semantic)
        self.assertEqual(publishers, [])
        self.assertEqual(records[rows[0]['id']]['publisher'], '')
        self.assertEqual(coverage['records_with_unresolved_publisher_property'], 1)

    def test_unsafe_source_reference_fails_closed(self):
        for url in ['https://user:secret@example.test/path', 'https://example.test/?api_key=secret',
                    'https://example.test/?%2574oken=secret', 'javascript:alert(1)', '/relative',
                    'https://example.test/"quoted"', 'https://example.test/<template>',
                    'https://example.test/%zz', 'https://example.test%40evil.test/']:
            rows, semantic = fixture()
            semantic[rows[0]['id']]['sources'].append({'resource': url})
            with self.subTest(url=url), self.assertRaises(ValueError):
                project_resources(rows, semantic)

    def test_metadata_identity_mismatch_and_duplicate_records_fail(self):
        rows, semantic = fixture()
        semantic[rows[0]['id']]['@id'] = rows[1]['id']
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            project_resources(rows, semantic)
        rows, semantic = fixture()
        with self.assertRaisesRegex(ValueError, 'unique record IDs'):
            project_resources(rows + [rows[0]], semantic)

    def test_unescaped_native_or_template_url_is_preserved_but_not_minted_as_a_direct_link(self):
        rows, semantic = fixture()
        semantic[rows[0]['id']]['resource'] = 'https://example.test/items/{source-id}'
        before = deepcopy(semantic)
        resources, _, _, coverage = project_resources(rows, semantic)
        self.assertEqual(semantic, before)
        self.assertNotIn(semantic[rows[0]['id']]['resource'], [item['url'] for item in resources])
        self.assertEqual(coverage['unprojected_source_field_occurrences'], 1)
        self.assertEqual(coverage['unprojected_source_fields'][0]['source_field'], '/resource')
        self.assertEqual(coverage['unprojected_source_fields'][0]['reason'], 'unescaped-or-template-source-url')


if __name__ == '__main__':
    unittest.main()
