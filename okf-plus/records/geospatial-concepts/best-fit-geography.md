---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/best-fit-geography",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Best-fit geography lookup",
  "description": "An allocation associating source areas with target geographies using a specified fitting methodology.",
  "nativeIdentifier": "best-fit-geography",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK geography",
    "Best-fit geography lookup",
    "best-fit-geography"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS postcode products",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts"
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
    "scopeBoundary": "Best fit need not preserve exact boundary containment.",
    "topic": "UK geography",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Best-fit geography lookup",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Best fit need not preserve exact boundary containment.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/relation"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/nspl"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/geography-vintage"
    }
  ],
  "okfp:machineImported": false
}
---

# Best-fit geography lookup

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts) · reviewed 2 October 2026.

Related concept records: [nspl](nspl.md), [geography vintage](geography-vintage.md).
