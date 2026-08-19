# MCP, WebMCP and Apps: small capabilities, explicit boundaries

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Runtime recommendation

Use a TypeScript gateway on the official MCP SDK, pinned to a reviewed release/commit implementing MCP 2026-07-28. Use a Python geospatial execution service behind an internal OpenAPI/typed message contract. This is the smallest two-runtime split that gives the control plane current MCP/OAuth strengths and the execution plane mature geospatial libraries. [S-MCP-TS] [S-MCP-PY]

A Python monolith is simpler to deploy but would mix identity, protocol and policy with geospatial dependencies. A TypeScript monolith reduces runtimes but weakens the deterministic geospatial ecosystem. More microservices are not justified for the initial scale.

## Primitive mapping

| Concept | Primary surface | Additional publication |
| --- | --- | --- |
| Datasets/collections/versions/licences/status | MCP resources | OKF, OGC Records/DCAT/STAC |
| Schemas/CRS/code lists/geographies | MCP resources | OKF and provider-native schema |
| Deterministic query/spatial/statistical/routing/export actions | MCP tools | Direct OpenAPI/OGC API where appropriate |
| Saved selection or explicit state handle | Resource/state store reference | Workflow state, not hidden server session |
| Long-running job | MCP Task | Workflow definition and evidence receipt |
| Interactive map/inspector/approval | MCP Apps | Complete non-UI tool result |
| Multi-step process | Arazzo plus `workflow.execute` | Tasks/MRTR for protocol interaction |
| Policy/provenance record | MCP resource with authorised view | OKF reference and evidence store authority |

## Twelve-tool capability model

| Tool | Purpose | Tiers | Principal risks |
| --- | --- | --- | --- |
| catalogue.search | Search policy-visible OKF and provider catalogue records. | open<br>PSGA<br>commercial | Unauthorised capability disclosure<br>prompt injection in metadata |
| catalogue.describe | Return a richly linked record, relationships, rights, freshness and source evidence. | open<br>PSGA<br>commercial | Protected metadata disclosure<br>stale record |
| selection.resolve | Resolve human or agent intent into a non-executing, provider-native selection plan. | open<br>PSGA<br>commercial | Intent injection<br>selection of unavailable dataset |
| data.query | Execute a bounded provider-native or cached data query and return a canonical result envelope. | open<br>PSGA<br>commercial | Data exfiltration<br>expensive query<br>provider limit breach |
| spatial.locate | Resolve coordinates, identifiers or place text and return containing/current/historic geographies. | open<br>PSGA<br>commercial | Sensitive location inference<br>false precision |
| spatial.analyse | Run deterministic spatial operations such as intersect, buffer, nearest, join or aggregate. | open<br>PSGA<br>commercial | Pathological geometry<br>inference<br>DoS<br>licence contamination |
| statistics.compare | Compare statistical observations across compatible geographies, periods or groups. | open | Invalid denominator<br>suppression disclosure<br>incomparable vintages |
| route.plan | Plan a deterministic route using an approved network and routing profile. | open<br>PSGA<br>commercial | Unsafe route interpretation<br>network licence leakage<br>location sensitivity |
| map.render | Render a deterministic map specification or static image from policy-approved layers. | open<br>PSGA<br>commercial | Protected feature leakage<br>missing attribution<br>visual misrepresentation |
| artefact.export | Create a governed downloadable result with manifest, expiry and audience constraints. | open<br>PSGA<br>commercial | Bulk exfiltration<br>licence breach<br>long-lived signed URL |
| evidence.inspect | Retrieve the policy decision, source lineage, transformations and receipt for an operation. | open<br>PSGA<br>commercial<br>auditor | Audit data privacy<br>evidence tampering |
| workflow.execute | Start or resume a registered, policy-approved workflow and return explicit state. | open<br>PSGA<br>commercial | Workflow confusion<br>replay<br>approval bypass<br>partial side effects |

Discovery returns only capabilities visible to the current authority context. Within a workflow, the gateway discloses only tools relevant to the current stage and permitted resources. A denied client need not learn that a protected dataset or action exists.

## Statelessness and explicit state

Requests do not rely on server affinity. Selection, workflow and task state use explicit opaque handles bound to actor, client, policy version, purpose and expiry. Catalogue ordering and cursors are deterministic. Cache hints state scope: public/shared, organisation, user/transaction or no-store. Per-request client metadata is verified rather than trusted blindly.

## WebMCP comparison

| Mechanism | Primary purpose | Adoption decision |
| --- | --- | --- |
| OKF | Structured knowledge, discovery, provenance and policy description | Core |
| WebMCP | Page-provided browser tools | Open read-only experiment |
| MCP | Remote/local AI-host access to tools and resources | Core agent interface |
| MCP Apps | Server-provided interactive UI in supporting hosts | Optional after core |
| OpenAPI/OGC API | Direct application/data contracts | Core service contracts |
| Arazzo | Explicit multi-step API workflow | Core workflow description |
| Static JSON/JSON-LD | Portable machine-readable publication | Core fallback/publication |

Fallback order for a browser agent is: WebMCP page tool when supported; linked JSON/OKF/JSON-LD; public API; remote MCP; visible HTML. Scraping and copy/paste are last-resort user actions, not the designed integration.

## Apps contracts

Proposed Apps: map, feature/place inspector, geography selector, statistical comparison, provenance viewer, policy explanation, export review and approval request. Widgets call the same gateway and PEP, receive only policy-projected data and cannot create a second credential or data path.
