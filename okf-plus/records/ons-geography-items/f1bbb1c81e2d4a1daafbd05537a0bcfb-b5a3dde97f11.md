---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/f1bbb1c81e2d4a1daafbd05537a0bcfb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Countries (December 2017) Boundaries GB BFC",
  "description": "This file contains the digital vector boundaries for Countries in Great Britain, as at 31 December 2017. The boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(December_2017)_FCB_in_Great_Britain/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2017_Full_Clipped_Boundaries_in_Great_Britain/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_December_2017_FCB_in_Great_Britain_2022/FeatureServer",
  "nativeIdentifier": "f1bbb1c81e2d4a1daafbd05537a0bcfb",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/f1bbb1c81e2d4a1daafbd05537a0bcfb",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Countries",
    "CTRY",
    "2017",
    "Administrative Boundaries",
    "Great Britain",
    "WFS",
    "WMS",
    "boundaries",
    "Latest_Boundaries",
    "CTRY_Boundaries",
    "BDY_ADM",
    "BDY_CTRY",
    "DEC_2017",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:47.937342Z",
      "responseSha256": "3cd9cfcb40f1be749ed4690824acc6ecea60f73f22f1cac948785d350c1f67c9",
      "sourcePointer": "/results/86",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1486",
      "normalisedRecordSha256": "8e11e3755dd21064fb9ca329f2056eb3974b404db3b44e13389745a5698f7455",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/f1bbb1c81e2d4a1daafbd05537a0bcfb"
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
    "metadataModified": "2025-08-11T07:55:34Z",
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
    "created": 1662482889000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Countries in Great Britain, as at 31 December 2017. The boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(December_2017)_FCB_in_Great_Britain/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2017_Full_Clipped_Boundaries_in_Great_Britain/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_December_2017_FCB_in_Great_Britain_2022/FeatureServer",
    "extent": [
      [
        -9.229867595983485,
        49.817621787807234
      ],
      [
        2.6980081028736893,
        60.866111341119
      ]
    ],
    "id": "f1bbb1c81e2d4a1daafbd05537a0bcfb",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898934000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Countries",
      "CTRY",
      "2017",
      "Administrative Boundaries",
      "Great Britain",
      "WFS",
      "WMS",
      "boundaries",
      "Latest_Boundaries",
      "CTRY_Boundaries",
      "BDY_ADM",
      "BDY_CTRY",
      "DEC_2017"
    ],
    "title": "Countries (December 2017) Boundaries GB BFC",
    "type": "Map Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Map Service",
      "Metadata",
      "Service",
      "WMTS",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(December_2017)_FCB_in_Great_Britain/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Countries (December 2017) Boundaries GB BFC

This file contains the digital vector boundaries for Countries in Great Britain, as at 31 December 2017. The boundaries are full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(December_2017)_FCB_in_Great_Britain/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2017_Full_Clipped_Boundaries_in_Great_Britain/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_December_2017_FCB_in_Great_Britain_2022/FeatureServer

Native identifier: `f1bbb1c81e2d4a1daafbd05537a0bcfb`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/f1bbb1c81e2d4a1daafbd05537a0bcfb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
