---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/9b5fec5d4a9a47bcabc98ebc2f956321",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "LAU1_2012_GB_BGC",
  "description": "This file contains digital vector boundaries for local administrative units, level 1 in Great Britain as at 1st January 2012. LAUs form part of a hierarchical classification of spatial units that provide a breakdown of the EU's territory for producing comparable regional statistics. LAU 1 replaced NUTS 4 in July 2003. They are made up of individual local authority districts. There are 389 LAU 1 areas in Great Britain. Please note that LAU 1 do not have the nine character codes as Eurostat use only their own seven character codes. The boundaries are Intermediate/Generalised (20m). Intermediate datasets are designed for high quality mapping, preserving much of the original detail from the full dataset, but typically 10% of the file size. They are great when used in conjunction with the OS raster products and for producing detailed regional and local maps, or large wall maps. They are also suitable for non-demanding GIS analyses (such as buffering). Intermediate datasets are a good compromise between detail and small file size. They have also been clipped to the coastline (Mean High Water mark), giving the coastline a more orthodox appearance. Please note that this product contains both Ordnance Survey and ONS Intellectual Property Rights.",
  "nativeIdentifier": "9b5fec5d4a9a47bcabc98ebc2f956321",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/9b5fec5d4a9a47bcabc98ebc2f956321",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Local administrative unit",
    " level 1",
    " LAU",
    " level 1",
    " LAU1",
    " Great Britain",
    " GB.",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:31.508620Z",
      "responseSha256": "1fe8c8cc318b789ed23ed3669e1624501fa4370936fd663d0b61730f18795298",
      "sourcePointer": "/results/33",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/33",
      "normalisedRecordSha256": "2fa696bc41bb6ad555b81eed145ee6efe29910a939b4ecac8ad5625f189c9bb3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/9b5fec5d4a9a47bcabc98ebc2f956321"
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
    "metadataModified": "2025-08-11T07:46:02Z",
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
    "created": 1411395921000,
    "culture": "en-gb",
    "description": "This file contains digital vector boundaries for local administrative units, level 1 in Great Britain as at 1st January 2012. LAUs form part of a hierarchical classification of spatial units that provide a breakdown of the EU's territory for producing comparable regional statistics. LAU 1 replaced NUTS 4 in July 2003. They are made up of individual local authority districts. There are 389 LAU 1 areas in Great Britain. Please note that LAU 1 do not have the nine character codes as Eurostat use only their own seven character codes. The boundaries are Intermediate/Generalised (20m). Intermediate datasets are designed for high quality mapping, preserving much of the original detail from the full dataset, but typically 10% of the file size. They are great when used in conjunction with the OS raster products and for producing detailed regional and local maps, or large wall maps. They are also suitable for non-demanding GIS analyses (such as buffering). Intermediate datasets are a good compromise between detail and small file size. They have also been clipped to the coastline (Mean High Water mark), giving the coastline a more orthodox appearance. Please note that this product contains both Ordnance Survey and ONS Intellectual Property Rights.",
    "extent": [
      [
        -7.485656582315717,
        49.817664759216356
      ],
      [
        2.697274119252334,
        60.78393333950662
      ]
    ],
    "id": "9b5fec5d4a9a47bcabc98ebc2f956321",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898362000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Local administrative units, level 1 in Great Britain as at 1st January 2012.",
    "spatialReference": "British_National_Grid",
    "tags": [
      "Local administrative unit",
      " level 1",
      " LAU",
      " level 1",
      " LAU1",
      " Great Britain",
      " GB."
    ],
    "title": "LAU1_2012_GB_BGC",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Service",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAU1_2012_GB_BGC/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# LAU1_2012_GB_BGC

This file contains digital vector boundaries for local administrative units, level 1 in Great Britain as at 1st January 2012. LAUs form part of a hierarchical classification of spatial units that provide a breakdown of the EU's territory for producing comparable regional statistics. LAU 1 replaced NUTS 4 in July 2003. They are made up of individual local authority districts. There are 389 LAU 1 areas in Great Britain. Please note that LAU 1 do not have the nine character codes as Eurostat use only their own seven character codes. The boundaries are Intermediate/Generalised (20m). Intermediate datasets are designed for high quality mapping, preserving much of the original detail from the full dataset, but typically 10% of the file size. They are great when used in conjunction with the OS raster products and for producing detailed regional and local maps, or large wall maps. They are also suitable for non-demanding GIS analyses (such as buffering). Intermediate datasets are a good compromise between detail and small file size. They have also been clipped to the coastline (Mean High Water mark), giving the coastline a more orthodox appearance. Please note that this product contains both Ordnance Survey and ONS Intellectual Property Rights.

Native identifier: `9b5fec5d4a9a47bcabc98ebc2f956321`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/9b5fec5d4a9a47bcabc98ebc2f956321)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
