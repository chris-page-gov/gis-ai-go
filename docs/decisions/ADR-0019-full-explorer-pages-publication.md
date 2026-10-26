# ADR-0019: Full OKF+ Explorer publication

- status: accepted design; implementation candidate
- decided on: 26 October 2026
- work item: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153)
- extends: ADR-0007 publication identity and distribution contract
- retains: ADR-0008 verified-payload transport and legacy v1 rollback

## Context

The GIS Pages pipeline publishes the smaller `apps/public-explorer` catalogue.
Its INSPIRE default does not expose the complete OKF+ Reader, linked learning
paths and field explanations implemented in the separate canonical Explorer.
The portable review package proves neither a public deployment nor a replacement
for the existing immutable publication contract.

## Decision

GIS AI GO owns assembly and publication of the public metadata surface. Reuse the
canonical application without forking its presentation code. Pin the consumer to
`chris-page-gov/okf-explorer` source
`7ffa3297ec85bf28c27963724f221d80579bed1b`, app tree
`d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93`,
and build-manifest SHA-256
`ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2`.
Verify the complete app build and retain its licence notices.

Generated guides form a separate closure from the unchanged app materials.
`explorer/GUIDE-PROVENANCE.json` records the pinned upstream source, original
Site tree, original and published file hashes, and reference mappings.
Out-of-scope guide links resolve to immutable upstream authored sources;
fragments are retained where a matching source heading exists. Changed guides
link to this provenance, and upstream licence and source references remain.

Place that unchanged app under `/gis-ai-go/explorer/`. The GIS root opens
`explorer/explore/` with the complete descriptor at
`/gis-ai-go/gis/explorer/okf-explorer.json`. Preserve recognised legacy catalogue
links through `/gis-ai-go/legacy/`, retaining their query and record fragment.
The root entrypoint is a separate publication file; it does not replace a file
within the verified canonical app.

Generate the full Reader and context from the checked GIS source, retaining
small linked learning records, source-native metadata and explicit unknowns.
Generate context for
`https://chris-page-gov.github.io/gis-ai-go/gis/explorer/context/`.
Do not rewrite a localhost-bound projection after its hashes have been generated.
The publication contains public metadata and guidance; credentials, private
captures and geographic feature payloads remain excluded.

Scope this main-target increment to the full public metadata, Reader/context,
learning and native-field/atomic source-card dependencies. The separate new
private capture extension remains unchanged at
[reconciliation commit 35318abc](https://github.com/chris-page-gov/gis-ai-go/tree/35318abcce5e23c1509ed6ce131d81f5dfd0d38c)
for [unresolved CodeQL review](../operations/EXPLORER_PAGES_CODEQL_REVIEW.md).
Public acceptance can proceed independently because it does not call that feature.
This neither fixes nor dismisses its findings; the wider acquisition objective
and existing main recovery remain. Retain full mandatory assurance on the public
tree and regenerate its source-bound projections after the scope change.

The v2 distribution contract binds both source identities, the app manifest,
complete Reader/context snapshot and exact publication inventory. Its served
files total less than 1,000,000,000 bytes, with at most 50,000 files and at most
32 MiB per payload file. Verification and staging stream bounded regular files,
check every declared byte count and digest, and reject traversal, links, special
files, missing files and unexpected inventory. The legacy v1 verifier and its
existing bounds remain available unchanged for retained rollback artefacts.

Keep the existing protected-main CI, exact archive attestation, manual Pages
selection and branch-restricted deployment environment. Deployment materialises
the verified archive and uses the pinned official Pages transport; it does not
build the application or regenerate projections. Public verification checks all
served bytes with bounded concurrency, then exercises default entry, all three
learning paths, field/source inspection, search, keyboard, narrow layouts and
legacy links. Record the exact candidate, deployment and results.

## Ownership and evidence

The repository owner maintains the publication contract; the upstream Explorer
owns its application build. The existing source, rights, security, accessibility
and release checks apply. This candidate addresses stale defaults, mixed source
identities, incomplete corpus closure and unsafe archive extraction through
exact inventories, pinned identities and bounded verification.

Retain an accepted v1 archive before cutover. Rehearse rollback to its exact
logical bytes and restore the accepted v2 bytes through the same manual workflow,
recording public verification after each. A new deployment failure does not
authorise a rebuild or a weaker verifier.

## Consequences

The public default can use the full knowledge bundle while old catalogue links
remain usable. The implementation remains a candidate until its source gates,
deployment, public browser checks and rollback/restore evidence exist. The
supported `v0.1.0` release stays immutable. This static publication does not
establish a supported `v0.2.0` gateway, protected-data entitlement or hosted Ask
OKF admission.
