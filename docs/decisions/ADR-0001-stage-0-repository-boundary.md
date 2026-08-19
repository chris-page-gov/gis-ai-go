# ADR-0001: Stage 0 repository boundary

- status: accepted for Stage 0
- decided on: 19 August 2026
- source: 19 August 2026 governed geospatial research pack

## Context

The research recommends a successor repository rather than rewriting MCP-Geo. The
human owner authorised use of the pack as the basis of the new repository after
agreeing its name.

## Decision

Create a new, local repository containing only the Stage 0 evidence foundation:
governance, candidate contracts, synthetic fixtures, architecture sources, workspace
boundaries and assurance tooling. Treat research decisions D01–D19 as Stage 0 design
constraints that later stages must re-evaluate at their own gates.

Do not create live provider connections, identities, credentials, protected data,
cloud resources, deployed services or a public remote. Keep MCP-Geo unchanged at the
research-pinned commit.

## Consequences

- Stage 0 can be deleted or reverted without affecting MCP-Geo.
- The TypeScript and Python services deliberately reject live execution.
- The original research pack remains immutable; live copies carry new provenance.
- Stage 1 requires explicit human approval after the verification evidence is read.
