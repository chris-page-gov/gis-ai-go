---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/lexical-alias",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Search variant",
  "description": "An alternative text form used to help find an existing term.",
  "nativeIdentifier": "lexical-alias",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Search variant"
  ],
  "sources": [
    {
      "resource": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/",
      "evidenceKind": "official-reference",
      "referenceTitle": "SKOS reference, 18 August 2009",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    },
    {
      "resource": "https://github.com/chris-page-gov/gis-ai-go/blob/d7fa5048bccecd0be7e630f96a2f378721aa5b91/docs/implementation/OKF-220_ASK_OKF_INTEGRATION.md",
      "evidenceKind": "project-method-reference",
      "referenceTitle": "GIS AI GO OKF-220 context integration, inspected commit",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "local-pinned-project-file-read"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://github.com/chris-page-gov/gis-ai-go/blob/d7fa5048bccecd0be7e630f96a2f378721aa5b91/docs/implementation/OKF-220_ASK_OKF_INTEGRATION.md"
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
      "termId": "lexical-alias",
      "definition": "An alternative text form used to help find an existing term.",
      "scopeNote": "A search match is not an identity assertion. Project variants are labelled as such and never generate equivalence.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Search variant",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A search match is not an identity assertion. Project variants are labelled as such and never generate equivalence.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/lexical-alias/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "alias",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/"
        },
        {
          "@id": "https://github.com/chris-page-gov/gis-ai-go/blob/d7fa5048bccecd0be7e630f96a2f378721aa5b91/docs/implementation/OKF-220_ASK_OKF_INTEGRATION.md"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/lexical-alias/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "synonym",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.w3.org/TR/2009/REC-skos-reference-20090818/"
        },
        {
          "@id": "https://github.com/chris-page-gov/gis-ai-go/blob/d7fa5048bccecd0be7e630f96a2f378721aa5b91/docs/implementation/OKF-220_ASK_OKF_INTEGRATION.md"
        }
      ]
    }
  ]
}
---

# Search variant

An alternative text form used to help find an existing term.

A search match is not an identity assertion. Project variants are labelled as such and never generate equivalence.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[SKOS reference, 18 August 2009](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) · [GIS AI GO OKF-220 context integration, inspected commit](https://github.com/chris-page-gov/gis-ai-go/blob/d7fa5048bccecd0be7e630f96a2f378721aa5b91/docs/implementation/OKF-220_ASK_OKF_INTEGRATION.md)

Project search variants: alias (search-variant; language en-GB); synonym (search-variant; language en-GB).
