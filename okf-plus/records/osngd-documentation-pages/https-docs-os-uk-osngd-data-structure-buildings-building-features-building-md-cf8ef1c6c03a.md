---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fbuildings%2Fbuilding-features%2Fbuilding.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Building",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md",
      "retrievedAt": "2026-10-02T08:13:11.042189Z",
      "responseSha256": "44fcacc0725b5fe38f8e88e0f274d06b23a69f2893ad8fd98de7c5b44df59f3f",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/107",
      "normalisedRecordSha256": "d89cbd9b2101a863099a02ac0fdbda752546b3702006885c8a91bf046e958c60",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:13:11.042189Z",
      "sha256": "44fcacc0725b5fe38f8e88e0f274d06b23a69f2893ad8fd98de7c5b44df59f3f",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "44fcacc0725b5fe38f8e88e0f274d06b23a69f2893ad8fd98de7c5b44df59f3f",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Building"
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
          "text": "geometry\\_area\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry\\_updatedate"
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
          "text": "description\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "physicalstate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "physicalstate\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingpartcount"
        },
        {
          "level": 3,
          "role": "section",
          "text": "isinsite"
        },
        {
          "level": 3,
          "role": "section",
          "text": "primarysiteid (formerly primarysite\\_id)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "containingsitecount"
        },
        {
          "level": 3,
          "role": "section",
          "text": "mainbuildingid (formerly mainbuilding\\_id)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "mainbuildingid\\_ismainbuilding (formerly ismainbuilding)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "mainbuildingid\\_updatedate (formerly mainbuilding\\_updatedate)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_oslandusetiera (formerly oslandusetiera)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_addresscount\\_total (formerly addresscount\\_total)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_addresscount\\_residential (formerly addresscount\\_residential)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_addresscount\\_commercial (formerly addresscount\\_commercial)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_addresscount\\_other (formerly addresscount\\_other)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildinguse\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "connectivity"
        },
        {
          "level": 3,
          "role": "section",
          "text": "connectivity\\_count (formerly connectivitycount)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "connectivity\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "constructionmaterial\\_thirdpartyprovenance"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_period"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_year"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingage\\_thirdpartyprovenance"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_selfcontained"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "basementpresence\\_thirdpartyprovenance"
        },
        {
          "level": 3,
          "role": "section",
          "text": "numberoffloors"
        },
        {
          "level": 3,
          "role": "section",
          "text": "numberoffloors\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "numberoffloors\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "numberoffloors\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "numberoffloors\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_absolutemin\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_absoluteroofbase\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_absolutemax\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_relativeroofbase\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_relativemax\\_m"
        },
        {
          "level": 3,
          "role": "section",
          "text": "height\\_confidencelevel"
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
          "text": "roofmaterial\\_primarymaterial"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_solarpanelpresence"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_greenroofpresence"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_confidenceindicator"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofmaterial\\_capturemethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_shape"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areapitched\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areaflat\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingnorth\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingnortheast\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingeast\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingsoutheast\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingsouth\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingsouthwest\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingwest\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areafacingnorthwest\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areaindeterminable\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_areatotal\\_m2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_confidenceindicator"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roofshapeaspect\\_capturemethod"
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
          "text": "buildingid"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 29,
        "headings": 105,
        "referenceCandidatesReviewed": 40,
        "referenceLinks": 40,
        "rejectedReferences": 2,
        "tables": 1
      },
      "omitted": {
        "agentInstructionSectionOmitted": true,
        "exampleOrContactSectionsOmitted": 0,
        "fencedBlocksOmitted": 0
      },
      "projectionTruncated": true,
      "projectionVersion": "os-documentation-structure.v2",
      "references": [
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md#data-schema-version-table"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/physicalstatevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/yesnovalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingusevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landusetieravalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingconnectivitytypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/constructionmaterialvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/constructionmaterialsourcevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturemethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingageperiodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/buildingagesourcevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/presencevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/basementpresencesourcevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/builtstructureheightconfidencevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roofmaterialvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roofconfidenceindicatorvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/roofshapevalue.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md#numberoffloors_evidencedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md#numberoffloors_updatedate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md#numberoffloors_source"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md#numberoffloors_capturemethod"
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
          "omittedCellCount": 27,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "4.1",
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
                  "nativeText": "3.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 2
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "3.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 3
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 4
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 5
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.2",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 6
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 7
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 8
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 9,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Building"
    },
    "structureStatus": "projected",
    "title": "Building",
    "url": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md"
  }
}
---

# Building

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
