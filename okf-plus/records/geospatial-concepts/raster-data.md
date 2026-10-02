---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/raster-data",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Raster spatial data",
  "description": "A representation arranging spatial values in cells of a grid.",
  "nativeIdentifier": "raster-data",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/sdw-bp/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "coverage",
    "Raster spatial data",
    "raster-data"
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
    "scopeBoundary": "Pixel values may represent measurements or visual portrayal.",
    "topic": "coverage",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Raster spatial data",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Pixel values may represent measurements or visual portrayal.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#Dataset"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/gridded-coverage"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/web-map-image"
    }
  ],
  "okfp:machineImported": false
}
---

# Raster spatial data

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/sdw-bp/) · reviewed 2 October 2026.

Related concept records: [gridded coverage](gridded-coverage.md), [web map image](web-map-image.md).
