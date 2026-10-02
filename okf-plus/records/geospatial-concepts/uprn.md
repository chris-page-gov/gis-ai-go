---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/uprn",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Unique Property Reference Number",
  "description": "A persistent identifier for an addressable location in Great Britain.",
  "nativeIdentifier": "uprn",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK identifiers",
    "Unique Property Reference Number",
    "uprn"
  ],
  "sources": [
    {
      "resource": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information",
      "evidenceKind": "official-reference",
      "referenceTitle": "Government property and street identifier standard",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information"
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
    "scopeBoundary": "One coordinate can correspond to multiple UPRNs.",
    "topic": "UK identifiers",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Unique Property Reference Number",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "One coordinate can correspond to multiple UPRNs.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/identifier"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/usrn"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/point"
    }
  ],
  "okfp:machineImported": false
}
---

# Unique Property Reference Number

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information) · reviewed 2 October 2026.

Related concept records: [usrn](usrn.md), [point](point.md).
