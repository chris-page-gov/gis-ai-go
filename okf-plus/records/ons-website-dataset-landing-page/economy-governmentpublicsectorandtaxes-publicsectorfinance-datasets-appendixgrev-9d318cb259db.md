---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicsectorfinance%2Fdatasets%2Fappendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Revisions to the first reported estimate of public sector net borrowing: Appendix F",
  "description": "Summarises revisions to the first estimate of UK public sector borrowing (excluding public sector banks) by sub-sector for the last six financial years. Revisions are shown at 6 and 12 months after year end.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "government",
    "deficit",
    "public finance",
    "PSF",
    "national debt",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/209",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3209",
      "normalisedRecordSha256": "50c70413ca493b69deed57019f449cd8ddf072a117f2cff3a66f2226095e763f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector"
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
    "id": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector",
    "keywords": [
      "government",
      "deficit",
      "public finance",
      "PSF",
      "national debt"
    ],
    "meta_description": "Summarises revisions to the first estimate of UK public sector borrowing (excluding public sector banks) by sub-sector for the last six financial years. Revisions are shown at 6 and 12 months after year end.",
    "nativeIdentityField": "uri",
    "release_date": "2023-08-21T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector",
    "sourceEvidence": {
      "pointer": "/items/209",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Summarises revisions to the first estimate of UK public sector borrowing (excluding public sector banks) by sub-sector for the last six financial years. Revisions are shown at 6 and 12 months after year end.",
    "title": "Revisions to the first reported estimate of public sector net borrowing: Appendix F",
    "topics": [
      "1245",
      "9828",
      "3863"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector"
  }
}
---

# Revisions to the first reported estimate of public sector net borrowing: Appendix F

Summarises revisions to the first estimate of UK public sector borrowing (excluding public sector banks) by sub-sector for the last six financial years. Revisions are shown at 6 and 12 months after year end.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/appendixgrevisionstothefirstreportedestimateoffinancialyearendpublicsectornetborrowingexcludingpublicsectorbanksbysubsector)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
