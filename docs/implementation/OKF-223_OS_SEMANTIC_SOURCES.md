# OKF-223: priority OS semantic sources

Reviewed on 18 October 2026 using the official documentation through the web
connector. This is a bounded, authored research supplement, not a full-page
capture, new API observation or entitlement determination. The accompanying
`okf-plus/source/os-field-semantics.json` contains 48 reviewed field statements
bound to six exact collection IDs in the retained NGD schema snapshot. Its hashes
cover the short displayed excerpts, explicitly not entire responses. Existing
source snapshots remain unchanged.

## Pavement width

The precise fields are `presenceofpavement_minimumwidth_m` and
`presenceofpavement_averagewidth_m`. Road Link attribution is available from
schema 2 onward; the supplement binds to `trn-ntwk-roadlink-5`. Width summaries
include both sides. These values differ from `roadwidth_minimum` and
`roadwidth_average`, which describe the carriageway.
[Road Link specification](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link).

OS assigns the pavement attribution algorithmically using topographic pavement
polygons and road links. It is not a separate pavement survey. Road-link
coverage can generalise small junction gaps, so a coverage percentage does not
locate every pavement discontinuity.
[Pavement attribution method](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-attribution).

For a particular side and subsection, use `trn-ntwk-pavementlink-1` with
`presenceofpavement_sideofroad` and `roadlinkid`. Its geometry follows the road
link; two sides can share coordinates. It is neither a pavement centreline nor
a connected pedestrian routing network. For the actual mapped pavement area,
OS points users to Road Track Or Path polygons.
[Pavement Link method](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-link-feature-type),
[field specification](https://docs.os.uk/osngd/data-structure/transport/transport-network/pavement-link).

## Building height

Preserve five distinct measures, in metres: ground elevation
(`height_absolutemin_m`), roof-base elevation (`height_absoluteroofbase_m`),
top elevation (`height_absolutemax_m`), ground-to-roof-base height
(`height_relativeroofbase_m`) and ground-to-top height
(`height_relativemax_m`). The absolute fields refer to a datum; the relative
fields refer to the building's ground level. Floor count is a separate measure.
Building v4 and Building Part v2 expose the named fields. Building Part v1 uses
documented former names, explicitly preserved in the supplement.
[Building](https://docs.os.uk/osngd/data-structure/buildings/building-features/building),
[Building Part](https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part).

Whole-building heights aggregate the extremes of constituent Building Parts.
They are not a representative average roof height. The automated route combines
building polygons with photogrammetric terrain and surface models.
[Building-height derivation](https://docs.os.uk/more-than-maps/data-demonstrators/topography-demonstrators/os-ngd-buildings/building-feature-type#building-height).

The confidence vocabulary distinguishes manual heighting, ordinary automated
derivation, geometry changed since height extraction, incomplete values and
unassessed confidence. The number of decimal places does not establish an error
bound. Preserve nulls, confidence and evidence/update dates when reporting a
height.
[Creation method](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-buildings/how-building-data-is-created#building-height),
[confidence meanings](https://docs.os.uk/osngd/code-lists/code-lists-overview/builtstructureheightconfidencevalue).

The separate MasterMap Building Height Attribute download uses `AbsHMin`,
`AbsH2`, `AbsHMax`, `RelH2` and `RelHMax`. Its documentation explicitly defines
relative values as differences between absolute values and specifies ODN for
mainland Britain, with other island datums where applicable. These download
facts are not silently attached to NGD fields: the reviewed NGD field pages say
“above datum” without establishing every record's datum.
[BHA field specification](https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-mastermap-topography-layer-building-height-attribute/os-mastermap-topography-layer-building-height-attribute-technical-specification/feature-type/building-height-attribute),
[BHA datum and precision](https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-mastermap-topography-layer-building-height-attribute/os-mastermap-topography-layer-building-height-attribute-overview/product-data).

## Road height above sea level

Use Road Link's 3D `geometry`, retaining `heightingmethod`. The documented method
labels are `DTM`, `Interpolated Bridge` and `Interpolated Tunnel`; their code-list
page supplies no more detailed definitions. `elevationgain_indirection` and
`elevationgain_againstdirection` are cumulative ascent, while
`startgradeseparation` and `endgradeseparation` are relative network levels.
Neither is an absolute elevation.
[Road Link specification](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link),
[heighting-method vocabulary](https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue).

Request supported EPSG:7405 output, which includes ODN height in metres; ordinary
EPSG:27700 is horizontal only. Verify the returned CRS and third ordinate.
ODN is a fixed reference based on historic mean sea level, not the current tide
or present-day mean sea level. A point between supplied vertices requires an
explicitly labelled interpolation. `physicallevel` is categorical relative
position, not height in metres.
[CRS definitions](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems),
[ODN definition](https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems/ordnance-datum-newlyn),
[physical levels](https://docs.os.uk/osngd/code-lists/code-lists-overview/physicallevelvalue).

An OS Terrain sample is a different answer: the DTM models bare ground and
removes supported bridges and other overhead structures. It must not silently
replace a requested road-deck height.
[OS Terrain source modelling](https://docs.os.uk/os-downloads/products/land-and-terrain-portfolio/os-terrain-5/os-terrain-5-overview/source-data).

## Retrieval and completeness

Recommended implementation: resolve the exact collection and schema first, use
the collection's `/schema` for available output and `/queryables` for permitted
filters, then retrieve bounded `/collections/{collectionId}/items` on demand.
The API defaults to CRS84; `crs` controls output and `bbox-crs` independently
controls the input box. A schema field's existence does not prove it is
filterable or populated. Preserve feature identity, version, response CRS and
the request's spatial/time scope in the retrieval evidence.
[API endpoints](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification),
[feature request parameters](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features).

Metadata coverage must reconcile three separate documentation families: API
capabilities, NGD feature/attribute/code-list definitions, and downloadable
product specifications and lifecycle notices. An index URL is not captured
page content; retained table headings and labels omit explanatory prose and
derivation guidance demonstrated above. NGD Features also excludes some NGD
collections, so its collection inventory is not the whole NGD catalogue.
[Current API catalogue](https://docs.os.uk/os-apis),
[NGD Features exclusions](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features),
[NGD access methods](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/terminology-and-access).

Select+Build creates selected NGD download packages. The Downloads API discovers
and retrieves existing packages and their versions; it cannot create or alter
packages. Package availability is account-specific. Public documentation cannot
establish an organisation's entitlement.
[Downloads API scope](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api),
[checking account API access](https://docs.os.uk/os-apis/core-concepts/getting-started-with-an-api-project#finding-out-what-os-apis-you-have-access-to).

Keep API major collection IDs and documented minor schema versions separate.
OS replaces minor versions while retaining some older major versions. The
supplement only adds definitions to exact retained field bindings; it does not
claim that current documentation retroactively refreshes older snapshots.
[Versioning policy](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning).

For retrieval pacing, the public FAQ states 600 transactions per minute per API
per project, or 50 for Premium development projects. A conservative default
below 50 per minute is an operator choice, not a claim about documentation-host
limits or a verified Downloads-specific exemption. Use bounded retries and
request ceilings, and retain failures as incomplete acquisition.
[Official throttling FAQ](https://osdatahub.os.uk/support/plans?lang=en).

The live catalogue now includes OS Net API. OS Match & Cleanse was withdrawn on
31 March 2026. Historical documentation and search results can still contain
withdrawn services; lifecycle status needs its own evidence.
[OS Net](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api),
[withdrawal notice](https://docs.os.uk/os-apis/accessing-os-apis/os-match-and-cleanse-api).
