---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fland-use.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "OS NGD Land Use",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/land-use.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/land-use.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/land-use.md",
      "retrievedAt": "2026-10-02T08:13:36.730908Z",
      "responseSha256": "09fe160a7ef0c7db613446cc8051b8c192c087014ca678f3d90866e9c1379bda",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/124",
      "normalisedRecordSha256": "ffd36d2a751514f55e15308e4f8b8d378738b9a078346a1c18b4e4aa85ed01ce",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/land-use.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/land-use.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:13:36.730908Z",
      "sha256": "09fe160a7ef0c7db613446cc8051b8c192c087014ca678f3d90866e9c1379bda",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/land-use.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "09fe160a7ef0c7db613446cc8051b8c192c087014ca678f3d90866e9c1379bda",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/land-use",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "OS NGD Land Use"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Introduction to the theme"
        },
        {
          "level": 4,
          "role": "section",
          "text": "How does OS NGD Land Theme data differ from OS NGD Land Use Theme data?"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Data structure"
        },
        {
          "level": 4,
          "role": "section",
          "text": "Site Routing Point Feature Type in an end-of-life state"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Unique identifiers"
        },
        {
          "level": 4,
          "role": "section",
          "text": "Additional unique identifiers for the theme"
        },
        {
          "level": 2,
          "role": "section",
          "text": "What are land use sites?"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Useful links"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 3,
        "headings": 9,
        "referenceCandidatesReviewed": 10,
        "referenceLinks": 10,
        "rejectedReferences": 7,
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
          "url": "https://docs.os.uk/osngd/data-structure/land-use.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-node.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/more-than-maps/data-demonstrators/topography-demonstrators/os-ngd-land-use"
        }
      ],
      "tables": [],
      "title": "OS NGD Land Use"
    },
    "structureStatus": "projected",
    "title": "OS NGD Land Use",
    "url": "https://docs.os.uk/osngd/data-structure/land-use.md"
  }
}
---

# OS NGD Land Use

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/land-use.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/land-use.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
