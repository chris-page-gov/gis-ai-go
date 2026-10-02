---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geography-code",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Geography code",
  "description": "A published identifier for a specified geographic entity within a coding system.",
  "nativeIdentifier": "geography-code",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK geography",
    "Geography code",
    "geography-code"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS names, codes and lookups",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups"
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
    "scopeBoundary": "Retain code, geography type and applicable release.",
    "topic": "UK geography",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Geography code",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Retain code, geography type and applicable release.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/identifier"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geography-vintage"
    }
  ],
  "okfp:machineImported": false
}
---

# Geography code

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups) · reviewed 2 October 2026.

Related concept records: [geography vintage](geography-vintage.md).
