---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/f663be6f48fe44d3b8cefdef121fe9a6",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Combined Authorities (December 2022) Boundaries EN BFE",
  "description": "This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2022_EN_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_December_2022_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2022)_EN_BFE/MapServer",
  "nativeIdentifier": "f663be6f48fe44d3b8cefdef121fe9a6",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/f663be6f48fe44d3b8cefdef121fe9a6",
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
    "Combined Authorities",
    "BDY_CAUTH",
    "England",
    "EN",
    "2022",
    "DEC_2022",
    "WFS",
    "WMS",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4401&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:22.921471Z",
      "responseSha256": "194df883aa1e692d8a6ad3c2f7d15e873401310378c6573ba3a0a77f0f76b5ee",
      "sourcePointer": "/results/70",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4470",
      "normalisedRecordSha256": "296ae3a7543a5476e1167bc634edcf2fd9de0f55118641d6c68323cc88955f1d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/f663be6f48fe44d3b8cefdef121fe9a6"
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
    "metadataModified": "2025-08-11T08:14:44Z",
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
      "/Categories/Boundaries - Administrative/2022",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1674639249000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2022_EN_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_December_2022_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2022)_EN_BFE/MapServer",
    "extent": [
      [
        -3.3389619783102304,
        51.248215025985
      ],
      [
        0.7403486778745381,
        55.81166453747748
      ]
    ],
    "id": "f663be6f48fe44d3b8cefdef121fe9a6",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900084000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Administrative Boundaries",
      "BDY_ADM",
      "Combined Authorities",
      "BDY_CAUTH",
      "England",
      "EN",
      "2022",
      "DEC_2022",
      "WFS",
      "WMS"
    ],
    "title": "Combined Authorities (December 2022) Boundaries EN BFE",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2022_EN_BFE/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Combined Authorities (December 2022) Boundaries EN BFE

This file contains the digital vector boundaries for Combined Authorities, in England, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_December_2022_EN_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Combined_Authorities_December_2022_EN_BFE/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Combined_Authorities_(December_2022)_EN_BFE/MapServer

Native identifier: `f663be6f48fe44d3b8cefdef121fe9a6`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/f663be6f48fe44d3b8cefdef121fe9a6)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
