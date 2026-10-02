---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/childrens-wellbeing",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Children's Well-being Measures",
  "description": "How children aged 0 to 15 years in the UK are coping in a range of areas that matter to their quality of life, reflecting the circumstances of their lives and their own perspectives. This is a subset of the children's well-being indicators. For the full dataset, please see 'Children's well-being and social relationships, UK: 2018' in the 'Related datasets' section.",
  "nativeIdentifier": "childrens-wellbeing",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "children's well-being",
    "well-being"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/39",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/39",
      "normalisedRecordSha256": "b0c9d8a41520750667bbb073a00959122b5ab676dc3bf829b2bbe7dae8269d28",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:23.029169Z",
      "responseSha256": "c7ffddb65d9e603fb7e515ddcf6c2fda5547cada3573a0b0fe0f80949b31b19c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/39",
      "normalisedRecordSha256": "589ee0d877389d4ec083617a34ed1c52ff815cf114c3ba174aa5f0e2c7beeff9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2012",
    "end": "2017",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "To be announced",
      "iri": null,
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "To be announced",
    "metadataModified": "2020-11-02T16:51:55.297Z",
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
    "description": "How children aged 0 to 15 years in the UK are coping in a range of areas that matter to their quality of life, reflecting the circumstances of their lives and their own perspectives.\n\nThis is a subset of the children's well-being indicators. For the full dataset, please see 'Children's well-being and social relationships, UK: 2018' in the 'Related datasets' section.",
    "id": "childrens-wellbeing",
    "keywords": [
      "children's well-being",
      "well-being"
    ],
    "last_updated": "2020-11-02T16:51:55.297Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/wellbeing"
      }
    },
    "methodologies": [
      {
        "href": "https://www.childrenssociety.org.uk",
        "title": "Source: The Children's Society"
      },
      {
        "description": "Please use this link for more information on Government Statistical Service (GSS) harmonised well-being questions.",
        "href": "https://gss.civilservice.gov.uk/policy-store/personal-well-being/",
        "title": "Personal well-being - GSS"
      }
    ],
    "next_release": "To be announced",
    "qmi": {},
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/articles/measuringnationalwellbeing/march2018",
        "title": "Children’s well-being and social relationships, UK: 2018"
      },
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/articles/measuringnationalwellbeing/internationalcomparisons2019",
        "title": "Measuring national well-being in the UK: international comparisons, 2019"
      }
    ],
    "release_frequency": "To be announced",
    "state": "published",
    "title": "Children's Well-being Measures",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "countries",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "id": "wellbeing-estimate",
          "label": "Estimate",
          "name": "estimate"
        },
        {
          "id": "measure-of-wellbeing",
          "label": "All measures of well-being",
          "name": "measureofwellbeing"
        }
      ],
      "edition": "time-series",
      "id": "childrens-wellbeing",
      "metadata": {
        "description": "How children aged 0 to 15 years in the UK are coping in a range of areas that matter to their quality of life, reflecting the circumstances of their lives and their own perspectives. This is a subset of the children's well-being indicators. For the full dataset, please see 'Children's well-being and social relationships, UK: 2018' in the 'Related datasets' section.",
        "last_updated": "2020-11-02T16:51:55.297Z",
        "next_release": "To be announced",
        "release_date": "2019-10-25T00:00:00.000Z",
        "release_frequency": "To be announced",
        "state": "published",
        "title": "Children's Well-being Measures"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "childrens-wellbeing",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:23.029169Z",
        "sha256": "c7ffddb65d9e603fb7e515ddcf6c2fda5547cada3573a0b0fe0f80949b31b19c",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2017",
          "minimumNative": "2012",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2012",
            "option": "2012"
          },
          {
            "dimension": "time",
            "label": "2013",
            "option": "2013"
          },
          {
            "dimension": "time",
            "label": "2014",
            "option": "2014"
          },
          {
            "dimension": "time",
            "label": "2015",
            "option": "2015"
          },
          {
            "dimension": "time",
            "label": "2016",
            "option": "2016"
          },
          {
            "dimension": "time",
            "label": "2017",
            "option": "2017"
          }
        ],
        "reportedTotal": 6,
        "retrievedUnique": 6,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "To be announced"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2017",
      "minimumNative": "2012",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Children's Well-being Measures

How children aged 0 to 15 years in the UK are coping in a range of areas that matter to their quality of life, reflecting the circumstances of their lives and their own perspectives. This is a subset of the children's well-being indicators. For the full dataset, please see 'Children's well-being and social relationships, UK: 2018' in the 'Related datasets' section.

Native identifier: `childrens-wellbeing`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/childrens-wellbeing)

Update cadence: To be announced.
Temporal evidence: normalised-source-options (available-native-period-options); start 2012, end 2017.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
