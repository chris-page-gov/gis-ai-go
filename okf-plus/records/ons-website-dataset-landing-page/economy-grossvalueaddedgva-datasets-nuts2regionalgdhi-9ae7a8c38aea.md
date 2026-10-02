---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Fnuts2regionalgdhi",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NUTS2 Regional GDHI",
  "description": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/423",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2423",
      "normalisedRecordSha256": "5fb9ba118e87bc550887831985d2f8201ce9b8ee05418fdca13150629f1893dd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi"
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
    "id": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi",
    "keywords": [],
    "meta_description": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
    "nativeIdentityField": "uri",
    "release_date": "2015-05-26T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi",
    "sourceEvidence": {
      "pointer": "/items/423",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
    "title": "NUTS2 Regional GDHI",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi"
  }
}
---

# NUTS2 Regional GDHI

Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.

Native identifier: `/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
