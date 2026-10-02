---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Faddress%2Faddress-related-components%2Fdelivery-point-alias.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Delivery Point Alias",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "specification",
    "documentation"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md",
      "retrievedAt": "2026-10-02T08:12:25.921595Z",
      "responseSha256": "fc66f92f1d30a964ed6694ec732988be8c9b744e667a121114cadf91c07e3a25",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/73",
      "normalisedRecordSha256": "3dc0d818ebd66d9854846a10a1f58b1eb0f9f57841cdc99669d88ef8c37ce464",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md"
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
    "The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.",
    "A captured guide does not establish complete vocabulary coverage or API conformance."
  ],
  "details": {
    "callable": false,
    "contentCaptured": true,
    "id": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:12:25.921595Z",
      "sha256": "fc66f92f1d30a964ed6694ec732988be8c9b744e667a121114cadf91c07e3a25",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "fc66f92f1d30a964ed6694ec732988be8c9b744e667a121114cadf91c07e3a25",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Delivery Point Alias"
        },
        {
          "level": 3,
          "role": "schema",
          "text": "Delivery Point Alias Component for Royal Mail Address Feature Type data schema version 2.0 onward"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Temporal filtering"
        },
        {
          "level": 2,
          "role": "schema-field",
          "text": "Related component attributes"
        },
        {
          "level": 3,
          "role": "section",
          "text": "aliasid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "udprn"
        },
        {
          "level": 3,
          "role": "section",
          "text": "featuretypeversiondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alias"
        },
        {
          "level": 3,
          "role": "section",
          "text": "aliasrecordtype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "aliascategory"
        },
        {
          "level": 3,
          "role": "update",
          "text": "aliascurrency"
        },
        {
          "level": 3,
          "role": "section",
          "text": "aliascode"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 2,
        "headings": 12,
        "referenceCandidatesReviewed": 4,
        "referenceLinks": 4,
        "rejectedReferences": 2,
        "tables": 0
      },
      "omitted": {
        "agentInstructionSectionOmitted": true,
        "exampleOrContactSectionsOmitted": 0,
        "fencedBlocksOmitted": 0
      },
      "projectionTruncated": false,
      "projectionVersion": "os-documentation-structure.v2",
      "references": [
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering.md"
        }
      ],
      "tables": [],
      "title": "Delivery Point Alias"
    },
    "structureStatus": "projected",
    "title": "Delivery Point Alias",
    "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md"
  }
}
---

# Delivery Point Alias

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
