---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fsatelliteaccounts%2Fdatasets%2Fhouseholdsatelliteaccountfullukaccounts2005to2014",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Household satellite account, UK",
  "description": "The Household Satellite Account (HHSA) presents estimates of unpaid home production in the UK. It captures a range of non-market services produced by households which are not included in the core UK National Accounts.",
  "nativeIdentifier": "/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "home production",
    "non-market",
    "unpaid work",
    "gross value added",
    "national accounts",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/737",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1737",
      "normalisedRecordSha256": "234d5e8db1e62d0153218a1a845d36ea12a4d6a9f001c439936b60424cb34a51",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014"
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
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": ""
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Website and API representations are retained separately; matching titles do not prove equivalence.",
    "Release dates do not establish the period covered by statistical observations."
  ],
  "details": {
    "canonical_topic": "",
    "cdid": "",
    "dataset_id": "",
    "edition": "",
    "id": "/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014",
    "keywords": [
      "home production",
      "non-market",
      "unpaid work",
      "gross value added",
      "national accounts"
    ],
    "meta_description": "The Household Satellite Account (HHSA) presents estimates of unpaid home production in the UK. It captures a range of non-market services produced by households which are not included in the core UK National Accounts.",
    "nativeIdentityField": "uri",
    "release_date": "2025-12-05T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014",
    "sourceEvidence": {
      "pointer": "/items/737",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Annual data on the output, intermediate consumption and gross value added of home-produced services.",
    "title": "Household satellite account, UK",
    "topics": [
      "4176",
      "1245",
      "2735"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014"
  }
}
---

# Household satellite account, UK

The Household Satellite Account (HHSA) presents estimates of unpaid home production in the UK. It captures a range of non-market services produced by households which are not included in the core UK National Accounts.

Native identifier: `/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/householdsatelliteaccountfullukaccounts2005to2014)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
