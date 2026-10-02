---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS053",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Occupancy rating for rooms",
  "description": "This dataset provides Census 2021 estimates that classify households in England and Wales by occupancy rating based on the number of rooms in the household. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS053",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:32:03.183455Z",
      "responseSha256": "f2cf678c9fb1ac48d16dc7af7e067672e19ae5a2c3ee8f96c081daec88a18485",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/75",
      "normalisedRecordSha256": "c93abcbb64261522510582a18ff23a6f60b32f24282471a13ca79431d1948a5c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4"
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
    "metadataModified": "0001-01-01T00:00:00Z",
    "releaseVersion": "4"
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
        "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
        "id": "ltla",
        "label": "Lower tier local authorities",
        "name": "ltla"
      },
      {
        "description": "Whether a household's accommodation is overcrowded, ideally occupied or under-occupied. This is calculated by comparing the number of rooms the household requires to the number of available rooms. The number of rooms the household requires uses a formula which states that: * one-person households require three rooms comprised of two common rooms and one bedroom * two-or-more person households require a minimum of two common rooms and a bedroom for each of the following: 1. married or cohabiting couple 2. single parent 3. person aged 16 years and over 4. pair of same-sex persons aged 10 to 15 years 5. person aged 10 to 15 years paired with a person under 10 years of the same sex 6. pair of children aged 10 years, regardless of their sex 7. person aged under 16 years who cannot share a bedroom with someone in 4, 5 or 6 above An occupancy rating of: * -1 or less implies that a household’s accommodation has fewer rooms than required (overcrowded) * +1 or more implies that a household’s accommodation has more rooms than required (under-occupied) * 0 suggests that a household’s accommodation has an ideal number of rooms The number of rooms is taken from Valuation Office Agency (VOA) administrative data for the first time in 2021. The number of rooms is recorded at the address level, whilst the 2011 Census recorded the number of rooms at the household level. This means that for households that live in a shared dwelling, the available number of rooms are counted for the whole dwelling in VOA, and not each individual household. VOA’s definition of a room does not include bathrooms, toilets, halls or landings, kitchens, conservatories or utility rooms. All other rooms, for example, living rooms, studies, bedrooms, separate dining rooms and rooms that can only be used for storage are included. Please note that the 2011 Census question included kitchens, conservatories and utility rooms while excluding rooms that can only be used for storage. To adjust for the definitional difference, the number of rooms required is deducted from the actual number of rooms it has available, and then 1 is added.",
        "id": "occupancy_rating_rooms_6a",
        "label": "Occupancy rating for rooms (6 categories)",
        "name": "occupancy_rating_rooms_6a"
      }
    ],
    "edition": "2021",
    "id": "TS053",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify households in England and Wales by occupancy rating based on the number of rooms in the household. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-03-28T00:00:00.000Z",
      "state": "published",
      "title": "Occupancy rating for rooms",
      "unit_of_measure": "Household"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4",
            "id": "4"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS053"
          }
        },
        "isBasedOn": {
          "@id": "HH",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:32:03.183455Z",
      "sha256": "f2cf678c9fb1ac48d16dc7af7e067672e19ae5a2c3ee8f96c081daec88a18485",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "4",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4"
  }
}
---

# Occupancy rating for rooms

This dataset provides Census 2021 estimates that classify households in England and Wales by occupancy rating based on the number of rooms in the household. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS053`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS053/editions/2021/versions/4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
