# Metadata and intake contract validation repairs

The owner authorised these improvements after the Explorer repairs in commit
`70249136`. They address [EX-07](../architecture/REVIEW_EXPERIMENTAL.md) and
[CT-02](../architecture/REVIEW_CONTRACTS.md). The historical review and generated
inventories retain their original baseline; implementation links here follow
this document's Git revision.

## Required metadata schemas

The [OKF+ builder](../../scripts/okf_plus/build.py#L44) requires all three local
schemas: record, source snapshot and search index. It loads and checks their
definitions before reading records. A missing definition is a build error,
and schema validation is no longer conditional on a file being present.

The build still stages output before replacing a generated bundle. Failed schema
admission leaves no new published output and preserves any previous bundle.
Small synthetic test checkouts now copy the real schema files. There is no
production option to bypass this validation.

The [build regressions](../../tests/contract/test_okf_plus_build.py#L369) exercise
each missing schema and a wholly absent schema tree, fresh and existing output,
and input shapes that pass manual provenance checks but violate JSON Schema.
Tests distinguish complete structural validation from provenance checking.

## Intake descriptor and producer conformance

The package test command automatically includes the new
[schema conformance test](../../packages/experience-intake/test/schema-contract.test.ts#L69).
It uses the repository's locked JSON Schema Draft 2020-12 validator to check the
[request](../../packages/experience-intake/schema/request.v1.schema.json#L1) and
[result](../../packages/experience-intake/schema/result.v1.schema.json#L1)
definitions, representative requests, and actual planner/ZIP outputs.

Positive cases cover supported result forms; negative mutations ensure the
published contracts reject representative unknown fields, invalid types/statuses
and changed policy guarantees. Additional cases distinguish structural schema
acceptance from the runtime's stricter path and byte-budget checks. A JSON-shaped
request is still untrusted input; the planner's runtime checks remain necessary.

This adds assurance using existing locked development dependencies. It does not
add a runtime dependency, change the published schema bytes or enable network,
archive extraction or persistence capabilities in the intake package.

The existing CI entrypoint invokes `pnpm run check`, whose test sequence includes
the Python tests and the experience-intake package test. No new CI lane or
conditional bypass is required. The [package README](../../packages/experience-intake/README.md)
records the Python development prerequisite.

## Verification record

Metadata verification:

- Before the fix, all eight missing-schema subcases failed their new assertions:
  each of three missing definitions, or all definitions missing, against both a
  fresh output and an existing generated bundle.
- After the fix, `.venv/bin/python -m unittest discover -s tests -p 'test_okf_plus_*.py'`
  passed all **181 tests**, including the missing-schema and schema-only invalid
  input regressions.
- All **11 generated files** were byte-identical before and after the builder
  change for the same complete one-record fixture and revision.

Intake verification:

- The existing `pnpm --filter @gis-ai-go/experience-intake run test` command,
  executed with pinned pnpm 10.33.2, built the package and passed all **21 tests**.
- The two new tests check both schema definitions and **43 labelled cases**:
  23 valid representative request/producer-result cases, 16 rejected mutations,
  and four checks demonstrating stricter runtime path/UTF-8 semantics.
- Four temporary mutation checks failed for the intended reason: allowing an
  unknown request property, narrowing the accepted file count from 64 to 63,
  making the result schema definition invalid, and changing an actual text-preview
  output to claim one network request. Published schemas and runtime code were
  not modified by these checks.
- Restricted execution timed out in the test harness's bounded validator
  subprocess calls. The same tests passed with additional local socket/network
  permission; no assertion was weakened or skipped.

Independent reviews found no actionable issues in either patch. Local Markdown
links, research hashes, source-ledger snapshots, changelog fragments and whitespace
checks passed. The offline secret/path scan reported no baseline matches.

At initial verification, remote publication was unavailable because the shell
GitHub API returned `Forbidden`. The subsequent [release closure work](RELEASE_CLOSURE.md)
uses the available connector and Git transport and records canonical CI separately.
No live provider, hosted deployment or full-corpus regeneration is claimed here.
