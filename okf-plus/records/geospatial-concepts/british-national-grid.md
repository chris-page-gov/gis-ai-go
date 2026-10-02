---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/british-national-grid",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "British National Grid",
  "description": "The projected British mapping reference system identified by EPSG:27700 in OS NGD guidance.",
  "nativeIdentifier": "british-national-grid",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "reference systems",
    "British National Grid",
    "british-national-grid"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD coordinate reference systems",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems"
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
    "scopeBoundary": "Record horizontal and vertical references separately.",
    "topic": "reference systems",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02"
  },
  "skos:prefLabel": {
    "@value": "British National Grid",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Record horizontal and vertical references separately.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://www.opengis.net/def/crs/EPSG/0/27700"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/height-datum"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/coordinate-reference-system"
    }
  ],
  "okfp:machineImported": false
}
---

# British National Grid

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/coordinate-reference-systems) · reviewed 2 October 2026.

Related concept records: [height datum](height-datum.md), [coordinate reference system](coordinate-reference-system.md).
