---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/level-of-detail",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Level of detail",
  "description": "An explicit level of representation within a 3D information model.",
  "nativeIdentifier": "level-of-detail",
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
    "Level of detail",
    "level-of-detail"
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
    "scopeBoundary": "Greater detail is not automatically greater accuracy.",
    "topic": "3D representation",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Level of detail",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Greater detail is not automatically greater accuracy.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/Standard"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/semantic-3d-model"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/quality-measurement"
    }
  ],
  "okfp:machineImported": false
}
---

# Level of detail

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ogc.org/standards/citygml/) · reviewed 2 October 2026.

Related concept records: [semantic 3d model](semantic-3d-model.md), [quality measurement](quality-measurement.md).
