---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/tax-benefits-statistics",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Effects of Taxes and Benefits on Household Income",
  "description": "Estimates of mean and median annual incomes in the UK, by quintile groups. The redistribution effects on individuals of direct and indirect taxation and benefits received in cash or kind.",
  "nativeIdentifier": "tax-benefits-statistics",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/10",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/10",
      "normalisedRecordSha256": "1b82e8db6d15db9807947161a6815445de67b3a82ac7292708fac0c52938af7f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions/time-series/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:30:34.939730Z",
      "responseSha256": "fe83a7bf78f8cc61e4674f33db78cc2f18c3124fe05168e56d6077378302e97a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/10",
      "normalisedRecordSha256": "28db5723fec556d13a9c67c5a3f5e43ca0ffbc29cedd02078b76dd7b127de528",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics"
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
    "nextRelease": "TBA",
    "metadataModified": "2022-09-16T06:15:01.401Z",
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
    "description": "Estimates of mean and median annual incomes in the UK, by quintile groups.\nThe redistribution effects on individuals of direct and indirect taxation and benefits received in cash or kind.",
    "id": "tax-benefits-statistics",
    "last_updated": "2022-09-16T06:15:01.401Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions/time-series/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/economy/governmentpublicsectorandtaxes/taxesandrevenue"
      }
    },
    "next_release": "TBA",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/methodologies/theeffectsoftaxesandbenefitsonukhouseholdincome"
    },
    "release_frequency": "Annual",
    "state": "published",
    "title": "Effects of Taxes and Benefits on Household Income",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "financial-and-calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "uk-only",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "quintile",
          "label": "Quintile",
          "name": "quintile"
        },
        {
          "id": "averages-and-percentiles",
          "label": "Statistics",
          "name": "averagesandpercentiles"
        },
        {
          "id": "income-type",
          "label": "Income type",
          "name": "income"
        },
        {
          "id": "value-deflation",
          "label": "Deflation status",
          "name": "deflation"
        }
      ],
      "edition": "time-series",
      "id": "tax-benefits-statistics",
      "metadata": {
        "description": "Estimates of mean and median annual incomes in the UK, by quintile groups. The redistribution effects on individuals of direct and indirect taxation and benefits received in cash or kind.",
        "last_updated": "2022-09-16T06:15:01.401Z",
        "next_release": "TBA",
        "release_date": "2022-09-09T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Effects of Taxes and Benefits on Household Income"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "tax-benefits-statistics",
          "version": 3
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:34.939730Z",
        "sha256": "fe83a7bf78f8cc61e4674f33db78cc2f18c3124fe05168e56d6077378302e97a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions/time-series/versions/3/metadata"
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
          },
          {
            "dimension": "time",
            "label": "2010-11",
            "option": "2010-11"
          },
          {
            "dimension": "time",
            "label": "2009-10",
            "option": "2009-10"
          },
          {
            "dimension": "time",
            "label": "2008-09",
            "option": "2008-09"
          },
          {
            "dimension": "time",
            "label": "2007-08",
            "option": "2007-08"
          },
          {
            "dimension": "time",
            "label": "2006-07",
            "option": "2006-07"
          },
          {
            "dimension": "time",
            "label": "2005-06",
            "option": "2005-06"
          },
          {
            "dimension": "time",
            "label": "2004-05",
            "option": "2004-05"
          },
          {
            "dimension": "time",
            "label": "2003-04",
            "option": "2003-04"
          },
          {
            "dimension": "time",
            "label": "2002-03",
            "option": "2002-03"
          },
          {
            "dimension": "time",
            "label": "2001-02",
            "option": "2001-02"
          },
          {
            "dimension": "time",
            "label": "2000-01",
            "option": "2000-01"
          },
          {
            "dimension": "time",
            "label": "1999-00",
            "option": "1999-00"
          },
          {
            "dimension": "time",
            "label": "1998-99",
            "option": "1998-99"
          },
          {
            "dimension": "time",
            "label": "1997-98",
            "option": "1997-98"
          },
          {
            "dimension": "time",
            "label": "1996-97",
            "option": "1996-97"
          },
          {
            "dimension": "time",
            "label": "1995-96",
            "option": "1995-96"
          },
          {
            "dimension": "time",
            "label": "1994-95",
            "option": "1994-95"
          },
          {
            "dimension": "time",
            "label": "1993",
            "option": "1993"
          },
          {
            "dimension": "time",
            "label": "1992",
            "option": "1992"
          },
          {
            "dimension": "time",
            "label": "1991",
            "option": "1991"
          },
          {
            "dimension": "time",
            "label": "1990",
            "option": "1990"
          },
          {
            "dimension": "time",
            "label": "1989",
            "option": "1989"
          },
          {
            "dimension": "time",
            "label": "1988",
            "option": "1988"
          },
          {
            "dimension": "time",
            "label": "1987",
            "option": "1987"
          },
          {
            "dimension": "time",
            "label": "1986",
            "option": "1986"
          },
          {
            "dimension": "time",
            "label": "1985",
            "option": "1985"
          },
          {
            "dimension": "time",
            "label": "1984",
            "option": "1984"
          },
          {
            "dimension": "time",
            "label": "1983",
            "option": "1983"
          },
          {
            "dimension": "time",
            "label": "1982",
            "option": "1982"
          },
          {
            "dimension": "time",
            "label": "1981",
            "option": "1981"
          },
          {
            "dimension": "time",
            "label": "1980",
            "option": "1980"
          },
          {
            "dimension": "time",
            "label": "1979",
            "option": "1979"
          },
          {
            "dimension": "time",
            "label": "1978",
            "option": "1978"
          },
          {
            "dimension": "time",
            "label": "1977",
            "option": "1977"
          }
        ],
        "reportedTotal": 44,
        "retrievedUnique": 44,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions/time-series/versions/3"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics/editions"
  }
}
---

# Effects of Taxes and Benefits on Household Income

Estimates of mean and median annual incomes in the UK, by quintile groups. The redistribution effects on individuals of direct and indirect taxation and benefits received in cash or kind.

Native identifier: `tax-benefits-statistics`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/tax-benefits-statistics)

Update cadence: Annual.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
