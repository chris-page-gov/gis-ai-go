---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/semantic-3d-model",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Semantic 3D city model",
  "description": "A representation combining urban object meaning, geometry and relationships in three dimensions.",
  "nativeIdentifier": "semantic-3d-model",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ogc.org/standards/citygml/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "3D representation",
    "Semantic 3D city model",
    "semantic-3d-model"
  ],
  "sources": [
    {
      "resource": "https://www.ogc.org/standards/citygml/",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC CityGML overview",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ogc.org/standards/citygml/"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "concept-record",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
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
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "The concept scheme is extensible and does not claim exhaustive geospatial coverage.",
    "Agent source review is not independent human acceptance."
  ],
  "details": {
    "scopeBoundary": "Visual realism alone does not establish object semantics.",
    "topic": "3D representation",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Semantic 3D city model",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Visual realism alone does not establish object semantics.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/geosparql#Feature"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geometry"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/level-of-detail"
    }
  ],
  "okfp:machineImported": false
}
---

# Semantic 3D city model

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ogc.org/standards/citygml/) · reviewed 2 October 2026.

Related concept records: [geometry](geometry.md), [level of detail](level-of-detail.md).
