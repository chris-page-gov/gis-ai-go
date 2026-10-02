---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Frevisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Revisions triangles: regional gross value added (balanced) in current basic prices",
  "description": "Annual growth rates by UK NUTS1 and NUTS2 regions for gross value added (GVA) in current basic prices.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "productivity",
    "UK cities",
    "NUTS",
    "GVA",
    "local authority",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/219",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3219",
      "normalisedRecordSha256": "e8dbff501ee2df2733f5d5e1704105155afaa81d53bc434bc0023505123c9c0f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices"
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
    "id": "/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices",
    "keywords": [
      "productivity",
      "UK cities",
      "NUTS",
      "GVA",
      "local authority"
    ],
    "meta_description": "Annual growth rates by UK NUTS1 and NUTS2 regions for gross value added (GVA) in current basic prices.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-22T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices",
    "sourceEvidence": {
      "pointer": "/items/219",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Revisions to annual levels and growth rates by UK ITL1, ITL2 and ITL3 regions for gross value added (GVA) in current basic prices.",
    "title": "Revisions triangles: regional gross value added (balanced) in current basic prices",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices"
  }
}
---

# Revisions triangles: regional gross value added (balanced) in current basic prices

Annual growth rates by UK NUTS1 and NUTS2 regions for gross value added (GVA) in current basic prices.

Native identifier: `/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/revisionstrianglesregionalgrossvalueaddedbalancedincurrentbasicprices)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
