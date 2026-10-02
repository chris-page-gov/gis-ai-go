---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/d14c2b843bf14a0ba47b1beff1aa2ec5",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Combined Authorities (March 2017) Names and Codes in EN",
  "description": "This file contains names and codes for Combined Authorities (CAUTH) in England as at 3 March 2017. This contains the two new combined authorities - Cambridgeshire and Peterborough and West of England. The names of the combined authorities in this product reflect those that are in common use, both within the areas and beyond. It should be noted that the names are not always the same as the names in the Statutory Instruments that established them. This is because the statutory names are often very long and not suitable for the presentation of statistics. (File Size - 16 KB) Column Descriptions: CAUTH17CD | Text | 9 CAUTH17NM | Text | 31 FID | Number | 1 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_March_2017_Names_and_Codes_in_England_2022/FeatureServer",
  "nativeIdentifier": "d14c2b843bf14a0ba47b1beff1aa2ec5",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/d14c2b843bf14a0ba47b1beff1aa2ec5",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Names and Codes",
    "England",
    "2017",
    "Combined Authorities",
    "CAUTH",
    "NAC_ADM",
    "NAC_CAUTH",
    "MAR_2017",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3801&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:16.239989Z",
      "responseSha256": "197b5422ff10730d626349afda862db34c86d2e01bb9e97b7ff7305f5365c3a8",
      "sourcePointer": "/results/53",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3853",
      "normalisedRecordSha256": "8a781abcb980692b2219d07e6efe85c2ba41227225a651c184969f04e350520d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/d14c2b843bf14a0ba47b1beff1aa2ec5"
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
    "metadataModified": "2025-08-11T08:10:41Z",
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
      "/Categories/Names and Codes/Administrative",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1666179431000,
    "culture": "en-us",
    "description": "This file contains names and codes for Combined Authorities (CAUTH) in England as at 3 March 2017. This contains the two new combined authorities - Cambridgeshire and Peterborough and West of England. The names of the combined authorities in this product reflect those that are in common use, both within the areas and beyond. It should be noted that the names are not always the same as the names in the Statutory Instruments that established them. This is because the statutory names are often very long and not suitable for the presentation of statistics. (File Size - 16 KB) Column Descriptions: CAUTH17CD | Text | 9 CAUTH17NM | Text | 31 FID | Number | 1 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_March_2017_Names_and_Codes_in_England_2022/FeatureServer",
    "extent": [],
    "id": "d14c2b843bf14a0ba47b1beff1aa2ec5",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899841000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Names and Codes",
    "spatialReference": "WGS_1984_Web_Mercator_Auxiliary_Sphere",
    "tags": [
      "Names and Codes",
      "England",
      "2017",
      "Combined Authorities",
      "CAUTH",
      "NAC_ADM",
      "NAC_CAUTH",
      "MAR_2017"
    ],
    "title": "Combined Authorities (March 2017) Names and Codes in EN",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_March_2017_Names_and_Codes_in_England_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Combined Authorities (March 2017) Names and Codes in EN

This file contains names and codes for Combined Authorities (CAUTH) in England as at 3 March 2017. This contains the two new combined authorities - Cambridgeshire and Peterborough and West of England. The names of the combined authorities in this product reflect those that are in common use, both within the areas and beyond. It should be noted that the names are not always the same as the names in the Statutory Instruments that established them. This is because the statutory names are often very long and not suitable for the presentation of statistics. (File Size - 16 KB) Column Descriptions: CAUTH17CD | Text | 9 CAUTH17NM | Text | 31 FID | Number | 1 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_March_2017_Names_and_Codes_in_England_2022/FeatureServer

Native identifier: `d14c2b843bf14a0ba47b1beff1aa2ec5`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/d14c2b843bf14a0ba47b1beff1aa2ec5)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
