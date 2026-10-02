---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fland-use%2Fland-use-features.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Land Use Features",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md",
      "retrievedAt": "2026-10-02T08:13:38.842405Z",
      "responseSha256": "d5d7bfbc59ad3c5924fe75c67381bc36f6507d8ec0b9f3beb35df4cb1c49545d",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/125",
      "normalisedRecordSha256": "be2ec1152555444ae22667a3544e396cffa6b9c693d620e307ce03f50f1912e0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:13:38.842405Z",
      "sha256": "d5d7bfbc59ad3c5924fe75c67381bc36f6507d8ec0b9f3beb35df4cb1c49545d",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "d5d7bfbc59ad3c5924fe75c67381bc36f6507d8ec0b9f3beb35df4cb1c49545d",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Land Use Features"
        },
        {
          "level": 4,
          "role": "section",
          "text": "What is a land use site?"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Collection applications"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Key elements"
        },
        {
          "level": 2,
          "role": "section",
          "text": "FAQs"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Coverage"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Default coordinate reference system"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Temporal filtering"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Supply formats"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Supply mechanism"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Using our data"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 3,
        "headings": 11,
        "referenceCandidatesReviewed": 7,
        "referenceLinks": 7,
        "rejectedReferences": 4,
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
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features/site.md#newstatus"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/faqs.md#os-ngd-land-and-land-use-themes-faqs"
        }
      ],
      "tables": [
        {
          "columns": [
            {
              "label": "Sites where Status attribute values are recorded",
              "position": 0,
              "role": "unprojected"
            }
          ],
          "complexSpans": false,
          "format": "markdown",
          "hasExplicitHeader": true,
          "omittedCellCount": 127,
          "raggedRowsOmitted": 0,
          "rows": [],
          "sourceColumnCount": 1,
          "sourceRowCount": 127,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Land Use Features"
    },
    "structureStatus": "projected",
    "title": "Land Use Features",
    "url": "https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md"
  }
}
---

# Land Use Features

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/land-use/land-use-features.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
