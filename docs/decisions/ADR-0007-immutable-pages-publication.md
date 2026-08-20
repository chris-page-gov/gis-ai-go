# ADR-0007: Immutable GitHub Pages publication

- status: partially superseded by ADR-0008
- decided on: 20 August 2026
- work item: DISC-104

## Context

The public Explorer is a static product whose source, catalogue, rights and browser
behaviour already pass repository assurance. Building it again during deployment
would create a second, weaker path between reviewed source and the public site.
Automatic deployment after every push would also make rollback depend on rebuilding
old source rather than retaining an accepted artefact.

GitHub Pages needs a tar archive delivered by a workflow with `pages: write` and
`id-token: write`. The repository's ordinary CI token is read-only and `main` is
protected by a no-bypass pull-request ruleset.

## Decision

Build the deployable Pages archive once, at the end of the complete assurance job
for a successful push to protected `main`. The deterministic archive contains only
the checked Explorer distribution, `.nojekyll` and publication metadata. It records
the source commit, product version, `/gis-ai-go/` base path, canonical URL, OKF
content root, complete file manifest, checksums, provenance, site receipt and
CycloneDX SBOM. Tar paths use the Pages-required `./` root, ownership uses a fixed
non-root numeric identity, and modes and modification times are normalised;
wall-clock time is excluded. The fixed identity describes archive transport only;
it does not claim an operating-system account.

Attest the exact tar archive in a separate successful-main job. Retain the tar,
checksum and outer receipt together as `pages-source-<source-commit>`. Deployment is
a manually dispatched workflow on `main` that must:

1. identify a successful `push` CI run for `main` and the exact source commit;
2. download the named retained artefact rather than check out and rebuild the site;
3. verify its declared SHA-256 digest, deterministic receipt and GitHub build
   provenance;
4. upload that unchanged tar as the current `github-pages` artefact, using the
   Actions service's standard compressed transport wrapper;
5. deploy through the branch-restricted `github-pages` environment; and
6. run the public-browser suite against the returned Pages URL.

Use the same workflow for `deploy`, `rollback` and `restore`. A rollback selects a
previously accepted source CI run and digest. A restore selects the later accepted
artefact. Neither action rebuilds source. Deployment reasons and selected identities
remain in the workflow record.

All executable deployment and public-verification code is checked out from the
current protected `main` workflow commit. The selected source commit is handled only
as an attested archive identity and never as executable workflow input. A retained
archive that is no longer compatible with the protected-main verifier must stop for
a reviewed compatibility change; the workflow must not execute its older source.

The deployed application continues to use its exact meta Content Security Policy.
GitHub Pages does not provide repository-controlled response headers, so this
decision does not claim `frame-ancestors` or other header-only controls.

## Consequences

- ordinary pull requests cannot publish a site;
- CI and deployment permissions remain separate and least privilege;
- the public URL can be traced to one source commit, content root, archive digest,
  attestation and deployment run;
- rollback is evidence that retained bytes can be redeployed, not merely that old
  source still compiles;
- GitHub Actions artefact retention is not permanent, so supported release archives,
  checksums and receipts must also be attached to the corresponding GitHub release;
  accepting a release asset for deployment requires a separately reviewed ingestion
  path and is not authorised by this workflow;
- a change to archive format or publication identity requires a new ADR version or
  superseding decision and new rollback evidence.

ADR-0008 supersedes only the unchanged-tar transport decision in step 4. The
protected Pages environment in step 5 and the deterministic source archive,
attestation, manual selection, public verification and rollback requirements remain
in force.
