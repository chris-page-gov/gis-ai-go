---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fnationalaccounts%2Fbalanceofpayments%2Ftimeseries%2Fhbqb%2Fukea",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "BoP IIP Liability level NSA £m",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=6000",
      "retrievedAt": "2026-10-02T07:59:03.051021Z",
      "responseSha256": "4fdf1be03df861e3ee44722c69111f4d28ca0567d4c28d43c51ed07379b0a2c4",
      "sourcePointer": "/items/157",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/6157",
      "normalisedRecordSha256": "081581b75ba0aced5a7470ce8ecf869a48f7301b2dd55c286856f2d28b58aea2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea"
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
    "cdid": "HBQB",
    "dataset_id": "UKEA",
    "edition": "",
    "id": "/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-29T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea",
    "sourceEvidence": {
      "pointer": "/items/157",
      "retrievedAt": "2026-10-02T07:59:03.051021Z",
      "sha256": "4fdf1be03df861e3ee44722c69111f4d28ca0567d4c28d43c51ed07379b0a2c4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=6000"
    },
    "summary": "",
    "title": "BoP IIP Liability level NSA £m",
    "topics": [
      "1245",
      "2735",
      "1583"
    ],
    "type": "timeseries",
    "uri": "/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea"
  }
}
---

# BoP IIP Liability level NSA £m

ONS website catalogue metadata.

Native identifier: `/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/hbqb/ukea)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
