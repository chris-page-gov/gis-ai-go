---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/web-map-image",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Web map image",
  "description": "A georeferenced visual portrayal returned by a map service.",
  "nativeIdentifier": "web-map-image",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ogc.org/standards/wms/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "map delivery",
    "Web map image",
    "web-map-image"
  ],
  "sources": [
    {
      "resource": "https://www.ogc.org/standards/wms/",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC WMS overview",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ogc.org/standards/wms/"
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
    "scopeBoundary": "An image is not the underlying feature table.",
    "topic": "map delivery",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Web map image",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "An image is not the underlying feature table.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#Distribution"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/feature"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/map-layer"
    }
  ],
  "okfp:machineImported": false
}
---

# Web map image

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ogc.org/standards/wms/) · reviewed 2 October 2026.

Related concept records: [feature](feature.md), [map layer](map-layer.md).
