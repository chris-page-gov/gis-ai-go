# OKF-220: ONS source-family review

Reviewed on 2 October 2026. Scope: public metadata, schemas, specifications and
discovery guidance for the authorised OKF+ inventory. This review acquired no
statistical observations, feature geometries, licensed payloads or credentials.
Facts below are distinguished from proposed harvesting methods and coverage gaps.

## Finding

ONS has several overlapping dissemination systems. A complete traversal of the
dataset API is useful but cannot establish complete ONS coverage. Keep distinct
inventories for the dataset API, Nomis, the Open Geography portal, Census query
definitions, website publications and supporting classifications/methodology.
Retain links between their native identifiers rather than merging similar titles.

The shared capture currently contains 338 unique ONS dataset identifiers and
1,617 Nomis key families. Independent bounded probes observed 39 Census
population types and 6,719 public ArcGIS items in the ONS organisation. These are
different units, not additive counts of datasets. The population and ArcGIS probes
read only the first page; their totals are reported denominators, not proof of
complete retrieval. See the source snapshots for the capture's later traversal
evidence: [ONS datasets](../../okf-plus/source/ons-datasets.json) and
[Nomis definitions](../../okf-plus/source/ons-nomis-datasets.json).

## Verified source families

| Family and official entry point | Native unit and traversal proposal | Coverage boundary |
| --- | --- | --- |
| [ONS dataset catalogue](https://api.beta.ons.gov.uk/v1/datasets), [contract](https://developer.ons.gov.uk/dataset/datasets/) | Dataset ID; page with `limit`/`offset`, reconcile unique IDs against `total_count`, then traverse editions and versions. | All datasets exposed by this API; excludes other dissemination systems. Capture `type`: a static download dataset need not support observations through the API. |
| [Dataset metadata routes](https://developer.ons.gov.uk/dataset/) | `/datasets/{id}/editions/{edition}/versions/{version}` and its `/metadata`, `/dimensions`, `/dimensions/{dimension}/options`. Keep dataset/edition/version together. | Capturing the advertised latest version is a current metadata inventory, not all historic versions. Missing version/dimension/time metadata remains unknown. |
| [ONS website search](https://developer.ons.gov.uk/search/search/) | `https://api.beta.ons.gov.uk/v1/search`; content type, topic, URI, dataset ID and CDID. Page with `limit` up to 1,000 and zero-based `offset`. | Query-index scope differs from the dataset API. Record `count`, `distinct_items_count`, content-type counts, filters and unique URIs separately; do not assume those counts are interchangeable. |
| [Release catalogue](https://developer.ons.gov.uk/search/search-releases/) | `https://api.beta.ons.gov.uk/v1/search/releases`; release URI, status and scheduled date. Enumerate published, upcoming and cancelled entries, with explicit date windows. | A release is a publication event and can contain several datasets or articles. Its date is not an observation period. |
| [Nomis API](https://www.nomisweb.co.uk/api/v01/help), [complete returned definitions](https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json) | `structure.keyfamilies.keyfamily`; preserve `NM_*` ID, components and referenced codelists. The full definition document is a direct denominator for this returned catalogue. | Nomis has its own catalogue and historical coverage. A definition and codelist reference do not prove all code values, dates or observations were acquired. |
| [Nomis source grouping](https://www.nomisweb.co.uk/api/v01/contenttype/index.json) | Discover content types, then `https://www.nomisweb.co.uk/api/v01/contenttype/sources.json`; reconcile group membership against key-family IDs. | Group metadata is navigation, not an additional count of datasets. Singleton JSON objects and arrays both occur. |
| [Open Geography portal](https://geoportal.statistics.gov.uk/) | ArcGIS item ID, service URL, layer/table ID and product release. Enumerate the portal's configured group union and wider public organisation search separately. | Maps, files, tables, services, guides, historical releases and alternative representations are different item types. An item count is not a unique statistical-product count. |
| [Census population definitions](https://developer.ons.gov.uk/population-types/) | `https://api.beta.ons.gov.uk/v1/population-types`, followed by population-specific area types, dimensions and categorisations. | These describe a query space; combinations are not a finite catalogue of already-published datasets. Only populations marked `type=microdata` support the custom-dataset route. |
| [Code lists](https://developer.ons.gov.uk/code-list/) and [hierarchies](https://developer.ons.gov.uk/hierarchy/) | `/code-lists/{id}/editions/{edition}/codes` and code-to-dataset links; `/hierarchies/{instance_id}/{dimension_name}` and child codes. | List/edition/code and instance/dimension are required identities. Not every dimension has a hierarchy; a code label alone is not an identity. |
| [Topics and navigation](https://developer.ons.gov.uk/topic/) | `/navigation`, `/topics`, `/topics/{id}/content`, `/topics/{id}/subtopics`; deduplicate IDs and record graph traversal. | Topic coverage is a navigation plane. It must not be used as proof that every publication is indexed or every topic has datasets. |
| [Classifications and standards](https://www.ons.gov.uk/methodology/classificationsandstandards), [quality and methodology](https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/qualityinofficialstatistics) | Versioned classification, correspondence table, QMI, user guide and methodology URI; follow explicit dataset/publication links and reviewed landing pages. | No single complete machine-readable denominator was verified. Record reviewed seeds, discovered documents and missing links; avoid claiming exhaustive coverage. |

The dataset API documents rich metadata including release frequency, next release,
units, methodologies and QMI links. These support source selection; a next-release
label such as `TBC` must remain a label, not be converted into a date. Dataset
catalogue and version metadata are separate evidence grains. The API's removed
`@context` field must not be a required parser field.
[Dataset documentation](https://developer.ons.gov.uk/dataset/)

## Geography identity, schema and history

The official portal HTML exposes organisation ID `ESMARspQHYMw9BZ9`, organisation
title `Office for National Statistics` and site item
`e2d91cb940234693bf2c78e5e2d7a504`. Its public
[site configuration](https://www.arcgis.com/sharing/rest/content/items/e2d91cb940234693bf2c78e5e2d7a504/data?f=json)
declares these seven catalogue groups:

```text
b542daa9c43646ac96a7118d655d681d
08656d18ae7b4878a3baae223027f9f1
2ef804ea72844a6ca8aa483ef04ee2c1
0f2e2e23e42d460a9ee70429ba557937
8dcdd2cbc3ae42c1af8c28b0dbc0884b
3a4398bd96ba4cc3a2db74cd10c3d525
f3cd1eb709884b908579039bfef59a6f
```

The broader query is
[`/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1`](https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1).
Search is permission-filtered and eventually consistent. ArcGIS allows at most
100 results per page and accurately reports/retrieves only the first 10,000
matches. Follow `nextStart`, count unique IDs, retain duplicate and mutation
evidence, and use documented sort fields such as `created`. If a query reaches
10,000, partition by documented fields and reconcile overlapping partitions;
10,000 is not proof of completeness. Equal totals cannot rule out substitutions
during pagination. [ArcGIS search contract](https://developers.arcgis.com/rest/users-groups-and-items/search/)

Proposed schema pass: inspect the item's advertised service root and each declared
layer/table's metadata, using `?f=json`. Capture native field names, types, domains,
geometry type, spatial reference, relationships, capabilities and record limits.
Do not call feature `/query`, export or download routes in the metadata pass.
Review service destinations before adding them to the closed URL policy; returned
URLs cannot grant egress authority. Keep item licence and attribution beside the
schema. Layer IDs are local to a service and need a service identity.

[Geographical products](https://www.ons.gov.uk/methodology/geography/geographicalproducts)
include boundaries, postcode products, names/codes and lookups. Preserve product
family, geographic extent, boundary resolution and release separately. ONSPD uses
postcode point-in-polygon allocation; NSPL assigns higher geographies through
Output Area best fit. Neither establishes that every address in a postcode falls
inside the assigned area. The official product guide states quarterly February,
May, August and November releases, but each captured release still needs its own
date and specification. [Postcode products](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts)

The Code History Database covers live and terminated geographic entities,
relationships and code changes from 1 January 2009; it is a separate history
source, not a reason to equate old and current area codes. Its overview is dated
2016, so current downloadable format and edition require portal evidence.
[CHD overview](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups/codehistorydatabasechd)

## Time, revisions and change discovery

Store four dates independently: retrieval time, metadata modification/publication
time, statistical reference period and geography/classification validity. A title
containing a year is only a source title unless the source explicitly defines its
meaning. Preserve original strings and derive parsed dates only with a recorded
rule. Empty temporal metadata is `unknown`, never an inferred earliest/latest
year. Do not infer continuity or completeness between minimum and maximum dates.

For ONS datasets, time-dimension options can establish published period codes for
the selected version without fetching observations. Preserve all returned native
labels/codes and the pagination denominator. For Nomis, the API documents time
codelists and `.metadata.json` routes carrying period and revision annotations;
the full definition document alone supplies release/update metadata, not full
time coverage. Frequency can be a dimension with several values. Keep the exact
native period, frequency and release strings rather than reducing them to one
assumed cadence. [Nomis metadata contract](https://www.nomisweb.co.uk/api/v01/help)

Nomis provides population, society and labour-market statistics, including earlier
census catalogues listed for 1921, 1931, 1951, 1961, 1981, 1991 and 2001 alongside
2011/2021. This does not mean every measure is available for every census or area.
Some labour-market series extend back to the 1970s, but exact dataset coverage
requires its metadata. [Nomis home](https://www.nomisweb.co.uk/),
[first-time visitor guide](https://www.nomisweb.co.uk/home/newuser.asp)

For the release catalogue, use explicit inclusive `fromDate`/`toDate` windows,
`limit`/`offset`, release status and `breakdown.total`. Retain cancelled,
postponed/provisional entries and `date_changes`. Reconcile the unique release
URIs in each window; do not add overlapping status-breakdown counts as if they
were mutually exclusive. [Release API](https://developer.ons.gov.uk/search/search-releases/)

The live release-calendar page advertises this
[RSS link](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)
and an [iCalendar link](https://www.ons.gov.uk/calendar/releasecalendar).
Their link targets were inspected; feed bodies were not fetched in this review.
The RSS link requests ten recent results, so use it as a change signal and never a
historical completeness denominator. Proposed refresh: compare captured metadata
digests, refresh signalled records, and periodically reconcile whole catalogues.
This is a recommendation, not an ONS service-level guarantee.
[Release calendar](https://www.ons.gov.uk/releasecalendar)

## Census, classifications and interpretation

Census 2021 describes England and Wales on 21 March 2021. A new metadata release
does not turn it into a 2026 population estimate. Its QMI describes decennial
frequency and coverage; retain geography, population base and variable
classification with every query definition. [Census QMI](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/qualityandmethodologyinformationqmiforcensus2021)

The custom-dataset service offers many combinations, with dynamic disclosure
checks. Some sensitive or sparse combinations are available only in pre-built
tables or at larger geographies. Enumerating dimensions/categorisations does not
prove that their cross-product will return data; no observation query is needed
to inventory this distinction. [Multivariate products](https://www.ons.gov.uk/census/aboutcensus/censusproducts/multivariatedata),
[custom-dataset API guide](https://developer.ons.gov.uk/createyourowndataset/)

UK SIC 2026 is published, but its adoption into operational ONS statistics is
staged; the guidance identifies the earliest National Accounts implementation as
Blue Book 2031. Preserve the classification actually used by a dataset, including
SIC 2007, and explicit correspondence tables. Never relabel existing industry
codes automatically. SOC 2020 has its own structure, coding index and NS-SEC
derivation documentation. [SIC 2026](https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2026),
[implementation guidance](https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2026guidance),
[SOC 2020](https://www.ons.gov.uk/methodology/classificationsandstandards/standardoccupationalclassificationsoc/soc2020)

Methodology is a source family in its own right: QMI reports, user guides,
glossaries and methodological papers explain comparability and limitations.
ONS requires regular established bulletins to have a QMI, but QMI pages need not
be updated on every statistical release. Therefore a methodology date alone does
not establish staleness or applicability; retain explicit output links and review
changes. [ONS methodology content guidance](https://service-manual.ons.gov.uk/content/content-types/methodology)

## Legacy routes and known discovery gaps

- ONS documents retirement of old aggregate `/data` listings and unversioned
  dataset/timeseries/search APIs. Read deprecation and sunset headers, record
  redirects/failures, and do not append `/data` to arbitrary content pages.
  [Retirement guide](https://developer.ons.gov.uk/retirement/)
- Current time-series discovery uses `/v1/search?content_type=timeseries`, with
  `cdids` and `dataset_ids`; preserve CDID, dataset ID and returned URI together.
  ONS documents `/v1/data?uri=...` for retrieving the series itself, but this can
  include observations and is outside the metadata pass. A stable series URI does
  not pin an observation vintage. [v0 migration guide](https://developer.ons.gov.uk/retirement/v0api/)
- Website downloads, user-requested/adhoc tables, historical Census products and
  archive documents can sit outside the current dataset API. Search and topic
  graphs improve discovery but no verified global denominator covers all of them.
  Record dataset/download links without acquiring statistical files.
- Public API specifications include write, ingestion and publication operations.
  Documentation coverage does not authorise calling them. Use only reviewed
  public metadata GET routes.
- The portal's curated seven-group union, its wider organisation search and
  downstream services need separate coverage rows. Service metadata and schema
  fields remain outstanding until explicitly captured.
- Metadata completeness, temporal-coverage completeness, schema completeness and
  successful evidence retrieval are independent. Failed, missing, oversized,
  deprecated and unsupported records must remain in the denominator.

## Reproducibility and bounded acquisition

Two reviewed Swagger sources are pinned to the latest file-changing commits
observed on 2 October 2026. These pins document reviewed contracts; they do not
prove that the live service runs the same revision.

| Source | Pinned revision | SHA-256 of exact `swagger.yaml` bytes |
| --- | --- | --- |
| [ONS dataset API](https://github.com/ONSdigital/dp-dataset-api/blob/ffe4c71027d7dd88484a408f0b19a823f312dfe6/swagger.yaml) | `ffe4c71027d7dd88484a408f0b19a823f312dfe6` | `269ed359fb2713734f450585027cae102585a6995559686cfe7404829a7d1f5a` |
| [ONS search API](https://github.com/ONSdigital/dp-search-api/blob/f634c78cc362654ddb464c4559d37202ba0034a9/swagger.yaml) | `f634c78cc362654ddb464c4559d37202ba0034a9` | `8b897c35a7c7d98cfef5faa158c8a12d04acebabf69b6eee849f1aaf70b95029` |

Independent probe evidence: `/datasets?limit=1&offset=0` reported 338;
`/population-types?limit=1` reported 39; public ArcGIS organisation search reported
6,719. Portal HTML SHA-256 was
`927407b6e1006b276a47ee61f1185bf59b8f837be477fcfd314d5e8a03444651`;
site configuration SHA-256 was
`4e9888d5162f8793e041c87d024f09e6cf4932da38176d97d0163e0cdc2717c7`.
The review's 4 MiB Nomis body ceiling rejected its full definition response;
the separately bounded shared capturer subsequently retained its complete
catalogue. An oversized response is a recorded limit, not an empty catalogue.

ONS currently documents 120 requests per 10 seconds and 200 per minute across
site/API assets, and 15 per 10 seconds for high-demand assets. These limits can
change. Use a slower per-host budget, a request ceiling, bounded response bodies
and deadlines; stop or respect `Retry-After` on HTTP 429. Identify the bot without
personal contact information. [ONS bot guidance](https://developer.ons.gov.uk/bots/)

Implementation probes subsequently verified that the latest ONS `/metadata`
response includes dimension definitions. For the sampled series, a separate
dimension-list request is unnecessary before traversing native `time` options.
The Nomis compact overview returned release/update dates but no observation-period
bounds. A further bounded
[Nomis time-codelist request](https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1/time.def.sdmx.json)
returned 519 period codes, from `1983-06` to `2026-08`, in 164,568 bytes. It also
provided selected period/revision annotations. This is one metadata sample, not
evidence that all 1,617 time codelists are the same size or have uniform periods.
Retain mixed or unrecognised native period syntax without invented bounds.

The supplemental capturer is
[`scripts/okf_plus/ons_enrichment.py`](../../scripts/okf_plus/ons_enrichment.py).
Its `ons-versions` and `nomis-times` families keep input-snapshot identities,
metadata receipts, failed records and batch denominators. The shared capture
layer owns cumulative request/byte budgets. Nine synthetic tests verify
pagination, duplicate/mutation failure, fixed provider URLs, period ambiguity,
contact exclusion and batch-source consistency. Bulk execution and its eventual
coverage remain separate from this implementation verification.

Proposed next acquisition order: finish distinct catalogue traversals; capture
latest-version metadata/dimensions and Nomis temporal definitions; enumerate
geography service/layer schemas; capture Census query definitions and code-list
editions; then reconcile website methodology, classifications and legacy
discovery. Publish explicit coverage at each grain, with gaps retained. Do not
describe latest-version coverage as the complete historical archive.

## Proposed retrieval and evidence questions

1. Which source offers small-area labour-market statistics, and why is claimant
   count not interchangeable with unemployment?
2. Which datasets cover Warwickshire, at which geographic levels and vintages?
3. Which available periods, frequencies and revisions are explicitly supported
   for this series, and which temporal fields remain unknown?
4. Does “latest” mean latest observation, metadata update, release or revision?
5. Which release superseded an earlier version, and can its source identity still
   be retrieved without silently substituting current values?
6. Is a Census result about usual residents, households or another population,
   and can this variable combination be requested at MSOA level?
7. Why might a custom Census table be unavailable while a pre-built table exists?
8. Which ONSPD/NSPL method fits a postcode-to-statistical-area task, and what
   boundary-straddling limitation should accompany the answer?
9. Is this geography code current, terminated or a historical equivalent, and
   which release supplies the relationship?
10. Which boundary representation and CRS does a service advertise, and are its
    fields, aliases and controlled values captured?
11. Does an industry dataset use SIC 2007 or SIC 2026, and is an official mapping
    available without claiming a lossless correspondence?
12. Which QMI or methodology defines a measure's coverage and comparability?
13. Was an expected release postponed, cancelled or published, and what changed?
14. Which catalogues and schema families were fully traversed, which were only
    sampled, and what remains outside every verified denominator?

These are evaluation proposals. A retrieved catalogue record can answer source
selection and metadata questions; it must not invent statistical values or imply
that an executable provider or installed connector has been accepted.
