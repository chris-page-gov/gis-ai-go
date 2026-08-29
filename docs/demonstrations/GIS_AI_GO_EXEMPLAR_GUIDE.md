# GIS AI GO as a governed MCP exemplar

Illustrated local demonstration and implementation report, 29 August 2026.

## Read this first

GIS AI GO is a credible **exemplar candidate**, not an approved UK government
standard or a supported public MCP service. The supported public release is still
the static [`v0.1.0` Explorer](https://chris-page-gov.github.io/gis-ai-go/).

Protected `main` at
[`c7eca721`](https://github.com/chris-page-gov/gis-ai-go/commit/c7eca721b084356dace8f264d7531b2180093b2d)
proves an unregistered local `v0.2.0` candidate with five read-only operations. It
does not prove public hosting, a live provider call through this candidate,
production operations, registry publication or a `v0.2.0` release. This report
keeps those states separate.

![The local exact-five demonstration passes while remaining an unregistered
candidate](assets/local-exact-five-demo.svg)

The terminal panel is a reconstructed illustration of the verified output shown
later in this report. The command and its tests are the evidence; the illustration
is not an execution receipt.

### What you need to know

- A **closed assembly** is the one fixed set of operations from which discovery,
  requests, readiness and documentation are derived. **Fail-closed** means that a
  missing or damaged control removes capability instead of quietly allowing it.
- The **direct API** is the ordinary HTTP interface over the same application
  behaviour. **STDIO** carries MCP messages through a client-managed process's
  standard input and output rather than a public network listener.
- `ttlMs` says how long discovery information may be reused; `cacheScope` says who
  may reuse it. Neither field means that the service is publicly deployed.
- An **idempotency key** identifies one intended provider operation.
  **Reconciliation** recovers its receipt after an uncertain response without
  executing the provider call again.
- An **OCI image** is the deployable container artefact; its **SBOM** lists included
  software. A **provider-admission lease** is a short, one-shot reservation that
  bounds concurrent first attempts before an immutable claim is created.

## What makes the approach distinctive

The implementation combines several ideas that are often treated separately:

1. **OKF is the knowledge plane.** It publishes portable, reviewable descriptions of
   datasets, providers, rights, capabilities and evidence. It does not become a
   runtime authority.
2. **MCP and the direct API are interfaces, not the governance regime.** Both derive
   from one closed assembly and the same server-owned policy, lifecycle and evidence
   state.
3. **Governance is executable.** Schemas, source locks, lifecycle states, negative
   tests, receipts, image attestations and release gates determine what can be
   discovered and called.
4. **Deterministic work stays deterministic.** Selection and geospatial calculation
   are implemented and tested in code rather than delegated to a language model.
5. **Claims travel with proof.** Every demonstrated call has structured data, an
   equivalent plain-text result, trace and policy information, and a verifiable
   receipt. The first four durable receipts can be challenged through
   `evidence.inspect`; the inspection call's own receipt is inline-only and
   independently verifiable rather than stored for another lookup.
6. **Safety is subtractive and fail-closed.** A suspended dependency disappears from
   discovery, damaged evidence blocks readiness, and an exhausted local claim store
   refuses new claim-bearing `data.query` work while preserving existing-key and
   evidence recovery.

These strengths are supported within their stated boundary by the
[source-by-source findings matrix](../research/2026-08-23/agentic-ai-governance-review/SOURCE_FINDINGS_MATRIX.md).
The survey results in that intake are respondent-reported context, not proof of this
implementation. The unofficial draft is research, not policy or instruction.

## The supported public starting point

![The static Explorer explains that INSPIRE polygons are indicative and are not
legal boundaries](assets/public-explorer-inspire-boundary.png)

The supported `v0.1.0` Explorer gives people a durable, accessible view of the same
reviewed catalogue knowledge. This example answers a common land question in plain
English, identifies HM Land Registry as the source authority and keeps the GIS AI GO
normalised projection separate from legal advice. It contains metadata only and
makes no provider request.

## The governance model in one picture

![Six linked controls connect knowledge and semantics to evidence and
assurance](../research/2026-08-19/research-pack/assets/diagrams/six-control-spine.svg)

The architecture illustrations in this report are retained from the immutable
19 August research pack. They show responsibility and target-direction views, not a
claim that every depicted component is deployed today.

The six-control spine prevents a familiar mistake: treating a successful tool call
as sufficient assurance. A result is supportable only when the knowledge, authority,
workflow, interface, computation and evidence controls agree.

For a beginner, the distinction is simple:

- **OKF says what exists and what is known about it.**
- **Policy says what this caller and release may do.**
- **MCP or the direct API carries the request and result.**
- **Deterministic code performs the calculation.**
- **A receipt records what actually happened.**

## MCP 2026-07-28 changes used by this candidate

The historical `mcp-geo` repository was a valuable learning journal with a broad
103-tool surface. GIS AI GO harvests its lessons but does not copy that shape. It
defines 12 governed capability profiles and admits exactly five to the local
read-only candidate.

The
[MCP 2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
changes several protocol assumptions an older implementer may bring. This table is
deliberately limited to changes exercised by the local candidate:

| Earlier implementation instinct | GIS AI GO and MCP 2026-07-28 practice |
| --- | --- |
| Initialise a transport session and retain an `Mcp-Session-Id`. | Each request is self-contained. `server/discover` provides optional up-front discovery. |
| Route by inspecting a long-lived connection or JSON body. | Streamable HTTP carries `Mcp-Method` and applicable `Mcp-Name` routing headers, checked against the body. |
| Treat a tool list as indefinitely fresh. | Discovery and list results carry explicit `ttlMs` and `cacheScope`; the local candidate returns zero-TTL, public-scope cache hints. |
| Expose every implemented function as a tool. | Keep a small composable surface; use resources for descriptions and admit tools only when their evidence gates pass. |
| Let each transport construct its own behaviour. | MCP HTTP, MCP STDIO, direct API, OpenAPI and readiness derive from one immutable assembly. |
| Trust client or server self-description as identity. | Treat client metadata as attribution only; authority is a separate server-owned contract. |
| Return a useful answer and log it later. | Return structured and plain-text parity plus an issue-time receipt; persist and inspect evidence through a separate contract. |
| Retry an uncertain provider call. | Claim the idempotency key first; reconcile a lost response by receipt without duplicating execution. |

This is not a complete migration checklist. The
[official SDK migration guide](https://ts.sdk.modelcontextprotocol.io/v2/migration/support-2026-07-28)
also covers multi-round-trip request state, authorisation opt-ins, per-era wire
codecs, `subscriptions/listen` and migration away from deprecated 2025-era Tasks
wire vocabulary. The anonymous read-only demonstration does not exercise those
features.

Tool names remain canonical dotted names on the MCP wire, for example
`catalogue.search`. Claude Code's observed permission surface converts dots to
underscores. The bounded host harness collision-checks that presentation alias; it
does not rename the public protocol operation.

## The exact-five local candidate

![Core components separate discovery, policy, execution and
evidence](../research/2026-08-19/research-pack/assets/diagrams/components.svg)

Text equivalent, from left to right: OKF discovery index → policy-filtered registry
→ MCP tools and resources → authority context and permit → provider adapter →
deterministic computation → canonical result → evidence receipt.

The local candidate contains exactly these operations:

| Operation | What the demonstration uses it for | Important safety property |
| --- | --- | --- |
| `catalogue.search` | Find reviewed public catalogue records. | Closed query contract and policy-filtered results. |
| `catalogue.describe` | Inspect one record, its rights and provenance. | Source-locked OKF content rather than model invention. |
| `selection.resolve` | Rank or report ambiguity between candidates. | Deterministic; no LLM performs the selection. |
| `data.query` | Return one bounded ONS-shaped aggregate observation. | Approved dataset/version/dimensions only; no arbitrary URL, SQL or provider. |
| `evidence.inspect` | Verify a receipt from an earlier result. | Separate lookup contract; the receipt cannot be inferred or substituted. |

Three MCP resources expose governed catalogue, record and receipt descriptions.
Seven other versioned profiles remain planned and absent from discovery. In
particular, mutating `workflow.execute` is deferred beyond the anonymous read-only
tier.

## Demonstration: 15 minutes from context to proof

### Before the meeting

Use Node.js `24.19.0`, pnpm `10.33.2`, Python 3.12 or later and uv `0.12.2`. To
reproduce the report's exact clean baseline without disturbing another checkout,
first create and enter a disposable Git worktree, then install dependencies there:

```bash
git fetch origin
git worktree add ../gis-ai-go-demo-c7eca721 \
  c7eca721b084356dace8f264d7531b2180093b2d
cd ../gis-ai-go-demo-c7eca721
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
git status --short
git rev-parse HEAD
```

Do not add a provider key. The demonstration neither needs nor uses one. The demo
prints the exact commit and either `clean` or `with local changes`. A dirty run can
help explain the journey, but it is not accepted repository evidence.

### Run it

```bash
pnpm run demo:local
```

The observed protected-main run at `c7eca721` completed in under four seconds after
dependencies were present. It rebuilt the 36-record OKF projection and started the
closed exact-five fixture over real operating-system STDIO pipes. The following is a
curated excerpt of its key outcomes; a healthy run also prints its source, transport,
provider boundary and truncated receipt identities:

```text
OS network isolation: not enforced; this demonstration is not a network sandbox
1. Discovery — exactly 5 tools verified
2. Resources — 3 governed resources verified
3. catalogue.search — passed; receipt verified
4. catalogue.describe — passed; receipt verified
5. selection.resolve — passed; receipt verified
6. data.query — passed; fixture observation 10471
7. evidence.inspect — passed; linked receipt verified
Boundary: candidate-unregistered; production_registration=false
Result: PASS
```

When the demonstration is finished, return to the original checkout and remove the
exact disposable worktree:

```bash
git worktree remove ../gis-ai-go-demo-c7eca721
```

Receipt identifiers are content-addressed. They repeat when the source and every
receipt-bound input are identical, and change when any bound material changes. The
demonstration identities are still local evidence, not permanent release evidence.

### Follow one request into its proof

The demonstration sends this closed operation request after discovery and resource
checks:

```json
{
  "name": "catalogue.search",
  "arguments": {"query": "INSPIRE", "limit": 1}
}
```

The verifier requires one returned record with the source-native ID
`hmlr:dataset:inspire-index-polygons`, source authority, public access,
`open-with-conditions` rights and current freshness. It also requires:

- `structuredContent.operation` to remain `catalogue.search`;
- the plain-text content to be the exact JSON serialisation of that structured
  result;
- request and trace identities to agree across the result, policy decision and
  receipt;
- a default-deny policy decision with `allow-with-obligations` for this call;
- SHA-256 receipt verification to pass; and
- the receipt to be persisted before the success is accepted.

The fifth operation then calls `evidence.inspect` with that exact search receipt ID.
It must verify the retained search receipt and return its own distinct inline-only
receipt. The verifier independently recomputes both receipt identities; a reused or
mismatched receipt fails the journey.

### Suggested run-of-show

| Time | Show | Explain |
| --- | --- | --- |
| 0–2 minutes | The public Explorer. | People and agents share the same governed discovery corpus; the site is the supported v0.1 product. |
| 2–5 minutes | The six-control and component diagrams. | OKF, MCP, policy, providers and evidence have distinct responsibilities. |
| 5–9 minutes | `pnpm run demo:local`. | Discovery is exact-five, selection is deterministic and every call yields verifiable evidence; the first four durable receipts are inspectable. |
| 9–12 minutes | The receipt and evidence-flow diagram. | A plausible answer is not enough; the system must reconstruct source, policy, transformation and output identity. |
| 12–15 minutes | The boundary and roadmap. | Local proof is real, but public hosting, a fresh live-provider result through the deployed candidate and operational acceptance are still gates rather than claims. |

If time is short, start with the final `Boundary` and `Result` lines. They illustrate
the project's central discipline: a passing test does not silently widen the release
claim.

## How one request becomes evidence

![An open-tier request passes through policy, deterministic data and evidence before
returning](../research/2026-08-19/research-pack/assets/diagrams/open-tier-sequence.svg)

The gateway does not bolt audit data onto an answer afterwards. Authority, policy,
provider version, transformation, software and result identities are inputs to an
issue-time receipt.

![Evidence connects the request and policy decision to the result and later
challenge](../research/2026-08-19/research-pack/assets/diagrams/evidence-flow.svg)

Text equivalent, from left to right: request and trace → authority context → policy
decision → tool or provider call → transformation → output hash → evidence receipt
→ append-only store → later challenge and reconstruction.

The durable ledger and reconciliation index address a difficult failure mode: a
provider may finish while the caller loses the response. A repeated idempotency key
must not execute again. Instead, `evidence.inspect` can recover the receipt while the
original result remains deliberately unavailable.

## Governance as code: where to look

| Question | Repository evidence |
| --- | --- |
| What capabilities exist? | [`profiles/tool-registry.v1.json`](../../profiles/tool-registry.v1.json) and its closed schema. |
| What is admitted locally? | [`governed-assembly.ts`](../../apps/mcp-gateway/src/governed-assembly.ts) and [`candidate-activation.ts`](../../apps/mcp-gateway/src/candidate-activation.ts). |
| How are rights and public authority represented? | [`okf/`](../../okf/) and versioned public authority/policy schemas under [`schemas/`](../../schemas/). |
| How are results constrained? | Operation-specific input/output schemas and transport parity tests in [`apps/mcp-gateway/test/`](../../apps/mcp-gateway/test/). |
| How is uncertain execution handled? | The reconciliation index in [`packages/evidence/`](../../packages/evidence/) and [ADR-0012](../decisions/ADR-0012-receipt-only-lost-response-reconciliation.md). |
| How is risk challenged? | The [Stage-2 threat model](../threat-model/QUAL-206_STAGE_2_RELEASE.md), evaluation cases and hostile-mutation tests. |
| How is the image trusted? | The [DEPLOY-207 container runbook](../operations/DEPLOY-207_GATEWAY_CONTAINER.md), independent derivation and GitHub attestations. |
| How are claims stopped from outrunning evidence? | [`CONTEXT.md`](../../CONTEXT.md), [`PROGRESS.md`](../../PROGRESS.md), release-readiness checks and milestone gates. |
| How are delivery agents constrained? | [`AGENTS.md`](../../AGENTS.md), short-lived branches, independent review and protected-main checks. |

The local 4,096-claim ceiling is a fail-closed repository safety bound, not a
production quota. Before a new immutable reconciliation claim is created, the data
path reserves a bounded provider-admission lease. If no new claim can be admitted,
`/readyz` reports `503 reconciliation-capacity-exhausted`; `/healthz`, existing-key
reconciliation and evidence inspection remain available. A real deployment still
needs shared admission, rate, storage and operator controls.

## Two meanings of “agent”

GIS AI GO keeps two different concerns separate:

- A **runtime agent** is an AI client or delegated process proposing a tool call.
  It is not trusted merely because it is intelligent or because its client metadata
  has a recognisable name. The gateway owns policy, validates the closed request and
  emits the receipt.
- A **delivery agent** helps change the repository. Its instructions, reasoning or
  apparent worker count are not product evidence. A change counts only when its
  bounded output is reviewed, committed, tested and accepted through the protected
  repository gates.

The current `v0.2.0` candidate is anonymous and read-only, so it contains no
delegated authority or human approval service. The following diagram shows the
**later protected-tier direction**, not deployed current behaviour.

![A future delegated action carries human purpose through policy, approval and a
transaction permit before execution](../research/2026-08-19/research-pack/assets/diagrams/delegated-agent-sequence.svg)

This distinction matters when evaluating an agentic software process: count useful,
independently verified outcomes rather than messages, attempts or nominal agents.
The separate project retrospective will analyse delivery efficiency; it is not a
reason to weaken the product gates.

## What the research supports — and what it does not

The 23 August intake supports five especially relevant conclusions:

- governance must surround the route from knowledge and authority to execution,
  evidence and recovery;
- declared policy is weaker than demonstrated, exact-commit evidence;
- MCP interoperability does not decide whether an action is lawful, authorised or
  proportionate;
- capability lifecycle and policy-filtered discovery matter as much as invocation;
  and
- incident categories should become adversarial tests, not marketing statistics.

GIS AI GO implements those ideas unusually coherently for a small public repository.
That makes it useful as an exemplar for discussion. It does **not** establish a
government owner, legal basis, service assessment, security accreditation or
organisational operating model. Those cannot be generated from an unofficial draft,
a vendor-sponsored survey or successful local tests.

## Static Sites, WebMCP and the persistent runtime

The Explorer can continue on GitHub Pages or another static-site host. OpenAI's
[Site tools documentation](https://learn.chatgpt.com/docs/webmcp) and
[demonstration video](https://youtu.be/Is2NHa7awWY) describe WebMCP support in the
ChatGPT desktop browser. GIS AI GO now implements that idea as a separate
[WebMCP Explorer candidate](../implementation/WEBMCP_EXPLORER_CANDIDATE.md): a
compatible browser-hosted AI can call exactly two bounded, read-only page tools
over the same validated public catalogue that a person can inspect manually.

That is page-level capability, not a replacement server. Availability still depends
on a compatible account, model and browser host. The page must stay open, and the
candidate does not itself embed or call a model. The
[WebMCP Community Group draft](https://webmachinelearning.github.io/webmcp/) is not
a W3C Recommendation and does not prescribe MCP's transport or data layer. The
candidate therefore remains behind one feature-detected adapter, and no live-host
interoperability claim is made without an exact, version-bound observation. On
29 August 2026, the owner-only Sites deployment passed both page-tool calls through
Codex built-in-browser Site tools and passed the native imperative page API in
Chrome `152.0.7977.64` and Edge Stable `152.0.4191.53` in the exact observed local
environment; the Edge API-enablement mechanism was not established. The separate
Gemini-in-Chrome session exposed no page-tool bridge. Edge DevTools and an Edge
AI-host bridge were not tested, so no Copilot or general Edge Stable claim follows. See
the [version-pinned WebMCP run-through](WEBMCP_EXPLORER_RUN_THROUGH.md) for the
compatibility matrix, screenshots and strict claim boundaries.

Neither static hosting nor WebMCP replaces the stateful server-side needs of this
candidate: durable receipts, reconciliation, controlled provider egress, workload
identity, operational limits, monitoring, backup and rollback. The website and MCP
runtime are complementary deployment planes.

## Proven now and still to prove

| State | Evidence-backed position on 29 August 2026 |
| --- | --- |
| Supported public product | Immutable `v0.1.0` static Explorer. No public MCP service. |
| Proven local candidate | Exact-five MCP 2026-07-28 over STDIO, direct/API parity, deterministic ONS-shaped fixture, receipts, suspension, bounded admission/readiness and reproducible attested OCI image. |
| Client evidence | Accepted bounded Claude Code local-STDIO and ChatGPT secure-tunnel exact-five observations; neither is a live provider or public service. |
| Still required for v0.2.0 | A selected public HTTPS runtime and hostname, numeric spend ceiling, workload identity/TLS/egress, persistent storage and operations, fresh live ONS evidence through the exact deployed candidate, remote acceptance, suspension and exact-image rollback. |
| Later direction | Protected authority and policy, bounded delegation, permits/approval where justified, synthetic consequential workflows, and richer protected receipts. |

The current release sequence is therefore:

1. deploy the exact attested image as an **unregistered** public candidate;
2. collect fresh live-provider evidence through that exact candidate plus QUAL-206
   security, persistence, interoperability and rollback evidence;
3. reconcile the five-tool implementation acceptance;
4. prepare the version-only release change, tag the exact verified commit and deploy
   those exact bytes;
5. publish the collision-checked registry identity only after the deployed release
   passes again; and
6. merge a final support-evidence update.

The first DEPLOY-207 image criterion is complete in
[issue 25](https://github.com/chris-page-gov/gis-ai-go/issues/25). The remaining
steps need an actual provider/hostname and numeric spending ceiling. Until then,
the honest demonstration is the local candidate above.

## Beginner glossary

- **OKF:** a portable Markdown/YAML knowledge format used here for reviewed
  descriptions and provenance.
- **MCP:** the protocol used by an AI client to discover resources and call tools.
- **Tool:** a bounded operation with a versioned input and output contract.
- **Resource:** descriptive content an MCP client can read without treating it as an
  action.
- **Policy decision:** the server-owned reason an operation is allowed or denied.
- **Receipt:** a content-bound record of the request, policy, sources, software,
  transformation and result.
- **Readiness:** whether the service may safely accept new work; it is deliberately
  stricter than basic process health.
- **Attestation:** signed provenance that binds an artefact to a source and build
  process.

## Evidence and source notes

- Protected-main [CI run 33237523106](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33237523106)
  and [CodeQL run 33237523042](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33237523042)
  are the exact acceptance evidence for `c7eca721`.
- The 23 August findings matrix records an earlier implementation baseline. This
  report refreshes operational status from `PROGRESS.md`, the merged activation and
  the exact protected-main runs; it does not rewrite the preserved research.
- The AvePoint/Osterman PDF remains local and Git-ignored because it is not
  redistributable. No page or image from it is reproduced here.
- The original unofficial draft remains local because it contains personal and
  collaboration metadata. Its privacy-scrubbed derivative and the supplied advisory
  Markdown remain research sources, not instructions or government approval.
- Protocol migration statements are checked against the official MCP 2026-07-28
  release and SDK migration guide. WebMCP statements are checked against OpenAI's
  announcement, site-tools guidance and the current Community Group draft; the
  proposed experiment remains page-level rather than a runtime claim.

For the complete operator boundary, use the
[local demonstration runbook](../operations/QUAL-206_LOCAL_DEMONSTRATION.md). For
live status, use [`PROGRESS.md`](../../PROGRESS.md); a report is never a substitute
for current execution evidence.
