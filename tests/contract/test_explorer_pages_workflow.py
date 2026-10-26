from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CI = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
PAGES = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
BUILD = ROOT / "scripts/build_explorer_pages_candidate.sh"


def job(workflow: str, identifier: str) -> str:
    match = re.search(
        rf"(?ms)^  {re.escape(identifier)}:\n(.*?)(?=^  [a-z][a-z0-9_-]*:\n|\Z)",
        workflow,
    )
    if match is None:
        raise AssertionError(f"missing workflow job {identifier}")
    return match.group(1)


class ExplorerPagesWorkflowTests(unittest.TestCase):
    def test_full_candidate_is_required_without_selective_shadow_routing(self) -> None:
        candidate = job(CI, "explorer_pages_candidate")
        header = candidate.split("    steps:\n", 1)[0]
        self.assertIn("needs: repository_assurance", header)
        self.assertNotIn("if:", header)
        self.assertIn("permissions:\n      contents: read", header)
        self.assertNotIn("write", header)
        self.assertNotIn("needs.ci_impact", candidate)
        self.assertNotIn("continue-on-error:", candidate)
        self.assertIn("timeout-minutes: 40", header)
        assurance = job(CI, "assurance")
        self.assertIn("- explorer_pages_candidate", assurance)
        self.assertIn(
            "EXPLORER_PAGES_RESULT: ${{ needs.explorer_pages_candidate.result }}",
            assurance,
        )
        self.assertIn('[[ "$EXPLORER_PAGES_RESULT" != \'success\' ]]', assurance)
        self.assertIn("exit 1", assurance)
        impact = json.loads((ROOT / ".github/ci/verification-impact-map.v2.json").read_text())
        self.assertEqual(impact["mode"], "shadow")
        self.assertIn("explorer_pages_candidate", impact["always_run"])

    def test_upstream_checkout_and_toolchain_match_the_reviewed_pin(self) -> None:
        candidate = job(CI, "explorer_pages_candidate")
        pin = json.loads((ROOT / "config/explorer-publication.json").read_text())
        checkout = candidate.split("- name: Check out the reviewed Explorer source", 1)[1].split(
            "\n\n      - name:", 1
        )[0]
        self.assertIn(f"repository: {pin['repository']}", checkout)
        self.assertIn(f"ref: {pin['sourceCommit']}", checkout)
        self.assertRegex(pin["sourceCommit"], r"^[0-9a-f]{40}$")
        self.assertIn("persist-credentials: false", checkout)
        self.assertIn("path: upstream-okf-explorer", checkout)
        self.assertIn("node-version: 24.22.1", candidate)
        self.assertIn("version: 0.12.2", candidate)
        build = BUILD.read_text(encoding="utf-8")
        self.assertIn('git -C "$explorer_checkout" rev-parse HEAD', build)
        self.assertIn("corepack pnpm install --frozen-lockfile", build)
        self.assertIn("corepack pnpm build:determinism", build)
        self.assertIn("uv python install", build)
        self.assertIn("uv sync --locked", build)
        self.assertIn("uv run --locked python scripts/build_site.py", build)

    def test_candidate_exercises_verified_archive_before_source_retention(self) -> None:
        build = BUILD.read_text(encoding="utf-8")
        sequence = [
            "scripts/okf_plus/build.py",
            "scripts/okf_plus/context_projection.py",
            "scripts/okf_plus/explorer_projection.py",
            "node scripts/build_explorer_pages.mjs",
            "scripts/package_explorer_pages.py",
            "scripts/verify_pages_archive.py",
            "scripts/stage_pages_payload.py",
            "python -m http.server 8131 --bind 127.0.0.1",
            "run test:explorer-public",
        ]
        positions = [build.index(command) for command in sequence]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('--publication-base "$context_base"', build)
        self.assertIn('--captured-at "$captured_at" --all-records', build)
        self.assertNotIn("--allow-local-preview", build)
        self.assertIn('--output-dir "$candidate_root/staged/gis-ai-go"', build)
        self.assertIn("PUBLIC_BASE_URL=http://127.0.0.1:8131/gis-ai-go/", build)
        self.assertIn('EXPECTED_ARCHIVE_SHA256="$archive_sha256"', build)
        self.assertIn('EXPECTED_PAYLOAD_ROOT="$payload_root"', build)
        self.assertIn("trap cleanup_candidate_server EXIT", build)
        candidate = job(CI, "explorer_pages_candidate")
        self.assertLess(
            candidate.index("bash scripts/build_explorer_pages_candidate.sh upstream-okf-explorer"),
            candidate.index("- name: Upload immutable Pages source"),
        )

    def test_only_successful_main_uses_the_deployment_source_artifact_name(self) -> None:
        candidate = job(CI, "explorer_pages_candidate")
        self.assertEqual(CI.count("name: pages-source-${{ github.sha }}"), 2)
        source = candidate.split("- name: Upload immutable Pages source", 1)[1].split(
            "\n\n      - name:", 1
        )[0]
        self.assertIn(
            "if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' && success() }}",
            source,
        )
        self.assertIn("name: pages-source-${{ github.sha }}", source)
        self.assertIn("retention-days: 90", source)
        review = candidate.split("- name: Retain the pull request review candidate", 1)[1].split(
            "\n\n      - name:", 1
        )[0]
        self.assertIn("github.event_name == 'pull_request' && success()", review)
        self.assertIn("name: pages-review-${{ github.sha }}", review)
        self.assertNotIn("name: pages-source-", review)
        provenance = job(CI, "provenance")
        self.assertIn("- assurance", provenance)
        self.assertIn("- explorer_pages_candidate", provenance)
        self.assertIn("subject-path: artifacts/pages/artifact.tar", provenance)

    def test_manual_deployment_dispatches_only_verified_supported_schemas(self) -> None:
        prepare = job(PAGES, "prepare")
        verify_position = prepare.index("- name: Verify archive structure and receipt")
        schema_position = prepare.index("publication_schema=")
        self.assertLess(verify_position, schema_position)
        self.assertIn("gis-ai-go.pages-archive-receipt.v1|gis-ai-go.pages-archive-receipt.v2", prepare)
        self.assertIn("publication_schema: ${{ steps.product.outputs.publication_schema }}", prepare)
        verification = job(PAGES, "public-verification")
        self.assertIn("PUBLICATION_SCHEMA: ${{ needs.prepare.outputs.publication_schema }}", verification)
        self.assertIn("case \"$PUBLICATION_SCHEMA\" in", verification)
        self.assertIn("gis-ai-go.pages-archive-receipt.v1)", verification)
        self.assertIn("run test:public", verification)
        self.assertIn("gis-ai-go.pages-archive-receipt.v2)", verification)
        self.assertIn("run test:explorer-public", verification)
        self.assertIn("No acceptance journey exists", verification)
        self.assertIn("exit 1", verification)
        self.assertIn("timeout-minutes: 35", verification)
        self.assertNotIn("build_explorer_pages", PAGES)
        self.assertNotIn("context_projection.py", PAGES)
        self.assertNotIn("checkout@7ffa", PAGES)

    def test_builder_shell_parses_and_refuses_a_different_source_commit(self) -> None:
        syntax = subprocess.run(["bash", "-n", str(BUILD)], capture_output=True, text=True)
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            env = {**os.environ, "GITHUB_SHA": "f" * 40}
            result = subprocess.run(
                ["bash", str(BUILD), temporary], cwd=ROOT, env=env,
                capture_output=True, text=True, timeout=10,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exact checked-out source commit", result.stderr)
        self.assertNotIn("Downloading", result.stdout)


if __name__ == "__main__":
    unittest.main()
