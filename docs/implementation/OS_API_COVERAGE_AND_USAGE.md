# OS API coverage and usage

Reviewed: 20 October 2026. Repository baseline: `a6ef5660`.
Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
This is a documentation and planning record; it adds no provider call, MCP tool
or runtime admission.

A service can be documented and included in a product catalogue without having
been called by an MCP tool. Usage figures therefore need their own scope and
evidence. A zero or missing counter does not establish absent data, absent
entitlement or complete coverage.

## Product and service coverage basis

Use the official [PSGA Product Summary Table][psga-table], reviewed on
20 October 2026, as the public product and service coverage basis. This is the
review date, not an asserted publication or edition date. Preserve the source
date and version where supplied, its included products, exclusions and lifecycle
notes. Keep organisation, account and project entitlement decisions in the
private operating record; this guide makes no account-specific claim.

The table groups OS NGD, APIs and download products. Expand an aggregate such as
OS NGD into the relevant collections and versions for a particular question.
A configured package, delivery recipe or API collection is not another product
by default. A package list cannot replace the product denominator, and a missing
package does not establish missing entitlement.

For each required product, record the required edition/version, format, area of
interest and fields alongside its delivery routes. Preserve separate states:

| Evidence state | What it establishes |
| --- | --- |
| Documentation captured | Source material is retained with provenance. It does not invoke the described API. |
| Executable route admitted | A reviewed implementation permits a particular operation and input contract. It does not prove a request occurred. |
| Request observed | A receipt records an actual attempt and its result for that route. A response can still be partial or fail validation. |
| Selected processing complete | Every input in the defined selection passed its processing and retention checks. This closes that selection, not the national catalogue. |
| Account usage reported | A provider or application reports a metric for its own service, project, period and counting rules. It is not a substitute for request or processing receipts. |

The existing [availability model](OS_DATA_AVAILABILITY.md) similarly separates
access, expected presence, observed presence and retrieval completion.

## Four services and the inspected MCP scope

The [connection inventory](EXPERIENCE-221_CONNECTIONS.md) distinguishes local
cached-data MCP, the private Sites pilot and broader OKF+ metadata. The inspected
Sites adapter admits OS Names and a small keyless OpenData product-metadata
operation. Its broader documentation corpus does not add callable tools.

| Service | Documented purpose and inspected implementation | What remains to establish |
| --- | --- | --- |
| [OS Linked Identifiers API][linked-identifiers] | The API returns identifier relationships, not the linked features' geometry or attributes. Its lookup contracts are captured, but no admitted Linked Identifiers executor was found in the inspected GIS AI GO MCP profiles. Reading Linked Data cards or `LIDS` product metadata does not call this API. | For a required crosswalk, review the exact lookup and product-version contract, relationship direction/cardinality and response scope; then test a bounded selection and retain its receipt. Do not infer identity equivalence from a shared label. |
| [OS NGD API – Tiles][ngd-tiles] | Documentation describes a vector basemap with selected feature types and attributes. No admitted tile executor was found in the inspected MCP profiles. Native feature/schema work does not itself request tiles. | For a map requirement, verify the selected collection, tile matrix, zoom, style, attribution and data cut, then test bounded tile retrieval and portrayal. Missing tile attributes do not establish missing native data. |
| [OS Vector Tile API][vector-tiles] | Documentation describes a customisable vector basemap. No admitted executor was found in the inspected MCP profiles. The source review records a planned retirement, which must qualify future route selection. | Check current lifecycle guidance and the required layer/style/CRS/zoom contract before a bounded portrayal test. A rendered map does not prove complete native attribute or geometry fidelity. |
| [OS Downloads API][downloads] | `sites_os_open_product` reads keyless metadata for `OpenNames`, `OpenUPRN` or `LIDS`; it does not download a dataset. Separate local recovery methods inventory authenticated package/version metadata. Generic archive processing accepts already acquired inputs and makes no provider call. | Reconcile metadata requests, download initiation and payload transfers separately. Verify the exact version, format, geographical scope, checksums and complete selected processing; keep private acquisition evidence separate from MCP capability claims. |

The bounded Linked Identifiers, NGD Tiles and Vector Tile API checks above do
not require creation of a download package.

Implementation anchors are the [Sites tool definitions][sites-tools], the
[product metadata adapter][sites-adapter] and the
[private metadata inventory boundary][inventory]. The captured
[API contracts][api-contracts] explicitly distinguish documentation from admission.
The [Downloads capability profile][download-profile] is planning evidence, not an
execution or entitlement grant.

## Downloads and usage accounting

There are separate operations to account for:

1. **OpenData metadata:** the current MCP product lookup sends no OS key. Its
   result lists product/version/format metadata; returning a download reference
   does not fetch that reference.
2. **Authenticated packages:** package discovery and version selection use the
   authenticated Downloads routes. [Download initiation][download-initiation]
   documents a redirect response. Record the API attempt and redirect separately.
3. **Payload delivery:** a permitted redirect can lead to a separate blob
   transfer. Validate the destination and transfer bounds, retain byte/checksum
   evidence and never forward the OS key to the delivery host. A successful
   redirect is not a completed or verified archive transfer.

The pilot's [application allowance][allowance] counts attempts before network
work and does not refund a failed request. It is distinct from OS transaction
reporting and billing. The [existing usage guidance][usage-guidance] already
requires these measures to be recorded separately.

For a zero or missing usage figure, identify the reporting surface, service
category, project scope, time window, observation time and metric definition.
Keep those account-specific observations private. An absent row is not an
observed zero; a reported zero alone does not prove that no requests occurred.
Compare the appropriate route receipts with the provider's documented counting
rules before assigning a cause. This record does not establish how keyless
metadata, authenticated Downloads requests or blob transfers appear in a provider
dashboard, and it makes no billing inference from their absence.

Documentation-page requests, local metadata searches, cached responses and
provider API requests also have different destinations and purposes. Report
which occurred rather than combining them into an unspecified MCP usage total.
The [OS rate policy][rate-policy] remains a separate execution constraint; an
application counter or a low reported total does not prove remaining allowance.

## Bounded closure and next actions

For each required service or product:

1. Bind the public catalogue source and the private entitlement decision to the
   requested edition/version, format, area and purpose. Preserve unknowns without
   reclassifying them as absent data.
2. Check whether an existing API route or package meets that requirement. Record
   documented capability, implemented admission and observed behaviour separately.
3. Where execution is needed and already authorised, define a bounded test with
   request/byte/time ceilings, rate limits, credential destinations and stop
   conditions. Use synthetic fixtures for public implementation tests.
4. Verify the complete selected input and retained knowledge before disposal.
   For COU, establish the product-specific baseline and change-order dependencies;
   a FULL label alone does not prove current or complete coverage.
5. Close only the evidenced selection and record any remaining product, semantic,
   portrayal or accounting gaps.

Prepare a package-creation requirement report only when this comparison proves
that the required edition, format or area is unavailable through the existing
suitable routes/packages. The report must specify the product ID, edition, format,
minimal area of interest, purpose, evidenced gap, checked alternatives, estimated
bytes and processing, and confirmed cost. Keep an unavailable estimate or cost
explicitly unknown until established. Do not request a package automatically for
every catalogue ID or treat that report as permission to create an order.

For tables, measurements and analysis, require the native fields, units, null
semantics, geometry/CRS and complete selection or explicit sample scope. Tiles
are useful for context and portrayal, but their attributes cannot be assumed to
replace native values. The [presentation research][presentation] and
[planner tests][planner-tests] already enforce this distinction. Select services
to answer the question; generating traffic merely to populate usage counters is
not a coverage test.

[psga-table]: https://docs.os.uk/os-downloads/resources/product-resources/psga-product-summary-table
[linked-identifiers]: https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api
[ngd-tiles]: https://docs.os.uk/osngd/accessing-os-ngd/access-the-os-ngd-api/os-ngd-api-tiles
[vector-tiles]: https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api
[downloads]: https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification
[download-initiation]: https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package
[rate-policy]: https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy
[sites-tools]: ../../apps/mcp-gateway/src/sites-pilot-http.ts
[sites-adapter]: ../../packages/provider-adapter-sdk/src/sites-pilot-providers.ts
[inventory]: ../../scripts/okf_plus/os_private_inventory.py
[api-contracts]: ../../okf-plus/source/os-api-contracts.json
[download-profile]: ../../okf-plus/profile/os-download-query-capabilities.json
[allowance]: ../../apps/mcp-gateway/src/sites-pilot-store.ts
[usage-guidance]: ../operations/SITES_MCP_CAPABILITY_MATRIX.md
[presentation]: OS_RETRIEVAL_PRESENTATION_RESEARCH.md
[planner-tests]: ../../tests/contract/test_okf_plus_query_planner.py
