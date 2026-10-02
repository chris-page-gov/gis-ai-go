---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Flabourproductivity%2Fdatasets%2Fregionaljobsandhours",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Regional Jobs and Hours",
  "description": "Output per hour, output per job and output per worker for the whole economy and a range of industries. Includes estimates of unit labour costs.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/80",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3080",
      "normalisedRecordSha256": "8490864f1f72e9688e2a3bb46eefd99b26da68112c74c0275157636dd719e90c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours"
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
    "id": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours",
    "keywords": [],
    "meta_description": "Output per hour, output per job and output per worker for the whole economy and a range of industries. Includes estimates of unit labour costs.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-23T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours",
    "sourceEvidence": {
      "pointer": "/items/80",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Breakdown by region of Jobs and Hours worked in the UK.",
    "title": "Regional Jobs and Hours",
    "topics": [
      "5687",
      "2114",
      "6663"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours"
  }
}
---

# Regional Jobs and Hours

Output per hour, output per job and output per worker for the whole economy and a range of industries. Includes estimates of unit labour costs.

Native identifier: `/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/regionaljobsandhours)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
