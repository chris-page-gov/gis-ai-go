---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/learning-path/pavement-width",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Find and qualify pavement width",
  "description": "Choose the appropriate versioned feature and explain what a pavement-width field can support before requesting geographic data.",
  "nativeIdentifier": "pavement-width",
  "sourceFamily": "learning-path",
  "resource": "https://github.com/chris-page-gov/gis-ai-go/blob/main/okf-plus/records/learning-path/pavement-width.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored learning-path metadata"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "project-authored-not-human-evaluated",
  "tags": [
    "learning path",
    "OS NGD",
    "pavement-width"
  ],
  "sources": [
    {
      "resource": "https://github.com/chris-page-gov/gis-ai-go/blob/main/docs/implementation/OKF_OS_RECOVERY.md",
      "evidenceKind": "project-source-review",
      "referenceTitle": "OS recovery: user example acceptance boundaries",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "retained-project-guide-read"
    },
    {
      "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Road Link",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://www.w3.org/TR/vocab-dcat-3/",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Dataset version",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://www.w3.org/TR/vocab-dqv/",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Quality measurement",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Road Link v5",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pavementlink-1",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Pavement Link v1",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-attribution.md",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Pavement attribution",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    }
  ],
  "temporal": {
    "status": "not-applicable",
    "kind": "learning-record",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Learning sequence; not a feature validity or observation period."
  },
  "update": {
    "frequency": {
      "status": "not-applicable",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Authored learning instructions with public-source references; source rights retained.",
    "describedData": "No data licence or entitlement established by a learning path.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Authored learning navigation, not a semantic relationship between OS features or an assessment programme.",
    "Retained project evidence was reviewed; current live source, complete geographic coverage and human learning outcomes are not verified.",
    "Selecting a step does not retrieve geographic data or authorise a provider call."
  ],
  "details": {
    "learningPath": {
      "schema": "gis-ai-go.okf-plus-learning-path.v1",
      "id": "pavement-width",
      "title": "Find and qualify pavement width",
      "description": "Choose the appropriate versioned feature and explain what a pavement-width field can support before requesting geographic data.",
      "objectives": [
        "Identify the parent collection and version for a pavement-width field.",
        "Distinguish Road Link attribution from separate Pavement Link features and report measurement limits."
      ],
      "prerequisiteConcepts": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
          "purpose": "Recognise a Road Link as a source-defined feature, rather than a pavement outline."
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version",
          "purpose": "Keep product and collection versions attached to field meanings."
        }
      ],
      "steps": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
          "title": "Identify the feature being described",
          "outcome": "Name the feature type and state why its label alone cannot establish pavement geometry.",
          "practice": "Read the linked Road Link concept and its scope note. Write the feature name that the question actually needs.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version"
          ],
          "sourceRefs": [
            "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5",
          "title": "Inspect Road Link v5 width fields",
          "outcome": "Find the source-native pavement-width fields and distinguish structural evidence from a complete definition.",
          "practice": "Find presenceofpavement_averagewidth_m and presenceofpavement_minimumwidth_m. Record the parent collection/version, units where evidenced, nullability and any missing definition.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version"
          ],
          "sourceRefs": [
            "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pavementlink-1",
          "title": "Compare the separate Pavement Link collection",
          "outcome": "Explain which parent collection is relevant without treating similar width labels as equivalent.",
          "practice": "Inspect Pavement Link v1. Compare its native width fields and version with Road Link v5; list the evidence still needed before choosing either.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version"
          ],
          "sourceRefs": [
            "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pavementlink-1"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fusing-os-ngd-data%2Fos-ngd-transport%2Fpavements%2Fpavement-attribution.md",
          "title": "Check the documented derivation and limits",
          "outcome": "Explain the distinction between Road Link pavement attribution and separate side-specific links.",
          "practice": "Read the retained pavement-attribution reference and follow its source. Explain that the documented links coincide with road geometry; do not infer pavement centre lines, outlines or a routable network. State any current-version or coverage gap.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
          ],
          "sourceRefs": [
            "https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-attribution.md"
          ]
        }
      ],
      "prerequisites": [],
      "relationshipScope": "learning-navigation-only"
    }
  },
  "okfp:machineImported": false
}
---

# Find and qualify pavement width

Choose the appropriate versioned feature and explain what a pavement-width field can support before requesting geographic data.

## Objectives

- Identify the parent collection and version for a pavement-width field.
- Distinguish Road Link attribution from separate Pavement Link features and report measurement limits.

## Before you start

- [Road Link](../vocabulary-learning/road-link.md): Recognise a Road Link as a source-defined feature, rather than a pavement outline.
- [Dataset version](../geospatial-concepts/dataset-version.md): Keep product and collection versions attached to field meanings.

## Ordered practice

### 1. Identify the feature being described

[Open the source record](../vocabulary-learning/road-link.md).

Read the linked Road Link concept and its scope note. Write the feature name that the question actually needs.

Expected outcome: Name the feature type and state why its label alone cannot establish pavement geometry.

### 2. Inspect Road Link v5 width fields

[Open the source record](../os-ngd-collections/trn-ntwk-roadlink-5-6a2673b158fc.md).

Find presenceofpavement_averagewidth_m and presenceofpavement_minimumwidth_m. Record the parent collection/version, units where evidenced, nullability and any missing definition.

Expected outcome: Find the source-native pavement-width fields and distinguish structural evidence from a complete definition.

### 3. Compare the separate Pavement Link collection

[Open the source record](../os-ngd-collections/trn-ntwk-pavementlink-1-630572050937.md).

Inspect Pavement Link v1. Compare its native width fields and version with Road Link v5; list the evidence still needed before choosing either.

Expected outcome: Explain which parent collection is relevant without treating similar width labels as equivalent.

### 4. Check the documented derivation and limits

[Open the source record](../osngd-documentation/https-docs-os-uk-osngd-using-os-ngd-data-os-ngd-transport-pavements-pavement-att-20d09c62fec6.md).

Read the retained pavement-attribution reference and follow its source. Explain that the documented links coincide with road geometry; do not infer pavement centre lines, outlines or a routable network. State any current-version or coverage gap.

Expected outcome: Explain the distinction between Road Link pavement attribution and separate side-specific links.

## Evidence and limits

Definitions stay in the linked authoritative records. These links organise learning; they assert no data relationship, field equivalence or completed retrieval.

[OS recovery and acceptance boundaries](https://github.com/chris-page-gov/gis-ai-go/blob/main/docs/implementation/OKF_OS_RECOVERY.md).

- [Road Link](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link)
- [Dataset version](https://www.w3.org/TR/vocab-dcat-3/)
- [Quality measurement](https://www.w3.org/TR/vocab-dqv/)
- [Road Link v5](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5)
- [Pavement Link v1](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pavementlink-1)
- [Pavement attribution](https://docs.os.uk/osngd/using-os-ngd-data/os-ngd-transport/pavements/pavement-attribution.md)

Practice progress is not assessment or certification. Current live availability, missing definitions and full geographic coverage remain separate checks.
