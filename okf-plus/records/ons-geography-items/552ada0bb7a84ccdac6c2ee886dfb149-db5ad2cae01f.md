---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-geography-items/552ada0bb7a84ccdac6c2ee886dfb149",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Rural Urban Classification (2021) of 260611 Police Force Areas (2025) EW",
  "description": "Rural Urban Classification (2021) The 2021 RUC is a statistical classification to provide a consistent and standardised method for classifying geographies as rural or urban. This is based on address density, physical settlement form, population size and Relative Access to Major towns and cities (populations of over 75,000 people). The classification is produced by the Office for National Statistics (ONS) with advice from the Department for Environment, Food and Rural Affairs (DEFRA), the Welsh Government and colleagues from the Government Geography Profession (GGP). 260611 Police Force Areas (2025) EW Rural Urban Classification (2021) of Police Force Areas (2025) This is 2021 rural-urban classification (RUC) of the 2025 Police Force Areas for England and Wales. This means that the 2021 RUC methodology has been applied to the 2025 Police Force Areas boundaries. Police Force Areas classifications are divided into four categories based on their populations: 1. Majority Rural: had at least 50% of their population residing in rural OAs 2. Intermediate Rural: 35-50% of their population residing in rural OAs 3. Intermediate Urban: 20-35% of their population residing in rural OAs 4. Urban: 20% of less of the population lived in rural OAs. Each 2025 Police Force Areas category is split into one of two Relative Access categories, using the same data as the 2021 Output Area RUC. If more than 50% of a population lives in ‘Nearer a major town or city’ OAs, it is deemed to be ‘nearer a major town or city’; otherwise, it is classified as ‘further from a major town or city’. Field Names – PFA25CD, PFA25NM, RUC21CD, RUC21NM, Rural Urban Flag, RUC21 settlement class, Proportion of population in rural OAs (%), RUC21 relative access, Proportion of population in OAs further from a major town or city (%) Field Types - Text, Text, Text, Text, Text, Text, Double, Text, Double Field Lengths - 9, 19, 3, 62, 5, 18, 4, 42, 4",
  "nativeIdentifier": "552ada0bb7a84ccdac6c2ee886dfb149",
  "sourceFamily": "ons-geography-items",
  "resource": "https://geoportal.statistics.gov.uk/items/552ada0bb7a84ccdac6c2ee886dfb149",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "CSV",
    "RUC",
    "Police_Force_Areas",
    "EW",
    "Feature Service"
  ],
  "sources": [
    {
      "resource": "https://www.arcgis.com/sharing/rest/search?f=json&q=orgid%3AESMARspQHYMw9BZ9&num=100&start=6701&sortField=created&sortOrder=asc",
      "retrievedAt": "2026-10-02T01:28:50.062941Z",
      "responseSha256": "2ef8f151923f7bf337c313d1b2dd05d2c879a32de30b8c65347ed6e4261e12d6",
      "sourcePointer": "/results/17",
      "normalisedSource": "okf-plus/source/ons-geography-items.json",
      "normalisedPointer": "/records/6717",
      "normalisedRecordSha256": "deb5f675425620d40c114b5993b34e5b88a8cd2a7eaaaad55d3a88cc84dd3f9e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://geoportal.statistics.gov.uk/items/552ada0bb7a84ccdac6c2ee886dfb149"
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
      "https://geoportal.statistics.gov.uk/"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": "2026-09-29T13:39:06Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "https://www.ons.gov.uk/methodology/geography/licences",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "A date in an item title is not automatically the observation/reference range.",
    "Portal items can be different representations or vintages of one product."
  ],
  "details": {
    "access": "public",
    "categories": [
      "/Categories/Products/Rural-Urban Classification",
      "/Categories/ONS Geography Open Data"
    ],
    "created": 1790093243000,
    "culture": "en-gb",
    "description": "Rural Urban Classification (2021) The 2021 RUC is a statistical classification to provide a consistent and standardised method for classifying geographies as rural or urban. This is based on address density, physical settlement form, population size and Relative Access to Major towns and cities (populations of over 75,000 people). The classification is produced by the Office for National Statistics (ONS) with advice from the Department for Environment, Food and Rural Affairs (DEFRA), the Welsh Government and colleagues from the Government Geography Profession (GGP). 260611 Police Force Areas (2025) EW Rural Urban Classification (2021) of Police Force Areas (2025) This is 2021 rural-urban classification (RUC) of the 2025 Police Force Areas for England and Wales. This means that the 2021 RUC methodology has been applied to the 2025 Police Force Areas boundaries. Police Force Areas classifications are divided into four categories based on their populations: 1. Majority Rural: had at least 50% of their population residing in rural OAs 2. Intermediate Rural: 35-50% of their population residing in rural OAs 3. Intermediate Urban: 20-35% of their population residing in rural OAs 4. Urban: 20% of less of the population lived in rural OAs. Each 2025 Police Force Areas category is split into one of two Relative Access categories, using the same data as the 2021 Output Area RUC. If more than 50% of a population lives in ‘Nearer a major town or city’ OAs, it is deemed to be ‘nearer a major town or city’; otherwise, it is classified as ‘further from a major town or city’. Field Names – PFA25CD, PFA25NM, RUC21CD, RUC21NM, Rural Urban Flag, RUC21 settlement class, Proportion of population in rural OAs (%), RUC21 relative access, Proportion of population in OAs further from a major town or city (%) Field Types - Text, Text, Text, Text, Text, Text, Double, Text, Double Field Lengths - 9, 19, 3, 62, 5, 18, 4, 42, 4",
    "extent": [
      [
        -5.4,
        51.3
      ],
      [
        -2.6,
        53.5
      ]
    ],
    "id": "552ada0bb7a84ccdac6c2ee886dfb149",
    "licenseInfo": "<p><a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://www.ons.gov.uk/methodology/geography/licences\">https://www.ons.gov.uk/methodology/geography/licences</a></p>",
    "modified": 1790689146000,
    "organisationId": "ESMARspQHYMw9BZ9",
    "snippet": "Rural Urban Classification (2021) of 260611 Police Force Areas (2025) EW",
    "spatialReference": null,
    "tags": [
      "CSV",
      "RUC",
      "Police_Force_Areas",
      "EW"
    ],
    "title": "Rural Urban Classification (2021) of 260611 Police Force Areas (2025) EW",
    "type": "Feature Service",
    "typeKeywords": [
      "ArcGIS Server",
      "Data",
      "Feature Access",
      "Feature Service",
      "Metadata",
      "Service",
      "Singlelayer",
      "Table",
      "Hosted Service"
    ],
    "url": "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/260611_Police_Force_Areas_2025_EW/FeatureServer"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  }
}
---

# Rural Urban Classification (2021) of 260611 Police Force Areas (2025) EW

Rural Urban Classification (2021) The 2021 RUC is a statistical classification to provide a consistent and standardised method for classifying geographies as rural or urban. This is based on address density, physical settlement form, population size and Relative Access to Major towns and cities (populations of over 75,000 people). The classification is produced by the Office for National Statistics (ONS) with advice from the Department for Environment, Food and Rural Affairs (DEFRA), the Welsh Government and colleagues from the Government Geography Profession (GGP). 260611 Police Force Areas (2025) EW Rural Urban Classification (2021) of Police Force Areas (2025) This is 2021 rural-urban classification (RUC) of the 2025 Police Force Areas for England and Wales. This means that the 2021 RUC methodology has been applied to the 2025 Police Force Areas boundaries. Police Force Areas classifications are divided into four categories based on their populations: 1. Majority Rural: had at least 50% of their population residing in rural OAs 2. Intermediate Rural: 35-50% of their population residing in rural OAs 3. Intermediate Urban: 20-35% of their population residing in rural OAs 4. Urban: 20% of less of the population lived in rural OAs. Each 2025 Police Force Areas category is split into one of two Relative Access categories, using the same data as the 2021 Output Area RUC. If more than 50% of a population lives in ‘Nearer a major town or city’ OAs, it is deemed to be ‘nearer a major town or city’; otherwise, it is classified as ‘further from a major town or city’. Field Names – PFA25CD, PFA25NM, RUC21CD, RUC21NM, Rural Urban Flag, RUC21 settlement class, Proportion of population in rural OAs (%), RUC21 relative access, Proportion of population in OAs further from a major town or city (%) Field Types - Text, Text, Text, Text, Text, Text, Double, Text, Double Field Lengths - 9, 19, 3, 62, 5, 18, 4, 42, 4

Native identifier: `552ada0bb7a84ccdac6c2ee886dfb149`.

Source family: `ons-geography-items`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://geoportal.statistics.gov.uk/items/552ada0bb7a84ccdac6c2ee886dfb149)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://geoportal.statistics.gov.uk/)

## Evidence limits

- A date in an item title is not automatically the observation/reference range.
- Portal items can be different representations or vintages of one product.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
