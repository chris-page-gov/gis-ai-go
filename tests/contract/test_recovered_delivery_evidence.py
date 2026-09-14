from __future__ import annotations

import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "index_recovered_delivery_evidence",
    SCRIPTS / "index_recovered_delivery_evidence.py",
)
assert SPEC is not None and SPEC.loader is not None
INDEXER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INDEXER)


def write_private(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_bytes(raw)
    path.chmod(0o600)


def projection_record(
    source_line: int,
    source_type: str,
    payload: dict[str, object],
    *,
    timestamp: str,
) -> dict[str, object]:
    return {
        "record": "projected-rollout-record",
        "source_line": source_line,
        "source_line_sha256": hashlib.sha256(
            f"synthetic-source-{source_line}".encode()
        ).hexdigest(),
        "source_bytes": 100 + source_line,
        "source_type": source_type,
        "payload": payload,
        "timestamp": timestamp,
    }


class SyntheticStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(mode=0o700)
        write_private(root / ".lock", b"")
        (root / "objects" / "sha256").mkdir(parents=True, mode=0o700)
        self.private_session_id = 987654
        self._build()

    def _put_object(self, raw: bytes) -> tuple[str, int]:
        digest = hashlib.sha256(raw).hexdigest()
        path = self.root / "objects" / "sha256" / digest[:2] / digest
        write_private(path, raw)
        return digest, len(raw)

    def _build(self) -> None:
        timestamp = "2026-09-14T08:00:00Z"
        call_records = [
            projection_record(
                1,
                "event_msg",
                {"type": "user_message", "message": "Please recover the evidence."},
                timestamp=timestamp,
            ),
            projection_record(
                2,
                "event_msg",
                {"type": "agent_message", "message": "Recovery has started."},
                timestamp=timestamp,
            ),
            projection_record(
                3,
                "response_item",
                {
                    "type": "agent_message",
                    "author": "agent",
                    "recipient": "parent",
                    "content": [
                        {"type": "input_text", "text": "Bounded review complete."}
                    ],
                },
                timestamp=timestamp,
            ),
            projection_record(
                4,
                "response_item",
                {
                    "type": "custom_tool_call",
                    "name": "spawn_agent",
                    "namespace": "collaboration",
                    "call_id": "assignment-call",
                    "arguments": {
                        "task_name": "bounded_review",
                        "message": "Review the bounded change.",
                    },
                },
                timestamp=timestamp,
            ),
            projection_record(
                5,
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "call_id": "assignment-call",
                    "output": [{"type": "text", "text": '{"status":"accepted"}'}],
                },
                timestamp=timestamp,
            ),
            projection_record(
                6,
                "response_item",
                {
                    "type": "custom_tool_call",
                    "name": "exec_command",
                    "call_id": "live-call",
                    "arguments": {
                        "cmd": (
                            "GIS_AI_GO_QUAL_206_CLAUDE_EXACT_FIVE_CAPABILITY=1 "
                            "node scripts/qual_206_claude_exact_five_capability_harness.mjs"
                        )
                    },
                },
                timestamp=timestamp,
            ),
            projection_record(
                7,
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "call_id": "live-call",
                    "output": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                {
                                    "session_id": self.private_session_id,
                                    "total_cost_usd": 1.25,
                                    "output": "Claude process running",
                                }
                            ),
                        }
                    ],
                },
                timestamp=timestamp,
            ),
            projection_record(
                8,
                "response_item",
                {
                    "type": "custom_tool_call",
                    "name": "write_stdin",
                    "call_id": "poll-call",
                    "arguments": {"session_id": self.private_session_id},
                },
                timestamp=timestamp,
            ),
            projection_record(
                9,
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "call_id": "poll-call",
                    "output": [{"type": "text", "text": "still running"}],
                },
                timestamp=timestamp,
            ),
            projection_record(
                10,
                "event_msg",
                {
                    "type": "token_count",
                    "info": {
                        "total_token_usage": {
                            "input_tokens": 100,
                            "output_tokens": 20,
                            "total_tokens": 120,
                        }
                    },
                },
                timestamp=timestamp,
            ),
            projection_record(
                11,
                "event_msg",
                {
                    "type": "task_complete",
                    "turn_id": "turn-private",
                    "duration_ms": 1500,
                },
                timestamp=timestamp,
            ),
        ]
        header = {
            "schema": INDEXER.CODEX_PROJECTION_SCHEMA,
            "record": "projection-header",
            "thread_id": "thread-private",
            "session_id": "session-private",
            "parent_thread_id": None,
            "source_path_sha256": "a" * 64,
            "boundaries": INDEXER.BOUNDARIES,
        }
        footer = {
            "schema": INDEXER.CODEX_PROJECTION_SCHEMA,
            "record": "projection-footer",
        }
        uncompressed = b"".join(
            INDEXER.canonical_json(value)
            for value in [header, *call_records, footer]
        )
        compressed_buffer = io.BytesIO()
        with gzip.GzipFile(
            fileobj=compressed_buffer,
            mode="wb",
            filename="",
            mtime=0,
        ) as stream:
            stream.write(uncompressed)
        projection_digest, projection_bytes = self._put_object(
            compressed_buffer.getvalue()
        )
        source_identity = "synthetic-projected-source"
        source_identity_sha = hashlib.sha256(source_identity.encode()).hexdigest()
        projection_event = {
            "sequence": 0,
            "event_sha256": "1" * 64,
            "source": {
                "kind": INDEXER.PROJECTION_KIND,
                "identity": source_identity,
            },
            "objects": [
                {"sha256": projection_digest, "bytes": projection_bytes}
            ],
            "disposition": {"status": "captured", "reason": "captured"},
        }
        manifest_item = {
            "thread_id": "thread-private",
            "session_id": "session-private",
            "parent_thread_id": None,
            "source_path_sha256": "a" * 64,
            "source_identity": source_identity,
            "source_identity_sha256": source_identity_sha,
            "disposition": "captured",
            "reason": "captured",
            "object_sha256": projection_digest,
            "object_bytes": projection_bytes,
            "uncompressed_sha256": hashlib.sha256(uncompressed).hexdigest(),
            "uncompressed_bytes": len(uncompressed),
            "retained_records": len(call_records),
            "skipped_record_types": {},
        }
        manifest = {
            "schema": INDEXER.CODEX_GENERATION_SCHEMA,
            "thread_id": "thread-private",
            "selection_rule": "target-and-transitive-descendants-by-parent-thread-id",
            "files": [manifest_item],
            "boundaries": INDEXER.BOUNDARIES,
            "collection_generation_sha256": "b" * 64,
            "collection_window": {
                "start_utc": timestamp,
                "end_utc": timestamp,
                "selected_files": 1,
                "selection_rule": "target-and-transitive-descendants-by-parent-thread-id",
            },
            "selected_file_count": 1,
            "aggregate_skipped_record_types": {},
        }
        manifest_digest, manifest_bytes = self._put_object(
            INDEXER.canonical_json(manifest, pretty=True)
        )
        manifest_event = {
            "sequence": 1,
            "event_sha256": "2" * 64,
            "source": {
                "kind": INDEXER.JOURNAL_KIND,
                "identity": "synthetic-generation",
            },
            "objects": [{"sha256": manifest_digest, "bytes": manifest_bytes}],
            "disposition": {"status": "captured", "reason": "captured"},
        }
        self.events = [projection_event, manifest_event]
        journal = b"".join(INDEXER.canonical_json(event) for event in self.events)
        write_private(self.root / "journal.jsonl", journal)
        self.verified = {
            "verified": True,
            "journal_events": len(self.events),
            "journal_head_sha256": manifest_event["event_sha256"],
            "journal_sha256": hashlib.sha256(journal).hexdigest(),
        }


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


@contextlib.contextmanager
def admitted_private_output() -> Any:
    with (
        mock.patch.object(INDEXER, "_require_enforced_volume_ownership") as admitted,
        mock.patch.object(INDEXER, "_has_extended_acl", return_value=False),
    ):
        yield admitted


class RecoveredDeliveryEvidenceTests(unittest.TestCase):
    def test_correlation_queries_use_bounded_lookup_indexes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = INDEXER._database(Path(temporary) / "working.sqlite3")
            try:
                paired_plan = " ".join(
                    str(row[3])
                    for row in database.execute(
                        "EXPLAIN QUERY PLAN SELECT output_json FROM outputs "
                        "WHERE paired_call_id = ? ORDER BY id",
                        (1,),
                    )
                )
                call_process_plan = " ".join(
                    str(row[3])
                    for row in database.execute(
                        "EXPLAIN QUERY PLAN SELECT classification FROM calls "
                        "WHERE process_ref = ? AND process_event = 'start'",
                        ("process-0001",),
                    )
                )
                output_process_plan = " ".join(
                    str(row[3])
                    for row in database.execute(
                        "EXPLAIN QUERY PLAN UPDATE outputs SET direct_claude = 1 "
                        "WHERE process_ref = ?",
                        ("process-0001",),
                    )
                )
            finally:
                database.close()
            self.assertIn("outputs_by_paired_call_id", paired_plan)
            self.assertIn("calls_by_process", call_process_plan)
            self.assertIn("outputs_by_process", output_process_plan)

    def test_candidate_classification_and_cost_boundaries(self) -> None:
        self.assertEqual(
            INDEXER.classify_claude_candidate("claude auth status --json"),
            "authentication",
        )
        self.assertEqual(
            INDEXER.classify_claude_candidate(
                "GIS_AI_GO_QUAL_206_CLAUDE_CAPABILITY=1 "
                "node qual_206_claude_capability_harness.mjs"
            ),
            "live-observation-candidate",
        )
        self.assertEqual(
            INDEXER.classify_claude_candidate("claude mcp list modern stdio"),
            "readiness",
        )
        self.assertEqual(
            INDEXER.classify_claude_candidate(
                "pytest test_qual_206_claude_capability.py"
            ),
            "verifier-or-test",
        )
        costs = INDEXER.extract_sdk_costs(
            {
                "total_cost_usd": 1.5,
                "cost_usd": -2,
                "other": '{"totalCostUsd":2.25,"billing":99}',
                "not_finite": {"costUsd": float("inf")},
            }
        )
        self.assertEqual([item["value"] for item in costs], [1.5, 2.25])
        self.assertTrue(
            all(
                item["classification"] == "reported-cost-field-candidate"
                for item in costs
            )
        )
        self.assertTrue(all(item["provider_usage_proven"] is False for item in costs))
        self.assertTrue(all(item["actual_billed_cost"] == "unknown" for item in costs))

    def test_builds_private_bound_indexes_from_synthetic_projections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "private-index"
            verification_called = False

            def verify(path: Path) -> dict[str, object]:
                nonlocal verification_called
                self.assertEqual(path, store.root)
                verification_called = True
                return store.verified

            with admitted_private_output() as admitted:
                counts = INDEXER.build_index(
                    store.root,
                    output,
                    verify_function=verify,
                )
            admitted.assert_called_once_with(parent.resolve())
            self.assertTrue(verification_called)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o700)
            self.assertTrue(
                all(
                    stat.S_IMODE(path.stat().st_mode) == 0o600
                    for path in output.iterdir()
                )
            )
            self.assertEqual(counts["selected_threads"], 1)
            self.assertEqual(counts["message_records"], 3)
            self.assertEqual(counts["agent_assignment_calls"], 1)
            self.assertEqual(counts["linked_process_sessions"], 1)
            self.assertEqual(counts["process_poll_calls"], 1)
            self.assertEqual(counts["sdk_cost_values"], 1)
            self.assertEqual(counts["token_usage_snapshots"], 1)

            manifest = json.loads((output / "manifest.json").read_text())
            self.assertFalse(manifest["boundaries"]["raw_rollouts_read"])
            self.assertFalse(manifest["boundaries"]["hidden_reasoning_read"])
            self.assertFalse(manifest["boundaries"]["provider_usage_proven"])
            self.assertEqual(manifest["boundaries"]["actual_billed_cost"], "unknown")
            self.assertEqual(len(manifest["input_bindings"]["projections"]), 1)
            self.assertEqual(len(manifest["outputs"]), len(INDEXER.OUTPUT_FILES))

            cost_record = read_jsonl(output / "sdk-costs.jsonl")[0]
            self.assertEqual(
                cost_record["classification"],
                "reported-cost-field-candidate",
            )
            self.assertFalse(cost_record["provider_usage_proven"])

            sessions = read_jsonl(output / "process-sessions.jsonl")
            self.assertEqual(len(sessions), 1)
            self.assertFalse(sessions[0]["session_identifier_published"])
            self.assertNotIn(
                str(store.private_session_id),
                (output / "process-sessions.jsonl").read_text(),
            )
            ledger = read_jsonl(output / "claude-ledger.jsonl")
            poll = next(
                item
                for item in ledger
                if item.get("record_kind") == "tool-call"
                and item.get("process_event") == "poll"
            )
            self.assertEqual(
                poll["model_attempt_status"],
                "orchestration-poll-not-a-model-attempt",
            )
            token_record = read_jsonl(output / "token-usage.jsonl")[0]
            self.assertEqual(token_record["classification"], "token-counts-not-money")

    def test_existing_output_is_preserved_without_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "existing"
            output.mkdir(mode=0o700)
            sentinel = output / "sentinel"
            sentinel.write_text("preserve")
            called = False

            def verify(_path: Path) -> dict[str, object]:
                nonlocal called
                called = True
                return store.verified

            with self.assertRaisesRegex(INDEXER.RecoveryIndexError, "output-already-exists"):
                INDEXER.build_index(store.root, output, verify_function=verify)
            self.assertFalse(called)
            self.assertEqual(sentinel.read_text(), "preserve")

    def test_command_output_is_aggregate_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "command-index"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                admitted_private_output(),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                status = INDEXER.main(
                    ["--store", str(store.root), "--output", str(output)],
                    verify_function=lambda _path: store.verified,
                )
            self.assertEqual(status, 0)
            self.assertEqual(stderr.getvalue(), "")
            summary = json.loads(stdout.getvalue())
            self.assertEqual(set(summary), {"indexed", *INDEXER.SAFE_SUMMARY_KEYS})
            self.assertNotIn(str(store.root), stdout.getvalue())
            self.assertNotIn(str(output), stdout.getvalue())
            self.assertNotIn(str(store.private_session_id), stdout.getvalue())
            self.assertNotIn("Claude", stdout.getvalue())

    def test_verification_failure_does_not_echo_private_detail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "failed-index"
            private_detail = "private-session-987654"

            def fail_verification(_path: Path) -> dict[str, object]:
                raise INDEXER.EvidenceVerificationError(private_detail)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                admitted_private_output(),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                status = INDEXER.main(
                    ["--store", str(store.root), "--output", str(output)],
                    verify_function=fail_verification,
                )
            self.assertEqual(status, 1)
            self.assertEqual(stdout.getvalue(), "")
            self.assertNotIn(private_detail, stderr.getvalue())
            self.assertNotIn(str(store.root), stderr.getvalue())
            self.assertEqual(
                json.loads(stderr.getvalue()),
                {"error": "private-store-verification-failed", "indexed": False},
            )
            self.assertFalse(output.exists())

    def test_unadmitted_output_volume_is_rejected_before_store_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "private-index"
            verification_called = False

            def verify(_path: Path) -> dict[str, object]:
                nonlocal verification_called
                verification_called = True
                return store.verified

            with mock.patch.object(
                INDEXER,
                "_require_enforced_volume_ownership",
                side_effect=INDEXER.EvidenceCaptureError("synthetic external volume"),
            ):
                with self.assertRaisesRegex(
                    INDEXER.RecoveryIndexError,
                    "output-volume-is-not-admitted",
                ):
                    INDEXER.build_index(store.root, output, verify_function=verify)
            self.assertFalse(verification_called)
            self.assertFalse(output.exists())
            self.assertEqual(list(parent.glob(".private-index.incoming-*")), [])

    def test_output_inside_another_git_checkout_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            checkout = parent / "checkout"
            checkout.mkdir(mode=0o700)
            (checkout / ".git").write_text("gitdir: synthetic\n")
            output = checkout / "private" / "recovered-index"
            output.parent.mkdir(mode=0o700)
            verification_called = False

            def verify(_path: Path) -> dict[str, object]:
                nonlocal verification_called
                verification_called = True
                return store.verified

            with mock.patch.object(
                INDEXER, "_require_enforced_volume_ownership"
            ) as admitted:
                with self.assertRaisesRegex(
                    INDEXER.RecoveryIndexError,
                    "output-must-be-outside-any-git-checkout",
                ):
                    INDEXER.build_index(store.root, output, verify_function=verify)
            admitted.assert_not_called()
            self.assertFalse(verification_called)
            self.assertFalse(output.exists())

    def test_inherited_acl_on_staging_is_rejected_before_store_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "private-index"
            verification_called = False

            def verify(_path: Path) -> dict[str, object]:
                nonlocal verification_called
                verification_called = True
                return store.verified

            with (
                mock.patch.object(INDEXER, "_require_enforced_volume_ownership"),
                mock.patch.object(INDEXER, "_has_extended_acl", return_value=True),
            ):
                with self.assertRaisesRegex(
                    INDEXER.RecoveryIndexError,
                    "private-output-inherits-extended-acl",
                ):
                    INDEXER.build_index(store.root, output, verify_function=verify)
            self.assertFalse(verification_called)
            self.assertFalse(output.exists())
            self.assertEqual(list(parent.glob(".private-index.incoming-*")), [])

    def test_journal_bytes_must_match_the_verified_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            store = SyntheticStore(parent / "store")
            output = parent / "private-index"
            changed = dict(store.events[0])
            changed["synthetic_mutation"] = True
            mutated_journal = b"".join(
                INDEXER.canonical_json(event)
                for event in [changed, store.events[1]]
            )
            write_private(store.root / "journal.jsonl", mutated_journal)

            with admitted_private_output():
                with self.assertRaisesRegex(
                    INDEXER.RecoveryIndexError,
                    "journal-changed-after-verification",
                ):
                    INDEXER.build_index(
                        store.root,
                        output,
                        verify_function=lambda _path: store.verified,
                    )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
