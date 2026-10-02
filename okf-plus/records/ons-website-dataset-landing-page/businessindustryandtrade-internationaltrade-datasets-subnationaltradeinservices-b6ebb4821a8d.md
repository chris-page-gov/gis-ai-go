---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Finternationaltrade%2Fdatasets%2Fsubnationaltradeinservices",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Subnational trade in services",
  "description": "Experimental estimated value of exports, imports and balance of services for 2020 for ITL1, ITL2, ITL3 and city regions, including industry and partner country.",
  "nativeIdentifier": "/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "subnational",
    "trade",
    "region",
    "industry",
    "services",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/417",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3417",
      "normalisedRecordSha256": "fe8fa17e5188f57c0bdcdf8227986e2f623d7ac92c299dddbc2e39a5a1ca19a4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices"
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
    "id": "/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices",
    "keywords": [
      "subnational",
      "trade",
      "region",
      "industry",
      "services"
    ],
    "meta_description": "Experimental estimated value of exports, imports and balance of services for 2020 for ITL1, ITL2, ITL3 and city regions, including industry and partner country.",
    "nativeIdentityField": "uri",
    "release_date": "2025-08-05T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices",
    "sourceEvidence": {
      "pointer": "/items/417",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Estimated value of exports, imports and balance of services for 2023 for International Territorial Levels (ITLs) 1, 2 and 3, and city regions. Includes EU and non-EU split along with data for top 20 partner countries. These are official statistics in development.",
    "title": "Subnational trade in services",
    "topics": [
      "9658",
      "5631"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices"
  }
}
---

# Subnational trade in services

Experimental estimated value of exports, imports and balance of services for 2020 for ITL1, ITL2, ITL3 and city regions, including industry and partner country.

Native identifier: `/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/subnationaltradeinservices)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
