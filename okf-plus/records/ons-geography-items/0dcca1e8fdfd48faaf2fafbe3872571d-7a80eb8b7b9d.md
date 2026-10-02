---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/0dcca1e8fdfd48faaf2fafbe3872571d",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Counties (December 2015) Boundaries EN BUC",
  "description": "This file contains the digital vector boundaries for ‘shire’ counties in England as at 31st December 2015. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(December_2015)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_December_2015_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_December_2015_UGCB_in_England_2022/FeatureServer",
  "nativeIdentifier": "0dcca1e8fdfd48faaf2fafbe3872571d",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/0dcca1e8fdfd48faaf2fafbe3872571d",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "County",
    "CTY",
    "2015",
    "England",
    "Administrative Boundaries",
    "WFS",
    "WMS",
    "County Boundaries",
    "boundaries",
    "BDY_ADM",
    "BDY_CTY",
    "DEC_2015",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1201&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:45.495592Z",
      "responseSha256": "85be0d8a87b81a5d80f639ddea0e111d7d40f0e50db4665f571b85d716f311e7",
      "sourcePointer": "/results/8",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1208",
      "normalisedRecordSha256": "7c1d42dd4ce5ff196b71599e8cf59b4f066006d137764ab961f3bace67b13666",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/0dcca1e8fdfd48faaf2fafbe3872571d"
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
    "metadataModified": "2025-08-11T07:53:51Z",
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
    "created": 1662462975000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for ‘shire’ counties in England as at 31st December 2015. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(December_2015)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_December_2015_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_December_2015_UGCB_in_England_2022/FeatureServer",
    "extent": [
      [
        -4.936838450178232,
        50.1592867517224
      ],
      [
        2.0097689667417113,
        55.19093689116909
      ]
    ],
    "id": "0dcca1e8fdfd48faaf2fafbe3872571d",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898831000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "County",
      "CTY",
      "2015",
      "England",
      "Administrative Boundaries",
      "WFS",
      "WMS",
      "County Boundaries",
      "boundaries",
      "BDY_ADM",
      "BDY_CTY",
      "DEC_2015"
    ],
    "title": "Counties (December 2015) Boundaries EN BUC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(December_2015)_UGCB_in_England/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Counties (December 2015) Boundaries EN BUC

This file contains the digital vector boundaries for ‘shire’ counties in England as at 31st December 2015. The boundaries are ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_(December_2015)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_December_2015_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_December_2015_UGCB_in_England_2022/FeatureServer

Native identifier: `0dcca1e8fdfd48faaf2fafbe3872571d`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/0dcca1e8fdfd48faaf2fafbe3872571d)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
