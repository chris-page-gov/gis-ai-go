---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/cca6931ac5e54dcfba12ebbee4d9ae60",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Regions (December 2020) Boundaries EN BUC",
  "description": "This file contains the digital vector boundaries for the Regions, in England as at December 2020. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_(Dec_2020)_EN_BUC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Regions_Dec_2020_EN_BUC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_Dec_2020_EN_BUC_2022/FeatureServer",
  "nativeIdentifier": "cca6931ac5e54dcfba12ebbee4d9ae60",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/cca6931ac5e54dcfba12ebbee4d9ae60",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "boundaries",
    "Latest_Boundaries",
    "BDY_RGN",
    "BDY_ADM",
    "Administrative Boundaries",
    "Regions",
    "2020",
    "DEC_2020",
    "England",
    "Cartographic",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:21.673184Z",
      "responseSha256": "80e86e21c7c51b06c639bdc8d9188e01eb31c3ca8a2c5ffcd54c6d13c0ad9c2d",
      "sourcePointer": "/results/18",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4318",
      "normalisedRecordSha256": "97d15ee22ef8496dcf5ac3eceb0994b0c58a388af4a3762cc93a637c66cf221f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/cca6931ac5e54dcfba12ebbee4d9ae60"
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
    "metadataModified": "2025-08-11T08:13:44Z",
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
    "created": 1669655317000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for the Regions, in England as at December 2020. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_(Dec_2020)_EN_BUC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Regions_Dec_2020_EN_BUC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_Dec_2020_EN_BUC_2022/FeatureServer",
    "extent": [
      [
        -6.979041470636608,
        49.88185309734096
      ],
      [
        2.0737283259868806,
        55.811200283712594
      ]
    ],
    "id": "cca6931ac5e54dcfba12ebbee4d9ae60",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900024000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "boundaries",
      "Latest_Boundaries",
      "BDY_RGN",
      "BDY_ADM",
      "Administrative Boundaries",
      "Regions",
      "2020",
      "DEC_2020",
      "England",
      "Cartographic"
    ],
    "title": "Regions (December 2020) Boundaries EN BUC",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_Dec_2020_EN_BUC_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Regions (December 2020) Boundaries EN BUC

This file contains the digital vector boundaries for the Regions, in England as at December 2020. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_(Dec_2020)_EN_BUC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Regions_Dec_2020_EN_BUC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Regions_Dec_2020_EN_BUC_2022/FeatureServer

Native identifier: `cca6931ac5e54dcfba12ebbee4d9ae60`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/cca6931ac5e54dcfba12ebbee4d9ae60)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
