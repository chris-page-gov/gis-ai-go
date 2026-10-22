# Product roadmap

The owner has authorised Codex to progress autonomously through the open-product
roadmap. Each release advances only when its tests and publication evidence pass;
this is an evidence gate, not a request for repeated permission.

## `v0.1.0` — public discovery product (released)

Status: supported and immutable at
[`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0).

Outcome: a useful, accessible static product that people can browse without an MCP
host or account.

Deliver:

- a reproducible canonical OKF 0.2 bundle;
- an accessible static Explorer with search, facets, graph, timeline, map and data
  card journeys;
- reviewed public HMLR, ONS and LandIS examples with provenance, rights and vintage;
- linked JSON and JSON-LD downloads;
- hardened URL handling, Content Security Policy and no dependence on the historical
  research viewer;
- immutable GitHub Pages artefact and deployment receipt.

Gate: source/data rights review, exact-source integrity, browser journeys, WCAG 2.2
AA acceptance, clean console, security checks, SBOM and rollback rehearsal.

## `v0.2.0` — open read-only MCP (next)

Outcome: the same governed catalogue and evidence model is usable by MCP clients and
direct API consumers without reducing the non-MCP product.

Deliver:

- protocol-conformant TypeScript gateway and typed Python execution boundary;
- deterministic fixture and open-data provider adapters;
- policy-aware catalogue discovery and immutable evidence receipts;
- complete non-App results for every advertised tool;
- lifecycle profiles for the researched 12-tool surface:
  `catalogue.search`, `catalogue.describe`, `selection.resolve`, `data.query`,
  `spatial.locate`, `spatial.analyse`, `statistics.compare`, `route.plan`,
  `map.render`, `artefact.export`, `evidence.inspect`, `workflow.execute`;
- an exact supported active set of `catalogue.search`, `catalogue.describe`,
  `evidence.inspect`, `selection.resolve` and `data.query`; and
- planned status for the other seven profiles, with map and artefact fallbacks
  required before their corresponding tools can become active.

Gate: protocol conformance, malicious-input tests, deterministic provider fixtures,
host interoperability, reproducibility, rate/complexity limits, exact lifecycle
agreement across MCP and direct API, no advertised unimplemented tool, and
deployment rollback. Public registration follows only when the deployed candidate
passes. [`ADR-0009`](../decisions/ADR-0009-read-only-mcp-tool-lifecycle.md) defines
the activation boundary; mutating `workflow.execute` is deferred to `v0.3.0`.

## `v0.3.0` — governed open platform

Outcome: discovery and invocation are governed by explicit, replayable policy.

Deliver authority-context construction, OPA policy packages, policy-filtered
discovery, Arazzo workflows, transaction-bound permits, synthetic open/PSGA/
commercial tier tests and challenge reconstruction.

Gate: no cross-tier leakage, policy and receipt replay, deny-by-default tests,
threat-model validation and accessible non-App behaviour.

## `v1.0.0` — supported public product

Outcome: the open product has an owned, supportable service boundary.

Gate: published service levels, operational ownership, dependency and provenance
assurance, disaster recovery, performance, security assessment, accessibility,
interoperability, incident response and a verified rollback from production.

## Conditional protected integrations

PSGA, commercial and multi-organisation integrations are not promises that this
repository alone can complete. Their interfaces and synthetic assurance can be
built openly, but live pilots require current agreements, provider/enterprise
credentials, DPIA and security approval, paid infrastructure where necessary and
physically isolated data planes. These external decisions do not block the open
roadmap.

## Additive OS and ONS knowledge framework

The [selected classification increment](CLASSIFICATION_RELEASE_DISCOVERY.md) adds
source-scoped code-list access and private small-knowledge exports. The durable
backlog remains edition-matched definitions, source discrepancy resolution,
complete national variants and independently reviewed mappings; a passed list
traversal is not full domain coverage.

The optional [label-origin contract](../../examples/geography-task-experience/LABEL-ORIGIN.md)
keeps project display fallbacks out of supplier-label assertions. Source-specific
label-field interpretation and independent reconstruction remain prerequisites;
structural validation alone does not close authoritative vocabulary coverage.

The later selected Census and ONSUD pass expands retained code-list contexts
while keeping source-page mnemonic conflicts, overlapping aggregate semantics
and missing revision metadata explicit. The authoritative product denominator,
technical route/format/edition cells and independent acceptance are separate
closure requirements. Supplier clarification material is prepared privately;
recorded differences must be classified before treating them as defects.

The owner authorised [OKF-220](OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md) on
2 October 2026. It extends metadata discovery through OKF+ without changing the
existing runtime or supported-release gates. Deliver measured source inventories,
source-backed Markdown/YAML-LD, schema and vocabulary mappings, provenance,
search, clear reference periods, update/release routes and question evaluations.

Acceptance separates catalogue traversal, metadata evidence, schema validation,
semantic curation, retrieval and live Ask OKF admission. Unknown completeness
denominators remain open; a large record count does not close them.

The 21 October learning increment adds a
[task composition model](GEOGRAPHY_TASK_COMPOSITION.md) and
[source-positioned term discovery](GEOSPATIAL_TERM_DISCOVERY.md). Task-specific
definitions and just-in-time help must preserve provider vocabulary, edition,
jurisdiction and provenance. An accessible search alias does not establish a
semantic mapping. Human learning, accessibility and complete external vocabulary
coverage remain separate acceptance gates.

The optional [field-documentary panel](../../examples/geography-task-experience/FIELD-DOCUMENTARY-LINKS.md)
adds a bounded source interface for native property/version context and explicit
attribute-level documentation links. It preserves missing and ambiguous matches
without asserting API adoption or vocabulary equivalence. Public checks use
fictional fixtures; source acceptance and rendered-host acceptance remain
separate requirements.

The 19 October [OS recovery increment](OKF_OS_RECOVERY.md) completed its accessible
bounded pass: 2,302 of 2,303 frozen documentation pages were captured, with one
recorded HTTP 307 gap and no unresolved targets; 216,765 passages passed audit,
and six newer pages were captured separately. All 94 NGD schema/queryables pairs
and 44 WFS feature-type schemas were retained. First pages from all 94 NGD
collections yielded 186 records and 3,968 field knowledge cards; verified disposal
left no raw payloads in that workset. The final explanation export matches all
2,915 field candidates with no missing or ambiguous links across 3,347 files
(maximum 16,383 bytes); documentation-version matching remains unverified.
All 353 affected tests and final-source CI/CodeQL passed; the initial increment
merged through PR #154. Its protected-main acceptance and subsequent bounded WFS
operation review are recorded in issue #153. Continue towards measured entitlement
coverage, version-matched
semantic links and resumable transient feature processing with reproducible
retrieval recipes and verified disposal. This pass does not establish national
feature traversal, all PSGA coverage or answers to every question. Bulk archive
transfers remain deferred pending the recorded exact Azure host adjustment;
source ambiguities and unsent support drafts remain explicit.

The owner extended this work with [presentation-aware retrieval research](OS_RETRIEVAL_PRESENTATION_RESEARCH.md)
and [scoped availability reporting](OS_DATA_AVAILABILITY.md). Map/table/analysis
requirements must be explicit when comparing cost; portrayal alone cannot satisfy
native-value questions. Investigate VizQL and related declarative visualisation
approaches and retain the underlying units, grain, geometry/CRS/datum, time,
aggregation and quality. Track missing data using separate access, expectation,
observation and retrieval states; missing route evidence is unknown data presence.
A completed selected retrieval closes that selector only; report the requested
scope directly and leave unproven source/version assertions visible.

The [bounded Linked Identifiers method](OS_LINKED_IDENTIFIER_METHOD.md) adds local
typed lookups and relationship-first candidate planning. Preserve correlation
methods, source versions, confidence meanings and set-valued cardinality before
considering a separately justified spatial fallback. Native references and API
links need compatible scope/version evidence; neither establishes transitive
identity. Current planner namespaces do not admit NGD Building/OSID or ONS GSS
bridges. Live selection evidence, those bridges and geographic rendering retain
separate acceptance gates; no new hosted tool is admitted.

## Learning and feature evaluation

[EXPERIENCE-221](EXPERIENCE-221_LEARNING_AND_EVALUATION.md) was authorised on
2 October 2026. It maps current facilities to personas, plain and specialist
language, source APIs/data, presentation forms, user stories and executable or
reviewable evaluation cases. Authored 100% coverage uses the closed current-feature
inventory, with baseline and new local facilities separated. Participant success,
natural-language/Voice execution, native Sites connection, Claude access and
proposed file converters remain independently measured. The first event route is
facilitator-led with offline activities; preserve the existing private audience.
