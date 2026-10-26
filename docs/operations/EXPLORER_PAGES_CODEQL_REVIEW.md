# Explorer publication CodeQL review

Work item: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Review date: 26 October 2026. The findings below remain open pending review of
their complete CodeQL paths. No query or required check has been disabled.

The first main-target migration run completed all three CodeQL analyses. Its
aggregate check reported two `py/weak-sensitive-data-hashing` findings and one
`py/incomplete-url-substring-sanitization` finding. These occur in the earlier
metadata integration, rather than the publication packager.

## Content checksum findings

| Location | Observed purpose |
| --- | --- |
| `scripts/okf_plus/metadata_refresh.py`, `digest` | SHA-256 identities for complete source bytes, normalised records, manifests and source URLs |
| `scripts/okf_plus/private_schema_cards.py`, `sha` | SHA-256 identities for original JSON, schema pointers, values and linked text fragments |

These outputs bind content and provenance; neither helper stores or compares a
password hash for authentication. Changing their algorithm changes existing
source identities and integrity contracts. The request credential travels in an
HTTP header. The refresh rejects a response containing the literal request key
before capture; the existing reflection test checks that this value is absent
from retained files.

The official rule's guidance recommends SHA-2 for content integrity. Its separate
password branch also classifies API keys as passwords through naming heuristics.
Each annotation reports four password-source paths, but the connection returns
HTTP 403 for the code-scanning alerts API, so those exact paths have not been
retrieved. Matching the number of heuristic sources is not proof of a path.

The next step is to inspect those paths through repository code-scanning access
and record the disposition. Do not rename credentials, switch hash APIs, change
digest bytes or exclude the query merely to remove an annotation.

## URL assertion and routing repairs

The URL annotation concerns a fake-transport call count in a Retry-After test.
The assertion now compares the parsed hostname exactly. Runtime admission already
checks parsed authority membership in the closed metadata host set.

The repository gate also identified the new tracked publication configuration as
an unmatched assurance path. It now explicitly selects complete assurance, with
a regression test. Unknown paths retain the existing complete-check fallback.

All 98 affected routing, workflow and metadata tests passed after those repairs.
Full canonical CI and the remaining CodeQL review still govern merge.
