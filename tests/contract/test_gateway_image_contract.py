from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Callable
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gateway_image import (  # noqa: E402
    BUILDKIT_CLASSIC_AMD64_CONFIG_ID,
    BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST,
    BUILDKIT_DIGEST,
    BUILDKIT_REFERENCE,
    BUILDKIT_REPOSITORY_DIGEST,
    BUILDKIT_VERSION,
    BUILDER_NAME,
    BUILDER_SOURCE_COPY_INSTRUCTIONS,
    EXPECTED_ENVIRONMENT,
    EXPECTED_ENTRYPOINT,
    EXPECTED_HEALTH_CONFIGURATION,
    EXPECTED_REGISTRY_ID,
    FORBIDDEN_PACKAGE_LIFECYCLE_SCRIPTS,
    MAX_PRIVACY_TEXT_BYTES,
    NODE_BASE_DIGEST,
    NODE_BASE_REFERENCE,
    OCI_INDEX_MEDIA_TYPE,
    PNPM_SHA512,
    PNPM_VERSION,
    TRIVY_REFERENCE,
    SourceIdentity,
    assert_no_private_json,
    assert_no_private_text,
    build_context_inventory,
    build_context_manifest_bytes,
    build_oci_archive,
    canonical_json_bytes,
    inspect_oci_archive,
    make_image_receipt,
    parse_checksum,
    parse_gateway_containerfile_pins,
    prohibited_json_reason,
    prohibited_text_reason,
    run as run_gateway_command,
    select_build_context_paths,
    sha256_bytes,
    sha256_file,
    verify_gateway_dockerignore,
    verify_package_manifest_lifecycle_policy,
    verify_pinned_builder,
    verify_root_package_manager,
)
from scan_gateway_image import (  # noqa: E402
    MAX_TRIVY_DIAGNOSTIC_BYTES,
    TRIVY_SCAN_TIMEOUT_SECONDS,
    _acquire_trivy_image,
    _docker_scan,
    _sanitise_trivy_diagnostic,
    evaluate_policy,
    generate_scan_evidence,
    inspect_database_archive,
    package_database,
    project_findings,
    verify_phase_timing,
)
from gateway_evidence import (  # noqa: E402
    ACCEPTED_FILES,
    load_bounded_json_object,
    parse_bounded_json_object,
    write_evidence_manifest,
)
from verify_gateway_oci import verify_gateway_oci  # noqa: E402
from verify_gateway_image_evidence import (  # noqa: E402
    TEXT_EVIDENCE,
    TEXT_FILE_LIMITS,
    _verify_acceptance_bindings,
    _verify_acceptance_phase_timings,
    _verify_outer_phase_containment,
    _verify_phases,
    _verify_text_evidence_privacy,
    _verify_tool_version_bindings,
)
from check_gateway_container import (  # noqa: E402
    COMPOSE_FILE,
    assert_host_unreachable,
    assert_transport_unchanged,
    classify_transport,
    expected_rendered_compose,
    normalise_container_labels,
    normalise_resource_labels,
    validate_rendered_compose,
)


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


JsonMutation = Callable[[dict[str, Any]], None]


def synthetic_oci(
    path: Path,
    *,
    config_mutation: JsonMutation | None = None,
    manifest_mutation: JsonMutation | None = None,
    index_mutation: JsonMutation | None = None,
    extra_blob: bool = False,
    invalid_layer_tar: bool = False,
    canonical: bool = True,
) -> None:
    created = "2026-08-21T00:00:00Z"
    revision = "a" * 40
    labels = {
        "org.opencontainers.image.title": "GIS AI GO blocked gateway candidate",
        "org.opencontainers.image.description": (
            "Repository-only zero-capability gateway container"
        ),
        "org.opencontainers.image.source": "https://github.com/chris-page-gov/gis-ai-go",
        "org.opencontainers.image.licenses": "MIT",
        "org.opencontainers.image.version": "0.1.0",
        "org.opencontainers.image.revision": revision,
        "org.opencontainers.image.created": created,
        "io.gis-ai-go.registry-id": EXPECTED_REGISTRY_ID,
        "io.gis-ai-go.lifecycle": "candidate-blocked",
        "io.gis-ai-go.source-tree-clean": "true",
        "io.gis-ai-go.live-provider-calls": "false",
        "io.gis-ai-go.active-tools": "[]",
        "io.gis-ai-go.active-api-operations": "[]",
    }
    if invalid_layer_tar:
        raw_layer = b"synthetic non-tar layer"
    else:
        layer_buffer = io.BytesIO()
        with tarfile.open(
            fileobj=layer_buffer, mode="w", format=tarfile.USTAR_FORMAT
        ) as layer_archive:
            payload = b"synthetic layer\n"
            payload_member = tarfile.TarInfo("synthetic.txt")
            payload_member.mode = 0o644
            payload_member.size = len(payload)
            layer_archive.addfile(payload_member, io.BytesIO(payload))
        raw_layer = layer_buffer.getvalue()
    layer = gzip.compress(raw_layer, mtime=0)
    config_value: dict[str, Any] = {
        "architecture": "amd64",
        "os": "linux",
        "created": created,
        "config": {
            "User": "65532:65532",
            "Entrypoint": EXPECTED_ENTRYPOINT,
            "WorkingDir": "/app/apps/mcp-gateway",
            "ExposedPorts": {"8787/tcp": {}},
            "Healthcheck": {
                **EXPECTED_HEALTH_CONFIGURATION,
                "Test": list(EXPECTED_HEALTH_CONFIGURATION["Test"]),
            },
            "Env": list(EXPECTED_ENVIRONMENT),
            "Labels": labels,
            "StopSignal": "SIGTERM",
        },
        "rootfs": {"type": "layers", "diff_ids": [digest(raw_layer)]},
        "history": [],
    }
    if config_mutation is not None:
        config_mutation(config_value)
    config = compact(config_value)
    manifest_value: dict[str, Any] = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "config": {
            "mediaType": "application/vnd.oci.image.config.v1+json",
            "digest": digest(config),
            "size": len(config),
        },
        "layers": [
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                "digest": digest(layer),
                "size": len(layer),
            }
        ],
    }
    if manifest_mutation is not None:
        manifest_mutation(manifest_value)
    manifest = compact(manifest_value)
    tag = f"deploy-207-{revision[:12]}"
    index_value: dict[str, Any] = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.index.v1+json",
        "manifests": [
            {
                "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "digest": digest(manifest),
                "size": len(manifest),
                "annotations": {
                    "io.containerd.image.name": (
                        f"docker.io/library/gis-ai-go-gateway:{tag}"
                    ),
                    "org.opencontainers.image.created": created,
                    "org.opencontainers.image.ref.name": tag,
                },
                "platform": {"architecture": "amd64", "os": "linux"},
            }
        ],
    }
    if index_mutation is not None:
        index_mutation(index_value)
    index = compact(index_value)
    docker_save_manifest = canonical_json_bytes(
        [
            {
                "Config": f"blobs/sha256/{digest(config).removeprefix('sha256:')}",
                "RepoTags": [f"gis-ai-go-gateway:{tag}"],
                "Layers": [
                    f"blobs/sha256/{digest(layer).removeprefix('sha256:')}"
                ],
            }
        ]
    )
    files = {
        "oci-layout": compact({"imageLayoutVersion": "1.0.0"}),
        "index.json": index,
        "manifest.json": docker_save_manifest,
        f"blobs/sha256/{digest(config).removeprefix('sha256:')}": config,
        f"blobs/sha256/{digest(layer).removeprefix('sha256:')}": layer,
        f"blobs/sha256/{digest(manifest).removeprefix('sha256:')}": manifest,
    }
    if extra_blob:
        files[f"blobs/sha256/{'f' * 64}"] = b"unreachable"
    with tarfile.open(path, "w", format=tarfile.USTAR_FORMAT) as archive:
        ordered: list[tuple[str, bytes | None]] = [
            ("blobs", None),
            ("index.json", files.pop("index.json")),
            ("manifest.json", files.pop("manifest.json")),
            ("oci-layout", files.pop("oci-layout")),
            ("blobs/sha256", None),
            *[(name, value) for name, value in sorted(files.items())],
        ]
        for name, value in ordered:
            member = tarfile.TarInfo(name)
            member.uid = 65532 if canonical else 0
            member.gid = 65532 if canonical else 0
            member.mtime = 0
            if value is None:
                member.type = tarfile.DIRTYPE
                member.mode = 0o755
                archive.addfile(member)
            else:
                member.type = tarfile.REGTYPE
                member.mode = 0o644
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value))


class GatewayImageContractTests(unittest.TestCase):
    @staticmethod
    def _builder_details() -> str:
        return "\n".join(
            (
                f"Name:          {BUILDER_NAME}",
                "Driver:        docker-container",
                "Nodes:",
                f"Name:                  {BUILDER_NAME}0",
                f'Driver Options:        image="{BUILDKIT_REFERENCE}"',
                "Status:                running",
                f"BuildKit version:      {BUILDKIT_VERSION}",
            )
        )

    @staticmethod
    def _builder_container(
        image_id: str, *, reference: str = BUILDKIT_REFERENCE
    ) -> dict[str, Any]:
        return {"Config": {"Image": reference}, "Image": image_id}

    @staticmethod
    def _builder_image(
        image_id: str,
        *,
        descriptor: Any = None,
        include_descriptor: bool = False,
        repo_digests: Any = ...,
    ) -> dict[str, Any]:
        image: dict[str, Any] = {
            "Architecture": "amd64",
            "Id": image_id,
            "Os": "linux",
            "RepoDigests": (
                [BUILDKIT_REPOSITORY_DIGEST]
                if repo_digests is ...
                else repo_digests
            ),
        }
        if include_descriptor:
            image["Descriptor"] = descriptor
        return image

    def _verify_builder_projection(
        self,
        *,
        container: dict[str, Any],
        image: dict[str, Any],
    ) -> None:
        outputs = (
            mock.Mock(stdout=self._builder_details()),
            mock.Mock(stdout=json.dumps([container])),
            mock.Mock(stdout=json.dumps([image])),
        )
        with mock.patch("gateway_image.run", side_effect=outputs) as run_mock:
            verify_pinned_builder()
        self.assertEqual(
            run_mock.call_args_list,
            [
                mock.call(
                    ("docker", "buildx", "inspect", BUILDER_NAME), capture=True
                ),
                mock.call(
                    ("docker", "inspect", f"buildx_buildkit_{BUILDER_NAME}0"),
                    capture=True,
                ),
                mock.call(
                    ("docker", "image", "inspect", BUILDKIT_REFERENCE),
                    capture=True,
                ),
            ],
        )

    def test_pinned_builder_accepts_containerd_image_identity(self) -> None:
        self._verify_builder_projection(
            container=self._builder_container(BUILDKIT_DIGEST),
            image=self._builder_image(
                BUILDKIT_DIGEST,
                include_descriptor=True,
                descriptor={
                    "mediaType": OCI_INDEX_MEDIA_TYPE,
                    "digest": BUILDKIT_DIGEST,
                    "size": 5296,
                },
            ),
        )

    def test_gateway_build_discards_buildkit_output_without_buffering(self) -> None:
        source = SourceIdentity(
            revision="a" * 40,
            version="0.1.0",
            source_date_epoch=1_787_270_400,
            created="2026-08-21T00:00:00Z",
            clean=True,
        )
        inspection = mock.Mock(platform="linux/amd64")
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch("gateway_image.verify_checked_inputs"),
            mock.patch("gateway_image.verify_pinned_builder"),
            mock.patch("gateway_image.build_context_inventory", return_value=()),
            mock.patch("gateway_image.materialise_build_context"),
            mock.patch("gateway_image.run") as run_mock,
            mock.patch("gateway_image.canonicalise_oci_archive"),
            mock.patch(
                "gateway_image.inspect_oci_archive", return_value=inspection
            ),
        ):
            result = build_oci_archive(
                Path(temporary) / "gateway-image.oci.tar",
                source=source,
                platform="linux/amd64",
                tag="gis-ai-go-gateway:fixture",
            )

        self.assertIs(result, inspection)
        self.assertTrue(run_mock.call_args.kwargs["discard_output"])
        self.assertNotIn("capture", run_mock.call_args.kwargs)
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 30 * 60)

    def test_discarded_command_output_is_not_buffered_or_reflected(self) -> None:
        command = (
            "import os;"
            "os.write(1,b'x'*(2*1024*1024));"
            "os.write(2,b'y'*(2*1024*1024))"
        )
        completed = run_gateway_command(
            (sys.executable, "-c", command),
            discard_output=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIsNone(completed.stdout)
        self.assertIsNone(completed.stderr)

        with self.assertRaises(subprocess.CalledProcessError) as raised:
            run_gateway_command(
                (sys.executable, "-c", "raise SystemExit(17)"),
                discard_output=True,
                timeout=10,
            )
        self.assertEqual(raised.exception.returncode, 17)
        self.assertIsNone(raised.exception.stdout)
        self.assertIsNone(raised.exception.stderr)

    def test_pinned_builder_accepts_classic_docker_config_identity(self) -> None:
        self.assertEqual(
            BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST,
            "moby/buildkit@"
            "sha256:040d34121c27906c4ff9ac152a30d52bf2c5d328d3bb748916bb3d2743c02528",
        )
        self.assertEqual(
            BUILDKIT_CLASSIC_AMD64_CONFIG_ID,
            "sha256:260cc297a47c57183fe53fb963885068c30e976060fabc90e32af04919dbd0bf",
        )
        for repo_digests in (
            [BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST],
            [BUILDKIT_REPOSITORY_DIGEST],
            [
                BUILDKIT_REPOSITORY_DIGEST,
                BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST,
            ],
        ):
            with self.subTest(repo_digests=repo_digests):
                self._verify_builder_projection(
                    container=self._builder_container(
                        BUILDKIT_CLASSIC_AMD64_CONFIG_ID
                    ),
                    image=self._builder_image(
                        BUILDKIT_CLASSIC_AMD64_CONFIG_ID,
                        repo_digests=repo_digests,
                    ),
                )

    def test_pinned_builder_rejects_reference_and_image_id_mismatches(self) -> None:
        valid_image = self._builder_image(
            BUILDKIT_DIGEST,
            include_descriptor=True,
            descriptor={
                "mediaType": OCI_INDEX_MEDIA_TYPE,
                "digest": BUILDKIT_DIGEST,
                "size": 5296,
            },
        )
        cases = {
            "wrong-container-reference": self._builder_container(
                BUILDKIT_DIGEST,
                reference="moby/buildkit:buildx-stable-1@sha256:" + "0" * 64,
            ),
            "container-image-id-mismatch": self._builder_container(
                "sha256:" + "c" * 64
            ),
            "malformed-container-and-image-id": self._builder_container(
                "sha256:short"
            ),
            "classic-unpinned-config-id": self._builder_container(
                "sha256:" + "c" * 64
            ),
        }
        for name, container in cases.items():
            if name == "malformed-container-and-image-id":
                image = self._builder_image("sha256:short")
            elif name == "classic-unpinned-config-id":
                image = self._builder_image(
                    "sha256:" + "c" * 64,
                    repo_digests=[BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST],
                )
            else:
                image = valid_image
            with self.subTest(name=name), self.assertRaises(ValueError):
                self._verify_builder_projection(container=container, image=image)

    def test_pinned_builder_rejects_containerd_descriptor_mutations(self) -> None:
        valid_descriptor = {
            "mediaType": OCI_INDEX_MEDIA_TYPE,
            "digest": BUILDKIT_DIGEST,
            "size": 5296,
        }
        cases: dict[str, tuple[str, Any]] = {
            "null-descriptor": (BUILDKIT_DIGEST, None),
            "non-object-descriptor": (BUILDKIT_DIGEST, "invalid"),
            "missing-media-type": (
                BUILDKIT_DIGEST,
                {"digest": BUILDKIT_DIGEST, "size": 5296},
            ),
            "wrong-media-type": (
                BUILDKIT_DIGEST,
                {**valid_descriptor, "mediaType": "application/json"},
            ),
            "wrong-digest": (
                BUILDKIT_DIGEST,
                {**valid_descriptor, "digest": "sha256:" + "0" * 64},
            ),
            "invalid-size": (BUILDKIT_DIGEST, {**valid_descriptor, "size": 0}),
            "oversized-descriptor": (
                BUILDKIT_DIGEST,
                {**valid_descriptor, "size": 4 * 1024 * 1024 + 1},
            ),
            "descriptor-with-classic-config-id": (
                "sha256:" + "c" * 64,
                valid_descriptor,
            ),
        }
        for name, (image_id, descriptor) in cases.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                self._verify_builder_projection(
                    container=self._builder_container(image_id),
                    image=self._builder_image(
                        image_id,
                        include_descriptor=True,
                        descriptor=descriptor,
                    ),
                )

    def test_pinned_builder_rejects_repository_digest_mutations(self) -> None:
        expected = BUILDKIT_REPOSITORY_DIGEST
        cases: dict[str, Any] = {
            "null": None,
            "string-not-list": expected,
            "empty": [],
            "malformed": ["moby/buildkit@sha256:short"],
            "foreign-repository": [f"foreign/buildkit@{BUILDKIT_DIGEST}"],
            "mismatched-digest": ["moby/buildkit@sha256:" + "0" * 64],
            "expected-plus-foreign": [
                expected,
                f"foreign/buildkit@{BUILDKIT_DIGEST}",
            ],
        }
        descriptor = {
            "mediaType": OCI_INDEX_MEDIA_TYPE,
            "digest": BUILDKIT_DIGEST,
            "size": 5296,
        }
        missing = self._builder_image(
            BUILDKIT_DIGEST,
            include_descriptor=True,
            descriptor=descriptor,
        )
        missing.pop("RepoDigests")
        with self.subTest(name="missing"), self.assertRaises(ValueError):
            self._verify_builder_projection(
                container=self._builder_container(BUILDKIT_DIGEST), image=missing
            )
        for name, repo_digests in cases.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                self._verify_builder_projection(
                    container=self._builder_container(BUILDKIT_DIGEST),
                    image=self._builder_image(
                        BUILDKIT_DIGEST,
                        include_descriptor=True,
                        descriptor=descriptor,
                        repo_digests=repo_digests,
                    ),
                )

        with self.subTest(name="classic-unpinned-child"), self.assertRaises(
            ValueError
        ):
            self._verify_builder_projection(
                container=self._builder_container(
                    BUILDKIT_CLASSIC_AMD64_CONFIG_ID
                ),
                image=self._builder_image(
                    BUILDKIT_CLASSIC_AMD64_CONFIG_ID,
                    repo_digests=["moby/buildkit@sha256:" + "0" * 64],
                ),
            )

    def test_pinned_builder_rejects_malformed_inspection_envelopes(self) -> None:
        valid_container = self._builder_container(BUILDKIT_DIGEST)
        valid_image = self._builder_image(
            BUILDKIT_DIGEST,
            include_descriptor=True,
            descriptor={
                "mediaType": OCI_INDEX_MEDIA_TYPE,
                "digest": BUILDKIT_DIGEST,
                "size": 5296,
            },
        )
        cases: dict[str, tuple[Any, Any]] = {
            "container-not-list": ({}, [valid_image]),
            "container-empty": ([], [valid_image]),
            "container-many": ([valid_container, valid_container], [valid_image]),
            "container-record-not-object": (["invalid"], [valid_image]),
            "image-not-list": ([valid_container], {}),
            "image-empty": ([valid_container], []),
            "image-many": ([valid_container], [valid_image, valid_image]),
            "image-record-not-object": ([valid_container], ["invalid"]),
        }
        for name, (container, image) in cases.items():
            outputs = (
                mock.Mock(stdout=self._builder_details()),
                mock.Mock(stdout=json.dumps(container)),
                mock.Mock(stdout=json.dumps(image)),
            )
            with (
                self.subTest(name=name),
                mock.patch("gateway_image.run", side_effect=outputs),
                self.assertRaises(ValueError),
            ):
                verify_pinned_builder()

    def test_receipt_schema_accepts_only_the_blocked_candidate(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "gateway-image-receipt.schema.json").read_bytes()
        )
        Draft202012Validator.check_schema(schema)
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "gateway-image.oci.tar"
            synthetic_oci(archive)
            inspection = inspect_oci_archive(archive)
        source = SourceIdentity(
            revision="a" * 40,
            version="0.1.0",
            source_date_epoch=1_777_000_000,
            created="2026-08-21T00:00:00Z",
            clean=True,
        )
        receipt = make_image_receipt(
            source=source,
            inspection=inspection,
            context_manifest_sha256="b" * 64,
            context_file_count=1,
            context_bytes=1,
            archive_name="gateway-image.oci.tar",
            realised_buildx_version="v0.35.0",
        )
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        validator.validate(receipt)
        weakened = json.loads(canonical_json_bytes(receipt))
        weakened["runtime_boundary"]["active_tools"] = ["catalogue.search"]
        self.assertTrue(list(validator.iter_errors(weakened)))
        dirty = json.loads(canonical_json_bytes(receipt))
        dirty["source"]["clean"] = False
        self.assertTrue(list(validator.iter_errors(dirty)))

    def test_inspector_rejects_tampered_oci_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "gateway-image.oci.tar"
            synthetic_oci(archive)
            inspection = inspect_oci_archive(archive)
            self.assertEqual(inspection.platform, "linux/amd64")
            self.assertEqual(inspection.labels["io.gis-ai-go.active-tools"], "[]")
            data = bytearray(archive.read_bytes())
            with tarfile.open(archive, "r") as opened:
                index_member = opened.getmember("index.json")
                data[index_member.offset_data] ^= 1
            archive.write_bytes(data)
            with self.assertRaises((tarfile.TarError, ValueError)):
                inspect_oci_archive(archive)

    def test_container_and_compose_have_no_activation_or_provider_input(self) -> None:
        containerfile = (ROOT / "apps" / "mcp-gateway" / "Containerfile").read_text()
        compose = (ROOT / "deploy" / "gateway" / "compose.candidate.yaml").read_text()
        self.assertIn(NODE_BASE_DIGEST, containerfile)
        self.assertIn('USER 65532:65532', containerfile)
        self.assertIn('ENTRYPOINT ["node", "dist/src/container-main.js"]', containerfile)
        self.assertNotRegex(containerfile, r"(?:ONS|API_KEY|ACTIVE_TOOLS|ACTIVE_OPERATIONS)")
        self.assertNotIn("COPY packages/tool-registry/ packages/tool-registry/", containerfile)
        self.assertIn("node_modules/.modules.yaml", containerfile)
        self.assertIn("-path '*/dist/test'", containerfile)
        self.assertIn("/usr/local/lib/node_modules/npm", containerfile)
        self.assertEqual(BUILDER_NAME, "gis-ai-go-gateway")
        self.assertIn("pull_policy: never", compose)
        self.assertIn("host_ip: 127.0.0.1", compose)
        self.assertIn("internal: true", compose)
        self.assertNotIn("environment:", compose)
        self.assertNotIn("build:", compose)

    def test_structural_pin_parser_rejects_coordinated_stale_comments(self) -> None:
        containerfile = (ROOT / "apps" / "mcp-gateway" / "Containerfile").read_text()
        parsed = parse_gateway_containerfile_pins(containerfile)
        self.assertEqual(parsed["node_reference"], NODE_BASE_REFERENCE)
        mutations = [
            containerfile.replace(
                f'ARG NODE_BASE="{NODE_BASE_REFERENCE}"',
                f'# {NODE_BASE_REFERENCE}\nARG NODE_BASE="node:24.19.0-bookworm-slim@sha256:{"0" * 64}"',
            ),
            containerfile.replace(
                f"npm pack pnpm@{PNPM_VERSION}",
                f"# pnpm@{PNPM_VERSION}\nRUN npm pack pnpm@9.0.0",
            ),
            containerfile.replace(PNPM_SHA512, "0" * 128) + f"\n# {PNPM_SHA512}\n",
            containerfile.replace(
                "COPY apps/mcp-gateway/ apps/mcp-gateway/",
                "COPY apps/mcp-gateway/ apps/mcp-gateway/\n"
                "RUN curl https://example.invalid",
            ),
            containerfile.replace(
                "COPY apps/mcp-gateway/ apps/mcp-gateway/",
                "COPY apps/mcp-gateway/ apps/mcp-gateway/\n"
                "ADD https://example.invalid/x /tmp/x",
            ),
            containerfile.replace(
                "RUN pnpm --filter @gis-ai-go/mcp-gateway deploy --prod --legacy "
                "--ignore-scripts \\\n"
                "      /runtime/apps/mcp-gateway",
                "RUN true",
            ),
        ]
        for mutation in mutations:
            with self.subTest():
                with self.assertRaises(ValueError):
                    parse_gateway_containerfile_pins(mutation)
        verify_root_package_manager({"packageManager": f"pnpm@{PNPM_VERSION}"})
        with self.assertRaises(ValueError):
            verify_root_package_manager({"packageManager": "pnpm@9.0.0"})

    def test_parser_closes_deploy_scripts_source_copy_order_and_networking(self) -> None:
        containerfile = (ROOT / "apps" / "mcp-gateway" / "Containerfile").read_text()
        deploy_block = (
            "RUN pnpm --filter @gis-ai-go/mcp-gateway deploy --prod --legacy "
            "--ignore-scripts \\\n"
            "      /runtime/apps/mcp-gateway"
        )
        mutations = {
            "deploy-scripts-enabled": containerfile.replace(
                "deploy --prod --legacy --ignore-scripts",
                "deploy --prod --legacy",
                1,
            ),
            "network-before-first-source-copy": containerfile.replace(
                BUILDER_SOURCE_COPY_INSTRUCTIONS[0],
                "RUN curl https://example.invalid/source\n"
                + BUILDER_SOURCE_COPY_INSTRUCTIONS[0],
                1,
            ),
            "duplicate-source-copy": containerfile.replace(
                BUILDER_SOURCE_COPY_INSTRUCTIONS[-1],
                BUILDER_SOURCE_COPY_INSTRUCTIONS[-1]
                + "\n"
                + BUILDER_SOURCE_COPY_INSTRUCTIONS[-1],
                1,
            ),
        }
        for source_copy in BUILDER_SOURCE_COPY_INSTRUCTIONS:
            moved = containerfile.replace(source_copy + "\n", "", 1)
            mutations[f"source-before-deploy:{source_copy}"] = moved.replace(
                deploy_block,
                source_copy + "\n" + deploy_block,
                1,
            )
        for name, mutation in mutations.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                parse_gateway_containerfile_pins(mutation)

    def test_admitted_manifests_reject_lifecycle_hooks_but_allow_ordinary_scripts(self) -> None:
        ordinary = {
            "scripts": {
                "build": "tsc --project tsconfig.json",
                "prepare:test": "pnpm run build",
                "test": "node --test",
            },
            "pnpm": {"onlyBuiltDependencies": ["@scoped/reviewed-dependency"]},
        }
        verify_package_manifest_lifecycle_policy(
            ordinary,
            logical_path="packages/contracts/package.json",
        )
        for hook in sorted(FORBIDDEN_PACKAGE_LIFECYCLE_SCRIPTS):
            package = json.loads(canonical_json_bytes(ordinary))
            package["scripts"][hook] = "node hostile-hook.js"
            with self.subTest(hook=hook), self.assertRaises(ValueError):
                verify_package_manifest_lifecycle_policy(
                    package,
                    logical_path="packages/contracts/package.json",
                )

    def test_dockerignore_closes_environment_file_negations(self) -> None:
        dockerignore = (
            ROOT / "apps" / "mcp-gateway" / "Containerfile.dockerignore"
        ).read_text()
        verify_gateway_dockerignore(dockerignore)
        with self.assertRaises(ValueError):
            verify_gateway_dockerignore(dockerignore.replace("**/.env.*\n", ""))
        with self.assertRaises(ValueError):
            verify_gateway_dockerignore(dockerignore + "!apps/mcp-gateway/.env\n")

    def test_ignored_environment_files_are_not_admitted_as_source_inputs(self) -> None:
        tracked = {"package.json", "apps/mcp-gateway/src/container-main.ts"}
        generated = {"artifacts/okf/build-receipt.json"}
        ignored_present = {
            "apps/mcp-gateway/.env",
            "packages/contracts/.env.local",
        }
        selected = select_build_context_paths(tracked, generated)
        self.assertTrue(ignored_present.isdisjoint(selected))
        for ignored in ignored_present:
            with self.subTest(ignored=ignored):
                with self.assertRaises(ValueError):
                    select_build_context_paths(tracked | {ignored}, generated)

    def test_oci_inspector_rejects_closed_contract_mutation_families(self) -> None:
        cases: list[tuple[str, dict[str, Any]]] = [
            (
                "config-media-type",
                {"manifest_mutation": lambda value: value["config"].update({"mediaType": "x"})},
            ),
            (
                "descriptor-size",
                {"manifest_mutation": lambda value: value["config"].update({"size": 1})},
            ),
            (
                "platform",
                {
                    "index_mutation": lambda value: value["manifests"][0]["platform"].update(
                        {"architecture": "arm64"}
                    )
                },
            ),
            ("extra-blob", {"extra_blob": True}),
            ("non-tar-layer", {"invalid_layer_tar": True}),
            (
                "diff-id-count",
                {"config_mutation": lambda value: value["rootfs"].update({"diff_ids": []})},
            ),
            (
                "diff-id-digest",
                {
                    "config_mutation": lambda value: value["rootfs"].update(
                        {"diff_ids": ["sha256:" + "b" * 64]}
                    )
                },
            ),
            (
                "extra-environment",
                {
                    "config_mutation": lambda value: value["config"]["Env"].append(
                        "NODE_OPTIONS=--require=/tmp/x"
                    )
                },
            ),
            (
                "extra-label",
                {
                    "config_mutation": lambda value: value["config"]["Labels"].update(
                        {"unexpected": "true"}
                    )
                },
            ),
            (
                "stop-signal",
                {
                    "config_mutation": lambda value: value["config"].update(
                        {"StopSignal": "SIGKILL"}
                    )
                },
            ),
            (
                "health-timing",
                {
                    "config_mutation": lambda value: value["config"]["Healthcheck"].update(
                        {"Timeout": 1}
                    )
                },
            ),
            ("noncanonical-tar", {"canonical": False}),
        ]
        for name, options in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                archive = Path(temporary) / "gateway-image.oci.tar"
                synthetic_oci(archive, **options)
                with self.assertRaises(ValueError):
                    inspect_oci_archive(archive)

    def test_oci_inspector_bounds_expanded_layer_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "gateway-image.oci.tar"
            synthetic_oci(archive)
            with mock.patch("gateway_image.MAX_LAYER_EXPANDED_BYTES", 1):
                with self.assertRaises(ValueError):
                    inspect_oci_archive(archive)

    def test_receipt_verifier_rejects_source_and_context_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "gateway-image.oci.tar"
            synthetic_oci(archive)
            inspection = inspect_oci_archive(archive)
            source = SourceIdentity(
                revision="a" * 40,
                version="0.1.0",
                source_date_epoch=1_787_270_400,
                created="2026-08-21T00:00:00Z",
                clean=True,
            )
            inventory = [("synthetic", "c" * 64, 9)]
            context_bytes = build_context_manifest_bytes(inventory)
            context = root / "build-context.sha256"
            context.write_bytes(context_bytes)
            checksum = root / "gateway-image.oci.tar.sha256"
            checksum.write_text(f"{sha256_file(archive)}  {archive.name}\n")
            receipt = make_image_receipt(
                source=source,
                inspection=inspection,
                context_manifest_sha256=sha256_bytes(context_bytes),
                context_file_count=1,
                context_bytes=9,
                archive_name=archive.name,
                realised_buildx_version="v0.35.0",
            )
            receipt_path = root / "image-receipt.json"
            with mock.patch("verify_gateway_oci.source_identity", return_value=source), mock.patch(
                "verify_gateway_oci.build_context_inventory", return_value=inventory
            ):
                receipt_path.write_bytes(canonical_json_bytes(receipt))
                verify_gateway_oci(
                    archive=archive,
                    checksum=checksum,
                    receipt_path=receipt_path,
                    context_path=context,
                    require_clean=True,
                )
                mutations = [
                    lambda value: value["source"].update({"version": "9.9.9"}),
                    lambda value: value["source"].update({"created": "2026-08-22T00:00:00Z"}),
                    lambda value: value["source"].update({"source_date_epoch": 1}),
                    lambda value: value["source"].update({"clean": False}),
                    lambda value: value["build"]["context"].update({"bytes": 10}),
                    lambda value: value.update(
                        {"classification": "non-publishable-development-build"}
                    ),
                ]
                for mutation in mutations:
                    altered = json.loads(canonical_json_bytes(receipt))
                    mutation(altered)
                    receipt_path.write_bytes(canonical_json_bytes(altered))
                    with self.assertRaises((ValueError, ValidationError)):
                        verify_gateway_oci(
                            archive=archive,
                            checksum=checksum,
                            receipt_path=receipt_path,
                            context_path=context,
                        )

    def test_direct_verifier_bounds_receipt_context_and_checksum_before_oci(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "gateway-image.oci.tar"
            checksum = root / "gateway-image.oci.tar.sha256"
            checksum.write_text(f"{'0' * 64}  {archive.name}\n")
            context = root / "build-context.sha256"
            context.write_bytes(b"context\n")
            receipt_path = root / "image-receipt.json"

            malformed_receipts = (
                b'{"schema":"x","schema":"y"}\n',
                b"[]\n",
                b'{"value":NaN}\n',
            )
            for raw in malformed_receipts:
                receipt_path.write_bytes(raw)
                with mock.patch(
                    "verify_gateway_oci.inspect_oci_archive"
                ) as inspect, self.assertRaises(ValueError):
                    verify_gateway_oci(
                        archive=archive,
                        checksum=checksum,
                        receipt_path=receipt_path,
                        context_path=context,
                    )
                inspect.assert_not_called()

            receipt_target = root / "receipt-target.json"
            receipt_target.write_bytes(b"{}\n")
            receipt_link = root / "receipt-link.json"
            receipt_link.symlink_to(receipt_target)
            receipt_fifo = root / "receipt-fifo.json"
            os.mkfifo(receipt_fifo)
            receipt_oversized = root / "receipt-oversized.json"
            receipt_oversized.write_bytes(b'{"value":1}\n')
            for name, path, bound in (
                ("symlink", receipt_link, None),
                ("fifo", receipt_fifo, None),
                ("oversized", receipt_oversized, 4),
            ):
                patcher = (
                    mock.patch(
                        "verify_gateway_oci.MAX_RECEIPT_JSON_BYTES",
                        bound,
                    )
                    if bound is not None
                    else mock.patch(
                        "verify_gateway_oci.MAX_RECEIPT_JSON_BYTES",
                        8 * 1024 * 1024,
                    )
                )
                with self.subTest(name=name), patcher, mock.patch(
                    "verify_gateway_oci.inspect_oci_archive"
                ) as inspect, self.assertRaises(ValueError):
                    verify_gateway_oci(
                        archive=archive,
                        checksum=checksum,
                        receipt_path=path,
                        context_path=context,
                    )
                inspect.assert_not_called()

            synthetic_oci(archive)
            inspection = inspect_oci_archive(archive)
            source = SourceIdentity(
                revision="a" * 40,
                version="0.1.0",
                source_date_epoch=1_787_270_400,
                created="2026-08-21T00:00:00Z",
                clean=True,
            )
            valid_receipt = make_image_receipt(
                source=source,
                inspection=inspection,
                context_manifest_sha256="b" * 64,
                context_file_count=1,
                context_bytes=1,
                archive_name=archive.name,
                realised_buildx_version="v0.35.0",
            )
            receipt_path.write_bytes(canonical_json_bytes(valid_receipt))
            schema_path = root / "receipt-schema.json"
            for raw in malformed_receipts:
                schema_path.write_bytes(raw)
                with self.subTest(schema=raw), mock.patch(
                    "verify_gateway_oci.RECEIPT_SCHEMA",
                    schema_path,
                ), mock.patch(
                    "verify_gateway_oci.inspect_oci_archive"
                ) as inspect, self.assertRaises(ValueError):
                    verify_gateway_oci(
                        archive=archive,
                        checksum=checksum,
                        receipt_path=receipt_path,
                        context_path=context,
                    )
                inspect.assert_not_called()
            schema_target = root / "schema-target.json"
            schema_target.write_bytes(b"{}\n")
            schema_link = root / "schema-link.json"
            schema_link.symlink_to(schema_target)
            schema_fifo = root / "schema-fifo.json"
            os.mkfifo(schema_fifo)
            schema_oversized = root / "schema-oversized.json"
            schema_oversized.write_bytes(b'{"type":"object"}\n')
            for name, path, bound in (
                ("symlink", schema_link, None),
                ("fifo", schema_fifo, None),
                ("oversized", schema_oversized, 4),
            ):
                bound_patcher = (
                    mock.patch("verify_gateway_oci.MAX_SCHEMA_JSON_BYTES", bound)
                    if bound is not None
                    else mock.patch(
                        "verify_gateway_oci.MAX_SCHEMA_JSON_BYTES",
                        2 * 1024 * 1024,
                    )
                )
                with self.subTest(name=f"schema-{name}"), bound_patcher, mock.patch(
                    "verify_gateway_oci.RECEIPT_SCHEMA",
                    path,
                ), mock.patch(
                    "verify_gateway_oci.inspect_oci_archive"
                ) as inspect, self.assertRaises(ValueError):
                    verify_gateway_oci(
                        archive=archive,
                        checksum=checksum,
                        receipt_path=receipt_path,
                        context_path=context,
                    )
                inspect.assert_not_called()

            context_target = root / "context-target.sha256"
            context_target.write_bytes(b"context\n")
            context_link = root / "context-link.sha256"
            context_link.symlink_to(context_target)
            context_fifo = root / "context-fifo.sha256"
            os.mkfifo(context_fifo)
            context_oversized = root / "context-oversized.sha256"
            context_oversized.write_bytes(b"context\n")
            for name, path, bound in (
                ("symlink", context_link, None),
                ("fifo", context_fifo, None),
                ("oversized", context_oversized, 4),
            ):
                patcher = (
                    mock.patch(
                        "verify_gateway_oci.MAX_CONTEXT_MANIFEST_BYTES",
                        bound,
                    )
                    if bound is not None
                    else mock.patch(
                        "verify_gateway_oci.MAX_CONTEXT_MANIFEST_BYTES",
                        2 * 1024 * 1024,
                    )
                )
                with self.subTest(name=f"context-{name}"), patcher, mock.patch(
                    "verify_gateway_oci.inspect_oci_archive"
                ) as inspect, self.assertRaises(ValueError):
                    verify_gateway_oci(
                        archive=archive,
                        checksum=checksum,
                        receipt_path=receipt_path,
                        context_path=path,
                    )
                inspect.assert_not_called()

            checksum_target = root / "checksum-target.sha256"
            checksum_target.write_text(f"{'0' * 64}  {archive.name}\n")
            self.assertEqual(parse_checksum(checksum_target, archive.name), "0" * 64)
            checksum_link = root / "checksum-link.sha256"
            checksum_link.symlink_to(checksum_target)
            checksum_fifo = root / "checksum-fifo.sha256"
            os.mkfifo(checksum_fifo)
            checksum_oversized = root / "checksum-oversized.sha256"
            checksum_oversized.write_bytes(b"x" * 4_097)
            for name, path in (
                ("symlink", checksum_link),
                ("fifo", checksum_fifo),
                ("oversized", checksum_oversized),
            ):
                with self.subTest(name=f"checksum-{name}"), self.assertRaises(
                    ValueError
                ):
                    parse_checksum(path, archive.name)

    def test_scan_policy_retains_unfixed_and_blocks_fixable_findings(self) -> None:
        report = {
            "Trivy": {"Version": "0.74.0"},
            "Results": [
                {
                    "Target": "fixture",
                    "Vulnerabilities": [
                        {
                            "VulnerabilityID": "CVE-UNFIXED",
                            "PkgName": "alpha",
                            "InstalledVersion": "1",
                            "FixedVersion": "",
                            "Severity": "HIGH",
                        },
                        {
                            "VulnerabilityID": "CVE-FIXABLE",
                            "PkgName": "beta",
                            "InstalledVersion": "1",
                            "FixedVersion": "2",
                            "Severity": "CRITICAL",
                        },
                    ],
                }
            ]
        }
        findings = project_findings(report)
        self.assertEqual(len(findings), 2)
        unfixed = next(item for item in findings if item["id"] == "CVE-UNFIXED")
        self.assertIsNone(unfixed["fixed_version"])
        fixable, passed = evaluate_policy(findings)
        self.assertEqual([item["id"] for item in fixable], ["CVE-FIXABLE"])
        self.assertFalse(passed)
        self.assertEqual(evaluate_policy([unfixed]), ([], True))

        malformed = json.loads(canonical_json_bytes(report))
        malformed["Results"][0]["Vulnerabilities"][0]["VulnerabilityID"] = None
        with self.assertRaises(ValueError):
            project_findings(malformed)
        numeric_fix = json.loads(canonical_json_bytes(report))
        numeric_fix["Results"][0]["Vulnerabilities"][0]["FixedVersion"] = 2
        with self.assertRaises(ValueError):
            project_findings(numeric_fix)
        wrong_scanner = json.loads(canonical_json_bytes(report))
        wrong_scanner["Trivy"]["Version"] = "9.9.9"
        with self.assertRaises(ValueError):
            project_findings(wrong_scanner)

    def test_retained_database_archive_rejects_absence_and_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            (cache / "db").mkdir(parents=True)
            (cache / "db" / "metadata.json").write_text("{}\n")
            (cache / "db" / "trivy.db").write_bytes(b"database")
            archive = root / "gateway-image.trivy-db.tar.gz"
            expected = package_database(cache, archive)
            self.assertEqual(inspect_database_archive(archive), expected)
            canonical = archive.read_bytes()
            raw_tar = gzip.decompress(canonical)

            def gzip_database(payload: bytes, *, mtime: int = 0) -> bytes:
                encoded = io.BytesIO()
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    fileobj=encoded,
                    compresslevel=6,
                    mtime=mtime,
                ) as compressed:
                    compressed.write(payload)
                return encoded.getvalue()

            alternate_header = bytearray(canonical)
            alternate_header[9] = 3 if alternate_header[9] != 3 else 0
            mutations = {
                "gzip-mtime": gzip_database(raw_tar, mtime=1),
                "gzip-header": bytes(alternate_header),
                "concatenated-stream": canonical + gzip_database(b"extra"),
                "trailing-bytes": canonical + b"trailing",
                "extra-tar-padding": gzip_database(raw_tar + b"\0" * 512),
            }
            for name, mutation in mutations.items():
                archive.write_bytes(mutation)
                with self.subTest(name=name), self.assertRaises(
                    (ValueError, tarfile.TarError, OSError)
                ):
                    inspect_database_archive(archive)
            archive.write_bytes(canonical)
            with self.assertRaises(FileNotFoundError):
                inspect_database_archive(root / "missing.tar.gz")
            data = bytearray(archive.read_bytes())
            data[len(data) // 2] ^= 1
            archive.write_bytes(data)
            with self.assertRaises((ValueError, tarfile.TarError, OSError)):
                inspect_database_archive(archive)

    def test_trivy_scan_success_preserves_exact_online_and_offline_commands(self) -> None:
        report = {"Trivy": {"Version": "0.74.0"}, "Results": []}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir()
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            completed = subprocess.CompletedProcess(
                args=(),
                returncode=0,
                stdout=canonical_json_bytes(report),
                stderr=b"Bearer " + b"success-stderr-must-remain-ignored",
            )
            with mock.patch(
                "scan_gateway_image.subprocess.run",
                return_value=completed,
            ) as run:
                _acquire_trivy_image()
                pull_command = run.call_args.args[0]
                self.assertEqual(pull_command, ("docker", "pull", TRIVY_REFERENCE))
                self.assertEqual(
                    _docker_scan(cache=cache, sbom=sbom, offline=True, pull="never"),
                    report,
                )
                self.assertEqual(
                    _docker_scan(cache=cache, sbom=sbom, offline=False, pull="never"),
                    report,
                )
                common = (
                    "docker",
                    "run",
                    "--rm",
                    "--pull=never",
                    "--read-only",
                    "--cap-drop=ALL",
                    "--security-opt=no-new-privileges",
                    f"--user={os.getuid()}:{os.getgid()}",
                    (
                        "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m,mode=0700,"
                        f"uid={os.getuid()},gid={os.getgid()}"
                    ),
                    f"--volume={sbom}:/input/gateway-image.sbom.cdx.json:ro",
                    f"--volume={cache}:/cache",
                )
                scanner = (
                    TRIVY_REFERENCE,
                    "sbom",
                    "--cache-dir=/cache",
                    "--scanners=vuln",
                    "--severity=HIGH,CRITICAL",
                    "--format=json",
                    "--no-progress",
                )
                target = "/input/gateway-image.sbom.cdx.json"
                self.assertEqual(
                    run.call_args_list,
                    [
                        mock.call(
                            ("docker", "pull", TRIVY_REFERENCE),
                            cwd=ROOT,
                            check=True,
                            timeout=TRIVY_SCAN_TIMEOUT_SECONDS,
                        ),
                        mock.call(
                            (*common, "--network=none", *scanner,
                             "--skip-db-update", "--offline-scan", target),
                            cwd=ROOT,
                            check=True,
                            capture_output=True,
                            timeout=TRIVY_SCAN_TIMEOUT_SECONDS,
                        ),
                        mock.call(
                            (*common, *scanner, target),
                            cwd=ROOT,
                            check=True,
                            capture_output=True,
                            timeout=TRIVY_SCAN_TIMEOUT_SECONDS,
                        ),
                    ],
                )
            with mock.patch("scan_gateway_image.subprocess.run") as run:
                with self.assertRaises(ValueError):
                    _docker_scan(cache=cache, sbom=sbom, offline=True, pull="always")
                run.assert_not_called()

    def test_trivy_scan_uses_the_native_cache_owner_without_capabilities(self) -> None:
        report = {"Trivy": {"Version": "0.74.0"}, "Results": []}
        completed = subprocess.CompletedProcess(
            args=(),
            returncode=0,
            stdout=canonical_json_bytes(report),
            stderr=b"",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir(mode=0o700)
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            with (
                mock.patch("scan_gateway_image.os.getuid", return_value=1001),
                mock.patch("scan_gateway_image.os.getgid", return_value=127),
                mock.patch(
                    "scan_gateway_image.subprocess.run", return_value=completed
                ) as run,
            ):
                self.assertEqual(
                    _docker_scan(
                        cache=cache,
                        sbom=sbom,
                        offline=False,
                        pull="never",
                    ),
                    report,
                )

            command = run.call_args.args[0]
            self.assertIn("--read-only", command)
            self.assertIn("--cap-drop=ALL", command)
            self.assertIn("--security-opt=no-new-privileges", command)
            self.assertIn("--user=1001:127", command)
            self.assertIn(
                "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m,mode=0700,"
                "uid=1001,gid=127",
                command,
            )

    def test_trivy_failure_retains_only_a_safe_actionable_cause(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir()
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            command_path = "/" + "private/tmp/project/hidden-input"
            error = subprocess.CalledProcessError(
                returncode=7,
                cmd=("docker", "run", command_path),
                output=b"",
                stderr=b"database download failed: connection reset\n",
            )
            with mock.patch(
                "scan_gateway_image.subprocess.run", side_effect=error
            ) as run, self.assertRaisesRegex(
                ValueError, "pinned Trivy scan failed with exit code 7"
            ) as raised:
                _docker_scan(cache=cache, sbom=sbom, offline=False, pull="never")

            message = str(raised.exception)
            self.assertIn('stderr_text="database download failed: connection reset"', message)
            self.assertIn("stdout_status=readable", message)
            self.assertIn("stderr_status=readable", message)
            self.assertNotIn(command_path, message)
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)
            run.assert_called_once()

    def test_trivy_failure_withholds_sensitive_private_and_nontext_streams(self) -> None:
        sentinel = b"ACTUALVALUE123456"
        private_key = b"-----BEGIN " + b"PRIVATE KEY-----" + sentinel
        sensitive = {
            "bearer-space": b"Bearer " + sentinel,
            "bearer-newline": b"Bearer\n" + sentinel,
            "bearer-percent": b"Bearer%20" + sentinel,
            "authorization-basic": b"Authorization: Basic " + sentinel,
            "authentication": b"Authentication failed " + sentinel,
            "oauth": b"OAuth " + sentinel,
            "credential": b"credential " + sentinel,
            "api-key": b"api_" + b"key=" + sentinel,
            "token-json": b'{"token":"' + sentinel + b'"}',
            "password-short": b"password x " + sentinel,
            "secret-bare": b"do-not-leak-secret-value " + sentinel,
            "url-userinfo": b"https://user:" + sentinel + b"@example.invalid/path",
            "url-query": b"https://example.invalid/?token=" + sentinel,
            "github-token": ("gh" + "p_" + "A" * 24).encode(),
            "github-token-line-wrap": b"github_\n" + b"pat_" + b"A" * 24,
            "github-token-literal-line-wrap": b"github_\\n"
            + b"pat_"
            + b"A" * 24,
            "github-token-percent-line-wrap": b"github_%0A"
            + b"pat_"
            + b"A" * 24,
            "github-token-form-feed-wrap": b"github_\\f"
            + b"pat_"
            + b"A" * 24,
            "github-token-unicode-line-wrap": (
                "github_\u2028" + "pat_" + "A" * 24
            ).encode(),
            "openai-token": ("s" + "k-" + "A" * 24).encode(),
            "slack-token": ("xo" + "xb-" + "A" * 24).encode(),
            "aws-key": ("AK" + "IA" + "A" * 16).encode(),
            "private-key": private_key,
            "private-key-line-wrap": b"-----BEGIN\n "
            + b"PRIVATE KEY-----"
            + sentinel,
            "private-key-unicode-line-wrap": (
                "-----BEGIN\u2028PRIVATE KEY-----"
            ).encode()
            + sentinel,
            "encrypted-private-key": b"-----BEGIN "
            + b"ENCRYPTED PRIVATE KEY-----"
            + sentinel,
            "dsa-private-key": b"-----BEGIN " + b"DSA PRIVATE KEY-----" + sentinel,
            "pgp-private-key": b"-----BEGIN "
            + b"PGP PRIVATE KEY BLOCK-----"
            + sentinel,
            "ssh2-private-key": b"-----BEGIN "
            + b"SSH2 ENCRYPTED PRIVATE KEY-----"
            + sentinel,
            "auth-token-env": b"AUTH_" + b"TOKEN=" + sentinel,
            "github-token-env": b"github_" + b"token=" + sentinel,
            "db-password-env": b"db_" + b"pass" + b"word=" + sentinel,
            "my-secret-env": b"my_" + b"secret=" + sentinel,
            "low-entropy-password": b"password=hunter22",
            "aws-secret-env": b"AWS_" + b"SECRET_ACCESS_KEY=" + sentinel,
            "authorization-token-camel": b"authorization" + b"Token=" + sentinel,
            "overlong-malformed-alias": (
                'log payload={"k'
                + "!" * 512
                + 'ey":"ENCRYPTION_KEY","value":"hunter22",}'
            ).encode(),
            "mismatched-malformed-alias": (
                "{'name':'PRIVATE_KEY','note':']','value':'hunter22'}"
            ).encode(),
            "commented-malformed-alias": (
                'log payload={"key"/*comment*/:"ENCRYPTION_KEY",'
                '"value":"hunter22",}'
            ).encode(),
            "malformed-direct-field": (
                'log payload={"P'
                + "!" * 512
                + 'ASSWORD":"hunter22",}'
            ).encode(),
            "malformed-direct-commented-field": (
                'log payload={"PASS/WORD"/*comment*/:"hunter22",}'
            ).encode(),
            "bare-basic-credential": b"Basic Zm9vOmJhcg==",
        }
        private_paths = {
            "mac-user": ("/" + "Users/runner/private/file").encode() + sentinel,
            "linux-user": ("/" + "home/runner/work/project/file").encode() + sentinel,
            "private-tmp": ("/" + "private/tmp/project/file").encode() + sentinel,
            "mac-tmpdir": ("/" + "var/folders/project/file").encode() + sentinel,
            "private-mac-tmpdir": ("/" + "private/var/folders/project/file").encode()
            + sentinel,
            "tmp": ("/" + "tmp/project/file").encode() + sentinel,
            "volume": ("/" + "Volumes/private/file").encode() + sentinel,
            "action-runner": ("/opt/" + "actions-runner/_work/file").encode()
            + sentinel,
            "hosted-tool": ("/opt/" + "hostedtoolcache/tool/file").encode()
            + sentinel,
            "container-work": ("/" + "__w/project/project/file").encode() + sentinel,
            "windows-user": ("C:" + "\\Users\\runner\\file").encode() + sentinel,
            "windows-work": ("D:" + "\\a\\project\\file").encode() + sentinel,
            "runner-env": b"RUNNER_TEMP=/safe-looking/value " + sentinel,
        }
        unsafe_streams = {
            "nul": b"safe\x00" + sentinel,
            "escape": b"safe\x1b[31m" + sentinel,
            "backspace": b"safe\x08" + sentinel,
            "delete": b"safe\x7f" + sentinel,
            "invalid-utf8": b"safe\xff" + sentinel,
            "bidi": ("safe\u202e").encode() + sentinel,
        }
        cases = {
            **{name: (payload, "sensitive") for name, payload in sensitive.items()},
            **{
                name: (payload, "private-path")
                for name, payload in private_paths.items()
            },
            **{
                name: (
                    payload,
                    "invalid-utf8" if name == "invalid-utf8" else "unsafe-control",
                )
                for name, payload in unsafe_streams.items()
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir()
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            for name, (payload, reason) in cases.items():
                error = subprocess.CalledProcessError(
                    1, ("docker", "run"), output=payload, stderr=b"safe failure"
                )
                with self.subTest(name=name), mock.patch(
                    "scan_gateway_image.subprocess.run", side_effect=error
                ) as run, self.assertRaises(ValueError) as raised:
                    _docker_scan(cache=cache, sbom=sbom, offline=False, pull="never")
                message = str(raised.exception)
                self.assertIn(f"stdout_reason={reason}", message)
                self.assertNotIn("stdout_bytes=", message)
                self.assertNotIn("stdout_sha256=", message)
                self.assertNotIn(hashlib.sha256(payload).hexdigest(), message)
                self.assertNotIn(sentinel.decode(), message)
                self.assertNotRegex(message, r"[\x00-\x1f\x7f-\x9f]")
                self.assertIsNone(raised.exception.__cause__)
                self.assertIsNone(raised.exception.__context__)
                run.assert_called_once()

    def test_trivy_failure_bounds_streams_and_closes_process_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir()
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            exact = b"A" * MAX_TRIVY_DIAGNOSTIC_BYTES
            over = exact + b"B"
            for name, payload, expected in (
                ("exact", exact, "stdout_status=readable"),
                ("over", over, "stdout_reason=over-bound"),
            ):
                error = subprocess.CalledProcessError(
                    1, ("docker", "run"), output=payload, stderr=b""
                )
                with self.subTest(name=name), mock.patch(
                    "scan_gateway_image.subprocess.run", side_effect=error
                ), self.assertRaises(ValueError) as raised:
                    _docker_scan(cache=cache, sbom=sbom, offline=False, pull="never")
                message = str(raised.exception)
                self.assertIn(expected, message)
                if name == "exact":
                    self.assertIn(f"stdout_bytes={len(payload)}", message)
                    self.assertIn(
                        f"stdout_sha256={hashlib.sha256(payload).hexdigest()}", message
                    )
                else:
                    self.assertNotIn("stdout_bytes=", message)
                    self.assertNotIn("stdout_sha256=", message)
                    self.assertNotIn(hashlib.sha256(payload).hexdigest(), message)
                    self.assertIn("stdout_truncated=true", message)
                    self.assertNotIn("A" * 64, message)
                self.assertLess(len(message.encode()), 20_000)
                self.assertIsNone(raised.exception.__cause__)
                self.assertIsNone(raised.exception.__context__)

            hidden_path = "/" + "private/tmp/hidden-command"
            failures = (
                (
                    subprocess.TimeoutExpired(
                        ("docker", hidden_path),
                        TRIVY_SCAN_TIMEOUT_SECONDS,
                        output=b"partial safe output",
                        stderr=b"network stalled",
                    ),
                    "pinned Trivy scan timed out after 1200 seconds",
                ),
                (
                    OSError(f"cannot execute {hidden_path}"),
                    "pinned Trivy scan could not be started",
                ),
            )
            for error, expected in failures:
                with self.subTest(error=type(error).__name__), mock.patch(
                    "scan_gateway_image.subprocess.run", side_effect=error
                ), self.assertRaisesRegex(ValueError, expected) as raised:
                    _docker_scan(cache=cache, sbom=sbom, offline=False, pull="never")
                self.assertNotIn(hidden_path, str(raised.exception))
                self.assertIsNone(raised.exception.__cause__)
                self.assertIsNone(raised.exception.__context__)

    def test_unsafe_trivy_report_is_rejected_before_persistence(self) -> None:
        marker = "unsafe-" + "ENCRYPTION_" + "KEY-value"
        report = {
            "properties": [
                {"name": "ENCRYPTION_" + "KEY", "value": marker},
            ]
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sbom = root / "gateway-image.sbom.cdx.json"
            receipt = root / "image-receipt.json"
            output = root / "gateway-image.vulnerability-scan.json"
            sbom.write_text("{}", encoding="utf-8")
            receipt.write_text(
                json.dumps(
                    {
                        "source": {"clean": True, "revision": "a" * 40},
                        "image": {"manifest_digest": "sha256:" + "b" * 64},
                    }
                ),
                encoding="utf-8",
            )

            def package(_cache: Path, archive: Path) -> list[dict[str, Any]]:
                archive.write_bytes(b"database")
                return []

            with (
                mock.patch("scan_gateway_image._acquire_trivy_image"),
                mock.patch(
                    "scan_gateway_image._docker_scan",
                    side_effect=[{}, report],
                ),
                mock.patch("scan_gateway_image.package_database", side_effect=package),
                mock.patch("scan_gateway_image.inspect_database_archive", return_value=[]),
                mock.patch("scan_gateway_image.cache_inventory", return_value=[]),
                self.assertRaisesRegex(
                    ValueError, "gateway Trivy report contains prohibited"
                ) as raised,
            ):
                generate_scan_evidence(sbom=sbom, receipt_path=receipt, output=output)

            self.assertNotIn(marker, str(raised.exception))
            self.assertFalse((root / "gateway-image.trivy-report.json").exists())
            self.assertFalse(output.exists())

    def test_unsafe_jose_report_is_rejected_before_persistence(self) -> None:
        header = base64.urlsafe_b64encode(b' {"alg":"RS256"}').rstrip(b"=").decode()
        token = f"{header}.{'B' * 4_097}.{'C' * 342}"
        report = {"ArtifactName": token}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sbom = root / "gateway-image.sbom.cdx.json"
            receipt = root / "image-receipt.json"
            output = root / "gateway-image.vulnerability-scan.json"
            sbom.write_text("{}", encoding="utf-8")
            receipt.write_text(
                json.dumps(
                    {
                        "source": {"clean": True, "revision": "a" * 40},
                        "image": {"manifest_digest": "sha256:" + "b" * 64},
                    }
                ),
                encoding="utf-8",
            )

            def package(_cache: Path, archive: Path) -> list[dict[str, Any]]:
                archive.write_bytes(b"database")
                return []

            with (
                mock.patch("scan_gateway_image._acquire_trivy_image"),
                mock.patch(
                    "scan_gateway_image._docker_scan",
                    side_effect=[{}, report],
                ),
                mock.patch("scan_gateway_image.package_database", side_effect=package),
                mock.patch("scan_gateway_image.inspect_database_archive", return_value=[]),
                mock.patch("scan_gateway_image.cache_inventory", return_value=[]),
                self.assertRaisesRegex(
                    ValueError, "gateway Trivy report contains prohibited"
                ) as raised,
            ):
                generate_scan_evidence(sbom=sbom, receipt_path=receipt, output=output)

            self.assertNotIn(token, str(raised.exception))
            self.assertFalse((root / "gateway-image.trivy-report.json").exists())
            self.assertFalse(output.exists())

    def test_trivy_failure_withholds_pat_and_escaped_windows_paths(self) -> None:
        def percent_encode(value: str, layers: int) -> bytes:
            encoded = value
            for _ in range(layers):
                encoded = "".join(f"%{ord(character):02X}" for character in encoded)
            return encoded.encode()

        sentinel = b"ACTUALVALUE123456"
        cases = {
            "fine-grained-pat": (
                ("github_" + "pat_").encode() + sentinel + b"A" * 8,
                "sensitive",
            ),
            "percent-pat": (
                ("github%255F" + "pat%255F").encode() + sentinel + b"A" * 8,
                "sensitive",
            ),
            "prefixed-api-key": (
                ("OPENAI_API_" + "KEY=").encode() + sentinel + b"A" * 8,
                "sensitive",
            ),
            "json-unicode-linux-path": (
                ("\\" + "u002fhome\\u002frunner\\u002fwork").encode()
                + sentinel,
                "private-path",
            ),
            "nested-linux-path": (
                b"failed,/" + b"home/runner/work/private" + sentinel,
                "private-path",
            ),
            "named-file-uri": (
                b"file://build-agent/" + b"home/runner/work" + sentinel,
                "private-path",
            ),
            "unc-windows-path": (
                ("\\\\build-agent\\" + "Users\\alice\\project").encode()
                + sentinel,
                "private-path",
            ),
            "unc-admin-share-path": (
                ("\\\\build-agent\\C$\\" + "Users\\alice\\project").encode()
                + sentinel,
                "private-path",
            ),
            "extended-unc-path": (
                ("\\\\?\\UNC\\build-agent\\share\\" + "Users\\alice\\project").encode()
                + sentinel,
                "private-path",
            ),
            "generic-unc-share-path": (
                ("\\\\build-agent\\share\\project\\file").encode() + sentinel,
                "private-path",
            ),
            "wsl-unc-home-path": (
                ("\\\\wsl$\\Ubuntu\\home\\alice\\project").encode() + sentinel,
                "private-path",
            ),
            "generic-extended-unc-path": (
                ("\\\\?\\UNC\\build-agent\\share\\project\\file").encode()
                + sentinel,
                "private-path",
            ),
            "generic-drive-path": (
                ("D:\\build\\checkout\\file").encode() + sentinel,
                "private-path",
            ),
            "named-file-share-uri": (
                b"file://build-agent/share/project" + sentinel,
                "private-path",
            ),
            "local-workspace-file-uri": (
                b"file://localhost/workspace/private" + sentinel,
                "private-path",
            ),
            "single-slash-file-uri": (
                b"file:/srv/private" + sentinel,
                "private-path",
            ),
            "ipv6-file-uri": (
                b"file://[2001:db8::1]/share/project" + sentinel,
                "private-path",
            ),
            "forward-unc-path": (
                b"//build-agent/share/project/file" + sentinel,
                "private-path",
            ),
            "mixed-unc-path": (
                b"//build-agent\\share\\project\\file" + sentinel,
                "private-path",
            ),
            "normalised-home-path": (
                b"/usr/../" + b"home/alice/project" + sentinel,
                "private-path",
            ),
            "root-traversal-path": (
                b"/../etc/" + b"passwd" + sentinel,
                "private-path",
            ),
            "long-traversal-path": (
                ("/" + "a/" * 1025 + "../" + "se" + "cret").encode()
                + sentinel,
                "private-path",
            ),
            "device-drive-path": (
                ("\\\\.\\C:\\build\\file").encode() + sentinel,
                "private-path",
            ),
            "extended-device-volume": (
                (
                    "\\\\?\\Volume{12345678-1234-1234-1234-123456789abc}"
                    "\\Users\\alice\\private"
                ).encode()
                + sentinel,
                "private-path",
            ),
            "unicode-linux-user-path": (
                ("/home/" + "álîcé/work").encode() + sentinel,
                "private-path",
            ),
            "unicode-windows-user-path": (
                ("C:\\Users\\" + "álîcé\\project").encode() + sentinel,
                "private-path",
            ),
            "private-key-b64": (
                b"SSH_PRIVATE_" + b"KEY_B64=" + sentinel,
                "sensitive",
            ),
            "private-key-camel-pem": (
                b"ssh" + b"PrivateKeyPem=" + sentinel,
                "sensitive",
            ),
            "private-key-pkcs12": (
                b"SSH_PRIVATE_" + b"KEY_PKCS12=" + sentinel,
                "sensitive",
            ),
            "complete-cpe-credential": (
                b"cpe:2.3:a:vendor:ENCRYPTION_"
                + b"KEY:hunter22:*:*:*:*:*:*:*"
                + sentinel,
                "sensitive",
            ),
            "slack-app-token": (
                b"xapp-1-" + b"A" * 32 + sentinel,
                "sensitive",
            ),
            "empty-user-uri-password": (
                b"https://:hunter2@example.invalid/path" + sentinel,
                "sensitive",
            ),
            "deep-material-suffix": (
                b"OPENAI_API_" + b"KEY_BASE64_ENCODED_VALUE=" + sentinel,
                "sensitive",
            ),
            "plural-private-key": (
                b"PRIVATE_" + b"KEYS=" + sentinel,
                "sensitive",
            ),
            "slash-namespaced-key": (
                b"config/OPENAI_API_" + b"KEY=" + sentinel,
                "sensitive",
            ),
            "safe-prefix-smuggling": (
                b"PASSWORD=[redacted] " + sentinel,
                "sensitive",
            ),
            "adjacent-placeholder-smuggling": (
                b"PASS" + b"WORD=${PASSWORD}foo=bar" + sentinel,
                "sensitive",
            ),
            "overlong-password-key": (
                b"A" * 160 + b"_PASS" + b"WORD=hunter2" + sentinel,
                "sensitive",
            ),
            "quoted-overlong-password-key": (
                b'"' + b"A" * 160 + b'_PASSWORD":"hunter2"' + sentinel,
                "sensitive",
            ),
            "short-authorization": (
                b"Authorization: Bearer x " + sentinel,
                "sensitive",
            ),
            "equals-authorization": (
                b"Authorization=Bearer x " + sentinel,
                "sensitive",
            ),
            "projected-authorization": (
                b"HTTP_" + b"AUTHORIZATION=Bearer x " + sentinel,
                "sensitive",
            ),
            "bracketed-authorization": (
                b"headers[" + b"Authorization]=Bearer x " + sentinel,
                "sensitive",
            ),
            "dotted-authorization": (
                b"request.Authorization=Negotiate hunter2 " + sentinel,
                "sensitive",
            ),
            "nested-bracket-key": (
                b"config[pass%77ord][value]=hunter22 " + sentinel,
                "sensitive",
            ),
            "structured-property": (
                b'{"properties":[{"name":"ENCRYPTION_'
                + b'KEY","value":"x"}]}'
                + sentinel,
                "sensitive",
            ),
            "embedded-key-property": (
                b'log payload={"key":"ENCRYPTION_'
                + b'KEY","value":"hunter22"}'
                + sentinel,
                "sensitive",
            ),
            "embedded-distant-property": (
                b'log payload={"name":"PRIVATE_'
                + b'KEY","padding":"'
                + b"x" * 513
                + b'","value":"hunter22"}'
                + sentinel,
                "sensitive",
            ),
            "normalised-property-collision": (
                b'{"key":"ENCRYPTION_'
                + b'KEY","key!":"safe","value":"hunter22"}'
                + sentinel,
                "sensitive",
            ),
            "malformed-normalised-property": (
                b'log payload={"env_name":"PRIVATE_'
                + b'KEY","value":"hunter22",}'
                + sentinel,
                "sensitive",
            ),
            "alternate-json-jwt-header": (
                base64.urlsafe_b64encode(b' {"alg":"RS256"}').rstrip(b"=")
                + b"."
                + b"B" * 12
                + b"."
                + b"C" * 12
                + sentinel,
                "sensitive",
            ),
            "short-jwt-claims": (
                base64.urlsafe_b64encode(b'{"alg":"HS256"}').rstrip(b"=")
                + b".e30."
                + b"C" * 43
                + sentinel,
                "sensitive",
            ),
            "direct-jwe": (
                base64.urlsafe_b64encode(
                    b'{"alg":"dir","enc":"A256GCM"}'
                ).rstrip(b"=")
                + b".."
                + b"A" * 16
                + b"."
                + b"B" * 24
                + b"."
                + b"C" * 22
                + sentinel,
                "sensitive",
            ),
            "encoded-embedded-json": (
                b'{"message":"log payload=%7B%22key%22:%22ENCRYPTION_'
                + b'KEY%22,%22value%22:%22hunter22%22%7D"}'
                + sentinel,
                "sensitive",
            ),
            "aggregate-auth": (
                b'{"key":"auth","value":{"opaque":"hunter22"}}'
                + sentinel,
                "sensitive",
            ),
            "overlong-jwt": (
                b"eyJhbGciOiJSUzI1NiJ9."
                + b"B" * 4097
                + b"."
                + b"C" * 342
                + sentinel,
                "over-bound",
            ),
            "short-query-token": (
                b"https://example.invalid/?token=x " + sentinel,
                "sensitive",
            ),
            "array-query-token": (
                b"https://example.invalid/?token[]=hunter22 " + sentinel,
                "sensitive",
            ),
            "indexed-query-token": (
                b"https://example.invalid/?token[0]=x " + sentinel,
                "sensitive",
            ),
            "named-query-token": (
                b"https://example.invalid/?token%5Bvalue%5D=x " + sentinel,
                "sensitive",
            ),
            "nested-query-token": (
                b"https://example.invalid/?token[0][value]=x " + sentinel,
                "sensitive",
            ),
            "four-layer-percent-key": (
                percent_encode("OPENAI_API_KEY=hunter22", 4) + sentinel,
                "sensitive",
            ),
            "wsl-windows-path": (
                ("/mnt/c/" + "Users/alice/project").encode() + sentinel,
                "private-path",
            ),
            "windows-double-separators": (
                ("C:" + "\\\\" + "Users" + "\\\\" + "runner\\\\file").encode()
                + sentinel,
                "private-path",
            ),
            "windows-multiple-separators": (
                ("D:" + "\\\\\\\\" + "a" + "\\\\\\\\" + "project\\\\\\\\file").encode()
                + sentinel,
                "private-path",
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = root / "cache"
            cache.mkdir()
            sbom = root / "gateway-image.sbom.cdx.json"
            sbom.write_text("{}")
            for name, (payload, reason) in cases.items():
                failures = (
                    subprocess.CalledProcessError(
                        1, ("docker", "run"), output=payload, stderr=b"safe failure"
                    ),
                    subprocess.TimeoutExpired(
                        ("docker", "run"),
                        TRIVY_SCAN_TIMEOUT_SECONDS,
                        output=payload,
                        stderr=b"safe failure",
                    ),
                )
                for failure in failures:
                    with (
                        self.subTest(name=name, failure=type(failure).__name__),
                        mock.patch(
                            "scan_gateway_image.subprocess.run", side_effect=failure
                        ),
                        self.assertRaises(ValueError) as raised,
                    ):
                        _docker_scan(
                            cache=cache, sbom=sbom, offline=False, pull="never"
                        )
                    message = str(raised.exception)
                    self.assertIn(f"stdout_reason={reason}", message)
                    self.assertNotIn("stdout_bytes=", message)
                    self.assertNotIn("stdout_sha256=", message)
                    self.assertNotIn(hashlib.sha256(payload).hexdigest(), message)
                    self.assertNotIn(payload.decode(), message)
                    self.assertNotIn(sentinel.decode(), message)
                    self.assertIsNone(raised.exception.__cause__)
                    self.assertIsNone(raised.exception.__context__)

    def test_bounded_json_reader_rejects_oversize_links_and_special_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = root / "valid.json"
            valid.write_bytes(b'{"value":1}')
            self.assertEqual(
                load_bounded_json_object(
                    valid,
                    maximum_bytes=32,
                    label="fixture",
                ),
                {"value": 1},
            )
            link = root / "linked.json"
            link.symlink_to(valid)
            fifo = root / "special.json"
            os.mkfifo(fifo)
            oversized = root / "oversized.json"
            oversized.write_bytes(b'{"value":123}')
            for name, path, maximum in (
                ("symlink", link, 32),
                ("fifo", fifo, 32),
                ("oversized", oversized, 4),
            ):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    load_bounded_json_object(
                        path,
                        maximum_bytes=maximum,
                        label="fixture",
                    )
            for raw in (
                b'{"value":1,"value":2}',
                b'{"value":NaN}',
                b"[]",
            ):
                with self.subTest(raw=raw), self.assertRaises(ValueError):
                    parse_bounded_json_object(
                        raw,
                        maximum_bytes=32,
                        label="fixture",
                    )

    def test_scan_and_manifest_phase_timings_are_bounded_and_consistent(self) -> None:
        scan_phase = {
            "started_at": "2026-08-21T10:00:00Z",
            "completed_at": "2026-08-21T10:00:02Z",
            "duration_ms": 2_000,
        }
        verify_phase_timing(scan_phase)
        scan_phase["duration_ms"] = 20_000
        with self.assertRaises(ValueError):
            verify_phase_timing(scan_phase)
        for invalid in (
            {
                "started_at": "2026-08-21T10:00:00Z",
                "completed_at": "2026-08-21T10:00:00Z",
                "duration_ms": 0,
            },
            {
                "started_at": "2026-08-21T10:00:01Z",
                "completed_at": "2026-08-21T10:00:00Z",
                "duration_ms": 1_000,
            },
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                verify_phase_timing(invalid)

        phases = []
        for offset, name in enumerate(
            [
                "okf",
                "package",
                "verify",
                "reproducibility",
                "sbom",
                "vulnerability-scan",
                "container-acceptance",
            ]
        ):
            phases.append(
                {
                    "name": name,
                    "started_at": f"2026-08-21T10:00:{offset:02d}Z",
                    "completed_at": f"2026-08-21T10:00:{offset + 1:02d}Z",
                    "duration_ms": 1_000,
                    "passed": True,
                }
            )
        _verify_phases(phases)
        phases[3]["duration_ms"] = 20_000
        with self.assertRaises(ValueError):
            _verify_phases(phases)

        equal_endpoint = json.loads(canonical_json_bytes(phases))
        equal_endpoint[3]["duration_ms"] = 1_000
        equal_endpoint[0]["completed_at"] = equal_endpoint[0]["started_at"]
        equal_endpoint[0]["duration_ms"] = 1
        _verify_phases(equal_endpoint)
        overlapping = json.loads(canonical_json_bytes(equal_endpoint))
        overlapping[1]["started_at"] = "2026-08-21T09:59:59Z"
        with self.assertRaises(ValueError):
            _verify_phases(overlapping)

    def test_acceptance_timings_are_ordered_and_contained_by_the_outer_phase(self) -> None:
        names = [
            "engine-identity",
            "exact-oci-load",
            "compose-render",
            "compose-start-and-probe",
            "restart-and-persistence",
            "service-suspension",
            "exact-image-restore",
        ]
        phases = [
            {
                "name": name,
                "started_at": f"2026-08-21T10:01:00.{offset * 10:03d}Z",
                "ended_at": f"2026-08-21T10:01:00.{(offset + 1) * 10:03d}Z",
                "duration_ms": 10,
                "status": "passed",
            }
            for offset, name in enumerate(names)
        ]
        started_at, ended_at, duration_ms = _verify_acceptance_phase_timings(phases)
        self.assertEqual(duration_ms, 70)
        outer = {
            "name": "container-acceptance",
            "started_at": "2026-08-21T10:00:59Z",
            "completed_at": "2026-08-21T10:01:01Z",
            "duration_ms": 2_000,
            "passed": True,
        }
        _verify_outer_phase_containment(
            outer,
            inner_started_at=started_at,
            inner_completed_at=ended_at,
            inner_duration_ms=duration_ms,
            label="gateway container acceptance",
        )

        zero_millisecond_phase = json.loads(canonical_json_bytes(phases))
        zero_millisecond_phase[0]["ended_at"] = zero_millisecond_phase[0]["started_at"]
        zero_millisecond_phase[0]["duration_ms"] = 0
        _verify_acceptance_phase_timings(zero_millisecond_phase)
        mutations = []
        changed = json.loads(canonical_json_bytes(phases))
        changed[1]["started_at"] = "2026-08-21T10:01:00.005Z"
        mutations.append(changed)
        changed = json.loads(canonical_json_bytes(phases))
        changed[0]["ended_at"] = "2026-08-21T10:00:59.999Z"
        mutations.append(changed)
        changed = json.loads(canonical_json_bytes(phases))
        changed[2]["duration_ms"] = 10_000
        mutations.append(changed)
        changed = json.loads(canonical_json_bytes(phases))
        changed[0], changed[1] = changed[1], changed[0]
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                _verify_acceptance_phase_timings(changed)

        for inner_start, inner_end, inner_duration in (
            ("2026-08-21T10:00:56Z", ended_at, 4_070),
            (started_at, "2026-08-21T10:01:04Z", 4_000),
            (started_at, ended_at, 10_000),
        ):
            with self.subTest(
                inner_start=inner_start,
                inner_end=inner_end,
            ), self.assertRaises(ValueError):
                _verify_outer_phase_containment(
                    outer,
                    inner_started_at=inner_start,
                    inner_completed_at=inner_end,
                    inner_duration_ms=inner_duration,
                    label="gateway container acceptance",
                )

    def test_evidence_writer_rejects_an_extra_directory_or_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for name in ACCEPTED_FILES - {"gateway-image-evidence-manifest.json"}:
                (output / name).write_bytes(b"x")
            extra = output / "unreviewed"
            extra.mkdir()
            with mock.patch("gateway_evidence.make_evidence_manifest", return_value={}):
                with self.assertRaises(ValueError):
                    write_evidence_manifest(output, [])
            extra.rmdir()
            (output / "unreviewed").symlink_to(output / "image-receipt.json")
            with mock.patch("gateway_evidence.make_evidence_manifest", return_value={}):
                with self.assertRaises(ValueError):
                    write_evidence_manifest(output, [])

    def test_shared_evidence_privacy_boundary_rejects_paths_and_credentials(self) -> None:
        def percent_encode(value: str, layers: int) -> str:
            encoded = value
            for _ in range(layers):
                encoded = "".join(f"%{ord(character):02X}" for character in encoded)
            return encoded

        private_cpe_paths = (
            "cpe:2.3:C:" + "\\Users\\alice\\secret",
            "cpe:2.3:c:" + "\\Users\\alice\\secret",
            "cpe:2.3:C:/" + "Users/alice/secret",
            "cpe:2.3:H:" + "\\Users\\zoe:product:1:*:*:*:*:*:*:*",
            "cpe:2.3:C:" + "\\" + "x" * 255,
            "cpe:2.3:C:" + "\\" + "x" * 256,
            "cpe:2.3:H:" + "\\" + "x" * 1_025,
            "cpe:/D:" + "\\build\\checkout",
            percent_encode("cpe:2.3:C:" + "\\Users\\alice\\secret", 1),
        )
        private_paths = (
            "/" + "Users/alice/project/file",
            "/" + "Users/alice",
            "/" + "home/alice/project/file",
            "/" + "home/runner",
            "/" + "Volumes/work/project/file",
            "/" + "private/tmp/project/file",
            "/" + "private/tmp/",
            "/" + "private/var/folders/project/file",
            "/" + "var/folders/project/file",
            "/" + "tmp/project/file",
            "/" + "root/private/file",
            "/" + "runner/project/file",
            "/" + "github/workspace/project/file",
            "/" + "__w/project/project/file",
            "/" + "__t/project/file",
            "/opt/" + "actions-runner/_work/file",
            "/opt/" + "hostedtoolcache/tool/file",
            "C:" + "\\Users\\alice\\file",
            "C:" + "\\Users\\alice",
            "D:" + "\\\\a\\\\project\\\\file",
            "RUNNER_" + "TEMP=/private/location",
            "GITHUB_" + "WORKSPACE=/private/location",
            "HOME=/" + "home/runner",
            "USERPROFILE=C:" + "\\Users\\alice",
            "file:///" + "Users/alice/work",
            "file:///" + "home/runner/work",
            "file:///C:/" + "Users/alice/file",
            "file://localhost/" + "home/runner",
            "file://build-agent/" + "home/runner",
            "file://build-agent/share/" + "Users/alice/project",
            "file://build-agent/share/" + "home/alice/project",
            "file:///C:" + "\\Users\\alice",
            "\\\\build-agent\\" + "Users\\alice\\project",
            "\\\\build-agent\\C$\\" + "Users\\alice\\project",
            "\\\\build-agent\\share\\project\\file",
            "\\\\build-agent\\C$\\Windows\\Temp\\file",
            "\\\\build-agent\\home\\alice\\private",
            "\\\\build-agent\\share\\home\\alice\\private",
            "\\\\wsl$\\Ubuntu\\home\\alice\\private",
            "\\\\?\\C:" + "\\Users\\alice\\project",
            "\\\\?\\UNC\\build-agent\\share\\" + "Users\\alice\\project",
            "\\\\?\\UNC\\build-agent\\share\\project\\file",
            "\\\\?\\UNC\\build-agent\\share\\home\\alice\\private",
            "C:" + "\\work\\project\\file",
            "D:" + "\\build\\checkout\\file",
            "/mnt/c/" + "Users/alice/project",
            "/" + "home/álîcé/work",
            "/" + "Users/álîcé/work",
            "C:" + "\\Users\\álîcé\\project",
            "/" + "Users/alice?source=build",
            "/" + "home/runner#cache",
            "artifact_path:/" + "Users/alice",
            "path:/" + "home/alice/file",
            "path:C:" + "\\work\\file",
            *private_cpe_paths,
            "file://localhost/workspace/private",
            "file:/srv/private",
            "file:///workspace/private",
            "file://[::1]/workspace/private",
            "file://[2001:db8::1]/share/project",
            "file://" + "a" * 65 + ".example/share/project",
            "//build-agent/share/project/file",
            "//wsl$/Ubuntu/" + "home/alice/project",
            "//?/UNC/server/share/secret.txt",
            "//build-agent\\share\\project\\file",
            "\\\\build-agent/share/project/file",
            "/" + "home//alice/project",
            "/usr/../" + "home/alice/project",
            "/../etc/" + "passwd",
            "/../etc/" + "shadow",
            "/" + "a/" * 1025 + "../" + "se" + "cret",
            "\\\\.\\C:\\build\\file",
            "\\\\?\\Volume{12345678-1234-1234-1234-123456789abc}"
            "\\Users\\alice\\private",
            "\\\\?\\GLOBALROOT\\Device\\HarddiskVolume1"
            "\\Users\\alice\\private",
            "C:\\",
            "C:/",
            "C:\\" + "a" * 65 + "\\file",
            "\\\\server\\" + "a" * 65 + "\\file",
            "%2F" + "home%2Falice%2Fproject%2Ffile",
            "%252F" + "home%252Falice%252Fproject%252Ffile",
            "\\" + "u002fhome\\u002falice\\u002fproject\\u002ffile",
            "C%3A%5C" + "Users%5Calice%5Cproject%5Cfile",
            percent_encode("/" + "home/alice/project/file", 4),
        )
        credentials = (
            "Authorization: " + "Bearer " + "A" * 24,
            "Bearer%20" + "A" * 24,
            "Authorization: " + "Basic " + "A" * 24,
            "Authorization: " + "Basic Zm9vOmJhcg==",
            "Basic Zm9vOmJhcg==",
            "Basic dTpw",
            "Basic OnBhc3M=",
            "Basic 6TpwYXNz",
            "Basic dXNlcjpw/3Nz",
            "Basic /zp4",
            "Basic 55So5oi3OuWvhueivA==",
            "Basic dTrDqQ",
            "Basic /zphYmM=",
            "Basic dTpwCg==",
            "Basic dTpwCg",
            "Basic dTpwAA==",
            "Basic dTpwAA",
            "Basic ADpw",
            "Basic dXNlcjpwfw==",
            "Basic dXNlcjpwfw",
            "Basic dXNlcjpwhQ",
            "https://user:" + "A" * 24 + "@example.invalid/path",
            "https://:hunter2@example.invalid/path",
            "postgresql://user:" + "A" * 24 + "@example.invalid/database",
            "postgresql://:x@example.invalid/database",
            "https://example.invalid/?" + "token=" + "A" * 24,
            "gh" + "p_" + "A" * 24,
            "github_" + "pat_" + "A" * 24,
            "s" + "k-" + "A" * 24,
            "s" + "k-proj-" + "A" * 24,
            "s" + "k_live_" + "A" * 24,
            "s" + "k_test_" + "A" * 24,
            "r" + "k_live_" + "A" * 24,
            "wh" + "sec_" + "A" * 24,
            "gl" + "pat-" + "A" * 24,
            "npm" + "_" + "A" * 24,
            "pypi-" + "AgEI" + "A" * 24,
            "AI" + "za" + "A" * 35,
            "xo" + "xb-" + "A" * 24,
            "xo" + "xc-" + "A" * 24,
            "xo" + "xe-" + "A" * 24,
            "xapp-1-" + "A" * 32,
            "AK" + "IA" + "A" * 16,
            "AS" + "IA" + "A" * 16,
            "AWS_" + "SECRET_ACCESS_KEY=" + "A" * 40,
            "AWS_" + "SESSION_TOKEN=" + "A" * 24,
            "-----BEGIN " + "PRIVATE KEY-----",
            "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----",
            "-----BEGIN " + "DSA PRIVATE KEY-----",
            "-----BEGIN " + "PGP PRIVATE KEY BLOCK-----",
            "-----BEGIN " + "SSH2 ENCRYPTED PRIVATE KEY-----",
            "gis-ai-go:" + "ik:v1:" + "a" * 64,
            '"token":"' + "A" * 16 + '"',
            "api" + "Key=" + "A" * 16,
            "client" + "Secret=" + "A" * 16,
            "access" + "Token=" + "A" * 16,
            "refresh_" + "token=" + "A" * 16,
            "db_" + "password=" + "A" * 16,
            "my_" + "secret=" + "A" * 16,
            "github_" + "token=" + "A" * 16,
            "authorization" + "Token=" + "A" * 16,
            "OPENAI_" + "API_KEY=" + "A" * 36,
            "ANTHROPIC_" + "API_KEY=" + "A" * 36,
            "NPM_" + "TOKEN=" + "A" * 36,
            "GH_" + "TOKEN=" + "A" * 36,
            "AZURE_" + "CLIENT_SECRET=" + "A" * 36,
            ":_auth" + "Token=" + "A" * 36,
            "secret=" + "A" * 16,
            "api_" + "token=" + "A" * 16,
            "service_" + "password=" + "A" * 16,
            "password=p@ssw0rd!value",
            "pass" + 'word="correct horse battery staple"',
            "PASS" + "WORD=correct horse battery staple",
            "PASS" + 'WORD="pa\\"ssword-123"',
            "SECRET_" + "KEY_BASE=" + "A" * 24,
            "RAILS_SECRET_" + "KEY_BASE=" + "A" * 24,
            "SECRET_" + "ACCESS_KEY=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_DATA=" + "A" * 24,
            "JWT_SIGNING_" + "KEY_VALUE=" + "A" * 24,
            "ENCRYPTION_" + "KEY_MATERIAL=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_B64=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_BASE64=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_PEM=" + "A" * 24,
            "PRIVATE_" + "KEY_CONTENT=" + "A" * 24,
            "PRIVATE_" + "KEY_BYTES=" + "A" * 24,
            "SECRET_" + "KEY_HEX=" + "A" * 24,
            "PASS" + "WORD_HASH=" + "A" * 24,
            "PASS" + "WORD_DIGEST=" + "A" * 24,
            "CLIENT_" + "SECRET_RAW=" + "A" * 24,
            "ACCESS_" + "TOKEN_RAW=" + "A" * 24,
            "JWT_SIGNING_" + "KEY_PEM=" + "A" * 24,
            "ENCRYPTION_" + "KEY_B64=" + "A" * 24,
            "OPENAI_API_" + "KEY_BASE64_ENCODED_VALUE=hunter22",
            "SSH_PRIVATE_" + "KEY_PKCS8=hunter22",
            "SSH_PRIVATE_" + "KEY_OPENSSH=hunter22",
            "ENCRYPTION_" + "KEY_SEED=hunter22",
            "ssh" + "PrivateKeyPem=" + "A" * 24,
            "secret" + "KeyBase64=" + "A" * 24,
            "pass" + "wordHash=hunter22",
            "client" + "SecretValue=hunter22",
            "access" + "TokenEncoded=hunter22",
            "SECRET_" + "KEY_PEM_BASE64_DATA=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_PEM_BASE64_ENCODED=" + "A" * 24,
            "SSH_PRIVATE_" + "KEY_PKCS12=hunter22",
            "SSH_PRIVATE_" + "KEY_PFX=hunter22",
            "SSH_PRIVATE_" + "KEY_SSH=hunter22",
            "ENCRYPTION_" + "KEY_AES256=hunter22",
            "SIGNING_" + "KEY_JWK_SET=hunter22",
            "OPENAI_API_" + "KEY_PEM_PKCS8_OPENSSH_SEED_RAW_BLOB_BODY_TEXT_DATA="
            "hunter22",
            "API_" + "KEYS=hunter22",
            "OPENAI_API_" + "KEYS=hunter22",
            "SECRET_" + "KEYS=hunter22",
            "PRIVATE_" + "KEYS=hunter22",
            "SIGNING_" + "KEYS=hunter22",
            "ENCRYPTION_" + "KEYS=hunter22",
            "HMAC_" + "KEYS=hunter22",
            "FERNET_" + "KEYS=hunter22",
            "JWT_" + "KEYS=hunter22",
            "SECRET_ACCESS_" + "KEYS=hunter22",
            "PASS" + "WORD=hunter2",
            "PASS" + "WORD=ab;cd-ef-gh-ij",
            "pass" + "word=1.2.3",
            "PASS" + "WORD: >-\n  hunter2",
            "Authorization: " + "Bearer abc12345",
            "X-" + "API-Key: hunter22",
            'os.environ["OPENAI_' + 'API_KEY"] = hunter22',
            "openai" + "ApiKey=" + "A" * 24,
            "azure" + "ClientSecret=" + "A" * 24,
            "service" + "Password=hunter2",
            "pass" + "word:hunter22",
            "env:OPENAI_" + "API_KEY=hunter22",
            "prefix:pass" + "word=hunter2",
            "pass" + "word:password:hunter2",
            "secret:secret:value",
            "token:token:abc12345",
            "OPENAI_API_" + "KEY:OPENAI_API_KEY:1hunter2",
            "db_" + "password:db_password:1hunter2",
            "encryption_" + "key:encryption_key:-hunter2",
            "cpe:2.3:a:vendor:product:1.0;OPENAI_API_" + "KEY:1hunter2",
            "cpe:2.3:a:vendor:product:1.0,ENCRYPTION_"
            "KEY:1hunter2:*:*:*:*:*:*:*",
            "cpe:2.3:a:ENCRYPTION_" + "KEY:hunter22:*",
            "cpe:2.3:a:vendor:ENCRYPTION_"
            "KEY:ENCRYPTION_KEY:hunter22:*:*:*:*:*:*:*",
            "cpe:2.3:a:vendor:ENCRYPTION_"
            "KEY:hunter22:*:*:*:*:*:*:*",
            "cpe:2.3:a:vendor:PRIVATE_"
            "KEY:hunter22:*:*:*:*:*:*:*",
            "cpe:2.3:a:vendor:product:1.0:pass"
            "word:hunter2:*:*:*:*:*",
            "cpe:/a:vendor:product:1.0:pass" + "word:hunter2:*",
            "cpe:2.3:a:evil:pass" + "word:12345678:*:*:*:*:*:*:*",
            "cpe:2.3:a:evil:pass" + "word:1.0\\:hunter2:*:*:*:*:*:*:*",
            "pass" + "word:12345678",
            "pass" + "word:1hunter2",
            "pass" + "word:v1hunter2",
            "pass" + "word:1.0:hunter2",
            "token:1234567890123456",
            "api-" + "key:12345678",
            "xcpe:2.3:a:pass" + "word:12345678",
            "notcpe:2.3:a:token:1234567890123456",
            "fakecpe:/a:api-" + "key:12345678",
            "prefix-cpe:2.3:a:pass" + "word:1hunter2",
            "https://example/cpe:2.3:a:pass" + "word:12345678",
            "token=token",
            "TOKEN=TOKEN",
            '{"token":' + '"token"}',
            '{\\"pass' + 'word\\":\\"hunter2\\"}',
            'log payload={\\"token\\":\\"token\\"}',
            '{\\"OPENAI_' + 'API_KEY\\":\\"' + "A" * 24 + '\\"}',
            '"details":"{\\"pass' + 'word\\":\\"hunter2\\"}"',
            json.dumps(json.dumps({"pass" + "word": "hunter2"})),
            "api-" + "key:api-key",
            "api-" + "key=api-key",
            "--api-" + "key=" + "A" * 24,
            "--pass" + "word=hunter22",
            "config.openai" + "ApiKey=" + "A" * 24,
            "config/OPENAI_API_" + "KEY=hunter22",
            "design_token=primary-colour OPENAI_API_" + "KEY=" + "A" * 36,
            "page_token=cursor-1 AZURE_CLIENT_" + "SECRET=hunter22",
            "theme_token=primary pass" + "word=hunter2",
            "X-API-" + "Key:hunter22",
            "OPENAI_API_" + "KEY:hunter22",
            "prefix pass" + "word:hunter22",
            " pass" + "word:hunter22",
            "SECRET_" + "KEY=" + "A" * 36,
            "DJANGO_SECRET_" + "KEY=" + "A" * 36,
            "API_SECRET_" + "KEY=" + "A" * 36,
            "PRIVATE_" + "KEY=" + "A" * 36,
            "SIGNING_" + "KEY=" + "A" * 36,
            "ENCRYPTION_" + "KEY=" + "A" * 36,
            "HMAC_" + "KEY=" + "A" * 36,
            "FERNET_" + "KEY=" + "A" * 36,
            "JWT_" + "KEY=" + "A" * 36,
            "https://example.invalid/?auth=hunter22",
            "https://example.invalid/?token=hunter22",
            "https://example.invalid/?token=x",
            "https://example.invalid/?api_key=x",
            "https://example.invalid/?secret=x",
            "https://example.invalid/?token[]=hunter22",
            "https://example.invalid/?token%5B%5D=hunter22",
            "https://example.invalid/?token[0]=x",
            "https://example.invalid/?token[value]=x",
            "https://example.invalid/?token%5B0%5D=x",
            "https://example.invalid/?token%5Bvalue%5D=x",
            "https://example.invalid/?token[0][value]=x",
            "https://example.invalid/?auth[credentials][value]=x",
            "https://example.invalid/?token[foo.bar]=x",
            "https://example.invalid/?token[" + "a" * 65 + "]=hunter22",
            "https://example.invalid/?service_token[]=x",
            "https://example.invalid/?gitlab_token[0]=x",
            "https://example.invalid/?tokens[]=x",
            "https://example.invalid/?passwords[0]=x",
            "https://example.invalid/?secrets[name]=x",
            "https://example.invalid/?api_keys[]=x",
            "Authorization: " + "Bearer+" + "A" * 24,
            "Bearer+" + "A" * 24,
            '"Authorization":"Bearer+' + "A" * 24 + '"',
            "Authorization: " + "Basic+" + "A" * 24,
            "Authorization: " + "Bearer hunter2",
            "Authorization: " + "Bearer x",
            "Authorization: " + "Basic x",
            "Authorization=Basic Zm9vOmJhcg==",
            "Authorization=Bearer x",
            "HTTP_" + "AUTHORIZATION=Bearer x",
            "headers[" + "Authorization]=Bearer x",
            'headers["' + 'Authorization"]=Bearer x',
            "Authorization[0]=Bearer x",
            "Authorization: Negotiate hunter22",
            "Authorization: Digest username=x",
            "%41uthorization: Negotiate hunter22",
            "access_" + "token=hunter2",
            "api_" + "key=hunter2",
            "service_" + "token=x",
            "service_" + "token=token",
            "service" + "Token=hunter2",
            "deploy_" + "token=deploy-token",
            "registry_" + "token=secret",
            "gitlab_" + "token=hunter2",
            "A" * 160 + "_PASS" + "WORD=hunter2",
            "namespace_" * 18 + "se" + "cret=hunter2",
            "A" * 160 + "_TOKEN=x",
            '"' + "A" * 160 + '_PASS' + 'WORD":"hunter2"',
            "'" + "A" * 160 + "_PASS" + "WORD'='hunter2'",
            'os.environ["' + "A" * 160 + '_PASS' + 'WORD"] = hunter2',
            '{\\"' + "A" * 160 + '_PASS' + 'WORD\\":\\"hunter2\\"}',
            "pass" + "word[value]=hunter22",
            "pass" + "word[]=hunter22",
            "pass" + "word" + "[x]" * 17 + "=hunter22",
            "config[pass%77ord][value]=hunter22",
            'config["api_' + 'key"][value]=hunter22',
            "pass%77ord" + "[x]" * 18 + "=hunter22",
            "A" * 160 + "_PASS" + "WORD[x]=hunter22",
            "Authorization" + "[x]" * 17 + "=Bearer x",
            "request.Authorization=Negotiate hunter2",
            "HTTP-AUTHORIZATION=Negotiate hunter2",
            "--Authorization hunter2",
            "https://example.invalid/?request.Authorization=Negotiate+x",
            "base_pass" + "word=9.9",
            "base_passwd: 1.2.3",
            "base-passwd:base-passwd:3.6.1:hunter2",
            '{"properties":[{"name":"ENCRYPTION_' + 'KEY","value":"x"}]}',
            '{"properties":[{"value":"x","name":"PRIVATE_' + 'KEY"}]}',
            '{"properties":[{"name":"API_' + 'KEY","type":"string","value":"x"}]}',
            'log payload={"name":"API_' + 'KEY","type":"string","value":"x"}',
            '{"config/ENCRYPTION_' + 'KEY":"x"}',
            "eyJhbGciOiJSUzI1NiJ9." + "B" * 4097 + "." + "C" * 342,
            "//user:hunter22@example.invalid/path",
            "--pass" + "word hunter22",
            "--pass%77ord hunter22",
            "--" + "A" * 160 + "_PASS" + "WORD hunter22",
            "PASS" + "WORD=${PASSWORD}hunter22",
            "PASS" + "WORD=[redacted]hunter22",
            "PASS" + 'WORD="redacted"hunter22',
            "PASS" + 'WORD=""hunter22',
            "PASS" + "WORD=${PASSWORD}foo=bar",
            "PASS" + 'WORD="${PASSWORD}"foo=bar',
            "PASS" + "WORD=" + "A" * 257,
            "PASS" + 'WORD="' + "A" * 257 + '"',
            "PASS" + "WORD=[redacted] garbage",
            "PASS" + "WORD=${PASSWORD} garbage",
            "PASS" + "WORD=null trailing",
            "CLIENT_" + "SECRET={{ secret_ref }} suffix",
            "token=sha256:" + "a" * 64 + " trailing",
            "token=" + "Ab1!" * 3,
            "password:password",
            "secret:secret",
            "token:token",
            "github%5F" + "pat%5F" + "A" * 24,
            "github%255F" + "pat%255F" + "A" * 24,
            "%67%68%70%5F" + "A" * 24,
            percent_encode("OPENAI_API_" + "KEY=hunter22", 4),
            "eyJ" + "A" * 12 + "." + "B" * 12 + "." + "C" * 12,
        )
        for value in private_paths:
            with self.subTest(value=value):
                self.assertEqual(prohibited_text_reason(value), "private-path")
                with self.assertRaisesRegex(ValueError, "prohibited private-path"):
                    assert_no_private_text(value.encode(), "fixture")
        for value in private_cpe_paths:
            document = {"cpe": value}
            with self.subTest(structured_private_cpe=value):
                self.assertIsNotNone(prohibited_json_reason(document))
                self.assertIsNotNone(
                    prohibited_text_reason(json.dumps(document, sort_keys=True))
                )
                with self.assertRaisesRegex(ValueError, "prohibited"):
                    assert_no_private_json(document, "fixture")
        for value in credentials:
            with self.subTest(value=value):
                self.assertEqual(prohibited_text_reason(value), "sensitive")
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_text(value, "fixture")

        legitimate = (
            "packages/authority-context",
            "/usr/bin/users",
            "/tmp",
            "/tmp:rw,noexec,nosuid,nodev,size=1m",
            "author OAuth OpenID passwd base-passwd chgpasswd",
            "https://github.com/chris-page-gov/gis-ai-go",
            "https://example.invalid/" + "home/alice/docs",
            "https://example.invalid/%2Fhome/alice/docs",
            "/usr/share/doc/pkg/" + "Users/Guide/index",
            "/usr/share/tmp/example",
            "https://example.invalid/?page=token",
            "pkg:deb/debian/base-passwd@3.6.1?arch=amd64",
            "cpe:2.3:a:base-passwd:base-passwd:3.6.1:*:*:*:*:*:*:*",
            "scope:cpe:2.3:a:base-passwd:base-passwd:3.6.1:*:*:*:*:*:*:*",
            "cpe:2.3:a:passwd:passwd:1\\:4.13\\+dfsg1-1\\+deb12u2:"
            "*:*:*:*:*:*:*",
            "cpe:/a:base-passwd:base-passwd:3.6.1:*:*:*",
            "cpe:2.3:a:passwd:passwd:1\\\\:4.13\\+dfsg1-1\\+deb12u2:"
            "*:*:*:*:*:*:*",
            "cpe:2.3:a:\\\\@modelcontextprotocol\\\\/core:"
            "\\\\@modelcontextprotocol\\\\/core:2.0.0:*:*:*:*:*:*:*",
            "sha256:" + "a" * 64,
            '"token":null',
            '"token":""',
            '"token":"[redacted]"',
            '"tokens":[]',
            '"secrets":{}',
            "token=pagination",
            "TOKEN=${TOKEN_VALUE}",
            "PASSWORD=${PASSWORD}",
            "CLIENT_SECRET={{ secret_ref }}",
            "design_token=primary-colour",
            "page_token=cursor-123456",
            "token=sha256:" + "a" * 64,
            "secret=[redacted]",
            "pass" + 'word="not applicable"',
            "password=not-applicable",
            "PASSWORD=********",
            "CLIENT_SECRET=********",
            "CLIENT_SECRET=not provided",
            "PASSWORD=false",
            "PASSWORD=true",
            "PASSWORD=" + "*" * 12,
            "Bearer redacted",
            "Basic redacted",
            "Basic configuration options",
            "Basic credentials are supported",
            "Authorization: Bearer redacted",
            "Authorization: Basic redacted",
            "HTTP_AUTHORIZATION=Bearer redacted",
            "headers[Authorization]=Bearer authentication",
            "request.Authorization=Bearer redacted",
            "HTTP-AUTHORIZATION=Basic redacted",
            "authorization_policy=required",
            "config[password_format]=PEM",
            "config[page_token]=cursor-1",
            "config[secrets]={}",
            '{"properties":[{"name":"ENCRYPTION_' + 'KEY","value":"[redacted]"}]}',
            '{"properties":[{"name":"PASSWORD","value":false}]}',
            '{"properties":[{"name":"private_key_format","value":"PEM"}]}',
            "https://:@example.invalid/path",
            "https://example.invalid/?token=pagination",
            "TOKEN=${TOKEN_VALUE} PAGE=1",
            "password_policy=strict",
            "password_length=12",
            "api_key_name=service",
            "api_key_header=X-API-Key",
            "private_key_algorithm=RSA",
            "private_key_format=PEM",
            "token_count=42",
            "token_type=access",
            "credentials_provider=aws",
            "/password:reset",
            "/password:change",
            "password: policy",
            "password: requirements",
            json.dumps(json.dumps({"safe": "value"})),
            json.dumps(json.dumps(json.dumps({"safe": "value"}))),
            json.dumps(
                json.dumps(
                    {
                        "cpe": (
                            "cpe:2.3:a:base-passwd:base-passwd:3.6.1:"
                            "*:*:*:*:*:*:*"
                        )
                    }
                )
            ),
            "HOME=/nonexistent",
            "Bearer authentication uses a token package",
        )
        for value in legitimate:
            with self.subTest(value=value):
                self.assertIsNone(prohibited_text_reason(value))
                assert_no_private_text(value, "fixture")

        reviewed_escaped_cpe = (
            "cpe:2.3:a:\\\\@modelcontextprotocol\\\\/core:"
            "\\\\@modelcontextprotocol\\\\/core:2.0.0:*:*:*:*:*:*:*"
        )
        reviewed_cpe_document = {"cpe": reviewed_escaped_cpe}
        self.assertIsNone(prohibited_json_reason(reviewed_cpe_document))
        self.assertIsNone(
            prohibited_text_reason(json.dumps(reviewed_cpe_document, sort_keys=True))
        )
        assert_no_private_json(reviewed_cpe_document, "fixture")
        trivy_diagnostic = _sanitise_trivy_diagnostic(
            reviewed_escaped_cpe.encode(), label="stdout"
        )
        self.assertIn("stdout_status=readable", trivy_diagnostic)
        self.assertIn(json.dumps(reviewed_escaped_cpe), trivy_diagnostic)

    def test_structured_privacy_aliases_collisions_and_generic_jose_tokens(self) -> None:
        aliases = ("name", "key", "variable", "envName")
        for alias in aliases:
            for reverse in (False, True):
                members = (
                    f'"value":"hunter22","{alias}":"ENCRYPTION_KEY"'
                    if reverse
                    else f'"{alias}":"ENCRYPTION_KEY","value":"hunter22"'
                )
                embedded = f'log payload={{{members}}} complete'
                with self.subTest(alias=alias, reverse=reverse):
                    self.assertEqual(prohibited_text_reason(embedded), "sensitive")

        distant = (
            'log payload={"name":"PRIVATE_KEY","metadata":{"note":"'
            + "x" * 4_096
            + '"},"value":"hunter22"}'
        )
        self.assertEqual(prohibited_text_reason(distant), "sensitive")

        collisions = (
            {"key": "ENCRYPTION_KEY", "key!": "safe", "value": "hunter22"},
            {"envName": "PRIVATE_KEY", "env_name": "safe", "value": "hunter22"},
        )
        for document in collisions:
            with self.subTest(document=document):
                self.assertEqual(prohibited_json_reason(document), "sensitive")
                self.assertEqual(
                    prohibited_text_reason(json.dumps(document, sort_keys=True)),
                    "sensitive",
                )
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_json(document, "fixture")

        safe = {
            "key": "ENCRYPTION_KEY",
            "key!": "private_key_format",
            "value": "[redacted]",
        }
        self.assertIsNone(prohibited_json_reason(safe))
        self.assertIsNone(prohibited_text_reason(json.dumps(safe, sort_keys=True)))

        encoded_inner = json.dumps(
            {
                "message": (
                    "log payload=%7B%22key%22:%22ENCRYPTION_KEY%22,"
                    "%22value%22:%22hunter22%22%7D"
                )
            },
            sort_keys=True,
        )
        self.assertEqual(prohibited_text_reason(encoded_inner), "sensitive")
        self.assertEqual(
            prohibited_json_reason(json.loads(encoded_inner)),
            "sensitive",
        )

        aggregate_auth = {"key": "auth", "value": {"opaque": "hunter22"}}
        self.assertEqual(prohibited_json_reason(aggregate_auth), "sensitive")
        self.assertEqual(
            prohibited_text_reason(json.dumps(aggregate_auth, sort_keys=True)),
            "sensitive",
        )
        self.assertIsNone(
            prohibited_json_reason({"key": "auth", "value": {}})
        )

        encoded_roles = (
            {"name": "pass%77ord", "value": "hunter2"},
            {"pass%77ord": "hunter2"},
            {"name": "PRIVATE%20KEY", "value": "hunter2"},
            {"na%6de": "password", "value": "hunter2"},
        )
        for document in encoded_roles:
            with self.subTest(encoded_role=document):
                self.assertEqual(prohibited_json_reason(document), "sensitive")
                self.assertEqual(
                    prohibited_text_reason(json.dumps(document, sort_keys=True)),
                    "sensitive",
                )

        huge_integer_documents = (
            "[" + "1" * 5_000 + "]",
            '{"value":' + "1" * 5_000 + "}",
            "log payload=[" + "1" * 5_000 + "] complete",
        )
        for value in huge_integer_documents:
            with self.subTest(huge_integer=len(value)):
                self.assertEqual(prohibited_text_reason(value), "sensitive")

        dense_json = "[" + "{}," * 350_000 + "{}]"
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(dense_json), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        malformed_aliases = (
            'log payload={"env_name":"PRIVATE_KEY","value":"hunter22",}',
            'log payload={"key!":"ENCRYPTION_KEY","value":"hunter22",}',
            "{'name': 'PRIVATE_KEY', 'value': 'hunter22'}",
            "{name:PRIVATE_KEY,value:hunter22}",
            "properties=[{name=PRIVATE_KEY,value=hunter22}]",
            "{'name':'PRIVATE_KEY','note':']','value':'hunter22'}",
            "{'value':'hunter22','note':']','name':'PRIVATE_KEY'}",
            "log payload={name:PRIVATE_KEY,note:],value:hunter22}",
            "{name:PRIVATE_KEY,note:\",value:hunter22}",
            "{key:PRIVATE_KEY,[value:hunter22}",
            "{name:password,{value:hunter2}",
            '{"password"[:"hunter22"}',
            "{password" + "]" * 16 + ":hunter22}",
            "{password" + "]" * 17 + ":hunter22}",
            "{key:PRIVATE_KEY,value" + "]" * 17 + ":hunter22}",
            "{value" + "]" * 17 + ":hunter22,key:PRIVATE_KEY}",
            (
                '{"name":"PRIVATE_KEY","note":"unterminated,'
                '"value":"hunter22"}'
            ),
            (
                'log payload={"key"/*comment*/:"ENCRYPTION_KEY",'
                '"value":"hunter22",}'
            ),
            "log payload={key/*comment*/:ENCRYPTION_KEY,value:hunter22}",
            '{"name"://comment\n"password","value"//comment\n:"hunter2"}',
            '{name://}\n"password",value:"hunter2"}',
            (
                'log payload={"key":"PRIVATE_KEY",/* } */'
                '"value":"hunter22",}'
            ),
            (
                'log payload={"key":"PRIVATE_KEY",// }\n'
                '"value":"hunter22",}'
            ),
            (
                'log payload={"key":"PRIVATE_KEY",/* } { */'
                '"value":"hunter22",}'
            ),
            'log payload={/* "key":"PRIVATE_KEY","value":"hunter22" */}',
            'log payload={// "key":"PRIVATE_KEY","value":"hunter22"\n}',
            'log payload={/* {"key":"PRIVATE_KEY","value":"hunter22"} */}',
            '/* key:PRIVATE_KEY,value:hunter22 */',
            (
                'log payload={// "key":"PRIVATE_KEY",\n'
                '// "value":"hunter22"\n}'
            ),
            '{/* "key":"PRIVATE KEY" } */ "value":"hunter22",}',
            '{"key":"PRIVATE KEY",/* { "value":"hunter22" */}',
            '{"key":"PRIVATE KEY","note":"{","value":"hunter22",}',
            "log payload={'message':'{\"key\":\"PRIVATE_KEY\","
            "\"value\":\"hunter22\"}',}",
            (
                "log payload={'message':'%7B%22key%22:%22PRIVATE_KEY%22,"
                "%22value%22:%22hunter22%22%7D',}"
            ),
            "{password''':hunter22}",
            "{'''password''':'''hunter22'''}",
            "{'''key''':'''PRIVATE_KEY''','''value''':'''hunter22'''}",
            "{pass'word':hunter22}",
            'PASSWORD={{ "hunter22" }}',
            '{"password":"{{ \\"hunter22\\" }}"}',
            'log payload=${"key":"PRIVATE_KEY","value":"hunter22"}',
            'log payload={{"key":"PRIVATE_KEY","value":"hunter22"}}',
            'log payload=\\{"key":"PRIVATE_KEY","value":"hunter22"}',
            '{"PRIVATE KEY"/*x*/:"sekret",}',
            '{"""key""":"""PRIVATE KEY""","""value""":"""sekret""",}',
            '{"""key\'\'\':"""PRIVATE KEY\'\'\',"""value\'\'\':"""sekret\'\'\',}',
            "{'''key\"\"\":'''PRIVATE KEY\"\"\",'''value\"\"\":'''sekret\"\"\",}",
            '{""key"":""PRIVATE KEY"",""value"":""sekret"",}',
            '{key:PRIVATE KEY,value:sekret,}',
            '{value:sekret,key:PRIVATE KEY,}',
            '{PRIVATE KEY:sekret,}',
            '{"PRIVATE/KEY\\\':"sekret",}',
            '{"key\':"PRIVATE KEY","value":"sekret",}',
            '{"key":"PRIVATE KEY","value\':"sekret",}',
            '{"PRIVATE/KEY\':"sekret",}',
            '{\'key":"PRIVATE KEY","value":"sekret",}',
            '{"key":"PRIVATE KEY",\'value":"sekret",}',
            '{\'PRIVATE/KEY":"sekret",}',
            (
                'log payload={"P'
                + "!" * 512
                + 'ASSWORD":"hunter22",}'
            ),
            'log payload={"PASS/WORD"/*comment*/:"hunter22",}',
            r'{name:"p\x61ssword",value:"hunter2"}',
            r"{'name':'p\x61ssword','value':'hunter2'}",
            r'{p\x61ssword:"hunter2"}',
            r'{na\x6de:"password",value:"hunter2"}',
            r"{'na\me':'password','value':'hunter2'}",
            r"{'name':'password','va\lue':'hunter2'}",
            r"{'p\assword':'hunter2'}",
            r"{na\me:password,value:hunter2}",
            "log payload={'config/OPENAI_API_KEY'='hunter22',}",
            (
                'log payload={"k'
                + "!" * 512
                + 'ey":"ENCRYPTION_KEY","value":"hunter22",}'
            ),
            (
                '{"url":"https://example.test/a//b",'
                '"password"/*comment*/:"hunter2"}'
            ),
            (
                '{"url":"https://example.test/a/*b",'
                '"name"/*comment*/:"password","value":"hunter2"}'
            ),
            '{"password":/*"hunter2"*/"${PASSWORD}"}',
            '{"password"://hunter2\n"[redacted]"}',
            '{"name":"password","value":/*hunter2*/"[redacted]"}',
            '{"name":"password","value":/*}hunter2*/"[redacted]"}',
            '{"name":"password","value":/*]hunter2[*/"[redacted]"}',
            '{"name":"password","value":/*//hunter2*/"[redacted]"}',
            '{"name":"password","value":/*%2F%2Fhunter2*/"[redacted]"}',
            '{"password":"${PASSWORD}"/*hunter2*/}',
            '{"password":"${PASSWORD}"//"hunter2"\n}',
            '{"name":"password","value":"[redacted]"/*hunter2*/}',
            (
                '{"value":"[redacted]"/*%68unter2*/,'
                '"name":"password"}'
            ),
            (
                '{"name":"password",/*"value":"hunter2"*/'
                '"value":"[redacted]"}'
            ),
            "{'pass,word':'hunter2'}",
            "{'pass:word':'hunter2'}",
            "{'na,me':'password','value':'hunter2'}",
            "{'name':'password','va:lue':'hunter2'}",
            '{"pass[word]":"hunter2"}',
            '{"p[ass]word":"hunter2"}',
            '{"pa[ss]word":"hunter2"}',
            '{"pass[]word":"hunter2"}',
            '{"pass[0]word":"hunter2"}',
            "{'na[me]':'password','value':'hunter2'}",
            "{'name':'password','va[lue]':'hunter2'}",
        )
        for value in malformed_aliases:
            with self.subTest(value=value):
                self.assertEqual(prohibited_text_reason(value), "sensitive")

        malformed_structural_boundaries = (
            "{key:PRIVATE_KEY,[value:hunter22}",
            "{name:password,{value:hunter2}",
            '{"password"[:"hunter22"}',
            "{password" + "]" * 17 + ":hunter22}",
            "{key:PRIVATE_KEY,value" + "]" * 17 + ":hunter22}",
            "{value" + "]" * 17 + ":hunter22,key:PRIVATE_KEY}",
        )
        for value in malformed_structural_boundaries:
            document = {"message": value}
            with self.subTest(malformed_structural_boundary=value[:32]):
                self.assertEqual(prohibited_text_reason(value), "sensitive")
                self.assertEqual(prohibited_json_reason(document), "sensitive")
                self.assertEqual(
                    prohibited_text_reason(json.dumps(document, sort_keys=True)),
                    "sensitive",
                )
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_text(value, "fixture")
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_json(document, "fixture")

        for separator in (
            "\u00a0",
            "\u1680",
            "\u2000",
            "\u2003",
            "\u2009",
            "\u202f",
            "\u205f",
            "\u3000",
        ):
            quoted = (
                'log payload={"name"'
                + separator
                + ':"PRIVATE_KEY","value"'
                + separator
                + ':"hunter22",}'
            )
            bare = (
                "log payload={name"
                + separator
                + ":PRIVATE_KEY,value"
                + separator
                + ":hunter22,}"
            )
            for value in (quoted, bare):
                with self.subTest(unicode_separator=ord(separator), value=value[:24]):
                    self.assertEqual(prohibited_text_reason(value), "sensitive")
                    self.assertEqual(
                        prohibited_json_reason({"message": value}), "sensitive"
                    )

        for terminator in ("\u2028", "\u2029"):
            value = (
                'log payload={"key":"PRIVATE_KEY",// comment'
                + terminator
                + '"value":"hunter22",}'
            )
            with self.subTest(jsonc_line_terminator=ord(terminator)):
                self.assertEqual(prohibited_text_reason(value), "sensitive")
                self.assertEqual(prohibited_json_reason({"message": value}), "sensitive")

        for value in (
            'log payload={"password_format":"PEM",}',
            "log payload={'private_key_format'='PEM',}",
        ):
            with self.subTest(safe_malformed=value):
                self.assertIsNone(prohibited_text_reason(value))

        wrapped_token = "github_\n" + "pat_" + "A" * 24
        wrapped_outer = json.dumps({"message": wrapped_token}, sort_keys=True)
        wrapped_private_key = "-----BEGIN\n " + "PRIVATE " + "KEY-----"
        wrapped_variants = (
            wrapped_token,
            wrapped_outer,
            wrapped_private_key,
            "github_\n\n" + "pat_" + "A" * 24,
            "github_\\\n" + "pat_" + "A" * 24,
            "github_\\n" + "pat_" + "A" * 24,
            "github_\\f" + "pat_" + "A" * 24,
            "github_\\u000a" + "pat_" + "A" * 24,
            "github_\\u0000" + "pat_" + "A" * 24,
            "github_\\b" + "pat_" + "A" * 24,
            "github_\\0" + "pat_" + "A" * 24,
            "github_\\x0b" + "pat_" + "A" * 24,
            "github_\\x0c" + "pat_" + "A" * 24,
            "github_\\x85" + "pat_" + "A" * 24,
            "github_%0A" + "pat_" + "A" * 24,
            "github_%E2%80%8B" + "pat_" + "A" * 24,
            "%FF%67%68%70%5F" + "A" * 24,
            "%C0%AF%67%68%70%5F" + "A" * 24,
            "%E2%28%A1%67%68%70%5F" + "A" * 24,
            "github_\0" + "pat_" + "A" * 24,
            "github_\x1b" + "pat_" + "A" * 24,
            "github_\u200b" + "pat_" + "A" * 24,
            "github_\v" + "pat_" + "A" * 24,
            "github_\f" + "pat_" + "A" * 24,
            "github_\x85" + "pat_" + "A" * 24,
            "github_\u2028" + "pat_" + "A" * 24,
            "github_\u2029" + "pat_" + "A" * 24,
            "github_\\u{2028}" + "pat_" + "A" * 24,
            "github_\\a" + "pat_" + "A" * 24,
            "github_\\12" + "pat_" + "A" * 24,
            "-----BEGIN\\n" + "PRIVATE " + "KEY-----",
            "-----BEGIN\\x0b" + "PRIVATE " + "KEY-----",
            "-----BEGIN\\x0c" + "PRIVATE " + "KEY-----",
            "-----BEGIN\\x85" + "PRIVATE " + "KEY-----",
            "-----BEGIN\\b" + "PRIVATE " + "KEY-----",
            "-----BEGIN\u2028" + "PRIVATE " + "KEY-----",
            "{'message':'github_\\n" + "pat_" + "A" * 24 + "'}",
            "Basic Zm9vOmJhcg==",
            "Basic\\\nZm9vOmJhcg==",
            "Basic OoA",
            "Basic OoE",
            "Basic OoU",
            "Basic OgA",
            "Basic Ogo",
            "Basic Ogs",
            "Basic Ogw",
            "Basic OsKF",
            "Basic OuKAqA",
            "Basic OuKAqQ",
        )
        for value in wrapped_variants:
            with self.subTest(value=value):
                self.assertEqual(prohibited_text_reason(value), "sensitive")
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_text(value, "fixture")
        self.assertEqual(
            prohibited_json_reason(json.loads(wrapped_outer)), "sensitive"
        )
        for wrapped in (
            "github_\\n" + "pat_" + "A" * 24,
            "github_\\u0000" + "pat_" + "A" * 24,
            "github_\0" + "pat_" + "A" * 24,
            "github_\u200b" + "pat_" + "A" * 24,
            "github_%E2%80%8B" + "pat_" + "A" * 24,
            "github_\u2028" + "pat_" + "A" * 24,
            malformed_aliases[5],
            malformed_aliases[8],
        ):
            outer = {"message": wrapped}
            with self.subTest(outer=wrapped[:24]):
                self.assertEqual(prohibited_json_reason(outer), "sensitive")
                self.assertEqual(
                    prohibited_text_reason(json.dumps(outer, sort_keys=True)),
                    "sensitive",
                )

        header = base64.urlsafe_b64encode(b' {"alg":"RS256"}').rstrip(b"=").decode()
        ordinary = f"{header}.{'B' * 12}.{'C' * 12}"
        overlong = f"{header}.{'B' * 4_097}.{'C' * 342}"
        short_claims = f"{header}.e30.{'C' * 43}"
        detached = f"{header}..{'C' * 43}"
        unsecured_header = base64.urlsafe_b64encode(
            b'{"alg":"none","typ":"JWT"}'
        ).rstrip(b"=").decode()
        unsecured = f"{unsecured_header}.e30."
        direct_header = base64.urlsafe_b64encode(
            b'{"alg":"dir","enc":"A256GCM"}'
        ).rstrip(b"=").decode()
        direct_jwe = f"{direct_header}..{'A' * 16}.{'B' * 24}.{'C' * 22}"
        for token in (
            ordinary,
            overlong,
            short_claims,
            detached,
            unsecured,
            direct_jwe,
        ):
            with self.subTest(length=len(token)):
                self.assertEqual(prohibited_text_reason(token), "sensitive")
                self.assertEqual(
                    prohibited_json_reason({"ArtifactName": token}),
                    "sensitive",
                )
                with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
                    assert_no_private_text(token, "fixture")

        legitimate_tokens = (
            "alpha.beta.gamma",
            "1.2.3",
            "pkg:npm/example@1.2.3",
            "Basic configuration options",
            "Basic credentials are supported",
            "Basic YWJjZA==",
            "Basic Ohio",
            "Basic Oliver",
            "Basic Olympic",
            "Basic azo",
            "Basic Old English",
            "Basic Olor",
            "Basic OnA",
            "PASSWORD=${{ secrets.NAME }}",
            "https://example.invalid/path",
            "GET https://example.test/private-key value:hunter2",
            "url=https://example.test/private-key value:hunter2",
        )
        for value in legitimate_tokens:
            with self.subTest(value=value):
                self.assertIsNone(prohibited_text_reason(value))

        harmless_malformed = (
            "log payload={name:package,value:1.2.3}",
            "properties=[{name='version',value='1.2.3'}]",
            '{"name":"colour","value":"blue",}',
            '{"description":"Basic password reset",}',
            "log payload={password:${PASSWORD},}",
            "{password:[redacted],}",
            "{key:PRIVATE_KEY,value:[redacted],}",
            (
                "log payload={cpe:cpe:2.3:a:base-passwd:base-passwd:"
                "3.6.1:*:*:*:*:*:*:*,}"
            ),
            "log payload={/* password requirements */ status:ok}",
            "{left:{key:PRIVATE_KEY},right:{value:hunter22},}",
            "[{key:PRIVATE_KEY},{value:hunter22}]",
            '{"password"[:"[redacted]"}',
            "{key:PRIVATE_KEY,[value:[redacted]}",
            "{left:{key:PRIVATE KEY},right:{value:sekret},}",
            "pass" + 'word: "{{ password }}"',
            "pass" + "word: '${{ secrets.password }}'",
            '"password": {{ password }}',
            "pass" + 'word="${PASSWORD}"',
            '"password":"${PASSWORD}"',
            '"password":${PASSWORD}',
            '"password":[redacted]',
            "{PRIVATE KEY:[redacted],}",
            "{PRIVATE KEY:${PRIVATE_KEY},}",
            "{key:PRIVATE KEY,value:[redacted],}",
            r'{pass' + r'word:"\x24\x7bPASSWORD\x7d"}',
            '{pass' + 'word:"%24%7BPASSWORD%7D"}',
            '{pass' + 'word:"%5Bredacted%5D"}',
            '{pass' + 'word:"not%20provided"}',
            '{name:password,value:"%5Bredacted%5D"}',
            '{PRIVATE KEY:%5Bredacted%5D,}',
            '{"password":/*note*/"${PASSWORD}"}',
            '{"password"://note\n"[redacted]"}',
            '{"password":"${PASSWORD}"/*note*/}',
            '{"password":"${PASSWORD}"/*provided at runtime*/}',
            '{"password":"${PASSWORD}"//note\n}',
            '{"password":"[redacted]"/*note*/,"status":"ok"}',
            '{"url":"a//b",/*note*/"password":"${PASSWORD}"}',
            '{"a":"x"//comment\n,/*note*/"b":"y"}',
            "{'private,key_format':'PEM'}",
            "{/* example key:PRIVATE_KEY */ value:blue}",
            "{/* key:PRIVATE_KEY */ description:example,value:blue}",
            '{"password":/*provided at runtime*/"${PASSWORD}"}',
            '{"password":/*configuration*/"[redacted]"}',
            '{"name":"password","value":/*TODO*/"[redacted]"}',
            '{"pass[word]_policy":"strict"}',
            '{"config[password_policy]":"strict"}',
            '{"compass[word]":"north"}',
            '{"compass_word":"north"}',
            '{"compass-word":"north"}',
            '{"value":"[redacted]"/*hunter2*/}',
            (
                '{"left":{"name":"password"},'
                '"right":{"value":"[redacted]"/*hunter2*/}}'
            ),
            (
                '[{"name":"password"},'
                '{"value":"[redacted]"/*hunter2*/}]'
            ),
            "phase ok: https://example.test/docs/private-key\nvalue: hunter2\n",
            "value://host name:password",
        )
        for value in harmless_malformed:
            with self.subTest(harmless_malformed=value):
                self.assertIsNone(prohibited_text_reason(value))

        aggregate_limit = MAX_PRIVACY_TEXT_BYTES
        started = time.monotonic()
        self.assertIsNone(
            prohibited_json_reason(
                ["a" * (aggregate_limit // 2), "b" * (aggregate_limit // 2)]
            )
        )
        self.assertLess(time.monotonic() - started, 10.0)
        self.assertEqual(
            prohibited_json_reason(
                [
                    "a" * (aggregate_limit // 2),
                    "b" * (aggregate_limit // 2 + 1),
                ]
            ),
            "sensitive",
        )
        self.assertIsNone(
            prohibited_json_reason({"k": "a" * (aggregate_limit - 1)})
        )
        self.assertEqual(
            prohibited_json_reason({"k": "a" * aggregate_limit}),
            "sensitive",
        )
        non_ascii = "£" * (aggregate_limit // 2)
        self.assertIsNone(prohibited_json_reason(non_ascii))
        self.assertEqual(prohibited_json_reason(non_ascii + "£"), "sensitive")
        shared = "x" * (aggregate_limit // 2 + 1)
        self.assertEqual(prohibited_json_reason([shared, shared]), "sensitive")

        alias_keys = []
        for mask in range(17):
            characters = list("name")
            for offset in range(4, -1, -1):
                if mask & (1 << offset):
                    characters.insert(offset, "!")
            alias_keys.append("".join(characters))
        over_alias_bound = {key: "safe" for key in alias_keys}
        over_alias_bound["padding"] = "x" * (8 * 1024 * 1024 - 1_024)
        over_alias_bound["value"] = "[redacted]"
        started = time.monotonic()
        self.assertEqual(prohibited_json_reason(over_alias_bound), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

    def test_final_privacy_gate_checks_every_textual_evidence_subject(self) -> None:
        prohibited = (
            ("github_" + "pat_" + "A" * 24).encode(),
            ("github_\n\n" + "pat_" + "A" * 24).encode(),
            ("github_\\n" + "pat_" + "A" * 24).encode(),
            ("github_%0A" + "pat_" + "A" * 24).encode(),
            ("github_\u200b" + "pat_" + "A" * 24).encode(),
            ("github_\u2028" + "pat_" + "A" * 24).encode(),
            b"Basic Zm9vOmJhcg==",
            b"{'name':'PRIVATE_KEY','note':']','value':'hunter22'}",
            b'{/* "key":"PRIVATE KEY" } */ "value":"hunter22",}',
            b"{name:PRIVATE_KEY,note:\",value:hunter22}",
            (
                b'log payload={"key"/*comment*/:"ENCRYPTION_KEY",'
                b'"value":"hunter22",}'
            ),
            (
                b'log payload={"P'
                + b"!" * 512
                + b'ASSWORD":"hunter22",}'
            ),
            b'{"properties":[{"name":"ENCRYPTION_' + b'KEY","value":"x"}]}',
            b'{"config/PRIVATE_' + b'KEY":"x"}',
            b'log payload={"variable":"ENCRYPTION_KEY",'
            + b'"metadata":{"nested":true},"value":"hunter22"}',
            b'{"message":"payload=%7B%22key%22:%22ENCRYPTION_KEY%22,'
            + b'%22value%22:%22hunter22%22%7D"}',
        )

        def safe_bytes(name: str) -> bytes:
            return b"{}\n" if name.endswith(".json") else b"safe\n"

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for name in TEXT_EVIDENCE:
                (output / name).write_bytes(safe_bytes(name))
            _verify_text_evidence_privacy(output)
            for payload in prohibited:
                for name in sorted(TEXT_EVIDENCE):
                    path = output / name
                    path.write_bytes(payload)
                    with self.subTest(name=name, payload=payload[:20]), self.assertRaisesRegex(
                        ValueError, "prohibited sensitive"
                    ):
                        _verify_text_evidence_privacy(output)
                    path.write_bytes(safe_bytes(name))
            first = output / sorted(TEXT_EVIDENCE)[0]
            first.write_bytes(b"unsafe\xff")
            with self.assertRaisesRegex(ValueError, "must be UTF-8") as raised:
                _verify_text_evidence_privacy(output)
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_final_privacy_gate_caps_reads_at_the_privacy_byte_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with mock.patch(
                "verify_gateway_image_evidence.read_bounded_regular_file",
                return_value=b"{}\n",
            ) as reader:
                _verify_text_evidence_privacy(output)

        bounds = {
            Path(call.args[0]).name: call.kwargs["maximum_bytes"]
            for call in reader.call_args_list
        }
        self.assertEqual(set(bounds), set(TEXT_EVIDENCE))
        for name, maximum_bytes in bounds.items():
            with self.subTest(name=name):
                self.assertEqual(
                    maximum_bytes,
                    min(TEXT_FILE_LIMITS[name], MAX_PRIVACY_TEXT_BYTES),
                )

    def test_shared_privacy_boundary_is_linear_for_long_assignment_prefixes(self) -> None:
        fixtures = (
            ("a_" * (8 * 1024 * 1024 // 2))[: 8 * 1024 * 1024],
            ("prefix_" * (8 * 1024 * 1024 // 7 + 1))[: 8 * 1024 * 1024],
            ("eyJ" * (8 * 1024 * 1024 // 3 + 1))[: 8 * 1024 * 1024],
        )
        for value in fixtures:
            started = time.monotonic()
            with self.subTest(prefix=value[:8]):
                self.assertIsNone(prohibited_text_reason(value))
                self.assertLess(time.monotonic() - started, 10.0)
        backslashes = "\\" * (8 * 1024 * 1024)
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(backslashes), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        colon_slashes = (":/" * (8 * 1024 * 1024 // 2))[: 8 * 1024 * 1024]
        started = time.monotonic()
        self.assertIsNone(prohibited_text_reason(colon_slashes))
        self.assertLess(time.monotonic() - started, 10.0)

        line_folds = ("a\n" * (4 * 1024 * 1024))[: 8 * 1024 * 1024]
        started = time.monotonic()
        self.assertIsNone(prohibited_text_reason(line_folds))
        self.assertLess(time.monotonic() - started, 10.0)

        spaces = " " * (8 * 1024 * 1024)
        started = time.monotonic()
        self.assertIsNone(prohibited_text_reason(spaces))
        self.assertLess(time.monotonic() - started, 10.0)

        continuations = ("a\\\n" * (8 * 1024 * 1024 // 3 + 1))[
            : 8 * 1024 * 1024
        ]
        started = time.monotonic()
        self.assertIsNone(prohibited_text_reason(continuations))
        self.assertLess(time.monotonic() - started, 10.0)

        escaped_quotes = "{" + '\\"' * ((8 * 1024 * 1024 - 1) // 2)
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(escaped_quotes), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        unclosed_comments = "{" + "name/*" * ((8 * 1024 * 1024 - 1) // 6)
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(unclosed_comments), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        dense_malformed_tokens = "{" + ("a " * (4 * 1024 * 1024 - 1)) + "}"
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(dense_malformed_tokens), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        sequential_frames = "{" + "{}" * 4_097 + "}"
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(sequential_frames), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        cpe_unit = "cpe:2.3:a:x:x:1:*:*:*:*:*:*:* "
        dense_cpe = (cpe_unit * (MAX_PRIVACY_TEXT_BYTES // len(cpe_unit) + 1))[
            :MAX_PRIVACY_TEXT_BYTES
        ]
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(dense_cpe), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        over_raw_bound = "a" * (16 * 1024 * 1024) + "\n"
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(over_raw_bound), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        aggregate_json = json.dumps(
            {
                "left": "a" * (4 * 1024 * 1024),
                "right": "b" * (4 * 1024 * 1024),
            },
            separators=(",", ":"),
        )
        started = time.monotonic()
        self.assertGreater(len(aggregate_json), 8 * 1024 * 1024)
        self.assertEqual(prohibited_text_reason(aggregate_json), "sensitive")
        self.assertLess(time.monotonic() - started, 10.0)

        over_utf8_bound = "£" * (4 * 1024 * 1024 + 1)
        over_utf8_bytes = over_utf8_bound.encode("utf-8")
        started = time.monotonic()
        self.assertLess(len(over_utf8_bound), 8 * 1024 * 1024)
        self.assertGreater(len(over_utf8_bytes), 8 * 1024 * 1024)
        self.assertEqual(prohibited_text_reason(over_utf8_bound), "sensitive")
        with self.assertRaisesRegex(ValueError, "prohibited sensitive"):
            assert_no_private_text(over_utf8_bytes, "fixture")
        self.assertLess(time.monotonic() - started, 10.0)

        encoded_run = "%41" * (MAX_PRIVACY_TEXT_BYTES // 3)
        started = time.monotonic()
        self.assertEqual(
            prohibited_json_reason({"safe": encoded_run}),
            "sensitive",
        )
        self.assertLess(time.monotonic() - started, 10.0)

        long_traversal = "/" + "a/" * (8 * 1024 * 1024 // 2 - 8) + "../private"
        started = time.monotonic()
        self.assertEqual(prohibited_text_reason(long_traversal), "private-path")
        self.assertLess(time.monotonic() - started, 10.0)

    def test_acceptance_binding_rejects_coordinated_runtime_mutations(self) -> None:
        source = {
            "repository": "chris-page-gov/gis-ai-go",
            "revision": "a" * 40,
            "version": "0.1.0",
            "created": "2026-08-21T00:00:00Z",
            "source_date_epoch": 1_787_270_400,
            "clean": True,
        }
        manifest_digest = "sha256:" + "b" * 64
        loaded_image_id = manifest_digest
        receipt = {
            "source": source,
            "build": {
                "platform": "linux/amd64",
                "buildx_version": "v0.35.0",
                "buildkit_version": "v0.32.2",
            },
            "image": {
                "archive_sha256": "d" * 64,
                "manifest_digest": manifest_digest,
                "config_digest": "sha256:" + "e" * 64,
            },
        }
        acceptance = {
            "classification": "local-mechanism-rehearsal",
            "source": {
                "repository": source["repository"],
                "revision": source["revision"],
                "version": source["version"],
                "created": source["created"],
                "source_date_epoch": source["source_date_epoch"],
                "tree_clean": source["clean"],
            },
            "image": {
                "archive_sha256": receipt["image"]["archive_sha256"],
                "manifest_digest": manifest_digest,
                "config_digest": receipt["image"]["config_digest"],
                "platform": "linux/amd64",
                "tag": "gis-ai-go-gateway:deploy-207-" + "a" * 12,
                "loaded_image_descriptor": {
                    "media_type": "application/vnd.oci.image.manifest.v1+json",
                    "digest": manifest_digest,
                    "bytes": 1_000,
                },
                "loaded_image_id": loaded_image_id,
                "restored_image_id": loaded_image_id,
            },
            "compose": {
                "file": "deploy/gateway/compose.candidate.yaml",
                "file_sha256": sha256_file(COMPOSE_FILE),
            },
            "engine": {"compose": {"version": "v5.3.1"}},
            "runtime": {
                "container": {
                    "image_id": loaded_image_id,
                    "labels": {"image": loaded_image_id, "version": "5.3.1"},
                },
                "network": {"labels": {"version": "5.3.1"}},
                "volumes": [
                    {"labels": {"version": "5.3.1"}},
                    {"labels": {"version": "5.3.1"}},
                ],
            },
            "boundary": {
                "health": {
                    "catalogue": {
                        "revision": source["revision"],
                        "version": source["version"],
                        "content_root_sha256": "f" * 64,
                        "record_count": 36,
                    }
                }
            },
            "claims": {
                "public_deployment": False,
                "production_activation": False,
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            okf = root / "artifacts" / "okf"
            okf.mkdir(parents=True)
            (okf / "build-receipt.json").write_bytes(
                canonical_json_bytes(
                    {
                        "revision": source["revision"],
                        "version": source["version"],
                        "contentRootSha256": "f" * 64,
                        "recordCount": 36,
                    }
                )
            )
            with mock.patch("verify_gateway_image_evidence.ROOT", root):
                _verify_acceptance_bindings(acceptance, receipt)
                mutations = [
                    lambda value: value["source"].update({"source_date_epoch": 1}),
                    lambda value: value["image"].update(
                        {"restored_image_id": "sha256:" + "9" * 64}
                    ),
                    lambda value: value["runtime"]["container"].update(
                        {"image_id": "sha256:" + "9" * 64}
                    ),
                    lambda value: (
                        value["image"].update(
                            {
                                "loaded_image_id": "sha256:" + "9" * 64,
                                "restored_image_id": "sha256:" + "9" * 64,
                            }
                        ),
                        value["runtime"]["container"].update(
                            {"image_id": "sha256:" + "9" * 64}
                        ),
                        value["runtime"]["container"]["labels"].update(
                            {"image": "sha256:" + "9" * 64}
                        ),
                    ),
                    lambda value: value["runtime"]["network"]["labels"].update(
                        {"version": "9.9.9"}
                    ),
                    lambda value: value["boundary"]["health"]["catalogue"].update(
                        {"content_root_sha256": "9" * 64}
                    ),
                    lambda value: value["claims"].update(
                        {"production_activation": True}
                    ),
                ]
                for mutation in mutations:
                    altered = json.loads(canonical_json_bytes(acceptance))
                    mutation(altered)
                    with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                        _verify_acceptance_bindings(altered, receipt)

        tool_manifest = {
            "tool_versions": {
                "docker_client": "29.6.2",
                "docker_server": "29.6.2",
                "compose": "v5.3.1",
                "buildx": "v0.35.0",
                "buildkit": "v0.32.2",
                "syft": "1.42.2",
                "trivy": "0.74.0",
            }
        }
        tool_acceptance = {
            "engine": {
                "client": {"version": "29.6.2"},
                "server": {"version": "29.6.2"},
                "compose": {"version": "v5.3.1"},
            }
        }
        tool_scan = {"scanner": {"version": "0.74.0"}}
        _verify_tool_version_bindings(
            tool_manifest, receipt, tool_scan, tool_acceptance
        )
        tool_manifest["tool_versions"]["buildx"] = "v9.9.9"
        with self.assertRaises(ValueError):
            _verify_tool_version_bindings(
                tool_manifest, receipt, tool_scan, tool_acceptance
            )


class GatewayComposeAcceptanceTests(unittest.TestCase):
    def test_acceptance_schema_is_closed_and_well_formed(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "gateway-container-acceptance.schema.json").read_bytes()
        )
        Draft202012Validator.check_schema(schema)
        self.assertIs(schema["additionalProperties"], False)
        for definition in schema["$defs"].values():
            if definition.get("type") == "object":
                self.assertIs(definition.get("additionalProperties"), False)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertTrue(list(validator.iter_errors({})))
        self.assertTrue(
            list(
                validator.iter_errors(
                    {
                        "schema": "gis-ai-go.gateway-container-acceptance.v1",
                        "classification": "local-mechanism-rehearsal",
                        "unexpected": True,
                    }
                )
            )
        )

    def test_rendered_compose_rejects_every_static_shape_mutation(self) -> None:
        project = "gis-ai-go-deploy207-test"
        image = "gis-ai-go-gateway:deploy-207-" + "a" * 12
        rendered = expected_rendered_compose(project, image)
        self.assertRegex(
            validate_rendered_compose(rendered, project, image), r"^[0-9a-f]{64}$"
        )
        mutations = []
        for key, value in (
            ("environment", {"UNREVIEWED": "1"}),
            ("command", ["sh"]),
            ("tmpfs", ["/tmp:rw"]),
        ):
            changed = json.loads(canonical_json_bytes(rendered))
            changed["services"]["gateway"][key] = value
            mutations.append(changed)
        changed = json.loads(canonical_json_bytes(rendered))
        changed["networks"]["offline"]["internal"] = False
        mutations.append(changed)
        changed = json.loads(canonical_json_bytes(rendered))
        changed["volumes"].pop("reconciliation-index")
        mutations.append(changed)
        changed = json.loads(canonical_json_bytes(rendered))
        changed["services"]["unexpected"] = {}
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed):
                with self.assertRaises(AssertionError):
                    validate_rendered_compose(changed, project, image)

    def test_transport_classifier_accepts_only_two_reviewed_modes(self) -> None:
        host = classify_transport({
            "8787/tcp": [{"HostIp": "127.0.0.1", "HostPort": "8787"}]
        })
        self.assertEqual(host["mode"], "host-loopback")
        self.assertTrue(host["host_reachable"])
        fallbacks = (
            classify_transport({"8787/tcp": []}),
            classify_transport({"8787/tcp": None}),
        )
        self.assertEqual(fallbacks[0], fallbacks[1])
        transport_schema = json.loads(
            (ROOT / "schemas" / "gateway-container-acceptance.schema.json").read_bytes()
        )["properties"]["transport"]
        transport_validator = Draft202012Validator(transport_schema)
        transport_validator.validate(host)
        for fallback in fallbacks:
            self.assertEqual(
                fallback["mode"], "container-loopback-internal-engine-fallback"
            )
            self.assertEqual(fallback["realised"], [])
            self.assertFalse(fallback["host_reachable"])
            transport_validator.validate(fallback)
        for port_map in (
            None,
            {},
            {"9999/tcp": None},
            {"8787/tcp": None, "9999/tcp": None},
            {"8787/udp": []},
            {"8787/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8787"}]},
            {"8787/tcp": [{"HostIp": "::", "HostPort": "8787"}]},
            {"8787/tcp": [{"HostIp": "::1", "HostPort": "8787"}]},
            {"8787/tcp": [{"HostIp": "127.0.0.1", "HostPort": "8788"}]},
            {"8787/tcp": [{"HostIp": "127.0.0.1", "HostPort": 8787}]},
            {"8787/tcp": [{
                "HostIp": "127.0.0.1", "HostPort": "8787", "Extra": "value"
            }]},
            {"8787/tcp": [
                {"HostIp": "127.0.0.1", "HostPort": "8787"},
                {"HostIp": "127.0.0.1", "HostPort": "8787"},
            ]},
        ):
            with self.subTest(port_map=port_map):
                with self.assertRaises(AssertionError):
                    classify_transport(port_map)

    def test_acceptance_privacy_gate_checks_the_generated_document(self) -> None:
        source = (ROOT / "scripts" / "check_gateway_container.py").read_text()
        self.assertIn(
            'assert_no_private_json(evidence, "gateway container acceptance receipt")',
            source,
        )
        self.assertNotIn(
            'assert_no_private_json(receipt, "gateway container acceptance receipt")',
            source,
        )

    def test_host_unreachable_requires_refusal_for_the_whole_interval(self) -> None:
        with (
            mock.patch(
                "check_gateway_container.socket.create_connection",
                side_effect=[
                    ConnectionRefusedError("closed"),
                    ConnectionRefusedError("closed"),
                    ConnectionRefusedError("closed"),
                ],
            ) as connect_probe,
            mock.patch(
                "check_gateway_container.time.monotonic",
                side_effect=[0.0, 0.4, 0.8, 1.1],
            ),
            mock.patch("check_gateway_container.time.sleep"),
        ):
            assert_host_unreachable(1.0)
        self.assertEqual(connect_probe.call_count, 3)
        connect_probe.assert_called_with(("127.0.0.1", 8787), timeout=0.5)

        accepted = mock.Mock()
        with mock.patch(
            "check_gateway_container.socket.create_connection", return_value=accepted
        ):
            with self.assertRaisesRegex(AssertionError, "became reachable"):
                assert_host_unreachable(1.0)
        accepted.close.assert_called_once_with()

        for error in (
            ConnectionResetError("reset"),
            TimeoutError("timed out"),
            OSError("unexpected socket failure"),
        ):
            with self.subTest(error=type(error).__name__):
                with mock.patch(
                    "check_gateway_container.socket.create_connection",
                    side_effect=error,
                ):
                    with self.assertRaisesRegex(
                        AssertionError, "did not receive a refusal"
                    ) as raised:
                        assert_host_unreachable(1.0)
                self.assertIsNone(raised.exception.__cause__)

    def test_restart_transport_must_remain_semantically_identical(self) -> None:
        fallback = classify_transport({"8787/tcp": []})
        with mock.patch(
            "check_gateway_container.assert_host_unreachable"
        ) as host_probe:
            actual = assert_transport_unchanged(
                {"NetworkSettings": {"Ports": {"8787/tcp": None}}}, fallback
            )
        self.assertEqual(actual, fallback)
        host_probe.assert_called_once_with()

        host = classify_transport({
            "8787/tcp": [{"HostIp": "127.0.0.1", "HostPort": "8787"}]
        })
        with self.assertRaisesRegex(AssertionError, "changed after restart"):
            assert_transport_unchanged(
                {"NetworkSettings": {"Ports": {"8787/tcp": None}}}, host
            )
        for inspection in (None, {}, {"NetworkSettings": {}}, {"NetworkSettings": {
            "Ports": {"8787/tcp": None, "9999/tcp": None}
        }}):
            with self.subTest(inspection=inspection):
                with self.assertRaises(AssertionError):
                    assert_transport_unchanged(inspection, fallback)

    def test_runtime_labels_are_exact_and_path_safe_after_normalisation(self) -> None:
        project = "gis-ai-go-deploy207-test"
        image_id = "sha256:" + "a" * 64
        image_labels = {
            "io.gis-ai-go.lifecycle": "candidate-blocked",
            "io.gis-ai-go.active-tools": "[]",
        }
        compose_labels = {
            "com.docker.compose.config-hash": "b" * 64,
            "com.docker.compose.container-number": "1",
            "com.docker.compose.depends_on": "",
            "com.docker.compose.image": image_id,
            "com.docker.compose.oneoff": "False",
            "com.docker.compose.project": project,
            "com.docker.compose.project.config_files": str(COMPOSE_FILE),
            "com.docker.compose.project.working_dir": str(COMPOSE_FILE.parent),
            "com.docker.compose.service": "gateway",
            "com.docker.compose.version": "5.3.1",
        }
        labels = {**image_labels, **compose_labels}
        normalised = normalise_container_labels(
            labels,
            image_labels=image_labels,
            project=project,
            image_id=image_id,
            compose_version="v5.3.1",
        )
        self.assertEqual(normalised["project"], "ephemeral-project")
        self.assertEqual(
            normalised["project_config_file"],
            "deploy/gateway/compose.candidate.yaml",
        )
        self.assertNotIn(str(ROOT), json.dumps(normalised))
        mutations = []
        for key, value in (
            ("com.docker.compose.project", "another-project"),
            ("com.docker.compose.image", "sha256:" + "c" * 64),
            ("com.docker.compose.project.config_files", "/private/tmp/other.yaml"),
        ):
            changed = dict(labels)
            changed[key] = value
            mutations.append(changed)
        changed = dict(labels)
        changed["com.docker.compose.unexpected"] = "true"
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed):
                with self.assertRaises(AssertionError):
                    normalise_container_labels(
                        changed,
                        image_labels=image_labels,
                        project=project,
                        image_id=image_id,
                        compose_version="v5.3.1",
                    )

    def test_network_and_volume_labels_require_project_ownership(self) -> None:
        project = "gis-ai-go-deploy207-test"
        labels = {
            "com.docker.compose.config-hash": "b" * 64,
            "com.docker.compose.project": project,
            "com.docker.compose.version": "5.3.1",
            "com.docker.compose.volume": "evidence-ledger",
        }
        normalised = normalise_resource_labels(
            labels,
            project=project,
            compose_version="v5.3.1",
            resource_kind="volume",
            logical_name="evidence-ledger",
        )
        self.assertEqual(normalised["volume"], "evidence-ledger")
        changed = dict(labels)
        changed["com.docker.compose.project"] = "unowned"
        with self.assertRaises(AssertionError):
            normalise_resource_labels(
                changed,
                project=project,
                compose_version="v5.3.1",
                resource_kind="volume",
                logical_name="evidence-ledger",
            )


if __name__ == "__main__":
    unittest.main()
