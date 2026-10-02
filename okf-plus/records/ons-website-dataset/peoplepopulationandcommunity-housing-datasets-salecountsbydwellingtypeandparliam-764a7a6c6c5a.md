---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fpeoplepopulationandcommunity%2Fhousing%2Fdatasets%2Fsalecountsbydwellingtypeandparliamentaryconstituencyenglandandwales%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Sale counts by dwelling type and parliamentary constituency, England and Wales",
  "description": "Number of houses sold by dwelling type for parliamentary constituencies, 1995–2013. Machine readable CSV",
  "nativeIdentifier": "/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "responseSha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "sourcePointer": "/items/503",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1503",
      "normalisedRecordSha256": "7b4963409d0151fcf5ec0fba0c9e209790477635fa92d278c962fc78f7a1556f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current"
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
    "id": "/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current",
    "keywords": [],
    "meta_description": "Number of houses sold by dwelling type for parliamentary constituencies, 1995–2013. Machine readable CSV",
    "nativeIdentityField": "uri",
    "release_date": "2015-02-17T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current",
    "sourceEvidence": {
      "pointer": "/items/503",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Number of houses sold by dwelling type for parliamentary constituencies, 1995–2013. Machine readable CSV",
    "title": "Sale counts by dwelling type and parliamentary constituency, England and Wales",
    "topics": [
      "9581",
      "5586"
    ],
    "type": "dataset",
    "uri": "/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current"
  }
}
---

# Sale counts by dwelling type and parliamentary constituency, England and Wales

Number of houses sold by dwelling type for parliamentary constituencies, 1995–2013. Machine readable CSV

Native identifier: `/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/salecountsbydwellingtypeandparliamentaryconstituencyenglandandwales/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
