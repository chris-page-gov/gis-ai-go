---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicsectorfinance%2Ftimeseries%2Fjw27%2Fpusf",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "BoE: Current Receipts: Taxes on income and wealth: £m CPNSA",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=5000",
      "retrievedAt": "2026-10-02T07:59:01.303625Z",
      "responseSha256": "a329140ee14a4db9aeeb81712948ca16610a1992fc36eef6e70dffdeca83a708",
      "sourcePointer": "/items/844",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/5844",
      "normalisedRecordSha256": "29bb63bdb6c4492c8c7d25d0599d344bf9590d6a08c16b67e42496684ad281f8",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf"
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
    "cdid": "JW27",
    "dataset_id": "PUSF",
    "edition": "",
    "id": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-21T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf",
    "sourceEvidence": {
      "pointer": "/items/844",
      "retrievedAt": "2026-10-02T07:59:01.303625Z",
      "sha256": "a329140ee14a4db9aeeb81712948ca16610a1992fc36eef6e70dffdeca83a708",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=5000"
    },
    "summary": "",
    "title": "BoE: Current Receipts: Taxes on income and wealth: £m CPNSA",
    "topics": [
      "1245",
      "9828",
      "3863"
    ],
    "type": "timeseries",
    "uri": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf"
  }
}
---

# BoE: Current Receipts: Taxes on income and wealth: £m CPNSA

ONS website catalogue metadata.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/jw27/pusf)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
