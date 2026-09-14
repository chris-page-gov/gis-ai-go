"""The public chronology is a checked projection, not a count of search hits."""
import csv
import json
import unittest
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'docs/chronicle/data'


class ClaudeRetrospectiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((DATA / 'claude-observations.json').read_text())
        cls.rows = cls.ledger['observations']

    def test_count_reconciles_without_claiming_exhaustiveness(self):
        self.assertEqual(self.ledger['documented_minimum_outcomes'], len(self.rows))
        self.assertEqual(self.ledger['category_counts'], dict(Counter(r['category'] for r in self.rows)))
        self.assertEqual(len({r['ref'] for r in self.rows}), len(self.rows))
        self.assertFalse(self.ledger['chronology_complete'])
        self.assertIsNone(self.ledger['full_attempt_count'])

    def test_original_twelve_are_crosswalked_once_not_added(self):
        old = [r['old_ref'] for r in self.rows if r['old_ref']]
        self.assertCountEqual(old, [f'C{i:02}' for i in range(1, 13)])
        self.assertEqual(len(old), len(set(old)))

    def test_accepted_observed_at_means_execution_finished_not_started(self):
        projections = {
            'C07': 'claude-code-2.1.245-host-002-capability-2026-08-26.json',
            'C12': 'claude-code-2.1.245-exact-five-capability-2026-08-27.json',
        }
        for old, name in projections.items():
            with self.subTest(old=old):
                row = next(r for r in self.rows if r['old_ref'] == old)
                source = json.loads((ROOT / 'tests/interoperability/evidence' / name).read_text())
                self.assertEqual(row['completed_at_utc'], source['observed_at'])
                self.assertIsNone(row['started_at_utc'])
                self.assertTrue(row['accepted_projection'])
        self.assertEqual(sum(r['accepted_projection'] for r in self.rows), 2)

    def test_observation_instant_is_not_silently_a_start(self):
        row = next(r for r in self.rows if r['old_ref'] == 'C01')
        self.assertIsNotNone(row['observed_at_utc'])
        self.assertIsNone(row['started_at_utc'])
        self.assertIsNone(row['completed_at_utc'])

    def test_times_preserve_offsets_and_unknowns(self):
        for row in self.rows:
            start, end = row['started_at_utc'], row['completed_at_utc']
            for key in ('started_at', 'completed_at'):
                value = row[key + '_utc']
                expected = datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(
                    ZoneInfo('Europe/London')).isoformat() if value else None
                self.assertEqual(row[key + '_london'], expected)
            if start and end:
                delta = (datetime.fromisoformat(end.replace('Z', '+00:00')) -
                         datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds()
                self.assertGreaterEqual(delta, 0)
                self.assertEqual(row['elapsed_seconds'], delta)
            else:
                self.assertIsNone(row['elapsed_seconds'])
            for key in ('active_work_seconds', 'actual_billed_cost', 'codex_attributable_usage', 'human_work_seconds'):
                self.assertIsNone(row[key])

    def test_first_public_probe_and_final_completion_window(self):
        window = self.ledger['observation_window']
        start = datetime.fromisoformat(window['first_public_event_utc'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(window['accepted_exact_five_completed_at_utc'].replace('Z', '+00:00'))
        self.assertEqual(window['public_observation_window_seconds'], (end - start).total_seconds())
        self.assertEqual(start.day, 20)
        self.assertEqual(end.day, 27)

    def test_each_source_anchor_resolves_and_cost_detail_is_not_exported(self):
        anchors = self.ledger['source_anchors']
        banned = {'session_id', 'run_id', 'call_id', 'launch_call_ref', 'call_source',
                  'total_cost_usd', 'modelUsage', 'private_root', 'prompt', 'sdk_results'}

        def check(value):
            if isinstance(value, dict):
                self.assertFalse(banned.intersection(value))
                for nested in value.values():
                    check(nested)
            elif isinstance(value, list):
                for nested in value:
                    check(nested)

        check(self.ledger)
        for row in self.rows:
            self.assertTrue(row['sources'])
            self.assertFalse(set(row['sources']) - anchors.keys())

    def test_csv_is_the_same_reviewed_rows_not_an_older_count(self):
        with (DATA / 'claude-observations.csv').open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([r['ref'] for r in rows], [r['ref'] for r in self.rows])
        for csv_row, json_row in zip(rows, self.rows):
            for key, value in csv_row.items():
                expected = json_row[key]
                expected = ';'.join(expected) if isinstance(expected, list) else '' if expected is None else str(expected)
                self.assertEqual(value, expected, (json_row['ref'], key))


if __name__ == '__main__':
    unittest.main()
