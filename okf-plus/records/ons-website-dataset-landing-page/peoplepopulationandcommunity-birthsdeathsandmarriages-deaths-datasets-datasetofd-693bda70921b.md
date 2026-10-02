---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fdatasetofdualcodeddataicd10nchsandiris",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)",
  "description": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/779",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/779",
      "normalisedRecordSha256": "8b0c88b56989a506c65db387e8d353ce18d2f82a578b11fac29a7b1ab4b414d6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris",
    "keywords": [],
    "meta_description": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
    "nativeIdentityField": "uri",
    "release_date": "2014-08-07T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris",
    "sourceEvidence": {
      "pointer": "/items/779",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
    "title": "Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)",
    "topics": [
      "7131",
      "2998",
      "9581"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris"
  }
}
---

# Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)

Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
