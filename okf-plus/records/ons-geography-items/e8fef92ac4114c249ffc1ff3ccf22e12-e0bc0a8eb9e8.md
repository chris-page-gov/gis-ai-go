---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/e8fef92ac4114c249ffc1ff3ccf22e12",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Output Area (2011) to LSOA to MSOA to LAD (December 2020) Exact Fit Lookup in EW",
  "description": "A lookup between Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA), local authority districts (LAD) and Regions as at 31 December 2020 in England and Wales. (File Size 15.3MB). Field Names – OA11CD, LSOA11CD, LSOA11NM, MSOA11CD, MSOA11NM, LAD20CD, LAD20NM, RGN20CD, RGN20NM Field Types – Text, Text, Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 9, 33, 9, 32, 9, 36, 9, 24 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA11_LSOA11_MSOA11_LAD20_RGN20_EW_LU_a1cf695c9b074c708921b2a7555f808a/FeatureServer",
  "nativeIdentifier": "e8fef92ac4114c249ffc1ff3ccf22e12",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/e8fef92ac4114c249ffc1ff3ccf22e12",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Lookup",
    "OA",
    "Output Area",
    "LSOA",
    "Lower Layer Super Output Area",
    "Output Areas",
    "Lower Layer Super Output Areas",
    "MSOA",
    "Middle Layer Super Output Area",
    "Middle Layer Super Output Areas",
    "LAD",
    "Local Authority",
    "Local Authority District",
    "Local Authority Districts",
    "England and Wales",
    "Census Lookups",
    "OA_LSOA_MSOA_2011_LU",
    "LUP_CEN",
    "LUP_OA_LSOA_MSOA_LAD",
    "LUP_OA",
    "DEC_2020",
    "2020",
    "Region",
    "RGN",
    "EXACT_FIT_LU_OA_2011",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=901&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:41.974135Z",
      "responseSha256": "038d829a6a15809b80f19d9b152473ae2b2d90d3a2202852d52c4a6c2b64ed1b",
      "sourcePointer": "/results/48",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/948",
      "normalisedRecordSha256": "2b9c73fd75593edc1c352035fa71dc0a306d3de6cb2fdcec43259439a427f693",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/e8fef92ac4114c249ffc1ff3ccf22e12"
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
    "metadataModified": "2025-08-11T07:52:12Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "https://www.ons.gov.uk/methodology/geography/licences",
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
      "/Categories/Lookups/Census",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1658498574000,
    "culture": "",
    "description": "A lookup between Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA), local authority districts (LAD) and Regions as at 31 December 2020 in England and Wales. (File Size 15.3MB). Field Names – OA11CD, LSOA11CD, LSOA11NM, MSOA11CD, MSOA11NM, LAD20CD, LAD20NM, RGN20CD, RGN20NM Field Types – Text, Text, Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 9, 33, 9, 32, 9, 36, 9, 24 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA11_LSOA11_MSOA11_LAD20_RGN20_EW_LU_a1cf695c9b074c708921b2a7555f808a/FeatureServer",
    "extent": [
      [
        -6,
        49.9
      ],
      [
        2,
        61
      ]
    ],
    "id": "e8fef92ac4114c249ffc1ff3ccf22e12",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898732000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "OA (2011) Exact Fit Lookup",
    "spatialReference": null,
    "tags": [
      "Lookup",
      "OA",
      "Output Area",
      "LSOA",
      "Lower Layer Super Output Area",
      "Output Areas",
      "Lower Layer Super Output Areas",
      "MSOA",
      "Middle Layer Super Output Area",
      "Middle Layer Super Output Areas",
      "LAD",
      "Local Authority",
      "Local Authority District",
      "Local Authority Districts",
      "England and Wales",
      "Census Lookups",
      "OA_LSOA_MSOA_2011_LU",
      "LUP_CEN",
      "LUP_OA_LSOA_MSOA_LAD",
      "LUP_OA",
      "DEC_2020",
      "2020",
      "Region",
      "RGN",
      "EXACT_FIT_LU_OA_2011"
    ],
    "title": "Output Area (2011) to LSOA to MSOA to LAD (December 2020) Exact Fit Lookup in EW",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-65664b00231444edb3f6f83c9d40591f",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA11_LSOA11_MSOA11_LAD20_RGN20_EW_LU_a1cf695c9b074c708921b2a7555f808a/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Output Area (2011) to LSOA to MSOA to LAD (December 2020) Exact Fit Lookup in EW

A lookup between Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA), local authority districts (LAD) and Regions as at 31 December 2020 in England and Wales. (File Size 15.3MB). Field Names – OA11CD, LSOA11CD, LSOA11NM, MSOA11CD, MSOA11NM, LAD20CD, LAD20NM, RGN20CD, RGN20NM Field Types – Text, Text, Text, Text, Text, Text, Text, Text, Text, Text Field Lengths – 9, 9, 33, 9, 32, 9, 36, 9, 24 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA11_LSOA11_MSOA11_LAD20_RGN20_EW_LU_a1cf695c9b074c708921b2a7555f808a/FeatureServer

Native identifier: `e8fef92ac4114c249ffc1ff3ccf22e12`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/e8fef92ac4114c249ffc1ff3ccf22e12)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
