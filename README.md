# GIS AI GO

**Governed geospatial knowledge and action for people, systems and AI agents.**

The name is a mnemonic: “give us AI governed output”. The formal product
boundary is deliberately broader than AI or MCP.

## Status

This repository is at **Stage 0: repository and evidence foundation**. It contains
governance, candidate contracts, synthetic fixtures, architecture sources and an
assurance harness. It does not contain a deployed MCP server, live provider calls,
credentials, protected data, cloud infrastructure or production policy integration.

Stage 1 requires explicit human approval after the Stage 0 verification gate.

## Identity

- product: **GIS AI GO**
- repository: `gis-ai-go`
- provisional MCP Registry identifier: `io.github.chris-page-gov/gis-ai-go`
- current stage: `0`
- licence: not yet selected; see [LICENSE](LICENSE)

The existing `chris-page-gov/mcp-geo` repository remains read-only historical
evidence at commit `56683b33c0cd02842b7f3ee465414c68a1f3f2a6`. Nothing is copied
from it wholesale.

## Research provenance

The original 19 August 2026 research ZIP and its extracted, hash-bound contents are
preserved unchanged under [`docs/research/2026-08-19/`](docs/research/2026-08-19/PROVENANCE.md).
Operational contracts in this repository are adapted candidates, not silent edits to
that evidence. The project-name decision is recorded in
[`ADR-0002`](docs/decisions/ADR-0002-project-name.md).

## Local verification

Prerequisites are Node.js 24.19.0 LTS, pnpm 10.33.2, Python 3.12 or later,
uv 0.12.2 and Graphviz. The Node.js baseline is recorded in `.nvmrc`.

```bash
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm run check
```

The check builds and type-checks the TypeScript boundary, runs TypeScript and Python
unit tests, validates schemas and fixtures, checks local links, performs a baseline
secret scan, renders diagrams and creates a CycloneDX SBOM in `artifacts/`.
The dated results and explicit limits are recorded in the
[`Stage 0 verification record`](docs/operations/STAGE_0_VERIFICATION.md).

## Repository map

- `apps/mcp-gateway/` — non-networked Stage 0 TypeScript gateway boundary
- `services/geo-execution/` — deterministic Python execution boundary
- `schemas/` — candidate contracts promoted from the research pack
- `providers/fixtures/` — synthetic examples only
- `architecture/source/` — live diagram sources rendered by CI
- `evaluation/` — acceptance and threat-test manifests
- `docs/research/` — immutable research evidence
- `scripts/` — Stage 0 assurance tooling
