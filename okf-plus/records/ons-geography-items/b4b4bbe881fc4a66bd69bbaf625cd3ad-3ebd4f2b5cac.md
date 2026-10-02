---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/b4b4bbe881fc4a66bd69bbaf625cd3ad",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Registration Districts (December 2016) Boundaries EW BFE",
  "description": "This file contains the digital vector boundaries for Registration Districts, in England and Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_(Dec_2016)_FEB_in_England_and_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Registration_Districts_December_2016_Full_Extent_Boundaries_in_England_and_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_Dec_2016_FEB_in_England_and_Wales_2022/FeatureServer",
  "nativeIdentifier": "b4b4bbe881fc4a66bd69bbaf625cd3ad",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/b4b4bbe881fc4a66bd69bbaf625cd3ad",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Registration Districts",
    "REGD",
    "2016",
    "Other Boundaries",
    "England and Wales",
    "WFS",
    "WMS",
    "boundaries",
    "BDY_OTH",
    "BDY_REGD",
    "DEC_2016",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=4101&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:19.524367Z",
      "responseSha256": "9c06bfa45225129a10c9c6243220b88fadb811b4501fd6c246b63e08100ad350",
      "sourcePointer": "/results/44",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/4144",
      "normalisedRecordSha256": "3742b38e04f4dd009024361319a45ba996061e9bd1e283beba63a5cd4dd7c61e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/b4b4bbe881fc4a66bd69bbaf625cd3ad"
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
    "metadataModified": "2025-08-11T08:12:35Z",
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
    "created": 1666808235000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Registration Districts, in England and Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_(Dec_2016)_FEB_in_England_and_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Registration_Districts_December_2016_Full_Extent_Boundaries_in_England_and_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_Dec_2016_FEB_in_England_and_Wales_2022/FeatureServer",
    "extent": [
      [
        -7.053294423207091,
        49.863963565826616
      ],
      [
        2.079245609195768,
        55.81166100419411
      ]
    ],
    "id": "b4b4bbe881fc4a66bd69bbaf625cd3ad",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899955000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Registration Districts",
      "REGD",
      "2016",
      "Other Boundaries",
      "England and Wales",
      "WFS",
      "WMS",
      "boundaries",
      "BDY_OTH",
      "BDY_REGD",
      "DEC_2016"
    ],
    "title": "Registration Districts (December 2016) Boundaries EW BFE",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Registration_Districts_December_2016_Full_Extent_Boundaries_in_England_and_Wales/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Registration Districts (December 2016) Boundaries EW BFE

This file contains the digital vector boundaries for Registration Districts, in England and Wales, as at December 2016. The boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_(Dec_2016)_FEB_in_England_and_Wales/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Registration_Districts_December_2016_Full_Extent_Boundaries_in_England_and_Wales/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/REGD_Dec_2016_FEB_in_England_and_Wales_2022/FeatureServer

Native identifier: `b4b4bbe881fc4a66bd69bbaf625cd3ad`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/b4b4bbe881fc4a66bd69bbaf625cd3ad)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
