---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS061",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Method used to travel to work",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their method used to travel to work (2001 specification). The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS061",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6/metadata",
      "retrievedAt": "2026-10-02T01:31:57.329216Z",
      "responseSha256": "89ef353a1b16b2e061ab88afb63fd16650795c1805099d73cb5e006876026aee",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/68",
      "normalisedRecordSha256": "a39bda6635890e94289040fd9a074e14e37d05dc4f338f8a35a19a7b050c294e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": null,
    "metadataModified": "0001-01-01T00:00:00Z",
    "releaseVersion": "6"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "dimensions": [
      {
        "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
        "id": "ltla",
        "label": "Lower tier local authorities",
        "name": "ltla"
      },
      {
        "description": "A person's place of work and their method of travel to work. This is the 2001 method of producing travel to work variables. \"Work mainly from home\" applies to someone who indicated their place of work as their home address and travelled to work by driving a car or van, for example visiting clients.",
        "id": "transport_to_workplace_12a",
        "label": "Method used to travel to workplace (12 categories)",
        "name": "transport_to_workplace_12a"
      }
    ],
    "edition": "2021",
    "id": "TS061",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their method used to travel to work (2001 specification). The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2024-01-15T00:00:00.000Z",
      "state": "published",
      "title": "Method used to travel to work",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6",
            "id": "6"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS061"
          }
        },
        "isBasedOn": {
          "@id": "UR",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:57.329216Z",
      "sha256": "89ef353a1b16b2e061ab88afb63fd16650795c1805099d73cb5e006876026aee",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "6",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6"
  }
}
---

# Method used to travel to work

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their method used to travel to work (2001 specification). The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS061`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS061/editions/2021/versions/6)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
