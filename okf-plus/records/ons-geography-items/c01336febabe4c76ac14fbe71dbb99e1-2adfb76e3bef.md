---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/c01336febabe4c76ac14fbe71dbb99e1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Postcode to OA (2021) to LSOA to MSOA to LAD (February 2026) Best Fit Lookup in the UK",
  "description": "A best-fit lookup between postcodes, 2021 Census Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA) and local authority districts (LAD). Postcodes are as at February 2026 in the UK and are best-fitted by plotting the location of the postcode's mean address into the areas of the output geographies. (File size 22 MB). Field Names - PCD7, PCD8, PCDS, DOINTR, DOTERM, USERTYPE, OA21CD, LSOA21CD, MSOA21CD, LADCD, LSOA21NM, MSOA21NM, LADNM, LADNMW Field Types - All Text Field Lengths - 7, 8, 8, 8, 8, 1, 9, 9, 9, 9, 55, 65, 45, 45",
  "nativeIdentifier": "c01336febabe4c76ac14fbe71dbb99e1",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/c01336febabe4c76ac14fbe71dbb99e1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "PCD",
    "Lookups",
    "Lookup",
    "Postcode Lookups",
    "Postcode",
    "Output Area",
    "Super Output Area",
    "Local Authority District",
    "OA",
    "LSOA",
    "MSOA",
    "LAD",
    "UK",
    "ZIP File",
    "PCD_OA_LSOA_MSOA_LAD",
    "LUP_PCD_OA_LSOA_MSOA_LAD",
    "latest_lookups",
    "Latest Lookups",
    "2026",
    "FEB_2026",
    "CSV Collection"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6301&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:45.613584Z",
      "responseSha256": "86ba1d0827620b73f335037b268218dfcc2857fe8d5d267ff9e786b507c5de21",
      "sourcePointer": "/results/89",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6389",
      "normalisedRecordSha256": "b0daad32eeeeff09e4583c0774ed011da8a749dcdc9169446e7acfe2a19ca933",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/c01336febabe4c76ac14fbe71dbb99e1"
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
    "metadataModified": "2026-08-24T14:20:39Z",
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
      "/Categories/Postcode Products/Postcode Lookups",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1772448871000,
    "culture": "en-gb",
    "description": "A best-fit lookup between postcodes, 2021 Census Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA) and local authority districts (LAD). Postcodes are as at February 2026 in the UK and are best-fitted by plotting the location of the postcode's mean address into the areas of the output geographies. (File size 22 MB). Field Names - PCD7, PCD8, PCDS, DOINTR, DOTERM, USERTYPE, OA21CD, LSOA21CD, MSOA21CD, LADCD, LSOA21NM, MSOA21NM, LADNM, LADNMW Field Types - All Text Field Lengths - 7, 8, 8, 8, 8, 1, 9, 9, 9, 9, 55, 65, 45, 45",
    "extent": [],
    "id": "c01336febabe4c76ac14fbe71dbb99e1",
    "licenseInfo": "<p><a style='background-color:rgb(255, 255, 255); border:0px solid currentcolor; box-sizing:border-box; color:rgb(0, 97, 155); font-family:&quot;Avenir Next&quot;, Avenir, &quot;Helvetica Neue&quot;, sans-serif; font-size:16px; font-style:normal; font-variant-caps:normal; font-variant-ligatures:normal; font-weight:400; letter-spacing:normal; line-height:1.5; text-align:start; text-decoration:none; text-indent:0px; text-transform:none; word-spacing:0px;' target='_blank' href='https://www.ons.gov.uk/methodology/geography/licences' rel='nofollow ugc noopener noreferrer'>https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1787581239000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Postcode Products",
    "spatialReference": null,
    "tags": [
      "PCD",
      "Lookups",
      "Lookup",
      "Postcode Lookups",
      "Postcode",
      "Output Area",
      "Super Output Area",
      "Local Authority District",
      "OA",
      "LSOA",
      "MSOA",
      "LAD",
      "UK",
      "ZIP File",
      "PCD_OA_LSOA_MSOA_LAD",
      "LUP_PCD_OA_LSOA_MSOA_LAD",
      "latest_lookups",
      "Latest Lookups",
      "2026",
      "FEB_2026"
    ],
    "title": "Postcode to OA (2021) to LSOA to MSOA to LAD (February 2026) Best Fit Lookup in the UK",
    "type": "CSV Collection",
    "typeKeywords": [
      "CSV Collection",
      "zip"
    ],
    "url": null
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Postcode to OA (2021) to LSOA to MSOA to LAD (February 2026) Best Fit Lookup in the UK

A best-fit lookup between postcodes, 2021 Census Output Areas (OA), Lower Layer Super Output Areas (LSOA), Middle Layer Super Output Areas (MSOA) and local authority districts (LAD). Postcodes are as at February 2026 in the UK and are best-fitted by plotting the location of the postcode's mean address into the areas of the output geographies. (File size 22 MB). Field Names - PCD7, PCD8, PCDS, DOINTR, DOTERM, USERTYPE, OA21CD, LSOA21CD, MSOA21CD, LADCD, LSOA21NM, MSOA21NM, LADNM, LADNMW Field Types - All Text Field Lengths - 7, 8, 8, 8, 8, 1, 9, 9, 9, 9, 55, 65, 45, 45

Native identifier: `c01336febabe4c76ac14fbe71dbb99e1`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/c01336febabe4c76ac14fbe71dbb99e1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
