---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Feconomicoutputandproductivity%2Foutput%2Ftimeseries%2Fk2q3%2Fdiop",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "CF:Manufacture of Basic Pharm Prods & Pharm Preparations: CVM: 3mo3m gr",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/economicoutputandproductivity/output/timeseries/k2q3/diop",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k2q3/diop",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=8000",
      "retrievedAt": "2026-10-02T07:59:05.675884Z",
      "responseSha256": "160b0ad7e0528f4ac3ab64af3a3b4ec94a10819372d5f5b143e5494713f3cb89",
      "sourcePointer": "/items/788",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/8788",
      "normalisedRecordSha256": "bd9195d057332f2c59b449a65551751016748041e1deafec19238ed6368e984d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k2q3/diop"
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
    "cdid": "K2Q3",
    "dataset_id": "DIOP",
    "edition": "",
    "id": "/economy/economicoutputandproductivity/output/timeseries/k2q3/diop",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-10T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k2q3/diop",
    "sourceEvidence": {
      "pointer": "/items/788",
      "retrievedAt": "2026-10-02T07:59:05.675884Z",
      "sha256": "160b0ad7e0528f4ac3ab64af3a3b4ec94a10819372d5f5b143e5494713f3cb89",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=8000"
    },
    "summary": "",
    "title": "CF:Manufacture of Basic Pharm Prods & Pharm Preparations: CVM: 3mo3m gr",
    "topics": [
      "1245",
      "2621",
      "6625"
    ],
    "type": "timeseries",
    "uri": "/economy/economicoutputandproductivity/output/timeseries/k2q3/diop"
  }
}
---

# CF:Manufacture of Basic Pharm Prods & Pharm Preparations: CVM: 3mo3m gr

ONS website catalogue metadata.

Native identifier: `/economy/economicoutputandproductivity/output/timeseries/k2q3/diop`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k2q3/diop)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
