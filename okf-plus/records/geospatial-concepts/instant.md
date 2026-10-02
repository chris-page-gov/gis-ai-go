---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/instant",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Temporal instant",
  "description": "A time position treated as having no duration in the model.",
  "nativeIdentifier": "instant",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/owl-time/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "time",
    "Temporal instant",
    "instant"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/owl-time/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C Time Ontology in OWL",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/owl-time/"
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
    "scopeBoundary": "State the temporal reference system.",
    "topic": "time",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Temporal instant",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "State the temporal reference system.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/2006/time#Instant"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/interval"
    }
  ],
  "okfp:machineImported": false
}
---

# Temporal instant

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/owl-time/) · reviewed 2 October 2026.

Related concept records: [interval](interval.md).
