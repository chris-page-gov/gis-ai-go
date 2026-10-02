---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/c2bdf4ca7dc34500ba9414eaa7adc320",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "National Assembly for Wales Electoral Regions (December 2018) Boundaries WA BSC",
  "description": "This file contains the digital vector boundaries for National Assembly for Wales Electoral Regions in Wales, as at December 2018. The BSC boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_(Dec_2018)_SGCB_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NAWER_Dec_2018_Super_Generalised_Clipped_Boundaries_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_Dec_2018_SGCB_Wales_2022/FeatureServer",
  "nativeIdentifier": "c2bdf4ca7dc34500ba9414eaa7adc320",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/c2bdf4ca7dc34500ba9414eaa7adc320",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "National Assembly for Wales Electoral Regions",
    "NAWER",
    "2018",
    "Electoral Boundaries",
    "Wales",
    "WFS",
    "WMS",
    "BDY_ELE",
    "BDY_NAWER",
    "DEC_2018",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3001&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:06.567855Z",
      "responseSha256": "c5871a4a72ed49389fa9e94d958aa5a6f8cc3f1ba5543ed1064e4788976cea04",
      "sourcePointer": "/results/52",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3052",
      "normalisedRecordSha256": "18f3f67b38ffeb33a73f691a58c7c28995e7d733fb1712237115b8572f374803",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/c2bdf4ca7dc34500ba9414eaa7adc320"
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
    "metadataModified": "2025-08-11T08:05:26Z",
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
    "created": 1664483338000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for National Assembly for Wales Electoral Regions in Wales, as at December 2018. The BSC boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_(Dec_2018)_SGCB_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NAWER_Dec_2018_Super_Generalised_Clipped_Boundaries_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_Dec_2018_SGCB_Wales_2022/FeatureServer",
    "extent": [
      [
        -5.616163120662944,
        51.32907961546323
      ],
      [
        -2.643831113680645,
        53.452847417724755
      ]
    ],
    "id": "c2bdf4ca7dc34500ba9414eaa7adc320",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899526000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "National Assembly for Wales Electoral Regions",
      "NAWER",
      "2018",
      "Electoral Boundaries",
      "Wales",
      "WFS",
      "WMS",
      "BDY_ELE",
      "BDY_NAWER",
      "DEC_2018"
    ],
    "title": "National Assembly for Wales Electoral Regions (December 2018) Boundaries WA BSC",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NAWER_Dec_2018_Super_Generalised_Clipped_Boundaries_Wales/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# National Assembly for Wales Electoral Regions (December 2018) Boundaries WA BSC

This file contains the digital vector boundaries for National Assembly for Wales Electoral Regions in Wales, as at December 2018. The BSC boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_(Dec_2018)_SGCB_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NAWER_Dec_2018_Super_Generalised_Clipped_Boundaries_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NAWER_Dec_2018_SGCB_Wales_2022/FeatureServer

Native identifier: `c2bdf4ca7dc34500ba9414eaa7adc320`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/c2bdf4ca7dc34500ba9414eaa7adc320)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
