---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/sexual-orientation-by-age-and-sex",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Sexual orientation by age and sex",
  "description": "Sexual orientation in the UK by sex and age, 2014 to 2020. Source: Annual Population Survey, ONS",
  "nativeIdentifier": "sexual-orientation-by-age-and-sex",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:30:40.806813Z",
      "responseSha256": "9e7c8178fc3731c0de7b46ada3153fcce44fe96578f755ef934d389dd0309408",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/14",
      "normalisedRecordSha256": "5fae8693e650c7256fb3d9a033836d82adf67fb0791f6d95d9355bbf5d3f924c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2014",
    "end": "2022",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
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
    "nextRelease": "To be announced",
    "metadataModified": "2023-10-18T09:27:20.485Z",
    "releaseVersion": "3"
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
        "id": "calendar-years",
        "label": "Time",
        "name": "time"
      },
      {
        "id": "uk-only",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "age-groups",
        "label": "Age groups",
        "name": "agegroups"
      },
      {
        "id": "sex",
        "label": "Sex",
        "name": "sex"
      },
      {
        "id": "sexual-orientation",
        "label": "Sexual orientation",
        "name": "sexualorientation"
      },
      {
        "description": "Percentages are calculated out of all men (or women) of a particular age group within a particular year. For example, 5.5% of women aged 16 to 24 in 2019 identified as bisexual. The percentages of each sexual orientation response category for men (or women) within an age group within a particular year will add up to 100% (subject to rounding)",
        "id": "unit-of-measure",
        "label": "Unit of measure",
        "name": "unitofmeasure"
      }
    ],
    "edition": "time-series",
    "id": "sexual-orientation-by-age-and-sex",
    "metadata": {
      "description": "Sexual orientation in the UK by sex and age, 2014 to 2020. Source: Annual Population Survey, ONS",
      "last_updated": "2023-10-18T09:27:20.485Z",
      "next_release": "To be announced",
      "release_date": "2023-10-18T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Sexual orientation by age and sex",
      "type": "filterable",
      "unit_of_measure": "Number of people (thousands) and percentage"
    },
    "metadataContract": {
      "catalogueType": "filterable",
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "sexual-orientation-by-age-and-sex",
        "version": 3
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:40.806813Z",
      "sha256": "9e7c8178fc3731c0de7b46ada3153fcce44fe96578f755ef934d389dd0309408",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2022",
        "minimumNative": "2014",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2022",
          "option": "2022"
        },
        {
          "dimension": "time",
          "label": "2021",
          "option": "2021"
        },
        {
          "dimension": "time",
          "label": "2020",
          "option": "2020"
        },
        {
          "dimension": "time",
          "label": "2019",
          "option": "2019"
        },
        {
          "dimension": "time",
          "label": "2018",
          "option": "2018"
        },
        {
          "dimension": "time",
          "label": "2017",
          "option": "2017"
        },
        {
          "dimension": "time",
          "label": "2016",
          "option": "2016"
        },
        {
          "dimension": "time",
          "label": "2015",
          "option": "2015"
        },
        {
          "dimension": "time",
          "label": "2014",
          "option": "2014"
        }
      ],
      "reportedTotal": 9,
      "retrievedUnique": 9,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "3",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2014",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Sexual orientation by age and sex

Sexual orientation in the UK by sex and age, 2014 to 2020. Source: Annual Population Survey, ONS

Native identifier: `sexual-orientation-by-age-and-sex`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-age-and-sex/editions/time-series/versions/3)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2014, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
