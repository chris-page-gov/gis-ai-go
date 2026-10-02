---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Fregionalgvanuts1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Regional GVA NUTS1",
  "description": "Annual estimates of NUTS1 regional Gross Value Added (GVA), Compensation of Employees (CoE) and Gross Operating Surplus (GOS). Tables show estimates of total GVA, GVA per head, GVA per head index and GVA by industry.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/regionalgvanuts1",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgvanuts1",
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
      "sourcePointer": "/items/70",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3070",
      "normalisedRecordSha256": "68777e9400f6b6cbe6c53a094c69a3a7d8dd6d8b15420c0ebe1b27b5e1e4991a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgvanuts1"
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
    "id": "/economy/grossvalueaddedgva/datasets/regionalgvanuts1",
    "keywords": [],
    "meta_description": "Annual estimates of NUTS1 regional Gross Value Added (GVA), Compensation of Employees (CoE) and Gross Operating Surplus (GOS). Tables show estimates of total GVA, GVA per head, GVA per head index and GVA by industry.",
    "nativeIdentityField": "uri",
    "release_date": "2014-12-10T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgvanuts1",
    "sourceEvidence": {
      "pointer": "/items/70",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Annual estimates of NUTS1 regional Gross Value Added (GVA), Compensation of Employees (CoE) and Gross Operating Surplus (GOS). Tables show estimates of total GVA, GVA per head, GVA per head index and GVA by industry.",
    "title": "Regional GVA NUTS1",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossvalueaddedgva/datasets/regionalgvanuts1"
  }
}
---

# Regional GVA NUTS1

Annual estimates of NUTS1 regional Gross Value Added (GVA), Compensation of Employees (CoE) and Gross Operating Surplus (GOS). Tables show estimates of total GVA, GVA per head, GVA per head index and GVA by industry.

Native identifier: `/economy/grossvalueaddedgva/datasets/regionalgvanuts1`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgvanuts1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
