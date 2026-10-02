---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/a2c204fedefe4120ac93f062c647bdcb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Wards (December 2022) Boundaries UK BFC",
  "description": "This file contains the digital vector boundaries for Wards in United Kingdom as at December 2022. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_December_2022_Boundaries_UK_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/MapServer",
  "nativeIdentifier": "a2c204fedefe4120ac93f062c647bdcb",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/a2c204fedefe4120ac93f062c647bdcb",
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
    "Wards",
    "BDY_WD",
    "United Kingdom",
    "UK",
    "2022",
    "DEC_2022",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4201&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:20.565395Z",
      "responseSha256": "efdc97178629b17b16dd067eee4d93d4bdee5b24c48d5048ec1c4371adac5ef1",
      "sourcePointer": "/results/52",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4252",
      "normalisedRecordSha256": "153c27b82ba7f434798d2b57b28815bfdd59af50b2d03a48dcafa579d5c50815",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/a2c204fedefe4120ac93f062c647bdcb"
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
    "metadataModified": "2025-08-11T08:13:19Z",
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
    "created": 1669299745000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Wards in United Kingdom as at December 2022. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_December_2022_Boundaries_UK_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/MapServer",
    "extent": [
      [
        -8.7,
        48.3
      ],
      [
        2.2,
        61
      ]
    ],
    "id": "a2c204fedefe4120ac93f062c647bdcb",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899999000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Administrative Boundaries",
      "BDY_ADM",
      "Wards",
      "BDY_WD",
      "United Kingdom",
      "UK",
      "2022",
      "DEC_2022"
    ],
    "title": "Wards (December 2022) Boundaries UK BFC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Wards (December 2022) Boundaries UK BFC

This file contains the digital vector boundaries for Wards in United Kingdom as at December 2022. The boundaries available are: (BFC) Full resolution - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Wards_December_2022_Boundaries_UK_BFC/WFSServer?service=wfs&request=getcapabilities REST URL of Map Server – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Wards_December_2022_Boundaries_UK_BFC/MapServer

Native identifier: `a2c204fedefe4120ac93f062c647bdcb`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/a2c204fedefe4120ac93f062c647bdcb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
