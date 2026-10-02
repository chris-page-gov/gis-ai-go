---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/generational-income",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Generational income: The effects of taxes and benefits",
  "description": "The effects of direct and indirect taxation and benefits received in cash or kind on household income, across the generations and by age. This data is estimated by combining multiple years of the Living Costs and Food Survey from 1978 to financial year ending March 2017 and the Household Finances Statistics, from financial year ending 2018 to financial year ending 2021 with the exception of 1979 and 1981. All financial amounts are adjusted for inflation using the Consumer Prices Index including owner occupiers’ housing costs (CPIH) excluding Council Tax, to their financial year ending March 2018. For example, the mean disposable income for those aged 35 and born in the 1970’s (£35,752) is estimated by taking the average (in real terms) of the household disposable income for these people across the combined dataset.",
  "nativeIdentifier": "generational-income",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/generational-income",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "taxes",
    "benefits,generational income"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/34",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/34",
      "normalisedRecordSha256": "0054517a7ca1cb9bb8fb3ffda8a257915158be0f2d1772c33a40e36d45f443a1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions/time-series/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:31:14.593099Z",
      "responseSha256": "f4bf57d67d08af12f1382f21def6ba13f4e78e40874ea84a9a0bbc69bcd6cdd8",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/34",
      "normalisedRecordSha256": "c1fe6c86e555a7436182529689e70500a30a6541f72276d384e29b24b08daedd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/generational-income"
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
    "nextRelease": "To be announced",
    "metadataModified": "2022-09-15T12:24:21.363Z",
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
    "description": "The effects of direct and indirect taxation and benefits received in cash or kind on household income, across the generations and by age.\n\nThis data is estimated by combining multiple years of the Living Costs and Food Survey from 1978 to financial year ending March 2017 and the Household Finances Statistics, from financial year ending 2018 to financial year ending 2021 with the exception of 1979 and 1981. All financial amounts are adjusted for inflation using the Consumer Prices Index including owner occupiers’ housing costs (CPIH) excluding Council Tax, to their financial year ending March 2018. For example, the mean disposable income for those aged 35 and born in the 1970’s (£35,752) is estimated by taking the average (in real terms) of the household disposable income for these people across the combined dataset.",
    "id": "generational-income",
    "keywords": [
      "taxes",
      "benefits,generational income"
    ],
    "last_updated": "2022-09-15T12:24:21.363Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions/time-series/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/generational-income"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth"
      }
    },
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/methodologies/theeffectsoftaxesandbenefitsonukhouseholdincome"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/theeffectsoftaxesandbenefitsonhouseholdincome/financialyearending2019",
        "title": "Generational income: The effects of taxes and benefits"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Generational income: The effects of taxes and benefits",
    "unit_of_measure": "£ (Mean average amount)",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "yyyy-yy",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "uk-only",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "single-year-of-age",
          "label": "Age",
          "name": "age"
        },
        {
          "id": "tax-benefit-type",
          "label": "Type of tax or benefit",
          "name": "typeoftaxorbenefit"
        },
        {
          "id": "decade",
          "label": "Decade",
          "name": "decade"
        }
      ],
      "edition": "time-series",
      "id": "generational-income",
      "metadata": {
        "description": "The effects of direct and indirect taxation and benefits received in cash or kind on household income, across the generations and by age. This data is estimated by combining multiple years of the Living Costs and Food Survey from 1978 to financial year ending March 2017 and the Household Finances Statistics, from financial year ending 2018 to financial year ending 2021 with the exception of 1979 and 1981. All financial amounts are adjusted for inflation using the Consumer Prices Index including owner occupiers’ housing costs (CPIH) excluding Council Tax, to their financial year ending March 2018. For example, the mean disposable income for those aged 35 and born in the 1970’s (£35,752) is estimated by taking the average (in real terms) of the household disposable income for these people across the combined dataset.",
        "last_updated": "2022-09-15T12:24:21.363Z",
        "next_release": "To be announced",
        "release_date": "2022-09-15T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Generational income: The effects of taxes and benefits",
        "unit_of_measure": "£ (Mean average amount)"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "generational-income",
          "version": 3
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:14.593099Z",
        "sha256": "f4bf57d67d08af12f1382f21def6ba13f4e78e40874ea84a9a0bbc69bcd6cdd8",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions/time-series/versions/3/metadata"
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
            "label": "1978 to 2020-21",
            "option": "1978-to-2020-21"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions/time-series/versions/3"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/generational-income/editions"
  }
}
---

# Generational income: The effects of taxes and benefits

The effects of direct and indirect taxation and benefits received in cash or kind on household income, across the generations and by age. This data is estimated by combining multiple years of the Living Costs and Food Survey from 1978 to financial year ending March 2017 and the Household Finances Statistics, from financial year ending 2018 to financial year ending 2021 with the exception of 1979 and 1981. All financial amounts are adjusted for inflation using the Consumer Prices Index including owner occupiers’ housing costs (CPIH) excluding Council Tax, to their financial year ending March 2018. For example, the mean disposable income for those aged 35 and born in the 1970’s (£35,752) is estimated by taking the average (in real terms) of the household disposable income for these people across the combined dataset.

Native identifier: `generational-income`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/generational-income)

Update cadence: Annual.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
