---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM075",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Method used to travel to work by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by method used to travel to work (2001 specification) and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM075",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM075",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "transport_to_workplace_12a,resident_age_6a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=200",
      "retrievedAt": "2026-10-02T01:18:03.316175Z",
      "responseSha256": "23965e57a732be944cd1c9954229e9957ca9a52c28b0632525da9642ff12011b",
      "sourcePointer": "/items/68",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/268",
      "normalisedRecordSha256": "f6429eb4934691ddd461edbc99bd8dd07202a2b9021b8b560c7a9b3646607189",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:34:44.767729Z",
      "responseSha256": "2ea6b255900f22b88404341df36a76d376cadf01cde1073646125957db045c49",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/268",
      "normalisedRecordSha256": "fd3fe50acfc29629907d5dd129a0639265dc0173e5ade91245eb51e352e07e2f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM075"
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
    "metadataModified": "2024-01-15T10:00:05.212Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by method used to travel to work (2001 specification) and by age. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM075",
    "keywords": [
      "ltla",
      "transport_to_workplace_12a,resident_age_6a"
    ],
    "last_updated": "2024-01-15T10:00:05.212Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions/2021/versions/4",
        "id": "4"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Method used to travel to work by age",
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
          "description": "A person's place of work and their method of travel to work. This is the 2001 method of producing travel to work variables. \"Work mainly from home\" applies to someone who indicated their place of work as their home address and travelled to work by driving a car or van, for example visiting clients.",
          "id": "transport_to_workplace_12a",
          "label": "Method used to travel to workplace (12 categories)",
          "name": "transport_to_workplace_12a"
        },
        {
          "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
          "id": "resident_age_6a",
          "label": "Age (6 categories)",
          "name": "resident_age_6a"
        }
      ],
      "edition": "2021",
      "id": "RM075",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by method used to travel to work (2001 specification) and by age. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Method used to travel to work by age",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions/2021/versions/4",
              "id": "4"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM075"
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
        "retrievedAt": "2026-10-02T01:34:44.767729Z",
        "sha256": "2ea6b255900f22b88404341df36a76d376cadf01cde1073646125957db045c49",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions/2021/versions/4/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "4",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions/2021/versions/4"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM075/editions"
  }
}
---

# Method used to travel to work by age

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by method used to travel to work (2001 specification) and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM075`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM075)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
