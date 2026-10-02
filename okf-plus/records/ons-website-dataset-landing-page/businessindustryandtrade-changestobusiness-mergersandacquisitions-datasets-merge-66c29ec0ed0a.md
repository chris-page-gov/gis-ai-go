---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fchangestobusiness%2Fmergersandacquisitions%2Fdatasets%2Fmergersandacquisitionsuk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Mergers and acquisitions (M&A) involving UK companies time series",
  "description": "Quarterly data on the value and number of mergers, acquisitions and disposals involving UK companies with values of £1 million or more.",
  "nativeIdentifier": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "inward",
    "outward",
    "domestic",
    "foreign companies",
    "transactions",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/309",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2309",
      "normalisedRecordSha256": "630c711cdbbf40087862e870d81104d5fb551ea30d5cf2ed29b4f47542e1cf4f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk"
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
    "dataset_id": "AM",
    "edition": "",
    "id": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk",
    "keywords": [
      "inward",
      "outward",
      "domestic",
      "foreign companies",
      "transactions"
    ],
    "meta_description": "Quarterly data on the value and number of mergers, acquisitions and disposals involving UK companies with values of £1 million or more.",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-31T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk",
    "sourceEvidence": {
      "pointer": "/items/309",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Quarterly data on the value and number of mergers, acquisitions and disposals involving UK companies with values of £1 million or more.",
    "title": "Mergers and acquisitions (M&A) involving UK companies time series",
    "topics": [
      "9658",
      "5383",
      "5163"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk"
  }
}
---

# Mergers and acquisitions (M&A) involving UK companies time series

Quarterly data on the value and number of mergers, acquisitions and disposals involving UK companies with values of £1 million or more.

Native identifier: `/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/datasets/mergersandacquisitionsuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
