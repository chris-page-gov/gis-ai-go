---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/wellbeing-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Personal well-being estimates by local authority",
  "description": "Estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety at the UK, country, regional, county, local and unitary authority level.",
  "nativeIdentifier": "wellbeing-local-authority",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "well-being"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/1",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/1",
      "normalisedRecordSha256": "6fe40e7bc25c33aac6de7d5aa29e67d2adec570348fae363e53a5e597180c019",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions/time-series/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:30:19.796888Z",
      "responseSha256": "8d1f31c60e06755fb4663d101d0a1d27fb489b237fa19a532a955328cdc92a9a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/1",
      "normalisedRecordSha256": "6f0956da05c4a3f8bb15bc6701480d25a0220a4d70c5c476f828ee70e58ce4d5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority"
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
      "status": "source-stated",
      "label": "Annual",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-A",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "TBC",
    "metadataModified": "2023-12-13T09:40:21.928Z",
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
    "description": "Estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety at the UK, country, regional, county, local and unitary authority level.",
    "id": "wellbeing-local-authority",
    "keywords": [
      "well-being"
    ],
    "last_updated": "2023-12-13T09:40:21.928Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions/time-series/versions/4",
        "id": "4"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/wellbeing"
      }
    },
    "national_statistic": true,
    "next_release": "TBC",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/methodologies/personalwellbeingintheukqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/bulletins/measuringnationalwellbeing/april2022tomarch2023",
        "title": "Personal well-being in the UK: April 2022 to March 2023"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Personal well-being estimates by local authority",
    "unit_of_measure": "Percentage",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "yyyy-yy",
          "label": "Time",
          "name": "time"
        },
        {
          "description": "Geographic areas are updated regularly where new unitary authorities may be created and replace existing local authorities. For more information see the \"Notes\" tab within the main dataset.",
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "description": "The well-being thresholds in this dataset are different to the standard well-being thresholds that are published as part of this release. This is because the data for the anxiety measure needs to be interpreted differently to the other three well-being measures. For example, high happiness scores relate to a positive well-being, while high anxiety scores relate to a poor well-being. The well-being thresholds used in this dataset map onto the thresholds used in the main publication in the following way: - Poor = Low levels of life satisfaction, worthwhile, happiness and high levels of anxiety. - Fair = Medium levels of life satisfaction, worthwhile, happiness and anxiety. - Good = High levels of life satisfaction, worthwhile, happiness and low levels of anxiety. - Very good = Very high levels of life satisfaction, worthwhile, happiness and very low levels of anxiety.",
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
      "id": "wellbeing-local-authority",
      "metadata": {
        "description": "Estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety at the UK, country, regional, county, local and unitary authority level.",
        "last_updated": "2023-12-13T09:40:21.928Z",
        "next_release": "TBC",
        "release_date": "2023-11-28T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Personal well-being estimates by local authority",
        "unit_of_measure": "Percentage"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "wellbeing-local-authority",
          "version": 4
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:19.796888Z",
        "sha256": "8d1f31c60e06755fb4663d101d0a1d27fb489b237fa19a532a955328cdc92a9a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions/time-series/versions/4/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "continuityEstablished": false,
          "maximumNative": null,
          "minimumNative": null,
          "status": "unknown-unrecognised-or-mixed-period-codes"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2022-23",
            "option": "2022-23"
          },
          {
            "dimension": "time",
            "label": "2021-22",
            "option": "2021-22"
          },
          {
            "dimension": "time",
            "label": "2020-21",
            "option": "2020-21"
          },
          {
            "dimension": "time",
            "label": "2019-20",
            "option": "2019-20"
          },
          {
            "dimension": "time",
            "label": "2018-19",
            "option": "2018-19"
          },
          {
            "dimension": "time",
            "label": "2017-18",
            "option": "2017-18"
          },
          {
            "dimension": "time",
            "label": "2016-17",
            "option": "2016-17"
          },
          {
            "dimension": "time",
            "label": "2015-16",
            "option": "2015-16"
          },
          {
            "dimension": "time",
            "label": "2014-15",
            "option": "2014-15"
          },
          {
            "dimension": "time",
            "label": "2013-14",
            "option": "2013-14"
          },
          {
            "dimension": "time",
            "label": "2012-13",
            "option": "2012-13"
          },
          {
            "dimension": "time",
            "label": "2011-12",
            "option": "2011-12"
          }
        ],
        "reportedTotal": 12,
        "retrievedUnique": 12,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "4",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions/time-series/versions/4"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority/editions"
  }
}
---

# Personal well-being estimates by local authority

Estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety at the UK, country, regional, county, local and unitary authority level.

Native identifier: `wellbeing-local-authority`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/wellbeing-local-authority)

Update cadence: Annual.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
