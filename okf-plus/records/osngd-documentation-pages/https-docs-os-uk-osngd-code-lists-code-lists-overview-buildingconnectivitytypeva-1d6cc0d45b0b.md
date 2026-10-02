---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Fbuildingconnectivitytypevalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "buildingconnectivitytypevalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md",
      "retrievedAt": "2026-10-02T08:16:16.889382Z",
      "responseSha256": "bd611dd6f8deb205e4145552f671fb2c7d1cbf034b9255b59d53c2caea766e10",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/218",
      "normalisedRecordSha256": "78db0605c1b67dc8af411ed4594e11371cf84df67846ced30bfc609de173afbb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:16:16.889382Z",
      "sha256": "bd611dd6f8deb205e4145552f671fb2c7d1cbf034b9255b59d53c2caea766e10",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "bd611dd6f8deb205e4145552f671fb2c7d1cbf034b9255b59d53c2caea766e10",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "buildingconnectivitytypevalue"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md"
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
            "retainedLabelRows": 4,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 4,
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
                "End-Connected"
              ],
              [
                1,
                "Multi-Connected"
              ],
              [
                2,
                "Semi-Connected"
              ],
              [
                3,
                "Standalone"
              ]
            ]
          },
          "omittedCellCount": 4,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 4,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "buildingconnectivitytypevalue"
    },
    "structureStatus": "projected",
    "title": "buildingconnectivitytypevalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md"
  }
}
---

# buildingconnectivitytypevalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
