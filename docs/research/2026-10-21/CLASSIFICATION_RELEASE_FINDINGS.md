# Selected address, Census and map classification lists

Review updated: 22 October 2026. This follows the initial
[33-family investigation](VOCABULARY_FAMILY_MATRIX.md). Complete selected-list
traversal is separate from definitions, edition adoption, mapping and whole-domain
coverage. Full source bodies and lists are retained privately; this public note
contains findings and methods, not licensed payloads.

## Sites and VectorMap documentary scope

Complete traversal of 17 retained OS MasterMap Sites Layer documents yields
47 field definitions, 50 documented GML-to-GeoPackage name mappings and 11
selected lists with 81 entries. Sixty entries have source definitions; 21 are
literal valid-combination strings. Grouped function values are not silently
split into invented atomic codes. This is documentary coverage, not validation
of delivered geometry, identifier joins or an actual format conversion.

The Sites field definitions distinguish an AccessPoint's site reference from
its optional routing references. A FunctionalSite's optional primary AddressBase
UPRN refers to its primary building; it does not enumerate all addresses.
Native field names containing `ITN` and prose referring to Highways are both
preserved, without assuming a dataset substitution. A documented `1900-01-01`
placeholder for a referenced road version is not treated as the road's creation
date. See the [Sites technical specification](https://docs.os.uk/os-downloads/products/land-and-terrain-portfolio/os-mastermap-sites-layer/os-mastermap-sites-layer-technical-specification)
and [access-direction definitions](https://docs.os.uk/os-downloads/products/land-and-terrain-portfolio/os-mastermap-sites-layer/os-mastermap-sites-layer-technical-specification/enumerations/accessdirectionvalue.md).

The selected VectorMap context contains 21 retained documents, 39 field
definitions and 32 tile-attribute rows. Six selected documentary lists retain
221 entries, including 67 uncoded Important Buildings names. One figure is
withheld from retained text, with its exact span and hash recorded privately;
its meaning has not been inspected. The [Important Buildings list](https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-vectormap-local/os-vectormap-local-technical-specification/important-buildings-classification.md)
provides source groups and names, not invented numeric codes or coded parents.

The selected index points to an OpenMap Local draw-level list, whereas a
VectorMap field points to its separate product list. The domains remain distinct.
The [TextFont list](https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-vectormap-local/os-vectormap-local-technical-specification/code-lists/textfontvalue.md)
retains two explicitly obsolete values that the structured font field excludes.
This can reflect version history; no supplier error or effective date is inferred.
Likewise, text-rendering height measures map text in ground-distance units, not
physical building height. Tile and GML coordinate-system declarations do not
prove coordinate transformation or attribute equivalence.

The private demonstration now exposes 50 selected schemes and 1,805 entries.
Separate YAML-LD exports of the added lists preserve uncoded names as
documentation records and retain source definitions, nulls, qualified lexical
forms and ambiguity.
These counts are a selected demonstration denominator, not a catalogue of every
domain vocabulary. Linked schema and XML code-list dependencies, actual payload
applicability, historical base/change chains and paired supplier conversions
remain open. A change-only deletion may mean leaving the selected area; it does
not by itself establish demolition. No private list or feature payload is added
to the repository by this source increment.

## AddressBase and NGD

The [AddressBase classification page](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/classification-scheme)
links the product classification package and reports an update on 17 January 2025.
The captured package contains four CSV files and a PDF. It does not contain an
XLSX file despite the page's description. The explanatory PDF is version 2.0,
dated April 2023. These dates and packaging observations are different facts;
they do not establish the effective date of every row.

The main CSV and the [NGD address classification list](https://docs.os.uk/osngd/code-lists/code-lists-overview/addressclassificationcodevalue)
each contain 579 entries with the same set of codes. There are 573 identical
labels and six differing labels. In particular, `ZU01` and `ZU04` have the
“Cave” and “Pothole / Natural Hole” descriptions reversed between the two captured
sources. Neither source is silently corrected, and no complete semantic
equivalence is asserted.

The main CSV's component columns preserve four levels. Hierarchy must use those
columns or explicit source relationships, not a guess from code length. A missing
immediate parent remains unresolved. The main list and NGD table supply labels;
the older explanatory PDF is not silently applied as a definition for every
current row. Product epochs, feature-schema versions and classification releases
remain separate.

## Census dictionaries and Nomis

The selected sources cover Census 2021 England and Wales, with the following
distinct denominators:

| Topic | ONS dictionary classification | Selected Nomis dataset and dimension | Entries: ONS / Nomis |
| --- | --- | --- | --- |
| Residence type | `residence_type` | TS001, `NM_2021_1`, `C2021_RESTYPE_3` | 2 / 3 |
| Ethnic group | `ethnic_group_tb_20b` | TS021, `NM_2041_1`, `C2021_ETH_20` | 20 / 25 |
| Religion | `religion_tb` | TS030, `NM_2049_1`, `C2021_RELIGION_10` | 10 / 10 |

Sources: ONS [residence type](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/residencetype),
[ethnic-group classifications](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/ethnicgroupnationalidentitylanguageandreligionvariablescensus2021/ethnicgroup/classifications),
[religion classifications](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/ethnicgroupnationalidentitylanguageandreligionvariablescensus2021/religion/classifications);
Nomis [residence categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2021_1/c2021_restype_3.def.sdmx.json),
[ethnic-group categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2041_1/c2021_eth_20.def.sdmx.json),
[religion categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2049_1/c2021_religion_10.def.sdmx.json).

All three selected Nomis lists include a total; ethnicity also includes five
group aggregates. The datasets state All usual residents as their universe,
Persons as their unit, and 21 March 2021 as the Census reference date.
An ONS not-applicable code is not
the same concept as a Nomis total. Seventeen of the 19 matching ethnic-group
leaf labels use different numeric codes between the selected dictionary and API
lists. Matching text is recorded as a comparison, not an authorised mapping.
Population, statistical unit, dataset, dimension and edition remain necessary.
Residence type classifies people, not buildings. Religion's unanswered category
must remain distinct from no religion. Totals must not be summed with their parts.

The capture includes dataset, measure and time metadata, preserving release and
revision context without retrieving statistical observations. Reference date,
dataset publication/revision, dictionary update and retrieval time are labelled
separately. A code-list identifier alone does not prove a separately dated list
release or the operational denominator of every measure.

## Rural/urban classes for the OA journey

The [ONS RUC 2021 user guide](https://www.arcgis.com/sharing/rest/content/items/c8e8e6db38e04cb8937569d74bce277a/data)
prints six names in its Output Area map legend. The complete legend was visually
checked and retained as a separate source list. It combines the three settlement
classes with relative access to a major town or city. The names come from the
legend itself, not a generated Cartesian product.

The guide does not supply native `RUC21CD` codes; these remain unknown in the
browser. It also distinguishes OA classification from the population-based
aggregation used for larger statistical areas and the separate LAD classification.
Guide and webpage threshold wording differ, so this increment does not implement
a threshold or silently choose one wording. The [current ONS RUC page](https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification)
and the guide remain distinct dated sources. The native `RUC21CD` dictionary
remains open; these class lists do not establish area assignments.

## Reused ONSUD domains

The later offline pass reopened the accepted ONS UPRN Directory (ONSUD)
ancillary evidence, without retrieving its national archive again. Independent
reconstruction verified all 52 `OAC21IND` rows, six England and Wales
`RUC21IND` rows and six Scottish `RUC21IND` rows. The selected OAC rows contain
eight Supergroup, 21 Group and 52 Subgroup labels in explicit source columns.
Those columns do not supply parent codes, so no code-prefix hierarchy is created.

The OAC member's title says UK; the ONSUD guide describes the field for Great
Britain. Preserve both facts. The Scottish six-fold rural/urban definitions are
retained from the guide; the other selected domains remain labels-only. Census
reference years, the May 2025 rural/urban filenames and the September 2026
ONSUD package edition are separate dates. Exact lookup publication dates and
language declarations remain unknown.

These native ONSUD domains do not establish equivalence with the separately
observed `RUC21CD` field, new area assignments or all OAC editions. See the ONS
[ONSUD overview](https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts)
and [residential area classification guidance](https://www.ons.gov.uk/methodology/geography/geographicalproducts/areaclassifications/2021and2022residentialbasedareaclassifications).

## Further Census contexts and source questions

A further bounded public metadata selection captures the complete category,
dataset, time and measure responses for TS054 tenure (`NM_2072_1`), TS008 sex
(`NM_2028_1`) and TS038 disability (`NM_2056_1`). It requests no statistical
observations or geography members. The selected Nomis lists contain 15, three
and seven entries respectively; those counts include supplied totals and
aggregate rows, not just leaf categories. Source `DisplayName` annotations are
qualified alternative labels, not invented synonyms or cross-scheme mappings.

All nine classification tables on the four selected ONS pages are retained:
the tenure variable table, all six tenure classification variants, sex and
disability. This yields 59 ONS entries alongside 25 Nomis entries. These are
separate source lists, not 84 distinct universal concepts.

The [tenure variable page](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/housingvariablescensus2021/tenureofhousehold)
uses `hh_tenure` for nine categories and reports an update on 28 November 2023.
The [classification page](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/housingvariablescensus2021/tenureofhousehold/classifications)
uses the same mnemonic for eleven categories and `hh_tenure_9a` for nine,
with an update on 26 October 2023. Source-page identity therefore remains part
of the projected scheme identity. The intended current relationship needs
clarification; a different page date alone does not resolve it.

The [Nomis tenure list](https://www.nomisweb.co.uk/api/v01/dataset/NM_2072_1/c2021_tenure_9.def.sdmx.json)
also contains derived aggregate codes whose `ChildCount` annotations do not
equal the number of rows with an explicit matching `parentcode`. The projection
preserves both fields and reports the difference without inventing aggregate
membership or treating this as a proven supplier error. For the selected tenure dataset, the statistical unit is households and the
universe is all households; sex and disability use persons and all usual residents. A property
or UPRN is neither a household count nor a person count.

The [sex dictionary](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/demographyvariablescensus2021/sex)
and [disability dictionary](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/healthdisabilityandunpaidcarevariablescensus2021/disability)
retain the source question, population and comparison limits. The captured
Nomis disability time list has no explicit Census-date or revision annotations,
while its dataset description separately states 21 March 2021. Missing revision
dates remain unknown. A preparation timestamp is neither a publication date nor
the period measured.

## AddressBase field definitions and four ancillary lists

A complete traversal of six retained AddressBase pages, with two separate
classification/format context pages, yields 26 field definitions, 18 code-list
entries and a 27-row CSV/GML name mapping. The four selected lists are
[change type](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/code-lists-and-enumerations/changetypecode.md),
[country](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/code-lists-and-enumerations/countrycode.md),
[postcode type](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/code-lists-and-enumerations/postcodetypecode.md)
and [representative point code](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/code-lists-and-enumerations/rpccode.md).
Their respective counts are three, seven, two and six. Fifteen entries have
source descriptions or implementation notes; the three change-type entries have
labels only. Language, effective edition, aliases and hierarchy remain unknown
where the source does not declare them.

A representative point code describes the address seed's placement and related
caveats. It is a category, not a numeric confidence score or an unconditional
accuracy guarantee. The full alternative clauses remain in the retained
source definitions. Postcode type distinguishes small and large postal users;
it is not a residential/commercial or household-size classification. A shared
country code list does not establish each product's coverage or valid subset.

The retained CSV/GML name-mapping table includes `DEPENDENT_THOROUGHFARE`,
but the selected Address feature page has no corresponding definition section. Two CSV/GML mapping cells are
empty, for `Y_COORDINATE` and `LONGITUDE`; empty documentation is not proof of
absent GML properties. SupplySet is described for GML only. The mapping is a
source name table, not an observed lossless conversion. Full schema, payload,
product-specific adoption and edition correspondence remain separate checks.

## Age, occupation and economic activity in Nomis

Twelve additional public metadata responses cover category, dataset, time and
measure context for these complete selected lists:

| Topic | Dataset and dimension | Retained entries | Statistical population |
| --- | --- | --- | --- |
| Age bands | TS007B, `NM_2018_1`, `C2021_AGE_12A` | 12 | All usual residents |
| Occupation | TS063, `NM_2080_1`, `C2021_OCC_10` | 10 | Usual residents aged 16 and over, employed in the week before the Census |
| Economic activity | TS066, `NM_2083_1`, `C2021_EASTAT_20` | 31 | All usual residents aged 16 and over |

Sources: Nomis [age categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2018_1/c2021_age_12a.def.sdmx.json),
[occupation categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2080_1/c2021_occ_10.def.sdmx.json)
and [economic-activity categories](https://www.nomisweb.co.uk/api/v01/dataset/NM_2083_1/c2021_eastat_20.def.sdmx.json).
These 53 entries contain 27 source-stated alternative labels. Scheme-level
explanatory text is retained, but separate category definitions are not supplied.
No statistical observations or geography-member lists were requested.

The age category definition states Census Day, 21 March 2021, for England and
Wales, although its selected time list does not repeat that annotation. The
occupation context uses SOC 2020 and the employment reference week of 15 to
21 March 2021; it explicitly warns against comparison with 2011. This selected
major-group list does not close the full SOC coding index or all SOC mappings.

Census economic activity uses a different definition from the International
Labour Organization definition used by the Labour Force Survey. Derived totals
and student categories do not form an automatically disjoint partition. The
`20` suffix in the dimension identifier is not a row-count rule: the complete
observed list contains 31 rows, including aggregates. Source hierarchy and
annotations are retained without inventing aggregate membership.

The occupation and economic-activity dataset notes describe UPRN or postcode
plotting into December 2022 National Park boundaries, and OA best fit for other
geographic levels. Neither a universal OA roll-up nor a person-to-UPRN join
follows. Census reference, dataset release/revision, response preparation and
retrieval dates remain separately labelled. The observed preparation timestamps
need clarification; they are not silently converted into publication dates.

Across the three successive selections, nine Nomis category lists now contain
116 entries. The private demo exposes 33 selected schemes and 1,503 entries
across all currently accepted sources. This is a dated local projection count,
not a count of unique universal concepts or full domain coverage. The seven new
schemes preserve their complete entries and context in small YAML-LD cards;
search collisions remain explicit.

## What is now accessible, and what remains open

The [classification browser method](../../implementation/CLASSIFICATION_RELEASE_DISCOVERY.md)
supports complete selected entries, source labels, available definitions, native
fields, explicit source relationships, lexical comparisons and visible coverage
limits. Private Markdown/YAML-LD cards and the term index preserve scheme and
source-snapshot identity. The public interface tests use synthetic data.

Still open: complete edition-matched address definitions; resolution of the six
OS label differences; product-specific adoption and independently reviewed
cross-scheme mappings; remaining Nomis dimensions and classification variants;
other Census nations and editions; the native `RUC21CD` field-domain mapping,
other OAC releases and deprivation schemes;
translations and deprecations. Learning and assistive-technology acceptance also
remain separate. No national feature or statistical-observation replica is
required or created by this metadata work.
