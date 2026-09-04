from __future__ import annotations

import json
import base64
import gzip
import hashlib
import io
import os
import plistlib
import random
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
import zlib
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import capture_delivery_evidence as capture  # noqa: E402
import verify_delivery_evidence as verify  # noqa: E402

MAC_USERS_ROOT = "/" + "Users"
POSIX_HOME_ROOT = "/" + "home"
PRIVATE_TMP_ROOT = "/" + "private/tmp"
PRIVATE_VAR_FOLDERS_ROOT = "/" + "private/var/folders"
VAR_TMP_ROOT = "/" + "var/tmp"
ROOT_HOME = "/" + "root"
VOLUMES_ROOT = "/" + "Volumes"
SYSTEM_DATA_VOLUME = "/" + "System/Volumes/Data"
MNT_ROOT = "/" + "mnt"
NETWORK_SERVERS_ROOT = "/" + "Network/Servers"
PRIVATE_KEY_HEADER = "-----BEGIN " + "PRIVATE KEY-----"
ENCRYPTED_PRIVATE_KEY_HEADER = "-----BEGIN ENCRYPTED " + "PRIVATE KEY-----"
REAL_CAPTURE_VOLUME_BOUNDARY = capture._require_enforced_volume_ownership


def private_file(path: Path, raw: bytes) -> Path:
    # Test-only synthetic credential fixtures must reach the file scanner in
    # clear text; the owner-only temporary directory and mode check are the
    # behaviour under test, not application storage.
    # codeql[py/clear-text-storage-sensitive-data]
    path.write_bytes(raw)
    path.chmod(0o600)
    return path


def fake_clone(source: Path, destination: Path) -> None:
    shutil.copyfile(source, destination)


def apfs(_: Path) -> str:
    return "apfs"


class FakeGitHubClient:
    def __init__(self) -> None:
        self.downloads: list[str] = []
        self.json_requests: list[str] = []
        self.fail_downloads = False
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            entry = zipfile.ZipInfo("bounded.log", date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, "bounded synthetic assurance output\n")
        self.download_payload = output.getvalue()
        self.run = {
            "id": 101,
            "status": "completed",
            "conclusion": "success",
            "run_attempt": 3,
            "head_sha": "a" * 40,
            "head_commit": {"id": "a" * 40, "tree_id": "b" * 40},
            "run_started_at": "2026-08-30T08:00:00Z",
            "updated_at": "2026-08-30T08:05:00Z",
        }

    def json(self, endpoint: str, *, paginate: bool = False) -> object:
        self.json_requests.append(endpoint)
        if endpoint == "repos/acme/project":
            return {
                "id": 4242,
                "node_id": "R_4242",
                "full_name": "acme/project",
                "html_url": "https://github.com/acme/project",
                "private": True,
                "visibility": "private",
                "archived": False,
                "default_branch": "main",
                "created_at": "2026-08-01T00:00:00Z",
                "updated_at": "2026-08-30T08:05:00Z",
                "pushed_at": "2026-08-30T08:05:00Z",
            }
        if endpoint.endswith("artifact-and-log-retention"):
            return {"days": 90}
        if endpoint.startswith("repos/acme/project/actions/runs?"):
            return [
                {
                    "total_count": 2,
                    "workflow_runs": [
                        self.run,
                        {
                            "id": 102,
                            "status": "in_progress",
                            "run_attempt": 1,
                            "head_sha": "b" * 40,
                            "run_started_at": "2026-08-30T08:00:00Z",
                            "updated_at": "2026-08-30T08:05:00Z",
                        },
                    ]
                }
            ]
        if endpoint in {
            "repos/acme/project/actions/runs/101/attempts/1",
            "repos/acme/project/actions/runs/101/attempts/2",
        }:
            attempt = int(endpoint.rsplit("/", 1)[1])
            return {
                **self.run,
                "run_attempt": attempt,
                "run_started_at": f"2026-08-30T0{6 + attempt}:00:00Z",
                "updated_at": f"2026-08-30T0{6 + attempt}:05:00Z",
            }
        if "/jobs?" in endpoint:
            parts = endpoint.split("/")
            run_id = int(parts[5])
            attempt = int(parts[7])
            head_sha = "c" * 40 if run_id == 103 else "a" * 40
            return [
                {
                    "jobs": [
                        {
                            "id": 3,
                            "name": "assurance",
                            "conclusion": "success",
                            "run_id": run_id,
                            "run_attempt": attempt,
                            "head_sha": head_sha,
                        }
                    ]
                }
            ]
        if endpoint.endswith("/artifacts?per_page=100"):
            run_id = int(endpoint.split("/")[5])
            head_sha = "c" * 40 if run_id == 103 else "a" * 40
            return [
                {
                    "artifacts": [
                        {
                            "id": 201,
                            "name": "ci-impact-plan-a",
                            "size_in_bytes": len(self.download_payload),
                            "expired": False,
                            "created_at": "2026-08-30T08:01:00Z",
                            "expires_at": "2026-09-29T08:01:00Z",
                            "workflow_run": {
                                "id": run_id,
                                "repository_id": 4242,
                                "head_sha": head_sha,
                            },
                        },
                        {
                            "id": 202,
                            "name": "large-image",
                            "size_in_bytes": 5_000,
                            "expired": False,
                            "created_at": "2026-08-30T08:01:00Z",
                            "expires_at": "2026-11-28T08:01:00Z",
                            "workflow_run": {
                                "id": run_id,
                                "repository_id": 4242,
                                "head_sha": head_sha,
                            },
                        },
                    ]
                }
            ]
        if endpoint == "repos/acme/project/issues/108":
            return {
                "number": 108,
                "title": "Provider pack",
                "url": "https://api.github.com/repos/acme/project/issues/108",
                "repository_url": "https://api.github.com/repos/acme/project",
                "pull_request": {
                    "url": "https://api.github.com/repos/acme/project/pulls/108"
                },
            }
        if endpoint.endswith("/issues/108/comments?per_page=100"):
            return [
                [
                    {
                        "id": 501,
                        "issue_url": "https://api.github.com/repos/acme/project/issues/108",
                    }
                ]
            ]
        if endpoint == "repos/acme/project/pulls/108":
            return {
                "number": 108,
                "merged": True,
                "url": "https://api.github.com/repos/acme/project/pulls/108",
                "base": {"repo": {"id": 4242, "full_name": "acme/project"}},
            }
        if endpoint.endswith("/pulls/108/reviews?per_page=100"):
            return [
                [
                    {
                        "id": 601,
                        "pull_request_url": (
                            "https://api.github.com/repos/acme/project/pulls/108"
                        ),
                    }
                ]
            ]
        if endpoint.endswith("/pulls/108/comments?per_page=100"):
            return [
                [
                    {
                        "id": 701,
                        "pull_request_url": (
                            "https://api.github.com/repos/acme/project/pulls/108"
                        ),
                    }
                ]
            ]
        raise AssertionError(f"unexpected fake GitHub endpoint: {endpoint}")

    def download(self, endpoint: str, *, max_bytes: int) -> bytes:
        self.downloads.append(endpoint)
        if self.fail_downloads:
            raise capture.GitHubProviderUnavailableError("synthetic download failure")
        raw = self.download_payload
        if len(raw) > max_bytes:
            raise capture.EvidenceCaptureError("too large")
        return raw


class DeliveryEvidencePreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.store = self.root / "private-store"
        self.capture_volume_patch = mock.patch.object(
            capture,
            "_require_enforced_volume_ownership",
            return_value=None,
        )
        self.verify_volume_patch = mock.patch.object(
            verify,
            "_require_enforced_volume_ownership",
            return_value=None,
        )
        self.capture_volume_patch.start()
        self.verify_volume_patch.start()

    def tearDown(self) -> None:
        self.verify_volume_patch.stop()
        self.capture_volume_patch.stop()
        self.temporary.cleanup()

    def capture_file(self, path: Path, *, redacted: bool = False) -> dict[str, object]:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_local_file(
                store,
                path,
                trigger="feature-completed",
                repository=None,
                redacted_jsonl=redacted,
            )
            return store.summary()

    def journal(self) -> list[dict[str, object]]:
        return capture.read_journal(self.store / "journal.jsonl")

    def rewrite_journal(self, events: list[dict[str, object]]) -> None:
        previous: str | None = None
        for event in events:
            event["previous_event_sha256"] = previous
            core = dict(event)
            core.pop("event_sha256")
            event["event_sha256"] = hashlib.sha256(
                capture.JOURNAL_DOMAIN + capture.canonical_json(core)[:-1]
            ).hexdigest()
            previous = str(event["event_sha256"])
        journal_raw = b"".join(capture.canonical_json(event) for event in events)
        journal = self.store / "journal.jsonl"
        journal.write_bytes(journal_raw)
        journal.chmod(0o600)
        ledger = capture.build_expiry_ledger(events, journal_raw)
        ledger_path = self.store / "expiry-ledger.json"
        ledger_path.write_bytes(capture.canonical_json(ledger, pretty=True))
        ledger_path.chmod(0o600)

    def replace_event_object(self, event: dict[str, object], raw: bytes) -> None:
        item = event["objects"][0]
        old_digest = item["sha256"]
        old_path = self.store / "objects" / "sha256" / old_digest[:2] / old_digest
        new_digest = hashlib.sha256(raw).hexdigest()
        shard = self.store / "objects" / "sha256" / new_digest[:2]
        shard.mkdir(mode=0o700, exist_ok=True)
        shard.chmod(0o700)
        private_file(shard / new_digest, raw)
        if old_path != shard / new_digest:
            old_path.unlink()
        item["sha256"] = new_digest
        item["bytes"] = len(raw)

    def transaction_source(
        self,
        identity: str = "test:pending-event:one",
        raw: bytes = b"transaction-evidence",
    ) -> dict[str, object]:
        source_stat = {
            "device": 1,
            "inode": 2,
            "mode": 0o600,
            "links": 1,
            "owner_uid": os.getuid(),
            "bytes": len(raw),
            "mtime_ns": 4,
            "ctime_ns": 5,
        }
        path_digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        content_digest = hashlib.sha256(raw).hexdigest()
        return capture._source_value(
            kind="local-file",
            identity=(
                f"local-file:path-sha256:{path_digest}:device:1:inode:2:"
                f"mtime-ns:4:ctime-ns:5:bytes:{len(raw)}:"
                f"content-sha256:{content_digest}"
            ),
            label="pending-event.txt",
            occurred_at_utc=None,
            expires_at_utc=None,
            expiry_basis="unknown",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="none",
            snapshot_method="stable-byte-copy",
            source_stat_before=source_stat,
            source_stat_after=source_stat,
            source_changed_after_snapshot=False,
            collection_generation_sha256=None,
            collection_window=None,
            redaction_categories=[],
            redaction_count=0,
        )

    def interrupt_transaction(self, point: str) -> dict[str, object]:
        def inject(actual: str) -> None:
            if actual == point:
                raise RuntimeError(f"synthetic crash at {point}")

        with self.assertRaisesRegex(RuntimeError, f"synthetic crash at {point}"):
            with capture.private_umask(), capture.EvidenceStore(
                self.store,
                fault_injector=inject,
            ) as store:
                staged = capture.stage_bytes(
                    b"transaction-evidence",
                    store.incoming,
                    max_bytes=100,
                )
                store.commit_staged(
                    staged,
                    trigger="manual",
                    repository=None,
                    source=self.transaction_source(),
                    role="local-source",
                    media_type="text/plain; charset=utf-8",
                    opaque=False,
                    secret_scan="high-confidence-text-scan-passed",
                    secret_scan_performed=True,
                    sensitivity="owner-only-raw",
                    captured_at=datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc),
                )
        pending_path = self.store / capture.PENDING_EVENT_NAME
        self.assertTrue(pending_path.exists())
        pending = capture.parse_json(pending_path.read_bytes(), "test pending transaction")
        self.assertIsInstance(pending, dict)
        return pending

    def assert_transaction_recovers_once(self) -> dict[str, object]:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual(1, store.summary()["journal_events"])
        self.assertFalse((self.store / capture.PENDING_EVENT_NAME).exists())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        events = self.journal()
        self.assertEqual(1, len(events))
        digest = events[0]["objects"][0]["sha256"]
        final = self.store / "objects" / "sha256" / digest[:2] / digest
        self.assertEqual(b"transaction-evidence", final.read_bytes())
        self.assertEqual(1, final.stat().st_nlink)
        self.assertTrue(verify.verify_store(self.store)["verified"])
        return events[0]

    def test_local_capture_is_private_content_addressed_and_idempotent(self) -> None:
        source = private_file(self.root / "result.txt", b"bounded result\n")
        first = self.capture_file(source)
        second = self.capture_file(source)

        self.assertEqual(1, first["captured"])
        self.assertEqual(0, second["captured"])
        self.assertEqual(1, second["no_op"])
        events = self.journal()
        self.assertEqual(1, len(events))
        digest = events[0]["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest
        self.assertEqual(b"bounded result\n", object_path.read_bytes())
        self.assertEqual(0o700, stat.S_IMODE(self.store.stat().st_mode))
        self.assertEqual(0o600, stat.S_IMODE(object_path.stat().st_mode))
        result = verify.verify_store(self.store)
        self.assertTrue(result["verified"])
        self.assertEqual(capture.BOUNDARIES, result["boundaries"])

    def test_noowners_macos_volume_is_rejected_for_private_store(self) -> None:
        disk = subprocess.CompletedProcess(
            args=["/bin/df"],
            returncode=0,
            stdout=(
                "Filesystem 512-blocks Used Available Capacity Mounted on\n"
                f"/dev/disk6s1 100 1 99 1% {VOLUMES_ROOT}/External\n"
            ).encode(),
            stderr=b"",
        )
        mounts = subprocess.CompletedProcess(
            args=["/sbin/mount"],
            returncode=0,
            stdout=(
                f"/dev/disk6s1 on {VOLUMES_ROOT}/External "
                "(apfs, local, journaled, noowners)\n"
            ).encode(),
            stderr=b"",
        )
        with (
            mock.patch.object(capture.sys, "platform", "darwin"),
            mock.patch.object(capture.subprocess, "run", side_effect=[disk, mounts]),
            self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "does not enforce ownership",
            ),
        ):
            REAL_CAPTURE_VOLUME_BOUNDARY(Path(f"{VOLUMES_ROOT}/External"))

    def test_external_macos_device_is_rejected_even_at_nonstandard_mount(self) -> None:
        disk = subprocess.CompletedProcess(
            args=["/bin/df"],
            returncode=0,
            stdout=(
                b"Filesystem 512-blocks Used Available Capacity Mounted on\n"
                b"/dev/disk6s1 100 1 99 1% /PrivateEvidence\n"
            ),
            stderr=b"",
        )
        mounts = subprocess.CompletedProcess(
            args=["/sbin/mount"],
            returncode=0,
            stdout=b"/dev/disk6s1 on /PrivateEvidence (apfs, local, journaled)\n",
            stderr=b"",
        )
        info = subprocess.CompletedProcess(
            args=["/usr/sbin/diskutil"],
            returncode=0,
            stdout=plistlib.dumps(
                {
                    "MountPoint": "/PrivateEvidence",
                    "DeviceNode": "/dev/disk6s1",
                    "DeviceIdentifier": "disk6s1",
                    "GlobalPermissionsEnabled": True,
                    "Internal": False,
                    "RemovableMediaOrExternalDevice": True,
                    "Ejectable": True,
                    "Encryption": True,
                    "FileVault": False,
                }
            ),
            stderr=b"",
        )
        with (
            mock.patch.object(capture.sys, "platform", "darwin"),
            mock.patch.object(capture.subprocess, "run", side_effect=[disk, mounts, info]),
            self.assertRaisesRegex(capture.EvidenceCaptureError, "not an attested internal"),
        ):
            REAL_CAPTURE_VOLUME_BOUNDARY(Path("/PrivateEvidence"))

    def test_internal_filevault_macos_device_is_accepted(self) -> None:
        disk = subprocess.CompletedProcess(
            args=["/bin/df"],
            returncode=0,
            stdout=(
                "Filesystem 512-blocks Used Available Capacity Mounted on\n"
                f"/dev/disk3s5 100 1 99 1% {SYSTEM_DATA_VOLUME}\n"
            ).encode(),
            stderr=b"",
        )
        mounts = subprocess.CompletedProcess(
            args=["/sbin/mount"],
            returncode=0,
            stdout=(
                f"/dev/disk3s5 on {SYSTEM_DATA_VOLUME} "
                "(apfs, local, journaled, nobrowse)\n"
            ).encode(),
            stderr=b"",
        )
        info = subprocess.CompletedProcess(
            args=["/usr/sbin/diskutil"],
            returncode=0,
            stdout=plistlib.dumps(
                {
                    "MountPoint": SYSTEM_DATA_VOLUME,
                    "DeviceNode": "/dev/disk3s5",
                    "DeviceIdentifier": "disk3s5",
                    "GlobalPermissionsEnabled": True,
                    "Internal": True,
                    "RemovableMediaOrExternalDevice": False,
                    "Ejectable": False,
                    "Encryption": True,
                    "FileVault": True,
                }
            ),
            stderr=b"",
        )
        with (
            mock.patch.object(capture.sys, "platform", "darwin"),
            mock.patch.object(capture.subprocess, "run", side_effect=[disk, mounts, info]),
        ):
            REAL_CAPTURE_VOLUME_BOUNDARY(Path(f"{SYSTEM_DATA_VOLUME}/private-store"))

    def test_pending_transaction_recovers_exact_partial_journal_event(self) -> None:
        pending = self.interrupt_transaction("after-journal-prefix")
        journal_raw = (self.store / "journal.jsonl").read_bytes()
        offset = pending["journal_before"]["bytes"]
        suffix = journal_raw[offset:]
        event_raw = capture.canonical_json(pending["events"][0])
        self.assertTrue(suffix)
        self.assertNotEqual(event_raw, suffix)
        self.assertTrue(event_raw.startswith(suffix))

        recovered = self.assert_transaction_recovers_once()
        self.assertEqual(
            pending["events"][0]["event_sha256"],
            recovered["event_sha256"],
        )

    def test_pending_transaction_recovers_link_before_staged_unlink(self) -> None:
        pending = self.interrupt_transaction("after-object-link")
        binding = pending["objects"][0]
        staged = self.store / ".incoming" / binding["staged_name"]
        final = self.store / binding["final_relative_path"]
        self.assertEqual(staged.stat().st_ino, final.stat().st_ino)
        self.assertEqual(2, staged.stat().st_nlink)
        self.assertEqual(2, final.stat().st_nlink)

        self.assert_transaction_recovers_once()

    def test_pending_transaction_recovers_unlink_before_journal(self) -> None:
        pending = self.interrupt_transaction("after-staged-unlink")
        binding = pending["objects"][0]
        staged = self.store / ".incoming" / binding["staged_name"]
        final = self.store / binding["final_relative_path"]
        self.assertFalse(staged.exists())
        self.assertEqual(1, final.stat().st_nlink)
        self.assertEqual(b"", (self.store / "journal.jsonl").read_bytes())

        self.assert_transaction_recovers_once()

    def test_pending_transaction_recovers_journal_before_ledger_without_replay(self) -> None:
        pending = self.interrupt_transaction("after-journal-append")
        journal_before = (self.store / "journal.jsonl").read_bytes()
        self.assertEqual(pending["events"], self.journal())
        ledger_before = capture.parse_json(
            (self.store / "expiry-ledger.json").read_bytes(),
            "test expiry ledger",
        )
        self.assertNotEqual(capture.sha256_bytes(journal_before), ledger_before["journal_sha256"])

        self.assert_transaction_recovers_once()
        self.assertEqual(journal_before, (self.store / "journal.jsonl").read_bytes())

    def test_pending_transaction_rejects_unprovable_partial_journal(self) -> None:
        self.interrupt_transaction("after-journal-prefix")
        journal = self.store / "journal.jsonl"
        tampered = journal.read_bytes()[:-1] + b"!"
        journal.write_bytes(tampered)
        journal.chmod(0o600)

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "unprovable partial"):
            with capture.private_umask(), capture.EvidenceStore(self.store):
                pass
        self.assertEqual(tampered, journal.read_bytes())
        self.assertTrue((self.store / capture.PENDING_EVENT_NAME).exists())

    def test_pending_transaction_does_not_accept_unknown_incoming(self) -> None:
        pending = self.interrupt_transaction("after-object-link")
        unknown = private_file(self.store / ".incoming" / "not-recognised", b"unknown")
        binding = pending["objects"][0]
        staged = self.store / ".incoming" / binding["staged_name"]
        final = self.store / binding["final_relative_path"]

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "unknown incoming"):
            with capture.private_umask(), capture.EvidenceStore(self.store):
                pass
        self.assertEqual(2, staged.stat().st_nlink)
        self.assertEqual(2, final.stat().st_nlink)
        unknown.unlink()
        self.assert_transaction_recovers_once()

    def test_pending_transaction_rejects_final_inode_substitution(self) -> None:
        pending = self.interrupt_transaction("after-staged-unlink")
        binding = pending["objects"][0]
        final = self.store / binding["final_relative_path"]
        original_inode = final.stat().st_ino
        replacement = private_file(
            final.with_name(f"{final.name}.replacement"), b"transaction-evidence"
        )
        self.assertNotEqual(original_inode, replacement.stat().st_ino)
        os.replace(replacement, final)
        self.assertNotEqual(original_inode, final.stat().st_ino)

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "inode binding"):
            with capture.private_umask(), capture.EvidenceStore(self.store):
                pass
        self.assertTrue((self.store / capture.PENDING_EVENT_NAME).exists())
        self.assertEqual(b"", (self.store / "journal.jsonl").read_bytes())

    def test_pending_batch_recovers_crash_between_staged_items(self) -> None:
        def inject(point: str) -> None:
            if point == "after-staged-unlink":
                raise RuntimeError("synthetic crash between batch items")

        with self.assertRaisesRegex(RuntimeError, "crash between batch items"):
            with capture.private_umask(), capture.EvidenceStore(
                self.store,
                fault_injector=inject,
            ) as store:
                first = capture.stage_bytes(b"projection-one", store.incoming, max_bytes=100)
                second = capture.stage_bytes(
                    b"generation-manifest",
                    store.incoming,
                    max_bytes=100,
                )
                items = [
                    capture.StagedCapture(
                        staged=first,
                        trigger="pre-compaction",
                        repository=None,
                        source=self.transaction_source(
                            "test:pending-batch:projection", b"projection-one"
                        ),
                        role="local-source",
                        media_type="text/plain; charset=utf-8",
                        opaque=False,
                        secret_scan="high-confidence-text-scan-passed",
                        secret_scan_performed=True,
                        sensitivity="owner-only-raw",
                    ),
                    capture.StagedCapture(
                        staged=second,
                        trigger="pre-compaction",
                        repository=None,
                        source=self.transaction_source(
                            "test:pending-batch:manifest", b"generation-manifest"
                        ),
                        role="local-source",
                        media_type="application/json",
                        opaque=False,
                        secret_scan="high-confidence-text-scan-passed",
                        secret_scan_performed=True,
                        sensitivity="owner-only-raw",
                    ),
                ]
                store.commit_staged_batch(items)

        pending_path = self.store / capture.PENDING_EVENT_NAME
        pending = capture.parse_json(pending_path.read_bytes(), "test pending batch")
        self.assertEqual(2, len(pending["events"]))
        first_binding, second_binding = pending["objects"]
        self.assertFalse(
            (self.store / ".incoming" / first_binding["staged_name"]).exists()
        )
        self.assertTrue(
            (self.store / ".incoming" / second_binding["staged_name"]).exists()
        )
        self.assertTrue((self.store / first_binding["final_relative_path"]).exists())
        self.assertFalse((self.store / second_binding["final_relative_path"]).exists())

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual(2, store.summary()["journal_events"])
        events = self.journal()
        self.assertEqual([0, 1], [event["sequence"] for event in events])
        self.assertEqual(events[0]["event_sha256"], events[1]["previous_event_sha256"])
        self.assertFalse(pending_path.exists())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_immutable_source_identity_collision_fails_closed(self) -> None:
        source_value = capture._source_value(
            kind="test",
            identity="immutable:test:one",
            label="test",
            occurred_at_utc=None,
            expires_at_utc=None,
            expiry_basis="unknown",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="none",
            snapshot_method="stable-byte-copy",
            source_stat_before={
                "device": 1,
                "inode": 2,
                "mode": 0o600,
                "links": 1,
                "owner_uid": os.getuid(),
                "bytes": 3,
                "mtime_ns": 4,
                "ctime_ns": 5,
            },
            source_stat_after={
                "device": 1,
                "inode": 2,
                "mode": 0o600,
                "links": 1,
                "owner_uid": os.getuid(),
                "bytes": 3,
                "mtime_ns": 4,
                "ctime_ns": 5,
            },
            source_changed_after_snapshot=False,
            collection_generation_sha256=None,
            collection_window=None,
            redaction_categories=[],
            redaction_count=0,
        )
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            first = capture.stage_bytes(b"one", store.incoming, max_bytes=20)
            store.commit_staged(
                first,
                trigger="manual",
                repository=None,
                source=source_value,
                role="test",
                media_type="text/plain; charset=utf-8",
                opaque=False,
                secret_scan="not-performed",
                secret_scan_performed=False,
                sensitivity="owner-only-raw",
            )
            second = capture.stage_bytes(b"two", store.incoming, max_bytes=20)
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "conflicting evidence"):
                store.commit_staged(
                    second,
                    trigger="manual",
                    repository=None,
                    source=source_value,
                    role="test",
                    media_type="text/plain; charset=utf-8",
                    opaque=False,
                    secret_scan="not-performed",
                    secret_scan_performed=False,
                    sensitivity="owner-only-raw",
                )

    def test_secret_is_excluded_without_copying_its_value(self) -> None:
        secret = "sk-proj-" + "A" * 32
        source = private_file(self.root / "secret.log", f"token={secret}\n".encode())
        summary = self.capture_file(source)
        self.assertEqual(1, summary["excluded"])
        self.assertEqual(0, summary["captured"])
        journal = (self.store / "journal.jsonl").read_text(encoding="utf-8")
        self.assertNotIn(secret, journal)
        self.assertIn("secret-category:openai-token", journal)
        self.assertEqual([], list((self.store / "objects" / "sha256").rglob("?" * 64)))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_local_same_size_restored_mtime_mutation_is_a_new_source(self) -> None:
        source = private_file(self.root / "mutable.txt", b"first-value")
        original = source.stat()
        self.capture_file(source)
        source.write_bytes(b"other-value")
        source.chmod(0o600)
        os.utime(source, ns=(original.st_atime_ns, original.st_mtime_ns))
        self.capture_file(source)

        events = self.journal()
        self.assertEqual(2, len(events))
        self.assertNotEqual(
            events[0]["source"]["identity"],
            events[1]["source"]["identity"],
        )
        self.assertNotEqual(
            events[0]["objects"][0]["sha256"],
            events[1]["objects"][0]["sha256"],
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_store_enforces_batch_bytes_and_free_space_before_install(self) -> None:
        source = private_file(self.root / "bounded.txt", b"four")
        with capture.private_umask(), capture.EvidenceStore(
            self.store,
            max_capture_bytes=3,
        ) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "byte boundary"):
                capture.capture_local_file(
                    store,
                    source,
                    trigger="daily-safety-sweep",
                    repository=None,
                )
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertEqual([], self.journal())

        usage = shutil._ntuple_diskusage(total=10, used=10, free=0)
        with mock.patch.object(capture.shutil, "disk_usage", return_value=usage):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "free-space"):
                    capture.capture_local_file(
                        store,
                        source,
                        trigger="daily-safety-sweep",
                        repository=None,
                    )
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertEqual([], self.journal())

    def test_store_bounds_object_free_events_and_metadata_growth(self) -> None:
        source_one = self.transaction_source("test:object-free:one")
        source_two = self.transaction_source("test:object-free:two")
        with mock.patch.object(capture, "MAX_CAPTURE_EVENTS", 1):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                store.record_without_object(
                    trigger="daily-safety-sweep",
                    repository=None,
                    source=source_one,
                    status_value="unavailable",
                    reason="synthetic-unavailable",
                )
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "event boundary"):
                    store.record_without_object(
                        trigger="daily-safety-sweep",
                        repository=None,
                        source=source_two,
                        status_value="unavailable",
                        reason="synthetic-unavailable",
                    )
        self.assertEqual(1, len(self.journal()))

        metadata_store = self.root / "metadata-store"
        with mock.patch.object(capture, "MAX_CAPTURE_METADATA_BYTES", 1):
            with capture.private_umask(), capture.EvidenceStore(metadata_store) as store:
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "metadata byte"):
                    store.record_without_object(
                        trigger="daily-safety-sweep",
                        repository=None,
                        source=source_one,
                        status_value="unavailable",
                        reason="synthetic-unavailable",
                    )
        self.assertEqual([], capture.read_journal(metadata_store / "journal.jsonl"))

        reserve_store = self.root / "reserve-store"
        with capture.private_umask(), capture.EvidenceStore(reserve_store):
            pass
        usage = shutil._ntuple_diskusage(
            total=capture.MIN_STORE_FREE_BYTES + 1,
            used=0,
            free=capture.MIN_STORE_FREE_BYTES + 1,
        )
        with mock.patch.object(capture.shutil, "disk_usage", return_value=usage):
            with capture.private_umask(), capture.EvidenceStore(reserve_store) as store:
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "free-space"):
                    store.record_without_object(
                        trigger="daily-safety-sweep",
                        repository=None,
                        source=source_one,
                        status_value="unavailable",
                        reason="synthetic-unavailable",
                    )
        self.assertEqual([], capture.read_journal(reserve_store / "journal.jsonl"))

    def test_explicit_redacted_jsonl_is_structurally_checked(self) -> None:
        source = private_file(self.root / "redacted.jsonl", b'{"redacted":true,"text":"ok"}\n')
        self.capture_file(source, redacted=True)
        event = self.journal()[0]
        self.assertEqual(
            "operator-supplied-redacted-jsonl-not-attested",
            event["source"]["redaction_mode"],
        )
        self.assertEqual("owner-only-redacted", event["objects"][0]["sensitivity"])
        self.assertFalse(event["objects"][0]["public_projection_eligible"])

        malformed = private_file(self.root / "malformed.jsonl", b"[]\n")
        with self.assertRaisesRegex(capture.EvidenceCaptureError, "must be an object"):
            self.capture_file(malformed, redacted=True)

    def test_verifier_rejects_self_consistent_local_metadata_substitution(self) -> None:
        source = private_file(self.root / "bounded.txt", b"bounded local evidence\n")
        self.capture_file(source)
        original = self.journal()[0]

        def mutate_kind(event):
            event["source"]["kind"] = "invented-source-kind"

        def mutate_role(event):
            event["objects"][0]["role"] = "invented-role"

        def mutate_scan(event):
            event["objects"][0]["secret_scan"] = "invented-scan-claim"

        def mutate_scan_marker(event):
            event["objects"][0]["secret_scan_performed"] = False

        def mutate_redaction(event):
            event["source"]["redaction_mode"] = "invented-redaction-mode"

        for label, mutate in (
            ("kind", mutate_kind),
            ("role", mutate_role),
            ("scan", mutate_scan),
            ("scan-marker", mutate_scan_marker),
            ("redaction", mutate_redaction),
        ):
            with self.subTest(label=label):
                event = json.loads(json.dumps(original))
                mutate(event)
                self.rewrite_journal([event])
                with self.assertRaises(verify.EvidenceVerificationError):
                    verify.verify_store(self.store)

    def test_source_link_hardlink_and_special_file_are_rejected(self) -> None:
        source = private_file(self.root / "source.txt", b"safe")
        symbolic = self.root / "symbolic.txt"
        symbolic.symlink_to(source)
        with self.assertRaises(capture.EvidenceCaptureError):
            self.capture_file(symbolic)
        hard = self.root / "hard.txt"
        os.link(source, hard)
        with self.assertRaisesRegex(capture.EvidenceCaptureError, "hard linked"):
            self.capture_file(hard)
        fifo = self.root / "fifo"
        os.mkfifo(fifo, 0o600)
        with self.assertRaises(capture.EvidenceCaptureError):
            self.capture_file(fifo)

    def test_byte_copy_detects_source_change_during_capture(self) -> None:
        source = private_file(self.root / "changing.txt", b"before")
        incoming = self.root / "incoming"
        incoming.mkdir(mode=0o700)

        def mutate() -> None:
            source.write_bytes(b"after-longer")

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "changed while"):
            capture.stage_regular_file(source, incoming, after_read_hook=mutate)
        self.assertEqual([], list(incoming.iterdir()))

    def test_byte_copy_detects_same_size_restored_mtime_change(self) -> None:
        source = private_file(self.root / "changing-same-size.txt", b"before")
        original = source.stat()
        incoming = self.root / "incoming-same-size"
        incoming.mkdir(mode=0o700)

        def mutate() -> None:
            source.write_bytes(b"after!")
            source.chmod(0o600)
            os.utime(source, ns=(original.st_atime_ns, original.st_mtime_ns))

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "changed while"):
            capture.stage_regular_file(source, incoming, after_read_hook=mutate)
        self.assertEqual([], list(incoming.iterdir()))

    def test_apfs_clone_capture_accepts_0644_owner_source_and_records_mutation(self) -> None:
        source = self.root / "rollout.jsonl"
        source.write_bytes(b'{"type":"session_meta"}\nraw\n')
        source.chmod(0o644)
        incoming = self.root / "incoming"
        incoming.mkdir(mode=0o700)

        def mutate() -> None:
            source.write_bytes(source.read_bytes() + b"later\n")

        result = capture.stage_apfs_clone(
            source,
            incoming,
            clone_function=fake_clone,
            filesystem_type_function=apfs,
            after_clone_hook=mutate,
        )
        self.assertTrue(result.source_changed_after_snapshot)
        self.assertEqual(b'{"type":"session_meta"}\nraw\n', result.staged.path.read_bytes())
        self.assertEqual(0o600, stat.S_IMODE(result.staged.path.stat().st_mode))

    def test_apfs_clone_has_no_silent_non_apfs_copy_fallback(self) -> None:
        source = private_file(self.root / "rollout.jsonl", b"raw")
        incoming = self.root / "incoming"
        incoming.mkdir(mode=0o700)
        invoked = False

        def unexpected_clone(_: Path, __: Path) -> None:
            nonlocal invoked
            invoked = True

        with self.assertRaisesRegex(capture.EvidenceCaptureError, "requires APFS"):
            capture.stage_apfs_clone(
                source,
                incoming,
                clone_function=unexpected_clone,
                filesystem_type_function=lambda _: "ext4",
            )
        self.assertFalse(invoked)

    def test_codex_closure_preserves_only_redacted_user_visible_projection(self) -> None:
        sessions = self.root / "sessions"
        sessions.mkdir(mode=0o700)

        def rollout(
            name: str,
            thread: str,
            parent: str | None,
            records: list[dict[str, object]],
        ) -> None:
            payload = {
                "id": thread,
                "session_id": thread,
                "timestamp": "2026-08-30T08:00:00Z",
                "cli_version": "1.2.3",
            }
            if parent is not None:
                payload["source"] = {
                    "subagent": {
                        "thread_spawn": {
                            "parent_thread_id": parent,
                            "depth": 1,
                            "agent_path": ["root", "child"],
                        }
                    }
                }
            values = [
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": payload,
                },
                *records,
            ]
            path = sessions / name
            path.write_text(
                "".join(json.dumps(value) + "\n" for value in values),
                encoding="utf-8",
            )
            path.chmod(0o644)

        secret = "sk-proj-" + "A" * 32
        rollout(
            "root.jsonl",
            "root-thread",
            None,
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "INJECTED RESPONSE USER CONTEXT"}
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "phase": "commentary",
                        "content": [
                            {"type": "output_text", "text": "DUPLICATE RESPONSE ASSISTANT"}
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "phase": "analysis",
                        "content": [{"type": "output_text", "text": "HIDDEN ANALYSIS MESSAGE"}],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "reasoning",
                        "summary": "HIDDEN REASONING SUMMARY",
                        "encrypted_content": "HIDDEN ENCRYPTED STATE",
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "mcp_tool_call_end",
                        "call_id": "call-1",
                        "duration": 42,
                        "invocation": {
                            "server": "evidence",
                            "tool": "bounded_check",
                            "arguments": {
                                "token": secret,
                                "oauth": (
                                    "https://user:password@example.invalid/callback"
                                    "?code=ABCDEFGHIJKLMN123456"
                                ),
                                "file_path": f"{MAC_USERS_ROOT}/person/private/input.txt",
                                "client_id": "raw-client-id",
                                "input_image": "data:image/png;base64,RAW-IMAGE",
                                "configuration": "api_key=UNQUOTEDSECRET1234567890",
                                "client_secret": "abcdefghijklmnopqrstuv",
                                "api_key": "zyxwvutsrqponmlkjihgfe",
                                "nested_json": json.dumps(
                                    {"repositoryCredential": "nested-secret-value"}
                                ),
                            },
                        },
                        "result": {
                            "output": "visible bounded tool result",
                            "_meta": {"browser_state": "HIDDEN HOST STATE"},
                            "sas": "https://example.invalid/blob?sig=AbCdEfGhIjKlMnOpQrStUv%2F%3D",
                            "siwc_bypass_bearer_token": "bearer-secret-value",
                            "image_url": "data:image/png;base64,RAW-RESULT-IMAGE",
                        },
                        "unexpected": "UNSUPPORTED MCP FIELD",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call-1",
                        "output": [
                            {
                                "type": "output_text",
                                "text": "UNSUPPORTED LEGACY TOOL BODY",
                            }
                        ],
                    },
                },
                {"type": "world_state", "payload": {"value": "HIDDEN WORLD STATE"}},
                {"type": "turn_context", "payload": {"value": "HIDDEN TURN CONTEXT"}},
                {"type": "compacted", "payload": {"value": "HIDDEN COMPACTED BODY"}},
                {
                    "type": "event_msg",
                    "payload": {"type": "agent_reasoning", "text": "HIDDEN EVENT REASONING"},
                },
                {
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "visible user request"},
                },
                {
                    "type": "event_msg",
                    "payload": {"type": "agent_message", "message": "visible commentary"},
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "last_token_usage": {"total_tokens": 123, "secret": 456},
                            "model_context_window": 272000,
                        },
                        "rate_limits": {
                            "primary": {
                                "used_percent": 12.5,
                                "resets_at": 123456,
                                "limit_id": "raw-limit-id",
                            },
                            "plan_type": "pro",
                        },
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {"type": "unknown_future_event", "secret_field": "UNSUPPORTED BODY"},
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "agent_message",
                        "author": "root",
                        "recipient": "child",
                        "content": [
                            {"type": "input_text", "text": "visible inter-agent status"},
                            {"type": "output_text", "text": "HIDDEN INTER-AGENT OUTPUT"},
                        ],
                        "encrypted_content": "HIDDEN INTER-AGENT ENCRYPTED CONTENT",
                    },
                },
            ],
        )
        rollout(
            "child.jsonl",
            "child-thread",
            "root-thread",
            [
                {
                    "type": "event_msg",
                    "payload": {"type": "agent_message", "message": "visible child final"},
                }
            ],
        )
        rollout("other.jsonl", "other-thread", None, [])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            count = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
            self.assertEqual(2, count)
        events = self.journal()
        self.assertEqual(3, len(events))
        projections = [
            event
            for event in events
            if event["source"]["kind"] == "codex-user-visible-projection"
        ]
        manifests = [
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        ]
        self.assertEqual(2, len(projections))
        self.assertEqual(1, len(manifests))
        self.assertTrue(
            all(event["objects"][0]["secret_scan_performed"] is True for event in projections)
        )
        self.assertTrue(
            all(event["objects"][0]["sensitivity"] == "owner-only-redacted" for event in events)
        )
        self.assertTrue(
            all(event["objects"][0]["public_projection_eligible"] is False for event in events)
        )

        projected_raw = b""
        for event in projections:
            digest = event["objects"][0]["sha256"]
            object_path = self.store / "objects" / "sha256" / digest[:2] / digest
            projected_raw += gzip.decompress(object_path.read_bytes())
        projected_text = projected_raw.decode("utf-8")
        self.assertIn("visible user request", projected_text)
        self.assertIn("visible commentary", projected_text)
        self.assertIn("visible child final", projected_text)
        self.assertIn("bounded_check", projected_text)
        self.assertIn("visible bounded tool result", projected_text)
        self.assertIn("visible inter-agent status", projected_text)
        self.assertIn('"total_tokens":123', projected_text)
        self.assertIn("https://example.invalid/callback", projected_text)
        self.assertNotIn(secret, projected_text)
        self.assertIn("X" * len(secret), projected_text)
        self.assertNotIn("user:password", projected_text)
        self.assertNotIn("?code=", projected_text)
        self.assertNotIn("ABCDEFGHIJKLMN123456", projected_text)
        self.assertNotIn("AbCdEfGhIjKlMnOpQrStUv%2F%3D", projected_text)
        self.assertNotIn("UNQUOTEDSECRET1234567890", projected_text)
        self.assertNotIn("abcdefghijklmnopqrstuv", projected_text)
        self.assertNotIn("zyxwvutsrqponmlkjihgfe", projected_text)
        self.assertNotIn("nested-secret-value", projected_text)
        self.assertNotIn("bearer-secret-value", projected_text)
        self.assertNotIn(f"{MAC_USERS_ROOT}/person/private/input.txt", projected_text)
        self.assertNotIn("raw-client-id", projected_text)
        self.assertEqual(1, projected_text.count("visible user request"))
        self.assertIn("unsupported-rollout-record", projected_text)
        for hidden in (
            "INJECTED RESPONSE USER CONTEXT",
            "DUPLICATE RESPONSE ASSISTANT",
            "HIDDEN ANALYSIS MESSAGE",
            "HIDDEN REASONING SUMMARY",
            "HIDDEN ENCRYPTED STATE",
            "HIDDEN WORLD STATE",
            "HIDDEN TURN CONTEXT",
            "HIDDEN COMPACTED BODY",
            "HIDDEN EVENT REASONING",
            "HIDDEN INTER-AGENT ENCRYPTED CONTENT",
            "HIDDEN INTER-AGENT OUTPUT",
            "HIDDEN HOST STATE",
            "RAW-IMAGE",
            "RAW-RESULT-IMAGE",
            "UNSUPPORTED LEGACY TOOL BODY",
            "UNSUPPORTED MCP FIELD",
            "UNSUPPORTED BODY",
        ):
            self.assertNotIn(hidden, projected_text)
        self.assertIn('"response_item:reasoning":1', projected_text)
        self.assertIn('"world_state":1', projected_text)

        manifest_digest = manifests[0]["objects"][0]["sha256"]
        manifest_path = self.store / "objects" / "sha256" / manifest_digest[:2] / manifest_digest
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(2, manifest["selected_file_count"])
        self.assertEqual(2, len(manifest["files"]))
        self.assertTrue(all(item["source_identity"] for item in manifest["files"]))
        self.assertTrue(verify.verify_store(self.store)["verified"])

        first_digests = [event["objects"][0]["sha256"] for event in events]
        projection_reads = 0

        def counted_clone(source_path: Path, destination: Path) -> None:
            nonlocal projection_reads
            projection_reads += 1
            shutil.copyfile(source_path, destination)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=counted_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(0, projection_reads)
        second_events = self.journal()
        self.assertEqual(3, len(second_events))
        self.assertEqual(first_digests, [event["objects"][0]["sha256"] for event in second_events])

        child = sessions / "child.jsonl"
        with child.open("a", encoding="utf-8") as stream:
            stream.write(
                json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "agent_message",
                            "message": "new child status",
                        },
                    }
                )
                + "\n"
            )
        projection_reads = 0
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="feature-completed",
                clone_function=counted_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(1, projection_reads)
        self.assertEqual(5, len(self.journal()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_structured_secret_fields_are_redacted_before_filesystem_write(self) -> None:
        secret_fields = {
            "password": "password-value",
            "pass-phrase": "passphrase-value",
            "Secret": "secret-value",
            "authToken": "token-value",
            "access-token": "access-value",
            "refreshToken": "refresh-value",
            "ID_TOKEN": "identity-value",
            "api.key": "api-value",
            "clientSecret": "client-value",
            "private-key": "private-value",
            "Authorization": "authorization-value",
            "bearer": "bearer-value",
            "cookie": "cookie-value",
            "session": "session-value",
            "JWT": "jwt-value",
            "repositoryCredential": "credential-value",
            "siwc_bypass_bearer_token": "nested-token-value",
            "secretField": "secret-field-value",
            "token_value": "token-field-value",
            "authorization_header": "authorisation-field-value",
        }
        value = {
            "outer": secret_fields,
            "encoded": json.dumps({"refresh_token": "json-string-value"}),
        }
        redacted_value, categories, count = capture._redact_codex_projection_value(value)
        serialised = capture.canonical_json(redacted_value)

        for key, secret in secret_fields.items():
            with self.subTest(key=key):
                self.assertNotIn(secret.encode(), serialised)
                self.assertEqual(
                    "X" * len(secret.encode()),
                    redacted_value["outer"][key],
                )
        self.assertNotIn(b"json-string-value", serialised)
        self.assertIn(b"X" * len(b"json-string-value"), serialised)
        self.assertEqual(["sensitive-key"], categories)
        self.assertEqual(len(secret_fields) + 1, count)

        path_value = {
            "user": f"read {MAC_USERS_ROOT}/private-person/secret.txt",
            "temporary": f"stored under {PRIVATE_TMP_ROOT}/private-capture/result.json",
            "resolved-temporary": (
                f"stored under {PRIVATE_VAR_FOLDERS_ROOT}/aa/private/result.json"
            ),
            "var-temporary": f"stored under {VAR_TMP_ROOT}/private/result.json",
            "home": f"opened {POSIX_HOME_ROOT}/private-person/config.json",
            "root": f"opened {ROOT_HOME}/private/config.json",
            "tilde": "opened ~/private/config.json",
            "windows": r"opened C:\Users\private-person\secret.txt",
        }
        redacted_paths, path_categories, path_count = (
            capture._redact_codex_projection_value(path_value)
        )
        path_text = json.dumps(redacted_paths, sort_keys=True)
        self.assertNotIn("private-person", path_text)
        self.assertEqual(["local-path"], path_categories)
        self.assertEqual(8, path_count)

        stateless = (
            b"ghs_subject_abcdefghijklmnopqrstuvwxyz."
            b"abcdefghijklmnopqrstuvwxyz.abcdefghijklmnopqrstuvwxyz"
        )
        redacted_stateless, stateless_categories, stateless_count = (
            capture.redact_projection_bytes(stateless)
        )
        self.assertEqual(b"X" * len(stateless), redacted_stateless)
        self.assertEqual(["github-stateless-installation-token"], stateless_categories)
        self.assertEqual(1, stateless_count)
        full_pattern = dict(capture.FIXED_LENGTH_REDACTION_PATTERNS)[
            "github-stateless-installation-token"
        ]
        self.assertIsNotNone(full_pattern.search(stateless))
        self.assertIsNone(full_pattern.search(redacted_stateless))

    def test_embedded_hidden_state_and_oversized_json_are_not_retained(self) -> None:
        value = {
            "embedded": json.dumps(
                {
                    "developerInstructions": "HIDDEN-DEVELOPER",
                    "chainOfThought": "HIDDEN-THOUGHT",
                    "visible": "safe",
                }
            )
        }
        redacted, _, _ = capture._redact_codex_projection_value(value)
        serialised = capture.canonical_json(redacted)
        self.assertNotIn(b"HIDDEN-DEVELOPER", serialised)
        self.assertNotIn(b"HIDDEN-THOUGHT", serialised)
        self.assertIn(b"safe", serialised)
        self.assertTrue(
            verify._contains_excluded_projection_key(
                {"embedded": json.dumps({"developerInstructions": "forged"})}
            )
        )

        oversized = json.dumps(
            {
                "token": "UNPREFIXED-SECRET-VALUE",
                "padding": "x" * capture.MAX_CODEX_TEXT_BYTES,
            }
        )
        bounded = capture._bounded_codex_text(oversized)
        self.assertEqual("oversized-structured-text", bounded["reason"])
        self.assertNotIn("text", bounded)
        self.assertNotIn(b"UNPREFIXED-SECRET-VALUE", capture.canonical_json(bounded))

        malformed = '{"developerInstructions":"PRIVATE-INSTRUCTION-BODY"'
        malformed_redacted, _, _ = capture._redact_codex_projection_value(malformed)
        malformed_raw = capture.canonical_json(malformed_redacted)
        self.assertNotIn(b"PRIVATE-INSTRUCTION-BODY", malformed_raw)
        self.assertEqual("invalid-structured-text", malformed_redacted["reason"])
        self.assertTrue(verify._contains_excluded_projection_key(malformed))

        escaped_fragments = (
            '"developer\\u0049nstructions":"ESCAPED-CASE-HIDDEN"}',
            '"developer\\u005finstructions":"ESCAPED-UNDERSCORE-HIDDEN"}',
            '"developer\\/instructions":"ESCAPED-SLASH-HIDDEN"}',
        )
        for fragment in escaped_fragments:
            with self.subTest(fragment=fragment):
                bounded = capture._bounded_codex_text(fragment)
                self.assertIsInstance(bounded, dict)
                self.assertEqual("hidden-structured-field", bounded["reason"])
                self.assertNotIn("HIDDEN", json.dumps(bounded, sort_keys=True))
                self.assertTrue(verify._contains_excluded_projection_key(fragment))

        for fragment in (
            'prefix "password":"tiny"}',
            "password=tiny",
            "password: tiny",
            "api-key: tiny",
            "token: tiny",
            "client_secret: 'tiny'",
        ):
            with self.subTest(sensitive_fragment=fragment):
                redacted_fragment, categories, count = (
                    capture._redact_codex_projection_value(fragment)
                )
                self.assertEqual("sensitive-structured-field", redacted_fragment["reason"])
                self.assertNotIn("tiny", json.dumps(redacted_fragment, sort_keys=True))
                self.assertEqual(["sensitive-key"], categories)
                self.assertEqual(1, count)

        for fragment in (
            "developerInstructions: UNQUOTED-HIDDEN-ONE",
            "DeVeLoPeR.Instructions = UNQUOTED-HIDDEN-TWO",
            "chain-of-thought: UNQUOTED-HIDDEN-THREE",
            "system_message=UNQUOTED-HIDDEN-FOUR",
            "analysis: UNQUOTED-HIDDEN-FIVE",
        ):
            with self.subTest(hidden_assignment=fragment):
                redacted_fragment, _, _ = capture._redact_codex_projection_value(fragment)
                self.assertEqual("hidden-structured-field", redacted_fragment["reason"])
                self.assertNotIn("UNQUOTED", json.dumps(redacted_fragment, sort_keys=True))

        for hidden in (
            {"developerInstructions": "DOUBLE-HIDDEN"},
            {"pass" + "word": "DOUBLE-TINY"},
            {"client_" + "secret": "DOUBLE-CLIENT"},
        ):
            encoded = json.dumps(json.dumps(hidden))
            redacted_encoded, categories, count = capture._redact_codex_projection_value(encoded)
            self.assertEqual(
                "nested-sensitive-structured-text", redacted_encoded["reason"]
            )
            self.assertNotIn("DOUBLE", json.dumps(redacted_encoded, sort_keys=True))
            self.assertEqual(["sensitive-key"], categories)
            self.assertEqual(1, count)

        deep = "[" * 1_000 + "0" + "]" * 1_000
        redacted_deep, categories, count = capture._redact_codex_projection_value(deep)
        self.assertEqual("maximum-depth", redacted_deep["reason"])
        self.assertEqual(["maximum-depth"], categories)
        self.assertEqual(1, count)

        embedded_document: object = "safe"
        for level in reversed(range(5)):
            embedded_document = {f"level_{level}": embedded_document}
        wrapped_embedded = {
            "record": "projected-rollout-record",
            "source_type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": "call",
                "output": [
                    {
                        "type": "text",
                        "text": json.dumps(embedded_document, sort_keys=True),
                    }
                ],
            },
        }
        first_pass, first_categories, _ = capture._redact_codex_projection_value(
            wrapped_embedded
        )
        second_pass, second_categories, _ = capture._redact_codex_projection_value(
            first_pass
        )
        self.assertEqual(first_pass, second_pass)
        self.assertEqual([], first_categories)
        self.assertEqual([], second_categories)

        for path in (
            f"open {MAC_USERS_ROOT}/private-person/My Private Evidence/store/journal.jsonl",
            f"open {MAC_USERS_ROOT}/private-person/My\\ Private\\ Evidence/store/journal.jsonl",
            f"open {VOLUMES_ROOT}/PrivateEvidence/store/journal.jsonl",
            f"open {SYSTEM_DATA_VOLUME}{MAC_USERS_ROOT}/private-person/store/journal.jsonl",
            f"open {MNT_ROOT}/private/store/journal.jsonl",
            f"open {NETWORK_SERVERS_ROOT}/private/store/journal.jsonl",
            "open /opt/private/evidence-store/journal.jsonl",
            "open /Library/Application Support/Codex/session/events.jsonl",
            "open /srv/evidence/store/journal.jsonl",
            "open /usr/local/var/private/data/events.jsonl",
        ):
            sanitised, count = capture._sanitise_codex_local_paths_in_text(path)
            self.assertGreaterEqual(count, 1)
            self.assertNotIn("journal.jsonl", sanitised)

    def test_codex_text_key_classifier_matches_prior_semantics(self) -> None:
        def prior_classification(value: str) -> tuple[bool, bool]:
            hidden = False
            sensitive = False
            for match in capture._CODEX_JSON_KEY_FRAGMENT_PATTERN.finditer(value):
                try:
                    key = json.loads(match.group(1))
                except json.JSONDecodeError:
                    return True, True
                if not isinstance(key, str):
                    return True, True
                hidden = hidden or (
                    capture._normalise_codex_key(key)
                    in capture._CODEX_HIDDEN_KEY_NORMALISATIONS
                )
                sensitive = sensitive or capture._codex_key_is_sensitive(key)
            for match in capture._CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN.finditer(value):
                key = match.group(1)
                hidden = hidden or (
                    capture._normalise_codex_key(key)
                    in capture._CODEX_HIDDEN_KEY_NORMALISATIONS
                )
                sensitive = sensitive or capture._codex_key_is_sensitive(key)
            return hidden, sensitive

        adversarial = (
            'prefix "developer\\u0049nstructions":"hidden"}',
            'prefix "pass\\u0077ord":"tiny"}',
            'prefix "password":"tiny","analysis":"hidden"}',
            "developerInstructions: hidden",
            "DeVeLoPeR.Instructions = hidden",
            "password=tiny",
            "api-key: tiny",
            "client_secret: 'tiny'",
            'prefix "token_count":1,"session_id":"safe"}',
            'prefix "tokenCount":1,"token_usage":2,"sessionName":"safe"}',
            "token_count=1 session_id=safe",
            "ordinary prose without structural markers",
            'prefix "bad\nkey":"ambiguous"}',
            'prefix "unterminated\\u00ZZ":"ambiguous"}',
        )
        for value in adversarial:
            with self.subTest(value=value):
                expected = prior_classification(value)
                self.assertEqual(
                    expected,
                    capture._classify_codex_text_key_fragments(value),
                )
                with mock.patch.object(
                    capture,
                    "_classify_codex_text_key_fragments",
                    side_effect=prior_classification,
                ):
                    prior_projection = capture._redact_codex_projection_value(value)
                self.assertEqual(
                    prior_projection,
                    capture._redact_codex_projection_value(value),
                )

        generator = random.Random(20260831)
        fragments = (
            "visible",
            "token_count",
            "session_id",
            "password",
            "developerInstructions",
            '"analysis"',
            '"pass\\u0077ord"',
            ":",
            "=",
            " ",
            "-",
            "_",
            "tiny",
            "123",
            "{}",
        )
        for _ in range(1_000):
            value = "".join(
                generator.choice(fragments)
                for _ in range(generator.randint(1, 16))
            )
            self.assertEqual(
                prior_classification(value),
                capture._classify_codex_text_key_fragments(value),
            )

    def test_codex_oversized_structural_keys_fail_closed_at_exact_limits(self) -> None:
        quoted_key = "a" * (513 - len("token")) + "token"
        quoted = f'prefix "{quoted_key}":"TINY-QUOTED-CREDENTIAL"}}'
        quoted_redacted, quoted_categories, quoted_count = (
            capture._redact_codex_projection_value(quoted)
        )
        self.assertEqual("sensitive-structured-field", quoted_redacted["reason"])
        self.assertNotIn("TINY-QUOTED-CREDENTIAL", json.dumps(quoted_redacted))
        self.assertEqual(["sensitive-key"], quoted_categories)
        self.assertEqual(1, quoted_count)
        self.assertTrue(verify._contains_excluded_projection_key(quoted))

        assignment_key = "a" * (129 - len("token")) + "token"
        assignment = f"{assignment_key}=TINY-ASSIGNED-CREDENTIAL"
        assignment_redacted, assignment_categories, assignment_count = (
            capture._redact_codex_projection_value(assignment)
        )
        self.assertEqual(
            "sensitive-structured-field",
            assignment_redacted["reason"],
        )
        self.assertNotIn("TINY-ASSIGNED-CREDENTIAL", json.dumps(assignment_redacted))
        self.assertEqual(["sensitive-key"], assignment_categories)
        self.assertEqual(1, assignment_count)
        self.assertTrue(verify._contains_excluded_projection_key(assignment))

        oversized_safe_key = "q" * 513
        oversized_safe = f'prefix "{oversized_safe_key}":"safe"}}'
        oversized_safe_redacted, _, _ = capture._redact_codex_projection_value(
            oversized_safe
        )
        self.assertEqual(
            "hidden-structured-field",
            oversized_safe_redacted["reason"],
        )
        self.assertTrue(verify._contains_excluded_projection_key(oversized_safe))

        exact_quoted_key = "q" * 512
        exact_quoted = f'prefix "{exact_quoted_key}":"safe"}}'
        exact_quoted_redacted, exact_quoted_categories, exact_quoted_count = (
            capture._redact_codex_projection_value(exact_quoted)
        )
        self.assertEqual(exact_quoted, exact_quoted_redacted)
        self.assertEqual([], exact_quoted_categories)
        self.assertEqual(0, exact_quoted_count)
        self.assertFalse(verify._contains_excluded_projection_key(exact_quoted))

        exact_assignment_key = "q" * 128
        exact_assignment = f"{exact_assignment_key}=safe"
        exact_assignment_redacted, exact_assignment_categories, exact_assignment_count = (
            capture._redact_codex_projection_value(exact_assignment)
        )
        self.assertEqual(exact_assignment, exact_assignment_redacted)
        self.assertEqual([], exact_assignment_categories)
        self.assertEqual(0, exact_assignment_count)
        self.assertFalse(verify._contains_excluded_projection_key(exact_assignment))

    def test_codex_oversized_assignment_scan_distinguishes_complete_padding(self) -> None:
        for size, padding in ((145, "=="), (146, "="), (617, "=")):
            token = base64.urlsafe_b64encode(
                b"\x80" + bytes(index % 256 for index in range(size - 1))
            ).decode("ascii")
            with self.subTest(padding=padding):
                self.assertTrue(token.endswith(padding))
                self.assertGreater(len(token), capture._CODEX_ASSIGNMENT_KEY_FRAGMENT_LIMIT)
                self.assertEqual(
                    (False, False),
                    capture._classify_codex_oversized_text_key_fragments(token),
                )
                self.assertEqual(
                    (False, False), capture._classify_codex_text_key_fragments(token)
                )
                projected, categories, count = capture._redact_codex_projection_fixed_point(
                    token
                )
                self.assertEqual(token, projected)
                self.assertEqual([], categories)
                self.assertEqual(0, count)
                self.assertFalse(verify._contains_excluded_projection_key(token))
                quoted = f'Public observation "{token}" remains opaque.'
                self.assertEqual(
                    (False, False),
                    capture._classify_codex_oversized_text_key_fragments(quoted),
                )
                self.assertEqual(
                    (quoted, [], 0), capture._redact_codex_projection_fixed_point(quoted)
                )
                self.assertFalse(verify._contains_excluded_projection_key(quoted))

    def test_codex_padding_recognition_does_not_accept_assignment_values(self) -> None:
        token = base64.urlsafe_b64encode(b"\x80" + b"a" * 144).decode("ascii")
        over_bound = base64.urlsafe_b64encode(
            b"\x80" + b"a" * capture.MAX_CODEX_TEXT_BYTES
        ).decode("ascii")
        cases = {
            "too-much-padding": token + "=",
            "invalid-alphabet": token[:2] + "." + token[3:],
            "attached-value": token + "assigned-value",
            "whitespace-value": token + " assigned-value",
            "newline-value": token + "\nassigned-value",
            "truncation-marker-and-prose": (
                f'<truncated original_characters="256" />{token}\n\n'
                "1. Later source text remains ambiguous."
            ),
            "whitespace-before-padding": token[:-2] + " ==",
            "oversized-token": over_bound,
            "quoted-assignment-key": f'"{token}":"assigned-value"',
            "quoted-equals-key": f'"{token}" = assigned-value',
            "mismatched-quotes": f'"{token}\' ',
            "single-quotes": f"'{token}'",
            "parentheses": f"({token})",
            "backticks": f"`{token}`",
            "escaped-opening-quote": f'\\"{token}"',
        }
        for label, value in cases.items():
            with self.subTest(case=label):
                self.assertEqual(
                    (True, False),
                    capture._classify_codex_oversized_text_key_fragments(value),
                )
                projected, _, _ = capture._redact_codex_projection_value(value)
                self.assertIsInstance(projected, dict)
                self.assertTrue(verify._contains_excluded_projection_key(value))

    def test_codex_padding_is_lexical_and_preserves_full_key_checks(self) -> None:
        token = base64.urlsafe_b64encode(b"\x80" + b"a" * 144).decode("ascii")
        for value in (token[:-3] + "B==", token[:-2] + "A=="):
            with self.subTest(size=len(value)):
                self.assertEqual(
                    (False, False), capture._classify_codex_text_key_fragments(value)
                )
                self.assertEqual(
                    (value, [], 0), capture._redact_codex_projection_fixed_point(value)
                )
                self.assertEqual(
                    (False, False),
                    capture._classify_codex_text_key_fragments(f'Visible "{value}".'),
                )

        for key, expected in (
            ("analysis" + "_" * 129, (True, False)),
            ("developer" + "_" * 129 + "instructions", (True, False)),
            ("a" * 129 + "token", (False, True)),
        ):
            for value in (key + "==", f'Visible "{key}==".'):
                with self.subTest(key=key, quoted=value.startswith("Visible")):
                    self.assertEqual(
                        expected, capture._classify_codex_text_key_fragments(value)
                    )
                    projected, _, _ = capture._redact_codex_projection_value(value)
                    self.assertIsInstance(projected, dict)

    def test_codex_padding_does_not_disable_other_field_or_secret_checks(self) -> None:
        token = base64.urlsafe_b64encode(b"\x80" + b"a" * 144).decode("ascii")
        for label, value, expected in (
            ("hidden-field", f'{token} "analysis":"PRIVATE-SYNTHETIC"', (True, False)),
            ("sensitive-field", f'{token} password=PRIVATE-SYNTHETIC', (True, True)),
            (
                "quoted-token-with-hidden-field",
                f'Observation "{token}"; "analysis":"PRIVATE-SYNTHETIC"',
                (True, False),
            ),
            (
                "quoted-token-with-sensitive-field",
                f'Observation "{token}"; password=PRIVATE-SYNTHETIC',
                (False, True),
            ),
        ):
            with self.subTest(case=label):
                self.assertEqual(expected, capture._classify_codex_text_key_fragments(value))
                projected, _, _ = capture._redact_codex_projection_value(value)
                self.assertNotIn("PRIVATE-SYNTHETIC", json.dumps(projected))

        synthetic_secret = "ghp_" + "S" * 24
        value = f'Observation "{token}"; {synthetic_secret}'
        projected, _, _ = capture._redact_codex_projection_fixed_point(value)
        redacted, categories, count = capture.redact_projection_bytes(
            capture.canonical_json(projected)
        )
        self.assertNotIn(synthetic_secret.encode(), redacted)
        self.assertEqual(["github-token"], categories)
        self.assertEqual(1, count)

    def test_codex_text_key_classifier_uses_one_shared_structural_pass(self) -> None:
        class CountingPattern:
            def __init__(self, pattern: re.Pattern[str]) -> None:
                self.pattern = pattern
                self.calls = 0

            def finditer(self, value: str) -> object:
                self.calls += 1
                return self.pattern.finditer(value)

        json_pattern = CountingPattern(capture._CODEX_JSON_KEY_FRAGMENT_PATTERN)
        assignment_pattern = CountingPattern(
            capture._CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN
        )
        value = 'prefix "visible_field": "' + "safe output " * 100_000 + '"}'
        with (
            mock.patch.object(
                capture,
                "_CODEX_JSON_KEY_FRAGMENT_PATTERN",
                json_pattern,
            ),
            mock.patch.object(
                capture,
                "_CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN",
                assignment_pattern,
            ),
        ):
            projected, categories, count = capture._redact_codex_projection_value(value)
        self.assertEqual(value, projected)
        self.assertEqual([], categories)
        self.assertEqual(0, count)
        self.assertEqual(1, json_pattern.calls)
        self.assertEqual(1, assignment_pattern.calls)

        json_pattern.calls = 0
        assignment_pattern.calls = 0
        with (
            mock.patch.object(
                capture,
                "_CODEX_JSON_KEY_FRAGMENT_PATTERN",
                json_pattern,
            ),
            mock.patch.object(
                capture,
                "_CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN",
                assignment_pattern,
            ),
        ):
            capture._classify_codex_text_key_fragments("safe output " * 100_000)
        self.assertEqual(0, json_pattern.calls)
        self.assertEqual(0, assignment_pattern.calls)

    def test_codex_event_projection_uses_exact_observed_allowlists(self) -> None:
        unwanted = "UNALLOWLISTED-CONTENT"
        cases: list[tuple[dict[str, object], set[str]]] = [
            (
                {
                    "type": "agent_message",
                    "message": "message",
                    "phase": "commentary",
                    "memory_citation": {
                        "entries": [
                            {
                                "path": f"{MAC_USERS_ROOT}/person/memory/MEMORY.md",
                                "lineStart": 10,
                                "lineEnd": 12,
                                "note": "bounded note",
                            }
                        ],
                        "rolloutIds": ["rollout-id"],
                    },
                    "content": unwanted,
                },
                {"type", "message", "phase", "memory_citation"},
            ),
            (
                {
                    "type": "task_started",
                    "turn_id": "turn",
                    "started_at": 1,
                    "model_context_window": 2,
                    "collaboration_mode_kind": "default",
                    "status": unwanted,
                },
                {
                    "type",
                    "turn_id",
                    "model_context_window",
                    "collaboration_mode_kind",
                },
            ),
            (
                {
                    "type": "task_complete",
                    "turn_id": "turn",
                    "started_at": 1,
                    "completed_at": 2,
                    "duration_ms": 3.5,
                    "time_to_first_token_ms": 1.25,
                    "last_agent_message": unwanted,
                    "error": {"code": "FAILED", "message": unwanted},
                },
                {
                    "type",
                    "turn_id",
                    "duration_ms",
                    "first_output_latency_ms",
                    "error",
                },
            ),
            (
                {
                    "type": "sub_agent_activity",
                    "agent_path": ["root", "child"],
                    "agent_thread_id": "child",
                    "event_id": "event",
                    "kind": "completed",
                    "occurred_at_ms": 4,
                    "message": unwanted,
                },
                {
                    "type",
                    "agent_path",
                    "agent_thread_id",
                    "event_id",
                    "kind",
                    "occurred_at_ms",
                },
            ),
            (
                {
                    "type": "item_completed",
                    "thread_id": "thread",
                    "turn_id": "turn",
                    "started_at_ms": 1,
                    "completed_at_ms": 2,
                    "item": {
                        "agent_path": ["root"],
                        "agent_thread_id": "child",
                        "id": "item",
                        "kind": "message",
                        "type": "agent_message",
                        "content": unwanted,
                    },
                },
                {"type", "thread_id", "turn_id", "started_at_ms", "completed_at_ms", "item"},
            ),
            (
                {
                    "type": "patch_apply_end",
                    "call_id": "call",
                    "turn_id": "turn",
                    "status": "completed",
                    "success": True,
                    "changes": {f"{MAC_USERS_ROOT}/person/private.py": unwanted},
                    "stdout": "safe output",
                    "stderr": "",
                },
                {
                    "type",
                    "call_id",
                    "turn_id",
                    "status",
                    "success",
                    "stdout",
                    "stderr",
                    "changes_omitted_count",
                },
            ),
            (
                {
                    "type": "turn_aborted",
                    "turn_id": "turn",
                    "started_at": 1,
                    "completed_at": 2,
                    "duration_ms": 3,
                    "reason": {"code": "cancelled", "message": unwanted},
                    "detail": unwanted,
                },
                {"type", "turn_id", "duration_ms", "reason"},
            ),
        ]
        for payload, expected_keys in cases:
            with self.subTest(event_type=payload["type"]):
                projected, reason = capture._codex_event_projection(payload)
                self.assertEqual("", reason)
                self.assertEqual(expected_keys, set(projected))
                self.assertNotIn(unwanted, json.dumps(projected, sort_keys=True))

        item, _ = capture._codex_event_projection(cases[4][0])
        self.assertEqual(
            {"agent_path", "agent_thread_id", "id", "kind", "type"},
            set(item["item"]),
        )
        completed, _ = capture._codex_event_projection(cases[2][0])
        self.assertEqual({"present": True, "code": "FAILED"}, completed["error"])
        agent, _ = capture._codex_event_projection(cases[0][0])
        citation = agent["memory_citation"]["entries"][0]
        self.assertEqual("MEMORY.md", citation["path_basename"])
        self.assertEqual(64, len(citation["path_sha256"]))
        self.assertNotIn(f"{MAC_USERS_ROOT}/", json.dumps(agent, sort_keys=True))

    def test_codex_projection_summarises_attachments_and_sanitises_urls(self) -> None:
        digest = "a" * 64
        user, _ = capture._codex_event_projection(
            {
                "type": "user_message",
                "message": "review this",
                "images": [
                    {
                        "type": "image/png",
                        "bytes": 123,
                        "sha256": digest,
                        "path": f"{MAC_USERS_ROOT}/person/private.png",
                    }
                ],
                "local_images": [f"{MAC_USERS_ROOT}/person/other.png"],
                "client_id": "raw-client-id",
            }
        )
        self.assertEqual({"type", "message", "attachment_summary"}, set(user))
        self.assertEqual(
            {"type": "image/png", "bytes": 123, "sha256": digest},
            user["attachment_summary"]["images"]["items"][0],
        )
        user_text = json.dumps(user, sort_keys=True)
        self.assertNotIn(f"{MAC_USERS_ROOT}/", user_text)
        self.assertNotIn("raw-client-id", user_text)
        redacted_user, _, _ = capture._redact_codex_projection_value(user)
        self.assertEqual(
            {"images_summary", "local_images"},
            set(redacted_user["attachment_summary"]),
        )
        verify._verify_codex_event_payload_domains(redacted_user)

        task_complete, _ = capture._codex_event_projection(
            {
                "type": "task_complete",
                "duration_ms": 3.5,
                "time_to_first_token_ms": 1.25,
            }
        )
        self.assertIsNotNone(task_complete)
        assert task_complete is not None
        redacted_task, _, _ = capture._redact_codex_projection_value(task_complete)
        self.assertEqual(1.25, redacted_task["first_output_latency_ms"])
        verify._verify_codex_event_payload_domains(redacted_task)
        legacy_task = dict(redacted_task)
        del legacy_task["first_output_latency_ms"]
        legacy_task["time_to_first_token_ms"] = "XXXX"
        verify._verify_codex_event_payload_domains(legacy_task)
        hybrid_task = dict(redacted_task)
        hybrid_task["time_to_first_token_ms"] = "XXXX"
        with self.assertRaises(verify.EvidenceVerificationError):
            verify._verify_codex_event_payload_domains(hybrid_task)
        for invalid_legacy_mask in ("", "XXXx", "X" * 65, 1.25, True):
            invalid_legacy_task = dict(legacy_task)
            invalid_legacy_task["time_to_first_token_ms"] = invalid_legacy_mask
            with self.assertRaises(verify.EvidenceVerificationError):
                verify._verify_codex_event_payload_domains(invalid_legacy_task)

        generic_call, _ = capture._codex_response_projection(
            {
                "type": "function_call",
                "name": "example",
                "arguments": {"time_to_first_token_ms": "opaque-private-value"},
            }
        )
        self.assertIsNotNone(generic_call)
        assert generic_call is not None
        redacted_call, categories, _ = capture._redact_codex_projection_value(generic_call)
        self.assertEqual(["sensitive-key"], categories)
        self.assertNotIn("opaque-private-value", json.dumps(redacted_call, sort_keys=True))

        for invalid_number in (
            -1,
            float("inf"),
            float("nan"),
            float(2**63),
            1e308,
            2**63,
            True,
        ):
            invalid_task, _ = capture._codex_event_projection(
                {
                    "type": "task_complete",
                    "duration_ms": invalid_number,
                    "time_to_first_token_ms": invalid_number,
                }
            )
            self.assertEqual({"type": "task_complete"}, invalid_task)

        web, _ = capture._codex_event_projection(
            {
                "type": "web_search_end",
                "call_id": "call",
                "action": "search",
                "query": "bounded query",
                "results": [
                    {
                        "type": "computer_initialize_state",
                        "ref_id": "ref",
                        "domain": "example.invalid",
                        "url": "https://user:pass@example.invalid/path?token=secret#fragment",
                        "title": "Title",
                        "snippet": "Snippet",
                        "thumbnail_url": "https://example.invalid/image?q=secret",
                        "raw": "UNALLOWLISTED-CONTENT",
                    }
                ],
            }
        )
        self.assertEqual({"type", "call_id", "action", "query", "results"}, set(web))
        self.assertEqual("https://example.invalid/path", web["results"][0]["url"])
        self.assertEqual(
            "https://example.invalid/image",
            web["results"][0]["thumbnail_url"],
        )

        embedded = capture._bounded_codex_text(
            "first https://user:pass@example.invalid/a?q=1 and "
            "second https://example.invalid/b?q=2"
        )
        self.assertEqual(
            "first https://example.invalid/a and second https://example.invalid/b",
            embedded,
        )
        self.assertEqual(
            "[invalid URL omitted]",
            capture._bounded_codex_text("https://example.invalid:bad/path?q=secret"),
        )
        truncated_url = capture._bounded_codex_text(
            "https://user:pass@example.invalid/"
            + "a" * (capture.MAX_CODEX_TEXT_BYTES * 2)
            + "?token=secret"
        )
        truncated_text = json.dumps(truncated_url, sort_keys=True)
        self.assertNotIn("user:pass", truncated_text)
        self.assertNotIn("?token=", truncated_text)
        self.assertTrue(truncated_url["truncated"])
        nested_omission = {
            "text_omitted": True,
            "reason": "sensitive-structured-field",
            "original_utf8_bytes": 128,
            "original_sha256": "a" * 64,
        }
        self.assertTrue(
            verify._is_bounded_text(
                {
                    "text": nested_omission,
                    "truncated": True,
                    "original_utf8_bytes": 256,
                    "original_sha256": "b" * 64,
                }
            )
        )
        self.assertFalse(
            verify._is_bounded_text(
                {
                    "text": {
                        "text": nested_omission,
                        "truncated": True,
                        "original_utf8_bytes": 192,
                        "original_sha256": "c" * 64,
                    },
                    "truncated": True,
                    "original_utf8_bytes": 256,
                    "original_sha256": "d" * 64,
                }
            )
        )

        session = capture._codex_session_meta_projection(
            {
                "id": "session",
                "parent_thread_id": "parent",
                "forked_from_id": "fork",
                "agent_path": ["root", "child"],
                "agent_nickname": "reviewer",
                "agent_role": "review",
                "source": {
                    "subagent": {
                        "thread_spawn": {
                            "parent_thread_id": "parent",
                            "depth": 1,
                            "agent_path": ["root", "child"],
                            "agent_nickname": "reviewer",
                            "agent_role": "review",
                            "task_name": "UNALLOWLISTED-CONTENT",
                        }
                    }
                },
                "git": {
                    "commit_hash": "a" * 40,
                    "branch": "main",
                    "repository_url": (
                        "https://user:pass@example.invalid/repository.git?token=secret"
                    ),
                },
            }
        )
        self.assertEqual("review", session["agent_role"])
        self.assertEqual("review", session["agent_parent_path"]["agent_role"])
        self.assertNotIn("task_name", json.dumps(session, sort_keys=True))
        self.assertEqual(
            "https://example.invalid/repository.git",
            session["git"]["repository_url"],
        )

    def test_codex_capture_and_verifier_domains_remain_aligned(self) -> None:
        header = {"thread_id": "thread", "session_id": "session"}
        cases = (
            (
                "session_meta",
                {
                    "id": "thread",
                    "session_id": "session",
                    "cli_version": 123,
                    "git": {"commit_hash": "a" * 40, "branch": 42},
                },
                {"cli_version"},
            ),
            (
                "event_msg",
                {"type": "agent_message", "message": "safe", "phase": 7},
                {"phase"},
            ),
            (
                "event_msg",
                {
                    "type": "task_started",
                    "turn_id": "turn",
                    "started_at": 1,
                    "model_context_window": "large",
                },
                {"started_at", "model_context_window"},
            ),
            (
                "event_msg",
                {
                    "type": "mcp_tool_call_end",
                    "call_id": "call",
                    "duration": "slow",
                    "read_only_hint": 1,
                },
                {"duration", "read_only_hint"},
            ),
            (
                "event_msg",
                {"type": "patch_apply_end", "call_id": "call", "success": 1},
                {"success"},
            ),
            (
                "event_msg",
                {
                    "type": "web_search_end",
                    "results": [{"title": "safe", "url": "/relative/private"}],
                },
                {"url"},
            ),
            ("event_msg", {"type": "token_count", "rate_limits": {}}, set()),
            (
                "event_msg",
                {"type": "turn_aborted", "reason": {"code": 503}},
                set(),
            ),
            (
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "output": [{"type": "input_image", "detail": "auto"}],
                },
                set(),
            ),
        )
        for source_type, payload, absent in cases:
            with self.subTest(source_type=source_type, payload=payload):
                projected, reason = capture._project_codex_record(
                    {"type": source_type, "payload": payload}
                )
                self.assertEqual("", reason)
                redacted, _categories, _count = capture._redact_codex_projection_value(
                    projected
                )
                self.assertIsInstance(redacted, dict)
                projected_payload = redacted["payload"]
                verify._verify_codex_projected_payload(
                    source_type, projected_payload, header
                )
                serialised = json.dumps(projected_payload, sort_keys=True)
                for key in absent:
                    self.assertNotIn(f'"{key}"', serialised)

        token_projected, _ = capture._project_codex_record(
            {
                "type": "event_msg",
                "payload": {"type": "token_count", "rate_limits": {}},
            }
        )
        self.assertEqual({}, token_projected["payload"]["info"])
        image_projected, _ = capture._project_codex_record(
            {
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call_output",
                    "output": [{"type": "input_image", "detail": "auto"}],
                },
            }
        )
        self.assertEqual([], image_projected["payload"]["output"])

        citation_projected, _ = capture._project_codex_record(
            {
                "type": "event_msg",
                "payload": {
                    "type": "agent_message",
                    "memory_citation": {
                        "entries": [
                            {"lineStart": -1, "lineEnd": 3, "note": "bounded"}
                        ]
                    },
                },
            }
        )
        citation = citation_projected["payload"]["memory_citation"]["entries"][0]
        self.assertNotIn("lineStart", citation)
        self.assertEqual(3, citation["lineEnd"])
        verify._verify_codex_projected_payload(
            "event_msg", citation_projected["payload"], header
        )

        for invalid_name in (None, 7, ""):
            projected, reason = capture._project_codex_record(
                {
                    "type": "response_item",
                    "payload": {"type": "function_call", "name": invalid_name},
                }
            )
            self.assertIsNone(projected)
            self.assertEqual("response_item:invalid-tool-call", reason)

    def test_codex_mcp_projection_sanitises_nested_results_and_images(self) -> None:
        payload = {
            "type": "mcp_tool_call_end",
            "call_id": "call",
            "duration": 1,
            "read_only_hint": True,
            "plugin_id": "plugin",
            "action_name": "action",
            "app_name": "app",
            "connector_id": "connector",
            "link_id": "link",
            "invocation": {
                "server": "server",
                "tool": "tool",
                "arguments": {
                    "file_path": f"{MAC_USERS_ROOT}/person/input.txt",
                    "client_id": "client",
                    "input_image": "RAW-INPUT-IMAGE",
                },
                "host": "UNALLOWLISTED-CONTENT",
            },
            "result": {
                "_meta": {"browser": "HOST-STATE"},
                "image_url": "RAW-RESULT-IMAGE",
                f"{MAC_USERS_ROOT}/person/output.txt": "path-key-value",
                "safe": "retained",
            },
            "error": "UNALLOWLISTED-CONTENT",
        }
        projected, reason = capture._codex_event_projection(payload)
        self.assertEqual("", reason)
        self.assertEqual(
            {
                "type",
                "call_id",
                "duration",
                "read_only_hint",
                "plugin_id",
                "action_name",
                "app_name",
                "connector_id",
                "link_id",
                "invocation",
                "result",
            },
            set(projected),
        )
        text = json.dumps(projected, sort_keys=True)
        for excluded in (
            f"{MAC_USERS_ROOT}/",
            "client",
            "RAW-INPUT-IMAGE",
            "RAW-RESULT-IMAGE",
            "HOST-STATE",
            "UNALLOWLISTED-CONTENT",
        ):
            self.assertNotIn(excluded, text)
        self.assertIn("input_image_summary", text)
        self.assertIn("image_url_summary", text)
        self.assertEqual("retained", projected["result"]["safe"])

    def test_codex_unknowns_are_bounded_and_hidden_records_are_excluded(self) -> None:
        unknown_type = "future-event-" + "x" * (capture.MAX_CODEX_TEXT_BYTES * 2)
        projected, reason = capture._codex_event_projection(
            {"type": unknown_type, "body": "UNSUPPORTED-BODY"}
        )
        self.assertIsNone(projected)
        self.assertLess(len(reason), 128)
        self.assertNotIn(unknown_type, reason)
        self.assertEqual("unsupported-rollout-record", capture._codex_stub_kind(reason))

        for hidden in (
            {"type": "agent_reasoning", "text": "HIDDEN"},
            {"type": "context_compacted", "content": "HIDDEN"},
            {"type": "thread_settings_applied", "content": "HIDDEN"},
        ):
            with self.subTest(hidden=hidden["type"]):
                projected, reason = capture._codex_event_projection(hidden)
                self.assertIsNone(projected)
                self.assertEqual("excluded-rollout-record", capture._codex_stub_kind(reason))

        response, reason = capture._codex_response_projection(
            {
                "type": "agent_message",
                "content": [
                    {"type": "input_text", "text": "retained"},
                    {"type": "output_text", "text": "HIDDEN"},
                ],
                "encrypted_content": "HIDDEN-ENCRYPTED",
            }
        )
        self.assertEqual("", reason)
        self.assertEqual(
            {"type": "agent_message", "content": [{"type": "input_text", "text": "retained"}]},
            response,
        )

    def test_codex_response_tools_use_closed_redacted_text_and_image_schemas(self) -> None:
        call, reason = capture._codex_response_projection(
            {
                "type": "function_call",
                "name": "inspect",
                "namespace": "workspace",
                "server": "local",
                "call_id": "call",
                "status": "completed",
                "arguments": json.dumps(
                    {
                        "accessToken": "tool-secret-value",
                        "file_path": f"{MAC_USERS_ROOT}/person/private.txt",
                        "input_image": "RAW-CALL-IMAGE",
                    }
                ),
                "output": "UNALLOWLISTED-CONTENT",
            }
        )
        self.assertEqual("", reason)
        self.assertEqual(
            {"type", "name", "namespace", "server", "call_id", "status", "arguments"},
            set(call),
        )
        self.assertIsInstance(call["arguments"], dict)
        redacted_call, _, count = capture._redact_codex_projection_value(call)
        call_text = json.dumps(redacted_call, sort_keys=True)
        self.assertEqual(1, count)
        self.assertNotIn("tool-secret-value", call_text)
        self.assertNotIn(f"{MAC_USERS_ROOT}/", call_text)
        self.assertNotIn("RAW-CALL-IMAGE", call_text)
        self.assertIn("input_image_summary", call_text)

        custom_call, _ = capture._codex_response_projection(
            {
                "type": "custom_tool_call",
                "name": "check",
                "call_id": "custom",
                "status": "completed",
                "input": {"safe": "retained"},
                "arguments": {"safe": "also retained"},
            }
        )
        self.assertEqual(
            {"type", "name", "call_id", "status", "input", "arguments"},
            set(custom_call),
        )

        output, reason = capture._codex_response_projection(
            {
                "type": "function_call_output",
                "call_id": "call",
                "status": "completed",
                "output": [
                    {"type": "input_text", "text": "retained input"},
                    {"type": "text", "text": "retained text"},
                    {"type": "output_text", "text": "UNALLOWLISTED-CONTENT"},
                    {
                        "type": "input_image",
                        "detail": "high",
                        "media_type": "image/png",
                        "image_url": "data:image/png;base64,RAW-OUTPUT-IMAGE",
                    },
                    {
                        "type": "input_image",
                        "image_url": "https://user:pass@example.invalid/image?token=secret",
                    },
                ],
                "encrypted_content": "HIDDEN-ENCRYPTED",
            }
        )
        self.assertEqual("", reason)
        self.assertEqual({"type", "call_id", "status", "output"}, set(output))
        output_text = json.dumps(output, sort_keys=True)
        self.assertIn("retained input", output_text)
        self.assertIn("retained text", output_text)
        self.assertIn("encoded_bytes", output_text)
        self.assertIn("https://example.invalid/image", output_text)
        for excluded in (
            "UNALLOWLISTED-CONTENT",
            "RAW-OUTPUT-IMAGE",
            "user:pass",
            "?token=",
            "HIDDEN-ENCRYPTED",
        ):
            self.assertNotIn(excluded, output_text)

        custom_output, _ = capture._codex_response_projection(
            {
                "type": "custom_tool_call_output",
                "call_id": "custom",
                "output": "plain output",
            }
        )
        self.assertEqual(
            [{"type": "text", "text": "plain output"}],
            custom_output["output"],
        )

    def test_codex_projection_accepts_consistent_session_metadata_restatements(self) -> None:
        sessions = self.root / "sessions-restated-metadata"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        session_record = {
            "timestamp": "2026-08-30T08:00:00Z",
            "type": "session_meta",
            "payload": {
                "id": "root-thread",
                "session_id": "root-thread",
                "timestamp": "2026-08-30T08:00:00Z",
            },
        }
        values = [
            session_record,
            {
                "type": "event_msg",
                "payload": {"type": "user_message", "message": "visible"},
            },
            session_record,
        ]
        source.write_text(
            "".join(json.dumps(value) + "\n" for value in values), encoding="utf-8"
        )
        source.chmod(0o600)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )

        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_projection_accepts_closed_transitive_lineage_restatements(self) -> None:
        sessions = self.root / "sessions-transitive-lineage"
        sessions.mkdir(mode=0o700)
        shared_session = "shared-session-id"
        parents = {
            "root-thread": None,
            "child-a": "root-thread",
            "grandchild": "child-a",
            "child-b": "root-thread",
        }

        def session_meta(
            thread: str,
            *,
            include_session: bool = True,
            marker: str | None = None,
        ) -> dict[str, object]:
            payload: dict[str, object] = {
                "id": thread,
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if include_session:
                payload["session_id"] = shared_session
            if thread in parents and parents[thread] is not None:
                payload["parent_thread_id"] = parents[thread]
            if marker is not None:
                payload["cli_version"] = marker
            return {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": payload,
            }

        sibling_restatement = session_meta(
            "child-b",
            marker="SIBLING-META-MUST-NOT-LEAK",
        )
        outside_restatement = session_meta("outside-lineage-raw-id")
        impossible_parent_restatement = session_meta("root-thread")
        impossible_parent_restatement["payload"]["parent_thread_id"] = "child-a"
        outside_fork_restatement = session_meta("root-thread")
        outside_fork_restatement["payload"]["forked_from_id"] = (
            "OUTSIDE-FORK-MUST-NOT-LEAK"
        )
        missing_session_restatement = session_meta(
            "root-thread",
            include_session=False,
            marker="MISSING-SESSION-MUST-NOT-LEAK",
        )
        missing_parent_restatement = session_meta("child-a")
        del missing_parent_restatement["payload"]["parent_thread_id"]
        null_parent_restatement = session_meta("child-a")
        null_parent_restatement["payload"]["parent_thread_id"] = None
        integer_parent_restatement = session_meta("child-a")
        integer_parent_restatement["payload"]["parent_thread_id"] = 17
        invalid_session_restatement = session_meta("child-a")
        invalid_session_restatement["payload"]["session_id"] = False
        restatements: dict[str, list[dict[str, object]]] = {
            "root-thread": [session_meta(shared_session, include_session=False)],
            "child-a": [
                session_meta("root-thread"),
                sibling_restatement,
            ],
            "grandchild": [
                session_meta("root-thread"),
                outside_restatement,
                impossible_parent_restatement,
                outside_fork_restatement,
                missing_session_restatement,
                missing_parent_restatement,
                null_parent_restatement,
                integer_parent_restatement,
                invalid_session_restatement,
            ],
            "child-b": [],
        }
        excluded_raw = [
            capture.canonical_json(value)
            for value in (
                sibling_restatement,
                outside_restatement,
                impossible_parent_restatement,
                outside_fork_restatement,
                missing_session_restatement,
                missing_parent_restatement,
                null_parent_restatement,
                integer_parent_restatement,
                invalid_session_restatement,
            )
        ]
        for number, thread in enumerate(parents):
            values = [
                session_meta(thread),
                {
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": f"visible {thread}"},
                },
                *restatements[thread],
            ]
            source = sessions / f"{number}-{thread}.jsonl"
            source.write_bytes(b"".join(capture.canonical_json(value) for value in values))
            source.chmod(0o600)

        records = capture._iter_explicit_codex_records([sessions])
        self.assertEqual(
            {
                "root-thread": frozenset({"root-thread"}),
                "child-a": frozenset({"child-a", "root-thread"}),
                "grandchild": frozenset(
                    {"grandchild", "child-a", "root-thread"}
                ),
                "child-b": frozenset({"child-b", "root-thread"}),
            },
            capture._codex_session_lineages(records),
        )

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            captured = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )

        self.assertEqual(4, captured)
        events = self.journal()
        observed = verify._object_paths(self.store)
        projected_ids: dict[str, list[str]] = {}
        stubs: list[dict[str, object]] = []
        aggregate_projection = b""
        for event in events:
            if event["source"]["kind"] != "codex-user-visible-projection":
                continue
            raw = gzip.decompress(observed[event["objects"][0]["sha256"]].read_bytes())
            aggregate_projection += raw
            values = [
                capture.parse_json(line, "test Codex projection")
                for line in raw.splitlines(keepends=True)
            ]
            header = values[0]
            projected_ids[header["thread_id"]] = [
                value["payload"]["id"]
                for value in values
                if value.get("record") == "projected-rollout-record"
                and value.get("source_type") == "session_meta"
            ]
            stubs.extend(
                value
                for value in values
                if value.get("source_type")
                == "session_meta:outside-selected-lineage"
            )
        self.assertEqual(
            {
                "root-thread": ["root-thread", shared_session],
                "child-a": ["child-a", "root-thread"],
                "grandchild": ["grandchild", "root-thread"],
                "child-b": ["child-b"],
            },
            projected_ids,
        )
        self.assertEqual(9, len(stubs))
        for stub in stubs:
            self.assertEqual(
                {"record", "source_line", "source_line_sha256", "source_bytes", "source_type"},
                set(stub),
            )
        self.assertEqual(
            sorted((capture.sha256_bytes(raw), len(raw)) for raw in excluded_raw),
            sorted((stub["source_line_sha256"], stub["source_bytes"]) for stub in stubs),
        )
        self.assertNotIn(b"outside-lineage-raw-id", aggregate_projection)
        self.assertNotIn(b"SIBLING-META-MUST-NOT-LEAK", aggregate_projection)
        self.assertNotIn(b"OUTSIDE-FORK-MUST-NOT-LEAK", aggregate_projection)
        self.assertNotIn(b"MISSING-SESSION-MUST-NOT-LEAK", aggregate_projection)
        manifest_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        manifest = capture.parse_json(
            observed[manifest_event["objects"][0]["sha256"]].read_bytes(),
            "test Codex manifest",
        )
        self.assertEqual(
            {"session_meta:outside-selected-lineage": 9},
            manifest["aggregate_skipped_record_types"],
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_session_alias_cannot_collide_with_selected_sibling(self) -> None:
        sessions = self.root / "sessions-alias-collision"
        sessions.mkdir(mode=0o700)

        def write_session(
            name: str,
            *,
            session_id: str,
            parent_thread_id: str | None,
        ) -> None:
            payload: dict[str, object] = {
                "id": name,
                "session_id": session_id,
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if parent_thread_id is not None:
                payload["parent_thread_id"] = parent_thread_id
            path = sessions / f"{name}.jsonl"
            path.write_bytes(
                capture.canonical_json(
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": payload,
                    }
                )
            )
            path.chmod(0o600)

        write_session("root-thread", session_id="shared-session", parent_thread_id=None)
        write_session("child-a", session_id="child-b", parent_thread_id="root-thread")
        write_session("child-b", session_id="shared-session", parent_thread_id="root-thread")
        records = capture._iter_explicit_codex_records([sessions])
        with self.assertRaisesRegex(
            capture.EvidenceCaptureError,
            "alias collides with a selected non-ancestor",
        ):
            capture._codex_session_lineages(records)

        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "outside the selected lineage",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {"id": "child-b", "session_id": "child-b"},
                {
                    "thread_id": "child-a",
                    "session_id": "child-b",
                    "parent_thread_id": "root-thread",
                },
                allowed_session_thread_ids=frozenset(
                    {"child-a", "root-thread"}
                ),
                session_lineage_metadata={
                    "child-a": ("child-b", "root-thread"),
                    "child-b": ("shared-session", "root-thread"),
                    "root-thread": ("shared-session", None),
                },
            )

    def test_codex_authoritative_session_rejects_explicit_invalid_session_id(self) -> None:
        raw = capture.canonical_json(
            {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "root-thread",
                    "session_id": False,
                    "timestamp": "2026-08-30T08:00:00Z",
                },
            }
        )
        with self.assertRaisesRegex(
            capture.EvidenceCaptureError,
            "lineage metadata is invalid",
        ):
            capture._parse_codex_session_meta(raw, label="invalid first record")

    def test_codex_fork_binding_uses_exact_raw_digest_before_url_sanitisation(self) -> None:
        source = self.root / "fork-binding.jsonl"
        source.write_text("placeholder\n", encoding="utf-8")
        source.chmod(0o600)
        record = capture.CodexSessionRecord(
            source,
            "root-thread",
            "root-thread",
            None,
            "2026-08-30T08:00:00Z",
            source.stat(),
        )
        raw_a = {
            "id": "root-thread",
            "session_id": "root-thread",
            "forked_from_id": "https://example.invalid/fork?source=A",
        }
        raw_b = {
            **raw_a,
            "forked_from_id": "https://example.invalid/fork?source=B",
        }
        projected_a = capture._codex_session_meta_projection(raw_a)
        projected_b = capture._codex_session_meta_projection(raw_b)
        self.assertEqual(
            projected_a["forked_from_id"],
            projected_b["forked_from_id"],
        )
        self.assertNotEqual(
            projected_a["forked_from_id_sha256"],
            projected_b["forked_from_id_sha256"],
        )
        self.assertTrue(
            capture._codex_session_meta_within_lineage(
                projected_a,
                record,
                frozenset({"root-thread"}),
                raw_payload=raw_a,
                lineage_metadata={"root-thread": ("root-thread", None)},
                authoritative=True,
            )
        )
        self.assertFalse(
            capture._codex_session_meta_within_lineage(
                projected_b,
                record,
                frozenset({"root-thread"}),
                raw_payload=raw_b,
                lineage_metadata={"root-thread": ("root-thread", None)},
                authoritative_forked_from_id_sha256=projected_a[
                    "forked_from_id_sha256"
                ],
                authoritative=False,
            )
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "fork source differs from the authoritative",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                projected_b,
                {"thread_id": "root-thread", "session_id": "root-thread"},
                allowed_session_thread_ids=frozenset({"root-thread"}),
                session_lineage_metadata={"root-thread": ("root-thread", None)},
                authoritative_forked_from_id_sha256=projected_a[
                    "forked_from_id_sha256"
                ],
            )
        for legacy_fork in (
            "tag https://example.invalid/fork",
            "[invalid URL omitted]",
            "tag [local-path-omitted]",
            "X" * 40,
        ):
            with self.subTest(legacy_fork=legacy_fork), self.assertRaisesRegex(
                verify.EvidenceVerificationError,
                "legacy Codex fork source is not provably lossless",
            ):
                verify._verify_codex_projected_payload(
                    "session_meta",
                    {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "forked_from_id": legacy_fork,
                    },
                    {"thread_id": "root-thread", "session_id": "root-thread"},
                    allowed_session_thread_ids=frozenset({"root-thread"}),
                    session_lineage_metadata={
                        "root-thread": ("root-thread", None)
                    },
                    projection_schema=capture.LEGACY_CODEX_PROJECTION_SCHEMA,
                )
        legacy_uuid = "019d0123-4567-789a-bcde-f0123456789a"
        verify._verify_codex_projected_payload(
            "session_meta",
            {
                "id": "root-thread",
                "session_id": "root-thread",
                "forked_from_id": legacy_uuid,
            },
            {"thread_id": "root-thread", "session_id": "root-thread"},
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
            authoritative_session_meta=True,
            projection_schema=capture.LEGACY_CODEX_PROJECTION_SCHEMA,
        )
        verify._verify_codex_projected_payload(
            "session_meta",
            {
                "id": "root-thread",
                "session_id": "root-thread",
                "forked_from_id": "019d0123-4567-789a-bcde-f0123456789b",
            },
            {"thread_id": "root-thread", "session_id": "root-thread"},
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
            projection_schema=capture.LEGACY_CODEX_PROJECTION_SCHEMA,
        )

    def test_codex_projection_excludes_unrelated_session_restatement(self) -> None:
        sessions = self.root / "sessions-unrelated-restatement"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        first = capture.canonical_json(
            {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "root-thread",
                    "session_id": "root-thread",
                    "timestamp": "2026-08-30T08:00:00Z",
                },
            }
        )
        unrelated = capture.canonical_json(
            {
                "timestamp": "2026-08-30T08:01:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "outside-thread-distinctive",
                    "session_id": "root-thread",
                    "parent_thread_id": "root-thread",
                    "timestamp": "2026-08-30T08:01:00Z",
                },
            }
        )
        source.write_bytes(first + unrelated)
        source.chmod(0o600)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )

        event = next(
            item
            for item in self.journal()
            if item["source"]["kind"] == "codex-user-visible-projection"
        )
        projection_path = verify._object_paths(self.store)[event["objects"][0]["sha256"]]
        raw_projection = gzip.decompress(projection_path.read_bytes())
        values = [
            capture.parse_json(line, "test Codex projection")
            for line in raw_projection.splitlines(keepends=True)
        ]
        excluded = next(value for value in values if value.get("source_line") == 2)
        self.assertEqual("excluded-rollout-record", excluded["record"])
        self.assertEqual(
            "session_meta:outside-selected-lineage",
            excluded["source_type"],
        )
        self.assertEqual(capture.sha256_bytes(unrelated), excluded["source_line_sha256"])
        self.assertNotIn(b"outside-thread-distinctive", raw_projection)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_session_verifier_enforces_lineage_and_first_record_authority(self) -> None:
        header = {
            "thread_id": "child-thread",
            "session_id": "root-thread",
            "parent_thread_id": "root-thread",
        }
        allowed = frozenset({"child-thread", "root-thread"})
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "outside the selected lineage",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {"id": "unrelated-thread", "session_id": "root-thread"},
                header,
                allowed_session_thread_ids=allowed,
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "payload thread differs",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {
                    "id": "root-thread",
                    "session_id": "root-thread",
                    "parent_thread_id": "root-thread",
                },
                header,
                allowed_session_thread_ids=allowed,
                authoritative_session_meta=True,
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "parent differs from its lineage",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {
                    "id": "root-thread",
                    "session_id": "shared-session-id",
                    "parent_thread_id": "child-a",
                },
                {
                    "thread_id": "grandchild",
                    "session_id": "shared-session-id",
                    "parent_thread_id": "child-a",
                },
                allowed_session_thread_ids=frozenset(
                    {"grandchild", "child-a", "root-thread", "shared-session-id"}
                ),
                session_lineage_metadata={
                    "grandchild": ("shared-session-id", "child-a"),
                    "child-a": ("shared-session-id", "root-thread"),
                    "root-thread": ("shared-session-id", None),
                },
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "parent differs from its lineage",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {"id": "child-a", "session_id": "shared-session-id"},
                {
                    "thread_id": "grandchild",
                    "session_id": "shared-session-id",
                    "parent_thread_id": "child-a",
                },
                allowed_session_thread_ids=frozenset(
                    {"grandchild", "child-a", "root-thread"}
                ),
                session_lineage_metadata={
                    "grandchild": ("shared-session-id", "child-a"),
                    "child-a": ("shared-session-id", "root-thread"),
                    "root-thread": ("shared-session-id", None),
                },
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "payload session differs",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {"id": "root-thread"},
                {
                    "thread_id": "grandchild",
                    "session_id": "shared-session-id",
                    "parent_thread_id": "child-a",
                },
                allowed_session_thread_ids=frozenset(
                    {"grandchild", "child-a", "root-thread", "shared-session-id"}
                ),
                session_lineage_metadata={
                    "grandchild": ("shared-session-id", "child-a"),
                    "child-a": ("shared-session-id", "root-thread"),
                    "root-thread": ("shared-session-id", None),
                },
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "fork source differs from the authoritative",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {
                    "id": "root-thread",
                    "session_id": "root-thread",
                    "forked_from_id": "unrelated-fork",
                    "forked_from_id_sha256": capture._codex_forked_from_id_sha256(
                        "unrelated-fork"
                    ),
                },
                {"thread_id": "root-thread", "session_id": "root-thread"},
                allowed_session_thread_ids=frozenset({"root-thread"}),
            )
        verify._verify_codex_projected_payload(
            "session_meta",
            {
                "id": "root-thread",
                "session_id": "root-thread",
                "forked_from_id": "external-fork-provenance",
                "forked_from_id_sha256": capture._codex_forked_from_id_sha256(
                    "external-fork-provenance"
                ),
            },
            {"thread_id": "root-thread", "session_id": "root-thread"},
            allowed_session_thread_ids=frozenset({"root-thread"}),
            authoritative_session_meta=True,
        )
        verify._verify_codex_projected_payload(
            "session_meta",
            {
                "id": "root-thread",
                "session_id": "root-thread",
                "forked_from_id": "external-fork-provenance",
                "forked_from_id_sha256": capture._codex_forked_from_id_sha256(
                    "external-fork-provenance"
                ),
            },
            {"thread_id": "root-thread", "session_id": "root-thread"},
            allowed_session_thread_ids=frozenset({"root-thread"}),
            authoritative_forked_from_id_sha256=(
                capture._codex_forked_from_id_sha256(
                    "external-fork-provenance"
                )
            ),
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "lineage is incomplete",
        ):
            verify._verify_codex_projected_payload(
                "session_meta",
                {"id": "root-thread", "session_id": "root-thread"},
                {"thread_id": "root-thread", "session_id": "root-thread"},
                allowed_session_thread_ids=frozenset(),
            )

        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        session_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "session_meta"
        )
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        variants = (
            (
                session_index,
                {"id": "allowed-ancestor", "session_id": "root-thread"},
                frozenset({"root-thread", "allowed-ancestor"}),
                "payload thread differs",
            ),
            (
                event_index,
                {"id": "hostile-outside", "session_id": "root-thread"},
                frozenset({"root-thread"}),
                "outside the selected lineage",
            ),
        )
        for number, (index, payload, allowed_ids, error) in enumerate(variants):
            values = json.loads(json.dumps(original))
            values[index]["source_type"] = "session_meta"
            values[index]["payload"] = payload
            path, item = self._write_projection_variant(
                values,
                bundle["manifest_item"],
                f"invalid-session-lineage-{number}.jsonl.gz",
            )
            with self.assertRaisesRegex(verify.EvidenceVerificationError, error):
                verify._verify_codex_projection(
                    path,
                    item,
                    bundle["projection_event"],
                    allowed_session_thread_ids=allowed_ids,
                )

    def test_legacy_codex_maximum_depth_gap_is_bounded_and_v2_rejects_it(self) -> None:
        self.assertFalse(
            verify._legacy_codex_omission_residual_is_bounded(1, 2)
        )
        self.assertTrue(
            verify._legacy_codex_omission_residual_is_bounded(2, 2)
        )
        self.assertFalse(
            verify._legacy_codex_omission_residual_is_bounded(
                capture.MAX_CODEX_LINE_BYTES * 2 + 1,
                2,
            )
        )
        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        legacy = json.loads(json.dumps(original))
        legacy[0]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[-1]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[event_index] = {
            "projection_omitted": True,
            "reason": "maximum-depth",
        }
        legacy_path, legacy_item = self._write_projection_variant(
            legacy,
            bundle["manifest_item"],
            "legacy-maximum-depth-gap.jsonl.gz",
        )
        verify._verify_codex_projection(
            legacy_path,
            legacy_item,
            bundle["projection_event"],
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
        )

        current = json.loads(json.dumps(original))
        current[event_index] = {
            "projection_omitted": True,
            "reason": "maximum-depth",
        }
        current_path, current_item = self._write_projection_variant(
            current,
            bundle["manifest_item"],
            "current-maximum-depth-gap.jsonl.gz",
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "current Codex projection has an unbound omission",
        ):
            verify._verify_codex_projection(
                current_path,
                current_item,
                bundle["projection_event"],
                allowed_session_thread_ids=frozenset({"root-thread"}),
                session_lineage_metadata={"root-thread": ("root-thread", None)},
            )

    def test_codex_projection_redaction_prefilter_preserves_all_pattern_results(self) -> None:
        fixtures = {
            "github-stateless-installation-token": (
                b"ghs_subject_abcdefghijklmnopqrstuvwxyz."
                b"abcdefghijklmnopqrstuvwxyz.abcdefghijklmnopqrstuvwxyz"
            ),
            "github-token": b"ghp_" + b"A" * 24,
            "github-fine-grained-token": b"github_pat_" + b"A" * 24,
            "openai-token": b"sk-" + b"A" * 24,
            "anthropic-token": b"sk-ant-" + b"A" * 24,
            "npm-granular-token": b"npm_" + b"A" * 36,
            "aws-access-key": b"AKIA" + b"A" * 16,
            "aws-temporary-access-key": b"ASIA" + b"A" * 16,
            "google-api-key": b"AIza" + b"A" * 35,
            "google-oauth-client-secret": b"GOCSPX-" + b"A" * 28,
            "gitlab-token": b"glpat-" + b"A" * 20,
            "pypi-token": b"pypi-AgEIcHlwaS5vcmc" + b"A" * 30,
            "slack-token": b"xoxb-" + b"A" * 20,
            "slack-app-token": b"xapp-1-" + b"A" * 40,
            "hugging-face-token": b"hf_" + b"A" * 34,
            "stripe-live-secret": b"sk_live_" + b"A" * 24,
            "sendgrid-api-key": b"SG." + b"A" * 16 + b"." + b"B" * 32,
            "docker-access-token": b"dckr_pat_" + b"A" * 20,
            "slack-webhook": (
                b"https://hooks.slack.com/services/"
                + b"A" * 8
                + b"/"
                + b"B" * 8
                + b"/"
                + b"C" * 16
            ),
            "bearer-token": b"Authorization: Bearer " + b"A" * 16,
            "basic-authorization": b"Authorization: Basic " + b"A" * 12,
            "session-cookie": b"Cookie: sessionid=" + b"A" * 20,
            "oauth-callback-code": b"https://example.invalid/?code=" + b"A" * 12,
            "database-credential-url": (
                b"DATABASE_URL=postgresql://owner:password@db.invalid/app"
            ),
            "userinfo-credential-url": b"https://owner:password@example.invalid/",
            "assigned-secret": b'token: "synthetic-value"',
            "assigned-secret-unquoted": b"token=synthetic-value",
            "signed-url": b"https://example.invalid/?sig=" + b"A" * 16,
        }
        patterns = dict(capture.FIXED_LENGTH_REDACTION_PATTERNS)
        self.assertEqual(
            set(patterns),
            set(verify._FIXED_LENGTH_REDACTION_MANDATORY_MARKERS),
        )

        def original_result(raw: bytes) -> str | None:
            try:
                for category, pattern in capture.FIXED_LENGTH_REDACTION_PATTERNS:
                    for match in pattern.finditer(raw):
                        captured = match.group(1)
                        verify._expect(
                            captured
                            and all(byte == ord("X") for byte in captured),
                            (
                                "Codex projection contains unredacted secret "
                                f"category {category}"
                            ),
                        )
            except verify.EvidenceVerificationError as error:
                return str(error)
            return None

        def optimised_result(raw: bytes) -> str | None:
            try:
                verify._verify_fixed_length_projection_redactions(raw)
            except verify.EvidenceVerificationError as error:
                return str(error)
            return None

        for category, raw in fixtures.items():
            with self.subTest(category=category):
                self.assertIsNotNone(patterns[category].search(raw))
                self.assertEqual(original_result(raw), optimised_result(raw))
                redacted, _, _ = capture.redact_projection_bytes(raw)
                self.assertEqual(original_result(redacted), optimised_result(redacted))

    def test_codex_projection_redaction_prefilter_skips_and_falls_back_safely(self) -> None:
        class CountingPattern:
            def __init__(self) -> None:
                self.calls = 0

            def finditer(self, _: bytes) -> tuple[()]:
                self.calls += 1
                return ()

        configured = CountingPattern()
        unknown = CountingPattern()
        safe = b'{"message":"' + b"safe governed geospatial output " * 32_768 + b'"}\n'
        with mock.patch.object(
            verify,
            "FIXED_LENGTH_REDACTION_PATTERNS",
            (
                ("openai-token", configured),
                ("future-secret-category", unknown),
            ),
        ):
            verify._verify_fixed_length_projection_redactions(safe)
        self.assertEqual(0, configured.calls)
        self.assertEqual(1, unknown.calls)

    def test_codex_projection_reuses_record_normalisation_for_its_payload(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        values = self._projection_values(bundle)
        with mock.patch.object(
            verify,
            "_redact_codex_projection_value",
            wraps=verify._redact_codex_projection_value,
        ) as normalise:
            verify._verify_codex_projection(
                bundle["observed"][
                    bundle["manifest_item"]["object_sha256"]
                ],
                bundle["manifest_item"],
                bundle["projection_event"],
            )
        self.assertEqual(len(values), normalise.call_count)

    def test_historical_codex_user_message_allows_only_exact_local_path_drift(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        legacy = json.loads(json.dumps(original))
        legacy[0]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[-1]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[event_index]["payload"]["message"] = (
            "Inspect /var/example/evidence.txt safely"
        )
        legacy_path, legacy_item = self._write_projection_variant(
            legacy,
            bundle["manifest_item"],
            "legacy-local-path.jsonl.gz",
        )
        verify._verify_codex_projection(
            legacy_path,
            legacy_item,
            bundle["projection_event"],
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
        )

        intermediate = json.loads(json.dumps(legacy))
        intermediate[0]["schema"] = capture.INTERMEDIATE_CODEX_PROJECTION_SCHEMA
        intermediate[-1]["schema"] = capture.INTERMEDIATE_CODEX_PROJECTION_SCHEMA
        intermediate_path, intermediate_item = self._write_projection_variant(
            intermediate,
            bundle["manifest_item"],
            "intermediate-local-path.jsonl.gz",
        )
        verify._verify_codex_projection(
            intermediate_path,
            intermediate_item,
            bundle["projection_event"],
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
        )

        for schema_label, historical in (
            ("legacy", legacy),
            ("intermediate", intermediate),
        ):
            for number, timestamp in enumerate(
                (
                    "https://example.invalid/observation?trace=synthetic#private",
                    "data:image/png;base64,AA==",
                )
            ):
                hostile = json.loads(json.dumps(historical))
                hostile[event_index]["timestamp"] = timestamp
                hostile_path, hostile_item = self._write_projection_variant(
                    hostile,
                    bundle["manifest_item"],
                    f"{schema_label}-local-path-plus-top-level-drift-{number}.jsonl.gz",
                )
                with self.assertRaisesRegex(
                    verify.EvidenceVerificationError,
                    "bypasses capture redaction",
                ):
                    verify._verify_codex_projection(
                        hostile_path,
                        hostile_item,
                        bundle["projection_event"],
                        allowed_session_thread_ids=frozenset({"root-thread"}),
                        session_lineage_metadata={"root-thread": ("root-thread", None)},
                    )

        current = json.loads(json.dumps(legacy))
        current[0]["schema"] = capture.CODEX_PROJECTION_SCHEMA
        current[-1]["schema"] = capture.CODEX_PROJECTION_SCHEMA
        current_path, current_item = self._write_projection_variant(
            current,
            bundle["manifest_item"],
            "current-local-path.jsonl.gz",
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "bypasses capture redaction",
        ):
            verify._verify_codex_projection(
                current_path,
                current_item,
                bundle["projection_event"],
                allowed_session_thread_ids=frozenset({"root-thread"}),
                session_lineage_metadata={"root-thread": ("root-thread", None)},
            )

    def test_current_codex_maximum_depth_uses_digest_bound_stub(self) -> None:
        sessions = self.root / "sessions-current-maximum-depth"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        nested: object = "leaf"
        for _ in range(10):
            nested = {"child": nested}
        source.write_bytes(
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "root-thread",
                            "session_id": "root-thread",
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "name": "bounded.call",
                            "arguments": nested,
                        },
                    },
                )
            )
        )
        source.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        event = next(
            item
            for item in self.journal()
            if item["source"]["kind"] == "codex-user-visible-projection"
        )
        observed = verify._object_paths(self.store)
        raw = gzip.decompress(observed[event["objects"][0]["sha256"]].read_bytes())
        values = [
            capture.parse_json(line, "current maximum-depth projection")
            for line in raw.splitlines(keepends=True)
        ]
        self.assertNotIn(
            {"projection_omitted": True, "reason": "maximum-depth"},
            values,
        )
        stub = next(
            value
            for value in values
            if value.get("source_type") == "projection:maximum-depth"
        )
        self.assertEqual("excluded-rollout-record", stub["record"])
        self.assertRegex(stub["source_line_sha256"], r"^[0-9a-f]{64}$")
        self.assertGreater(stub["source_bytes"], 0)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_current_codex_redaction_must_reach_a_fixed_point(self) -> None:
        sessions = self.root / "sessions-current-redaction-fixed-point"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        nested: object = "{invalid-structured-text"
        for _ in range(6):
            nested = {"child": nested}
        source.write_bytes(
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "root-thread",
                            "session_id": "root-thread",
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "mcp_tool_call_end",
                            "result": nested,
                        },
                    },
                )
            )
        )
        source.chmod(0o600)
        projected, _ = capture._codex_event_projection(
            {"type": "mcp_tool_call_end", "result": nested}
        )
        candidate = {
            "record": "projected-rollout-record",
            "source_line": 2,
            "source_line_sha256": "a" * 64,
            "source_bytes": 1,
            "source_type": "event_msg",
            "payload": projected,
        }
        first, _, _ = capture._redact_codex_projection_value(candidate)
        second, second_categories, _ = capture._redact_codex_projection_value(first)
        self.assertNotEqual(first, second)
        self.assertIn("maximum-depth", second_categories)
        with self.assertRaises(capture._CodexProjectionRedactionNotStable):
            capture._redact_codex_projection_fixed_point(candidate)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        event = next(
            item
            for item in self.journal()
            if item["source"]["kind"] == "codex-user-visible-projection"
        )
        observed = verify._object_paths(self.store)
        raw = gzip.decompress(observed[event["objects"][0]["sha256"]].read_bytes())
        values = [
            capture.parse_json(line, "current fixed-point projection")
            for line in raw.splitlines(keepends=True)
        ]
        stub = next(
            value
            for value in values
            if value.get("source_type") == "projection:redaction-maximum-depth"
        )
        self.assertEqual("excluded-rollout-record", stub["record"])
        self.assertRegex(stub["source_line_sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_current_codex_byte_masking_cannot_write_invalid_structured_text(self) -> None:
        sessions = self.root / "sessions-byte-redaction-fixed-point"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        tool_record = {
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": "bounded.call",
                "arguments": {
                    "database_url": (
                        "postgres" + "://fixture-reader:fixture-password@"
                        'database.example.invalid/catalogue"quoted'
                    )
                },
            },
        }
        source.write_bytes(
            capture.canonical_json(
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                }
            )
            + capture.canonical_json(tool_record)
        )
        source.chmod(0o600)
        first, categories, _ = capture._redact_codex_projection_fixed_point(tool_record)
        self.assertEqual(tool_record, first)
        masked, byte_categories, _ = capture.redact_projection_bytes(
            capture.canonical_json(first)
        )
        self.assertIn("database-credential-url", byte_categories)
        with self.assertRaises(capture.EvidenceCaptureError):
            capture.parse_json(masked, "synthetic byte masking")
        with self.assertRaises(capture._CodexProjectionRedactionNotStable):
            capture._require_codex_projection_final_fixed_point(
                masked, categories + byte_categories
            )

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        event = next(
            item
            for item in self.journal()
            if item["source"]["kind"] == "codex-user-visible-projection"
        )
        observed = verify._object_paths(self.store)
        raw = gzip.decompress(observed[event["objects"][0]["sha256"]].read_bytes())
        self.assertNotIn(b"database_url", raw)
        values = [capture.parse_json(line, "byte masking projection") for line in raw.splitlines()]
        stub = next(
            value
            for value in values
            if value.get("source_type") == "projection:redaction-fixed-point"
        )
        self.assertEqual("excluded-rollout-record", stub["record"])
        self.assertEqual(
            hashlib.sha256(capture.canonical_json(tool_record)).hexdigest(),
            stub["source_line_sha256"],
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_final_codex_bytes_reject_normalisation_and_canonical_drift(self) -> None:
        for label, raw in (
            ("structured-redaction", capture.canonical_json({"text": "analysis: SYNTHETIC"})),
            ("canonical-order", b'{"z":1,"a":2}\n'),
        ):
            with self.subTest(case=label):
                with self.assertRaises(capture._CodexProjectionRedactionNotStable):
                    capture._require_codex_projection_final_fixed_point(raw, [])

    def test_unchanged_codex_bytes_reuse_the_existing_fixed_point_proof(self) -> None:
        with mock.patch.object(
            capture,
            "_require_codex_projection_final_fixed_point",
            wraps=capture._require_codex_projection_final_fixed_point,
        ) as final_guard:
            self._capture_minimal_codex_generation()
        final_guard.assert_not_called()
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_changed_codex_bytes_and_secret_fallback_receive_final_verification(self) -> None:
        for label, message in (
            ("masked", "ghp_" + "S" * 24),
            ("fallback", PRIVATE_KEY_HEADER),
        ):
            with self.subTest(case=label):
                sessions = self.root / f"sessions-final-guard-{label}"
                sessions.mkdir(mode=0o700)
                source = sessions / "root.jsonl"
                source.write_bytes(
                    capture.canonical_json(
                        {
                            "type": "session_meta",
                            "payload": {
                                "id": "root-thread",
                                "session_id": "root-thread",
                                "timestamp": "2026-08-30T08:00:00Z",
                            },
                        }
                    )
                    + capture.canonical_json(
                        {"type": "event_msg", "payload": {"type": "user_message", "message": message}}
                    )
                )
                source.chmod(0o600)
                case_store = self.root / f"store-final-guard-{label}"
                with (
                    mock.patch.object(
                        capture,
                        "_require_codex_projection_final_fixed_point",
                        wraps=capture._require_codex_projection_final_fixed_point,
                    ) as final_guard,
                    capture.private_umask(),
                    capture.EvidenceStore(case_store) as store,
                ):
                    capture.capture_codex_thread_closure(
                        store,
                        thread_id="root-thread",
                        session_roots=[sessions],
                        trigger="pre-compaction",
                        clone_function=fake_clone,
                        filesystem_type_function=apfs,
                    )
                final_guard.assert_called_once()
                guarded_bytes = final_guard.call_args.args[0]
                self.assertNotIn(message.encode(), guarded_bytes)
                guarded = capture.parse_json(guarded_bytes, "synthetic final guard")
                self.assertEqual(
                    "projected-rollout-record" if label == "masked" else "excluded-rollout-record",
                    guarded["record"],
                )
                self.assertTrue(verify.verify_store(case_store)["verified"])

    def test_final_codex_guard_needs_one_normalisation(self) -> None:
        value = {"message": "safe visible output"}
        with mock.patch.object(
            capture,
            "_redact_codex_projection_value",
            wraps=capture._redact_codex_projection_value,
        ) as normalise:
            capture._require_codex_projection_final_fixed_point(
                capture.canonical_json(value), []
            )
        normalise.assert_called_once_with(value)

    def test_codex_canonical_bytes_reject_nonfinite_numbers(self) -> None:
        for value in (float("inf"), float("-inf"), float("nan")):
            with self.subTest(value=str(value)):
                with self.assertRaises(capture._CodexProjectionRedactionNotStable):
                    capture._canonical_codex_projection_json({"value": value})
        for value in (0, -0.0, 1.25, 1e308):
            with self.subTest(value=value):
                self.assertEqual(
                    capture.canonical_json({"value": value}),
                    capture._canonical_codex_projection_json({"value": value}),
                )
        for raw in (b'{"value":1e999}\n', b'{"value":-1e999}\n'):
            with self.subTest(raw=raw):
                with self.assertRaises(capture._CodexProjectionRedactionNotStable):
                    capture._require_codex_projection_final_fixed_point(raw, [])

    def test_codex_numeric_overflow_uses_digest_bound_omission(self) -> None:
        sessions = self.root / "sessions-numeric-overflow"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        source_lines = [
            capture.canonical_json(
                {
                    "type": "session_meta",
                    "payload": {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                }
            )
        ]
        source_lines.extend(
            b'{"type":"event_msg","payload":{"type":"mcp_tool_call_end","result":'
            + number
            + b"}}\n"
            for number in (b"1e999", b"-1e999")
        )
        source.write_bytes(b"".join(source_lines))
        source.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        event = next(
            item
            for item in self.journal()
            if item["source"]["kind"] == "codex-user-visible-projection"
        )
        observed = verify._object_paths(self.store)
        raw = gzip.decompress(observed[event["objects"][0]["sha256"]].read_bytes())
        self.assertNotIn(b"Infinity", raw)
        self.assertNotIn(b"NaN", raw)
        records = [capture.parse_json(line, "finite projection") for line in raw.splitlines()]
        stubs = [
            value
            for value in records
            if value.get("source_type") == "projection:redaction-fixed-point"
        ]
        self.assertEqual(2, len(stubs))
        for line_number, stub in enumerate(stubs, start=2):
            self.assertEqual("excluded-rollout-record", stub["record"])
            self.assertEqual(line_number, stub["source_line"])
            self.assertEqual(len(source_lines[line_number - 1]), stub["source_bytes"])
            self.assertEqual(
                hashlib.sha256(source_lines[line_number - 1]).hexdigest(),
                stub["source_line_sha256"],
            )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_invalid_codex_header_or_footer_aborts_capture(self) -> None:
        original_redactor = capture.redact_projection_bytes
        original_serialiser = capture._canonical_codex_projection_json
        for target, failure_stage in (
            (target, stage)
            for target in ("projection-header", "projection-footer")
            for stage in ("byte-mask", "nonfinite-number")
        ):
            with self.subTest(record=target, stage=failure_stage):
                sessions = self.root / f"sessions-{target}-{failure_stage}"
                sessions.mkdir(mode=0o700)
                source = sessions / "root.jsonl"
                source.write_bytes(
                    capture.canonical_json(
                        {
                            "type": "session_meta",
                            "payload": {
                                "id": "root-thread",
                                "session_id": "root-thread",
                                "timestamp": "2026-08-30T08:00:00Z",
                            },
                        }
                    )
                )
                source.chmod(0o600)
                case_store = self.root / f"store-{target}-{failure_stage}"

                def invalid_byte_redaction(raw: bytes) -> tuple[bytes, list[str], int]:
                    redacted, categories, count = original_redactor(raw)
                    if (
                        failure_stage == "byte-mask"
                        and capture.parse_json(raw, "synthetic redactor").get("record") == target
                    ):
                        # Reported redaction metadata must not decide whether a
                        # changed output needs its final-byte proof.
                        self.assertEqual(([], 0), (categories, count))
                        return redacted[:-1] + b"}\n", categories, count
                    return redacted, categories, count

                def nonfinite_serialisation(value: object) -> bytes:
                    if (
                        failure_stage == "nonfinite-number"
                        and isinstance(value, dict)
                        and value.get("record") == target
                    ):
                        return original_serialiser({**value, "value": float("inf")})
                    return original_serialiser(value)

                with (
                    mock.patch.object(
                        capture, "redact_projection_bytes", side_effect=invalid_byte_redaction
                    ),
                    mock.patch.object(
                        capture, "_canonical_codex_projection_json", side_effect=nonfinite_serialisation
                    ),
                    self.assertRaises(capture._CodexProjectionRedactionNotStable),
                    capture.private_umask(),
                    capture.EvidenceStore(case_store) as store,
                ):
                    capture.capture_codex_thread_closure(
                        store,
                        thread_id="root-thread",
                        session_roots=[sessions],
                        trigger="pre-compaction",
                        clone_function=fake_clone,
                        filesystem_type_function=apfs,
                    )
                self.assertEqual([], capture.read_journal(case_store / "journal.jsonl"))

    def test_intermediate_v2_depth_drift_is_verified_but_not_reused(self) -> None:
        sessions = self.root / "sessions-intermediate-v2-depth-drift"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        nested: object = "{invalid-structured-text"
        for _ in range(6):
            nested = {"child": nested}
        source.write_bytes(
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "root-thread",
                            "session_id": "root-thread",
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "mcp_tool_call_end",
                            "result": nested,
                        },
                    },
                )
            )
        )
        source.chmod(0o600)
        with (
            mock.patch.object(
                capture,
                "CODEX_PROJECTION_SCHEMA",
                capture.INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
            ),
            mock.patch.object(
                capture,
                "_redact_codex_projection_fixed_point",
                side_effect=capture._redact_codex_projection_value,
            ),
            # Reconstruct the historical pipeline before either fixed-point gate.
            mock.patch.object(capture, "_require_codex_projection_final_fixed_point"),
            capture.private_umask(),
            capture.EvidenceStore(self.store) as store,
        ):
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )

        self.assertTrue(verify.verify_store(self.store)["verified"])
        records = capture._iter_explicit_codex_records([sessions])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual({}, capture._reusable_codex_projections(store, records))
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="daily-safety-sweep",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(4, len(self.journal()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_legacy_codex_wrapper_depth_is_split_normalised_only(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        nested: object = "leaf"
        for _ in range(7):
            nested = {"child": nested}
        legacy = json.loads(json.dumps(original))
        legacy[0]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[-1]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[event_index]["source_type"] = "response_item"
        legacy[event_index]["payload"] = {
            "type": "function_call",
            "name": "bounded.call",
            "arguments": nested,
        }
        self.assertTrue(capture._codex_value_exceeds_depth(legacy[event_index]))
        self.assertTrue(
            all(
                not capture._codex_value_exceeds_depth(child)
                for child in legacy[event_index].values()
            )
        )
        legacy_path, legacy_item = self._write_projection_variant(
            legacy,
            bundle["manifest_item"],
            "legacy-wrapper-depth.jsonl.gz",
        )
        verify._verify_codex_projection(
            legacy_path,
            legacy_item,
            bundle["projection_event"],
            allowed_session_thread_ids=frozenset({"root-thread"}),
            session_lineage_metadata={"root-thread": ("root-thread", None)},
        )

        current = json.loads(json.dumps(legacy))
        current[0]["schema"] = capture.CODEX_PROJECTION_SCHEMA
        current[-1]["schema"] = capture.CODEX_PROJECTION_SCHEMA
        current_path, current_item = self._write_projection_variant(
            current,
            bundle["manifest_item"],
            "current-wrapper-depth.jsonl.gz",
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "bypasses capture redaction",
        ):
            verify._verify_codex_projection(
                current_path,
                current_item,
                bundle["projection_event"],
                allowed_session_thread_ids=frozenset({"root-thread"}),
                session_lineage_metadata={"root-thread": ("root-thread", None)},
            )

    def test_legacy_codex_wrapper_does_not_bypass_aggregate_node_cap(self) -> None:
        def exact_node_tree(nodes: int) -> object:
            if nodes == 1:
                return 0
            children = min(65, nodes - 1)
            quotient, remainder = divmod(nodes - 1, children)
            return [
                exact_node_tree(quotient + (1 if index < remainder else 0))
                for index in range(children)
            ]

        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        legacy = json.loads(json.dumps(original))
        legacy[0]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[-1]["schema"] = capture.LEGACY_CODEX_PROJECTION_SCHEMA
        legacy[event_index]["source_type"] = "response_item"
        legacy[event_index]["payload"] = {
            "type": "function_call",
            "name": "bounded.call",
            "arguments": exact_node_tree(99_992),
        }
        self.assertTrue(capture._codex_value_exceeds_depth(legacy[event_index]))
        self.assertFalse(
            verify._codex_value_has_only_depth_overflow(legacy[event_index])
        )
        node_cap_path, node_cap_item = self._write_projection_variant(
            legacy,
            bundle["manifest_item"],
            "legacy-wrapper-node-cap.jsonl.gz",
        )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "bypasses capture redaction",
        ):
            verify._verify_codex_projection(
                node_cap_path,
                node_cap_item,
                bundle["projection_event"],
                allowed_session_thread_ids=frozenset({"root-thread"}),
                session_lineage_metadata={"root-thread": ("root-thread", None)},
            )

    def test_codex_projection_uses_transient_clone_when_live_source_appends(self) -> None:
        sessions = self.root / "sessions"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        values = [
            {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "root-thread",
                    "session_id": "root-thread",
                    "timestamp": "2026-08-30T08:00:00Z",
                },
            },
            {
                "type": "event_msg",
                "payload": {"type": "user_message", "message": "snapshot-visible"},
            },
        ]
        source.write_text(
            "".join(json.dumps(value) + "\n" for value in values), encoding="utf-8"
        )
        source.chmod(0o644)

        def clone_then_append(source_path: Path, destination: Path) -> None:
            shutil.copyfile(source_path, destination)
            with source_path.open("a", encoding="utf-8") as stream:
                stream.write(
                    json.dumps(
                        {
                            "type": "event_msg",
                            "payload": {
                                "type": "user_message",
                                "message": "appended-after-clone",
                            },
                        }
                    )
                    + "\n"
                )

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=clone_then_append,
                filesystem_type_function=apfs,
            )
        projection = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        self.assertTrue(projection["source"]["source_changed_after_snapshot"])
        digest = projection["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest
        text = gzip.decompress(object_path.read_bytes()).decode("utf-8")
        self.assertIn("snapshot-visible", text)
        self.assertNotIn("appended-after-clone", text)
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_closure_accepts_append_after_immutable_projection_snapshot(self) -> None:
        sessions = self.root / "sessions-append-after-projection"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        source.write_text(
            json.dumps(
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        source.chmod(0o600)
        original_inventory = capture._iter_explicit_codex_records
        inventory_calls = 0

        def append_before_final_inventory(
            roots: list[Path],
        ) -> list[capture.CodexSessionRecord]:
            nonlocal inventory_calls
            inventory_calls += 1
            if inventory_calls == 2:
                with source.open("a", encoding="utf-8") as stream:
                    stream.write(
                        json.dumps(
                            {
                                "type": "event_msg",
                                "payload": {
                                    "type": "user_message",
                                    "message": "appended-after-projection",
                                },
                            }
                        )
                        + "\n"
                    )
            return original_inventory(roots)

        with mock.patch.object(
            capture,
            "_iter_explicit_codex_records",
            side_effect=append_before_final_inventory,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                captured = capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )
        self.assertEqual(1, captured)
        projection = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        digest = projection["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest
        text = gzip.decompress(object_path.read_bytes()).decode("utf-8")
        self.assertNotIn("appended-after-projection", text)
        source_stat_before = projection["source"]["source_stat_before"]
        source_stat_after = projection["source"]["source_stat_after"]
        self.assertFalse(projection["source"]["source_changed_after_snapshot"])
        self.assertEqual(source_stat_before, source_stat_after)
        manifest_event = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        manifest_digest = manifest_event["objects"][0]["sha256"]
        manifest_path = (
            self.store
            / "objects"
            / "sha256"
            / manifest_digest[:2]
            / manifest_digest
        )
        manifest_item = json.loads(manifest_path.read_text(encoding="utf-8"))["files"][0]
        final_stat = manifest_item["source_stat_final_observation"]
        self.assertTrue(manifest_item["source_changed_by_final_observation"])
        self.assertEqual(source.stat().st_size, final_stat["bytes"])
        self.assertGreater(final_stat["bytes"], source_stat_before["bytes"])
        footer = next(
            json.loads(line)
            for line in text.splitlines()
            if json.loads(line).get("record") == "projection-footer"
        )
        self.assertEqual(source_stat_after, footer["source_stat_after"])
        self.assertEqual(source_stat_before["bytes"], footer["source_bytes"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_closure_records_same_size_rewrite_after_projection(self) -> None:
        sessions = self.root / "sessions-rewrite-after-projection"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        values = [
            {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "root-thread",
                    "session_id": "root-thread",
                    "timestamp": "2026-08-30T08:00:00Z",
                },
            },
            {
                "type": "event_msg",
                "payload": {"type": "user_message", "message": "before"},
            },
        ]
        source.write_text(
            "".join(json.dumps(value) + "\n" for value in values),
            encoding="utf-8",
        )
        source.chmod(0o600)
        original_inventory = capture._iter_explicit_codex_records
        inventory_calls = 0

        def rewrite_before_final_inventory(
            roots: list[Path],
        ) -> list[capture.CodexSessionRecord]:
            nonlocal inventory_calls
            inventory_calls += 1
            if inventory_calls == 2:
                original = source.read_bytes()
                rewritten = original.replace(b'"message": "before"', b'"message": "after!"')
                self.assertEqual(len(original), len(rewritten))
                source.write_bytes(rewritten)
                source.chmod(0o600)
            return original_inventory(roots)

        with mock.patch.object(
            capture,
            "_iter_explicit_codex_records",
            side_effect=rewrite_before_final_inventory,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )
        projection = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        source_stat_before = projection["source"]["source_stat_before"]
        source_stat_after = projection["source"]["source_stat_after"]
        self.assertEqual(source_stat_before, source_stat_after)
        self.assertFalse(projection["source"]["source_changed_after_snapshot"])
        manifest_event = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        manifest_digest = manifest_event["objects"][0]["sha256"]
        manifest_path = (
            self.store
            / "objects"
            / "sha256"
            / manifest_digest[:2]
            / manifest_digest
        )
        manifest_item = json.loads(manifest_path.read_text(encoding="utf-8"))["files"][0]
        final_stat = manifest_item["source_stat_final_observation"]
        self.assertEqual(source_stat_before["bytes"], final_stat["bytes"])
        self.assertTrue(manifest_item["source_changed_by_final_observation"])
        self.assertNotEqual(
            (source_stat_before["mtime_ns"], source_stat_before["ctime_ns"]),
            (final_stat["mtime_ns"], final_stat["ctime_ns"]),
        )
        digest = projection["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest
        text = gzip.decompress(object_path.read_bytes()).decode("utf-8")
        self.assertIn("before", text)
        self.assertNotIn("after!", text)
        footer = next(
            json.loads(line)
            for line in text.splitlines()
            if json.loads(line).get("record") == "projection-footer"
        )
        self.assertEqual(source_stat_after, footer["source_stat_after"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_closure_records_reused_source_change_then_reprojects_next_sweep(self) -> None:
        sessions = self.root / "sessions-reused-change"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        source.write_text(
            json.dumps(
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        source.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        original_events = self.journal()
        original_inventory = capture._iter_explicit_codex_records
        inventory_calls = 0

        def append_before_final_inventory(
            roots: list[Path],
        ) -> list[capture.CodexSessionRecord]:
            nonlocal inventory_calls
            inventory_calls += 1
            if inventory_calls == 2:
                with source.open("a", encoding="utf-8") as stream:
                    stream.write(
                        json.dumps(
                            {
                                "type": "event_msg",
                                "payload": {
                                    "type": "user_message",
                                    "message": "new-generation",
                                },
                            }
                        )
                        + "\n"
                    )
            return original_inventory(roots)

        with mock.patch.object(
            capture,
            "_iter_explicit_codex_records",
            side_effect=append_before_final_inventory,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )
        after_observation = self.journal()
        self.assertEqual(len(original_events) + 1, len(after_observation))
        observation_manifest_event = after_observation[-1]
        self.assertEqual(
            "codex-thread-closure-generation-manifest",
            observation_manifest_event["source"]["kind"],
        )
        observation_manifest_digest = observation_manifest_event["objects"][0]["sha256"]
        observation_manifest_path = (
            self.store
            / "objects"
            / "sha256"
            / observation_manifest_digest[:2]
            / observation_manifest_digest
        )
        observation_item = json.loads(
            observation_manifest_path.read_text(encoding="utf-8")
        )["files"][0]
        self.assertTrue(observation_item["source_changed_by_final_observation"])
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        original_projection = next(
            event
            for event in original_events
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        old_stable_stat = original_projection["source"]["source_stat_before"]
        current_records = original_inventory([sessions])
        with mock.patch.object(
            capture,
            "_recorded_source_stat",
            return_value=old_stable_stat,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                self.assertEqual(
                    {},
                    capture._reusable_codex_projections(store, current_records),
                )
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertGreater(len(self.journal()), len(after_observation))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_closure_rejects_duplicate_thread_identity_before_staging(self) -> None:
        sessions = self.root / "sessions-duplicate"
        sessions.mkdir(mode=0o700)
        record = {
            "timestamp": "2026-08-30T08:00:00Z",
            "type": "session_meta",
            "payload": {
                "id": "root-thread",
                "session_id": "same-session",
                "timestamp": "2026-08-30T08:00:00Z",
            },
        }
        for name in ("first.jsonl", "second.jsonl"):
            path = sessions / name
            path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            path.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "duplicate thread identity",
            ):
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )
        self.assertEqual([], self.journal())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_codex_closure_uses_parent_graph_when_threads_share_a_session(self) -> None:
        sessions = self.root / "sessions-shared-root"
        sessions.mkdir(mode=0o700)

        def write_rollout(name: str, thread: str, parent: str | None) -> None:
            payload: dict[str, object] = {
                "id": thread,
                "session_id": "shared-session",
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if parent is not None:
                payload["parent_thread_id"] = parent
            path = sessions / name
            path.write_text(
                json.dumps(
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": payload,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            path.chmod(0o600)

        write_rollout("root.jsonl", "root-thread", None)
        write_rollout("child.jsonl", "child-thread", "root-thread")
        write_rollout("unrelated.jsonl", "unrelated-thread", None)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            captured = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(2, captured)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_closure_rejects_self_parent_and_cycles(self) -> None:
        def write_rollout(
            directory: Path,
            name: str,
            thread: str,
            parent: str | None,
        ) -> None:
            payload: dict[str, object] = {
                "id": thread,
                "session_id": "shared-session",
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if parent is not None:
                payload["parent_thread_id"] = parent
            path = directory / name
            path.write_text(
                json.dumps(
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": payload,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            path.chmod(0o600)

        self_parent = self.root / "sessions-self-parent"
        self_parent.mkdir(mode=0o700)
        write_rollout(self_parent, "self.jsonl", "self-thread", "self-thread")
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "self-parent"):
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="self-thread",
                    session_roots=[self_parent],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )

        cycle_store = self.root / "cycle-store"
        cycle_sessions = self.root / "sessions-cycle"
        cycle_sessions.mkdir(mode=0o700)
        write_rollout(cycle_sessions, "root.jsonl", "cycle-root", "cycle-child")
        write_rollout(cycle_sessions, "child.jsonl", "cycle-child", "cycle-root")
        with capture.private_umask(), capture.EvidenceStore(cycle_store) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "parent cycle"):
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="cycle-root",
                    session_roots=[cycle_sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )

        external_store = self.root / "external-parent-store"
        external_sessions = self.root / "sessions-external-parent"
        external_sessions.mkdir(mode=0o700)
        write_rollout(external_sessions, "child.jsonl", "selected-child", "outside-parent")
        with capture.private_umask(), capture.EvidenceStore(external_store) as store:
            captured = capture.capture_codex_thread_closure(
                store,
                thread_id="selected-child",
                session_roots=[external_sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(1, captured)
        self.assertTrue(verify.verify_store(external_store)["verified"])

    def test_codex_projection_rejects_path_replacement_during_clone(self) -> None:
        sessions = self.root / "sessions-replaced"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"

        def rollout(thread_id: str) -> bytes:
            return (
                json.dumps(
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": thread_id,
                            "session_id": thread_id,
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")

        source.write_bytes(rollout("root-thread"))
        source.chmod(0o600)
        original = source.stat()

        def replace_then_clone(source_path: Path, destination: Path) -> None:
            replacement = source_path.with_suffix(".replacement")
            replacement.write_bytes(rollout("evil-thread"))
            replacement.chmod(0o600)
            os.utime(replacement, ns=(original.st_atime_ns, original.st_mtime_ns))
            os.replace(replacement, source_path)
            shutil.copyfile(source_path, destination)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "identity changed while cloning|metadata differs",
            ):
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=replace_then_clone,
                    filesystem_type_function=apfs,
                )
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_codex_closure_enforces_cumulative_staging_boundary(self) -> None:
        sessions = self.root / "sessions-bounded"
        sessions.mkdir(mode=0o700)

        def write_rollout(path: Path, thread_id: str, parent: str | None) -> None:
            values = [
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": thread_id,
                        "session_id": thread_id,
                        "parent_thread_id": parent,
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": os.urandom(2_048).hex(),
                    },
                },
            ]
            path.write_text(
                "".join(json.dumps(value) + "\n" for value in values),
                encoding="utf-8",
            )
            path.chmod(0o600)

        write_rollout(sessions / "root.jsonl", "root-thread", None)
        write_rollout(sessions / "child.jsonl", "child-thread", "root-thread")
        with capture.private_umask(), capture.EvidenceStore(
            self.store,
            max_capture_bytes=capture.MAX_METADATA_BYTES + 7_000,
        ) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "byte boundary"):
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )
        self.assertEqual([], self.journal())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_codex_closure_recovers_retained_excluded_and_manifest_batch(self) -> None:
        sessions = self.root / "sessions-recoverable-batch"
        sessions.mkdir(mode=0o700)

        def write_rollout(
            path: Path,
            thread_id: str,
            parent: str | None,
            timestamp: str,
            message: str,
        ) -> None:
            path.write_bytes(
                b"".join(
                    capture.canonical_json(value)
                    for value in (
                        {
                            "timestamp": timestamp,
                            "type": "session_meta",
                            "payload": {
                                "id": thread_id,
                                "session_id": thread_id,
                                "parent_thread_id": parent,
                                "timestamp": timestamp,
                            },
                        },
                        {
                            "timestamp": timestamp,
                            "type": "event_msg",
                            "payload": {
                                "type": "user_message",
                                "message": message,
                            },
                        },
                    )
                )
            )
            path.chmod(0o600)

        write_rollout(
            sessions / "root.jsonl",
            "root-thread",
            None,
            "2026-08-30T08:00:00Z",
            "safe visible request",
        )
        write_rollout(
            sessions / "child.jsonl",
            "child-thread",
            "root-thread",
            "2026-08-30T08:01:00Z",
            f"{PRIVATE_KEY_HEADER}\nexcluded rather than retained",
        )

        def inject(point: str) -> None:
            if point == "after-staged-unlink":
                raise RuntimeError("synthetic closure batch crash")

        with self.assertRaisesRegex(RuntimeError, "closure batch crash"):
            with capture.private_umask(), capture.EvidenceStore(
                self.store,
                fault_injector=inject,
            ) as store:
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                )

        self.assertTrue((self.store / capture.PENDING_EVENT_NAME).exists())
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual(3, store.summary()["journal_events"])
        events = self.journal()
        self.assertEqual(
            [
                "codex-user-visible-projection",
                "codex-user-visible-projection",
                "codex-thread-closure-generation-manifest",
            ],
            [event["source"]["kind"] for event in events],
        )
        self.assertEqual(
            ["captured", "excluded", "captured"],
            [event["disposition"]["status"] for event in events],
        )
        self.assertFalse((self.store / capture.PENDING_EVENT_NAME).exists())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

        observed = verify._object_paths(self.store)
        manifest_event = events[-1]
        manifest_digest = manifest_event["objects"][0]["sha256"]
        manifest = capture.parse_json(
            observed[manifest_digest].read_bytes(),
            "mixed-disposition generation manifest",
        )
        projection_event = events[0]
        self._rewrite_captured_generation_projection_schema(
            {
                "events": events,
                "observed": observed,
                "projection_event": projection_event,
                "manifest_event": manifest_event,
                "manifest": manifest,
                "manifest_item": manifest["files"][0],
            },
            capture.LEGACY_CODEX_PROJECTION_SCHEMA,
        )
        records = capture._iter_explicit_codex_records([sessions])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual({}, capture._reusable_codex_projections(store, records))
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            captured = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="daily-safety-sweep",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(2, captured)
        self.assertEqual(5, len(self.journal()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_verifier_rejects_projection_without_completion_manifest(self) -> None:
        source = capture._source_value(
            kind="codex-user-visible-projection",
            identity="codex-user-visible-projection:test:partial",
            label="partial.jsonl",
            occurred_at_utc="2026-08-30T08:00:00.000Z",
            expires_at_utc=None,
            expiry_basis="unknown",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="fixed-length-high-confidence-projection-redaction",
            snapshot_method="streamed-user-visible-projection",
            source_stat_before={
                "device": 1,
                "inode": 2,
                "mode": 0o600,
                "links": 1,
                "owner_uid": os.getuid(),
                "bytes": 3,
                "mtime_ns": 4,
                "ctime_ns": 5,
            },
            source_stat_after={
                "device": 1,
                "inode": 2,
                "mode": 0o600,
                "links": 1,
                "owner_uid": os.getuid(),
                "bytes": 3,
                "mtime_ns": 4,
                "ctime_ns": 5,
            },
            source_changed_after_snapshot=False,
            collection_generation_sha256=None,
            collection_window=None,
            redaction_categories=[],
            redaction_count=0,
        )
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            staged = capture.stage_bytes(b"not-a-retained-raw-rollout", store.incoming, max_bytes=100)
            store.commit_staged(
                staged,
                trigger="manual",
                repository=None,
                source=source,
                role="codex-user-visible-projection-gzip",
                media_type="application/gzip",
                opaque=False,
                secret_scan="fixed-length-high-confidence-redaction-completed",
                secret_scan_performed=True,
                sensitivity="owner-only-redacted",
            )
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "partial"):
            verify.verify_store(self.store)

    def _capture_minimal_codex_generation(self) -> dict[str, object]:
        sessions = self.root / "minimal-codex-sessions"
        sessions.mkdir(mode=0o700)
        source = sessions / "root.jsonl"
        source.write_bytes(
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "root-thread",
                            "session_id": "root-thread",
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {"type": "user_message", "message": "visible request"},
                    },
                )
            )
        )
        source.chmod(0o644)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        events = self.journal()
        observed = verify._object_paths(self.store)
        projection_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        manifest_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        manifest_digest = manifest_event["objects"][0]["sha256"]
        manifest = capture.parse_json(
            observed[manifest_digest].read_bytes(),
            "test Codex generation manifest",
        )
        return {
            "events": events,
            "observed": observed,
            "projection_event": projection_event,
            "manifest_event": manifest_event,
            "manifest": manifest,
            "manifest_item": manifest["files"][0],
        }

    def _projection_values(self, bundle: dict[str, object]) -> list[dict[str, object]]:
        item = bundle["manifest_item"]
        observed = bundle["observed"]
        raw = gzip.decompress(observed[item["object_sha256"]].read_bytes())
        return [
            capture.parse_json(line, f"test projection line {number}")
            for number, line in enumerate(raw.splitlines(keepends=True), start=1)
        ]

    def _rewrite_captured_generation_projection_schema(
        self,
        bundle: dict[str, object],
        projection_schema: str,
    ) -> None:
        """Rewrite a captured test generation with complete durable bindings."""

        values = self._projection_values(bundle)
        values[0]["schema"] = projection_schema
        values[-1]["schema"] = projection_schema
        uncompressed = b"".join(capture.canonical_json(value) for value in values)
        output = io.BytesIO()
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as stream:
            stream.write(uncompressed)
        compressed = output.getvalue()

        events = json.loads(json.dumps(bundle["events"]))
        projection_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        old_projection_digest = projection_event["objects"][0]["sha256"]
        self.replace_event_object(projection_event, compressed)
        new_projection_digest = projection_event["objects"][0]["sha256"]
        old_identity = projection_event["source"]["identity"]
        new_identity = old_identity.replace(
            f"projection-sha256:{old_projection_digest}",
            f"projection-sha256:{new_projection_digest}",
        )
        self.assertNotEqual(old_identity, new_identity)
        projection_event["source"]["identity"] = new_identity
        projection_event["source"]["identity_sha256"] = capture.source_identity_sha256(
            new_identity
        )

        manifest = json.loads(json.dumps(bundle["manifest"]))
        item = manifest["files"][0]
        item["source_identity"] = new_identity
        item["source_identity_sha256"] = capture.source_identity_sha256(new_identity)
        item["object_sha256"] = new_projection_digest
        item["object_bytes"] = len(compressed)
        item["uncompressed_sha256"] = capture.sha256_bytes(uncompressed)
        item["uncompressed_bytes"] = len(uncompressed)
        generation_material = {
            "schema": capture.CODEX_GENERATION_SCHEMA,
            "thread_id": manifest["thread_id"],
            "selection_rule": manifest["selection_rule"],
            "files": manifest["files"],
            "boundaries": capture.BOUNDARIES,
        }
        generation = capture.sha256_bytes(capture.canonical_json(generation_material))
        manifest["collection_generation_sha256"] = generation

        manifest_event = next(
            event
            for event in events
            if event["source"]["kind"]
            == "codex-thread-closure-generation-manifest"
        )
        manifest_identity = f"codex-thread-closure:generation:{generation}:manifest"
        manifest_event["source"]["identity"] = manifest_identity
        manifest_event["source"]["identity_sha256"] = capture.source_identity_sha256(
            manifest_identity
        )
        manifest_event["source"]["collection_generation_sha256"] = generation
        self.replace_event_object(
            manifest_event,
            capture.canonical_json(manifest, pretty=True),
        )
        self.rewrite_journal(events)

    def _write_projection_variant(
        self,
        values: list[dict[str, object]],
        manifest_item: dict[str, object],
        name: str,
    ) -> tuple[Path, dict[str, object]]:
        uncompressed = b"".join(capture.canonical_json(value) for value in values)
        path = self.root / name
        with path.open("wb") as output:
            with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as stream:
                stream.write(uncompressed)
        path.chmod(0o600)
        item = json.loads(json.dumps(manifest_item))
        item["uncompressed_sha256"] = capture.sha256_bytes(uncompressed)
        item["uncompressed_bytes"] = len(uncompressed)
        return path, item

    def _write_manifest_variant(
        self,
        bundle: dict[str, object],
        manifest: dict[str, object],
        name: str,
    ) -> tuple[list[dict[str, object]], dict[str, Path]]:
        generation_material = {
            "schema": capture.CODEX_GENERATION_SCHEMA,
            "thread_id": manifest["thread_id"],
            "selection_rule": manifest["selection_rule"],
            "files": manifest["files"],
            "boundaries": capture.BOUNDARIES,
        }
        generation = capture.sha256_bytes(capture.canonical_json(generation_material))
        manifest["collection_generation_sha256"] = generation
        raw = capture.canonical_json(manifest, pretty=True)
        digest = capture.sha256_bytes(raw)
        path = private_file(self.root / name, raw)
        events = json.loads(json.dumps(bundle["events"]))
        manifest_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        identity = f"codex-thread-closure:generation:{generation}:manifest"
        manifest_event["source"]["identity"] = identity
        manifest_event["source"]["identity_sha256"] = capture.source_identity_sha256(identity)
        manifest_event["source"]["collection_generation_sha256"] = generation
        manifest_event["objects"][0]["sha256"] = digest
        manifest_event["objects"][0]["bytes"] = len(raw)
        observed = dict(bundle["observed"])
        observed[digest] = path
        return events, observed

    def test_verify_store_invokes_codex_generation_verification(self) -> None:
        self._capture_minimal_codex_generation()
        with mock.patch.object(
            verify,
            "_verify_codex_generations",
            wraps=verify._verify_codex_generations,
        ) as generation_check:
            self.assertTrue(verify.verify_store(self.store)["verified"])
        generation_check.assert_called_once()

    def test_verifier_progress_is_bounded_path_free_and_available_to_cli(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        progress: list[dict[str, object]] = []
        with mock.patch.object(verify, "CODEX_VERIFICATION_PROGRESS_BYTES", 1):
            result = verify.verify_store(
                self.store,
                progress_function=lambda value: progress.append(dict(value)),
            )
        self.assertTrue(result["verified"])

        integrity_progress = [
            item
            for item in progress
            if str(item["stage"]).startswith("store-integrity-")
        ]
        self.assertEqual("store-integrity-start", integrity_progress[0]["stage"])
        self.assertEqual("store-integrity-complete", integrity_progress[-1]["stage"])
        integrity_keys = {
            "stage",
            "completed_objects",
            "total_objects",
            "completed_object_bytes",
            "total_object_bytes",
            "elapsed_seconds",
        }
        self.assertTrue(
            all(set(item) == integrity_keys for item in integrity_progress)
        )
        self.assertEqual(0, integrity_progress[0]["completed_objects"])
        self.assertEqual(0, integrity_progress[0]["completed_object_bytes"])
        self.assertEqual(result["objects"], integrity_progress[-1]["completed_objects"])
        self.assertEqual(result["bytes"], integrity_progress[-1]["completed_object_bytes"])
        self.assertEqual(result["bytes"], integrity_progress[-1]["total_object_bytes"])
        for key in (
            "completed_objects",
            "completed_object_bytes",
            "elapsed_seconds",
        ):
            self.assertEqual(
                sorted(item[key] for item in integrity_progress),
                [item[key] for item in integrity_progress],
            )

        codex_progress = [
            item
            for item in progress
            if str(item["stage"]).startswith("codex-verification-")
        ]
        self.assertEqual("codex-verification-start", codex_progress[0]["stage"])
        self.assertEqual("codex-verification-complete", codex_progress[-1]["stage"])
        self.assertIn(
            "codex-verification-progress",
            [item["stage"] for item in codex_progress],
        )
        expected_keys = {
            "stage",
            "completed_projections",
            "total_projections",
            "completed_projection_bytes",
            "elapsed_seconds",
        }
        self.assertTrue(all(set(item) == expected_keys for item in codex_progress))
        self.assertEqual(0, codex_progress[0]["completed_projections"])
        self.assertEqual(0, codex_progress[0]["completed_projection_bytes"])
        self.assertEqual(1, codex_progress[-1]["completed_projections"])
        self.assertEqual(1, codex_progress[-1]["total_projections"])
        self.assertEqual(
            bundle["manifest_item"]["uncompressed_bytes"],
            codex_progress[-1]["completed_projection_bytes"],
        )
        for key in (
            "completed_projections",
            "completed_projection_bytes",
            "elapsed_seconds",
        ):
            self.assertEqual(
                sorted(item[key] for item in codex_progress),
                [item[key] for item in codex_progress],
            )
        middle = [
            item
            for item in codex_progress
            if item["stage"] == "codex-verification-progress"
        ]
        self.assertTrue(any(item["completed_projections"] == 0 for item in middle))
        self.assertTrue(all(item["completed_projection_bytes"] > 0 for item in middle))
        self.assertNotIn(str(self.root), json.dumps(progress, sort_keys=True))
        arguments = verify.parser().parse_args(
            ["--store", str(self.store), "--progress", "--workers", "4"]
        )
        self.assertTrue(arguments.progress)
        self.assertEqual(4, arguments.workers)

    def test_parallel_codex_projection_verification_matches_serial_results(self) -> None:
        self._capture_minimal_codex_generation()
        sessions = self.root / "second-minimal-codex-sessions"
        sessions.mkdir(mode=0o700)
        source = sessions / "other.jsonl"
        source.write_bytes(
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:01:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "other-thread",
                            "session_id": "other-thread",
                            "timestamp": "2026-08-30T08:01:00Z",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "message": "second visible request",
                        },
                    },
                )
            )
        )
        source.chmod(0o644)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="other-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        events = self.journal()
        observed = verify._object_paths(self.store)
        serial_progress: list[dict[str, object]] = []
        parallel_progress: list[dict[str, object]] = []
        with mock.patch.object(verify, "CODEX_VERIFICATION_PROGRESS_BYTES", 1):
            serial = verify._verify_codex_generations(
                events,
                observed,
                progress_function=lambda value: serial_progress.append(dict(value)),
            )
            parallel = verify._verify_codex_generations(
                events,
                observed,
                progress_function=lambda value: parallel_progress.append(dict(value)),
                workers=2,
            )
        self.assertEqual(serial, parallel)
        self.assertTrue(parallel)
        self.assertEqual(
            serial_progress[-1]["completed_projection_bytes"],
            parallel_progress[-1]["completed_projection_bytes"],
        )
        self.assertEqual(2, parallel_progress[-1]["completed_projections"])
        for key in (
            "completed_projections",
            "completed_projection_bytes",
            "elapsed_seconds",
        ):
            self.assertEqual(
                sorted(item[key] for item in parallel_progress),
                [item[key] for item in parallel_progress],
            )
        self.assertNotIn(str(self.root), json.dumps(parallel_progress, sort_keys=True))

    def test_parallel_projection_errors_are_raised_in_manifest_order(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        values = self._projection_values(bundle)
        first_values = [json.loads(json.dumps(values[0]))]
        first_values.append(json.loads(json.dumps(values[1])))
        for source_line in range(2, 2_002):
            repeated = json.loads(json.dumps(values[2]))
            repeated["source_line"] = source_line
            first_values.append(repeated)
        first_error = json.loads(json.dumps(values[2]))
        first_error["source_line"] = 2_003
        first_values.append(first_error)
        first_values.append(json.loads(json.dumps(values[-1])))
        first_path, first_item = self._write_projection_variant(
            first_values,
            bundle["manifest_item"],
            "first-invalid-projection.jsonl.gz",
        )

        second_values = json.loads(json.dumps(values))
        second_values[1]["record"] = "invalid-projection-record"
        second_path, second_item = self._write_projection_variant(
            second_values,
            bundle["manifest_item"],
            "second-invalid-projection.jsonl.gz",
        )
        source_event = bundle["projection_event"]
        lineage = frozenset({"root-thread"})
        metadata = {"root-thread": ("root-thread", None)}
        tasks = [
            (
                "first",
                first_path,
                first_item,
                source_event,
                lineage,
                metadata,
            ),
            (
                "second",
                second_path,
                second_item,
                source_event,
                lineage,
                metadata,
            ),
        ]
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "Codex source-line sequence differs",
        ):
            verify._verify_codex_projections_parallel(
                tasks,
                workers=2,
                progress_bytes_function=None,
                completed_function=lambda _: None,
            )

    def test_parallel_progress_failure_suppresses_reporting_after_25_completions(
        self,
    ) -> None:
        bundle = self._capture_minimal_codex_generation()
        item = bundle["manifest_item"]
        path = bundle["observed"][item["object_sha256"]]
        source_event = bundle["projection_event"]
        lineage = frozenset({"root-thread"})
        metadata = {"root-thread": ("root-thread", None)}
        tasks = [
            (
                f"projection-{index}",
                path,
                item,
                source_event,
                lineage,
                metadata,
            )
            for index in range(30)
        ]
        callback_calls = 0

        def fail_on_first_progress(_: int) -> None:
            nonlocal callback_calls
            callback_calls += 1
            raise RuntimeError(f"synthetic callback failure at {self.root}")

        with mock.patch.object(verify, "CODEX_VERIFICATION_PROGRESS_BYTES", 1):
            with self.assertRaisesRegex(
                verify.EvidenceVerificationError,
                "Codex projection progress reporting failed closed",
            ) as raised:
                verify._verify_codex_projections_parallel(
                    tasks,
                    workers=1,
                    progress_bytes_function=fail_on_first_progress,
                    completed_function=lambda _: None,
                )
        self.assertEqual(1, callback_calls)
        self.assertNotIn(str(self.root), str(raised.exception))

    def test_parallel_completion_callback_failure_is_attempted_once(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        item = bundle["manifest_item"]
        path = bundle["observed"][item["object_sha256"]]
        source_event = bundle["projection_event"]
        lineage = frozenset({"root-thread"})
        metadata = {"root-thread": ("root-thread", None)}
        tasks = [
            (
                f"projection-{index}",
                path,
                item,
                source_event,
                lineage,
                metadata,
            )
            for index in range(3)
        ]
        completion_calls = 0

        def fail_on_first_completion(_: str) -> None:
            nonlocal completion_calls
            completion_calls += 1
            raise RuntimeError(f"synthetic completion failure at {self.root}")

        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "Codex projection progress reporting failed closed",
        ) as raised:
            verify._verify_codex_projections_parallel(
                tasks,
                workers=1,
                progress_bytes_function=None,
                completed_function=fail_on_first_completion,
            )
        self.assertEqual(1, completion_calls)
        self.assertNotIn(str(self.root), str(raised.exception))

    def test_worker_count_is_closed_and_capture_reuse_remains_serial(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        for workers in (False, 0, 5):
            with self.subTest(workers=workers):
                with self.assertRaisesRegex(
                    verify.EvidenceVerificationError,
                    "worker count is invalid",
                ):
                    verify.verify_store(self.store, workers=workers)
        with self.assertRaises(SystemExit), mock.patch("sys.stderr", io.StringIO()):
            verify.parser().parse_args(
                ["--store", str(self.store), "--workers", "5"]
            )

        manifest_identity = bundle["manifest_event"]["source"]["identity"]
        with mock.patch.object(
            verify,
            "_verify_codex_projections_parallel",
            side_effect=AssertionError("capture reuse must remain serial"),
        ):
            self.assertTrue(
                verify._verify_codex_generations(
                    bundle["events"],
                    bundle["observed"],
                    required_projection_schema=capture.CODEX_PROJECTION_SCHEMA,
                    workers=2,
                )
            )
            reused = verify.validate_reusable_codex_generation(
                self.store,
                bundle["events"],
                manifest_identity,
                required_projection_schema=capture.CODEX_PROJECTION_SCHEMA,
            )
        self.assertIsNotNone(reused)

    def test_reuse_deeply_rejects_semantically_invalid_canonical_manifest(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        events = bundle["events"]
        manifest_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        manifest = json.loads(json.dumps(bundle["manifest"]))
        manifest["selected_file_count"] = 999
        replacement = capture.canonical_json(manifest, pretty=True)
        self.replace_event_object(manifest_event, replacement)
        self.rewrite_journal(events)
        sessions = self.root / "minimal-codex-sessions"
        records = capture._iter_explicit_codex_records([sessions])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "prior Codex generation failed semantic validation",
            ) as failure:
                capture._reusable_codex_projections(store, records)
        self.assertNotIn(str(self.root), str(failure.exception))
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_reuse_rejects_in_memory_event_drift_from_durable_journal(self) -> None:
        self._capture_minimal_codex_generation()
        sessions = self.root / "minimal-codex-sessions"
        records = capture._iter_explicit_codex_records([sessions])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            manifest_event = next(
                event
                for event in store.events
                if event["source"]["kind"]
                == "codex-thread-closure-generation-manifest"
            )
            manifest_event["objects"][0]["bytes"] += 1
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "prior Codex generation failed semantic validation",
            ):
                capture._reusable_codex_projections(store, records)
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_legacy_generation_is_authenticated_but_not_deeply_reused(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        self._rewrite_captured_generation_projection_schema(
            bundle,
            capture.LEGACY_CODEX_PROJECTION_SCHEMA,
        )
        sessions = self.root / "minimal-codex-sessions"
        records = capture._iter_explicit_codex_records([sessions])
        with mock.patch.object(
            verify,
            "_verify_codex_projected_payload",
            side_effect=AssertionError("legacy body should not be walked for reuse"),
        ) as projected_payload:
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                self.assertEqual({}, capture._reusable_codex_projections(store, records))
        projected_payload.assert_not_called()

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            count = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="daily-safety-sweep",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        self.assertEqual(1, count)
        self.assertEqual(4, len(self.journal()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_reuse_schema_preflight_rejects_compressed_object_digest_drift(self) -> None:
        self._capture_minimal_codex_generation()
        projection_event = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        digest = projection_event["objects"][0]["sha256"]
        path = self.store / "objects" / "sha256" / digest[:2] / digest
        raw = bytearray(path.read_bytes())
        raw[-1] ^= 1
        path.write_bytes(raw)
        path.chmod(0o600)
        sessions = self.root / "minimal-codex-sessions"
        records = capture._iter_explicit_codex_records([sessions])
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "prior Codex generation failed semantic validation",
            ):
                capture._reusable_codex_projections(store, records)
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_reuse_schema_validation_rejects_path_replacement_after_hashing(self) -> None:
        self._capture_minimal_codex_generation()
        projection_event = next(
            event
            for event in self.journal()
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        digest = projection_event["objects"][0]["sha256"]
        path = self.store / "objects" / "sha256" / digest[:2] / digest
        original_verifier = verify._verify_codex_generations
        replaced = False

        def replace_path_then_verify(*args: object, **kwargs: object) -> bool:
            nonlocal replaced
            replacement = path.with_name(f"{digest}.replacement")
            private_file(replacement, path.read_bytes())
            os.replace(replacement, path)
            replaced = True
            return original_verifier(*args, **kwargs)

        sessions = self.root / "minimal-codex-sessions"
        records = capture._iter_explicit_codex_records([sessions])
        with mock.patch.object(
            verify,
            "_verify_codex_generations",
            side_effect=replace_path_then_verify,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                with self.assertRaisesRegex(
                    capture.EvidenceCaptureError,
                    "prior Codex generation failed semantic validation",
                ):
                    capture._reusable_codex_projections(store, records)
        self.assertTrue(replaced)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_unchanged_all_excluded_generation_is_a_repeatable_no_op(self) -> None:
        sessions = self.root / "all-excluded-sessions"
        sessions.mkdir(mode=0o700)
        private_file(
            sessions / "root.jsonl",
            b"".join(
                capture.canonical_json(value)
                for value in (
                    {
                        "timestamp": "2026-08-30T08:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "root-thread",
                            "session_id": "root-thread",
                            "timestamp": "2026-08-30T08:00:00Z",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "message": f"{PRIVATE_KEY_HEADER}\nnot retained",
                        },
                    },
                )
            ),
        )
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="pre-compaction",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
            )
        before = self.journal()
        self.assertEqual(
            ["excluded", "captured"],
            [event["disposition"]["status"] for event in before],
        )
        progress: list[dict[str, object]] = []
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="daily-safety-sweep",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
                progress_function=lambda value: progress.append(dict(value)),
            )
            summary = store.summary()
        self.assertEqual(before, self.journal())
        self.assertGreaterEqual(summary["no_op"], 2)
        self.assertEqual("commit-complete", progress[-1]["stage"])
        self.assertEqual(1, progress[-1]["reused_files"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_valid_unchanged_codex_generation_reuse_is_a_true_no_op(self) -> None:
        self._capture_minimal_codex_generation()
        before = self.journal()
        sessions = self.root / "minimal-codex-sessions"
        progress: list[dict[str, object]] = []
        with mock.patch.object(
            verify,
            "_verify_codex_generations",
            wraps=verify._verify_codex_generations,
        ) as generation_check:
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                count = capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-thread",
                    session_roots=[sessions],
                    trigger="daily-safety-sweep",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                    progress_function=lambda value: progress.append(dict(value)),
                )
                summary = store.summary()
        self.assertEqual(1, count)
        self.assertEqual(before, self.journal())
        self.assertGreaterEqual(summary["no_op"], 2)
        self.assertEqual([], list((self.store / ".incoming").iterdir()))
        self.assertEqual("commit-complete", progress[-1]["stage"])
        self.assertEqual(1, progress[-1]["reused_files"])
        self.assertEqual(0, progress[-1]["staged_projection_bytes"])
        generation_check.assert_called()
        self.assertTrue(
            any(
                call.kwargs.get("required_projection_schema")
                == capture.CODEX_PROJECTION_SCHEMA
                for call in generation_check.call_args_list
            )
        )

    def test_codex_capture_progress_is_aggregate_path_free_and_committed_last(self) -> None:
        sessions = self.root / "progress-sessions"
        sessions.mkdir(mode=0o700)

        def write_rollout(name: str, thread: str, parent: str | None) -> None:
            payload: dict[str, object] = {
                "id": thread,
                "session_id": "progress-session",
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if parent is not None:
                payload["parent_thread_id"] = parent
            private_file(
                sessions / name,
                b"".join(
                    capture.canonical_json(value)
                    for value in (
                        {
                            "timestamp": "2026-08-30T08:00:00Z",
                            "type": "session_meta",
                            "payload": payload,
                        },
                        {
                            "type": "event_msg",
                            "payload": {"type": "user_message", "message": "visible"},
                        },
                    )
                ),
            )

        write_rollout("root.jsonl", "root-thread", None)
        write_rollout("child.jsonl", "child-thread", "root-thread")
        progress: list[dict[str, object]] = []
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            count = capture.capture_codex_thread_closure(
                store,
                thread_id="root-thread",
                session_roots=[sessions],
                trigger="feature-completed",
                clone_function=fake_clone,
                filesystem_type_function=apfs,
                progress_function=lambda value: progress.append(dict(value)),
            )
        self.assertEqual(2, count)
        self.assertEqual(
            [
                "inventory-complete",
                "reuse-validation-start",
                "reuse-validation-complete",
                "projection-progress",
                "final-topology-start",
                "final-topology-complete",
                "commit-start",
                "commit-complete",
            ],
            [item["stage"] for item in progress],
        )
        expected_keys = {
            "stage",
            "completed_files",
            "total_files",
            "completed_source_bytes",
            "total_source_bytes",
            "staged_projection_bytes",
            "reused_files",
            "elapsed_seconds",
        }
        self.assertTrue(all(set(item) == expected_keys for item in progress))
        for key in (
            "completed_files",
            "completed_source_bytes",
            "staged_projection_bytes",
            "reused_files",
            "elapsed_seconds",
        ):
            self.assertEqual(
                sorted(item[key] for item in progress),
                [item[key] for item in progress],
            )
        rendered = json.dumps(progress, sort_keys=True)
        self.assertNotIn(str(self.root), rendered)
        self.assertNotIn("root-thread", rendered)
        self.assertNotIn("progress-session", rendered)
        self.assertEqual(2, progress[-1]["completed_files"])
        self.assertEqual(2, progress[-1]["total_files"])
        self.assertEqual(3, len(self.journal()))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_codex_progress_does_not_claim_commit_when_topology_changes(self) -> None:
        sessions = self.root / "progress-topology-sessions"
        sessions.mkdir(mode=0o700)
        private_file(
            sessions / "root.jsonl",
            capture.canonical_json(
                {
                    "timestamp": "2026-08-30T08:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": "root-thread",
                        "session_id": "root-thread",
                        "timestamp": "2026-08-30T08:00:00Z",
                    },
                }
            ),
        )
        original_inventory = capture._iter_explicit_codex_records
        inventory_calls = 0

        def add_child_before_final_inventory(
            roots: list[Path],
        ) -> list[capture.CodexSessionRecord]:
            nonlocal inventory_calls
            inventory_calls += 1
            if inventory_calls == 2:
                private_file(
                    sessions / "new-child.jsonl",
                    capture.canonical_json(
                        {
                            "timestamp": "2026-08-30T08:00:00Z",
                            "type": "session_meta",
                            "payload": {
                                "id": "new-child-thread",
                                "session_id": "new-child-thread",
                                "parent_thread_id": "root-thread",
                                "timestamp": "2026-08-30T08:00:00Z",
                            },
                        }
                    ),
                )
            return original_inventory(roots)

        progress: list[dict[str, object]] = []
        with mock.patch.object(
            capture,
            "_iter_explicit_codex_records",
            side_effect=add_child_before_final_inventory,
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                with self.assertRaisesRegex(
                    capture.EvidenceCaptureError,
                    "closure topology changed",
                ):
                    capture.capture_codex_thread_closure(
                        store,
                        thread_id="root-thread",
                        session_roots=[sessions],
                        trigger="pre-compaction",
                        clone_function=fake_clone,
                        filesystem_type_function=apfs,
                        progress_function=lambda value: progress.append(dict(value)),
                    )
        stages = [item["stage"] for item in progress]
        self.assertIn("final-topology-start", stages)
        self.assertNotIn("final-topology-complete", stages)
        self.assertNotIn("commit-start", stages)
        self.assertNotIn("commit-complete", stages)
        self.assertEqual([], self.journal())
        self.assertEqual([], list((self.store / ".incoming").iterdir()))

    def test_codex_reuse_is_bound_to_current_transitive_lineage(self) -> None:
        sessions = self.root / "lineage-reuse-sessions"
        sessions.mkdir(mode=0o700)
        shared_session = "shared-session"

        def session_meta(thread: str, parent: str | None = None) -> dict[str, object]:
            payload: dict[str, object] = {
                "id": thread,
                "session_id": shared_session,
                "timestamp": "2026-08-30T08:00:00Z",
            }
            if parent is not None:
                payload["parent_thread_id"] = parent
            return {
                "timestamp": "2026-08-30T08:00:00Z",
                "type": "session_meta",
                "payload": payload,
            }

        root = sessions / "root-a.jsonl"
        parent = sessions / "parent.jsonl"
        child = sessions / "child.jsonl"
        root.write_bytes(capture.canonical_json(session_meta("root-a")))
        parent.write_bytes(
            capture.canonical_json(session_meta("parent-thread", "root-a"))
        )
        child.write_bytes(
            capture.canonical_json(session_meta("child-thread", "parent-thread"))
            + capture.canonical_json(session_meta("root-a"))
        )
        for source in (root, parent, child):
            source.chmod(0o600)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual(
                3,
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="root-a",
                    session_roots=[sessions],
                    trigger="pre-compaction",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                ),
            )
        first_events = self.journal()
        first_observed = verify._object_paths(self.store)
        first_manifest_event = next(
            event
            for event in first_events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        )
        first_manifest = capture.parse_json(
            first_observed[first_manifest_event["objects"][0]["sha256"]].read_bytes(),
            "test first lineage manifest",
        )
        first_child = next(
            item for item in first_manifest["files"] if item["thread_id"] == "child-thread"
        )

        parent.write_bytes(
            capture.canonical_json(session_meta("parent-thread", "root-b"))
        )
        parent.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            self.assertEqual(
                2,
                capture.capture_codex_thread_closure(
                    store,
                    thread_id="parent-thread",
                    session_roots=[sessions],
                    trigger="post-topology-change",
                    clone_function=fake_clone,
                    filesystem_type_function=apfs,
                ),
            )

        events = self.journal()
        observed = verify._object_paths(self.store)
        manifest_events = [
            event
            for event in events
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
        ]
        self.assertEqual(2, len(manifest_events))
        latest_manifest = capture.parse_json(
            observed[manifest_events[-1]["objects"][0]["sha256"]].read_bytes(),
            "test changed lineage manifest",
        )
        latest_child = next(
            item for item in latest_manifest["files"] if item["thread_id"] == "child-thread"
        )
        self.assertNotEqual(first_child["object_sha256"], latest_child["object_sha256"])
        projection = gzip.decompress(
            observed[latest_child["object_sha256"]].read_bytes()
        )
        self.assertNotIn(b'"id":"root-a"', projection)
        self.assertIn(b'"source_type":"session_meta:outside-selected-lineage"', projection)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_manifest_metadata_and_limit_are_checked_before_read(self) -> None:
        digest = "a" * 64
        object_value = {
            "role": "codex-thread-closure-generation-manifest",
            "sha256": digest,
            "bytes": 1,
            "media_type": "application/json",
            "opaque": False,
            "secret_scan": "high-confidence-text-scan-passed",
            "secret_scan_performed": True,
            "sensitivity": "owner-only-redacted",
            "public_projection_eligible": False,
        }
        source = {
            "identity": "codex-thread-closure:generation:test:manifest",
            "kind": "codex-thread-closure-generation-manifest",
            "snapshot_method": "derived-generation-manifest",
            "redaction_mode": "generated-from-owner-only-redacted-projections",
        }
        cases = (
            ("role", "not-a-generation-manifest", "role"),
            ("media_type", "text/plain", "media type"),
            ("bytes", capture.MAX_METADATA_BYTES + 1, "byte boundary"),
        )
        for field, replacement, error in cases:
            with self.subTest(field=field):
                candidate = dict(object_value)
                candidate[field] = replacement
                unread = mock.Mock(name="unread_manifest_path")
                event = {
                    "source": dict(source),
                    "objects": [candidate],
                    "disposition": {"status": "captured", "reason": None},
                }
                with self.assertRaisesRegex(verify.EvidenceVerificationError, error):
                    verify._verify_codex_generations([event], {digest: unread})
                self.assertEqual([], unread.mock_calls)

    def test_verifier_rejects_non_object_and_excluded_projected_payloads(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        event_index = next(
            index
            for index, value in enumerate(original)
            if value.get("source_type") == "event_msg"
        )
        cases = (
            (["not-an-object"], "payload is not an object"),
            ({"type": "agent_reasoning", "text": "not user-visible"}, "event leaked"),
            (
                {
                    "type": "agent_message",
                    "message": {
                        "password": "tiny",
                        "path": f"{MAC_USERS_ROOT}/private-person/secret.txt",
                    },
                },
                "bypasses capture redaction",
            ),
            (
                {
                    "type": "agent_message",
                    "message": f"read {MAC_USERS_ROOT}/private-person/secret.txt",
                },
                "bypasses capture redaction",
            ),
        )
        for number, (payload, error) in enumerate(cases):
            with self.subTest(payload=payload):
                values = json.loads(json.dumps(original))
                values[event_index]["payload"] = payload
                path, item = self._write_projection_variant(
                    values,
                    bundle["manifest_item"],
                    f"invalid-payload-{number}.jsonl.gz",
                )
                with self.assertRaisesRegex(verify.EvidenceVerificationError, error):
                    verify._verify_codex_projection(path, item, bundle["projection_event"])

        values = json.loads(json.dumps(original))
        values[event_index]["timestamp"] = f"{PRIVATE_TMP_ROOT}/owner-only/evidence-store"
        path, item = self._write_projection_variant(
            values,
            bundle["manifest_item"],
            "invalid-top-level-timestamp.jsonl.gz",
        )
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "record bypasses"):
            verify._verify_codex_projection(path, item, bundle["projection_event"])

    def test_verifier_binds_projection_footer_stats_and_source_byte_totals(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        original = self._projection_values(bundle)
        footer_index = next(
            index
            for index, value in enumerate(original)
            if value.get("record") == "projection-footer"
        )
        record_index = next(
            index
            for index, value in enumerate(original)
            if value.get("record") == "projected-rollout-record"
        )
        cases = (
            (footer_index, "source_stat_before", "source stats differ"),
            (record_index, "source_bytes", "source-byte total differs"),
        )
        for number, (index, field, error) in enumerate(cases):
            with self.subTest(field=field):
                values = json.loads(json.dumps(original))
                if field == "source_stat_before":
                    values[index][field]["mtime_ns"] += 1
                else:
                    values[index][field] += 1
                path, item = self._write_projection_variant(
                    values,
                    bundle["manifest_item"],
                    f"invalid-footer-{number}.jsonl.gz",
                )
                with self.assertRaisesRegex(verify.EvidenceVerificationError, error):
                    verify._verify_codex_projection(path, item, bundle["projection_event"])

    def test_verifier_binds_generation_window_count(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        manifest = json.loads(json.dumps(bundle["manifest"]))
        manifest["collection_window"]["selected_files"] += 1
        raw = capture.canonical_json(manifest, pretty=True)
        digest = capture.sha256_bytes(raw)
        path = private_file(self.root / "bad-window-manifest.json", raw)
        manifest_event = json.loads(json.dumps(bundle["manifest_event"]))
        manifest_event["source"]["collection_window"] = manifest["collection_window"]
        manifest_event["objects"][0]["sha256"] = digest
        manifest_event["objects"][0]["bytes"] = len(raw)
        events = [
            manifest_event
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
            else event
            for event in bundle["events"]
        ]
        observed = dict(bundle["observed"])
        observed[digest] = path
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "selected-file count"):
            verify._verify_codex_generations(events, observed)

    def test_verifier_rejects_tampered_codex_final_observations(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        base = json.loads(json.dumps(bundle["manifest"]))
        source_stat_before = bundle["projection_event"]["source"]["source_stat_before"]
        cases: tuple[tuple[str, object, str], ...] = (
            (
                "marker",
                lambda item: item.__setitem__(
                    "source_changed_by_final_observation",
                    not item["source_changed_by_final_observation"],
                ),
                "mutation marker differs",
            ),
            (
                "identity",
                lambda item: (
                    item["source_stat_final_observation"].__setitem__(
                        "inode",
                        item["source_stat_final_observation"]["inode"] + 1,
                    ),
                    item.__setitem__("source_changed_by_final_observation", True),
                ),
                "identity differs",
            ),
            (
                "truncated",
                lambda item: (
                    item["source_stat_final_observation"].__setitem__(
                        "bytes",
                        source_stat_before["bytes"] - 1,
                    ),
                    item.__setitem__("source_changed_by_final_observation", True),
                ),
                "observation is truncated",
            ),
            (
                "missing-field",
                lambda item: item.pop("source_stat_final_observation"),
                "manifest file is not closed",
            ),
            (
                "extra-field",
                lambda item: item.__setitem__("unreviewed_final_stat", {}),
                "manifest file is not closed",
            ),
        )
        for number, (label, mutate, error) in enumerate(cases):
            with self.subTest(label=label):
                manifest = json.loads(json.dumps(base))
                mutate(manifest["files"][0])
                events, observed = self._write_manifest_variant(
                    bundle,
                    manifest,
                    f"invalid-final-observation-{number}.json",
                )
                with self.assertRaisesRegex(verify.EvidenceVerificationError, error):
                    verify._verify_codex_generations(events, observed)

    def test_verifier_rejects_codex_snapshot_identity_change(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        manifest = json.loads(json.dumps(bundle["manifest"]))
        item = manifest["files"][0]
        item["source_stat_final_observation"]["inode"] += 1
        item["source_changed_by_final_observation"] = False
        events, observed = self._write_manifest_variant(
            bundle,
            manifest,
            "invalid-snapshot-identity.json",
        )
        projection_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        projection_event["source"]["source_stat_after"]["inode"] += 1
        projection_event["source"]["source_changed_after_snapshot"] = True
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "snapshot source identity changed",
        ):
            verify._verify_codex_generations(events, observed)

    def test_duplicate_projection_object_is_verified_for_every_manifest_binding(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        second_manifest = json.loads(json.dumps(bundle["manifest"]))
        second_manifest["files"][0]["thread_id"] = "tampered-thread"
        generation_material = {
            "schema": capture.CODEX_GENERATION_SCHEMA,
            "thread_id": second_manifest["thread_id"],
            "selection_rule": second_manifest["selection_rule"],
            "files": second_manifest["files"],
            "boundaries": capture.BOUNDARIES,
        }
        generation = capture.sha256_bytes(capture.canonical_json(generation_material))
        second_manifest["collection_generation_sha256"] = generation
        raw = capture.canonical_json(second_manifest, pretty=True)
        digest = capture.sha256_bytes(raw)
        path = private_file(self.root / "second-generation-manifest.json", raw)
        second_event = json.loads(json.dumps(bundle["manifest_event"]))
        identity = f"codex-thread-closure:generation:{generation}:manifest"
        second_event["source"]["identity"] = identity
        second_event["source"]["identity_sha256"] = capture.source_identity_sha256(identity)
        second_event["source"]["collection_generation_sha256"] = generation
        second_event["objects"][0]["sha256"] = digest
        second_event["objects"][0]["bytes"] = len(raw)
        observed = dict(bundle["observed"])
        observed[digest] = path
        with mock.patch.object(
            verify,
            "_verify_codex_projection",
            wraps=verify._verify_codex_projection,
        ) as projection_check:
            with self.assertRaisesRegex(verify.EvidenceVerificationError, "identity differs"):
                verify._verify_codex_generations(
                    [*bundle["events"], second_event],
                    observed,
                )
        self.assertEqual(2, projection_check.call_count)

    def test_verifier_requires_exact_projection_object_metadata(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        events = json.loads(json.dumps(bundle["events"]))
        projection_event = next(
            event
            for event in events
            if event["source"]["kind"] == "codex-user-visible-projection"
        )
        projection_event["objects"][0]["role"] = "generic-gzip"
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "object role"):
            verify._verify_codex_generations(events, bundle["observed"])

    def test_projection_gzip_scan_bypass_requires_exact_bound_classification(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        projection_object = bundle["projection_event"]["objects"][0]
        claims = [(projection_object, "codex-user-visible-projection")]
        self.assertTrue(verify._is_bound_codex_projection_gzip("gzip", claims))
        self.assertFalse(verify._is_bound_codex_projection_gzip(None, claims))
        self.assertFalse(
            verify._is_bound_codex_projection_gzip(
                "gzip",
                [(projection_object, "local-file")],
            )
        )
        wrong_role = dict(projection_object)
        wrong_role["role"] = "generic-gzip"
        self.assertFalse(
            verify._is_bound_codex_projection_gzip(
                "gzip",
                [(wrong_role, "codex-user-visible-projection")],
            )
        )
        wrong_metadata = dict(projection_object)
        wrong_metadata["media_type"] = "application/octet-stream"
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "object media type",
        ):
            verify._is_bound_codex_projection_gzip(
                "gzip",
                [(wrong_metadata, "codex-user-visible-projection")],
            )

    def test_bound_projection_gzip_skips_only_compressed_binary_secret_scan(self) -> None:
        self._capture_minimal_codex_generation()
        original_scan = verify._scan_secret_binary_stream
        scanned_gzip = False

        def observe_scan(stream: object, *, prefix: bytes = b"") -> None:
            nonlocal scanned_gzip
            position = stream.tell()
            marker = prefix[:2] or stream.read(2)
            stream.seek(position)
            if marker == b"\x1f\x8b":
                scanned_gzip = True
            original_scan(stream, prefix=prefix)

        with mock.patch.object(
            verify,
            "_scan_secret_binary_stream",
            side_effect=observe_scan,
        ):
            self.assertTrue(verify.verify_store(self.store)["verified"])
        self.assertFalse(scanned_gzip)

    def test_projection_label_on_plain_secret_does_not_bypass_generic_scan(self) -> None:
        bundle = self._capture_minimal_codex_generation()
        self.replace_event_object(
            bundle["projection_event"],
            b"AWS_SESSION_TOKEN=synthetic-secret-value-1234567890",
        )
        self.rewrite_journal(bundle["events"])
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "unredacted secret category assigned-secret-unquoted",
        ):
            verify.verify_store(self.store)

    def test_verifier_rejects_projection_values_capture_cannot_emit(self) -> None:
        header = {"thread_id": "thread", "session_id": "session"}
        cases = (
            (
                "event_msg",
                {"type": "user_message", "message": {"safe": "forged"}},
            ),
            (
                "event_msg",
                {"type": "task_complete", "error": {"present": True, "arbitrary": []}},
            ),
            (
                "session_meta",
                {"id": "thread", "session_id": "session", "git": []},
            ),
            (
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "output": [{"type": "text", "text": 123}],
                },
            ),
            (
                "response_item",
                {
                    "type": "custom_tool_call_output",
                    "output": [{"type": "input_image", "url": "javascript:alert(1)"}],
                },
            ),
        )
        for source_type, payload in cases:
            with self.subTest(source_type=source_type, payload=payload):
                with self.assertRaises(verify.EvidenceVerificationError):
                    verify._verify_codex_projected_payload(
                        source_type,
                        payload,
                        header,
                    )

    def test_verifier_keeps_exact_topology_and_lock_protections(self) -> None:
        source = private_file(self.root / "source.txt", b"evidence")
        self.capture_file(source)
        unexpected = private_file(self.store / "unexpected", b"")
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "top-level file"):
            verify.verify_store(self.store)
        unexpected.unlink()

        lock = self.store / ".lock"
        lock.chmod(0o644)
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "store lock"):
            verify.verify_store(self.store)
        lock.chmod(0o600)
        with mock.patch.object(verify.os, "getuid", return_value=os.getuid() + 1):
            with self.assertRaisesRegex(verify.EvidenceVerificationError, "store lock"):
                verify.verify_store(self.store)

    def test_opaque_zip_is_never_extracted(self) -> None:
        archive = self.root / "hostile.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("../../escape", "hostile")
        archive.chmod(0o600)
        self.capture_file(archive)
        event = self.journal()[0]
        self.assertTrue(event["objects"][0]["opaque"])
        self.assertFalse((self.root / "escape").exists())
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_zip_with_real_pkcs8_der_private_key_is_excluded(self) -> None:
        synthetic_test_key = base64.b64decode(
            "MIIBOQIBAAJBAK2ORrEx4J/WlJqnR1sJufL9eMLpWoifGcS4jdectihEmlulMWvs"
            "kahP2N3d74BZCiXEEtuPePCY3id0An4Xk5MCAwEAAQJAV4wUht/VImvYzGajbP3s"
            "CfHoj9GstIwlMIG0M1Y+4PJdEXzavCRRUpGzbwjshXY32iBJ1XIDUfYOAyr9UD3pQ"
            "QIhAOGUMD0zTQ6zLwqVMvDSu8BsvvpziF+0y+dKfc3QgYvzAiEAxPYPKTIyBPPRv"
            "AqrOwejJcYPK5T3PcDTyWfcbFSZ4eECIGnhLXc8YhnZPuY/u4ZP03JxWH6jxcnuSZ"
            "rJWx1EldnDAiB+LF6T9mrij0rZWkBM5VyXMyS+t4QXFDLX/+fNofieIQIgGTvNSS8g"
            "8NY0UEYQ7x+8FoRrBylio1GzNRWch+lE8ig="
        )
        archive_path = self.root / "synthetic-key-container.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("synthetic-test-only.p8", synthetic_test_key)
        archive_path.chmod(0o600)
        summary = self.capture_file(archive_path)
        self.assertEqual(1, summary["excluded"])
        self.assertEqual(0, summary["captured"])
        self.assertIn("private-key-container", self.journal()[0]["disposition"]["reason"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_valid_png_is_the_only_supported_local_opaque_binary(self) -> None:
        def chunk(chunk_type: bytes, content: bytes) -> bytes:
            checksum = zlib.crc32(chunk_type + content) & 0xFFFFFFFF
            return (
                len(content).to_bytes(4, "big")
                + chunk_type
                + content
                + checksum.to_bytes(4, "big")
            )

        header = (
            (1).to_bytes(4, "big")
            + (1).to_bytes(4, "big")
            + bytes((8, 6, 0, 0, 0))
        )
        raw = (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00\x00"))
            + chunk(b"IEND", b"")
        )
        image = private_file(self.root / "screenshot.png", raw)
        summary = self.capture_file(image)
        self.assertEqual(1, summary["captured"])
        event = self.journal()[0]
        self.assertEqual("image/png", event["objects"][0]["media_type"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_png_compressed_text_secret_is_excluded(self) -> None:
        def chunk(chunk_type: bytes, content: bytes) -> bytes:
            checksum = zlib.crc32(chunk_type + content) & 0xFFFFFFFF
            return (
                len(content).to_bytes(4, "big")
                + chunk_type
                + content
                + checksum.to_bytes(4, "big")
            )

        header = (
            (1).to_bytes(4, "big")
            + (1).to_bytes(4, "big")
            + bytes((8, 6, 0, 0, 0))
        )
        secret = b"github_" + b"pat_" + b"A" * 40
        raw = (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"zTXt", b"Comment\x00\x00" + zlib.compress(secret))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00\x00"))
            + chunk(b"IEND", b"")
        )
        image = private_file(self.root / "compressed-secret.png", raw)
        summary = self.capture_file(image)
        self.assertEqual(1, summary["excluded"])
        self.assertEqual(0, summary["captured"])
        self.assertNotIn(secret, (self.store / "journal.jsonl").read_bytes())
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_jpeg_magic_overrides_misleading_png_suffix_and_scans_metadata(self) -> None:
        def segment(marker: int, content: bytes) -> bytes:
            return b"\xff" + bytes((marker,)) + (len(content) + 2).to_bytes(2, "big") + content

        safe = (
            b"\xff\xd8"
            + segment(0xE0, b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
            + segment(0xDA, b"\x01\x01\x00\x00\x3f\x00")
            + b"\x01\x02\xff\x00\x03"
            + b"\xff\xd9"
        )
        image = private_file(self.root / "phone-screenshot.png", safe)
        summary = self.capture_file(image)
        self.assertEqual(1, summary["captured"])
        event = self.journal()[0]
        self.assertEqual("image/jpeg", event["objects"][0]["media_type"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

        secret_store = self.root / "jpeg-secret-store"
        self.store = secret_store
        secret = b"github_" + b"pat_" + b"A" * 40
        hostile = (
            b"\xff\xd8"
            + segment(0xE1, secret)
            + segment(0xDA, b"\x01\x01\x00\x00\x3f\x00")
            + b"\x01\x02\x03"
            + b"\xff\xd9"
        )
        image = private_file(self.root / "metadata-secret.jpg", hostile)
        summary = self.capture_file(image)
        self.assertEqual(1, summary["excluded"])
        self.assertEqual(0, summary["captured"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_opaque_binary_and_disguised_archives_are_scanned(self) -> None:
        secret = b"sk-proj-" + b"A" * 32
        opaque = private_file(self.root / "opaque.bin", b"prefix\x00" + secret)
        summary = self.capture_file(opaque)
        self.assertEqual(1, summary["excluded"])
        self.assertEqual(0, summary["captured"])

        disguised = self.root / "disguised.bin"
        with zipfile.ZipFile(disguised, "w") as archive:
            archive.writestr("secret.txt", secret)
        disguised.chmod(0o600)
        summary = self.capture_file(disguised)
        self.assertEqual(1, summary["excluded"])

        safe_disguised = self.root / "safe-disguised.bin"
        with zipfile.ZipFile(safe_disguised, "w") as archive:
            archive.writestr("evidence.txt", "safe bounded evidence")
        safe_disguised.chmod(0o600)
        self.capture_file(safe_disguised)
        captured = [event for event in self.journal() if event["objects"]]
        self.assertEqual("application/zip", captured[-1]["objects"][0]["media_type"])
        self.assertTrue(captured[-1]["objects"][0]["secret_scan_performed"])

        sfx_zip = io.BytesIO()
        with zipfile.ZipFile(sfx_zip, "w") as archive:
            archive.writestr("secret.txt", secret)
        sfx = private_file(
            self.root / "self-extracting.bin",
            b"synthetic-sfx-stub" + sfx_zip.getvalue(),
        )
        summary = self.capture_file(sfx)
        self.assertEqual(1, summary["excluded"])

        compressed = private_file(self.root / "compressed.bin", b"\x1f\x8bopaque")
        summary = self.capture_file(compressed)
        self.assertEqual(1, summary["unavailable"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

        for name, raw in {
            "prefixed-gzip": b"MZ-SYNTHETIC-STUB" + gzip.compress(secret),
            "wrapped-zip": b"P" * 1024 + sfx_zip.getvalue() + b"T" * 70_000,
            "unknown-opaque": b"safe but unclassified binary\x00payload",
        }.items():
            with self.subTest(name=name):
                store = self.root / f"store-{name}"
                source = private_file(self.root / f"{name}.bin", raw)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        source,
                        trigger="client-observation",
                        repository=None,
                    )
                    self.assertEqual(1, evidence_store.summary()["unavailable"])
                    self.assertEqual(0, evidence_store.summary()["captured"])
                self.assertTrue(verify.verify_store(store)["verified"])

    def test_zip_rejects_named_and_magic_disguised_nested_compression(self) -> None:
        secret = b"github_pat_" + b"A" * 32
        for member_name in ("secret.gz", "innocent.bin"):
            with self.subTest(member_name=member_name):
                archive_path = self.root / f"nested-{member_name.replace('.', '-')}.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr(member_name, gzip.compress(secret))
                archive_path.chmod(0o600)
                store = self.root / f"store-{member_name.replace('.', '-')}"
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    with self.assertRaisesRegex(
                        capture.EvidenceCaptureError,
                        "nested archive or compressed",
                    ):
                        capture.capture_local_file(
                            evidence_store,
                            archive_path,
                            trigger="client-observation",
                            repository=None,
                        )
                self.assertEqual([], capture.read_journal(store / "journal.jsonl"))

        prefixed = self.root / "nested-prefixed-gzip.zip"
        with zipfile.ZipFile(prefixed, "w") as archive:
            archive.writestr("innocent.bin", b"MZ-SYNTHETIC-STUB" + gzip.compress(secret))
        prefixed.chmod(0o600)
        store = self.root / "store-nested-prefixed-gzip"
        with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "nested archive or compressed",
            ):
                capture.capture_local_file(
                    evidence_store,
                    prefixed,
                    trigger="client-observation",
                    repository=None,
                )

    def test_zip_directory_entry_with_payload_is_rejected(self) -> None:
        secret = b"github_" + b"pat_" + b"A" * 32
        archive_path = self.root / "payload-directory.zip"
        entry = zipfile.ZipInfo("hidden/")
        entry.compress_type = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr(entry, secret)
        archive_path.chmod(0o600)
        with capture.private_umask(), capture.EvidenceStore(self.store) as evidence_store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "directory entries cannot contain",
            ):
                capture.capture_local_file(
                    evidence_store,
                    archive_path,
                    trigger="client-observation",
                    repository=None,
                )
        self.assertEqual([], self.journal())

    def test_utf16_secrets_are_excluded_from_binary_and_zip_sources(self) -> None:
        token = "github_" + "pat_" + "A" * 32
        cases = {
            "utf16le-bom": b"\xff\xfe" + token.encode("utf-16-le"),
            "utf16le-no-bom": token.encode("utf-16-le"),
            "utf16be-bom": b"\xfe\xff" + token.encode("utf-16-be"),
            "utf32le-bom": b"\xff\xfe\x00\x00" + token.encode("utf-32-le"),
            "utf32be-bom": b"\x00\x00\xfe\xff" + token.encode("utf-32-be"),
        }
        for name, raw in cases.items():
            with self.subTest(name=name, container="binary"):
                store = self.root / f"store-{name}-binary"
                source = private_file(self.root / f"{name}.bin", raw)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        source,
                        trigger="client-observation",
                        repository=None,
                    )
                    self.assertEqual(1, evidence_store.summary()["excluded"])
                self.assertTrue(verify.verify_store(store)["verified"])

            with self.subTest(name=name, container="zip"):
                store = self.root / f"store-{name}-zip"
                archive_path = self.root / f"{name}.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr("secret.txt", raw)
                archive_path.chmod(0o600)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        archive_path,
                        trigger="client-observation",
                        repository=None,
                    )
                    self.assertEqual(1, evidence_store.summary()["excluded"])
                self.assertTrue(verify.verify_store(store)["verified"])

    def test_zip_secret_shaped_filenames_and_comments_are_excluded(self) -> None:
        token = "github_" + "pat_" + "A" * 32
        cases = {
            "filename": (token, b""),
            "archive-comment": ("safe.txt", token.encode()),
        }
        for name, (member_name, comment) in cases.items():
            with self.subTest(name=name):
                store = self.root / f"store-zip-metadata-{name}"
                archive_path = self.root / f"zip-metadata-{name}.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr(member_name, b"safe content")
                    archive.comment = comment
                archive_path.chmod(0o600)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        archive_path,
                        trigger="client-observation",
                        repository=None,
                    )
                    self.assertEqual(1, evidence_store.summary()["excluded"])
                self.assertTrue(verify.verify_store(store)["verified"])

        safe_zip = io.BytesIO()
        with zipfile.ZipFile(safe_zip, "w") as archive:
            archive.writestr("safe.txt", b"safe content")
        for name, raw in {
            "sfx-prefix": b"MZ-SYNTHETIC-STUB-" + token.encode() + safe_zip.getvalue(),
            "trailing-data": safe_zip.getvalue() + b"-TRAILER-" + token.encode(),
            "sfx-prefix-utf16le": token.encode("utf-16-le") + safe_zip.getvalue(),
            "trailing-utf16le": safe_zip.getvalue() + token.encode("utf-16-le"),
            "sfx-prefix-utf16be": token.encode("utf-16-be") + safe_zip.getvalue(),
            "trailing-utf16be": safe_zip.getvalue() + token.encode("utf-16-be"),
            "sfx-prefix-utf32le": (
                b"\xff\xfe\x00\x00" + token.encode("utf-32-le") + safe_zip.getvalue()
            ),
            "trailing-utf32be": (
                safe_zip.getvalue() + b"\x00\x00\xfe\xff" + token.encode("utf-32-be")
            ),
        }.items():
            with self.subTest(name=name):
                store = self.root / f"store-zip-raw-{name}"
                archive_path = private_file(self.root / f"zip-raw-{name}.bin", raw)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        archive_path,
                        trigger="client-observation",
                        repository=None,
                    )
                    self.assertEqual(1, evidence_store.summary()["excluded"])
                self.assertTrue(verify.verify_store(store)["verified"])

    def test_streaming_secret_scan_rejects_cross_boundary_session_cookie(self) -> None:
        chunk_bytes = 1024 * 1024
        raw = (
            b"." * (chunk_bytes - 2_500)
            + b"Cookie: harmless=value; "
            + b"x" * 3_000
            + b"; session=shortsecret"
        )
        with self.assertRaisesRegex(capture.SecretDetectedError, "session-cookie"):
            capture._scan_secret_binary_stream(io.BytesIO(raw))

        source = private_file(self.root / "cross-boundary-cookie.txt", raw)
        with self.assertRaisesRegex(capture.SecretDetectedError, "session-cookie"):
            capture._scan_secret_text(source)

    def test_streaming_secret_scan_rejects_unclosed_megabyte_assignment(self) -> None:
        raw = b'token="' + b"A" * (1024 * 1024 + 4_096) + b'"'
        self.assertIsNotNone(
            dict(capture.FIXED_LENGTH_REDACTION_PATTERNS)["assigned-secret"].search(
                raw
            )
        )
        with self.assertRaisesRegex(capture.SecretDetectedError, "assigned-secret"):
            capture._scan_secret_binary_stream(io.BytesIO(raw))

    def test_zip_member_secret_scan_retains_cross_boundary_overlap(self) -> None:
        member_boundary = 512 + 1024 * 1024
        raw = (
            b"." * (member_boundary - 2_500)
            + b"Cookie: harmless=value; "
            + b"x" * 3_000
            + b"; session=shortsecret"
        )
        archive_path = self.root / "cross-boundary-cookie.zip"
        with zipfile.ZipFile(
            archive_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            archive.writestr("bounded.log", raw)
        archive_path.chmod(0o600)
        self.assertNotIn(b"Cookie:", archive_path.read_bytes())
        with self.assertRaisesRegex(capture.SecretDetectedError, "session-cookie"):
            capture._scan_zip_archive(archive_path)

    def test_verifier_rejects_claimed_safe_cross_boundary_secret(self) -> None:
        raw = b'token="' + b"A" * (1024 * 1024 + 4_096) + b'"'
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            staged = capture.stage_bytes(
                raw,
                store.incoming,
                max_bytes=len(raw) + 1,
            )
            store.commit_staged(
                staged,
                trigger="manual",
                repository=None,
                source=self.transaction_source("test:cross-boundary-secret", raw),
                role="local-source",
                media_type="text/plain; charset=utf-8",
                opaque=False,
                secret_scan="high-confidence-text-scan-passed",
                secret_scan_performed=True,
                sensitivity="owner-only-raw",
            )
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "unredacted secret category assigned-secret",
        ):
            verify.verify_store(self.store)

    def test_extended_high_confidence_secret_patterns_are_excluded(self) -> None:
        cases = {
            "aws": b"AWS_SECRET_ACCESS_KEY=abcdefghijklmnopqrstuvwx12345678",
            "npm": b"NPM_TOKEN=npm-token-value-1234567890",
            "database": b"DATABASE_URL=postgresql://owner:private-password@db.invalid/app",
            "json-token": b'{"token":"generic-token-value-123456"}',
            "json-secret": b'{"secret":"generic-secret-value-12345"}',
            "stateless": (
                b"ghs_subject_abcdefghijklmnopqrstuvwxyz."
                b"abcdefghijklmnopqrstuvwxyz.abcdefghijklmnopqrstuvwxyz"
            ),
            "encrypted-pkcs8": ENCRYPTED_PRIVATE_KEY_HEADER.encode(),
            "pgp": b"-----BEGIN PGP PRIVATE KEY BLOCK-----",
            "putty-v3": ("PuTTY-User" + "-Key-File-3: ssh-ed25519").encode(),
            "putty-v1": ("PuTTY-User" + "-Key-File-1: ssh-rsa").encode(),
            "ssh2-encrypted": (
                "-----BEGIN SSH2 ENCRYPTED " + "PRIVATE KEY-----"
            ).encode(),
            "ssh2-actual": (
                "---- BEGIN SSH2 ENCRYPTED " + "PRIVATE KEY ----"
            ).encode(),
            "npm-granular": ("npm_" + "A" * 36).encode(),
            "dh-private": ("-----BEGIN DH " + "PRIVATE KEY-----").encode(),
            "basic-auth": b"Authorization: Ba" + b"sic dXNlcjpwYXNzd29yZA==",
            "npmrc-auth": (
                b"//registry.npmjs.org/:_auth" + b"Token=npm-token-value-1234567890"
            ),
            "aws-session": (
                b"AWS_SESSION_" + b"TOKEN=session-token-value-1234567890"
            ),
            "node-auth": b"NODE_AUTH_" + b"TOKEN=node-token-value-1234567890",
            "session-cookie": (
                b"Cookie: session" + b"id=session-cookie-value-1234567890"
            ),
            "aws-temporary": (b"AS" + b"IA" + b"A" * 16),
            "google-api": (b"AI" + b"za" + b"A" * 35),
            "google-oauth": (b"GOC" + b"SPX-" + b"A" * 28),
            "gitlab": (b"gl" + b"pat-" + b"A" * 20),
            "pypi": (b"pypi-AgEIcHlwaS5v" + b"cmc" + b"A" * 30),
            "slack-app": (b"xapp-" + b"1-" + b"A" * 40),
            "hugging-face": (b"hf_" + b"A" * 40),
            "stripe-live": (b"sk_live_" + b"A" * 32),
            "sendgrid": (b"SG." + b"A" * 20 + b"." + b"B" * 40),
            "docker": (b"dckr_pat_" + b"A" * 32),
            "slack-webhook": (
                b"https://hooks.slack.com/services/"
                + b"T" * 12
                + b"/"
                + b"B" * 12
                + b"/"
                + b"A" * 24
            ),
            "short-password": b"pass" + b"word: tiny",
            "short-client-secret": b"client_" + b"secret=short",
            "later-session-cookie": (
                b"Cookie: harmless=value; session" + b"id=abcdefghijklmnopqrstuv"
            ),
            "host-session-cookie": (
                b"Set-Cookie: __Host-" + b"session=abcdefghijklmnopqrstuv; Secure"
            ),
            "connect-session-cookie": (
                b"Cookie: connect." + b"sid=abcdefghijklmnopqrstuv"
            ),
            "java-session-cookie": b"Cookie: JSESSIONID=abcdefghijklmnopqrstuv",
            "quoted-session-cookie": b'Cookie: sessionid="abcdefghijklmnopqrstuv"',
            "postgres-userinfo": (
                b"postgresql://owner:" + b"private-password@db.invalid/app"
            ),
            "redis-userinfo": (
                b"redis://default:" + b"private-password@cache.invalid:6379"
            ),
            "http-userinfo": (
                b"https://owner:" + b"private-password@example.invalid/path"
            ),
        }
        for name, raw in cases.items():
            with self.subTest(name=name):
                store = self.root / f"store-{name}"
                source = private_file(self.root / f"{name}.bin", raw)
                with capture.private_umask(), capture.EvidenceStore(store) as evidence_store:
                    capture.capture_local_file(
                        evidence_store,
                        source,
                        trigger="client-observation",
                        repository=None,
                    )
                    summary = evidence_store.summary()
                self.assertEqual(1, summary["excluded"])
                self.assertNotIn(raw, (store / "journal.jsonl").read_bytes())
                self.assertTrue(verify.verify_store(store)["verified"])

    def test_secret_shaped_source_label_is_sanitised_before_journalling(self) -> None:
        token = "github_" + "pat_" + "a" * 40
        source = private_file(self.root / token, b"safe content")
        self.capture_file(source)
        event = self.journal()[0]
        journal_raw = (self.store / "journal.jsonl").read_text(encoding="utf-8")
        self.assertNotIn(token, journal_raw)
        self.assertIn("redacted-github-fine-grained-token", event["source"]["label"])
        self.assertIn(
            "journal-label:github-fine-grained-token",
            event["source"]["redaction_categories"],
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_verifier_independently_rescans_claimed_safe_content_object(self) -> None:
        raw = b"AWS_SESSION_" + b"TOKEN=session-token-value-1234567890"
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            staged = capture.stage_bytes(raw, store.incoming, max_bytes=1_000)
            store.commit_staged(
                staged,
                trigger="manual",
                repository=None,
                source=self.transaction_source("test:claimed-safe-object", raw),
                role="local-source",
                media_type="text/plain; charset=utf-8",
                opaque=False,
                secret_scan="high-confidence-text-scan-passed",
                secret_scan_performed=True,
                sensitivity="owner-only-raw",
            )
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "unredacted secret"):
            verify.verify_store(self.store)

    def test_verifier_rejects_journal_tamper_missing_and_unindexed_objects(self) -> None:
        source = private_file(self.root / "source.txt", b"evidence")
        self.capture_file(source)
        journal = self.store / "journal.jsonl"
        original = journal.read_bytes()
        journal.write_bytes(original.replace(b"feature-completed", b"feature_tampered"))
        journal.chmod(0o600)
        with self.assertRaises(verify.EvidenceVerificationError):
            verify.verify_store(self.store)
        journal.write_bytes(original)
        journal.chmod(0o600)
        event = self.journal()[0]
        digest = event["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest
        object_path.unlink()
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "differ"):
            verify.verify_store(self.store)

    def test_verifier_rejects_oversized_journal_before_scanning_it(self) -> None:
        source = private_file(self.root / "source.txt", b"evidence")
        self.capture_file(source)
        journal = self.store / "journal.jsonl"
        with journal.open("r+b") as stream:
            stream.truncate(capture.MAX_STORE_JOURNAL_BYTES + 1)
        with (
            mock.patch.object(verify, "_scan_secret_binary_stream") as scanner,
            self.assertRaisesRegex(verify.EvidenceVerificationError, "byte boundary"),
        ):
            verify.verify_store(self.store)
        scanner.assert_not_called()

    def test_expiry_ledger_lifetime_cap_is_checked_before_replace(self) -> None:
        source = capture._source_value(
            kind="test",
            identity="test:expiring-source",
            label="expiring source",
            occurred_at_utc="2026-08-30T08:00:00.000Z",
            expires_at_utc="2026-09-30T08:00:00.000Z",
            expiry_basis="provider-observed",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="none",
            snapshot_method="github-api-download",
            source_stat_before=None,
            source_stat_after=None,
            source_changed_after_snapshot=None,
            collection_generation_sha256=None,
            collection_window=None,
            redaction_categories=[],
            redaction_count=0,
        )
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            store.record_without_object(
                trigger="manual",
                repository=None,
                source=source,
                status_value="unavailable",
                reason="synthetic-unavailable",
            )
            with (
                mock.patch.object(capture, "MAX_STORE_LEDGER_BYTES", 1),
                mock.patch.object(capture, "atomic_replace") as replace,
                self.assertRaisesRegex(capture.EvidenceCaptureError, "ledger exceeds"),
            ):
                store._refresh_ledger()
            replace.assert_not_called()

    def test_verifier_rejects_broad_modes_and_hardlinks(self) -> None:
        source = private_file(self.root / "source.txt", b"evidence")
        self.capture_file(source)
        ledger = self.store / "expiry-ledger.json"
        ledger.chmod(0o644)
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "mode"):
            verify.verify_store(self.store)
        ledger.chmod(0o600)
        hard = self.store / "hard-linked-ledger"
        os.link(ledger, hard)
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "hard-linked"):
            verify.verify_store(self.store)

    @unittest.skipUnless(sys.platform == "darwin", "macOS extended metadata test")
    def test_verifier_rejects_resource_forks_and_extended_acls(self) -> None:
        source = private_file(self.root / "source.txt", b"evidence")
        self.capture_file(source)
        event = self.journal()[0]
        digest = event["objects"][0]["sha256"]
        object_path = self.store / "objects" / "sha256" / digest[:2] / digest

        subprocess.run(
            ["/usr/bin/xattr", "-wx", "com.apple.ResourceFork", "010203", str(object_path)],
            check=True,
        )
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "extended attributes"):
            verify.verify_store(self.store)
        subprocess.run(
            ["/usr/bin/xattr", "-d", "com.apple.ResourceFork", str(object_path)],
            check=True,
        )

        owner = subprocess.run(
            ["/usr/bin/id", "-un"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            ["/bin/chmod", "+a", f"{owner} allow read", str(object_path)],
            check=True,
        )
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "extended ACL"):
            verify.verify_store(self.store)
        subprocess.run(["/bin/chmod", "-N", str(object_path)], check=True)
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_capture_uses_attempt_ids_retention_and_selective_artifacts(self) -> None:
        client = FakeGitHubClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
            first_event_count = len(store.events)
            artifacts_endpoint = "repos/acme/project/actions/runs/101/artifacts?per_page=100"
            self.assertEqual(1, client.json_requests.count(artifacts_endpoint))
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
            self.assertEqual(2, client.json_requests.count(artifacts_endpoint))
            self.assertEqual(first_event_count, len(store.events))
        events = self.journal()
        identities = {event["source"]["identity"] for event in events}
        self.assertIn("github:repository:4242:run:101:attempt:1:logs", identities)
        self.assertIn("github:repository:4242:run:101:attempt:2:logs", identities)
        self.assertIn("github:repository:4242:run:101:attempt:3:logs", identities)
        self.assertIn("github:repository:4242:run:101:artifact:201:zip", identities)
        self.assertNotIn("github:repository:4242:run:102:attempt:1:metadata", identities)
        large = [event for event in events if "artifact:202" in event["source"]["identity"]]
        self.assertEqual("unavailable", large[0]["disposition"]["status"])
        logs = [event for event in events if event["source"]["kind"] == "github-actions-run-logs"]
        self.assertEqual("unknown", logs[0]["source"]["expiry_basis"])
        self.assertIsNone(logs[0]["source"]["expires_at_utc"])
        run_events = [
            event
            for event in events
            if event["source"]["kind"].startswith("github-actions-")
            and ":run:101:" in event["source"]["identity"]
        ]
        self.assertTrue(run_events)
        self.assertTrue(
            all(event["source"]["tree_sha"] == "b" * 40 for event in run_events)
        )
        self.assertTrue(logs[0]["objects"][0]["opaque"])
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_retention_lookup_failure_is_recorded_and_later_succeeds(self) -> None:
        class RetentionUnavailableOnceClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.retention_available = False

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                if endpoint.endswith("artifact-and-log-retention"):
                    if not self.retention_available:
                        raise capture.GitHubProviderUnavailableError(
                            "synthetic retention lookup failure"
                        )
                return super().json(endpoint, paginate=paginate)

        client = RetentionUnavailableOnceClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.retention_available = True
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        identities = {event["source"]["identity"] for event in self.journal()}
        self.assertTrue(
            any(
                identity.startswith(
                    "github:repository:4242:actions-retention:"
                    "observation:lookup-unavailable:source-sha256:"
                )
                for identity in identities
            )
        )
        self.assertTrue(
            any(
                identity.startswith("github:repository:4242:actions-retention:snapshot:")
                for identity in identities
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])
        events = self.journal()
        unavailable = next(
            event
            for event in events
            if ":actions-retention:observation:lookup-unavailable:source-sha256:" in (
                event["source"]["identity"]
            )
        )
        unavailable["disposition"]["reason"] = "forged-provider-reason"
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError, "retention lookup observation is invalid"
        ):
            verify.verify_store(self.store)

    def test_github_rejects_malformed_retention_policy(self) -> None:
        malformed_values: tuple[object, ...] = (
            {"days": True},
            {"days": 0},
            {"days": 401},
            {"days": 10**1_000},
            {"days": "90"},
            [],
        )
        for index, malformed in enumerate(malformed_values):
            with self.subTest(malformed=malformed):
                self.store = self.root / f"malformed-retention-{index}"

                class MalformedRetentionClient(FakeGitHubClient):
                    def json(self, endpoint: str, *, paginate: bool = False) -> object:
                        if endpoint.endswith("artifact-and-log-retention"):
                            return malformed
                        return super().json(endpoint, paginate=paginate)

                with self.assertRaisesRegex(
                    capture.EvidenceCaptureError, "retention policy is invalid"
                ):
                    with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                        capture.capture_github(
                            store,
                            repository="acme/project",
                            since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                            trigger="daily-safety-sweep",
                            download_run_logs=False,
                            artifact_max_bytes=1_000,
                            client=MalformedRetentionClient(),
                        )

    def test_verifier_rejects_retained_retention_policy_above_provider_maximum(self) -> None:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=FakeGitHubClient(),
            )
        events = self.journal()
        retention_event = next(
            event
            for event in events
            if event["source"]["kind"] == "github-actions-retention-policy-snapshot"
        )
        replacement = capture.canonical_json({"days": 401}, pretty=True)
        self.replace_event_object(retention_event, replacement)
        replacement_digest = hashlib.sha256(replacement).hexdigest()
        identity_prefix = retention_event["source"]["identity"].rsplit(":snapshot:", 1)[0]
        retention_event["source"]["identity"] = (
            f"{identity_prefix}:snapshot:{replacement_digest}"
        )
        retention_event["source"]["identity_sha256"] = capture.source_identity_sha256(
            retention_event["source"]["identity"]
        )
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError, "retention policy is invalid"
        ):
            verify.verify_store(self.store)

    def test_github_log_observations_are_idempotent_when_current_retention_changes(self) -> None:
        class MutableRetentionClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.days = 90
                self.fail_downloads = True

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                if endpoint.endswith("artifact-and-log-retention"):
                    return {"days": self.days}
                return super().json(endpoint, paginate=paginate)

        client = MutableRetentionClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.days = 30
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        log_observations = [
            event
            for event in self.journal()
            if event["source"]["kind"] == "github-actions-run-logs"
            and event["disposition"]["status"] == "unavailable"
        ]
        self.assertEqual(3, len(log_observations))
        self.assertEqual(3, len({event["source"]["identity"] for event in log_observations}))
        retention_snapshots = [
            event
            for event in self.journal()
            if event["source"]["kind"] == "github-actions-retention-policy-snapshot"
            and event["disposition"]["status"] == "captured"
        ]
        self.assertEqual(2, len(retention_snapshots))
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_verifier_keeps_historical_log_expiry_unknown(self) -> None:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=FakeGitHubClient(),
            )
        events = self.journal()
        log_event = next(
            event
            for event in events
            if event["source"]["kind"] == "github-actions-run-logs"
        )
        log_event["source"]["expires_at_utc"] = "2026-11-28T07:05:00.000Z"
        log_event["source"]["expiry_basis"] = "policy-snapshot-derived"
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "historical log expiry is not independently evidenced",
        ):
            verify.verify_store(self.store)

    def test_github_rejects_non_boolean_artifact_expiry_marker(self) -> None:
        class MalformedExpiryClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.malformed = True

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if self.malformed and endpoint.endswith("/artifacts?per_page=100"):
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["expired"] = "false"
                return value

        client = MalformedExpiryClient()
        with self.assertRaisesRegex(
            capture.EvidenceCaptureError, "expiry marker is invalid"
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="daily-safety-sweep",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=client,
                )
        self.assertTrue(verify.verify_store(self.store)["verified"])
        self.assertFalse(
            any(
                event["source"]["kind"] == "github-actions-artifact-metadata"
                for event in self.journal()
            )
        )

        client.malformed = False
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_verifier_binds_expired_observation_to_provider_metadata(self) -> None:
        class ExpiredArtifactClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["expired"] = True
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=ExpiredArtifactClient(),
            )
        self.assertTrue(verify.verify_store(self.store)["verified"])

        events = self.journal()
        metadata_event = next(
            event
            for event in events
            if event["source"]["kind"] == "github-actions-artifact-metadata"
        )
        item = metadata_event["objects"][0]
        metadata_path = (
            self.store / "objects" / "sha256" / item["sha256"][:2] / item["sha256"]
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["artifacts"][0]["expired"] = False
        replacement = capture.canonical_json(metadata, pretty=True)
        self.replace_event_object(metadata_event, replacement)
        replacement_digest = hashlib.sha256(replacement).hexdigest()
        identity_prefix = metadata_event["source"]["identity"].rsplit(":snapshot:", 1)[0]
        metadata_event["source"]["identity"] = (
            f"{identity_prefix}:snapshot:{replacement_digest}"
        )
        metadata_event["source"]["identity_sha256"] = capture.source_identity_sha256(
            metadata_event["source"]["identity"]
        )
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError, "exact preceding metadata snapshot"
        ):
            verify.verify_store(self.store)

    def test_verifier_rejects_captured_artifact_bound_only_to_expired_metadata(self) -> None:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=FakeGitHubClient(),
            )
        events = self.journal()
        metadata_event = next(
            event
            for event in events
            if event["source"]["kind"] == "github-actions-artifact-metadata"
        )
        item = metadata_event["objects"][0]
        metadata_path = (
            self.store / "objects" / "sha256" / item["sha256"][:2] / item["sha256"]
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["artifacts"][0]["expired"] = True
        replacement = capture.canonical_json(metadata, pretty=True)
        self.replace_event_object(metadata_event, replacement)
        replacement_digest = hashlib.sha256(replacement).hexdigest()
        identity_prefix = metadata_event["source"]["identity"].rsplit(":snapshot:", 1)[0]
        metadata_event["source"]["identity"] = (
            f"{identity_prefix}:snapshot:{replacement_digest}"
        )
        metadata_event["source"]["identity_sha256"] = capture.source_identity_sha256(
            metadata_event["source"]["identity"]
        )
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError, "exact preceding metadata snapshot"
        ):
            verify.verify_store(self.store)

    def test_verifier_binds_artifact_to_exact_preceding_metadata_snapshot(self) -> None:
        class MutableArtifactExpiryClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.expires_at = "2026-09-29T08:01:00Z"

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["expires_at"] = self.expires_at
                return value

        client = MutableArtifactExpiryClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.expires_at = "2026-10-15T08:01:00Z"
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        self.assertTrue(verify.verify_store(self.store)["verified"])
        events = self.journal()
        artifact_event = next(
            event
            for event in events
            if event["source"]["kind"] == "github-actions-artifact"
            and event["disposition"]["status"] == "captured"
        )
        metadata_events = sorted(
            (
                event
                for event in events
                if event["source"]["kind"] == "github-actions-artifact-metadata"
            ),
            key=lambda event: event["sequence"],
        )
        self.assertEqual(2, len(metadata_events))
        first_digest = metadata_events[0]["source"]["identity"].rsplit(":", 1)[1]
        later_digest = metadata_events[1]["source"]["identity"].rsplit(":", 1)[1]
        self.assertEqual(
            first_digest,
            artifact_event["source"]["collection_generation_sha256"],
        )
        artifact_event["source"]["expires_at_utc"] = "2026-10-15T08:01:00.000Z"
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError, "expiry differs from provider metadata"
        ):
            verify.verify_store(self.store)

        artifact_event["source"]["collection_generation_sha256"] = later_digest
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "does not bind its exact preceding metadata snapshot",
        ):
            verify.verify_store(self.store)

    def test_verifier_rejects_cross_snapshot_artifact_rebinding_both_directions(self) -> None:
        class MutableArtifactExpiryClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.expires_at = "2026-09-29T08:01:00Z"

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["expires_at"] = self.expires_at
                return value

        client = MutableArtifactExpiryClient()
        client.fail_downloads = True
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.expires_at = "2026-10-15T08:01:00Z"
        client.fail_downloads = False
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        self.assertTrue(verify.verify_store(self.store)["verified"])

        events = self.journal()
        metadata_events = sorted(
            (
                event
                for event in events
                if event["source"]["kind"] == "github-actions-artifact-metadata"
            ),
            key=lambda event: event["sequence"],
        )
        earlier_digest = metadata_events[0]["source"]["identity"].rsplit(":", 1)[1]
        later_digest = metadata_events[1]["source"]["identity"].rsplit(":", 1)[1]
        artifact_events = [
            event
            for event in events
            if event["source"]["kind"] == "github-actions-artifact"
            and ":artifact:201:zip" in event["source"]["identity"]
        ]
        observation = next(
            event
            for event in artifact_events
            if event["disposition"]["status"] == "unavailable"
        )
        captured = next(
            event
            for event in artifact_events
            if event["disposition"]["status"] == "captured"
        )
        self.assertEqual(
            earlier_digest, observation["source"]["collection_generation_sha256"]
        )
        self.assertEqual(
            later_digest, captured["source"]["collection_generation_sha256"]
        )

        captured["source"]["collection_generation_sha256"] = earlier_digest
        captured["source"]["expires_at_utc"] = "2026-09-29T08:01:00.000Z"
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "does not bind its exact preceding metadata snapshot",
        ):
            verify.verify_store(self.store)

        captured["source"]["collection_generation_sha256"] = later_digest
        captured["source"]["expires_at_utc"] = "2026-10-15T08:01:00.000Z"
        observation_source = observation["source"]
        base_identity = observation_source["identity"].split(":observation:", 1)[0]
        observation_source["collection_generation_sha256"] = later_digest
        observation_source["expires_at_utc"] = "2026-10-15T08:01:00.000Z"
        observation_source["identity"] = base_identity
        observation_source["identity_sha256"] = capture.source_identity_sha256(base_identity)
        source_digest = hashlib.sha256(capture.canonical_json(observation_source)).hexdigest()
        observation_source["identity"] = (
            f"{base_identity}:observation:download-unavailable:"
            f"source-sha256:{source_digest}"
        )
        observation_source["identity_sha256"] = capture.source_identity_sha256(
            observation_source["identity"]
        )
        self.rewrite_journal(events)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "does not bind its exact preceding metadata snapshot",
        ):
            verify.verify_store(self.store)

    def test_verifier_binds_github_run_and_artifact_occurrence_times(self) -> None:
        cases = (
            ("github-actions-run-metadata", "run occurrence differs"),
            ("github-actions-run-jobs", "attempt occurrence differs"),
            ("github-actions-run-logs", "attempt occurrence differs"),
            ("github-actions-artifact-metadata", "artefact metadata occurrence differs"),
            ("github-actions-artifact", "artefact occurrence differs"),
        )
        for index, (kind, message) in enumerate(cases):
            with self.subTest(kind=kind):
                self.store = self.root / f"github-occurrence-{index}"
                with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                    capture.capture_github(
                        store,
                        repository="acme/project",
                        since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                        trigger="daily-safety-sweep",
                        download_run_logs=True,
                        artifact_max_bytes=1_000,
                        client=FakeGitHubClient(),
                    )
                events = self.journal()
                event = next(
                    item
                    for item in events
                    if item["source"]["kind"] == kind
                    and item["disposition"]["status"] == "captured"
                )
                event["source"]["occurred_at_utc"] = "2099-01-01T00:00:00.000Z"
                self.rewrite_journal(events)
                with self.assertRaisesRegex(verify.EvidenceVerificationError, message):
                    verify.verify_store(self.store)

    def test_github_artifact_provider_digest_mismatch_is_not_captured(self) -> None:
        class DigestMismatchClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["digest"] = "sha256:" + "0" * 64
                return value

        client = DigestMismatchClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        artifact_events = [
            event
            for event in self.journal()
            if ":artifact:201:zip" in event["source"]["identity"]
        ]
        self.assertEqual(1, len(artifact_events))
        self.assertEqual("unavailable", artifact_events[0]["disposition"]["status"])
        self.assertIn(
            "provider-digest-mismatch",
            artifact_events[0]["source"]["identity"],
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_verifier_binds_github_snapshot_identity_to_canonical_object(self) -> None:
        kinds = (
            "github-repository-identity-snapshot",
            "github-actions-retention-policy-snapshot",
            "github-actions-run-metadata",
            "github-actions-run-jobs",
            "github-actions-artifact-metadata",
        )
        for index, kind in enumerate(kinds):
            with self.subTest(kind=kind):
                self.store = self.root / f"snapshot-store-{index}"
                with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                    capture.capture_github(
                        store,
                        repository="acme/project",
                        since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                        trigger="protected-main-completed",
                        download_run_logs=False,
                        artifact_max_bytes=1_000,
                        client=FakeGitHubClient(),
                    )
                events = self.journal()
                event = next(item for item in events if item["source"]["kind"] == kind)
                identity_prefix = event["source"]["identity"].rsplit(":", 1)[0]
                event["source"]["identity"] = f"{identity_prefix}:{'0' * 64}"
                event["source"]["identity_sha256"] = capture.source_identity_sha256(
                    event["source"]["identity"]
                )
                self.rewrite_journal(events)
                with self.assertRaisesRegex(
                    verify.EvidenceVerificationError, "snapshot digest differs"
                ):
                    verify.verify_store(self.store)

    def test_verifier_rejects_unknown_github_source_kind(self) -> None:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=FakeGitHubClient(),
            )
        events = self.journal()
        event = next(
            item
            for item in events
            if item["source"]["kind"] == "github-actions-run-metadata"
        )
        event["source"]["kind"] = "github-forged-provider-record"
        self.rewrite_journal(events)
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "closed capture contract"):
            verify.verify_store(self.store)

    def test_github_requires_canonical_repository_casing_before_capture(self) -> None:
        class CaseVariantClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                if endpoint == "repos/Acme/Project":
                    return super().json("repos/acme/project", paginate=paginate)
                return super().json(endpoint, paginate=paginate)

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError, "identity differs from the request"
            ):
                capture.capture_github(
                    store,
                    repository="Acme/Project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=CaseVariantClient(),
                )
        self.assertEqual([], self.journal())

    def test_verifier_binds_artifact_bytes_to_provider_digest_and_size(self) -> None:
        def stored_zip(content: bytes) -> bytes:
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
                entry = zipfile.ZipInfo("bounded.log", date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_STORED
                archive.writestr(entry, content)
            return output.getvalue()

        original = stored_zip(b"provider-bound-evidence-A")
        replacement = stored_zip(b"provider-bound-evidence-B")
        self.assertEqual(len(original), len(replacement))

        class DigestClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.download_payload = original

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["digest"] = (
                        "sha256:" + hashlib.sha256(original).hexdigest()
                    )
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=DigestClient(),
            )
        events = self.journal()
        event = next(
            item
            for item in events
            if item["source"]["kind"] == "github-actions-artifact"
            and item["disposition"]["status"] == "captured"
        )
        self.replace_event_object(event, replacement)
        self.rewrite_journal(events)
        with self.assertRaisesRegex(verify.EvidenceVerificationError, "provider digest differs"):
            verify.verify_store(self.store)

    def test_github_secret_shaped_artifact_name_excludes_metadata_and_archive(self) -> None:
        token = "github_" + "pat_" + "a" * 40

        class SecretNameClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/artifacts?per_page=100"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["artifacts"][0]["name"] = token
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=SecretNameClient(),
            )
        journal_raw = (self.store / "journal.jsonl").read_text(encoding="utf-8")
        self.assertNotIn(token, journal_raw)
        self.assertIn("secret-category:github-fine-grained-token", journal_raw)
        self.assertFalse(
            any(
                event["source"]["kind"] == "github-actions-artifact"
                for event in self.journal()
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_secret_in_run_metadata_excludes_children_and_verifies(self) -> None:
        token = "sk-" + "A" * 32

        class SecretRunClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.startswith("repos/acme/project/actions/runs?"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["workflow_runs"][0]["display_title"] = token
                elif endpoint in {
                    "repos/acme/project/actions/runs/101/attempts/1",
                    "repos/acme/project/actions/runs/101/attempts/2",
                }:
                    assert isinstance(value, dict)
                    value = {**value, "display_title": token}
                return value

        client = SecretRunClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        events = self.journal()
        excluded_runs = [
            event
            for event in events
            if event["source"]["kind"] == "github-actions-run-metadata"
            and event["disposition"]["status"] == "excluded"
        ]
        self.assertEqual(3, len(excluded_runs))
        self.assertFalse(
            any(
                event["source"]["kind"]
                in {
                    "github-actions-run-jobs",
                    "github-actions-run-logs",
                    "github-actions-artifact-metadata",
                    "github-actions-artifact",
                }
                for event in events
            )
        )
        self.assertFalse(
            any(
                token.encode() in path.read_bytes()
                for path in self.store.rglob("*")
                if path.is_file()
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_secret_in_repository_snapshot_aborts_without_children(self) -> None:
        token = "sk-" + "B" * 32

        class SecretRepositoryClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint == "repos/acme/project":
                    assert isinstance(value, dict)
                    value = {**value, "default_branch": token}
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError, "repository identity was excluded"
            ):
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=SecretRepositoryClient(),
                )
        events = self.journal()
        self.assertEqual(1, len(events))
        self.assertEqual("excluded", events[0]["disposition"]["status"])
        self.assertFalse(
            any(
                token.encode() in path.read_bytes()
                for path in self.store.rglob("*")
                if path.is_file()
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_attempts_must_bind_one_commit_and_tree(self) -> None:
        class InconsistentClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.endswith("/attempts/1"):
                    assert isinstance(value, dict)
                    return {
                        **value,
                        "head_commit": {"id": "a" * 40, "tree_id": "c" * 40},
                    }
                return value

        client = InconsistentClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "inconsistent source"):
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=client,
                )

        class InconsistentHeadClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.startswith("repos/acme/project/actions/runs?"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["workflow_runs"][0]["head_commit"]["id"] = "e" * 40
                return value

        with capture.private_umask(), capture.EvidenceStore(
            self.root / "inconsistent-head-store"
        ) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "head commit identity"):
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=InconsistentHeadClient(),
                )

    def test_github_child_metadata_must_bind_its_run(self) -> None:
        class WrongJobClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if "/jobs?" in endpoint:
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["jobs"][0]["run_id"] = 999
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "job identity"):
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=WrongJobClient(),
                )

    def test_github_discovers_long_running_run_updated_inside_window(self) -> None:
        class LongRunningClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.startswith("repos/acme/project/actions/runs?"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["total_count"] = 3
                    value[0]["workflow_runs"].append(
                        {
                            "id": 103,
                            "status": "completed",
                            "conclusion": "success",
                            "run_attempt": 1,
                            "head_sha": "c" * 40,
                            "head_commit": {"id": "c" * 40, "tree_id": "d" * 40},
                            "created_at": "2026-07-28T08:00:00Z",
                            "run_started_at": "2026-07-28T08:00:00Z",
                            "updated_at": "2026-08-30T08:05:00Z",
                        }
                    )
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=LongRunningClient(),
            )
        self.assertTrue(
            any(
                ":run:103:attempt:1:metadata:" in event["source"]["identity"]
                for event in self.journal()
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_fails_closed_when_filtered_run_discovery_is_truncated(self) -> None:
        class TruncatedClient(FakeGitHubClient):
            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                if endpoint.startswith("repos/acme/project/actions/runs?"):
                    assert isinstance(value, list)
                    value = json.loads(json.dumps(value))
                    value[0]["total_count"] = 1_001
                return value

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "discovery is truncated"):
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                    trigger="protected-main-completed",
                    download_run_logs=False,
                    artifact_max_bytes=1_000,
                    client=TruncatedClient(),
                )

    def test_github_mutable_run_and_job_metadata_are_content_versioned(self) -> None:
        client = FakeGitHubClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="protected-main-completed",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.run["conclusion"] = "failure"
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        run_metadata = [
            event
            for event in self.journal()
            if event["source"]["kind"] == "github-actions-run-metadata"
        ]
        self.assertEqual(6, len(run_metadata))
        self.assertTrue(
            all(":metadata:snapshot:" in event["source"]["identity"] for event in run_metadata)
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_client_bounds_metadata_and_stalled_children(self) -> None:
        oversized = self.root / "oversized-gh"
        oversized.write_text(
            "#!/bin/sh\ndd if=/dev/zero bs=1 count=257 2>/dev/null | tr '\\000' x\n",
            encoding="utf-8",
        )
        oversized.chmod(0o700)
        with mock.patch.object(capture, "MAX_METADATA_BYTES", 128):
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "byte boundary"):
                capture.GhClient(str(oversized)).json("repos/acme/project")

        stalled = self.root / "stalled-gh"
        stalled.write_text("#!/bin/sh\nsleep 2\nprintf '{}\\n'\n", encoding="utf-8")
        stalled.chmod(0o700)
        started = time.monotonic()
        with mock.patch.object(capture, "GITHUB_METADATA_TIMEOUT_SECONDS", 0.05):
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "timed out"):
                capture.GhClient(str(stalled)).json("repos/acme/project")
        self.assertLess(time.monotonic() - started, 1.0)

        incoming = self.root / "download-incoming"
        incoming.mkdir(mode=0o700)
        started = time.monotonic()
        with mock.patch.object(capture, "GITHUB_DOWNLOAD_TIMEOUT_SECONDS", 0.05):
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "timed out"):
                capture.GhClient(str(stalled)).download_to(
                    "repos/acme/project/actions/runs/1/logs",
                    incoming,
                    max_bytes=128,
                )
        self.assertLess(time.monotonic() - started, 1.0)
        self.assertEqual([], list(incoming.iterdir()))

    def test_github_json_retries_transient_failures_and_accounts_every_attempt(self) -> None:
        class TransientGhClient(capture.GhClient):
            def __init__(self) -> None:
                super().__init__("synthetic-gh")
                self.calls = 0
                self.timeout_values: list[float | None] = []

            def json(
                self,
                endpoint: str,
                *,
                paginate: bool = False,
                timeout_seconds: float | None = None,
            ) -> object:
                self.calls += 1
                self.timeout_values.append(timeout_seconds)
                self.last_response_bytes = (7, 11, 13)[self.calls - 1]
                if self.calls < 3:
                    raise capture.GitHubProviderUnavailableError(
                        "synthetic transient metadata failure"
                    )
                return {"status": "available"}

        client = TransientGhClient()
        delays: list[float] = []
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            value = capture._github_json(
                store,
                client,
                "repos/acme/project",
                retry_sleep=delays.append,
            )
            self.assertEqual(3, store.github_api_invocations)
            self.assertEqual(31, store.github_metadata_bytes)
        self.assertEqual({"status": "available"}, value)
        self.assertEqual(3, client.calls)
        self.assertEqual(
            [capture.GITHUB_METADATA_RETRY_DELAY_SECONDS] * 2,
            delays,
        )
        self.assertTrue(
            all(
                isinstance(value, float) and value > 0
                for value in client.timeout_values
            )
        )

    def test_github_json_retry_exhaustion_preserves_provider_error(self) -> None:
        class UnavailableGhClient(capture.GhClient):
            def __init__(self) -> None:
                super().__init__("synthetic-gh")
                self.calls = 0

            def json(
                self,
                endpoint: str,
                *,
                paginate: bool = False,
                timeout_seconds: float | None = None,
            ) -> object:
                self.calls += 1
                self.last_response_bytes = 5
                raise capture.GitHubProviderUnavailableError(
                    "synthetic persistent metadata failure"
                )

        client = UnavailableGhClient()
        delays: list[float] = []
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            with self.assertRaisesRegex(
                capture.GitHubProviderUnavailableError,
                "synthetic persistent metadata failure",
            ):
                capture._github_json(
                    store,
                    client,
                    "repos/acme/project",
                    retry_sleep=delays.append,
                )
            self.assertEqual(capture.GITHUB_METADATA_MAX_ATTEMPTS, client.calls)
            self.assertEqual(capture.GITHUB_METADATA_MAX_ATTEMPTS, store.github_api_invocations)
            self.assertEqual(15, store.github_metadata_bytes)
        self.assertEqual(
            [capture.GITHUB_METADATA_RETRY_DELAY_SECONDS] * 2,
            delays,
        )

    def test_github_json_retries_remain_inside_api_and_wall_clock_boundaries(self) -> None:
        class UnavailableGhClient(capture.GhClient):
            def __init__(self) -> None:
                super().__init__("synthetic-gh")
                self.calls = 0

            def json(
                self,
                endpoint: str,
                *,
                paginate: bool = False,
                timeout_seconds: float | None = None,
            ) -> object:
                self.calls += 1
                self.last_response_bytes = 0
                raise capture.GitHubProviderUnavailableError(
                    "synthetic transient metadata failure"
                )

        api_client = UnavailableGhClient()
        api_delays: list[float] = []
        api_store_path = self.root / "retry-api-boundary-store"
        with (
            mock.patch.object(capture, "MAX_GITHUB_API_INVOCATIONS", 2),
            capture.private_umask(),
            capture.EvidenceStore(api_store_path) as store,
        ):
            with self.assertRaisesRegex(capture.EvidenceCaptureError, "API invocation"):
                capture._github_json(
                    store,
                    api_client,
                    "repos/acme/project",
                    retry_sleep=api_delays.append,
                )
            self.assertEqual(2, store.github_api_invocations)
        self.assertEqual(2, api_client.calls)
        self.assertEqual([capture.GITHUB_METADATA_RETRY_DELAY_SECONDS], api_delays)

        wall_client = UnavailableGhClient()
        wall_store_path = self.root / "retry-wall-boundary-store"
        wall_delays: list[float] = []
        with capture.private_umask(), capture.EvidenceStore(wall_store_path) as store:
            def expire_capture(delay: float) -> None:
                wall_delays.append(delay)
                store.github_capture_started -= capture.MAX_GITHUB_CAPTURE_SECONDS + 1

            with self.assertRaisesRegex(capture.EvidenceCaptureError, "wall-clock boundary"):
                capture._github_json(
                    store,
                    wall_client,
                    "repos/acme/project",
                    retry_sleep=expire_capture,
                )
            self.assertEqual(1, store.github_api_invocations)
        self.assertEqual(1, wall_client.calls)
        self.assertEqual([capture.GITHUB_METADATA_RETRY_DELAY_SECONDS], wall_delays)

    def test_github_json_cleans_up_each_timed_out_process_before_retry(self) -> None:
        stalled = self.root / "retry-stalled-gh"
        stalled.write_text("#!/bin/sh\nexec sleep 2\n", encoding="utf-8")
        stalled.chmod(0o700)
        client = capture.GhClient(str(stalled))
        spawned: list[subprocess.Popen[bytes]] = []
        real_popen = subprocess.Popen

        def observe_popen(*args: Any, **kwargs: Any) -> subprocess.Popen[bytes]:
            process = real_popen(*args, **kwargs)
            spawned.append(process)
            return process

        started = time.monotonic()
        with (
            mock.patch.object(capture, "GITHUB_METADATA_TIMEOUT_SECONDS", 0.03),
            mock.patch.object(capture.subprocess, "Popen", side_effect=observe_popen),
            capture.private_umask(),
            capture.EvidenceStore(self.store) as store,
        ):
            with self.assertRaisesRegex(
                capture.GitHubProviderUnavailableError,
                "timed out",
            ):
                capture._github_json(
                    store,
                    client,
                    "repos/acme/project",
                    retry_sleep=lambda _: None,
                )
            self.assertEqual(capture.GITHUB_METADATA_MAX_ATTEMPTS, store.github_api_invocations)
        self.assertLess(time.monotonic() - started, 1.0)
        self.assertEqual(capture.GITHUB_METADATA_MAX_ATTEMPTS, len(spawned))
        self.assertTrue(all(process.poll() is not None for process in spawned))
        self.assertTrue(
            all(process.stdout is None or process.stdout.closed for process in spawned)
        )

    def test_github_json_does_not_retry_byte_json_or_policy_failures(self) -> None:
        def executable(name: str, body: str) -> Path:
            path = self.root / name
            path.write_text(
                f"#!{sys.executable}\nimport sys\n{body}\n",
                encoding="utf-8",
            )
            path.chmod(0o700)
            return path

        oversized = executable(
            "retry-oversized-gh",
            'sys.stdout.buffer.write(b"x" * 129)',
        )
        invalid_json = executable(
            "retry-invalid-json-gh",
            'sys.stdout.write("{\\n")',
        )
        invalid_policy = executable(
            "retry-invalid-policy-gh",
            'sys.stdout.write("{}\\n")',
        )

        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            before = store.github_api_invocations
            with (
                mock.patch.object(capture, "MAX_METADATA_BYTES", 128),
                self.assertRaisesRegex(capture.EvidenceCaptureError, "byte boundary"),
            ):
                capture._github_json(
                    store,
                    capture.GhClient(str(oversized)),
                    "repos/acme/project",
                    retry_sleep=lambda _: None,
                )
            self.assertEqual(before + 1, store.github_api_invocations)

            before = store.github_api_invocations
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "not valid UTF-8 JSON",
            ):
                capture._github_json(
                    store,
                    capture.GhClient(str(invalid_json)),
                    "repos/acme/project",
                    retry_sleep=lambda _: None,
                )
            self.assertEqual(before + 1, store.github_api_invocations)

            before = store.github_api_invocations
            value = capture._github_json(
                store,
                capture.GhClient(str(invalid_policy)),
                "repos/acme/project",
                retry_sleep=lambda _: None,
            )
            with self.assertRaisesRegex(
                capture.EvidenceCaptureError,
                "does not contain workflow_runs",
            ):
                capture._flatten_pages(value, "workflow_runs")
            self.assertEqual(before + 1, store.github_api_invocations)

    def test_github_downloads_share_request_and_wall_clock_boundaries(self) -> None:
        client = FakeGitHubClient()
        with mock.patch.object(capture, "MAX_GITHUB_API_INVOCATIONS", 1):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                capture._github_json(store, client, "repos/acme/project")
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "API invocation"):
                    capture._download_to_stage(
                        client,
                        "repos/acme/project/actions/runs/101/attempts/1/logs",
                        store.incoming,
                        max_bytes=1_000,
                        store=store,
                    )
        self.assertEqual([], client.downloads)

        wall_clock_store = self.root / "wall-clock-store"
        with mock.patch.object(capture, "MAX_GITHUB_CAPTURE_SECONDS", 0):
            with capture.private_umask(), capture.EvidenceStore(wall_clock_store) as store:
                with self.assertRaisesRegex(capture.EvidenceCaptureError, "wall-clock"):
                    capture._download_to_stage(
                        client,
                        "repos/acme/project/actions/runs/101/attempts/1/logs",
                        store.incoming,
                        max_bytes=1_000,
                        store=store,
                    )

    def test_github_discussion_snapshots_are_content_versioned(self) -> None:
        client = FakeGitHubClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github_discussion(
                store,
                repository="acme/project",
                number=108,
                trigger="pull-request-merged",
                client=client,
            )
            capture.capture_github_discussion(
                store,
                repository="acme/project",
                number=108,
                trigger="daily-safety-sweep",
                client=client,
            )
        events = self.journal()
        self.assertEqual(6, len(events))
        self.assertTrue(
            all(":snapshot:" in event["source"]["identity"] for event in events)
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_github_discussion_rejects_cross_repository_and_parent_substitution(self) -> None:
        class HostileDiscussionClient(FakeGitHubClient):
            def __init__(self, mode: str) -> None:
                super().__init__()
                self.mode = mode

            def json(self, endpoint: str, *, paginate: bool = False) -> object:
                value = super().json(endpoint, paginate=paginate)
                value = json.loads(json.dumps(value))
                if endpoint == "repos/acme/project/issues/108":
                    if self.mode == "number":
                        value["number"] = 999
                    elif self.mode == "repository":
                        value["repository_url"] = "https://api.github.com/repos/other/repo"
                if endpoint.endswith("/issues/108/comments?per_page=100") and self.mode == "comment":
                    value[0][0]["issue_url"] = "https://api.github.com/repos/other/repo/issues/108"
                if endpoint == "repos/acme/project/pulls/108" and self.mode == "pull-base":
                    value["base"]["repo"] = {"id": 999, "full_name": "other/repo"}
                return value

        for mode in ("number", "repository", "comment", "pull-base"):
            with self.subTest(mode=mode):
                store_path = self.root / f"discussion-{mode}"
                with capture.private_umask(), capture.EvidenceStore(store_path) as store:
                    with self.assertRaisesRegex(
                        capture.EvidenceCaptureError,
                        "differs|inconsistent",
                    ):
                        capture.capture_github_discussion(
                            store,
                            repository="acme/project",
                            number=108,
                            trigger="pull-request-merged",
                            client=HostileDiscussionClient(mode),
                        )
                kinds = {
                    event["source"]["kind"]
                    for event in capture.read_journal(store_path / "journal.jsonl")
                }
                self.assertNotIn("github-discussion-snapshot", kinds)

    def test_verifier_rejects_rebound_github_discussion_object(self) -> None:
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github_discussion(
                store,
                repository="acme/project",
                number=108,
                trigger="pull-request-merged",
                client=FakeGitHubClient(),
            )
        events = self.journal()
        event = next(
            item
            for item in events
            if ":issue-or-pull-request:snapshot:" in item["source"]["identity"]
        )
        old_digest = event["objects"][0]["sha256"]
        old_path = self.store / "objects" / "sha256" / old_digest[:2] / old_digest
        value = json.loads(old_path.read_text(encoding="utf-8"))
        value["number"] = 999
        value["url"] = "https://api.github.com/repos/acme/project/issues/999"
        raw = capture.canonical_json(value, pretty=True)
        new_digest = hashlib.sha256(raw).hexdigest()
        shard = self.store / "objects" / "sha256" / new_digest[:2]
        shard.mkdir(mode=0o700, exist_ok=True)
        shard.chmod(0o700)
        new_path = private_file(shard / new_digest, raw)
        self.assertTrue(new_path.exists())
        old_path.unlink()
        event["objects"][0]["sha256"] = new_digest
        event["objects"][0]["bytes"] = len(raw)
        identity = event["source"]["identity"].rsplit(":snapshot:", 1)[0]
        event["source"]["identity"] = f"{identity}:snapshot:{new_digest}"
        event["source"]["identity_sha256"] = capture.source_identity_sha256(
            event["source"]["identity"]
        )
        previous = None
        for item in events:
            item["previous_event_sha256"] = previous
            core = dict(item)
            core.pop("event_sha256")
            item["event_sha256"] = hashlib.sha256(
                capture.JOURNAL_DOMAIN + capture.canonical_json(core)[:-1]
            ).hexdigest()
            previous = item["event_sha256"]
        journal_raw = b"".join(capture.canonical_json(item) for item in events)
        journal = self.store / "journal.jsonl"
        journal.write_bytes(journal_raw)
        journal.chmod(0o600)
        ledger = capture.build_expiry_ledger(events, journal_raw)
        ledger_path = self.store / "expiry-ledger.json"
        ledger_path.write_bytes(capture.canonical_json(ledger, pretty=True))
        ledger_path.chmod(0o600)
        with self.assertRaisesRegex(
            verify.EvidenceVerificationError,
            "issue binding differs",
        ):
            verify.verify_store(self.store)

    def test_github_download_failure_does_not_block_later_success(self) -> None:
        client = FakeGitHubClient()
        client.fail_downloads = True
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 6, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.fail_downloads = False
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 6, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        identities = {event["source"]["identity"] for event in self.journal()}
        canonical = "github:repository:4242:run:101:attempt:1:logs"
        self.assertIn(canonical, identities)
        self.assertTrue(
            any(
                identity.startswith(
                    f"{canonical}:observation:download-unavailable:source-sha256:"
                )
                for identity in identities
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_local_download_boundary_failure_is_not_provider_unavailability(self) -> None:
        class LocalBoundaryClient(FakeGitHubClient):
            def download(self, endpoint: str, *, max_bytes: int) -> bytes:
                self.downloads.append(endpoint)
                raise capture.EvidenceCaptureError("synthetic local byte boundary failure")

        with self.assertRaisesRegex(
            capture.EvidenceCaptureError, "local byte boundary failure"
        ):
            with capture.private_umask(), capture.EvidenceStore(self.store) as store:
                capture.capture_github(
                    store,
                    repository="acme/project",
                    since=datetime(2026, 8, 30, 6, 0, tzinfo=timezone.utc),
                    trigger="daily-safety-sweep",
                    download_run_logs=True,
                    artifact_max_bytes=1_000,
                    client=LocalBoundaryClient(),
                )
        identities = {
            event["source"]["identity"]
            for event in self.journal()
        }
        self.assertFalse(
            any(identity.endswith(":observation:download-unavailable") for identity in identities)
        )

    def test_github_archive_validation_failure_does_not_block_later_success(self) -> None:
        class CorruptOnceClient(FakeGitHubClient):
            def __init__(self) -> None:
                super().__init__()
                self.corrupt = True

            def download(self, endpoint: str, *, max_bytes: int) -> bytes:
                if self.corrupt:
                    self.downloads.append(endpoint)
                    return b"not-a-zip"
                return super().download(endpoint, max_bytes=max_bytes)

        client = CorruptOnceClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 6, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        client.corrupt = False
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 6, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=True,
                artifact_max_bytes=1_000,
                client=client,
            )
        identities = {event["source"]["identity"] for event in self.journal()}
        canonical = "github:repository:4242:run:101:attempt:1:logs"
        self.assertIn(canonical, identities)
        self.assertTrue(
            any(
                identity.startswith(
                    f"{canonical}:observation:archive-validation-failed:source-sha256:"
                )
                for identity in identities
            )
        )
        self.assertTrue(verify.verify_store(self.store)["verified"])

    def test_expiry_ledger_is_deterministic_and_has_fourteen_day_warning(self) -> None:
        client = FakeGitHubClient()
        with capture.private_umask(), capture.EvidenceStore(self.store) as store:
            capture.capture_github(
                store,
                repository="acme/project",
                since=datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc),
                trigger="daily-safety-sweep",
                download_run_logs=False,
                artifact_max_bytes=1_000,
                client=client,
            )
        first = (self.store / "expiry-ledger.json").read_bytes()
        self.assertIn(b'"warning_at_utc": "2026-09-15T08:01:00.000Z"', first)
        verify.verify_store(self.store)
        second = (self.store / "expiry-ledger.json").read_bytes()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
