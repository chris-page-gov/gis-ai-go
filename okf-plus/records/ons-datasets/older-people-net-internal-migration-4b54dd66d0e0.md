---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/older-people-net-internal-migration",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, net internal migration people aged 65 and over and 85 and over",
  "description": "Figures presented show the movement of older people between local authorities and regions. Both indicators included in this dataset have been derived from the published 2019 internal migration dataset for England and Wales. The numbers presented are the net number of people aged 65 years and over and 85 years and over entering/ leaving the local authority or region in the 12-month period stated. This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool is interactive, and users are able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
  "nativeIdentifier": "older-people-net-internal-migration",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ageing",
    "population"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/25",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/25",
      "normalisedRecordSha256": "1420929af62c2a34722b25415ab3b78ce051cc55f7f19ba5f3be89589f700e1a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:30:59.466099Z",
      "responseSha256": "ce403cc6ec9fef250b1161ba3a7fe3f4f6c526520214ef6de2af0a5f49087f4a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/25",
      "normalisedRecordSha256": "4647249a3732aeb156a0d196aa278fa728cad4a43de36685d307f8677ddb9d6e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2019",
    "end": "2019",
    "sourceField": "timeMetadata.temporal.options",
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
    "nextRelease": "1 June 2021",
    "metadataModified": "2020-11-02T10:44:52.936Z",
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
    "description": "Figures presented show the movement of older people between local authorities and regions. Both indicators included in this dataset have been derived from the published 2019 internal migration dataset for England and Wales. The numbers presented are the net number of people aged 65 years and over and 85 years and over entering/ leaving the local authority or region in the 12-month period stated.\n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool is interactive, and users are able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
    "id": "older-people-net-internal-migration",
    "keywords": [
      "ageing",
      "population"
    ],
    "last_updated": "2020-11-02T10:44:52.936Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing"
      }
    },
    "next_release": "1 June 2021",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/migrationwithintheuk/methodologies/internalmigrationestimatesqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/migrationwithintheuk/datasets/internalmigrationlaandregionmovesandbysexandsingleyearofagetotals",
        "title": "Internal migration: by local authority and region, age and sex"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Local authority ageing statistics, net internal migration people aged 65 and over and 85 and over",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "description": "Data are available at a local authority and regional level for England and Wales.",
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "description": "Data are available for All Persons, Males and Females.",
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "description": "Data are available for those aged 65 years and over and 85 years and over.",
          "id": "age-groups",
          "label": "Age groups",
          "name": "agegroups"
        }
      ],
      "edition": "time-series",
      "id": "older-people-net-internal-migration",
      "metadata": {
        "description": "Figures presented show the movement of older people between local authorities and regions. Both indicators included in this dataset have been derived from the published 2019 internal migration dataset for England and Wales. The numbers presented are the net number of people aged 65 years and over and 85 years and over entering/ leaving the local authority or region in the 12-month period stated. This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool is interactive, and users are able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
        "last_updated": "2020-11-02T10:44:52.936Z",
        "next_release": "1 June 2021",
        "release_date": "2020-06-30T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Local authority ageing statistics, net internal migration people aged 65 and over and 85 and over"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "older-people-net-internal-migration",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:59.466099Z",
        "sha256": "ce403cc6ec9fef250b1161ba3a7fe3f4f6c526520214ef6de2af0a5f49087f4a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2019",
          "minimumNative": "2019",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2019",
            "option": "2019"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2019",
      "minimumNative": "2019",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Local authority ageing statistics, net internal migration people aged 65 and over and 85 and over

Figures presented show the movement of older people between local authorities and regions. Both indicators included in this dataset have been derived from the published 2019 internal migration dataset for England and Wales. The numbers presented are the net number of people aged 65 years and over and 85 years and over entering/ leaving the local authority or region in the 12-month period stated. This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool is interactive, and users are able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.

Native identifier: `older-people-net-internal-migration`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/older-people-net-internal-migration)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2019, end 2019.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
