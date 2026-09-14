# WEB-216: source and story crosswalk

Date: 14 September 2026. Scope: bounded read-only source review for the
[public-data workbench](WEB-216_PUBLIC_DATA_WORKBENCH.md).

## Source baselines and preservation

| Source | Inspected local commit | Treatment |
| --- | --- | --- |
| `mcp-geo` | `56683b33c0cd02842b7f3ee465414c68a1f3f2a6` | Tracked historical personas, scenarios and geography contracts only; untracked research and generated artefacts excluded. |
| `okf-ons` | `4aa41c71dd570ceccb661768af95c4d69f49162b` | Use committed contracts and evaluation material. The checkout also has substantial uncommitted enrichment/guidance changes; those are not the accepted integration baseline. |
| `govuk-webmcp` | `32f3d55bf34c4056a4b51b8fa00ad3c94a799d03` | Competition source is read-only, including submission state. Its one pre-existing submission-state modification is not part of this work. |

These are local source baselines, not claims that remote branches were refreshed.
No source repository, source deployment or competition artefact was changed during
the review. Later integration must keep a digest/commit-based before-and-after
check and use source-native attribution. Repository code licensing does not grant
blanket redistribution rights over every dataset or research input.

## Findings and reuse decisions

### MCP-Geo

[Prototype personas](https://github.com/chris-page-gov/mcp-geo/blob/56683b33c0cd02842b7f3ee465414c68a1f3f2a6/docs/spec_package/02_personas_user_stories.md)
use numbered headings: local-authority geo analyst, platform data engineer, civic
app developer, ONS/policy researcher and prototype product manager.
[Map personas](https://github.com/chris-page-gov/mcp-geo/blob/56683b33c0cd02842b7f3ee465414c68a1f3f2a6/research/map_delivery_research_2026-02/01_personas_and_user_journeys.md)
use A–F: resident, local policy/service analyst, journalist/researcher, GIS
specialist, product engineer and an accessibility/assisted-technology user.
Neither inspected set explicitly names a central-government employee.

Six [map story fixtures](https://github.com/chris-page-gov/mcp-geo/blob/56683b33c0cd02842b7f3ee465414c68a1f3f2a6/playground/trials/fixtures/map_story_scenarios.json)
retain their `story-1` to `story-6` identifiers and full descriptive suffixes.
The gallery exercises supplied map overlays; its displayed tool list is not an
executed end-to-end data workflow. Do not promote those screenshots into live
joined OS/ONS proof. Do not reuse election campaign/canvassing framing as a
government-service story.

Reuse the [geography extension contract](https://github.com/chris-page-gov/mcp-geo/blob/56683b33c0cd02842b7f3ee465414c68a1f3f2a6/docs/agent_context/geography-extension-contract.md)
and [boundary guidance](https://github.com/chris-page-gov/mcp-geo/blob/56683b33c0cd02842b7f3ee465414c68a1f3f2a6/docs/Boundaries.md):
shared code/level semantics, explicit nation/vintage/CRS, source-native fields,
accessible map alternatives and cross-surface regression coverage.

### OKF-ONS

The [committed design](https://github.com/chris-page-gov/okf-ons/blob/4aa41c71dd570ceccb661768af95c4d69f49162b/README.md)
already separates frozen metadata discovery, narrowing/comparison, exact record
hydration and a non-executing selection plan from separately authorised retrieval.
The documented demonstrator contains 5,097 metadata records, not 5,097 independent
statistical datasets: 337 ONS Data API, 1,617 Nomis, 3,035 Open Geography and 108
Explore Local Statistics representations. They are a frozen corpus, not current
exhaustive coverage.

Reuse the [source-qualified metadata model](https://github.com/chris-page-gov/okf-ons/blob/4aa41c71dd570ceccb661768af95c4d69f49162b/docs/metadata-model.md)
and [selection contract](https://github.com/chris-page-gov/okf-ons/blob/4aa41c71dd570ceccb661768af95c4d69f49162b/docs/mcp-selection-contract.md).
Its downstream bindings name MCP-Geo, not GIS AI GO: translate them through an
explicit adapter rather than executing supplied tool names or URLs. General Open
Geography and ELS execution bindings are planned. ELS rights remain unevaluated in
the reviewed source register; do not admit ELS data to the public experiment on
the strength of catalogue presence alone.

Six [persona IDs and eight journey IDs](https://github.com/chris-page-gov/okf-ons/blob/4aa41c71dd570ceccb661768af95c4d69f49162b/evaluation/ai-client/personas-and-journeys.json)
provide reusable acceptance anchors. In particular, `government-statistician`,
`policy-researcher`, `geography-analyst`, `data-engineer`, `standards-assessor` and
`ai-evaluation-operator` directly support the new staff-facing workbench.
Journeys include comparison, exact hydration, a read-only MCP plan, recovery
without substitution and reproducible sharing.

### GOV.UK WebMCP competition entry

The [beginner PRD](https://github.com/chris-page-gov/govuk-webmcp/blob/32f3d55bf34c4056a4b51b8fa00ad3c94a799d03/docs/product/beginner-trust-pathway-prd.md)
describes four explicitly synthetic personas: Amina (family administration), Ben
(household/small-business organisation), Carys (data curiosity) and Dev (privacy
and scepticism). Preserve their hypothesis status; these are not interview findings.

The [twelve case contracts](https://github.com/chris-page-gov/govuk-webmcp/blob/32f3d55bf34c4056a4b51b8fa00ad3c94a799d03/evals/personal-agent-cases.json)
include direct foundations for this work: US-06 (CPIH discovery), US-07 (do not
invent today's unemployment value), US-10 (minimal context), US-11 (clarify with
no calls) and US-12 (unrelated calculation with no government attribution).
The family, tax, housing and other service stories remain source context, not an
instruction to expand this OS/ONS work package into those services.

Reuse evidence-first presentation, human/tool action parity and
Explain → Inspect → Do → Check → Reflect. Keep source assertion, freshness,
verification, integrity, rights and coverage separate; do not collapse them into
a trust score. The [evaluation protocol](https://github.com/chris-page-gov/govuk-webmcp/blob/32f3d55bf34c4056a4b51b8fa00ad3c94a799d03/docs/competition/personal-agent-evaluation-protocol.md)
separates model selection, deterministic execution, page parity and answer safety.
An unavailable observation is not a passing result.

## Proposed reconciled personas

These are new GIS AI GO design hypotheses derived from the sources, not a claim
of completed research with government staff. Preserve historical identifiers in
the crosswalk instead of renaming the upstream records.

| New ID | Role and need | Existing anchors |
| --- | --- | --- |
| P01 | Central-government policy analyst: prepare a reproducible area briefing. | MCP-Geo ONS/policy researcher and map persona B; OKF-ONS `policy-researcher`. |
| P02 | Government statistician: establish measure, population, period and comparability. | OKF-ONS `government-statistician`; competition Carys/US-06–US-07. |
| P03 | Local-government service analyst: examine neighbourhood need without inferring individual circumstances. | MCP-Geo local-authority analyst and map persona B; OKF-ONS `geography-analyst`. |
| P04 | Government GIS/data engineer: resolve places and build defensible OS/ONS joins and reproducible exports. | MCP-Geo map personas D/E and platform engineer; OKF-ONS `data-engineer`. |
| P05 | Data-assurance reviewer: inspect evidence, limits and transformations. | OKF-ONS `standards-assessor`; competition Dev. |
| P06 | Resident or civic researcher: understand place-based public evidence in plain language. | MCP-Geo A/C; competition Carys, with Amina/Ben's beginner needs. |
| P07 | Integration/evaluation engineer: verify host interoperability, recovery and efficiency. | MCP-Geo product engineer; OKF-ONS `ai-evaluation-operator`. |

Accessibility, privacy, low technical confidence and low-bandwidth needs apply
across every persona. Retain the historical accessibility persona in source
attribution without making access needs the responsibility of only one user group.

## Proposed story set

All WP-* stories below are proposed compositions. Provider availability and
geography support must be verified before promising a particular answer.

| ID | User goal | Existing test/story anchors | Required outcome |
| --- | --- | --- | --- |
| WP-01 | P01/P02 identifies and retrieves a declared CPIH observation for a briefing. | Competition US-06; OKF-ONS AI-SMOKE-003. | Dataset, version, dimensions, period, value and receipt agree; no false latest claim. |
| WP-02 | P02/P03 chooses a labour-market measure and compares suitable areas. | Competition US-07; MCP-Geo I014; OKF-ONS AI-SMOKE-004/006. | Distinguish ONS/Nomis and confusable records; clarify measure, period and geography before retrieval. |
| WP-03 | P01/P03 retrieves population by age and sex for a council area. | OKF-ONS ONS-Q003; MCP-Geo B008C. | Resolve GSS identity and compatible dimensions, retain units and reference period, expose bounded values. |
| WP-04 | P03/P04 maps a supported housing or occupancy measure. | OKF-ONS ONS-Q012; MCP-Geo I015 and `story-6-westminster-policy-layering`. | Use an appropriate boundary/OS context; do not conflate occupancy, affordability and property facts. |
| WP-05 | P04/P06 resolves an area from a place or postcode and inspects its public profile. | MCP-Geo personas A/B and postcode walkthrough; `story-2-village-hotel-catchment`. | Show ambiguous candidates, nation, lookup mode and vintage; a postcode is not a service catchment. |
| WP-06 | P04/P05 reproduces an OS/ONS evidence map or table. | MCP-Geo `story-5-manchester-inventory-export`; OKF-ONS `share-reproducible-selection`. | Retain source identities, join method, CRS, rights, limits and receipt; reject incompatible vintages without a supported crosswalk. |
| WP-07 | Any persona asks something ambiguous, irrelevant or unnecessarily personal. | Competition US-10–US-12; OKF-ONS `recover-without-substitution`. | Ask a minimal clarification, minimise transmitted context or make zero data calls as appropriate. |
| WP-08 | P07 checks a failed/retried request and its visible result. | OKF-ONS `prepare-read-only-mcp-plan` and recovery journey; competition evaluation protocol. | Distinguish unsupported host, provider failure, stale data and invalid selection; no duplicate execution or fabricated success. |

Start development with the existing smoke/gold cases, then keep an independently
labelled hold-out set separate from tuning. Human testing with actual staff is
still outstanding; automated role simulation cannot validate these personas.
