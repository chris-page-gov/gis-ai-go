---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/projections-older-people-in-single-households",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, household projections for older people",
  "description": "Projected indicators included are derived from the published 2018-based household projections for England and 2018-based household projections for Scotland for the years 2018 up to 2043. The indicators are the percentage of one-person households, in which the householder is aged 65 years and over and the percentage of one-person households, in which the householder is aged 85 years and over. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data availability: England, Wales, Scotland and Northern Ireland independently publish subnational household projections. Each country publishes a different set of age breakdowns and only England and Scotland provide the breakdowns required to calculate the indicators included above.",
  "nativeIdentifier": "projections-older-people-in-single-households",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:30:52.722209Z",
      "responseSha256": "0f542ea43df42d8c4b865bf4f5bcf52a45fc9c3e30b6dc919836fcae6c42b24e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/21",
      "normalisedRecordSha256": "fe08e271ff85b758c6e3b54996ad4f35f742a447e22fe10a6f80a3b1b24c8359",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2018",
    "end": "2043",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Biennial",
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
    "metadataModified": "2020-11-11T16:34:11.057Z",
    "releaseVersion": "2"
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
        "id": "age-groups",
        "label": "Age group",
        "name": "agegroups"
      }
    ],
    "edition": "time-series",
    "id": "projections-older-people-in-single-households",
    "metadata": {
      "description": "Projected indicators included are derived from the published 2018-based household projections for England and 2018-based household projections for Scotland for the years 2018 up to 2043. The indicators are the percentage of one-person households, in which the householder is aged 65 years and over and the percentage of one-person households, in which the householder is aged 85 years and over. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data availability: England, Wales, Scotland and Northern Ireland independently publish subnational household projections. Each country publishes a different set of age breakdowns and only England and Scotland provide the breakdowns required to calculate the indicators included above.",
      "last_updated": "2020-11-11T16:34:11.057Z",
      "next_release": "To be announced",
      "release_date": "2020-11-11T00:00:00.000Z",
      "release_frequency": "Biennial",
      "state": "published",
      "title": "Local authority ageing statistics, household projections for older people"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "projections-older-people-in-single-households",
        "version": 2
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:52.722209Z",
      "sha256": "0f542ea43df42d8c4b865bf4f5bcf52a45fc9c3e30b6dc919836fcae6c42b24e",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2043",
        "minimumNative": "2018",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2018",
          "option": "2018"
        },
        {
          "dimension": "time",
          "label": "2019",
          "option": "2019"
        },
        {
          "dimension": "time",
          "label": "2020",
          "option": "2020"
        },
        {
          "dimension": "time",
          "label": "2021",
          "option": "2021"
        },
        {
          "dimension": "time",
          "label": "2022",
          "option": "2022"
        },
        {
          "dimension": "time",
          "label": "2023",
          "option": "2023"
        },
        {
          "dimension": "time",
          "label": "2024",
          "option": "2024"
        },
        {
          "dimension": "time",
          "label": "2025",
          "option": "2025"
        },
        {
          "dimension": "time",
          "label": "2026",
          "option": "2026"
        },
        {
          "dimension": "time",
          "label": "2027",
          "option": "2027"
        },
        {
          "dimension": "time",
          "label": "2028",
          "option": "2028"
        },
        {
          "dimension": "time",
          "label": "2029",
          "option": "2029"
        },
        {
          "dimension": "time",
          "label": "2030",
          "option": "2030"
        },
        {
          "dimension": "time",
          "label": "2031",
          "option": "2031"
        },
        {
          "dimension": "time",
          "label": "2032",
          "option": "2032"
        },
        {
          "dimension": "time",
          "label": "2033",
          "option": "2033"
        },
        {
          "dimension": "time",
          "label": "2034",
          "option": "2034"
        },
        {
          "dimension": "time",
          "label": "2035",
          "option": "2035"
        },
        {
          "dimension": "time",
          "label": "2036",
          "option": "2036"
        },
        {
          "dimension": "time",
          "label": "2037",
          "option": "2037"
        },
        {
          "dimension": "time",
          "label": "2038",
          "option": "2038"
        },
        {
          "dimension": "time",
          "label": "2039",
          "option": "2039"
        },
        {
          "dimension": "time",
          "label": "2040",
          "option": "2040"
        },
        {
          "dimension": "time",
          "label": "2041",
          "option": "2041"
        },
        {
          "dimension": "time",
          "label": "2042",
          "option": "2042"
        },
        {
          "dimension": "time",
          "label": "2043",
          "option": "2043"
        }
      ],
      "reportedTotal": 26,
      "retrievedUnique": 26,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "2",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2"
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "Biennial"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2043",
      "minimumNative": "2018",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Local authority ageing statistics, household projections for older people

Projected indicators included are derived from the published 2018-based household projections for England and 2018-based household projections for Scotland for the years 2018 up to 2043. The indicators are the percentage of one-person households, in which the householder is aged 65 years and over and the percentage of one-person households, in which the householder is aged 85 years and over. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data availability: England, Wales, Scotland and Northern Ireland independently publish subnational household projections. Each country publishes a different set of age breakdowns and only England and Scotland provide the breakdowns required to calculate the indicators included above.

Native identifier: `projections-older-people-in-single-households`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-in-single-households/editions/time-series/versions/2)

Update cadence: Biennial.
Temporal evidence: normalised-source-options (available-native-period-options); start 2018, end 2043.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
