---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2FRM066%2Feditions%2F2021%2Fversions%2F1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Living arrangements by age - Household Reference Person",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/RM066/editions/2021/versions/1",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/RM066/editions/2021/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "living_arrangements_10a,resident_age_5c",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/87",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2087",
      "normalisedRecordSha256": "75db5e4426d42838a49ba430a13f7c8fbca8b6d17bdde63b54b50ef2a30f727b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/RM066/editions/2021/versions/1"
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
    "dataset_id": "RM066",
    "dimensions": [
      {
        "label": "Living arrangements",
        "name": "living_arrangements_10a",
        "raw_label": "Living arrangements (10 categories)"
      },
      {
        "label": "Age (C)",
        "name": "resident_age_5c",
        "raw_label": "Age (C) (5 categories)"
      }
    ],
    "edition": "2021",
    "id": "/datasets/RM066/editions/2021/versions/1",
    "keywords": [
      "ltla",
      "living_arrangements_10a,resident_age_5c"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2023-04-18T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/RM066/editions/2021/versions/1",
    "sourceEvidence": {
      "pointer": "/items/87",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "This dataset provides Census 2021 estimates that classify the Household Reference Persons aged 16 years and over in England and Wales by living arrangements and by age. The estimates are as at Census Day, 21 March 2021.",
    "title": "Living arrangements by age - Household Reference Person",
    "topics": [
      "6646"
    ],
    "type": "dataset_landing_page",
    "uri": "/datasets/RM066/editions/2021/versions/1"
  }
}
---

# Living arrangements by age - Household Reference Person

ONS website catalogue metadata.

Native identifier: `/datasets/RM066/editions/2021/versions/1`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/RM066/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
