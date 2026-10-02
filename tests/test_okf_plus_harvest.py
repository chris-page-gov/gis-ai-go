"""Offline capture-boundary checks; no provider requests or shared ledger writes."""
import json
import signal
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request

from scripts.okf_plus.harvest import Capture, Redirect, allowed, deadline


class HarvestBoundaryTests(unittest.TestCase):
    def test_literal_encoded_and_nested_dot_segments_are_rejected(self):
        paths = ['os-apis/../private.md', 'os-apis/./private.md',
                 'os-apis/%2e%2e/private.md', 'os-apis/.%2E/private.md',
                 'os-apis/%2e./private.md', 'os-apis/%252e%252e/private.md',
                 'os-apis/%25252e/private.md']
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                allowed('https://docs.os.uk/' + path)

    def test_encoded_slashes_and_backslashes_cannot_change_route_boundaries(self):
        paths = ['os-apis/%2fprivate.md', 'os-apis/%2Fprivate.md',
                 'os-apis/%5cprivate.md', 'os-apis/%5Cprivate.md',
                 'os-apis/%252fprivate.md', 'os-apis/%255cprivate.md',
                 'os-apis/..\\private.md', 'os-apis/%255c%252e%252e%255cprivate.md']
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                allowed('https://docs.os.uk/' + path)

    def test_malformed_escapes_and_path_parameters_are_not_accepted_as_metadata(self):
        paths = ['os-apis/%ZZ/private.md', 'os-apis/%/private.md',
                 'os-apis/%ff/private.md', 'os-apis/private.md;other-route']
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                allowed('https://docs.os.uk/' + path)

    def test_refused_url_does_not_consume_admission_or_touch_network(self):
        with tempfile.TemporaryDirectory() as folder:
            cap = Capture(Path(folder), max_requests=1)
            cap.opener = Mock()
            with self.assertRaises(ValueError):
                cap.get('https://docs.os.uk/os-apis/%252e%252e/private.md')
            cap.opener.open.assert_not_called()
            self.assertEqual(cap.ledger['requests'], [])
            self.assertFalse(cap.path.exists())

    def test_existing_metadata_routes_and_query_contracts_stay_admitted(self):
        urls = [
            'https://api.os.uk/downloads/v1/products',
            'https://api.os.uk/downloads/v1/products/OpenNames',
            'https://api.os.uk/features/ngd/ofa/v1/collections',
            'https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema',
            'https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables',
            'https://docs.os.uk/os-apis/llms.txt',
            'https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering.md',
            'https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0',
            'https://api.beta.ons.gov.uk/v1/datasets/demo/editions/time-series/versions/1/metadata',
            'https://api.beta.ons.gov.uk/v1/datasets/demo/editions/time-series/versions/1/dimensions/time/options?limit=1000&offset=0',
            'https://api.beta.ons.gov.uk/v1/code-lists?limit=1000&offset=0',
            'https://api.beta.ons.gov.uk/v1/search?content_type=dataset&limit=1000&offset=0',
            'https://api.beta.ons.gov.uk/v1/search/releases?release-type=type-published&limit=1000&offset=0',
            'https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json',
            'https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.overview.json?select=firstreleased,lastupdated',
            'https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1/time.def.sdmx.json',
            'https://www.nomisweb.co.uk/api/v01/contenttype/index.json',
            'https://www.arcgis.com/sharing/rest/portals/ESMARspQHYMw9BZ9?f=json',
            'https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1&sortField=created&sortOrder=asc',
            'https://osmetadata.astuntechnology.com/geonetwork/api/collections/main?f=opensearch',
            'https://osmetadata.astuntechnology.com/geonetwork/api/collections/044fac9d-3bba-4214-b010-eeb9978422b2/items?f=json&q=&startIndex=0',
            'https://osmetadata.astuntechnology.com/geonetwork/api/collections/044fac9d-3bba-4214-b010-eeb9978422b2/items?f=json&q=&startindex=10&limit=10',
            'https://www.ordnancesurvey.co.uk/products/search-for-os-products',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(allowed(url), url)

    def test_os_delivery_query_remains_exact_and_does_not_admit_other_content(self):
        base = 'https://www.ordnancesurvey.co.uk/api/delivery/projects/osweb/entries/search?'
        query = {'aggregations': json.dumps({'sf_dataType.sys.id': {'field': 'dataType.sys.id', 'size': 100},
                    'sf_access.sys.id': {'field': 'access.sys.id', 'size': 100}}),
            'fields': 'pageMetaData.pageTitle,pageMetaData.image,sys.properties,pageMetaData.description,pageMetaData.sectors,dataType,access,title',
            'linkDepth': 3, 'pageIndex': 0, 'pageSize': 60,
            'where': json.dumps([{'field': 'sys.versionStatus', 'equalTo': 'published'},
                 {'field': 'sys.language', 'in': ['en-GB']}, {'field': 'sys.contentTypeId', 'in': ['product']}])}
        url = base + urlencode(query)
        self.assertEqual(allowed(url), url)
        for patch in [{'pageSize': 100}, {'pageIndex': 101}, {'fields': '*'}, {'where': '[]'}]:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                allowed(base + urlencode({**query, **patch}))

    def test_population_types_has_only_a_bounded_metadata_list_route(self):
        base = 'https://api.beta.ons.gov.uk/v1/population-types'
        for query in ['', '?limit=1&offset=0', '?limit=1000&offset=1000000']:
            self.assertEqual(allowed(base + query), base + query)
        for suffix in ['/usual-residents', '/usual-residents/observations', '/../datasets',
                       '?limit=1001&offset=0', '?limit=0&offset=0', '?limit=1&offset=-1',
                       '?limit=1&offset=1000001', '?limit=1&offset=0&offset=1',
                       '?limit=1', '?limit=1&offset=0&filter=example', '?limit=1.0&offset=0',
                       '?limit=1&offset=', '?limit=1&offset=0&%61pi_key=synthetic']:
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                allowed(base + suffix)

    def test_all_redirect_destinations_require_a_separate_admission(self):
        request = Request('https://api.os.uk/downloads/v1/products')
        for target in ['https://api.os.uk/downloads/v1/products/OpenNames',
                       'https://api.os.uk/features/ngd/ofa/v1/collections/example/items',
                       'https://example.invalid/private']:
            with self.subTest(target=target):
                with self.assertRaises(HTTPError) as raised:
                    Redirect().redirect_request(request, None, 302, 'Found', {}, target)
                raised.exception.close()

    @unittest.skipUnless(hasattr(signal, 'SIGALRM'), 'POSIX wall deadline')
    def test_wall_deadline_interrupts_stalled_work_and_restores_signal_handler(self):
        if signal.getitimer(signal.ITIMER_REAL)[0]:
            self.skipTest('A caller owns the process alarm')
        previous = signal.getsignal(signal.SIGALRM)
        with self.assertRaises(TimeoutError):
            with deadline(.01):
                time.sleep(.1)
        self.assertEqual(signal.getsignal(signal.SIGALRM), previous)
        self.assertEqual(signal.getitimer(signal.ITIMER_REAL)[0], 0)
        self.assertEqual(deadline.__wrapped__.__defaults__, (30,))


if __name__ == '__main__':
    unittest.main()
