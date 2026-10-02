---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-transformation",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Coordinate transformation",
  "description": "A defined operation converting coordinates between reference systems, such as the OSTN15 transformation.",
  "nativeIdentifier": "coordinate-transformation",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/coordinate-reference-systems",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "reference systems",
    "Coordinate transformation",
    "coordinate-transformation"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/coordinate-reference-systems",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS cartographic coordinate reference guidance",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/coordinate-reference-systems"
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
    "scopeBoundary": "Changing a CRS label does not transform coordinates.",
    "topic": "reference systems",
    "mappingInterpretation": "No direct external ontology term is asserted. The source-reviewed definition and internal concept relationships are retained without a guessed mapping.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Coordinate transformation",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Changing a CRS label does not transform coordinates.",
    "@language": "en-GB"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/datum"
    }
  ],
  "okfp:machineImported": false
}
---

# Coordinate transformation

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/coordinate-reference-systems) · reviewed 2 October 2026.

Related concept records: [coordinate reference system](coordinate-reference-system.md), [datum](datum.md).
