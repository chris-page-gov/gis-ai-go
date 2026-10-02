---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fdeathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath%2F20072011",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of deaths where S. aureus and MRSA were mentioned on the death certificate by place of death",
  "description": "Number of deaths where S. aureus and MRSA were mentioned on the death certificate: by place of death.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Meticillin-resistant",
    "Staphylococcus",
    "Aureus",
    "mortality",
    "infections",
    "hospital",
    "nursing",
    "deaths",
    "of",
    "older",
    "people",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/947",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/947",
      "normalisedRecordSha256": "94bbfddfb3f8ea1e44bf2169f2150347522ea345e8602fb3cbc8a6a633c3b465",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011"
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
    "releaseVersion": "2007 - 2011"
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
    "edition": "2007 - 2011",
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011",
    "keywords": [
      "Meticillin-resistant",
      "Staphylococcus",
      "Aureus",
      "mortality",
      "infections",
      "hospital",
      "nursing",
      "deaths",
      "of",
      "older",
      "people"
    ],
    "meta_description": "Number of deaths where S. aureus and MRSA were mentioned on the death certificate: by place of death.",
    "nativeIdentityField": "uri",
    "release_date": "2014-09-02T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011",
    "sourceEvidence": {
      "pointer": "/items/947",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Number of deaths where S. aureus and MRSA were mentioned on the death certificate: by place of death.",
    "title": "Number of deaths where S. aureus and MRSA were mentioned on the death certificate by place of death",
    "topics": [
      "7131",
      "2998",
      "9581"
    ],
    "type": "dataset",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011"
  }
}
---

# Number of deaths where S. aureus and MRSA were mentioned on the death certificate by place of death

Number of deaths where S. aureus and MRSA were mentioned on the death certificate: by place of death.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingmrsanumberofdeathswheresaureusandmrsawerementionedonthedeathcertificatebyplaceofdeath/20072011)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
