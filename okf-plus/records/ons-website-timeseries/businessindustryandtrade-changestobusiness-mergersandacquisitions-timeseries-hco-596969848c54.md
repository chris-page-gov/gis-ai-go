---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Fbusinessindustryandtrade%2Fchangestobusiness%2Fmergersandacquisitions%2Ftimeseries%2Fhco7%2Fam",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Africa Inward Acquisitions Number",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am",
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
      "sourcePointer": "/items/435",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/3435",
      "normalisedRecordSha256": "837b4ce0cb83a4345e6d85c6a957d85b571dbb035a716dd28a5336480435e466",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am"
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
    "cdid": "HCO7",
    "dataset_id": "AM",
    "edition": "",
    "id": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-31T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am",
    "sourceEvidence": {
      "pointer": "/items/435",
      "retrievedAt": "2026-10-02T07:58:58.981684Z",
      "sha256": "3e8bf64e1263b10deed5483f4b714a928fd42cf955ba9565b43faa4268b475a9",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "",
    "title": "Africa Inward Acquisitions Number",
    "topics": [
      "5163",
      "9658",
      "5383"
    ],
    "type": "timeseries",
    "uri": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am"
  }
}
---

# Africa Inward Acquisitions Number

ONS website catalogue metadata.

Native identifier: `/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hco7/am)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
