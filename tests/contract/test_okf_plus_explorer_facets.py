"""Coverage of explicit source metadata exposed as Explorer facets."""
from copy import deepcopy
import unittest

from scripts.okf_plus.explorer_facets import (
    FACET_DEFINITIONS, facet_values, presentation_facets, publisher_rows,
    publisher_label_candidates,
)


class ExplorerFacetTests(unittest.TestCase):
    def test_all_named_source_fields_are_exposed_without_rewriting_metadata(self):
        metadata = {
            'type': 'Dataset', 'sourceFamily': 'synthetic-source',
            'tags': ['Height', 'height', 'Height', '', ' '],
            'dcterms:publisher': {'@id': 'https://publisher.example.test/',
                                  'rdfs:label': {'@value': 'Synthetic publisher', '@language': 'en-GB'}},
            'reviewStatus': 'source-reviewed', 'assertionStatus': 'normalised', 'status': 'draft',
            'temporal': {'status': 'source-stated', 'kind': 'dataset-reference-period'},
            'update': {'frequency': {'status': 'source-stated', 'label': 'Quarterly'}, 'releaseVersion': 4},
            'rights': {'retrievalAuthority': 'metadata-only', 'executionAdmitted': False},
            'sources': [{'evidenceKind': 'official-reference'}, {'evidenceKind': 'captured-public-metadata'}],
            'details': {'unit_of_measure': 'metres', 'spatialReference': '27700',
                        'crs': ['http://www.opengis.net/def/crs/EPSG/0/27700'],
                        'storageCrs': 'http://www.opengis.net/def/crs/EPSG/0/27700'},
        }
        original = deepcopy(metadata)
        values = facet_values(metadata)
        self.assertEqual(values, {
            'record_type': ['Dataset'], 'source_family': ['synthetic-source'],
            'tag': ['Height', 'height'], 'source_publisher': ['https://publisher.example.test/'],
            'review_status': ['source-reviewed'], 'assertion_status': ['normalised'],
            'lifecycle_status': ['draft'], 'temporal_status': ['source-stated'],
            'temporal_kind': ['dataset-reference-period'], 'update_frequency': ['Quarterly'],
            'update_frequency_status': ['source-stated'], 'release_version': ['4'],
            'retrieval_authority': ['metadata-only'],
            'source_evidence_kind': ['captured-public-metadata', 'official-reference'],
            'unit': ['metres'], 'spatial_reference': ['27700'],
            'crs': ['http://www.opengis.net/def/crs/EPSG/0/27700'],
            'storage_crs': ['http://www.opengis.net/def/crs/EPSG/0/27700'],
        })
        self.assertEqual(metadata, original)

    def test_missing_and_blank_values_stay_absent_but_explicit_unknown_status_is_retained(self):
        metadata = {'sourceFamily': 'not-a-publisher', 'tags': [None, '', ' '],
                    'reviewStatus': 'not-human-reviewed',
                    'temporal': {'status': 'not-evidenced', 'start': None},
                    'update': {'frequency': {'status': 'not-applicable', 'label': None}, 'releaseVersion': ''},
                    'rights': {'executionAdmitted': False},
                    'details': {'unit_of_measure': {'unrecognised': 'metres'}, 'crs': None}}
        values = facet_values(metadata)
        self.assertEqual(values['source_publisher'], [])
        self.assertEqual(values['tag'], [])
        self.assertEqual(values['unit'], [])
        self.assertEqual(values['crs'], [])
        self.assertEqual(values['temporal_status'], ['not-evidenced'])
        self.assertEqual(values['update_frequency_status'], ['not-applicable'])
        self.assertEqual(values['release_version'], [])
        self.assertEqual(values['retrieval_authority'], [])

    def test_explicit_multivalued_publisher_identities_are_not_merged_by_label(self):
        first = {'@id': 'http://publisher.example.test/one', 'rdfs:label': 'Same source label'}
        second = {'@id': 'https://publisher.example.test/two', 'rdfs:label': 'Same source label'}
        metadata = {'dcterms:publisher': [second, first, first, 'Literal name without an IRI']}
        expected = [
            {'id': first['@id'], 'label': 'Same source label'},
            {'id': second['@id'], 'label': 'Same source label'},
        ]
        self.assertEqual(publisher_rows(metadata), expected)
        self.assertEqual(facet_values(metadata)['source_publisher'], [row['id'] for row in expected])
        self.assertEqual(publisher_rows({'dcterms:publisher': {'@id': first['@id']}}),
                         [{'id': first['@id'], 'label': first['@id']}])

    def test_conflicting_labels_for_one_publisher_identity_do_not_depend_on_source_order(self):
        identifier = 'https://publisher.example.test/one'
        first = {'@id': identifier, 'rdfs:label': 'First retained label'}
        second = {'@id': identifier, 'rdfs:label': 'Second retained label'}
        expected = [{'id': identifier, 'label': identifier}]
        for items in ([first, second], [second, first]):
            metadata = {'dcterms:publisher': deepcopy(items)}
            original = deepcopy(metadata)
            self.assertEqual(publisher_rows(metadata), expected)
            self.assertEqual(facet_values(metadata)['source_publisher'], [identifier])
            self.assertEqual(metadata, original)
        self.assertEqual(publisher_rows({'dcterms:publisher': [{'@id': identifier}, first, first]}),
                         [{'id': identifier, 'label': first['rdfs:label']}])

    def test_publisher_entities_refuse_unsafe_or_credential_bearing_identifiers(self):
        for identifier in (
            '/relative/publisher', 'urn:publisher:one', 'https://user:secret@publisher.example.test/',
            'https://publisher.example.test/?api_key=secret',
            'https://publisher.example.test/?%2561pi%255Fkey=secret',
            'https://publisher.example.test/?access%5Ftoken=secret',
            'https://publisher.example.test:65536/', 'https://publisher.example.test:0/',
            'https://publisher.example.test/%zz', 'https://publisher.example.test/a b',
            'https://publisher.example.test/"unsafe', "https://publisher.example.test/'unsafe",
            'https://publisher.example.test/unsafe|delimiter',
        ):
            with self.subTest(identifier=identifier):
                with self.assertRaisesRegex(ValueError, 'Publisher|publisher'):
                    publisher_rows({'dcterms:publisher': {'@id': identifier}})

    def test_multivalued_publisher_labels_keep_conflicts_and_property_priority(self):
        identifier = 'https://publisher.example.test/one'
        for labels in (['B', 'A'], ['A', 'B']):
            metadata = {'dcterms:publisher': {'@id': identifier, 'rdfs:label': labels}}
            self.assertEqual(publisher_label_candidates(metadata), [{'id': identifier, 'labels': ['A', 'B']}])
            self.assertEqual(publisher_rows(metadata), [{'id': identifier, 'label': identifier}])
        self.assertEqual(publisher_rows({'dcterms:publisher': {
            '@id': identifier, 'skos:prefLabel': 'Preferred', 'rdfs:label': 'Alternate',
        }}), [{'id': identifier, 'label': 'Preferred'}])

    def test_exact_native_values_are_not_equated_or_inferred_from_names(self):
        values = facet_values({
            'title': 'OS NGD height in EPSG:27700, metres, OGL, annual',
            'resource': 'https://publisher.example.test/catalogue',
            'details': {'spatialReference': '27700', 'crs': [{'@id': 'http://www.opengis.net/def/crs/EPSG/0/27700'}],
                        'unit_of_measure': '  metres  '},
        })
        self.assertEqual(values['spatial_reference'], ['27700'])
        self.assertEqual(values['crs'], ['http://www.opengis.net/def/crs/EPSG/0/27700'])
        self.assertEqual(values['unit'], ['  metres  '])
        self.assertEqual(values['source_publisher'], [])
        self.assertEqual(values['update_frequency'], [])
        self.assertNotIn('license', values)
        self.assertNotIn('product', values)

    def test_dimension_inventory_is_finite_and_presentation_keeps_four_suggested_facets(self):
        keys = [definition['key'] for definition in FACET_DEFINITIONS]
        self.assertEqual(len(keys), 18)
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(set(facet_values({})), set(keys))
        self.assertTrue(all(definition['source_paths'] for definition in FACET_DEFINITIONS))
        shown = [row['key'] for row in presentation_facets() if row['default_state'] == 'shown']
        self.assertEqual(shown, ['record_type', 'source_family', 'tag', 'review_status'])
        self.assertTrue(all(row['default_state'] in ('shown', 'hidden') for row in presentation_facets()))


if __name__ == '__main__':
    unittest.main()
