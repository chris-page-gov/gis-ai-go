# EVID-204 evidence inspection transport candidate

- status: local conformance candidate; not activated or deployed
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decision: [ADR-0011](../decisions/ADR-0011-durable-public-evidence-ledger.md)
- protected-main base: `364c8680ad11399e0547a843be2a04da7a737301`

## Outcome boundary

This slice connects the accepted transport-neutral `evidence.inspect` application
to the existing direct API and modern MCP HTTP and STDIO candidates. All faces call
the same `createEvidenceInspectApplication` instance over one already opened and
verified `PublicEvidenceLedger`.

The integration is available only through explicit constructor options:

- direct `POST /evidence/inspect` when `enabledApiOperations` includes
  `evidence.inspect` and an `evidenceApplication` is supplied;
- the read-only MCP `evidence.inspect` tool when `enabledOperations` includes it;
  and
- the MCP resource template
  `gis-ai-go://evidence/receipts/{receipt_id}` when `enabledResources` includes
  `evidence.receipt`.

The production activation arrays remain empty. The shipped HTTP and STDIO entry
points supply no ledger path, inspection application or activation override.
Readiness remains `503` with zero active tools and API operations. No listener is
published and no registry entry or deployment is created.

## Contract and parity

The direct API and MCP advertisements use the same closed repository schemas for
the exact receipt lookup and complete evidence result. The generated OpenAPI and
MCP output schema are self-contained projections of the canonical full-checkout
schemas; the gateway build is deliberately not a standalone `dist/` package.

Every successful face returns the same complete object: public evidence record,
hash-chain event, durable storage reference and explicit verification statements.
MCP supplies that object as both `structuredContent` and identical plain JSON text.
The resource returns the same plain JSON text. The result states that ingest
material was verified but not retained and that no attestation exists.

The shared result is bounded so the duplicated MCP compatibility representation,
resource response and direct response all fail closed before transport limits are
crossed. Stored data remains untrusted data, never instructions.

## Controlled failures

| Condition | HTTP status | Public code |
| --- | ---: | --- |
| malformed or non-receipt lookup | `400` | `invalid_request` |
| valid receipt identity absent from the ledger | `404` | `evidence_not_found` |
| verification, corruption or ledger I/O failure | `503` | `evidence_unavailable` |
| unexpected gateway failure | `500` | `internal_error` |

Problem responses contain request and trace identities but never the submitted
receipt text, ledger root, machine path, file name or raw exception. MCP tool
failures use the same problem object in structured and plain-text forms. The MCP
resource-not-found protocol response necessarily echoes its bounded public resource
URI; it contains only the receipt content identity, never a storage path. A resource
verification failure maps to one fixed non-reflective error.

Corruption is never repaired in place. Stop the affected operation, quarantine the
complete ledger root and restore a complete independently verified copy as set out
in [the durable-ledger runbook](EVID-204_DURABLE_LEDGER.md).

## Repeatable verification

From a clean full checkout at the candidate commit:

```bash
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm --filter @gis-ai-go/mcp-gateway run test
pnpm run validate:contracts
pnpm run check
```

The focused suite creates a temporary ledger, persists an evidenced catalogue
result, reopens and verifies the ledger, and then compares direct API, MCP HTTP,
MCP STDIO, resource and plain-text results. It also truncates an immutable event and
proves all affected operation faces return only the controlled unavailable problem.
Temporary machine paths are assertions against leakage and are not placed in
fixtures, logs or durable repository evidence.

No live provider, external identity, OPA service, public deployment or original
query/result replay is part of this procedure.
