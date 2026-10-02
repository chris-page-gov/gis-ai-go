---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Femploymentandlabourmarket%2Fpeoplenotinwork%2Fredundancies%2Fdatasets%2Fredundancieslevelsandratesseasonallyadjustedred01sa%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Redundancies levels and rates (seasonally adjusted): RED01 SA",
  "description": "Number of people (levels), men and women made redundant and redundancy rates, seasonally adjusted.",
  "nativeIdentifier": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "responseSha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "sourcePointer": "/items/371",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1371",
      "normalisedRecordSha256": "ba46a376e31dbbffb4d0a79ec15d03093d43b2d696e5b2ba46e3473443fd0416",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current"
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
    "id": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current",
    "keywords": [],
    "meta_description": "Number of people (levels), men and women made redundant and redundancy rates, seasonally adjusted.",
    "nativeIdentityField": "uri",
    "release_date": "2016-08-16T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current",
    "sourceEvidence": {
      "pointer": "/items/371",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Number of people (levels), men and women made redundant and redundancy rates, seasonally adjusted.",
    "title": "Redundancies levels and rates (seasonally adjusted): RED01 SA",
    "topics": [
      "7583",
      "5687",
      "4361"
    ],
    "type": "dataset",
    "uri": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current"
  }
}
---

# Redundancies levels and rates (seasonally adjusted): RED01 SA

Number of people (levels), men and women made redundant and redundancy rates, seasonally adjusted.

Native identifier: `/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundancieslevelsandratesseasonallyadjustedred01sa/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
