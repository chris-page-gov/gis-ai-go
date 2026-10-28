---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/controlled-vocabulary",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Controlled vocabulary",
  "description": "A managed set of terms, labels or codes within a stated scheme.",
  "nativeIdentifier": "controlled-vocabulary",
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
    "Controlled vocabulary"
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
      "resource": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/",
      "evidenceKind": "official-reference",
      "referenceTitle": "SKOS reference, 18 August 2009",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
    },
    {
      "@id": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/"
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
      "termId": "controlled-vocabulary",
      "definition": "A managed set of terms, labels or codes within a stated scheme.",
      "scopeNote": "The permitted labels in one field are not automatically the permitted labels in another.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Controlled vocabulary",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "The permitted labels in one field are not automatically the permitted labels in another.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/controlled-vocabulary/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "code list",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
        },
        {
          "@id": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/controlled-vocabulary/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "codelist",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/code-lists/code-lists-overview"
        },
        {
          "@id": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/"
        }
      ]
    }
  ]
}
---

# Controlled vocabulary

A managed set of terms, labels or codes within a stated scheme.

The permitted labels in one field are not automatically the permitted labels in another.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD code lists overview](https://docs.os.uk/osngd/code-lists/code-lists-overview) · [SKOS reference, 18 August 2009](https://www.w3.org/TR/2009/REC-skos-reference-20090818/)

Project search variants: code list (search-variant; language en-GB); codelist (search-variant; language en-GB).
