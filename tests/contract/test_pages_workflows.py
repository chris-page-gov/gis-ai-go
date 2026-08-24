from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CI_WORKFLOW = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
PAGES_WORKFLOW = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
    encoding="utf-8"
)


class PagesWorkflowTests(unittest.TestCase):
    def test_every_external_action_is_pinned_to_a_full_commit(self) -> None:
        for workflow_name, workflow in (
            ("ci.yml", CI_WORKFLOW),
            ("pages.yml", PAGES_WORKFLOW),
        ):
            uses = re.findall(r"^\s*uses:\s+([^@\s]+)@([^\s]+)", workflow, re.MULTILINE)
            self.assertGreater(len(uses), 0, workflow_name)
            for action, revision in uses:
                with self.subTest(workflow=workflow_name, action=action):
                    self.assertRegex(revision, r"^[0-9a-f]{40}$")

    def test_ci_enforces_release_readiness_only_on_a_version_transition(self) -> None:
        checkout = CI_WORKFLOW.split("- name: Check out repository", 1)[1].split(
            "\n\n      - name:", 1
        )[0]
        self.assertIn("fetch-depth: 0", checkout)
        self.assertIn("verifies immutable QUAL runtime-base Git blobs", checkout)

        assurance_name = "- name: Run assurance"
        transition_name = "- name: Enforce release readiness on a version transition"
        package_name = "- name: Package immutable Pages source"
        self.assertLess(CI_WORKFLOW.index(assurance_name), CI_WORKFLOW.index(transition_name))
        self.assertLess(CI_WORKFLOW.index(transition_name), CI_WORKFLOW.index(package_name))

        transition = CI_WORKFLOW.split(transition_name, 1)[1].split(
            f"\n\n      {package_name}", 1
        )[0]
        self.assertIn("PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}", transition)
        self.assertIn("PUSH_BASE_SHA: ${{ github.event.before }}", transition)
        self.assertIn('case "$GITHUB_EVENT_NAME" in', transition)
        self.assertIn('pull_request) base_sha="$PR_BASE_SHA" ;;', transition)
        self.assertIn('push) base_sha="$PUSH_BASE_SHA" ;;', transition)
        self.assertIn('[[ ! "$base_sha" =~ ^[0-9a-f]{40}$ ]]', transition)
        self.assertIn("0000000000000000000000000000000000000000", transition)
        self.assertIn('git cat-file -e "$base_sha^{commit}"', transition)
        self.assertIn('git cat-file -e "$GITHUB_SHA^{commit}"', transition)
        self.assertIn(
            'git diff --quiet "$base_sha" "$GITHUB_SHA" -- VERSION',
            transition,
        )
        self.assertIn("version_diff_status=$?", transition)
        self.assertIn("1) pnpm run validate:release-readiness ;;", transition)
        self.assertIn("*) echo 'Unable to compare VERSION with the event base'", transition)

        scripts = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"]
        self.assertNotIn("validate:release-readiness", scripts["check"])

    def test_workflows_default_to_no_token_permissions(self) -> None:
        self.assertIn("\npermissions: {}\n", CI_WORKFLOW)
        self.assertIn("\npermissions: {}\n", PAGES_WORKFLOW)

        self.assertIn("\n    permissions:\n      contents: read\n", CI_WORKFLOW)
        self.assertIn(
            "\n    permissions:\n"
            "      actions: read\n"
            "      attestations: write\n"
            "      contents: read\n"
            "      id-token: write\n",
            CI_WORKFLOW,
        )
        self.assertNotIn("contents: write", CI_WORKFLOW + PAGES_WORKFLOW)

    def test_ci_exposes_one_stable_assurance_gate_for_both_producers(self) -> None:
        repository = CI_WORKFLOW.split("\n  repository_assurance:\n", 1)[1].split(
            "\n  gateway_image:\n", 1
        )[0]
        gateway = CI_WORKFLOW.split("\n  gateway_image:\n", 1)[1].split(
            "\n  assurance:\n", 1
        )[0]
        assurance = CI_WORKFLOW.split("\n  assurance:\n", 1)[1].split(
            "\n  provenance:\n", 1
        )[0]

        self.assertEqual(CI_WORKFLOW.count("\n  assurance:\n"), 1)
        self.assertIn("name: Repository assurance", repository)
        self.assertIn("timeout-minutes: 20", repository)
        self.assertIn("name: Gateway image assurance", gateway)
        self.assertIn("needs: repository_assurance", gateway)
        self.assertIn("timeout-minutes: 50", gateway)
        self.assertNotIn("\n  gateway-image:\n", CI_WORKFLOW)

        self.assertIn("name: assurance", assurance)
        self.assertIn("if: always()", assurance)
        self.assertIn("permissions: {}", assurance)
        self.assertIn("- repository_assurance", assurance)
        self.assertIn("- gateway_image", assurance)
        self.assertIn(
            "REPOSITORY_ASSURANCE_RESULT: ${{ needs.repository_assurance.result }}",
            assurance,
        )
        self.assertIn(
            "GATEWAY_IMAGE_RESULT: ${{ needs.gateway_image.result }}", assurance
        )
        self.assertIn(
            '[[ "$REPOSITORY_ASSURANCE_RESULT" != \'success\' ]]', assurance
        )
        self.assertIn('[[ "$GATEWAY_IMAGE_RESULT" != \'success\' ]]', assurance)
        self.assertIn("exit 1", assurance)

        self.assertLess(
            CI_WORKFLOW.index("\n  repository_assurance:\n"),
            CI_WORKFLOW.index("\n  gateway_image:\n"),
        )
        self.assertLess(
            CI_WORKFLOW.index("\n  gateway_image:\n"),
            CI_WORKFLOW.index("\n  assurance:\n"),
        )

    def test_ci_gateway_uploads_only_complete_successful_evidence(self) -> None:
        gateway = CI_WORKFLOW.split("\n  gateway_image:\n", 1)[1].split(
            "\n  assurance:\n", 1
        )[0]
        accepted_name = "- name: Upload immutable gateway image evidence"
        accepted = gateway.split(accepted_name, 1)[1]
        self.assertIn("if: success()", accepted)
        self.assertIn(
            "name: gateway-image-${{ github.sha }}-without-grype-db", accepted
        )
        self.assertIn("path: |\n            artifacts/gateway/", accepted)
        self.assertIn(
            "!artifacts/gateway/gateway-node.grype-db.tar.zst", accepted
        )
        self.assertIn("if-no-files-found: error", accepted)
        self.assertNotIn("if: always()", accepted)
        self.assertEqual(
            gateway.count("!artifacts/gateway/gateway-node.grype-db.tar.zst"), 1
        )
        self.assertNotIn("gateway-image-failure-", gateway)
        self.assertNotIn(".gateway-quarantine-", gateway)

    def test_ci_publishes_pages_source_only_after_successful_main_assurance(self) -> None:
        guard = (
            "if: ${{ github.event_name == 'push' && "
            "github.ref == 'refs/heads/main' && success() }}"
        )
        self.assertGreaterEqual(CI_WORKFLOW.count(guard), 3)
        self.assertIn("name: pages-source-${{ github.sha }}", CI_WORKFLOW)
        self.assertIn("if-no-files-found: error", CI_WORKFLOW)
        self.assertIn("retention-days: 90", CI_WORKFLOW)

        diagnostic = CI_WORKFLOW.split("- name: Upload generated evidence", 1)[1].split(
            "\n\n  gateway_image:", 1
        )[0]
        self.assertIn("if: always()", diagnostic)
        self.assertIn("!artifacts/pages/**", diagnostic)
        self.assertNotIn("pages-source-${{ github.sha }}", diagnostic)

    def test_ci_reverifies_and_attests_the_exact_archive(self) -> None:
        provenance = CI_WORKFLOW.split("\n  provenance:\n", 1)[1].split(
            "\n  gateway-provenance:\n", 1
        )[0]
        self.assertIn("- assurance", provenance)
        self.assertIn("- repository_assurance", provenance)
        self.assertIn("timeout-minutes: 10", provenance)
        self.assertIn("actions: read", provenance)
        self.assertIn("attestations: write", provenance)
        self.assertIn("id-token: write", provenance)
        self.assertIn("name: pages-source-${{ github.sha }}", provenance)
        self.assertIn("scripts/verify_pages_archive.py", provenance)
        self.assertIn(
            "actions/attest-build-provenance@4d101475d8b20a2381f78447822ac1eab6504dd8",
            provenance,
        )
        self.assertIn("subject-path: artifacts/pages/artifact.tar", provenance)

    def test_gateway_provenance_rebuilds_context_before_complete_verification(
        self,
    ) -> None:
        provenance = CI_WORKFLOW.split("\n  gateway-provenance:\n", 1)[1]
        self.assertIn("- assurance", provenance)
        self.assertIn("- gateway_image", provenance)
        self.assertIn("timeout-minutes: 30", provenance)
        self.assertIn("version: 10.33.2", provenance)
        self.assertIn("node-version: 24.19.0", provenance)
        self.assertIn("version: 0.12.2", provenance)
        self.assertIn("pnpm install --frozen-lockfile", provenance)
        self.assertIn(
            "uv sync --locked --group dev --cache-dir .uv-cache", provenance
        )

        download = "- name: Download immutable gateway image evidence"
        rebuild = "- name: Regenerate the governed OKF projection"
        acquire_trivy = "- name: Acquire and validate pinned Trivy scanner over network"
        acquire_grype = "- name: Acquire and validate pinned Grype scanner over network"
        rehydrate = "- name: Rehydrate checksum-bound private Grype database"
        verify = "- name: Verify complete protected-main gateway image evidence"
        self.assertLess(provenance.index(download), provenance.index(rebuild))
        self.assertLess(provenance.index(rebuild), provenance.index(acquire_trivy))
        self.assertLess(provenance.index(acquire_trivy), provenance.index(acquire_grype))
        self.assertLess(provenance.index(acquire_grype), provenance.index(rehydrate))
        self.assertLess(provenance.index(rehydrate), provenance.index(verify))
        for attestation in (
            "- name: Attest immutable gateway OCI archive",
            "- name: Attest gateway image SBOM",
            "- name: Attest gateway image evidence manifest",
        ):
            with self.subTest(attestation=attestation):
                self.assertLess(provenance.index(verify), provenance.index(attestation))
        self.assertIn("run: pnpm run build:okf", provenance)
        self.assertIn("run: pnpm run verify:gateway-image-evidence", provenance)

        trivy_acquisition = provenance.split(acquire_trivy, 1)[1].split(
            f"\n\n      {acquire_grype}", 1
        )[0]
        digest = "62b1e65e8869bc4b4c6aa4fa2b21595256c7c2f6018a9d9ad61caf87187c1969"
        self.assertIn(
            f"TRIVY_IMAGE: aquasec/trivy:0.74.0@sha256:{digest}", trivy_acquisition
        )
        self.assertIn(
            f"TRIVY_REPO_DIGEST: aquasec/trivy@sha256:{digest}", trivy_acquisition
        )
        self.assertIn('docker pull "$TRIVY_IMAGE"', trivy_acquisition)
        self.assertIn('docker image inspect "$TRIVY_IMAGE"', trivy_acquisition)
        self.assertIn(
            'jq -e --arg expected "$TRIVY_REPO_DIGEST"', trivy_acquisition
        )
        self.assertIn(".[0].RepoDigests", trivy_acquisition)
        self.assertIn("index($expected) != null", trivy_acquisition)

        grype_acquisition = provenance.split(acquire_grype, 1)[1].split(
            f"\n\n      {rehydrate}", 1
        )[0]
        grype_digest = (
            "ab8d929faec38875a45aba74c9651549cd096756d1981773c04375f282e91075"
        )
        self.assertIn(
            f"GRYPE_IMAGE: anchore/grype:v0.117.0@sha256:{grype_digest}",
            grype_acquisition,
        )
        self.assertIn(
            f"GRYPE_REPO_DIGEST: anchore/grype@sha256:{grype_digest}",
            grype_acquisition,
        )
        self.assertIn(
            'docker pull --platform linux/amd64 "$GRYPE_IMAGE"', grype_acquisition
        )
        self.assertIn('docker image inspect "$GRYPE_IMAGE"', grype_acquisition)

        restore = provenance.split(rehydrate, 1)[1].split(
            f"\n\n      {verify}", 1
        )[0]
        self.assertIn("scripts/node_runtime_advisory.py", restore)
        self.assertIn("restore-database", restore)
        self.assertIn(
            "--scan artifacts/gateway/gateway-image.vulnerability-scan.json",
            restore,
        )
        self.assertIn("--output-dir artifacts/gateway", restore)

        for subject in (
            "artifacts/gateway/gateway-image.oci.tar",
            "artifacts/gateway/gateway-image.sbom.cdx.json",
            "artifacts/gateway/gateway-image-evidence-manifest.json",
        ):
            with self.subTest(subject=subject):
                self.assertIn(f"subject-path: {subject}", provenance)

        for forbidden in (
            "docker push",
            "docker tag",
            "docker compose up",
            "docker stack deploy",
            "git tag",
            "gh release",
            "kubectl",
            "helm upgrade",
            "fly deploy",
            "MCP_GEO_ACTIVE_PROVIDER",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, CI_WORKFLOW)

    def test_deployment_is_manual_and_has_the_exact_audit_inputs(self) -> None:
        self.assertIn("\n  workflow_dispatch:\n", PAGES_WORKFLOW)
        self.assertNotRegex(PAGES_WORKFLOW, r"(?m)^  (push|pull_request|schedule):")

        inputs = PAGES_WORKFLOW.split("    inputs:\n", 1)[1].split(
            "\npermissions: {}", 1
        )[0]
        names = re.findall(r"^      ([a-z][a-z0-9_]*):$", inputs, re.MULTILINE)
        self.assertEqual(
            names,
            ["source_run_id", "source_commit", "archive_sha256", "mode", "reason"],
        )
        for name in names:
            match = re.search(
                rf"(?ms)^      {name}:\n(.*?)(?=^      [a-z][a-z0-9_]*:$|\Z)",
                inputs,
            )
            self.assertIsNotNone(match)
            self.assertIn("required: true", match.group(1))
        self.assertRegex(
            inputs,
            r"options:\n\s+- deploy\n\s+- rollback\n\s+- restore",
        )

    def test_prepare_accepts_only_an_exact_successful_main_ci_artifact(self) -> None:
        for assertion in (
            "GITHUB_REF\" != 'refs/heads/main'",
            'GITHUB_WORKFLOW_REF\" != \"$expected_workflow_ref\"',
            "GITHUB_REF_PROTECTED\" != 'true'",
            '.event == "push"',
            '.status == "completed"',
            '.conclusion == "success"',
            '.head_branch == "main"',
            ".head_sha == $source_commit",
            '.path == ".github/workflows/ci.yml"',
            ".repository.full_name == $repository",
            ".head_repository.full_name == $repository",
            'artifact_name="pages-source-${SOURCE_COMMIT}"',
            "select(.name == $artifact_name and .expired == false)",
            "^sha256:[0-9a-f]{64}$",
        ):
            with self.subTest(assertion=assertion):
                self.assertIn(assertion, PAGES_WORKFLOW)

        self.assertIn('[[ "$REASON" =~ [[:cntrl:]] ]]', PAGES_WORKFLOW)
        self.assertIn("run-id: ${{ inputs.source_run_id }}", PAGES_WORKFLOW)
        self.assertIn("name: pages-source-${{ inputs.source_commit }}", PAGES_WORKFLOW)
        self.assertIn(
            '--expected-archive-sha256 "$ARCHIVE_SHA256"', PAGES_WORKFLOW
        )

    def test_prepare_binds_the_selected_archive_version_across_rollbacks(self) -> None:
        prepare = PAGES_WORKFLOW.split("\n  prepare:\n", 1)[1].split(
            "\n  deploy:\n", 1
        )[0]
        download_name = "- name: Download exact CI artefact"
        selected_name = "- name: Read selected archive version"
        verify_name = "- name: Verify archive structure and receipt"
        product_name = "- name: Record accepted product identity"
        stage_name = "- name: Materialise verified Pages payload"
        self.assertLess(prepare.index(download_name), prepare.index(selected_name))
        self.assertLess(prepare.index(selected_name), prepare.index(verify_name))
        self.assertLess(prepare.index(verify_name), prepare.index(product_name))
        self.assertLess(prepare.index(product_name), prepare.index(stage_name))

        selected = prepare.split(selected_name, 1)[1].split(
            f"\n\n      {verify_name}", 1
        )[0]
        self.assertIn("id: selected_version", selected)
        self.assertIn("jq -er", selected)
        self.assertIn('if (.version | type) == "string" then', selected)
        self.assertIn(".version", selected)
        self.assertIn(
            'if [[ ! "$selected_version" =~ '
            "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\."
            "(0|[1-9][0-9]*)$ ]]; then",
            selected,
        )
        self.assertIn(
            "printf 'version=%s\\n' \"$selected_version\" >> \"$GITHUB_OUTPUT\"",
            selected,
        )
        self.assertNotIn("eval", selected)

        stable_semver = re.compile(
            r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
        )
        older_selected_version = "0.0.1"
        self.assertRegex(older_selected_version, stable_semver)
        self.assertNotRegex("0.0.1-rc.1", stable_semver)

        selected_binding = (
            "SELECTED_VERSION: ${{ steps.selected_version.outputs.version }}"
        )
        self.assertEqual(prepare.count(selected_binding), 3)
        self.assertEqual(prepare.count('--expected-version "$SELECTED_VERSION"'), 2)
        self.assertIn("printf 'version=%s\\n' \"$SELECTED_VERSION\"", prepare)
        self.assertIn(
            "product_version: ${{ steps.product.outputs.version }}", prepare
        )
        self.assertIn(
            "PRODUCT_VERSION: ${{ steps.product.outputs.version }}", prepare
        )
        self.assertIn('--arg productVersion "$PRODUCT_VERSION"', prepare)
        public_verification = PAGES_WORKFLOW.split(
            "\n  public-verification:\n", 1
        )[1]
        self.assertIn(
            "EXPECTED_VERSION: ${{ needs.prepare.outputs.product_version }}",
            public_verification,
        )
        self.assertIn(
            "PRODUCT_VERSION: ${{ needs.prepare.outputs.product_version }}",
            public_verification,
        )
        self.assertNotRegex(prepare, r"<\s*VERSION\b")
        self.assertNotIn("tr -d", prepare)

    def test_prepare_enforces_github_provenance_identity(self) -> None:
        for flag in (
            '--repo "$GITHUB_REPOSITORY"',
            '--signer-workflow "$signer_workflow"',
            '--signer-digest "$SOURCE_COMMIT"',
            "--source-ref refs/heads/main",
            '--source-digest "$SOURCE_COMMIT"',
            "--deny-self-hosted-runners",
        ):
            with self.subTest(flag=flag):
                self.assertIn(flag, PAGES_WORKFLOW)

    def test_prepare_materialises_and_stages_only_the_verified_payload(self) -> None:
        prepare = PAGES_WORKFLOW.split("\n  prepare:\n", 1)[1].split(
            "\n  deploy:\n", 1
        )[0]
        stage_command = (
            "uv run --locked --cache-dir .uv-cache python "
            "scripts/stage_pages_payload.py"
        )
        self.assertIn("mkdir -p deployment-staging", prepare)
        for argument in (
            "--archive artifacts/pages/artifact.tar",
            "--checksum artifacts/pages/artifact.tar.sha256",
            "--receipt artifacts/pages/archive-receipt.json",
            "--output-dir deployment-staging/site",
            '--expected-source-commit "$SOURCE_COMMIT"',
            '--expected-repository "$GITHUB_REPOSITORY"',
            '--expected-version "$SELECTED_VERSION"',
            "--expected-base-path /gis-ai-go/",
            '--expected-archive-sha256 "$ARCHIVE_SHA256"',
        ):
            with self.subTest(argument=argument):
                self.assertIn(argument, prepare)

        upload_action = (
            "actions/upload-pages-artifact@"
            "fc324d3547104276b827a68afc52ff2a11cc49c9"
        )
        self.assertEqual(PAGES_WORKFLOW.count(upload_action), 1)
        upload = prepare.split(f"uses: {upload_action}", 1)[1].split("\n\n", 1)[0]
        self.assertIn("name: github-pages", upload)
        self.assertIn("path: deployment-staging/site", upload)
        self.assertIn("retention-days: 1", upload)
        self.assertIn("include-hidden-files: true", upload)
        self.assertNotIn("if: always()", upload)

        self.assertLess(
            prepare.index("scripts/verify_pages_archive.py"),
            prepare.index(stage_command),
        )
        self.assertLess(
            prepare.index("gh attestation verify"), prepare.index(stage_command)
        )
        self.assertLess(
            prepare.index("mkdir -p deployment-staging"),
            prepare.index(stage_command),
        )
        self.assertLess(prepare.index(stage_command), prepare.index(upload_action))

        diagnostic = prepare.split("- name: Upload validation evidence", 1)[1].split(
            "\n\n      - name:", 1
        )[0]
        self.assertNotIn("deployment-staging", diagnostic)

    def test_deploy_job_has_only_pages_deployment_authority(self) -> None:
        deploy = PAGES_WORKFLOW.split("\n  deploy:\n", 1)[1].split(
            "\n  public-verification:\n", 1
        )[0]
        self.assertIn("environment:\n      name: github-pages", deploy)
        self.assertIn(
            "permissions:\n      actions: read\n      id-token: write\n      pages: write",
            deploy,
        )
        self.assertNotIn("contents:", deploy)
        self.assertNotIn("attestations:", deploy)
        self.assertIn("artifact_name: github-pages", deploy)
        uses = re.findall(r"^\s*uses:\s+([^@\s]+)@", deploy, re.MULTILINE)
        self.assertEqual(uses, ["actions/configure-pages", "actions/deploy-pages"])
        for forbidden in (
            "actions/checkout",
            "actions/download-artifact",
            "actions/upload-artifact",
            "actions/upload-pages-artifact",
            "scripts/stage_pages_payload.py",
            "artifacts/pages",
            "sha256sum",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, deploy)

    def test_deployment_workflow_never_rebuilds_the_site(self) -> None:
        for forbidden in (
            "scripts/package_pages.py",
            "pnpm run build",
            "vite build",
            "npm run build",
            "tar -x",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PAGES_WORKFLOW)

    def test_public_acceptance_uses_exact_source_and_deployment_receipt_values(self) -> None:
        self.assertIn(
            "okf_content_root: ${{ steps.product.outputs.okf_content_root }}",
            PAGES_WORKFLOW,
        )
        self.assertIn(
            "payload_root: ${{ steps.product.outputs.payload_root }}",
            PAGES_WORKFLOW,
        )
        self.assertIn(
            "public_checksums_sha256: ${{ steps.product.outputs.public_checksums_sha256 }}",
            PAGES_WORKFLOW,
        )
        self.assertIn("'.okfContentRootSha256'", PAGES_WORKFLOW)
        self.assertIn("'.payloadRootSha256'", PAGES_WORKFLOW)
        self.assertIn("'.publication.checksumsSha256'", PAGES_WORKFLOW)
        verification = PAGES_WORKFLOW.split("\n  public-verification:\n", 1)[1]
        self.assertEqual(PAGES_WORKFLOW.count("ref: ${{ github.sha }}"), 2)
        self.assertNotIn("ref: ${{ inputs.source_commit }}", PAGES_WORKFLOW)
        self.assertIn("PUBLIC_BASE_URL: ${{ needs.deploy.outputs.page_url }}", verification)
        self.assertIn("EXPECTED_SOURCE_COMMIT: ${{ inputs.source_commit }}", verification)
        self.assertIn(
            "EXPECTED_VERSION: ${{ needs.prepare.outputs.product_version }}",
            verification,
        )
        self.assertIn(
            "EXPECTED_OKF_CONTENT_ROOT: ${{ needs.prepare.outputs.okf_content_root }}",
            verification,
        )
        self.assertIn(
            "EXPECTED_PAYLOAD_ROOT: ${{ needs.prepare.outputs.payload_root }}",
            verification,
        )
        self.assertIn(
            "EXPECTED_PUBLIC_CHECKSUMS_SHA256: "
            "${{ needs.prepare.outputs.public_checksums_sha256 }}",
            verification,
        )
        self.assertIn("EXPECTED_ARCHIVE_SHA256: ${{ inputs.archive_sha256 }}", verification)
        self.assertIn(
            "pnpm --filter @gis-ai-go/public-explorer run test:public", verification
        )

    def test_successful_public_acceptance_writes_and_uploads_canonical_receipt(
        self,
    ) -> None:
        verification = PAGES_WORKFLOW.split("\n  public-verification:\n", 1)[1]
        acceptance_command = (
            "pnpm --filter @gis-ai-go/public-explorer run test:public"
        )
        receipt_name = "- name: Write public verification receipt"
        upload_name = "- name: Upload public verification evidence"
        failure_upload_name = "- name: Upload failed public verification diagnostics"
        summary_name = "- name: Record accepted deployment"
        self.assertLess(
            verification.index(acceptance_command), verification.index(receipt_name)
        )
        self.assertLess(
            verification.index(receipt_name), verification.index(upload_name)
        )
        self.assertLess(
            verification.index(upload_name), verification.index(failure_upload_name)
        )
        self.assertLess(
            verification.index(failure_upload_name), verification.index(summary_name)
        )

        receipt = verification.split(receipt_name, 1)[1].split(
            f"\n\n      {upload_name}", 1
        )[0]
        for binding in (
            "ARCHIVE_SHA256: ${{ inputs.archive_sha256 }}",
            "DEPLOYMENT_MODE: ${{ inputs.mode }}",
            "OKF_CONTENT_ROOT: ${{ needs.prepare.outputs.okf_content_root }}",
            "PAGE_URL: ${{ needs.deploy.outputs.page_url }}",
            "PAYLOAD_ROOT: ${{ needs.prepare.outputs.payload_root }}",
            "PRODUCT_VERSION: ${{ needs.prepare.outputs.product_version }}",
            "PUBLIC_CHECKSUMS_SHA256: "
            "${{ needs.prepare.outputs.public_checksums_sha256 }}",
            "REPOSITORY: ${{ github.repository }}",
            "SOURCE_COMMIT: ${{ inputs.source_commit }}",
            "SOURCE_RUN_ID: ${{ inputs.source_run_id }}",
            "WORKFLOW_COMMIT: ${{ github.sha }}",
            "WORKFLOW_RUN_ATTEMPT: ${{ github.run_attempt }}",
            "WORKFLOW_RUN_ID: ${{ github.run_id }}",
            "WORKFLOW_RUN_URL: ${{ github.server_url }}/"
            "${{ github.repository }}/actions/runs/${{ github.run_id }}",
        ):
            with self.subTest(binding=binding):
                self.assertIn(binding, receipt)

        self.assertIn("jq -S -n", receipt)
        self.assertIn(
            "--arg schemaVersion "
            "'gis-ai-go.pages-public-verification-receipt.v1'",
            receipt,
        )
        for argument_binding in (
            '--arg repository "$REPOSITORY"',
            '--arg workflowRun "$WORKFLOW_RUN_URL"',
            '--arg workflowRunAttempt "$WORKFLOW_RUN_ATTEMPT"',
            '--arg workflowRunId "$WORKFLOW_RUN_ID"',
            '--arg workflowCommit "$WORKFLOW_COMMIT"',
            '--arg mode "$DEPLOYMENT_MODE"',
            '--arg publicUrl "$PAGE_URL"',
            '--arg productVersion "$PRODUCT_VERSION"',
            '--arg sourceRunId "$SOURCE_RUN_ID"',
            '--arg sourceCommit "$SOURCE_COMMIT"',
            '--arg archiveSha256 "$ARCHIVE_SHA256"',
            '--arg payloadRoot "$PAYLOAD_ROOT"',
            '--arg okfContentRoot "$OKF_CONTENT_ROOT"',
            '--arg publicChecksumsSha256 "$PUBLIC_CHECKSUMS_SHA256"',
        ):
            with self.subTest(argument_binding=argument_binding):
                self.assertIn(argument_binding, receipt)
        for field_binding in (
            "schemaVersion: $schemaVersion",
            "repository: $repository",
            "workflowRun: $workflowRun",
            "workflowRunAttempt: $workflowRunAttempt",
            "workflowRunId: $workflowRunId",
            "workflowCommit: $workflowCommit",
            "mode: $mode",
            "publicUrl: $publicUrl",
            "productVersion: $productVersion",
            "sourceRunId: $sourceRunId",
            "sourceCommit: $sourceCommit",
            "archiveSha256: $archiveSha256",
            "payloadRootSha256: $payloadRoot",
            "okfContentRootSha256: $okfContentRoot",
            "publicChecksumsSha256: $publicChecksumsSha256",
        ):
            with self.subTest(field_binding=field_binding):
                self.assertIn(field_binding, receipt)
        self.assertIn(
            "> public-verification-evidence/public-verification-receipt.json",
            receipt,
        )
        self.assertNotIn("validatedAt", receipt)
        self.assertNotIn("date -u", receipt)

        upload = verification.split(upload_name, 1)[1].split(
            f"\n\n      {failure_upload_name}", 1
        )[0]
        self.assertNotIn("if: always()", upload)
        self.assertIn(
            "public-verification-evidence/public-verification-receipt.json",
            upload,
        )
        self.assertIn("apps/public-explorer/test-results/", upload)
        self.assertIn("if-no-files-found: error", upload)
        self.assertIn("retention-days: 90", upload)

    def test_failed_public_acceptance_uploads_diagnostics_only(self) -> None:
        verification = PAGES_WORKFLOW.split("\n  public-verification:\n", 1)[1]
        success_upload_name = "- name: Upload public verification evidence"
        failure_upload_name = "- name: Upload failed public verification diagnostics"
        summary_name = "- name: Record accepted deployment"
        self.assertLess(
            verification.index(success_upload_name),
            verification.index(failure_upload_name),
        )

        failure_upload = verification.split(failure_upload_name, 1)[1].split(
            f"\n\n      {summary_name}", 1
        )[0]
        self.assertIn("if: failure()", failure_upload)
        self.assertIn(
            "uses: actions/upload-artifact@"
            "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            failure_upload,
        )
        self.assertIn("name: public-verification-failure-", failure_upload)
        self.assertIn("path: apps/public-explorer/test-results/", failure_upload)
        self.assertIn("if-no-files-found: warn", failure_upload)
        self.assertIn("retention-days: 90", failure_upload)
        self.assertNotIn("public-verification-receipt.json", failure_upload)
        self.assertNotIn("if: always()", failure_upload)


if __name__ == "__main__":
    unittest.main()
