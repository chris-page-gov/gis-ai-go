---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fresearchanddevelopmentexpenditure%2Fdatasets%2Fbusinessenterpriseresearchanddevelopmenttimeseriesspreadsheet",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Business enterprise research and development time series",
  "description": "Annual breakdown of research and development spending and employment by UK businesses across different market sectors.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "R&D",
    "intramural",
    "region",
    "BERD",
    "science and technology",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/321",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/321",
      "normalisedRecordSha256": "b88c934c8befc7a5b15f6e24783bd488c2d3258f624c8c9a41c9c5c60e07d06d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet"
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
    "dataset_id": "BERD",
    "edition": "",
    "id": "/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet",
    "keywords": [
      "R&D",
      "intramural",
      "region",
      "BERD",
      "science and technology"
    ],
    "meta_description": "Annual breakdown of research and development spending and employment by UK businesses across different market sectors.",
    "nativeIdentityField": "uri",
    "release_date": "2021-11-19T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet",
    "sourceEvidence": {
      "pointer": "/items/321",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Annual breakdown of research and development spending and employment by UK businesses across different market sectors.",
    "title": "Business enterprise research and development time series",
    "topics": [
      "1245",
      "9828",
      "8183"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet"
  }
}
---

# Business enterprise research and development time series

Annual breakdown of research and development spending and employment by UK businesses across different market sectors.

Native identifier: `/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/researchanddevelopmentexpenditure/datasets/businessenterpriseresearchanddevelopmenttimeseriesspreadsheet)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
