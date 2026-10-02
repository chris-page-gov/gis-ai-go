---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fgetting-started%2Fstyling-os-ngd-data.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Styling OS NGD Data",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md",
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
      "resource": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md",
      "retrievedAt": "2026-10-02T08:11:45.576724Z",
      "responseSha256": "0e408bba3f0b50bb58b7a0c72a4900f8e539856e986e210a154df1db229e2544",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/40",
      "normalisedRecordSha256": "bf10955456038d4d92bd8793904dae427b7dc8c149ddac0ad609e4b2ef03d583",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md"
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
    "id": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:11:45.576724Z",
      "sha256": "0e408bba3f0b50bb58b7a0c72a4900f8e539856e986e210a154df1db229e2544",
      "status": 200,
      "url": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "0e408bba3f0b50bb58b7a0c72a4900f8e539856e986e210a154df1db229e2544",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Styling OS NGD Data"
        },
        {
          "level": 2,
          "role": "section",
          "text": "OS Select+Build and OS NGD API – Features"
        },
        {
          "level": 3,
          "role": "section",
          "text": "Tutorials on downloading and using OS stylesheets and styling data analytically"
        },
        {
          "level": 2,
          "role": "section",
          "text": "OS NGD API – Tiles"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 5,
        "headings": 4,
        "referenceCandidatesReviewed": 8,
        "referenceLinks": 8,
        "rejectedReferences": 3,
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
          "url": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/geodataviz-assets/stylesheets/how-to-download-and-use-os-stylesheets"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/geodataviz-assets/styling-data/ngd-analytical-styling"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/os-apis/core-concepts/styling-os-ngd-data/creating-a-custom-style-for-os-ngd-api-tiles"
        }
      ],
      "tables": [],
      "title": "Styling OS NGD Data"
    },
    "structureStatus": "projected",
    "title": "Styling OS NGD Data",
    "url": "https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md"
  }
}
---

# Styling OS NGD Data

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/getting-started/styling-os-ngd-data.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
