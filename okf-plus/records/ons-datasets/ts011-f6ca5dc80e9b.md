---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/TS011",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Households by deprivation dimensions",
  "description": "This dataset provides Census 2021 estimates that classify households in England and Wales by four dimensions of deprivation: Employment, education, health and disability, and household overcrowding. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS011",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS011",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "hh_deprivation"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/16",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/116",
      "normalisedRecordSha256": "982ff94d9595267992371c40e52647b38189f2e20514c3a33d6bfa3590fd50c1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions/2021/versions/6/metadata",
      "retrievedAt": "2026-10-02T01:32:37.420401Z",
      "responseSha256": "9889d8e60eb0a4ec41eeb05420e2bfa62f2bac63c9b3e5e51f8fc197ac68b2dd",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/116",
      "normalisedRecordSha256": "627e998ef52bf416e639115ad7131b6f33e0529553fcf2ffbbbd5740400637ba",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS011"
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
    "metadataModified": "2024-01-15T10:00:04.572Z",
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
    "description": "This dataset provides Census 2021 estimates that classify households in England and Wales by four dimensions of deprivation: Employment, education, health and disability, and household overcrowding. The estimates are as at Census Day, 21 March 2021.",
    "id": "TS011",
    "keywords": [
      "ltla",
      "hh_deprivation"
    ],
    "last_updated": "2024-01-15T10:00:04.572Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions/2021/versions/6",
        "id": "6"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Households by deprivation dimensions",
    "type": "cantabular_flexible_table",
    "unit_of_measure": "Household",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
          "id": "ltla",
          "label": "Lower tier local authorities",
          "name": "ltla"
        },
        {
          "description": "The dimensions of deprivation used to classify households are indicators based on four selected household characteristics. Education A household is classified as deprived in the education dimension if no one has at least level 2 education and no one aged 16 to 18 years is a full-time student. Employment A household is classified as deprived in the employment dimension if any member, not a full-time student, is either unemployed or economically inactive due to long-term sickness or disability. Health A household is classified as deprived in the health dimension if any person in the household has general health that is bad or very bad or is identified as disabled. People who have assessed their day-to-day activities as limited by long-term physical or mental health conditions or illnesses are considered disabled. This definition of a disabled person meets the harmonised standard for measuring disability and is in line with the Equality Act (2010). Housing A household is classified as deprived in the housing dimension if the household's accommodation is either overcrowded, in a shared dwelling, or has no central heating.",
          "id": "hh_deprivation",
          "label": "Household deprivation (6 categories)",
          "name": "hh_deprivation"
        }
      ],
      "edition": "2021",
      "id": "TS011",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify households in England and Wales by four dimensions of deprivation: Employment, education, health and disability, and household overcrowding. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Households by deprivation dimensions",
        "unit_of_measure": "Household"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions/2021/versions/6",
              "id": "6"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/TS011"
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
        "retrievedAt": "2026-10-02T01:32:37.420401Z",
        "sha256": "9889d8e60eb0a4ec41eeb05420e2bfa62f2bac63c9b3e5e51f8fc197ac68b2dd",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions/2021/versions/6/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "6",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions/2021/versions/6"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS011/editions"
  }
}
---

# Households by deprivation dimensions

This dataset provides Census 2021 estimates that classify households in England and Wales by four dimensions of deprivation: Employment, education, health and disability, and household overcrowding. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS011`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS011)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
