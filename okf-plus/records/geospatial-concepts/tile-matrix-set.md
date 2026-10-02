---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/tile-matrix-set",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Tile matrix set",
  "description": "A scheme defining tiled coverage across coordinate space and resolution levels.",
  "nativeIdentifier": "tile-matrix-set",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ogc.org/standards/tms/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "map delivery",
    "Tile matrix set",
    "tile-matrix-set"
  ],
  "sources": [
    {
      "resource": "https://www.ogc.org/standards/tms/",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC Two Dimensional Tile Matrix Set",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ogc.org/standards/tms/"
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
    "scopeBoundary": "Tile indices require the matching scheme.",
    "topic": "map delivery",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Tile matrix set",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Tile indices require the matching scheme.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/Standard"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/map-tile"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/spatial-resolution"
    }
  ],
  "okfp:machineImported": false
}
---

# Tile matrix set

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ogc.org/standards/tms/) · reviewed 2 October 2026.

Related concept records: [map tile](map-tile.md), [spatial resolution](spatial-resolution.md).
