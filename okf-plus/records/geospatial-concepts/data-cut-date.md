---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/data-cut-date",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Data-cut date",
  "description": "The point used to determine which source changes enter a release.",
  "nativeIdentifier": "data-cut-date",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "data lifecycle",
    "Data-cut date",
    "data-cut-date"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS product refresh dates",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates"
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
    "scopeBoundary": "Later publication does not imply equally recent source content.",
    "topic": "data lifecycle",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Data-cut date",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Later publication does not imply equally recent source content.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/temporal"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/release-date"
    }
  ],
  "okfp:machineImported": false
}
---

# Data-cut date

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates) · reviewed 2 October 2026.

Related concept records: [release date](release-date.md).
