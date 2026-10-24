# OKF Explorer integration review

Related work: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
This implements the [agreed handoff](OKF_EXPLORER_CLOUD_HANDOFF.md) in two
repositories. GIS AI GO owns the retained metadata and linked learning records.
The existing `chris-page-gov/okf-explorer` application consumes their generated
large Reader and context projections.

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
  artifacts/okf-plus artifacts/okf-explorer-review SOURCE_COMMIT
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
