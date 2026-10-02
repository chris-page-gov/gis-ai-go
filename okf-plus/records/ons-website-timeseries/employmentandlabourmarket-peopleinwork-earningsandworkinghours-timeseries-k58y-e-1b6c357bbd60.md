---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Femploymentandlabourmarket%2Fpeopleinwork%2Fearningsandworkinghours%2Ftimeseries%2Fk58y%2Femp",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "AWE: Other Services Level (£): Non Seasonally Adjusted Bonus",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp",
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
      "sourcePointer": "/items/69",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/3069",
      "normalisedRecordSha256": "8370a06873623dff1244931eab0d0295135081dd7c002949fdcd927b89e730bb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp"
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
    "cdid": "K58Y",
    "dataset_id": "EMP",
    "edition": "",
    "id": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp",
    "sourceEvidence": {
      "pointer": "/items/69",
      "retrievedAt": "2026-10-02T07:58:58.981684Z",
      "sha256": "3e8bf64e1263b10deed5483f4b714a928fd42cf955ba9565b43faa4268b475a9",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "",
    "title": "AWE: Other Services Level (£): Non Seasonally Adjusted Bonus",
    "topics": [
      "5687",
      "2114",
      "8817"
    ],
    "type": "timeseries",
    "uri": "/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp"
  }
}
---

# AWE: Other Services Level (£): Non Seasonally Adjusted Bonus

ONS website catalogue metadata.

Native identifier: `/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/k58y/emp)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
