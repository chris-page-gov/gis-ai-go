---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/toid",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Topographic Identifier",
  "description": "A persistent identifier for a feature in OS MasterMap products.",
  "nativeIdentifier": "toid",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK identifiers",
    "Topographic Identifier",
    "toid"
  ],
  "sources": [
    {
      "resource": "https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS mapping reference numbers",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers"
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
    "scopeBoundary": "A TOID is not interchangeable with a UPRN.",
    "topic": "UK identifiers",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Topographic Identifier",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A TOID is not interchangeable with a UPRN.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/identifier"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/feature"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/uprn"
    }
  ],
  "okfp:machineImported": false
}
---

# Topographic Identifier

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers) · reviewed 2 October 2026.

Related concept records: [feature](feature.md), [uprn](uprn.md).
