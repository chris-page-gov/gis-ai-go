---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/e479c0eebf4846afa711636ed63daeff",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Covid Infection Survey (October 2020) to Country Lookup for the UK",
  "description": "A lookup file between 2020 Covid Infection Survey Geography to 2020 Countries in the United Kingdom, as at 1 October 2020. (File size - 32 KB) Field Names - CIS20CD, CTRY19CD, CTRY19NM, FID Field Types - Text, Text, Text, Numeric Field Lengths - 9, 9, 16 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Covid_Infection_Survey__October_2020__to_Country_Lookup_for_the_United_Kingdom/FeatureServer",
  "nativeIdentifier": "e479c0eebf4846afa711636ed63daeff",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/e479c0eebf4846afa711636ed63daeff",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "LUP_HLT",
    "OCT_2020",
    "Covid Infection Survey",
    "2020",
    "CIS",
    "LUP_CIS",
    "Local Authority District",
    "LUP_CIS_CTRY",
    "CTRY",
    "Countries",
    "UK",
    "United Kingdom",
    "LUP_EXACT_CIS",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=1101&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:27:44.236548Z",
      "responseSha256": "508c68b7523d50e1cd043fec68a7e3b66cae3eaeb8d58e729423f5277149fbd8",
      "sourcePointer": "/results/65",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/1165",
      "normalisedRecordSha256": "dccd25f2a0e466a7800c3bd9ede5300c8b637487962a25f2c1f8c1a3c4c4024d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/e479c0eebf4846afa711636ed63daeff"
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
    "metadataModified": "2025-08-11T07:53:34Z",
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
      "/Categories/ONS Geography Open Data",
      "/Categories/Lookups/Health"
    ],
    "created": 1659175652000,
    "culture": "en-gb",
    "description": "A lookup file between 2020 Covid Infection Survey Geography to 2020 Countries in the United Kingdom, as at 1 October 2020. (File size - 32 KB) Field Names - CIS20CD, CTRY19CD, CTRY19NM, FID Field Types - Text, Text, Text, Numeric Field Lengths - 9, 9, 16 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Covid_Infection_Survey__October_2020__to_Country_Lookup_for_the_United_Kingdom/FeatureServer",
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
    "id": "e479c0eebf4846afa711636ed63daeff",
    "licenseInfo": "<a href='https://www.ons.gov.uk/methodology/geography/licences' target='_blank' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a>",
    "modified": 1754898814000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Health Lookup",
    "spatialReference": null,
    "tags": [
      "LUP_HLT",
      "OCT_2020",
      "Covid Infection Survey",
      "2020",
      "CIS",
      "LUP_CIS",
      "Local Authority District",
      "LUP_CIS_CTRY",
      "CTRY",
      "Countries",
      "UK",
      "United Kingdom",
      "LUP_EXACT_CIS"
    ],
    "title": "Covid Infection Survey (October 2020) to Country Lookup for the UK",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "source-953f3e0955824967a97b3ae2f58dd4b1",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Covid_Infection_Survey__October_2020__to_Country_Lookup_for_the_United_Kingdom/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Covid Infection Survey (October 2020) to Country Lookup for the UK

A lookup file between 2020 Covid Infection Survey Geography to 2020 Countries in the United Kingdom, as at 1 October 2020. (File size - 32 KB) Field Names - CIS20CD, CTRY19CD, CTRY19NM, FID Field Types - Text, Text, Text, Numeric Field Lengths - 9, 9, 16 FID = The FID, or Feature ID is created by the publication process when the names and codes / lookup products are published to the Open Geography portal. REST URL of Feature Access Service – https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Covid_Infection_Survey__October_2020__to_Country_Lookup_for_the_United_Kingdom/FeatureServer

Native identifier: `e479c0eebf4846afa711636ed63daeff`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/e479c0eebf4846afa711636ed63daeff)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
