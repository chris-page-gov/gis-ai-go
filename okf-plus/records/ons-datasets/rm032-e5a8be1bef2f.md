---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM032",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Ethnic group by sex by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by ethnic group, by sex, and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM032",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM032",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "ethnic_group_tb_20b,sex,resident_age_5c"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=300",
      "retrievedAt": "2026-10-02T01:18:03.582092Z",
      "responseSha256": "49f3fe8ddc5f16a3c2801331f3e03dcac39702fa0a6d3b856b562bcc92dec23b",
      "sourcePointer": "/items/10",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/310",
      "normalisedRecordSha256": "d926c03b80e639e664c3d526c71018d94be910e42ba8af89bc21830552814df4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:35:19.864325Z",
      "responseSha256": "77081a90cd2e46a408e94aa241907e192e14db90178e6e7106a587ba1b504430",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/310",
      "normalisedRecordSha256": "85608fa968055650194c068a96e31e542e78d8ca064e12384a5f5757e086f895",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM032"
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
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": null,
    "metadataModified": "2023-03-28T08:30:08.58Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by ethnic group, by sex, and by age. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM032",
    "keywords": [
      "ltla",
      "ethnic_group_tb_20b,sex,resident_age_5c"
    ],
    "last_updated": "2023-03-28T08:30:08.58Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions/2021/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Ethnic group by sex by age",
    "type": "cantabular_multivariate_table",
    "unit_of_measure": "Person",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
          "id": "ltla",
          "label": "Lower tier local authorities",
          "name": "ltla"
        },
        {
          "description": "The ethnic group that the person completing the census feels they belong to. This could be based on their culture, family background, identity or physical appearance. Respondents could choose one out of 19 tick-box response categories, including write-in response options.",
          "id": "ethnic_group_tb_20b",
          "label": "Ethnic group (20 categories)",
          "name": "ethnic_group_tb_20b"
        },
        {
          "description": "This is the sex recorded by the person completing the census. The options were “Female” and “Male”.",
          "id": "sex",
          "label": "Sex (2 categories)",
          "name": "sex"
        },
        {
          "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
          "id": "resident_age_5c",
          "label": "Age (C) (5 categories)",
          "name": "resident_age_5c"
        }
      ],
      "edition": "2021",
      "id": "RM032",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by ethnic group, by sex, and by age. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-03-28T00:00:00.000Z",
        "state": "published",
        "title": "Ethnic group by sex by age",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions/2021/versions/1",
              "id": "1"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM032"
            }
          },
          "isBasedOn": {
            "@id": "UR",
            "@type": "cantabular_multivariate_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:35:19.864325Z",
        "sha256": "77081a90cd2e46a408e94aa241907e192e14db90178e6e7106a587ba1b504430",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions/2021/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions/2021/versions/1"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM032/editions"
  }
}
---

# Ethnic group by sex by age

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by ethnic group, by sex, and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM032`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM032)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
