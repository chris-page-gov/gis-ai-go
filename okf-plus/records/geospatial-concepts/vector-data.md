---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/vector-data",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Vector spatial data",
  "description": "A representation using discrete features and geometries such as points, lines and polygons.",
  "nativeIdentifier": "vector-data",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/sdw-bp/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "geospatial representation",
    "Vector spatial data",
    "vector-data"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/sdw-bp/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C/OGC Spatial Data on the Web best-practice note",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/sdw-bp/"
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
    "scopeBoundary": "The representation does not establish positional accuracy.",
    "topic": "geospatial representation",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Vector spatial data",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "The representation does not establish positional accuracy.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/geosparql#Geometry"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/feature"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geometry"
    }
  ],
  "okfp:machineImported": false
}
---

# Vector spatial data

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/sdw-bp/) · reviewed 2 October 2026.

Related concept records: [feature](feature.md), [geometry](geometry.md).
