---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/f81df4a1d06e45a0a7fbda219df82cb3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "National Parks (December 2014) Boundaries GB BFE",
  "description": "This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2014. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2014_GB_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/MapServer",
  "nativeIdentifier": "f81df4a1d06e45a0a7fbda219df82cb3",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/f81df4a1d06e45a0a7fbda219df82cb3",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Other Boundaries",
    "BDY_OTH",
    "National Parks",
    "BDY_NPARK",
    "Great Britain",
    "GB",
    "2014",
    "Dec_2014",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4601&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:25.414775Z",
      "responseSha256": "5220715eb22e908dfacb1a83854a6490d1ea2150c3fe0f8deba12ca50095d719",
      "sourcePointer": "/results/21",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4621",
      "normalisedRecordSha256": "dd9e3fc5a9a8305eb02bdad2693002d95b707eaf3e4e9a7b65f83287483d99a3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/f81df4a1d06e45a0a7fbda219df82cb3"
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
    "metadataModified": "2025-08-11T08:15:45Z",
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
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1677757946000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2014. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2014_GB_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/MapServer",
    "extent": [
      [
        -5.839337407642381,
        50.352495005537364
      ],
      [
        2.196008061950274,
        57.420392493728585
      ]
    ],
    "id": "f81df4a1d06e45a0a7fbda219df82cb3",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900145000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Other Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Other Boundaries",
      "BDY_OTH",
      "National Parks",
      "BDY_NPARK",
      "Great Britain",
      "GB",
      "2014",
      "Dec_2014"
    ],
    "title": "National Parks (December 2014) Boundaries GB BFE",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# National Parks (December 2014) Boundaries GB BFE

This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2014. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2014_GB_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_December_2014_GB_BFE/MapServer

Native identifier: `f81df4a1d06e45a0a7fbda219df82cb3`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/f81df4a1d06e45a0a7fbda219df82cb3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
