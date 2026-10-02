---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/ec1b2a8e6d864e98aa6bdcc3adb7b6cd",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "LSOA (2011) to Clinical Commissioning Group to LAD (April 2018) Lookup in EN",
  "description": "A lookup file between 2011 Lower Layer Super Output Areas (LSOA), to clinical commissioning groups (CCG) and local authority districts (LAD) in England, as at 1 April 2018. (File size - 8MB) This file includes the newly formed CCGs - NHS Birmingham and Solihull CCG (E38000220), NHS Berkshire West CCG (E38000221), NHS Bristol, North Somerset and South Gloucestershire CCG (E380002220), NHS Buckinghamshire CCG (E38000223), NHS East Berkshire CCG (E38000224) and NHS Leeds CCG (E38000225) It also includes changes to the codes for NHS Fylde and Wyre CCG (E38000226), NHS Greater Preston CCG (E38000227) and NHS Morecambe Bay CCG (E38000228) following a boundary change. It also includes the local authority name change of Shepway to Folkestone and Hythe (E07000112) Field Names - LSOA11CD, LSOA11NM, CCG18CD, CCG18CDH, CCG18NM, LAD18CD, LAD18NM Field Types - Text, Text, Text, Text, Text, Text, Text Field Lengths - 9, 33, 9, 3, 57, 9, 28 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_CCG18_LAD18_EN_LU_3aaed40f43e84c2787ba8b5ace264b6c/FeatureServer",
  "nativeIdentifier": "ec1b2a8e6d864e98aa6bdcc3adb7b6cd",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/ec1b2a8e6d864e98aa6bdcc3adb7b6cd",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Lookup",
    "LSOA_CCG_LAD_LU",
    "LSOA",
    "CCG",
    "LAD",
    "Clinical Commissioning Group",
    "Lower Layer Super Output Area",
    "Local Authority District",
    "2018",
    "England",
    "Health Lookup",
    "APR_2018",
    "LUP_HLT",
    "LUP_EXACT_LSOA11_CCG_LAD",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1101&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:44.236548Z",
      "responseSha256": "508c68b7523d50e1cd043fec68a7e3b66cae3eaeb8d58e729423f5277149fbd8",
      "sourcePointer": "/results/27",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1127",
      "normalisedRecordSha256": "0bbb2f0a2f557e0a3604ea5ee0426684eb38cfc0784aeac65363f9f92d1429a6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/ec1b2a8e6d864e98aa6bdcc3adb7b6cd"
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
    "metadataModified": "2025-08-11T07:53:20Z",
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
      "/Categories/ONS Geography Open Data",
      "/Categories/Lookups/Health"
    ],
    "created": 1658747637000,
    "culture": "en-us",
    "description": "A lookup file between 2011 Lower Layer Super Output Areas (LSOA), to clinical commissioning groups (CCG) and local authority districts (LAD) in England, as at 1 April 2018. (File size - 8MB) This file includes the newly formed CCGs - NHS Birmingham and Solihull CCG (E38000220), NHS Berkshire West CCG (E38000221), NHS Bristol, North Somerset and South Gloucestershire CCG (E380002220), NHS Buckinghamshire CCG (E38000223), NHS East Berkshire CCG (E38000224) and NHS Leeds CCG (E38000225) It also includes changes to the codes for NHS Fylde and Wyre CCG (E38000226), NHS Greater Preston CCG (E38000227) and NHS Morecambe Bay CCG (E38000228) following a boundary change. It also includes the local authority name change of Shepway to Folkestone and Hythe (E07000112) Field Names - LSOA11CD, LSOA11NM, CCG18CD, CCG18CDH, CCG18NM, LAD18CD, LAD18NM Field Types - Text, Text, Text, Text, Text, Text, Text Field Lengths - 9, 33, 9, 3, 57, 9, 28 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_CCG18_LAD18_EN_LU_3aaed40f43e84c2787ba8b5ace264b6c/FeatureServer",
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
    "id": "ec1b2a8e6d864e98aa6bdcc3adb7b6cd",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898800000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Health Lookup",
    "spatialReference": null,
    "tags": [
      "Lookup",
      "LSOA_CCG_LAD_LU",
      "LSOA",
      "CCG",
      "LAD",
      "Clinical Commissioning Group",
      "Lower Layer Super Output Area",
      "Local Authority District",
      "2018",
      "England",
      "Health Lookup",
      "APR_2018",
      "LUP_HLT",
      "LUP_EXACT_LSOA11_CCG_LAD"
    ],
    "title": "LSOA (2011) to Clinical Commissioning Group to LAD (April 2018) Lookup in EN",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-0c90bf46583c4016a1b01ce9dfd561cb",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_CCG18_LAD18_EN_LU_3aaed40f43e84c2787ba8b5ace264b6c/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# LSOA (2011) to Clinical Commissioning Group to LAD (April 2018) Lookup in EN

A lookup file between 2011 Lower Layer Super Output Areas (LSOA), to clinical commissioning groups (CCG) and local authority districts (LAD) in England, as at 1 April 2018. (File size - 8MB) This file includes the newly formed CCGs - NHS Birmingham and Solihull CCG (E38000220), NHS Berkshire West CCG (E38000221), NHS Bristol, North Somerset and South Gloucestershire CCG (E380002220), NHS Buckinghamshire CCG (E38000223), NHS East Berkshire CCG (E38000224) and NHS Leeds CCG (E38000225) It also includes changes to the codes for NHS Fylde and Wyre CCG (E38000226), NHS Greater Preston CCG (E38000227) and NHS Morecambe Bay CCG (E38000228) following a boundary change. It also includes the local authority name change of Shepway to Folkestone and Hythe (E07000112) Field Names - LSOA11CD, LSOA11NM, CCG18CD, CCG18CDH, CCG18NM, LAD18CD, LAD18NM Field Types - Text, Text, Text, Text, Text, Text, Text Field Lengths - 9, 33, 9, 3, 57, 9, 28 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_CCG18_LAD18_EN_LU_3aaed40f43e84c2787ba8b5ace264b6c/FeatureServer

Native identifier: `ec1b2a8e6d864e98aa6bdcc3adb7b6cd`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/ec1b2a8e6d864e98aa6bdcc3adb7b6cd)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
