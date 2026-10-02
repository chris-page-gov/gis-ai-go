---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM152",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Ability to speak Welsh by occupation",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh and by occupation. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM152",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM152",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "welsh_skills_speak,occupation_current_10a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/91",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/191",
      "normalisedRecordSha256": "913a26b3e26f98cbb31f774d43697551d55f3bf4cdb76e27cc2960a02709d3c6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:33:40.282857Z",
      "responseSha256": "da408ec6d2b321d94fd422465cb76dac6669f62276866b646fe11f0804699f39",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/191",
      "normalisedRecordSha256": "59c15b2fc61a1714595ef377d7a34121d5bfee60085e7280ab6db848407d315c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM152"
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
    "metadataModified": "2024-01-15T10:00:04.916Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh and by occupation. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM152",
    "keywords": [
      "ltla",
      "welsh_skills_speak,occupation_current_10a"
    ],
    "last_updated": "2024-01-15T10:00:04.916Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Ability to speak Welsh by occupation",
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
          "description": "Classifies what people aged 16 years and over do as their main job. Their job title or details of activities they do in their job and any supervisory or management responsibilities form this classification. This information is used to code responses to an occupation using the Standard Occupational Classification (SOC) 2020. It classifies people who were in employment between 15 March and 21 March 2021, by the SOC code that represents their current occupation. The lowest level of detail available is the four-digit SOC code which includes all codes in three, two and one digit SOC code levels.",
          "id": "occupation_current_10a",
          "label": "Occupation (current) (10 categories)",
          "name": "occupation_current_10a"
        }
      ],
      "edition": "2021",
      "id": "RM152",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh and by occupation. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Ability to speak Welsh by occupation",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM152"
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
        "retrievedAt": "2026-10-02T01:33:40.282857Z",
        "sha256": "da408ec6d2b321d94fd422465cb76dac6669f62276866b646fe11f0804699f39",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM152/editions"
  }
}
---

# Ability to speak Welsh by occupation

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in Wales by ability to speak Welsh and by occupation. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM152`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM152)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
