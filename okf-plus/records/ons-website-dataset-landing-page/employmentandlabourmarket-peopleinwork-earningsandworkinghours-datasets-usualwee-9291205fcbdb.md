---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Fearningsandworkinghours%2Fdatasets%2Fusualweeklyhoursworkednotseasonallyadjustedhour02nsa",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "HOUR02 NSA: Usual weekly hours worked (not seasonally adjusted)",
  "description": "Usual weekly hours worked including by sex, full-time, part-time and second jobs, UK, rolling three-monthly figures published monthly, non-seasonally adjusted. Labour Force Survey.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "hours worked per week",
    "total hours worked",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/528",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1528",
      "normalisedRecordSha256": "99c5dc4d0be37403571ae669ce0c8dfa44c6f3d8ed7fd432bf3c690ac7f487bf",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa"
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
    "id": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa",
    "keywords": [
      "hours worked per week",
      "total hours worked"
    ],
    "meta_description": "Usual weekly hours worked including by sex, full-time, part-time and second jobs, UK, rolling three-monthly figures published monthly, non-seasonally adjusted. Labour Force Survey.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa",
    "sourceEvidence": {
      "pointer": "/items/528",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Usual weekly hours worked including by sex, full-time, part-time and second jobs, UK, rolling three-monthly figures published monthly, non-seasonally adjusted. Labour Force Survey. These are official statistics.",
    "title": "HOUR02 NSA: Usual weekly hours worked (not seasonally adjusted)",
    "topics": [
      "5687",
      "2114",
      "8817"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa"
  }
}
---

# HOUR02 NSA: Usual weekly hours worked (not seasonally adjusted)

Usual weekly hours worked including by sex, full-time, part-time and second jobs, UK, rolling three-monthly figures published monthly, non-seasonally adjusted. Labour Force Survey.

Native identifier: `/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/usualweeklyhoursworkednotseasonallyadjustedhour02nsa)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
