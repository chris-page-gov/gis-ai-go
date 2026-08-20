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

The complete local candidate gate passed on 20 August 2026 against the uncommitted
DISC-104 candidate based on protected `main` at
`e5a522ee17f3a0a6f5857245c5ae3acd767efc25`:

- 17 deterministic archive and hostile-input contract tests;
- 10 workflow event, identity, provenance, permission and no-build deployment
  contract tests;
- 4 gateway tests, 16 Explorer build-policy tests, 42 Explorer unit and component
  tests, 58 repository Python tests and 2 execution-boundary tests;
- 25 existing local real-browser journeys;
- 8 schemas and 53 evaluation records, 289 local links, 183 immutable research
  hashes, 2 source-ledger snapshots and 71 source identifiers;
- 442 text files scanned without a baseline secret or machine-path match;
- 9 rendered diagrams and a 145-component repository CycloneDX SBOM.

The candidate packager and verifier reproduced uncompressed canonical POSIX ustar
archive SHA-256
`aca0decf3637e836e0818619456deec75601b0a99475ca6d71b17a23c8fc0f31`
and payload root
`9b0f95f52bc77f45924a767cf774f70e9806b5b10b0ccbe0e460701e3e05ee55`
from merged source commit `e5a522e` and OKF content root
`c3fdadf975194580d1f659e7f3f3b609099b720129b9d8149801115f659c4040`.
This is a local rehearsal identity, not the future protected-main publication
artefact. The archive was extracted under the `/gis-ai-go/` mount and the separate
public suite passed all 4 identity, accepted-manifest payload, trusted-ledger checksum,
reviewed-journey, history, network, CSP, accessibility and 320 CSS-pixel tests.

All nine external Action pins were independently resolved against their official
GitHub tag refs; the annotated pnpm tag was dereferenced to its exact commit.

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
