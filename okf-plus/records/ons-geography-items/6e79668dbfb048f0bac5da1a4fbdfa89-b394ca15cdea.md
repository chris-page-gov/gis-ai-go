---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/6e79668dbfb048f0bac5da1a4fbdfa89",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Counties and Unitary Authorities (April 2019) Boundaries UK BFE",
  "description": "This file contains the digital vector boundaries for Counties and Unitary Authorities in the United Kingdom, as at April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_(April_2019)_Full_extent_Boundaries_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK_2022/FeatureServer",
  "nativeIdentifier": "6e79668dbfb048f0bac5da1a4fbdfa89",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/6e79668dbfb048f0bac5da1a4fbdfa89",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Boundaries",
    "Counties and Unitary Authorities",
    "CTYUA",
    "2019",
    "Administrative Boundaries",
    "United Kingdom",
    "WFS",
    "WMS",
    "BDY_ADM",
    "BDY_CTYUA",
    "APR_2019",
    "WFS"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1801&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:52.698003Z",
      "responseSha256": "6dd833eb8661ef64b7bd37798926a4ac099a2a58630cd90c9ec05ae3aa33a5fe",
      "sourcePointer": "/results/42",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1842",
      "normalisedRecordSha256": "127670213552a5e472aeaf3931ae42978ca8fbaf446fdc63e6e1234dac1d4949",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/6e79668dbfb048f0bac5da1a4fbdfa89"
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
    "metadataModified": "2025-08-11T07:57:44Z",
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
    "created": 1662726668000,
    "culture": "en-gb",
    "description": "This file contains the digital vector boundaries for Counties and Unitary Authorities in the United Kingdom, as at April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_(April_2019)_Full_extent_Boundaries_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK_2022/FeatureServer",
    "extent": [
      [
        -9.332052555387207,
        49.81385905889074
      ],
      [
        2.7043084581023917,
        60.86611141007168
      ]
    ],
    "id": "6e79668dbfb048f0bac5da1a4fbdfa89",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754899064000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Boundaries",
    "spatialReference": "27700",
    "tags": [
      "Boundaries",
      "Counties and Unitary Authorities",
      "CTYUA",
      "2019",
      "Administrative Boundaries",
      "United Kingdom",
      "WFS",
      "WMS",
      "BDY_ADM",
      "BDY_CTYUA",
      "APR_2019"
    ],
    "title": "Counties and Unitary Authorities (April 2019) Boundaries UK BFE",
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
    "url": "https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK/WFSServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Counties and Unitary Authorities (April 2019) Boundaries UK BFE

This file contains the digital vector boundaries for Counties and Unitary Authorities in the United Kingdom, as at April 2019. The BFE boundaries are full resolution - extent of the realm (usually this is the Mean Low Water mark but in some cases boundaries extend beyond this to include off shore islands). Contains both Ordnance Survey and ONS Intellectual Property Rights. REST URL of ArcGIS for INSPIRE View Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_(April_2019)_Full_extent_Boundaries_UK/MapServer REST URL of ArcGIS for INSPIRE Feature DownloadService – https://dservices1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK/WFSServer?service=wfs&request=getcapabilities REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_April_2019_Full_extent_Boundaries_UK_2022/FeatureServer

Native identifier: `6e79668dbfb048f0bac5da1a4fbdfa89`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/6e79668dbfb048f0bac5da1a4fbdfa89)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
