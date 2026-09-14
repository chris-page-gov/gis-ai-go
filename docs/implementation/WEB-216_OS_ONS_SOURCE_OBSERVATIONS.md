# WEB-216: OS and ONS source observations

Status: bounded public-source evidence; no completed spatial join.  
Observation date: 14 September 2026.

This record supports the [WEB-216 public-data workbench](WEB-216_PUBLIC_DATA_WORKBENCH.md).
Its [machine-readable projection](../chronicle/data/web216-os-ons-source-observations-20260914.json)
contains the exact public-safe identifiers, timestamps, byte counts and digests.
It does not contain the OS archive, raw selected members, a temporary signed URL,
personal data or a private machine path.

## Outcome

The experiment established a source-bound OS Open Names representative point for
the populated place `Warwick` and verified the metadata contract for a candidate
ONS MSOA 2021 boundary layer. It did **not** establish which MSOA contains that
point. Both bounded ONS point-query attempts timed out without a captured HTTP
status or response body. Their result is therefore **unavailable**, not “no match”.

The point and layer both declare British National Grid (`EPSG:27700`), but matching
CRS labels do not establish containment. A later successful query must return one
unambiguous feature and its native `MSOA21CD`; no name, nearby feature or OS context
URI may be substituted.

## Source-by-source findings

| Source | What was observed | Evidence boundary |
| --- | --- | --- |
| [OS Open Names product metadata](https://api.os.uk/downloads/v1/products/OpenNames) | Product ID `OpenNames`, version `2026-07`, GB coverage and CSV, GML 3 and GeoPackage formats. The Downloads API offered GB-wide archives only; there was no SP-area download. | Two metadata GETs returned HTTP 200. No credential, premium product, redirect or payload was used in this capture. Metadata alone did not prove archive contents or payload terms. |
| OS Open Names GB CSV archive | The 103,259,564-byte archive matched the API-supplied MD5. Its recorded SHA-256 is `6175912f1a3be7fffe556b4621a8d0686f1ea145e20ca61ce2b115a75a9bd69f`. | The SHA-256 was recorded during the source-time capture and was not recalculated for this document. The API MD5 and HTTP `Content-MD5` detect transfer inconsistency but are not independent publisher authentication. The archive remains outside the repository. |
| Selected Open Names members | Safety inspection found 824 members, including 819 data CSVs. Only the licence, README, separate header and `Data/SP26.csv` were decompressed within the declared member bound. | Central-directory and selected-member checks did not decompress or validate all 1.81 GB of declared uncompressed content. No raw member is published here. |
| OS Open Names Warwick point | Native ID `osgb4000000074555874`, URI `http://data.ordnancesurvey.co.uk/id/4000000074555874`, type `populatedPlace`, local type `Town`, point `(428119, 265114)` in `EPSG:27700`. | The SP26 member contained two exact name matches: the town and Warwick railway station. The field predicates selected the town. This is a representative named-place point, not a unique-name claim. |
| [ONS MSOA December 2021 BFC V7](https://www.data.gov.uk/dataset/b9d6e8eb-95a8-4a32-832f-e8a746252f43/middle-layer-super-output-areas-december-2021-boundaries-ew-bfc-v7) | Feature service item `12baf1e6a44441208ffe5ba5ed063a68`, layer 0 `MSOA_2021_EW_BFC_V7`, polygon geometry, `EPSG:27700`, object ID `FID`, display/GSS-code field `MSOA21CD` and England-and-Wales scope. | Service and layer metadata returned HTTP 200. The captured description and copyright fields were empty, so those responses do not establish rights. Preserve the December 2021 vintage and BFC V7 boundary variant. |
| ONS full-geometry point query | A maximum-five, point-intersects request was attempted after metadata discovery. | It timed out. The exact query start time, HTTP status, body, candidate count and feature IDs are unknown. No response must be inferred. |
| ONS two-stage point query | An attributes-first point-intersects request began at `2026-09-14T17:01:30.018616Z` and failed at `2026-09-14T17:01:50.095162Z`. | It timed out without a status or body. Because no unambiguous `FID` was returned, the conditional full-geometry request was not made. |

## Exact response evidence

The first OS metadata response was 1,056 bytes with SHA-256
`0686ddc14e500d9077b23d68c061739dd012accd4ad364c3ef1d4de3a4f1d03f`;
the second was 687 bytes with SHA-256
`066d2264b9c9caa2f4da09d0dda40133e83cb0d40fe1eadd671d3d47150b73ac`.
The source `Date` values were `2026-09-14T16:07:25Z` and
`2026-09-14T16:07:52Z` respectively.

The ONS service metadata response was 3,642 bytes with SHA-256
`bba8ac07aaf5ca46890ba9a6b35b9d739bad732c0f24b0a4d7289199011e8233`.
The layer metadata response was 9,675 bytes with SHA-256
`9017c62a1e48fe170c7cbece16dc2ef9e8d07a3fe3b4314d378b2f338455f7e9`.
They completed at `2026-09-14T16:57:38.209433Z` and
`2026-09-14T16:57:38.453606Z`. Their HTTP `Last-Modified` value was
`Wed, 10 Jul 2024 10:18:48 GMT`; that header is not a substitute for the named
December 2021 boundary vintage.

The retained collector-source export digests are:

- OS product-metadata collector:
  `4fbff7e83c0f0ab7430a18339d25dcf6a42513286f0a0b60114ab8d71d5e4e62`;
- first ONS metadata-and-query collector:
  `10e74655f20f498e6104b6b69afbd9fe69c0217a6df39192aa885196a1ac5726`;
- second ONS attributes-first collector:
  `a9e739b50948804239150239f2ab91102d8e121a338a5fb66ab5590024cad402`.

The archive capture has no separate collector-source export. Its bounded request
plan, response records and manifest are retained instead; this document does not
invent a missing code hash.

## Geography and vintage boundary

The OS point comes from product version July 2026. The candidate ONS polygon is a
December 2021 Census geography. A later result must retain both vintages rather
than describing the join as simply “current”. The defensible join is:

1. preserve the OS native identifier and representative point in `EPSG:27700`;
2. ask the fixed ONS layer for polygons intersecting that exact point;
3. require exactly one supported feature and validate its full geometry;
4. join statistics using returned `MSOA21CD`, not `Warwick`, `FID` or an OS context
   URI;
5. expose the cross-vintage warning and source lineage with the result.

None of steps 3 to 5 happened in these attempts. In particular, this evidence does
not identify an MSOA, describe a Warwick boundary, prove the point represents the
whole town, or support a postcode, address or property inference.

## Rights and redistribution

The inspected archive licence member supplied
[`http://os.uk/opendata/licence`](http://os.uk/opendata/licence) and the following
attribution statements:

- Contains OS data © Crown Copyright and database rights 2026.
- Contains Royal Mail data © Royal Mail copyright and database right 2026.
- Contains National Statistics data © Crown copyright and database right 2026.

Those notices and the product documentation are rights evidence, not an automatic
permission decision. This repository publishes only the bounded point projection
and provenance, not the archive or selected tile. Any reuse must follow the current
official terms and attribution.

The captured ONS ArcGIS service and layer copyright fields were empty. Do not turn
an empty field into a public-domain claim. Follow the official
[ONS geography licence guidance](https://www.ons.gov.uk/methodology/geography/licences),
including its attribution and third-party-rights boundaries, before distributing
a later boundary payload.

## Consequence for WEB-216

The Warwick point is suitable input for the next bounded real-geometry experiment.
It is not yet a completed X04 result or evidence for a user-facing MSOA tool. Keep
the existing synthetic edge, overlap, zero-match, duplicate and vintage tests as
contract evidence; a successful provider response and an appropriate deterministic
geometry validator are still required before claiming the real join.

No provider request was made while deriving this documentation. The two failed
ONS attempts remain preserved as failures rather than being retried or rewritten.
