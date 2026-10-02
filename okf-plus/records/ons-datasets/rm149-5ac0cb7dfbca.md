---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM149",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Ability to speak Welsh by industry",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh by industry. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM149",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM149",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "welsh_skills_speak,industry_current_9a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/94",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/194",
      "normalisedRecordSha256": "0cdf152f530de7e6c5792700ee8f02005ade71243be2d36d558a50bea036e76a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:33:42.804750Z",
      "responseSha256": "a2b47516f7f9c953a49afd6eb2439f6f87c7663c479e33c4fbb181f6904be90e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/194",
      "normalisedRecordSha256": "309f0793b48eaf24e05193e9c0db7fe0d7e8737da2a57e477446538d36875096",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM149"
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
    "metadataModified": "2024-01-15T10:00:04.906Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh by industry. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM149",
    "keywords": [
      "ltla",
      "welsh_skills_speak,industry_current_9a"
    ],
    "last_updated": "2024-01-15T10:00:04.906Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Ability to speak Welsh by industry",
    "type": "cantabular_multivariate_table",
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
          "description": "This classifies a person as being able to \"Speak Welsh\". They may have also ticked one or more of the following: * understand spoken Welsh * read Welsh * write Welsh In results that classify people by Welsh language skills, a person may appear in more than one category depending on which combination of skills they have.",
          "id": "welsh_skills_speak",
          "label": "Welsh speaking ability (3 categories)",
          "name": "welsh_skills_speak"
        },
        {
          "description": "Classifies people aged 16 years and over who were in employment between 15 March and 21 March 2021 by the Standard Industrial Classification (SIC) code that represents their current industry or business. The SIC code is assigned based on the information provided about a firm or organisation’s main activity.",
          "id": "industry_current_9a",
          "label": "Industry (current) (9 categories)",
          "name": "industry_current_9a"
        }
      ],
      "edition": "2021",
      "id": "RM149",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh by industry. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Ability to speak Welsh by industry",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM149"
            }
          },
          "isBasedOn": {
            "@id": "UR",
            "@type": "cantabular_multivariate_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:33:42.804750Z",
        "sha256": "a2b47516f7f9c953a49afd6eb2439f6f87c7663c479e33c4fbb181f6904be90e",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM149/editions"
  }
}
---

# Ability to speak Welsh by industry

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh by industry. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM149`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM149)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
