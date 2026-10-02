---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Femploymentandlabourmarket%2Fpeopleinwork%2Fworkplacepensions%2Fdatasets%2Fannualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7%2F2010revised",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Employee Contribution Bands by Occupation and by Pension Type (P7)",
  "description": "Estimates of the proportion of employees in employee’s contribution bands by 2 digit Standard Occupation Classification 2010 and by contracted out status and pension type.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ashe",
    "scheme membership",
    "defined benefit",
    "occupational",
    "employer contribution rates",
    "ashe",
    "scheme",
    "membership",
    "defined",
    "benefit",
    "occupational",
    "employer",
    "contribution",
    "rates",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/456",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/456",
      "normalisedRecordSha256": "e54cdb2164628a7b14eb36981c33070ed3fac7be0a469a1a22de752daa2d3c36",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised"
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
    "releaseVersion": "2010 (revised)"
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
    "edition": "2010 (revised)",
    "id": "/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised",
    "keywords": [
      "ashe",
      "scheme membership",
      "defined benefit",
      "occupational",
      "employer contribution rates",
      "ashe",
      "scheme",
      "membership",
      "defined",
      "benefit",
      "occupational",
      "employer",
      "contribution",
      "rates"
    ],
    "meta_description": "Estimates of the proportion of employees in employee’s contribution bands by 2 digit Standard Occupation Classification 2010 and by contracted out status and pension type.",
    "nativeIdentityField": "uri",
    "release_date": "2015-02-26T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised",
    "sourceEvidence": {
      "pointer": "/items/456",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Estimates of the proportion of employees in employee’s contribution bands by 2 digit Standard Occupation Classification 2010 and by contracted out status and pension type.",
    "title": "Employee Contribution Bands by Occupation and by Pension Type (P7)",
    "topics": [
      "5687",
      "2114",
      "4263"
    ],
    "type": "dataset",
    "uri": "/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised"
  }
}
---

# Employee Contribution Bands by Occupation and by Pension Type (P7)

Estimates of the proportion of employees in employee’s contribution bands by 2 digit Standard Occupation Classification 2010 and by contracted out status and pension type.

Native identifier: `/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacepensions/datasets/annualsurveyofhoursandearningspensiontablesemployeecontributionbandsbyoccupationandbypensiontypep7/2010revised)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
