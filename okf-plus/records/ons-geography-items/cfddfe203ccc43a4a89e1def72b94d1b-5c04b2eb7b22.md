---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/cfddfe203ccc43a4a89e1def72b94d1b",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "National Parks (December 2022) Boundaries GB BFE (V3)",
  "description": "This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Version 2: Some name changes have taken place S21000002 Loch Lomond and Trossachs to Loch Lomond and The Trossachs W18000001 Brecon Beacons to Bannau Brycheiniog W18000002 Change in Welsh names to Arfordir Sir Benfro W18000003 Snowdonia to Eryri Version 3: Minor sliver corrections to Lake District only REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NPARK_DEC_2022_GB_BFE_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2022_Boundaries_GB_BFE_V3/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_(December_2022)_Boundaries_GB_BFE_(V3)/MapServer",
  "nativeIdentifier": "cfddfe203ccc43a4a89e1def72b94d1b",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/cfddfe203ccc43a4a89e1def72b94d1b",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6001&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:42.113987Z",
      "responseSha256": "657837777306a97562f58898f9485183f4d7995327451e452a03a06be5925abf",
      "sourcePointer": "/results/70",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6070",
      "normalisedRecordSha256": "ed7bf40a3adcfe002ecabc5288eb56e08f9ef66741da793c36bfccb9de384586",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/cfddfe203ccc43a4a89e1def72b94d1b"
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
    "metadataModified": "2025-08-11T08:25:10Z",
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
      "/Categories/Boundaries - Other/2022",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1749560905000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Version 2: Some name changes have taken place S21000002 Loch Lomond and Trossachs to Loch Lomond and The Trossachs W18000001 Brecon Beacons to Bannau Brycheiniog W18000002 Change in Welsh names to Arfordir Sir Benfro W18000003 Snowdonia to Eryri Version 3: Minor sliver corrections to Lake District only REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NPARK_DEC_2022_GB_BFE_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2022_Boundaries_GB_BFE_V3/WFSServer?service=wfs&request=getcapabilities <o:p></o:p> REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_(December_2022)_Boundaries_GB_BFE_(V3)/MapServer",
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
    "id": "cfddfe203ccc43a4a89e1def72b94d1b",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754900710000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Other Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries"
    ],
    "title": "National Parks (December 2022) Boundaries GB BFE (V3)",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_(December_2022)_Boundaries_GB_BFE_(V3)/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# National Parks (December 2022) Boundaries GB BFE (V3)

This file contains the digital vector boundaries for National Parks, in Great Britain, as at December 2022. The boundaries available are: (BFE) Full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Version 2: Some name changes have taken place S21000002 Loch Lomond and Trossachs to Loch Lomond and The Trossachs W18000001 Brecon Beacons to Bannau Brycheiniog W18000002 Change in Welsh names to Arfordir Sir Benfro W18000003 Snowdonia to Eryri Version 3: Minor sliver corrections to Lake District only REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/NPARK_DEC_2022_GB_BFE_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/National_Parks_December_2022_Boundaries_GB_BFE_V3/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/National_Parks_(December_2022)_Boundaries_GB_BFE_(V3)/MapServer

Native identifier: `cfddfe203ccc43a4a89e1def72b94d1b`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/cfddfe203ccc43a4a89e1def72b94d1b)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
