---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Fwaterdescriptionvalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "waterdescriptionvalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md",
      "retrievedAt": "2026-10-02T08:21:16.332794Z",
      "responseSha256": "6b5ebfcb8e83c8fb2089b13824809235131210e1732fc50ba0565c2b0a8866c2",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/396",
      "normalisedRecordSha256": "33b9bbe796b6ee9a014e262fc6b22fd452dd30d7baf8ef91e2064f333472ed11",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:21:16.332794Z",
      "sha256": "6b5ebfcb8e83c8fb2089b13824809235131210e1732fc50ba0565c2b0a8866c2",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "6b5ebfcb8e83c8fb2089b13824809235131210e1732fc50ba0565c2b0a8866c2",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "waterdescriptionvalue"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md"
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
            "retainedLabelRows": 54,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 54,
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
                "Buried Open Reservoir"
              ],
              [
                1,
                "Buried Open Reservoir With Solar Panels"
              ],
              [
                2,
                "Buried Open Water Tank"
              ],
              [
                3,
                "Canal"
              ],
              [
                4,
                "Canal And Reeds"
              ],
              [
                5,
                "Canal Feeder"
              ],
              [
                6,
                "Cascade"
              ],
              [
                7,
                "Collects"
              ],
              [
                8,
                "Coniferous Trees"
              ],
              [
                9,
                "Cooling Pond"
              ],
              [
                10,
                "Dew Pond"
              ],
              [
                11,
                "Drain"
              ],
              [
                12,
                "Fish Ladder"
              ],
              [
                13,
                "Fish Lock"
              ],
              [
                14,
                "Fish Trap"
              ],
              [
                15,
                "Leat"
              ],
              [
                16,
                "Lock"
              ],
              [
                17,
                "Mill Leat"
              ],
              [
                18,
                "Mineral Spring"
              ],
              [
                19,
                "Mixed Trees In Water"
              ],
              [
                20,
                "Moat"
              ],
              [
                21,
                "Non-Coniferous Trees In Water"
              ],
              [
                22,
                "Open Reservoir"
              ],
              [
                23,
                "Open Reservoir And Reeds"
              ],
              [
                24,
                "Open Reservoir With Solar Panels"
              ],
              [
                25,
                "Open Tank Reservoir"
              ],
              [
                26,
                "Open Tank Reservoir With Solar Panels"
              ],
              [
                27,
                "Open Water Tank"
              ],
              [
                28,
                "Overflow"
              ],
              [
                29,
                "Oyster Pit"
              ],
              [
                30,
                "Paddling Pool"
              ],
              [
                31,
                "Reed Bed For Waste Water"
              ],
              [
                32,
                "Reeds In Water"
              ],
              [
                33,
                "Reeds In Watercourse"
              ],
              [
                34,
                "Scattered Coniferous Trees In Water"
              ],
              [
                35,
                "Scattered Coniferous Trees In Water And Reeds"
              ],
              [
                36,
                "Scattered Mixed Trees In Water"
              ],
              [
                37,
                "Scattered Mixed Trees In Water And Reeds"
              ],
              [
                38,
                "Scattered Non-Coniferous Trees In Water"
              ],
              [
                39,
                "Scattered Non-Coniferous Trees In Water And Reeds"
              ],
              [
                40,
                "Sea"
              ],
              [
                41,
                "Settling Pond"
              ],
              [
                42,
                "Sinks"
              ],
              [
                43,
                "Spreads"
              ],
              [
                44,
                "Spring"
              ],
              [
                45,
                "Spring And Trough"
              ],
              [
                46,
                "Spring As Source Of Watercourse"
              ],
              [
                47,
                "Static Water As Source Of Watercourse"
              ],
              [
                48,
                "Still Water"
              ],
              [
                49,
                "Still Water With Solar Panels"
              ],
              [
                50,
                "Swimming Pool"
              ],
              [
                51,
                "Watercourse"
              ],
              [
                52,
                "Watercress Bed"
              ],
              [
                53,
                "Waterfall"
              ]
            ]
          },
          "omittedCellCount": 54,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 54,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "waterdescriptionvalue"
    },
    "structureStatus": "projected",
    "title": "waterdescriptionvalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md"
  }
}
---

# waterdescriptionvalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/waterdescriptionvalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
