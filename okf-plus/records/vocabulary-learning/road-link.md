---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Road Link",
  "description": "A linear feature representing a section of a road network between network points.",
  "nativeIdentifier": "road-link",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Road Link"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD Road Link",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    },
    {
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS Linked Identifiers API technical specification",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification"
    },
    {
      "@id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link"
    }
  ],
  "temporal": {
    "status": "not-applicable",
    "kind": "concept-record",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Concept explanation, not a dataset reference period."
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
    "metadata": "Authored factual explanation with public source citations; source rights retained.",
    "describedData": "No data licence or entitlement established.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Scoped project glossary; not complete geospatial vocabulary coverage.",
    "Source review is not independent semantic acceptance or provider conformance."
  ],
  "details": {
    "learningGlossary": {
      "termId": "road-link",
      "definition": "A linear feature representing a section of a road network between network points.",
      "scopeNote": "Read the feature schema and network references; a line on a map alone does not prove routability.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Road Link",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Read the feature schema and network references; a line on a map alone does not prove routability.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/road-link/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "RoadLink"
      },
      "okfp:formKind": "native-type-form",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link"
        },
        {
          "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification"
        }
      ]
    }
  ]
}
---

# Road Link

A linear feature representing a section of a road network between network points.

Read the feature schema and network references; a line on a map alone does not prove routability.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD Road Link](https://docs.os.uk/osngd/data-structure/transport/transport-network/road-link) · [OS Linked Identifiers API technical specification](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification)

Source-stated forms: RoadLink (native-type-form; language unknown).
