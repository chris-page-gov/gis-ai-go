---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/4cf1df0e611c48718a8be59cbbd49b48",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Scottish Parliamentary Constituencies (May 2021) Boundaries SC BFE",
  "description": "This file contains the digital vector boundaries for Scottish Parliamentary Constituencies in Scotland as at May 2021. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_(May_2021)_Boundaries_SC_BFE/MapServer",
  "nativeIdentifier": "4cf1df0e611c48718a8be59cbbd49b48",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/4cf1df0e611c48718a8be59cbbd49b48",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4501&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:24.307945Z",
      "responseSha256": "9a3a58624cfcf55a0519dc56f73d41adfad9f098a32bb9eabf6f31b623150bff",
      "sourcePointer": "/results/59",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4559",
      "normalisedRecordSha256": "e05835ce76652a141b09008afa1c45c2f60a48a403c2b140050d191f3c407ca5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/4cf1df0e611c48718a8be59cbbd49b48"
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
    "metadataModified": "2025-08-11T08:15:20Z",
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
    "created": 1676455652000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Scottish Parliamentary Constituencies in Scotland as at May 2021. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_(May_2021)_Boundaries_SC_BFE/MapServer",
    "extent": [
      [
        -9.229884423869661,
        54.51335447335799
      ],
      [
        -0.7071874063845653,
        60.866185278429874
      ]
    ],
    "id": "4cf1df0e611c48718a8be59cbbd49b48",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900120000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries"
    ],
    "title": "Scottish Parliamentary Constituencies (May 2021) Boundaries SC BFE",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_(May_2021)_Boundaries_SC_BFE/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Scottish Parliamentary Constituencies (May 2021) Boundaries SC BFE

This file contains the digital vector boundaries for Scottish Parliamentary Constituencies in Scotland as at May 2021. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Scottish_Parliamentary_Constituencies_May_2021_Boundaries_SC_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Scottish_Parliamentary_Constituencies_(May_2021)_Boundaries_SC_BFE/MapServer

Native identifier: `4cf1df0e611c48718a8be59cbbd49b48`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/4cf1df0e611c48718a8be59cbbd49b48)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
