---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ngd",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "OS National Geographic Database",
  "description": "OS data organised into themes, collections and feature types.",
  "nativeIdentifier": "ngd",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "OS National Geographic Database"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd/code-lists/code-lists-overview",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD code lists overview",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
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
      "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
    },
    {
      "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
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
      "termId": "ngd",
      "definition": "OS data organised into themes, collections and feature types.",
      "scopeNote": "Feature type, schema version, collection and data release are separate identifiers.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "OS National Geographic Database",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Feature type, schema version, collection and data release are separate identifiers.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ngd/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "NGD"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
        },
        {
          "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ngd/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "OS NGD",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
        },
        {
          "@id": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "NGD"
    }
  ]
}
---

# OS National Geographic Database

OS data organised into themes, collections and feature types.

Feature type, schema version, collection and data release are separate identifiers.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD code lists overview](https://docs.os.uk/osngd/code-lists/code-lists-overview) · [OS NGD unique identifiers](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers)

Source-stated forms: NGD (abbreviation; language unknown).

Project search variants: OS NGD (search-variant; language en-GB).
