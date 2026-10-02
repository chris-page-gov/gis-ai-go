---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/2021e4dacf884ff0bfdba2944d2eb580",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Health Boards (December 2023) Boundaries WA BFE",
  "description": "This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2023. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_December_2023_WA_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2023_WA_BFE/WFSServer?service=wfs&request=getcapabilities",
  "nativeIdentifier": "2021e4dacf884ff0bfdba2944d2eb580",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/2021e4dacf884ff0bfdba2944d2eb580",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Health Boundaries",
    "BDY_HLTH",
    "Local Health Boards",
    "BDY_LHB",
    "DEC_2023",
    "2023",
    "Wales",
    "WA",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=5301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:33.950580Z",
      "responseSha256": "79acbc43d1206626ded6a42a23c77fdbaa4487807d066c5932fb63052caf5618",
      "sourcePointer": "/results/74",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/5374",
      "normalisedRecordSha256": "4f930fd153b80e0e261a826191a57f7598ac9ea9cec22e2b28aa2174965e0289",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/2021e4dacf884ff0bfdba2944d2eb580"
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
    "metadataModified": "2025-08-11T08:20:30Z",
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
      "/Categories/Boundaries - Health/2023",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1708612654000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2023. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_December_2023_WA_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2023_WA_BFE/WFSServer?service=wfs&request=getcapabilities",
    "extent": [
      [
        -5.812370027016079,
        51.32289451486255
      ],
      [
        -2.643521992146085,
        53.45880541951222
      ]
    ],
    "id": "2021e4dacf884ff0bfdba2944d2eb580",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900430000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Health Boundaries",
      "BDY_HLTH",
      "Local Health Boards",
      "BDY_LHB",
      "DEC_2023",
      "2023",
      "Wales",
      "WA"
    ],
    "title": "Local Health Boards (December 2023) Boundaries WA BFE",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2023_WA_BFE/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Health Boards (December 2023) Boundaries WA BFE

This file contains the digital vector boundaries for Local Health Boards in Wales, as at December 2023. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Health_Boards_December_2023_WA_BFE/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Local_Health_Boards_December_2023_WA_BFE/WFSServer?service=wfs&request=getcapabilities

Native identifier: `2021e4dacf884ff0bfdba2944d2eb580`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/2021e4dacf884ff0bfdba2944d2eb580)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
