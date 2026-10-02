---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/8f9adc44c4b24c1bb806ba59bafd7e6f",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Westminster Parliamentary Constituencies (December 2021) Boundaries UK BGC",
  "description": "This file contains the digital vector boundaries for Westminster Parliamentary Constituencies in United Kingdom as at December 2021. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_(Dec_2021)_UK_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC_2022/FeatureServer",
  "nativeIdentifier": "8f9adc44c4b24c1bb806ba59bafd7e6f",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/8f9adc44c4b24c1bb806ba59bafd7e6f",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Westminster Parliamentary Constituencies",
    "PCON",
    "2021",
    "Electoral Boundaries",
    "United Kingdom",
    "BDY_PCON",
    "WMS",
    "WFS",
    "DEC_2021",
    "BDY_ELE",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3001&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:06.567855Z",
      "responseSha256": "c5871a4a72ed49389fa9e94d958aa5a6f8cc3f1ba5543ed1064e4788976cea04",
      "sourcePointer": "/results/80",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3080",
      "normalisedRecordSha256": "a62641bd57b3996e5c88daff6d400ba4db5262cd17331b011bc8ebc234bf540c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/8f9adc44c4b24c1bb806ba59bafd7e6f"
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
    "metadataModified": "2025-08-11T08:05:35Z",
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
      "/Categories/Boundaries - Electoral/2021",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1664485992000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Westminster Parliamentary Constituencies in United Kingdom as at December 2021. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_(Dec_2021)_UK_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC_2022/FeatureServer",
    "extent": [
      [
        -9.331242635047623,
        49.81405886624706
      ],
      [
        2.698173798193357,
        60.86611139495808
      ]
    ],
    "id": "8f9adc44c4b24c1bb806ba59bafd7e6f",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899535000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Electoral Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Westminster Parliamentary Constituencies",
      "PCON",
      "2021",
      "Electoral Boundaries",
      "United Kingdom",
      "BDY_PCON",
      "WMS",
      "WFS",
      "DEC_2021",
      "BDY_ELE"
    ],
    "title": "Westminster Parliamentary Constituencies (December 2021) Boundaries UK BGC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Westminster Parliamentary Constituencies (December 2021) Boundaries UK BGC

This file contains the digital vector boundaries for Westminster Parliamentary Constituencies in United Kingdom as at December 2021. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_(Dec_2021)_UK_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Westminster_Parliamentary_Constituencies_Dec_2021_UK_BGC_2022/FeatureServer

Native identifier: `8f9adc44c4b24c1bb806ba59bafd7e6f`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/8f9adc44c4b24c1bb806ba59bafd7e6f)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
