---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/117fd89abfe348fd8ffecb2e353dfde8",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Authority Districts (December 2025) Boundaries UK BSC",
  "description": "This file contains the digital vector boundaries for Local Authority Districts, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_DEC_2025_Boundaries_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/MapServer",
  "nativeIdentifier": "117fd89abfe348fd8ffecb2e353dfde8",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/117fd89abfe348fd8ffecb2e353dfde8",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "LADs",
    "Local Authority Districts",
    "Boundaries",
    "Administrative Boundaries",
    "BDY_ADM",
    "BDY_LAD",
    "DEC_2025",
    "2025",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:46.927746Z",
      "responseSha256": "c0585c8bf9311083c4d1d11cbda9681327cd1a54fa645fc5e8604ac2d0e47db0",
      "sourcePointer": "/results/41",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6441",
      "normalisedRecordSha256": "bd9cfc7bb127b542e0e1322a1d34d7b0d38e623dacc9aaf532949adecec92954",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/117fd89abfe348fd8ffecb2e353dfde8"
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
    "metadataModified": "2026-04-29T08:33:08Z",
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
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1776939811000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Local Authority Districts, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_DEC_2025_Boundaries_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/MapServer",
    "extent": [
      [
        -9.332069613280487,
        49.829262095770254
      ],
      [
        2.6980191058442555,
        60.866186619557816
      ]
    ],
    "id": "117fd89abfe348fd8ffecb2e353dfde8",
    "licenseInfo": "<p><a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.ons.gov.uk/methodology/geography/licences\">https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1777451588000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "LADs",
      "Local Authority Districts",
      "Boundaries",
      "Administrative Boundaries",
      "BDY_ADM",
      "BDY_LAD",
      "DEC_2025",
      "2025"
    ],
    "title": "Local Authority Districts (December 2025) Boundaries UK BSC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_DEC_2025_Boundaries_UK_BSC/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Authority Districts (December 2025) Boundaries UK BSC

This file contains the digital vector boundaries for Local Authority Districts, in the United Kingdom, as at December 2025. The boundaries available are: (BSC) Super Generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_DEC_2025_Boundaries_UK_BSC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_(DEC_2025)_Boundaries_UK_BSC/MapServer

Native identifier: `117fd89abfe348fd8ffecb2e353dfde8`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/117fd89abfe348fd8ffecb2e353dfde8)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
