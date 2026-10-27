# Explorer discovery projection

Related work: [OKF-223 #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Implementation candidate: 27 October 2026. Source and publication acceptance for
this increment remain pending.

The accepted public archive at GIS source
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

The retained corpus produces 137 explicit `skos:related` assertions whose two
endpoints both resolve to retained record routes. Each projected assertion keeps
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

The candidate pins reviewed consumer source
`757537090af94eb6dda51de16938aa221fcda48d` from
[Explorer PR #185](https://github.com/chris-page-gov/okf-explorer/pull/185), with
app tree `827ac61a364500a2c73ad949dfda36f0839e54056644edd414ddb34f96aee960`
and manifest `bbb482b252b9385149ab06a0bb5cbaae778e65a9498ea5c06d3683f4aa297d7a`.
The exact pin allows both repositories' candidate checks to run in parallel.
The consumer's full required CI and merge remain prerequisites for GIS merge;
its protected-main checks also remain required before public acceptance.

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

Final source and canonical app pins, complete CI results, archive identity,
public HTTPS/browser acceptance and rollback/restore results must be recorded
under the existing [publication requirements](../decisions/ADR-0019-full-explorer-pages-publication.md)
before this increment is described as publicly accepted. No assurance gate,
private-feature finding, protected-data right or hosted Ask OKF admission changes.
