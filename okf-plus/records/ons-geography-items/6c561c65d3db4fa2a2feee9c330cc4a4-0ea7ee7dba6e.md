---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/6c561c65d3db4fa2a2feee9c330cc4a4",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NHS Commissioning Regions (April 2016) Boundaries EN BUC",
  "description": "This file contains the digital vector boundaries for NHS commissioning regions (NHSCR) in England as at April 2016. The boundaries are Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_(Apr_2016)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHSCR_Apr_2016_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_Apr_2016_UGCB_in_England_2022/FeatureServer",
  "nativeIdentifier": "6c561c65d3db4fa2a2feee9c330cc4a4",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/6c561c65d3db4fa2a2feee9c330cc4a4",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "NHS Commissioning Regions",
    "NHSCR",
    "2016",
    "England",
    "Health Boundaries",
    "WFS",
    "WMS",
    "boundaries",
    "BDY_HLT",
    "APR_2016",
    "BDY_NHSER",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:58.300760Z",
      "responseSha256": "8e910251c93459359ef89d3b87c74fbfb61372ce1efc9aa1b268978f01946b43",
      "sourcePointer": "/results/63",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2363",
      "normalisedRecordSha256": "d97947fc1bcd18510532ac6cfbb908ed623ca2bf45b2f0f0ee0265442ad76cd3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/6c561c65d3db4fa2a2feee9c330cc4a4"
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
    "metadataModified": "2025-08-11T08:01:04Z",
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
    "created": 1664386250000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for NHS commissioning regions (NHSCR) in England as at April 2016. The boundaries are Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_(Apr_2016)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHSCR_Apr_2016_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_Apr_2016_UGCB_in_England_2022/FeatureServer",
    "extent": [
      [
        -6.979689255910928,
        49.88183266048537
      ],
      [
        2.0730910733493264,
        55.81119902120039
      ]
    ],
    "id": "6c561c65d3db4fa2a2feee9c330cc4a4",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899264000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Health Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "NHS Commissioning Regions",
      "NHSCR",
      "2016",
      "England",
      "Health Boundaries",
      "WFS",
      "WMS",
      "boundaries",
      "BDY_HLT",
      "APR_2016",
      "BDY_NHSER"
    ],
    "title": "NHS Commissioning Regions (April 2016) Boundaries EN BUC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_Apr_2016_UGCB_in_England_2022/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# NHS Commissioning Regions (April 2016) Boundaries EN BUC

This file contains the digital vector boundaries for NHS commissioning regions (NHSCR) in England as at April 2016. The boundaries are Ultra generalised (500m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_(Apr_2016)_UGCB_in_England/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/NHSCR_Apr_2016_Ultra_Generalised_Clipped_Boundaries_in_England/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NHSCR_Apr_2016_UGCB_in_England_2022/FeatureServer

Native identifier: `6c561c65d3db4fa2a2feee9c330cc4a4`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/6c561c65d3db4fa2a2feee9c330cc4a4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
