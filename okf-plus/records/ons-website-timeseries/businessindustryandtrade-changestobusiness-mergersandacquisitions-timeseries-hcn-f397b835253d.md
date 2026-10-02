---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Fbusinessindustryandtrade%2Fchangestobusiness%2Fmergersandacquisitions%2Ftimeseries%2Fhcn9%2Fam",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Australasia & Oceania Inward Disposals Number",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=4000",
      "retrievedAt": "2026-10-02T07:59:00.122599Z",
      "responseSha256": "0701d9bb17bb56aec7affb143df4a8e033b18018701254d3d62a52c9c179f80c",
      "sourcePointer": "/items/7",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/4007",
      "normalisedRecordSha256": "b6d4fc117488e02843ad8da0e1b5f72e768559d6711cdeb8048b4ea7e71d7e4d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am"
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
    "cdid": "HCN9",
    "dataset_id": "AM",
    "edition": "",
    "id": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-31T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am",
    "sourceEvidence": {
      "pointer": "/items/7",
      "retrievedAt": "2026-10-02T07:59:00.122599Z",
      "sha256": "0701d9bb17bb56aec7affb143df4a8e033b18018701254d3d62a52c9c179f80c",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=4000"
    },
    "summary": "",
    "title": "Australasia & Oceania Inward Disposals Number",
    "topics": [
      "9658",
      "5383",
      "5163"
    ],
    "type": "timeseries",
    "uri": "/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am"
  }
}
---

# Australasia & Oceania Inward Disposals Number

ONS website catalogue metadata.

Native identifier: `/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/changestobusiness/mergersandacquisitions/timeseries/hcn9/am)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
