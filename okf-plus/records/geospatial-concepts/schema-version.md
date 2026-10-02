---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/schema-version",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Schema version",
  "description": "An identified revision of the contract defining a feature type and its fields.",
  "nativeIdentifier": "schema-version",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "schema lifecycle",
    "Schema version",
    "schema-version"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD schema versioning",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning"
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
    "scopeBoundary": "Maintained older schemas may still receive current data.",
    "topic": "schema lifecycle",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Schema version",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Maintained older schemas may still receive current data.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/conformsTo"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/dataset-version"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/queryable-field"
    }
  ],
  "okfp:machineImported": false
}
---

# Schema version

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning) · reviewed 2 October 2026.

Related concept records: [dataset version](dataset-version.md), [queryable field](queryable-field.md).
