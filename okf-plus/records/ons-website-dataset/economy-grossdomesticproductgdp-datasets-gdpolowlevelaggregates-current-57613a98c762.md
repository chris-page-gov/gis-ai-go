---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fgrossdomesticproductgdp%2Fdatasets%2Fgdpolowlevelaggregates%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GDP(O) Low Level Aggregates",
  "description": "Annual and quarterly low level aggregates of output gross value added (GVA) on a constant and current price basis, in an index and pounds million format.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "uk economy",
    "national accounts",
    "economic growth",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/586",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/586",
      "normalisedRecordSha256": "9385d1abfbc07d0e4d7df44c856dcf1fc1ead963984198b3667cf586566d437c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current"
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
    "releaseVersion": "Current"
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
    "edition": "Current",
    "id": "/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current",
    "keywords": [
      "uk economy",
      "national accounts",
      "economic growth"
    ],
    "meta_description": "Annual and quarterly low level aggregates of output gross value added (GVA) on a constant and current price basis, in an index and pounds million format.",
    "nativeIdentityField": "uri",
    "release_date": "2015-10-27T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current",
    "sourceEvidence": {
      "pointer": "/items/586",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Annual and quarterly low level aggregates of output gross value added (GVA) on a constant and current price basis, in an index and pounds million format.",
    "title": "GDP(O) Low Level Aggregates",
    "topics": [
      "9691",
      "1245"
    ],
    "type": "dataset",
    "uri": "/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current"
  }
}
---

# GDP(O) Low Level Aggregates

Annual and quarterly low level aggregates of output gross value added (GVA) on a constant and current price basis, in an index and pounds million format.

Native identifier: `/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/gdpolowlevelaggregates/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
