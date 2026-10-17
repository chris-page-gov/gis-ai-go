# Architecture review verification

This record covers the documentation and inline-comment change built from
baseline `97bc45635a91064cd78f06bf0848ad7636f05439`. It is local review evidence,
not a release attestation or a substitute for the repository's mandatory CI.
Commands below run from the repository root unless stated otherwise. The
[machine-readable record](verification-results.json) retains the individual
TypeScript projects, Mermaid blocks, comment-only files and UI observations.

## Documentation and inventory

| Check | Method and result |
| --- | --- |
| Source coverage and Git references | `python3 scripts/review_architecture.py --check` regenerates the immutable source inventory in memory, compares both generated files and checks every recognised source permalink against the baseline Git object and line count. All references passed. This proves that the cited range exists, not that it supports a claim. |
| Contract inventory | `python3 scripts/build_architecture_contract_inventory.py --check` passed. It reproduces 115 JSON Schemas, 469 exported TypeScript declarations (438 authored, 31 vendored), 21 dataclasses and 116 embedded schema/registration sites, plus separately listed protocol and SQL assets. |
| Generator syntax | `python3 -m py_compile scripts/review_architecture.py scripts/build_architecture_contract_inventory.py` passed. Independent review prompted inclusion of SQL and explicit separation of the pinned vendor dependency. |
| Diagrams | All 24 Mermaid blocks parsed with `mermaid@11.12.3`, using jsdom from the existing Explorer dependencies. The parser was installed in a disposable directory; repository dependencies and lockfiles were unchanged. This is syntax validation, not a screenshot/accessibility or GitHub rendering acceptance test. |
| Worked contract examples | JSON Schema Draft 2020-12 accepted the search, empty-search and actual query examples; rejected the oversized limit, extra URL property and all-zero key. Eleven query terms passed structural schema validation as documented; the separate runtime guard is linked in the guide. |
| Pilot SQL constraints | Executed the actual migration in an in-memory SQLite database: four seeds appeared; invalid counters, flags, maxima and oversized receipt JSON were rejected; applying the seed again preserved existing usage. This checks the documented constraints, not production database admission or concurrency. |
| Local links and immutable research | `python3 scripts/check_links.py` checks repository-local Markdown targets, the research ZIP/file hashes, source-ledger snapshots and source identifiers. Results are recorded below. |
| Change hygiene | `python3 scripts/check_changelog_fragments.py` and `git diff --check` check changelog structure and whitespace. Research files have no Git diff. |

The source register inventories all 32,138 baseline files and identifies 484 code,
presentation, migration, launcher and CI files: 479 authored plus five vendored.
Its 30,833 imported metadata records are counted as data; no exhaustive audit of
their semantic truth or rights is claimed. Per-domain review depth appears in
[the review](REVIEW.md#review-coverage-and-method).

## Implementation checks

- All 11 existing application/package configurations passed
  `node node_modules/typescript/bin/tsc --project <configuration> --noEmit`.
  This used the ordinary project options and existing generated inputs.
- A separate diagnostic with `--noUnusedLocals --noUnusedParameters` identified
  11 unique declarations. Its non-zero exits are expected findings under stricter
  optional flags, not failures of the ordinary configuration. Full commands and
  deduplicated diagnostics are in [unused-declarations.json](unused-declarations.json).
- Python AST parsing succeeded for all 148 maintained Python files and indexed
  3,094 function definitions. This is a structural check, not execution coverage.
- All 24 changed implementation files were checked against the baseline diff:
  added/removed executable-file lines were comments, and modified Python ASTs
  were equal to the baseline with location metadata excluded. No runtime
  refactoring, dead-code deletion, schema-byte change or dependency update is
  included in this patch.
- `.venv/bin/python scripts/validate_contracts.py` validated 102 root schemas
  and 153 records, rejected all ten forbidden selection mutations, and checked
  counts/unique identities in three evaluation manifests. The separate intake
  schemas are outside this existing validator's root scan; see CT-02.

## Focused existing tests and reproduced defects

| Area | Observed outcome |
| --- | --- |
| Explorer state/graph, WebMCP adapter, workbench/controller/learning/drop | 47 Vitest tests passed across the three applications. This is a focused selection, not every browser test. |
| Experience intake | TypeScript build and both compiled Node test files passed. |
| OKF+ metadata | 178 unique tests passed with `.venv/bin/python -m unittest discover -s tests -p 'test_okf_plus_*.py'`. This includes the separately passing 97-test contract subset. |
| Experience and native mount | 18 passed with `node --test --test-isolation=none --test-reporter=tap --test-timeout=20000 tests/test_experience_evaluate.mjs tests/interoperability/test_sites_native_mount.mjs`. |
| Experimental gateway | 60 passed against the existing compiled `sites-pilot`, `web216-cpih-mcp` and `web216-hosted-cpih-application` test modules. These supplement source equivalence and type checks; a fresh full runtime build is not claimed. |
| Sites evaluator, selected cases | 12 passed with `node --test --test-isolation=none --test-reporter=tap --test-timeout=10000 --test-skip-pattern='official client exercises' tests/interoperability/test_sites_mcp_evaluate.mjs`. The three excluded protocol cases remain unverified as explained below. |

Run the retained demonstration with:

```sh
node docs/architecture/examples/reproduce-ui.mjs
```

It imports the actual Explorer state/graph code through Vite and uses jsdom. At
the reviewed baseline it observes:

```json
{"case":"Unicode query roundtrip","canonicalCodePoints":101,"canonicalUtf16Units":202,"parsedQuery":""}
{"case":"Actual graph renderer focus","target":"view-heading-graph","tabindexAttribute":null,"activeElement":"BODY"}
```

These observations support UI-01 and UI-02. This script records current behaviour;
it is not an assertion that defects should remain. Real-browser keyboard
acceptance is still required for a fix. Manual text input has a separate UTF-16
length cap, so UI-02 is specifically a canonical state/URL round-trip defect.

## Limits and remaining integration steps

Three Sites evaluator protocol cases could not complete in this sandbox. The
harness's `execFileSync` call to the Python interpreter reported `EPERM`; a minimal
subprocess printing `123` reproduced that error despite an exit status of zero
and the expected stdout. Two bounded full-suite attempts timed out. The selected
passing tests did not modify or weaken those assertions.

The GitHub API request for this repository returned `Forbidden`. No remote pull
request, push, canonical CI result or hosted deployment is claimed for this
change. Integration still requires the repository's full mandatory checks and
an issue-linked pull request from an environment with GitHub access.

No live provider requests, private evidence acquisition, full image rebuild,
native OAuth/Voice acceptance or full-corpus metadata regeneration was needed
for this documentation/comment patch. Existing release requirements continue
to govern any future activation or deployment.

## Final local check results

- Immutable source inventory and **2,475 Git line references** passed.
- **1,228 local Markdown links**, **183 research hashes**, **two ledger
  snapshots** and **71 source identifiers** passed the existing link checker.
- All **105 changelog fragments** passed the existing validator.
- `git diff --cached --check` passed, and the immutable research directory has no diff.
- `python3 scripts/scan_secrets.py` scanned 32,252 text files with no baseline
  secret or machine-path match.
