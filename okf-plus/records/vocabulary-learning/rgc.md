---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/rgc",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Register of Geographic Codes",
  "description": "An ONS published register of geography codes.",
  "nativeIdentifier": "rgc",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://geoportal.statistics.gov.uk/",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Register of Geographic Codes"
  ],
  "sources": [
    {
      "resource": "https://geoportal.statistics.gov.uk/",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS Open Geography Portal",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    },
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS names, codes and lookups",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://geoportal.statistics.gov.uk/"
    },
    {
      "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups"
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
      "termId": "rgc",
      "definition": "An ONS published register of geography codes.",
      "scopeNote": "Use the selected edition and documented entity/instance fields. This glossary does not enumerate the register or infer a code’s current validity.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Register of Geographic Codes",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "Use the selected edition and documented entity/instance fields. This glossary does not enumerate the register or infer a code’s current validity.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/rgc/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "RGC"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://geoportal.statistics.gov.uk/"
        },
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "RGC"
    }
  ]
}
---

# Register of Geographic Codes

An ONS published register of geography codes.

Use the selected edition and documented entity/instance fields. This glossary does not enumerate the register or infer a code’s current validity.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[ONS Open Geography Portal](https://geoportal.statistics.gov.uk/) · [ONS names, codes and lookups](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups)

Source-stated forms: RGC (abbreviation; language unknown).
