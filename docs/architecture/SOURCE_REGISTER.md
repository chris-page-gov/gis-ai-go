# Source coverage register

Immutable review baseline: `97bc45635a91064cd78f06bf0848ad7636f05439`.

The tree contains **32,138 tracked files**. The register below identifies **484 code, presentation, migration, launcher and CI files** (**204,809 lines**): **479 project-authored files** and **5 pinned vendor files**. Vendor code is a dependency boundary, not a local refactoring target.

Every listed file received inventory and structural/reference coverage. Component chapters describe the implementation and boundary traces; [the review](REVIEW.md) records depth and limitations. A row is not a claim that every line received a manual semantic audit. Generated/imported knowledge records, immutable research and third-party material remain data/evidence: their inventory does not establish semantic completeness.

The inventory is derived from Git objects, so later inline comments cannot shift these references. Counts describe the baseline, not documentation added by this review. Reproduce with `python3 scripts/review_architecture.py --write`; check with `python3 scripts/review_architecture.py --check`.

## Complete top-level inventory

| Tree or root file | Tracked files |
| --- | ---: |
| `.dockerignore` | 1 |
| `.editorconfig` | 1 |
| `.gitattributes` | 1 |
| `.github` | 9 |
| `.gitignore` | 1 |
| `.nvmrc` | 1 |
| `AGENTS.md` | 1 |
| `CHANGELOG.md` | 1 |
| `CODE_OF_CONDUCT.md` | 1 |
| `CONTEXT.md` | 1 |
| `CONTRIBUTING.md` | 1 |
| `GOVERNANCE.md` | 1 |
| `LICENSE` | 1 |
| `PROGRESS.md` | 1 |
| `README.md` | 1 |
| `RELEASE_NOTES` | 1 |
| `SECURITY.md` | 1 |
| `THIRD_PARTY.md` | 1 |
| `VERSION` | 1 |
| `apps` | 182 |
| `architecture` | 19 |
| `changelog.d` | 105 |
| `deploy` | 2 |
| `docs` | 354 |
| `evaluation` | 12 |
| `infra` | 2 |
| `okf` | 14 |
| `okf-plus` | 30,888 |
| `package.json` | 1 |
| `packages` | 120 |
| `pnpm-lock.yaml` | 1 |
| `pnpm-workspace.yaml` | 1 |
| `policies` | 1 |
| `profiles` | 3 |
| `providers` | 38 |
| `pyproject.toml` | 1 |
| `schemas` | 103 |
| `scripts` | 107 |
| `services` | 17 |
| `sites` | 9 |
| `tests` | 128 |
| `tsconfig.base.json` | 1 |
| `uv.lock` | 1 |
| `workflows` | 1 |

## Build and operations

| Source at review baseline | Lines | Role |
| --- | ---: | --- |
| [.github/workflows/ci.yml](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/workflows/ci.yml#L1-L646) | 646 | build, operator or assurance tooling |
| [.github/workflows/pages.yml](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/workflows/pages.yml#L1-L489) | 489 | build, operator or assurance tooling |
| [scripts/build_chronicle.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/build_chronicle.py#L1-L436) | 436 | build, operator or assurance tooling |
| [scripts/build_local214_guide.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/build_local214_guide.py#L1-L256) | 256 | build, operator or assurance tooling |
| [scripts/build_okf.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/build_okf.py#L1-L1537) | 1,537 | build, operator or assurance tooling |
| [scripts/capture_delivery_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L1-L7873) | 7,873 | build, operator or assurance tooling |
| [scripts/check_changelog_fragments.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_changelog_fragments.py#L1-L152) | 152 | build, operator or assurance tooling |
| [scripts/check_evidence_checkpoint.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_evidence_checkpoint.mjs#L1-L82) | 82 | build, operator or assurance tooling |
| [scripts/check_evidence_filesystem_capabilities.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_evidence_filesystem_capabilities.mjs#L1-L289) | 289 | build, operator or assurance tooling |
| [scripts/check_execution_container.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_execution_container.py#L1-L118) | 118 | build, operator or assurance tooling |
| [scripts/check_gateway_container.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_gateway_container.py#L1-L1441) | 1,441 | build, operator or assurance tooling |
| [scripts/check_gateway_image_reproducibility.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_gateway_image_reproducibility.py#L1-L62) | 62 | build, operator or assurance tooling |
| [scripts/check_links.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_links.py#L1-L142) | 142 | build, operator or assurance tooling |
| [scripts/check_local214_profile.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_local214_profile.py#L1-L70) | 70 | build, operator or assurance tooling |
| [scripts/check_public_read_v2.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_public_read_v2.mjs#L1-L559) | 559 | build, operator or assurance tooling |
| [scripts/check_release_reproducibility.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_release_reproducibility.py#L1-L393) | 393 | build, operator or assurance tooling |
| [scripts/check_versions.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_versions.py#L1-L159) | 159 | build, operator or assurance tooling |
| [scripts/codex_key_quarantine.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/codex_key_quarantine.py#L1-L247) | 247 | build, operator or assurance tooling |
| [scripts/compile_qual_206_strict_modern_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/compile_qual_206_strict_modern_evidence.py#L1-L1117) | 1,117 | build, operator or assurance tooling |
| [scripts/create_evidence_checkpoint.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/create_evidence_checkpoint.mjs#L1-L40) | 40 | build, operator or assurance tooling |
| [scripts/evidence_checkpoint_operator_common.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/evidence_checkpoint_operator_common.mjs#L1-L126) | 126 | build, operator or assurance tooling |
| [scripts/evidence_checkpoint_rehearsal_fixture_writer.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/evidence_checkpoint_rehearsal_fixture_writer.mjs#L1-L52) | 52 | build, operator or assurance tooling |
| [scripts/finalise_qual_206_chatgpt_tunnel_exact_five.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/finalise_qual_206_chatgpt_tunnel_exact_five.py#L1-L241) | 241 | build, operator or assurance tooling |
| [scripts/gateway_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_evidence.py#L1-L191) | 191 | build, operator or assurance tooling |
| [scripts/gateway_image.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L1-L6155) | 6,155 | build, operator or assurance tooling |
| [scripts/generate_gateway_image_sbom.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/generate_gateway_image_sbom.py#L1-L181) | 181 | build, operator or assurance tooling |
| [scripts/generate_sbom.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/generate_sbom.py#L1-L234) | 234 | build, operator or assurance tooling |
| [scripts/index_recovered_delivery_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/index_recovered_delivery_evidence.py#L1-L1610) | 1,610 | build, operator or assurance tooling |
| [scripts/local214_demo.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/local214_demo.mjs#L1-L259) | 259 | build, operator or assurance tooling |
| [scripts/local214_package.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/local214_package.py#L1-L306) | 306 | build, operator or assurance tooling |
| [scripts/node_runtime_advisory.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/node_runtime_advisory.py#L1-L1599) | 1,599 | build, operator or assurance tooling |
| [scripts/package_gateway_oci.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_gateway_oci.py#L1-L79) | 79 | build, operator or assurance tooling |
| [scripts/package_pages.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_pages.py#L1-L550) | 550 | build, operator or assurance tooling |
| [scripts/package_web216_hosted_runtime.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_web216_hosted_runtime.mjs#L1-L200) | 200 | build, operator or assurance tooling |
| [scripts/plan_ci_impact.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/plan_ci_impact.py#L1-L635) | 635 | build, operator or assurance tooling |
| [scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs#L1-L1248) | 1,248 | build, operator or assurance tooling |
| [scripts/qual_206_chatgpt_tunnel_exact_five_observer.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_chatgpt_tunnel_exact_five_observer.mjs#L1-L1711) | 1,711 | build, operator or assurance tooling |
| [scripts/qual_206_claude_capability_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_claude_capability_harness.mjs#L1-L1892) | 1,892 | build, operator or assurance tooling |
| [scripts/qual_206_claude_exact_five_capability_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_claude_exact_five_capability_harness.mjs#L1-L62) | 62 | build, operator or assurance tooling |
| [scripts/qual_206_claude_runtime_closure.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_claude_runtime_closure.mjs#L1-L531) | 531 | build, operator or assurance tooling |
| [scripts/qual_206_claude_stdio_observer.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_claude_stdio_observer.mjs#L1-L2478) | 2,478 | build, operator or assurance tooling |
| [scripts/qual_206_conformance_server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_conformance_server.mjs#L1-L61) | 61 | build, operator or assurance tooling |
| [scripts/qual_206_exact_five_event_collector.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_exact_five_event_collector.mjs#L1-L2341) | 2,341 | build, operator or assurance tooling |
| [scripts/qual_206_legacy_conformance_server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_legacy_conformance_server.mjs#L1-L70) | 70 | build, operator or assurance tooling |
| [scripts/qual_206_local_demo.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_local_demo.mjs#L1-L959) | 959 | build, operator or assurance tooling |
| [scripts/qual_206_local_evaluations.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_local_evaluations.mjs#L1-L796) | 796 | build, operator or assurance tooling |
| [scripts/qual_206_local_http_preflight.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_local_http_preflight.mjs#L1-L1070) | 1,070 | build, operator or assurance tooling |
| [scripts/qual_206_strict_modern_identity.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_strict_modern_identity.mjs#L1-L47) | 47 | build, operator or assurance tooling |
| [scripts/qual_206_telemetry_proxy.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_telemetry_proxy.mjs#L1-L281) | 281 | build, operator or assurance tooling |
| [scripts/qual_206_validate_local_http_schemas.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_validate_local_http_schemas.mjs#L1-L47) | 47 | build, operator or assurance tooling |
| [scripts/qual_206_verify_local_http_preflight.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/qual_206_verify_local_http_preflight.py#L1-L1826) | 1,826 | build, operator or assurance tooling |
| [scripts/reconcile_evidence_checkpoint_publication.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/reconcile_evidence_checkpoint_publication.mjs#L1-L81) | 81 | build, operator or assurance tooling |
| [scripts/rehearse_evidence_checkpoint_recovery.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/rehearse_evidence_checkpoint_recovery.mjs#L1-L237) | 237 | build, operator or assurance tooling |
| [scripts/render_diagrams.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/render_diagrams.mjs#L1-L86) | 86 | build, operator or assurance tooling |
| [scripts/restore_evidence_checkpoint.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/restore_evidence_checkpoint.mjs#L1-L40) | 40 | build, operator or assurance tooling |
| [scripts/run_gateway_image_assurance.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/run_gateway_image_assurance.py#L1-L580) | 580 | build, operator or assurance tooling |
| [scripts/scan_gateway_image.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/scan_gateway_image.py#L1-L2297) | 2,297 | build, operator or assurance tooling |
| [scripts/scan_secrets.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/scan_secrets.py#L1-L65) | 65 | build, operator or assurance tooling |
| [scripts/stage_pages_payload.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/stage_pages_payload.py#L1-L466) | 466 | build, operator or assurance tooling |
| [scripts/start-local-candidate](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/start-local-candidate#L1-L46) | 46 | build, operator or assurance tooling |
| [scripts/start-public-data-workbench](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/start-public-data-workbench#L1-L11) | 11 | build, operator or assurance tooling |
| [scripts/validate_contracts.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/validate_contracts.py#L1-L1167) | 1,167 | build, operator or assurance tooling |
| [scripts/verify_delivery_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_delivery_evidence.py#L1-L4376) | 4,376 | build, operator or assurance tooling |
| [scripts/verify_deployment_admission.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_deployment_admission.py#L1-L551) | 551 | build, operator or assurance tooling |
| [scripts/verify_gateway_image_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_gateway_image_evidence.py#L1-L617) | 617 | build, operator or assurance tooling |
| [scripts/verify_gateway_oci.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_gateway_oci.py#L1-L140) | 140 | build, operator or assurance tooling |
| [scripts/verify_gateway_provenance.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_gateway_provenance.py#L1-L645) | 645 | build, operator or assurance tooling |
| [scripts/verify_pages_archive.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_pages_archive.py#L1-L683) | 683 | build, operator or assurance tooling |
| [scripts/verify_qual_206_chatgpt_tunnel_exact_five.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_chatgpt_tunnel_exact_five.py#L1-L1359) | 1,359 | build, operator or assurance tooling |
| [scripts/verify_qual_206_chatgpt_tunnel_exact_five_results.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_chatgpt_tunnel_exact_five_results.mjs#L1-L337) | 337 | build, operator or assurance tooling |
| [scripts/verify_qual_206_claude_capability.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_claude_capability.py#L1-L1449) | 1,449 | build, operator or assurance tooling |
| [scripts/verify_qual_206_claude_composite_observation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_claude_composite_observation.py#L1-L1314) | 1,314 | build, operator or assurance tooling |
| [scripts/verify_qual_206_claude_exact_five_capability.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_claude_exact_five_capability.py#L1-L1408) | 1,408 | build, operator or assurance tooling |
| [scripts/verify_qual_206_claude_exact_five_results.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_claude_exact_five_results.mjs#L1-L403) | 403 | build, operator or assurance tooling |
| [scripts/verify_qual_206_strict_modern_host_events.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_strict_modern_host_events.py#L1-L943) | 943 | build, operator or assurance tooling |
| [scripts/web216_build_workbench_data.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_build_workbench_data.py#L1-L19) | 19 | build, operator or assurance tooling |
| [scripts/web216_corpus.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_corpus.py#L1-L348) | 348 | build, operator or assurance tooling |
| [scripts/web216_current_cpih.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_current_cpih.py#L1-L218) | 218 | build, operator or assurance tooling |
| [scripts/web216_experiments.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_experiments.py#L1-L240) | 240 | build, operator or assurance tooling |
| [scripts/web216_geography_contract.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_geography_contract.py#L1-L389) | 389 | build, operator or assurance tooling |
| [scripts/web216_hosted_cpih_bundle_entry.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_hosted_cpih_bundle_entry.ts#L1-L8) | 8 | build, operator or assurance tooling |
| [scripts/web216_storage_experiment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_storage_experiment.py#L1-L290) | 290 | build, operator or assurance tooling |
| [scripts/web216_worker_mcp_fixture.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_worker_mcp_fixture.ts#L1-L79) | 79 | build, operator or assurance tooling |
| [scripts/web216_worker_mcp_probe.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_worker_mcp_probe.mjs#L1-L342) | 342 | build, operator or assurance tooling |
| [scripts/web216_worker_storage_fixture.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_worker_storage_fixture.ts#L1-L57) | 57 | build, operator or assurance tooling |
| [scripts/web216_worker_storage_probe.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/web216_worker_storage_probe.mjs#L1-L145) | 145 | build, operator or assurance tooling |
| [tests/__init__.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/__init__.py#L1-L1) | 1 | test or test fixture |
| [tests/contract/__init__.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/__init__.py#L1-L1) | 1 | test or test fixture |
| [tests/contract/test_catalogue_api_schemas.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_catalogue_api_schemas.py#L1-L437) | 437 | test or test fixture |
| [tests/contract/test_changelog_fragments.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_changelog_fragments.py#L1-L98) | 98 | test or test fixture |
| [tests/contract/test_chronicle_builder.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_chronicle_builder.py#L1-L166) | 166 | test or test fixture |
| [tests/contract/test_ci_impact_plan.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_ci_impact_plan.py#L1-L686) | 686 | test or test fixture |
| [tests/contract/test_ci_okf_plus_evidence_privacy.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_ci_okf_plus_evidence_privacy.py#L1-L31) | 31 | test or test fixture |
| [tests/contract/test_claude_retrospective.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_claude_retrospective.py#L1-L109) | 109 | test or test fixture |
| [tests/contract/test_codex_key_quarantine.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_codex_key_quarantine.py#L1-L265) | 265 | test or test fixture |
| [tests/contract/test_data_query_contracts.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_data_query_contracts.py#L1-L340) | 340 | test or test fixture |
| [tests/contract/test_delivery_evidence_preservation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_delivery_evidence_preservation.py#L1-L9514) | 9,514 | test or test fixture |
| [tests/contract/test_deployment_admission.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_deployment_admission.py#L1-L667) | 667 | test or test fixture |
| [tests/contract/test_evidence_checkpoint_contracts.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_evidence_checkpoint_contracts.py#L1-L435) | 435 | test or test fixture |
| [tests/contract/test_evidence_schemas.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_evidence_schemas.py#L1-L994) | 994 | test or test fixture |
| [tests/contract/test_execution_schemas.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_execution_schemas.py#L1-L189) | 189 | test or test fixture |
| [tests/contract/test_gateway_container_diagnostics.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_gateway_container_diagnostics.py#L1-L389) | 389 | test or test fixture |
| [tests/contract/test_gateway_image_assurance.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_gateway_image_assurance.py#L1-L946) | 946 | test or test fixture |
| [tests/contract/test_gateway_image_contract.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_gateway_image_contract.py#L1-L5993) | 5,993 | test or test fixture |
| [tests/contract/test_gateway_oci_compatibility.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_gateway_oci_compatibility.py#L1-L365) | 365 | test or test fixture |
| [tests/contract/test_gateway_provenance.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_gateway_provenance.py#L1-L532) | 532 | test or test fixture |
| [tests/contract/test_local214_guide.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_local214_guide.py#L1-L60) | 60 | test or test fixture |
| [tests/contract/test_local214_profile.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_local214_profile.py#L1-L77) | 77 | test or test fixture |
| [tests/contract/test_node_runtime_advisory.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_node_runtime_advisory.py#L1-L1112) | 1,112 | test or test fixture |
| [tests/contract/test_okf_bundle.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_bundle.py#L1-L848) | 848 | test or test fixture |
| [tests/contract/test_okf_plus_build.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_build.py#L1-L486) | 486 | test or test fixture |
| [tests/contract/test_okf_plus_context.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_context.py#L1-L155) | 155 | test or test fixture |
| [tests/contract/test_okf_plus_export.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_export.py#L1-L221) | 221 | test or test fixture |
| [tests/contract/test_okf_plus_export_documents.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_export_documents.py#L1-L106) | 106 | test or test fixture |
| [tests/contract/test_okf_plus_model.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_model.py#L1-L55) | 55 | test or test fixture |
| [tests/contract/test_okf_plus_search.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_search.py#L1-L253) | 253 | test or test fixture |
| [tests/contract/test_okf_plus_time_table.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_time_table.py#L1-L25) | 25 | test or test fixture |
| [tests/contract/test_okf_plus_verify.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_okf_plus_verify.py#L1-L172) | 172 | test or test fixture |
| [tests/contract/test_pages_publication.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_pages_publication.py#L1-L440) | 440 | test or test fixture |
| [tests/contract/test_pages_staging.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_pages_staging.py#L1-L306) | 306 | test or test fixture |
| [tests/contract/test_pages_workflows.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_pages_workflows.py#L1-L888) | 888 | test or test fixture |
| [tests/contract/test_qual_206_chatgpt_tunnel_exact_five.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_chatgpt_tunnel_exact_five.py#L1-L1630) | 1,630 | test or test fixture |
| [tests/contract/test_qual_206_claude_capability.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_capability.py#L1-L1145) | 1,145 | test or test fixture |
| [tests/contract/test_qual_206_claude_code_stdio_observation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_code_stdio_observation.py#L1-L530) | 530 | test or test fixture |
| [tests/contract/test_qual_206_claude_composite_observation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_composite_observation.py#L1-L822) | 822 | test or test fixture |
| [tests/contract/test_qual_206_claude_composite_stdio_readiness.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_composite_stdio_readiness.py#L1-L373) | 373 | test or test fixture |
| [tests/contract/test_qual_206_claude_composite_stdio_readiness_v2.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_composite_stdio_readiness_v2.py#L1-L373) | 373 | test or test fixture |
| [tests/contract/test_qual_206_claude_exact_five_capability.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_claude_exact_five_capability.py#L1-L1024) | 1,024 | test or test fixture |
| [tests/contract/test_qual_206_legacy_stdio_readiness.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_legacy_stdio_readiness.py#L1-L378) | 378 | test or test fixture |
| [tests/contract/test_qual_206_local_evaluation_receipts.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_local_evaluation_receipts.py#L1-L357) | 357 | test or test fixture |
| [tests/contract/test_qual_206_local_http_transport_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_local_http_transport_evidence.py#L1-L378) | 378 | test or test fixture |
| [tests/contract/test_qual_206_local_protocol_evidence_matrix.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_local_protocol_evidence_matrix.py#L1-L886) | 886 | test or test fixture |
| [tests/contract/test_qual_206_strict_modern_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_strict_modern_evidence.py#L1-L840) | 840 | test or test fixture |
| [tests/contract/test_qual_206_strict_modern_host_events.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_qual_206_strict_modern_host_events.py#L1-L663) | 663 | test or test fixture |
| [tests/contract/test_recovered_delivery_evidence.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_recovered_delivery_evidence.py#L1-L649) | 649 | test or test fixture |
| [tests/contract/test_release_metadata.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_release_metadata.py#L1-L249) | 249 | test or test fixture |
| [tests/contract/test_release_reproducibility.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_release_reproducibility.py#L1-L111) | 111 | test or test fixture |
| [tests/contract/test_repository_boundary.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_repository_boundary.py#L1-L109) | 109 | test or test fixture |
| [tests/contract/test_research_source_boundaries.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_research_source_boundaries.py#L1-L217) | 217 | test or test fixture |
| [tests/contract/test_secret_token_boundary.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_secret_token_boundary.py#L1-L14) | 14 | test or test fixture |
| [tests/contract/test_tool_registry.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_tool_registry.py#L1-L329) | 329 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_exact_five_stdio_server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_exact_five_stdio_server.mjs#L1-L323) | 323 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_fake_claude_capability_client.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_fake_claude_capability_client.mjs#L1-L281) | 281 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_fake_claude_exact_five_client.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_fake_claude_exact_five_client.mjs#L1-L340) | 340 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs#L1-L65) | 65 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs#L1-L385) | 385 | test or test fixture |
| [tests/interoperability/fixtures/qual_206_unresponsive_child.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/fixtures/qual_206_unresponsive_child.mjs#L1-L14) | 14 | test or test fixture |
| [tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_harness.mjs#L1-L1126) | 1,126 | test or test fixture |
| [tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_observer.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_observer.mjs#L1-L879) | 879 | test or test fixture |
| [tests/interoperability/test_qual_206_claude_capability_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_claude_capability_harness.mjs#L1-L592) | 592 | test or test fixture |
| [tests/interoperability/test_qual_206_claude_exact_five_capability_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_claude_exact_five_capability_harness.mjs#L1-L452) | 452 | test or test fixture |
| [tests/interoperability/test_qual_206_claude_stdio_observer.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_claude_stdio_observer.mjs#L1-L883) | 883 | test or test fixture |
| [tests/interoperability/test_qual_206_event_collector.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_event_collector.mjs#L1-L1144) | 1,144 | test or test fixture |
| [tests/interoperability/test_qual_206_exact_five_stdio.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_exact_five_stdio.mjs#L1-L634) | 634 | test or test fixture |
| [tests/interoperability/test_qual_206_harness.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_harness.mjs#L1-L953) | 953 | test or test fixture |
| [tests/interoperability/test_qual_206_local_demo.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_local_demo.mjs#L1-L276) | 276 | test or test fixture |
| [tests/interoperability/test_qual_206_local_http_preflight.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_local_http_preflight.mjs#L1-L473) | 473 | test or test fixture |
| [tests/interoperability/test_qual_206_local_http_preflight.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_qual_206_local_http_preflight.py#L1-L867) | 867 | test or test fixture |
| [tests/interoperability/test_sites_mcp_evaluate.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_sites_mcp_evaluate.mjs#L1-L183) | 183 | test or test fixture |
| [tests/interoperability/test_sites_native_mount.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/interoperability/test_sites_native_mount.mjs#L1-L153) | 153 | test or test fixture |
| [tests/test_experience_evaluate.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_experience_evaluate.mjs#L1-L149) | 149 | test or test fixture |
| [tests/test_local214_demo.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_local214_demo.mjs#L1-L77) | 77 | test or test fixture |
| [tests/test_local214_launcher.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_local214_launcher.py#L1-L40) | 40 | test or test fixture |
| [tests/test_local214_package.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_local214_package.py#L1-L188) | 188 | test or test fixture |
| [tests/test_okf_plus_documentation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_documentation.py#L1-L277) | 277 | test or test fixture |
| [tests/test_okf_plus_harvest.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_harvest.py#L1-L132) | 132 | test or test fixture |
| [tests/test_okf_plus_ons_catalogues.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_ons_catalogues.py#L1-L185) | 185 | test or test fixture |
| [tests/test_okf_plus_ons_enrichment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_ons_enrichment.py#L1-L313) | 313 | test or test fixture |
| [tests/test_okf_plus_os_enrichment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_os_enrichment.py#L1-L251) | 251 | test or test fixture |
| [tests/test_okf_plus_vocabulary_usage.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_okf_plus_vocabulary_usage.py#L1-L146) | 146 | test or test fixture |
| [tests/test_package_web216_hosted_runtime.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_package_web216_hosted_runtime.mjs#L1-L99) | 99 | test or test fixture |
| [tests/test_qual_206_local_http_preflight.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_qual_206_local_http_preflight.py#L1-L8) | 8 | test or test fixture |
| [tests/test_web216_corpus.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_corpus.py#L1-L301) | 301 | test or test fixture |
| [tests/test_web216_current_cpih.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_current_cpih.py#L1-L268) | 268 | test or test fixture |
| [tests/test_web216_experiments.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_experiments.py#L1-L132) | 132 | test or test fixture |
| [tests/test_web216_geography_contract.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_geography_contract.py#L1-L287) | 287 | test or test fixture |
| [tests/test_web216_hosted_packager.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_hosted_packager.py#L1-L23) | 23 | test or test fixture |
| [tests/test_web216_storage_experiment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/test_web216_storage_experiment.py#L1-L197) | 197 | test or test fixture |

## Core gateway

| Source at review baseline | Lines | Role |
| --- | ---: | --- |
| [apps/mcp-gateway/Containerfile](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/Containerfile#L1-L237) | 237 | configuration |
| [apps/mcp-gateway/src/activation.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/activation.ts#L1-L25) | 25 | application or library |
| [apps/mcp-gateway/src/bounded-json.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/bounded-json.ts#L1-L223) | 223 | application or library |
| [apps/mcp-gateway/src/candidate-activation.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/candidate-activation.ts#L1-L94) | 94 | application or library |
| [apps/mcp-gateway/src/catalogue-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-application.ts#L1-L1224) | 1,224 | application or library |
| [apps/mcp-gateway/src/catalogue-snapshot.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L1-L838) | 838 | application or library |
| [apps/mcp-gateway/src/container-healthcheck.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-healthcheck.ts#L1-L165) | 165 | application or library |
| [apps/mcp-gateway/src/container-ingress.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-ingress.ts#L1-L73) | 73 | application or library |
| [apps/mcp-gateway/src/container-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-main.ts#L1-L223) | 223 | application or library |
| [apps/mcp-gateway/src/cursor.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/cursor.ts#L1-L212) | 212 | application or library |
| [apps/mcp-gateway/src/data-query-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/data-query-application.ts#L1-L1307) | 1,307 | application or library |
| [apps/mcp-gateway/src/evidence-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/evidence-application.ts#L1-L426) | 426 | application or library |
| [apps/mcp-gateway/src/execution-envelope.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/execution-envelope.ts#L1-L407) | 407 | application or library |
| [apps/mcp-gateway/src/governed-assembly.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/governed-assembly.ts#L1-L603) | 603 | application or library |
| [apps/mcp-gateway/src/http-app.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-app.ts#L1-L808) | 808 | application or library |
| [apps/mcp-gateway/src/http-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-main.ts#L1-L31) | 31 | application or library |
| [apps/mcp-gateway/src/http-server.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-server.ts#L1-L957) | 957 | application or library |
| [apps/mcp-gateway/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/index.ts#L1-L18) | 18 | application or library |
| [apps/mcp-gateway/src/local-candidate-capability.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/local-candidate-capability.ts#L1-L88) | 88 | application or library |
| [apps/mcp-gateway/src/local-candidate-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/local-candidate-main.ts#L1-L432) | 432 | application or library |
| [apps/mcp-gateway/src/mcp-constants.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-constants.ts#L1-L4) | 4 | application or library |
| [apps/mcp-gateway/src/mcp-http-core.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-http-core.ts#L1-L389) | 389 | application or library |
| [apps/mcp-gateway/src/mcp-http.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-http.ts#L1-L67) | 67 | application or library |
| [apps/mcp-gateway/src/mcp-request-signal.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-request-signal.ts#L1-L53) | 53 | application or library |
| [apps/mcp-gateway/src/mcp-server.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-server.ts#L1-L1005) | 1,005 | application or library |
| [apps/mcp-gateway/src/mcp-stdio-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-stdio-main.ts#L1-L42) | 42 | application or library |
| [apps/mcp-gateway/src/mcp-stdio.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-stdio.ts#L1-L377) | 377 | application or library |
| [apps/mcp-gateway/src/mcp-wire-guards.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-wire-guards.ts#L1-L65) | 65 | application or library |
| [apps/mcp-gateway/src/metadata.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/metadata.ts#L1-L13) | 13 | application or library |
| [apps/mcp-gateway/src/openapi.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/openapi.ts#L1-L850) | 850 | application or library |
| [apps/mcp-gateway/src/problem.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/problem.ts#L1-L309) | 309 | application or library |
| [apps/mcp-gateway/src/public-origin.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/public-origin.ts#L1-L52) | 52 | application or library |
| [apps/mcp-gateway/src/readiness-integrity.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/readiness-integrity.ts#L1-L225) | 225 | application or library |
| [apps/mcp-gateway/src/reconciliation-applications.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/reconciliation-applications.ts#L1-L37) | 37 | application or library |
| [apps/mcp-gateway/src/selection-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/selection-application.ts#L1-L682) | 682 | application or library |
| [apps/mcp-gateway/test/candidate-activation.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/candidate-activation.test.ts#L1-L196) | 196 | test or test fixture |
| [apps/mcp-gateway/test/catalogue-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/catalogue-application.test.ts#L1-L814) | 814 | test or test fixture |
| [apps/mcp-gateway/test/catalogue-snapshot.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/catalogue-snapshot.test.ts#L1-L215) | 215 | test or test fixture |
| [apps/mcp-gateway/test/container-main.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/container-main.test.ts#L1-L248) | 248 | test or test fixture |
| [apps/mcp-gateway/test/cursor.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/cursor.test.ts#L1-L119) | 119 | test or test fixture |
| [apps/mcp-gateway/test/data-query-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/data-query-application.test.ts#L1-L1821) | 1,821 | test or test fixture |
| [apps/mcp-gateway/test/evidence-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/evidence-application.test.ts#L1-L431) | 431 | test or test fixture |
| [apps/mcp-gateway/test/evidence-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/evidence-transport.test.ts#L1-L873) | 873 | test or test fixture |
| [apps/mcp-gateway/test/execution-envelope.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/execution-envelope.test.ts#L1-L259) | 259 | test or test fixture |
| [apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs#L1-L472) | 472 | test or test fixture |
| [apps/mcp-gateway/test/governed-assembly.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/governed-assembly.test.ts#L1-L1815) | 1,815 | test or test fixture |
| [apps/mcp-gateway/test/http-app.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-app.test.ts#L1-L691) | 691 | test or test fixture |
| [apps/mcp-gateway/test/http-server-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-server-transport.test.ts#L1-L739) | 739 | test or test fixture |
| [apps/mcp-gateway/test/http-server.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-server.test.ts#L1-L96) | 96 | test or test fixture |
| [apps/mcp-gateway/test/index.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/index.test.ts#L1-L27) | 27 | test or test fixture |
| [apps/mcp-gateway/test/local-candidate-acceptance.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-acceptance.test.ts#L1-L733) | 733 | test or test fixture |
| [apps/mcp-gateway/test/local-candidate-launcher.acceptance.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-launcher.acceptance.ts#L1-L267) | 267 | test or test fixture |
| [apps/mcp-gateway/test/local-candidate-main.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-main.test.ts#L1-L522) | 522 | test or test fixture |
| [apps/mcp-gateway/test/mcp-http-core.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-http-core.test.ts#L1-L196) | 196 | test or test fixture |
| [apps/mcp-gateway/test/mcp-stdio.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-stdio.test.ts#L1-L1321) | 1,321 | test or test fixture |
| [apps/mcp-gateway/test/mcp-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-transport.test.ts#L1-L1206) | 1,206 | test or test fixture |
| [apps/mcp-gateway/test/public-read-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/public-read-transport.test.ts#L1-L2027) | 2,027 | test or test fixture |
| [apps/mcp-gateway/test/qual-206-exact-five-http.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-exact-five-http.test.ts#L1-L1104) | 1,104 | test or test fixture |
| [apps/mcp-gateway/test/qual-206-host-015.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-host-015.test.ts#L1-L267) | 267 | test or test fixture |
| [apps/mcp-gateway/test/qual-206-local-protocol-matrix.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-local-protocol-matrix.test.ts#L1-L355) | 355 | test or test fixture |
| [apps/mcp-gateway/test/readiness-integrity.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/readiness-integrity.test.ts#L1-L155) | 155 | test or test fixture |
| [apps/mcp-gateway/test/selection-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/selection-application.test.ts#L1-L344) | 344 | test or test fixture |

## Core packages and execution

| Source at review baseline | Lines | Role |
| --- | ---: | --- |
| [packages/authority-context/src/evidence-inspect-v3.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/authority-context/src/evidence-inspect-v3.ts#L1-L51) | 51 | application or library |
| [packages/authority-context/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/authority-context/src/index.ts#L1-L53) | 53 | application or library |
| [packages/authority-context/src/public-read-v2.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/authority-context/src/public-read-v2.ts#L1-L48) | 48 | application or library |
| [packages/authority-context/test/authority-context.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/authority-context/test/authority-context.test.ts#L1-L143) | 143 | test or test fixture |
| [packages/contracts/src/catalogue/catalogue.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/catalogue/catalogue.ts#L1-L1031) | 1,031 | application or library |
| [packages/contracts/src/catalogue/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/catalogue/index.ts#L1-L3) | 3 | application or library |
| [packages/contracts/src/catalogue/links.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/catalogue/links.ts#L1-L103) | 103 | application or library |
| [packages/contracts/src/catalogue/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/catalogue/types.ts#L1-L207) | 207 | application or library |
| [packages/contracts/src/execution/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/execution/index.ts#L1-L1) | 1 | application or library |
| [packages/contracts/src/execution/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/execution/types.ts#L1-L135) | 135 | application or library |
| [packages/contracts/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/src/index.ts#L1-L9) | 9 | application or library |
| [packages/contracts/test/catalogue.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/test/catalogue.test.ts#L1-L356) | 356 | test or test fixture |
| [packages/contracts/test/fixtures.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/test/fixtures.ts#L1-L122) | 122 | test or test fixture |
| [packages/contracts/test/links.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/contracts/test/links.test.ts#L1-L54) | 54 | test or test fixture |
| [packages/evidence/src/canonical-json.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/canonical-json.ts#L1-L254) | 254 | application or library |
| [packages/evidence/src/checkpoint-publication-test-seam.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/checkpoint-publication-test-seam.ts#L1-L53) | 53 | application or library |
| [packages/evidence/src/checkpoint.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/checkpoint.ts#L1-L2530) | 2,530 | application or library |
| [packages/evidence/src/digest.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/digest.ts#L1-L120) | 120 | application or library |
| [packages/evidence/src/evidence-inspect-receipt.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/evidence-inspect-receipt.ts#L1-L945) | 945 | application or library |
| [packages/evidence/src/idempotency-constants.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/idempotency-constants.ts#L1-L2) | 2 | application or library |
| [packages/evidence/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/index.ts#L1-L11) | 11 | application or library |
| [packages/evidence/src/public-ledger-capacity.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/public-ledger-capacity.ts#L1-L28) | 28 | application or library |
| [packages/evidence/src/public-ledger.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/public-ledger.ts#L1-L1525) | 1,525 | application or library |
| [packages/evidence/src/public-read-receipt.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/public-read-receipt.ts#L1-L2045) | 2,045 | application or library |
| [packages/evidence/src/receipt.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/receipt.ts#L1-L1746) | 1,746 | application or library |
| [packages/evidence/src/reconciliation-index-capacity.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/reconciliation-index-capacity.ts#L1-L29) | 29 | application or library |
| [packages/evidence/src/reconciliation-index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/reconciliation-index.ts#L1-L1812) | 1,812 | application or library |
| [packages/evidence/src/web216-cpih-receipt.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/web216-cpih-receipt.ts#L1-L308) | 308 | application or library |
| [packages/evidence/src/web216-pure.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/web216-pure.ts#L1-L13) | 13 | application or library |
| [packages/evidence/src/web216-transactional-contract.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/web216-transactional-contract.ts#L1-L293) | 293 | application or library |
| [packages/evidence/src/web216-transactional-d1.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/src/web216-transactional-d1.ts#L1-L174) | 174 | application or library |
| [packages/evidence/test/canonical-json.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/canonical-json.test.ts#L1-L102) | 102 | test or test fixture |
| [packages/evidence/test/checkpoint-recovery.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/checkpoint-recovery.test.ts#L1-L1740) | 1,740 | test or test fixture |
| [packages/evidence/test/digest.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/digest.test.ts#L1-L75) | 75 | test or test fixture |
| [packages/evidence/test/evidence-inspect-receipt.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/evidence-inspect-receipt.test.ts#L1-L750) | 750 | test or test fixture |
| [packages/evidence/test/fixtures.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/fixtures.ts#L1-L246) | 246 | test or test fixture |
| [packages/evidence/test/operator-checkpoint-commands.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/operator-checkpoint-commands.test.ts#L1-L342) | 342 | test or test fixture |
| [packages/evidence/test/provider-fixtures.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/provider-fixtures.test.ts#L1-L197) | 197 | test or test fixture |
| [packages/evidence/test/public-ledger-capacity.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/public-ledger-capacity.test.ts#L1-L75) | 75 | test or test fixture |
| [packages/evidence/test/public-ledger.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/public-ledger.test.ts#L1-L596) | 596 | test or test fixture |
| [packages/evidence/test/public-read-fixtures.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/public-read-fixtures.ts#L1-L237) | 237 | test or test fixture |
| [packages/evidence/test/public-read-ledger.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/public-read-ledger.test.ts#L1-L236) | 236 | test or test fixture |
| [packages/evidence/test/public-read-receipt.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/public-read-receipt.test.ts#L1-L460) | 460 | test or test fixture |
| [packages/evidence/test/receipt.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/receipt.test.ts#L1-L595) | 595 | test or test fixture |
| [packages/evidence/test/reconciliation-index.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/reconciliation-index.test.ts#L1-L575) | 575 | test or test fixture |
| [packages/evidence/test/web216-cpih-ledger.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-cpih-ledger.test.ts#L1-L327) | 327 | test or test fixture |
| [packages/evidence/test/web216-cpih-receipt.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-cpih-receipt.test.ts#L1-L216) | 216 | test or test fixture |
| [packages/evidence/test/web216-cpih-reconciliation.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-cpih-reconciliation.test.ts#L1-L270) | 270 | test or test fixture |
| [packages/evidence/test/web216-pure.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-pure.test.ts#L1-L116) | 116 | test or test fixture |
| [packages/evidence/test/web216-transactional-contract.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-transactional-contract.test.ts#L1-L219) | 219 | test or test fixture |
| [packages/evidence/test/web216-transactional-d1.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/evidence/test/web216-transactional-d1.test.ts#L1-L302) | 302 | test or test fixture |
| [packages/policy-client/src/evidence-inspect-v3.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/src/evidence-inspect-v3.ts#L1-L201) | 201 | application or library |
| [packages/policy-client/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/src/index.ts#L1-L243) | 243 | application or library |
| [packages/policy-client/src/public-read-v2.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/src/public-read-v2.ts#L1-L262) | 262 | application or library |
| [packages/policy-client/test/evidence-inspect-v3.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/test/evidence-inspect-v3.test.ts#L1-L397) | 397 | test or test fixture |
| [packages/policy-client/test/policy-client.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/test/policy-client.test.ts#L1-L233) | 233 | test or test fixture |
| [packages/policy-client/test/public-read-v2.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/test/public-read-v2.test.ts#L1-L160) | 160 | test or test fixture |
| [packages/policy-client/test/web216-cpih-legacy-inspection.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/policy-client/test/web216-cpih-legacy-inspection.test.ts#L1-L49) | 49 | test or test fixture |
| [packages/provider-adapter-sdk/src/contract.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/contract.ts#L1-L207) | 207 | application or library |
| [packages/provider-adapter-sdk/src/fixed-https.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/fixed-https.ts#L1-L504) | 504 | application or library |
| [packages/provider-adapter-sdk/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/index.ts#L1-L18) | 18 | application or library |
| [packages/provider-adapter-sdk/src/ons-approved-cache.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/ons-approved-cache.ts#L1-L490) | 490 | application or library |
| [packages/provider-adapter-sdk/src/ons-data-api.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/ons-data-api.ts#L1-L1374) | 1,374 | application or library |
| [packages/provider-adapter-sdk/src/ons-live-probe-record.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/ons-live-probe-record.ts#L1-L219) | 219 | application or library |
| [packages/provider-adapter-sdk/src/ons-live-probe.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/ons-live-probe.ts#L1-L56) | 56 | application or library |
| [packages/provider-adapter-sdk/src/sites-pilot-providers.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/sites-pilot-providers.ts#L1-L366) | 366 | application or library |
| [packages/provider-adapter-sdk/src/strict-json.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/strict-json.ts#L1-L154) | 154 | application or library |
| [packages/provider-adapter-sdk/src/synthetic-fixture.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/synthetic-fixture.ts#L1-L268) | 268 | application or library |
| [packages/provider-adapter-sdk/src/trace-context.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/trace-context.ts#L1-L128) | 128 | application or library |
| [packages/provider-adapter-sdk/src/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/src/types.ts#L1-L225) | 225 | application or library |
| [packages/provider-adapter-sdk/test/egress-policy.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/egress-policy.test.ts#L1-L350) | 350 | test or test fixture |
| [packages/provider-adapter-sdk/test/fixed-https.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/fixed-https.test.ts#L1-L330) | 330 | test or test fixture |
| [packages/provider-adapter-sdk/test/ons-approved-cache.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/ons-approved-cache.test.ts#L1-L203) | 203 | test or test fixture |
| [packages/provider-adapter-sdk/test/ons-data-api.live.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/ons-data-api.live.test.ts#L1-L41) | 41 | test or test fixture |
| [packages/provider-adapter-sdk/test/ons-data-api.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/ons-data-api.test.ts#L1-L1256) | 1,256 | test or test fixture |
| [packages/provider-adapter-sdk/test/sites-pilot-providers.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/sites-pilot-providers.test.ts#L1-L207) | 207 | test or test fixture |
| [packages/provider-adapter-sdk/test/strict-json.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/strict-json.test.ts#L1-L48) | 48 | test or test fixture |
| [packages/provider-adapter-sdk/test/synthetic-fixture.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/synthetic-fixture.test.ts#L1-L204) | 204 | test or test fixture |
| [packages/provider-adapter-sdk/test/trace-context.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/provider-adapter-sdk/test/trace-context.test.ts#L1-L69) | 69 | test or test fixture |
| [packages/tool-registry/scripts/copy-profile.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/scripts/copy-profile.mjs#L1-L8) | 8 | build, operator or assurance tooling |
| [packages/tool-registry/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/src/index.ts#L1-L2) | 2 | application or library |
| [packages/tool-registry/src/registry.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/src/registry.ts#L1-L914) | 914 | application or library |
| [packages/tool-registry/src/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/src/types.ts#L1-L224) | 224 | application or library |
| [packages/tool-registry/test/tool-registry.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/tool-registry/test/tool-registry.test.ts#L1-L384) | 384 | test or test fixture |
| [services/geo-execution/Containerfile](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/Containerfile#L1-L22) | 22 | configuration |
| [services/geo-execution/src/gis_ai_go_execution/__init__.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/__init__.py#L1-L27) | 27 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/__main__.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/__main__.py#L1-L18) | 18 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/boundary.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/boundary.py#L1-L33) | 33 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/canonical.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/canonical.py#L1-L144) | 144 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/errors.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/errors.py#L1-L129) | 129 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/fixtures.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/fixtures.py#L1-L72) | 72 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/geometry.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/geometry.py#L1-L132) | 132 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/http.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/http.py#L1-L549) | 549 | application or library |
| [services/geo-execution/src/gis_ai_go_execution/service.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/src/gis_ai_go_execution/service.py#L1-L468) | 468 | application or library |
| [services/geo-execution/tests/__init__.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/tests/__init__.py#L1-L1) | 1 | test or test fixture |
| [services/geo-execution/tests/fixtures.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/tests/fixtures.py#L1-L25) | 25 | test or test fixture |
| [services/geo-execution/tests/test_boundary.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/tests/test_boundary.py#L1-L31) | 31 | test or test fixture |
| [services/geo-execution/tests/test_http.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/tests/test_http.py#L1-L302) | 302 | test or test fixture |
| [services/geo-execution/tests/test_service.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/services/geo-execution/tests/test_service.py#L1-L344) | 344 | test or test fixture |

## Experimental and knowledge

| Source at review baseline | Lines | Role |
| --- | ---: | --- |
| [apps/mcp-gateway/src/sites-pilot-http.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/sites-pilot-http.ts#L1-L269) | 269 | application or library |
| [apps/mcp-gateway/src/sites-pilot-store.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/sites-pilot-store.ts#L1-L134) | 134 | application or library |
| [apps/mcp-gateway/src/web216-cpih-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-cpih-application.ts#L1-L173) | 173 | application or library |
| [apps/mcp-gateway/src/web216-cpih-input-schemas.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-cpih-input-schemas.ts#L1-L21) | 21 | application or library |
| [apps/mcp-gateway/src/web216-cpih-mcp.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-cpih-mcp.ts#L1-L194) | 194 | application or library |
| [apps/mcp-gateway/src/web216-cpih-selection.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-cpih-selection.ts#L1-L101) | 101 | application or library |
| [apps/mcp-gateway/src/web216-hosted-cpih-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-hosted-cpih-application.ts#L1-L206) | 206 | application or library |
| [apps/mcp-gateway/src/web216-hosted-cpih-http.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-hosted-cpih-http.ts#L1-L18) | 18 | application or library |
| [apps/mcp-gateway/src/web216-hosted-cpih-mcp.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-hosted-cpih-mcp.ts#L1-L196) | 196 | application or library |
| [apps/mcp-gateway/src/web216-workbench-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-workbench-main.ts#L1-L144) | 144 | application or library |
| [apps/mcp-gateway/src/web216-workbench-server.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/web216-workbench-server.ts#L1-L189) | 189 | application or library |
| [apps/mcp-gateway/test/sites-pilot.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/sites-pilot.test.ts#L1-L543) | 543 | test or test fixture |
| [apps/mcp-gateway/test/web216-cpih-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-cpih-application.test.ts#L1-L169) | 169 | test or test fixture |
| [apps/mcp-gateway/test/web216-cpih-legacy-inspection.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-cpih-legacy-inspection.test.ts#L1-L57) | 57 | test or test fixture |
| [apps/mcp-gateway/test/web216-cpih-mcp.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-cpih-mcp.test.ts#L1-L287) | 287 | test or test fixture |
| [apps/mcp-gateway/test/web216-cpih-selection.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-cpih-selection.test.ts#L1-L72) | 72 | test or test fixture |
| [apps/mcp-gateway/test/web216-hosted-cpih-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-hosted-cpih-application.test.ts#L1-L199) | 199 | test or test fixture |
| [apps/mcp-gateway/test/web216-hosted-cpih-mcp.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-hosted-cpih-mcp.test.ts#L1-L278) | 278 | test or test fixture |
| [apps/mcp-gateway/test/web216-workbench-main.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-workbench-main.test.ts#L1-L55) | 55 | test or test fixture |
| [apps/mcp-gateway/test/web216-workbench-server.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/web216-workbench-server.test.ts#L1-L159) | 159 | test or test fixture |
| [okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/corpus.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/corpus.ts#L1-L276) | 276 | pinned vendored dependency |
| [okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/corpusV3.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/corpusV3.ts#L1-L590) | 590 | pinned vendored dependency |
| [okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/index.ts#L1-L723) | 723 | pinned vendored dependency |
| [okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/types.ts#L1-L210) | 210 | pinned vendored dependency |
| [okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/unit.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/okf-plus/vendor/explorer-context/apps/okf-explorer/src/lib/context/unit.ts#L1-L73) | 73 | pinned vendored dependency |
| [scripts/check_experience_browser.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/check_experience_browser.mjs#L1-L290) | 290 | build, operator or assurance tooling |
| [scripts/experience_evaluate.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/experience_evaluate.mjs#L1-L301) | 301 | build, operator or assurance tooling |
| [scripts/okf_plus/build.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/build.py#L1-L205) | 205 | build, operator or assurance tooling |
| [scripts/okf_plus/context_projection.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/context_projection.py#L1-L471) | 471 | build, operator or assurance tooling |
| [scripts/okf_plus/documentation.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/documentation.py#L1-L443) | 443 | build, operator or assurance tooling |
| [scripts/okf_plus/export.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/export.py#L1-L320) | 320 | build, operator or assurance tooling |
| [scripts/okf_plus/export_documents.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/export_documents.py#L1-L208) | 208 | build, operator or assurance tooling |
| [scripts/okf_plus/freeze_locators.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/freeze_locators.py#L1-L64) | 64 | build, operator or assurance tooling |
| [scripts/okf_plus/harvest.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/harvest.py#L1-L261) | 261 | build, operator or assurance tooling |
| [scripts/okf_plus/import_sources.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/import_sources.py#L1-L318) | 318 | build, operator or assurance tooling |
| [scripts/okf_plus/model.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/model.py#L1-L146) | 146 | build, operator or assurance tooling |
| [scripts/okf_plus/ons_catalogues.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/ons_catalogues.py#L1-L336) | 336 | build, operator or assurance tooling |
| [scripts/okf_plus/ons_enrichment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/ons_enrichment.py#L1-L490) | 490 | build, operator or assurance tooling |
| [scripts/okf_plus/os_enrichment.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/os_enrichment.py#L1-L384) | 384 | build, operator or assurance tooling |
| [scripts/okf_plus/search.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/search.py#L1-L402) | 402 | build, operator or assurance tooling |
| [scripts/okf_plus/verify.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/verify.py#L1-L361) | 361 | build, operator or assurance tooling |
| [scripts/okf_plus/vocabulary_usage.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/okf_plus/vocabulary_usage.py#L1-L146) | 146 | build, operator or assurance tooling |
| [scripts/package_experience_offline.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_experience_offline.mjs#L1-L29) | 29 | build, operator or assurance tooling |
| [scripts/package_sites_pilot_runtime.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_sites_pilot_runtime.mjs#L1-L88) | 88 | build, operator or assurance tooling |
| [scripts/sites_mcp_evaluate.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/sites_mcp_evaluate.mjs#L1-L298) | 298 | build, operator or assurance tooling |
| [scripts/sites_pilot_bundle_entry.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/sites_pilot_bundle_entry.ts#L1-L2) | 2 | build, operator or assurance tooling |
| [scripts/test_sites_pilot_built_worker.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/test_sites_pilot_built_worker.mjs#L1-L326) | 326 | build, operator or assurance tooling |
| [scripts/test_sites_pilot_page.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/test_sites_pilot_page.mjs#L1-L35) | 35 | build, operator or assurance tooling |
| [sites/private-pilot/app/mcp/route.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/app/mcp/route.ts#L1-L10) | 10 | application or library |
| [sites/private-pilot/app/pilot/learning.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/app/pilot/learning.ts#L1-L8) | 8 | application or library |
| [sites/private-pilot/app/pilot/mcp/route.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/app/pilot/mcp/route.ts#L1-L9) | 9 | application or library |
| [sites/private-pilot/app/pilot/page.tsx](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/app/pilot/page.tsx#L1-L187) | 187 | application or library |
| [sites/private-pilot/db/sites-pilot-schema.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/db/sites-pilot-schema.ts#L1-L28) | 28 | application or library |
| [sites/private-pilot/drizzle/0001_sites_pilot.sql](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/drizzle/0001_sites_pilot.sql#L1-L23) | 23 | database migration and constraints |
| [sites/private-pilot/server/sites-pilot-runtime.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/sites/private-pilot/server/sites-pilot-runtime.mjs#L1-L73) | 73 | application or library |

## User interfaces and intake

| Source at review baseline | Lines | Role |
| --- | ---: | --- |
| [apps/public-data-workbench/experience.html](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/experience.html#L1-L44) | 44 | presentation |
| [apps/public-data-workbench/index.html](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/index.html#L1-L43) | 43 | presentation |
| [apps/public-data-workbench/src/controller.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/controller.ts#L1-L160) | 160 | application or library |
| [apps/public-data-workbench/src/discovery.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/discovery.ts#L1-L28) | 28 | application or library |
| [apps/public-data-workbench/src/experience-drop.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/experience-drop.ts#L1-L156) | 156 | application or library |
| [apps/public-data-workbench/src/experience-tools.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/experience-tools.ts#L1-L45) | 45 | application or library |
| [apps/public-data-workbench/src/experience.css](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/experience.css#L1-L1) | 1 | presentation |
| [apps/public-data-workbench/src/experience.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/experience.ts#L1-L173) | 173 | application or library |
| [apps/public-data-workbench/src/main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/main.ts#L1-L123) | 123 | application or library |
| [apps/public-data-workbench/src/mcp-client.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/mcp-client.ts#L1-L46) | 46 | application or library |
| [apps/public-data-workbench/src/styles.css](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/styles.css#L1-L591) | 591 | presentation |
| [apps/public-data-workbench/src/webmcp.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/src/webmcp.ts#L1-L59) | 59 | application or library |
| [apps/public-data-workbench/test/controller.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/test/controller.test.ts#L1-L250) | 250 | test or test fixture |
| [apps/public-data-workbench/test/experience-drop.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/test/experience-drop.test.ts#L1-L159) | 159 | test or test fixture |
| [apps/public-data-workbench/test/experience-tools.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/test/experience-tools.test.ts#L1-L33) | 33 | test or test fixture |
| [apps/public-data-workbench/test/mcp-client.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/test/mcp-client.test.ts#L1-L70) | 70 | test or test fixture |
| [apps/public-data-workbench/vite.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/vite.config.ts#L1-L22) | 22 | configuration |
| [apps/public-data-workbench/vitest.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-data-workbench/vitest.config.ts#L1-L2) | 2 | configuration |
| [apps/public-explorer/index.html](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/index.html#L1-L66) | 66 | presentation |
| [apps/public-explorer/playwright.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/playwright.config.ts#L1-L35) | 35 | configuration |
| [apps/public-explorer/playwright.public.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/playwright.public.config.ts#L1-L55) | 55 | configuration |
| [apps/public-explorer/scripts/build-boundary.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/build-boundary.mjs#L1-L172) | 172 | build, operator or assurance tooling |
| [apps/public-explorer/scripts/check-build-boundary.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/check-build-boundary.mjs#L1-L14) | 14 | build, operator or assurance tooling |
| [apps/public-explorer/scripts/check-dist.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/check-dist.mjs#L1-L198) | 198 | build, operator or assurance tooling |
| [apps/public-explorer/scripts/dist-policy.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/dist-policy.mjs#L1-L119) | 119 | build, operator or assurance tooling |
| [apps/public-explorer/scripts/prepare-data.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/scripts/prepare-data.mjs#L1-L130) | 130 | build, operator or assurance tooling |
| [apps/public-explorer/src/catalogue.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/catalogue.ts#L1-L32) | 32 | application or library |
| [apps/public-explorer/src/dom.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/dom.ts#L1-L158) | 158 | application or library |
| [apps/public-explorer/src/links.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/links.ts#L1-L4) | 4 | application or library |
| [apps/public-explorer/src/main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/main.ts#L1-L625) | 625 | application or library |
| [apps/public-explorer/src/state.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/state.ts#L1-L212) | 212 | application or library |
| [apps/public-explorer/src/styles.css](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/styles.css#L1-L659) | 659 | presentation |
| [apps/public-explorer/src/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/types.ts#L1-L42) | 42 | application or library |
| [apps/public-explorer/src/views/cards.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/cards.ts#L1-L350) | 350 | application or library |
| [apps/public-explorer/src/views/graph.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/graph.ts#L1-L216) | 216 | application or library |
| [apps/public-explorer/src/views/map.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/map.ts#L1-L173) | 173 | application or library |
| [apps/public-explorer/src/views/timeline.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/src/views/timeline.ts#L1-L134) | 134 | application or library |
| [apps/public-explorer/test/browser/accessibility.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/accessibility.spec.ts#L1-L158) | 158 | test or test fixture |
| [apps/public-explorer/test/browser/downloads.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/downloads.spec.ts#L1-L72) | 72 | test or test fixture |
| [apps/public-explorer/test/browser/journeys.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/journeys.spec.ts#L1-L310) | 310 | test or test fixture |
| [apps/public-explorer/test/browser/public-deployment.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/public-deployment.spec.ts#L1-L313) | 313 | test or test fixture |
| [apps/public-explorer/test/browser/reviewed-examples.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/reviewed-examples.spec.ts#L1-L205) | 205 | test or test fixture |
| [apps/public-explorer/test/browser/security.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/browser/security.spec.ts#L1-L68) | 68 | test or test fixture |
| [apps/public-explorer/test/build/build-boundary.test.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/build/build-boundary.test.mjs#L1-L89) | 89 | test or test fixture |
| [apps/public-explorer/test/build/dist-policy.test.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/build/dist-policy.test.mjs#L1-L109) | 109 | test or test fixture |
| [apps/public-explorer/test/component/cards.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/component/cards.test.ts#L1-L116) | 116 | test or test fixture |
| [apps/public-explorer/test/component/fixtures.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/component/fixtures.ts#L1-L193) | 193 | test or test fixture |
| [apps/public-explorer/test/component/graph.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/component/graph.test.ts#L1-L61) | 61 | test or test fixture |
| [apps/public-explorer/test/component/map.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/component/map.test.ts#L1-L22) | 22 | test or test fixture |
| [apps/public-explorer/test/component/timeline.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/component/timeline.test.ts#L1-L54) | 54 | test or test fixture |
| [apps/public-explorer/test/fixtures/assurance.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/fixtures/assurance.ts#L1-L56) | 56 | test or test fixture |
| [apps/public-explorer/test/fixtures/network.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/fixtures/network.ts#L1-L3) | 3 | test or test fixture |
| [apps/public-explorer/test/fixtures/publication.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/fixtures/publication.ts#L1-L103) | 103 | test or test fixture |
| [apps/public-explorer/test/unit/catalogue.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/catalogue.test.ts#L1-L223) | 223 | test or test fixture |
| [apps/public-explorer/test/unit/fixtures.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/fixtures.ts#L1-L122) | 122 | test or test fixture |
| [apps/public-explorer/test/unit/links.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/links.test.ts#L1-L37) | 37 | test or test fixture |
| [apps/public-explorer/test/unit/network.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/network.test.ts#L1-L22) | 22 | test or test fixture |
| [apps/public-explorer/test/unit/publication.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/publication.test.ts#L1-L47) | 47 | test or test fixture |
| [apps/public-explorer/test/unit/state.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/test/unit/state.test.ts#L1-L111) | 111 | test or test fixture |
| [apps/public-explorer/vite.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/vite.config.ts#L1-L10) | 10 | configuration |
| [apps/public-explorer/vitest.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/public-explorer/vitest.config.ts#L1-L8) | 8 | configuration |
| [apps/webmcp-explorer/index.html](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/index.html#L1-L283) | 283 | presentation |
| [apps/webmcp-explorer/playwright.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/playwright.config.ts#L1-L32) | 32 | configuration |
| [apps/webmcp-explorer/scripts/build-boundary.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/build-boundary.mjs#L1-L133) | 133 | build, operator or assurance tooling |
| [apps/webmcp-explorer/scripts/check-dist.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/check-dist.mjs#L1-L62) | 62 | build, operator or assurance tooling |
| [apps/webmcp-explorer/scripts/chrome-preflight.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/chrome-preflight.mjs#L1-L227) | 227 | build, operator or assurance tooling |
| [apps/webmcp-explorer/scripts/html-boundary.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/html-boundary.mjs#L1-L120) | 120 | build, operator or assurance tooling |
| [apps/webmcp-explorer/scripts/prepare-data.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/scripts/prepare-data.mjs#L1-L50) | 50 | build, operator or assurance tooling |
| [apps/webmcp-explorer/src/catalogue-tools.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/src/catalogue-tools.ts#L1-L389) | 389 | application or library |
| [apps/webmcp-explorer/src/dom.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/src/dom.ts#L1-L28) | 28 | application or library |
| [apps/webmcp-explorer/src/main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/src/main.ts#L1-L187) | 187 | application or library |
| [apps/webmcp-explorer/src/styles.css](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/src/styles.css#L1-L656) | 656 | presentation |
| [apps/webmcp-explorer/src/webmcp-adapter.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/src/webmcp-adapter.ts#L1-L226) | 226 | application or library |
| [apps/webmcp-explorer/test/browser/accessibility.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/browser/accessibility.spec.ts#L1-L115) | 115 | test or test fixture |
| [apps/webmcp-explorer/test/browser/journeys.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/browser/journeys.spec.ts#L1-L269) | 269 | test or test fixture |
| [apps/webmcp-explorer/test/browser/security.spec.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/browser/security.spec.ts#L1-L209) | 209 | test or test fixture |
| [apps/webmcp-explorer/test/build/build-boundary.test.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/build/build-boundary.test.mjs#L1-L93) | 93 | test or test fixture |
| [apps/webmcp-explorer/test/build/chrome-preflight.test.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/build/chrome-preflight.test.mjs#L1-L122) | 122 | test or test fixture |
| [apps/webmcp-explorer/test/unit/catalogue-tools.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/unit/catalogue-tools.test.ts#L1-L75) | 75 | test or test fixture |
| [apps/webmcp-explorer/test/unit/fixture.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/unit/fixture.ts#L1-L109) | 109 | test or test fixture |
| [apps/webmcp-explorer/test/unit/webmcp-adapter.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/test/unit/webmcp-adapter.test.ts#L1-L96) | 96 | test or test fixture |
| [apps/webmcp-explorer/vite.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/vite.config.ts#L1-L10) | 10 | configuration |
| [apps/webmcp-explorer/vitest.config.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/webmcp-explorer/vitest.config.ts#L1-L8) | 8 | configuration |
| [packages/experience-intake/src/index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/index.ts#L1-L228) | 228 | application or library |
| [packages/experience-intake/src/previews.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/previews.ts#L1-L157) | 157 | application or library |
| [packages/experience-intake/src/strict-json.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/strict-json.ts#L1-L155) | 155 | application or library |
| [packages/experience-intake/src/types.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/types.ts#L1-L87) | 87 | application or library |
| [packages/experience-intake/src/zip.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/src/zip.ts#L1-L132) | 132 | application or library |
| [packages/experience-intake/test/intake.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/test/intake.test.ts#L1-L169) | 169 | test or test fixture |
| [packages/experience-intake/test/zip.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/packages/experience-intake/test/zip.test.ts#L1-L111) | 111 | test or test fixture |
