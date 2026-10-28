# Explorer discovery projection

Related work: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Implementation merged, protected-main archive verified, public deploy and
rollback/restore accepted: 27 October 2026.

The previously accepted public archive at GIS source
`8e67ae88e68341120a712d102f692894fbd89659` retains the complete metadata, but its
Explorer projection exposes only record type and source family as facets and
reports zero resources, publishers and relationships. The source records already
contain more discovery information. This increment projects that information
without changing their retained metadata or the small linked learning records.
The [earlier publication evidence](../operations/EXPLORER_PAGES_PUBLICATION.md#completed-publication-evidence)
remains evidence for that historical archive, rather than acceptance of this fix.

## Facets and compact presentation

The producer uses the same exact values in full Reader records, compact search
rows and static filter postings. Missing and null properties acquire no invented
value. Native units, CRS spellings, release versions and status values remain
distinct. `discovery-coverage.json` records each dimension's source paths,
nonempty records, missing records, distinct values and memberships.

| Facet key | Retained source property | Suggested by default |
| --- | --- | --- |
| `record_type` | `type` | Yes |
| `source_family` | `sourceFamily` | Yes |
| `tag` | `tags[]` | Yes |
| `source_publisher` | `dcterms:publisher[].@id` | No |
| `review_status` | `reviewStatus` | Yes |
| `assertion_status` | `assertionStatus` | No |
| `lifecycle_status` | `status` | No |
| `temporal_status` | `temporal.status` | No |
| `temporal_kind` | `temporal.kind` | No |
| `update_frequency` | `update.frequency.label` | No |
| `update_frequency_status` | `update.frequency.status` | No |
| `release_version` | `update.releaseVersion` | No |
| `retrieval_authority` | `rights.retrievalAuthority` | No |
| `source_evidence_kind` | `sources[].evidenceKind` | No |
| `unit` | `details.unit_of_measure`, `details.unit`, `qudt:unit` | No |
| `spatial_reference` | `details.spatialReference` | No |
| `crs` | `details.crs[]` | No |
| `storage_crs` | `details.storageCrs` | No |

Four suggested facets remain folded, with thin colour bars and accessible colour
controls. **All** exposes the other dimensions. The candidate browser contract
retains 12-pixel bars and a maximum folded card height of 64 pixels. A facet value
is a discovery aid; matching names do not establish identity or equivalence.

## Relationships and source references

The retained corpus produces 137 explicit `skos:related` assertions across 89
retained record nodes; both endpoints resolve to retained record routes. Each
projected assertion keeps
its source and target IRIs, predicate, source pointer, evidence, rights, status,
scope and provenance. The graph overview shows up to 128 connected records;
selecting a record uses its exact incident links. Learning links, shared tags and
Markdown links do not create semantic assertions.

The same audit finds 73,656 explicit references to external or nested entities.
Those remain in the complete raw metadata and in grouped coverage counts; they
are outside this retained-record graph. An omitted graph edge does not imply
that the source has no relationship. The GIS-owned
[relationship schema](../../okf-plus/schemas/explorer-relationship.schema.json)
and source-pointer checks validate the projected assertions without claiming a
different upstream relationship profile.

The candidate contains 61,309 record-to-source-URL associations covering 30,501
distinct URLs. It labels these **source references**. They establish neither
downloadable distributions nor execution permission, media format, payload size
or observed geographic data availability. Two publisher entities come from
explicit `dcterms:publisher` IRIs; source-family labels do not mint publishers.
Conflicting publisher labels fall back to the retained IRI.

One retained source URL contains unescaped braces. It stays unchanged in raw
metadata and receives an explicit coverage omission, rather than a rewritten or
clickable source-reference row. All other admitted source-reference rows retain
the exact URL and their originating source fields. Per-record deduplication
preserves multiple source-field pointers to the same URL.

## Bounded loading contract

The optional `record_resources` entrypoint and data-manifest index refer to
`record-resources.json`, with schema `okf-record-resource-index.v1`, the corpus
snapshot and the `fnv1a32-prefix-2` bucket algorithm. Its hash-bound locator buckets
map each record route to its exact dataset name, count and shared-chunk row
selectors. Resource chunks group at most 32 records. Selecting one record returns
only its rows, even when a fetched chunk also holds neighbouring records.
This optional contract requires `record_locator` to load and bind the selected
dataset identity; it cannot substitute a route-derived name for that check.

The consumer verifies relative paths, snapshot, byte counts, SHA-256 digests,
unique row selectors, dataset identity and declared counts. Limits are 256 KiB for
the index, 1 MiB per locator bucket, and 16 chunks, 256 selected rows and 2 MiB of
chunk bytes per selected record. Each shared chunk has at most 1,024 raw rows.
The Reader and selected-record Resources view use this bounded path when the
entrypoint exists. Older bundles keep their existing loading contract.

Overview counts, facet postings, graph labels and relationship adjacency have
separate bounded projections. Opening a selected record's references must not
hydrate all 30,876 complete records or all source-reference chunks.

The graph overview carries labels for its own nodes. Individual records and
references retain their own source labels. The producer does not advertise a
partial global endpoint-label registry: that upstream contract requires complete
route coverage and would correctly report missing labels for every omitted route.

## Verification and publication

The publication configuration pins reviewed consumer source
`757537090af94eb6dda51de16938aa221fcda48d` from
[Explorer PR #185](https://github.com/chris-page-gov/okf-explorer/pull/185), with
app tree `827ac61a364500a2c73ad949dfda36f0839e54056644edd414ddb34f96aee960`
and manifest `bbb482b252b9385149ab06a0bb5cbaae778e65a9498ea5c06d3683f4aa297d7a`.
That immutable reviewed head remains the pin after merge because its Git tree
exactly matches accepted consumer main. The upstream prerequisites are complete
required PR CI, merge, identical reviewed/merged Git trees and successful normal
main workflow selection. Record conditional skips as skips; they do not become a
full main behavioural rerun or authorise forced selectors. These prerequisites
were satisfied before the GIS implementation merged, as recorded below.

Producer checks cover exact facet postings, complete metadata preservation,
source-reference identity and rights, row selectors, relationship source pointers,
schema validation, coverage commitments and deterministic bytes. Consumer checks
cover bounded loading, corrupt or mismatched bindings, shared-chunk isolation,
source labels and selected-record navigation. GIS browser acceptance adds all
18 facets, source-reference inspection, the 137-assertion inventory and actual
Links/Graph navigation while retaining keyboard, narrow-layout and compactness
checks.

Local development verification passed 39 focused producer tests. An independent
inventory audit checked all 30,876 route locators, 61,309 source-reference IDs and
965 shared resource chunks, including their digests and selected dataset identity.
The repaired development projection contains 37,760 files / 830,812,967 bytes before
the app, guides, legacy routes and publication metadata are assembled. These are
development results; they do not establish final-source CI or public acceptance.

Six real-data development browser cases also passed without retries: discovery,
native field explanations, full-corpus search/Ask and compact controls at 1440,
390 and 320 pixels. The discovery case checks actual Links/Graph navigation,
source-reference labels, shared-chunk isolation and Reader navigation within the
same document. These checks use the retained source-353 prototype and the
[consumer change](https://github.com/chris-page-gov/okf-explorer/pull/185), rather
than an accepted publication archive. Earlier failed development attempts remain
recorded separately.

The exact accepted historical source `8e67ae88…` keeps its two-facet, zero-graph
profile for rollback verification. Other sources must satisfy the new discovery
contract; absent discovery metadata cannot select the historical profile.

The completed public HTTPS/browser and rollback/restore results below satisfy
the existing [publication requirements](../decisions/ADR-0019-full-explorer-pages-publication.md)
for this static increment. Future publications require their own exact-source
evidence. No assurance gate, private-feature finding, protected-data right or
hosted Ask OKF admission changes.

## Merged implementation and review evidence

### Canonical consumer

[Explorer PR #185](https://github.com/chris-page-gov/okf-explorer/pull/185)
merged as `46928e2a90fe3a118f4f51d23d472cbba0389844`. Its Git tree
`fbe122440bcfc62c3df0722013697f971bae9ed4` exactly matches reviewed head
`757537090af94eb6dda51de16938aa221fcda48d`. Independent inspection recomputed
all 43 app file hashes and the app tree/manifest identities above.

The final-head [full PR CI](https://github.com/chris-page-gov/okf-explorer/actions/runs/40494428324)
passed all 14 executed jobs. `browser-targeted` was the skipped alternative to
`browser-full`. Chrome, Firefox and WebKit checks passed 531 UI cases and 78
Foundry cases, with 15 inherited UI skips and zero reported flaky cases. The
unchanged Heritage evaluation passed all 100 questions at the 80-point threshold
(mean 92.6) and all three journeys. Earlier failed candidates remain separate
observations; these results bind the final reviewed tree.

The merged-main [normal manual workflow](https://github.com/chris-page-gov/okf-explorer/actions/runs/40497909068)
succeeded with six executed jobs and nine declared conditional skips. Its impact
plan found no changed paths against `origin/main`. This was the normal selected
main check, rather than a full behavioural rerun; the full behavioural evidence
is the identical-tree PR run above. The separate upstream
[Pages publication](https://github.com/chris-page-gov/okf-explorer/actions/runs/40497799194)
passed all six jobs. Its installed-Chrome estate-registry journey verified live
publication identity `46928e2a…`. That verifies the canonical Explorer site; GIS
publication remains a separate acceptance step.

### GIS review candidate

[GIS PR #187](https://github.com/chris-page-gov/gis-ai-go/pull/187) merged as
`93fe753460a2a3c907d9b8257060e89c758e3c4e` after all required PR checks passed.
The [complete PR CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40496267348)
and [PR CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40496265796)
succeeded. Main-only independent derivation and attestation jobs were conditional
PR skips and remain required on protected main.

The candidate used synthetic merge checkout
`299c705a687d51d00678d99dc22cfb7bb760cf39`, not the final main commit. Complete
loopback verification checked 38,604 files / 899,129,361 bytes with zero retries.
All eight browser cases passed first attempt, with zero skipped, flaky or
unexpected results. Its 929,628,160-byte review tar has SHA-256
`9671127dac4141b542382980a2c5be2cacad7d426e161ee93a0c06e843bd4063`.
The candidate stays below the 1,000,000,000-byte and 50,000-file publication limits.
This PR archive is review evidence and cannot be selected as the protected-main
deployment archive.

### Verified protected-main archive

Protected-main [CI 40500356691](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40500356691)
and [CodeQL 40500357370](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40500357370)
both succeeded on attempt 1 for exact source
`93fe753460a2a3c907d9b8257060e89c758e3c4e`. All 13 checks passed: ten CI jobs,
including independent image derivation, provenance and attestation, plus three
CodeQL analyses. None were skipped. The main candidate's complete loopback walk
checked 38,604 files / 899,129,361 bytes with zero transport retries. All eight
browser cases passed first attempt, with zero skipped, flaky or unexpected
results or reported errors.

| Identity | Verified main value |
| --- | --- |
| GIS source | `93fe753460a2a3c907d9b8257060e89c758e3c4e` |
| Source CI / attempt | `40500356691` / `1` |
| Source artefact ID | `12734561797` |
| Actions ZIP SHA-256 / bytes | `16af4eaebcd398f5200538e4e05fd2ae720fea34bcd86643456a080a388e89b7` / 148,637,938 |
| Source artefact retention expiry | 25 January 2027, 12:00:10 UTC; recheck before future use |
| Source tar SHA-256 / bytes | `742eb25f698355fe021780d321e025a4b542a6ee32b8da60921c4a0d2e3b39b4` / 929,628,160 |
| OKF input root SHA-256 | `709e8e87b36b0db9a41e862361f744cd7ae880772100b4a860422be208b78891` |
| Logical payload root SHA-256 | `5d9835c039eed7e11aefd0edaa87e98e9e35cbf58555e66fad9a2c1dec864e4f` |
| Public checksum ledger SHA-256 | `d647ec82619fb3f322ccf730b1d6ed92ba1fa75406c6db8ad0dcc3a3c6cec939` |
| Build attestation ID | `60368914` |

The build attestation binds the tar digest to `.github/workflows/ci.yml` at
`refs/heads/main`, this exact source and source-CI attempt 1 on GitHub-hosted
runners. The selected main tar differs from the review-only PR tar above; their
identities and results remain separate.

### Accepted initial public deploy

Actual [deploy 40506483121](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40506483121)
was dispatched at 12:46:55 UTC on 27 October 2026 with workflow/source `93fe7534…`,
source CI `40500356691` and the main tar `742eb25f…` above. All three jobs passed on
attempt 1: archive/attestation preparation, deployment and actual public
verification. The selected archive was not regenerated. The retained reports
verify the actual canonical HTTPS site, with no loopback mirrors or reported
browser transport failures.

| Actual deploy evidence | Result |
| --- | --- |
| Source / tar | `93fe7534…` / `742eb25f…`, exact identities above |
| Verified files / bytes | 38,604 / 899,129,361 |
| Matched roots and app | Payload `5d9835c0…`, OKF `709e8e87…`, ledger `d647ec82…`; app source `75753709…`, tree `827ac61a…`, manifest `bbb482b2…` |
| Complete-walk elapsed / peak active requests | 799,041 ms / 12 |
| Minimum observed paced request gap | 20.000509 ms |
| Readiness probes / bytes | 1 / 1,398 |
| Transient responses / extra attempts | 18 HTTP 503 / 18 |
| Reserved replay / received extra-response bytes | 142,197 / 142,197 |
| Application-consumed error-body bytes | 0 |
| Browser first-attempt / flaky / skipped / unexpected | 8 / 0 / 0 / 0 |
| Public verification artefact ID | `12735923900` |
| Evidence ZIP SHA-256 / bytes | `2d2c07ef214c3a80635071c53e2c5cb5d79574b5a7895561f85603896dbc73df` / 11,483 |

The existing automatic transport policy recovered each HTTP 503 with one
predefined one-second retry. Its 18 extra requests and 142,197 replay bytes stayed
within the unchanged ceilings of 64 extra requests and 64 MiB. No manual rerun
was needed. Verified inventory totals count successful logical bytes once. All
eight browser cases passed first attempt in `deployed-publication` mode, with
zero mirrors, reported transport failures or errors.

This accepts the initial deploy phase. The historical rollback and final restore
below have separate actual public verification results.

### Accepted historical rollback

Actual [rollback 40509547583](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40509547583)
passed all three jobs on attempt 1 using workflow `93fe7534…` and the previously
accepted source `8e67ae88…` / source CI `40412716168` / tar `3fe87087…`. Complete
actual HTTPS verification matched all 37,279 files / 714,610,618 bytes and the
unchanged historical roots: OKF `4baa9767…`, payload `fd08e1e0…` and ledger
`7b4291bb…`. It also matched the historical app `7ffa3297…` / tree `d127aadb…` /
manifest `ab227164…` recorded in the earlier publication evidence.

All eight current browser cases passed first attempt, with zero flaky, skipped
or unexpected results, mirrors or reported transport failures. The discovery
case explicitly selected `accepted-pre-discovery-v2`: two facets and zero
relationships. This verifies recovery of the exact historical archive without
claiming rich discovery for its older projection.

The 775,081 ms walk used at most 12 concurrent requests, with a minimum paced gap of
20.000912 ms. Readiness required one probe / 1,398 bytes. Five HTTP 503 responses
recovered automatically on their second attempt after one second each, using
five extra requests and 25,008 reserved/replayed bytes; application-consumed
error-body bytes were zero. Public evidence artefact `12736324738` has ZIP
SHA-256 `6e7420cb4b5078cf83a2c9a0cf591b3b07d83d725dd0f44a34c3aa187fc68aa0`.

### Accepted restore of the identical new archive

Actual [restore 40512243266](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40512243266)
passed all three jobs on attempt 1 using workflow/source `93fe7534…`, source CI
`40500356691` and the same main tar `742eb25f…`. Source validation and deployment
did not rebuild or regenerate the archive. Fresh public verification matched all
38,604 files / 899,129,361 bytes, the exact new payload/OKF/ledger roots and app
`75753709…` / tree `827ac61a…` / manifest `bbb482b2…` above.

| Actual restore evidence | Result |
| --- | --- |
| Complete-walk elapsed / peak active requests | 809,979 ms / 12 |
| Minimum observed paced request gap | 20.000965 ms |
| Readiness probes / bytes | 1 / 1,398 |
| Transient responses / extra attempts | 10 HTTP 503 / 10 |
| Reserved replay / received extra-response bytes | 280,000 / 280,000 |
| Application-consumed error-body bytes | 0 |
| Browser first-attempt / flaky / skipped / unexpected | 8 / 0 / 0 / 0 |
| Public verification artefact ID | `12738328419` |
| Evidence ZIP SHA-256 / bytes | `31c1ab15d8aa09c18c1a4b52815ba9985aa9cae39bc83443fc74caf3245380c9` / 11,022 |

Each transient HTTP 503 recovered with one predefined one-second retry inside
the unchanged transport budgets. All eight browser cases passed first attempt
in `deployed-publication` mode, with zero mirrors, reported transport failures or
errors. The actual discovery contract reports 18 facets, 137 relationships,
61,309 source-reference associations and two publishers.

Deploy, historical rollback and restore therefore complete this static
publication and recovery rehearsal. The current bare
[GIS public URL](https://chris-page-gov.github.io/gis-ai-go/) serves the identical
accepted `93fe7534…` archive. Later documentation commits do not become the served
source. Human learning assessment, the separate private capture findings and
wider acquisition work remain outstanding.

### Local orchestration correction

A local orchestration assertion initially expected `accepted-live-rollback-phase`
instead of the receipt's `accepted-live-historical-rollback-phase`. The shell
continued to the already authorised restore request after that assertion failed.
The actual rollback byte/browser evidence and fresh source-selection gate had
already passed. The exact historical status, source, archive, counts and browser
results were rechecked; restore was submitted once as `40512243266`. Subsequent
dependent shell commands explicitly fail closed. The single restore subsequently
passed the actual verification recorded above. This correction changes no
archive bytes or workflow verification requirement.
