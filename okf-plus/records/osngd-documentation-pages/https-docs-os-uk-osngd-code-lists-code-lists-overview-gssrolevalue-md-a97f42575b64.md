---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Fgssrolevalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "gssrolevalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md",
      "retrievedAt": "2026-10-02T08:17:42.017046Z",
      "responseSha256": "b5cac4fdb9f38d460820fc01b523ff17d713ec70644155df4fd2fd387549ded6",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/263",
      "normalisedRecordSha256": "c133b25eb515c489f32c76847bf65aedc0bc3a1ed4b1b00e98f447e22bda1116",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:17:42.017046Z",
      "sha256": "b5cac4fdb9f38d460820fc01b523ff17d713ec70644155df4fd2fd387549ded6",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "b5cac4fdb9f38d460820fc01b523ff17d713ec70644155df4fd2fd387549ded6",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "gssrolevalue"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 1,
        "headings": 1,
        "referenceCandidatesReviewed": 2,
        "referenceLinks": 2,
        "rejectedReferences": 1,
        "tables": 1
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
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md"
        }
      ],
      "tables": [
        {
          "columns": [
            {
              "label": "Label",
              "position": 0,
              "role": "native-value-label"
            },
            {
              "label": "Definition",
              "position": 1,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "markdown",
          "hasExplicitHeader": true,
          "nativeLabelScope": {
            "identity": "Source page, table ordinal and source row; duplicate labels are not merged.",
            "omittedLabelRows": 0,
            "retainedLabelRows": 3,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 3,
            "status": "source-code-list-labels-not-api-enum-assertions"
          },
          "nativeLabelTable": {
            "columns": [
              "sourceRow",
              "nativeText"
            ],
            "encoding": "os-documentation-native-label-table.v1",
            "rows": [
              [
                0,
                "Lower Tier Local Authority"
              ],
              [
                1,
                "Unitary Local Authority"
              ],
              [
                2,
                "Upper Tier Local Authority"
              ]
            ]
          },
          "omittedCellCount": 3,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 3,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "gssrolevalue"
    },
    "structureStatus": "projected",
    "title": "gssrolevalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md"
  }
}
---

# gssrolevalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/gssrolevalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
