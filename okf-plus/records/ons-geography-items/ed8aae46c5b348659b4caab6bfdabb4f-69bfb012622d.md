---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/ed8aae46c5b348659b4caab6bfdabb4f",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NHS England (Region, Local Office) (April 2019) Boundaries EN BFE",
  "description": "This file contains the digital vector boundaries for NHS Region Local Offices, in England, as at 1st April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_(April_2019)_FEB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_Region_Local_Offices_April_2019_Full_Extent_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_April_2019_FEB_EN_2022/FeatureServer",
  "nativeIdentifier": "ed8aae46c5b348659b4caab6bfdabb4f",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/ed8aae46c5b348659b4caab6bfdabb4f",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "NHS England Region Local Office",
    "NHSRLO",
    "2019",
    "Health Boundaries",
    "England",
    "WFS",
    "WMS",
    "BDY_HLT",
    "APR_2019",
    "BDY_NHSRLO",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2501&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:00.730195Z",
      "responseSha256": "83b4c1bb9b95fb1616099886fd26cada31970367451bdb227921df096e233fe3",
      "sourcePointer": "/results/44",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2544",
      "normalisedRecordSha256": "210dcdd683e1ca664f038d0b4d1416014a50a0744411167bece50600c3822340",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/ed8aae46c5b348659b4caab6bfdabb4f"
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
    "metadataModified": "2025-11-27T10:58:47Z",
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
    "created": 1664392941000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for NHS Region Local Offices, in England, as at 1st April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_(April_2019)_FEB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_Region_Local_Offices_April_2019_Full_Extent_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_April_2019_FEB_EN_2022/FeatureServer",
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
    "id": "ed8aae46c5b348659b4caab6bfdabb4f",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1764241127000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "NHS England Region Local Office",
      "NHSRLO",
      "2019",
      "Health Boundaries",
      "England",
      "WFS",
      "WMS",
      "BDY_HLT",
      "APR_2019",
      "BDY_NHSRLO"
    ],
    "title": "NHS England (Region, Local Office) (April 2019) Boundaries EN BFE",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_Region_Local_Offices_April_2019_Full_Extent_Boundaries_EN/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# NHS England (Region, Local Office) (April 2019) Boundaries EN BFE

This file contains the digital vector boundaries for NHS Region Local Offices, in England, as at 1st April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_(April_2019)_FEB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHS_Region_Local_Offices_April_2019_Full_Extent_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHS_Region_Local_Offices_April_2019_FEB_EN_2022/FeatureServer

Native identifier: `ed8aae46c5b348659b4caab6bfdabb4f`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/ed8aae46c5b348659b4caab6bfdabb4f)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
