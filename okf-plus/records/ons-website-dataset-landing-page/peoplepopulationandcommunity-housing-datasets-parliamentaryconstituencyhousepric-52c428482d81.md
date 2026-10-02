---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhousing%2Fdatasets%2Fparliamentaryconstituencyhousepricestatisticsforsmallareas",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Parliamentary constituency House Price Statistics for Small Areas",
  "description": "Number of residential property sales and median price paid in England and Wales, by property type and parliamentary constituencies. Quarterly rolling annual data. Formerly part of HPSSA dataset 21 and HPSSA dataset 24.",
  "nativeIdentifier": "/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "house prices",
    "hpssa",
    "parliamentary constituencies",
    "house sales",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/691",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2691",
      "normalisedRecordSha256": "08c4fb64a98eeddaa7c3787697bce66442b33635afed56fb1fc80b48be4c6cb6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas"
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
    "id": "/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas",
    "keywords": [
      "house prices",
      "hpssa",
      "parliamentary constituencies",
      "house sales"
    ],
    "meta_description": "Number of residential property sales and median price paid in England and Wales, by property type and parliamentary constituencies. Quarterly rolling annual data. Formerly part of HPSSA dataset 21 and HPSSA dataset 24.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-16T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas",
    "sourceEvidence": {
      "pointer": "/items/691",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Number of residential property sales and median price paid in England and Wales, by property type and parliamentary constituencies. Quarterly rolling annual data. Formerly part of HPSSA datasets 21, 24 and 26.",
    "title": "Parliamentary constituency House Price Statistics for Small Areas",
    "topics": [
      "9581",
      "5586"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas"
  }
}
---

# Parliamentary constituency House Price Statistics for Small Areas

Number of residential property sales and median price paid in England and Wales, by property type and parliamentary constituencies. Quarterly rolling annual data. Formerly part of HPSSA dataset 21 and HPSSA dataset 24.

Native identifier: `/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/parliamentaryconstituencyhousepricestatisticsforsmallareas)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
