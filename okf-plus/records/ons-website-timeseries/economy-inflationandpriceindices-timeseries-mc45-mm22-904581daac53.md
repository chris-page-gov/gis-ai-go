---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Finflationandpriceindices%2Ftimeseries%2Fmc45%2Fmm22",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "6107320500: GSI (excl. CCL) - Inputs for Manufacture of Other Chemical products",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/inflationandpriceindices/timeseries/mc45/mm22",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/mc45/mm22",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "timeseries"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:57.811101Z",
      "responseSha256": "22932aba91e4c035fde2020af198daa96c384d76c08d4e23d85ecf4f2d28f649",
      "sourcePointer": "/items/376",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/2376",
      "normalisedRecordSha256": "7f9ff86f098abae5ddf6f3048d48450c341428670a32e5b6c552dfd45405e377",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/mc45/mm22"
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
    "cdid": "MC45",
    "dataset_id": "MM22",
    "edition": "",
    "id": "/economy/inflationandpriceindices/timeseries/mc45/mm22",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2020-10-20T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/mc45/mm22",
    "sourceEvidence": {
      "pointer": "/items/376",
      "retrievedAt": "2026-10-02T07:58:57.811101Z",
      "sha256": "22932aba91e4c035fde2020af198daa96c384d76c08d4e23d85ecf4f2d28f649",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "",
    "title": "6107320500: GSI (excl. CCL) - Inputs for Manufacture of Other Chemical products",
    "topics": [
      "4972",
      "1245"
    ],
    "type": "timeseries",
    "uri": "/economy/inflationandpriceindices/timeseries/mc45/mm22"
  }
}
---

# 6107320500: GSI (excl. CCL) - Inputs for Manufacture of Other Chemical products

ONS website catalogue metadata.

Native identifier: `/economy/inflationandpriceindices/timeseries/mc45/mm22`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/mc45/mm22)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
