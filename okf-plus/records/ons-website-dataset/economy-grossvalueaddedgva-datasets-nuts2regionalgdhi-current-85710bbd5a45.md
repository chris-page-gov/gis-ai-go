---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Fnuts2regionalgdhi%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NUTS2 Regional GDHI",
  "description": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current",
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
      "sourcePointer": "/items/892",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/892",
      "normalisedRecordSha256": "e32f007ba62977504aa8ae007ef4283186cbf0f04938a449464706b877e21eb5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current"
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
    "id": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current",
    "keywords": [],
    "meta_description": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
    "nativeIdentityField": "uri",
    "release_date": "2015-05-26T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current",
    "sourceEvidence": {
      "pointer": "/items/892",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.",
    "title": "NUTS2 Regional GDHI",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset",
    "uri": "/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current"
  }
}
---

# NUTS2 Regional GDHI

Annual estimates of NUTS2 regional gross disposable household income (GDHI). Tables show estimates of total GDHI, GDHI per head, GDHI per head index and components of GDHI.

Native identifier: `/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/nuts2regionalgdhi/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
