# Selected address and Census classification lists

Review date: 21 October 2026. This follows the initial
[33-family investigation](VOCABULARY_FAMILY_MATRIX.md). Complete selected-list
traversal is separate from definitions, edition adoption, mapping and whole-domain
coverage. Full source bodies and lists are retained privately; this public note
contains findings and methods, not licensed payloads.

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
and the guide remain distinct dated sources. The native code dictionary remains open; these class lists do not establish area assignments.

## What is now accessible, and what remains open

The [classification browser method](../../implementation/CLASSIFICATION_RELEASE_DISCOVERY.md)
supports complete selected entries, source labels, available definitions, native
fields, explicit source relationships, lexical comparisons and visible coverage
limits. Private Markdown/YAML-LD cards and the term index preserve scheme and
source-snapshot identity. The public interface tests use synthetic data.

Still open: complete edition-matched address definitions; resolution of the six
OS label differences; product-specific adoption and independently reviewed
cross-scheme mappings; all other Nomis dimensions and classification variants;
other Census nations and editions; the native RUC code dictionary, complete OAC
and deprivation schemes;
translations and deprecations. Learning and assistive-technology acceptance also
remain separate. No national feature or statistical-observation replica is
required or created by this metadata work.
