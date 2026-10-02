---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Faddress%2Fgb-address%2Fstreet-address.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Street Address",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md",
      "retrievedAt": "2026-10-02T08:12:07.573367Z",
      "responseSha256": "53341d12a4d11864e789cf143768991137834c65fc60f30ddc067e5298138a79",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/59",
      "normalisedRecordSha256": "2952a08c615f7770ad3d6c1ee48927c7254b20dbb262da23b6010910dfa8c472",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:12:07.573367Z",
      "sha256": "53341d12a4d11864e789cf143768991137834c65fc60f30ddc067e5298138a79",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "53341d12a4d11864e789cf143768991137834c65fc60f30ddc067e5298138a79",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Street Address"
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
          "text": "usrn"
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
          "text": "streettype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "classification"
        },
        {
          "level": 3,
          "role": "section",
          "text": "operationalstate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "operationalstatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "streetname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "locality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "townname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "administrativearea"
        },
        {
          "level": 3,
          "role": "section",
          "text": "country"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatelanguagestreetname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatelanguagelocality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatelanguagetownname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatelanguageadministrativearea"
        },
        {
          "level": 3,
          "role": "section",
          "text": "alternatelanguage"
        },
        {
          "level": 3,
          "role": "section",
          "text": "snnauthoritycode"
        },
        {
          "level": 3,
          "role": "section",
          "text": "snnauthoritydescription"
        },
        {
          "level": 3,
          "role": "section",
          "text": "surfacematerial"
        },
        {
          "level": 3,
          "role": "section",
          "text": "starteasting"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startnorthing"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endeasting"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endnorthing"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startlatitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "startlongitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endlatitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "endlongitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry"
        },
        {
          "level": 3,
          "role": "section",
          "text": "streettolerance"
        },
        {
          "level": 3,
          "role": "section",
          "text": "effectivestartdate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "effectiveenddate"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 11,
        "headings": 40,
        "referenceCandidatesReviewed": 13,
        "referenceLinks": 13,
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
          "url": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/streetdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/addressstreettypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/streetclassificationvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/streetstatecode.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/countryvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/languagevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/streetsurfacecode.md"
        }
      ],
      "tables": [],
      "title": "Street Address"
    },
    "structureStatus": "projected",
    "title": "Street Address",
    "url": "https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md"
  }
}
---

# Street Address

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/address/gb-address/street-address.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
