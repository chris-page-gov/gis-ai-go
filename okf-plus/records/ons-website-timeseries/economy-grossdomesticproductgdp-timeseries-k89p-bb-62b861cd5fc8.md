---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgrossdomesticproductgdp%2Ftimeseries%2Fk89p%2Fbb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "CO - electricity gas and water supply - thousand tonnes",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/timeseries/k89p/bb",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k89p/bb",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "responseSha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "sourcePointer": "/items/878",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/9878",
      "normalisedRecordSha256": "7ea4ef5aee5915972f41bb473be4fcdf5ddcf92aa6c565935e23285c1dfde232",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k89p/bb"
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
    "cdid": "K89P",
    "dataset_id": "BB",
    "edition": "",
    "id": "/economy/grossdomesticproductgdp/timeseries/k89p/bb",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2017-10-31T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k89p/bb",
    "sourceEvidence": {
      "pointer": "/items/878",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "sha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000"
    },
    "summary": "",
    "title": "CO - electricity gas and water supply - thousand tonnes",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "timeseries",
    "uri": "/economy/grossdomesticproductgdp/timeseries/k89p/bb"
  }
}
---

# CO - electricity gas and water supply - thousand tonnes

ONS website catalogue metadata.

Native identifier: `/economy/grossdomesticproductgdp/timeseries/k89p/bb`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k89p/bb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
