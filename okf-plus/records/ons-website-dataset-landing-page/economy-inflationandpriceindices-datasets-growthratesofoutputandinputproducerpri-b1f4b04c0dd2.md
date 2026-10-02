---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Fgrowthratesofoutputandinputproducerpriceinflation",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Growth rates of output and input producer price inflation (PPI)",
  "description": "Monthly and annual inflation rates for UK input and output PPI, 1996 to 2025.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "manufacturing",
    "input prices",
    "output prices",
    "producer prices",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/497",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1497",
      "normalisedRecordSha256": "5c0445cd18155baea824e7bc1ee5ba93d42c8b240ed6f200034c1a7ef27d5015",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation"
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
    "id": "/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation",
    "keywords": [
      "manufacturing",
      "input prices",
      "output prices",
      "producer prices"
    ],
    "meta_description": "Monthly and annual inflation rates for UK input and output PPI, 1996 to 2025.",
    "nativeIdentityField": "uri",
    "release_date": "2025-02-19T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation",
    "sourceEvidence": {
      "pointer": "/items/497",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Monthly and annual inflation rates for UK input and output producer price inflation (PPI), 1996 to 2025.",
    "title": "Growth rates of output and input producer price inflation (PPI)",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation"
  }
}
---

# Growth rates of output and input producer price inflation (PPI)

Monthly and annual inflation rates for UK input and output PPI, 1996 to 2025.

Native identifier: `/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/growthratesofoutputandinputproducerpriceinflation)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
