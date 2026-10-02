---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/555c4933e77d447fbcdc8a1cc64baafd",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Authority Districts (December 2016) Boundaries GB BGC",
  "description": "This file contains the digital vector boundaries for Local Authority Districts, in Great Britain, as at 31 December 2016. The boundaries available are: Generalised (20m) - clipped to the coastline (Mean High Water mark) Contains both Ordnance Survey and ONS Intellectual Property Rights. Download File Sizes Generalised (20m) - clipped to the coastline (6 MB) REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_(Dec_2016)_GB_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAD_Dec_2016_GB_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2016_GB_BGC_2022/FeatureServer",
  "nativeIdentifier": "555c4933e77d447fbcdc8a1cc64baafd",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/555c4933e77d447fbcdc8a1cc64baafd",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Local Authority District",
    "LAD",
    "2016",
    "Administrative Boundaries",
    "Great Britain",
    "WFS",
    "WMS",
    "Latest_Boundaries",
    "boundaries",
    "BDY_ADM",
    "BDY_LAD",
    "DEC_2016",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=3701&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:14.974738Z",
      "responseSha256": "3dc3db0ce636918cd82e72d59548293210a5e447403d11c8f2030bf6749173f9",
      "sourcePointer": "/results/43",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/3743",
      "normalisedRecordSha256": "c7b6c38927b09cb126336093817ab27c4ddb983f70fb7c8d03b66a345871ed01",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/555c4933e77d447fbcdc8a1cc64baafd"
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
    "metadataModified": "2025-08-11T08:09:58Z",
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
      "/Categories/Boundaries - Administrative/2016",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1664962091000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Local Authority Districts, in Great Britain, as at 31 December 2016. The boundaries available are: Generalised (20m) - clipped to the coastline (Mean High Water mark) Contains both Ordnance Survey and ONS Intellectual Property Rights. Download File Sizes Generalised (20m) - clipped to the coastline (6 MB) REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_(Dec_2016)_GB_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAD_Dec_2016_GB_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2016_GB_BGC_2022/FeatureServer",
    "extent": [
      [
        -9.22986758508968,
        49.817664753318475
      ],
      [
        2.6980081028736893,
        60.86611134111886
      ]
    ],
    "id": "555c4933e77d447fbcdc8a1cc64baafd",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899798000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Local Authority District",
      "LAD",
      "2016",
      "Administrative Boundaries",
      "Great Britain",
      "WFS",
      "WMS",
      "Latest_Boundaries",
      "boundaries",
      "BDY_ADM",
      "BDY_LAD",
      "DEC_2016"
    ],
    "title": "Local Authority Districts (December 2016) Boundaries GB BGC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2016_GB_BGC_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Authority Districts (December 2016) Boundaries GB BGC

This file contains the digital vector boundaries for Local Authority Districts, in Great Britain, as at 31 December 2016. The boundaries available are: Generalised (20m) - clipped to the coastline (Mean High Water mark) Contains both Ordnance Survey and ONS Intellectual Property Rights. Download File Sizes Generalised (20m) - clipped to the coastline (6 MB) REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_(Dec_2016)_GB_BGC/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAD_Dec_2016_GB_BGC/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2016_GB_BGC_2022/FeatureServer

Native identifier: `555c4933e77d447fbcdc8a1cc64baafd`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/555c4933e77d447fbcdc8a1cc64baafd)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
