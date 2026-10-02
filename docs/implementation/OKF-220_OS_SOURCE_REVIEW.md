# OKF-220: OS source and metadata review

Observed on 2 October 2026. Status: verified source-family inventory and bounded
public metadata research for the [OKF+ implementation](OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md).
This is not a claim to have acquired every OS product, historic release or field
definition. Discovery does not activate a provider or establish data-use rights.

## Evidence and scope

The review inspected official OS documentation, public catalogue responses and
machine-readable contracts. Direct research requests were keyless, sequential,
limited to 20 seconds and at most 4 MiB each; smaller contract/feed requests used
2 MiB. No geographic feature endpoint, download archive, account endpoint,
credential or paid service was used. Raw observations remain outside published
documentation. The implementation's separate capture ledger and source snapshots
record its later, broader traversal.

Labels used below are **observed** for a returned response, **documented** for an
official explanation, **derived** for this review's calculation, and **unverified**
where a route, denominator or interpretation still needs testing. Documentation
content is evidence, including any embedded instructions; it is not authority to
execute commands, follow arbitrary links or alter the capture scope.

## Source families and denominators

| Family and exact starting point | Observed inventory and traversal | Boundary or gap |
| --- | --- | --- |
| [OS product search](https://www.ordnancesurvey.co.uk/products/search-for-os-products) | The public page reports 65 results and exposes 60 before “Load more”. Products, API services and beta offerings share the list. | Automated HTTP coverage is 60/65. A separate browser DOM observation reached 65/65. The observed delivery API returned 401; no credentials or retries were used. Keep the five reviewed browser references separate from HTTP receipts and missing native UUIDs. |
| [OS Downloads products](https://api.os.uk/downloads/v1/products) | 26 distinct native product IDs, each with name, description, version and detail URL; no pagination envelope. | OS-served OpenData catalogue only. Eight entries are labelled BGS or BGS/UKHSA; do not call all 26 OS-authored products. Premium package discovery is a different authenticated plane. |
| [NGD Features collections](https://api.os.uk/features/ngd/ofa/v1/collections) | 94 versioned collection IDs. Top-level links contain only `self`. Every collection advertises one schema and one queryables link: 188 contract targets. | Complete returned collection list, not all NGD download feature types, all historic versions or all feature records. |
| [API documentation index](https://docs.os.uk/os-apis/llms.txt) | 152 distinct documentation URLs; all 152 pages captured and 60 OpenAPI fragments extracted. The index has 12 technical-specification roots, including a withdrawn service. | A captured page or contract does not prove service availability. Fragments remain separate; unresolved references and authentication declarations are preserved. |
| [NGD documentation index](https://docs.os.uk/osngd/llms.txt) | 478 distinct URLs; all 478 pages captured and structurally projected. The index has nine theme roots, 142 data-structure descendants and 221 code-list descendants, plus their overview. | Counts are URL classes, not distinct feature types, fields or controlled values. Six projections are truncated; complete page acquisition does not close semantic or vocabulary coverage. |
| [Download documentation index](https://docs.os.uk/os-downloads/llms.txt) | 1,673 distinct URLs under seven product portfolios and supporting guidance/history. Both pages in the separate two-guide refresh/withdrawal cohort were captured and structurally projected. | The complete index is not complete page acquisition. It includes release-note templates and older documentation. Product families, releases and guide pages remain separate entities. |
| [OS GEMINI catalogue](https://osmetadata.astuntechnology.com/geonetwork) | Officially linked by the [NGD catalogue guidance](https://docs.os.uk/osngd/extra-links/data-catalogue). Corrected traversal captured 156/156 distinct metadata UUIDs with a stable reported total and no duplicates. | The advertised `startIndex` repeated the first ten UUIDs; the explicit corrected traversal uses documented lowercase `startindex`. Equal-count substitutions during a changing catalogue remain possible. Catalogue `/items` records are metadata, unlike NGD geographic `/items`. |
| [FAQs](https://docs.os.uk/os-apis/core-concepts/faqs), [API change log](https://docs.os.uk/os-apis/service-and-data-status/change-log), [NGD change log](https://docs.os.uk/osngd/os-ngd-news/change-log) and [withdrawal notices](https://docs.os.uk/os-downloads/resources/product-resources/end-of-life-product-notices) | Source-linked operating explanations, documentation changes, planned enhancements and product retirement evidence. | These do not form a complete data-release event stream or establish how often users encounter a problem. |

The [OS product overview](https://www.ordnancesurvey.co.uk/products) adds OS Net
positioning data to the seven familiar data portfolios. GNSS/RINEX and other
specialist products therefore cannot be assumed covered by the Downloads
documentation structure. Maps, raster, imagery, tiles, feature services, search,
identifiers and downloads also describe different delivery capabilities.

### Reproducible observation binding

The five primary captures below returned HTTP 200 between 01:12:40 and 01:12:42
UTC. The documentation denominator is distinct exact URLs matched by
`^- \[(.*?)\]\((https://[^)]+)\)` in multiline mode. An earlier restrictive
title parser omitted 11 download-documentation titles containing escaped square
brackets; all were templates. The corrected count is 1,673 against the same
unchanged source bytes. Neither labels nor similar URLs were semantically merged.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| API index | 20,863 | `68c2d2f6cdb5fb4b3d9da9d2f67c1d30de9a232e578dc7341155fb249333280f` |
| NGD index | 64,264 | `d800778698a17411c3345148f3736a5c4c4d30ece426844bdad3b77508183e9d` |
| Downloads index | 382,384 | `43c91058e6e5b775024035cb198f85b7ac21f9305d483c3ed6ea0918201c12ad` |
| OpenData product list | 13,987 | `7a61842705bd7e0b74b80f0faf7e3a473f29ebb2dd1e486d82cf64fd783f6be1` |
| NGD collection list | 195,642 | `cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9` |

## APIs, schemas and controlled values

The current [API documentation](https://docs.os.uk/os-apis) groups 11 service
families: NGD Features, NGD Tiles, Features, Vector Tile, Maps, Places, Names,
Linked Identifiers, Downloads, Net and OAuth 2. Its index also retains the
Match & Cleanse technical specification. Preserve that withdrawn service as
historical evidence rather than making it discoverable as a current capability.

Machine-readable contracts are available in JSON fences on individual endpoint
Markdown pages. Three inspected examples are:

| Endpoint documentation | Declared contract | Meaning |
| --- | --- | --- |
| [NGD schema](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/schema.md) | OpenAPI 3.0.1; service version `v1.8.1` | One documented operation, `/collections/{collectionId}/schema`, and its enumerated collection parameter. |
| [Names find](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md) | OpenAPI 3.0.1; `v1.0` | Search parameters, response structures and documented authentication. |
| [Downloads products](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md) | OpenAPI 3.0.0; `1.0.0` | OpenData catalogue operation, distinct from acquiring a download. |

A technical-specification parent page need not contain a contract. Preserve each
fragment's source URL, retrieval time and digest before combining operations.
Conflicting component definitions, unresolved references, incompatible versions
and documented security requirements must survive extraction. Documentation
operation examples are not permission to call those operations.

For legacy [OS Features](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification),
WFS capabilities and `DescribeFeatureType` provide service metadata and XSD;
`GetFeature` supplies geographic records. The [FAQ](https://docs.os.uk/os-apis/core-concepts/faqs)
explicitly distinguishes this service from NGD Features. A common “OS Features”
label must not collapse the two protocols or their product coverage.

The 94 live NGD collection IDs have these native theme prefixes:

| Prefix | Versioned collections |
| --- | ---: |
| `asu` | 2 |
| `bld` | 8 |
| `gnm` | 4 |
| `lnd` | 7 |
| `lus` | 5 |
| `str` | 9 |
| `trn` | 49 |
| `wtr` | 10 |

Removing a terminal numeric version suffix produces 69 groups, a **derived naming
heuristic**, not an authoritative feature-type denominator. The nine documented
themes additionally include Address; the two live `asu` collections are GB
postcode unit area/point. A blanket assertion that Administrative and Statistical
Units are unavailable through the API is therefore already incorrect.

Each observed collection contains its native identifier, description, supported
CRSs, storage CRS, item type, spatial/temporal extent and typed links. Follow
`describedby` to `/schema` and the OGC queryables relation to `/queryables`; do
not follow the geographic `items` relation. Keep the collection's major-version
suffix, returned schema identity, minor version and hash separately.

The [Building field documentation](https://docs.os.uk/osngd/data-structure/buildings/building-features/building)
adds meanings, nullability, units, lengths, code-list references and schema
applicability. These enrich a structural schema, while queryables identify the
filtering contract. The [bounded NGD validation](SITES-218_NGD_VALIDATION.md)
already shows different field/queryable counts and an upstream Road Link
required-property casing defect. A syntactically valid schema is not proof of
record conformance; preserve defects and prohibit automatic remote reference
fetches during validation.

Code-list discovery starts with the [code-list overview](https://docs.os.uk/osngd/code-lists/code-lists-overview)
and indexed children. Count lists, list versions and values separately; paths
such as `physicallevelvalue` and `physicallevelvalue-1` require inspection before
deduplication. OS [schema-versioning guidance](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning)
states that versions apply per feature type. Older major schemas may remain
maintained and receive data updates; minor versions replace their predecessors.
Code-list additions increment that list's version and implementing schemas'
minor versions. An old schema is therefore not necessarily an old data snapshot.

## Releases, currency and historical coverage

Store retrieval time, metadata modification, documentation revision, publication
date, data-cut date, feature validity, schema version and retrievable history as
different properties. A catalogue's `version` is a source-native label: some
OpenData entries use `2026-10`, while partner entries use labels such as
`Version 5`. Do not invent an ISO date for the latter.

| Source evidence | Required interpretation |
| --- | --- |
| [Product refresh dates](https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates) | Cadence differs: Open Names and Code-Point Open are quarterly; Open USRN monthly; Open UPRN and Open Linked Identifiers six-weekly; Terrain 50 annual. Publication and data-cut dates are distinct. A scheduled month does not establish that its release has already occurred. |
| [NGD ordering and currency](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/os-ngd-data-ordering-and-currency) | Source updates and delivery schedules differ. Many feature collections update daily; Transport Network/RAMI and GB postcodes monthly; Water Network quarterly. Availability also differs by delivery service. Full supply, change-only updates and filtered delivery are different products of the same source. |
| [Temporal filtering](https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering) | Select+Build offers a one-off past/current snapshot. Most feature types begin on 29 September 2022; later additions have later start dates. A request before a feature type existed can return no records. This is a documented ordering capability, not a tested current API predicate. |
| Observed NGD collection extents | All 94 intervals have an open end; starts range from 30 July 2022 to 19 February 2026. Preserve those advertised values without overriding service-specific temporal-filter rules or claiming every intervening version can be retrieved. |
| [Features product availability](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/what-data-is-available) and [Product Archive](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/os-product-archive) | Annual archive snapshots use the last full release of the calendar year. Documented families include Highways from 2016, ITN Roads 2004–2019 and ITN Urban Paths 2010–2019. This is not arbitrary daily history. |
| [NGD change log](https://docs.os.uk/osngd/os-ngd-news/change-log) | Documentation changes include previews of later releases. Preserve explicit preview/current/retired status; a future attribute in documentation does not establish availability in a live collection. |

The current Features availability page explicitly records Detailed Path Network
withdrawal on 30 September 2026 and Water Network withdrawal on 31 March 2026.
Retained product documentation is useful history, but must not revive those
routes. The product-refresh page also distinguishes a final data release from
the later withdrawal date. Source status needs its own effective date.

The GEMINI landing page advertises a [metadata RSS feed](https://osmetadata.astuntechnology.com/geonetwork/api/collections/main/items?f=rss&sortby=-createDate&size=30).
It returned 10 items despite the requested size of 30. This is a recent metadata
feed, not proof of complete product release history. Its [OpenSearch description](https://osmetadata.astuntechnology.com/geonetwork/api/collections/main?f=opensearch)
advertises JSON, XML, DCAT, schema.org and RSS representations with zero-based
`startIndex`. The first JSON response uses `hits.total.value: 156`,
`hits.total.relation: "eq"` and 10 `hits.hits`; it has no next-page link. Preserve
UUIDs and distinguish `resourceDate` from catalogue `createDate`/`changeDate`.
Named contacts and account-oriented response fields are unnecessary for a public
knowledge projection and must be omitted.

## Source-backed questions and common mistakes

These are proposed evaluation questions derived from official guidance, not
findings from user interviews or measured support volumes.

| Question | Expected distinction and source |
| --- | --- |
| Can I use OS Features API to retrieve NGD buildings? | Select NGD Features, preserving protocol and collection version; the [FAQ](https://docs.os.uk/os-apis/core-concepts/faqs) says WFS Features does not expose NGD. |
| Why is an attribute missing from an NGD vector tile? | Tiles use a visualisation subset of types and attributes; do not infer absent source data. [Tiles FAQ](https://docs.os.uk/os-apis/core-concepts/faqs) |
| Can I filter on every field in a feature schema? | Consult the collection's queryables separately; missing filter capability is not a missing returned attribute. [Queryable contract](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables) |
| Does an old major schema return old features? | No such inference: maintained schemas continue receiving updates. [Versioning](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning) |
| Why is a newly introduced feature type empty in annual supply? | Annual supply represents 1 January; a later addition may not appear until the next annual snapshot. [Versioning and annual supply](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning) |
| Does a postcode label imply the same geography across products? | Preserve GB/NI scope and point/area representation; the live catalogue distinguishes them. [Collection catalogue](https://api.os.uk/features/ngd/ofa/v1/collections) |
| Can an archived technical specification justify a current provider call? | Check service/product withdrawal and actual live discovery before admission. [Availability and withdrawals](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/what-data-is-available) |
| Is the latest catalogue modification the date the geography was true? | Preserve metadata and feature dates independently; decline an unsupported historical claim. [Temporal filtering](https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering) |

## Capture and modelling recommendations

1. Use fixed official origins and closed metadata route patterns. Separate
   acquisition of source documents from projection of structural facts,
   identifiers, controlled values and citations. Never publish whole guide text
   merely because it was publicly readable.
2. Record source URL, final URL, HTTP status, retrieval time, byte count, hash,
   content type, ETag and Last-Modified when provided. Preserve failed attempts,
   truncation and pagination state; retries consume the same central budget.
3. Measure coverage separately for source families, product IDs, versioned
   collections, schemas, schema fields, queryables, code lists, values, guide
   references and tested questions. Unknown denominators remain unknown.
4. For documentation, retain exact URL/title and classify templates, previews,
   migrations, withdrawals and historic releases. For OpenAPI, preserve native
   operation IDs, parameter names, methods, paths, server declarations and
   security references without exposing arbitrary execution.
5. For catalogue pagination, compare stable reported totals, unique IDs and
   forward progress. Reject duplicate/non-progressing pages as completeness
   evidence. Even a stable total cannot exclude equal-count substitutions during
   a changing catalogue; record the capture interval.
6. Keep rights, reachability, provider admission and content acquisition separate.
   The owner-authorised metadata build does not imply universal PSGA eligibility,
   redistribution, third-party processing approval or a paid fallback.

The final captured cohorts close the 156-record GEMINI traversal, all 152 indexed
API pages, all 478 indexed NGD pages and the two selected Download guides. Product
search is reconciled to 65 entries through two explicitly different evidence
methods: 60 HTTP records and five browser references. The implementation also
captured all 94 advertised schemas and all 94 queryables. Their source snapshots
and generated coverage report supply the acquisition evidence; none of these
counts proves field semantics, full code-list/value coverage or a complete release
history. Those semantic and temporal relations remain acceptance work. Premium
account/package inventories, exhaustive historical releases, all specialist
products and every documentation claim remain outside any completeness assertion.


## Implementation capture and catalogue corrections

The later capture retained all 152 indexed OS API pages and extracted 60 OpenAPI
fragments, containing 60 operation declarations: 59 GET and one POST. There
were no JSON-fence extraction errors. Thirty-one operations inherit a documented
root security declaration; 29 have no security declaration, which is unknown
rather than public access. All seven selected lifecycle guides were captured. These are separate
denominators: a page can have no contract, and a contract fragment can document
several operations. Extraction keeps native operation IDs, HTTP methods, paths,
parameters, schema constraints, references and declared authentication. A safe
HTTP method or a response property's `readOnly` annotation does not authorise a
provider invocation; every operation remains `callable: false` and
`admission: not-reviewed`. Descriptions, examples and guide text remain outside
the public structural projection. Unresolved component classes and references
are retained as limitations rather than silently resolved over the network.

The GEMINI OpenSearch template uses camel-case `startIndex`. The observed second
page repeated the same ten metadata UUIDs, so the harvester stopped at 10/156
instead of claiming completion. The official
[GeoNetwork OGC API Records README](https://github.com/geonetwork/geonetwork-microservices/tree/main/modules/services/ogc-api-records)
documents lowercase `startindex` and `limit`. Two subsequent bounded probes with
`startindex=0&limit=10` and `startindex=10&limit=10` each returned ten records,
reported the same exact total of 156 and had zero UUID overlap. The explicit
`--gemini-documented-pagination` option records both the defective advertised
template and the reviewed traversal template. It does not silently retry failed
pages or erase the original pagination defect. The final
`os-gemini-metadata` snapshot records 156 distinct UUIDs from an exact, stable
reported total of 156, no duplicates and no stop reason. This closes that returned
catalogue cohort, without claiming a transactionally frozen source or complete
product release history.

For the product catalogue, the browser's rendered completion count was 65/65,
while the initial public HTML retained only 60 entries. The observed delivery API
returned 401. No credentials were sought and no repeated request was made. An
optional `--product-ui-supplement` accepts reviewed product URLs, titles, the
observation date, the source page and the visible completion count. It adds no
network request. Initial HTML coverage remains 60/65; the final `combinedCoverage`
records 65/65 reviewed entries after adding the five browser references. The five browser-only entries have
no captured native UUID, HTTP response hash or retrieval timestamp. Their local
reference identity is the canonical product URL; this must not be represented as
an OS-assigned identifier. An entry's existence in the catalogue does not establish
current availability: retirement evidence is still needed.

The offline OS contract tests cover schema/security preservation, partial-page
and duplicate detection, the corrected documented pagination, the separation of
browser and HTTP evidence, forbidden reference routes, XML entity rejection and
parsing catalogue state without executing source JavaScript. Fixtures are
synthetic public metadata contracts; they make no live-provider claim.

### Final documentation capture and extraction limits

The frozen source snapshots distinguish navigation references from captured
pages. [`osngd-documentation-pages.json`](../../okf-plus/source/osngd-documentation-pages.json)
records 478 attempted, captured and structurally projected pages against 478
indexed URLs, all with HTTP 200 evidence. Recorded source retrieval times span
07:29:13 to 08:23:29 UTC on 2 October 2026, including reused capture evidence.
[`os-download-guide-pages.json`](../../okf-plus/source/os-download-guide-pages.json)
records two attempted, captured and projected pages against its selected two-page
cohort. These are the refresh-date and withdrawal guides already present in the
1,673-entry Download index. They overlap the earlier seven-guide lifecycle
capture and must not be counted as seven additional unique pages.

Derived directly from those projections:

| Projection measure | Indexed NGD pages | Selected Download guides |
| --- | ---: | ---: |
| Captured/projected pages | 478/478 | 2/2 |
| Pages with retained table structure | 319 | 2 |
| Retained table structures | 428 | 7 |
| Tables with at least one retained native row | 298 | 6 |
| Retained native rows/cells, including compact labels | 6,397/6,412 | 83/207 |
| Explicitly omitted table cells | 12,124 | 44 |
| Pages flagged `projectionTruncated` | 4 | 0 |

Table shapes and selected labels are factual structural metadata. The initial
projection omitted 17,929 cells because their headers were not admitted; 5,936
were labelled `Label`, 5,428 `Definition`, 839 had blank headers and 525 were
labelled `Description`. This was an extraction gap, not missing upstream values.
The reviewed code-list lane contains 231 `Label`/`Definition` tables, four with
an additional blank column and two `Label`/`Description` tables. Its other two
tables are overview navigation and a network illustration, not admitted label
tables.

The v2 projection retains all 6,067 native label rows from those 237 admitted
tables. It requires an exact code-list descendant route and reviewed header
shape. The 1,024-row ceiling accommodates the two largest tables, whose 579 and
576 rows exceeded the previous 512-row ceiling. Labels have a separate bound of
160 characters, 640 UTF-8 bytes and 32 words; the observed maxima are 147 bytes
and 27 words. Definitions and descriptions remain private. The compact
`os-documentation-native-label-table.v1` representation declares columns
`sourceRow` and `nativeText`; it preserves duplicate labels, exact decoded text
and table/row identity without repeated cell-object keys. All source label rows
are retained, but this is not a unique-term denominator or an API enum assertion.

For example, [access type](https://docs.os.uk/osngd/code-lists/code-lists-overview/accesstypevalue)
has three native labels, including `Pedestrian`; [address classification code](https://docs.os.uk/osngd/code-lists/code-lists-overview/addressclassificationcodevalue)
has 579 rows, with `C` and `CA` under `Label`, not a column named `Code`.
[Physical level](https://docs.os.uk/osngd/code-lists/code-lists-overview/physicallevelvalue)
and its separately indexed `physicallevelvalue-1` page retain separate source
identities; similar titles and values do not establish equivalent versions.
The 94 machine-readable collection schemas are a separate source of enum
constraints; documentation labels are not silently substituted for them.
The withdrawal guide has a retained table structure but no projected native rows,
so it supplies references rather than a complete retirement-event table.

The four remaining truncation flags affect the FME and GDAL GeoPackage guides,
NGD improvements and Building pages. Flags include headings or references exceeding
the projection's limits; they do not indicate a failed HTTP capture. The Building
page retains 96 of 105 recognised headings. Narrative definitions, unrecognised
columns, examples and contacts are deliberately omitted; native cell text is not
a typed schema assertion. The exporter also removed the appended agent-instruction
section from all 480 pages, and removed 11 fenced blocks and 18 example/contact
sections across the NGD cohort. Land-use/NLUD relationship tables still need a
separate reviewed mapping; they are not treated as flat code lists. These
omissions are recorded, not interpreted as
absence from the source.

Full raw originals and acquisition receipts remain in private ignored evidence.
The v2 replay used only retained bodies, with network operations denied. The
478 original response hashes, capture receipts, source-index hash and capture
ledger were unchanged. The updated snapshot SHA-256 is
`b716faf7b9bdf87b95f59b63e56dc76152d9f13971fcc1c9f44bf1c853421731`.
All 478 complete mapped documentation evidence texts fit the unchanged pinned
100,000-character consumer limit; the largest is 47,812 characters. This size
check is distinct from the final whole-corpus consumer validation. Eighteen
synthetic documentation tests pass, including route/header scope, literal label
preservation, duplicate row identity, instruction/contact rejection and explicit
row/byte omissions.

Public records retain source hashes, canonical URLs, bounded headings, typed
references and the supported structures. No discovered reference was followed as
part of extraction. `catalogueComplete: true` closes only the stated page cohort;
`globalDocumentationComplete: false` remains explicit. Complete NGD field meanings,
code-list identity/version/value relationships, effective-dated release relations,
and the unselected Download page contents remain gaps for a separately measured
increment.

## Geospatial concept and ontology review

The authored concept layer contains 89 draft concepts, with 33 distinct official
reference URLs. Definitions and scope boundaries are hand-normalised statements,
not copied guides. They cover geometry and topology; coordinate systems and units;
vector, raster, tiles, coverage, sensors and 3D; time, quality and provenance;
statistical dimensions and code lists; UK identifiers, geography vintages,
postcode allocation and exact/best-fit methods; and rights, releases and refresh.
This is an extensible starting set, not an exhaustive geospatial ontology.

Each record preserves an official reference, an agent review date and a scope
boundary. `reviewStatus: source-reviewed` means the agent checked the cited primary
source; it is not independent human acceptance, licence advice or evidence of a
fresh HTTP capture. Review-only references therefore do not invent `retrievedAt`
or a response digest. GOV.UK, OS and ONS explanatory pages are source references,
not automatically formal standards. All records retain the metadata-only execution
boundary.

There are 85 associative `skos:relatedMatch` links using 62 distinct external
terms, plus internal `skos:related` links. These are actual RDF predicates in the
source, not merely namespace declarations. No `skos:exactMatch` or
`owl:equivalentClass` claim is made. The
[SKOS reference](https://www.w3.org/TR/skos-reference/) permits a resource to be
both a SKOS concept and an OWL class or property, but that does not turn an
associative mapping into class equivalence or prove ontology conformance.

| Reference family | Actual external terms used in concept mappings | Interpretation and status |
| --- | --- | --- |
| [GeoSPARQL 1.1](https://docs.ogc.org/is/22-047r1/22-047r1.html) and its Simple Features vocabulary | `geo:Feature`, `geo:Geometry`, `geo:SpatialObject`, `geo:hasGeometry`, `geo:hasBoundingBox`, `geo:sfContains`, `geo:sfDisjoint`, `geo:sfIntersects`, `geo:sfWithin`; Simple Features `Point`, `LineString`, `Polygon`, `GeometryCollection`; `geof:getSRID` | OGC standard terms. The `getSRID` mapping connects the CRS concept to the function returning a geometry's CRS identifier; it does not say a CRS is a function. |
| [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) and [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) | `dcat:Dataset`, `Distribution`, `DataService`, `version`, `spatialResolutionInMeters`; DCMI `identifier`, `issued`, `temporal`, `spatial`, `accrualPeriodicity`, `accessRights`, `rightsHolder`, `conformsTo`, `relation`, `extent`, `LicenseDocument`, `Standard`, `LocationPeriodOrJurisdiction` | DCAT is a W3C Recommendation; DCMI maintains its terms. General metadata associations are deliberately broader than product-specific concepts. |
| [RDF Data Cube](https://www.w3.org/TR/vocab-data-cube/) | `qb:Observation`, `DimensionProperty`, `MeasureProperty`, `AttributeProperty`, `DataStructureDefinition`, `codeList`; SDMX `attribute#unitMeasure` and `dimension#refPeriod` | W3C Recommendation and the SDMX vocabulary terms used by it. Unit and reference period remain distinct from measures and release dates. |
| [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [OWL-Time](https://www.w3.org/TR/owl-time/) and [PROV-O](https://www.w3.org/TR/prov-o/) | SOSA `Sensor`, `Observation`, `ObservableProperty`, `FeatureOfInterest`, `Result`, `phenomenonTime`, `resultTime`; Time `Instant`, `Interval`, `Duration`; PROV `Entity`, `Activity`, `Agent`, `wasDerivedFrom` | W3C standards-backed vocabularies. Observed phenomenon time, result time, dataset reference period and provenance activity are separate concepts. |
| [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) | `dqv:Dimension`, `Metric`, `QualityMeasurement`, `QualityPolicy` | W3C Working Group Note, not a Recommendation. A quality measurement or policy link does not certify fitness for a particular use. |
| [SKOS](https://www.w3.org/TR/skos-reference/), RDF and the [EPSG CRS reference](http://www.opengis.net/def/crs/EPSG/0/27700) | `skos:ConceptScheme`, `skos:relatedMatch`, `rdf:Property`, EPSG 27700 | SKOS/RDF provide modelling terms; EPSG 27700 identifies British National Grid. The CRS identifier alone does not perform a coordinate transformation. |

The review removed four unsupported `geo:hasSRS` mappings and replaced the fifth,
for coordinate reference system, with the verified `geof:getSRID` association.
Datum, axis order, height datum and coordinate transformation retain their checked
definitions and internal relationships without a guessed external mapping.
`geo:hasSRS` is not asserted as a GeoSPARQL 1.1 property.

Additional definition references include the OGC WMS, WMTS, Tile Matrix Set, CIS
and CityGML standards; the LAS Community Standard; RFC 7946; official OS/ONS
methodology and identifier guidance; and the SDMX glossary. The
[Spatial Data on the Web Best Practices](https://www.w3.org/TR/sdw-bp/) reference
is a W3C Group Draft Note/OGC best-practice document, not an OGC implementation
standard. A concept's citation to one of these documents does not establish
conformance of a dataset, API, calculation or tool to that document.
