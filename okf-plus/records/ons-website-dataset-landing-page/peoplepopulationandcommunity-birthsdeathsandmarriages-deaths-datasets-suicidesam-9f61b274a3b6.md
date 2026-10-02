---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fsuicidesamongpeoplediagnosedwithseverehealthconditionsengland",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Suicides among people diagnosed with severe health conditions, England",
  "description": "Deaths due to suicide in England and the rate per 100,000 people by days since diagnosis, comparing patients with selected health conditions with matched controls. Includes Hospital Episode Statistics (HES) diagnosis and deaths that occurred between 1 January 2017 and 31 March 2020.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "terminal illness",
    "assisted suicide",
    "terminally ill",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/434",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3434",
      "normalisedRecordSha256": "63b80e356977dc5cf49c4223e85d525b65f709ec56831b3ecd2d0b0ff079433f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland",
    "keywords": [
      "terminal illness",
      "assisted suicide",
      "terminally ill"
    ],
    "meta_description": "Deaths due to suicide in England and the rate per 100,000 people by days since diagnosis, comparing patients with selected health conditions with matched controls. Includes Hospital Episode Statistics (HES) diagnosis and deaths that occurred between 1 January 2017 and 31 March 2020.",
    "nativeIdentityField": "uri",
    "release_date": "2022-04-19T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland",
    "sourceEvidence": {
      "pointer": "/items/434",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Deaths due to suicide in England and the rate per 100,000 people by days since diagnosis, comparing patients with selected health conditions with matched controls. Includes Hospital Episode Statistics (HES) diagnosis and deaths that occurred between 1 January 2017 and 31 March 2020.",
    "title": "Suicides among people diagnosed with severe health conditions, England",
    "topics": [
      "9581",
      "7131",
      "2998"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland"
  }
}
---

# Suicides among people diagnosed with severe health conditions, England

Deaths due to suicide in England and the rate per 100,000 people by days since diagnosis, comparing patients with selected health conditions with matched controls. Includes Hospital Episode Statistics (HES) diagnosis and deaths that occurred between 1 January 2017 and 31 March 2020.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/suicidesamongpeoplediagnosedwithseverehealthconditionsengland)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
