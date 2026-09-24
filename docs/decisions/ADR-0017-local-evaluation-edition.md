# ADR-0017: A separately identified local evaluation edition

- status: accepted for implementation; publication remains gated
- date: 24 September 2026
- decision owner: Chris Page
- work item: [LOCAL-214 #118](https://github.com/chris-page-gov/gis-ai-go/issues/118)

## Context and authority

The owner authorised completing the standalone local edition and correcting stale
tracking on 24 September 2026. Browser sign-in to Sites has succeeded, but it has
not established a directly authenticated remote MCP connection. Local completion
must not wait for that separate platform question or weaken public release gates.

## Decision

Keep the provider-free, loopback-only, disposable assembly in
[ADR-0015](ADR-0015-provider-free-loopback-local-candidate.md). Add a separately
identified **local evaluation edition**, proposed tag `v0.2.0-local.1`. It is not
the supported `v0.2.0` service. The latest supported public product remains
`v0.1.0`.

The local edition identifier versions the evaluation package, not the software
manifests. `VERSION`, package versions and `software_version` remain `0.1.0`;
`target_release` remains `0.2.0`. A later stable version change continues to use
the existing supported-release checks. Do not change historical receipts or
rename old results to make these identities appear equal.

The edition consists of a clean, identified source archive, source inventory and
checksums, locked dependency installation, one documented launcher, a separate
bounded MCP demonstration, an illustrated walkthrough and an A4 PDF. No owner
cache, SSD, private evidence store, provider credential or model subscription is
required. Dependency installation may access package registries. This is not an
operating-system network sandbox.

The acceptance record follows
[`local-edition-acceptance.v1.schema.json`](../../schemas/local-edition-acceptance.v1.schema.json).
It binds an exact source commit and tree, artefact hashes and distinct checks. A
valid record is not automatically a passing record. Pending, failed or unavailable
gates must remain explicit. Publication requires every required gate to pass,
including an unaided colleague walkthrough. An independent automated/agent
clean-room review is valuable engineering evidence but is not human user research
or a substitute for that named gate.

When accepted, publish an immutable GitHub **prerelease**, explicitly not latest,
at the checked protected-main commit with its exact artefacts. Never publish the
stable `v0.2.0` tag or close public-service gates #23, #24 or #25 from this result.
Before publication, rerun acceptance where source, dependencies or environment
changed; reuse valid unchanged observations with their exact identities.

## Lifetime and data

The approved T04 cache retains its existing expiry of
`2027-02-20T20:21:08.947Z`. Startup and a separate local capability-health field
show its source, capture and approval dates, expiry and non-current-data warning.
Assembly readiness does not assert data freshness. At and after expiry the data
query fails closed; discovery and session evidence inspection remain available.
No environment variable changes the clock, approval or cache identity.

Chris Page owns renewal decisions through #118 or its explicit successor. A
reviewed replacement requires new source/provenance, rights, bytes, approval and
tests. Until then an expired edition remains usable for learning about refusal
and evidence, not for successful data retrieval. There is no silent synthetic
substitute or approval extension.

Receipts survive only the running process. Orderly stop removes the private
temporary state; abrupt termination may leave temporary files and does not prove
crash cleanup, restart recovery or durable-service operation. Save permitted
demonstration output before stopping if it is needed later.

## Scope and limits

Record each actually tested OS, architecture and tool version; a minimum version
is not a test result. macOS and Linux require separate clean-source observations.
Do not claim Windows support without its own test. No new live AI observation is
needed for an unchanged protocol/client contract.

Sites declaration, OAuth discovery, hosted persistence/rollback, OS/ONS joins and
wider staff stories remain in [WEB-216 #125](https://github.com/chris-page-gov/gis-ai-go/issues/125).
Scheduled EVID-211 preservation remains paused at the owner's request. Ordinary
source-controlled implementation notes do not restart private capture.
