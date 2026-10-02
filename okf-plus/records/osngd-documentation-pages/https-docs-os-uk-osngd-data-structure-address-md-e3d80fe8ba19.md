---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Faddress.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "OS NGD Address",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/address.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/address.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/address.md",
      "retrievedAt": "2026-10-02T08:11:59.056857Z",
      "responseSha256": "d07169205af46cc57ebd4d784a4c8f981cc58ef5e5122388893e0f966ba52bc6",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/52",
      "normalisedRecordSha256": "2e702027d4f88da8ce9a8541505dd1d934b4da7e4cba1a5e7b14f31e322c223f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/address.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/address.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:11:59.056857Z",
      "sha256": "d07169205af46cc57ebd4d784a4c8f981cc58ef5e5122388893e0f966ba52bc6",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/address.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "d07169205af46cc57ebd4d784a4c8f981cc58ef5e5122388893e0f966ba52bc6",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/address",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "OS NGD Address"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Introduction to the theme"
        },
        {
          "level": 2,
          "role": "section",
          "text": "OS NGD Address data is not available through the APIs"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":arrows\\_clockwise: Recent data enhancements to the theme"
        },
        {
          "level": 2,
          "role": "section",
          "text": ":arrows\\_clockwise: Data structure"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":arrows\\_clockwise: Data structure diagram"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Postal Address Related Component"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":arrows\\_clockwise: Address related components"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Unique identifiers"
        },
        {
          "level": 3,
          "role": "section",
          "text": "OS unique identifiers"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":arrows\\_clockwise: PAF unique identifiers"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Useful links"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 12,
        "headings": 12,
        "referenceCandidatesReviewed": 17,
        "referenceLinks": 17,
        "rejectedReferences": 5,
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
          "url": "https://docs.os.uk/osngd/data-structure/address.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/os-downloads/addressing-and-location/addressbase-premium"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/postal-address.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/alternate-address.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/other-classification.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/related-entity.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/multiple-residence.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/delivery-point-alias.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/address-related-components/other-alias.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/more-than-maps/data-demonstrators/addressing-and-location-demonstrators/os-ngd-address"
        }
      ],
      "tables": [],
      "title": "OS NGD Address"
    },
    "structureStatus": "projected",
    "title": "OS NGD Address",
    "url": "https://docs.os.uk/osngd/data-structure/address.md"
  }
}
---

# OS NGD Address

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/address.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/address.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
