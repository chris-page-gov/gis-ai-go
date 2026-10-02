---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-code-lists/averages-and-percentiles",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "averages-and-percentiles",
  "description": "Native ONS code-lists catalogue entry.",
  "nativeIdentifier": "averages-and-percentiles",
  "sourceFamily": "ons-code-lists",
  "resource": "https://api.beta.ons.gov.uk/v1/code-lists",
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
      "resource": "https://api.beta.ons.gov.uk/v1/code-lists?limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:59:13.223015Z",
      "responseSha256": "eda7f22021a40798da744e4876db16a089579f401feab43d6270992a99e1a5f4",
      "sourcePointer": "/items/3",
      "normalisedSource": "okf-plus/source/ons-code-lists.json",
      "normalisedPointer": "/records/3",
      "normalisedRecordSha256": "29b5d61dec177b25dd9ec69e1676ecb876e7372b66b4b7d80526b3d2e62568b6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/code-lists"
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
    "advertisedLinks": {
      "editions": {
        "href": "http://api.beta.ons.gov.uk/v1/code-lists/averages-and-percentiles/editions"
      },
      "self": {
        "href": "http://api.beta.ons.gov.uk/v1/code-lists/averages-and-percentiles",
        "id": "averages-and-percentiles"
      }
    },
    "id": "averages-and-percentiles",
    "linkTraversal": "not-requested",
    "nativeIdentityField": "/links/self/id",
    "resource": "https://api.beta.ons.gov.uk/v1/code-lists",
    "sourceEvidence": {
      "pointer": "/items/3",
      "retrievedAt": "2026-10-02T07:59:13.223015Z",
      "sha256": "eda7f22021a40798da744e4876db16a089579f401feab43d6270992a99e1a5f4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/code-lists?limit=1000&offset=0"
    }
  },
  "skos:prefLabel": {
    "@value": "averages-and-percentiles",
    "@language": "en"
  }
}
---

# averages-and-percentiles

Native ONS code-lists catalogue entry.

Native identifier: `averages-and-percentiles`.

Source family: `ons-code-lists`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/code-lists)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- A catalogue entry does not enumerate all subordinate variables, categories or code-list editions.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
