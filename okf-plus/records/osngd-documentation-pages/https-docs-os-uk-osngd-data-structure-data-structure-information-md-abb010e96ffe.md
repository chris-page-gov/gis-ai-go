---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fdata-structure-information.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Data Structure Information",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/data-structure-information.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/data-structure-information.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/data-structure-information.md",
      "retrievedAt": "2026-10-02T08:11:57.969745Z",
      "responseSha256": "f020abf81cda74505685b70330c8dc0791eb245f2c7419b941c57117d7c7c0bb",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/51",
      "normalisedRecordSha256": "14abc1e468d610c25d805925425ffc9bf0260df521a3861fe9f60e7bbd35c575",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/data-structure-information.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/data-structure-information.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:11:57.969745Z",
      "sha256": "f020abf81cda74505685b70330c8dc0791eb245f2c7419b941c57117d7c7c0bb",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/data-structure-information.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "f020abf81cda74505685b70330c8dc0791eb245f2c7419b941c57117d7c7c0bb",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/data-structure-information",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Data Structure Information"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Overview of the OS NGD data structure"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Explore OS NGD data"
        },
        {
          "level": 2,
          "role": "section",
          "text": "What's next?"
        },
        {
          "level": 3,
          "role": "code-list",
          "text": "📝 Code Lists"
        },
        {
          "level": 3,
          "role": "section",
          "text": "📖 OS NGD Fundamentals"
        },
        {
          "level": 3,
          "role": "section",
          "text": "▶️ Getting Started"
        },
        {
          "level": 3,
          "role": "section",
          "text": "📣 OS NGD News"
        },
        {
          "level": 3,
          "role": "section",
          "text": "⚙️ Data and Service Status"
        },
        {
          "level": 3,
          "role": "section",
          "text": "🗺️ OS NGD Sample Data"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 16,
        "headings": 10,
        "referenceCandidatesReviewed": 27,
        "referenceLinks": 27,
        "rejectedReferences": 10,
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
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/data-structure-information.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/address.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/buildings"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/geographical-names"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/structures"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/transport"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/water"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/getting-started-information.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/os-ngd-news/os-ngd-news.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/data-and-service-status/data-and-service-status-information.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/introduction-to-os-ngd/os-ngd-sample-data.md"
        }
      ],
      "tables": [
        {
          "columns": [
            {
              "label": null,
              "position": 0,
              "role": "unprojected"
            },
            {
              "label": null,
              "position": 1,
              "role": "unprojected"
            },
            {
              "label": "Cover image",
              "position": 2,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "html",
          "hasExplicitHeader": true,
          "omittedCellCount": 27,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 3,
          "sourceRowCount": 9,
          "structureStatus": "bounded-structural-projection"
        },
        {
          "columns": [
            {
              "label": null,
              "position": 0,
              "role": "unprojected"
            },
            {
              "label": null,
              "position": 1,
              "role": "unprojected"
            },
            {
              "label": null,
              "position": 2,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "html",
          "hasExplicitHeader": true,
          "omittedCellCount": 18,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 3,
          "sourceRowCount": 6,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Data Structure Information"
    },
    "structureStatus": "projected",
    "title": "Data Structure Information",
    "url": "https://docs.os.uk/osngd/data-structure/data-structure-information.md"
  }
}
---

# Data Structure Information

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/data-structure-information.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/data-structure-information.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
