# Reconciliation of the local OS extension and main

Owner instruction: 24 October 2026. Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).

This integrates local commits `63b5cafe` and `a4e66e1a` with main at
`59ba0dd1f3d2d06e1188ce382211e82fb679b258`. Main contains 22 commits after their
common base, `f8292cbb`. The original local branch and portable handoff are
preserved. The reconciliation has its own branch and worktree.

This historical record describes the full reconciliation preserved at
[35318abc](https://github.com/chris-page-gov/gis-ai-go/tree/35318abcce5e23c1509ed6ce131d81f5dfd0d38c).
The later public-default migration selects its public metadata, native-field,
atomic and learning subset. The separate new private capture feature stays in
that commit for [unresolved CodeQL review](../operations/EXPLORER_PAGES_CODEQL_REVIEW.md);
accepted main OS recovery is retained. Results below keep their original branch
scope and do not accept the deferred feature for protected main.

## Implementation decisions

| Area | Reconciled behaviour |
| --- | --- |
| Current recovery workflow | Keep main's field cards, passages, field/document candidates, native lexical forms, query planning and transient processing. Its documented live results remain dated evidence, not new observations from this work. |
| Additional atomic view | Keep `semantic.py`, bounded SQLite search/explain and independent source verification. These provide small field, value, contract and operation records with exact linked qualifications. |
| Metadata acquisition | Keep the frozen `os_document_sync`/`recovery_run` cohort and the broader [`metadata_refresh`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/metadata_refresh.py)/[`private_schema_cards`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/private_schema_cards.py) producer in separate directories and ledgers. The latter includes the 2,303 frozen documentation URLs and 251 additional starting routes, with further reviewed discovery. |
| Planner name collision | Keep main's `retrieval_plan.py` and its `{api, bulk}` measurement contract unchanged. Rename the older richer request-contract estimator to `request_retrieval_plan.py`; retain its schema and tests. It is offline and has no execution adapter. |
| Geographic acquisition | Retire the older persistent `os_retrieve.py`, its request schema and tests. Keep main's `ngd_extract.py`, separate `transient_profile.py` and verified `discard_payloads` lifecycle. The documentation supervisor does not orchestrate geographic acquisition or disposal. |
| API registry | Bind the NGD operation's implementation evidence and declared subset to the canonical extraction/profile workflow. Registry generation remains offline and does not establish live access. Other implemented workflows and the experimental Sites profile retain their separate inventories. |
| Repository checks | Keep main's security repairs, experience checks and existing required gates. Add atomic verification to the OKF check, and regenerate the source-bound local evaluation receipts for the final package script identity. Historical evidence pins stay unchanged. |

The two field-card formats have different identities, parents and evidence scopes.
Main's candidate explanatory passages and the 48 curated local field statements
must not overwrite each other. A shared native name is not an automatic version
match, alias or semantic equivalence. The atomic view remains a view of its pinned
sources; the recovery records describe separate captures and private outputs.
Direct schema type/null declarations also require inspection of enum, const and
composed constraints before asserting which values a complete schema accepts.
The registry format advances to v2 because its execution profile changes. All
reader modes reject v1 bundles and require regeneration in a new directory;
existing bundles remain historical evidence and are never overwritten.

## Operational limits retained explicitly

The broader metadata capture resumes previously successful sources without expiry;
it is not a periodic freshness updater. Its durable limiter is not shared by
main's per-process inventory/extraction clients. Do not run those clients
concurrently against the same OS project and service until their budgets are
coordinated. Independent users of the project can also consume capacity.

The accepted main executor does not inherit the retired fetcher's exact live
schema-hash preflight, automatic native 3D CRS selection, persistent Retry-After
handling or reflected-key rejection. Its default output is EPSG:27700; request
EPSG:7405 explicitly when a suitable collection and the question require 3D
coordinates. It rebuilds pagination from the selected scope instead of following
next URLs. Response bodies are retained before page/CRS validation. These are
explicit differences requiring separate implementation and acceptance, not
protections transferred by this merge.

Acquisition, complete selected profiling and verified disposal remain separate
steps. Raw payloads must remain available until profiling and verification finish;
the reconciliation neither acquires nor deletes provider data. It adds no hosted
tool, service deployment or entitlement claim.

The private fresh captures reported on main are not present in this worktree.
Their successful historical capture is not independently replayed here. This
task's running environment still lacks an OS credential binding and the four OS
metadata host allowances; that does not negate success in the other environment.
The [recovery record](OKF_OS_RECOVERY.md) and [API coverage guide](OS_API_COVERAGE_AND_USAGE.md)
remain the current source of accepted acquisition scope and outstanding work.
The three preserved OKF-223 records are explicitly historical branch evidence.

## Verification and rollback

Independent review found no remaining interface collision or contradictory
execution claim. Focused metadata, planner, extraction/profile, atomic-card and
registry checks passed. The canonical local receipt generator reran its suites;
only the package binding and derived set identity changed, and all 33 receipt
and strict-modern tests passed. Local links, contracts, changelog and secret
checks passed. At merge commit `c377bfdb`, independent atomic verification passed
all 32,596 cards, with a maximum of 14,838 bytes. The separate registry v2 contains
72 cards, at most 12,923 bytes. A Building v4 explanation returned 13 complete
linked cards in 70,493 bytes, with no traversal omission and explicit unknown
datum/access evidence.

The complete existing OKF verification also passed its importer, build, retrieval,
whole-corpus projection, record/schema audit and pinned-engine stages at that
commit; its unassessed K37–K40 cases remain unassessed. TypeScript, gateway,
interoperability and front-end unit checks passed. The 22 execution-service tests,
local client, execution-container, experience, reproducibility, version,
public-read, diagram and SBOM checks passed separately.

The full repository gate remains incomplete. The first attempt found restrictive
checkout execute permissions on the existing launchers; restoring their required
mode fixed that failure. The subsequent Python run executed 1,661 tests with six
failures, one error and seven skips in unchanged observer/private-output tests.
All ten private-output tests passed when rerun with an owner-only temporary
directory outside Git: this managed environment places Git markers in its usual
temporary and workspace roots. The observer's Darwin-mapping and SIGKILL cases
still failed outside the sandbox; diagnostics found a negative mounted executable
inode and an unreaped zombie process. Their code and tests are unchanged from
main. Browser checks cannot launch because the required Chrome distribution is
absent. No check or runtime guard was weakened to obtain a pass.

No prior receipt is promoted to acceptance of changed files. Full assurance is
still required for a release or merge to protected main. This local reconciliation
does not publish a branch or pull request and does not change protected main.

Rollback is to use the preserved original local branch or main's pinned revision.
Generated directories and private ledgers are separate from source history and
are not replaced by the Git merge. No private capture is needed to undo this
source integration.
