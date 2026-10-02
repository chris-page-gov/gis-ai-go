---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgrossdomesticproductgdp%2Ftimeseries%2Fl8ph%2Fbb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "CG: D.613: Res: Households actual social contributions: CP: NSA",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/timeseries/l8ph/bb",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l8ph/bb",
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
      "sourcePointer": "/items/215",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/9215",
      "normalisedRecordSha256": "9129552c9054aa2f3e6fe41d0d56312a34c06de15f82425b76eb67026d4f53b9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l8ph/bb"
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
    "cdid": "L8PH",
    "dataset_id": "BB",
    "edition": "",
    "id": "/economy/grossdomesticproductgdp/timeseries/l8ph/bb",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2025-10-31T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l8ph/bb",
    "sourceEvidence": {
      "pointer": "/items/215",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "sha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000"
    },
    "summary": "",
    "title": "CG: D.613: Res: Households actual social contributions: CP: NSA",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "timeseries",
    "uri": "/economy/grossdomesticproductgdp/timeseries/l8ph/bb"
  }
}
---

# CG: D.613: Res: Households actual social contributions: CP: NSA

ONS website catalogue metadata.

Native identifier: `/economy/grossdomesticproductgdp/timeseries/l8ph/bb`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l8ph/bb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
