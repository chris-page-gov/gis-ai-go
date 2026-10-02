---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgrossdomesticproductgdp%2Ftimeseries%2Fkq74%2Fukea",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Actual Individual Consumption SA CVM per head",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/timeseries/kq74/ukea",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/kq74/ukea",
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
      "sourcePointer": "/items/415",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/3415",
      "normalisedRecordSha256": "0adc84eebfe48744fb70976bcc7205692fa35b2d60763c424e07c79585ef3e0c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/kq74/ukea"
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
    "cdid": "KQ74",
    "dataset_id": "UKEA",
    "edition": "",
    "id": "/economy/grossdomesticproductgdp/timeseries/kq74/ukea",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2017-06-29T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/kq74/ukea",
    "sourceEvidence": {
      "pointer": "/items/415",
      "retrievedAt": "2026-10-02T07:58:58.981684Z",
      "sha256": "3e8bf64e1263b10deed5483f4b714a928fd42cf955ba9565b43faa4268b475a9",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "",
    "title": "Actual Individual Consumption SA CVM per head",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "timeseries",
    "uri": "/economy/grossdomesticproductgdp/timeseries/kq74/ukea"
  }
}
---

# Actual Individual Consumption SA CVM per head

ONS website catalogue metadata.

Native identifier: `/economy/grossdomesticproductgdp/timeseries/kq74/ukea`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/kq74/ukea)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
