---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/exact-fit-geography",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Exact-fit geography statistics",
  "description": "Statistics allocated to the specified boundary rather than approximated using whole source areas.",
  "nativeIdentifier": "exact-fit-geography",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/methodologynoteonproductionofpopulationestimatesbyoutputareaselectoralhealthandothergeographiesenglandandwales",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK geography",
    "Exact-fit geography statistics",
    "exact-fit-geography"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/methodologynoteonproductionofpopulationestimatesbyoutputareaselectoralhealthandothergeographiesenglandandwales",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS population-estimate geography methodology",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/methodologynoteonproductionofpopulationestimatesbyoutputareaselectoralhealthandothergeographiesenglandandwales"
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
    "scopeBoundary": "Availability differs by statistical product and method.",
    "topic": "UK geography",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Exact-fit geography statistics",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Availability differs by statistical product and method.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/spatial"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/best-fit-geography"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geography-vintage"
    }
  ],
  "okfp:machineImported": false
}
---

# Exact-fit geography statistics

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/methodologynoteonproductionofpopulationestimatesbyoutputareaselectoralhealthandothergeographiesenglandandwales) · reviewed 2 October 2026.

Related concept records: [best fit geography](best-fit-geography.md), [geography vintage](geography-vintage.md).
