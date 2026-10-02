---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2FST012%2Feditions%2F2021%2Fversions%2F2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of non-UK born short-term residents by NS-SEC",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/ST012/editions/2021/versions/2",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/ST012/editions/2021/versions/2",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "ns_sec_12a",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/531",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2531",
      "normalisedRecordSha256": "411abb43d313915912fd57f5ec33b7135c77a7e049c1cc0042775469807fd588",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/ST012/editions/2021/versions/2"
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
    "releaseVersion": "2021"
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
    "canonical_topic": "7779",
    "cdid": "",
    "dataset_id": "ST012",
    "dimensions": [
      {
        "label": "National Statistics Socio-economic Classification (NS-SeC)",
        "name": "ns_sec_12a",
        "raw_label": "National Statistics Socio-economic Classification (NS-SeC) (12 categories)"
      }
    ],
    "edition": "2021",
    "id": "/datasets/ST012/editions/2021/versions/2",
    "keywords": [
      "ltla",
      "ns_sec_12a"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2023-04-28T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/ST012/editions/2021/versions/2",
    "sourceEvidence": {
      "pointer": "/items/531",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "This dataset provides Census 2021 estimates that classify non-UK born short-term residents aged 16 years and over in England and Wales by NS-SEC. The estimates are as at Census Day, 21 March 2021. We have not adjusted these estimates to correct for non-response. Consider this when comparing results with 2011 Census short-term resident estimates.",
    "title": "Number of non-UK born short-term residents by NS-SEC",
    "topics": [
      "7755"
    ],
    "type": "dataset_landing_page",
    "uri": "/datasets/ST012/editions/2021/versions/2"
  }
}
---

# Number of non-UK born short-term residents by NS-SEC

ONS website catalogue metadata.

Native identifier: `/datasets/ST012/editions/2021/versions/2`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/ST012/editions/2021/versions/2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
