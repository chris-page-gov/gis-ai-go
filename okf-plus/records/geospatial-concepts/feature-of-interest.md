---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/feature-of-interest",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Feature of interest",
  "description": "The entity whose property is examined by an observation.",
  "nativeIdentifier": "feature-of-interest",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/vocab-ssn/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "observation",
    "Feature of interest",
    "feature-of-interest"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/vocab-ssn/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C Semantic Sensor Network Ontology",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/vocab-ssn/"
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
    "scopeBoundary": "It need not be identical to a sampling feature.",
    "topic": "observation",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Feature of interest",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "It need not be identical to a sampling feature.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/sosa/FeatureOfInterest"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/observation"
    }
  ],
  "okfp:machineImported": false
}
---

# Feature of interest

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/vocab-ssn/) · reviewed 2 October 2026.

Related concept records: [observation](observation.md).
