---
type: Index
title: Findings
description: Index of findings in the research pack.
generated:
  by: process:research-pack-builder
  at: '2026-08-19T13:30:00+01:00'
---

# Findings

- [F01: MCP 2026-07-28 is the final baseline](f01.md) — The successor should not inherit MCP-Geo’s default 2025-11-25 runtime. The 2026-07-28 final specification provides the current stateless, routable and self-describing baseline.
- [F02: MCP-Geo is explicitly a learning journal](f02.md) — The repository presents itself as personal research and not production code or a formal proposal. Its 103-tool manifest and broad coupling make it evidence to harvest rather than the successor skeleton.
- [F03: OKF 0.2 is Markdown/YAML, not a JSON runtime schema](f03.md) — The normative core is a directory of Markdown concepts with YAML frontmatter. Explorer descriptors, JSON-LD, YAML-LD and sharded indexes are additive application/publication conventions.
- [F04: Keep OKF descriptive](f04.md) — OKF should describe providers, datasets, capabilities, licences, policies, workflows, lineage, trust, freshness and attested-computation interfaces while referring to runtime authorities.
- [F05: WebMCP remains a draft](f05.md) — WebMCP is a Community Group draft with active API changes and unresolved browser security and lifecycle questions.
- [F06: Constrain WebMCP to open read-only operations](f06.md) — Use it only for catalogue search, facets, record inspection, relationships, map selection and current-view evidence in the demonstrator.
- [F07: ChatGPT Sites is not the protected path](f07.md) — Sites is a beta surface; UK availability and data/inference residency must be checked per current official documentation. It does not evidence the controls needed for PSGA or commercial data.
- [F08: OS OAuth is provider project authentication](f08.md) — For relevant OS APIs, OAuth uses client credentials. It authenticates a project/workload; it does not create delegated user authority.
- [F09: Broker upstream credentials server-side](f09.md) — The platform should authorise the human/agent action itself, then select an organisation-owned provider credential. Provider tokens must not reach browsers or unauthorised clients.
- [F10: HMLR is not one open tier](f10.md) — Price Paid Data is open with additional address-field rights, while title, official-copy, Business Gateway and licensed bulk services have separate access and fee conditions.
- [F11: LandIS provides open discovery but record rights remain specific](f11.md) — The 2026 open-access portal and OGC Records interface support machine discovery. Each product record must still carry its own licence, scale and fitness-for-purpose evidence.
- [F12: ONS data, geography and Nomis are distinct provider lanes](f12.md) — They have different identifiers, interfaces, update cycles, licensing details and statistical/geographic semantics. A single “ONS adapter” would hide important differences.
- [F13: Use deterministic geospatial software](f13.md) — Containment, intersection, transformation, routing, simplification, aggregation and rendering should be performed by tested libraries/services, not inferred by the language model.
- [F14: Treat cache as a governed subsystem](f14.md) — Every cache entry needs provider, dataset/version, source checksum, retrieval time, licence, entitlement, policy version, transformation, expiry, audience and permitted operations.
- [F15: Filter discovery as well as invocation](f15.md) — The policy enforcement path must cover catalogue search, MCP capability listing, workflow initiation, provider credential selection, attribute projection, map generation, export and audit access.
- [F16: Allow decisions should carry obligations](f16.md) — Examples include attribution, feature limits, aggregation, masking, reduced resolution, no persistent export, approval, cost controls, retention and destination constraints.
- [F17: Return a result-level evidence receipt](f17.md) — Every material result should bind actor chain, policy decision, sources, versions, CRS/transformation parameters, software, output hashes, licence obligations and trace context.
- [F18: Do not treat an LLM plan as workflow authority](f18.md) — Use Arazzo or a deterministic workflow model for governed multi-step processes; use Tasks and MRTR for protocol interaction and approval/resumption.
- [F19: Separate the public plane from protected services](f19.md) — A portable static public discovery plane and separate authenticated control/data plane give a safer initial topology than one shared multi-tier deployment.
- [F20: Initial protected users are Entra-managed](f20.md) — The Azure recommendation assumes the first public-sector pilot can use Entra federation and Intune/Conditional Access posture.
- [F21: The first pilot is departmental, not national-scale](f21.md) — Sizing assumes tens to low hundreds of concurrent users, bounded exports and reference datasets in the tens to hundreds of gigabytes before tile artefacts.
- [F22: Exact PSGA cache and derived-output conditions](f22.md) — These must be confirmed against the organisation’s current OS agreements and selected products before any protected cache is loaded.
- [F23: Actual departmental landing zone](f23.md) — Azure is the default recommendation, but the sponsoring organisation’s approved cloud, network and monitoring services may change deployment details.
- [F24: Enterprise-managed authorisation host support](f24.md) — MCP EMA is stable as an extension, but end-to-end support must be tested for each target host and enterprise identity environment.
- [F25: Formal clearance for Locus Accord](f25.md) — Preliminary search found no exact GitHub repository conflict, but package registries, domains, UKIPO and common-law product usage require formal checks.
- [F26: Preserve temporal identifiers](f26.md) — UPRN, BLPU, USRN, TOID, OSID and ONS geography codes need source, namespace, validity interval, successor/predecessor relations and provider-native attributes.
- [F27: Use WGS84 for interchange and EPSG:27700 for GB metric work](f27.md) — Record source CRS, axis order, transformation operation/software and output CRS. Do not silently convert coordinates.
- [F28: Govern emergency controls across registry, credentials, agents and evidence](f28.md) — Suspension must include service/tool registry, credential revocation, workflow cancellation, cache quarantine, agent quarantine, evidence freeze and rollback.
- [F29: Keep the public pack usable without JavaScript](f29.md) — The static site should progressively enhance a readable HTML/Markdown evidence pack, with keyboard operation and WCAG 2.2 AA acceptance tests.
- [F30: Use an integrated OpenAI/development workflow](f30.md) — Use Deep Research for current evidence, GitHub-connected analysis for repositories, this static pack for decisions, Codex for staged implementation, and Codex Security after code exists. No newer single capability replaces the evidence-synthesis role.
