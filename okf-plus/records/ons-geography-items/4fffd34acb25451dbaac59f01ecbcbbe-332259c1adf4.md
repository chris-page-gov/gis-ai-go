---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/4fffd34acb25451dbaac59f01ecbcbbe",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Wards (December 2025) Boundaries UK BSC",
  "description": "This file contains the digital vector boundaries for Wards, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/WD_DEC_2025_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_(December_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://vectortileservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_(December_2025)_Boundaries_UK_BSC/VectorTileServer",
  "nativeIdentifier": "4fffd34acb25451dbaac59f01ecbcbbe",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/4fffd34acb25451dbaac59f01ecbcbbe",
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
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:45.613584Z",
      "responseSha256": "86ba1d0827620b73f335037b268218dfcc2857fe8d5d267ff9e786b507c5de21",
      "sourcePointer": "/results/10",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6310",
      "normalisedRecordSha256": "5c48fd5fe85cc4a5533ac05a51b0a24f894e0ce29fa365fd0403cfb73532c279",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/4fffd34acb25451dbaac59f01ecbcbbe"
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
    "metadataModified": "2025-12-18T09:00:08Z",
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
      "/Categories/Boundaries - Administrative",
      "/Categories/LATEST",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1766048353000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Wards, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/WD_DEC_2025_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_(December_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://vectortileservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_(December_2025)_Boundaries_UK_BSC/VectorTileServer",
    "extent": [
      [
        -9.33206961328049,
        49.829262095770254
      ],
      [
        2.6980191058442595,
        60.86618661955783
      ]
    ],
    "id": "4fffd34acb25451dbaac59f01ecbcbbe",
    "licenseInfo": "<p><a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.ons.gov.uk/methodology/geography/licences\">https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1766048408000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries"
    ],
    "title": "Wards (December 2025) Boundaries UK BSC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_(December_2025)_Boundaries_UK_BSC/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Wards (December 2025) Boundaries UK BSC

This file contains the digital vector boundaries for Wards, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/WD_DEC_2025_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_(December_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://vectortileservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_(December_2025)_Boundaries_UK_BSC/VectorTileServer

Native identifier: `4fffd34acb25451dbaac59f01ecbcbbe`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/4fffd34acb25451dbaac59f01ecbcbbe)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
