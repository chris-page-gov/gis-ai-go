---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fland-use%2Fland-use-features%2Fsite.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Site",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md",
      "retrievedAt": "2026-10-02T08:13:39.907235Z",
      "responseSha256": "105125d0253a8e4bb141192b493d6ba81a5a08f948b75412abd28968f72f9bb9",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/126",
      "normalisedRecordSha256": "50428a392a75201d4181d8bfe4e4cbd8f1600699e18e2f362c0ae449be414030",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:13:39.907235Z",
      "sha256": "105125d0253a8e4bb141192b493d6ba81a5a08f948b75412abd28968f72f9bb9",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "105125d0253a8e4bb141192b493d6ba81a5a08f948b75412abd28968f72f9bb9",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Site"
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
          "text": "stakeholder"
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
          "text": "name1\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name1\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name1\\_source"
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
          "text": "name2\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name2\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "name2\\_source"
        },
        {
          "level": 3,
          "role": "section",
          "text": "extentdefinition"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matcheduprn (formerly primaryuprn)"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matcheduprn\\_method"
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
          "text": "address\\_classificationcorrelation"
        },
        {
          "level": 3,
          "role": "section",
          "text": "address\\_classificationsource"
        },
        {
          "level": 3,
          "role": "section",
          "text": "addresscount\\_total"
        },
        {
          "level": 3,
          "role": "section",
          "text": "addresscount\\_residential"
        },
        {
          "level": 3,
          "role": "section",
          "text": "addresscount\\_commercial"
        },
        {
          "level": 3,
          "role": "section",
          "text": "addresscount\\_other"
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
          "text": "mainbuildingid"
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
          "text": "Site to Address Reference"
        },
        {
          "level": 3,
          "role": "section",
          "text": "uprn"
        },
        {
          "level": 3,
          "role": "section",
          "text": "siteid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "siteversiondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "relationshiptype"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 40,
        "headings": 64,
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
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#data-schema-version-table"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sitedescriptionvalue.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/stakeholdervalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/siteextentdefinitionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/matcheduprnvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/classificationcorrelationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/addressclassificationsourcevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/statusvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/relationshiptypevalue.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newgeometry_capturemethod"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newdescription_capturemethod"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newoslanduse_capturemethod"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newmatcheduprn_method"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddress_classificationcode"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddress_secondarydescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddress_classificationcorrelation"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddress_classificationsource"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddresscount_total"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddresscount_residential"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddresscount_commercial"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newaddresscount_other"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newnlud_code"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newnlud_orderdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newnlud_groupdescription"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newmainbuildingid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newstatus"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newuprn"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newsiteid"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newsiteversiondate"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newrelationshiptype"
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
          "omittedCellCount": 24,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.3",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.2",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.1",
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
                  "nativeText": "1.3",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 4
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.2",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 5
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 6
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 7
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 8,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Site"
    },
    "structureStatus": "projected",
    "title": "Site",
    "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md"
  }
}
---

# Site

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
