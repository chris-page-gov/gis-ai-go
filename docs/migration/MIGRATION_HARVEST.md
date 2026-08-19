# MCP-Geo migration harvest

Source: `chris-page-gov/mcp-geo@56683b33c0cd02842b7f3ee465414c68a1f3f2a6`. Do not copy wholesale.

| Asset | Classification | Rationale |
| --- | --- | --- |
| Repository purpose and learning history | preserve only as historical evidence | The repository explicitly describes itself as a learning journal; retain history and release records without making them product authority. |
| Geography-level model and parity contract | retain concept but redesign | Cross-surface geography semantics are valuable; implement as a versioned domain profile and temporal identifier service. |
| OS, ONS, Nomis and LandIS adapters | migrate after testing | Harvest provider-specific error cases and parsers; rewrite behind a common adapter contract with live licence/version checks. |
| Boundary and statistics caches | retain concept but redesign | Useful reference data, but cache entries need entitlement, licence, source checksum, policy and audience metadata. |
| pgRouting route computation | migrate after testing | Deterministic routing is reusable if its network rights, profile contract and tests are re-established. |
| Static map and overlay fallback contracts | retain concept but redesign | Non-App clients need complete results; rebuild against the new map specification and policy model. |
| MCP Apps widgets | preserve only as historical evidence | Use interaction lessons and host fallbacks; rebuild widgets against the stable Apps extension and shared PEP. |
| 2026-07-28 RC protocol work | retain concept but redesign | The experiments anticipated final features; implement afresh against the final specification and official SDK. |
| Tool and resource schemas | migrate after testing | Retain useful field names, examples and errors, but map them into the 12-tool capability model. |
| 103-tool manifest | discard | It documents the old surface and tool proliferation; keep only as evidence in the archive. |
| OWASP control catalogue and locked risk manifest | retain unchanged as evidence; update mappings | High-value assurance evidence and regression inputs. Do not claim current control effectiveness without revalidation. |
| Evaluation questions, fixtures and failure cases | migrate after testing | Use as seed material for the new 25-scenario suite and host interoperability tests. |
| Correlation IDs and provenance fields | retain concept but redesign | Map to Trace Context, canonical audit events and result receipts. |
| FastAPI monolith and dynamic tool registration | discard | It couples protocol, provider, execution and presentation responsibilities and obscures enforcement boundaries. |
| Browser-visible or user-supplied provider keys | discard | Production access must use server-side credential brokerage and enterprise identity. |
| Absolute-path and local-volume assumptions | discard | Replace with portable configuration, managed object storage and explicit local fixtures. |
| Svelte playground and transcripts | retain concept but redesign | A useful developer surface; rebuild as a separate test client and avoid storing sensitive prompts by default. |
| Provider research notes and licences | unresolved pending investigation | Harvest only after each claim is rechecked against current primary sources and dated in the new source ledger. |
