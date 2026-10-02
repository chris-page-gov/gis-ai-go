---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/reference-period",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Statistical reference period",
  "description": "The time dimension identifying when a statistical observation applies.",
  "nativeIdentifier": "reference-period",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.w3.org/TR/vocab-data-cube/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "statistics",
    "Statistical reference period",
    "reference-period"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/vocab-data-cube/",
      "evidenceKind": "official-reference",
      "referenceTitle": "W3C RDF Data Cube Vocabulary",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.w3.org/TR/vocab-data-cube/"
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
    "scopeBoundary": "Publication and revision dates are different metadata.",
    "topic": "statistics",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Statistical reference period",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Publication and revision dates are different metadata.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/release-date"
    }
  ],
  "okfp:machineImported": false
}
---

# Statistical reference period

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.w3.org/TR/vocab-data-cube/) · reviewed 2 October 2026.

Related concept records: [release date](release-date.md).
