---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/db64e5f5fc2a4abebde0f942f2c93f5c",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Health Boards (December 2016) Boundaries WA BFE",
  "description": "This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_(Dec_2016)_FEB_in_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2016_Full_Extent_Boundaries_in_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_Dec_2016_FEB_in_Wales_2022/FeatureServer",
  "nativeIdentifier": "db64e5f5fc2a4abebde0f942f2c93f5c",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/db64e5f5fc2a4abebde0f942f2c93f5c",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Local Health Boards",
    "LHB",
    "2016",
    "Health Boundaries",
    "Wales",
    "WFS",
    "WMS",
    "boundaries",
    "BDY_HLT",
    "BDY_LHB",
    "DEC_2016",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:59.481120Z",
      "responseSha256": "d432ca376905999f72917b543ee9fa05bb0c6b69eefe5a4f56c832f77c64768e",
      "sourcePointer": "/results/21",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2421",
      "normalisedRecordSha256": "d86a34c1c6d4a79957c1945f5a4b25a5f97bb33693eb9d238ff21b968c93834d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/db64e5f5fc2a4abebde0f942f2c93f5c"
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
    "metadataModified": "2025-08-11T08:01:25Z",
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
    "created": 1664388413000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_(Dec_2016)_FEB_in_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2016_Full_Extent_Boundaries_in_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_Dec_2016_FEB_in_Wales_2022/FeatureServer",
    "extent": [
      [
        -5.812370026855507,
        51.322894513965096
      ],
      [
        -2.6435219921334774,
        53.458805417714665
      ]
    ],
    "id": "db64e5f5fc2a4abebde0f942f2c93f5c",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899285000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Local Health Boards",
      "LHB",
      "2016",
      "Health Boundaries",
      "Wales",
      "WFS",
      "WMS",
      "boundaries",
      "BDY_HLT",
      "BDY_LHB",
      "DEC_2016"
    ],
    "title": "Local Health Boards (December 2016) Boundaries WA BFE",
    "type": "Map Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Map Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "WMTS",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_(Dec_2016)_FEB_in_Wales/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Health Boards (December 2016) Boundaries WA BFE

This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_(Dec_2016)_FEB_in_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2016_Full_Extent_Boundaries_in_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_Dec_2016_FEB_in_Wales_2022/FeatureServer

Native identifier: `db64e5f5fc2a4abebde0f942f2c93f5c`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/db64e5f5fc2a4abebde0f942f2c93f5c)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
