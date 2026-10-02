---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgrossvalueaddedgva%2Ftimeseries%2Fr35w%2Fragv",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "COE UK less Extra-Regio Accommodation & food Raw total £m",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/timeseries/r35w/ragv",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/timeseries/r35w/ragv",
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
      "sourcePointer": "/items/927",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/9927",
      "normalisedRecordSha256": "3d8c8d3d09910c1694e3967534fed54fc3a3ec0ba0abcbc399f08da9943bae56",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/timeseries/r35w/ragv"
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
    "cdid": "R35W",
    "dataset_id": "RAGV",
    "edition": "",
    "id": "/economy/grossvalueaddedgva/timeseries/r35w/ragv",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2014-12-10T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/timeseries/r35w/ragv",
    "sourceEvidence": {
      "pointer": "/items/927",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "sha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000"
    },
    "summary": "",
    "title": "COE UK less Extra-Regio Accommodation & food Raw total £m",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "timeseries",
    "uri": "/economy/grossvalueaddedgva/timeseries/r35w/ragv"
  }
}
---

# COE UK less Extra-Regio Accommodation & food Raw total £m

ONS website catalogue metadata.

Native identifier: `/economy/grossvalueaddedgva/timeseries/r35w/ragv`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/timeseries/r35w/ragv)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
