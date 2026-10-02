---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fdeathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of Deaths where Clostridium difficile was Mentioned on the Death Certificate - By Place of Death",
  "description": "Number of deaths where Clostridium difficile was mentioned on the death certificate: by place of death, 2006–10 (provisional).",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "mortality",
    "infections",
    "hospital",
    "nursing",
    "deaths",
    "of",
    "older",
    "people",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/503",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2503",
      "normalisedRecordSha256": "d540bf6c01728c95931ef7ddaf10f09829a827b3f6dbb20658e00987aecf9e67",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath",
    "keywords": [
      "mortality",
      "infections",
      "hospital",
      "nursing",
      "deaths",
      "of",
      "older",
      "people"
    ],
    "meta_description": "Number of deaths where Clostridium difficile was mentioned on the death certificate: by place of death, 2006–10 (provisional).",
    "nativeIdentityField": "uri",
    "release_date": "2014-09-02T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath",
    "sourceEvidence": {
      "pointer": "/items/503",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Number of deaths where Clostridium difficile was mentioned on the death certificate: by place of death, 2006–10 (provisional).",
    "title": "Number of Deaths where Clostridium difficile was Mentioned on the Death Certificate - By Place of Death",
    "topics": [
      "9581",
      "7131",
      "2998"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath"
  }
}
---

# Number of Deaths where Clostridium difficile was Mentioned on the Death Certificate - By Place of Death

Number of deaths where Clostridium difficile was mentioned on the death certificate: by place of death, 2006–10 (provisional).

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingclostridiumdifficilenumberofdeathswhereclostridiumdifficilewasmentionedonthedeathcertificatebyplaceofdeath)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
