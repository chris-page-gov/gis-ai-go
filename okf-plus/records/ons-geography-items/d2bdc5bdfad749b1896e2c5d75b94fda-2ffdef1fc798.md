---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/d2bdc5bdfad749b1896e2c5d75b94fda",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Norfolk polygons",
  "description": "",
  "nativeIdentifier": "d2bdc5bdfad749b1896e2c5d75b94fda",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/d2bdc5bdfad749b1896e2c5d75b94fda",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=5001&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:30.287065Z",
      "responseSha256": "c41e0a85902216f12ce16ef5de38165c61f4e42b237fa894f7f9d2d519e31d15",
      "sourcePointer": "/results/96",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/5096",
      "normalisedRecordSha256": "f417004f0c5767ac8daf88b8cfaa66828c26e8c28a53286dc1c431d348eb92f3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/d2bdc5bdfad749b1896e2c5d75b94fda"
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
    "metadataModified": "2023-11-08T13:58:18Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Consult the portal item licence; no licence inferred.",
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
    "created": 1695903961000,
    "culture": "en-gb",
    "description": "",
    "extent": [
      [
        0.13929237747173157,
        52.34026709633685
      ],
      [
        1.7784293309853487,
        52.99776634791331
      ]
    ],
    "id": "d2bdc5bdfad749b1896e2c5d75b94fda",
    "licenseInfo": "",
    "modified": 1699451898000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "",
    "spatialReference": "",
    "tags": [
      ""
    ],
    "title": "Norfolk polygons",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS API for JavaScript",
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Service",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Norfolk_polygons/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Norfolk polygons



Native identifier: `d2bdc5bdfad749b1896e2c5d75b94fda`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/d2bdc5bdfad749b1896e2c5d75b94fda)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
