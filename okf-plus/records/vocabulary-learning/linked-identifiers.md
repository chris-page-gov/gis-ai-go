---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/linked-identifiers",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "OS Linked Identifiers",
  "description": "An OS service and product family describing typed relationships between identifiers.",
  "nativeIdentifier": "linked-identifiers",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "OS Linked Identifiers"
  ],
  "sources": [
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
      "termId": "linked-identifiers",
      "definition": "An OS service and product family describing typed relationships between identifiers.",
      "scopeNote": "A correlation is not identity, containment or a claim that an address is a building. Preserve method, direction, source and target versions.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "OS Linked Identifiers",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A correlation is not identity, containment or a claim that an address is a building. Preserve method, direction, source and target versions.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/linked-identifiers/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "linked IDs",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/linked-identifiers/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "identifier links",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification"
        }
      ]
    }
  ]
}
---

# OS Linked Identifiers

An OS service and product family describing typed relationships between identifiers.

A correlation is not identity, containment or a claim that an address is a building. Preserve method, direction, source and target versions.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS Linked Identifiers API technical specification](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification)

Project search variants: linked IDs (search-variant; language en-GB); identifier links (search-variant; language en-GB).
