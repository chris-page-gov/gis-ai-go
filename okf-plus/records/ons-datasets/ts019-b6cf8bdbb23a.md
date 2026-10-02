---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/TS019",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Migrant Indicator",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged one year and over in England and Wales by their address one year ago, in order to determine their status as a migrant from within or outside the UK. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS019",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS019",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "migrant_ind"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/9",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/109",
      "normalisedRecordSha256": "aafecc29b391981f06d02cd8826dcd602b55c14d58b8487269d7c642a85dd9fe",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:32:31.533686Z",
      "responseSha256": "69444f97f068cce9350debfac0403802855b0d252b1f50357dad940a54e19ce0",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/109",
      "normalisedRecordSha256": "e35bc2eda763f6d0809de376d4100afdbb1cd45645da4c50446b442152614fa3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS019"
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
    "metadataModified": "2023-03-28T08:30:09.84Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "ONS published-data terms apply; dataset-specific notices and third-party rights must be checked.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Time-option extrema describe available native codes; continuity and populated observation cells have not been established."
  ],
  "details": {
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged one year and over in England and Wales by their address one year ago, in order to determine their status as a migrant from within or outside the UK. The estimates are as at Census Day, 21 March 2021.",
    "id": "TS019",
    "keywords": [
      "ltla",
      "migrant_ind"
    ],
    "last_updated": "2023-03-28T08:30:09.84Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Migrant Indicator",
    "type": "cantabular_flexible_table",
    "unit_of_measure": "Person",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
          "id": "ltla",
          "label": "Lower tier local authorities",
          "name": "ltla"
        },
        {
          "description": "The migration indicator classifies people based on the difference between their current address and their address one year ago. It provides an indicator of the movement of people within the UK and from outside the UK, in the one-year period before the census.",
          "id": "migrant_ind",
          "label": "Migrant indicator (5 categories)",
          "name": "migrant_ind"
        }
      ],
      "edition": "2021",
      "id": "TS019",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged one year and over in England and Wales by their address one year ago, in order to determine their status as a migrant from within or outside the UK. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-03-28T00:00:00.000Z",
        "state": "published",
        "title": "Migrant Indicator",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS019"
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
        "retrievedAt": "2026-10-02T01:32:31.533686Z",
        "sha256": "69444f97f068cce9350debfac0403802855b0d252b1f50357dad940a54e19ce0",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS019/editions"
  }
}
---

# Migrant Indicator

This dataset provides Census 2021 estimates that classify usual residents aged one year and over in England and Wales by their address one year ago, in order to determine their status as a migrant from within or outside the UK. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS019`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS019)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
