---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/1279edb096ed441ba3d4fc404e3a4eac",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NHS England (Regions) (April 2018) Boundaries EN BFE",
  "description": "This file contains the digital vector boundaries for NHS England Regions in England, as at 1 April 2018. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_(April_2018)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_England_Regions_April_2018_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_April_2018_EN_BFE_2022/FeatureServer",
  "nativeIdentifier": "1279edb096ed441ba3d4fc404e3a4eac",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/1279edb096ed441ba3d4fc404e3a4eac",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "NHS England Regions",
    "NHSER",
    "2018",
    "Health Boundaries",
    "England",
    "WFS",
    "WMS",
    "boundaries",
    "BDY_NHSER",
    "APR_2018",
    "BDY_HLT",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2501&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:00.730195Z",
      "responseSha256": "83b4c1bb9b95fb1616099886fd26cada31970367451bdb227921df096e233fe3",
      "sourcePointer": "/results/15",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2515",
      "normalisedRecordSha256": "ea870ae17ee827f96e466b13cb470dce90ebdc3f66e432ff1a1307ac509ee38a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/1279edb096ed441ba3d4fc404e3a4eac"
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
    "metadataModified": "2025-08-11T08:02:01Z",
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
    "created": 1664391884000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for NHS England Regions in England, as at 1 April 2018. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_(April_2018)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_England_Regions_April_2018_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_April_2018_EN_BFE_2022/FeatureServer",
    "extent": [
      [
        -7.053294424025302,
        49.86396356208084
      ],
      [
        2.079245664803893,
        55.811660973646546
      ]
    ],
    "id": "1279edb096ed441ba3d4fc404e3a4eac",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899321000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Health Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "NHS England Regions",
      "NHSER",
      "2018",
      "Health Boundaries",
      "England",
      "WFS",
      "WMS",
      "boundaries",
      "BDY_NHSER",
      "APR_2018",
      "BDY_HLT"
    ],
    "title": "NHS England (Regions) (April 2018) Boundaries EN BFE",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_April_2018_EN_BFE_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# NHS England (Regions) (April 2018) Boundaries EN BFE

This file contains the digital vector boundaries for NHS England Regions in England, as at 1 April 2018. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_(April_2018)_EN_BFE/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_England_Regions_April_2018_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_England_Regions_April_2018_EN_BFE_2022/FeatureServer

Native identifier: `1279edb096ed441ba3d4fc404e3a4eac`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/1279edb096ed441ba3d4fc404e3a4eac)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
