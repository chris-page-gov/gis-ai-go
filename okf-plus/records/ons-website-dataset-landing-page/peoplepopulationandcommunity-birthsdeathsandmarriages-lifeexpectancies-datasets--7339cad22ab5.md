---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Flifeexpectancies%2Fdatasets%2Flifeexpectancyincarehomesenglandandwales",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Life expectancy in care homes, England and Wales",
  "description": "The average number of years people aged 65 and over who are living in care homes are expected to live beyond their current age in England and Wales, 2011 to 2012. Classified as Experimental Statistics.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Care home",
    "care residents",
    "life expectancy",
    "survival",
    "mortality",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/74",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2074",
      "normalisedRecordSha256": "c8e6499023228b655a8ad22e60ba902471c9d696526bcee0ec47febb2579d6e6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales",
    "keywords": [
      "Care home",
      "care residents",
      "life expectancy",
      "survival",
      "mortality"
    ],
    "meta_description": "The average number of years people aged 65 and over who are living in care homes are expected to live beyond their current age in England and Wales, 2011 to 2012. Classified as Experimental Statistics.",
    "nativeIdentityField": "uri",
    "release_date": "2023-03-16T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales",
    "sourceEvidence": {
      "pointer": "/items/74",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "The average number of years care home residents aged 65 years and over are expected to live beyond their current age in England and Wales. Classified as Experimental Statistics.",
    "title": "Life expectancy in care homes, England and Wales",
    "topics": [
      "6788",
      "9581",
      "7131"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales"
  }
}
---

# Life expectancy in care homes, England and Wales

The average number of years people aged 65 and over who are living in care homes are expected to live beyond their current age in England and Wales, 2011 to 2012. Classified as Experimental Statistics.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/datasets/lifeexpectancyincarehomesenglandandwales)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
