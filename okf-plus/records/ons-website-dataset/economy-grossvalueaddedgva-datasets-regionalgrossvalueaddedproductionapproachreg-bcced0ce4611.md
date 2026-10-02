---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fgrossvalueaddedgva%2Fdatasets%2Fregionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables%2Flatestversion",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Regional Gross Value Added (Production Approach) Unconstrained Data Tables",
  "description": "Experimental statistics showing annual estimates of regional GVA(P) NUTS1 and NUTS2 CVM (2011 = 100). These data are not constrained to ensure that the regions sum to the UK total.",
  "nativeIdentifier": "/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Regional",
    "GVA(P)",
    "constant price",
    "chained volume measure",
    "CVM",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "responseSha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "sourcePointer": "/items/458",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1458",
      "normalisedRecordSha256": "baee3cc9a120adb52b93d9a0a9d7aabd6bd9a5a3f212985c9dd65988ffd4e757",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion"
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
    "releaseVersion": "Latest version"
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
    "edition": "Latest version",
    "id": "/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion",
    "keywords": [
      "Regional",
      "GVA(P)",
      "constant price",
      "chained volume measure",
      "CVM"
    ],
    "meta_description": "Experimental statistics showing annual estimates of regional GVA(P) NUTS1 and NUTS2 CVM (2011 = 100). These data are not constrained to ensure that the regions sum to the UK total.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-17T16:36:11.808Z",
    "resource": "https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion",
    "sourceEvidence": {
      "pointer": "/items/458",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Experimental statistics showing annual estimates of regional GVA(P) NUTS1 and NUTS2 CVM (2011 = 100). These data are not constrained to ensure that the regions sum to the UK total.",
    "title": "Regional Gross Value Added (Production Approach) Unconstrained Data Tables",
    "topics": [
      "1245",
      "7521"
    ],
    "type": "dataset",
    "uri": "/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion"
  }
}
---

# Regional Gross Value Added (Production Approach) Unconstrained Data Tables

Experimental statistics showing annual estimates of regional GVA(P) NUTS1 and NUTS2 CVM (2011 = 100). These data are not constrained to ensure that the regions sum to the UK total.

Native identifier: `/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossvalueaddedgva/datasets/regionalgrossvalueaddedproductionapproachregionalgvapunconstraineddatatables/latestversion)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
