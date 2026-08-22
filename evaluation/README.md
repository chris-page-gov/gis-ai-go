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
