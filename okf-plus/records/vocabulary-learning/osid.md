---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/osid",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "OS Identifier",
  "description": "The primary persistent identifier used for many OS NGD features.",
  "nativeIdentifier": "osid",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "OS Identifier"
  ],
  "sources": [
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
      "termId": "osid",
      "definition": "The primary persistent identifier used for many OS NGD features.",
      "scopeNote": "Uniqueness is at feature-type level: the same OSID may identify related representations in different feature types.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "OS Identifier",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Uniqueness is at feature-type level: the same OSID may identify related representations in different feature types.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/osid/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "OSID"
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
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/osid/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "osid"
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
      "@value": "OSID"
    }
  ]
}
---

# OS Identifier

The primary persistent identifier used for many OS NGD features.

Uniqueness is at feature-type level: the same OSID may identify related representations in different feature types.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD unique identifiers](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/unique-identifiers)

Source-stated forms: OSID (abbreviation; language unknown); osid (native-field-form; language unknown).
