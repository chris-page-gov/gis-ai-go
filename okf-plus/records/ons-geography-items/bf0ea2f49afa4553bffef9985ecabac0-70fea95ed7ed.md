---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/bf0ea2f49afa4553bffef9985ecabac0",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Scottish Parliamentary Constituencies to SPR (December 2018) Lookup in SC",
  "description": "A lookup file between Scottish Parliamentary Constituencies and Scottish Parliamentary Regions in Scotland as at 31st December 2018. (File Size - 32 KB) Field Names - SPC18CD, SPC18 NM, SPR18CD, SPR18NM Field Types - Text, Text, Text, Text Field Lengths - 9, 42, 9, 21 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/SPC18_SPR18_SC_LU_e885dba76b0f49db83f1949db267a660/FeatureServer",
  "nativeIdentifier": "bf0ea2f49afa4553bffef9985ecabac0",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/bf0ea2f49afa4553bffef9985ecabac0",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Lookup",
    "Electoral Lookups",
    "Scottish Parliamentary Constituency to Scottish Parliamentary Region Lookup",
    "SPC",
    "Scottish Parliamentary Constituencies",
    "SPR",
    "Scottish Parliamentary Regions",
    "2018",
    "Scotland",
    "DEC_2018",
    "LUP_ELE",
    "LUP_SPC_SPR",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=901&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:41.974135Z",
      "responseSha256": "038d829a6a15809b80f19d9b152473ae2b2d90d3a2202852d52c4a6c2b64ed1b",
      "sourcePointer": "/results/61",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/961",
      "normalisedRecordSha256": "09a5bd9219ddfacdb59e54a53903253213fe5116e15997bf4591fc7774b850ab",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/bf0ea2f49afa4553bffef9985ecabac0"
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
    "metadataModified": "2025-08-11T07:52:16Z",
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
      "/Categories/Lookups/Electoral",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1658501010000,
    "culture": "en-us",
    "description": "A lookup file between Scottish Parliamentary Constituencies and Scottish Parliamentary Regions in Scotland as at 31st December 2018. (File Size - 32 KB) Field Names - SPC18CD, SPC18 NM, SPR18CD, SPR18NM Field Types - Text, Text, Text, Text Field Lengths - 9, 42, 9, 21 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/SPC18_SPR18_SC_LU_e885dba76b0f49db83f1949db267a660/FeatureServer",
    "extent": [
      [
        -7.9,
        54.4
      ],
      [
        -0.4,
        60.9
      ]
    ],
    "id": "bf0ea2f49afa4553bffef9985ecabac0",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898736000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Electoral Lookup",
    "spatialReference": null,
    "tags": [
      "Lookup",
      "Electoral Lookups",
      "Scottish Parliamentary Constituency to Scottish Parliamentary Region Lookup",
      "SPC",
      "Scottish Parliamentary Constituencies",
      "SPR",
      "Scottish Parliamentary Regions",
      "2018",
      "Scotland",
      "DEC_2018",
      "LUP_ELE",
      "LUP_SPC_SPR"
    ],
    "title": "Scottish Parliamentary Constituencies to SPR (December 2018) Lookup in SC",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "source-bdacbe4634df4fd08a896cdbf3c5a9e8",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/SPC18_SPR18_SC_LU_e885dba76b0f49db83f1949db267a660/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Scottish Parliamentary Constituencies to SPR (December 2018) Lookup in SC

A lookup file between Scottish Parliamentary Constituencies and Scottish Parliamentary Regions in Scotland as at 31st December 2018. (File Size - 32 KB) Field Names - SPC18CD, SPC18 NM, SPR18CD, SPR18NM Field Types - Text, Text, Text, Text Field Lengths - 9, 42, 9, 21 REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/SPC18_SPR18_SC_LU_e885dba76b0f49db83f1949db267a660/FeatureServer

Native identifier: `bf0ea2f49afa4553bffef9985ecabac0`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/bf0ea2f49afa4553bffef9985ecabac0)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
