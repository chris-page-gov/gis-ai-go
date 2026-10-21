---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/msoa",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Middle layer Super Output Area",
  "description": "A statistical geography made from groups of Lower layer Super Output Areas in England and Wales.",
  "nativeIdentifier": "msoa",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Middle layer Super Output Area"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS Census 2021 geographies",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies"
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
      "termId": "msoa",
      "definition": "A statistical geography made from groups of Lower layer Super Output Areas in England and Wales.",
      "scopeNote": "A hierarchy join needs the matching published lookup and vintage.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Middle layer Super Output Area",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A hierarchy join needs the matching published lookup and vintage.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/msoa/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "MSOA"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/msoa/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "Middle-layer Super Output Area",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "MSOA"
    }
  ]
}
---

# Middle layer Super Output Area

A statistical geography made from groups of Lower layer Super Output Areas in England and Wales.

A hierarchy join needs the matching published lookup and vintage.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[ONS Census 2021 geographies](https://www.ons.gov.uk/methodology/geography/ukgeographies/censusgeographies/census2021geographies)

Source-stated forms: MSOA (abbreviation; language unknown).

Project search variants: Middle-layer Super Output Area (search-variant; language en-GB).
