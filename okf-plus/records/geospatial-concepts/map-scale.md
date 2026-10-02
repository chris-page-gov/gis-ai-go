---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/map-scale",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Map scale",
  "description": "The relationship between distance on a map and represented ground distance.",
  "nativeIdentifier": "map-scale",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/scale",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "cartography",
    "Map scale",
    "map-scale"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/scale",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS cartographic scale guidance",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/scale"
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
    "scopeBoundary": "A smaller-scale map usually needs more generalisation.",
    "topic": "cartography",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Map scale",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A smaller-scale map usually needs more generalisation.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/extent"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/cartographic-generalisation"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/spatial-resolution"
    }
  ],
  "okfp:machineImported": false
}
---

# Map scale

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/scale) · reviewed 2 October 2026.

Related concept records: [cartographic generalisation](cartographic-generalisation.md), [spatial resolution](spatial-resolution.md).
