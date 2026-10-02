---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM090",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "NS-SEC by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by NS-SEC and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM090",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM090",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "ns_sec_10a,resident_age_6a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=200",
      "retrievedAt": "2026-10-02T01:18:03.316175Z",
      "responseSha256": "23965e57a732be944cd1c9954229e9957ca9a52c28b0632525da9642ff12011b",
      "sourcePointer": "/items/53",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/253",
      "normalisedRecordSha256": "5054b7ecb35158e7766bb07e4dd43adc71dcef397c5d10681c97470801cca21b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:34:32.239981Z",
      "responseSha256": "07ed2d282476068d7a275185159cd862591c1d030d2be5f74c3d2642494fe520",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/253",
      "normalisedRecordSha256": "b0a68d2ee9ee5da8c02cc56ef219490dc068523951084f10a06c9fbbd799c476",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM090"
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
    "metadataModified": "2024-01-15T10:00:05.237Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by NS-SEC and by age. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM090",
    "keywords": [
      "ltla",
      "ns_sec_10a,resident_age_6a"
    ],
    "last_updated": "2024-01-15T10:00:05.237Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "NS-SEC by age",
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
          "description": "The National Statistics Socio-economic Classification (NS-SEC) indicates a person's socio-economic position based on their occupation and other job characteristics. It is an Office for National Statistics standard classification. NS-SEC categories are assigned based on a person's occupation, whether employed, self-employed, or supervising other employees. Full-time students are recorded in the \"full-time students\" category regardless of whether they are economically active.",
          "id": "ns_sec_10a",
          "label": "National Statistics Socio-economic Classification (NS-SeC) (10 categories)",
          "name": "ns_sec_10a"
        },
        {
          "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
          "id": "resident_age_6a",
          "label": "Age (6 categories)",
          "name": "resident_age_6a"
        }
      ],
      "edition": "2021",
      "id": "RM090",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by NS-SEC and by age. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "NS-SEC by age",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM090"
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
        "retrievedAt": "2026-10-02T01:34:32.239981Z",
        "sha256": "07ed2d282476068d7a275185159cd862591c1d030d2be5f74c3d2642494fe520",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM090/editions"
  }
}
---

# NS-SEC by age

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by NS-SEC and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM090`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM090)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
