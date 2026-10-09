"""Adversarial offline image receipt tests; fake scanners are never hosted proof."""

from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/security/image_assurance.py"
SPEC = importlib.util.spec_from_file_location("security_image_assurance", CLI)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
NOW = dt.datetime(2026, 10, 9, 12, tzinfo=dt.timezone.utc)


def encoded(value):
    return json.dumps(value, sort_keys=True).encode()


def layer_bytes(files=None):
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode="w") as archive:
        for name, raw in (files or {"etc/passwd": b"root:x:0:0:root:/root:/bin/sh\nvscode:x:1000:1000:fixture:/home/vscode:/bin/sh\n"}).items():
            member = tarfile.TarInfo(name)
            member.size = len(raw)
            archive.addfile(member, io.BytesIO(raw))
    return result.getvalue()


class ImageFixture:
    def __init__(self, *, user="65532:65532", index=False, attestation=False, passwd=None, oci11=False):
        self.files = {"oci-layout": encoded({"imageLayoutVersion": "1.0.0"})}
        self.layer = layer_bytes(passwd)
        layer = self.blob(gzip.compress(self.layer, mtime=0), "application/vnd.oci.image.layer.v1.tar+gzip")
        self.diff_ids = ["sha256:" + hashlib.sha256(self.layer).hexdigest()]
        self.config = {"architecture": "amd64", "os": "linux", "config": {"User": user},
                       "rootfs": {"type": "layers", "diff_ids": self.diff_ids}}
        config = self.blob(encoded(self.config), runner.IMAGE_CONFIG)
        self.config_digest = config["digest"]
        self.manifest = {"schemaVersion": 2, "mediaType": runner.IMAGE_MANIFEST,
                         "config": config, "layers": [layer]}
        runtime = self.blob(encoded(self.manifest), runner.IMAGE_MANIFEST)
        self.runtime_digest = runtime["digest"]
        runtime["platform"] = {"architecture": "amd64", "os": "linux"}
        children = [runtime]
        if attestation:
            att_config = self.blob(encoded({}) if oci11 else encoded({"architecture": "unknown", "os": "unknown"}),
                                   runner.EMPTY_CONFIG if oci11 else runner.IMAGE_CONFIG)
            if oci11:
                att_config["data"] = "e30="
            att_layer = self.blob(encoded({"_type": "https://in-toto.io/Statement/v0.1", "subject": []}),
                                  "application/vnd.in-toto+json")
            manifest = {"schemaVersion": 2, "mediaType": runner.IMAGE_MANIFEST,
                        "config": att_config, "layers": [att_layer]}
            if oci11:
                manifest["artifactType"] = "application/vnd.docker.attestation.manifest.v1+json"
                manifest["subject"] = {key: runtime[key] for key in ("mediaType", "digest", "size")}
            att = self.blob(encoded(manifest), runner.IMAGE_MANIFEST)
            att.update({"platform": {"architecture": "unknown", "os": "unknown"},
                        "annotations": {"vnd.docker.reference.type": "attestation-manifest",
                                        "vnd.docker.reference.digest": self.runtime_digest}})
            children.append(att)
        root = {"schemaVersion": 2, "mediaType": runner.IMAGE_INDEX, "manifests": children}
        if index:
            descriptor = self.blob(encoded(root), runner.IMAGE_INDEX)
            self.expected = descriptor["digest"]
            root = {"schemaVersion": 2, "mediaType": runner.IMAGE_INDEX, "manifests": [descriptor]}
        else:
            self.expected = self.runtime_digest
        self.files["index.json"] = encoded(root)

    def mutate_attestation(self, mutate):
        outer = json.loads(self.files["index.json"])
        root_descriptor = outer["manifests"][0]
        root = json.loads(self.files["blobs/sha256/" + root_descriptor["digest"][7:]])
        descriptor = root["manifests"][1]
        old = "blobs/sha256/" + descriptor["digest"][7:]
        manifest = json.loads(self.files.pop(old))
        mutate(manifest)
        replacement = self.blob(encoded(manifest), runner.IMAGE_MANIFEST)
        descriptor.update(replacement)
        del self.files["blobs/sha256/" + root_descriptor["digest"][7:]]
        root_descriptor.update(self.blob(encoded(root), runner.IMAGE_INDEX))
        self.expected = root_descriptor["digest"]
        self.files["index.json"] = encoded(outer)

    def blob(self, raw, media):
        digest = hashlib.sha256(raw).hexdigest()
        self.files["blobs/sha256/" + digest] = raw
        return {"mediaType": media, "digest": "sha256:" + digest, "size": len(raw)}

    def write(self, path, extra=()):
        with tarfile.open(path, "w") as archive:
            for name, raw in self.files.items():
                member = tarfile.TarInfo(name)
                member.size = len(raw)
                archive.addfile(member, io.BytesIO(raw))
            for member, raw in extra:
                archive.addfile(member, io.BytesIO(raw) if raw is not None else None)

    def reports(self):
        artifacts = [{"id": "deb-fixture", "name": "nodejs", "version": "24.19.0", "type": "deb"},
                     {"id": "npm-fixture", "name": "openid-client", "version": "6.8.8", "type": "npm"}]
        syft = {"descriptor": {"name": "syft", "version": runner.SYFT_VERSION},
                "source": {"type": "image", "metadata": {"imageID": self.config_digest}}, "artifacts": artifacts}
        spdx = {"spdxVersion": "SPDX-2.3", "SPDXID": "SPDXRef-DOCUMENT",
                "creationInfo": {"creators": ["Tool: syft-" + runner.SYFT_VERSION]},
                "packages": [{"SPDXID": "SPDXRef-" + item["id"], "name": item["name"], "versionInfo": item["version"]}
                             for item in artifacts]}
        trivy = {"SchemaVersion": 2, "ArtifactName": "/input/image", "ArtifactType": "container_image",
                 "ArtifactID": self.config_digest, "Metadata": {"ImageID": self.config_digest,
                 "DiffIDs": self.diff_ids, "OS": {"Family": "debian", "Name": "13"}},
                 "Results": [{"Target": "debian fixture", "Class": "os-pkgs", "Type": "debian",
                              "Packages": [{"Name": "nodejs", "Version": "24.19.0"}]},
                             {"Target": "package-lock.json", "Class": "lang-pkgs", "Type": "npm",
                              "Packages": [{"Name": "openid-client", "Version": "6.8.8"}]}]}
        return syft, spdx, trivy


def db_fixture(path, now=NOW, **changes):
    (path / "db").mkdir(parents=True)
    metadata = {"Version": 2, "UpdatedAt": (now - dt.timedelta(hours=1)).isoformat(),
                "NextUpdate": (now + dt.timedelta(hours=1)).isoformat()}
    metadata.update(changes)
    (path / "db/metadata.json").write_bytes(encoded(metadata))
    (path / "db/trivy.db").write_bytes(b"synthetic database fixture; scanners are mocked\n")


class OfflineImageAssuranceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gis-security-test-")
        self.root = Path(self.temp.name)
        self.archive = self.root / "fixture.oci.tar"
        self.image = ImageFixture()
        self.image.write(self.archive)
        self.cache = self.root / "cache"
        db_fixture(self.cache, dt.datetime.now(dt.timezone.utc))
        self.output = self.root / "result"

    def tearDown(self):
        self.temp.cleanup()

    def assert_blocked(self, reason, call, *args):
        with self.assertRaises(runner.Blocked) as context:
            call(*args)
        self.assertEqual(reason, context.exception.code)

    def test_real_image_and_index_attestations_are_distinct(self):
        image = ImageFixture(index=True, attestation=True)
        image.write(self.archive)
        observed = runner.inspect_oci(self.archive, image.expected)
        self.assertEqual(image.runtime_digest, observed["manifest_digest"])
        self.assertEqual(image.expected, observed["requested_manifest_digest"])
        self.assertEqual(1, len(observed["attestations"]))
        self.assertFalse(observed["attestations_verified"])
        self.assertEqual(65532, observed["resolved_uid"])

    def test_buildkit_0322_max_provenance_oci11_empty_inline_config(self):
        # Matches the observed BuildKit 0.32.2 exporter shape, not signature proof.
        image = ImageFixture(index=True, attestation=True, oci11=True)
        image.write(self.archive)
        observed = runner.inspect_oci(self.archive, image.expected)
        self.assertEqual(image.runtime_digest, observed["manifest_digest"])
        self.assertEqual(1, len(observed["attestations"]))
        self.assertFalse(observed["attestations_verified"])

    def test_inline_oci_data_requires_exact_base64_digest_size_and_archived_blob(self):
        for inline, reason in (("!not-base64!", "invalid_inline_oci_data"),
                               ("e3w=", "inline_oci_data_mismatch"),
                               ("e30=AA==", "invalid_inline_oci_data")):
            with self.subTest(inline=inline):
                image = ImageFixture(index=True, attestation=True, oci11=True)
                image.mutate_attestation(lambda manifest: manifest["config"].update(data=inline))
                image.write(self.archive)
                self.assert_blocked(reason, runner.inspect_oci, self.archive, image.expected)
        image = ImageFixture(index=True, attestation=True, oci11=True)
        del image.files["blobs/sha256/" + hashlib.sha256(b"{}").hexdigest()]
        image.write(self.archive)
        self.assert_blocked("oci_descriptor_size_or_blob_mismatch", runner.inspect_oci, self.archive, image.expected)

    def test_remote_attestation_descriptor_never_uses_network(self):
        image = ImageFixture(index=True, attestation=True, oci11=True)
        image.mutate_attestation(lambda manifest: manifest["config"].update(urls=["https://fixture.invalid/config"]))
        image.write(self.archive)
        self.assert_blocked("external_oci_descriptor", runner.inspect_oci, self.archive, image.expected)

    def test_oci11_attestation_subject_must_match_runtime(self):
        image = ImageFixture(index=True, attestation=True, oci11=True)
        image.mutate_attestation(lambda manifest: manifest["subject"].update(mediaType=runner.IMAGE_CONFIG))
        image.write(self.archive)
        self.assert_blocked("attestation_subject_mismatch", runner.inspect_oci, self.archive, image.expected)

    def test_empty_config_does_not_become_an_executable_runtime_image(self):
        image = ImageFixture(index=True, attestation=True, oci11=True)
        outer = json.loads(image.files["index.json"])
        descriptor = outer["manifests"][0]
        index = json.loads(image.files.pop("blobs/sha256/" + descriptor["digest"][7:]))
        index["manifests"][1]["annotations"]["vnd.docker.reference.type"] = "runtime"
        descriptor.update(image.blob(encoded(index), runner.IMAGE_INDEX))
        image.expected = descriptor["digest"]
        image.files["index.json"] = encoded(outer)
        image.write(self.archive)
        self.assert_blocked("invalid_oci_config_media_type", runner.inspect_oci, self.archive, image.expected)

    def test_forged_requested_digest_is_blocked(self):
        self.assert_blocked("expected_manifest_not_reachable", runner.inspect_oci, self.archive, "sha256:" + "1" * 64)

    def test_tampered_content_addressed_blob_is_blocked(self):
        key = "blobs/sha256/" + self.image.config_digest[7:]
        self.image.files[key] += b" "
        self.image.write(self.archive)
        self.assert_blocked("oci_blob_digest_mismatch", runner.inspect_oci, self.archive, self.image.expected)

    def test_tampered_descriptor_size_is_blocked(self):
        index = json.loads(self.image.files["index.json"])
        index["manifests"][0]["size"] += 1
        self.image.files["index.json"] = encoded(index)
        self.image.write(self.archive)
        self.assert_blocked("oci_descriptor_size_or_blob_mismatch", runner.inspect_oci, self.archive, self.image.expected)

    def test_duplicate_outer_path_is_blocked(self):
        member = tarfile.TarInfo("index.json")
        raw = self.image.files["index.json"]
        member.size = len(raw)
        self.image.write(self.archive, [(member, raw)])
        self.assert_blocked("duplicate_oci_entry", runner.inspect_oci, self.archive, self.image.expected)

    def test_traversal_absolute_and_noncanonical_paths_are_blocked(self):
        for name in ("../escape", "/escape", "blobs/../escape", "blobs//escape", "blobs\\escape"):
            with self.subTest(name=name):
                member = tarfile.TarInfo(name)
                self.image.write(self.archive, [(member, b"")])
                self.assert_blocked("unsafe_oci_path", runner.inspect_oci, self.archive, self.image.expected)

    def test_outer_links_and_special_files_are_blocked_without_extraction(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE):
            with self.subTest(kind=kind):
                member = tarfile.TarInfo("escape")
                member.type = kind
                member.linkname = "../../outside"
                self.image.write(self.archive, [(member, None)])
                self.assert_blocked("oci_link_or_special_entry", runner.inspect_oci, self.archive, self.image.expected)
        self.assertFalse((self.root.parent / "outside").exists())

    def test_unreachable_blob_is_blocked(self):
        self.image.blob(b"unreachable", runner.IMAGE_CONFIG)
        self.image.write(self.archive)
        self.assert_blocked("unreachable_oci_blob", runner.inspect_oci, self.archive, self.image.expected)

    def test_duplicate_json_keys_are_blocked(self):
        self.image.files["oci-layout"] = b'{"imageLayoutVersion":"1.0.0","imageLayoutVersion":"1.0.0"}'
        self.image.write(self.archive)
        self.assert_blocked("duplicate_json_key", runner.inspect_oci, self.archive, self.image.expected)

    def test_root_and_missing_user_are_blocked(self):
        for user in ("0", "0:1000", "root", ""):
            with self.subTest(user=user):
                image = ImageFixture(user=user)
                image.write(self.archive)
                self.assert_blocked("image_user_not_nonroot", runner.inspect_oci, self.archive, image.expected)

    def test_named_user_resolves_actual_passwd_uid(self):
        image = ImageFixture(user="vscode")
        image.write(self.archive)
        self.assertEqual(1000, runner.inspect_oci(self.archive, image.expected)["resolved_uid"])

    def test_nonroot_looking_name_with_root_uid_is_blocked(self):
        image = ImageFixture(user="vscode", passwd={"etc/passwd": b"vscode:x:0:0:fixture:/home/vscode:/bin/sh\n"})
        image.write(self.archive)
        self.assert_blocked("image_user_not_nonroot", runner.inspect_oci, self.archive, image.expected)

    def test_named_user_with_deleted_passwd_is_blocked(self):
        image = ImageFixture(user="vscode", passwd={"etc/.wh.passwd": b""})
        image.write(self.archive)
        self.assert_blocked("unresolved_image_user", runner.inspect_oci, self.archive, image.expected)

    def test_decompressed_layer_bound_is_enforced(self):
        with patch.object(runner, "MAX_EXPANDED", 1):
            self.assert_blocked("expanded_layer_size_limit", runner.inspect_oci, self.archive, self.image.expected)

    def test_numeric_user_does_not_bypass_layer_tar_validation(self):
        self.assert_blocked("invalid_oci_archive_or_layer", self.inspect_corrupt_layer)

    def inspect_corrupt_layer(self):
        old = self.image.manifest["layers"][0]["digest"]
        del self.image.files["blobs/sha256/" + old[7:]]
        raw = b"not a tar layer" * 100
        layer = self.image.blob(gzip.compress(raw, mtime=0), "application/vnd.oci.image.layer.v1.tar+gzip")
        self.image.config["rootfs"]["diff_ids"] = ["sha256:" + hashlib.sha256(raw).hexdigest()]
        del self.image.files["blobs/sha256/" + self.image.config_digest[7:]]
        config = self.image.blob(encoded(self.image.config), runner.IMAGE_CONFIG)
        del self.image.files["blobs/sha256/" + self.image.runtime_digest[7:]]
        manifest = {"schemaVersion": 2, "mediaType": runner.IMAGE_MANIFEST, "config": config, "layers": [layer]}
        descriptor = self.image.blob(encoded(manifest), runner.IMAGE_MANIFEST)
        self.image.files["index.json"] = encoded({"schemaVersion": 2, "mediaType": runner.IMAGE_INDEX,
                                                 "manifests": [descriptor]})
        self.image.write(self.archive)
        return runner.inspect_oci(self.archive, descriptor["digest"])

    def test_stale_future_expired_and_wrong_schema_databases_are_blocked(self):
        cases = [("stale_or_future_trivy_db", {"UpdatedAt": (NOW - dt.timedelta(hours=24)).isoformat()}),
                 ("stale_or_future_trivy_db", {"UpdatedAt": (NOW + dt.timedelta(seconds=1)).isoformat()}),
                 ("expired_trivy_db", {"NextUpdate": NOW.isoformat()}),
                 ("unsupported_trivy_db_schema", {"Version": 1})]
        for index, (reason, changes) in enumerate(cases):
            with self.subTest(reason=reason, changes=changes):
                cache = self.root / f"cache-{index}"
                db_fixture(cache, NOW, **changes)
                self.assert_blocked(reason, runner.validate_db, cache, NOW)

    def test_db_inventory_is_closed_and_link_free(self):
        (self.cache / "other").write_text("unexpected")
        self.assert_blocked("db_unclosed_inventory", runner.validate_db, self.cache, NOW)
        (self.cache / "other").unlink()
        (self.cache / "db/trivy.db").unlink()
        (self.cache / "db/trivy.db").symlink_to(self.archive)
        self.assert_blocked("db_symlink_or_special_file", runner.validate_db, self.cache, NOW)

    def test_output_in_checkout_or_existing_shared_directory_is_blocked(self):
        self.assert_blocked("output_inside_build_context", runner.private_output, ROOT / "artifacts/security")
        self.output.mkdir(mode=0o755)
        self.output.chmod(0o755)
        self.assert_blocked("output_not_fresh_private_directory", runner.private_output, self.output)

    def test_source_symlink_is_blocked(self):
        link = self.root / "image-link"
        link.symlink_to(self.archive)
        self.assert_blocked("symlink_path", runner.snapshot, link, self.root / "copy", runner.MAX_ARCHIVE)

    def test_scanners_are_networkless_and_never_receive_socket_or_credentials(self):
        arguments = runner.container(runner.TRIVY_REFERENCE, ((self.archive, "/input/image.oci.tar"),
                                                             (self.cache, "/cache")))
        for flag in ("--pull=never", "--network=none", "--read-only", "--cap-drop=ALL",
                     "--security-opt=no-new-privileges", f"--user={os.getuid()}:{os.getgid()}"):
            self.assertIn(flag, arguments)
        self.assertTrue(any("size=4g" in value and "noexec,nosuid,nodev" in value for value in arguments))
        self.assertIn("--memory=6g", arguments)
        self.assertIn("--memory-swap=6g", arguments)
        self.assertIn("--cpus=2", arguments)
        self.assertIn("--pids-limit=256", arguments)
        self.assertTrue(all(value.endswith(",readonly") for value in arguments if value.startswith("--mount=")))
        self.assertFalse(any("docker.sock" in value or "DOCKER_CONFIG" in value for value in arguments))
        self.assertIn("--env=HTTPS_PROXY=", arguments)
        with patch.dict(os.environ, {"DOCKER_HOST": "tcp://unapproved", "DOCKER_CONTEXT": "unapproved"}):
            self.assertNotIn("DOCKER_HOST", runner.docker_env())
            self.assertNotIn("DOCKER_CONTEXT", runner.docker_env())

    def test_forged_tool_digest_or_version_cannot_pass(self):
        with patch.object(runner, "run_docker", return_value=encoded([{"Id": "sha256:" + "a" * 64,
                                                                            "RepoDigests": []}])):
            self.assert_blocked("preloaded_tool_digest_mismatch", runner.inspect_tool, runner.SYFT_REFERENCE)

    def test_actual_tool_version_mismatch_is_blocked(self):
        execute, _ = self.fake_docker()
        self.output.mkdir(mode=0o700)
        def wrong_version(args, **kwargs):
            if args[-3:] == ["version", "-o", "json"]:
                return encoded({"version": "0.0.0-synthetic"})
            return execute(args, **kwargs)
        with patch.object(runner, "run_docker", side_effect=wrong_version):
            self.assert_blocked("syft_version_mismatch", runner.verify_versions, self.output)

    def fake_docker(self, changes=None):
        reports = list(self.image.reports())
        if changes:
            changes(reports)
        calls = []

        def execute(args, **kwargs):
            calls.append(args)
            if args[:2] == ["image", "inspect"]:
                reference = args[2]
                digest = reference.split(":", 1)[0] + "@" + reference.split("@", 1)[1]
                return encoded([{"Id": "sha256:" + "a" * 64, "RepoDigests": [digest]}])
            if args[-3:] == ["version", "-o", "json"]:
                return encoded({"version": runner.SYFT_VERSION})
            if args[-1] == "--version":
                return b"Version: 0.74.0\n"
            if "--output=syft-json" in args:
                return encoded(reports[0])
            if "--output=spdx-json" in args:
                return encoded(reports[1])
            if "--format=json" in args:
                return encoded(reports[2])
            self.fail("unexpected subprocess contract")

        return execute, calls

    def run_mock(self, changes=None):
        execute, calls = self.fake_docker(changes)
        with patch.object(runner, "run_docker", side_effect=execute):
            code = runner.assure(self.archive, self.image.expected, self.cache, self.output)
        return code, json.loads((self.output / "receipt.json").read_bytes()), calls

    def test_complete_mock_retains_binding_and_raw_evidence(self):
        code, receipt, calls = self.run_mock()
        self.assertEqual(0, code)
        self.assertEqual("PASS", receipt["status"])
        self.assertEqual(hashlib.sha256(self.archive.read_bytes()).hexdigest(), receipt["archive"]["sha256"])
        self.assertEqual(self.image.config_digest, receipt["image"]["config_digest"])
        self.assertEqual(2, receipt["database"]["schema_version"])
        self.assertEqual({severity: 0 for severity in runner.SEVERITIES}, receipt["scan"]["severity_counts"])
        self.assertEqual("not_assessed", receipt["hosted_authentication"])
        self.assertFalse(receipt["deployment_authorised"])
        self.assertEqual(7, len(calls))
        self.assertTrue({"syft.json", "sbom.spdx.json", "trivy.json", "db-inventory.json"}
                        <= {item["path"] for item in receipt["evidence"]})
        self.assertNotIn(str(self.root), json.dumps(receipt))
        self.assertEqual(0o400, (self.output / "inputs/image.oci.tar").stat().st_mode & 0o777)
        self.assertEqual(0o600, (self.output / "receipt.json").stat().st_mode & 0o777)
        trivy_command = calls[-1]
        self.assertIn("--skip-db-update", trivy_command)
        self.assertIn("--skip-java-db-update", trivy_command)
        self.assertIn("--offline-scan", trivy_command)
        self.assertIn("--severity=UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL", trivy_command)

    def test_normalized_input_preserves_child_config_diffids_and_original_authority(self):
        self.image = ImageFixture(index=True, attestation=True, oci11=True)
        self.image.write(self.archive)
        original_sha = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        code, receipt, calls = self.run_mock()
        self.assertEqual(0, code)
        self.assertEqual(original_sha, receipt["archive"]["sha256"])
        self.assertEqual(self.image.expected, receipt["image"]["requested_manifest_digest"])
        self.assertEqual(1, len(receipt["image"]["attestations"]))
        self.assertFalse(receipt["image"]["attestations_verified"])
        scanner_input = receipt["scanner_input"]
        self.assertEqual("validated_runtime_manifest_closure_directory", scanner_input["normalization"])
        self.assertEqual(original_sha, scanner_input["original_archive_sha256"])
        self.assertTrue(scanner_input["inventory_sha256"])
        normalized = self.output / scanner_input["evidence_path"]
        inspected = runner.validate_scanner_directory(normalized, receipt["image"])
        self.assertEqual(inspected["inventory_sha256"], scanner_input["inventory_sha256"])
        index = json.loads((normalized / "index.json").read_text())
        self.assertEqual(1, len(index["manifests"]))
        self.assertEqual(self.image.runtime_digest, index["manifests"][0]["digest"])
        original_image = runner.inspect_oci(self.archive, self.image.expected)
        self.assertEqual(original_image["config_digest"], scanner_input["config_digest"])
        self.assertEqual(original_image["diff_ids"], scanner_input["diff_ids"])
        self.assertTrue(any(str(normalized) in argument for argument in calls[-1]))
        self.assertEqual(original_sha, hashlib.sha256(self.archive.read_bytes()).hexdigest())

    def test_normalizer_refuses_config_identity_mismatch(self):
        image = runner.inspect_oci(self.archive, self.image.expected)
        image["config_digest"] = "sha256:" + "f" * 64
        self.assert_blocked("normalization_binding_mismatch", runner.normalize_scanner_directory,
                            self.archive, self.root / "derived", image)

    def test_normalized_directory_mutation_blocks_while_original_stays_bound(self):
        self.image = ImageFixture(index=True, attestation=True, oci11=True)
        self.image.write(self.archive)
        execute, _ = self.fake_docker()
        def tamper(args, **kwargs):
            raw = execute(args, **kwargs)
            if "--format=json" in args:
                path = self.output / "inputs/scanner-image/index.json"
                path.chmod(0o600)
                with path.open("ab") as stream:
                    stream.write(b" ")
            return raw
        with patch.object(runner, "run_docker", side_effect=tamper):
            self.assertEqual(2, runner.assure(self.archive, self.image.expected, self.cache, self.output))
        receipt = json.loads((self.output / "receipt.json").read_bytes())
        self.assertEqual("immutable_scanner_directory_changed", receipt["blocked_reason"])
        original = self.output / "inputs/image.oci.tar"
        self.assertEqual(receipt["archive"]["sha256"], hashlib.sha256(original.read_bytes()).hexdigest())

    def test_every_severity_is_counted_and_high_blocks_with_raw_report(self):
        def changes(reports):
            reports[2]["Results"][1]["Vulnerabilities"] = [
                {"VulnerabilityID": "SYNTHETIC-" + severity, "PkgName": "openid-client",
                 "InstalledVersion": "6.8.8", "Severity": severity} for severity in runner.SEVERITIES]
        code, receipt, _ = self.run_mock(changes)
        self.assertEqual(2, code)
        self.assertEqual("high_or_critical_vulnerabilities", receipt["blocked_reason"])
        self.assertEqual({severity: 1 for severity in runner.SEVERITIES}, receipt["scan"]["severity_counts"])
        self.assertTrue((self.output / "trivy.json").exists())

    def test_empty_malformed_or_wrong_image_scan_cannot_pass(self):
        image = runner.inspect_oci(self.archive, self.image.expected)
        syft, spdx, original = self.image.reports()
        sbom = runner.validate_sbom(syft, spdx, image)
        cases = [("empty_or_invalid_trivy_results", lambda report: report.update(Results=[])),
                 ("empty_or_invalid_trivy_package_inventory", lambda report: report["Results"][0].update(Packages=[])),
                 ("invalid_trivy_package_class", lambda report: report["Results"][0].update(Class="secret")),
                 ("trivy_image_binding_mismatch", lambda report: report["Metadata"].update(ImageID="sha256:" + "f" * 64)),
                 ("incomplete_trivy_os_inventory", lambda report: report["Results"][0]["Packages"][0].update(Name="unrelated")),
                 ("incomplete_trivy_language_inventory", lambda report: report["Results"][1]["Packages"][0].update(Name="unrelated")),
                 ("missing_trivy_language_inventory", lambda report: report["Results"].pop()),
                 ("missing_or_duplicate_trivy_os_inventory", lambda report: report["Results"].pop(0))]
        for reason, mutate in cases:
            with self.subTest(reason=reason):
                report = json.loads(json.dumps(original))
                mutate(report)
                self.assert_blocked(reason, runner.validate_trivy, report, image, sbom)

    def test_empty_spdx_and_syft_inventory_cannot_pass(self):
        image = runner.inspect_oci(self.archive, self.image.expected)
        syft, spdx, _ = self.image.reports()
        spdx["packages"] = []
        self.assert_blocked("empty_or_incomplete_spdx_inventory", runner.validate_sbom, syft, spdx, image)
        syft["artifacts"] = []
        self.assert_blocked("empty_or_invalid_syft_inventory", runner.validate_sbom, syft, spdx, image)

    def test_unassessed_package_type_is_blocked(self):
        image = runner.inspect_oci(self.archive, self.image.expected)
        syft, spdx, trivy = self.image.reports()
        syft["artifacts"][0]["type"] = "unassessed-fixture-type"
        sbom = runner.validate_sbom(syft, spdx, image)
        self.assert_blocked("unassessed_syft_package_type", runner.validate_trivy, trivy, image, sbom)

    def test_real_node_pkg_report_type_covers_npm_installed_inventory(self):
        image = runner.inspect_oci(self.archive, self.image.expected)
        syft, spdx, trivy = self.image.reports()
        trivy["Results"][1]["Type"] = "node-pkg"
        summary = runner.validate_trivy(trivy, image, runner.validate_sbom(syft, spdx, image))
        self.assertEqual(1, summary["result_types"]["node-pkg"])

    def test_coverage_failure_still_retains_validated_vulnerability_counts(self):
        def changes(reports):
            reports[0]["artifacts"][0]["type"] = "binary"
            reports[2]["Results"][1]["Vulnerabilities"] = [{"VulnerabilityID": "SYNTHETIC-CRITICAL",
                "PkgName": "openid-client", "InstalledVersion": "6.8.8", "Severity": "CRITICAL"}]
        code, receipt, _ = self.run_mock(changes)
        self.assertEqual(2, code)
        self.assertEqual("unassessed_syft_package_type", receipt["blocked_reason"])
        self.assertEqual(1, receipt["scan"]["severity_counts"]["CRITICAL"])
        self.assertEqual("blocked", receipt["scan"]["coverage"])

    def test_versionless_go_binary_inventory_preserves_high_counts_and_blocks(self):
        def changes(reports):
            reports[2]["Results"].append({"Target": "usr/local/bin/terraform", "Class": "lang-pkgs",
                "Type": "gobinary", "Packages": [{"Name": "synthetic/main", "Version": None},
                    {"Name": "synthetic/dependency", "Version": "v1.0.0"}],
                "Vulnerabilities": [{"VulnerabilityID": "SYNTHETIC-HIGH", "PkgName": "synthetic/dependency",
                    "InstalledVersion": "v1.0.0", "Severity": "HIGH"}]})
        code, receipt, _ = self.run_mock(changes)
        self.assertEqual(2, code)
        self.assertEqual("invalid_package_inventory", receipt["blocked_reason"])
        self.assertEqual("blocked", receipt["scan"]["coverage"])
        self.assertEqual(1, receipt["scan"]["severity_counts"]["HIGH"])
        self.assertEqual(4, receipt["scan"]["inventory_entries"])
        self.assertEqual(3, receipt["scan"]["versioned_packages"])
        self.assertEqual(1, receipt["scan"]["versionless_packages"])
        self.assertEqual(3, receipt["scan"]["packages"])
        self.assertTrue((self.output / "trivy.json").exists())

    def test_missing_tools_write_blocked_receipt_without_fabricated_scan(self):
        with patch.object(runner, "run_docker", side_effect=runner.Blocked("scanner_or_preloaded_tool_unavailable")):
            code = runner.assure(self.archive, self.image.expected, self.cache, self.output)
        receipt = json.loads((self.output / "receipt.json").read_bytes())
        self.assertEqual(2, code)
        self.assertEqual("BLOCKED", receipt["status"])
        self.assertNotIn("scan", receipt)

    def test_postscan_snapshot_tampering_is_blocked(self):
        execute, _ = self.fake_docker()
        def tamper(args, **kwargs):
            raw = execute(args, **kwargs)
            if "--format=json" in args:
                path = self.output / "inputs/image.oci.tar"
                path.chmod(0o600)
                with path.open("ab") as stream:
                    stream.write(b"tampering")
            return raw
        with patch.object(runner, "run_docker", side_effect=tamper):
            self.assertEqual(2, runner.assure(self.archive, self.image.expected, self.cache, self.output))
        receipt = json.loads((self.output / "receipt.json").read_bytes())
        self.assertEqual("immutable_archive_changed", receipt["blocked_reason"])

    def test_executable_cli_calls_only_closed_offline_docker_contract(self):
        reports = self.image.reports()
        fixtures = self.root / "reports.json"
        fixtures.write_bytes(encoded(reports))
        log = self.root / "calls.jsonl"
        executable = self.root / "docker"
        executable.write_text(f'''#!{sys.executable}
import json, sys
args=sys.argv[1:]
with open({str(log)!r}, 'a') as f: f.write(json.dumps(args)+'\\n')
assert args[0]=='--host=unix:///var/run/docker.sock'
args=args[1:]
reports=json.load(open({str(fixtures)!r}))
if args[:2]==['image','inspect']:
 ref=args[2]; print(json.dumps([{{'Id':'sha256:'+'a'*64,'RepoDigests':[ref.split(':',1)[0]+'@'+ref.split('@',1)[1]]}}]))
elif args[-3:]==['version','-o','json']: print(json.dumps({{'version':'1.42.2'}}))
elif args[-1]=='--version': print('Version: 0.74.0')
elif '--output=syft-json' in args: print(json.dumps(reports[0]))
elif '--output=spdx-json' in args: print(json.dumps(reports[1]))
elif '--format=json' in args: print(json.dumps(reports[2]))
else: sys.exit(9)
''')
        executable.chmod(0o700)
        environment = os.environ.copy()
        environment["PATH"] = str(self.root) + os.pathsep + environment["PATH"]
        environment["DOCKER_HOST"] = "tcp://unapproved:2375"
        observed = subprocess.run([str(CLI), "--archive", str(self.archive), "--manifest-digest", self.image.expected,
                                   "--db-cache", str(self.cache), "--output-dir", str(self.output)],
                                  capture_output=True, timeout=30, env=environment)
        self.assertEqual(0, observed.returncode, observed.stderr.decode())
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertEqual(7, len(calls))
        self.assertTrue(all(args[0] == "--host=unix:///var/run/docker.sock" for args in calls))
        self.assertTrue(all("--network=none" in args for args in calls if args[1] == "run"))
        self.assertFalse(any("pull" == value or "--download-db-only" in value for args in calls for value in args))

    def test_executable_cli_no_docker_fails_closed(self):
        environment = os.environ.copy()
        environment["PATH"] = str(self.root)
        observed = subprocess.run([sys.executable, str(CLI), "--archive", str(self.archive),
                                   "--manifest-digest", self.image.expected, "--db-cache", str(self.cache),
                                   "--output-dir", str(self.output)], capture_output=True, timeout=30, env=environment)
        self.assertEqual(2, observed.returncode)
        receipt = json.loads((self.output / "receipt.json").read_bytes())
        self.assertEqual("docker_unavailable", receipt["blocked_reason"])
        self.assertNotIn("scan", receipt)
        self.assertTrue((self.output / "syft-inspect.stderr.txt").exists())

    def test_nonzero_subprocess_retains_sanitized_bounded_stderr(self):
        executable = self.root / "docker"
        executable.write_text(f'''#!{sys.executable}
import sys
sys.stderr.write('unable to populate OCI layer cache: no space left on device\\n')
sys.stderr.write('Authorization: Bearer fixture\\napi_key=synthetic\\n')
sys.stderr.write({str(self.archive)!r}+'\\n')
sys.exit(1)
''')
        executable.chmod(0o700)
        diagnostic = self.root / "failure.stderr.txt"
        arguments = runner.container(runner.SYFT_REFERENCE, ((self.archive, "/input/image.oci.tar"),))
        with patch.dict(os.environ, {"PATH": str(self.root) + os.pathsep + os.environ["PATH"]}):
            self.assert_blocked("scanner_or_preloaded_tool_unavailable", runner.run_docker,
                                arguments, 5, 4096, diagnostic)
        text = diagnostic.read_text()
        self.assertIn("no space left on device", text)
        self.assertIn("[redacted]", text)
        self.assertNotIn("Bearer fixture", text)
        self.assertNotIn("api_key=synthetic", text)
        self.assertNotIn(str(self.archive), text)
        self.assertIn("/input/image.oci.tar", text)
        self.assertEqual(0o600, diagnostic.stat().st_mode & 0o777)
        self.assertLessEqual(diagnostic.stat().st_size, runner.MAX_DIAGNOSTIC)

    def test_oversized_subprocess_diagnostic_is_bounded_and_blocks(self):
        executable = self.root / "docker"
        executable.write_text(f'''#!{sys.executable}
import sys
if 'container' in sys.argv: sys.exit(0)
sys.stderr.write('x'*({runner.MAX_DIAGNOSTIC}+1024))
''')
        executable.chmod(0o700)
        diagnostic = self.root / "large.stderr.txt"
        with patch.dict(os.environ, {"PATH": str(self.root) + os.pathsep + os.environ["PATH"]}):
            self.assert_blocked("scanner_output_limit", runner.run_docker,
                                runner.container(runner.SYFT_REFERENCE), 5, 4096, diagnostic)
        self.assertLessEqual(diagnostic.stat().st_size, runner.MAX_DIAGNOSTIC)
        self.assertIn("truncated", diagnostic.read_text())


if __name__ == "__main__":
    unittest.main()
