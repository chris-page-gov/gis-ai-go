---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fadministrative-and-statistical-units%2Ffunctional-areas%2Fretail-area-minor.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Retail Area Minor",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md",
      "retrievedAt": "2026-10-02T08:12:58.052526Z",
      "responseSha256": "df3f0da1c2833be7e6b21cc137cd6fcfd521ac781afdf79c311e59d3cf332acb",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/99",
      "normalisedRecordSha256": "450e46a720d2fd63d1d76f155cfc1b8491731e832a2dbce7e2d5258745f69499",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:12:58.052526Z",
      "sha256": "df3f0da1c2833be7e6b21cc137cd6fcfd521ac781afdf79c311e59d3cf332acb",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "df3f0da1c2833be7e6b21cc137cd6fcfd521ac781afdf79c311e59d3cf332acb",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Retail Area Minor"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Temporal filtering"
        },
        {
          "level": 2,
          "role": "section",
          "text": "What is temporal filtering?"
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
          "text": "featureid"
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
          "text": "dividingfeature\\_siteid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name1\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name1\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name2\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name2\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name3\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name3\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name4\\_text"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dividingfeature\\_name4\\_language"
        },
        {
          "level": 3,
          "role": "section",
          "text": "oslandusetiera"
        },
        {
          "level": 3,
          "role": "section",
          "text": "addresscount\\_retail"
        },
        {
          "level": 3,
          "role": "section",
          "text": "retailareaaggregatedid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "easting"
        },
        {
          "level": 3,
          "role": "section",
          "text": "northing"
        },
        {
          "level": 3,
          "role": "section",
          "text": "longitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "latitude"
        },
        {
          "level": 2,
          "role": "section",
          "text": "Related Entity"
        },
        {
          "level": 3,
          "role": "section",
          "text": "relatedentityid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "featuretypeid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "featuretypeversiondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "crossreferencefeature"
        },
        {
          "level": 3,
          "role": "section",
          "text": "crossreferenceid"
        },
        {
          "level": 3,
          "role": "section",
          "text": "relationshiptype"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 10,
        "headings": 37,
        "referenceCandidatesReviewed": 15,
        "referenceLinks": 15,
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
          "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/retailareaminordescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/landusetieravalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/dataentitycatalogueretailareavalue.md"
        },
        {
          "followed": false,
          "kind": "schema-reference",
          "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/pages/Q7gtOUP3ZsUiEz6ix01v#v2.0"
        }
      ],
      "tables": [],
      "title": "Retail Area Minor"
    },
    "structureStatus": "projected",
    "title": "Retail Area Minor",
    "url": "https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md"
  }
}
---

# Retail Area Minor

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/administrative-and-statistical-units/functional-areas/retail-area-minor.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
