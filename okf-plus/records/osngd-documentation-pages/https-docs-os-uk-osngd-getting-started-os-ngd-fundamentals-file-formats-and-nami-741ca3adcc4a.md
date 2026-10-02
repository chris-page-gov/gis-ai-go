---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fgetting-started%2Fos-ngd-fundamentals%2Ffile-formats-and-naming.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "File formats and naming",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md",
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
      "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md",
      "retrievedAt": "2026-10-02T08:11:09.371714Z",
      "responseSha256": "fc0f7385f845b0946497621f9a91abdbb46f7c0235e79d1a8446dcd37f23101c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/8",
      "normalisedRecordSha256": "45b77ec37864c8776fa44e9860eff899e9c31705fb174d5d057e15c81f63b60f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md"
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
    "id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:11:09.371714Z",
      "sha256": "fc0f7385f845b0946497621f9a91abdbb46f7c0235e79d1a8446dcd37f23101c",
      "status": 200,
      "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "fc0f7385f845b0946497621f9a91abdbb46f7c0235e79d1a8446dcd37f23101c",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "File formats and naming"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Available formats for OS NGD data"
        },
        {
          "level": 3,
          "role": "section",
          "text": "CSV overview"
        },
        {
          "level": 4,
          "role": "section",
          "text": "CSV structure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "GeoPackage overview"
        },
        {
          "level": 3,
          "role": "section",
          "text": "GeoJSON overview"
        },
        {
          "level": 3,
          "role": "section",
          "text": "Vector tiles overview"
        },
        {
          "level": 2,
          "role": "section",
          "text": "File naming"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 1,
        "headings": 8,
        "referenceCandidatesReviewed": 3,
        "referenceLinks": 3,
        "rejectedReferences": 2,
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
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md"
        }
      ],
      "tables": [
        {
          "columns": [
            {
              "label": "Attribute type",
              "position": 0,
              "role": "unprojected"
            },
            {
              "label": "Quotes (Y/N)",
              "position": 1,
              "role": "unprojected"
            },
            {
              "label": "If NULL",
              "position": 2,
              "role": "unprojected"
            },
            {
              "label": "Example",
              "position": 3,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "html",
          "hasExplicitHeader": true,
          "omittedCellCount": 32,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 4,
          "sourceRowCount": 8,
          "structureStatus": "bounded-structural-projection"
        },
        {
          "columns": [
            {
              "label": "Theme",
              "position": 0,
              "role": "unprojected"
            },
            {
              "label": "Theme Short Code",
              "position": 1,
              "role": "unprojected"
            },
            {
              "label": "Collection",
              "position": 2,
              "role": "collection"
            },
            {
              "label": "Collection Short Code",
              "position": 3,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "html",
          "hasExplicitHeader": true,
          "omittedCellCount": 48,
          "raggedRowsOmitted": 0,
          "rows": [
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS GB Address",
                  "role": "collection"
                }
              ],
              "sourceRow": 0
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Islands Address",
                  "role": "collection"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Boundaries",
                  "role": "collection"
                }
              ],
              "sourceRow": 2
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Functional Areas",
                  "role": "collection"
                }
              ],
              "sourceRow": 3
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS GB Postcodes",
                  "role": "collection"
                }
              ],
              "sourceRow": 4
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS NI Postcodes",
                  "role": "collection"
                }
              ],
              "sourceRow": 5
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Building Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 6
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Named Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 7
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Land Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 8
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Land Use Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 9
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Structure Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 10
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Transport Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 11
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Transport Network",
                  "role": "collection"
                }
              ],
              "sourceRow": 12
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS RAMI",
                  "role": "collection"
                }
              ],
              "sourceRow": 13
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Water Features",
                  "role": "collection"
                }
              ],
              "sourceRow": 14
            },
            {
              "cells": [
                {
                  "column": 2,
                  "nativeText": "OS Water Network",
                  "role": "collection"
                }
              ],
              "sourceRow": 15
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 16,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "File formats and naming"
    },
    "structureStatus": "projected",
    "title": "File formats and naming",
    "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md"
  }
}
---

# File formats and naming

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/file-formats-and-naming.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
