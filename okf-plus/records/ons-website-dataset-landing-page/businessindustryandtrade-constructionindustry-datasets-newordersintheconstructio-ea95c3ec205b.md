---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fconstructionindustry%2Fdatasets%2Fnewordersintheconstructionindustry",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "New orders in the construction industry",
  "description": "Quarterly new orders at current price and chained volume measures, seasonally adjusted by public and private sector. Quarterly non–seasonally adjusted type of work and regional data.",
  "nativeIdentifier": "/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "building",
    "infrastructure",
    "industrial",
    "commercial",
    "housing",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/470",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2470",
      "normalisedRecordSha256": "95f2e5fd9606afcb0eb98d81691ed4be8eac24e0545c7093b9c448b42329d0e5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry"
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
    "id": "/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry",
    "keywords": [
      "building",
      "infrastructure",
      "industrial",
      "commercial",
      "housing"
    ],
    "meta_description": "Quarterly new orders at current price and chained volume measures, seasonally adjusted by public and private sector. Quarterly non–seasonally adjusted type of work and regional data.",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-12T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry",
    "sourceEvidence": {
      "pointer": "/items/470",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Quarterly new orders at current price and chained volume measures, seasonally adjusted by public and private sector. Quarterly non–seasonally adjusted type of work and regional data.",
    "title": "New orders in the construction industry",
    "topics": [
      "9658",
      "1346"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry"
  }
}
---

# New orders in the construction industry

Quarterly new orders at current price and chained volume measures, seasonally adjusted by public and private sector. Quarterly non–seasonally adjusted type of work and regional data.

Native identifier: `/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/newordersintheconstructionindustry)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
