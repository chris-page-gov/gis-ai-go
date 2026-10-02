---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coverage",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Spatial coverage",
  "description": "A function associating positions in a domain with values in a range.",
  "nativeIdentifier": "coverage",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.ogc.org/is/09-146r8/09-146r8.html",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "coverage",
    "Spatial coverage",
    "coverage"
  ],
  "sources": [
    {
      "resource": "https://docs.ogc.org/is/09-146r8/09-146r8.html",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC Coverage Implementation Schema 1.1",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.ogc.org/is/09-146r8/09-146r8.html"
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
    "scopeBoundary": "Coverage is more general than a map image.",
    "topic": "coverage",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Spatial coverage",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Coverage is more general than a map image.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#Dataset"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coverage-domain"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coverage-range"
    }
  ],
  "okfp:machineImported": false
}
---

# Spatial coverage

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.ogc.org/is/09-146r8/09-146r8.html) · reviewed 2 October 2026.

Related concept records: [coverage domain](coverage-domain.md), [coverage range](coverage-range.md).
