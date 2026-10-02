---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/c3b35ea3ec1b41f184fe4fe3c0b2caf4",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Counties and Unitary Authorities (May 2021) Boundaries UK BUC",
  "description": "This file contains the digital vector boundaries for Counties and Unitary Authorities, in the United Kingdom as at May 2021. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/FeatureServer REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/MapServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/WFSServer?service=wfs&request=getcapabilities",
  "nativeIdentifier": "c3b35ea3ec1b41f184fe4fe3c0b2caf4",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/c3b35ea3ec1b41f184fe4fe3c0b2caf4",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Counties and Unitary Authorities",
    "CTYUA",
    "2021",
    "Administrative Boundaries",
    "UK",
    "WFS",
    "WMS",
    "boundaries",
    "Latest_Boundaries",
    "BDY_CTYUA",
    "BDY_ADM",
    "MAY_2021",
    "Cartographic",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:22.921471Z",
      "responseSha256": "194df883aa1e692d8a6ad3c2f7d15e873401310378c6573ba3a0a77f0f76b5ee",
      "sourcePointer": "/results/65",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4465",
      "normalisedRecordSha256": "0d49b158fa509503d6a1d35f6e81f6b23af00b64d0dcef6d2772a08feb73995c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/c3b35ea3ec1b41f184fe4fe3c0b2caf4"
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
    "metadataModified": "2025-08-11T08:14:41Z",
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
    "created": 1674471433000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Counties and Unitary Authorities, in the United Kingdom as at May 2021. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/FeatureServer REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/MapServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/WFSServer?service=wfs&request=getcapabilities",
    "extent": [
      [
        -9.328623905709584,
        49.829262095770254
      ],
      [
        2.6957969832202315,
        60.85098138550182
      ]
    ],
    "id": "c3b35ea3ec1b41f184fe4fe3c0b2caf4",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900081000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Counties and Unitary Authorities",
      "CTYUA",
      "2021",
      "Administrative Boundaries",
      "UK",
      "WFS",
      "WMS",
      "boundaries",
      "Latest_Boundaries",
      "BDY_CTYUA",
      "BDY_ADM",
      "MAY_2021",
      "Cartographic"
    ],
    "title": "Counties and Unitary Authorities (May 2021) Boundaries UK BUC",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Counties and Unitary Authorities (May 2021) Boundaries UK BUC

This file contains the digital vector boundaries for Counties and Unitary Authorities, in the United Kingdom as at May 2021. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/FeatureServer REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/MapServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_May_2021_UK_BUC_2022/WFSServer?service=wfs&request=getcapabilities

Native identifier: `c3b35ea3ec1b41f184fe4fe3c0b2caf4`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/c3b35ea3ec1b41f184fe4fe3c0b2caf4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
