---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/0e4ec1c6efab4b2ca5a695d6afa1b606",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Countries (December 2019) Boundaries GB BUC",
  "description": "This file contains the digital vector boundaries for Countries in Great Britain, as at December 2019. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(Dec_2019)_UGCB_GB/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2019_Ultra_Generalised_Clipped_Boundaries_GB/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_Dec_2019_UGCB_GB_2022/FeatureServer",
  "nativeIdentifier": "0e4ec1c6efab4b2ca5a695d6afa1b606",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/0e4ec1c6efab4b2ca5a695d6afa1b606",
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
    "2019",
    "Administrative Boundaries",
    "Great Britain",
    "WFS",
    "WMS",
    "BDY_ADM",
    "BDY_CTRY",
    "DEC_2019",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2101&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:55.884377Z",
      "responseSha256": "c4e883c6db4a1792c85b50649386974d8e1897756f77d4f04f444a16b9a76165",
      "sourcePointer": "/results/88",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2188",
      "normalisedRecordSha256": "75e102a7468cca5964a13ac3ab9cce5ee18c836469ba18878439b9e1a3822721",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/0e4ec1c6efab4b2ca5a695d6afa1b606"
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
    "metadataModified": "2025-08-11T07:59:54Z",
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
    "created": 1663235087000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Countries in Great Britain, as at December 2019. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(Dec_2019)_UGCB_GB/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2019_Ultra_Generalised_Clipped_Boundaries_GB/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_Dec_2019_UGCB_GB_2022/FeatureServer",
    "extent": [
      [
        -9.226488968046064,
        49.832988355913436
      ],
      [
        2.6959647306576247,
        60.85099593425502
      ]
    ],
    "id": "0e4ec1c6efab4b2ca5a695d6afa1b606",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899194000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Countries",
      "CTRY",
      "2019",
      "Administrative Boundaries",
      "Great Britain",
      "WFS",
      "WMS",
      "BDY_ADM",
      "BDY_CTRY",
      "DEC_2019"
    ],
    "title": "Countries (December 2019) Boundaries GB BUC",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2019_Ultra_Generalised_Clipped_Boundaries_GB/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Countries (December 2019) Boundaries GB BUC

This file contains the digital vector boundaries for Countries in Great Britain, as at December 2019. The BUC boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_(Dec_2019)_UGCB_GB/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Countries_December_2019_Ultra_Generalised_Clipped_Boundaries_GB/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_Dec_2019_UGCB_GB_2022/FeatureServer

Native identifier: `0e4ec1c6efab4b2ca5a695d6afa1b606`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/0e4ec1c6efab4b2ca5a695d6afa1b606)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
