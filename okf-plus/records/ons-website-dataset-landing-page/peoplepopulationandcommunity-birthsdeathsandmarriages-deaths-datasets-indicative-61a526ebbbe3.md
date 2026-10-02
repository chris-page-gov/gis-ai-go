---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Findicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Indicative comparability ratios for underlying cause of death by ICD-10 chapter and leading cause of death between MUSE 5.5 and MUSE 5.8",
  "description": "Underlying cause of death by ICD-10 chapter and leading cause of death in a sample of 42,413 death registrations from 2017 in England and Wales, coded through MUSE 5.5 and MUSE 5.8.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Mortality",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/844",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1844",
      "normalisedRecordSha256": "5b771c3e13f1b03c7f25f278a3fcc66e6a5078679d7c207b3e3302e5300da601",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58",
    "keywords": [
      "Mortality"
    ],
    "meta_description": "Underlying cause of death by ICD-10 chapter and leading cause of death in a sample of 42,413 death registrations from 2017 in England and Wales, coded through MUSE 5.5 and MUSE 5.8.",
    "nativeIdentityField": "uri",
    "release_date": "2022-01-07T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58",
    "sourceEvidence": {
      "pointer": "/items/844",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Underlying cause of death by ICD-10 chapter and leading cause of death in a sample of 42,413 death registrations from 2017 in England and Wales, coded through MUSE 5.5 and MUSE 5.8.",
    "title": "Indicative comparability ratios for underlying cause of death by ICD-10 chapter and leading cause of death between MUSE 5.5 and MUSE 5.8",
    "topics": [
      "9581",
      "7131",
      "2998"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58"
  }
}
---

# Indicative comparability ratios for underlying cause of death by ICD-10 chapter and leading cause of death between MUSE 5.5 and MUSE 5.8

Underlying cause of death by ICD-10 chapter and leading cause of death in a sample of 42,413 death registrations from 2017 in England and Wales, coded through MUSE 5.5 and MUSE 5.8.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/indicativecomparabilityratiosforunderlyingcauseofdeathbyicd10chapterandleadingcauseofdeathbetweenmuse55andmuse58)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
