---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgrossdomesticproductgdp%2Ftimeseries%2Fk87g%2Fbb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Air emissions Sulphur Dioxide (SO2)-Manufacturing-Thousand tonnes SO2 equivalent",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/timeseries/k87g/bb",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k87g/bb",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:58.981684Z",
      "responseSha256": "3e8bf64e1263b10deed5483f4b714a928fd42cf955ba9565b43faa4268b475a9",
      "sourcePointer": "/items/936",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/3936",
      "normalisedRecordSha256": "660c38120af5aca053e8f542d8475a74a42e1ded09812f8cd40f0a8e0f489bf9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k87g/bb"
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
    "cdid": "K87G",
    "dataset_id": "BB",
    "edition": "",
    "id": "/economy/grossdomesticproductgdp/timeseries/k87g/bb",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2025-10-31T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k87g/bb",
    "sourceEvidence": {
      "pointer": "/items/936",
      "retrievedAt": "2026-10-02T07:58:58.981684Z",
      "sha256": "3e8bf64e1263b10deed5483f4b714a928fd42cf955ba9565b43faa4268b475a9",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "",
    "title": "Air emissions Sulphur Dioxide (SO2)-Manufacturing-Thousand tonnes SO2 equivalent",
    "topics": [
      "9691",
      "1245"
    ],
    "type": "timeseries",
    "uri": "/economy/grossdomesticproductgdp/timeseries/k87g/bb"
  }
}
---

# Air emissions Sulphur Dioxide (SO2)-Manufacturing-Thousand tonnes SO2 equivalent

ONS website catalogue metadata.

Native identifier: `/economy/grossdomesticproductgdp/timeseries/k87g/bb`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/k87g/bb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
