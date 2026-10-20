# Geography and native identifier bridges

Method version: 1. Reviewed: 21 October 2026.
Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
This is an acceptance method for separate local experiments. It adds no executor,
provider route, hosted tool, entitlement decision or live coverage claim.

The intended journey is from a local authority through statistical areas to
roads, building polygons and UPRNs. The display may resemble a hierarchy, but
its underlying evidence is a graph: geography membership, property lookups,
closest-road associations and building references have different meanings.
The same UPRN can have several relationships. A UI must preserve those differences.

## Establish identifier relationships first

Investigate the [Linked Identifiers contracts](OS_LINKED_IDENTIFIER_METHOD.md)
and source-native references before proposing a spatial operation. An existing
published relationship can answer a linkage question without point-in-polygon,
nearest-neighbour or intersection processing. It still needs evidence for its
direction, feature and identifier types, cardinality, source method and versions.
A spatial selection is justified separately when the desired relationship is
not supplied, or when the question itself asks about location or containment.

Do not force every stage into a single join or infer a chain's missing links.
Use separately reviewed bridges:

| Stage | Required evidence | What it does not establish |
| --- | --- | --- |
| Authority → MSOA → LSOA → OA | Dated published membership or lookup rows, native geography codes, the applicable jurisdiction and boundary editions. | Geometric containment, a current boundary match or applicability to every UK jurisdiction. |
| OA → UPRN | Complete processing of the selected lookup input, its source epoch, native codes, duplicate/conflict checks and current/historical status semantics. | A current-only property list, property coordinates or a building polygon. |
| UPRN → RoadLink | A typed published relationship with native method and endpoint versions. | Physical access, a serving road or a navigable route. |
| UPRN → TopographicArea | The published cross-reference and native endpoint versions. | Classification of that area as a building or containment of the property. |
| Returned TOID → native feature | An exact, documented identifier filter against a named collection/version, with complete response and native identity checks. | Equivalence of other identifier namespaces, a parent Building or a temporally aligned snapshot. |
| Building → BuildingPart / UPRN | An explicit reference contract and observed values in that direction. | A reverse-query capability or a parent association inferred from a similarly named site reference. |

Methods 5 and 9 can supply two associations from the same BLPU, respectively to
a TopographicArea and the published closest RoadLink. Their combination is not
transitive identity or proof of road access. Method 2 relates Road Links to road
surfaces and must not be used to label a road-surface polygon as a building.
See the [source-bound capability profile](../../okf-plus/profile/os-linked-identifiers-capabilities.json)
for those definitions and their limitations.

A BuildingPart collection match can establish that the returned feature is a
BuildingPart in that collection. It does not establish a Building parent or
resolve every TopographicArea returned by the relationship API. PathLink needs
its own source-backed route and relationship contract; do not reuse a RoadLink
rule solely because both contain the word “link”.

The published [Building feature definition](https://docs.os.uk/osngd/data-structure/buildings/building-features/building)
describes its BuildingPart and UPRN reference tables. Those forward references
do not establish a reverse filter: check the collection's queryables and endpoint
contract separately.

## Keep editions and completeness explicit

Record each source independently: geography year and edition, lookup epoch,
underlying address release, API product metadata where captured, collection and
schema versions, and every native endpoint version/date. A retrieval timestamp
is not a feature's validity date. Reusing a dated metadata response is not a
metadata refresh or an edition-synchronisation certificate.

An England selection must not be labelled UK coverage. Establish the relevant
statistical geography types and membership separately for other jurisdictions.
Published best-fit membership and observed geometric containment are distinct
claims, particularly where boundary and statistical geography dates differ.

Choose a small, deterministic selection that closes a recorded coverage gap.
Define selection rules before the calls and preserve failures; do not replace an
unsuccessful seed with a successful example and present the result as the
original selection. Deduplicate only identical typed targets within the same
collection while retaining every contributing source edge and its provenance.

For an exact native query, validate every returned feature, native identifier,
geometry/CRS, counts and links. Preserve zero matches as a query result, several
matches as several records, and an incomplete page as incomplete. A one-response
profile must state its stopping rule; a next-page link cannot silently authorise
another request. Do not reinterpret an incomplete response as evidence that
there are no other matches.

## Preserve strict validation and source-specific corrections

Keep the original schema bytes and strict validation result. Where a source
schema contradicts its own declarations, a separately reviewed derived profile
may express only the exact supported correction. Bind it to the original schema
hash, document the changed constraint and retain both results. The derived pass
does not turn the strict result into a pass.

Do not rename native payload fields, introduce aliases, relax all enums to admit
null, or apply a correction from another collection/version. A new discrepancy
remains a diagnostic until its own source-specific assessment. Null, absent,
empty, zero, unknown and unavailable values must remain distinguishable.

Height attributes need their native units, absolute/relative meaning, quality
and evidence/update dates. A field suffix indicating metres does not establish
a vertical datum. A horizontal CRS does not establish the datum of a separate
height attribute, and a stored decimal precision is not measurement accuracy.
Do not transfer a legacy product's definition to NGD merely because field labels
look similar. See [presentation-aware retrieval](OS_RETRIEVAL_PRESENTATION_RESEARCH.md)
for the existing height and geometry interpretation boundaries.

## Separate tiles from native features

A tile metadata observation, a decoded binary tile and a rendered map are three
separate results. A matrix-list schema is not automatically a matrix-detail
schema; a binary-response schema does not validate tileset metadata. A documented
example's consumed fields are useful partial evidence, not a complete invented
required-field contract.

Before a tile request, establish the exact collection, matrix identifiers,
origin, dimensions, axis order, CRS, tile row/column and documented binary route.
Retain the derivation of the selected tile. A returned URL template, style,
sprite or glyph reference must not extend the request selection automatically.

For binary processing, traverse the complete selected input and retain native
layer and dictionary order, field types, feature-ID presence and value, properties,
command counts and source provenance. Distinguish bounded wire/command validation
from polygon topology, full format conformance and visual rendering. Tile
coordinates, clipped/generalised features and omitted attributes are not proved
equivalent to native feature geometry or fields by a successful decode.

The [API coverage and usage guide](OS_API_COVERAGE_AND_USAGE.md) explains why
calls through these separate local methods do not establish a hosted MCP tool or
a particular dashboard counter. Do not make traffic solely to populate a counter.

## Retain small knowledge, then review disposal

Complete processing means reaching the selected input's end and reconciling all
selected records and fields, including rejected or unmatched cases. Record source
hashes, native paths, values and controlled meanings, conversion losses and exact
unresolved questions in bounded, linked knowledge cards. A navigation index does
not replace the source values it points to.

An independent reader should verify the exact inventory and reconstruct the
claimed retained evidence without importing the producer. Lossless bytes,
lossless JSON values and geometry-excluded projections are different retention
claims. State which is provided and what cannot be reconstructed.

Before raw disposal, verify independent copies on separate suitable storage and
check that no active method or prototype still depends on the raw input. Dispose
only of the exact reviewed acquired payload, preserving its hash and disposal
receipt. Do not delete the original recovery archive, unrelated files or pending
inputs. A pathname unlink is not secure erasure and does not itself prove that
an open handle has released physical storage.

## Acceptance cases for a private explorer

- Keyboard selection follows the published geography membership and announces the
  selected area. Reset restores the authority view and clears dependent selections.
- UPRN lists state their lookup scope and whether current and previous records
  can be distinguished. Pagination and empty searches preserve the full selection.
- An unqueried UPRN says that no API observation is retained. Selecting it must
  not silently launch a new provider request.
- An observed relationship shows its type, direction, method, cardinality,
  endpoint versions and relevant uncertainty. Native confidence is not displayed
  as a probability or positional-accuracy score.
- Geometry and height panels distinguish validated native matches, zero matches,
  schema diagnostics and pending evidence. A visually plausible shape is not an
  identifier or containment test.
- Every result states its dated selection and source scope. A relationship target
  is not assumed to lie within the selected area's boundary. Passing the private
  explorer checks does not establish national coverage or general accessibility
  conformance.
