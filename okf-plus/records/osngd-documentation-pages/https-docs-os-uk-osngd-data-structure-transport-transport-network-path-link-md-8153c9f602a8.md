---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Ftransport%2Ftransport-network%2Fpath-link.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Path Link",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md",
      "retrievedAt": "2026-10-02T08:14:50.023433Z",
      "responseSha256": "292461a3a8e4a4a370d60f9c2187cd16ea06b4f3781be8af2cd98f37a7b0a6aa",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/167",
      "normalisedRecordSha256": "bfe13ecd579979c9dc38d41707220a14dbdf279bae722cce89ea50cf588db445",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:14:50.023433Z",
      "sha256": "292461a3a8e4a4a370d60f9c2187cd16ea06b4f3781be8af2cd98f37a7b0a6aa",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "292461a3a8e4a4a370d60f9c2187cd16ea06b4f3781be8af2cd98f37a7b0a6aa",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Path Link"
        },
        {
          "level": 2,
          "role": "schema",
          "text": "Data schema versioning"
        },
        {
          "level": 3,
          "role": "schema",
          "text": "Data schema version table"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Temporal filtering"
        },
        {
          "level": 2,
          "role": "schema-field",
          "text": "Feature type attributes"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Loading OS NGD CSV files into databases"
        },
        {
          "level": 3,
          "role": "section",
          "text": "osid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "toid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "versiondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "versionavailablefromdate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "versionavailabletodate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "changetype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_length\\_m (formerly geometry\\_length)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "theme"
        },
        {
          "level": 3,
          "role": "section",
          "text": "description"
        },
        {
          "level": 3,
          "role": "section",
          "text": "pathname1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "pathname1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "pathname2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "pathname2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatename1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatename1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatename2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatename2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "surfacetype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "cyclefacility"
        },
        {
          "level": 3,
          "role": "section",
          "text": "cyclefacility\\_wholelink"
        },
        {
          "level": 3,
          "role": "section",
          "text": "elevationgain\\_indirection"
        },
        {
          "level": 3,
          "role": "section",
          "text": "elevationgain\\_againstdirection"
        },
        {
          "level": 3,
          "role": "section",
          "text": "heightingmethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "capturespecification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchstatus"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startnode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startgradeseparation"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endnode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endgradeseparation"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofstreetlight\\_coverage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofstreetlight\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofstreetlight\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofstreetlight\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_overall\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_overallpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_indirection\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_indirectionsegregated\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_indirectionpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_inoppositedirection\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_inoppositedirectionsegregated\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_inoppositedirectionpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofcyclelane\\_capturemethod"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 16,
        "headings": 51,
        "referenceCandidatesReviewed": 22,
        "referenceLinks": 22,
        "rejectedReferences": 2,
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
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md#data-schema-version-table"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-csv.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/changetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/themevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/formofwaytypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/surfacetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/cyclefacilityvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturespecificationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/matchstatusvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/illuminationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturemethodvalue.md"
        }
      ],
      "tables": [
        {
          "columns": [
            {
              "label": "Version ↓",
              "position": 0,
              "role": "schema-version"
            },
            {
              "label": "Launch Date",
              "position": 1,
              "role": "unprojected"
            },
            {
              "label": "Latest Date",
              "position": 2,
              "role": "unprojected"
            },
            {
              "label": "Change",
              "position": 3,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "html",
          "hasExplicitHeader": true,
          "omittedCellCount": 9,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "3.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 2
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 3,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Path Link"
    },
    "structureStatus": "projected",
    "title": "Path Link",
    "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md"
  }
}
---

# Path Link

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/transport/transport-network/path-link.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
