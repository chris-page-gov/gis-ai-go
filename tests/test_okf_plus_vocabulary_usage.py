"""Offline semantic-position usage, literal mappings and build integration."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
from model import CONTEXT, CTX, PREFIXES, apply_frequency, record
from vocabulary_usage import vocabulary_usage
from tests.contract.test_okf_plus_build import BUILD, REVISION, fixture


def register(*prefixes):
    return {'standards': [{'prefix': p, 'terms': ['Unused'],
                          'source': 'https://example.org/standard',
                          'mappingReview': 'usage-reported-at-build-not-semantic-certification'}
                         for p in prefixes]}


def usage(rows, standards=None):
    return vocabulary_usage(rows, standards or register('dcat', 'geo', 'adms', 'odrl'), REVISION, 'a' * 64)


def namespace(report, prefix):
    return next(n for n in report['namespaces'] if n['prefix'] == prefix)


def term(report, prefix, local):
    return next(t for t in namespace(report, prefix)['terms'] if t['iri'] == PREFIXES[prefix] + local)


class VocabularyUsageTests(unittest.TestCase):
    def test_aliases_expand_and_literals_do_not_become_terms(self):
        row = {'@context': CONTEXT, '@id': PREFIXES['geo'] + 'Geometry',
               'title': 'dcat:Dataset', 'description': PREFIXES['odrl'] + 'Policy',
               'type': 'Dataset', 'status': 'draft'}
        report = usage([row])
        self.assertEqual(term(report, 'dcterms', 'title')['predicateOccurrences'], 1)
        self.assertEqual(term(report, 'okfp', 'recordType')['predicateOccurrences'], 1)
        self.assertEqual(term(report, 'okfp', 'lifecycleStatus')['predicateOccurrences'], 1)
        self.assertFalse(namespace(report, 'geo')['used'])
        self.assertFalse(namespace(report, 'adms')['used'])
        self.assertFalse(namespace(report, 'odrl')['used'])
        self.assertEqual(report['outsideDeclaredNamespaces']['distinctIris'], 0)

    def test_predicates_types_object_and_datatype_references_are_separate(self):
        row = {'@id': 'https://example.org/record', '@type': ['dcat:Dataset', 'geo:Feature'],
               'skos:relatedMatch': [{'@id': 'geo:Geometry'}, {'@id': PREFIXES['geo'] + 'Geometry'}],
               'resource': PREFIXES['geo'] + 'Feature',
               'dcterms:temporal': {'@type': 'dcterms:PeriodOfTime',
                                    'dcat:startDate': {'@value': '2026-10-02', '@type': 'xsd:date'}}}
        report = usage([row])
        self.assertEqual(term(report, 'skos', 'relatedMatch')['predicateOccurrences'], 1)
        self.assertEqual(term(report, 'geo', 'Geometry')['objectReferences'], 2)
        feature = term(report, 'geo', 'Feature')
        self.assertEqual((feature['typeReferences'], feature['objectReferences']), (1, 1))
        self.assertEqual(term(report, 'rdf', 'type')['predicateOccurrences'], 3)
        self.assertEqual(term(report, 'xsd', 'date')['datatypeReferences'], 1)
        self.assertEqual(term(report, 'xsd', 'date')['typeReferences'], 0)

    def test_context_and_opaque_json_internals_never_establish_usage(self):
        payload = {'@type': 'odrl:Policy', 'adms:status': {'@id': 'geo:Geometry'}}
        row = {'@context': CTX, '@id': 'https://example.org/a',
               'details': payload, 'generated': {'by': 'geo:Feature'},
               'okfp:sourceJson': {'@value': payload, '@type': '@json'}}
        report = usage([row])
        for prefix in ('odrl', 'adms', 'geo'):
            self.assertFalse(namespace(report, prefix)['used'])
        self.assertEqual(term(report, 'okfp', 'details')['predicateOccurrences'], 1)
        self.assertEqual(report['totals']['typeReferences'], 0)

    def test_unused_and_additional_terms_are_explicit_without_polluting_counts(self):
        standards = register('dcat', 'odrl')
        standards['standards'][0]['terms'] = ['Dataset', 'DataService']
        row = {'@type': 'dcat:Dataset', 'dcat:keyword': ['one', 'two'],
               'okfp:flag': True, 'dcat:landingPage': {'@id': 'https://example.org/data'}}
        report = usage([row], standards)
        dcat = namespace(report, 'dcat')
        self.assertEqual(dcat['unusedRegisteredTerms'], [PREFIXES['dcat'] + 'DataService'])
        self.assertIn(PREFIXES['dcat'] + 'keyword', dcat['additionalUsedTerms'])
        self.assertIn('odrl', report['unusedRegisteredPrefixes'])
        self.assertIn('okfp', report['usedUnregisteredPrefixes'])
        self.assertEqual(report['outsideDeclaredNamespaces']['distinctIris'], 1)
        self.assertEqual(report, usage([copy.deepcopy(row)], copy.deepcopy(standards)))

    def test_record_counts_do_not_count_same_record_twice(self):
        rows = [{'@id': 'https://example.org/a', '@type': 'geo:Feature',
                 'skos:relatedMatch': {'@id': 'geo:Feature'}},
                {'@id': 'https://example.org/b', '@type': 'geo:Feature'}]
        report = usage(rows)
        self.assertEqual(term(report, 'geo', 'Feature')['recordCount'], 2)
        self.assertEqual(report, usage(list(reversed(rows))))

    def test_lists_preserve_object_positions_and_unknown_contexts_are_refused(self):
        report = usage([{'skos:relatedMatch': {'@list': [{'@id': 'geo:Feature'}]}}])
        self.assertEqual(term(report, 'geo', 'Feature')['objectReferences'], 1)
        for row in ({'@context': 'https://example.org/unreviewed-context'},
                    {'@reverse': {'geo:hasGeometry': {'@id': 'geo:Geometry'}}}):
            with self.subTest(row=row), self.assertRaises(ValueError):
                usage([row])

    def test_local_lifecycle_and_unrecognised_frequency_keep_resource_ranges(self):
        self.assertEqual(CTX['status'], 'okfp:lifecycleStatus')
        self.assertEqual(CTX['type'], 'okfp:recordType')
        row = record('synthetic', 'one', 'One', 'Synthetic metadata',
                     'https://example.org/one', {'resource': 'https://example.org/one'})
        apply_frequency(row, 'Every six weeks', 'frequency')
        self.assertEqual(row['dcterms:accrualPeriodicity'],
                         {'@type': 'dcterms:Frequency', 'rdfs:label': 'Every six weeks'})
        self.assertEqual(row['update']['frequency']['label'], 'Every six weeks')
        self.assertEqual(row['update']['frequency']['sourceField'], 'frequency')
        self.assertIsNone(row['update']['frequency']['iri'])
        report = usage([row])
        self.assertEqual(term(report, 'dcterms', 'Frequency')['typeReferences'], 1)
        self.assertFalse(namespace(report, 'adms')['used'])
        apply_frequency(row, 'Monthly', 'frequency')
        self.assertEqual(row['dcterms:accrualPeriodicity'], {'@id': PREFIXES['sdmx-code'] + 'freq-M'})

    def test_build_report_is_revision_bound_exposed_and_checksummed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'; root.mkdir()
            fixture(root)
            profile = root / 'okf-plus/profile'; profile.mkdir()
            (profile / 'standards.json').write_text(json.dumps(register('dcat', 'adms')))
            output = Path(directory) / 'bundle'
            BUILD.build(root, output, REVISION)
            report_bytes = (output / 'vocabulary-usage.json').read_bytes()
            report = json.loads(report_bytes)
            descriptor = json.loads((output / 'okf.json').read_text())
            source_lock = json.loads((output / 'source-lock.json').read_text())
            checksums = json.loads((output / 'checksums.json').read_text())
            self.assertEqual(report['revision'], REVISION)
            self.assertEqual(report['inputDigest'], source_lock['sha256'])
            self.assertEqual(report['recordCount'], 1)
            self.assertEqual(descriptor['entrypoints']['vocabularyUsage'], 'vocabulary-usage.json')
            self.assertEqual(checksums['vocabulary-usage.json'], hashlib.sha256(report_bytes).hexdigest())


if __name__ == '__main__':
    unittest.main()
