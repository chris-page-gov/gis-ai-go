# OKF-223: OS coverage gaps and completion criteria

Offline review of commit `63b5cafe6511c9f3ad0f373d031574a0e010f785` on
18 October 2026. This review made no network requests and accessed no credentials.
Source counts describe the retained 2 October captures; the 48 curated field
interpretations were reviewed on 18 October. They do not establish current service
availability or a complete inventory of the owner's accessible data.

The retained catalogue identifies all 11 service families in the reviewed
[OS API catalogue](https://docs.os.uk/os-apis). Knowing their names and operations,
understanding every supplied field, and executing each service are separate goals.
The current implementation substantially improves discovery but leaves all three
with explicit gaps.

## Service roles and executable coverage

“Implemented” below means an authored request path exists in this checkout. It
does not certify live acceptance or that these exact bytes are deployed. The
[private Sites pilot](../../packages/provider-adapter-sdk/src/sites-pilot-providers.ts)
and the [local NGD executor](../../scripts/okf_plus/os_retrieve.py) have different
credentials, limits and admission states.

| API and official definition | Function | Implemented path and remaining work |
| --- | --- | --- |
| [NGD Features](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features) | Retrieve structured NGD features and attributes, with versioned collections and filtering. | Local private `/items` executor, pagination and resume exist. Validate live collection/schema/CRS behaviour; no hosted NGD tool is admitted. |
| [Features](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api) | WFS access to its documented product layers, including service-specific archive supply; distinct from NGD. | Offline estimates exist. WFS capabilities/XSD acquisition, feature execution and response parsing remain absent. |
| [NGD Tiles](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles) | Present NGD through tiles and styles. Visualisation coverage is not the full feature/attribute catalogue. | Documentation is retained; service-resource discovery and tile execution remain absent. |
| [Vector Tile](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api) | Retrieve styled vector mapping tiles. | No tile/style retrieval adapter. Tile attributes must not be assumed equivalent to feature-service schemas. |
| [Maps](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api) | Retrieve raster map images through tiled map interfaces. | No raster-map executor. Image pixels are not a substitute for source feature attributes. |
| [Names](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api) | Find named places and nearby names using the service's gazetteer. | Experimental Sites `/find` adapter returns up to five candidates. Nearest search and broader extraction are not implemented. Place points are not postal addresses or boundaries. |
| [Places](https://docs.os.uk/os-apis/accessing-os-apis/os-places-api) | Address search and lookup, including identifier and spatial searches. | No address-search executor; the existing pilot excludes address search. |
| [Linked Identifiers](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api) | Resolve documented relationships between identifiers and their associated feature types. | No identifier-lookup executor. Reading the LIDS download-product metadata does not implement this API. |
| [Downloads](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api) | Discover OpenData and existing account data packages, versions and downloadable files. | Local metadata capture and three pilot product-metadata lookups exist. File transfer, verification, unpacking and ingestion remain absent. The API cannot create or amend packages. |
| [OAuth 2](https://docs.os.uk/os-apis/accessing-os-apis/oauth-2-api) | Obtain OS access tokens for supported protected services. | No OS token-flow executor. Authentication to the Sites application is a separate OAuth system. |
| [Net](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api) | Access OS Net station information and GNSS RINEX data. | No station/RINEX executor. This specialist positioning data is not covered by NGD feature retrieval. |

The retained API projection contains 60 operation fragments across 152 pages,
including a withdrawn Match & Cleanse operation. It contains no extracted OAuth
operation. Those are extraction counts, not an authoritative operation denominator.
[Match & Cleanse was withdrawn](https://docs.os.uk/os-apis/accessing-os-apis/os-match-and-cleanse-api);
historical documentation must not make it eligible for current execution.

The [offline service registry](../../scripts/okf_plus/service_registry.py) turns
these retained services and operations into individually readable, source-bound
cards. Its implementation flags describe the local private retrieval profile,
with experimental Sites adapters explicitly outside that profile. Registry
generation does not execute routes or establish live access.

## Metadata and semantic completeness matrix

The [retained source review](OKF-220_OS_SOURCE_REVIEW.md),
[source snapshots](../../okf-plus/source/) and
[refresh admission rules](../../scripts/okf_plus/metadata_refresh.py) support the
following gaps. Queue completion is measured only over admitted routes.

| Evidence family | Retained or implemented coverage | Remaining gap and concrete next action |
| --- | --- | --- |
| Public documentation | Indexes contain 152 API, 478 NGD and 1,673 Downloads URLs. API contracts and NGD structural projections exist; the separate Downloads guide projection contains only two pages. | Run the four-index refresh, including More Than Maps, and account for every discovered URL, failure and revision. Page capture must be distinguished from usable field definitions. |
| NGD response schemas and queryables | 94 versioned collections, 188 schema roots and 2,915 field/queryable cards. | Refresh and compare exact schema identities. This API list is not the download feature-type catalogue: documented exclusions include Boundaries, Functional Areas and GB Address. Reconcile with the [NGD access catalogue](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features). |
| Field meaning and qualification | 48 curated field statements across six collections, with 92 companion links. The other 2,867 field/queryable cards have no curated supplement. | Capture supporting passages privately; bind definitions, units, dates, quality, null semantics, code meanings and relationships to exact versions. A schema label or successful text capture does not establish interpretation. |
| Controlled vocabularies and API contracts | 15,298 code-value cards include both schema enums and documentation labels. Unresolved references remain explicit. | Preserve list/field/version scope; map meanings only where evidenced. Acquire admitted referenced schemas and test contract extraction for services whose specifications are prose, XML or other formats. |
| Live service metadata outside the current profile | Documentation describes capabilities, layers, styles and identifier types. Refresh currently admits NGD collection/schema/queryables and Downloads metadata, not every service's metadata routes. | Add separately reviewed acquisition for WFS capabilities/XSD, map/tile capabilities and styles, NGD conformance/API descriptions, Linked Identifiers type/product-version inventories, and Net station/file inventories. Keep metadata discovery distinct from payload retrieval. |
| Product search and GEMINI | 156 GEMINI records; 65 historical product-search entries comprise 60 HTTP entries plus five browser observations. Both HTTP catalogue refresh paths exist. | Reconcile fresh totals and IDs. Product-search HTTP pagination is incomplete when the embedded page omits entries; the five old browser observations cannot close a new capture. Product/service marketing entries are not distinct datasets. |
| Downloads and account packages | 26 OS-served OpenData products, including partner products. Authenticated package/version metadata is queued but not newly captured. | Enumerate current configured packages, files, versions and full/change-only supply; map them to product/schema coverage. Configured packages do not enumerate every PSGA entitlement. Existing owner authority does not supply missing project observations. |
| Specialist and linked material | Four documentation projects are admitted; two reviewed specialist pages are seeded explicitly. | Inventory other official projects, linked PDFs, images/diagrams, external schemas and downloadable specifications. The closed refresh does not follow these attachments automatically. Admit exact routes with provenance and parsing tests. |
| Lifecycle and history | Seven selected lifecycle guides and source-native version/temporal metadata are retained. | Build dated product/service status and available-history records. A schema version is not a historical dataset; a refresh schedule or metadata edit date is not a completed data release. |
| Retrieval integration | Private schema capture can emit bounded cards; the public execution catalogue remains pinned separately. | Review fresh schema changes before updating execution bindings; join product, API/download route, schema version and lifecycle evidence. Validate every supported executor and record unsupported routes explicitly. |

The source evidence currently cannot substantiate a universal denominator for
“all OS metadata”. In particular, 32,596 cards are neither 32,596 datasets nor
32,596 independently validated meanings. Likewise, the 2,554 initial refresh
routes are a starting queue, not a completeness proof.

## Questions the cited sources cannot answer directly

These are limits of the specified product or measurement, not assertions that no
possible OS product could contain related evidence. Return an explicit unknown
or a clearly labelled derivation rather than silently substituting a different
quantity.

| Requested answer | Source limitation and correct handling |
| --- | --- |
| Exact unobstructed pavement width at an arbitrary point now | [Pavement attribution](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-attribution) is algorithmic and summarised. Road Link values aggregate both sides; Pavement Link adds side/subsection context. These values do not directly establish present obstructions or a pinpoint clear-passage measurement. |
| Every building's height with a numeric error bound | [NGD height confidence](https://docs.os.uk/osngd/code-lists/code-lists-overview/builtstructureheightconfidencevalue) is categorical; heights can be absent. Decimal precision is not an accuracy guarantee. Preserve nulls and the exact absolute/relative height definition. |
| Road-deck height from a terrain sample | [OS Terrain modelling](https://docs.os.uk/os-downloads/products/land-and-terrain-portfolio/os-terrain-5/os-terrain-5-overview/source-data) removes supported bridges. Use suitable 3D road geometry and heighting-method evidence; interpolation between vertices is a derived result, not another source observation. |
| Current sea level from an ODN elevation | [ODN](https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems/ordnance-datum-newlyn) is a fixed reference based on historical mean sea level. It does not supply current tide or present-day sea level. |
| Any feature at any historical instant | [Temporal ordering](https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering) and [Features archives](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/os-product-archive) have product-specific start dates and snapshots. Maintained older schemas can still return current data. |

## Work order and acceptance

1. **Restore technical access and observe it.** The root task reports that runtime
   configuration revision 6 lacks the four metadata hosts and the OS credential.
   This review did not re-test that configuration. Validate the documented hosts
   and existing credential through the supported environment workflow; do not
   infer access from licence authority or a declaration alone.
2. **Close known metadata queues and preserve gaps.** Capture private originals,
   reconcile per-family totals, index small evidence records and retain failed or
   unsupported routes. Add service metadata and attachment handlers using public
   or synthetic fixtures before live calls. This fixture work can proceed offline.
3. **Expand semantic coverage systematically.** Prioritise missing meanings for
   currently retrievable fields, then download-only products and specialist APIs.
   Add exact-version evidence links and questions that distinguish likely
   confusions; never treat an extracted label as a validated definition.
4. **Complete retrieval by service and delivery type.** Prioritise verified bulk
   file retrieval alongside NGD for large requests, then the missing feature,
   search, identifier, map/tile and positioning operations. Each needs an explicit
   contract, rights handling, limits, receipts, failure tests and live acceptance.
   Resolve archive, compression, full/change-only and schema-version differences
   before claiming an equivalent download is faster than an API query.
5. **Publish a coverage report with separate denominators.** Track current
   services/operations, products, versions, fields, code meanings, source passages,
   executable routes and tested questions. Report unknown measurements and
   unavailable evidence as valid outcomes. A finite test suite cannot prove every
   conceivable OS-related answer, even after every enumerated route is covered.
