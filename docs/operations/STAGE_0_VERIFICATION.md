# Stage 0 verification record

Verified locally on 19 August 2026. The exact Git commit is reported in the
handover after the repository is initialised; embedding a commit identifier in
the commit it identifies would be self-referential.

## Locked toolchain and dependencies

- Node.js 24.19.0 LTS baseline and pnpm 10.33.2;
- TypeScript 7.0.2 and `@types/node` 24.13.3;
- official MCP TypeScript server package 2.0.0, with core 2.0.0 and Zod 4.4.3;
- Python compatibility floor 3.12, resolved locally with CPython 3.12.11;
- uv 0.12.2 and `jsonschema` 4.26.0;
- Graphviz 15.1.1.

JavaScript dependencies are locked by `pnpm-lock.yaml`. Python dependencies are
locked by `uv.lock`. The repository contains no application runtime dependency
that can call a live provider.

## Results

The complete `pnpm run check` command passed:

- TypeScript: 2 projects type-checked; 4 gateway boundary tests passed;
- Python: 4 repository tests and 2 execution-boundary tests passed;
- contracts: 7 schemas and 52 records validated; expected counts and unique
  identifiers checked in 3 evaluation manifests;
- integrity: 250 local Markdown links, 183 research hashes, the complete research
  inventory, 2 unchanged ledger snapshots and 71 source identifiers checked;
- baseline secret scan: 294 text files checked with no configured secret or
  machine-path match;
- diagrams: 9 Graphviz sources rendered successfully;
- SBOM: a CycloneDX manifest with 32 components generated successfully.

The baseline scan is a repository safeguard, not a claim of exhaustive secret
or vulnerability detection. The GitHub Actions workflow is prepared but has not
run remotely because this local Stage 0 repository has no remote.

The complete suite was run through Node.js 24.19.0, and a child-process probe
confirmed that pnpm scripts used that LTS runtime.

## Source and generated boundaries

- `docs/research/2026-08-19/research-pack/` is immutable historical evidence;
- `docs/research/2026-08-19/governed-geospatial-research-pack.zip` preserves the
  received archive with SHA-256
  `08ecb65f18f8bef8af0d79dd3c9974da5939544fdecd899e62532c3089798e34`;
- live schemas and fixtures are reviewed adaptations;
- source ledgers are unchanged, byte-compared dated snapshots;
- live diagram sources are reviewed copies;
- `artifacts/`, `dist/`, dependency installations, caches and Python virtual
  environments are generated locally and ignored by Git.

## Decision alignment and deviations

- D01 to D19 are treated as architecture constraints or future-stage decisions,
  not as evidence that their production controls already exist;
- D06 and D17 have Stage 0 contract scaffolds only; protocol conformance and a
  deployable MCP service remain future work;
- D18 is satisfied by a clean repository and selective evidence-led adaptation;
- D19 is satisfied only for Stage 0 and does not authorise Stage 1;
- D20 is superseded by
  [ADR-0002](../decisions/ADR-0002-project-name.md) following the repository
  owner's explicit name decision.

Open-source licensing, third-party attribution and formal name clearance remain
unresolved. They block public publication, but not this local verification gate.

## Rollback

Before any remote is created, rollback is deletion of the new local
`gis-ai-go` directory. The existing `mcp-geo` repository is independent and was
not modified. After later commits, ordinary Git revert or branch removal should
be preferred to history rewriting.
