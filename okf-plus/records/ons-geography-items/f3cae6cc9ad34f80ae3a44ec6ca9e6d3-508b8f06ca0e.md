---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/f3cae6cc9ad34f80ae3a44ec6ca9e6d3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Counties (May 2023) Boundaries EN BFC",
  "description": "This file contains the digital vector boundaries for Counties, in England, as at May 2023. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_May_2023_Boundaries_EN_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/MapServer",
  "nativeIdentifier": "f3cae6cc9ad34f80ae3a44ec6ca9e6d3",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/f3cae6cc9ad34f80ae3a44ec6ca9e6d3",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Administrative Boundaries",
    "BDY_ADM",
    "Counties",
    "BDY_CTY",
    "2023",
    "England",
    "EN",
    "WFS",
    "WMS",
    "May_2023",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4701&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:26.670662Z",
      "responseSha256": "4a85ccefdebb47c9aaba4cf753c1869af7cd79c224f9d6d101fea4ef0a1e6556",
      "sourcePointer": "/results/91",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4791",
      "normalisedRecordSha256": "27210e049af2c270899d4013a62c5ed290496e11fc8fd5b73987c05eb6ff19ba",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/f3cae6cc9ad34f80ae3a44ec6ca9e6d3"
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
    "metadataModified": "2025-08-11T08:16:53Z",
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
      "/Categories/Boundaries - Administrative/2023",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1683885364000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Counties, in England, as at May 2023. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_May_2023_Boundaries_EN_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/MapServer",
    "extent": [
      [
        -6,
        49.9
      ],
      [
        2,
        56
      ]
    ],
    "id": "f3cae6cc9ad34f80ae3a44ec6ca9e6d3",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900213000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Administrative Boundaries",
      "BDY_ADM",
      "Counties",
      "BDY_CTY",
      "2023",
      "England",
      "EN",
      "WFS",
      "WMS",
      "May_2023"
    ],
    "title": "Counties (May 2023) Boundaries EN BFC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Counties (May 2023) Boundaries EN BFC

This file contains the digital vector boundaries for Counties, in England, as at May 2023. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_May_2023_Boundaries_EN_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_May_2023_Boundaries_EN_BFC/MapServer

Native identifier: `f3cae6cc9ad34f80ae3a44ec6ca9e6d3`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/f3cae6cc9ad34f80ae3a44ec6ca9e6d3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
