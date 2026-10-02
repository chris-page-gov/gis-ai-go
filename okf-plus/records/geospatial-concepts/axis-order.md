---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/axis-order",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Coordinate axis order",
  "description": "The sequence assigned to coordinate components; RFC 7946 uses longitude then latitude.",
  "nativeIdentifier": "axis-order",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.rfc-editor.org/rfc/rfc7946",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "geometry encoding",
    "Coordinate axis order",
    "axis-order"
  ],
  "sources": [
    {
      "resource": "https://www.rfc-editor.org/rfc/rfc7946",
      "evidenceKind": "official-reference",
      "referenceTitle": "IETF RFC 7946",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.rfc-editor.org/rfc/rfc7946"
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
    "scopeBoundary": "Do not infer order from numeric plausibility.",
    "topic": "geometry encoding",
    "mappingInterpretation": "No direct external ontology term is asserted. The source-reviewed definition and internal concept relationships are retained without a guessed mapping.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Coordinate axis order",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Do not infer order from numeric plausibility.",
    "@language": "en-GB"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system"
    }
  ],
  "okfp:machineImported": false
}
---

# Coordinate axis order

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.rfc-editor.org/rfc/rfc7946) · reviewed 2 October 2026.

Related concept records: [coordinate reference system](coordinate-reference-system.md).
