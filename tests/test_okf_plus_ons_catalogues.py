"""Synthetic ONS catalogue contracts; no live requests or source observations."""
import hashlib
import json
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.okf_plus.ons_catalogues import code_lists, population_types, release_calendar, website_search


class Capture:
    def __init__(self, *responses):
        self.responses = list(responses); self.calls = []

    def get(self, url):
        self.calls.append(url); response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        data, status = (response, 200) if not isinstance(response, tuple) else response
        return data, {'url': url, 'status': status, 'retrievedAt': '2026-10-02T00:00:00Z',
                      'sha256': hashlib.sha256(json.dumps(data).encode()).hexdigest()}

    def save(self, family, records, receipts, coverage):
        self.family = family; self.result = {'records': records, 'receipts': receipts, 'coverage': coverage}


def item(uri='/datasets/synthetic/a', content_type='dataset'):
    return {'uri': uri, 'title': 'Synthetic catalogue record', 'type': content_type,
            'cdid': 'ABCD', 'dataset_id': 'SYNTHETIC', 'release_date': '2026-09-01T00:00:00Z',
            'contact': {'name': 'Synthetic Contact'}, 'summary': 'Synthetic metadata only.'}


def search(items, total, distinct=999):
    return {'items': items, 'count': total, 'distinct_items_count': distinct,
            'content_types': [{'type': 'dataset', 'count': 900}, {'type': 'timeseries', 'count': 9999}]}


def release():
    return {'uri': '/releases/synthetic', 'date_changes': [
        {'previous_date': '2026-01-01T09:30:00Z', 'change_notice': 'Synthetic postponement',
         'contact': 'Synthetic Contact'}],
        'description': {'title': 'Synthetic release', 'summary': 'Synthetic metadata only.',
                        'release_date': '2026-01-08T09:30:00Z', 'published': True,
                        'cancelled': False, 'finalised': True, 'postponed': False, 'census': False,
                        'contact': 'Synthetic Contact'}}


class CatalogueTests(unittest.TestCase):
    def test_search_uses_filtered_count_and_keeps_overlapping_representations(self):
        cap = Capture(search([item('/datasets/a'), item('/datasets/b')], 3),
                      search([item('/datasets/c')], 3))
        website_search(cap, 'dataset', page_size=2)
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(len(cap.calls), 2)
        self.assertEqual(cap.result['coverage']['reportedTotal'], 3)
        self.assertEqual(cap.result['coverage']['pageCounts'][0]['distinctItemsCount'], 999)
        self.assertEqual({x['cdid'] for x in cap.result['records']}, {'ABCD'})
        self.assertEqual(len(cap.result['records']), 3)
        self.assertEqual(cap.result['records'][2]['sourceEvidence']['pointer'], '/items/0')
        self.assertEqual(parse_qs(urlsplit(cap.calls[1]).query)['offset'], ['2'])
        self.assertNotIn('Synthetic Contact', json.dumps(cap.result))

    def test_duplicate_uri_cannot_claim_complete_catalogue(self):
        cap = Capture(search([item(), item()], 2))
        website_search(cap, 'dataset')
        self.assertFalse(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(cap.result['coverage']['duplicateCount'], 1)
        self.assertEqual(cap.result['coverage']['stopReason'], 'count-mismatch-or-mutation')

    def test_changed_counts_and_empty_page_preserve_incomplete_evidence(self):
        cap = Capture(search([item()], 2), search([], 3))
        website_search(cap, 'dataset', page_size=1)
        self.assertFalse(cap.result['coverage']['stableReportedTotal'])
        self.assertEqual(cap.result['coverage']['stopReason'], 'count-mismatch-or-mutation')
        self.assertEqual(cap.result['coverage']['reportedTotal'], 2)
        self.assertEqual(cap.result['coverage']['lastReportedTotal'], 3)
        self.assertEqual(cap.result['coverage']['retrievedUnique'], 1)

    def test_invalid_item_or_filtered_type_never_triggers_follow_on_fetch(self):
        for bad in (item('https://example.invalid/data'), item('//example.invalid/data'),
                    item('/../data'), item('/data?download=yes'), item(content_type='timeseries')):
            with self.subTest(bad=bad):
                cap = Capture(search([bad], 1))
                website_search(cap, 'dataset')
                self.assertEqual(cap.result['coverage']['stopReason'], 'invalid-page-contract')
                self.assertEqual(cap.result['records'], [])
                self.assertEqual(len(cap.calls), 1)

    def test_timeseries_metadata_preserves_native_ids_without_observations(self):
        data = item('/economy/example/timeseries/abcd/synthetic', 'timeseries')
        data['months'] = [{'date': '2026-01', 'value': 123}]
        cap = Capture(search([data], 1))
        website_search(cap, 'timeseries')
        self.assertEqual(cap.family, 'ons-website-timeseries')
        self.assertEqual(cap.result['records'][0]['dataset_id'], 'SYNTHETIC')
        self.assertNotIn('months', cap.result['records'][0])
        self.assertTrue(all(urlsplit(x).path == '/v1/search' for x in cap.calls))

    def test_release_window_state_changes_and_overlapping_breakdown_are_retained(self):
        cap = Capture({'breakdown': {'total': 1, 'published': 1, 'census': 1}, 'releases': [release()]})
        release_calendar(cap, 'type-published', from_date='2026-01-01', to_date='2026-12-31')
        row = cap.result['records'][0]
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(row['description']['release_date'], '2026-01-08T09:30:00Z')
        self.assertEqual(row['date_changes'][0]['previous_date'], '2026-01-01T09:30:00Z')
        self.assertEqual(row['sourceEvidence']['pointer'], '/releases/0')
        self.assertEqual(cap.result['coverage']['pageCounts'][0]['breakdown']['census'], 1)
        self.assertNotIn('Synthetic Contact', json.dumps(cap.result))
        for start, end in [(None, None), ('2026-02-30', '2026-12-31'), ('2026-12-31', '2026-01-01')]:
            denied = Capture()
            with self.assertRaises(ValueError):
                release_calendar(denied, 'type-published', from_date=start, to_date=end)
            self.assertEqual(denied.calls, [])

    def test_population_definitions_do_not_enumerate_query_combinations(self):
        cap = Capture({'items': [{'name': 'synthetic-people', 'label': 'People', 'type': 'microdata',
                                  'description': 'Synthetic universe', 'contact': 'Synthetic Contact'},
                                 {'name': 'synthetic-dwellings', 'label': 'Dwellings', 'type': 'tabular'}],
                       'count': 2, 'offset': 0, 'limit': 1000, 'total_count': 2})
        population_types(cap)
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(cap.result['records'][0]['nativeIdentityField'], 'name')
        self.assertEqual(len(cap.calls), 1)
        self.assertNotIn('Synthetic Contact', json.dumps(cap.result))

    def test_http_failure_page_ceiling_and_shared_stop_remain_explicit(self):
        denied = Capture((None, 403)); website_search(denied, 'dataset')
        self.assertEqual(denied.result['coverage']['requestStatuses'], [403])
        self.assertFalse(denied.result['coverage']['catalogueComplete'])
        self.assertIsNone(denied.result['coverage']['reportedTotal'])
        partial = Capture(search([item()], 2)); website_search(partial, 'dataset', page_size=1, max_pages=1)
        self.assertEqual(partial.result['coverage']['stopReason'], 'page-ceiling')
        stopped = Capture(search([item()], 2), RuntimeError('Synthetic shared ceiling'))
        with self.assertRaises(RuntimeError):
            website_search(stopped, 'dataset', page_size=1)
        self.assertEqual(stopped.result['coverage']['stopReason'], 'shared-capture-stopped')
        self.assertEqual(stopped.result['coverage']['retrievedUnique'], 1)

    def test_code_list_inventory_keeps_native_ids_without_following_children(self):
        cap = Capture({'items': [{'id': 'synthetic-years', 'label': 'Synthetic years',
                                  'links': {'editions': {'href': 'https://example.invalid/data'}}}],
                       'count': 1, 'offset': 0, 'limit': 1000, 'total_count': 1})
        code_lists(cap)
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(cap.result['records'][0]['id'], 'synthetic-years')
        self.assertNotIn('links', cap.result['records'][0])
        self.assertEqual(len(cap.calls), 1)

    def test_code_list_nested_identity_and_http_links_are_retained_inert(self):
        nested = {'links': {'self': {'id': 'synthetic-geography',
                    'href': 'http://api.beta.ons.gov.uk/v1/code-lists/synthetic-geography'},
                    'editions': {'href': 'http://api.beta.ons.gov.uk/v1/code-lists/synthetic-geography/editions'}}}
        cap = Capture({'items': [nested], 'count': 1, 'offset': 0, 'total_count': 1})
        code_lists(cap)
        row = cap.result['records'][0]
        self.assertEqual(row['nativeIdentityField'], '/links/self/id')
        self.assertEqual(row['id'], 'synthetic-geography')
        self.assertEqual(row['advertisedLinks'], nested['links'])
        self.assertEqual(len(cap.calls), 1)
        nested['id'] = 'conflicting-identity'
        cap = Capture({'items': [nested], 'count': 1, 'offset': 0, 'total_count': 1})
        code_lists(cap)
        self.assertEqual(cap.result['coverage']['stopReason'], 'invalid-page-contract')
        self.assertEqual(cap.result['records'], [])

    def test_result_window_zero_count_does_not_erase_original_denominator(self):
        cap = Capture(search([item()], 58708), search([], 0, distinct=0))
        website_search(cap, 'dataset', page_size=1)
        self.assertEqual(cap.result['coverage']['reportedTotal'], 58708)
        self.assertEqual(cap.result['coverage']['lastReportedTotal'], 0)
        self.assertEqual(cap.result['coverage']['retrievedUnique'], 1)
        self.assertFalse(cap.result['coverage']['catalogueComplete'])
        self.assertEqual(cap.result['coverage']['stopReason'], 'count-mismatch-or-mutation')

    def test_closed_types_and_page_bounds_fail_before_network(self):
        cap = Capture()
        for kind in ('observations', 'dataset,timeseries', 'https://example.invalid/data'):
            with self.assertRaises(ValueError):
                website_search(cap, kind)
        with self.assertRaises(ValueError):
            website_search(cap, 'dataset', page_size=1001)
        self.assertEqual(cap.calls, [])


if __name__ == '__main__':
    unittest.main()
