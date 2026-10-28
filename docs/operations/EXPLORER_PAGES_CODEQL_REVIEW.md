# Explorer publication scope and deferred CodeQL review

Work item: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Review date: 26 October 2026. The review findings below remain unresolved for the
deferred source. This scope change neither fixes nor dismisses them, and does not
assert a current GitHub alert state for a branch without its own recorded scan.
No query or required check has been disabled. Evidence pointers were updated on
27 October 2026 after public acceptance; the private findings remain unresolved.

## Current public increment

The main-target publication retains the full public bundle, Reader/context,
learning and native-field/atomic source-card dependencies. It does not call the
separate new private capture feature. That complete feature, including its
credential/rate helpers, tests and active command surface, remains unchanged at
[reconciliation commit 35318abc](https://github.com/chris-page-gov/gis-ai-go/tree/35318abcce5e23c1509ed6ce131d81f5dfd0d38c).
Existing main OS recovery is retained. Its broader acquisition objective remains
outstanding alongside this independently testable static publication.

The first, broader main-target migration run completed all three CodeQL analyses. Its
aggregate check reported two `py/weak-sensitive-data-hashing` findings and one
`py/incomplete-url-substring-sanitization` finding. These occur in the earlier
private capture integration, rather than the publication packager. The narrowed
public source passed complete main CI and full CodeQL with the existing query
coverage; its [publication evidence](EXPLORER_PAGES_PUBLICATION.md#completed-publication-evidence)
identifies the exact runs. Passing those checks does not establish acceptance of
the deferred source.

## Content checksum findings

| Location | Observed purpose |
| --- | --- |
| [`metadata_refresh.py:88`, `digest`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/metadata_refresh.py#L88) | SHA-256 identities for complete source bytes, normalised records, manifests and source URLs |
| [`private_schema_cards.py:23`, `sha`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/private_schema_cards.py#L23) | SHA-256 identities for original JSON, schema pointers, values and linked text fragments |

These observed content/provenance uses do not resolve the rule's complete
sensitive-data paths. Changing their algorithm changes source identities and
integrity contracts. The retained refresh passes its request credential in an
HTTP header and has a literal reflected-key refusal test; that observation alone
does not classify the findings as false positives.

The official rule's guidance recommends SHA-2 for content integrity. Its separate
password branch also classifies API keys as passwords through naming heuristics.
The historical [check containing both hash annotations](https://github.com/chris-page-gov/gis-ai-go/runs/121844685603)
belongs to migration head `1c10fcd2cb4ccd97077dea0a45b7d3157c893769`.
Each annotation reports four password-source paths. Both the normal GitHub
connector and the existing cloud CLI returned HTTP 403 for the full code-scanning
alerts API; exact alert-number URLs and complete source-to-sink paths were not
available. Matching the number of heuristic sources is not proof of a path.
SHA-256 content checksums and password hashing have different requirements;
source inspection alone does not establish which sensitive values reach a sink.

The historical Python analysis used CodeQL CLI 2.27.3. Its ordinary workflow
artefacts API returned no retained artefacts, and the job logs did not supply the
complete flow paths. Unresolved relative-import warnings are diagnostic evidence,
not a false-positive decision. No finding was dismissed or reclassified.

The separate follow-up is to inspect those paths through repository code-scanning
access and record the disposition before bringing the private feature forward.
Do not rename credentials, switch hash APIs, change digest bytes or exclude the
query merely to remove an annotation. No finding was dismissed and no scan
exclusion, baseline change or weaker main gate is introduced by this scope split.

## URL assertion and routing repairs

The URL annotation concerned a fake-transport call count in the private
Retry-After test. An intermediate migration head changed the assertion to compare
the parsed hostname exactly. That test is now deferred with the feature; the
retained reconciliation source is unchanged, so this records no fix or disposition
for that source.

The repository gate also identified the new tracked publication configuration as
an unmatched assurance path. It now explicitly selects complete assurance, with
a regression test. Unknown paths retain the existing complete-check fallback.

The earlier 98 routing, workflow and metadata test results describe that broader
working tree. Fresh full assurance governs the narrowed public tree; complete
source-path review remains outstanding for the separate private feature.
