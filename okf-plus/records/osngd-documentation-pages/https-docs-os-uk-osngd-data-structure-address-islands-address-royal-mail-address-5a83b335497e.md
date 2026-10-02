---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation-pages/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Faddress%2Fislands-address%2Froyal-mail-address.md",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Royal Mail Address",
  "description": "Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.",
  "nativeIdentifier": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md",
  "sourceFamily": "osngd-documentation-pages",
  "resource": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md",
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
      "resource": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md",
      "retrievedAt": "2026-10-02T08:12:15.644750Z",
      "responseSha256": "1c132b1638b106e36b42cf0ffee16a776c69b0dde619080aa67ec9dde3f0f6f1",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/osngd-documentation-pages.json",
      "normalisedPointer": "/records/65",
      "normalisedRecordSha256": "e211bde1783cf60e89e9c91a81af77631ff5cb8f227f1e619ef58d78f4313747",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md"
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
    "id": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md",
    "kind": "documentation-page",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T08:12:15.644750Z",
      "sha256": "1c132b1638b106e36b42cf0ffee16a776c69b0dde619080aa67ec9dde3f0f6f1",
      "status": 200,
      "url": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md"
    },
    "metadataStatus": "captured",
    "sourceSha256": "1c132b1638b106e36b42cf0ffee16a776c69b0dde619080aa67ec9dde3f0f6f1",
    "structure": {
      "canonicalUrl": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address",
      "contentCompleteness": "structure-only-not-full-guide-or-vocabulary-conformance",
      "headings": [
        {
          "level": 1,
          "role": "section",
          "text": "Royal Mail Address"
        },
        {
          "level": 2,
          "role": "schema",
          "text": "Data schema versioning"
        },
        {
          "level": 3,
          "role": "schema",
          "text": ":arrows\\_clockwise: Data schema version table"
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
          "text": "udprn"
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
          "text": "organisationname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "departmentname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "subbuildingname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingname"
        },
        {
          "level": 3,
          "role": "section",
          "text": "buildingnumber"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dependentthoroughfare"
        },
        {
          "level": 3,
          "role": "section",
          "text": "thoroughfare"
        },
        {
          "level": 3,
          "role": "section",
          "text": "doubledependentlocality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "dependentlocality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "posttown"
        },
        {
          "level": 3,
          "role": "section",
          "text": "postcode"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: postcodearea"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: postcodedistrict"
        },
        {
          "level": 3,
          "role": "section",
          "text": "Note"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: postcodesector"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: pifchecksumdigit"
        },
        {
          "level": 3,
          "role": "section",
          "text": "Note"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: pifdisplaytext"
        },
        {
          "level": 3,
          "role": "section",
          "text": "Note"
        },
        {
          "level": 3,
          "role": "section",
          "text": "postcodetype"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: country"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: fulladdress"
        },
        {
          "level": 3,
          "role": "section",
          "text": "deliverypointsuffix"
        },
        {
          "level": 3,
          "role": "section",
          "text": "welshdependentthoroughfare"
        },
        {
          "level": 3,
          "role": "section",
          "text": "welshthoroughfare"
        },
        {
          "level": 3,
          "role": "section",
          "text": "welshdoubledependentlocality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "welshdependentlocality"
        },
        {
          "level": 3,
          "role": "section",
          "text": "welshposttown"
        },
        {
          "level": 3,
          "role": "section",
          "text": "poboxnumber"
        },
        {
          "level": 3,
          "role": "section",
          "text": "updatedate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "entrydate"
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
          "text": "latitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "longitude"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometry"
        },
        {
          "level": 3,
          "role": "section",
          "text": "positionalaccuracy"
        },
        {
          "level": 3,
          "role": "section",
          "text": "geometryallocationmethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "unmatchedreason"
        },
        {
          "level": 3,
          "role": "section",
          "text": "unmatchedreasondate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "uprn"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchedaddressfeaturetype"
        },
        {
          "level": 3,
          "role": "section",
          "text": ":new: primaryuprnmatch"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchtype"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchdate"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchmethod"
        },
        {
          "level": 3,
          "role": "section",
          "text": "matchingorganisation"
        }
      ],
      "normalisationRule": "Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.",
      "observed": {
        "distinctAcceptedReferences": 16,
        "headings": 60,
        "referenceCandidatesReviewed": 27,
        "referenceLinks": 27,
        "rejectedReferences": 8,
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
          "url": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md"
        },
        {
          "followed": false,
          "kind": "documentation-reference",
          "url": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md"
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
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/royalmailaddressdescriptionvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/postcodetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/countryvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/positionalaccuracyvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/geometryallocationmethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/matchedaddressfeaturetypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/yesnovalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/rmtolamatchtypevalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/matchmethodvalue.md"
        },
        {
          "followed": false,
          "kind": "code-list-reference",
          "url": "https://docs.os.uk/osngd/code-lists/code-lists-overview/matchingorganisationvalue.md"
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
          "omittedCellCount": 9,
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
                  "nativeText": "1.1",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 1
            },
            {
              "cells": [
                {
                  "column": 0,
                  "nativeText": "1.0",
                  "role": "schema-version"
                }
              ],
              "sourceRow": 2
            }
          ],
          "sourceColumnCount": 4,
          "sourceRowCount": 3,
          "structureStatus": "bounded-structural-projection"
        }
      ],
      "title": "Royal Mail Address"
    },
    "structureStatus": "projected",
    "title": "Royal Mail Address",
    "url": "https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md"
  }
}
---

# Royal Mail Address

Captured official documentation with structural metadata for schema, vocabulary, lifecycle and update discovery.

Native identifier: `https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md`.

Source family: `osngd-documentation-pages`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/osngd/data-structure/address/islands-address/royal-mail-address.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


## Evidence limits

- The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.
- A captured guide does not establish complete vocabulary coverage or API conformance.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
