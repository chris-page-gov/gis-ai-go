# ADR-0018: A private Sites pilot for bounded OS and ONS retrieval

- status: proposed experimental architecture; implementation and deployment
  authorised by the owner, acceptance pending
- date: 1 October 2026
- decision owner: Chris Page
- work package: [WEB-216 #125](https://github.com/chris-page-gov/gis-ai-go/issues/125)
- pilot increment: [issue #138](https://github.com/chris-page-gov/gis-ai-go/issues/138)
- release target: owner-private experimental pilot, not supported `v0.2.0`

## Context and authority

On 1 October 2026 the owner authorised progressing the existing private Sites
deployment into a native MCP experiment with OS and ONS API data, common-question
tests and a repeatable evaluation harness. The owner requested unattended work,
visible progress, capability review and usage tracking. The owner supplied
entitlement context for private assessment; organisation, account, credential and
usage details remain private. No new paid service or chargeable overage is
authorised; use open data when protected-data admission cannot be established.
A private test ingress token is authorised if required, with no implied
equivalence to signed-in-owner OAuth.

These instructions permit implementation and a bounded private deployment. They
do not themselves establish every provider licence condition, platform control
or acceptance result. Record unresolved prerequisites without stopping
independent open-data development. Keep the original private Site and audience.

The [capability matrix](../operations/SITES_MCP_CAPABILITY_MATRIX.md) separates
documented capability, current readback, inspected source and tests still needed.
In particular, the previous publication has no native MCP declaration. A browser
route and successful browser sign-in are not proof of direct-client MCP support.

## Proposed architecture

Add a separately named experimental live-pilot assembly with closed tool, input,
result, provider and receipt contracts. Its own entrypoint and manifest identify
the pilot and its experimental status. Do not add tools to, rename tools in or
relax the exact-five public candidate. Do not activate the inactive generic
production registries. Preserve the existing static Explorer, LOCAL-212/214,
legacy demonstration and captured-CPIH workbench behaviour.

Use the existing Site's Workers-compatible runtime and `DB` binding. Native MCP,
manual controls and any page tools call the same admitted application functions.
The exact supported native MCP declaration must come from current official
documentation or implementation. Do not guess manifest keys or treat accepting
a same-origin HTTP route as native MCP registration.

The initial executable capabilities are:

| Capability | Bounded question class | Required interpretation boundary |
| --- | --- | --- |
| OS Open Names lookup | Find a named place and show its source-native identifier, type and coordinates; identify ambiguity between similarly named places. | A place point is not a property address, UPRN match, boundary containment or jurisdiction decision. |
| OS open-product metadata | Read current source metadata for an admitted open product. | Product metadata is not a dataset download, property lookup or feature-level result. |
| ONS MSOA name/code lookup | List at most five MSOA 2021 names and native codes matching a name prefix in England and Wales. | Preserve explicit incompleteness and vintage. A name match is not point containment, a population observation or UK-wide geography coverage. |
| Maintained ONS CPIH | Retrieve admitted periods from L522/MM23 and compare published index observations using deterministic arithmetic. | Preserve index unit and base year. A percentage change derived from two index values must be labelled as that calculation, not as a different published inflation series. |
| Pilot evidence inspection | Show the recorded source, observation time, licence, request bounds and result digest for a successful pilot call. | A receipt establishes recorded material and checks; it does not guarantee independent source authenticity or legal fitness. |

Exact advertised names and schemas belong to the implementation's closed
manifest. Discovery cannot add capabilities. A later OS/ONS spatial join needs
its own reviewed geography vintage, coordinate reference system, transformation,
boundary source and failure tests; it is not implied by the initial providers.
No LLM performs deterministic geospatial or statistical calculations. No embedded
model request is required: the owner's connected client is the interpretation
layer.

## Rights and provider admission

Treat entitlement, API authentication, product licence, allowed purpose, hosting
permission, storage permission and onward transmission to an AI client as
separate checks. Owner-only access reduces the audience; it does not answer all
these questions. Sites currently provides no data-residency guarantee. Do not
derive a rights conclusion from the presence of a working API key.

Start with OS Open Names and ONS open data under verified current terms and
attribution. A protected PSGA capability remains unavailable until its exact
product and use are covered by recorded authority, including relevant third-party
processing and client/model transmission conditions. Never persist licensed
payloads in public Git, fixtures, documentation, logs or public evaluation
artefacts. The repository may record a non-secret admission decision and source
terms; private entitlement evidence remains private.

Fallback is explicit. If an address-specific PSGA query is unavailable, explain
the missing capability and offer a place-name search only if that answers a
different useful question. Never silently substitute open place data for an
authoritative address or protected dataset. Authentication and quota failures
must not become synthetic successes.

All provider invocation uses fixed server-authored hosts, paths and bounded
parameters. Reject arbitrary URLs, redirects, credentials in input, unknown
fields and oversized requests/results. Apply deadlines and cancellation. Fetch
allowlisting is an application control; it does not claim the previous Node
pinned-address transport, platform-wide egress denial or non-static workload
identity is reproduced on Sites.

## Identity, secrets and allowance

Preserve Sites owner-only access and test the actual identity contract for native
MCP. Trust only the platform-supported authenticated identity at its verified
ingress boundary. Reject missing identity or an unauthorised user. Caller-written
headers, query parameters and a test ingress bearer are not owner identity.
Use exact returned OAuth endpoint/resource metadata. No claim of client support
is made until that client completes its own authenticated MCP test.

While the native declaration remains blocked, a separately labelled ordinary
MCP endpoint at `/pilot/mcp` may support private test access through the additional
`x-sites-pilot-test-token` header. Compare its hash with a server-configured
SHA-256 value and retain the unchanged Sites private ingress boundary. Test
credentials must never be reflected into evidence or error messages. This mode
can provide transport, provider and performance observations; it cannot pass the
native declaration, OAuth, signed-in-owner or independent-client acceptance gates.

Keep the OS key in server runtime secret storage. Never place it in browser
bundles, a manifest, Git, URLs returned to clients, public receipts or logs.
Document rotation and revocation without publishing a secret or local location.

Use a central D1-backed allowance shared by all pilot entrypoints and Worker
instances. Atomically reserve an attempt before provider egress, including any
retry. Deny when the allowance is exhausted, its record cannot be verified or
accounting storage fails. Cancellation, provider errors and uncertain completion
do not refund an issued attempt. Request limits, concurrency, deadlines and
response-byte limits remain separately enforced.

Set explicit numeric application bounds in the reviewed pilot configuration and
evaluation profile. Record OS transaction allowance, ONS request allowance,
hosting limits and Codex usage separately. A near Codex reset does not enlarge
provider entitlement. An application call counter is not a proven platform
financial stop. Disable an affected provider if chargeable overage cannot be
excluded within the admitted plan. Never enable automatic paid top-up.

## Storage and evidence

Use a new, clearly namespaced set of pilot D1 tables for allowance and receipts.
Do not migrate, clear, initialise, adopt or reuse `web216_cpih_snapshot` for live
data. Keep the captured-data receipt family and its existing verification rules
unchanged. Schema changes must be additive and reviewed against older deployed
versions before publication.

The pilot receipt records bounded inputs, admitted provider/product, licence,
source-native identifiers, observation and retrieval times, response digest,
transformation, source/deployment identity and measured execution phases. Store
only fields permitted by the selected provider's terms. Minimise private query
content and identity. A successful material result requires the required receipt
to be persisted and inspectable; persistence uncertainty must be visible.

Define retention and implement deletion before claiming either. A retention
field is not an operational guarantee. An independently retained checkpoint is
needed to detect restoration of an older valid database. Describe backup,
restoration, code rollback and data rollback as distinct operations. Do not
claim POSIX durability, independent rollback detection or a recovery objective
from local D1 tests alone. R2 is unnecessary unless a later accepted requirement
needs permitted object storage.

## Evaluation and deployment gates

Maintain a versioned common-question corpus with expected capability, bounded
arguments, source/semantic assertions and expected refusal cases. Keep live
observations separate from deterministic fixture tests. Evaluate at least place
ambiguity, unavailable protected data, unsupported period, invalid input,
provider timeout/error, exhausted allowance, receipt failure and unauthorised
access as well as successful OS and ONS questions.

The harness must exercise the actual MCP wire protocol for a deployed-service
claim. A direct function call or browser-only request is labelled accordingly.
Report per-run sample size, success/refusal/error counts, phase timings, p50/p95
and maximum latency, bytes, concurrency, source freshness and provider attempts.
Report cold/warm assumptions and client/network/model overhead separately. Never
turn a small bounded pilot into a throughput or cost guarantee. Retained
evaluation output must be publishable; redact credentials, personal identifiers
and restricted data before committing summaries.

Acceptance proceeds through distinct recorded gates:

1. Current supported Worker packaging, closed schemas, rights admission and
   threat/policy tests. Native declaration is a separate unresolved capability;
   it does not block the explicitly labelled ordinary guarded MCP test route.
2. Meaningful local runtime, provider-boundary, atomic accounting, persistence,
   cancellation and hostile-input checks; independent review.
3. Exact source push, saved version, private deployment, terminal status and
   unchanged-audience readback.
4. Record the actual authentication mode. Native acceptance requires MCP
   declaration readback, supported OAuth discovery and authenticated owner calls;
   Codex and independent-client observations remain separate. A guarded
   test-token route may proceed experimentally with these native gates pending.
5. Bounded live OS and ONS evaluation with durable inspectable receipts and
   measured performance. Missing provider authority blocks only that provider.
6. Persistence across redeployment, independent checkpoint comparison, explicit
   code rollback and separately observed data restoration.
7. Required canonical repository assurance and a reconciled status/handover
   identifying every passed, failed, unavailable and pending gate.

Private deployment approval is already supplied by the owner; routine next-stage
permission is not a gate. A missing schema, credential, rights condition or
platform capability remains a real prerequisite. A stronger model or a newer
OpenAI feature does not replace executable or deployment evidence.

## Consequences and unchanged boundaries

This pilot provides a practical route to learn native Sites MCP behaviour and
OS/ONS performance without asserting equivalence to full DEPLOY-207. It creates
additional code, policy, evidence and operational acceptance obligations. The
owner must be able to stop provider requests, revoke credentials and retain
permitted evidence before recovery or rollback.

The supported product stays `v0.1.0`; no stable `v0.2.0` release or public service
is authorised by this experimental result. Existing DEPLOY-207 OCI, exact-five,
filesystem, identity, egress, budget and public-HTTPS gates remain intact. The
local evaluation edition's separate acceptance also remains intact. EVID-211
preservation is unchanged by this task; normal implementation notes and test
receipts do not alter its scheduling or establish its current operational state.
The immutable research pack and read-only source repositories are unchanged.
