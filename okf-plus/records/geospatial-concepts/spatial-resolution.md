---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/spatial-resolution",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Spatial resolution",
  "description": "A stated spatial detail level associated with a dataset or distribution.",
  "nativeIdentifier": "spatial-resolution",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/vocab-dcat-3/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "catalogue",
    "Spatial resolution",
    "spatial-resolution"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/vocab-dcat-3/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C DCAT 3",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/vocab-dcat-3/"
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
    "scopeBoundary": "Resolution does not by itself establish positional accuracy.",
    "topic": "catalogue",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Spatial resolution",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Resolution does not by itself establish positional accuracy.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#spatialResolutionInMeters"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/gridded-coverage"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
    }
  ],
  "okfp:machineImported": false
}
---

# Spatial resolution

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/vocab-dcat-3/) · reviewed 2 October 2026.

Related concept records: [gridded coverage](gridded-coverage.md), [quality measurement](quality-measurement.md).
