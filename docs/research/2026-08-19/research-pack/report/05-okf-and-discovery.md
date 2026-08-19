# OKF and discovery: describe richly, enforce elsewhere

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Normative and experimental boundaries

**Verified fact.** Normative OKF 0.2 is a directory of Markdown concepts with YAML frontmatter. `type` is the only always-required field; provenance, generation, verification, lifecycle and attested-computation fields are optional first-class families. [S-OKF-SPEC]

This pack therefore contains:

- a normative-style OKF corpus under [`okf/`](../okf/index.md);
- an additive Explorer/publication descriptor at [`data/research.okf.json`](../data/research.okf.json);
- JSON/HTML projections for search, facets, graph, timeline, map and data cards.

Explorer JSON shards, JSON-LD/YAML-LD, predicate registries, search postings and provider datapacks are application/domain conventions. They must not be presented as normative OKF core. [S-OKF-EXPLORER]

## What OKF should describe

Providers, datasets, collections, distributions, APIs, MCP servers, tools/resources, workflows, licences, access tiers, identity/entitlement requirements, policy references, lineage, transformations, quality, uncertainty, trust signals, lifecycle, freshness, examples, evaluation cases and attested-computation interfaces.

It should not contain live access tokens, protected data, runtime allow/deny authority, mutable workflow state or the canonical audit store.

## Mapping

| OKF concept | Related standard/surface | Canonical authority |
| --- | --- | --- |
| Provider/dataset/distribution | DCAT 3, GeoDCAT-AP, OGC Records, STAC | Provider catalogue/contract; OKF is curated discovery view |
| API/service | OpenAPI, OGC API, AsyncAPI | Published service contract |
| MCP server/capability | MCP resources and capability metadata | MCP server registry plus policy-filtered `server/discover` |
| Workflow | Arazzo and MCP Tasks | Versioned workflow definition and runtime state store |
| Licence/policy reference | ODRL mapping plus provider terms | Signed/current legal agreement and policy repository |
| Lineage/provenance | W3C PROV mapping | Source ledger and evidence receipt |
| Computation | OKF Attested Computation interface | Pinned executor, runtime receipt and deterministic attester |
| Map asset | STAC/OGC/PMTiles/COG metadata | Provider/object artefact manifest |

## Verification is not attestation

Verification records that a person or process checked a knowledge claim or bundle using a stated method. Attestation records that a computation was executed under a sanctioned interface and that a deterministic attester accepted its receipt. A human review of prose is not a computation attestation; a passing schema build is not proof that the statistics are true.

## Progressive disclosure

The bundle gives a client a small root index, then provider/domain summaries, then individual records and source evidence. The same records drive:

- left-hand search and facets;
- central result/map/graph/timeline views;
- right-hand selected-item cards;
- MCP resources and capability descriptions;
- policy input references;
- source citation and evidence inspection;
- the Codex implementation hand-off.

## Explorer changes required

The current Explorer already supports large static corpora, facets, map/graph/timeline views and provider datapacks. The successor needs additive first-class rendering for:

- access tier versus classification versus personal-data status;
- identity and entitlement requirements;
- policy references and obligations;
- authoritative versus generated/verified/attested actors;
- source/rights warnings on the map and export path;
- accepted/rejected/deferred decisions and side-by-side comparison;
- evidence receipts and policy challenge links.

These changes should be proposed to Explorer separately; Stage 1 can use a self-contained pack without modifying that repository.
