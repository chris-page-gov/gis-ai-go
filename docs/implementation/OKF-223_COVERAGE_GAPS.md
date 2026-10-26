# OKF-223: historical coverage baseline and completion criteria

Offline review of commit `63b5cafe6511c9f3ad0f373d031574a0e010f785` on
18 October 2026. This review made no network requests and accessed no credentials.
Source counts describe the retained 2 October captures; the 48 curated field
interpretations were reviewed on 18 October. They do not establish current service
availability or a complete inventory of the owner's accessible data.

Reconciliation note, 24 October: this is the original branch's baseline, not the
current repository capability report. The branch subsequently reached `a4e66e1a`;
main's separate recovery work is recorded in [OS recovery](OKF_OS_RECOVERY.md) and
[API coverage and usage](OS_API_COVERAGE_AND_USAGE.md). Those records supersede the
old environment and unimplemented-route observations where they supply later
evidence. They retain different source, output and validation denominators.

The recovery records 2,302 captured frozen documentation targets plus one retained
redirect, fresh schemas and queryables for 94 NGD collections, 44 advertised WFS
schemas, and 47 configured packages with 374 version references. It also records
bounded NGD samples and WFS feature controls. These observations do not prove
complete national retrieval. A [local Linked Identifiers
client](OS_LINKED_IDENTIFIER_METHOD.md) now exists; its method record does not
claim hosted MCP admission or successful live acceptance.

The retained catalogue identifies all 11 service families in the reviewed
[OS API catalogue](https://docs.os.uk/os-apis). Knowing their names and operations,
understanding every supplied field, and executing each service are separate goals.
The original implementation improved discovery while leaving each with explicit
gaps. Use the linked recovery records to determine which have since progressed.

## Service roles and the 18 October execution baseline

“Implemented” in this historical table means an authored request path existed in
the original profile. It does not describe all later recovery code or certify
live acceptance or deployment. The
[private Sites pilot](../../packages/provider-adapter-sdk/src/sites-pilot-providers.ts)
and the original `os_retrieve.py` at `a4e66e1a` had different credentials, limits
and admission states. The latter is superseded in the reconciled tree by
[ngd_extract.py](../../scripts/okf_plus/ngd_extract.py) and
[transient_profile.py](../../scripts/okf_plus/transient_profile.py); its old tests
and observations must not be reassigned to those implementations.

| API and official definition | Function | Original profile; later evidence where relevant |
| --- | --- | --- |
| [NGD Features](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features) | Retrieve structured NGD features and attributes, with versioned collections and filtering. | The original local `/items` executor had synthetic validation only. [Recovery](OKF_OS_RECOVERY.md#user-example-acceptance-boundaries) subsequently observed bounded live features and EPSG:7405 road geometry through its own methods; no hosted NGD admission follows. |
| [Features](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api) | WFS access to its documented product layers, including service-specific archive supply; distinct from NGD. | The original profile had estimates only. [Recovery](OKF_OS_RECOVERY.md#query-capabilities-and-route-comparisons) subsequently captured capabilities and 44 schemas and ran bounded GetFeature controls; generic operation/product coverage remains unproven. |
| [NGD Tiles](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles) | Present NGD through tiles and styles. Visualisation coverage is not the full feature/attribute catalogue. | Documentation existed without a tile executor in the original profile. Consult the current usage guide for the inspected MCP scope and remaining portrayal checks. |
| [Vector Tile](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api) | Retrieve styled vector mapping tiles. | No tile/style adapter existed in the original profile. Later route selection must also check lifecycle guidance; tile attributes are not equivalent to feature schemas. |
| [Maps](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api) | Retrieve raster map images through tiled map interfaces. | No raster-map executor existed in the original profile. Image pixels are not a substitute for source feature attributes. |
| [Names](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api) | Find named places and nearby names using the service's gazetteer. | The inspected experimental Sites `/find` adapter returned up to five candidates, without nearest search or broader extraction. Place points are not postal addresses or boundaries. |
| [Places](https://docs.os.uk/os-apis/accessing-os-apis/os-places-api) | Address search and lookup, including identifier and spatial searches. | No address-search executor existed in the original profile; the inspected pilot excluded address search. |
| [Linked Identifiers](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api) | Resolve documented relationships between identifiers and their associated feature types. | The original profile had no lookup executor. The later [typed local client](OS_LINKED_IDENTIFIER_METHOD.md) implements bounded lookups and product-version metadata; live success and hosted admission remain separate. LIDS product metadata is not a lookup. |
| [Downloads](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api) | Discover OpenData and existing account data packages, versions and downloadable files. | Original metadata capture and three pilot lookups did not transfer files. Later recovery inventoried packages, while [local archive processing](OS_LOCAL_GML_PROCESSING.md) accepts already acquired inputs. Neither establishes automatic bulk transfer or complete payload processing. The API cannot create or amend packages. |
| [OAuth 2](https://docs.os.uk/os-apis/accessing-os-apis/oauth-2-api) | Obtain OS access tokens for supported protected services. | No OS token-flow executor existed in the original profile. Authentication to the Sites application is a separate OAuth system. |
| [Net](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api) | Access OS Net station information and GNSS RINEX data. | No station/RINEX executor existed in the original profile. This specialist positioning data is not covered by NGD feature retrieval. |

The retained API projection contains 60 operation fragments across 152 pages,
including a withdrawn Match & Cleanse operation. It contains no extracted OAuth
operation. Those are extraction counts, not an authoritative operation denominator.
[Match & Cleanse was withdrawn](https://docs.os.uk/os-apis/accessing-os-apis/os-match-and-cleanse-api);
historical documentation must not make it eligible for current execution.

The [offline service registry](../../scripts/okf_plus/service_registry.py) turns
these retained services and operations into individually readable, source-bound
cards. Implementation flags must be read with their named profile and source
revision; the original flags were not an inventory of subsequent recovery code.
Experimental Sites adapters are outside the local private profile. Registry
generation does not execute routes or establish live access.

## Original metadata baseline and subsequent evidence

The [retained source review](OKF-220_OS_SOURCE_REVIEW.md),
[source snapshots](../../okf-plus/source/) and
[refresh admission rules retained on the reconciliation branch](https://github.com/chris-page-gov/gis-ai-go/blob/35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/metadata_refresh.py) support the
following original counts. Later closure is cited explicitly below; queue
completion remains measured only over its own admitted routes.

| Evidence family | Original retained or implemented coverage | Subsequent evidence and remaining qualification |
| --- | --- | --- |
| Public documentation | Indexes contained 152 API, 478 NGD and 1,673 Downloads URLs. Public projections retained API contracts and NGD structure; the separate Downloads guide projection contained two pages. | [Recovery's frozen traversal](OKF_OS_RECOVERY.md#completed-accessible-pass-and-retained-evidence) accounts for all 2,303 targets: 2,302 captured and one redirect, with a separate current-navigation supplement. This differs from the original four-index refresh queue and does not close all possible documentation. |
| NGD response schemas and queryables | 94 versioned collections, 188 schema roots and 2,915 field/queryable cards. | Recovery subsequently captured all 94 schemas and 94 queryables. These remain API-list denominators, not all download feature types; preserve [documented access exclusions](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features). |
| Field meaning and qualification | 48 curated field statements across six collections, with 92 companion links; 2,867 cards lacked this particular supplement. | Recovery retained native annotations and candidate explanation navigation for all 2,915 fields. The 48-fact supplement is no longer the only explanatory evidence; neither candidate navigation nor captured prose proves version-matched semantic equivalence. |
| Controlled vocabularies and API contracts | 15,298 code-value cards include both schema enums and documentation labels. Unresolved references remain explicit. | Preserve list/field/version scope; map meanings only where evidenced. Acquire admitted referenced schemas and test contract extraction for services whose specifications are prose, XML or other formats. |
| Live service metadata outside the original profile | Its refresh admitted NGD collection/schema/queryables and Downloads metadata, not every service's metadata routes. | Recovery captured WFS capabilities and 44 native schemas. Check remaining map/tile, NGD conformance, identifier and Net resource needs against current methods and receipts; the original profile's omission is not proof that later acquisition is absent. |
| Product search and GEMINI | 156 GEMINI records; 65 historical product-search entries comprise 60 HTTP entries plus five browser observations. Both HTTP catalogue refresh paths exist. | Reconcile fresh totals and IDs. Product-search HTTP pagination is incomplete when the embedded page omits entries; the five old browser observations cannot close a new capture. Product/service marketing entries are not distinct datasets. |
| Downloads and account packages | 26 OS-served OpenData products, including partner products. Authenticated package/version metadata was queued without capture in this lane. | Recovery subsequently inventoried 47 packages and 374 version references. Configured packages still do not enumerate every PSGA entitlement, establish complete archive processing or replace a product/edition denominator. |
| Specialist and linked material | Four documentation projects are admitted; two reviewed specialist pages are seeded explicitly. | Inventory other official projects, linked PDFs, images/diagrams, external schemas and downloadable specifications. The closed refresh does not follow these attachments automatically. Admit exact routes with provenance and parsing tests. |
| Lifecycle and history | Seven selected lifecycle guides and source-native version/temporal metadata are retained. | Build dated product/service status and available-history records. A schema version is not a historical dataset; a refresh schedule or metadata edit date is not a completed data release. |
| Retrieval integration | Private schema capture can emit bounded cards; the public execution catalogue remains pinned separately. | Review fresh schema changes before updating execution bindings; join product, API/download route, schema version and lifecycle evidence. Validate every supported executor and record unsupported routes explicitly. |

Neither this baseline nor the later scoped recovery substantiates a universal
denominator for “all OS metadata”. In particular, 32,596 cards are neither 32,596 datasets nor
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

## Reconciled priorities and acceptance

1. **Use dated access evidence.** Configuration revision 6 was the original
   task's blocker. Recovery later recorded successful access; neither observation
   proves every host or route works in a new task. Reuse existing owner authority
   and check only the prerequisites needed for the selected operation.
2. **Reconcile completed and outstanding metadata work.** Start with recovery's
   captured targets and private receipts before scheduling another acquisition.
   Keep its frozen traversal, later supplements and the original refresh queue
   separate. Preserve unresolved attachments, route limits and lifecycle gaps.
3. **Expand semantic coverage systematically.** Prioritise missing meanings for
   currently retrievable fields, then download-only products and specialist APIs.
   Add exact-version evidence links and questions that distinguish likely
   confusions; never treat an extracted label as a validated definition.
4. **Complete retrieval by service and delivery type.** Use current method records
   to distinguish implemented clients, actual calls and remaining operations.
   Compare verified bulk transfer with NGD for large selections; retain separate
   feature, identifier, search, map/tile and positioning evidence. Each needs an
   explicit contract, rights handling, limits, receipts, failure tests and live acceptance.
   Resolve archive, compression, full/change-only and schema-version differences
   before claiming an equivalent download is faster than an API query.
5. **Publish a coverage report with separate denominators.** Track current
   services/operations, products, versions, fields, code meanings, source passages,
   executable routes and tested questions. Report unknown measurements and
   unavailable evidence as valid outcomes. A finite test suite cannot prove every
   conceivable OS-related answer, even after every enumerated route is covered.
