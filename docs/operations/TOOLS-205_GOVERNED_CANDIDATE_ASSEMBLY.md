# TOOLS-205 governed candidate assembly

Status: repository candidate; not activated, deployed,
released or registered for production.

Reviewed on 23 August 2026.

## Outcome and authority boundary

The gateway now has one compile-time `candidate-unregistered` assembly for exactly
the five supported read-only operations: `catalogue.search`, `catalogue.describe`,
`evidence.inspect`, `selection.resolve` and `data.query`.

The assembly derives its operation set from the checked-in tool registry and binds
the checked-in anonymous-open policies, one checksum-verified catalogue snapshot,
one exact ONS adapter lifecycle and one linked durable ledger and reconciliation
index. The direct API, MCP HTTP, MCP STDIO and combined Node server constructors all
receive that same branded assembly and its application instances. They cannot add a
planned profile or replace an application, operation array or evidence dependency.
Wrapper option bags and nested host and origin allowlists are copied only from
dense data-property arrays; proxies, accessors and later caller mutation cannot
change the admitted network authority.

This is not production activation. `productionRegistration` is always `false`.
The production activation document and all shipped HTTP, STDIO and container
entrypoints remain unchanged with empty operation arrays. There is no environment,
command-line or serialised activation form, no real provider call, no public
listener and no registry publication.

## Discovery, lifecycle and readiness

The registry's separate candidate projection contains only implemented,
target-active, read-only profiles with accepted request, result and problem
contracts. It does not change `listCurrentCallableTools()`, which remains empty.
Planned operations, including `map.render` and mutating `workflow.execute`, cannot
enter the assembly.

Provider and explicit suspension are subtractive and apply identically to OpenAPI,
MCP HTTP discovery and MCP STDIO discovery:

| Condition | Removed candidate operations |
| --- | --- |
| ONS discovery suspended | `selection.resolve`, `data.query` |
| ONS invocation suspended | `data.query` |
| explicit operation suspension | that operation |
| `evidence.inspect` suspended | `evidence.inspect`, `data.query` |

Any reduced set returns readiness `503` with reason
`relevant-capability-suspended`. Complete evidence corruption returns `503` with
`evidence-integrity-failed`. The exact evidence instances, their runtime-dispatched
methods and captured runtime prototypes are locked before exposure, and provider integrity
is rechecked. A relevant substitution therefore fails readiness and guarded calls
closed. Readiness and health always include
`production_registration: false`; a corrupt or suspended candidate is never
presented as production registered.

Readiness is the whole exact-five candidate gate, not a global blackout of the
advertised subset. Before each call, a per-operation guard re-verifies that the
operation is still advertised and that the evidence and provider dependencies are
intact. A non-suspended operation therefore remains callable with its verified
receipt while readiness is `503`; a removed operation is absent from OpenAPI and MCP
discovery and cannot be called through the direct or MCP face.

MCP resources follow the same lifecycle without becoming substitute operations:
the full-bundle `catalogue.public` resource requires both `catalogue.search` and
`catalogue.describe`, `catalogue.record` requires `catalogue.describe`, and
`evidence.receipt` requires `evidence.inspect`. Suspending one tool cannot retain an
equivalent resource read.

The assembly-specific OpenAPI document describes the mounted candidate paths,
both possible readiness statuses and the `candidate-unregistered` lifecycle. The
ordinary production document remains `candidate-blocked` with no operation path.

## Results, trace and receipt semantics

The server owns every request and W3C trace identity. Every successful exact-five
result carries the current call's request and trace identifiers, allowed policy
decision and independently verifiable receipt. MCP `structuredContent`, compact
plain-text JSON and the direct JSON result are equivalent. STDIO uses the same MCP
factory and result boundary.

`evidence.inspect` now returns `gis-ai-go.evidence-inspect-result.v3` with a
dedicated current-call `gis-ai-go.evidence-receipt.v3`:

- the top-level result, inline receipt and receipt policy decision bind the current
  inspection request and trace;
- policy permits inspection only after the server has resolved and independently
  restart-verified an anonymous-open stored target;
- the receipt binds the exact stored ledger, receipt, record and event identities,
  software and transformations, and a digest of the receipt-free result core;
- receipt-ID and v2 idempotency lookup parameters are represented only by a digest
  of safe normalised material; the raw key and its public key hash are not returned;
- `data.record.receipt` and its request, trace and policy decision remain the
  distinct earlier operation being inspected; and
- the current receipt is inline-only, not persisted, not attested and creates no
  ledger record or event, including when the ledger is already at capacity.

The unchanged v1 and v2 lookup requests still resolve existing v1 or v2 durable
records. Their request and stored-record bytes are unchanged; the new v3 operation
result dispatcher returns only v3. Regression tests make the two trace scopes
unequal and explicit across direct JSON, MCP HTTP, MCP STDIO, receipt resource and
plain-text projections.

This implements issue 23's literal current-call receipt condition in the repository
candidate. Issue closure still requires protected integration assurance; this
candidate does not close or activate it by itself.

## Remaining QUAL-206 and release gates

Issue 24 remains open. Repository fixtures cover the candidate parity and
fail-closed paths, but the following still require their own accepted evidence:

- the official client and exact-version matrix across a real STDIO desktop host
  and remote HTTP host;
- live-host cancellation and unsupported-traffic parity without unexplained
  variance;
- two clean image and artefact builds plus current vulnerability evidence with no
  unresolved Critical or High finding;
- complete accessibility evidence for any human-facing UI or map alternative;
- accepted E01, E02, E09, E13, E15, E17 and E20 evaluation receipts; and
- reviewed activation, deployment, rollback and release authority.

## Focused verification

```bash
pnpm --filter @gis-ai-go/tool-registry test
pnpm --filter @gis-ai-go/mcp-gateway test
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_tool_registry \
  tests.contract.test_gateway_image_contract \
  tests.contract.test_qual_206_local_evaluation_receipts
pnpm run test:qual-206-local-evaluations
```

The full repository and exact clean-image gates remain required before protected
integration. Nothing in this candidate authorises deployment, publication, tagging
or a live ONS request.
