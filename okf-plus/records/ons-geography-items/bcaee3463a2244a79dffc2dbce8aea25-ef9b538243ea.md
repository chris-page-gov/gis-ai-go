---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/bcaee3463a2244a79dffc2dbce8aea25",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Enterprise Partnerships (April 2020) Boundaries EN BFC",
  "description": "This file contains the digital vector boundaries for Local Enterprise Partnerships in England, as at April 2020. The BFC boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_(April_2020)_FRCB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Enterprise_Partnerships_April_2020_Full_Resolution_Clipped_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_April_2020_FRCB_EN_2022/FeatureServer",
  "nativeIdentifier": "bcaee3463a2244a79dffc2dbce8aea25",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/bcaee3463a2244a79dffc2dbce8aea25",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Local Enterprise Partnerships",
    "LEP",
    "2020",
    "Other Boundaries",
    "England",
    "WMS",
    "WFS",
    "BDY_OTH",
    "BDY_LEP",
    "APR_2020",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3601&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:13.722378Z",
      "responseSha256": "22d6cb0212897a984182c010c968858dee0425d893881af65417780e39bf4f9e",
      "sourcePointer": "/results/61",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3661",
      "normalisedRecordSha256": "a129e3c2710d5ea6c14aa92dd0b5f6d13f2a6b7d460677570bed750b50039419",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/bcaee3463a2244a79dffc2dbce8aea25"
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
    "metadataModified": "2025-08-11T08:09:22Z",
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
    "created": 1664876526000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Local Enterprise Partnerships in England, as at April 2020. The BFC boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_(April_2020)_FRCB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Enterprise_Partnerships_April_2020_Full_Resolution_Clipped_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_April_2020_FRCB_EN_2022/FeatureServer",
    "extent": [
      [
        -7.052770538728189,
        49.86401714599724
      ],
      [
        2.073860703153312,
        55.811090035388176
      ]
    ],
    "id": "bcaee3463a2244a79dffc2dbce8aea25",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899762000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Local Enterprise Partnerships",
      "LEP",
      "2020",
      "Other Boundaries",
      "England",
      "WMS",
      "WFS",
      "BDY_OTH",
      "BDY_LEP",
      "APR_2020"
    ],
    "title": "Local Enterprise Partnerships (April 2020) Boundaries EN BFC",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Enterprise_Partnerships_April_2020_Full_Resolution_Clipped_Boundaries_EN/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Enterprise Partnerships (April 2020) Boundaries EN BFC

This file contains the digital vector boundaries for Local Enterprise Partnerships in England, as at April 2020. The BFC boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_(April_2020)_FRCB_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Enterprise_Partnerships_April_2020_Full_Resolution_Clipped_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LEP_April_2020_FRCB_EN_2022/FeatureServer

Native identifier: `bcaee3463a2244a79dffc2dbce8aea25`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/bcaee3463a2244a79dffc2dbce8aea25)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
