---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/learning-path/road-elevation",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Assess road elevation and vertical datum",
  "description": "Distinguish elevation gain, a 3D road coordinate and terrain-derived estimates before answering a height-above-sea-level question.",
  "nativeIdentifier": "road-elevation",
  "sourceFamily": "learning-path",
  "resource": "https://github.com/chris-page-gov/gis-ai-go/blob/main/okf-plus/records/learning-path/road-elevation.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored learning-path metadata"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "project-authored-not-human-evaluated",
  "tags": [
    "learning path",
    "OS NGD",
    "road-elevation"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Road Link v5",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue.md",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "heightingmethodvalue",
      "reviewedOn": "2026-10-24",
      "reviewMethod": "linked-OKF-record-read-not-live-source-validation"
    },
    {
      "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems.md",
      "evidenceKind": "retained-record-reference",
      "referenceTitle": "Coordinate reference systems",
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
      "id": "road-elevation",
      "title": "Assess road elevation and vertical datum",
      "description": "Distinguish elevation gain, a 3D road coordinate and terrain-derived estimates before answering a height-above-sea-level question.",
      "objectives": [
        "Explain why elevation-gain fields cannot answer an absolute road-elevation question.",
        "Check coordinate dimension, vertical reference, heighting method and bridge/tunnel limits before using a road height."
      ],
      "prerequisiteConcepts": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
          "purpose": "Name the vertical reference rather than assuming an instantaneous sea-level meaning."
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system",
          "purpose": "Distinguish horizontal and compound coordinate-reference systems."
        }
      ],
      "steps": [
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
          "title": "Clarify what height the question requires",
          "outcome": "Distinguish an absolute vertical coordinate from elevation gain or a relative height.",
          "practice": "Read Height datum. Write the requested quantity and vertical reference; list any ambiguity in the phrase height above sea level.",
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
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5",
          "title": "Inspect road geometry and elevation fields",
          "outcome": "Identify the versioned geometry evidence and keep gain separate from absolute elevation.",
          "practice": "Inspect Road Link v5. Find elevationgain_indirection and elevationgain_againstdirection and explain why their discovery does not answer absolute road elevation. Check geometry dimension and available heightingmethod evidence.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version"
          ],
          "sourceRefs": [
            "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fcode-lists%2Fcode-lists-overview%2Fheightingmethodvalue.md",
          "title": "Inspect heighting-method evidence",
          "outcome": "Report what the retained method list states and what it leaves undefined.",
          "practice": "Read the HeightingMethodValue source record. Inspect DTM, Interpolated Bridge and Interpolated Tunnel where retained. A method label does not establish an algorithm, direct survey accuracy or bridge clearance.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum"
          ],
          "sourceRefs": [
            "https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue.md"
          ]
        },
        {
          "recordId": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/osngd-documentation/https%3A%2F%2Fdocs.os.uk%2Fosngd%2Fgetting-started%2Fos-ngd-fundamentals%2Fcoordinate-reference-systems.md",
          "title": "Check the response reference and qualify the route",
          "outcome": "Explain the need for explicit response CRS, vertical datum, method and area-coverage evidence.",
          "practice": "Read the coordinate-reference-systems guidance. Check the documented EPSG:7405 and ODN-height route against an actual authorised response before claiming retrieval. Distinguish ODN height from instantaneous sea level and any separately derived terrain estimate. Retain missing CRS, method, accuracy and incomplete-paging gaps.",
          "minutes": 5,
          "conceptRefs": [
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
            "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
          ],
          "sourceRefs": [
            "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems.md"
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

# Assess road elevation and vertical datum

Distinguish elevation gain, a 3D road coordinate and terrain-derived estimates before answering a height-above-sea-level question.

## Objectives

- Explain why elevation-gain fields cannot answer an absolute road-elevation question.
- Check coordinate dimension, vertical reference, heighting method and bridge/tunnel limits before using a road height.

## Before you start

- [Height datum](../geospatial-concepts/height-datum.md): Name the vertical reference rather than assuming an instantaneous sea-level meaning.
- [Coordinate reference system](../geospatial-concepts/coordinate-reference-system.md): Distinguish horizontal and compound coordinate-reference systems.

## Ordered practice

### 1. Clarify what height the question requires

[Open the source record](../geospatial-concepts/height-datum.md).

Read Height datum. Write the requested quantity and vertical reference; list any ambiguity in the phrase height above sea level.

Expected outcome: Distinguish an absolute vertical coordinate from elevation gain or a relative height.

### 2. Inspect road geometry and elevation fields

[Open the source record](../os-ngd-collections/trn-ntwk-roadlink-5-6a2673b158fc.md).

Inspect Road Link v5. Find elevationgain_indirection and elevationgain_againstdirection and explain why their discovery does not answer absolute road elevation. Check geometry dimension and available heightingmethod evidence.

Expected outcome: Identify the versioned geometry evidence and keep gain separate from absolute elevation.

### 3. Inspect heighting-method evidence

[Open the source record](../osngd-documentation/https-docs-os-uk-osngd-code-lists-code-lists-overview-heightingmethodvalue-md-9998cf5f0049.md).

Read the HeightingMethodValue source record. Inspect DTM, Interpolated Bridge and Interpolated Tunnel where retained. A method label does not establish an algorithm, direct survey accuracy or bridge clearance.

Expected outcome: Report what the retained method list states and what it leaves undefined.

### 4. Check the response reference and qualify the route

[Open the source record](../osngd-documentation/https-docs-os-uk-osngd-getting-started-os-ngd-fundamentals-coordinate-reference--35a318edb915.md).

Read the coordinate-reference-systems guidance. Check the documented EPSG:7405 and ODN-height route against an actual authorised response before claiming retrieval. Distinguish ODN height from instantaneous sea level and any separately derived terrain estimate. Retain missing CRS, method, accuracy and incomplete-paging gaps.

Expected outcome: Explain the need for explicit response CRS, vertical datum, method and area-coverage evidence.

## Evidence and limits

Definitions stay in the linked authoritative records. These links organise learning; they assert no data relationship, field equivalence or completed retrieval.

[OS recovery and acceptance boundaries](https://github.com/chris-page-gov/gis-ai-go/blob/main/docs/implementation/OKF_OS_RECOVERY.md).

- [Road Link](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link)
- [Coordinate reference system](https://docs.ogc.org/is/22-047r1/22-047r1.html)
- [Height datum](https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems)
- [Dataset version](https://www.w3.org/TR/vocab-dcat-3/)
- [Quality measurement](https://www.w3.org/TR/vocab-dqv/)
- [Road Link v5](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5)
- [heightingmethodvalue](https://docs.os.uk/osngd/code-lists/code-lists-overview/heightingmethodvalue.md)
- [Coordinate reference systems](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems.md)

Practice progress is not assessment or certification. Current live availability, missing definitions and full geographic coverage remain separate checks.
