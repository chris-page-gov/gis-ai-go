---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Coordinate reference system",
  "description": "A coordinate system connected to its reference object through a datum.",
  "nativeIdentifier": "coordinate-reference-system",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "geospatial representation",
    "Coordinate reference system",
    "coordinate-reference-system"
  ],
  "sources": [
    {
      "resource": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC GeoSPARQL 1.1",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.ogc.org/is/22-047r1/22-047r1.html"
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
    "scopeBoundary": "Coordinates alone do not establish location.",
    "topic": "geospatial representation",
    "mappingInterpretation": "Associative link to the GeoSPARQL function that retrieves a geometry CRS identifier; this concept is not the function and does not assert class equivalence.",
    "reviewedOn": "2026-10-02",
    "mappingReference": "https://docs.ogc.org/is/22-047r1/22-047r1.html"
  },
  "skos:prefLabel": {
    "@value": "Coordinate reference system",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Coordinates alone do not establish location.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/def/function/geosparql/getSRID"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/datum"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/axis-order"
    }
  ],
  "okfp:machineImported": false
}
---

# Coordinate reference system

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.ogc.org/is/22-047r1/22-047r1.html) · reviewed 2 October 2026.

Related concept records: [datum](datum.md), [axis order](axis-order.md).
