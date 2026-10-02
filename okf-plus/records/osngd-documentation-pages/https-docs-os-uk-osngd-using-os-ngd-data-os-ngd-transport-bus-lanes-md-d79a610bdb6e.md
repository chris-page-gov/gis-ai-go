---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fusing-os-ngd-data%2Fos-ngd-transport%2Fbus-lanes.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Bus lanes",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md",
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
      "resource": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md",
      "retrievedAt": "2026-10-02T08:22:35.072505Z",
      "responseSha256": "a67aaffc8a8ec38b0419ca00ab3c43357396437211f1447b97f2455a9f142a1e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/444",
      "normalisedRecordSha256": "15728c0cc86b9c034f8da6323204b09411bb79644de96d0fe14c21b3ac83858b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md"
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
    "id": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:22:35.072505Z",
      "sha256": "a67aaffc8a8ec38b0419ca00ab3c43357396437211f1447b97f2455a9f142a1e",
      "status": 200,
      "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "a67aaffc8a8ec38b0419ca00ab3c43357396437211f1447b97f2455a9f142a1e",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Bus lanes"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Introduction"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Use cases and applications"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Data provision"
        },
        {
          "level": 2,
          "role": "section",
          "text": "What you'll find in this sub-section"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 7,
        "headings": 5,
        "referenceCandidatesReviewed": 9,
        "referenceLinks": 9,
        "rejectedReferences": 1,
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
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/bus-lane.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes/bus-lane-feature-type.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes/road-link-attribution.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes/how-bus-lane-data-are-created.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes/known-limitations.md"
        }
      ],
      "tables": [],
      "title": "Bus lanes"
    },
    "structureStatus": "projected",
    "title": "Bus lanes",
    "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md"
  }
}
---

# Bus lanes

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/bus-lanes.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
