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
    },
    {
      "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD unique identifiers",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
    },
    {
      "@id": "https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers"
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
    "scopeBoundary": "A TOID is not interchangeable with a UPRN.",
    "topic": "UK identifiers",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02",
    "learningGlossary": {
      "termId": "toid",
      "definition": "An OS feature identifier also supplied as an optional secondary identifier in much of NGD.",
      "scopeNote": "Its presence is not guaranteed on every NGD feature. A TOID lookup needs an identified feature type and source version.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
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
  "okfp:machineImported": false,
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/toid/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "TOID"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/toid/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "toid"
      },
      "okfp:formKind": "native-field-form",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "TOID"
    }
  ]
}
---

# Topographic Identifier

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers) · reviewed 2 October 2026.

Related concept records: [feature](feature.md), [uprn](uprn.md).

## Learning terms and search forms

An OS feature identifier also supplied as an optional secondary identifier in much of NGD.

Its presence is not guaranteed on every NGD feature. A TOID lookup needs an identified feature type and source version.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD unique identifiers](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers)

Source-stated forms: TOID (abbreviation; language unknown); toid (native-field-form; language unknown).
