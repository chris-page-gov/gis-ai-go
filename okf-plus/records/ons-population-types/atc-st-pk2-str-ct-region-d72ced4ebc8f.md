---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-population-types/atc-st-pk2-str-ct-region",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "All non-UK born short-term residents",
  "description": "All non-UK born short-term residents",
  "nativeIdentifier": "atc-st-pk2-str-ct-region",
  "sourceFamily": "ons-population-types",
  "resource": "https://api.beta.ons.gov.uk/v1/population-types",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/population-types?limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:59:12.057850Z",
      "responseSha256": "1ba1f96cadab4501d99432e79cdf17779949de76af862fba5087efe1532ff1e3",
      "sourcePointer": "/items/18",
      "normalisedSource": "okf-plus/source/ons-population-types.json",
      "normalisedPointer": "/records/18",
      "normalisedRecordSha256": "86a47f2b54278ef2b5636c99042b9f3329f807017af21ac56153c713dc8a1ca6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/population-types"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
  },
  "update": {
    "frequency": {
      "status": "not-applicable",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "A catalogue entry does not enumerate all subordinate variables, categories or code-list editions."
  ],
  "details": {
    "description": "All non-UK born short-term residents",
    "id": "atc-st-pk2-str-ct-region",
    "label": "All non-UK born short-term residents",
    "name": "atc-st-pk2-str-ct-region",
    "nativeIdentityField": "name",
    "resource": "https://api.beta.ons.gov.uk/v1/population-types",
    "sourceEvidence": {
      "pointer": "/items/18",
      "retrievedAt": "2026-10-02T07:59:12.057850Z",
      "sha256": "1ba1f96cadab4501d99432e79cdf17779949de76af862fba5087efe1532ff1e3",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/population-types?limit=1000&offset=0"
    },
    "type": "tabular"
  },
  "skos:prefLabel": {
    "@value": "All non-UK born short-term residents",
    "@language": "en"
  }
}
---

# All non-UK born short-term residents

All non-UK born short-term residents

Native identifier: `atc-st-pk2-str-ct-region`.

Source family: `ons-population-types`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/population-types)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- A catalogue entry does not enumerate all subordinate variables, categories or code-list editions.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
