# WebMCP Explorer candidate

Status: experimental implementation candidate; not a supported release or
deployment.

Work item: [WEB-210](https://github.com/chris-page-gov/gis-ai-go/issues/101).

Decision: [ADR-0013](../decisions/ADR-0013-webmcp-page-tools-boundary.md).

## Purpose

This candidate tests one focused proposition: a person's own compatible AI can
interpret a question and call narrow tools on the page they are viewing, while GIS
AI GO keeps catalogue validation, data selection and source tracing deterministic.

It is both a working demonstration and a research instrument. The implementation
makes the practical boundary visible rather than describing a hypothetical product.
It does not add WebMCP to the supported public Explorer and does not expand the
`v0.2.0` persistent MCP release.

The primary references are:

- [OpenAI Site tools documentation](https://learn.chatgpt.com/docs/webmcp), for the
  currently supported ChatGPT browser surface and its limitations; and
- the [WebMCP Community Group draft](https://webmachinelearning.github.io/webmcp/),
  for the proposed browser API, tool annotations and cancellation contract.

WebMCP is a Community Group draft, not a W3C Recommendation. As at 29 August 2026,
OpenAI's built-in browser supports imperative tools registered from a top-level
page. It does not support declarative form tools or tools registered in iframes.
Compatibility is therefore an observed capability, not a universal browser
assumption.

## Goals

- Show a browser-hosted AI translating natural language into bounded tool arguments.
- Search and describe the same checksum-verified public OKF catalogue used by GIS AI
  GO.
- Reuse the shared catalogue parser and search functions rather than create a second
  semantic implementation.
- Make authority, access, rights, freshness, source records and limitations visible
  to both the person and the AI.
- Demonstrate progressive enhancement: the page remains a complete manual teaching
  aid when WebMCP is unavailable.
- Establish a testable security and accessibility pattern for future page-tool
  research.
- Explain where a page tool stops and the persistent MCP gateway begins.

## Non-goals

This candidate does not:

- embed, purchase or call an AI model;
- accept or store a model API key, provider credential or user identity;
- implement `data.query`, `selection.resolve`, `evidence.inspect` or any other
  gateway operation;
- call ONS, HMLR, LandIS or a licensed provider;
- issue a policy decision, provider receipt, durable receipt or ledger event;
- persist a call, query, result or browser session;
- keep working after the page closes or navigates away;
- claim MCP transport or `v0.2.0` protocol conformance;
- register in an MCP registry;
- change the supported `v0.1.0` Explorer or canonical GitHub Pages artefact; or
- establish production deployment, capacity, service ownership or support.

## Why this is part of this repository

The candidate belongs in `apps/webmcp-explorer` because it uses the repository's
canonical generated catalogue and `@gis-ai-go/contracts` package. Keeping it beside
those sources lets CI detect semantic drift and allows reviewers to compare the
page-tool and gateway boundaries in one change.

A new repository would create a second catalogue supply chain, lock file and
assurance boundary without adding useful isolation at this stage. Reconsider a
separate repository only if the candidate later gains an independent owner,
deployment, support lifecycle or release programme.

The supported `apps/public-explorer` remains unchanged and independently useful.

## Architecture

```text
Person asks a question in a compatible AI host
                    |
                    v
AI selects a registered page tool and prepares JSON arguments
                    |
                    v
       Static WebMCP adapter on the open page
                    |
              validates again
                    |
                    v
  Shared catalogue parser and deterministic search code
                    |
                    v
   Checksum-copied public OKF catalogue in the artefact
                    |
                    v
Compact page result returned to the AI and shown in the page
```

The AI host owns the probabilistic step. GIS AI GO owns the deterministic input
validation, catalogue lookup and structured result. The candidate makes no request
to an AI or data provider.

### Build-time path

1. The canonical OKF build produces the public catalogue and checksum ledger.
2. The candidate's data-preparation step verifies the source tree before copying
   it into the static application.
3. The built-artefact checker verifies the copied inventory, checksums, marker,
   Content Security Policy and same-origin executable assets.
4. The result is an ordinary static artefact. No server function is required.

### Runtime path

1. The page fetches `./catalogue/okf-bundle.json` from its own origin.
2. `@gis-ai-go/contracts` parses and validates the complete bundle.
3. Only after successful validation, the adapter checks for
   `document.modelContext.registerTool` on the top-level page.
4. A supported browser receives exactly two static tool registrations.
5. The executable handler validates every call independently of the JSON Schema.
6. The shared deterministic catalogue functions produce a compact result.
7. The same result is returned to the AI and rendered visibly as text for the
   person.
8. Closing or navigating away from the page aborts the registrations. Nothing is
   retained.

If any catalogue or registration step fails, tool registration stops. The page does
not select substitute data or contact another source.

## Tool contracts

The tools deliberately use page-specific names. They must not be presented as the
persistent gateway's canonical operation or result contract.

### `explorer_search_catalogue`

Purpose: search validated public catalogue metadata and return at most five compact
records.

Input:

| Field | Requirement |
| --- | --- |
| `query` | Required non-empty string; at most 256 characters and 10 normalised terms |
| `facets` | Optional non-empty object using only the governed facet fields |
| `limit` | Optional integer from 1 to 5; default 5 |

The governed facet fields are `types`, `authority`, `access`, `rights`, `freshness`
and `tags`. Their enumerations and array sizes are closed and bounded. Unknown
fields, duplicate values, unsupported control characters and unsupported enum
values are rejected.

The result identifies:

- the `gis-ai-go.webmcp-page-result.v1` schema;
- the page tool and related `catalogue.search` gateway intent;
- catalogue identity, revision and record count;
- total, returned and truncated match information;
- at most five compact records; and
- the explicit page boundary.

### `explorer_describe_record`

Purpose: describe one exact record already present in the validated catalogue.

Input:

| Field | Requirement |
| --- | --- |
| `record_id` | Required exact source-native identifier; at most 512 characters |

No fuzzy identifier resolution is performed. An absent record is a fixed
`record_not_found` application error.

The result adds the record's full authority, access, rights, freshness and status,
plus bounded limitations and linked source records. It does not dereference an
external source URL or call a provider.

### Shared result boundary

Every successful result states:

| Claim | Value |
| --- | --- |
| Data scope | Validated public catalogue metadata only |
| Page-scoped | `true` |
| Provider call | `false` |
| Durable receipt | `false` |
| Persistent service | `false` |
| Visible page update | `true` |

Both registrations set `readOnlyHint: true` and `untrustedContentHint: true`. These
are hints to the user agent, not replacements for validation, browser review or
human judgement.

## What the candidate can and cannot demonstrate

| Question | WebMCP candidate | Persistent MCP gateway |
| --- | --- | --- |
| Can a person's AI map a question to a narrow call? | Yes, in a compatible host | Yes, through a configured MCP client |
| Must the page remain open? | Yes | No, when the service is deployed |
| Can the person and AI inspect the same visible interface? | Yes | Not inherently |
| Does it search validated public catalogue metadata? | Yes | Yes |
| Does it call a foundational data provider? | No | Designed to, after admission gates |
| Does it create durable evidence? | No | Designed to |
| Does it support later evidence inspection or lost-response recovery? | No | Designed to |
| Does it prove the AI's answer is correct? | No | No; evidence can support review |
| Does static hosting deploy the persistent MCP service? | No | No |

This is the main lesson of the demonstration. WebMCP is useful at the visible
presentation plane. A persistent MCP service is still needed for background access,
provider execution, governed receipts and recovery.

## Threats and controls

OpenAI's documentation treats website-provided tool definitions and results as
untrusted. The candidate also treats the AI-generated call arguments as unknown
input.

| Threat | Candidate control | Residual boundary |
| --- | --- | --- |
| Tool poisoning through data-derived metadata | Exactly two static, code-authored registrations | The host still decides whether to select a tool |
| Prompt injection in catalogue text | `untrustedContentHint`; compact results; visible text rendering | The AI and person must not treat catalogue prose as instructions |
| Over-parameterisation leaks unrelated conversation data | Narrow closed schemas; no personalisation, URL or free-form instruction fields | A person can still put sensitive text in `query`; the interface warns against it |
| Schema-only validation bypass | The handler repeats exact-key, type, bound, enum and complexity checks | Browser mediation is not an authorisation system |
| Cross-origin or provider exfiltration | Same-origin catalogue only; restrictive Content Security Policy; no provider code | The hosting origin and build supply chain still require assurance |
| Persistent query history | No cookies, storage, analytics or page-side call history | The person's AI host may retain its own conversation under its policies |
| Hidden background execution | Page-lifetime registration and cancellation; no worker or service | A future service needs a separate decision and controls |
| Misleading evidence claim | Separate result schema and explicit false boundary fields | An AI can still summarise badly; the visible result supports checking |
| API or browser implementation drift | One adapter, feature detection and exact-host observation gate | The draft can change and compatibility can regress |

The candidate does not accept identity, credential, file, callback, origin, selector,
provider or persistence inputs. Adding any such field requires a new threat review
and decision rather than a loose schema extension.

## Accessibility and manual fallback

WebMCP is progressive enhancement, not the only route through the demonstration.
The page provides:

- a visible status for catalogue validation and Site tools availability;
- a labelled manual search form using the same `executePageSearch` function;
- buttons that use the same `executePageDescribe` function;
- live-region status updates that do not rely on colour;
- keyboard and touch-operable controls with visible focus;
- structured semantic headings, lists, definition lists and a table;
- a compact JSON view for inspecting what the AI receives;
- a narrow-width layout and horizontal containment for the comparison table;
- reduced-motion and forced-colours support; and
- catalogue and checksum downloads plus an architectural explanation when
  JavaScript is off.

An unsupported browser must say that Site tools are unavailable while leaving the
manual journey fully usable. A registration failure must fail closed in the same
way. The manual route is part of acceptance, not a temporary developer control.

## Demonstration

### Build and run

From the repository root:

```bash
pnpm run build:webmcp-explorer
pnpm --filter @gis-ai-go/webmcp-explorer run preview
```

Open the local preview URL in an ordinary browser to verify the manual route. Use a
compatible AI host only for the page-tool part of the demonstration.

### Manual journey

1. Confirm the catalogue status shows a validated record count, version and
   revision.
2. Confirm the Site tools status either reports two read-only tools or clearly
   reports that the browser does not support them.
3. Search for `ONS population data`.
4. Inspect the bounded record cards and compact JSON.
5. Choose **Describe record and sources** for the most relevant record.
6. Inspect authority, access, rights, freshness, limitations and linked source
   records.
7. Confirm the result boundary says there was no provider call, durable receipt or
   persistent service.

### Compatible-host journey

1. Open the same exact candidate build in the supported built-in browser.
2. Inspect the available Site tools and confirm that only
   `explorer_search_catalogue` and `explorer_describe_record` are registered.
3. Ask:

   > Find the ONS provider capability for population data. Describe the most
   > relevant record, its sources and its limitations.

4. Review each proposed call and its structured arguments before it runs.
5. Confirm the search result appears visibly in the page.
6. Confirm the describe result names the exact searched record and linked source
   records.
7. Inspect the AI's explanation against the structured result. Do not treat fluent
   prose as evidence by itself.
8. Close or navigate away from the page and confirm its tools are no longer
   available.

Record the exact commit, built artefact digest, host and application version, model
where relevant, date, tool count, arguments, result boundary and outcome. A mocked
browser test does not replace this observation.

## Acceptance criteria

### Source and build

- The candidate remains under `apps/webmcp-explorer` and does not change the
  supported Explorer's runtime.
- The generated catalogue is excluded from Git and copied only after source-tree
  checksum and inventory verification.
- The built artefact contains only allowlisted regular files, expected executable
  assets and no source maps.
- The Content Security Policy and executable assets permit only the required
  same-origin static runtime.

### Contract and security

- Exactly the two named tools register after catalogue validation.
- Tool metadata, schemas and annotations are static and tested.
- Executable validation rejects wrong types, extra fields, excessive length or
  complexity, invalid facets, duplicates, control characters and missing records.
- Both handlers honour the supplied cancellation signal.
- A call makes no external request and writes no cookie, `localStorage` or
  `sessionStorage` value.
- Result fields always preserve the explicit page boundary.

### Browser and accessibility

- Manual search and describe journeys pass in the repository browser runner.
- A controlled WebMCP adapter test proves discovery, execution and visible result
  rendering without claiming live-host interoperability.
- Unsupported and failed-registration paths retain the complete manual journey.
- WCAG 2.2 A and AA automated checks, keyboard journeys and 320 CSS-pixel reflow
  checks pass.
- No unexpected console error or network request occurs.

### Evidence and claims

- The candidate is labelled experimental in the interface and documentation.
- Any compatible-host claim is bound to an exact commit and recorded observation.
- No page, pull request, issue or demonstration describes the candidate as the
  supported `v0.2.0` MCP service, a provider integration or a durable evidence
  system.

## Hosting and release boundary

The candidate is static and may later be hosted on an HTTPS origin that can serve
its same-origin catalogue. That could make the page available to a compatible
browser-hosted AI. It would not deploy or replace the persistent MCP gateway.

This implementation does not change the canonical GitHub Pages artefact. Do not add
it to the supported Pages package or `v0.2.0` release merely because the local
demonstration passes. Publication needs a separate exact-commit artefact and:

- rights and provenance verification;
- security, accessibility and real-browser acceptance;
- a compatible-host observation;
- an explicit URL and support statement;
- rollback evidence; and
- confirmation that the persistent gateway remains a separate deployment.

Static Sites or Pages hosting is suitable for this page-scoped candidate. It cannot
provide a persistent MCP listener, provider admission lease, evidence ledger or
background execution. Those remain in the gateway's deployment and release gates.

## Follow-on research

After this candidate has exact-host evidence, evaluate:

- whether other supported AI hosts implement the same imperative contract;
- whether tool selection remains reliable across representative beginner questions;
- whether users understand the difference between AI interpretation, catalogue
  metadata and foundational data;
- whether compact results contain enough provenance without inviting prompt
  injection or unnecessary disclosure;
- how browser and specification changes affect the adapter; and
- whether any future write or provider-backed page tool has a defensible authority,
  confirmation, evidence and recovery model.

Do not expand the callable surface during that evaluation. Any provider-backed,
identity-bearing, persistent or mutating tool is a new architecture and threat
decision, not a larger version of this static demonstration.
