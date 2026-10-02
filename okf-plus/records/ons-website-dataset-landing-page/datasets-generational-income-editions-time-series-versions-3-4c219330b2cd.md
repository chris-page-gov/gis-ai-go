---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2Fgenerational-income%2Feditions%2Ftime-series%2Fversions%2F3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Generational income: The effects of taxes and benefits",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/generational-income/editions/time-series/versions/3",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/generational-income/editions/time-series/versions/3",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "taxes",
    "benefits,generational income",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/449",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1449",
      "normalisedRecordSha256": "e3a8c919a1d92db68b968e8637f7c8d7c1ce7e58ab77366fde45c97709079736",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/generational-income/editions/time-series/versions/3"
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
    "releaseVersion": "time-series"
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
    "dataset_id": "generational-income",
    "edition": "time-series",
    "id": "/datasets/generational-income/editions/time-series/versions/3",
    "keywords": [
      "taxes",
      "benefits,generational income"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2022-09-15T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/generational-income/editions/time-series/versions/3",
    "sourceEvidence": {
      "pointer": "/items/449",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "The effects of direct and indirect taxation and benefits received in cash or kind on household income, across the generations and by age. This data is estimated by combining multiple years of the Living Costs and Food Survey from 1978 to financial year ending March 2017 and the Household Finances Statistics, from financial year ending 2018 to financial year ending 2021 with the exception of 1979 and 1981. All financial amounts are adjusted for inflation using the Consumer Prices Index including owner occupiers’ housing costs (CPIH) excluding Council Tax, to their financial year ending March 2018. For example, the mean disposable income for those aged 35 and born in the 1970’s (£35,752) is estimated by taking the average (in real terms) of the household disposable income for these people across the combined dataset.",
    "title": "Generational income: The effects of taxes and benefits",
    "type": "dataset_landing_page",
    "uri": "/datasets/generational-income/editions/time-series/versions/3"
  }
}
---

# Generational income: The effects of taxes and benefits

ONS website catalogue metadata.

Native identifier: `/datasets/generational-income/editions/time-series/versions/3`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/generational-income/editions/time-series/versions/3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
