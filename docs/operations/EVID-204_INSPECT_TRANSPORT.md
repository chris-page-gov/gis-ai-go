# EVID-204 evidence inspection transport candidate

- status: accepted inactive transport on protected `main`; not activated or deployed
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decisions: [ADR-0011](../decisions/ADR-0011-durable-public-evidence-ledger.md)
  and [ADR-0012](../decisions/ADR-0012-receipt-only-lost-response-reconciliation.md)
- accepted implementation: [pull request 37](https://github.com/chris-page-gov/gis-ai-go/pull/37),
  protected `main` commit `c4d43f9d0f7af143e01eb3381e5adc4625fac2f0`

## Outcome boundary

This slice connects the accepted transport-neutral `evidence.inspect` application
to the existing direct API and modern MCP HTTP and STDIO candidates. All faces call
the same `createEvidenceInspectApplication` instance over one already opened and
verified `PublicEvidenceLedger`. The later v2 key lookup also closes the application
over that ledger's exact reconciliation-index instance.

The integration is available only through explicit constructor options:

- direct `POST /evidence/inspect` when `enabledApiOperations` includes
  `evidence.inspect` and an `evidenceApplication` is supplied;
- the read-only MCP `evidence.inspect` tool when `enabledOperations` includes it;
  and
- the MCP resource template
  `gis-ai-go://evidence/receipts/{receipt_id}` when `enabledResources` includes
  `evidence.receipt`.

Any face that mounts `data.query` must mount this tool on the same transport and
must supply the application branded with the exact same index as the data
application. Mismatched, legacy and proxy-wrapped pairs fail construction.

The production activation arrays remain empty. The blocked HTTP container opens the
fixed ledger and reconciliation roots only for inactive readiness-integrity checks;
it supplies no inspection application or activation override. The STDIO entry point
also supplies no inspection application or activation override. Readiness remains
`503` with zero active tools and API operations. No listener is published and no
registry entry or deployment is created.

## Contract and parity

The direct API and MCP advertisements use the same closed repository dispatchers.
The unchanged `evidence-inspect-request.schema.json` v1 branch accepts one exact
receipt identity. The additive `gis-ai-go.evidence-inspect-request.v2` branch
accepts exactly `schema`, `source_operation: data.query` and the caller-known
idempotency key. A v2 lookup is available only when the inspector is constructed
with the exact ledger-linked reconciliation index. The generated OpenAPI and MCP
schemas are self-contained projections of the canonical full-checkout schemas; the
gateway build is deliberately not a standalone `dist/` package.

Every successful face returns the same complete object: public evidence record,
hash-chain event, durable storage reference and explicit verification statements.
MCP supplies that object as both `structuredContent` and identical plain JSON text.
The resource returns the same plain JSON text. The current operation result is
`gis-ai-go.evidence-inspect-result.v3`. It contains a dedicated, independently
verifiable current-call `gis-ai-go.evidence-receipt.v3` while retaining the earlier
stored receipt beneath `data.record.receipt`.

The current receipt is constructed only after the server resolves and
restart-verifies an anonymous-open stored target. It binds the current request,
trace, inspection authority and policy decision, safe normalised lookup digest,
exact ledger, receipt, record and event identities, software and transformations,
and a digest of the receipt-free result core. It is inline-only, not persisted or
attested, and creates no ledger record or event. Inspection therefore remains
available when the durable ledger is at its event ceiling.

The v2 key lookup resolves internally to the original v2 receipt and record. It
never returns the reconciliation claim, raw key, public key hash, original
observation or original `data.query` result. The receipt contains only a further
domain-separated digest of safe lookup material. The MCP resource remains only
`gis-ai-go://evidence/receipts/{receipt_id}`; no resource URI accepts or embeds an
idempotency key.

The accepted v1 and v2 request, stored-record, inspection-result and v1/v2 operation
dispatcher contracts remain byte-identical. A separately identified v3 operation
dispatcher returns only the current v3 result.

New v3 timestamps use one canonical UTC millisecond form
(`YYYY-MM-DDTHH:mm:ss.sssZ`). The v3 schemas bound real month lengths, leap days
and time components; runtime verification additionally reuses the established
receipt calendar validator and requires an exact ISO round trip. Historical v1 and
v2 schema bytes and timestamp acceptance are unchanged.

The shared result is bounded so the duplicated MCP compatibility representation,
resource response and direct response all fail closed before transport limits are
crossed. Stored data remains untrusted data, never instructions.

## Controlled failures

| Condition | HTTP status | Public code |
| --- | ---: | --- |
| malformed receipt or v2 key lookup | `400` | `invalid_request` |
| valid receipt identity or v2 key absent from its store | `404` | `evidence_not_found` |
| known claim without verified completion | `503` | `evidence_unavailable` |
| verification, corruption, index or ledger I/O failure | `503` | `evidence_unavailable` |
| unexpected gateway failure | `500` | `internal_error` |

Problem responses contain request and trace identities but never the submitted
receipt or key text, key digest, ledger/index root, machine path, file name or raw
exception. MCP tool
failures use the same problem object in structured and plain-text forms. The MCP
resource-not-found protocol response necessarily echoes its bounded public resource
URI; it contains only the receipt content identity, never a storage path. A resource
verification failure maps to one fixed non-reflective error.

Corruption is never repaired in place. Stop the affected operation, identify the
failed verified root, quarantine the linked ledger and reconciliation index as one
coherent pair, and restore a complete independently verified pair as set out in
[the durable-ledger runbook](EVID-204_DURABLE_LEDGER.md).

## Repeatable verification

From a clean full checkout at the candidate commit:

```bash
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm --filter @gis-ai-go/mcp-gateway run test
pnpm run validate:contracts
pnpm run check
```

The focused suite creates temporary ledger and index roots, persists evidenced
catalogue and data results, reopens and verifies the stores, and then compares
direct API, MCP HTTP, MCP STDIO, resource and plain-text results. It covers v1
receipt lookup, v2 key lookup, absent and incomplete key states, and proves that no
resource URI accepts a key. It also verifies the inline receipt against independent
policy, software, result-core and target-identity material, proves that inspection
does not add a ledger event at capacity, truncates immutable evidence and proves all
affected operation faces return only the controlled unavailable problem. Temporary
machine paths and raw keys are assertions against leakage and are not placed in
fixtures, logs or durable repository evidence.

The transport was accepted through protected pull-request assurance and remains
inactive. No live provider, external identity, OPA service, public deployment or
original query/result replay is part of this procedure.
