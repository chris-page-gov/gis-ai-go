---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/point",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Point geometry",
  "description": "A geometry encoded by a single coordinate position.",
  "nativeIdentifier": "point",
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
    "Point geometry",
    "point"
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
    "scopeBoundary": "A representative point is not an area.",
    "topic": "geometry encoding",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Point geometry",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A representative point is not an area.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/sf#Point"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/polygon"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/postcode-allocation"
    }
  ],
  "okfp:machineImported": false
}
---

# Point geometry

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.rfc-editor.org/rfc/rfc7946) · reviewed 2 October 2026.

Related concept records: [polygon](polygon.md), [postcode allocation](postcode-allocation.md).
