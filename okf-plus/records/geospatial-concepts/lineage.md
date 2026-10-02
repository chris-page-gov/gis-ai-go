---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/lineage",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Data lineage",
  "description": "Evidence of derivation linking an output to entities and activities that produced it.",
  "nativeIdentifier": "lineage",
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
    "Data lineage",
    "lineage"
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
    "scopeBoundary": "A source URL alone is incomplete process evidence.",
    "topic": "provenance",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Data lineage",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A source URL alone is incomplete process evidence.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/prov#wasDerivedFrom"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/provenance-entity"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/provenance-activity"
    }
  ],
  "okfp:machineImported": false
}
---

# Data lineage

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/prov-o/) · reviewed 2 October 2026.

Related concept records: [provenance entity](provenance-entity.md), [provenance activity](provenance-activity.md).
