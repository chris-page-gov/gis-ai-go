"""Synthetic evidence tests for offline retrieval estimates."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.okf_plus.retrieval_plan import plan_retrieval


class RetrievalPlanTests(unittest.TestCase):
    def fixture(self):
        return {'api': {'count': 250, 'page_size': 100, 'rate_ceiling': 2,
                        'latency_seconds': {'min': .1, 'max': 1},
                        'processing_seconds': {'min': 4, 'max': 5},
                        'bytes_per_page': 1000, 'coverage': 'synthetic-selection'},
                'bulk': {'known_bytes': 10000,
                         'throughput_bytes_per_second': {'min': 10000, 'max': 20000},
                         'unpack_seconds': {'min': 0, 'max': 1},
                         'processing_seconds': {'min': 0, 'max': 1},
                         'coverage': 'synthetic-selection'}}

    def test_measured_ranges_separate_processing_and_compare(self):
        source = self.fixture()
        before = copy.deepcopy(source)
        result = plan_retrieval(source)
        self.assertEqual(source, before)
        self.assertTrue(result['metadata_only'])
        self.assertFalse(result['execution'])
        self.assertEqual(result['routes']['api']['acquisition_seconds'], {'min': 1.1, 'max': 3})
        self.assertEqual(result['routes']['api']['estimated_transfer_bytes'], 3000)
        self.assertEqual(result['routes']['bulk']['acquisition_seconds'], {'min': .5, 'max': 1})
        self.assertEqual(result['routes']['bulk']['processing_seconds'], {'min': 0, 'max': 2})
        self.assertEqual(result['comparison']['preferred'], 'bulk')

    def test_unknowns_do_not_become_defaults(self):
        result = plan_retrieval({'api': {'count': 100}, 'bulk': {}})
        for route in result['routes'].values():
            self.assertIsNone(route['acquisition_seconds'])
            self.assertIsNone(route['processing_seconds'])
            self.assertIsNone(route['total_seconds'])
            self.assertTrue(route['unknowns'])
        self.assertIsNone(result['comparison']['preferred'])

    def test_different_coverage_never_compared(self):
        source = self.fixture()
        source['bulk']['coverage'] = 'different-selection'
        self.assertIsNone(plan_retrieval(source)['comparison']['preferred'])

    def test_zero_count_has_no_requests(self):
        source = self.fixture()
        source['api']['count'] = 0
        api = plan_retrieval(source)['routes']['api']
        self.assertEqual(api['pages'], 0)
        self.assertEqual(api['acquisition_seconds'], {'min': 0, 'max': 0})

    def test_rejects_bad_numbers_types_fields_and_ranges(self):
        for field, value in [('count', True), ('count', 1.5), ('count', -1),
                             ('count', 10**19), ('page_size', 0),
                             ('rate_ceiling', float('nan')), ('rate_ceiling', float('inf')),
                             ('rate_ceiling', '2'), ('rate_ceiling', 5e-324), ('coverage', ''), ('unknown', 1),
                             ('latency_seconds', {'min': 3, 'max': 2}),
                             ('latency_seconds', {'min': 1, 'max': 2, 'other': 3})]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                plan_retrieval({'api': {field: value}})
        with self.assertRaises(ValueError):
            plan_retrieval({'bulk': {'throughput_bytes_per_second': {'min': 0, 'max': 2}}})

    def test_cli_emits_json_and_rejects_oversized_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.json'
            source.write_text(json.dumps(self.fixture()))
            run = subprocess.run([sys.executable, '-m', 'scripts.okf_plus.retrieval_plan', str(source)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse(json.loads(run.stdout)['execution'])
            source.write_text(' ' * 65537)
            run = subprocess.run([sys.executable, '-m', 'scripts.okf_plus.retrieval_plan', str(source)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn('exceeds', run.stderr)
