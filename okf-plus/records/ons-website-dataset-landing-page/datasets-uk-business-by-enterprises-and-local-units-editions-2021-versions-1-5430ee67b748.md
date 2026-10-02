---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2Fuk-business-by-enterprises-and-local-units%2Feditions%2F2021%2Fversions%2F1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Business: Activity, Size and Location",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "enterprises",
    "local units,IDBR,business counts,Inter-Departmental Business Register",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/637",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3637",
      "normalisedRecordSha256": "25d55ee6c738bafa56fc697a5929f2d3c03303e69b00551e7a51c8ba24c16aef",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1"
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
    "releaseVersion": "2021"
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
    "dataset_id": "uk-business-by-enterprises-and-local-units",
    "edition": "2021",
    "id": "/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1",
    "keywords": [
      "enterprises",
      "local units,IDBR,business counts,Inter-Departmental Business Register"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2021-10-04T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1",
    "sourceEvidence": {
      "pointer": "/items/637",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "The data contained in these tables are numbers of enterprises and local units produced from a snapshot of the Inter-Departmental Business Register (IDBR) taken on 12 March 2021. This dataset contains details of the number of VAT and/or PAYE based enterprises and local units in districts, counties and unitary authorities within region and country by broad industry group.",
    "title": "UK Business: Activity, Size and Location",
    "type": "dataset_landing_page",
    "uri": "/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1"
  }
}
---

# UK Business: Activity, Size and Location

ONS website catalogue metadata.

Native identifier: `/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/uk-business-by-enterprises-and-local-units/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
