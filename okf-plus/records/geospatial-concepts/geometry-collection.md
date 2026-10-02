---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geometry-collection",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Geometry collection",
  "description": "A container for multiple geometry objects, potentially of different types.",
  "nativeIdentifier": "geometry-collection",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.rfc-editor.org/rfc/rfc7946",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "geometry encoding",
    "Geometry collection",
    "geometry-collection"
  ],
  "sources": [
    {
      "resource": "https://www.rfc-editor.org/rfc/rfc7946",
      "evidenceKind": "official-reference",
      "referenceTitle": "IETF RFC 7946",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.rfc-editor.org/rfc/rfc7946"
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
    "scopeBoundary": "It is distinct from a feature collection.",
    "topic": "geometry encoding",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Geometry collection",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "It is distinct from a feature collection.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/sf#GeometryCollection"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geometry"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/feature"
    }
  ],
  "okfp:machineImported": false
}
---

# Geometry collection

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.rfc-editor.org/rfc/rfc7946) · reviewed 2 October 2026.

Related concept records: [geometry](geometry.md), [feature](feature.md).
