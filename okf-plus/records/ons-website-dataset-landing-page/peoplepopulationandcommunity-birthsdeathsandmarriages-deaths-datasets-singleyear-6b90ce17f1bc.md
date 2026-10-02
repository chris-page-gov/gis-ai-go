---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fsingleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Single year of age and average age of death of people whose death was due to or involved coronavirus (COVID-19)",
  "description": "Single year of age and average age of death (median and mean) of persons whose death was due to COVID-19 or involved COVID-19, deaths registered in March 2020 to September 2021, England and Wales.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "cause of death",
    "death registrations",
    "deaths by local area",
    "pre-existing conditions",
    "age-standardised mortality rate",
    "coronavirus",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/363",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3363",
      "normalisedRecordSha256": "903979064376ab7a91d5a6e06facde91d2b5afb5089b75032f0e74a160b3d1e7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19",
    "keywords": [
      "cause of death",
      "death registrations",
      "deaths by local area",
      "pre-existing conditions",
      "age-standardised mortality rate",
      "coronavirus"
    ],
    "meta_description": "Single year of age and average age of death (median and mean) of persons whose death was due to COVID-19 or involved COVID-19, deaths registered in March 2020 to September 2021, England and Wales.",
    "nativeIdentityField": "uri",
    "release_date": "2023-08-22T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19",
    "sourceEvidence": {
      "pointer": "/items/363",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Provisional deaths registration data for single year of age and average age of death (median and mean) of persons whose death involved coronavirus (COVID-19), England and Wales. Includes deaths due to COVID-19 and breakdowns by sex.",
    "title": "Single year of age and average age of death of people whose death was due to or involved coronavirus (COVID-19)",
    "topics": [
      "9581",
      "7131",
      "2998"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19"
  }
}
---

# Single year of age and average age of death of people whose death was due to or involved coronavirus (COVID-19)

Single year of age and average age of death (median and mean) of persons whose death was due to COVID-19 or involved COVID-19, deaths registered in March 2020 to September 2021, England and Wales.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/singleyearofageandaverageageofdeathofpeoplewhosedeathwasduetoorinvolvedcovid19)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
