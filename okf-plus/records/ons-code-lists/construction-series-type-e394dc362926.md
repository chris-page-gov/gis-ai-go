---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-code-lists/construction-series-type",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "construction-series-type",
  "description": "Native ONS code-lists catalogue entry.",
  "nativeIdentifier": "construction-series-type",
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
      "sourcePointer": "/items/11",
      "normalisedSource": "okf-plus/source/ons-code-lists.json",
      "normalisedPointer": "/records/11",
      "normalisedRecordSha256": "aa784c818561549d211c6d31f2e0f70213cd0522ab9e77638bc7d4a2a1f570da",
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
        "href": "http://api.beta.ons.gov.uk/v1/code-lists/construction-series-type/editions"
      },
      "self": {
        "href": "http://api.beta.ons.gov.uk/v1/code-lists/construction-series-type",
        "id": "construction-series-type"
      }
    },
    "id": "construction-series-type",
    "linkTraversal": "not-requested",
    "nativeIdentityField": "/links/self/id",
    "resource": "https://api.beta.ons.gov.uk/v1/code-lists",
    "sourceEvidence": {
      "pointer": "/items/11",
      "retrievedAt": "2026-10-02T07:59:13.223015Z",
      "sha256": "eda7f22021a40798da744e4876db16a089579f401feab43d6270992a99e1a5f4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/code-lists?limit=1000&offset=0"
    }
  },
  "skos:prefLabel": {
    "@value": "construction-series-type",
    "@language": "en"
  }
}
---

# construction-series-type

Native ONS code-lists catalogue entry.

Native identifier: `construction-series-type`.

Source family: `ons-code-lists`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/code-lists)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- A catalogue entry does not enumerate all subordinate variables, categories or code-list editions.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
