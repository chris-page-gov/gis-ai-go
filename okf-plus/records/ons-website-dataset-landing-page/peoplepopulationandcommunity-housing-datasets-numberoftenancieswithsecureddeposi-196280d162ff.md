---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhousing%2Fdatasets%2Fnumberoftenancieswithsecureddepositsengland",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of tenancies with secured deposits, England",
  "description": "Data taken from three Tenancy Deposit Protection(TDP)scheme providers, to estimate the number of dwellings that have tenancies with a secured deposit held, for different geographies in England.",
  "nativeIdentifier": "/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Secured deposits",
    "Private rent",
    "tenancy",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/559",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2559",
      "normalisedRecordSha256": "c2310425d7d62714ba6981b58ab91f1bd86aa2286b5b2fe367b726c3fa646286",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland"
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
    "id": "/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland",
    "keywords": [
      "Secured deposits",
      "Private rent",
      "tenancy"
    ],
    "meta_description": "Data taken from three Tenancy Deposit Protection(TDP)scheme providers, to estimate the number of dwellings that have tenancies with a secured deposit held, for different geographies in England.",
    "nativeIdentityField": "uri",
    "release_date": "2019-03-01T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland",
    "sourceEvidence": {
      "pointer": "/items/559",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "The number of privately rented dwellings that have tenancies with secured deposits held, for subnational geographies in England.",
    "title": "Number of tenancies with secured deposits, England",
    "topics": [
      "9581",
      "5586"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland"
  }
}
---

# Number of tenancies with secured deposits, England

Data taken from three Tenancy Deposit Protection(TDP)scheme providers, to estimate the number of dwellings that have tenancies with a secured deposit held, for different geographies in England.

Native identifier: `/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/numberoftenancieswithsecureddepositsengland)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
