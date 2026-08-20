# GIS AI GO

**Governed geospatial knowledge and action for people, systems and AI agents.**

The name is a mnemonic: “give us AI governed output”. The formal product
boundary is deliberately broader than AI or MCP.

## Status

**QUAL-105 is complete and `v0.1.0` is assembled for release.** The current public
site at <https://chris-page-gov.github.io/gis-ai-go/> remains the verified `0.0.0`
candidate until the tagged `v0.1.0` artefact is deployed and its public-verification
receipt passes. Support will be declared only after the protected tag, verified
deployment, immutable GitHub Release, durable checksummed assets and merged final
evidence all exist and pass their gates.

The Explorer is a static, metadata-only product; there is no MCP service. Live status is in
[`PROGRESS.md`](PROGRESS.md); current authority and boundaries are in
[`CONTEXT.md`](CONTEXT.md); notable changes are in [`CHANGELOG.md`](CHANGELOG.md).

## Identity

- product: **GIS AI GO**
- repository: `gis-ai-go`
- provisional MCP Registry identifier: `io.github.chris-page-gov/gis-ai-go`
- release being assembled: `v0.1.0`
- licence: [MIT](LICENSE), copyright © 2026 Chris Page; identified
  [third-party material](THIRD_PARTY.md) retains its own terms

The existing `chris-page-gov/mcp-geo` repository remains read-only historical
evidence at commit `56683b33c0cd02842b7f3ee465414c68a1f3f2a6`. Nothing is copied
from it wholesale.

## Research provenance

The original 19 August 2026 research ZIP and its extracted, hash-bound contents are
preserved unchanged under [`docs/research/2026-08-19/`](docs/research/2026-08-19/PROVENANCE.md).
Operational contracts in this repository are adapted candidates, not silent edits to
that evidence. The project-name decision is recorded in
[`ADR-0002`](docs/decisions/ADR-0002-project-name.md).

## Licence

GIS AI GO code, documentation, schemas and research are licensed under the
[MIT licence](LICENSE), copyright © 2026 Chris Page. This includes the immutable
research ZIP and its extracted copy; the licensing decision is recorded in
[`ADR-0003`](docs/decisions/ADR-0003-mit-licence.md). Linked external resources
and imported material identified in [`THIRD_PARTY.md`](THIRD_PARTY.md) retain their
own rights and licence terms.

## Local verification

Prerequisites are Node.js 24.19.0 LTS, pnpm 10.33.2, Python 3.12 or later and
uv 0.12.2. The Node.js baseline is recorded in `.nvmrc`; diagram rendering uses
the lockfile-pinned WebAssembly renderer.

```bash
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm run check
```

The check builds and type-checks the TypeScript boundary, runs TypeScript and Python
unit tests, reproducibly builds and validates the public OKF candidate and Explorer,
runs its real-browser accessibility and security journeys, validates other schemas
and fixtures, checks local links, performs a baseline secret scan, renders diagrams
and creates a CycloneDX SBOM in `artifacts/`.
The foundation baseline and its explicit limits are preserved in the
[`Stage 0 verification record`](docs/operations/STAGE_0_VERIFICATION.md); each OKF
build emits its own ignored manifest, checksums and deterministic receipt.

## Repository map

- `apps/public-explorer/` — static accessible catalogue Explorer
- `apps/mcp-gateway/` — TypeScript gateway, currently a fail-closed scaffold
- `services/geo-execution/` — deterministic Python execution boundary
- `schemas/` — candidate contracts promoted from the research pack
- `providers/fixtures/` — synthetic examples only
- `architecture/source/` — live diagram sources rendered by CI
- `evaluation/` — acceptance and threat-test manifests
- `okf/` — reviewed public publication inputs, profile, source lock and provenance
- `docs/research/` — immutable research evidence
- `scripts/` — repository and release assurance tooling
- `docs/implementation/` — live roadmap, backlog and delivery model
