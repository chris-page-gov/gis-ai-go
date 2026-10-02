---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/fbed6f3bb9ae4cab9f74b3cb331d39ed",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "County Electoral Division (May 2024) Boundaries EN BUC (V3)",
  "description": "This file contains the digital vector boundaries for County Electoral Division, in England, as at May 2024. The boundaries available are: (BUC) Ultra Generalised (500m) - clipped to the coastline (Mean High Water Mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/CED_MAY_2024_EN_BUC_V3/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/MapServer",
  "nativeIdentifier": "fbed6f3bb9ae4cab9f74b3cb331d39ed",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/fbed6f3bb9ae4cab9f74b3cb331d39ed",
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
    "County_Electoral",
    "County_Electoral_Division",
    "BDY_CED",
    "England",
    "EN",
    "MAY_2024",
    "2024",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6001&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:42.113987Z",
      "responseSha256": "657837777306a97562f58898f9485183f4d7995327451e452a03a06be5925abf",
      "sourcePointer": "/results/34",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6034",
      "normalisedRecordSha256": "4388ae58320dcc27095ae78aea2a8e9b3a485f18d840d3d5e23304c103baaaaa",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/fbed6f3bb9ae4cab9f74b3cb331d39ed"
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
    "metadataModified": "2025-08-11T08:24:52Z",
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
      "/Categories/LATEST",
      "/Categories/ONS Geography Open Data",
      "/Categories/Boundaries - Administrative/2024"
    ],
    "created": 1744622642000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for County Electoral Division, in England, as at May 2024. The boundaries available are: (BUC) Ultra Generalised (500m) - clipped to the coastline (Mean High Water Mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/CED_MAY_2024_EN_BUC_V3/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/MapServer",
    "extent": [
      [
        -4.87206418866828,
        50.159852332390884
      ],
      [
        1.9179525192624471,
        54.24044606950282
      ]
    ],
    "id": "fbed6f3bb9ae4cab9f74b3cb331d39ed",
    "licenseInfo": "<p><a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.ons.gov.uk/methodology/geography/licences\">https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1754900692000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Administrative Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Administrative Boundaries",
      "BDY_ADM",
      "County_Electoral",
      "County_Electoral_Division",
      "BDY_CED",
      "England",
      "EN",
      "MAY_2024",
      "2024"
    ],
    "title": "County Electoral Division (May 2024) Boundaries EN BUC (V3)",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# County Electoral Division (May 2024) Boundaries EN BUC (V3)

This file contains the digital vector boundaries for County Electoral Division, in England, as at May 2024. The boundaries available are: (BUC) Ultra Generalised (500m) - clipped to the coastline (Mean High Water Mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/FeatureServer REST URL of WFS Server – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/CED_MAY_2024_EN_BUC_V3/WFSServer?service=wfs&request=getcapabilities REST URL of MapServer – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/CED_MAY_2024_EN_BUC_V3/MapServer

Native identifier: `fbed6f3bb9ae4cab9f74b3cb331d39ed`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/fbed6f3bb9ae4cab9f74b3cb331d39ed)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
