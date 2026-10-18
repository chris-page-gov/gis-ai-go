"""Synthetic bounded GEMINI and inert product-state capture contracts."""
from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.okf_plus import metadata_refresh as M
from scripts.okf_plus.os_enrichment import GEMINI_PATH, OPENSEARCH, PRODUCT_SEARCH
from tests.contract.test_okf_plus_metadata_refresh import Clock, FakeTransport

GEMINI_HOST = 'osmetadata.astuntechnology.com'
PRODUCT_HOST = 'www.ordnancesurvey.co.uk'
GEMINI_BASE = 'https://' + GEMINI_HOST + GEMINI_PATH
TEMPLATE = GEMINI_BASE + '?f=json&q={searchTerms}&startIndex={startIndex?}'


def page_url(offset):
    return GEMINI_BASE + '?f=json&q=&startindex=' + str(offset) + '&limit=10'


def root_xml(template=TEMPLATE):
    return ('<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">'
            '<Url type="application/json" indexOffset="0" template="' +
            template.replace('&', '&amp;') + '"/></OpenSearchDescription>').encode()


def gemini_page(start, count, total):
    return {'timed_out': False, '_shards': {'failed': 0},
            'hits': {'total': {'value': total, 'relation': 'eq'},
                     'hits': [{'_id': 'synthetic-' + str(index),
                               '_source': {'uuid': 'synthetic-' + str(index),
                                           'resourceTitleObject': {'default': 'Synthetic catalogue ' + str(index)},
                                           'abstract': 'Full synthetic metadata definition.'}}
                              for index in range(start, start + count)]}}


def product_html(count=60, total=65):
    state = {'search': {'listings': {'productListing': {
        'pagingInfo': {'totalCount': total, 'pageIndex': 0, 'pageSize': count},
        'results': [{'id': 'synthetic-' + str(index), 'uri': '/products/synthetic-' + str(index),
                     'title': 'Synthetic product ' + str(index), 'tags': {}}
                    for index in range(count)]}}}}
    return ('<html><script>window.REDUX_DATA = ' + json.dumps(state) + ';</script>'
            '<script src="https://not-followed.invalid/code.js">throw Error("Never execute");</script>'
            '<a href="https://not-followed.invalid/data.zip">not followed</a></html>').encode()


class MetadataCatalogueTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.clock = Clock()
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)

    def refresh(self, urls, responses, *, semantic_cards=True):
        initial = [M.task(url, 'synthetic-catalogue-test') for url in urls]
        self.stack.enter_context(patch.object(M, 'seeds', return_value=(initial, [])))
        self.transport = FakeTransport(responses)
        return M.Refresh(self.root, transport=self.transport, clock=self.clock,
                         sleeper=self.clock.sleep, semantic_cards=semantic_cards,
                         policy_path=self.root / 'no-environment-policy.json')

    def run_capture(self, refresh, **kwargs):
        return refresh.run(allowed_hosts=[GEMINI_HOST, PRODUCT_HOST], **kwargs)

    def test_offline_seed_plan_includes_catalogue_roots_before_paginated_requests(self):
        planned, _ = M.seeds(self.root)
        urls = [item['url'] for item in planned]
        self.assertIn(OPENSEARCH, urls)
        self.assertIn(PRODUCT_SEARCH, urls)
        self.assertNotIn(page_url(0), urls)
        self.assertTrue(all(not item['authenticated'] for item in planned
                            if item['url'] in (OPENSEARCH, PRODUCT_SEARCH)))
        self.assertFalse((self.root / M.PRIVATE_PATH).exists())

    def test_exact_reviewed_catalogue_routes_admitted_and_payload_query_variants_rejected(self):
        for url in (OPENSEARCH, page_url(0), page_url(10), PRODUCT_SEARCH):
            with self.subTest(url=url):
                self.assertFalse(M.admit(url)[1])
        denied = [
            GEMINI_BASE + '?f=json&q=&startIndex=0&limit=10',
            GEMINI_BASE + '?f=json&q=&startindex=0&limit=1000',
            GEMINI_BASE + '?f=json&q=&startindex=-1&limit=10',
            GEMINI_BASE + '?f=json&q=&startindex=0&startindex=10&limit=10',
            GEMINI_BASE + '?f=json&q=arbitrary&startindex=0&limit=10',
            page_url(0) + '&key=synthetic',
            page_url(0) + '&redirect=https://not-followed.invalid',
            GEMINI_BASE + '/synthetic-record',
            'https://' + GEMINI_HOST + '/geonetwork/api/records',
            PRODUCT_SEARCH + '?page=2',
            'https://' + PRODUCT_HOST + '/products/synthetic-1',
            'https://' + PRODUCT_HOST + '/products/search-for-os-products/../dataset',
            'https://' + PRODUCT_HOST + '/downloads/v1/dataPackages',
            'https://' + GEMINI_HOST + '/downloads/v1/dataPackages',
            'https://' + PRODUCT_HOST + '/features/ngd/ofa/v1/collections',
            'https://' + GEMINI_HOST + '/downloads/v1/products',
        ]
        for url in denied:
            with self.subTest(url=url), self.assertRaises(ValueError):
                M.admit(url)

    def test_unreviewed_template_and_xml_entities_are_rejected_without_following_links(self):
        targets, gaps = M.discover(OPENSEARCH, root_xml())
        self.assertEqual(targets, [page_url(0)])
        self.assertFalse(gaps)
        for raw in (root_xml(TEMPLATE.replace(GEMINI_HOST, 'not-followed.invalid')),
                    b'<!DOCTYPE x [<!ENTITY remote SYSTEM "https://not-followed.invalid/">]>' + root_xml(),
                    root_xml().replace(b'indexOffset="0"', b'indexOffset="1"')):
            with self.subTest(raw=raw[:40]), self.assertRaises(ValueError):
                M.discover(OPENSEARCH, raw)

    def test_gemini_pagination_uses_bounded_canonical_offsets_and_checkpoints_once(self):
        responses = {OPENSEARCH: root_xml(), page_url(0): json.dumps(gemini_page(0, 10, 12)).encode(),
                     page_url(10): json.dumps(gemini_page(10, 2, 12)).encode()}
        refresh = self.refresh([OPENSEARCH], responses)
        first = self.run_capture(refresh, max_requests=2)
        self.assertEqual(first['requestsTotal'], 2)
        self.assertEqual(first['stopReason'], 'operational-checkpoint')
        self.assertEqual([url for url, _, _ in self.transport.calls], [OPENSEARCH, page_url(0)])
        self.clock.sleep(2)
        result = self.run_capture(refresh)
        self.assertEqual(result['requestsTotal'], 3)
        self.assertEqual(result['bytesTotal'], sum(len(raw) for raw in responses.values()))
        self.assertEqual([url for url, _, _ in self.transport.calls], list(responses))
        self.assertEqual(result['metadataCoverage'], 'complete-for-admitted-queue')
        self.assertEqual(result['overallOSMetadataCoverage'], 'incomplete')
        coverage = result['catalogueFamilies']['os-gemini-metadata']
        self.assertEqual(coverage['reportedTotal'], 12)
        self.assertEqual(coverage['retrievedUnique'], 12)
        self.assertTrue(coverage['catalogueComplete'])
        self.assertTrue(all(not sent_key for _, sent_key, _ in self.transport.calls))
        for item in refresh.state['queue']:
            self.assertEqual(refresh.verify_capture(item), responses[item['url']])
        again = self.run_capture(refresh)
        self.assertEqual(again['runRequests'], 0)
        self.assertEqual(again['capturedCorpusSha256'], result['capturedCorpusSha256'])
        rate_state = json.loads(refresh.limiter.path.read_text())
        service = M.admit(OPENSEARCH)[0]
        self.assertEqual(rate_state['services'][service]['attemptReservations'], 3)

    def test_product_65_total_60_embedded_remains_explicitly_partial_and_inert(self):
        raw = product_html()
        refresh = self.refresh([PRODUCT_SEARCH], {PRODUCT_SEARCH: raw})
        result = self.run_capture(refresh)
        self.assertEqual(len(self.transport.calls), 1)
        self.assertEqual(result['metadataCoverage'], 'incomplete')
        self.assertEqual(result['overallOSMetadataCoverage'], 'incomplete')
        coverage = result['catalogueFamilies']['os-product-search']
        self.assertEqual(coverage['reportedTotal'], 65)
        self.assertEqual(coverage['retrievedUnique'], 60)
        self.assertFalse(coverage['catalogueComplete'])
        self.assertTrue(result['gaps'])
        item = refresh.state['queue'][0]
        self.assertEqual(refresh.verify_capture(item), raw)
        raw_path = refresh.private / 'raw' / (hashlib.sha256(raw).hexdigest() + '.body')
        self.assertEqual(raw_path.read_bytes(), raw)
        manifest = json.loads((refresh.private / item['manifest']).read_text())
        parts = [json.loads((refresh.private / path).read_text()) for path in manifest['records']]
        self.assertEqual(b''.join(part['body'].encode() for part in parts), raw)
        cards = list((refresh.private / 'cards').glob('*/*.md'))
        self.assertTrue(cards)
        self.assertTrue(all(path.stat().st_size <= 16384 for path in cards))
        self.assertTrue(all(path.stat().st_mode & 0o777 == 0o600 for path in [raw_path, *cards]))
        self.assertEqual([url for url, _, _ in self.transport.calls], [PRODUCT_SEARCH])
        self.assertFalse((self.root / 'okf-plus/source/os-product-search.json').exists())

    def test_embedded_product_state_rejects_javascript_expressions(self):
        malicious = [b'<script>window.REDUX_DATA = fetch("https://not-followed.invalid/");</script>',
                     product_html(1, 1).replace(b';</script>', b'; fetch("https://not-followed.invalid/");</script>', 1)]
        for raw in malicious:
            with self.subTest(raw=raw[:40]), self.assertRaises((ValueError, KeyError, TypeError)):
                M.discover(PRODUCT_SEARCH, raw)

    def test_inexact_or_failed_gemini_pages_never_schedule_continuation(self):
        original = gemini_page(0, 10, 12)
        variants = []
        for change in ('inexact', 'timeout', 'shards', 'empty'):
            page = deepcopy(original)
            if change == 'inexact':
                page['hits']['total']['relation'] = 'gte'
            elif change == 'timeout':
                page['timed_out'] = True
            elif change == 'shards':
                page['_shards']['failed'] = 1
            else:
                page['hits']['hits'] = []
            variants.append(page)
        for page in variants:
            with self.subTest(page=page['hits']['total']):
                targets, gaps = M.discover(page_url(0), json.dumps(page).encode())
                self.assertFalse(targets)
                self.assertTrue(gaps)

    def test_provider_next_links_never_override_reviewed_pagination_route(self):
        page = gemini_page(0, 10, 12)
        page['links'] = [{'rel': 'next', 'href': 'https://not-followed.invalid/collect'}]
        targets, _ = M.discover(page_url(0), json.dumps(page).encode())
        self.assertEqual(targets, [page_url(10)])

    def test_cross_page_duplicates_and_unstable_totals_block_completeness(self):
        for variant in ('duplicate', 'changed-total'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                self.root = Path(directory)
                second = gemini_page(0, 2, 12) if variant == 'duplicate' else gemini_page(10, 3, 13)
                responses = {OPENSEARCH: root_xml(), page_url(0): json.dumps(gemini_page(0, 10, 12)).encode(),
                             page_url(10): json.dumps(second).encode()}
                refresh = self.refresh([OPENSEARCH], responses)
                result = self.run_capture(refresh)
                self.assertEqual(result['requestsTotal'], 3)
                self.assertFalse(result['catalogueFamilies']['os-gemini-metadata']['catalogueComplete'])
                self.assertEqual(result['metadataCoverage'], 'incomplete')
                self.assertTrue(result['gaps'])
                self.assertEqual([url for url, _, _ in self.transport.calls], list(responses))

    def test_new_catalogue_service_honours_durable_shared_retry_after(self):
        responses = {OPENSEARCH: (429, b'Rate limited', {'Retry-After': '120'}),
                     page_url(0): json.dumps(gemini_page(0, 0, 0)).encode()}
        refresh = self.refresh([OPENSEARCH], responses)
        first = self.run_capture(refresh)
        self.assertEqual(first['requestsTotal'], 1)
        service = M.admit(OPENSEARCH)[0]
        reserved = M.SharedRateLimiter(self.root, clock=self.clock).reserve_attempt(service)
        self.assertFalse(reserved['allowed'])
        self.assertGreaterEqual(reserved['delay'], 120)
        self.run_capture(refresh)
        self.assertEqual(len(self.transport.calls), 1)
        self.clock.sleep(120)
        responses[OPENSEARCH] = root_xml()
        result = self.run_capture(refresh)
        self.assertEqual(result['requestsTotal'], 3)
        self.assertTrue(result['catalogueFamilies']['os-gemini-metadata']['catalogueComplete'])
        self.assertEqual([url for url, _, _ in self.transport.calls], [OPENSEARCH, OPENSEARCH, page_url(0)])


if __name__ == '__main__':
    unittest.main()
