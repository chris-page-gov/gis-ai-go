---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Femploymentandlabourmarket%2Fpeoplenotinwork%2Foutofworkbenefits%2Fdatasets%2Fjobseekersallowancebyageanddurationben03%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Jobseeker's Allowance by age and duration: BEN03",
  "description": "Jobseeker’s Allowance by age and duration.",
  "nativeIdentifier": "/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current",
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
      "sourcePointer": "/items/801",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/801",
      "normalisedRecordSha256": "e49dd78516bd9613ce77d8fcec83bdf6c1b5765d26e5fe37a9483b4b19b9dca8",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current"
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
    "id": "/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current",
    "keywords": [],
    "meta_description": "Jobseeker’s Allowance by age and duration.",
    "nativeIdentityField": "uri",
    "release_date": "2016-08-16T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current",
    "sourceEvidence": {
      "pointer": "/items/801",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Jobseeker’s Allowance by age and duration.",
    "title": "Jobseeker's Allowance by age and duration: BEN03",
    "topics": [
      "5687",
      "4361",
      "3692"
    ],
    "type": "dataset",
    "uri": "/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current"
  }
}
---

# Jobseeker's Allowance by age and duration: BEN03

Jobseeker’s Allowance by age and duration.

Native identifier: `/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/outofworkbenefits/datasets/jobseekersallowancebyageanddurationben03/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
