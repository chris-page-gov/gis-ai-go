"""Controlled-list discovery uses schema locations, not arbitrary matching keys."""
import copy
import json
from pathlib import Path
import unittest

import jsonschema
from scripts.okf_plus.model import read_markdown
from scripts.okf_plus.vocabulary_inventory import record_nodes, schema_constraints, schema_roots

ROOT = Path(__file__).resolve().parents[1]


class VocabularyInventoryTests(unittest.TestCase):
    def test_annotations_are_opaque(self):
        schema = {'enum': ['native', None], 'default': {'enum': ['not a constraint']},
                  'examples': [{'const': 'example'}], 'x-extension': {'enum': ['annotation']}}
        self.assertEqual(list(schema_constraints(schema)), [('/enum', 'enum', ['native', None])])

    def test_property_names_are_not_keywords(self):
        schema = {'properties': {'enum': {'type': 'array', 'items': {'type': 'string'}},
                                 'const': {'enum': ['actual constraint']}}}
        self.assertEqual(list(schema_constraints(schema)),
                         [('/properties/const/enum', 'enum', ['actual constraint'])])

    def test_nested_schema_positions_and_escaped_pointer(self):
        schema = {'$defs': {'a/b~': {'enum': [0, False]}},
                  'items': [{'const': 2}, True], 'if': {'enum': ['if']},
                  'then': {'not': {'const': 3}}, 'dependentSchemas': {'x': {'enum': ['x']}},
                  'dependencies': {'y': ['required-name']},
                  'anyOf': [{'const': {'enum': 'native object'}}, False],
                  '$ref': 'https://example.invalid/never-fetched'}
        paths = [row[0] for row in schema_constraints(schema)]
        self.assertEqual(paths, ['/$defs/a~1b~0/enum', '/items/0/const', '/if/enum',
                                 '/then/not/const', '/dependentSchemas/x/enum', '/anyOf/0/const'])

    def test_invalid_constraint_refused(self):
        with self.assertRaises(ValueError):
            list(schema_constraints({'enum': {'type': 'array'}}))

    def test_openapi_root_locations(self):
        row = {'sourceFamily': 'os-api-contracts', 'details': {'contracts': [{
            'schemas': {'A': {'enum': ['schema']}},
            'componentParameters': {'p': {'schema': {'const': 'parameter'}}},
            'operations': [{'parameters': [{'schema': {'enum': [1]}}],
                            'requestBody': {'content': {'application/json': {'schema': {'const': 2}}}},
                            'responses': {'200': {'content': {'application/json': {'schema': {'enum': [3]}}},
                                                 'headers': {'x': {'schema': {'const': 4}}}}},
                            'examples': {'schema': {'enum': ['not a root']}}}]}]}}
        roots = list(schema_roots(row))
        self.assertEqual(len(roots), 6)
        self.assertEqual(sum(len(list(schema_constraints(s, p))) for p, s in roots), 6)

    def test_nominal_ids_and_retained_time_differ(self):
        row = {'sourceFamily': 'ons-nomis-datasets', 'details': {'components': {
            'dimension': [{'codelist': 'CL_X_TIME', 'conceptref': 'TIME'}],
            'attribute': [{'codelist': 'CL_X_TIME', 'conceptref': 'OTHER'}]}}}
        nodes = list(record_nodes(row))
        self.assertEqual(len(nodes), 2)
        self.assertNotEqual(nodes[0]['pointer'], nodes[1]['pointer'])
        self.assertEqual(nodes[0]['nativeId'], nodes[1]['nativeId'])
        time = {'sourceFamily': 'ons-nomis-time-options', 'details': {
            'codeListId': 'CL_X_TIME', 'timeOptionsTable': {'rows': [[2021], [2023]]}}}
        self.assertEqual(list(record_nodes(time))[0]['rowCount'], 2)

    def test_source_label_duplicates_are_preserved(self):
        row = {'sourceFamily': 'osngd-documentation-pages', 'details': {'tables': [{
            'nativeLabelTable': {'rows': [[0, 'Unknown'], [1, 'Unknown']]},
            'nativeLabelScope': {'omittedLabelRows': 0}}]}}
        node = list(record_nodes(row))[0]
        self.assertEqual((node['rowCount'], node['omittedRows']), (2, 0))


class AuthoredVocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / 'okf-plus/profile/learning-vocabulary.json').read_text())
        cls.lexical = json.loads((ROOT / 'okf-plus/schemas/lexical-form.schema.json').read_text())

    def test_records_sources_and_qualified_forms(self):
        record_schema = json.loads((ROOT / 'okf-plus/schemas/record.schema.json').read_text())
        source_ids = {source['id'] for source in self.registry['sources']}
        term_ids, record_ids = set(), set()
        for term in self.registry['terms']:
            self.assertNotIn(term['id'], term_ids)
            self.assertNotIn(term['recordId'], record_ids)
            term_ids.add(term['id'])
            record_ids.add(term['recordId'])
            self.assertTrue(set(term['sourceRefs']) <= source_ids)
            row, body = read_markdown(ROOT / term['recordFile'])
            self.assertEqual(row['@id'], term['recordId'])
            jsonschema.Draft202012Validator(record_schema).validate(row)
            for form in row.get('okfp:lexicalForm', []):
                jsonschema.Draft202012Validator(self.lexical).validate(form)
                self.assertIn(form['rdf:value']['@value'], body)
                self.assertTrue(form['prov:wasDerivedFrom'])
            for forbidden in ('skos:exactMatch', 'owl:sameAs', 'owl:equivalentClass'):
                self.assertNotIn(forbidden, row)
        self.assertEqual(len(term_ids), 46)
        self.assertFalse(self.registry['globalComplete'])

    def test_unknown_language_and_closed_authority(self):
        validator = jsonschema.Draft202012Validator(self.lexical)
        row, _ = read_markdown(ROOT / 'okf-plus/records/vocabulary-learning/la.md')
        form = copy.deepcopy(row['okfp:lexicalForm'][0])
        form['rdf:value'].pop('@language', None)
        validator.validate(form)
        form['rdf:value']['@language'] = None
        self.assertTrue(list(validator.iter_errors(form)))
        form['rdf:value'].pop('@language')
        form['okfp:authority'] = 'unqualified-synonym'
        self.assertTrue(list(validator.iter_errors(form)))

    def test_project_variant_never_source_alternative(self):
        row, _ = read_markdown(ROOT / 'okf-plus/records/vocabulary-learning/jit.md')
        form = copy.deepcopy(row['okfp:lexicalForm'][0])
        self.assertEqual(form['okfp:authority'], 'project-search-variant')
        form['okfp:formKind'] = 'source-alternative-label'
        self.assertTrue(list(jsonschema.Draft202012Validator(self.lexical).iter_errors(form)))

    def test_source_review_states_do_not_claim_raw_responses(self):
        states = {'official-page-opened-text-reviewed', 'official-search-result-extract-reviewed',
                  'local-pinned-project-file-read'}
        for source in self.registry['sources']:
            self.assertIn(source['reviewState'], states)
            self.assertFalse(source['responseBytesRetained'])
            self.assertNotIn('responseSha256', source)


if __name__ == '__main__':
    unittest.main()
