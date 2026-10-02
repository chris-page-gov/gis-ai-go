---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicspending%2Fdatasets%2Fexcessivedeficitprocedureedpcalendaryearmaintables",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Excessive deficit procedure main tables (calendar years)",
  "description": "Reports government deficit or surplus by government sector, debt levels and other supporting information.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "surplus",
    "taxes",
    "expenditure",
    "maastricht",
    "EDP",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/194",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1194",
      "normalisedRecordSha256": "2bf8da3741bfcd7a8d27520cc4e05926f5d64350b60ca45b1548842e591a082e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables"
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
    "id": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables",
    "keywords": [
      "surplus",
      "taxes",
      "expenditure",
      "maastricht",
      "EDP"
    ],
    "meta_description": "Reports government deficit or surplus by government sector, debt levels and other supporting information.",
    "nativeIdentityField": "uri",
    "release_date": "2020-10-18T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables",
    "sourceEvidence": {
      "pointer": "/items/194",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Government deficit or surplus by sector, debt levels and other supporting information.",
    "title": "Excessive deficit procedure main tables (calendar years)",
    "topics": [
      "8233",
      "1245",
      "9828"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables"
  }
}
---

# Excessive deficit procedure main tables (calendar years)

Reports government deficit or surplus by government sector, debt levels and other supporting information.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
