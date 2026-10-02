---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicspending%2Fdatasets%2Fexcessivedeficitprocedureedpcalendaryearmaintables%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Excessive Deficit Procedure (EDP) Calendar Year Main Tables",
  "description": "Reports government deficit/surplus by government sector, debt levels and other supporting information.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/566",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/566",
      "normalisedRecordSha256": "cc1e61326530fa3d43eeb8659a390837701e535cd38298a380d29c9049861282",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current"
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
    "id": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current",
    "keywords": [],
    "meta_description": "Reports government deficit/surplus by government sector, debt levels and other supporting information.",
    "nativeIdentityField": "uri",
    "release_date": "2015-10-15T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current",
    "sourceEvidence": {
      "pointer": "/items/566",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Reports government deficit/surplus by government sector, debt levels and other supporting information.",
    "title": "Excessive Deficit Procedure (EDP) Calendar Year Main Tables",
    "topics": [
      "1245",
      "9828",
      "8233"
    ],
    "type": "dataset",
    "uri": "/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current"
  }
}
---

# Excessive Deficit Procedure (EDP) Calendar Year Main Tables

Reports government deficit/surplus by government sector, debt levels and other supporting information.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/datasets/excessivedeficitprocedureedpcalendaryearmaintables/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
