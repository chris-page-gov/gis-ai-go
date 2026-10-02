---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/c67c27d16a2e4f05aafac1bffe6f92fa",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NUTS, level 3 (January 2018) Boundaries UK BUC",
  "description": "This file contains the digital vector boundaries for Nomenclature of Territorial Units for Statistics Level 3, in the United Kingdom, as at January 2018. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_(Jan_2018)_UGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NUTS3_Jan_2018_Ultra_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_Jan_2018_UGCB_in_the_UK_2022/FeatureServer",
  "nativeIdentifier": "c67c27d16a2e4f05aafac1bffe6f92fa",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/c67c27d16a2e4f05aafac1bffe6f92fa",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Nomenclature of Territorial Units for Statistics Level 3",
    "NUTS3",
    "2018",
    "Eurostat Boundaries",
    "United Kingdom",
    "WFS",
    "WMS",
    "NUTS 3 Boundaries",
    "NUTS3_Boundaries_2018",
    "Latest_Boundaries",
    "boundaries",
    "BDY_NUTS3",
    "JAN_2018",
    "BDY_EUR",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2801&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:03.989429Z",
      "responseSha256": "437fd7c3ed0f08c55b726d79d847c51e21cb7fda85c67fe372b9332585733feb",
      "sourcePointer": "/results/3",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2803",
      "normalisedRecordSha256": "44b9235608abca41c39f2a45829817472ff91bed6d777b443dcf024c919519a4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/c67c27d16a2e4f05aafac1bffe6f92fa"
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
    "metadataModified": "2025-08-11T08:03:50Z",
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
      "/Categories/Boundaries - OECD_Eurostat/2018",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1664453803000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Nomenclature of Territorial Units for Statistics Level 3, in the United Kingdom, as at January 2018. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_(Jan_2018)_UGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NUTS3_Jan_2018_Ultra_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_Jan_2018_UGCB_in_the_UK_2022/FeatureServer",
    "extent": [
      [
        -9.331218035317935,
        49.82929364151816
      ],
      [
        2.6972741654076593,
        60.86611136658711
      ]
    ],
    "id": "c67c27d16a2e4f05aafac1bffe6f92fa",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899430000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "OECD/Eurostat Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Nomenclature of Territorial Units for Statistics Level 3",
      "NUTS3",
      "2018",
      "Eurostat Boundaries",
      "United Kingdom",
      "WFS",
      "WMS",
      "NUTS 3 Boundaries",
      "NUTS3_Boundaries_2018",
      "Latest_Boundaries",
      "boundaries",
      "BDY_NUTS3",
      "JAN_2018",
      "BDY_EUR"
    ],
    "title": "NUTS, level 3 (January 2018) Boundaries UK BUC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_Jan_2018_UGCB_in_the_UK_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# NUTS, level 3 (January 2018) Boundaries UK BUC

This file contains the digital vector boundaries for Nomenclature of Territorial Units for Statistics Level 3, in the United Kingdom, as at January 2018. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_(Jan_2018)_UGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NUTS3_Jan_2018_Ultra_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NUTS3_Jan_2018_UGCB_in_the_UK_2022/FeatureServer

Native identifier: `c67c27d16a2e4f05aafac1bffe6f92fa`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/c67c27d16a2e4f05aafac1bffe6f92fa)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
