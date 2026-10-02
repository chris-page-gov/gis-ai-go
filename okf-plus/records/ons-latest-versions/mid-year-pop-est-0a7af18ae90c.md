---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/mid-year-pop-est",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Population Estimates for UK, England and Wales, Scotland and Northern Ireland",
  "description": "Estimates of the usual resident population for the UK as at 30 June of the reference year. Provided by administrative area, single year of age and sex.",
  "nativeIdentifier": "mid-year-pop-est",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:31:02.831817Z",
      "responseSha256": "d46ab030bee533dadef34583ba62a4e1fa85195b09a652aebcec785c1e848bc4",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/27",
      "normalisedRecordSha256": "eadaedb89e6d801bb69795c194dcf29370996031263fbb189bb11fd57af4b02b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2011",
    "end": "2023",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Annually",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-A",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "Summer 2025",
    "metadataModified": "2024-09-10T09:29:27.068Z",
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
        "id": "administrative-geography",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "sex",
        "label": "Sex",
        "name": "sex"
      },
      {
        "id": "single-year-of-age",
        "label": "Age",
        "name": "age"
      }
    ],
    "edition": "mid-2022-england-wales",
    "id": "mid-year-pop-est",
    "metadata": {
      "description": "Estimates of the usual resident population for the UK as at 30 June of the reference year. Provided by administrative area, single year of age and sex.",
      "last_updated": "2024-09-10T09:29:27.068Z",
      "next_release": "Summer 2025",
      "release_date": "2024-09-04T00:00:00.000Z",
      "release_frequency": "Annually",
      "state": "published",
      "title": "Population Estimates for UK, England and Wales, Scotland and Northern Ireland",
      "unit_of_measure": "Number of people"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "mid-2022-england-wales",
        "id": "mid-year-pop-est",
        "version": 3
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:02.831817Z",
      "sha256": "d46ab030bee533dadef34583ba62a4e1fa85195b09a652aebcec785c1e848bc4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2023",
        "minimumNative": "2011",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2023",
          "option": "2023"
        },
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
        },
        {
          "dimension": "time",
          "label": "2013",
          "option": "2013"
        },
        {
          "dimension": "time",
          "label": "2012",
          "option": "2012"
        },
        {
          "dimension": "time",
          "label": "2011",
          "option": "2011"
        }
      ],
      "reportedTotal": 13,
      "retrievedUnique": 13,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "3",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3"
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
      "maximumNative": "2023",
      "minimumNative": "2011",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Population Estimates for UK, England and Wales, Scotland and Northern Ireland

Estimates of the usual resident population for the UK as at 30 June of the reference year. Provided by administrative area, single year of age and sex.

Native identifier: `mid-year-pop-est`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/mid-year-pop-est/editions/mid-2022-england-wales/versions/3)

Update cadence: Annually.
Temporal evidence: normalised-source-options (available-native-period-options); start 2011, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
