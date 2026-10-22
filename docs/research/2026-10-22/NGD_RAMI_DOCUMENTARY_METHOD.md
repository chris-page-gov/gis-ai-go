# NGD and RAMI documentary method findings

Reviewed on 22 October 2026 using selected official text retained on 19 October.
These are dated documentary findings, not fresh checks of the live pages,
delivered features or current product editions. The accompanying
[source register](NGD_RAMI_DOCUMENTARY_SOURCES.json) records exact official URLs,
retrieval times and source hashes without republishing private source bundles.

## NGD tables: preserve the source's role and version

The selected retained inventory contains 221 NGD code-list pages and 238 table
occurrences. Independent reconstruction retained 6,022 row occurrences from
237 recognised tables; one historical table remains unresolved. These counts
describe a fixed documentary selection, not unique concepts, all current NGD
values or a supplier-wide semantic denominator. A complete selected-source
traversal is broader than semantic admission.

The [Link Reference Confidence](https://docs.os.uk/osngd/code-lists/code-lists-overview/linkreferenceconfidencevalue.md)
page illustrates that distinction. Its retained v1.0 table has a value-shaped
header where the v2.0 table has Label/Definition headings. The former table's
header, rows and template controls remain preserved without repairing it into
an invented list. This is an unresolved documentary clarification, not a
confirmed supplier defect. Similarly, repeated native labels in
[Land Description](https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md)
remain separate occurrences rather than being silently deduplicated.

Across the selection, 32 tables have source version tabs and 206 do not.
Version labels, release statements, retrieval dates and unknown publication or
reference dates remain distinct. A historical table cannot establish the
applicable schema or enum for a newly acquired feature. Missing definitions
also remain explicit: 2,091 admitted rows have an empty definition or a native
missing-definition statement. The display uses a null definition while retaining
which source form was present. It does not replace labels with invented prose.

A Label column is a documentary value column. A string in it may be a field's
actual enumeration value, but the heading alone does not prove a separate code,
preferred language label, synonym, alias or cross-version replacement. A
projection can leave `code` null while preserving every native cell and its
exact source locator. This does not reinterpret separately evidenced
Address classification codes or deny string enum semantics.

Feature context matters. [Address Classification Source](https://docs.os.uk/osngd/code-lists/code-lists-overview/addressclassificationsourcevalue.md)
describes different derivation routes; it is not evidence that any particular
feature satisfies one. [Access Level](https://docs.os.uk/osngd/code-lists/code-lists-overview/accesslevelvalue.md)
distinguishes Building Access Location context from a similarly named physical
level. The selected [Heighting Method](https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue.md)
list supplies values without definitions. Matching words cannot close those
meaning gaps.

## RAMI: document mappings without inventing conversion equivalence

The selected Routing and Asset Management Information (RAMI) review covers
53 retained pages, including 160 declaration sections and 232 GML/GeoPackage
mapping rows. Thirteen declaration sections are explicitly ambiguous
repetitions. Counts are documentary occurrences, not a complete, unique field
model or delivered-schema conformance result.

The retained [TemporalPropertyType](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/data-types/temporalpropertytype.md)
page contains an attribute block identical to the
[Special Designation](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/asset-management/feature-types/special-designation.md)
block. The temporal introduction and repeated block must be kept separate; the
repetition does not establish usable TemporalPropertyType fields. The flat
[data-types page](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/data-types.md)
describes Paths and links nine types, whereas the nested
[RAMI data-types page](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/routing-and-asset-management-feature-information/data-types.md)
links five network-reference types. Different scopes and routes do not prove
aliasing or edition succession.

The [GeoPackage overview](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/geopackage-overview.md)
states that some GML attributes are not mapped and describes separate geometry
representation. Native mapping rows, generated-attribute markers and unresolved
field names therefore remain evidence, not executable conversions. The
[COU supply description](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-mastermap-highways-network-routing-and-asset-management-information/os-mastermap-highways-network-routing-and-asset-management-information-technical-specification/change-only-update-cou-supply.md)
distinguishes initial/full supply and later changes, including features leaving
an order's area. A deletion observation alone does not prove real-world removal.
No delivery sequence was applied by this documentary review.

## Reusable retention and learning rules

Keep full native rows, source spans, version tabs and absent/empty/null states
before deriving display terms. Treat template controls and media separately
from list entries; account explicitly for any withheld span rather than claiming
lossless retention. Preserve repeated values and order. Keep links and mapping
labels distinct from proven target identifiers or XPath paths.

The [collection selector](../../../examples/geography-task-experience/COLLECTION-SELECTION.md)
supports bounded navigation between separately reviewed projections without
raising the widget's limits. Its search scope is the active collection. Neither
the selector nor an exact string match supplies a semantic crosswalk.

Next evidence needs are edition-matched field/schema adoption, complete linked
domains where not yet reviewed, clarification of ambiguous headings, and paired
GML/GeoPackage evidence for nulls, repeats, geometry, reference order and change
meaning. Documentation alone does not prove those conversions. This public
method note includes no provider payload, credentials, local paths, private
feature identifiers, contact message or data-publication authority.
