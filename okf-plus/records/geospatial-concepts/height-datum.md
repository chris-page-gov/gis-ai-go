---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Height datum",
  "description": "The reference used to interpret vertical coordinates or heights.",
  "nativeIdentifier": "height-datum",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "reference systems",
    "Height datum",
    "height-datum"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS coordinate systems guide",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems"
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
    "scopeBoundary": "Ellipsoidal and national height references differ.",
    "topic": "reference systems",
    "mappingInterpretation": "No direct external ontology term is asserted. The source-reviewed definition and internal concept relationships are retained without a guessed mapping.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Height datum",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Ellipsoidal and national height references differ.",
    "@language": "en-GB"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/british-national-grid"
    }
  ],
  "okfp:machineImported": false
}
---

# Height datum

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/more-than-maps/a-guide-to-coordinate-systems-in-great-britain/ordnance-survey-coordinate-systems) · reviewed 2 October 2026.

Related concept records: [british national grid](british-national-grid.md).
