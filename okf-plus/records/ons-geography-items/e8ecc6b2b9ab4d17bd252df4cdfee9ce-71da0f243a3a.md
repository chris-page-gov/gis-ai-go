---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/e8ecc6b2b9ab4d17bd252df4cdfee9ce",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Non-Civil Parished Area to Local Authority District (April 2020) Lookup in EN (V2)",
  "description": "This file is a lookup between non-civil parished areas to local authority districts in England as at 31st December 2020. (File Size - 48 KB) Field Names - NCP20CD, NCP20NM, LAD20CD, LAD20NM, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 52, 9, 35 ID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. File updated to include changes to 6 parishes and Leeds, unparished area in Leeds following late receipt of parish order - The Leeds (Reorganisation of Community Governance) Amendment Order 2018 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NCP20_LAD20_EN_LU_v2_ec577709189448f489458ca4ca6b184a/FeatureServer",
  "nativeIdentifier": "e8ecc6b2b9ab4d17bd252df4cdfee9ce",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/e8ecc6b2b9ab4d17bd252df4cdfee9ce",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "LUP_ADM",
    "LUP_NCP_LAD",
    "NCP",
    "Non-Civil Parished Areas",
    "LAD",
    "Local Authority",
    "Local Authority Districts",
    "England",
    "2020",
    "APR_2020",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=901&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:41.974135Z",
      "responseSha256": "038d829a6a15809b80f19d9b152473ae2b2d90d3a2202852d52c4a6c2b64ed1b",
      "sourcePointer": "/results/30",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/930",
      "normalisedRecordSha256": "86bd1d36421712ddcad7ca6184f96ef010708069a76171f951ef2d03215c6007",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/e8ecc6b2b9ab4d17bd252df4cdfee9ce"
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
    "metadataModified": "2025-11-25T09:40:34Z",
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
      "/Categories/Lookups/Administrative",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1658492824000,
    "culture": "en-gb",
    "description": "This file is a lookup between non-civil parished areas to local authority districts in England as at 31st December 2020. (File Size - 48 KB) Field Names - NCP20CD, NCP20NM, LAD20CD, LAD20NM, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 52, 9, 35 ID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. File updated to include changes to 6 parishes and Leeds, unparished area in Leeds following late receipt of parish order - The Leeds (Reorganisation of Community Governance) Amendment Order 2018 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NCP20_LAD20_EN_LU_v2_ec577709189448f489458ca4ca6b184a/FeatureServer",
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
    "id": "e8ecc6b2b9ab4d17bd252df4cdfee9ce",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1764063634000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Lookup",
    "spatialReference": null,
    "tags": [
      "LUP_ADM",
      "LUP_NCP_LAD",
      "NCP",
      "Non-Civil Parished Areas",
      "LAD",
      "Local Authority",
      "Local Authority Districts",
      "England",
      "2020",
      "APR_2020"
    ],
    "title": "Non-Civil Parished Area to Local Authority District (April 2020) Lookup in EN (V2)",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-d1ac580844bc4bedbcd4fab2e39cea00",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NCP20_LAD20_EN_LU_v2_ec577709189448f489458ca4ca6b184a/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Non-Civil Parished Area to Local Authority District (April 2020) Lookup in EN (V2)

This file is a lookup between non-civil parished areas to local authority districts in England as at 31st December 2020. (File Size - 48 KB) Field Names - NCP20CD, NCP20NM, LAD20CD, LAD20NM, FID Field Types - Text, Text, Text, Text, Numeric Field Lengths - 9, 52, 9, 35 ID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. File updated to include changes to 6 parishes and Leeds, unparished area in Leeds following late receipt of parish order - The Leeds (Reorganisation of Community Governance) Amendment Order 2018 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NCP20_LAD20_EN_LU_v2_ec577709189448f489458ca4ca6b184a/FeatureServer

Native identifier: `e8ecc6b2b9ab4d17bd252df4cdfee9ce`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/e8ecc6b2b9ab4d17bd252df4cdfee9ce)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
