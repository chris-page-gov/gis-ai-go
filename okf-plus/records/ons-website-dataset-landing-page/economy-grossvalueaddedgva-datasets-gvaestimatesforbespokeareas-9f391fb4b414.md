---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Fgvaestimatesforbespokeareas",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GVA estimates for bespoke areas",
  "description": "The total estimated GVA, per year, for each bespoke area 1998 to 2019. The user-defined areas are the West Midlands Metro region, the Old Oak and Park Royal Development Corporation region, the Clyde Gateway, and Clyde River region.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "gross value added",
    "lower-level geography",
    "bespoke geographies",
    "productivity",
    "small areas",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/399",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1399",
      "normalisedRecordSha256": "9aa998a5b2b72d2c4bd5d455b11e409837edef53cfc05cbc4a50c4bd3c280934",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas"
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
    "cdid": "",
    "dataset_id": "",
    "edition": "",
    "id": "/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas",
    "keywords": [
      "gross value added",
      "lower-level geography",
      "bespoke geographies",
      "productivity",
      "small areas"
    ],
    "meta_description": "The total estimated GVA, per year, for each bespoke area 1998 to 2019. The user-defined areas are the West Midlands Metro region, the Old Oak and Park Royal Development Corporation region, the Clyde Gateway, and Clyde River region.",
    "nativeIdentityField": "uri",
    "release_date": "2021-12-13T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas",
    "sourceEvidence": {
      "pointer": "/items/399",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "The total estimated GVA, per year, for each bespoke area 1998 to 2019. The user-defined areas are the West Midlands Metro region, the Old Oak and Park Royal Development Corporation region, the Clyde Gateway, and Clyde River region.",
    "title": "GVA estimates for bespoke areas",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas"
  }
}
---

# GVA estimates for bespoke areas

The total estimated GVA, per year, for each bespoke area 1998 to 2019. The user-defined areas are the West Midlands Metro region, the Old Oak and Park Royal Development Corporation region, the Clyde Gateway, and Clyde River region.

Native identifier: `/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/gvaestimatesforbespokeareas)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
