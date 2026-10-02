---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Fsideofroadvalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "sideofroadvalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md",
      "retrievedAt": "2026-10-02T08:20:10.383318Z",
      "responseSha256": "d19641b6396e30c9ff2ad43d4135db413c1ab071469fb5563d0125d7b4f2f407",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/359",
      "normalisedRecordSha256": "f17c731704b7d59920cae27772d1e36b109bd780d4cedbb3bf4b1eeb6122f1b0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:20:10.383318Z",
      "sha256": "d19641b6396e30c9ff2ad43d4135db413c1ab071469fb5563d0125d7b4f2f407",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "d19641b6396e30c9ff2ad43d4135db413c1ab071469fb5563d0125d7b4f2f407",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "sideofroadvalue"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md"
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
            "retainedLabelRows": 2,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 2,
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
                "Left"
              ],
              [
                1,
                "Right"
              ]
            ]
          },
          "omittedCellCount": 2,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 2,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "sideofroadvalue"
    },
    "structureStatus": "projected",
    "title": "sideofroadvalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md"
  }
}
---

# sideofroadvalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/sideofroadvalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
