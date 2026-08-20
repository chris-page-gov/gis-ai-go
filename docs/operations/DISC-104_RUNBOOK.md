# DISC-104 GitHub Pages runbook

This runbook publishes or restores an already built GIS AI GO Pages artefact. It
must never build the Explorer during deployment.

## Publication identities

Record all of these before dispatch:

- the successful `CI` push run ID for protected `main`;
- its full 40-character source commit;
- artefact name `pages-source-<source-commit>`;
- SHA-256 of `artifact.tar` from `artifact.tar.sha256`;
- product version, publication payload root, public checksum-ledger digest and OKF
  content root from `archive-receipt.json`;
- the successful GitHub provenance attestation for that tar.

The retained artefact contains exactly:

```text
artifact.tar
artifact.tar.sha256
archive-receipt.json
```

The tar contains only the generated site plus `.nojekyll` and the
`publication/` manifest, checksums, provenance, site receipt and SBOM.

## First-time repository configuration

The repository owner performs this once after the publication workflow has merged
and a successful protected-`main` source artefact exists:

1. set the Pages build type to GitHub Actions and enforce HTTPS;
2. leave the custom domain unset;
3. configure the `github-pages` environment to accept only the exact `main` branch;
4. retain the existing no-bypass `main` ruleset and required `assurance` check;
5. require complete commit-SHA pins for Actions; and
6. confirm workflow token permissions remain read-only by default.

Record the API responses in the verification record. Do not enable branch-folder
publication, publish `docs/`, or upload the repository root.

## Inspect and verify a source artefact

Replace the examples with the exact run and commit being considered:

```bash
gh run view SOURCE_RUN_ID --repo chris-page-gov/gis-ai-go
gh run download SOURCE_RUN_ID \
  --repo chris-page-gov/gis-ai-go \
  --name pages-source-SOURCE_COMMIT \
  --dir /tmp/gis-ai-go-pages-source
shasum -a 256 /tmp/gis-ai-go-pages-source/artifact.tar
gh attestation verify /tmp/gis-ai-go-pages-source/artifact.tar \
  --repo chris-page-gov/gis-ai-go
```

The digest must equal both `artifact.tar.sha256` and
`archive-receipt.json.archive.sha256`. The receipt source commit must equal the CI
run head. Stop on any mismatch.

## Deploy

Dispatch only the workflow stored on protected `main`:

```bash
gh workflow run pages.yml \
  --repo chris-page-gov/gis-ai-go \
  --ref main \
  -f source_run_id=SOURCE_RUN_ID \
  -f source_commit=SOURCE_COMMIT \
  -f archive_sha256=ARCHIVE_SHA256 \
  -f mode=deploy \
  -f reason='Initial v0.1.0 public discovery deployment'
```

The workflow validates the source run, archive and attestation before the
`github-pages` environment is entered. It then deploys the unchanged tar and runs
the public Playwright suite against the URL returned by GitHub Pages. A failed
public check is a failed deployment gate even if Pages accepted the bytes.

Record the workflow run, deployment ID, public URL, source run and commit, archive
digest, attestation URL, version, OKF root and public-test result.

## Roll back and restore

Rollback requires two previously accepted artefacts, A and B. B is the current
site; A is its accepted predecessor.

1. Reverify A's source run, digest, outer receipt and GitHub attestation.
2. Dispatch the same workflow with A's identities, `mode=rollback` and a clear
   reason.
3. Confirm the public receipt now identifies A and the complete public suite passes.
4. Reverify B without rebuilding it.
5. Dispatch B with `mode=restore` and a clear reason.
6. Confirm the public receipt identifies B and the complete public suite passes.

Example mode-specific fields are:

```text
-f mode=rollback -f reason='DISC-104 rollback rehearsal to accepted artefact A'
-f mode=restore  -f reason='DISC-104 restore rehearsal to accepted artefact B'
```

Never substitute a local rebuild, a workflow artefact from a pull request, a failed
run or a mutable branch archive. The current workflow accepts only an unexpired
Actions source artefact. A release asset preserves evidence but is not an accepted
deployment input; if the Actions artefact has expired, stop until a separately
reviewed release-asset ingestion path exists.

## Public acceptance

The workflow's public suite must verify:

- receipt, provenance, source commit, version, publication payload root, trusted
  public checksum-ledger digest and OKF content root;
- every trusted-ledger checksum, every accepted-manifest payload byte and
  JSON/JSON-LD identifier parity;
- the default HMLR legal-boundary caveat and the Price Paid, ONS and LandIS
  discovery journeys;
- direct query/fragment routes and browser history;
- the exact Content Security Policy, clean console and publication-path-only
  network traffic; and
- keyboard skip navigation, WCAG A/AA checks and 320 CSS-pixel reflow.

Do not mark DISC-104 complete until deploy, rollback and restore each have a public
receipt and passing public-browser evidence.
