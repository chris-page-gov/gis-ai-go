---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/c24a3c19e6f54a5cbc59e4bb4c86a2de",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "LAD (2018) to Covid Infection Survey (October 2020) Lookup in EN",
  "description": "A lookup file between 2018 Local Authority Districts to 2020 Covid Infection Survey Geography in the United Kingdom, as at 1 October 2020. (File size - 48KB) Field Names - LAD18CD, LAD18NM, LAD18NMW, CIS20CD, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 28, 28, 9 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD18_CIS20_EN_LU_v1_5fbc82fc73e6407facd67a1c5e4cc043/FeatureServer",
  "nativeIdentifier": "c24a3c19e6f54a5cbc59e4bb4c86a2de",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/c24a3c19e6f54a5cbc59e4bb4c86a2de",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "LUP_HLT",
    "LUP_LAD_CIS",
    "LAD",
    "Local Authority Disticts",
    "2020",
    "2018",
    "CIS",
    "Covid Infection Survey",
    "England",
    "LUP_CIS",
    "LUP_EXACT_CIS",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1101&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:44.236548Z",
      "responseSha256": "508c68b7523d50e1cd043fec68a7e3b66cae3eaeb8d58e729423f5277149fbd8",
      "sourcePointer": "/results/61",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1161",
      "normalisedRecordSha256": "219369808ba0365687fd7c9df0954f7eb4aeeed73b11b5eb80b5713301a8715a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/c24a3c19e6f54a5cbc59e4bb4c86a2de"
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
    "metadataModified": "2025-08-11T07:53:33Z",
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
    "created": 1659175432000,
    "culture": "en-gb",
    "description": "A lookup file between 2018 Local Authority Districts to 2020 Covid Infection Survey Geography in the United Kingdom, as at 1 October 2020. (File size - 48KB) Field Names - LAD18CD, LAD18NM, LAD18NMW, CIS20CD, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 28, 28, 9 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD18_CIS20_EN_LU_v1_5fbc82fc73e6407facd67a1c5e4cc043/FeatureServer",
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
    "id": "c24a3c19e6f54a5cbc59e4bb4c86a2de",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898813000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Health Lookup",
    "spatialReference": null,
    "tags": [
      "LUP_HLT",
      "LUP_LAD_CIS",
      "LAD",
      "Local Authority Disticts",
      "2020",
      "2018",
      "CIS",
      "Covid Infection Survey",
      "England",
      "LUP_CIS",
      "LUP_EXACT_CIS"
    ],
    "title": "LAD (2018) to Covid Infection Survey (October 2020) Lookup in EN",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-c7e48beb4a724f959711bc98230ea87a",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD18_CIS20_EN_LU_v1_5fbc82fc73e6407facd67a1c5e4cc043/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# LAD (2018) to Covid Infection Survey (October 2020) Lookup in EN

A lookup file between 2018 Local Authority Districts to 2020 Covid Infection Survey Geography in the United Kingdom, as at 1 October 2020. (File size - 48KB) Field Names - LAD18CD, LAD18NM, LAD18NMW, CIS20CD, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 28, 28, 9 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD18_CIS20_EN_LU_v1_5fbc82fc73e6407facd67a1c5e4cc043/FeatureServer

Native identifier: `c24a3c19e6f54a5cbc59e4bb4c86a2de`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/c24a3c19e6f54a5cbc59e4bb4c86a2de)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
