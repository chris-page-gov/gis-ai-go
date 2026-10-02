---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/e489d4e5fe9f4f9caa6af161da5442af",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Westminster Parliamentary Constituencies (July 2024) Boundaries UK BFE",
  "description": "This file contains the digital vector boundaries for Westminster Parliamentary Constituencies, in the United Kingdom, as at 4th July 2024. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/MapServer",
  "nativeIdentifier": "e489d4e5fe9f4f9caa6af161da5442af",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/e489d4e5fe9f4f9caa6af161da5442af",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Electoral Boundaries",
    "BDY_ELE",
    "Westminster Parliamentary Constituencies",
    "BDY_PCON",
    "PCON",
    "United Kingdom",
    "UK",
    "July_2024",
    "July_2024_PCON_Boundaries",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=5501&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:36.362811Z",
      "responseSha256": "3e2adb565131481b475d86ebeb8d5631d02cd2edc7ce5761d540cf373325d5d5",
      "sourcePointer": "/results/87",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/5587",
      "normalisedRecordSha256": "e16165bf5d025adf77a9f79c79def6725e3d66d568ae1448d54cf489bf15a2e6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/e489d4e5fe9f4f9caa6af161da5442af"
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
    "metadataModified": "2025-11-11T17:01:04Z",
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
      "/Categories/Boundaries - Electoral/2024",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1717429031000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Westminster Parliamentary Constituencies, in the United Kingdom, as at 4th July 2024. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/MapServer",
    "extent": [
      [
        -9.332068812906007,
        49.81386094505947
      ],
      [
        2.704388182273093,
        60.866186642226886
      ]
    ],
    "id": "e489d4e5fe9f4f9caa6af161da5442af",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' style='color:rgb(0, 97, 155); text-decoration-line:none; font-family:&quot;Avenir Next W01&quot;, &quot;Avenir Next W00&quot;, &quot;Avenir Next&quot;, Avenir, &quot;Helvetica Neue&quot;, sans-serif; font-size:16px;' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1762880464000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Electoral Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Electoral Boundaries",
      "BDY_ELE",
      "Westminster Parliamentary Constituencies",
      "BDY_PCON",
      "PCON",
      "United Kingdom",
      "UK",
      "July_2024",
      "July_2024_PCON_Boundaries"
    ],
    "title": "Westminster Parliamentary Constituencies (July 2024) Boundaries UK BFE",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS API for JavaScript",
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Westminster Parliamentary Constituencies (July 2024) Boundaries UK BFE

This file contains the digital vector boundaries for Westminster Parliamentary Constituencies, in the United Kingdom, as at 4th July 2024. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_July_2024_Boundaries_UK_BFE/MapServer

Native identifier: `e489d4e5fe9f4f9caa6af161da5442af`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/e489d4e5fe9f4f9caa6af161da5442af)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
