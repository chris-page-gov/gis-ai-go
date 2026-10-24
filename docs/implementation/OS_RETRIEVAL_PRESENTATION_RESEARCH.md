# OS retrieval by presentation intent: research record

Date: 19 October 2026, Europe/London. Status: research and candidate metadata;
no renderer, Tableau connection, new provider route or publication is implemented.

A map and a table can need different retrieval plans. Choose the analytical
question, required fields and fidelity first; then compare routes that can meet
that contract. A fast contextual basemap is useful for navigation but cannot
replace complete feature attributes for a table, measurement or explanation.
The small [output-intent profile](../../okf-plus/profile/os-output-intents.json)
records recommended metadata rather than executable route grants.

## Evidence already available

The repository OS source review already records tile attribution limits at
[OKF-220_OS_SOURCE_REVIEW.md](OKF-220_OS_SOURCE_REVIEW.md). No existing VizQL study
was found in the inspected research and implementation Markdown.

| Official source | Evidence and implication |
| --- | --- |
| [OS API FAQs](https://docs.os.uk/os-apis/core-concepts/faqs.md) | Private captured body SHA256 `2c2870b8194b92967983669b6474ad6321a6eb516d77336025ede324ab6eedda`, lines 29–33: NGD Tiles includes selected feature types and attributes for a lightweight contextual basemap. Missing tile fields are not absent source data. Lines 43–45 describe a separate weekly basemap refresh/data cut. |
| [OS Maps technical specification](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification.md) | Private body SHA256 `7a0cc492885f66159b8af1dab5f1a3a887f95cc2fb7d558798f204734284a998`, lines 23–25: WMTS and ZXY raster tiles. A rendered pixel is not a returned native measurement. |
| [OS Vector Tile API](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api.md) | Private body SHA256 `9dbfab9d4db4c04559e1ba815b02450fd06ad6f58a9f946c9a6a03e16717c7ab`, lines 23–27: interactive vector basemap and styles; line 9 anticipates retirement in autumn 2028. Product lifecycle must qualify a route recommendation. |
| [Styling OS NGD data](https://docs.os.uk/os-apis/core-concepts/styling-os-ngd-data.md) | Private body SHA256 `4bf759ff16e49eb0847ed1cb5f5d09dbef2787f547d3a64520dc81daac08080e`, lines 9–13: contextual/cartographic and analytical styles; lines 24–26: hosted resources/custom styles. A style category does not establish measurement suitability. |

The public output-intent profile separately binds the earlier committed factual
source snapshot and its capture hashes. Those historical public hashes differ
from this fresh private capture; neither represents a live endpoint guarantee.
Provider text is evidence and cannot instruct the agent to follow embedded links
or execute documentation commands.

## VizQL and VizQL Data Service

Working background for follow-up: Tableau VizQL is Tableau's visual query
technology, connecting visual specifications to queries and visual output.
Tableau VizQL Data Service is a separate programmatic data-query facility over
published Tableau data sources. It should not be assumed to supply a rendered
chart, query arbitrary OS APIs, or expose an OS endpoint called VizQL. A Tableau
integration would introduce its own deployed datasource, authentication,
permissions, semantic model and possible licensing constraints.

The initial official Tableau-hosted documentation requests could not be inspected.
Three bounded unauthenticated requests to official Tableau locations were
rejected by the network tunnel with HTTP 403 before content retrieval:

- `https://www.tableau.com/why-tableau/what-is-tableau/vizql`
- `https://help.tableau.com/current/api/vizql-data-service/en-us/docs/vds_get_started.html`
- `https://help.tableau.com/current/api/vizql-data-service/en-us/docs/vds_overview.html`

These remain unverified Tableau-hosted URL leads. The follow-up vendor GitHub
review below supplies a published API contract; it does not verify those URLs or
any deployed service. No Tableau credential, account, paid service or connector
was used.

### Vendor GitHub follow-up: inspected contract

Eight bounded public GitHub read calls identified the Tableau-owned
[tableau/VizQL-Data-Service](https://github.com/tableau/VizQL-Data-Service) repository.
The inspected commit is
[`f0ec79951be3d0c59dbc2e9503fdcc453530c8d9`](https://github.com/tableau/VizQL-Data-Service/commit/f0ec79951be3d0c59dbc2e9503fdcc453530c8d9).
The commit's tree was checked against the inspected blob identities. Files were
read as evidence; no SDK, sample, repository instruction or remote code ran. Decoded
blob bytes and a retrieval/verification record are retained privately under
`artifacts/okf-plus/private-vizql-research/20261019/`, including the licence.
The record distinguishes decoded blob evidence from an unretained HTTP envelope.

| Pinned file | Git blob SHA1 | Body SHA256 |
| --- | --- | --- |
| [README.md](https://github.com/tableau/VizQL-Data-Service/blob/f0ec79951be3d0c59dbc2e9503fdcc453530c8d9/README.md) | `da7f1a25da497ffdd02c9085d7fccc3d633a80f2` | `b914c078a3ef3d75c10ae5f89b7a96eb800794c21780947e8e89444fb5b374ac` |
| [VizQLDataServiceOpenAPISchema.json](https://github.com/tableau/VizQL-Data-Service/blob/f0ec79951be3d0c59dbc2e9503fdcc453530c8d9/VizQLDataServiceOpenAPISchema.json) | `1b4e2c12a30b678f4a97c259785cf143aa0c94c5` | `12d5d7f2f54c2eed7b66b0f0d049ff750c3b46c0e650893c779516a249016247` |
| [LICENSE.txt](https://github.com/tableau/VizQL-Data-Service/blob/f0ec79951be3d0c59dbc2e9503fdcc453530c8d9/LICENSE.txt) | `63cbbd63f3d03c5187c9ee1258333d423596d8e3` | `a0f6ca149df543190889494675b6da6794bfdd13c23782297eb5797842c00faa` |
| [python_sdk/src/api/client.py](https://github.com/tableau/VizQL-Data-Service/blob/f0ec79951be3d0c59dbc2e9503fdcc453530c8d9/python_sdk/src/api/client.py) | `59262e215d5767a1c353c7024b03d2f284c6c569` | `447ba9dc5a84ef03c51f33ad9830adc1663145f150302a4e4aac4b0726890641` |

The README explicitly identifies the vendor-published schema and SDK. The licence
is Apache 2.0, copyright Salesforce; this record paraphrases source facts without
copying implementation code. Repository licensing does not supply a Tableau
service licence, OS data entitlement or recipient permission.

The schema `/info` describes an API for Tableau published data sources, version
`20263.0`; `/servers/0/url` is `/api/v1/vizql-data-service`. Relevant JSON pointers:

| Method and relative path | Request/response contract |
| --- | --- |
| `POST /read-metadata` | `ReadMetadataRequest` requires `datasource`; optional `options`. Response `MetadataOutput` has `data` field metadata and optional `extraData` for parameters/calendar properties. |
| `POST /query-datasource` | `QueryRequest` requires `datasource` and `query`; optional `options`. `Query` requires `fields`; optional `filters` and `parameters`. JSON response `QueryOutput` advertises `data` array and `error` object; the operation also advertises `text/event-stream` with `SseResultStream`. |
| `POST /get-datasource-model` | Returns `DatasourceModelOutput`: logical tables and their relationships. This is model metadata, not an OS identity crosswalk. |
| `POST /list-supported-functions` | Requires `ListSupportedFunctionRequest`; response is an array of supported functions. |
| `POST /user-has-query-permissions` | Checks the calling user's datasource query permissions; response `QueryPermissionsOutput`. |
| `GET /simple-request` | Advertises a string JSON response and an empty operation security array. This exception is not anonymous datasource query access. |

Operation pointers are `/paths/~1read-metadata/post`,
`/paths/~1query-datasource/post` and corresponding escaped paths; definitions are
under `/components/schemas/<name>`. `/components/securitySchemes/XTableauAuth`
defines the `X-Tableau-Auth` header, inherited through top-level `/security` except
where overridden. Reading this contract did not authenticate to Tableau.

`Datasource` advertises `datasourceLuid`, `workbookDatasourceId` and connections;
the LUID description includes published or workbook data sources. Do not reduce
the inspected version to only one source mode. `FieldMetadata` distinguishes
logical `fieldName`, presentation `fieldCaption`, datatype, role/type, default
aggregation, formulas, logical-table identity, formatting, hidden state and other
metadata. Options can request remote database names. These are useful modelling
lessons: retain logical/native identity separately from labels and aggregation.
They do not establish geographic CRS, vertical datum or OS field equivalence.

No image, map-tile or chart-rendering operation is advertised by this schema.
The defensible conclusion is a documented data/model query service with structured
fields and filters, not a demonstrated renderer. The contract is stronger evidence
than the earlier background description, but actual deployed versions, permissions,
licensing, source connections and geospatial behaviour remain unverified. No
VizQL service endpoint was called.

The useful architectural question is whether a declarative output intent can
help the existing planner select a source route and deterministic transformations.
That idea can be evaluated locally without adopting Tableau or generating SQL
from unaudited prose. Any future Tableau-specific route needs an independently
reviewed contract and authority; this record adds neither.

## Underlying data understanding required

For every proposed visualisation, retain small linked metadata for:

- Question and purpose; entity/feature grain; native field and collection version;
  identities, relationship direction/cardinality and evidenced mappings.
- Unit, measure definition, null/unknown conventions, allowed categories, source
  derivation, precision, confidence and fitness limitations.
- Reference/validity time, evidence/capture date, publication/data cut, source
  refresh and schema/product version. A tile cache can lag a feature route.
- Geometry type, dimensionality, horizontal CRS/axis order, vertical CRS/datum,
  heighting method and transformation provenance. Displaying 3D does not establish
  surveyed elevation, building clearance or measurement accuracy.
- Coverage, selection and denominator; aggregation function, grouping, weighting,
  missingness handling and suppression. Sampling must remain visible.
- Portrayal: geometry/mark/channel, colour scale, classification breaks, legend,
  styles/sprites/fonts, zoom/scale range, tile matrix and rendering CRS. Record
  generalisation/simplification/clipping/quantisation if established; otherwise
  preserve them as unresolved fidelity questions, not asserted OS algorithms.
- Accessibility and inspectability: text/table alternative, units and time in
  labels, keyboard access, distinguishable missing values and cited source.
- Acquisition and processing estimates, output size, cancellation/resume,
  permitted audience and transient-data disposal evidence.

Example recommendations are conditional. Pavement widths can support an exact
native-field table and, with appropriate geometry/context, a graduated line map;
Pavement Link geometry is not a measured pavement outline. Building heights may
support a labelled table or height-coloured/extruded map only after absolute versus
relative meaning and datum are established. Road ODN heights may support a route
profile only with ordered geometry and vertical-reference evidence; elevation
gain fields alone cannot provide that profile. A histogram or summary table needs
an explicit population and denominator, not merely whichever features fit a page.

For tables, test raw-feature routes and documented WFS field projection against
required exact attributes; NGD documents CQL-text row filtering, not field
projection. For contextual maps, evaluate suitable raster/vector tiles; for an
analytical map, combine a contextual basemap with a separately evidenced feature
selection where necessary. For large aggregate analysis, compare download plus
transient deterministic processing with API paging. These are candidate route
families, not claims of identical source coverage or fields.

## Research backlog and acceptance

1. Vendor GitHub contract inspection is complete for the pinned version above.
   Review deployment/licensing and the architectural value before proposing any
   Tableau route. Acceptance: explicit decision whether it adds value without a
   new paid dependency; no OS API equivalence or renderer inferred from the schema.
2. Extend the initial evidence-constrained planner output-intent contract: map, table, chart, profile and machine export;
   requested fields, population, transformations, fidelity and rights. Acceptance:
   planner fixtures show different route candidates for the same question's map
   and exact-table outputs without inferring field equivalence.
3. Review tile schemas, styles, zoom/scale behaviour, data cut and attribution.
   Acceptance: field availability and geometry fidelity are evidenced per product;
   omitted attributes cannot satisfy table/measurement requirements.
4. Define deterministic visualisation recipes and quality checks. Acceptance:
   sample-only tests distinguish absolute/relative height, unknown datum, missing
   widths, biased pages and double-counted joins; show a table alternative.
5. Validate a bounded prototype only after contracts and owner scope permit it.
   Acceptance: source-bound results, acquisition/processing estimates, accessible
   output and verified transient payload disposal. No renderer is built here.

