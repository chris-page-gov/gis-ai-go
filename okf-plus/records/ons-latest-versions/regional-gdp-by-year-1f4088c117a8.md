---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/regional-gdp-by-year",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Annual GDP for England, Wales and the English regions",
  "description": "Annual economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and the Humber, East Midlands, West Midlands, East of England, Greater London, South East, South West).",
  "nativeIdentifier": "regional-gdp-by-year",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6/metadata",
      "retrievedAt": "2026-10-02T01:30:47.672680Z",
      "responseSha256": "b465ceb1010ecf04c6f4367514f0aae3ec51b71b52072062c3d3824b8facfe15",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/18",
      "normalisedRecordSha256": "76ed4f09cd59243b3278c1bf60d53f5a8a5df1e05bceb64534177387dda0670e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2012",
    "end": "2021",
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
    "nextRelease": "TBA",
    "metadataModified": "2023-05-24T08:36:20.126Z",
    "releaseVersion": "6"
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
        "id": "nuts",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "sic-unofficial",
        "label": "Standard Industrial Classification",
        "name": "unofficialstandardindustrialclassification"
      },
      {
        "id": "type-of-prices",
        "label": "Prices",
        "name": "prices"
      },
      {
        "id": "quarterly-index-and-growth-rate",
        "label": "Measure",
        "name": "growthrate"
      }
    ],
    "edition": "time-series",
    "id": "regional-gdp-by-year",
    "metadata": {
      "description": "Annual economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and the Humber, East Midlands, West Midlands, East of England, Greater London, South East, South West).",
      "last_updated": "2023-05-24T08:36:20.126Z",
      "next_release": "TBA",
      "release_date": "2023-05-18T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Annual GDP for England, Wales and the English regions"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "regional-gdp-by-year",
        "version": 6
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:47.672680Z",
      "sha256": "b465ceb1010ecf04c6f4367514f0aae3ec51b71b52072062c3d3824b8facfe15",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2021",
        "minimumNative": "2012",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
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
        }
      ],
      "reportedTotal": 10,
      "retrievedUnique": 10,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "6",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6"
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
      "maximumNative": "2021",
      "minimumNative": "2012",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Annual GDP for England, Wales and the English regions

Annual economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and the Humber, East Midlands, West Midlands, East of England, Greater London, South East, South West).

Native identifier: `regional-gdp-by-year`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-year/editions/time-series/versions/6)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2012, end 2021.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
