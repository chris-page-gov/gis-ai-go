---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Ftransport%2Frami%2Frestriction.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Restriction",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md",
      "retrievedAt": "2026-10-02T08:14:15.331403Z",
      "responseSha256": "dc81ba0cf64422c9dad5cb9f2049490c7867efbba0f96c82f02b3d7576c39e36",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/146",
      "normalisedRecordSha256": "cb18bcfa29de26a5c1ea10e5a848500cb1c520726bb7098999f8e85f455a9a93",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:14:15.331403Z",
      "sha256": "dc81ba0cf64422c9dad5cb9f2049490c7867efbba0f96c82f02b3d7576c39e36",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "dc81ba0cf64422c9dad5cb9f2049490c7867efbba0f96c82f02b3d7576c39e36",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Restriction"
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
          "text": "geometry\\_length"
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
          "text": "restriction"
        },
        {
          "level": 3,
          "role": "section",
          "text": "trafficsign1"
        },
        {
          "level": 3,
          "role": "section",
          "text": "trafficsign2"
        },
        {
          "level": 3,
          "role": "section",
          "text": "structure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "inclusion"
        },
        {
          "level": 3,
          "role": "section",
          "text": "exemption"
        },
        {
          "level": 3,
          "role": "section",
          "text": "timeinterval"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure1\\_value"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure1\\_unitofmeasure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure1\\_sourceofmeasure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure2\\_value"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure2\\_unitofmeasure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "measure2\\_sourceofmeasure"
        },
        {
          "level": 3,
          "role": "section",
          "text": "atpositionxcoordinate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "atpositionycoordinate"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Date Time Qualifier"
        },
        {
          "level": 3,
          "role": "section",
          "text": "datetimequalifierid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "restrictionid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "restrictionversiondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "nameddate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startdate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "enddate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startmonthday"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endmonthday"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namedtime"
        },
        {
          "level": 3,
          "role": "section",
          "text": "starttime"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endtime"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namedperiod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "namedday"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Restriction Network Reference"
        },
        {
          "level": 3,
          "role": "section",
          "text": "networkreferenceid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "networkfeaturetype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadlinkdirection"
        },
        {
          "level": 3,
          "role": "section",
          "text": "roadlinksequence"
        },
        {
          "level": 3,
          "role": "section",
          "text": "restrictionid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "restrictionversiondate"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 15,
        "headings": 50,
        "referenceCandidatesReviewed": 19,
        "referenceLinks": 19,
        "rejectedReferences": 2,
        "tables": 0
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
          "url": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/restrictiontypedescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/restrictionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/structuretypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/vehiclequalifiervalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/sourceofmeasurevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/nameddatevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/namedtimevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/namedperiodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/nameddayvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/networkfeaturetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/linkdirectionvalue.md"
        }
      ],
      "tables": [],
      "title": "Restriction"
    },
    "structureStatus": "projected",
    "title": "Restriction",
    "url": "https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md"
  }
}
---

# Restriction

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/transport/rami/restriction.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
