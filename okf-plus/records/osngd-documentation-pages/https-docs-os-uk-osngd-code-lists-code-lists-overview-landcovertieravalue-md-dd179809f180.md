---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Flandcovertieravalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "landcovertieravalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md",
      "retrievedAt": "2026-10-02T08:18:02.402229Z",
      "responseSha256": "51b24b6bd197bcf1936e7ec9cf43eda9002f4a9eb809f2c5cdda59370cfdc710",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/277",
      "normalisedRecordSha256": "22eb942a515703781b8da17a48cc4706c211ad6d569b12bee2f18647dde3064f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:18:02.402229Z",
      "sha256": "51b24b6bd197bcf1936e7ec9cf43eda9002f4a9eb809f2c5cdda59370cfdc710",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "51b24b6bd197bcf1936e7ec9cf43eda9002f4a9eb809f2c5cdda59370cfdc710",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "landcovertieravalue"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md"
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
            "retainedLabelRows": 9,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 9,
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
                "Excavated Or Deposited"
              ],
              [
                1,
                "Made"
              ],
              [
                2,
                "Mineral"
              ],
              [
                3,
                "Multiple"
              ],
              [
                4,
                "Open Vegetation"
              ],
              [
                5,
                "Open Vegetation And Mineral"
              ],
              [
                6,
                "Trees"
              ],
              [
                7,
                "Under Construction"
              ],
              [
                8,
                "Water"
              ]
            ]
          },
          "omittedCellCount": 9,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 9,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "landcovertieravalue"
    },
    "structureStatus": "projected",
    "title": "landcovertieravalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md"
  }
}
---

# landcovertieravalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/landcovertieravalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
