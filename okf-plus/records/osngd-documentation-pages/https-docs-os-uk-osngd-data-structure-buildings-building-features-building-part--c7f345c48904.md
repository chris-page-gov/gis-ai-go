---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fbuildings%2Fbuilding-features%2Fbuilding-part.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Building Part",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md",
      "retrievedAt": "2026-10-02T08:13:14.569766Z",
      "responseSha256": "1f5697494b5f6fb9f039d35dc66e20cd2a68863ddd29aa020675054427368c5b",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/110",
      "normalisedRecordSha256": "2320b2cdfc777e2d352027d4e183c8699fbc4bfbdcd0845eadec52e989be572a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:13:14.569766Z",
      "sha256": "1f5697494b5f6fb9f039d35dc66e20cd2a68863ddd29aa020675054427368c5b",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "1f5697494b5f6fb9f039d35dc66e20cd2a68863ddd29aa020675054427368c5b",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Building Part"
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
          "text": "geometry\\_area\\_m2 (formerly geometry\\_area)"
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
          "text": "height\\_absoluteroofbase\\_m (formerly absoluteheightroofbase)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_relativeroofbase\\_m (formerly relativeheightroofbase)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_absolutemax\\_m (formerly absoluteheightmaximum)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_relativemax\\_m (formerly relativeheightmaximum)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_absolutemin\\_m (formerly absoluteheightminimum)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_confidencelevel (formerly heightconfidencelevel )"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_source"
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
          "text": "buildingpartid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingpartversiondate"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 47,
        "headings": 70,
        "referenceCandidatesReviewed": 56,
        "referenceLinks": 56,
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
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#data-schema-version-table"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingpartdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingpartlandcovertieravalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingpartlandcovertierbvalue.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/builtstructureheightconfidencevalue.md"
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
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#osid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#toid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#versiondate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#versionavailablefromdate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#versionavailabletodate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#firstdigitalcapturedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#geometry_evidencedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#geometry_updatedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#geometry_source"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newdescription_capturemethod"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newcontainingsitecount"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newsmallestsite_siteid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newsmallestsite_landusetiera"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newsmallestsite_landusetierb"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newlargestsite_landusetiera"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newlargestsite_landusetierb"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newnlud_code"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newnlud_orderdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newnlud_groupdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newaddress_classificationcode"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newaddress_primarydescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newaddress_secondarydescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newlowertierlocalauthority_gsscode"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newlowertierlocalauthority_count"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newstatus"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newstatus_updatedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newsiteid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newbuildingpartid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md#newbuildingpartversiondate"
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
                  "nativeText": "2.2",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 2
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.1",
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
      "title": "Building Part"
    },
    "structureStatus": "projected",
    "title": "Building Part",
    "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md"
  }
}
---

# Building Part

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/buildings/building-features/building-part.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
