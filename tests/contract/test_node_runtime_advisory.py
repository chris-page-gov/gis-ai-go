from __future__ import annotations

import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gateway_image import (  # noqa: E402
    NODE_BINARY_SHA256,
    NODE_RUNTIME_CPE,
    NODE_RUNTIME_PURL,
    NODE_SECURITY_ADVISORY_URL,
    NODE_UPSTREAM_ARCHIVE_SHA256,
    NODE_UPSTREAM_ARCHIVE_URL,
    canonical_json_bytes,
)
from node_runtime_advisory import (  # noqa: E402
    GRYPE_INPUT_PATH,
    GRYPE_REFERENCE,
    GRYPE_VERSION,
    MAX_GRYPE_REPORT_BYTES,
    NODE_CALIBRATION_HIGH_IDS,
    NODE_ROLE_FILES,
    NODE_ROLES,
    _actual_assessment,
    _bytes_binding,
    _calibration_projection,
    _database_age_seconds,
    _provider_age_seconds,
    _role_evidence,
    _run_grype,
    download_database_archive,
    extract_node_identity,
    make_node_input,
    normalise_cyclonedx_report,
    normalise_json_report,
    restore_database_from_scan,
    verify_node_advisory,
)


ROOTFS_SHA256 = "d" * 64
DATABASE_BUILT = "2026-08-23T06:15:27Z"
DATABASE_CAPTURED = "2026-08-23T00:18:37Z"
ASSESSED_AT = "2026-08-24T06:15:27Z"


def node_fixture() -> tuple[dict[str, object], dict[str, object]]:
    receipt: dict[str, object] = {
        "build": {
            "runtime_composition": {
                "node_binary": {
                    "version": "24.19.0",
                    "path": "/usr/local/bin/node",
                    "sha256": NODE_BINARY_SHA256,
                    "purl": NODE_RUNTIME_PURL,
                    "cpe": NODE_RUNTIME_CPE,
                    "upstream_archive_url": NODE_UPSTREAM_ARCHIVE_URL,
                    "upstream_archive_sha256": NODE_UPSTREAM_ARCHIVE_SHA256,
                    "security_advisory_url": NODE_SECURITY_ADVISORY_URL,
                }
            }
        },
        "image": {
            "rootfs": {
                "inventory_sha256": ROOTFS_SHA256,
                "critical_entries": [
                    {
                        "path": "/usr/local/bin/node",
                        "sha256": NODE_BINARY_SHA256,
                    }
                ],
            }
        },
    }
    sbom: dict[str, object] = {
        "components": [
            {
                "type": "application",
                "name": "node",
                "version": "24.19.0",
                "purl": NODE_RUNTIME_PURL,
                "cpe": NODE_RUNTIME_CPE,
                "properties": [
                    {
                        "name": "syft:location:0:path",
                        "value": "/usr/local/bin/node",
                    }
                ],
            },
            {
                "type": "file",
                "name": "node",
                "version": "24.19.0",
                "hashes": [{"alg": "SHA-256", "content": NODE_BINARY_SHA256}],
                "properties": [
                    {
                        "name": "gis-ai-go:runtime-file-path",
                        "value": "/usr/local/bin/node",
                    },
                    {
                        "name": "gis-ai-go:rootfs-inventory-sha256",
                        "value": ROOTFS_SHA256,
                    },
                    {
                        "name": "gis-ai-go:upstream-archive",
                        "value": NODE_UPSTREAM_ARCHIVE_URL,
                    },
                    {
                        "name": "gis-ai-go:upstream-archive-sha256",
                        "value": NODE_UPSTREAM_ARCHIVE_SHA256,
                    },
                ],
            },
        ]
    }
    return sbom, receipt


def grype_default_ignore_rules() -> list[dict[str, object]]:
    packages = (
        ("rpm", "kernel-headers", "kernel"),
        ("deb", "linux(-.*)?-headers-.*", "linux.*"),
        ("deb", "linux-libc-dev", "linux"),
        ("deb", "linux-kbuild-.*", "linux.*"),
    )
    return [
        {
            "vulnerability": "",
            "include-aliases": False,
            "reason": "",
            "namespace": "",
            "fix-state": "",
            "package": {
                "name": name,
                "version": "",
                "language": "",
                "type": package_type,
                "location": "",
                "upstream-name": upstream,
            },
            "vex-status": "",
            "vex-justification": "",
            "match-type": "exact-indirect-match",
        }
        for package_type, name, upstream in packages
    ]


def database_source(sha256: str) -> str:
    return (
        "https://grype.anchore.io/databases/v6/"
        "vulnerability-db_v6.1.9_2026-08-23T00:17:31Z_1787465727.tar.zst"
        f"?checksum=sha256%3A{sha256}"
    )


def grype_json_report(
    input_document: dict[str, object],
    *,
    database_sha256: str,
    vulnerability_ids: tuple[str, ...] = (),
    manual_import: bool = False,
) -> dict[str, object]:
    component = input_document["components"][0]  # type: ignore[index]
    version = component["version"]  # type: ignore[index]
    purl = component["purl"]  # type: ignore[index]
    cpe = component["cpe"]  # type: ignore[index]
    matches = []
    for identifier in vulnerability_ids:
        matches.append(
            {
                "artifact": {
                    "name": "node",
                    "version": version,
                    "type": "UnknownPackage",
                    "purl": purl,
                    "cpes": [cpe],
                },
                "vulnerability": {
                    "id": identifier,
                    "severity": "High",
                    "namespace": "nvd:cpe",
                    "fix": {"state": "fixed", "versions": ["24.18.1"]},
                },
                "matchDetails": [
                    {
                        "type": "cpe-match",
                        "matcher": "stock-matcher",
                        "searchedBy": {
                            "namespace": "nvd:cpe",
                            "cpes": [cpe],
                            "package": {"name": "node", "version": version},
                        },
                        "found": {
                            "vulnerabilityID": identifier,
                            "versionConstraint": "< 24.18.1 (unknown)",
                            "cpes": ["cpe:2.3:a:nodejs:node.js:*:*:*:*:*:*:*:*"],
                        },
                        "fix": {"suggestedVersion": "24.18.1"},
                    }
                ],
            }
        )
    return {
        "matches": matches,
        "source": {"type": "sbom-file", "target": GRYPE_INPUT_PATH},
        "descriptor": {
            "name": "grype",
            "version": GRYPE_VERSION,
            "configuration": {
                "match": {"stock": {"using-cpes": True}},
                "db": {
                    "auto-update": False,
                    "validate-by-hash-on-start": True,
                    "validate-age": False,
                    "require-update-check": False,
                },
                "check-for-app-update": False,
                "add-cpes-if-none": False,
                "show-suppressed": True,
                "vex-documents": [],
                "ignore-wontfix": "",
                "only-fixed": False,
                "only-notfixed": False,
                "exclude": [],
                "ignore": grype_default_ignore_rules(),
                "externalSources": {"enable": False},
            },
            "db": {
                "status": {
                    "schemaVersion": "v6.1.9",
                    "from": (
                        "manual import"
                        if manual_import
                        else database_source(database_sha256)
                    ),
                    "built": DATABASE_BUILT,
                    "valid": True,
                },
                "providers": {
                    "nvd": {
                        "captured": DATABASE_CAPTURED,
                        "input": "xxh64:bb284f07d6636ef2",
                    }
                },
            },
        },
    }


def grype_cyclonedx_report(
    input_document: dict[str, object], *, vulnerability_ids: tuple[str, ...] = ()
) -> dict[str, object]:
    component = input_document["components"][0]  # type: ignore[index]
    version = component["version"]  # type: ignore[index]
    purl = component["purl"]  # type: ignore[index]
    cpe = component["cpe"]  # type: ignore[index]
    reference = f"{purl}?package-id={quote(str(purl), safe='')}"
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.7",
        "metadata": {
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "author": "anchore",
                        "name": "grype",
                        "version": GRYPE_VERSION,
                    }
                ]
            }
        },
        "components": [
            {
                "bom-ref": "urn:gis-ai-go:node-runtime-advisory-input",
                "type": "library",
                "name": "gis-ai-go-node-runtime-advisory-input",
                "version": version,
            },
            {
                "bom-ref": reference,
                "type": "library",
                "name": "node",
                "version": version,
                "purl": purl,
                "cpe": cpe,
            },
        ],
        "vulnerabilities": [
            {"id": identifier, "affects": [{"ref": reference}]}
            for identifier in vulnerability_ids
        ],
    }


class NodeRuntimeAdvisoryTests(unittest.TestCase):
    def test_exact_node_identity_is_bound_across_receipt_sbom_and_rootfs(self) -> None:
        sbom, receipt = node_fixture()
        identity = extract_node_identity(sbom, receipt)
        self.assertEqual(identity["purl"], NODE_RUNTIME_PURL)
        self.assertEqual(identity["cpe"], NODE_RUNTIME_CPE)
        self.assertEqual(identity["file_sha256"], NODE_BINARY_SHA256)

        mutations = []
        wrong_purl = copy.deepcopy((sbom, receipt))
        wrong_purl[0]["components"][0]["purl"] = "pkg:generic/node@24.18.0"  # type: ignore[index]
        mutations.append(wrong_purl)
        wrong_cpe = copy.deepcopy((sbom, receipt))
        wrong_cpe[0]["components"][0]["cpe"] = (  # type: ignore[index]
            "cpe:2.3:a:nodejs:node.js:24.18.0:*:*:*:*:*:*:*"
        )
        mutations.append(wrong_cpe)
        wrong_hash = copy.deepcopy((sbom, receipt))
        wrong_hash[0]["components"][1]["hashes"][0]["content"] = "0" * 64  # type: ignore[index]
        mutations.append(wrong_hash)
        second_application = copy.deepcopy((sbom, receipt))
        second_application[0]["components"].append(  # type: ignore[index]
            copy.deepcopy(second_application[0]["components"][0])  # type: ignore[index]
        )
        mutations.append(second_application)
        second_executable = copy.deepcopy((sbom, receipt))
        shadow = copy.deepcopy(second_executable[0]["components"][1])  # type: ignore[index]
        shadow["properties"][0]["value"] = "/opt/node"  # type: ignore[index]
        second_executable[0]["components"].append(shadow)  # type: ignore[index]
        mutations.append(second_executable)
        for altered_sbom, altered_receipt in mutations:
            with self.subTest(altered=altered_sbom), self.assertRaises(ValueError):
                extract_node_identity(altered_sbom, altered_receipt)

    def test_report_requires_visible_component_exact_cpe_and_no_suppression(self) -> None:
        sbom, receipt = node_fixture()
        identity = extract_node_identity(sbom, receipt)
        input_document = make_node_input(
            identity, version="24.18.0", calibration="affected"
        )
        report = grype_json_report(
            input_document,
            database_sha256="a" * 64,
            vulnerability_ids=tuple(sorted(NODE_CALIBRATION_HIGH_IDS)),
        )
        projected = normalise_json_report(report, input_document)
        self.assertEqual(
            {item["id"] for item in projected["matches"]},
            NODE_CALIBRATION_HIGH_IDS,
        )

        ignored = copy.deepcopy(report)
        ignored["ignoredMatches"] = [copy.deepcopy(ignored["matches"][0])]  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "match inventory"):
            normalise_json_report(ignored, input_document)

        synthesised = copy.deepcopy(report)
        synthesised["descriptor"]["configuration"]["add-cpes-if-none"] = True  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "offline CPE mode"):
            normalise_json_report(synthesised, input_document)

        node_ignore = copy.deepcopy(report)
        node_ignore["descriptor"]["configuration"]["ignore"][0]["package"][  # type: ignore[index]
            "name"
        ] = "node"
        with self.assertRaisesRegex(ValueError, "ignore rules"):
            normalise_json_report(node_ignore, input_document)

        excluded = copy.deepcopy(report)
        excluded["descriptor"]["configuration"]["exclude"] = ["/usr/local/bin/node"]  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "offline CPE mode"):
            normalise_json_report(excluded, input_document)

        no_nvd = copy.deepcopy(report)
        no_nvd["descriptor"]["db"]["providers"].pop("nvd")  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "NVD"):
            normalise_json_report(no_nvd, input_document)

    def test_cyclonedx_report_requires_one_node_and_exact_affects_reference(self) -> None:
        sbom, receipt = node_fixture()
        identity = extract_node_identity(sbom, receipt)
        input_document = make_node_input(
            identity, version="24.18.0", calibration="affected"
        )
        report = grype_cyclonedx_report(
            input_document,
            vulnerability_ids=tuple(sorted(NODE_CALIBRATION_HIGH_IDS)),
        )
        projected = normalise_cyclonedx_report(report, input_document)
        self.assertEqual(set(projected["vulnerability_ids"]), NODE_CALIBRATION_HIGH_IDS)

        invisible = copy.deepcopy(report)
        invisible["components"] = []
        with self.assertRaisesRegex(ValueError, "one exact Node"):
            normalise_cyclonedx_report(invisible, input_document)

        wrong_reference = copy.deepcopy(report)
        wrong_reference["vulnerabilities"][0]["affects"][0]["ref"] = "other"  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "Node binding"):
            normalise_cyclonedx_report(wrong_reference, input_document)

    def test_calibration_requires_positive_and_fixed_boundary_controls(self) -> None:
        roles = {
            "actual": {
                "matched_ids": [],
                "high_critical_ids": [],
                "component_visible": True,
            },
            "affected": {
                "matched_ids": sorted(NODE_CALIBRATION_HIGH_IDS),
                "high_critical_ids": sorted(NODE_CALIBRATION_HIGH_IDS),
                "component_visible": True,
            },
            "fixed": {
                "matched_ids": [],
                "high_critical_ids": [],
                "component_visible": True,
            },
        }
        self.assertTrue(_calibration_projection(roles)["passed"])
        missing = copy.deepcopy(roles)
        missing["affected"]["matched_ids"].pop()
        with self.assertRaisesRegex(ValueError, "fixed security boundary"):
            _calibration_projection(missing)
        still_affected = copy.deepcopy(roles)
        still_affected["fixed"]["matched_ids"] = [next(iter(NODE_CALIBRATION_HIGH_IDS))]
        with self.assertRaisesRegex(ValueError, "fixed security boundary"):
            _calibration_projection(still_affected)
        downgraded = copy.deepcopy(roles)
        downgraded["affected"]["high_critical_ids"] = []
        with self.assertRaisesRegex(ValueError, "fixed security boundary"):
            _calibration_projection(downgraded)

    def test_actual_assessment_rejects_every_high_or_critical_match(self) -> None:
        actual = {
            "matched_ids": ["CVE-2026-99999"],
            "high_critical_ids": ["CVE-2026-99999"],
            "component_visible": True,
        }
        with self.assertRaisesRegex(ValueError, "High or Critical"):
            _actual_assessment(actual)
        actual["high_critical_ids"] = []
        self.assertEqual(_actual_assessment(actual)["matched_ids"], ["CVE-2026-99999"])

    def test_database_freshness_is_bound_to_original_assessment_time(self) -> None:
        database = {
            "built": DATABASE_BUILT,
            "provider": {"captured": DATABASE_CAPTURED},
        }
        self.assertEqual(_database_age_seconds(database, ASSESSED_AT), 86_400)
        self.assertEqual(_provider_age_seconds(database, ASSESSED_AT), 107_810)
        with self.assertRaisesRegex(ValueError, "not current enough"):
            _database_age_seconds(database, "2026-08-27T06:15:28Z")
        with self.assertRaisesRegex(ValueError, "not current enough"):
            _database_age_seconds(database, "2026-08-23T06:15:26Z")
        stale_provider = copy.deepcopy(database)
        stale_provider["provider"]["captured"] = "2026-08-20T00:18:37Z"  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "provider is not current enough"):
            _provider_age_seconds(stale_provider, ASSESSED_AT)
        future_provider = copy.deepcopy(database)
        future_provider["provider"]["captured"] = "2026-08-23T06:15:28Z"  # type: ignore[index]
        with self.assertRaisesRegex(ValueError, "provider is not current enough"):
            _provider_age_seconds(future_provider, ASSESSED_AT)

    def _write_retained_fixture(
        self, directory: Path
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        sbom, receipt = node_fixture()
        identity = extract_node_identity(sbom, receipt)
        archive = directory / "gateway-node.grype-db.tar.zst"
        archive.write_bytes(b"bounded-test-database")
        database_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()
        (directory / "gateway-node.grype-db.tar.zst.sha256").write_text(
            f"{database_sha256}  {archive.name}\n", encoding="utf-8"
        )
        roles: dict[str, dict[str, object]] = {}
        database: dict[str, object] | None = None
        configuration: dict[str, object] | None = None
        source_binding = {
            "schema_version": "v6.1.9",
            "source_url": database_source(database_sha256),
            "source_sha256": database_sha256,
            "built": DATABASE_BUILT,
            "valid": True,
        }
        for role, (version, calibration) in NODE_ROLES.items():
            input_document = make_node_input(
                identity, version=version, calibration=calibration
            )
            identifiers = (
                tuple(sorted(NODE_CALIBRATION_HIGH_IDS))
                if role == "affected"
                else ()
            )
            report = grype_json_report(
                input_document,
                database_sha256=database_sha256,
                vulnerability_ids=identifiers,
                manual_import=True,
            )
            cdx = grype_cyclonedx_report(
                input_document, vulnerability_ids=identifiers
            )
            projected_json = normalise_json_report(
                report, input_document, database_source=source_binding
            )
            projected_cdx = normalise_cyclonedx_report(cdx, input_document)
            input_bytes = canonical_json_bytes(input_document)
            report_bytes = canonical_json_bytes(report)
            cdx_bytes = canonical_json_bytes(cdx)
            files = NODE_ROLE_FILES[role]
            (directory / files["input"]).write_bytes(input_bytes)
            (directory / files["json_report"]).write_bytes(report_bytes)
            (directory / files["cyclonedx_report"]).write_bytes(cdx_bytes)
            roles[role] = _role_evidence(
                role=role,
                version=version,
                input_bytes=input_bytes,
                report_bytes=report_bytes,
                cdx_bytes=cdx_bytes,
                projected_json=projected_json,
                projected_cdx=projected_cdx,
            )
            database = projected_json["database"]
            configuration = projected_json["configuration"]
        assert database is not None and configuration is not None
        database.update(
            {
                "assessed_at": ASSESSED_AT,
                "age_seconds": 86_400,
                "provider_age_seconds": 107_810,
                "archive": {
                    "file": archive.name,
                    "sha256": database_sha256,
                    "bytes": archive.stat().st_size,
                },
                "expanded_files": [
                    {"path": "6/import.json", "sha256": "a" * 64, "bytes": 1},
                    {
                        "path": "6/vulnerability.db",
                        "sha256": "b" * 64,
                        "bytes": 2,
                    },
                ],
            }
        )
        node: dict[str, object] = {
            "scanner": {
                "image": GRYPE_REFERENCE,
                "version": GRYPE_VERSION,
                "platform": "linux/amd64",
            },
            "component": identity,
            "database": database,
            "configuration": configuration,
            "roles": roles,
            "calibration": _calibration_projection(roles),
            "assessment": _actual_assessment(roles["actual"]),
            "replay": {
                "pull": "never",
                "network": "none",
                "database_import": True,
                "database_age_validation": False,
                "database_hash_validation": True,
                "stock_cpe_matching": True,
            },
        }
        return node, sbom, receipt

    def test_static_verifier_rejects_swapped_or_forged_roles(self) -> None:
        phase = {
            "started_at": "2026-08-24T06:15:00Z",
            "completed_at": "2026-08-24T06:16:00Z",
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            node, sbom, receipt = self._write_retained_fixture(directory)
            self.assertEqual(
                verify_node_advisory(
                    node=node,
                    directory=directory,
                    sbom=sbom,
                    receipt=receipt,
                    phase=phase,
                    replay=False,
                ),
                [],
            )

            affected_path = directory / NODE_ROLE_FILES["affected"]["json_report"]
            fixed_path = directory / NODE_ROLE_FILES["fixed"]["json_report"]
            fixed_path.write_bytes(affected_path.read_bytes())
            node["roles"]["fixed"]["json_report"] = _bytes_binding(  # type: ignore[index]
                fixed_path.name, fixed_path.read_bytes()
            )
            with self.assertRaises(ValueError):
                verify_node_advisory(
                    node=node,
                    directory=directory,
                    sbom=sbom,
                    receipt=receipt,
                    phase=phase,
                    replay=False,
                )

    def test_public_transport_rehydrates_only_the_exact_anchore_database(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            node, _, _ = self._write_retained_fixture(directory)
            archive = directory / "gateway-node.grype-db.tar.zst"
            archive_bytes = archive.read_bytes()
            archive.unlink()
            scan_path = directory / "gateway-image.vulnerability-scan.json"
            scan_path.write_bytes(
                canonical_json_bytes(
                    {
                        "schema": "gis-ai-go.gateway-image-vulnerability-scan.v3",
                        "node_runtime": node,
                    }
                )
            )

            def download(_status: dict[str, object], output: Path) -> None:
                output.write_bytes(archive_bytes)

            with mock.patch(
                "node_runtime_advisory.download_database_archive", side_effect=download
            ):
                self.assertEqual(
                    restore_database_from_scan(
                        scan_path=scan_path, output=directory
                    ),
                    archive,
                )
            self.assertEqual(archive.read_bytes(), archive_bytes)
            with self.assertRaisesRegex(ValueError, "overwrite"):
                restore_database_from_scan(scan_path=scan_path, output=directory)

            archive.unlink()
            forged = json.loads(scan_path.read_bytes())
            forged["node_runtime"]["database"]["source_url"] = (  # type: ignore[index]
                database_source("0" * 64).replace(
                    "grype.anchore.io", "attacker.invalid"
                )
            )
            scan_path.write_bytes(canonical_json_bytes(forged))
            with self.assertRaisesRegex(ValueError, "closed origin"):
                restore_database_from_scan(scan_path=scan_path, output=directory)

    def test_database_download_uses_only_closed_public_request_headers(self) -> None:
        payload = b"bounded-test-database"
        digest = hashlib.sha256(payload).hexdigest()
        source = database_source(digest)

        class Headers:
            @staticmethod
            def get_content_type() -> str:
                return "application/zstd"

            @staticmethod
            def get(name: str) -> str | None:
                return str(len(payload)) if name == "Content-Length" else None

        response = io.BytesIO(payload)
        response.status = 200  # type: ignore[attr-defined]
        response.headers = Headers()  # type: ignore[attr-defined]
        response.geturl = lambda: source  # type: ignore[attr-defined]
        opener = mock.Mock()
        opener.open.return_value = response
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "node_runtime_advisory.build_opener", return_value=opener
        ):
            output = Path(temporary) / "database.tar.zst"
            download_database_archive(
                {"source_url": source, "source_sha256": digest}, output
            )
            self.assertEqual(output.read_bytes(), payload)

        request = opener.open.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.full_url, source)
        self.assertEqual(
            {key.lower(): value for key, value in request.header_items()},
            {
                "accept": "application/zstd",
                "user-agent": "gis-ai-go/0.1 vulnerability-evidence",
            },
        )
        self.assertFalse(
            {"authorization", "cookie", "proxy-authorization"}
            & {key.lower() for key, _ in request.header_items()}
        )
        self.assertEqual(opener.open.call_args.kwargs, {"timeout": 60})

    def test_static_verifier_rejects_ignored_roles(self) -> None:
        phase = {
            "started_at": "2026-08-24T06:15:00Z",
            "completed_at": "2026-08-24T06:16:00Z",
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            node, sbom, receipt = self._write_retained_fixture(directory)
            actual_path = directory / NODE_ROLE_FILES["actual"]["json_report"]
            forged = json.loads(actual_path.read_bytes())
            forged["ignoredMatches"] = [{"forged": True}]
            forged_bytes = canonical_json_bytes(forged)
            actual_path.write_bytes(forged_bytes)
            node["roles"]["actual"]["json_report"] = _bytes_binding(  # type: ignore[index]
                actual_path.name, forged_bytes
            )
            with self.assertRaisesRegex(ValueError, "match inventory"):
                verify_node_advisory(
                    node=node,
                    directory=directory,
                    sbom=sbom,
                    receipt=receipt,
                    phase=phase,
                    replay=False,
                )

    def test_offline_replay_binds_full_normalised_match_semantics(self) -> None:
        phase = {
            "started_at": "2026-08-24T06:15:00Z",
            "completed_at": "2026-08-24T06:16:00Z",
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            node, sbom, receipt = self._write_retained_fixture(directory)
            replay_node = copy.deepcopy(node)
            replay_node["database"] = {  # type: ignore[index]
                key: node["database"][key]  # type: ignore[index]
                for key in (
                    "schema_version",
                    "source_url",
                    "source_sha256",
                    "built",
                    "valid",
                    "load_mode",
                    "provider",
                )
            }
            replay_node.pop("replay")

            role = "affected"
            input_path = directory / NODE_ROLE_FILES[role]["input"]
            report_path = directory / NODE_ROLE_FILES[role]["json_report"]
            cdx_path = directory / NODE_ROLE_FILES[role]["cyclonedx_report"]
            input_document = json.loads(input_path.read_bytes())
            forged = json.loads(report_path.read_bytes())
            forged["matches"][0]["matchDetails"][0]["found"][  # type: ignore[index]
                "versionConstraint"
            ] = "forged boundary"
            forged_bytes = canonical_json_bytes(forged)
            report_path.write_bytes(forged_bytes)
            projected_json = normalise_json_report(
                forged,
                input_document,
                database_source={
                    key: node["database"][key]  # type: ignore[index]
                    for key in (
                        "schema_version",
                        "source_url",
                        "source_sha256",
                        "built",
                        "valid",
                    )
                },
            )
            cdx = json.loads(cdx_path.read_bytes())
            projected_cdx = normalise_cyclonedx_report(cdx, input_document)
            node["roles"][role] = _role_evidence(  # type: ignore[index]
                role=role,
                version="24.18.0",
                input_bytes=input_path.read_bytes(),
                report_bytes=forged_bytes,
                cdx_bytes=cdx_path.read_bytes(),
                projected_json=projected_json,
                projected_cdx=projected_cdx,
            )
            self.assertNotEqual(
                node["roles"][role]["normalised_matches_sha256"],  # type: ignore[index]
                replay_node["roles"][role]["normalised_matches_sha256"],  # type: ignore[index]
            )

            inventory = node["database"]["expanded_files"]  # type: ignore[index]
            imported_status = {
                key: replay_node["database"][key]  # type: ignore[index]
                for key in (
                    "schema_version",
                    "source_url",
                    "source_sha256",
                    "built",
                    "valid",
                    "load_mode",
                )
            }
            self.assertNotIn("provider", imported_status)
            with (
                mock.patch(
                    "node_runtime_advisory.import_database",
                    return_value=imported_status,
                ),
                mock.patch(
                    "node_runtime_advisory.database_inventory",
                    return_value=inventory,
                ),
                mock.patch(
                    "node_runtime_advisory.assess_node",
                    return_value=(replay_node, {}, []),
                ),
                self.assertRaisesRegex(ValueError, "offline Grype Node replay differs"),
            ):
                verify_node_advisory(
                    node=node,
                    directory=directory,
                    sbom=sbom,
                    receipt=receipt,
                    phase=phase,
                    replay=True,
                )

    def test_static_verifier_rejects_cross_database_role(self) -> None:
        phase = {
            "started_at": "2026-08-24T06:15:00Z",
            "completed_at": "2026-08-24T06:16:00Z",
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            node, sbom, receipt = self._write_retained_fixture(directory)
            fixed_path = directory / NODE_ROLE_FILES["fixed"]["json_report"]
            altered = json.loads(fixed_path.read_bytes())
            altered["descriptor"]["db"]["status"]["built"] = (  # type: ignore[index]
                "2026-08-22T06:15:27Z"
            )
            altered_bytes = canonical_json_bytes(altered)
            fixed_path.write_bytes(altered_bytes)
            node["roles"]["fixed"]["json_report"] = _bytes_binding(  # type: ignore[index]
                fixed_path.name, altered_bytes
            )
            with self.assertRaisesRegex(ValueError, "manual Grype import differs"):
                verify_node_advisory(
                    node=node,
                    directory=directory,
                    sbom=sbom,
                    receipt=receipt,
                    phase=phase,
                    replay=False,
                )

    @mock.patch("node_runtime_advisory.subprocess.run")
    def test_grype_scan_command_is_offline_pinned_and_fail_closed(
        self, run: mock.Mock
    ) -> None:
        run.return_value = subprocess.CompletedProcess((), 0, stdout=b"{}", stderr=b"")
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary) / "cache"
            cache.mkdir()
            input_file = Path(temporary) / "input.json"
            input_file.write_text("{}", encoding="utf-8")
            self.assertEqual(
                _run_grype(
                    [f"sbom:{GRYPE_INPUT_PATH}", "--output", "json"],
                    cache=cache,
                    network=False,
                    input_file=input_file,
                ),
                b"{}",
            )
        command = run.call_args.args[0]
        self.assertIn("--network=none", command)
        self.assertIn("--pull=never", command)
        self.assertIn("--env=GRYPE_MATCH_STOCK_USING_CPES=true", command)
        self.assertIn("--env=GRYPE_ADD_CPES_IF_NONE=false", command)
        self.assertIn("--env=GRYPE_DB_AUTO_UPDATE=false", command)
        self.assertIn(GRYPE_REFERENCE, command)

        run.return_value = subprocess.CompletedProcess(
            (), 0, stdout=b"x" * 3, stderr=b""
        )
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch("node_runtime_advisory.MAX_GRYPE_REPORT_BYTES", 2),
        ):
            cache = Path(temporary) / "cache"
            cache.mkdir()
            with self.assertRaisesRegex(ValueError, "exceeds"):
                _run_grype([], cache=cache, network=False)

        private_path = ("/" + "Users/private/token").encode()
        run.side_effect = subprocess.CalledProcessError(
            1, (), output=b"Authorization: secret", stderr=private_path
        )
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary) / "cache"
            cache.mkdir()
            with self.assertRaises(ValueError) as raised:
                _run_grype([], cache=cache, network=False)
        self.assertNotIn("secret", str(raised.exception))
        self.assertNotIn(private_path.decode(), str(raised.exception))


if __name__ == "__main__":
    unittest.main()
