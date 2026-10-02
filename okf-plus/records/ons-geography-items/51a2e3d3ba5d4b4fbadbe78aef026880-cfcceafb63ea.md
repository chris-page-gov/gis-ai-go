---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/51a2e3d3ba5d4b4fbadbe78aef026880",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Police Force Areas (December 2024) Boundaries EW BGC",
  "description": "This file contains the digital vector boundaries for Police Force Areas, in England and Wales, as at December 2024. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_Dec_2024_EW_BGC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/MapServer",
  "nativeIdentifier": "51a2e3d3ba5d4b4fbadbe78aef026880",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/51a2e3d3ba5d4b4fbadbe78aef026880",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:45.613584Z",
      "responseSha256": "86ba1d0827620b73f335037b268218dfcc2857fe8d5d267ff9e786b507c5de21",
      "sourcePointer": "/results/72",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6372",
      "normalisedRecordSha256": "3a4251057ba0fcae9ac9fd4a66cc3ea08b7a963037e1c63b82718664369f0e15",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/51a2e3d3ba5d4b4fbadbe78aef026880"
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
    "metadataModified": "2026-01-23T16:18:02Z",
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
      "/Categories/Boundaries - Administrative/2024",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1769184684000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Police Force Areas, in England and Wales, as at December 2024. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_Dec_2024_EW_BGC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/MapServer",
    "extent": [
      [
        -7.05282959503753,
        49.864147119737304
      ],
      [
        2.0738637974415104,
        55.81111975600752
      ]
    ],
    "id": "51a2e3d3ba5d4b4fbadbe78aef026880",
    "licenseInfo": "<p><a target='_blank' href='https://www.ons.gov.uk/methodology/geography/licences' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1769185082000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries"
    ],
    "title": "Police Force Areas (December 2024) Boundaries EW BGC",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Police Force Areas (December 2024) Boundaries EW BGC

This file contains the digital vector boundaries for Police Force Areas, in England and Wales, as at December 2024. The boundaries available are: (BGC) Generalised (20m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_Dec_2024_EW_BGC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Police_Force_Areas_(December_2024)_Boundaries_EW_BGC/MapServer

Native identifier: `51a2e3d3ba5d4b4fbadbe78aef026880`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/51a2e3d3ba5d4b4fbadbe78aef026880)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
