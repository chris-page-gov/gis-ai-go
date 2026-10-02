---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Flabourproductivity%2Fdatasets%2Fhomeworkingintheukworkfromhomestatus",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Homeworking in the UK, work from home status",
  "description": "Experimental estimates from the Annual Population Survey for homeworking in the UK, including breakdowns by sex, full-time or part-time, ethnicity, occupation, industry, qualifications, hours worked, pay and sickness absence among others. Includes regression outputs on the different outcomes for homeworkers.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "home working",
    "bonuses",
    "productivity",
    "promotion",
    "remote working",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/662",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1662",
      "normalisedRecordSha256": "6d024c8c3b88372c29edf98b5202ccf51bd85fb72cc85b578eff05b5262406b9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus"
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
    "id": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus",
    "keywords": [
      "home working",
      "bonuses",
      "productivity",
      "promotion",
      "remote working"
    ],
    "meta_description": "Experimental estimates from the Annual Population Survey for homeworking in the UK, including breakdowns by sex, full-time or part-time, ethnicity, occupation, industry, qualifications, hours worked, pay and sickness absence among others. Includes regression outputs on the different outcomes for homeworkers.",
    "nativeIdentityField": "uri",
    "release_date": "2021-04-18T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus",
    "sourceEvidence": {
      "pointer": "/items/662",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Experimental estimates from the Annual Population Survey for homeworking in the UK, including breakdowns by sex, full-time or part-time, ethnicity, occupation, industry, qualifications, hours worked, pay and sickness absence among others. Includes regression outputs on the different outcomes for homeworkers.",
    "title": "Homeworking in the UK, work from home status",
    "topics": [
      "5687",
      "2114",
      "6663"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus"
  }
}
---

# Homeworking in the UK, work from home status

Experimental estimates from the Annual Population Survey for homeworking in the UK, including breakdowns by sex, full-time or part-time, ethnicity, occupation, industry, qualifications, hours worked, pay and sickness absence among others. Includes regression outputs on the different outcomes for homeworkers.

Native identifier: `/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/homeworkingintheukworkfromhomestatus)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
