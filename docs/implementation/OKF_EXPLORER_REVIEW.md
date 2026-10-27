# OKF Explorer integration review

Related work: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
This implements the [agreed handoff](OKF_EXPLORER_CLOUD_HANDOFF.md) in two
repositories. GIS AI GO owns the retained metadata and linked learning records.
The existing `chris-page-gov/okf-explorer` application consumes their generated
large Reader and context projections.

> Current evidence — 27 October 2026: the compact canonical Explorer and complete
> public bundle are now the [verified GIS public default](../operations/EXPLORER_PAGES_PUBLICATION.md#discovery-publication-evidence).
> The local candidates below retain their original dated identities and limits;
> they are separate from later public acceptance and the unresolved private work.

The subsequent [discovery repair](OKF_EXPLORER_DISCOVERY.md) adds source-backed
facets, explicit links between retained records and bounded source-reference
loading. Its acceptance is separate from the dated candidates below and the
earlier public archive's two-facet, zero-relationship projection. Both discovery
implementations have merged after required PR assurance. Complete GIS main CI,
CodeQL and the attested main archive have passed. Initial deployment passed the
complete actual public HTTPS walk and all eight browser cases first attempt.
Historical rollback and restore of the identical new archive also passed their
actual public checks, completing the static discovery publication and recovery
rehearsal.

## Reproduce the local candidate

Install each repository's locked dependencies using its own instructions.
Keep the Explorer checkout beside GIS AI GO. Run these commands from GIS AI GO,
using the actual UTC capture time for `CAPTURED_AT`:

```sh
CAPTURED_AT=2026-10-24T11:00:00Z
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/build.py
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/context_projection.py \
  --search-index artifacts/okf-plus/bundle/search-index.json \
  --bundle artifacts/okf-plus/bundle/okf-bundle.json \
  --output artifacts/okf-plus/context \
  --publication-base http://127.0.0.1:8130/gis/explorer/context/ \
  --allow-local-preview --captured-at "$CAPTURED_AT" --all-records
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/explorer_projection.py \
  --search-index artifacts/okf-plus/bundle/search-index.json \
  --bundle artifacts/okf-plus/bundle/okf-bundle.json \
  --context-directory artifacts/okf-plus/context \
  --output artifacts/okf-plus/explorer --captured-at "$CAPTURED_AT"
```

The Reader producer requires a new output directory, preserving previous
candidates. The existing context producer replaces only its own marked output.
The optional local-preview flag permits HTTP only for an explicit loopback host
and port. Public candidates still require HTTPS. This opt-in changes no supplier
source URLs, provider access rules or hosted admission.

Build and check the matching Explorer app according to its own instructions,
including `pnpm build:determinism` in `apps/okf-explorer`. Its packager accepts the
GIS projection root, a new preview directory and the actual GIS source commit:

```sh
node ../okf-explorer/scripts/package_gis_learning_preview.mjs \
  artifacts/okf-plus artifacts/okf-explorer-review SOURCE_COMMIT LICENSE
node artifacts/okf-explorer-review/serve.mjs
```

Open `http://127.0.0.1:8130/start.html`. Keep port 8130 because the generated
passages bind that exact local address. Regenerate the context for another
address before packaging. The package needs Node.js 24 or later and no API key
or package installation. Metadata and learning navigation run locally; supplier
source links need internet access. Generated outputs remain outside Git.

## Identity and evidence

The producer verifies the complete input pair and every context output binding.
It preserves source-native routes and semantic identifiers without joining the
separate atomic view by field name. Every retained record has a Reader record,
complete narrative, original metadata and provenance. A route map, snapshot,
input digest and projection manifest make the identity mapping inspectable.

Record shards contain at most 32 records and remain below 4 MiB. A hash-bound
locator selects the required shard. Static Reader search and Ask OKF both cover
the full retained corpus through separate bounded contracts. Neither requires
all complete records to be loaded before explaining a selected field.

The [small learning records](OKF_EXPLORER_LEARNING_RECORDS.md) remain the source
of objectives, prerequisites, sequence, practice and concept/source references.
They produce the existing unassessed learning presentation. Selecting an exact
native field preserves its identifier, schema and source; containing-record
coverage and qualifications do not become observed field values.

## Verification and remaining acceptance

Focused producer checks cover complete identity, metadata preservation,
determinism, byte bindings, corrupt context rejection, bounded shards, learning
links and safe installation. Consumer checks cover field identity, safe source
links, absent/null/empty/zero distinctions, prerequisite cycles and bounded
evidence routes. Browser review must cover all three learning paths, native
fields, normal search, Ask OKF, keyboard access, narrow screens and lazy loading.

The 24 October environment probe returned HTTP 200 and 94 NGD collections from
one bounded metadata request. No credential or response payload was retained in
the review package. This establishes that metadata route only; protected
feature-data entitlement, full-area retrieval and current semantic completeness
remain separate. Human comprehension and assistive-technology acceptance remain
open. Existing repository-wide CI and release gates still apply.

## Checked candidate — 24 October 2026

The second local package is bound to GIS implementation commit
`444f640d9301800c203db3eb4c658af79029b5f1` and Explorer commit
`00adcf1e5c3243bbc0a1c0d8f282d4f764b0b1c0`. Documentation updates after the
GIS implementation commit do not change that candidate's source inputs.
The corpus snapshot is `okf-plus-dee8c607b379fbc514609206` and the exact app tree
SHA-256 is `79551c35c007b831f1cf4b2455054c98f4febf5668346aebe6d1ac99716f34bb`.
Producer [PR #182](https://github.com/chris-page-gov/gis-ai-go/pull/182) targets
the reconciled handoff branch; consumer
[PR #183](https://github.com/chris-page-gov/okf-explorer/pull/183) targets its main.
Both changes use separate assurance gates before merge.

The full context export passed all-record schema validation. The Reader contains
all 30,876 records in 965 lazy record shards, at most 1,032,325 bytes each, plus
bounded search and the complete matching context corpus. The package manifest
binds 36,955 files; independent byte/hash verification passed. The ZIP passed
its integrity check. The three authored paths contain 11 steps, and each source
learning record remains below 16 KiB.

Verification passed 21 producer/source/context checks, 858 consumer unit tests,
clean Svelte checks, deterministic builds, dependency policy and assembled-Site
checks covering 393 reading pages and 8,328 internal references. The complete
candidate passed 18 real Chromium 151 checks: every learning step, three exact
native fields and source references, three normal searches, three full-corpus
Ask queries, keyboard controls, reversible progress and 390-pixel mobile use.
Desktop and mobile axe scans reported no violations; screenshots were visually
inspected. Initial loading fetched zero dataset record shards. A learning
selection fetched at most one targeted shard.

Each representative Ask query searched the declared 30,876-record corpus and
stayed within its budgets. Pavement width, building height and road elevation
returned 501, 296 and 274 candidates respectively, selecting 16 records each.
All three packages retained `insufficient` evidence status. These are verified
retrieval journeys, not complete answers or specialist approval. There were no
page, console or HTTP errors. The report separately retains 49 cancellation
events after successful HTTP 200 response headers; the tested packages and
journeys completed without unexpected transport failure.

An unchanged local acceptance-lock descendant-cleanup test failed in this
container, which retains zombie descendants under PID 1. No guard was weakened.
The corresponding earlier Explorer CI app job passed after the browser-suite
registry correction; final-source CI and full cross-engine release gates remain
independent. Human comprehension, assistive-technology acceptance, live protected
feature entitlement and hosted Ask OKF admission are not established here.
