---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fwater%2Fwater-network%2Fwater-link.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Water Link",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md",
      "retrievedAt": "2026-10-02T08:15:29.682181Z",
      "responseSha256": "f91c20f97778bd5ec59c5054dc050e11c167e18ded990b6064f7a8c5c9870574",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/190",
      "normalisedRecordSha256": "9ca9735c4292c4205e413dc77a93faea387517e09d8e8bf84e36267545c5c054",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:15:29.682181Z",
      "sha256": "f91c20f97778bd5ec59c5054dc050e11c167e18ded990b6064f7a8c5c9870574",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "f91c20f97778bd5ec59c5054dc050e11c167e18ded990b6064f7a8c5c9870574",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Water Link"
        },
        {
          "level": 2,
          "role": "schema",
          "text": "Data schema versioning"
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
          "text": "primacy"
        },
        {
          "level": 3,
          "role": "section",
          "text": "watertype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "physicallevel"
        },
        {
          "level": 3,
          "role": "section",
          "text": "physicalcontainment"
        },
        {
          "level": 3,
          "role": "section",
          "text": "flowdirection"
        },
        {
          "level": 3,
          "role": "section",
          "text": "permanence"
        },
        {
          "level": 3,
          "role": "section",
          "text": "capturespecification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "levelofdetail"
        },
        {
          "level": 3,
          "role": "section",
          "text": "catchmentname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "catchmentid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_average"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_minimum"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_maximum"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_derivationmethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_evidencedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "width\\_updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "gradient"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startnode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endnode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nameid"
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
          "text": "namesecondaryid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namesecondary1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namesecondary1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namesecondary2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namesecondary2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nametertiaryid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nametertiary1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nametertiary1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nametertiary2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nametertiary2\\_language"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 18,
        "headings": 57,
        "referenceCandidatesReviewed": 25,
        "referenceLinks": 25,
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
          "url": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address/gb-address/built-address#data-schema-version-table"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-temporal-filtering"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkgeometrysourcevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/themevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkprimacyvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkwatertypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/physicallevelvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkphysicalcontainmentvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkflowdirectionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkpermanencevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/capturespecificationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinklevelofdetailvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/waterlinkwidthderivationmethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
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
          "omittedCellCount": 6,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "2.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 2,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Water Link"
    },
    "structureStatus": "projected",
    "title": "Water Link",
    "url": "https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md"
  }
}
---

# Water Link

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/water/water-network/water-link.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
