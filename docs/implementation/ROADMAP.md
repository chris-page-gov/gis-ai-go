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
- complete non-App results and map/artefact fallbacks;
- the researched 12-tool surface:
  `catalogue.search`, `catalogue.describe`, `selection.resolve`, `data.query`,
  `spatial.locate`, `spatial.analyse`, `statistics.compare`, `route.plan`,
  `map.render`, `artefact.export`, `evidence.inspect`, `workflow.execute`.

Gate: protocol conformance, malicious-input tests, deterministic provider fixtures,
host interoperability, reproducibility, rate/complexity limits and deployment
rollback. Public registration follows only when the deployed candidate passes.

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
