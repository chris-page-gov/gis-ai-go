---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/eb1b9adc301e4e479c73abbda7f39edc",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Counties (December 2020) Boundaries EN BFE",
  "description": "This file contains the digital vector boundaries for Counties, in England as at December 2020. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(Dec_2020)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_Dec_2020_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_Dec_2020_EN_BFE_2022/FeatureServer",
  "nativeIdentifier": "eb1b9adc301e4e479c73abbda7f39edc",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/eb1b9adc301e4e479c73abbda7f39edc",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "['Boundaries'",
    "'boundaries'",
    "'Latest_Boundaries'",
    "'BDY_CTY'",
    "'Counties'",
    "'BDY_ADM'",
    "'DEC_2020'",
    "'2020'",
    "'England'",
    "'Administrative",
    "Boundaries']",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:21.673184Z",
      "responseSha256": "80e86e21c7c51b06c639bdc8d9188e01eb31c3ca8a2c5ffcd54c6d13c0ad9c2d",
      "sourcePointer": "/results/5",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4305",
      "normalisedRecordSha256": "f829a95a59a24cb31f5579e874a6bbcdb66882a732874996fd82007f2874b379",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/eb1b9adc301e4e479c73abbda7f39edc"
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
    "metadataModified": "2025-08-11T08:13:40Z",
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
    "categories": [],
    "created": 1669651562000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Counties, in England as at December 2020. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(Dec_2020)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_Dec_2020_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_Dec_2020_EN_BFE_2022/FeatureServer",
    "extent": [
      [
        -4.941078882022872,
        50.158265178278434
      ],
      [
        2.01578103009851,
        55.19093688111541
      ]
    ],
    "id": "eb1b9adc301e4e479c73abbda7f39edc",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900020000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "['Boundaries'",
      "'boundaries'",
      "'Latest_Boundaries'",
      "'BDY_CTY'",
      "'Counties'",
      "'BDY_ADM'",
      "'DEC_2020'",
      "'2020'",
      "'England'",
      "'Administrative",
      "Boundaries']"
    ],
    "title": "Counties (December 2020) Boundaries EN BFE",
    "type": "WFS",
    "typeKeywords": [
      "Data",
      "Metadata",
      "Multilayer",
      "OGC",
      "Service",
      "Web Feature Service",
      "WFS",
      "Hosted Service"
    ],
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_Dec_2020_EN_BFE/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Counties (December 2020) Boundaries EN BFE

This file contains the digital vector boundaries for Counties, in England as at December 2020. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(Dec_2020)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_Dec_2020_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_Dec_2020_EN_BFE_2022/FeatureServer

Native identifier: `eb1b9adc301e4e479c73abbda7f39edc`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/eb1b9adc301e4e479c73abbda7f39edc)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
