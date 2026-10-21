"""Synthetic proofs for private selected-list retention, scope and identity."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus import classification_release as release
from scripts.okf_plus.model import digest, read_markdown
from scripts.okf_plus.term_discovery import search_discovery


def payload():
    return {'schema': release.SCHEMA, 'reviewedOn': '2026-10-21', 'globalComplete': False,
            'schemes': [{'id': 'synthetic-a', 'title': 'Synthetic scheme', 'edition': 'v1',
                         'referenceDate': None, 'publishedDate': '2025-01-17',
                         'retrievedAt': '2026-10-21T13:00:00Z', 'jurisdiction': 'Synthetic',
                         'description': 'No real data.', 'sources': [{'id': 'source',
                         'title': 'Synthetic source', 'url': 'https://example.org/list', 'sha256': 'a' * 64}],
                         'coverage': {'status': 'complete-selected-list', 'expectedEntries': 2,
                         'retainedEntries': 2, 'definitionsStatus': 'mixed-or-partial'},
                         'gaps': ['Only the selected synthetic list is covered.'],
                         'entries': [{'id': 'one', 'code': '01', 'label': 'Alpha',
                         'definition': None, 'level': 'one', 'parentCode': None,
                         'aliases': [{'text': 'first kind', 'kind': 'search-variant',
                         'authority': 'project-search-variant', 'sourceId': 'source'}],
                         'sourceId': 'source', 'sourceLocator': '/rows/0',
                         'native': {'code': '01', 'null': None, 'empty': '', 'space': ' ', 'zero': 0, 'false': False}},
                         {'id': 'two', 'code': '01', 'label': 'Alpha', 'definition': '',
                         'level': None, 'parentCode': 'missing', 'aliases': [],
                         'sourceId': 'source', 'sourceLocator': '/rows/1', 'native': {'code': '01'}}]}]}


class ClassificationReleaseTests(unittest.TestCase):
    def test_export_reconstructs_all_entries_and_native_values(self):
        source = payload()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'new'
            receipt = release.export(source, out, 'b' * 64)
            rows = [read_markdown(p)[0] for p in (out / 'cards').glob('*.md')]
            self.assertEqual(len(rows), 2)
            self.assertEqual({r['details']['entry']['id']: r['details']['entry'] for r in rows},
                             {e['id']: e for e in source['schemes'][0]['entries']})
            for f in receipt['files']:
                raw = (out / f['path']).read_bytes()
                self.assertEqual(len(raw), f['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), f['sha256'])
            self.assertEqual(receipt['canonicalPayloadSha256'], digest(source))
            self.assertFalse(receipt['globalComplete'])
            self.assertTrue((out / 'COMPLETE.json').is_file())

    def test_equal_codes_across_or_within_schemes_never_merge(self):
        source = payload()
        second = copy.deepcopy(source['schemes'][0]); second['id'] = 'synthetic-b'
        source['schemes'].append(second)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'new'; release.export(source, out, 'b' * 64)
            index = json.loads((out / 'term-discovery.json').read_text())
            self.assertEqual(index['recordCount'], 4)
            hits = search_discovery(index, '01')['hits']
            self.assertEqual(len(hits), 4)
            self.assertEqual(len({h['recordId'] for h in hits}), 4)
            self.assertTrue(all(h['meaning'] == 'lexical-navigation-only' for h in hits))

    def test_null_and_empty_definitions_remain_distinct_without_invented_dates(self):
        p = payload(); s = p['schemes'][0]
        null = release.concept_record(s, s['entries'][0], digest(p))
        empty = release.concept_record(s, s['entries'][1], digest(p))
        self.assertNotIn('skos:definition', null)
        self.assertEqual(empty['skos:definition'], '')
        self.assertIsNone(null['temporal']['start'])
        self.assertIsNone(null['update']['metadataModified'])
        self.assertNotIn('skos:broader', empty)

    def test_unknown_editions_remain_bound_to_distinct_source_snapshots(self):
        p = payload(); s = p['schemes'][0]; s['edition'] = None
        before = release.concept_record(s, s['entries'][0], digest(p))
        s['sources'][0]['sha256'] = 'b' * 64
        after = release.concept_record(s, s['entries'][0], digest(p))
        self.assertNotEqual(before['@id'], after['@id'])
        self.assertNotEqual(before['skos:inScheme'], after['skos:inScheme'])

    def test_declared_language_is_retained_without_guessing_absent_language(self):
        p = payload(); s = p['schemes'][0]; e = s['entries'][0]
        before = release.concept_record(s, e, digest(p))
        self.assertEqual(before['skos:prefLabel'], 'Alpha')
        e['labelLanguage'] = 'cy'
        release.validate(p)
        after = release.concept_record(s, e, digest(p))
        self.assertEqual(after['skos:prefLabel'], {'@value': 'Alpha', '@language': 'cy'})

    def test_uncoded_explanatory_rows_do_not_become_extra_concepts(self):
        p = payload(); s = p['schemes'][0]; e = s['entries'][0]
        for code in [None, '', ' ']:
            e['code'] = code
            row = release.concept_record(s, e, digest(p))
            self.assertEqual(row['type'], 'Documentation')
            self.assertNotIn('skos:notation', row)
            self.assertNotIn('skos:Concept', row['@type'])
            self.assertEqual(row['details']['entry']['code'], code)

    def test_generated_records_and_lexical_forms_validate_existing_contracts(self):
        root = release.ROOT; p = payload(); s = p['schemes'][0]
        validators = {n: Draft202012Validator(json.loads((root / 'okf-plus/schemas' / n).read_text()))
                      for n in ['record.schema.json', 'lexical-form.schema.json']}
        for e in s['entries']:
            r = release.concept_record(s, e, digest(p))
            validators['record.schema.json'].validate(r)
            for form in r.get('okfp:lexicalForm', []):
                validators['lexical-form.schema.json'].validate(form)

    def test_counts_sources_identity_and_global_claims_fail_closed(self):
        for change in [lambda p: p.update(globalComplete=True),
                       lambda p: p['schemes'][0]['coverage'].update(expectedEntries=None),
                       lambda p: p['schemes'][0]['coverage'].update(retainedEntries=1),
                       lambda p: p['schemes'][0]['entries'][0].update(sourceId='absent'),
                       lambda p: p['schemes'][0]['entries'][0].update(id='two'),
                       lambda p: p['schemes'][0]['entries'][0].pop('definition'),
                       lambda p: p['schemes'][0]['sources'][0].update(url='https://example.org/?key=synthetic')]:
            p = payload(); change(p)
            with self.subTest(payload=p), self.assertRaises((ValueError, ValidationError)):
                release.validate(p)

    def test_unknown_denominator_is_allowed_only_as_partial(self):
        p = payload(); p['schemes'][0]['coverage'].update(expectedEntries=None, status='partial')
        release.validate(p)

    def test_definition_coverage_does_not_confuse_labels_and_definitions(self):
        p = payload(); p['schemes'][0]['coverage']['definitionsStatus'] = 'source-definitions-retained'
        with self.assertRaises(ValueError): release.validate(p)
        p['schemes'][0]['coverage']['definitionsStatus'] = 'labels-only'
        release.validate(p)
        p['schemes'][0]['entries'][0]['definition'] = 'A separate definition.'
        with self.assertRaises(ValueError): release.validate(p)

    def test_no_overwrite_and_no_success_after_write_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'exists'; out.mkdir(); (out / 'user').write_text('keep')
            with self.assertRaises(ValueError): release.export(payload(), out, 'b' * 64)
            self.assertEqual((out / 'user').read_text(), 'keep')
            new = Path(tmp) / 'new'
            original = Path.open
            def fail(path, *args, **kwargs):
                if path.name == 'term-discovery.json': raise OSError('Synthetic disk failure')
                return original(path, *args, **kwargs)
            with patch.object(Path, 'open', fail), self.assertRaises(OSError):
                release.export(payload(), new, 'b' * 64)
            self.assertFalse((new / 'COMPLETE.json').exists())

    def test_bounded_reader_rejects_duplicate_keys_symlink_fifo_and_oversize(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; source.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError): release.read_payload(source)
            link = root / 'link'; link.symlink_to(source)
            with self.assertRaises(OSError): release.read_payload(link)
            fifo = root / 'fifo'; os.mkfifo(fifo)
            with self.assertRaises(ValueError): release.read_payload(fifo)
            source.write_text('{}')
            with patch.object(release, 'MAX_BYTES', 1), self.assertRaises(ValueError):
                release.read_payload(source)

    def test_completion_fsync_failure_never_publishes_complete_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'new'
            original = os.fsync
            calls = 0
            def fail_last(fd):
                nonlocal calls
                calls += 1
                # Two cards, index, payload, then pending completion receipt.
                if calls == 5: raise OSError('Synthetic marker flush failure')
                return original(fd)
            with patch.object(release.os, 'fsync', fail_last), self.assertRaises(OSError):
                release.export(payload(), out, 'b' * 64)
            self.assertFalse((out / 'COMPLETE.json').exists())

    def test_payload_digest_is_computed_once_for_export(self):
        p = payload()
        with tempfile.TemporaryDirectory() as tmp, patch.object(release, 'digest', wraps=release.digest) as spy:
            release.export(p, Path(tmp) / 'new', 'b' * 64)
            self.assertEqual(sum(call.args[0] is p for call in spy.call_args_list), 1)

    def test_oversized_card_refused_before_any_output(self):
        p = payload(); p['schemes'][0]['entries'][0]['native']['large'] = 'x' * 17000
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'new'
            with self.assertRaises(ValueError): release.export(p, out, 'b' * 64)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
