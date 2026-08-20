# DISC-104 GitHub Pages verification record

- status: implementation candidate
- reviewed on: 20 August 2026
- work item: DISC-104
- public URL: not deployed

## Outcome

DISC-104 packages the checked Explorer distribution once and separates build,
attestation and deployment. The deployment workflow can publish, roll back or
restore only a successful protected-`main` artefact whose source run, commit,
SHA-256 digest, deterministic receipt and GitHub provenance all agree.

No workflow publishes the repository root, immutable research viewer, source tree,
provider payload, credential or protected data. Deployment performs no build.

Deployment-time verifier and browser-test code always comes from the current
protected-main workflow commit. A dispatch-selected source commit remains
non-executable archive identity data.

## Candidate gates

Before merge, record:

- deterministic archive tests, including repeated byte-for-byte output;
- malicious path, symlink, hard-link, special-file, inventory and checksum
  rejection;
- workflow event, source-run, branch, commit, artefact-name, digest, attestation and
  least-privilege contract tests;
- complete repository assurance and CodeQL at the pull-request head; and
- independent review of the archive, workflow and public-browser boundaries.

The complete local candidate gate most recently passed on 20 August 2026 against
the Pages compatibility candidate based on protected `main` at
`8e48e68ed6f072be22d46cc866dac947a7a71a4d`:

- 20 deterministic archive and hostile-input contract tests;
- 10 workflow event, identity, provenance, permission and no-build deployment
  contract tests;
- 4 gateway tests, 16 Explorer build-policy tests, 42 Explorer unit and component
  tests, 61 repository Python tests and 2 execution-boundary tests;
- 25 existing local real-browser journeys;
- 8 schemas and 53 evaluation records, 289 local links, 183 immutable research
  hashes, 2 source-ledger snapshots and 71 source identifiers;
- 443 text files scanned without a baseline secret or machine-path match;
- 9 rendered diagrams and a 145-component repository CycloneDX SBOM.

Before the Pages header compatibility correction, packager and verifier contract
`1.0.0` reproduced uncompressed canonical POSIX ustar archive SHA-256
`aca0decf3637e836e0818619456deec75601b0a99475ca6d71b17a23c8fc0f31`
and payload root
`9b0f95f52bc77f45924a767cf774f70e9806b5b10b0ccbe0e460701e3e05ee55`
from merged source commit `e5a522e` and OKF content root
`c3fdadf975194580d1f659e7f3f3b609099b720129b9d8149801115f659c4040`.
This is a historical local rehearsal identity, not a compatible protected-main
publication artefact. The archive was extracted under the `/gis-ai-go/` mount and
the separate public suite passed all 4 identity, accepted-manifest payload,
trusted-ledger checksum, reviewed-journey, history, network, CSP, accessibility and
320 CSS-pixel tests.

All nine external Action pins were independently resolved against their official
GitHub tag refs; the annotated pnpm tag was dereferenced to its exact commit.

## Pages ingestion compatibility evidence

The first three deployment attempts stopped after validation, provenance,
configuration and artefact staging had passed:

- runs
  [`32319998787`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32319998787)
  and
  [`32320096985`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32320096985)
  selected the artefact from source commit `9ff1281`;
- run
  [`32320645861`](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32320645861)
  selected the artefact from source commit `8e48e68` after restoring the standard
  compressed Actions transport;
- all three reached `actions/deploy-pages`, created a Pages deployment and then
  returned GitHub's generic `deployment_failed` state; public verification was
  correctly skipped.

The exact staged archive from the third run retained SHA-256
`d151284c48467c7420f37c1bca7a99619c3230711a0c5d6a9162f7f12c8ac573`.
It contained 57 regular members, but all member paths omitted the required `./`
root and all used numeric owner and group `0`. GitHub's Pages maintainer documents
the `./` prefix as an intentional ingestion requirement in
[`actions/deploy-pages` issue 203](https://github.com/actions/deploy-pages/issues/203#issuecomment-1652804586),
and the same tracker documents root-owned members as a cause of the opaque failure
in
[`actions/deploy-pages` issue 58](https://github.com/actions/deploy-pages/issues/58#issuecomment-1367490639).

Packager and verifier contract `1.0.1` therefore requires `./` member paths and
fixed non-root numeric ownership. Regressions reject an unprefixed path and a
root-owned member. The deployment job still cannot rebuild or repackage an accepted
archive; a fresh protected-main build and attestation are required before another
dispatch.

## Protected-main source evidence

Complete after the implementation pull request merges:

- source commit: pending;
- successful CI push run and `assurance` job: pending;
- source artefact name and ID: pending;
- `artifact.tar` SHA-256 and outer receipt: pending;
- GitHub build-provenance attestation: pending;
- product version and OKF content root: pending.

## Repository configuration evidence

Complete before first deployment:

- Pages build type `workflow`, HTTPS enforced and no custom domain: pending;
- `github-pages` environment restricted to exact branch `main`: pending;
- complete-SHA Action pin enforcement: pending;
- existing protected-main ruleset and read-only default workflow token reverified:
  pending.

## Deployment and public evidence

Complete after first deployment:

- deployment workflow run, Pages deployment ID and public URL: pending;
- live receipt identity equals selected source artefact: pending;
- checksum and JSON/JSON-LD parity: pending;
- default, Price Paid, ONS, LandIS, direct-route and history journeys: pending;
- exact CSP, clean console and publication-path-only requests: pending;
- keyboard, axe A/AA and 320 CSS-pixel acceptance: pending.

## Rollback rehearsal

Complete with two accepted protected-main artefacts:

- artefact A identities and original deployment: pending;
- artefact B identities and original deployment: pending;
- rollback run redeploying A without a build and its public evidence: pending;
- restore run redeploying B without a build and its public evidence: pending.

DISC-104 remains incomplete while any item in this record is pending.
