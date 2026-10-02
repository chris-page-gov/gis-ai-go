---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Flanddescriptionvalue.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "landdescriptionvalue",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md",
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
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md",
      "retrievedAt": "2026-10-02T08:17:57.300535Z",
      "responseSha256": "a542c51057d1ba6b35ae51feada543bd4e405b6d50ecf3b2b9bc2c22d87f1ab8",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/273",
      "normalisedRecordSha256": "f9b1696a3463f162538b8c90c44aeb96525ebf4525ae2838710147faf2cf47ae",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md"
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
    "id": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:17:57.300535Z",
      "sha256": "a542c51057d1ba6b35ae51feada543bd4e405b6d50ecf3b2b9bc2c22d87f1ab8",
      "status": 200,
      "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "a542c51057d1ba6b35ae51feada543bd4e405b6d50ecf3b2b9bc2c22d87f1ab8",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "landdescriptionvalue"
        },
        {
          "level": 4,
          "role": "section",
          "text": "What's new?"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 1,
        "headings": 2,
        "referenceCandidatesReviewed": 2,
        "referenceLinks": 2,
        "rejectedReferences": 1,
        "tables": 2
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md"
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
            "retainedLabelRows": 110,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 110,
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
                "Arable Or Grazing Land"
              ],
              [
                1,
                "Bare Earth Or Grass"
              ],
              [
                2,
                "Boulder"
              ],
              [
                3,
                "Boulders Or Rock"
              ],
              [
                4,
                "Boulders Or Rock And Heath Or Rough Grassland"
              ],
              [
                5,
                "Boulders Or Rock And Heath Or Rough Grassland And Marsh"
              ],
              [
                6,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                7,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                8,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                9,
                ":x: Boulders Or Rock And Heath Or Rough Grassland Or Marsh"
              ],
              [
                10,
                "Boulders Or Rock And Marsh"
              ],
              [
                11,
                "Boulders Or Rock And Mud"
              ],
              [
                12,
                "Boulders Or Rock And Mud And Sand Or Shingle"
              ],
              [
                13,
                "Boulders Or Rock And Mud And Sand Or Shingle"
              ],
              [
                14,
                "Boulders Or Rock And Sand Or Shingle"
              ],
              [
                15,
                "Boulders Or Rock And Sand Or Shingle And Scattered Coniferous Trees"
              ],
              [
                16,
                "Boulders Or Rock And Scattered Coniferous Trees"
              ],
              [
                17,
                "Boulders Or Rock And Scattered Mixed Trees"
              ],
              [
                18,
                "Boulders Or Rock And Scattered Non-Coniferous Trees"
              ],
              [
                19,
                "Coniferous Trees"
              ],
              [
                20,
                "Coniferous Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                21,
                "Coniferous Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                22,
                "Coniferous Trees And Scrub"
              ],
              [
                23,
                "Construction Site"
              ],
              [
                24,
                "Firing Point"
              ],
              [
                25,
                "Floral Clock"
              ],
              [
                26,
                "Gallops"
              ],
              [
                27,
                "Games Court"
              ],
              [
                28,
                ":x: Heath"
              ],
              [
                29,
                "Heath Or Rough Grassland"
              ],
              [
                30,
                "Heath Or Rough Grassland And Boulders Or Rock And Scattered Mixed Trees"
              ],
              [
                31,
                "Heath Or Rough Grassland And Marsh"
              ],
              [
                32,
                "Heath Or Rough Grassland And Marsh And Scattered Coniferous Trees"
              ],
              [
                33,
                "Heath Or Rough Grassland And Marsh And Scattered Mixed Trees"
              ],
              [
                34,
                "Heath Or Rough Grassland And Marsh And Scattered Non-Coniferous Trees"
              ],
              [
                35,
                "Heath Or Rough Grassland And Marsh And Scrub"
              ],
              [
                36,
                "Heath Or Rough Grassland And Sand Or Shingle"
              ],
              [
                37,
                "Heath Or Rough Grassland And Scattered Boulders Or Scattered Rock"
              ],
              [
                38,
                "Heath Or Rough Grassland And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                39,
                "Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                40,
                "Heath Or Rough Grassland And Scattered Coniferous Trees And Scrub"
              ],
              [
                41,
                "Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                42,
                "Heath Or Rough Grassland And Scattered Mixed Trees And Scrub"
              ],
              [
                43,
                "Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                44,
                "Heath Or Rough Grassland And Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                45,
                "Heath Or Rough Grassland And Scattered Rock"
              ],
              [
                46,
                "Heath Or Rough Grassland And Scattered Rock And Scrub"
              ],
              [
                47,
                "Heath Or Rough Grassland And Scrub"
              ],
              [
                48,
                "Helipad"
              ],
              [
                49,
                "Inspection Cover"
              ],
              [
                50,
                "Landfill"
              ],
              [
                51,
                "Livestock Pen"
              ],
              [
                52,
                "Made Surface"
              ],
              [
                53,
                "Marsh"
              ],
              [
                54,
                "Marsh And Heath Or Rough Grassland"
              ],
              [
                55,
                "Marsh And Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                56,
                "Marsh And Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                57,
                "Marsh And Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                58,
                "Marsh And Heath Or Rough Grassland And Scrub"
              ],
              [
                59,
                "Marsh And Non-Coniferous Trees"
              ],
              [
                60,
                "Marsh And Non-Coniferous Trees And Scrub"
              ],
              [
                61,
                "Marsh And Scattered Boulders Or Scattered Rock"
              ],
              [
                62,
                "Marsh And Scrub"
              ],
              [
                63,
                "Mixed Trees"
              ],
              [
                64,
                "Mixed Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                65,
                "Mixed Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                66,
                "Mixed Trees And Scrub"
              ],
              [
                67,
                "Mud"
              ],
              [
                68,
                "Mud And Boulders Or Rock"
              ],
              [
                69,
                "Mud And Boulders Or Rock And Sand Or Shingle"
              ],
              [
                70,
                "Mud And Sand Or Shingle"
              ],
              [
                71,
                "Natural Chimney"
              ],
              [
                72,
                "Non-Coniferous Trees"
              ],
              [
                73,
                "Non-Coniferous Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                74,
                "Non-Coniferous Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                75,
                "Non-Coniferous Trees And Scrub"
              ],
              [
                76,
                "Orchard"
              ],
              [
                77,
                "Peat"
              ],
              [
                78,
                "Quarry"
              ],
              [
                79,
                "Residential Garden"
              ],
              [
                80,
                "Runway"
              ],
              [
                81,
                "Saltmarsh"
              ],
              [
                82,
                "Sand Or Shingle"
              ],
              [
                83,
                "Scattered Boulders Or Scattered Rock"
              ],
              [
                84,
                "Scattered Boulders Or Scattered Rock And Scattered Coniferous Trees"
              ],
              [
                85,
                "Scattered Boulders Or Scattered Rock And Scattered Mixed Trees And Scrub"
              ],
              [
                86,
                "Scattered Boulders Or Scattered Rock And Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                87,
                "Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                88,
                "Scattered Coniferous Trees"
              ],
              [
                89,
                "Scattered Coniferous Trees And Scrub"
              ],
              [
                90,
                "Scattered Mixed Trees"
              ],
              [
                91,
                "Scattered Mixed Trees And Scrub"
              ],
              [
                92,
                "Scattered Non-Coniferous Trees"
              ],
              [
                93,
                "Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                94,
                "Scree"
              ],
              [
                95,
                "Scrub"
              ],
              [
                96,
                "Shellfish Farming on Mud And Sand Or Shingle"
              ],
              [
                97,
                "Shellfish Farming on Sand Or Shingle"
              ],
              [
                98,
                "Slipway"
              ],
              [
                99,
                "Sloping Masonry"
              ],
              [
                100,
                "Slurry Bed"
              ],
              [
                101,
                "Spoil Heap"
              ],
              [
                102,
                "Spreads"
              ],
              [
                103,
                "Steps"
              ],
              [
                104,
                "Target"
              ],
              [
                105,
                "Taxiway"
              ],
              [
                106,
                "Tennis Court"
              ],
              [
                107,
                "Vineyard"
              ],
              [
                108,
                "Watercress Bed"
              ],
              [
                109,
                "{% endtab %}"
              ]
            ]
          },
          "omittedCellCount": 110,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 110,
          "structureStatus": "bounded-structural-projection"
        },
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
            "retainedLabelRows": 111,
            "rowLimit": 1024,
            "sourceColumn": "Label",
            "sourceLabelRows": 111,
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
                "Arable Or Grazing Land"
              ],
              [
                1,
                "Bare Earth Or Grass"
              ],
              [
                2,
                "Boulder"
              ],
              [
                3,
                "Boulders Or Rock"
              ],
              [
                4,
                "Boulders Or Rock And Heath Or Rough Grassland"
              ],
              [
                5,
                "Boulders Or Rock And Heath Or Rough Grassland And Marsh"
              ],
              [
                6,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                7,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                8,
                "Boulders Or Rock And Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                9,
                "Boulders Or Rock And Heath Or Rough Grassland Or Marsh"
              ],
              [
                10,
                "Boulders Or Rock And Marsh"
              ],
              [
                11,
                "Boulders Or Rock And Mud"
              ],
              [
                12,
                "Boulders Or Rock And Mud And Sand Or Shingle"
              ],
              [
                13,
                "Boulders Or Rock And Mud And Sand Or Shingle"
              ],
              [
                14,
                "Boulders Or Rock And Sand Or Shingle"
              ],
              [
                15,
                "Boulders Or Rock And Sand Or Shingle And Scattered Coniferous Trees"
              ],
              [
                16,
                "Boulders Or Rock And Scattered Coniferous Trees"
              ],
              [
                17,
                "Boulders Or Rock And Scattered Mixed Trees"
              ],
              [
                18,
                "Boulders Or Rock And Scattered Non-Coniferous Trees"
              ],
              [
                19,
                "Coniferous Trees"
              ],
              [
                20,
                "Coniferous Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                21,
                "Coniferous Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                22,
                "Coniferous Trees And Scrub"
              ],
              [
                23,
                "Construction Site"
              ],
              [
                24,
                "Firing Point"
              ],
              [
                25,
                "Floral Clock"
              ],
              [
                26,
                "Gallops"
              ],
              [
                27,
                "Games Court"
              ],
              [
                28,
                "Heath"
              ],
              [
                29,
                "Heath Or Rough Grassland"
              ],
              [
                30,
                "Heath Or Rough Grassland And Boulders Or Rock And Scattered Mixed Trees"
              ],
              [
                31,
                "Heath Or Rough Grassland And Marsh"
              ],
              [
                32,
                "Heath Or Rough Grassland And Marsh And Scattered Coniferous Trees"
              ],
              [
                33,
                "Heath Or Rough Grassland And Marsh And Scattered Mixed Trees"
              ],
              [
                34,
                "Heath Or Rough Grassland And Marsh And Scattered Non-Coniferous Trees"
              ],
              [
                35,
                "Heath Or Rough Grassland And Marsh And Scrub"
              ],
              [
                36,
                "Heath Or Rough Grassland And Sand Or Shingle"
              ],
              [
                37,
                "Heath Or Rough Grassland And Scattered Boulders Or Scattered Rock"
              ],
              [
                38,
                "Heath Or Rough Grassland And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                39,
                "Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                40,
                "Heath Or Rough Grassland And Scattered Coniferous Trees And Scrub"
              ],
              [
                41,
                "Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                42,
                "Heath Or Rough Grassland And Scattered Mixed Trees And Scrub"
              ],
              [
                43,
                "Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                44,
                "Heath Or Rough Grassland And Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                45,
                "Heath Or Rough Grassland And Scattered Rock"
              ],
              [
                46,
                "Heath Or Rough Grassland And Scattered Rock And Scrub"
              ],
              [
                47,
                "Heath Or Rough Grassland And Scrub"
              ],
              [
                48,
                "Helipad"
              ],
              [
                49,
                "Inspection Cover"
              ],
              [
                50,
                "Landfill"
              ],
              [
                51,
                "Livestock Pen"
              ],
              [
                52,
                "Made Surface"
              ],
              [
                53,
                "Marsh"
              ],
              [
                54,
                "Marsh And Heath Or Rough Grassland"
              ],
              [
                55,
                "Marsh And Heath Or Rough Grassland And Scattered Coniferous Trees"
              ],
              [
                56,
                "Marsh And Heath Or Rough Grassland And Scattered Mixed Trees"
              ],
              [
                57,
                "Marsh And Heath Or Rough Grassland And Scattered Non-Coniferous Trees"
              ],
              [
                58,
                "Marsh And Heath Or Rough Grassland And Scrub"
              ],
              [
                59,
                "Marsh And Non-Coniferous Trees"
              ],
              [
                60,
                "Marsh And Non-Coniferous Trees And Scrub"
              ],
              [
                61,
                "Marsh And Scattered Boulders Or Scattered Rock"
              ],
              [
                62,
                "Marsh And Scrub"
              ],
              [
                63,
                "Mixed Trees"
              ],
              [
                64,
                "Mixed Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                65,
                "Mixed Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                66,
                "Mixed Trees And Scrub"
              ],
              [
                67,
                "Mud"
              ],
              [
                68,
                "Mud And Boulders Or Rock"
              ],
              [
                69,
                "Mud And Boulders Or Rock And Sand Or Shingle"
              ],
              [
                70,
                "Mud And Sand Or Shingle"
              ],
              [
                71,
                "Natural Chimney"
              ],
              [
                72,
                "Non-Coniferous Trees"
              ],
              [
                73,
                "Non-Coniferous Trees And Scattered Boulders Or Scattered Rock"
              ],
              [
                74,
                "Non-Coniferous Trees And Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                75,
                "Non-Coniferous Trees And Scrub"
              ],
              [
                76,
                "Orchard"
              ],
              [
                77,
                "Peat"
              ],
              [
                78,
                "Quarry"
              ],
              [
                79,
                "Residential Garden"
              ],
              [
                80,
                "Runway"
              ],
              [
                81,
                "Saltmarsh"
              ],
              [
                82,
                "Sand Or Shingle"
              ],
              [
                83,
                "Scattered Boulders Or Scattered Rock"
              ],
              [
                84,
                "Scattered Boulders Or Scattered Rock And Scattered Coniferous Trees"
              ],
              [
                85,
                "Scattered Boulders Or Scattered Rock And Scattered Mixed Trees And Scrub"
              ],
              [
                86,
                "Scattered Boulders Or Scattered Rock And Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                87,
                "Scattered Boulders Or Scattered Rock And Scrub"
              ],
              [
                88,
                "Scattered Coniferous Trees"
              ],
              [
                89,
                "Scattered Coniferous Trees And Scrub"
              ],
              [
                90,
                "Scattered Mixed Trees"
              ],
              [
                91,
                "Scattered Mixed Trees And Scrub"
              ],
              [
                92,
                "Scattered Non-Coniferous Trees"
              ],
              [
                93,
                "Scattered Non-Coniferous Trees And Scrub"
              ],
              [
                94,
                "Scree"
              ],
              [
                95,
                "Scrub"
              ],
              [
                96,
                "Shellfish Farming on Mud And Sand Or Shingle"
              ],
              [
                97,
                "Shellfish Farming on Sand Or Shingle"
              ],
              [
                98,
                "Slipway"
              ],
              [
                99,
                "Sloping Masonry"
              ],
              [
                100,
                "Slurry Bed"
              ],
              [
                101,
                "Spoil Heap"
              ],
              [
                102,
                "Spreads"
              ],
              [
                103,
                "Steps"
              ],
              [
                104,
                "Target"
              ],
              [
                105,
                "Taxiway"
              ],
              [
                106,
                "Tennis Court"
              ],
              [
                107,
                "Vineyard"
              ],
              [
                108,
                "Watercress Bed"
              ],
              [
                109,
                "{% endtab %}"
              ],
              [
                110,
                "{% endtabs %}"
              ]
            ]
          },
          "omittedCellCount": 111,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 2,
          "sourceRowCount": 111,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "landdescriptionvalue"
    },
    "structureStatus": "projected",
    "title": "landdescriptionvalue",
    "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md"
  }
}
---

# landdescriptionvalue

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/code-lists/code-lists-overview/landdescriptionvalue.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
