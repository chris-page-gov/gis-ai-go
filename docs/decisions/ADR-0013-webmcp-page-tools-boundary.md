# ADR-0013: WebMCP page-tools boundary

- status: accepted; experimental
- date: 29 August 2026
- decision owner: Chris Page
- work item: [WEB-210](https://github.com/chris-page-gov/gis-ai-go/issues/101)
- release target: none

## Context

GIS AI GO needs a small demonstration of how a person's own browser-hosted AI can
turn a natural-language question into bounded calls over governed foundational
metadata. The supported static Explorer already lets a person inspect the public OKF
catalogue, while the `v0.2.0` programme is building a persistent MCP gateway with
provider admission, policy and durable evidence.

[OpenAI Site tools](https://learn.chatgpt.com/docs/webmcp) implement the proposed
WebMCP browser API. A compatible AI can discover tools registered by the page that
the person is viewing. The tools belong to that page and can become unavailable when
the page closes or navigates away. OpenAI's current implementation supports
imperative registration from a top-level page, but not declarative form tools or
tools registered inside an iframe.

The [WebMCP Community Group draft](https://webmachinelearning.github.io/webmcp/)
defines tool names, descriptions, JSON Schema inputs, an execution callback,
annotations and cancellation. It is a Community Group draft, not a W3C
Recommendation. Its surface and browser support can therefore change.

Page tools and persistent MCP solve related but different problems. Giving a page
the gateway's canonical operation names or result contracts would imply transport,
policy, provider execution and durable evidence that the page cannot provide.
Making the supported Explorer depend on WebMCP would also remove its existing
ordinary-browser and no-integration guarantee.

## Decision

Add an experimental, standalone static component at `apps/webmcp-explorer`. Keep it
in this repository because it consumes the same generated catalogue and shared
`@gis-ai-go/contracts` search and parsing code. Do not alter the supported
`apps/public-explorer` application or its canonical GitHub Pages artefact.

Register exactly two read-only tools from the top-level page, and only after the
same-origin catalogue has passed the shared bounded parser:

- `explorer_search_catalogue` searches validated public catalogue metadata using a
  bounded query and optional governed facets, returning at most five compact
  records; and
- `explorer_describe_record` reads one exact catalogue record and returns its
  authority, access, rights, freshness, limitations and linked source records.

The `explorer_` prefix and underscore names are deliberate. They identify a
presentation-plane capability and do not claim the canonical gateway operations
`catalogue.search` or `catalogue.describe`. A page result may name the related
gateway operation for teaching, but uses the separate
`gis-ai-go.webmcp-page-result.v1` contract.

The page will:

- feature-detect `document.modelContext.registerTool` and fail closed if it is not
  available;
- register static, code-authored names, descriptions and schemas through one
  isolated adapter;
- set both `readOnlyHint` and `untrustedContentHint` to `true`;
- validate unknown fields, bounds, enumerations, control characters, duplicate
  values and query complexity again in executable code;
- honour the execution and registration cancellation signals;
- use only the checksum-copied, validated public OKF catalogue and shared
  deterministic catalogue functions;
- return compact JSON-serialisable metadata and mirror the result into the visible
  page using text-safe rendering;
- make no external runtime request; and
- preserve a keyboard, touch and screen-reader accessible manual search and
  describe journey that uses the same application functions.

The page does not embed or call a model. The person's compatible AI host owns the
probabilistic question-to-tool interpretation. The page receives only structured
arguments, validates them deterministically and reads the local catalogue. It uses
no model API key, provider credential, cookie, browser storage, analytics or stored
call history.

## Capability boundary

This candidate can demonstrate:

- an AI choosing between narrow page tools while the person sees the same page;
- natural language being reduced to bounded, inspectable structured arguments;
- deterministic catalogue search and source tracing over governed public metadata;
- progressive enhancement without a separate MCP-server installation; and
- a complete manual teaching journey when WebMCP is unavailable.

It cannot provide or evidence:

- a service that remains callable without the page being open;
- `data.query`, provider admission or live ONS, HMLR, LandIS or licensed data calls;
- the persistent MCP transport, its exact supported tool set or protocol
  conformance;
- a policy decision, durable receipt, evidence ledger, later evidence inspection
  or lost-response reconciliation;
- identity, authorisation, registry publication, service capacity, production
  deployment or rollback; or
- the correctness of the host AI's interpretation or final explanation.

The result boundary must state that the data scope is validated public catalogue
metadata only and that the call is page-scoped, makes no provider call, creates no
durable receipt and uses no persistent service.

## Threat controls

Tool metadata and results are untrusted content. The browser's review of a call is
an additional user control, not proof that the page or output is safe. The candidate
therefore applies the following controls:

- exactly two static tool registrations; no data-derived or record-derived tool
  name, description or schema;
- closed JSON Schema inputs plus matching executable validation;
- public metadata only, with copy asking people not to enter personal information;
- small length, term, facet and result-count bounds;
- no arbitrary URL, free-form instruction, provider, credential, file, selector,
  origin, callback or persistence parameter;
- same-origin catalogue fetches and a restrictive Content Security Policy;
- text rendering rather than interpreting returned catalogue values as markup;
- explicit `untrustedContentHint` on both results; and
- cancellation and page-lifetime disposal, with no background or cross-page work.

These controls bound the candidate; they do not turn WebMCP output into trusted
policy or evidence.

## Acceptance and publication

Repository acceptance requires deterministic unit and build-boundary tests,
malicious-input tests, a regular-file-only and checksum-verified catalogue copy,
browser journeys for both tools and the manual fallback, WCAG 2.2 AA checks, narrow
viewport and keyboard checks, no unexpected network request, no browser storage and
a fail-closed unsupported-browser journey.

An exact compatible-host observation is required before making a public claim that
an AI client interoperates with the candidate. Local mocks prove the adapter
contract, not host support. The claim must identify the tested browser or AI host,
application version, model where relevant, exact commit, date and outcome.

Static hosting may publish the validated candidate because all executable data and
logic are in the page artefact. Hosting it does not deploy the persistent MCP
gateway. This decision makes no change to the canonical GitHub Pages artefact, the
supported `v0.1.0` product, `v0.2.0` scope, provider activation, registry status or
release readiness. A future publication requires its own exact-commit build,
security, accessibility, browser, rollback and support evidence.

## Consequences

- Research and implementation remain together as one reviewable experiment rather
  than becoming a detached speculative report.
- The candidate can share catalogue semantics without sharing the gateway's stronger
  contracts or release claims.
- The manual journey keeps the educational value and public metadata available in
  browsers that do not support WebMCP.
- Browser API change is contained in one adapter and cannot silently alter the
  canonical Explorer or persistent gateway.
- A separate repository is not justified while the candidate relies on the same
  contracts, catalogue and assurance. Reconsider that boundary only if it gains an
  independent owner, support lifecycle, deployment or release programme.
- Provider execution and durable evidence remain in the persistent gateway. They
  must not be added to this static page through direct browser-side credentials or
  an implied proxy.
