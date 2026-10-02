---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/provenance-entity",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Provenance entity",
  "description": "An identifiable thing whose production or use can be described.",
  "nativeIdentifier": "provenance-entity",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/prov-o/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "provenance",
    "Provenance entity",
    "provenance-entity"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/prov-o/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C PROV-O",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/prov-o/"
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
    "scopeBoundary": "Keep versions distinguishable where their attributes differ.",
    "topic": "provenance",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Provenance entity",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Keep versions distinguishable where their attributes differ.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/prov#Entity"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/provenance-activity"
    }
  ],
  "okfp:machineImported": false
}
---

# Provenance entity

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/prov-o/) · reviewed 2 October 2026.

Related concept records: [provenance activity](provenance-activity.md).
