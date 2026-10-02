# SITES-218: bounded OS NGD validation

Observed on 2 October 2026. Status: local feature access and bounded structural
checks passed; collection-schema validation and hosted NGD admission remain open.

The owner authorised this separate PSGA validation using existing included access.
The [rights assessment](../operations/SITES_MCP_RIGHTS_ASSESSMENT.md) records the
permitted scope and remaining hosting conditions. These observations do not add
NGD tools to the deployed open-data pilot, establish the credential's account
tier, verify the processor arrangements or demonstrate a financial stop.

## Observed scope and results

The first phase made exactly three sequential requests: one keyless collection
catalogue request, followed by one authenticated Building v4 request and one
authenticated Road Link v5 request. Each feature request used `limit=2` within a
fixed small public Warwick test area. The bounding box used CRS84 longitude and
latitude; returned geometry requested British National Grid, EPSG:27700.
The [Features contract](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features)
defines bounding-box selection as intersection, not clipping or containment.

| Observation | HTTP status | Response bytes | Client elapsed time | Result |
| --- | ---: | ---: | ---: | --- |
| Collection catalogue | 200 | 195,642 | 442.364 ms | 94 collections; reviewed versioned building and road-link collections advertised both required CRSs |
| Building v4 sample | 200 | 12,295 | 708.316 ms | Two features; both passed the bounded structural profile |
| Road Link v5 sample | 200 | 9,552 | 638.473 ms | Two features; both passed the bounded structural profile |

Both feature responses supplied the requested BNG response header. Every sampled
feature had a feature identifier, an OSID and a parseable date in the inspected
date-field set. Geometry structure, finite coordinates, broad GB bounds and
intersection of the geometry's envelope with the test window passed. The building
sample contained 52 coordinate positions and the road sample nine. Both responses
included a next-page link, which was not followed: these are incomplete samples,
not counts of all buildings or road links in the area.

The helper imposed a 10-second deadline and 1 MiB streamed-response limit per
request. It counted attempts before egress and allowed no retries, redirects,
pagination, alternate product or chargeable fallback. The credential was used
only in the OS request header. Feature bodies were processed in memory and were
not retained. The private record contains aggregate checks, byte counts, timings
and hashes; it contains no sampled feature values, identifiers or geometry.
JavaScript buffer clearing cannot guarantee erasure of every runtime string copy.

These are single-request elapsed times, not latency distributions or service-level
evidence. The checks did not establish geometric topology, exact intersection,
identifier equality, complete coverage or full collection-schema conformance.

## Public schema and queryable evidence

A separate authorised phase made exactly four additional keyless GET requests:
the documented [schema](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/schema)
and [queryables](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables)
endpoints for each selected collection. All four returned HTTP 200, within the
same 10-second/1 MiB bounds. This phase requested no features and read no
credential. Source documents and an observation record are retained privately.

| Public metadata | Bytes | Elapsed time | Returned contract |
| --- | ---: | ---: | --- |
| [Building v4 schema](https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema) | 40,985 | 177.407 ms | `bld-fts-building-4.1`; major 4, minor 1; 90 properties |
| [Building v4 queryables](https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables) | 12,962 | 92.293 ms | 24 queryable properties |
| [Road Link v5 schema](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema) | 28,792 | 98.958 ms | `trn-ntwk-roadlink-5.0`; major 5, minor 0; 79 properties |
| [Road Link v5 queryables](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/queryables) | 7,464 | 52.592 ms | 29 queryable properties |

All four documents declare JSON Schema Draft 7 and pass its meta-schema check.
That checks schema syntax; it does not establish that any feature conforms.
Pin the exact public collection ID, returned schema identity and content hash:
the collection's major-version suffix alone does not identify its minor schema.

Both collection schemas use these native feature-version fields:

| Field | Type and meaning boundary |
| --- | --- |
| `versiondate` | Required string with `date` format |
| `versionavailablefromdate` | Required string with `date-time` format |
| `versionavailabletodate` | Required string or null with `date-time` format; null is admitted |

The initial helper looked for `version`, `versionnumber` or `versionid` and found
none. Those names are absent from the returned schemas. Its zero generic-version
counter therefore does not demonstrate missing source version information. Its
date counter also does not prove that all three native version fields passed
their formats or temporal consistency checks. No additional feature request was
made to resolve this: the discarded samples cannot be validated retrospectively.

The queryable lists contain none of these three version fields. They must not
become arbitrary client-supplied CQL predicates merely because they appear in a
feature schema. Their return and filtering contracts are separate.

### A concrete Road Link schema defect

The observed Road Link schema has `additionalProperties: false`, but requires
two names that differ in case from their declared properties:

| Name in `required` | Name in `properties` |
| --- | --- |
| `presenceOfstreetlight_coverage` | `presenceofstreetlight_coverage` |
| `presenceofcyclelane_overallPercentage` | `presenceofcyclelane_overallpercentage` |

JSON property names are case-sensitive. For an object, those required names are
also forbidden additional properties, so the unmodified observed schema cannot
validate a complete road-link record. Preserve the upstream document and hash.
Do not silently repair it or report a full-schema pass. Obtain a corrected source
schema or explicitly review, version and test a narrowly scoped compatibility
rule before using it as an admission gate. This issue does not change the already
observed HTTP access or bounded geometry results.

## Validation strategy before a hosted extension

1. Keep the GeoJSON feature wrapper separate from the collection record schema.
   The returned schema describes native attributes plus `geometry`, not a whole
   `FeatureCollection`. Require an object explicitly: neither collection schema
   declares a root `type`. Define and test the exact mapping from feature
   properties and geometry, refusing collisions, and check feature ID/OSID
   equality in memory without publishing either value.
2. Use a pinned Draft 7 validator with UUID, date and date-time format checks
   enabled. Respect required-but-nullable fields, nested arrays and source units.
   Retain the original schema and identify any reviewed compatibility projection
   separately. Resolve the Road Link defect before claiming full conformance.
   The current locked Python environment exposes UUID and date checkers but has
   no date-time checker registered. Passing `FormatChecker` alone therefore does
   not enforce this format. Add and test a strict checker or pinned dependency;
   do not accept an unknown-format pass as temporal validation.
3. Pin the external geometry schemas in an offline reference registry. The
   building schema references `https://geojson.org/schema/Polygon.json`; the road
   schema references `https://geojson.org/schema/LineString.json`. Neither was
   fetched in the four-request phase. Deny automatic remote reference retrieval
   at validation time. GeoJSON structural validation still needs separate CRS,
   coordinate, topology and deterministic spatial checks.
4. Build public synthetic cases for valid and missing fields, nulls, invalid
   dates/UUIDs, wrong units/CRS, geometry failures, unexpected properties and the
   two source-schema case mismatches. Add no licensed sample fixture. A later
   authorised live check should validate ephemeral records against the pinned
   contract and retain only aggregate outcomes and receipt hashes.
5. Admit a narrow fixed-collection tool contract with rights-aware evidence,
   durable allowance, cancellation and storage behaviour. The current open-data
   receipts label their sources as OGL; they cannot be reused unchanged for
   protected or mixed-source results. Test denied access, missing entitlement,
   stale schema, truncated results and provider failures without a paid fallback.

## Useful future MCP questions

These are proposed questions, not current advertised capabilities.

| Question | Required answer boundary |
| --- | --- |
| Show a small sample of building footprints in the approved area, with OS-recorded footprint area and height evidence. | Preserve whole-feature square metres, height units, evidence dates and nulls. Do not present whole-feature area as clipped area or infer households. |
| What use and physical-state classifications does OS record for the selected building? | Use the validated source fields and dates; do not infer occupants, addresses, ownership or current occupation. |
| Show a small sample of road links, their classifications and recorded lengths. | Preserve native geometry and metre units. The sample does not establish a connected network, complete route or legal access. |
| What bus-lane or cycle-lane provision does OS record on these selected links? | Validate v5 field names, directional measures, percentages and evidence dates. Do not turn a feature attribute into a routing or safety recommendation. |
| Which collection, schema and feature-version dates support this result? | Bind the approved query, source version and rights to a protected evidence receipt; inspection must not silently refresh the provider. |

The next evaluation must measure semantic correctness and denial behaviour before
performance. It needs separately labelled full-record schema, geometry, rights,
receipt and hosted-access outcomes. Repeated timings should hold the admitted
collection, query, schema and runtime constant and report the sample size. The
open-data profile remains available while those NGD gates are completed.
