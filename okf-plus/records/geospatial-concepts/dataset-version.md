---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Dataset version",
  "description": "An identified revision of a dataset or related catalogue resource.",
  "nativeIdentifier": "dataset-version",
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
    "Dataset version",
    "dataset-version"
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
    "scopeBoundary": "Keep version identity separate from observation period.",
    "topic": "catalogue",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Dataset version",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Keep version identity separate from observation period.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#version"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/reference-period"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/release-date"
    }
  ],
  "okfp:machineImported": false
}
---

# Dataset version

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/vocab-dcat-3/) · reviewed 2 October 2026.

Related concept records: [reference period](reference-period.md), [release date](release-date.md).
