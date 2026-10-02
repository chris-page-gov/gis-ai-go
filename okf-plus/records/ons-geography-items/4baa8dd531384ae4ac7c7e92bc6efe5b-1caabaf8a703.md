---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/4baa8dd531384ae4ac7c7e92bc6efe5b",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local Administrative Units, level 1 (January 2018) Boundaries UK BSC",
  "description": "This file contains the digital vector boundaries for Local Administrative Units Level 1, in the United Kingdom, as at January 2018. The boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_(Jan_2018)_SGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAU1_Jan_2018_Super_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_Jan_2018_SGCB_in_the_UK_2022/FeatureServer",
  "nativeIdentifier": "4baa8dd531384ae4ac7c7e92bc6efe5b",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/4baa8dd531384ae4ac7c7e92bc6efe5b",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Local Administrative Units Level 1",
    "LAU1",
    "2018",
    "Eurostat Boundaries",
    "UK",
    "WFS",
    "WMS",
    "LAU 1 Boundaries",
    "Latest_Boundaries",
    "boundaries",
    "LAU_1_Boundaries_2018",
    "BDY_EUR",
    "BDY_LAU1",
    "JAN_2018",
    "Map Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=2701&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:03.005385Z",
      "responseSha256": "35fe73f1f0481f726d41fe01aeb85a6c25ef17b93add8625fd2a748545626cd7",
      "sourcePointer": "/results/86",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/2786",
      "normalisedRecordSha256": "a8cf21cd2eea141ca1912611f825a0459f28a3c3176aeecb5a5be6bd42009a50",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/4baa8dd531384ae4ac7c7e92bc6efe5b"
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
    "metadataModified": "2025-08-11T08:03:44Z",
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
    "created": 1664453208000,
    "culture": "en-us",
    "description": "This file contains the digital vector boundaries for Local Administrative Units Level 1, in the United Kingdom, as at January 2018. The boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_(Jan_2018)_SGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAU1_Jan_2018_Super_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_Jan_2018_SGCB_in_the_UK_2022/FeatureServer",
    "extent": [
      [
        -9.330219522919432,
        49.81570424352799
      ],
      [
        2.6949116252363647,
        60.86170628372345
      ]
    ],
    "id": "4baa8dd531384ae4ac7c7e92bc6efe5b",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899424000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Local Administrative Units Level 1",
      "LAU1",
      "2018",
      "Eurostat Boundaries",
      "UK",
      "WFS",
      "WMS",
      "LAU 1 Boundaries",
      "Latest_Boundaries",
      "boundaries",
      "LAU_1_Boundaries_2018",
      "BDY_EUR",
      "BDY_LAU1",
      "JAN_2018"
    ],
    "title": "Local Administrative Units, level 1 (January 2018) Boundaries UK BSC",
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
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_(Jan_2018)_SGCB_in_the_UK/MapServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Local Administrative Units, level 1 (January 2018) Boundaries UK BSC

This file contains the digital vector boundaries for Local Administrative Units Level 1, in the United Kingdom, as at January 2018. The boundaries are super generalised (200m) - clipped to the coastline (Mean High Water mark). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_(Jan_2018)_SGCB_in_the_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/LAU1_Jan_2018_Super_Generalised_Clipped_Boundaries_in_the_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_Jan_2018_SGCB_in_the_UK_2022/FeatureServer

Native identifier: `4baa8dd531384ae4ac7c7e92bc6efe5b`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/4baa8dd531384ae4ac7c7e92bc6efe5b)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
