---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/cbfe64cc03d74af982c1afec639bafd1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW (V3)",
  "description": "This is an exact fit lookup file between Lower layer Super Output Areas as at December 2011 and Lower layer Super Output Areas as at December 2021 and Local Authority Districts as at December 2022 in England and Wales. This product has been provided with a 'change indicator' field, that define the lookup between 2011 and 2021 LSOA. This field indicates which super output areas have changed between 2011 and 2021. This is a version 3 of the lookup where the Change Indicator has been changed from splits to complex in less than 10 LSOAs and four 2011 LSOAs - Shepway 014E to Shepway 014H corrected to Shepway 015A - Shepway 015D There are four designated categories to describe the changes, and these are as follows: U - No Change from 2011 to 2021. This means that direct comparisons can be made between these 2011 and 2021 LSOA. S - Split. This means that the 2011 LSOA has been split into two or more 2021 LSOA. There will be one record for each of the 2021 LSOA that the 2011 LSOA has been split into. This means direct comparisons can be made between estimates for the single 2011 LSOA and the estimates from the aggregated 2021 LSOA. M - Merged. 2011 LSOA have been merged with another one or more 2011 LSOA to form a single 2021 LSOA. This means direct comparisons can be made between the aggregated 2011 LSOAs’ estimates and the single 2021 LSOA’s estimates. X - The relationship between 2011 and 2021 LSOA is irregular and fragmented. This has occurred where 2011 LSOA have been redesigned because of local authority district boundary changes, or to improve their social homogeneity. These can’t be easily mapped to equivalent 2021 LSOA like the regular splits (S) and merges (M), and therefore like for like comparisons of estimates for 2011 LSOA and 2021 LSOA are not possible. Field Names – LSOA11CD, LSOA11NM, CHGIND, LSOA21CD, LSOA21NM, LAD22CD, LAD22NM, LAD22NMW Field Types – Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 33, 1, 9, 40, 9, 35, 24",
  "nativeIdentifier": "cbfe64cc03d74af982c1afec639bafd1",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/cbfe64cc03d74af982c1afec639bafd1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "England and Wales",
    "2021_Census",
    "LUP_LSOA_2021_LAD",
    "DEC_2021",
    "2021",
    "LAD",
    "Local Authority",
    "Local Authority District",
    "Local Authority Districts",
    "Census Lookups",
    "LUP_CEN",
    "Lower Layer Super Output Area",
    "Lower Layer Super Output Areas",
    "LSOA",
    "LUP_EXACT_LSOA11_LSOA21",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=5601&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:37.383925Z",
      "responseSha256": "f1600a8f251a175b84915953640d232f61187cd7113efc57f173390c78a2430c",
      "sourcePointer": "/results/84",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/5684",
      "normalisedRecordSha256": "ff52b9ffc61b06f963827b663d42e8fe2c21125ac348a1323408657920eb3e56",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/cbfe64cc03d74af982c1afec639bafd1"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://geoportal.statistics.gov.uk/"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": "2025-08-11T08:22:30Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "<!--[if !supportLists]--> 1. https://www.ons.gov.uk/methodology/geography/licences",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "A date in an item title is not automatically the observation/reference range.",
    "Portal items can be different representations or vintages of one product."
  ],
  "details": {
    "access": "public",
    "categories": [
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1723116907000,
    "culture": "en-gb",
    "description": "This is an exact fit lookup file between Lower layer Super Output Areas as at December 2011 and Lower layer Super Output Areas as at December 2021 and Local Authority Districts as at December 2022 in England and Wales. This product has been provided with a 'change indicator' field, that define the lookup between 2011 and 2021 LSOA. This field indicates which super output areas have changed between 2011 and 2021. This is a version 3 of the lookup where the Change Indicator has been changed from splits to complex in less than 10 LSOAs and four 2011 LSOAs - Shepway 014E to Shepway 014H corrected to Shepway 015A - Shepway 015D There are four designated categories to describe the changes, and these are as follows: U - No Change from 2011 to 2021. This means that direct comparisons can be made between these 2011 and 2021 LSOA. S - Split. This means that the 2011 LSOA has been split into two or more 2021 LSOA. There will be one record for each of the 2021 LSOA that the 2011 LSOA has been split into. This means direct comparisons can be made between estimates for the single 2011 LSOA and the estimates from the aggregated 2021 LSOA. M - Merged. 2011 LSOA have been merged with another one or more 2011 LSOA to form a single 2021 LSOA. This means direct comparisons can be made between the aggregated 2011 LSOAs’ estimates and the single 2021 LSOA’s estimates. X - The relationship between 2011 and 2021 LSOA is irregular and fragmented. This has occurred where 2011 LSOA have been redesigned because of local authority district boundary changes, or to improve their social homogeneity. These can’t be easily mapped to equivalent 2021 LSOA like the regular splits (S) and merges (M), and therefore like for like comparisons of estimates for 2011 LSOA and 2021 LSOA are not possible. Field Names – LSOA11CD, LSOA11NM, CHGIND, LSOA21CD, LSOA21NM, LAD22CD, LAD22NM, LAD22NMW Field Types – Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 33, 1, 9, 40, 9, 35, 24",
    "extent": [
      [
        -6,
        49.9
      ],
      [
        2,
        56
      ]
    ],
    "id": "cbfe64cc03d74af982c1afec639bafd1",
    "licenseInfo": "<p style='text-indent:-18.0pt;'>&lt;!--[if !supportLists]--&gt;<span><span>1.<span style='font:7.0pt &quot;Times New Roman&quot;;'>       </span></span></span><a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1754900550000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "LSOA (2021) Exact Fit Lookup",
    "spatialReference": null,
    "tags": [
      "England and Wales",
      "2021_Census",
      "LUP_LSOA_2021_LAD",
      "DEC_2021",
      "2021",
      "LAD",
      "Local Authority",
      "Local Authority District",
      "Local Authority Districts",
      "Census Lookups",
      "LUP_CEN",
      "Lower Layer Super Output Area",
      "Lower Layer Super Output Areas",
      "LSOA",
      "LUP_EXACT_LSOA11_LSOA21"
    ],
    "title": "LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW (V3)",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_LSOA21_LAD22_EW_LU_v5/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW (V3)

This is an exact fit lookup file between Lower layer Super Output Areas as at December 2011 and Lower layer Super Output Areas as at December 2021 and Local Authority Districts as at December 2022 in England and Wales. This product has been provided with a 'change indicator' field, that define the lookup between 2011 and 2021 LSOA. This field indicates which super output areas have changed between 2011 and 2021. This is a version 3 of the lookup where the Change Indicator has been changed from splits to complex in less than 10 LSOAs and four 2011 LSOAs - Shepway 014E to Shepway 014H corrected to Shepway 015A - Shepway 015D There are four designated categories to describe the changes, and these are as follows: U - No Change from 2011 to 2021. This means that direct comparisons can be made between these 2011 and 2021 LSOA. S - Split. This means that the 2011 LSOA has been split into two or more 2021 LSOA. There will be one record for each of the 2021 LSOA that the 2011 LSOA has been split into. This means direct comparisons can be made between estimates for the single 2011 LSOA and the estimates from the aggregated 2021 LSOA. M - Merged. 2011 LSOA have been merged with another one or more 2011 LSOA to form a single 2021 LSOA. This means direct comparisons can be made between the aggregated 2011 LSOAs’ estimates and the single 2021 LSOA’s estimates. X - The relationship between 2011 and 2021 LSOA is irregular and fragmented. This has occurred where 2011 LSOA have been redesigned because of local authority district boundary changes, or to improve their social homogeneity. These can’t be easily mapped to equivalent 2021 LSOA like the regular splits (S) and merges (M), and therefore like for like comparisons of estimates for 2011 LSOA and 2021 LSOA are not possible. Field Names – LSOA11CD, LSOA11NM, CHGIND, LSOA21CD, LSOA21NM, LAD22CD, LAD22NM, LAD22NMW Field Types – Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 33, 1, 9, 40, 9, 35, 24

Native identifier: `cbfe64cc03d74af982c1afec639bafd1`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/cbfe64cc03d74af982c1afec639bafd1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
