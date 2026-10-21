"""Source-position and semantic-boundary proofs for lexical discovery."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest import mock
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
from model import PREFIXES, digest, write_markdown
import term_discovery
from term_discovery import build_discovery, search_discovery, load_index
from tests.contract.test_okf_plus_build import BUILD, REVISION, fixture


def row(identifier='one'):
    return {'@id': 'https://example.org/' + identifier, 'title': 'A test concept',
            'nativeIdentifier': identifier, 'description': 'Synthetic parent definition.',
            'resource': 'https://example.org/source', 'sourceFamily': 'synthetic',
            'sources': [{'resource': 'https://example.org/source'}],
            'skos:prefLabel': {'@value': 'Output Area', '@language': 'en-GB'},
            'skos:altLabel': [{'@value': 'OA', '@language': 'en-GB'},
                              {'@value': 'Ardal Gynnyrch', '@language': 'cy'}],
            'skos:notation': {'@value': 'E01', '@type': 'xsd:string'},
            'details': {'ignored': {'skos:altLabel': 'Not a semantic alias'}}}


def build(*rows, usage=None):
    return build_discovery(list(rows), usage or {}, REVISION, 'a' * 64)


def resolve(source, pointer):
    value = source
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


class TermDiscoveryTests(unittest.TestCase):
    def test_every_form_reconstructs_exact_source_value(self):
        source = row()
        source['skos:hiddenLabel'] = {'@value': ' Output  area '}
        result = build(source)
        for form in result['records'][0]['forms']:
            self.assertEqual(resolve(source, form['pointer']), form['value'])
        self.assertEqual(result['records'][0]['recordSha256'], digest(source))

    def test_language_and_notation_datatype_are_not_guessed(self):
        result = build(row())
        hit = search_discovery(result, 'Ardal Gynnyrch')['hits'][0]
        self.assertEqual(hit['form']['language'], 'cy')
        code = search_discovery(result, 'E01')['hits'][0]
        self.assertEqual(code['form']['datatype'], 'xsd:string')
        self.assertIsNone(code['form']['language'])

    def test_native_enums_preserve_null_number_bool_empty_and_order(self):
        source = row()
        values = [None, False, 0, '', ' ', 'A', 'A', {'kind': 'A'}, ['A']]
        source['okfp:field'] = [{'@id': source['@id'] + '/field/a',
                                'dcterms:identifier': 'a/b~c', 'rdfs:label': 'Native field',
                                'okfp:schemaDefinition': {'@type': '@json', '@value': {
                                    'items': {'oneOf': [{'enum': values}, {'const': 'fixed'}]}}}}]
        result = build(source)
        forms = [f for f in result['records'][0]['forms'] if f['kind'] == 'native-enum']
        self.assertEqual([f['value'] for f in forms], values)
        self.assertEqual(len(forms), len(values))
        for form in result['records'][0]['forms']:
            self.assertEqual(resolve(source, form['pointer']), form['value'])
        self.assertEqual(search_discovery(result, 'a/b~c')['hits'][0]['form']['kind'], 'native-field-name')

    def test_native_table_duplicates_and_whitespace_stay_distinct(self):
        source = row()
        source['details']['table'] = {'encoding': 'os-documentation-native-label-table.v1',
                                     'columns': ['sourceRow', 'nativeText'],
                                     'rows': [[4, 'Road'], [8, 'Road'], [9, ' '], [10, '']]}
        result = build(source)
        forms = [f for f in result['records'][0]['forms'] if f['kind'] == 'native-table-label']
        self.assertEqual([f['value'] for f in forms], ['Road', 'Road', ' ', ''])
        self.assertEqual(search_discovery(result, 'Road')['matchedForms'], 2)
        for f in forms:
            self.assertEqual(resolve(source, f['pointer']), f['value'])

    def test_schema_keyword_positions_do_not_confuse_field_names_or_examples(self):
        source = row()
        schema = {'properties': {'enum': {'type': 'string'}, 'const': {'type': 'string'},
                                 'a/b~c': {'enum': ['actual']}},
                  '$defs': {'enum': {'const': 'definition'}},
                  'examples': [{'enum': ['not a constraint'], 'const': 'not a constraint'}],
                  'default': {'const': 'not a constraint'},
                  'unknownKeyword': {'enum': ['not a constraint']},
                  'dependencies': {'field': ['enum', 'const']},
                  'if': {'properties': {'flag': {'const': True}}},
                  'then': {'items': [{'enum': [1]}]}}
        source['okfp:field'] = [{'@id': source['@id'] + '/field/a',
                                'okfp:schemaDefinition': {'@type': '@json', '@value': schema}}]
        result = build(source)
        native = [f for f in result['records'][0]['forms'] if f['kind'] in ('native-enum', 'native-constant')]
        self.assertEqual([f['value'] for f in native], ['actual', 'definition', True, 1])
        for f in native:
            self.assertEqual(resolve(source, f['pointer']), f['value'])

    def test_no_labels_from_arbitrary_opaque_json_or_prose(self):
        result = build(row())
        self.assertEqual(search_discovery(result, 'Not a semantic alias')['hits'], [])
        self.assertEqual(search_discovery(result, 'Synthetic parent definition')['hits'], [])

    def test_collisions_are_visible_and_never_merge_concepts(self):
        result = build(row('one'), row('two'))
        self.assertEqual(len(search_discovery(result, 'OA')['hits']), 2)
        collision = next(x for x in result['ambiguousForms'] if x['normalisedForm'] == 'oa')
        self.assertEqual(len(collision['nodeIds']), 2)
        self.assertFalse(search_discovery(result, 'OA')['inferencePerformed'])

    def test_project_search_form_is_not_promoted_to_skos_equivalence(self):
        source = row()
        source['okfp:lexicalForm'] = [{'@type': 'okfp:LexicalForm',
            'rdf:value': {'@value': 'small census area', '@language': 'en-GB'},
            'okfp:formKind': 'plain-language-search', 'okfp:authority': 'project-search-variant',
            'prov:wasDerivedFrom': {'@id': 'https://example.org/source'}}]
        result = build(source)
        form = search_discovery(result, 'small census area')['hits'][0]['form']
        self.assertEqual(form['authority'], 'project-search-variant')
        self.assertEqual(form['kind'], 'qualified-lexical-form')
        self.assertNotIn('skos:exactMatch', json.dumps(result))

    def test_unqualified_authored_forms_fail(self):
        source = row()
        source['okfp:lexicalForm'] = [{'rdf:value': {'@value': 'guess'}}]
        with self.assertRaises(ValueError):
            build(source)

    def test_qualified_form_preserves_multiple_sources_and_refuses_unsafe_source(self):
        source = row()
        form = {'@id': source['@id'] + '/form/1',
                'rdf:value': {'@value': 'OA'}, 'okfp:formKind': 'abbreviation',
                'okfp:authority': 'source-stated',
                'prov:wasDerivedFrom': [{'@id': 'https://example.org/one'}, {'@id': 'https://example.org/two'}]}
        source['okfp:lexicalForm'] = [form]
        forms = build(source)['records'][0]['forms']
        actual = next(f for f in forms if f['kind'] == 'qualified-lexical-form')
        self.assertEqual(actual['sources'], ['https://example.org/one', 'https://example.org/two'])
        self.assertEqual(actual['formId'], form['@id'])
        form['prov:wasDerivedFrom'] = [{'@id': 'javascript:alert(1)'}]
        with self.assertRaises(ValueError):
            build(source)

    def test_full_iri_predicates_and_literal_lists_are_supported(self):
        source = row()
        source[PREFIXES['skos'] + 'hiddenLabel'] = {'@list': ['Area output', 'OA hint']}
        result = build(source)
        self.assertEqual(search_discovery(result, 'OA hint')['hits'][0]['form']['kind'], 'hidden-label')

    def test_explicit_empty_language_is_preserved(self):
        source = row()
        source['rdfs:label'] = {'@value': 'Label', '@language': ''}
        self.assertEqual(search_discovery(build(source), 'Label')['hits'][0]['form']['language'], '')

    def test_record_order_deterministic_and_source_unmodified(self):
        first, second = row('one'), row('two')
        before = copy.deepcopy(first)
        self.assertEqual(build(first, second), build(second, first))
        self.assertEqual(first, before)
        with self.assertRaises(ValueError):
            build(first, first)

    def test_search_bounds_and_no_hidden_truncation(self):
        index = build(row(), row('two'))
        result = search_discovery(index, 'OA', 1)
        self.assertTrue(result['truncated'])
        self.assertEqual(result['matchedForms'], 2)
        for query, limit in [('', 10), ('x' * 501, 10), ('OA', True), ('OA', 101)]:
            with self.subTest(query=query, limit=limit), self.assertRaises(ValueError):
                search_discovery(index, query, limit)

    def test_semantic_prefix_and_full_iri_link_to_same_term_without_fetch(self):
        iri = PREFIXES['skos'] + 'Concept'
        usage = {'namespaces': [{'prefix': 'skos', 'namespace': PREFIXES['skos'],
                  'source': 'https://www.w3.org/TR/skos-reference/', 'mappingReview': 'not-certified',
                  'terms': [{'iri': iri, 'used': True}]}]}
        index = build(row(), usage=usage)
        self.assertEqual(search_discovery(index, 'skos:Concept')['semanticTerms'],
                         search_discovery(index, iri)['semanticTerms'])

    def test_malformed_recognised_native_table_fails_closed(self):
        source = row()
        source['details']['table'] = {'encoding': 'os-documentation-native-label-table.v1',
                                     'columns': ['nativeText'], 'rows': []}
        with self.assertRaises(ValueError):
            build(source)

    def test_retained_contract_and_queryable_values_keep_separate_source_positions(self):
        api = row('api'); api['sourceFamily'] = 'os-api-contracts'
        api['details'] = {'contracts': [{'schemas': {'Example': {
            'properties': {'enum': {'type': 'array'}, 'mode': {'enum': ['Full', 'FULL']},
                           'other': {'examples': [{'enum': ['not-a-constraint']}]}}}},
            'operations': [{'parameters': [{'schema': {'enum': ['csv']}}]}]}]}
        ngd = row('ngd'); ngd['sourceFamily'] = 'os-ngd-collections'
        ngd['details'] = {'schemas': {'queryables': {'properties': {
            'kind': {'enum': ['native-kind', None]}}}}}
        result = build(api, ngd)
        original = {source['@id']: source for source in (api, ngd)}
        values = []
        for entry in result['records']:
            for form in entry['forms']:
                if form['kind'] == 'native-enum':
                    self.assertEqual(resolve(original[entry['recordId']], form['pointer']), form['value'])
                    values.append(form['value'])
        self.assertEqual(values, ['Full', 'FULL', 'csv', 'native-kind', None])

    def test_build_descriptor_checksum_and_revision_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'; root.mkdir()
            fixture(root)
            output = Path(directory) / 'bundle'
            BUILD.build(root, output, REVISION)
            raw = (output / 'term-discovery.json').read_bytes()
            index = json.loads(raw)
            self.assertEqual(index['revision'], REVISION)
            self.assertEqual(index['inputDigest'], json.loads((output / 'source-lock.json').read_text())['sha256'])
            self.assertEqual(json.loads((output / 'checksums.json').read_text())['term-discovery.json'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(json.loads((output / 'okf.json').read_text())['entrypoints']['termDiscovery'], 'term-discovery.json')
            self.assertEqual(index['recordCount'], 1)
            self.assertEqual(index['coverage']['allPossibleTermForms'], 'not-established')

    def test_authored_lexical_schema_is_enforced_before_output_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'; root.mkdir()
            source, path, _ = fixture(root)
            source['okfp:lexicalForm'] = [{
                '@id': source['@id'] + '/lexical-form/1', '@type': 'okfp:LexicalForm',
                'rdf:value': {'@value': 'small census area', '@language': 'en-GB'},
                'okfp:formKind': 'search-variant', 'okfp:authority': 'project-search-variant',
                'prov:wasDerivedFrom': [{'@id': 'https://example.org/synthetic-source'}]}]
            write_markdown(path, source, '# Synthetic lexical record')
            output = Path(directory) / 'bundle'
            BUILD.build(root, output, REVISION)
            before = {p.name: p.read_bytes() for p in output.iterdir() if p.is_file()}
            # A project search aid must not masquerade as a source-stated abbreviation.
            source['okfp:lexicalForm'][0]['okfp:formKind'] = 'abbreviation'
            write_markdown(path, source, '# Synthetic invalid lexical record')
            with self.assertRaises(ValidationError):
                BUILD.build(root, output, REVISION)
            self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir() if p.is_file()})

    def test_actual_index_read_is_bounded_and_rejects_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'index.json'
            path.write_text('{"value":1}')
            self.assertEqual(load_index(path), {'value': 1})
            with mock.patch.object(term_discovery, 'MAX_INPUT_BYTES', 4), self.assertRaises(ValueError):
                load_index(path)
            original = term_discovery.os.fstat
            calls = []
            def replace_after_read(fd):
                result = original(fd)
                calls.append(fd)
                if len(calls) == 2:
                    path.unlink()
                    path.write_text('{"value":2}')
                return result
            with mock.patch.object(term_discovery.os, 'fstat', side_effect=replace_after_read), self.assertRaises(ValueError):
                load_index(path)

    def test_fifo_is_rejected_without_waiting_for_a_writer(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fifo'
            os.mkfifo(path)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/okf_plus/term_discovery.py'),
                                     '--index', str(path), '--query', 'OA'],
                                    capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('bounded regular file', result.stderr)

    def test_output_schema_refuses_kind_confusion_and_completeness_promotion(self):
        schema = json.loads((ROOT / 'okf-plus/schemas/term-discovery.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        index = build(row())
        validator.validate(index)
        bad = copy.deepcopy(index)
        bad['coverage']['globalVocabularyCompleteness'] = 'complete'
        with self.assertRaises(ValidationError):
            validator.validate(bad)
        bad = copy.deepcopy(index)
        bad['records'][0]['forms'][0]['kind'] = 'sameAs'
        with self.assertRaises(ValidationError):
            validator.validate(bad)


if __name__ == '__main__':
    unittest.main()
