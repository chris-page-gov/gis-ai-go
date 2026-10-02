---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/3b5d1af5cbc449ceb28859beadee845c",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "London Assembly Constituencies (December 2018) Boundaries EN BUC",
  "description": "This file contains the digital vector boundaries for London Assembly Constituencies, in England, as at 31 December 2018. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_(Dec_2018)_Ultra_Generalised_Boundaries_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/London_Assembly_Constituencies_December_2018_Ultra_Generalised_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_Dec_2018_Ultra_Generalised_Boundaries_EN_2022/FeatureServer",
  "nativeIdentifier": "3b5d1af5cbc449ceb28859beadee845c",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/3b5d1af5cbc449ceb28859beadee845c",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "London Assembly Constituencies",
    "LAC",
    "2018",
    "Other Boundaries",
    "England",
    "WFS",
    "WMS",
    "BDY_OTH",
    "BDY_LAC",
    "DEC_2018",
    "Cartographic",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:10.452643Z",
      "responseSha256": "55779753a3c9af57f9514affc88d7d6774e128e0e9789ecab5f8a2669e30c2bf",
      "sourcePointer": "/results/78",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3378",
      "normalisedRecordSha256": "bf5daf97cc2d88c926fbcbca7410c8a454cda382b377a58abb3a267999e1d854",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/3b5d1af5cbc449ceb28859beadee845c"
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
    "metadataModified": "2025-08-11T08:07:33Z",
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
      "/Categories/Boundaries - Electoral/2018",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1664498690000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for London Assembly Constituencies, in England, as at 31 December 2018. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_(Dec_2018)_Ultra_Generalised_Boundaries_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/London_Assembly_Constituencies_December_2018_Ultra_Generalised_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_Dec_2018_Ultra_Generalised_Boundaries_EN_2022/FeatureServer",
    "extent": [
      [
        -0.5154300400720855,
        51.27878158976894
      ],
      [
        0.34138640097467376,
        51.69760123418787
      ]
    ],
    "id": "3b5d1af5cbc449ceb28859beadee845c",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899653000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Electoral Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "London Assembly Constituencies",
      "LAC",
      "2018",
      "Other Boundaries",
      "England",
      "WFS",
      "WMS",
      "BDY_OTH",
      "BDY_LAC",
      "DEC_2018",
      "Cartographic"
    ],
    "title": "London Assembly Constituencies (December 2018) Boundaries EN BUC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_Dec_2018_Ultra_Generalised_Boundaries_EN_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# London Assembly Constituencies (December 2018) Boundaries EN BUC

This file contains the digital vector boundaries for London Assembly Constituencies, in England, as at 31 December 2018. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_(Dec_2018)_Ultra_Generalised_Boundaries_EN/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/London_Assembly_Constituencies_December_2018_Ultra_Generalised_Boundaries_EN/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/London_Assembly_Constituencies_Dec_2018_Ultra_Generalised_Boundaries_EN_2022/FeatureServer

Native identifier: `3b5d1af5cbc449ceb28859beadee845c`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/3b5d1af5cbc449ceb28859beadee845c)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
