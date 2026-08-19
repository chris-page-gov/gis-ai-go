# Current state: preserve the learning, reset the implementation

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Repository ledger

| Repository | Branch | Commit SHA | Apparent version | Assessment |
| --- | --- | --- | --- | --- |
| chris-page-gov/mcp-geo | main | `56683b33c0cd02842b7f3ee465414c68a1f3f2a6` | 0.8.2 | historical research prototype and learning journal |
| chris-page-gov/okf-explorer | main | `c8af0b05cab49a5341e0b787e17d49a674868d3a` | 0.7.0 | canonical experimental Explorer application and profiles |
| chris-page-gov/okf-ons | main | `b0283b0d0dd2bbd06a8311dd5d1342eea0c36fdf` | post-0.2.0 main | metadata-only ONS domain discovery pack |
| chris-page-gov/okf-LandRegistry | main | `4580c9e4afef10a102b852b01083ee5cb7d34018` | 0.3.0 proof of concept | metadata-only HMLR worked example |
| GoogleCloudPlatform/knowledge-catalog | main | `e7e4660d14586e6bf39a94ec47de6fb1c43b8dfd` | OKF 0.2 | current normative OKF specification |
| modelcontextprotocol/modelcontextprotocol | main | `4df2d6b6e3588efb46e7542d98498e5c630a0a86` | 2026-07-28 | current final MCP specification and documentation |
| modelcontextprotocol/typescript-sdk | main | `3924de99df834302d89f5997a1b64ca268282284` | v2 line | official TypeScript SDK |
| modelcontextprotocol/python-sdk | main | `0d92192765fa7d6a20fbfe7e62e242e44933574f` | active main | official Python SDK |
| webmachinelearning/webmcp | main | `9c7ce3e35e9124e46c4f21fc12dce38b9a5753b9` | community group draft | draft browser-resident tool API |
| OAI/Arazzo-Specification | main | `fc140d26c440291b0061c62a53e45a8fb07cc369` | 1.1.0 | workflow description specification |

## What the present prototype proves

**Verified fact.** MCP-Geo combines OS, ONS, Nomis and LandIS access, boundary/statistics caches, PostGIS/pgRouting, MCP Apps experiments, static map fallbacks, structured outputs, correlation identifiers, an evaluation harness and an OWASP-oriented tool manifest. Its package is version 0.8.2, uses Python 3.11/FastAPI and records 103 tools. [S-MCP-GEO]

It also records a valuable cross-surface lesson: adding a geography type is not a local adapter change. It affects aliases, code inference, hierarchy, selection, statistics, cache, UI, export, audit and host behaviour. That lesson becomes a versioned geography domain profile and parity test in the successor.

## Why a reset is safer

The current repository puts protocol adaptation, provider access, computation, presentation and local data assumptions close together. This makes it difficult to prove that discovery, credential selection, cache reads, map rendering and exports all pass through the same policy enforcement and evidence path. The successor needs explicit trust boundaries from the outset.

**Recommendation.** Mark the existing repository as historical learning evidence. Do not delete it, rewrite its history or present it as deprecated production software. Create a new repository after decision approval and migrate only reviewed assets.

## Forensic harvest matrix

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

## Reuse rules

1. Every migrated parser or algorithm gets a source reference, new interface contract, licence review, malicious-input tests and deterministic fixtures.
2. Every migrated test is classified as provider conformance, protocol conformance, security, accessibility, performance or regression.
3. No `.env`, provider credential, licensed data payload, local absolute path or generated cache is copied.
4. Historical protocol and Apps experiments remain evidence, not current authority; live specifications and official SDKs control implementation.
5. The 103-tool manifest is retained in the archived repository as evidence of tool proliferation. The successor starts from the 12-tool catalogue in [`data/tool-catalogue.json`](../data/tool-catalogue.json).

## Material gaps in the current prototype

- no end-user OIDC/OAuth authority chain;
- no trusted device posture or organisational entitlement model;
- no policy-filtered discovery;
- no portable PDP or obligation enforcement;
- no physical open/PSGA/commercial isolation;
- no transaction-bound permits;
- no result receipt tying policy, data versions, CRS transforms, software and outputs;
- no durable workflow authority independent of an LLM plan;
- no clear product boundary between discovery, control, execution, evidence and presentation.

These gaps are architectural, not defects to close by adding more endpoints to the same server.
