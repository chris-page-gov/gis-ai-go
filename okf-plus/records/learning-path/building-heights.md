---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/learning-path/building-heights",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Interpret building heights with their reference",
  "description": "Keep absolute and relative building heights, units, quality and product versions separate when selecting evidence.",
  "nativeIdentifier": "building-heights",
  "sourceFamily": "learning-path",
  "resource": "https://github.com/chris-page-gov/gis-ai-go/blob/main/okf-plus/records/learning-path/building-heights.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored learning-path metadata"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "project-authored-not-human-evaluated",
  "tags": [
    "learning path",
    "OS NGD",
    "building-heights"
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
      "resource": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Coordinate reference system",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Height datum",
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Building v4",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Building",
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
      "id": "building-heights",
      "title": "Interpret building heights with their reference",
      "description": "Keep absolute and relative building heights, units, quality and product versions separate when selecting evidence.",
      "objectives": [
        "Distinguish absolute maximum, absolute minimum and relative building heights.",
        "Record the vertical reference, method, quality and source-version limits that qualify a height interpretation."
      ],
      "prerequisiteConcepts": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
          "purpose": "Distinguish the vertical reference from a relative difference in height."
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version",
          "purpose": "Avoid transferring rules from a different product or edition."
        }
      ],
      "steps": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
          "title": "Start with the vertical reference",
          "outcome": "State which reference is needed to interpret an absolute height.",
          "practice": "Read Height datum and its source. Explain why an absolute height needs a documented vertical reference, while a relative height describes a difference.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system"
          ],
          "sourceRefs": [
            "https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4",
          "title": "Inspect the Building v4 field evidence",
          "outcome": "Identify native height, method and quality fields without treating field discovery as observed data.",
          "practice": "Find height_absolutemax_m, height_absolutemin_m and height_absoluteroofbase_m. Contrast them with the relative-height fields. Record units, nullability, method, quality and date fields where evidenced; mark missing information explicitly.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
          ],
          "sourceRefs": [
            "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fdata-structure%2Fbuildings%2Fbuilding-features%2Fbuilding.md",
          "title": "Check the product definition before comparing heights",
          "outcome": "Explain the documented maximum and minimum meanings and retain the product-specific qualification.",
          "practice": "Read the retained NGD Building reference and its source. Check the maximum-height chimney qualification and underlying-ground minimum. Do not transfer legacy Building Height Attribute rules into NGD Building. State the documented datum or leave it unresolved.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
          ],
          "sourceRefs": [
            "https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md"
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

# Interpret building heights with their reference

Keep absolute and relative building heights, units, quality and product versions separate when selecting evidence.

## Objectives

- Distinguish absolute maximum, absolute minimum and relative building heights.
- Record the vertical reference, method, quality and source-version limits that qualify a height interpretation.

## Before you start

- [Height datum](../geospatial-concepts/height-datum.md): Distinguish the vertical reference from a relative difference in height.
- [Dataset version](../geospatial-concepts/dataset-version.md): Avoid transferring rules from a different product or edition.

## Ordered practice

### 1. Start with the vertical reference

[Open the source record](../geospatial-concepts/height-datum.md).

Read Height datum and its source. Explain why an absolute height needs a documented vertical reference, while a relative height describes a difference.

Expected outcome: State which reference is needed to interpret an absolute height.

### 2. Inspect the Building v4 field evidence

[Open the source record](../os-ngd-collections/bld-fts-building-4-5930dadf2ce2.md).

Find height_absolutemax_m, height_absolutemin_m and height_absoluteroofbase_m. Contrast them with the relative-height fields. Record units, nullability, method, quality and date fields where evidenced; mark missing information explicitly.

Expected outcome: Identify native height, method and quality fields without treating field discovery as observed data.

### 3. Check the product definition before comparing heights

[Open the source record](../osngd-documentation/https-docs-os-uk-osngd-data-structure-buildings-building-features-building-md-cf8ef1c6c03a.md).

Read the retained NGD Building reference and its source. Check the maximum-height chimney qualification and underlying-ground minimum. Do not transfer legacy Building Height Attribute rules into NGD Building. State the documented datum or leave it unresolved.

Expected outcome: Explain the documented maximum and minimum meanings and retain the product-specific qualification.

## Evidence and limits

Definitions stay in the linked authoritative records. These links organise learning; they assert no data relationship, field equivalence or completed retrieval.

[OS recovery and acceptance boundaries](https://github.com/chris-page-gov/gis-ai-go/blob/main/docs/implementation/OKF_OS_RECOVERY.md).

- [Coordinate reference system](https://docs.ogc.org/is/22-047r1/22-047r1.html)
- [Height datum](https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems)
- [Dataset version](https://www.w3.org/TR/vocab-dcat-3/)
- [Quality measurement](https://www.w3.org/TR/vocab-dqv/)
- [Building v4](https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4)
- [Building](https://docs.os.uk/osngd/data-structure/buildings/building-features/building.md)

Practice progress is not assessment or certification. Current live availability, missing definitions and full geographic coverage remain separate checks.
