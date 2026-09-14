# Current progress

Last updated: 14 September 2026

## Current checkpoint

- Supported public product: [v0.1.0 static Explorer](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0).
- Accepted local runtime: LOCAL-212 through [PR #112](https://github.com/chris-page-gov/gis-ai-go/pull/112),
  commit `57e49322e305b499fccfbb6c46bc15e2a0ff38f9`. A clean clone can run
  the five tools and three resources with approved cached data and no provider egress.
- Chronicle baseline: `6c76c92a18da779766f8d49acbbd7dbbd31abb97`, following
  preservation repairs #114/#115. Protected-main [CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34810081520)
  and [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34810081562) passed.
- Public MCP hosting, live deployment acceptance and the `v0.2.0` tag/release
  remain open in #23, #24 and #25.

## Authorised current work

The owner authorised [WEB-216 #125](https://github.com/chris-page-gov/gis-ai-go/issues/125):
advance WebMCP into OKF-led ONS discovery and governed retrieval, with OS/ONS
geography, consistent staff stories, reproducible experiments and a shared
person/AI evidence interface. Continue until blocked and merge verified increments.
The inception is merged through [PR #126](https://github.com/chris-page-gov/gis-ai-go/pull/126)
at `87c5997eecc6b6ddf4487cc226d3905544f5595f`.
The metadata foundation is merged through [PR #127](https://github.com/chris-page-gov/gis-ai-go/pull/127)
at `52c46d9cd619d5c349472c250d2d03aebb3beb3c`, with complete protected-main CI,
CodeQL and provenance passing. A bounded maintained-CPIH API observation returned
two HTTP 200 responses; the full captured series passes the new offline validator.
This is empirical API evidence, not a new live MCP operation or Site deployment.
The retired `cpih01` source is explicitly distinguished from maintained L522/MM23.
PR #128 is accepted at `4c8e6144dfb02ea5d9dcf4cb34fbe34f36529f3e`, with complete
protected-main CI and CodeQL passing. PR #129 is accepted at
`806fdcc5b39cee75c6a9144ffa18cc92a66bfc2a`; PR #130's closed CPIH contracts and
application are accepted at `f4b1a90d64b4aea4c6be3f4b08bcbee1cdfe68ec`. Both
complete protected-main CI and CodeQL runs passed. The separate local workbench
increment has demonstrated genuine in-app-browser page tools calling MCP,
durable July retrieval/inspection, and identical receipt inspection after restart.
Manual January retrieval and Chrome/Edge July retrieval also passed. This working
tree observation is not an accepted-build attestation or hosted capability claim.
See the [local walkthrough](docs/implementation/WEB-216_LOCAL_WORKBENCH_WALKTHROUGH.md).
PR #131 is merged at `fd8106691bb5c3d63e5f11c21b16f1e7c26f4321`; required PR
checks and protected-main source assurance passed. Both main image builds failed
during packaging, including the single unchanged-source retry; the inner failure
cause was not retained. The following PR #132 storage foundation is now accepted at
`b9729b5cacc77e9f2b12790c40ad6349fae7b370`: complete protected-main
[assurance](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34884325687)
and [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34884325565)
passed, including both image derivations, attestation verification and provenance.
This does not retrospectively explain the earlier failure. Bounded diagnostic
improvements are isolated separately. The inactive storage foundation passes 35
focused tests and a real local Workers/D1 restart experiment. It adds no endpoint
or deployment. PR #133's diagnostic repair and PR #134's hosted transport are now
accepted at `67ab535ff4d16f54f777dd45787c2f4742a5150c` and
`1a89c73c7e8dec671cb3abd92c271d3d071c2830`, with complete protected-main
assurance and CodeQL passing. A subsequent guarded Workers experiment passed
19 wire requests, five negative cases and exact receipt inspection after restart,
with no provider egress. The reviewed HTTP/pure-evidence extraction is accepted
through PR #135 at `cbdda51d2753a668670ad3a4dd4cf2b019fdb883`, with complete
protected-main assurance and CodeQL passing. The separately assembled private
Site candidate was deployed on 14 September 2026 at 20:26 UTC. Its schema is
present and its store is empty; operator access remains disabled. The final
built-Site local test passed 19 requests and exact receipt inspection after restart,
but used synthetic identity. Hosted sign-in is awaiting the owner's passkey;
hosted initialisation, browser journeys and retention acceptance remain pending.
The old Site demonstration and local workbench are unchanged. See the
[storage experiment](docs/implementation/WEB-216_HOSTED_STORAGE_EXPERIMENT.md).
The OS Open Names Warwick point is captured; ONS boundary metadata succeeded but
three bounded point queries timed out (two GETs and one POST). A real MSOA join
and hosted persistence acceptance remain open. The private candidate deployment
is not a public MCP service or a supported release.
See the [retrieval experiment](docs/implementation/WEB-216_ONS_RETRIEVAL_EXPERIMENT.md), the
[work package](docs/implementation/WEB-216_PUBLIC_DATA_WORKBENCH.md),
[experiment protocol](docs/implementation/WEB-216_EXPERIMENTS.md) and
[source-time journal](docs/chronicle/WEB-216_JOURNAL.md).
`mcp-geo`, `okf-ons` and the `govuk-webmcp` competition entry remain read-only.

## Earlier chronicle checkpoint

The owner started [RETRO-208 #86](https://github.com/chris-page-gov/gis-ai-go/issues/86)
and [CHRON-213 #117](https://github.com/chris-page-gov/gis-ai-go/issues/117) at this
natural break. Work covers the private evidence analysis, public draft chronicle,
agent history, beginner learning path, A4 illustrations, repository code review,
GPT-6 Astra guidance review and a plan for local completion without hosted service.

The code review produces a separate modularisation and optimisation stage. The
local-completion investigation proposes scope and acceptance before changing runtime
or supported-release definitions. Public drafts use evidence cleared for that purpose;
private evidence remains local.

The review edition contains 12 chapters, eight diagrams, a 14-part learning path,
source-linked code findings and a pseudonymous census of 1,043 task threads.
The recovery edition reconciles 23 public outcomes with additional permitted
private evidence into a reviewed minimum of 31 outcomes. It corrects completion
timestamps, joins the recovered asynchronous launches and keeps granular timing,
costs and provenance private. Earlier archives are unchanged. The public revision
contains reviewed paraphrases and aggregates, not private logs or identifiers.
Issue #86 was closed on 14 September 2026 with owner approval on the basis
“all recoverable evidence reconciled; irrecoverable gaps documented”. A
first-ever/exhaustive count still cannot be certified across the remaining
redaction/quarantine gaps. Follow-ons #122/#123 cover client-contract
preflight and source-time attempt journalling without starting implementation.
[LOCAL-214 #118](https://github.com/chris-page-gov/gis-ai-go/issues/118)
defines the next local-edition stages; [IMPROVE-215 #119](https://github.com/chris-page-gov/gis-ai-go/issues/119)
holds the separate implementation plan. Neither plan has changed runtime behaviour.

## Preservation

EVID-211 continues daily and at material milestones. The post-#115 capture reached
`commit-complete` and complete four-worker offline verification passed for that
snapshot: 3,293 objects and 3,110 projections. Current store identity, inventory and
subsequent results are held in the private operating record. The predecessor remains
unchanged with its recorded semantic failure. [Issue #116](https://github.com/chris-page-gov/gis-ai-go/issues/116)
tracks future incremental-parallel optimisation; it does not block the chronicle.

The 14 September WEB-216 milestone passed complete verification at 3,676 objects
and 4,456 events. A separately verified, owner-only text-recovery supplement
retains 191 objects across 198 events, including previously unsupported source
representations and the private deployment checkpoint. Seven secret-pattern
exclusions remain explicit; the existing stores and daily destination are unchanged.
These are separate verification scopes, not a new whole-history completeness claim.

## Handoff and historical evidence

Read [AGENTS.md](AGENTS.md) for the working rules, [CONTEXT.md](CONTEXT.md) for
authority, the [roadmap](docs/implementation/ROADMAP.md) for product stages and the
[chronicle](docs/chronicle/README.md) for the learning record. GitHub issues are
authoritative for current item state.

The former 1,147-line progress history is preserved in the
[fixed baseline snapshot](https://github.com/chris-page-gov/gis-ai-go/blob/6c76c92a18da779766f8d49acbbd7dbbd31abb97/PROGRESS.md).
Historical evidence remains in the operation runbooks, changelog and immutable
research pack. This short checkpoint replaces repeated loading of that history.
