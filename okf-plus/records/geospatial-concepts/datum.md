---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/datum",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Geodetic datum",
  "description": "Parameters connecting a coordinate system with its reference object.",
  "nativeIdentifier": "datum",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "geospatial representation",
    "Geodetic datum",
    "datum"
  ],
  "sources": [
    {
      "resource": "https://docs.ogc.org/is/22-047r1/22-047r1.html",
      "evidenceKind": "official-reference",
      "referenceTitle": "OGC GeoSPARQL 1.1",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    },
    {
      "resource": "https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS guide to coordinate systems in Great Britain",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    },
    {
      "resource": "https://www.ordnancesurvey.co.uk/geodesy-positioning/coordinate-transformations",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS coordinate transformations",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.ogc.org/is/22-047r1/22-047r1.html"
    },
    {
      "@id": "https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf"
    },
    {
      "@id": "https://www.ordnancesurvey.co.uk/geodesy-positioning/coordinate-transformations"
    }
  ],
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
    "scopeBoundary": "Preserve datum when transforming coordinates.",
    "topic": "geospatial representation",
    "mappingInterpretation": "No direct external ontology term is asserted. The source-reviewed definition and internal concept relationships are retained without a guessed mapping.",
    "reviewedOn": "2026-10-02",
    "learningGlossary": {
      "termId": "datum",
      "definition": "A reference that connects a coordinate system to the Earth.",
      "scopeNote": "Keep geodetic and height datums separate; neither is merely a map projection.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "skos:prefLabel": {
    "@value": "Geodetic datum",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Preserve datum when transforming coordinates.",
    "@language": "en-GB"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-transformation"
    }
  ],
  "okfp:machineImported": false
}
---

# Geodetic datum

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.ogc.org/is/22-047r1/22-047r1.html) · reviewed 2 October 2026.

Related concept records: [coordinate transformation](coordinate-transformation.md).

## Learning terms and search forms

A reference that connects a coordinate system to the Earth.

Keep geodetic and height datums separate; neither is merely a map projection.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS guide to coordinate systems in Great Britain](https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf) · [OS coordinate transformations](https://www.ordnancesurvey.co.uk/geodesy-positioning/coordinate-transformations)
