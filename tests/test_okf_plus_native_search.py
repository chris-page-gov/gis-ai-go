"""Synthetic source-native discovery without code, alias or equivalence promotion."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus import classification_release as release
from scripts.okf_plus.model import digest, read_markdown
from scripts.okf_plus.native_search import resolve_native
from scripts.okf_plus.term_discovery import build_discovery, search_discovery
from tests.test_okf_plus_classification_release import payload


def source():
    p = payload()
    e = p['schemes'][0]['entries'][0]
    e.update(code=None, aliases=[], codeRole='unresolved-native-value')
    e['native']['value'] = '🆕ZZ13SA'
    e['nativeSearchForms'] = [{'text': '🆕ZZ13SA', 'kind': 'source-native-value',
                             'authority': 'source-stated', 'sourceId': e['sourceId'],
                             'sourceLocator': e['sourceLocator'], 'nativePointer': '/native/value',
                             'language': None}]
    return p


def record(p):
    s = p['schemes'][0]
    return release.concept_record(s, s['entries'][0], digest(p))


def discover(row):
    return build_discovery([row], {'namespaces': []}, 'a' * 40, 'b' * 64)


class NativeSearchTests(unittest.TestCase):
    def test_actual_export_retains_whole_native_context_and_searches_full_value(self):
        p = source(); before = copy.deepcopy(p)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'new'; release.export(p, out, 'b'*64)
            rows = [read_markdown(f)[0] for f in (out/'cards').glob('*.md')]
            r = next(r for r in rows if r['details']['entry']['code'] is None)
            self.assertEqual(r['type'], 'Documentation')
            self.assertNotIn('skos:notation', r)
            self.assertNotIn('skos:altLabel', r)
            self.assertEqual(r['details']['entry'], p['schemes'][0]['entries'][0])
            index = json.loads((out/'term-discovery.json').read_text())
            hits = search_discovery(index, 'ZZ13SA')['hits']
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]['form']['value'], '🆕ZZ13SA')
            self.assertEqual(hits[0]['form']['sourcePointer'], '/details/entry/native/value')
            self.assertEqual(p, before)

    def test_all_projected_records_forms_and_index_validate(self):
        r = record(source()); index = discover(r)
        for name, value in [('record', r), ('lexical-form', r['okfp:lexicalForm'][0]), ('term-discovery', index)]:
            schema = json.loads((release.ROOT/'okf-plus/schemas'/(name+'.schema.json')).read_text())
            Draft202012Validator(schema).validate(value)

    def test_source_pointer_escape_and_empty_key(self):
        for key, pointer in [('', '/native/'), ('a/b~c', '/native/a~1b~0c')]:
            p = source(); e = p['schemes'][0]['entries'][0]
            e['native'] = {key: '🆕ZZ13SA'}; e['nativeSearchForms'][0]['nativePointer'] = pointer
            release.validate(p)
            self.assertEqual(len(search_discovery(discover(record(p)), 'ZZ13SA')['hits']), 1)

    def test_unresolved_or_false_source_pointer_refused(self):
        for key, value in [('nativePointer','/native/missing'), ('nativePointer','/label'),
                           ('nativePointer','/native/a~2b'), ('sourceLocator','elsewhere'),
                           ('sourceId','missing'), ('text','ZZ13SA'), ('language','en'),
                           ('authority','project-search-variant')]:
            p = source(); p['schemes'][0]['entries'][0]['nativeSearchForms'][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises((ValueError, ValidationError)): release.validate(p)

    def test_null_empty_and_nonstring_values_do_not_become_text(self):
        for value in [None, '', False, 0, [], {}]:
            p = source(); p['schemes'][0]['entries'][0]['native']['value'] = value
            with self.subTest(value=value), self.assertRaises((ValueError, ValidationError)): release.validate(p)

    def test_unresolved_role_cannot_promote_a_code(self):
        p = source(); p['schemes'][0]['entries'][0]['code'] = 'ZZ13SA'
        with self.assertRaisesRegex(ValueError, 'code role conflict'): release.validate(p)

    def test_native_only_value_does_not_become_a_form(self):
        p = source(); del p['schemes'][0]['entries'][0]['nativeSearchForms']
        self.assertEqual(search_discovery(discover(record(p)), 'ZZ13SA')['hits'], [])

    def test_qualified_back_reference_rejects_modified_context_form_or_identity(self):
        for change in [lambda r: r['okfp:lexicalForm'][0].update({'okfp:sourcePointer':'/details/entry/native/missing'}),
                       lambda r: r['okfp:lexicalForm'][0]['rdf:value'].update({'@value':'ZZ13SA'}),
                       lambda r: r['okfp:lexicalForm'][0].update({'@id':'https://example.org/other'}),
                       lambda r: r['okfp:lexicalForm'][0]['prov:wasDerivedFrom'][0].update({'@id':'https://example.org/other'}),
                       lambda r: r['details']['entry']['native'].update(value='changed'),
                       lambda r: r['details']['entry'].pop('nativeSearchForms'),
                       lambda r: r['details']['entry']['nativeSearchForms'][0].update(sourceLocator='elsewhere')]:
            r = record(source()); change(r)
            with self.assertRaises((ValueError, ValidationError)): discover(r)

    def test_duplicate_qualified_native_form_refused(self):
        r = record(source()); r['okfp:lexicalForm'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate source-native'): discover(r)

    def test_non_native_form_cannot_smuggle_source_pointer(self):
        r = record(source()); r['okfp:lexicalForm'][0]['okfp:formKind'] = 'search-variant'
        with self.assertRaisesRegex(ValueError, 'Source pointer requires'): discover(r)

    def test_equal_forms_across_schemes_do_not_merge(self):
        p = source(); a = record(p); p['schemes'][0]['id'] = 'other'; b = record(p)
        index = build_discovery([a,b], {}, 'a'*40, 'b'*64)
        self.assertEqual(len(search_discovery(index, 'ZZ13SA')['hits']), 2)
        self.assertNotEqual(a['okfp:lexicalForm'][0]['@id'], b['okfp:lexicalForm'][0]['@id'])

    def test_unicode_character_ceiling_preserves_supplementary_characters(self):
        p = source(); e = p['schemes'][0]['entries'][0]
        e['native']['value'] = e['nativeSearchForms'][0]['text'] = '🆕'*1000
        release.validate(p)
        e['native']['value'] = e['nativeSearchForms'][0]['text'] = '🆕'*1001
        with self.assertRaises((ValueError, ValidationError)): release.validate(p)

    def test_unpaired_surrogates_are_refused_in_forms_and_native_keys(self):
        for bad in ['\ud800', '\udfff']:
            p = source(); e = p['schemes'][0]['entries'][0]
            e['native']['value'] = e['nativeSearchForms'][0]['text'] = bad
            with self.assertRaises(ValueError): release.validate(p)
            p = source(); e = p['schemes'][0]['entries'][0]
            e['native'][bad] = 'source text'
            with self.assertRaises(ValueError): release.validate(p)

    def test_depth_order_duplicate_and_size_bounds(self):
        for pointer in ['/native/values/01', '/native/values/-']:
            with self.assertRaises((ValueError, ValidationError)): resolve_native({'native':{'values':['x']}}, pointer)
        p = source(); e = p['schemes'][0]['entries'][0]; e['nativeSearchForms'] *= 2
        with self.assertRaisesRegex(ValueError, 'duplicate pointer'): release.validate(p)
        p = source(); e = p['schemes'][0]['entries'][0]
        e['native']['value'] = e['nativeSearchForms'][0]['text'] = 'x'*1001
        with self.assertRaises((ValueError, ValidationError)): release.validate(p)


if __name__ == '__main__': unittest.main()
