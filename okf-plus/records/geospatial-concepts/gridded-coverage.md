---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/gridded-coverage",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Gridded coverage",
  "description": "A coverage whose domain positions are organised using a grid.",
  "nativeIdentifier": "gridded-coverage",
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
    "Gridded coverage",
    "gridded-coverage"
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
    "scopeBoundary": "A grid need not be a simple regular image.",
    "topic": "coverage",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Gridded coverage",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A grid need not be a simple regular image.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.w3.org/ns/dcat#Dataset"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coverage"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/spatial-resolution"
    }
  ],
  "okfp:machineImported": false
}
---

# Gridded coverage

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.ogc.org/is/09-146r8/09-146r8.html) · reviewed 2 October 2026.

Related concept records: [coverage](coverage.md), [spatial resolution](spatial-resolution.md).
