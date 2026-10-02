---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/postcode-allocation",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Postcode point allocation",
  "description": "Assignment using a postcode representative point within a geographic boundary.",
  "nativeIdentifier": "postcode-allocation",
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
    "Postcode point allocation",
    "postcode-allocation"
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
    "scopeBoundary": "It does not locate every address separately.",
    "topic": "UK geography",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "Postcode point allocation",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "It does not locate every address separately.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/ont/geosparql#sfWithin"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/point"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/onspd"
    }
  ],
  "okfp:machineImported": false
}
---

# Postcode point allocation

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts) · reviewed 2 October 2026.

Related concept records: [point](point.md), [onspd](onspd.md).
