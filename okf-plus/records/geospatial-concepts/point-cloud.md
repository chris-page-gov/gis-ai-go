---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/point-cloud",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Point cloud",
  "description": "A collection of spatial point records, commonly including LiDAR-derived coordinates and attributes.",
  "nativeIdentifier": "point-cloud",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ogc.org/standards/las/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "3D representation",
    "Point cloud",
    "point-cloud"
  ],
  "sources": [
    {
      "resource": "https://www.ogc.org/standards/las/",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC LAS community standard overview",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ogc.org/standards/las/"
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
    "scopeBoundary": "Points do not automatically form a semantic building model.",
    "topic": "3D representation",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Point cloud",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Points do not automatically form a semantic building model.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/geosparql#Geometry"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/point"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/semantic-3d-model"
    }
  ],
  "okfp:machineImported": false
}
---

# Point cloud

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ogc.org/standards/las/) · reviewed 2 October 2026.

Related concept records: [point](point.md), [semantic 3d model](semantic-3d-model.md).
