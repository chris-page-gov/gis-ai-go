---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fadministrative-and-statistical-units%2Fboundaries%2Fparish-or-community.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Parish Or Community",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md",
      "retrievedAt": "2026-10-02T08:12:45.883650Z",
      "responseSha256": "c66760f7a5e17c2da3db8ee612702e9ff25b1f0b8c98423ef2163ca68924dbd9",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/89",
      "normalisedRecordSha256": "1a6e5a8160a254e5c508059a6f14cd2d7e69900ccbdb9fe710a07fd29c0a2794",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:12:45.883650Z",
      "sha256": "c66760f7a5e17c2da3db8ee612702e9ff25b1f0b8c98423ef2163ca68924dbd9",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "c66760f7a5e17c2da3db8ee612702e9ff25b1f0b8c98423ef2163ca68924dbd9",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Parish Or Community"
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
          "text": "geometry\\_area"
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
          "text": "gsscode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundarytype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_id"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_featuretype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_classification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_name1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_name1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_name2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference1\\_name2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_id"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_featuretype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_classification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_name1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_name1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_name2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "boundaryparentreference2\\_name2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "landareahectares"
        },
        {
          "level": 3,
          "role": "section",
          "text": "tidalareahectares"
        },
        {
          "level": 3,
          "role": "section",
          "text": "totalareahectares"
        },
        {
          "level": 3,
          "role": "section",
          "text": "hassharedarea"
        },
        {
          "level": 3,
          "role": "section",
          "text": "hasdetachedpart"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 9,
        "headings": 39,
        "referenceCandidatesReviewed": 18,
        "referenceLinks": 18,
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
          "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/parishorcommunitydescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/boundarytypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/parentfeaturetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/parentboundarydescriptionvalue.md"
        }
      ],
      "tables": [],
      "title": "Parish Or Community"
    },
    "structureStatus": "projected",
    "title": "Parish Or Community",
    "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md"
  }
}
---

# Parish Or Community

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/boundaries/parish-or-community.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
