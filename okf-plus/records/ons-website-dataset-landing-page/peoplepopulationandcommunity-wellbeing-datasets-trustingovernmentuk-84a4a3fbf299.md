---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fwellbeing%2Fdatasets%2Ftrustingovernmentuk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Trust in government, UK",
  "description": "UK-specific results on people’s trust in government and institutions, opinions of public services and attitudes toward political issues. Annual data. These are official statistics in development.",
  "nativeIdentifier": "/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "distrust",
    "parliament",
    "confidence",
    "political engagement",
    "most important social issues",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/629",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3629",
      "normalisedRecordSha256": "f5733cd5634899bdc76491eccb9a797ca337c268aeb9eb7b015976be199a668e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk"
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
    "id": "/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk",
    "keywords": [
      "distrust",
      "parliament",
      "confidence",
      "political engagement",
      "most important social issues"
    ],
    "meta_description": "UK-specific results on people’s trust in government and institutions, opinions of public services and attitudes toward political issues. Annual data. These are official statistics in development.",
    "nativeIdentityField": "uri",
    "release_date": "2024-03-01T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk",
    "sourceEvidence": {
      "pointer": "/items/629",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "UK-specific results on people’s trust in government and institutions, opinions of public services and attitudes toward political issues. These are official statistics in development.",
    "title": "Trust in government, UK",
    "topics": [
      "2456",
      "9581"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk"
  }
}
---

# Trust in government, UK

UK-specific results on people’s trust in government and institutions, opinions of public services and attitudes toward political issues. Annual data. These are official statistics in development.

Native identifier: `/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/trustingovernmentuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
