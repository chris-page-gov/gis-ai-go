---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Femploymentandemployeetypes%2Fdatasets%2Foccupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Occupations of those in employment, by local area, working pattern, employment status and disability status, England and Wales, Census 2021",
  "description": "Occupation data for people aged 16 years and older and in employment, as recorded on Census 2021, to a detailed level (4-digit Standard Occupational Classification). Tables included for counts and percentages by local authority district and upper tier local authority, full-time or part-time work, and employees compared with those self-employed.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "district",
    "work",
    "job",
    "local jobs",
    "part-time",
    "self-employment",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/619",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2619",
      "normalisedRecordSha256": "5d1420d7b5511a594ad627b116231b33923ce4433485f4ae0a97228debb4f8c0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021"
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
    "id": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021",
    "keywords": [
      "district",
      "work",
      "job",
      "local jobs",
      "part-time",
      "self-employment"
    ],
    "meta_description": "Occupation data for people aged 16 years and older and in employment, as recorded on Census 2021, to a detailed level (4-digit Standard Occupational Classification). Tables included for counts and percentages by local authority district and upper tier local authority, full-time or part-time work, and employees compared with those self-employed.",
    "nativeIdentityField": "uri",
    "release_date": "2023-05-30T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021",
    "sourceEvidence": {
      "pointer": "/items/619",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Census 2021 occupation data for people aged 16 years and older and in employment, to a detailed level (4-digit Standard Occupational Classification). Tables include occupation by local authority district and upper tier local authority, full-time or part-time work, disability status, and employees compared with those self-employed.",
    "title": "Occupations of those in employment, by local area, working pattern, employment status and disability status, England and Wales, Census 2021",
    "topics": [
      "5687",
      "2114",
      "9243"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021"
  }
}
---

# Occupations of those in employment, by local area, working pattern, employment status and disability status, England and Wales, Census 2021

Occupation data for people aged 16 years and older and in employment, as recorded on Census 2021, to a detailed level (4-digit Standard Occupational Classification). Tables included for counts and percentages by local authority district and upper tier local authority, full-time or part-time work, and employees compared with those self-employed.

Native identifier: `/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/occupationsofthoseinemploymentbylocalareaworkingpatternemploymentstatusanddisabilitystatusenglandandwalescensus2021)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
