---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Fearningsandworkinghours%2Fdatasets%2Femploymentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Employments from Pay As You Earn Real Time Information: ad hoc estimates of payrolled employees by NUTS1 region and nationality",
  "description": "Pay As You Earn (PAYE) Real Time Information (RTI) estimates of employees from UK, EU and rest of the world, by UK region, seasonally adjusted. Ad hoc monthly data, nationality determined using the Migrant Worker Scan. Experimental Statistics.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "migrant worker scan",
    "workforce",
    "country of origin",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/107",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1107",
      "normalisedRecordSha256": "8d60d5c1e19073ec87a5887c4417c941027d7a4796591fe03938bdde304a941c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted"
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
    "id": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted",
    "keywords": [
      "migrant worker scan",
      "workforce",
      "country of origin"
    ],
    "meta_description": "Pay As You Earn (PAYE) Real Time Information (RTI) estimates of employees from UK, EU and rest of the world, by UK region, seasonally adjusted. Ad hoc monthly data, nationality determined using the Migrant Worker Scan. Experimental Statistics.",
    "nativeIdentityField": "uri",
    "release_date": "2023-03-23T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted",
    "sourceEvidence": {
      "pointer": "/items/107",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Pay As You Earn (PAYE) Real Time Information (RTI) estimates of employees from UK, EU and rest of the world, by UK region, seasonally adjusted. Ad hoc monthly data, nationality determined using the Migrant Worker Scan. Experimental Statistics.",
    "title": "Employments from Pay As You Earn Real Time Information: ad hoc estimates of payrolled employees by NUTS1 region and nationality",
    "topics": [
      "2114",
      "8817",
      "5687"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted"
  }
}
---

# Employments from Pay As You Earn Real Time Information: ad hoc estimates of payrolled employees by NUTS1 region and nationality

Pay As You Earn (PAYE) Real Time Information (RTI) estimates of employees from UK, EU and rest of the world, by UK region, seasonally adjusted. Ad hoc monthly data, nationality determined using the Migrant Worker Scan. Experimental Statistics.

Native identifier: `/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/employmentsfrompayasyouearnrealtimeinformationadhocestimatesofpayrolledemployeesbynuts1regionandnationalityseasonallyadjusted)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
