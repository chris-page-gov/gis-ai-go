---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Ftransport%2Ftransport-network%2Froad-link.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Road Link",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md",
      "retrievedAt": "2026-10-02T08:15:01.248606Z",
      "responseSha256": "108c83189ffa9a51e3e8e076e13ce5d8cbb2a07b7acbd6f3353d57ba1ea7b605",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/175",
      "normalisedRecordSha256": "41d7d87e5f1d21152e81b009d74c6b61c4927a615b555a140088d0c1b617328d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:15:01.248606Z",
      "sha256": "108c83189ffa9a51e3e8e076e13ce5d8cbb2a07b7acbd6f3353d57ba1ea7b605",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "108c83189ffa9a51e3e8e076e13ce5d8cbb2a07b7acbd6f3353d57ba1ea7b605",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Road Link"
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
          "text": "roadclassification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "routehierarchy"
        },
        {
          "level": 3,
          "role": "section",
          "text": "trunkroad"
        },
        {
          "level": 3,
          "role": "section",
          "text": "primaryroute"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadclassificationnumber"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name2\\_language"
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
          "text": "operationalstate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "directionality"
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
          "text": "roadstructure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadwidth\\_average"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadwidth\\_minimum"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadwidth\\_confidencelevel"
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
          "text": "presenceofpavement\\_overall\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_overallpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_left\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_leftpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_right\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_rightpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_minimumwidth\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_averagewidth\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofpavement\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceoftram\\_extentoflink"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceoftram\\_linkdirection"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceoftram\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceoftram\\_source"
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
          "text": "presenceofbuslane\\_overall\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_overallpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_indirection\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_indirectionpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_inoppositedirection\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_inoppositedirectionpercentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "presenceofbuslane\\_capturemethod"
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
        },
        {
          "level": 2,
          "role": "section",
          "text": "Road Track Or Path Reference"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadtrackorpathid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadlinkid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadlinkversiondate"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 22,
        "headings": 90,
        "referenceCandidatesReviewed": 31,
        "referenceLinks": 31,
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
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md#data-schema-version-tabl"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadclassificationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadfunctionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/operationalstatevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/linkdirectionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/cyclefacilityvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadstructurevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadwidthconfidencelevelvalue.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturemethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/extentoflinkvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/illuminationvalue.md"
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
          "omittedCellCount": 15,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "5.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "4.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "3.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 2
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 3
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 4
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 5,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Road Link"
    },
    "structureStatus": "projected",
    "title": "Road Link",
    "url": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md"
  }
}
---

# Road Link

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
