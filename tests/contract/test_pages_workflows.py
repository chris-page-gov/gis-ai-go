from __future__ import annotations

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
            "\n\n  provenance:", 1
        )[0]
        self.assertIn("if: always()", diagnostic)
        self.assertIn("!artifacts/pages/**", diagnostic)
        self.assertNotIn("pages-source-${{ github.sha }}", diagnostic)

    def test_ci_reverifies_and_attests_the_exact_archive(self) -> None:
        provenance = CI_WORKFLOW.split("\n  provenance:\n", 1)[1]
        self.assertIn("needs: assurance", provenance)
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
            '--expected-version "$(tr -d \'\\r\\n\' < VERSION)"',
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


if __name__ == "__main__":
    unittest.main()
