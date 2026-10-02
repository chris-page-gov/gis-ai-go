---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS051",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of rooms",
  "description": "This dataset provides Census 2021 estimates that classify all household spaces with at least one usual resident in England and Wales by number of rooms. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS051",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:32:04.854179Z",
      "responseSha256": "57750698a8cd517c410135df45f483e7f64423414202446281d1ef685ee2a09b",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/77",
      "normalisedRecordSha256": "bad1a10dc774a625f2be9aaa3347dffb7f4caa52acde893154cfeafb6ffc6aaf",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4"
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
    "releaseVersion": "4"
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
        "description": "A room can be any room in a dwelling apart from bathrooms, toilets, halls or landings, kitchens, conservatories or utility rooms. All other rooms, for example, living rooms, studies, bedrooms, separate dining rooms and rooms that can only be used for storage are included. If two rooms have been converted into one, they are counted as one room. The number of rooms is recorded by address, this means that for households living in a shared dwelling the number of rooms are counted for the whole dwelling and not the individual household. This definition is based on the Valuation Office Agency’s (VOA) definition.",
        "id": "voa_number_of_rooms_9a",
        "label": "Number of rooms (Valuation Office Agency) (9 categories)",
        "name": "voa_number_of_rooms_9a"
      }
    ],
    "edition": "2021",
    "id": "TS051",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify all household spaces with at least one usual resident in England and Wales by number of rooms. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-03-28T00:00:00.000Z",
      "state": "published",
      "title": "Number of rooms",
      "unit_of_measure": "Household"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4",
            "id": "4"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS051"
          }
        },
        "isBasedOn": {
          "@id": "HH",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:32:04.854179Z",
      "sha256": "57750698a8cd517c410135df45f483e7f64423414202446281d1ef685ee2a09b",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "4",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4"
  }
}
---

# Number of rooms

This dataset provides Census 2021 estimates that classify all household spaces with at least one usual resident in England and Wales by number of rooms. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS051`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS051/editions/2021/versions/4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
