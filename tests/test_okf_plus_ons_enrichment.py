"""Synthetic metadata-only contract tests; no network or provider observations."""
import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import Mock

from scripts.okf_plus.ons_enrichment import (
    CENSUS_TYPES, CacheOnlyCapture, NOMIS_BASE, NOMIS_SELECT, native_period_bounds,
    nomis_overviews, nomis_times, ons_versions,
)
from urllib.parse import urlencode
from scripts.okf_plus.harvest import Capture as FileCapture


class Capture:
    def __init__(self, root, responses=None):
        self.public = Path(root)
        self.responses = responses or {}
        self.calls = []

    def source(self, name, records):
        (self.public / (name + '.json')).write_text(json.dumps({'records': records}))

    def get(self, url, kind='json'):
        self.calls.append(url)
        data = self.responses[url]
        return data, {'url': url, 'retrievedAt': '2026-10-02T00:00:00Z',
                      'status': 200 if data is not None else 503,
                      'sha256': hashlib.sha256(json.dumps(data).encode()).hexdigest()}

    def save(self, name, records, receipts, coverage):
        self.result = {'records': records, 'receipts': receipts, 'coverage': coverage}
        (self.public / (name + '.json')).write_text(json.dumps(self.result))


BASE = 'https://api.beta.ons.gov.uk/v1/datasets/demo/editions/time-series/versions/2'
DATASET = {'id': 'demo', 'links': {'latest_version': {'href': BASE}}}
METADATA = {'id': 'demo', 'edition': 'time-series', 'version': 2,
            'title': 'Synthetic series', 'release_date': '2026-10-01T00:00:00Z',
            'release_frequency': 'Quarterly', 'contacts': [{'name': 'Synthetic Contact'}],
            'dimensions': [{'name': 'time', 'label': 'Time', 'id': 'yyyy-qq'}]}
CENSUS_METADATA = {'version': 2, 'title': 'Synthetic Census table',
    'contacts': [{'name': 'Synthetic Contact'}], 'release_date': '2026-10-01T00:00:00Z',
    'dataset_links': {'self': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/demo'},
                      'editions': {'href': 'https://api.beta.ons.gov.uk/v1/datasets/demo/editions'},
                      'latest_version': {'href': BASE, 'id': '2'}},
    'is_based_on': {'@id': 'synthetic-native-table', '@type': 'cantabular_flexible_table'},
    'dimensions': [{'name': 'ltla', 'label': 'Local authority', 'id': 'ltla'},
                   {'name': 'year_arrival_uk', 'label': 'Year of arrival'}]}
NOMIS = {'id': 'NM_1_1', 'components': {'timedimension': {'conceptref': 'TIME', 'codelist': 'CL_1_1_TIME'},
          'dimension': [{'conceptref': 'FREQ', 'codelist': 'CL_1_1_FREQ', 'isfrequencydimension': 'true'}]}}


def page(offset, total, values):
    return {'offset': offset, 'limit': 1, 'count': len(values), 'total_count': total,
            'items': [{'option': x, 'label': x, 'dimension': 'time'} for x in values]}


class EnrichmentTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.cap = Capture(self.folder.name)

    def test_ons_pagination_keeps_release_and_native_periods_separate(self):
        self.cap.source('ons-datasets', [DATASET])
        self.cap.responses = {BASE + '/metadata': METADATA,
            BASE + '/dimensions/time/options?limit=1&offset=0': page(0, 2, ['2020-Q2']),
            BASE + '/dimensions/time/options?limit=1&offset=1': page(1, 2, ['2019-Q4'])}
        ons_versions(self.cap, page_size=1)
        row = self.cap.result['records'][0]
        self.assertEqual(row['temporal']['bounds']['minimumNative'], '2019-Q4')
        self.assertEqual(row['metadata']['release_date'], METADATA['release_date'])
        self.assertTrue(row['temporal']['complete'])
        self.assertNotIn('Synthetic Contact', json.dumps(self.cap.result))
        self.assertEqual(len(self.cap.calls), 3)

    def test_ons_duplicate_codes_cannot_claim_complete_bounds(self):
        self.cap.source('ons-datasets', [DATASET])
        self.cap.responses = {BASE + '/metadata': METADATA,
            BASE + '/dimensions/time/options?limit=1000&offset=0': page(0, 2, ['2020', '2020'])}
        ons_versions(self.cap)
        result = self.cap.result['records'][0]['temporal']
        self.assertFalse(result['complete'])
        self.assertIsNone(result['bounds']['minimumNative'])
        self.assertEqual(result['duplicateCount'], 1)

    def test_ons_changed_total_and_premature_empty_page_are_incomplete(self):
        self.cap.source('ons-datasets', [DATASET])
        self.cap.responses = {BASE + '/metadata': METADATA,
            BASE + '/dimensions/time/options?limit=1&offset=0': page(0, 2, ['2020']),
            BASE + '/dimensions/time/options?limit=1&offset=1': page(1, 3, [])}
        ons_versions(self.cap, page_size=1)
        result = self.cap.result['records'][0]['temporal']
        self.assertFalse(result['complete'])
        self.assertFalse(result['stableReportedTotal'])
        self.assertEqual(result['stopReason'], 'empty-page-before-total')

    def test_arbitrary_latest_url_is_not_requested(self):
        self.cap.source('ons-datasets', [{'id': 'demo', 'links': {'latest_version': {'href': 'https://example.invalid/observations'}}}])
        ons_versions(self.cap)
        self.assertEqual(self.cap.calls, [])
        self.assertEqual(self.cap.result['records'][0]['metadataStatus'], 'invalid-latest-version-link')

    def test_census_variants_use_exact_typed_links_without_inferred_periods(self):
        for source_type in sorted(CENSUS_TYPES):
            with self.subTest(source_type=source_type), tempfile.TemporaryDirectory() as root:
                cap = Capture(root); source = {**DATASET, 'type': source_type}
                metadata = deepcopy(CENSUS_METADATA)
                metadata['is_based_on']['@type'] = source_type
                cap.source('ons-datasets', [source]); cap.responses[BASE + '/metadata'] = metadata
                ons_versions(cap)
                row = cap.result['records'][0]
                self.assertEqual(row['metadataStatus'], 'captured')
                self.assertEqual(row['metadataContract']['variant'], 'cantabular-dataset-links')
                self.assertEqual(row['metadataContract']['identityEvidence']['isBasedOn']['@type'], source_type)
                self.assertEqual(row['dimensions'][0]['id'], 'ltla')
                self.assertNotIn('codeListId', row['dimensions'][0])
                self.assertEqual(row['temporal']['reason'], 'no-native-time-dimension')
                self.assertIsNone(row['temporal']['minimumNative'])
                self.assertEqual(cap.calls, [BASE + '/metadata'])
                self.assertNotIn('Synthetic Contact', json.dumps(cap.result))

    def test_census_mismatched_identity_or_type_does_not_admit_time_requests(self):
        mutations = [
            lambda d: d.update(version=3),
            lambda d: d.update(version=True),
            lambda d: d.update(id='different'),
            lambda d: d.update(edition='different'),
            lambda d: d.update(type='filterable'),
            lambda d: d['dataset_links']['self'].update(href='https://example.invalid/demo'),
            lambda d: d['dataset_links']['editions'].update(href='https://api.beta.ons.gov.uk/v1/datasets/other/editions'),
            lambda d: d['dataset_links']['latest_version'].update(href=BASE + '0'),
            lambda d: d['dataset_links']['latest_version'].update(id='3'),
            lambda d: d['is_based_on'].update({'@type': 'cantabular_multivariate_table'}),
            lambda d: d['is_based_on'].update({'@id': ''}),
            lambda d: d.update(dimensions=None),
        ]
        for number, mutate in enumerate(mutations):
            with self.subTest(case=number), tempfile.TemporaryDirectory() as root:
                cap = Capture(root); metadata = deepcopy(CENSUS_METADATA); mutate(metadata)
                cap.source('ons-datasets', [{**DATASET, 'type': 'cantabular_flexible_table'}])
                cap.responses[BASE + '/metadata'] = metadata
                ons_versions(cap)
                self.assertEqual(cap.result['records'][0]['metadataStatus'], 'invalid-metadata-contract')
                self.assertEqual(cap.calls, [BASE + '/metadata'])

    def test_static_omitted_dimensions_are_valid_metadata_but_unknown_time(self):
        self.cap.source('ons-datasets', [{**DATASET, 'type': 'static'}])
        metadata = {**METADATA, 'type': 'static', 'title': 'Synthetic 1981 to 2011 static data',
                    'links': {'self': {'href': BASE + '/metadata'}, 'version': {'href': BASE, 'id': '2'}}}
        del metadata['dimensions']
        self.cap.responses[BASE + '/metadata'] = metadata
        ons_versions(self.cap)
        row = self.cap.result['records'][0]
        self.assertEqual(row['metadataStatus'], 'captured')
        self.assertEqual(row['metadataContract']['variant'], 'static-scalar-identity')
        self.assertFalse(row['metadataContract']['dimensionListPresent'])
        self.assertEqual(row['dimensions'], [])
        self.assertIsNone(row['temporal']['minimumNative'])
        self.assertEqual(self.cap.calls, [BASE + '/metadata'])
        metadata['type'] = 'filterable'
        ons_versions(self.cap)
        self.assertEqual(self.cap.result['records'][0]['metadataStatus'], 'invalid-metadata-contract')

    def test_cache_only_never_delegates_uncaptured_url(self):
        self.cap.ledger = {'requests': [{'url': BASE + '/metadata', 'status': 200}]}
        self.cap.responses[BASE + '/metadata'] = METADATA
        cached = CacheOnlyCapture(self.cap)
        value, receipt = cached.get(BASE + '/metadata')
        self.assertEqual(value, METADATA)
        self.assertEqual(receipt['status'], 200)
        value, receipt = cached.get(BASE + '/dimensions/time/options?limit=1000&offset=0')
        self.assertIsNone(value)
        self.assertEqual(receipt['status'], 'not-captured-cache-only')
        self.assertEqual(self.cap.calls, [BASE + '/metadata'])

    def test_cache_only_preserves_failed_request_evidence_without_retry(self):
        failure={'url':BASE+'/metadata','status':500,'retrievedAt':'2026-10-02T00:00:00Z'}
        self.cap.ledger={'requests':[failure]}
        value,receipt=CacheOnlyCapture(self.cap).get(BASE+'/metadata')
        self.assertIsNone(value)
        self.assertEqual(receipt,failure)
        self.assertEqual(self.cap.calls,[])

    def test_real_cache_preserves_json_default_and_explicit_text_without_network(self):
        cap = FileCapture(Path(self.folder.name))
        cap.private.mkdir(parents=True)
        text_url = 'https://docs.os.uk/os-apis/synthetic.md'
        json_url = 'https://api.beta.ons.gov.uk/v1/datasets/synthetic'
        for url, raw in [(text_url, b'# Synthetic official guide\n'),
                         (json_url, b'{"id":"synthetic"}')]:
            digest = hashlib.sha256(raw).hexdigest()
            (cap.private / (digest + '.body')).write_bytes(raw)
            cap.ledger['requests'].append({'url': url, 'status': 200,
                'sha256': digest, 'rawFile': digest + '.body'})
        cap.opener = Mock()
        cached = CacheOnlyCapture(cap)
        text, _ = cached.get(text_url, 'text')
        data, _ = cached.get(json_url)
        self.assertEqual(text, '# Synthetic official guide\n')
        self.assertEqual(data, {'id': 'synthetic'})
        cap.opener.open.assert_not_called()

    def test_period_bounds_reject_invalid_mixed_and_partial_periods(self):
        for values, complete in [(['2026-13'], True), (['2025', '2025-01'], True), (['2020-Q1'], False), (['2020/21'], True)]:
            self.assertIsNone(native_period_bounds([{'option': x} for x in values], complete)['minimumNative'])

    def test_nomis_overview_preserves_unknown_periods_and_excludes_contact(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        url = NOMIS_BASE + '/NM_1_1.overview.json?' + urlencode({'select': NOMIS_SELECT})
        self.cap.responses[url] = {'overview': {'id': 'NM_1_1', 'firstreleased': '2004-06-16 09:30:00',
            'contact': {'name': 'Synthetic Contact'}, 'dimensions': {'dimension': {'concept': 'time', 'name': 'date'}}}}
        nomis_overviews(self.cap)
        row = self.cap.result['records'][0]
        self.assertEqual(row['releaseDates']['firstreleased'], '2004-06-16 09:30:00')
        self.assertIsNone(row['temporal']['minimumNative'])
        self.assertEqual(row['frequency']['status'], 'unknown')
        self.assertNotIn('Synthetic Contact', json.dumps(self.cap.result))
        self.assertNotIn('Contact', self.cap.calls[0])
        self.assertEqual(len(row['dimensions']), 1)

    def test_nomis_time_codelist_retains_native_dates_and_selected_revisions(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
            'id': 'CL_1_1_TIME', 'code': [{'value': '1983-06', 'description': {'value': 'June 1983', 'lang': 'en'},
                'annotations': {'annotation': [{'annotationtitle': 'CurrentRevisionReleased', 'annotationtext': '2004-06-16 09:30:00'},
                    {'annotationtitle': 'Contact', 'annotationtext': 'Synthetic Contact'}]}}, {'value': '2026-08'}]}}}}
        nomis_times(self.cap)
        row = self.cap.result['records'][0]
        self.assertEqual(row['bounds']['minimumNative'], '1983-06')
        self.assertEqual(row['codes'][0]['revisionMetadata'][0]['value'], '2004-06-16 09:30:00')
        self.assertNotIn('Synthetic Contact', json.dumps(self.cap.result))
        self.assertEqual(self.cap.result['coverage']['temporalBoundsKnown'], 1)

    def test_nomis_duplicate_time_codes_fail_validation(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
            'id': 'CL_1_1_TIME', 'code': [{'value': '2020'}, {'value': '2020'}]}}}}
        nomis_times(self.cap)
        self.assertEqual(self.cap.result['records'][0]['metadataStatus'], 'invalid-time-codelist-contract')
        self.assertFalse(self.cap.result['coverage']['timeCodelistsComplete'])

    def test_nomis_numeric_annual_codes_and_descriptions_preserve_native_types(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
            'id': 'CL_1_1_TIME', 'code': [{'value': 2026, 'description': {'value': 2026, 'lang': 'en'}},
                                      {'value': 1971, 'description': {'value': 1971, 'lang': 'en'}}]}}}}
        nomis_times(self.cap)
        row = self.cap.result['records'][0]
        self.assertEqual(row['metadataStatus'], 'captured')
        self.assertIs(type(row['codes'][0]['value']), int)
        self.assertIs(type(row['codes'][0]['description']['value']), int)
        self.assertEqual(row['bounds']['minimumNative'], 1971)
        self.assertEqual(row['bounds']['maximumNative'], 2026)
        self.assertEqual(row['bounds']['comparisonRule'], 'Nomis-native-integer-year.v1')
        self.assertFalse(row['bounds']['continuityEstablished'])

    def test_nomis_decimal_mixed_and_non_year_codes_do_not_imply_year_bounds(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        for values in [[1971, '2026'], [1971.0, 2026.0], [99, 100], [10000, 10001]]:
            self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
                'id': 'CL_1_1_TIME', 'code': [{'value': v, 'description': {'value': v}} for v in values]}}}}
            with self.subTest(values=values):
                nomis_times(self.cap)
                row = self.cap.result['records'][0]
                self.assertEqual(row['metadataStatus'], 'captured')
                self.assertEqual([v['value'] for v in row['codes']], values)
                self.assertIsNone(row['bounds']['minimumNative'])
                self.assertEqual(row['bounds']['status'], 'unknown-unrecognised-or-mixed-period-codes')

    def test_nomis_boolean_nonfinite_and_duplicate_numeric_codes_fail_closed(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        for codes in [[{'value': True}], [{'value': False}], [{'value': float('nan')}],
                      [{'value': float('inf')}], [{'value': float('-inf')}],
                      [{'value': 1971}, {'value': 1971}], [{'value': 1971}, {'value': 1971.0}],
                      [{'value': 1971, 'description': {'value': True}}],
                      [{'value': 1971, 'description': {'value': float('nan')}}]]:
            self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
                'id': 'CL_1_1_TIME', 'code': codes}}}}
            with self.subTest(codes=codes):
                nomis_times(self.cap)
                row = self.cap.result['records'][0]
                self.assertEqual(row['metadataStatus'], 'invalid-time-codelist-contract')
                self.assertIsNone(row['bounds']['minimumNative'])
                self.assertFalse(self.cap.result['coverage']['timeCodelistsComplete'])

    def test_numeric_descriptions_are_not_used_to_invent_period_extrema(self):
        self.cap.source('ons-nomis-datasets', [NOMIS])
        self.cap.responses[NOMIS_BASE + '/NM_1_1/time.def.sdmx.json'] = {'structure': {'codelists': {'codelist': {
            'id': 'CL_1_1_TIME', 'code': [{'value': 'A', 'description': {'value': 1971}},
                                      {'value': 'B', 'description': {'value': 2026}}]}}}}
        nomis_times(self.cap)
        row = self.cap.result['records'][0]
        self.assertEqual(row['metadataStatus'], 'captured')
        self.assertIsNone(row['bounds']['minimumNative'])

    def test_batch_merge_preserves_denominator_and_rejects_changed_cohort(self):
        self.cap.source('ons-datasets', [{'id': 'first'}, {'id': 'second'}])
        ons_versions(self.cap, start=0, limit=1)
        self.assertEqual(self.cap.result['coverage']['reportedTotal'], 2)
        ons_versions(self.cap, start=1, limit=1)
        self.assertEqual(self.cap.result['coverage']['attemptedUnique'], 2)
        self.cap.source('ons-datasets', [{'id': 'replacement'}])
        with self.assertRaisesRegex(ValueError, 'input changed'):
            ons_versions(self.cap)


if __name__ == '__main__':
    unittest.main()
