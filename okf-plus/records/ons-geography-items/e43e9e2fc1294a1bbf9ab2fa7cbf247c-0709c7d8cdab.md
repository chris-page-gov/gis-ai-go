---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/e43e9e2fc1294a1bbf9ab2fa7cbf247c",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Authority District to Fire and Rescue Authority (December 2016) Lookup in EW",
  "description": "A lookup file between local authority districts (LAD) and fire and rescue authorities (FRA) in England and Wales as at 31 December 2016. (File Size - 64 KB) Column Descriptions: LAD16CD | Text | 9 LAD16NM | Text | 28 FRA16CD | Text | 9 FRA16NM | Text | 44 FID | Number | 3 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD16_FRA16_EW_LU_df3bd0ab11684f11b9c626df78f30d6d/FeatureServer",
  "nativeIdentifier": "e43e9e2fc1294a1bbf9ab2fa7cbf247c",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/e43e9e2fc1294a1bbf9ab2fa7cbf247c",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Lookups",
    "Local Authority",
    "Local Authority District",
    "Local Authority Districts",
    "LAD",
    "Lookup",
    "England and Wales",
    "2016",
    "Fire and Rescue Authority",
    "Fire and Rescue Authorities",
    "FRA",
    "LAD_FRA_LU",
    "DEC_2016",
    "LUP_OTH",
    "LUP_LAD_FRA",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=901&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:41.974135Z",
      "responseSha256": "038d829a6a15809b80f19d9b152473ae2b2d90d3a2202852d52c4a6c2b64ed1b",
      "sourcePointer": "/results/91",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/991",
      "normalisedRecordSha256": "c2a72832cc3270f614cf1b31b8333b10852c55cc37ce4bc9ef2ad6db837b314b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/e43e9e2fc1294a1bbf9ab2fa7cbf247c"
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
    "metadataModified": "2025-12-04T10:50:25Z",
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
      "/Categories/Lookups/Other Geography",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1658564791000,
    "culture": "en-us",
    "description": "A lookup file between local authority districts (LAD) and fire and rescue authorities (FRA) in England and Wales as at 31 December 2016. (File Size - 64 KB) Column Descriptions: LAD16CD | Text | 9 LAD16NM | Text | 28 FRA16CD | Text | 9 FRA16NM | Text | 44 FID | Number | 3 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD16_FRA16_EW_LU_df3bd0ab11684f11b9c626df78f30d6d/FeatureServer",
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
    "id": "e43e9e2fc1294a1bbf9ab2fa7cbf247c",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1764845425000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Other Geography Lookup",
    "spatialReference": null,
    "tags": [
      "Lookups",
      "Local Authority",
      "Local Authority District",
      "Local Authority Districts",
      "LAD",
      "Lookup",
      "England and Wales",
      "2016",
      "Fire and Rescue Authority",
      "Fire and Rescue Authorities",
      "FRA",
      "LAD_FRA_LU",
      "DEC_2016",
      "LUP_OTH",
      "LUP_LAD_FRA"
    ],
    "title": "Local Authority District to Fire and Rescue Authority (December 2016) Lookup in EW",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-2bf2451f25824fa9a237275a49395d6b",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD16_FRA16_EW_LU_df3bd0ab11684f11b9c626df78f30d6d/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Authority District to Fire and Rescue Authority (December 2016) Lookup in EW

A lookup file between local authority districts (LAD) and fire and rescue authorities (FRA) in England and Wales as at 31 December 2016. (File Size - 64 KB) Column Descriptions: LAD16CD | Text | 9 LAD16NM | Text | 28 FRA16CD | Text | 9 FRA16NM | Text | 44 FID | Number | 3 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD16_FRA16_EW_LU_df3bd0ab11684f11b9c626df78f30d6d/FeatureServer

Native identifier: `e43e9e2fc1294a1bbf9ab2fa7cbf247c`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/e43e9e2fc1294a1bbf9ab2fa7cbf247c)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
