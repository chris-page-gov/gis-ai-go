---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Ftransport%2Ftransport-features%2Froad-track-or-path.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Road Track Or Path",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md",
      "retrievedAt": "2026-10-02T08:14:30.998817Z",
      "responseSha256": "70ac2144620481971fc46af60a52a889619f748e72097e38460d539f5f5afa4f",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/156",
      "normalisedRecordSha256": "872ffef322ffa6b32fa49695566c6eb35ad31d265e4ad6b697262ef24fe8dd33",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:14:30.998817Z",
      "sha256": "70ac2144620481971fc46af60a52a889619f748e72097e38460d539f5f5afa4f",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "70ac2144620481971fc46af60a52a889619f748e72097e38460d539f5f5afa4f",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Road Track Or Path"
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
          "text": "firstdigitalcapturedate"
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
          "text": "geometry\\_area\\_m2 (formerly geometry\\_area )"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_capturemethod"
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
          "text": "description\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "description\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "description\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "description\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcovertiera"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcovertierb"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcover\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcover\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcover\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandcover\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandusetiera"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandusetierb"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslanduse\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslanduse\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslanduse\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslanduse\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "istidal"
        },
        {
          "level": 3,
          "role": "section",
          "text": "associatedstructure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "isobscured"
        },
        {
          "level": 3,
          "role": "section",
          "text": "physicallevel"
        },
        {
          "level": 3,
          "role": "section",
          "text": "capturespecification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "containingsitecount"
        },
        {
          "level": 3,
          "role": "section",
          "text": "smallestsite\\_siteid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "smallestsite\\_landusetiera"
        },
        {
          "level": 3,
          "role": "section",
          "text": "smallestsite\\_landusetierb"
        },
        {
          "level": 3,
          "role": "section",
          "text": "largestsite\\_landusetiera"
        },
        {
          "level": 3,
          "role": "section",
          "text": "largestsite\\_landusetierb"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nlud\\_code"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nlud\\_orderdescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nlud\\_groupdescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "address\\_classificationcode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "address\\_primarydescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "address\\_secondarydescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "lowertierlocalauthority\\_gsscode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "lowertierlocalauthority\\_count"
        },
        {
          "level": 3,
          "role": "section",
          "text": "status"
        },
        {
          "level": 3,
          "role": "section",
          "text": "status\\_updatedate"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Habitat Coverage Reference"
        },
        {
          "level": 3,
          "role": "section",
          "text": "osid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "scheme"
        },
        {
          "level": 3,
          "role": "section",
          "text": "habitatcode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "habitatdescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "percentage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "percentage\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "percentage\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "featuretypeversiondate"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Site Reference"
        },
        {
          "level": 3,
          "role": "section",
          "text": "siteid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadtrackorpathid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadtrackorpathversiondate"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 37,
        "headings": 71,
        "referenceCandidatesReviewed": 46,
        "referenceLinks": 46,
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
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#data-schema-version-table"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturemethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/themevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadtrackorpathdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadtrackorpathlandcovertieravalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roadtrackorpathlandcovertierbvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landusetieravalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landusetierbvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/compoundstructuredescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/physicallevelvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturespecificationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/statusvalue.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-land-cover-enhancements/cross-reference-table"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newcontainingsitecount"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newsmallestsite_siteid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newsmallestsite_landusetiera"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newsmallestsite_landusetierb"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newlargestsite_landusetiera"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newlargestsite_landusetierb"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newnlud_code"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newnlud_orderdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#new-nlud_groupdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newaddress_classificationcode"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newaddress_primarydescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newaddress_secondarydescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newlowertierlocalauthority_gsscode"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newlowertierlocalauthority_count"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newstatus"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newstatus_updatedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newsiteid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newroadtrackorpathid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md#newroadtrackorpathversiondate"
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
                  "nativeText": "3.2",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "3.1",
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
      "title": "Road Track Or Path"
    },
    "structureStatus": "projected",
    "title": "Road Track Or Path",
    "url": "https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md"
  }
}
---

# Road Track Or Path

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/transport/transport-features/road-track-or-path.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
