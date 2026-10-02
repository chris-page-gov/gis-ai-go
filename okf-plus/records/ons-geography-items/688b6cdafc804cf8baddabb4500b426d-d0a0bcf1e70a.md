---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/688b6cdafc804cf8baddabb4500b426d",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Combined Authorities (December 2025) Boundaries EN BUC",
  "description": "This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2025. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2025_Boundaries_EN_BUC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/MapServer",
  "nativeIdentifier": "688b6cdafc804cf8baddabb4500b426d",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/688b6cdafc804cf8baddabb4500b426d",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "CAUTH",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:46.927746Z",
      "responseSha256": "c0585c8bf9311083c4d1d11cbda9681327cd1a54fa645fc5e8604ac2d0e47db0",
      "sourcePointer": "/results/61",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6461",
      "normalisedRecordSha256": "a76f56a8d3b19b1e42a4d8caeadc87d858ae630c4d2d33476979c7a12dcceaeb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/688b6cdafc804cf8baddabb4500b426d"
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
    "metadataModified": "2026-04-27T14:31:36Z",
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
    "created": 1777300110000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2025. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2025_Boundaries_EN_BUC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/MapServer",
    "extent": [
      [
        -4.987594070669031,
        50.185402578604794
      ],
      [
        0.7403152794285129,
        55.81118839921194
      ]
    ],
    "id": "688b6cdafc804cf8baddabb4500b426d",
    "licenseInfo": "<p><a target='_blank' href='https://www.ons.gov.uk/methodology/geography/licences' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1777300296000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "CAUTH"
    ],
    "title": "Combined Authorities (December 2025) Boundaries EN BUC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Combined Authorities (December 2025) Boundaries EN BUC

This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2025. The boundaries available are: (BUC) Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2025_Boundaries_EN_BUC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/WFSServer?request=getcapabilities&service=wfs REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2025)_Boundaries_EN_BUC/MapServer

Native identifier: `688b6cdafc804cf8baddabb4500b426d`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/688b6cdafc804cf8baddabb4500b426d)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
