---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/wellbeing-quarterly",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Quarterly personal well-being estimates",
  "description": "Seasonally and non seasonally-adjusted quarterly estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety in the UK.",
  "nativeIdentifier": "wellbeing-quarterly",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9/metadata",
      "retrievedAt": "2026-10-02T01:30:18.068135Z",
      "responseSha256": "0c2d7c23a8fbd45c8df2565c446ab05490a4893f80d635a0dfc1c197bf82f159",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/0",
      "normalisedRecordSha256": "daf70a49d2ce1d2e9b189719af686e1c94c174d628e3896e94f52386067bfe6f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9"
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
      "label": "Quarterly",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-Q",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "TBC",
    "metadataModified": "2023-12-13T09:40:24.204Z",
    "releaseVersion": "9"
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
        "id": "yyyy-qq",
        "label": "Time",
        "name": "time"
      },
      {
        "id": "uk-only",
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
      },
      {
        "id": "seasonal-adjustment",
        "label": "Seasonal adjustment",
        "name": "seasonaladjustment"
      }
    ],
    "edition": "time-series",
    "id": "wellbeing-quarterly",
    "metadata": {
      "description": "Seasonally and non seasonally-adjusted quarterly estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety in the UK.",
      "last_updated": "2023-12-13T09:40:24.204Z",
      "next_release": "TBC",
      "release_date": "2023-11-28T00:00:00.000Z",
      "release_frequency": "Quarterly",
      "state": "published",
      "title": "Quarterly personal well-being estimates",
      "unit_of_measure": "Percentage"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "wellbeing-quarterly",
        "version": 9
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:18.068135Z",
      "sha256": "0c2d7c23a8fbd45c8df2565c446ab05490a4893f80d635a0dfc1c197bf82f159",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9/metadata"
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
          "label": "2023 Q2",
          "option": "2023-q2"
        },
        {
          "dimension": "time",
          "label": "2023 Q1",
          "option": "2023-q1"
        },
        {
          "dimension": "time",
          "label": "2022 Q4",
          "option": "2022-q4"
        },
        {
          "dimension": "time",
          "label": "2022 Q3",
          "option": "2022-q3"
        },
        {
          "dimension": "time",
          "label": "2022 Q2",
          "option": "2022-q2"
        },
        {
          "dimension": "time",
          "label": "2022 Q1",
          "option": "2022-q1"
        },
        {
          "dimension": "time",
          "label": "2021 Q4",
          "option": "2021-q4"
        },
        {
          "dimension": "time",
          "label": "2021 Q3",
          "option": "2021-q3"
        },
        {
          "dimension": "time",
          "label": "2021 Q2",
          "option": "2021-q2"
        },
        {
          "dimension": "time",
          "label": "2021 Q1",
          "option": "2021-q1"
        },
        {
          "dimension": "time",
          "label": "2020 Q4",
          "option": "2020-q4"
        },
        {
          "dimension": "time",
          "label": "2020 Q3",
          "option": "2020-q3"
        },
        {
          "dimension": "time",
          "label": "2020 Q2",
          "option": "2020-q2"
        },
        {
          "dimension": "time",
          "label": "2020 Q1",
          "option": "2020-q1"
        },
        {
          "dimension": "time",
          "label": "2019 Q4",
          "option": "2019-q4"
        },
        {
          "dimension": "time",
          "label": "2019 Q3",
          "option": "2019-q3"
        },
        {
          "dimension": "time",
          "label": "2019 Q2",
          "option": "2019-q2"
        },
        {
          "dimension": "time",
          "label": "2019 Q1",
          "option": "2019-q1"
        },
        {
          "dimension": "time",
          "label": "2018 Q4",
          "option": "2018-q4"
        },
        {
          "dimension": "time",
          "label": "2018 Q3",
          "option": "2018-q3"
        },
        {
          "dimension": "time",
          "label": "2018 Q2",
          "option": "2018-q2"
        },
        {
          "dimension": "time",
          "label": "2018 Q1",
          "option": "2018-q1"
        },
        {
          "dimension": "time",
          "label": "2017 Q4",
          "option": "2017-q4"
        },
        {
          "dimension": "time",
          "label": "2017 Q3",
          "option": "2017-q3"
        },
        {
          "dimension": "time",
          "label": "2017 Q2",
          "option": "2017-q2"
        },
        {
          "dimension": "time",
          "label": "2017 Q1",
          "option": "2017-q1"
        },
        {
          "dimension": "time",
          "label": "2016 Q4",
          "option": "2016-q4"
        },
        {
          "dimension": "time",
          "label": "2016 Q3",
          "option": "2016-q3"
        },
        {
          "dimension": "time",
          "label": "2016 Q2",
          "option": "2016-q2"
        },
        {
          "dimension": "time",
          "label": "2016 Q1",
          "option": "2016-q1"
        },
        {
          "dimension": "time",
          "label": "2015 Q4",
          "option": "2015-q4"
        },
        {
          "dimension": "time",
          "label": "2015 Q3",
          "option": "2015-q3"
        },
        {
          "dimension": "time",
          "label": "2015 Q2",
          "option": "2015-q2"
        },
        {
          "dimension": "time",
          "label": "2015 Q1",
          "option": "2015-q1"
        },
        {
          "dimension": "time",
          "label": "2014 Q4",
          "option": "2014-q4"
        },
        {
          "dimension": "time",
          "label": "2014 Q3",
          "option": "2014-q3"
        },
        {
          "dimension": "time",
          "label": "2014 Q2",
          "option": "2014-q2"
        },
        {
          "dimension": "time",
          "label": "2014 Q1",
          "option": "2014-q1"
        },
        {
          "dimension": "time",
          "label": "2013 Q4",
          "option": "2013-q4"
        },
        {
          "dimension": "time",
          "label": "2013 Q3",
          "option": "2013-q3"
        },
        {
          "dimension": "time",
          "label": "2013 Q2",
          "option": "2013-q2"
        },
        {
          "dimension": "time",
          "label": "2013 Q1",
          "option": "2013-q1"
        },
        {
          "dimension": "time",
          "label": "2012 Q4",
          "option": "2012-q4"
        },
        {
          "dimension": "time",
          "label": "2012 Q3",
          "option": "2012-q3"
        },
        {
          "dimension": "time",
          "label": "2012 Q2",
          "option": "2012-q2"
        },
        {
          "dimension": "time",
          "label": "2012 Q1",
          "option": "2012-q1"
        },
        {
          "dimension": "time",
          "label": "2011 Q4",
          "option": "2011-q4"
        },
        {
          "dimension": "time",
          "label": "2011 Q3",
          "option": "2011-q3"
        },
        {
          "dimension": "time",
          "label": "2011 Q2",
          "option": "2011-q2"
        }
      ],
      "reportedTotal": 49,
      "retrievedUnique": 49,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "9",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-Q"
  }
}
---

# Quarterly personal well-being estimates

Seasonally and non seasonally-adjusted quarterly estimates of life satisfaction, feeling that the things done in life are worthwhile, happiness and anxiety in the UK.

Native identifier: `wellbeing-quarterly`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/wellbeing-quarterly/editions/time-series/versions/9)

Update cadence: Quarterly.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
