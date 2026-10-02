# Sites pilot: OS and ONS rights assessment

Assessed on 2 October 2026. This is a bounded technical admission assessment,
not a substitute for the organisation's interpretation of its agreements.
Entitlement and account details are held privately.

## Current decision and authority

The reviewed hosted profile contains OS Open Names place discovery, OS open
product metadata, ONS maintained CPIH and the fixed ONS MSOA 2021 names/codes table.
On 2 October the owner explicitly authorised bounded validation of PSGA data,
including OS National Geographic Database (NGD) Features, using the existing
organisational entitlement and credential. Only included access is authorised:
no paid plan, chargeable overage or automatic top-up. This supersedes the earlier
absence of authority for protected validation. It does not change licence terms.

Proceed with bounded local NGD validation. Treat hosted NGD admission as a separate
decision supported by the actual account, recipient arrangements, implementation
and observations. This assessment establishes a permitted contractual route for
contractor hosting; it does not establish that every service in the Sites and AI
processing chain already meets it. No protected payload or account evidence is
included in this document.

| Route | Source and conditions | Pilot decision |
| --- | --- | --- |
| OS Names API | [Product](https://www.ordnancesurvey.co.uk/products/os-names-api) and [find contract](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find). OpenData place, road and postcode discovery; requires a configured credential. | At most five candidates. Retain native identifiers, GB coverage, representative-point meaning and OS/Royal Mail/National Statistics acknowledgements. |
| OS Downloads product metadata | [Contract](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification). OpenData metadata is keyless. | Fixed three-product allowlist; no archive download or claim to have queried its contents. |
| ONS CPIH | [Maintained API migration](https://developer.ons.gov.uk/retirement/v0api/). L522/MM23 identity, release and index unit are checked. | Open Government Licence attribution; preserve source release and observation month. Arithmetic does not turn index levels into a separately published inflation measure. |
| ONS MSOA names/codes | [ONS geography licences](https://www.ons.gov.uk/methodology/geography/licences). Fixed December 2021 England-and-Wales names/codes table. | Retain GSS codes, vintage, attribution and explicit partial-page status. No boundary payload, point containment or property inference. |
| OS Places | [Product](https://www.ordnancesurvey.co.uk/products/os-places-api). Address data has separate addressing and end-user rights. | Disabled pending product/purpose/recipient admission. An open named place is not an equivalent address lookup. |
| OS NGD Features | [PSGA product summary](https://docs.os.uk/os-downloads/resources/product-resources/psga-product-summary) includes NGD Features. Collection-specific licensed access. | Bounded local validation authorised. Proposed first collections: Building v4 and Road Link v5. Hosted admission requires the evidence below; no arbitrary collection, bounding-box or CQL proxy. |

## Confirmed OS terms and their limits

**Included access.** OS lists NGD Features among the products available to PSGA
members on an unlimited basis. The [API Service Terms](https://osdatahub.os.uk/legal/apiTermsConditions)
state that Public Sector API Service use attracts no API fees. Public-sector use
follows the PSGA Member Licence, which takes precedence where those terms conflict.
This is different from the Premium API plan's royalty-free threshold. A successful
request alone does not identify which plan the credential uses. Do not switch to
a Premium plan or infer a spending ceiling from a small response.

**Purpose and machine processing.** The current [PSGA Member Licence, v3.0 May
2024](https://www.ordnancesurvey.co.uk/documents/licensing/psga-member-licence.pdf)
was checked directly. Appendix 1 permits internal business use and delivery of
the member's core public-sector activity, excluding commercial or competing
activity. Clause 2.7 permits contractors to process data for the member's licensed
use with the required restrictions and obligations; clause 2.7.4 governs digital
transfers between contractors. Automated API access is expressly contemplated by
the API terms. Bounded deterministic analysis is therefore a credible use within
an established licensed purpose; automation does not itself establish a new right.

**Contractor hosting.** The member licence, Appendix 1 paragraph 11.1.2(f), requires
compliance with [OS web-service/API guidance, v1.0 December
2022](https://www.ordnancesurvey.co.uk/documents/psga/psga-wfs-wms-guidance.pdf).
That guidance explicitly accommodates a contractor's network. For feature data
without a watermark it describes a server-side proxy with restricted access and
other access-control safeguards. A private authenticated MCP service can be
assessed against that model; cloud hosting is not categorically excluded. The
[contractor licence guidance](https://www.ordnancesurvey.co.uk/licensing/public-sector-contractor-licence)
provides a free standard form or permits an agreement containing the relevant
member-licence obligations. Owner-only visibility is an access control, not evidence
of the contractual chain.

**AI use.** The reviewed terms do not supply an unconditional permission for model
training, general vendor reuse or onward redistribution. Retrieval for a member's
specific task, model inference, training and publishing a reusable dataset are
different processing purposes. For this pilot, restrict protected processing to
the authorised task, with deterministic calculations and no training or vendor
reuse authorised by this assessment. Establish the actual processor, retention,
deletion and output arrangements before passing licensed results into an AI
service. No blanket AI prohibition is inferred from the absence of an AI clause.

## Account-specific evidence for hosted admission

The owner's entitlement statement is recorded authority. These remaining facts
must be established privately rather than inferred from public product pages:

1. The member, applicable project purpose and existing Public Sector API plan;
   NGD Features enabled for that project, without chargeable fallback.
2. Coverage of the actual Sites host, infrastructure providers and consuming AI
   service under the relevant contractor or other permitted-recipient terms.
3. The organisation's approved access, processing-location, storage, retention,
   deletion and model-processing arrangements for this account. The [Sites
   documentation](https://learn.chatgpt.com/docs/sites) gives no residency guarantee.
4. A reviewed route that protects upstream credentials, enforces a closed scope
   and durable allowance, and excludes licensed feature bodies from public logs,
   fixtures and evaluation reports.
5. Applicable [OS copyright acknowledgements](https://www.ordnancesurvey.co.uk/customers/public-sector/public-sector-licensing/copyright-acknowledgments),
   including the member's licence number for non-open data and any product-specific
   rights. Do not relabel a licensed or mixed result as Open Government Licence.

These are admission facts, not a request to repeat the owner's validation
authorisation. An unavailable collection or missing API permission should stop
that route and leave the open profile usable.

## Recommended bounded NGD validation

The separately recorded [executed observation](../implementation/SITES-218_NGD_VALIDATION.md)
used three initial requests (two features per selected collection), followed by
four keyless schema/queryable requests. The plan below is a prospective validation
profile, not a description of that completed run. Full schema conformance remains
open, including the observed Road Link source-schema inconsistency.

The current [NGD Features specification, v1.8.1](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features)
uses `https://api.os.uk/features/ngd/ofa/v1`. Pin the collection IDs
`bld-fts-building-4` and `trn-ntwk-roadlink-5`; do not silently substitute an
unversioned collection. First check each [collection](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection),
[schema](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/schema)
and [queryables](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables)
endpoints: `/collections/{collectionId}`, plus its `/schema` and `/queryables`
subpaths.
Validate returned identity, supported CRS, field types and nullability before
interpreting a feature response.

Suggested first wave: six metadata requests and two feature requests, sequentially,
with no retries or pagination. Use `GET /collections/{collectionId}/items`, a fixed
reviewed 200-metre square, `limit=5`, `offset=0`, and both `bbox-crs` and `crs` set to
`http://www.opengis.net/def/crs/EPSG/0/27700`. The default is CRS84 longitude/latitude,
so omitting either CRS is not equivalent. Set a 10-second deadline and 1 MiB streamed
body limit per request. Reject redirects, unexpected media/types and malformed
payloads; stop on 401/403/429 or entitlement uncertainty. Count attempts before
fetch, including failures. These are recommended pilot bounds, not OS tariffs.

| Question | Useful returned evidence | Interpretation boundary |
| --- | --- | --- |
| Which building footprints occur in this small test area, and what area, use or height does OS record? | [Building](https://docs.os.uk/osngd/data-structure/buildings/building-features/building) native identity/version, Polygon geometry, `geometry_area_m2`, and schema-validated use or height fields with their evidence dates and nulls. | Footprints are not households or addresses. A returned whole-feature area is not area clipped to the test square; missing height is not zero. |
| Which road links occur here, and what classifications or bus/cycle-lane attributes are available? | [Road Link](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link) native identity/version, network geometry and verified v5 attributes, including their units and dates. | A small link sample cannot establish a usable route, legal access, road safety or a complete network. |

Bounding-box selection means geometry **intersects** the box. Return a labelled
sample, not a count of all features in the area. Preserve source-native IDs,
collection/version, CRS, source timestamps, units, nulls and attribution; retain
the presence of a next-page link without following it. Record only sanitised
status, counts, timing, byte totals and hashes in publishable evidence. Use public
or synthetic fixtures for implementation tests. No LLM should calculate geometry,
distance or totals.

## Operational conditions

Keep credentials server-side and secret. OS authentication uses the documented
[`key` header](https://docs.os.uk/os-apis/core-concepts/authentication), never a
URL parameter, result, public artefact or browser variable. Do not forward it to
ONS or OS keyless metadata endpoints. All source payloads remain untrusted data.

The application initially admits at most 120 attempts per provider, with at most
20 attempts in its fixed one-minute window, counted before each fetch. There is
no refund after cancellation or failure. These are deliberately small pilot
bounds, not provider tariffs or a Sites billing guarantee. The published OS
[rate policy](https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy) and
ONS [request guidance](https://developer.ons.gov.uk/bots/) are separate source
limits. OS currently publishes 50 transactions per minute per API/project in
development mode and 600 in live mode, with HTTP 429 on excess. The proposed NGD
wave is a separate small allowance; the existing four-provider allowance does not
silently authorise a fifth provider. No chargeable operation or automatic top-up
is authorised.

Reassess rights before adding a dataset or client. A protected result must
never enter the public repository, public test fixtures or public evaluation
reports. The open-data fallback remains a useful independently testable profile.
