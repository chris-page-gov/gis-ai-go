# Explorer publication scope and deferred CodeQL review

Work item: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Review date: 26 October 2026. The review findings below remain unresolved for the
deferred source. This scope change neither fixes nor dismisses them, and does not
assert a current GitHub alert state for a branch without its own recorded scan.
No query or required check has been disabled.

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
public tree must pass fresh full CI and CodeQL with the existing query coverage.
Passing those checks will not establish acceptance of the deferred source.

## Content checksum findings

| Location | Observed purpose |
| --- | --- |
| [`metadata_refresh.py`, `digest`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/metadata_refresh.py) | SHA-256 identities for complete source bytes, normalised records, manifests and source URLs |
| [`private_schema_cards.py`, `sha`](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/private_schema_cards.py) | SHA-256 identities for original JSON, schema pointers, values and linked text fragments |

These observed content/provenance uses do not resolve the rule's complete
sensitive-data paths. Changing their algorithm changes source identities and
integrity contracts. The retained refresh passes its request credential in an
HTTP header and has a literal reflected-key refusal test; that observation alone
does not classify the findings as false positives.

The official rule's guidance recommends SHA-2 for content integrity. Its separate
password branch also classifies API keys as passwords through naming heuristics.
Each annotation reports four password-source paths, but the connection returns
HTTP 403 for the code-scanning alerts API, so those exact paths have not been
retrieved. Matching the number of heuristic sources is not proof of a path.

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
