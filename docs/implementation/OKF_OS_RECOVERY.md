# OS knowledge and acquisition recovery

Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Owner instruction and observation date: 19 October 2026. Local implementation
from `f8292cbb`; no deployment, installed connector registration or protected-main
acceptance is implied. The initial working tree was clean. No execution log for
the quoted failed prompt was supplied, so its precise failure cause is unknown.

## Objective and authority

Preserve small, rich OKF+ evidence files with Linked Data. A question should locate
the relevant native field and its explanatory evidence without requiring the
model to consume a whole catalogue. Keep source identifiers, version, units,
nulls, quality, measurement methods, datum, applicability, rights and provenance
distinct. Missing explanations remain missing rather than being inferred.

The owner clarified the objective: process available feature data transiently,
retain semantic knowledge and reproducible efficient methods, then discard feature
payloads after verified processing. Permanent national feature storage is not a
prerequisite. Bounded staging capacity, complete processing evidence and verified
cleanup are required for each selected acquisition. An archive host is a deferred
fill-in if a later operation needs it; no new storage service is selected here.

The owner confirmed government PSGA rights and authorised the existing key for
private retrieval. This authority persists during unattended execution. It does
not require another approval for each request. Existing restrictions on public
licensed payloads, new services and chargeable overage remain. No secret value
was printed or placed in a URL, source file or receipt.

## Confirmed starting point

- The last accepted metadata checkpoint reports 30,833 Markdown/Linked Data
  records. The recovery build reproduced that count and retained 2,915 NGD field
  nodes; its 12 known schema findings remain visible.
- Live NGD discovery returned 94 versioned collections. This is the returned API
  catalogue, not all OS data or the complete PSGA entitlement.
- Authenticated Downloads discovery returned 47 configured packages containing
  374 version references. Configured packages do not enumerate every product the
  government can order or every API operation the key can invoke.
- The official [rate policy](https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy)
  states 600 transactions/minute for live projects and 50 for development
  projects, per API and project. Project mode is unconfirmed. The private API
  inventory uses at most about 30 starts/minute, no redirects or automatic retries,
  and stops on 429. Other consumers of the same project can still consume capacity.
- About 30 GB was available locally. The first 34 inspected versions alone listed
  about 328 GB of compressed file entries. This includes historical releases and
  is not a deduplicated current national-data requirement. Keeping that archive
  cohort locally would exceed available capacity. Transient processing can use
  bounded selections and staging; these counts do not prove a national scan.

The initial documentation requests returned HTTP 403 with the default client
user agent. The documented metadata client identity then succeeded normally;
no proxy, access check or TLS verification was bypassed.

## Implemented evidence path

```mermaid
flowchart LR
  Q[Question] --> I[Deterministic discovery]
  I --> F[Small native field card]
  F --> S[Collection and schema provenance]
  F --> P[Private explanatory passages]
  S --> R[API or download plan]
  R --> E[Measured acquisition and processing estimate]
  R --> C[Capacity and resumable acquisition checkpoint]
```

The diagram describes the intended connected evidence path. The tools below are
local maintenance operations, not new hosted MCP tools. Live feature execution,
complete graph traversal and installed Ask OKF admission remain separate work.

| Operation | Concrete behaviour | Material limit |
| --- | --- | --- |
| Existing build/search | Retains and searches complete `okfp:field` metadata with the parent record. | Whole-record retrieval can still omit an oversized collection explicitly. |
| `field_cards.py` | Exports 2,915 independent JSON-LD field cards, about 3–12 KB each, with parent/schema/source hashes, rights and limitations. Bounded search returns whole cards. | Evidence derives from retained schemas; no missing definitions, units or datum are invented. The optional machine index is larger than an individual card. |
| `passages.py` | Splits original Markdown losslessly into bounded JSON-LD passages with source digest, heading context, line and byte/character offsets. Reconstruction is exact, including Unicode and original line endings. | Private original text remains untrusted evidence. A manifest is an ordered index and may exceed the individual-passage ceiling. |
| `field_passages.py` | Creates private candidate links from exact native headings to full explanatory section passages for three explicitly bound collection versions. Actual export: 178 matches and 19 missing headings across 197 fields. | Route review and exact-heading matching do not independently establish documentation-version equivalence. Ambiguous headings are refused. |
| `os_document_sync.py` | Captures only the 2,303 exact URLs in three frozen committed documentation indexes, with separate private ledger, one-writer lock, budgets, failures and resumable passage verification. | The frozen October index may omit later pages. A bounded batch is not full documentation coverage. No page-discovered links are followed. |
| `os_private_inventory.py` | Retrieves fixed catalogue and validated native package-version metadata routes, retaining private checksum-backed receipts. | File URLs are recorded privately, never executed. Inventory is not feature acquisition or proof of complete entitlement. |
| `retrieval_plan.py` | Compares acquisition and processing estimates from explicit counts, page sizes, rate ceilings, latency, archive sizes and measured throughput. | Missing measurements yield unknown estimates. Comparison requires matching coverage. It does not execute a provider call. |
| `query_planner.py` | Builds offline candidate recipes from explicit native field identities, coverage and evidenced mappings/capabilities. | No inferred join, cross-collection capability, field equivalence or execution grant. |
| `ngd_extract.py` | Acquires bounded NGD selections with checkpoints and integrity checks; disposal requires a complete selection-bound profile. | Pagination and a complete bounded selection do not establish a full national scan. |
| `transient_profile.py` | Profiles bounded GeoJSON or streaming NDJSON without retaining feature contents in its report. | Input deletion is opt-in after complete success and restricted to ignored artefacts; retention intent alone does not prove cleanup. |
| `route_comparison.py` | Compares supplied route observations with explicit identity paths, context and reviewed mappings; prepares candidate support drafts. | Draft only: no automatic OS support submission, semantic equivalence decision or source-independence guarantee. |
| Query capability profiles | Small source-bound [NGD](../../okf-plus/profile/os-ngd-query-capabilities.json), [WFS](../../okf-plus/profile/os-wfs-query-capabilities.json) and [Downloads](../../okf-plus/profile/os-download-query-capabilities.json) registries. | Documented, observed and unverified claims remain separate; profiles grant no execution authority. |

The operation-output contract is
[`recovery-operations.schema.json`](../../okf-plus/schemas/recovery-operations.schema.json).
It provides optional structural assurance, not upstream byte verification or
execution permission. Owner: repository owner. Threats include source instructions,
credential leakage, redirects, unsafe paths, checksum substitution, oversized
responses, rate exhaustion and false completeness. Policy: fixed routes and source
scope, private evidence, whole-evidence byte limits, no source execution and no
public account/licensed data. Synthetic tests exercise refusal and preservation.

Passage directories are staged and verified before atomic publication, so an
interrupted write does not publish a partial final directory. Existing destinations
are preserved even if created concurrently. This publication currently requires
Linux `renameat2`; unsupported hosts fail closed. The managed acquisition host
passed these checks. This does not establish a cross-platform capture guarantee.

## User example acceptance boundaries

- **Pavement width:** actual native fields include
  `presenceofpavement_averagewidth_m` and
  `presenceofpavement_minimumwidth_m`. Road Link and Pavement Link are distinct
  parents; source attribution must establish which is appropriate.
- **Building height:** `height_absolutemax_m`, `height_absolutemin_m` and
  `height_absoluteroofbase_m` differ from relative heights. Absolute maximum can
  include a chimney; absolute minimum describes underlying ground. Do not replace
  the documented datum with an assumed sea-level reference.
- **Road height above sea level:** `elevationgain_indirection` and
  `elevationgain_againstdirection` describe gain, not absolute elevation. Finding
  them is useful discovery, not a successful answer to the original question.
  Geometry dimension, heighting method, datum, bridge/tunnel behaviour, accuracy
  and any terrain-derived estimate need their own source-backed checks.

A private bounded Road Link v5 request subsequently returned HTTP 200 in about
1.0 second with two finite 3D LineStrings and a matching EPSG:7405 response header.
The official CRS guidance defines this as British National Grid plus ODN Height.
Both sampled methods were Interpolated Bridge. This demonstrates an ODN-height
retrieval route, not direct survey accuracy, bridge clearance, instantaneous sea
level or a complete area dataset. Building v4 and Pavement Link v1 requests also
returned two features each, with the selected height/quality/date and width fields
present and non-null. All three had next-page links. Their receipts remain private under `artifacts/okf-plus/private-ngd-samples/`;
raw bodies are disposed only after complete sample profiling and verified
knowledge-file publication, or preserved when publication cannot complete.

The captured Road Link definition confirms non-null 3D LineString geometry.
`heightingmethod` describes its origin and derivation; the separate code list
currently lists DTM, Interpolated Bridge and Interpolated Tunnel with no definitions
for the values. The presence of a method label does not establish its algorithm.
Pavement guidance distinguishes algorithmically derived Road Link attribution
(including both sides) from the separate Pavement Link features for each side.
Those links coincide with the road geometry and are not pavement centre lines or
a routable pavement network. These distinctions must survive an answer.

Do not silently transfer legacy Building Height Attribute rules into NGD Building.
The legacy product documents excluded residential chimneys from its maximum-height
rule, whereas the NGD Building description says maximum height can include a chimney.
Product, version and provenance must qualify a seemingly identical measurement.

Literal substring matching of native compounds supports “pavement width”,
“building height” and “road elevation”; it adds no synonyms or physical inference.
Definitions in the private documentation are richer than the public structural
schema projection. Linking each field/version to the correct passage is a separate
semantic assertion and must remain distinguishable from lexical discovery.

## Query capabilities and route comparisons

The captured NGD contract documents `filter-lang=cql-text` for row selection,
with collection-specific queryables, at most 100 features per page and one
collection per items path. It does not advertise field projection, multi-collection
queries or server-side joins. This absence is not universal proof of rejection:
an unknown parameter may simply be ignored. WFS separately documents
`propertyName` field projection; do not transfer that parameter to NGD.

Live WFS metadata requests returned HTTP 200. The `Highways_RoadLink` schema
exposes `RoadWidthAverage`, `RoadWidthMinimum` and `RoadWidthConfidenceLevel`;
`Topography_TopographicArea` exposes `TOID`, BHA version/process date, absolute
and relative height fields and confidence. These observations correct the earlier
uncertainty about their presence, but do not prove equality with NGD measurements.
Private schema receipts remain under `private-route-comparisons/`.

NGD Road Link `toid` explicitly refers to the MasterMap feature identifier and
is a candidate identity bridge. OSID is not a TOID; NGD Building has no established
direct TOID mapping in this review. Compare exact identity, feature grain, source
version/time, CRS, units, datum, measurement definitions and quality before
claiming agreement or disagreement. Legacy and NGD chimney rules already differ.
A bounded live comparison retrieved two identical native WFS road IDs through
full-record and projected requests. `RoadWidthAverage`, `RoadWidthMinimum` and
`RoadWidthConfidenceLevel` agreed for both records. Including `SHAPE` in the
projection reduced the response from 4,668 to 2,084 bytes; mandatory extra fields
remained. This is measured agreement within WFS, not statistical confidence or
proof of WFS/NGD semantic equivalence. WFS numeric widths were strings, reinforcing
the need to preserve native types.

The same-bbox WFS projection omitting `SHAPE` returned HTTP 200 but malformed
GeoJSON; full-record and geometry-including controls parsed normally. Separately,
NGD `IN` returned 500 while equivalent equality-OR selection returned both records.
Private unsent support drafts preserve sanitised exact calls, source references,
response hashes, parser/status observations and methodology. These are candidate
issues with bounded reproduction, not a conclusion that every collection fails.
Valid comparison payloads were fully profiled and discarded; evidence receipts,
small knowledge files and minimum diagnostic excerpts remain private.

Use evidence status rather than an invented numerical confidence: documented
capability, observed behaviour, corroborated within a controlled comparison, or
unresolved equivalence. Agreement from a shared provider backend is not independent
validation. Route comparisons and candidate OS support notes are drafts for review;
no external message or definitive cross-product equivalence is implied.

## Output intent and scoped availability

The owner extended the same recovery objective with
[presentation-aware retrieval research](OS_RETRIEVAL_PRESENTATION_RESEARCH.md) and
[availability reporting](OS_DATA_AVAILABILITY.md). The small
[output-intent profile](../../okf-plus/profile/os-output-intents.json) records
required geometry, units, datum, time, grain, aggregation, quality and portrayal
understanding. VizQL and related visual query approaches are research leads,
separate from OS NGD CQL-text and WFS; Tableau-hosted pages remain blocked, but a vendor-published OpenAPI contract
was verified through the official GitHub repository at a pinned commit. It
documents data/model queries; deployed service access remains unverified.

`query_planner.py` accepts optional output requirements for table, map or analysis
with explicit `native-values`, `geometry` and/or `portrayal` capability evidence.
It filters unsuitable or unproven candidates before comparing acquisition and
processing costs. A map intent alone implies neither a renderer nor geometry
fidelity; portrayal-only evidence cannot satisfy native-value requirements.

`availability.py` produces private, offline per-source/version/selector/field
assessments with evidence hashes. Access, expected presence, observed presence and
retrieval completion are separate. Null, zero, absent property, outside coverage,
complete empty filtering, uncollected data, unavailable product, incomplete paging
and request failure remain distinct. Missing planner candidates leave data presence
unknown. Request-level HTTP 401/403 rejection is retained separately from PSGA
licence rights. Source claims are evidence, not independently established facts.
Normal responses describe the exact requested scope, avoiding irrelevant coverage
boilerplate.

All-collection explanation linking uses exact frozen collection/document titles
and native field headings, retaining every field's match or unresolved reason.
It creates candidate links rather than asserting current documentation applies to
older collection versions. Every explanation reference file is bounded to 16 KB,
with lossless manifests when references span multiple files.

Two title exceptions have explicit source-reviewed candidate bindings in the
[small binding registry](../../okf-plus/profile/os-collection-document-bindings.json):
GB Postcode Unit Point is distinguished from the identically schemed NI source by
native collection and documented geographic/API scope; RoutingStructure is matched
to Routing Structure using the source definition. Neither curation asserts
version equivalence. Registry bytes, source records and receipt hashes are checked.

Query planning refuses credential-bearing request descriptors or evidence URLs.
Availability receipt adapters bind every response, including failures, to the
requested collection and selection digest before using it. Known failed capture
receipts cannot be hidden by later pending ledger entries and retried blindly.

## Unattended continuation

The owner explicitly authorised continuation through the night. The
[bounded supervisor](../operations/OS_UNATTENDED_RECOVERY.md) waits for an existing
document writer, resumes unresolved targets under the same cumulative request
ceiling, audits captured checksums and passage reconstruction, and exports final
all-field candidate links. It records partial completion when a known redirect
failure remains. Its default wall budget is eight hours and it does not guarantee
workspace lifetime. Closing the laptop should not itself stop cloud processes,
but a saved status is not proof that a process survives or is still running.

The current metadata refresh captured all 94 collection queryables and all 94
schemas in 188 successful bounded requests. It retained complete native schema
metadata, 840 queryable-property cards, 2,915 returned-property cards and a
collection card for each response. Comparable retained definitions match the
2 October baseline. There are 2,075 returned-field entries outside the current
queryables catalogue; this limits filtering, not returned-value availability.
Provider-native schema IDs are preserved separately from endpoint URLs.

## Run and resume

From the checkout root, with locked development dependencies:

```sh
uv sync --locked --group dev --cache-dir .uv-cache
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.field_cards \
  --question 'pavement width' --max-records 3 --max-bytes 16384
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.field_passages
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.os_private_inventory \
  --max-requests 500 --wall-seconds 1800
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/os_document_sync.py \
  --max-requests 3000 --max-documents 100 --deadline-seconds 1800
```

Private outputs remain under ignored `artifacts/okf-plus/private-os-inventory/`
and `artifacts/okf-plus/private-os-documents/`. Repeat the same commands to reuse
verified successes and continue. Never launch competing writers. The package
inventory's exclusive lock is removed on ordinary completion; after a hard crash,
prove no writer remains before removing a stale lock. A prior 429 requires a
separately reviewed capture after the provider's retry window; do not erase the
receipt to force continuation. A changed frozen documentation scope requires a
new preserved capture lane. Local files are not a durable off-machine backup.

The package inventory's ceilings are cumulative: 500 attempts in the command
above, 128 MiB total, 8 MiB per response and 25-second per-request wall limit.
Documentation uses the existing capture bounds: 256 MiB total, 16 MiB per response,
0.75-second pacing, stop on 429 and a between-document run deadline. One in-flight
request can finish after the documentation run deadline.

The live navigation comparison found unchanged API (152) and NGD (478) URL sets,
but the Downloads index now contains 1,678 URLs: six added and one removed against
the frozen 1,673-target snapshot. Preserve the frozen run and record the six new
pages separately under `private-current-documentation-supplement/`; do not silently
change its denominator or treat a removed navigation link as deletion authority.
This comparison alone does not prove that unchanged URLs have unchanged content.

Before fulfilling a dataset request, state its geographical, temporal, version,
field and format coverage; estimate acquisition and processing separately; compare
the equivalent download where available; and label unknowns. Metadata timings
alone are not feature-transfer throughput. A large request needs a known archive
size or feature count, a bounded processing plan, sufficient transient staging
capacity and a verified disposal path. Permanent national storage is not required.
An archive host remains deferred unless a concrete operation needs one; do not
buy storage or select a cloud account implicitly.

## Remaining completion gates

1. The configured package-version inventory is complete. Finish the frozen
   documentation traversal; retain exact coverage, failures and unknown
   denominators in their checkpoints.
2. Establish useful current-release coverage separately from historical and
   repeated package entries; size bounded transient staging and processing,
   retain semantic findings/recipes and verify feature-payload disposal.
3. Complete source/version-matched field-to-explanation and code-list links,
   including the three examples above and explicit evidence for absent answers.
4. Implement and validate resumable feature/archive retrieval and processing,
   with integrity, coverage, rights, spatial/vertical reference and quality checks.
5. Verify connected runtime/consumer behaviour and mandatory repository assurance
   before claiming deployment or accepted integration.

No finite question set proves that every conceivable question can be answered.
The measurable goal is complete retained-source coverage, precise discovery,
source-backed explanations and honest retrieval/derivation limits.

## Local verification and integration

The affected Python discovery run passed all 306 tests. Complete offline OKF+
verification passed source/import consistency, the 30,833-record build, the declared
retrieval corpus, all-record consumer-schema validation, whole-corpus audit and
four pinned-engine cases. Four existing context-required questions remain
unassessed. Its retained report is
`artifacts/okf-plus/recovery-verification/verification.json`; the report's source
revision and exact input digest distinguish this working-tree observation from
later producer-integrity/schema edits and canonical final-source acceptance.

The existing public OKF build and repository contract checks also passed. Link,
secret and changelog checks are separate from feature or hosted acceptance.
Oversized nested field definitions are retained as bounded, lossless canonical-JSON
text fragments with checksum-backed manifests and child-card navigation; the full
definition can be reconstructed exactly. Oversized statistics/navigation still
fail closed and preserve the input. The optional transient and route-comparison
schemas validate the corresponding producer outputs and refuse authority claims.

No required CI gate, independent image derivation or deployment criterion was
relaxed. The private acquisition continues independently of integration checks.
