# Evaluation baseline

The 25 research evaluation cases and 30 research risks are dated inputs to the future
programme. Stage 0 checks their expected record counts, unique identifiers and source
references; it does not fully schema-validate these manifests or mark future service
scenarios as passed.

`stage-0-tests.json` is the executable Stage 0 manifest. Later stages must create
evidence receipts rather than changing unchecked boxes in the research copy.

## QUAL-206 repository-only preflight

`qual-206-local-evaluation-receipts.v1.json` contains deterministic supporting
receipts for exactly E01, E02, E09, E13, E15, E17 and E20. The generator executes
selected application, transport and static Explorer tests against checked-in
fixtures, then binds the test names and repository materials by SHA-256.

Generate or verify the receipts with:

```bash
pnpm run generate:qual-206-local-evaluations
pnpm run test:qual-206-local-evaluations
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_qual_206_local_evaluation_receipts
```

The [receipt schema][qual-206-receipt-schema] is closed. Every receipt is
repository-only, non-live and unscored, with `case_complete` fixed to `false`.
These receipts do not complete the research cases or authorise a provider call,
host session, activation, deployment, registration or release.

[qual-206-receipt-schema]: ../schemas/qual-206-local-evaluation-receipt-set.schema.json

## QUAL-206 local protocol matrix

[`qual-206-local-protocol-evidence-matrix.v1.json`][protocol-matrix] is a
separate, compact record of the protocol evidence already present at runtime base
commit `7fa8b720d3cbaa3e0a1ebfadf0fb355a7330a04c`. It binds the exact gateway
source, transport tests, gateway manifest and lockfile bytes. Its four rows
distinguish the pinned official MCP client 2.0.0 from independent raw JSON-RPC
coverage over HTTP and STDIO, including the 2026-07-28 protocol, cancellation and
unsupported traffic.

The accompanying assembly regression checks every provider or explicit tool
suspension through `startGovernedCandidateStdio` and raw JSON-RPC over an in-memory
transport. It verifies reduced tool and resource discovery, a valid call to a
remaining advertised catalogue operation, rejected calls to all suspended
operations and zero provider calls. This is in-process STDIO server wiring, not
operating-system pipe framing or desktop, remote-host or live-provider evidence.

Run the focused checks with:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
node --test apps/mcp-gateway/dist/test/qual-206-local-protocol-matrix.test.js
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_qual_206_local_protocol_evidence_matrix
```

The [matrix schema][protocol-matrix-schema] fixes every live, host, activation,
deployment, registration, scoring and release claim to `false`. This record does
not alter or supersede the frozen interoperability corpus or earlier evaluation
receipts.

[protocol-matrix]: qual-206-local-protocol-evidence-matrix.v1.json
[protocol-matrix-schema]: ../schemas/qual-206-local-protocol-evidence-matrix.schema.json
