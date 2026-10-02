---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/TS018",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Age of arrival in the UK",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their age of arrival in the UK. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS018",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS018",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "age_arrival_uk_18a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/10",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/110",
      "normalisedRecordSha256": "680fb837ca3a52d4da3ba7d8961b45a24b73903daef36069320676991bf45f9d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:32:32.372592Z",
      "responseSha256": "4397568b5d521aa7e2dc72aef5ff973d00754be330def8a77cb11aa0479e1e9e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/110",
      "normalisedRecordSha256": "5b6ae3c2e94dac25b1b3d25721457ec1eff308f1a2f84728f949cd2cdc80bbdf",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS018"
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
    "metadataModified": "2023-02-16T09:30:01.219Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their age of arrival in the UK. The estimates are as at Census Day, 21 March 2021.",
    "id": "TS018",
    "keywords": [
      "ltla",
      "age_arrival_uk_18a"
    ],
    "last_updated": "2023-02-16T09:30:01.219Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Age of arrival in the UK",
    "type": "cantabular_flexible_table",
    "unit_of_measure": "Person",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Lower tier local authorities provide a range of local services. In England there are 309 lower tier local authorities. These are made up of non-metropolitan districts (181), unitary authorities (59), metropolitan districts (36) and London boroughs (33, including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities. Of these local authority types, only non-metropolitan districts are not additionally classified as upper tier local authorities.",
          "id": "ltla",
          "label": "Lower Tier Local Authorities",
          "name": "ltla"
        },
        {
          "description": "The date a person last arrived to live in the UK and their age. Arrival dates do not include returning from short trips away from the UK. Age of arrival only applies to usual residents not born in the UK. It does not include usual residents born in the UK who have emigrated and since returned. These are recorded in the category “born in the UK”.",
          "id": "age_arrival_uk_18a",
          "label": "Age of arrival in the UK (18 categories)",
          "name": "age_arrival_uk_18a"
        }
      ],
      "edition": "2021",
      "id": "TS018",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their age of arrival in the UK. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-02-16T00:00:00.000Z",
        "state": "published",
        "title": "Age of arrival in the UK",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS018"
            }
          },
          "isBasedOn": {
            "@id": "atc-ts-demmig-ur-ct-oa",
            "@type": "cantabular_flexible_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:32:32.372592Z",
        "sha256": "4397568b5d521aa7e2dc72aef5ff973d00754be330def8a77cb11aa0479e1e9e",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS018/editions"
  }
}
---

# Age of arrival in the UK

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by their age of arrival in the UK. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS018`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS018)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
