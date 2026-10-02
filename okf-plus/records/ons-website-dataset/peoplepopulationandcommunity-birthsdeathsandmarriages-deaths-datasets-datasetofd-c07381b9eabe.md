---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fdatasetofdualcodeddataicd10nchsandiris%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)",
  "description": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/342",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/342",
      "normalisedRecordSha256": "41ec61d35ed825aeae4cb17ba1e0d17470b4ac6e7b0e75db3609af2b823b9887",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current"
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
    "releaseVersion": "Current"
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
    "edition": "Current",
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current",
    "keywords": [],
    "meta_description": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
    "nativeIdentityField": "uri",
    "release_date": "2014-08-07T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current",
    "sourceEvidence": {
      "pointer": "/items/342",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.",
    "title": "Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)",
    "topics": [
      "7131",
      "2998",
      "9581"
    ],
    "type": "dataset",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current"
  }
}
---

# Dataset of dual coded data, ICD-10 v2010 (NCHS) and ICD-10 v2013 (IRIS)

Dataset of dual coded data, including the selected underlying cause of death every mentioned condition on the death certificate coded using both ICD-10 (NCHS) and ICD-10 (IRIS), by age and sex.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/datasetofdualcodeddataicd10nchsandiris/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
