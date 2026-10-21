---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/la",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Local authority",
  "description": "A local-government organisation; its administrative area is a separate geographic object.",
  "nativeIdentifier": "la",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Local authority"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS administrative geographies",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography"
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
      "termId": "la",
      "definition": "A local-government organisation; its administrative area is a separate geographic object.",
      "scopeNote": "The local-government structure and relevant tier depend on nation and date. A council and a local authority district are not interchangeable identities.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Local authority",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "The local-government structure and relevant tier depend on nation and date. A council and a local authority district are not interchangeable identities.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/la/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "LA"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/la/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "council",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "LA"
    }
  ]
}
---

# Local authority

A local-government organisation; its administrative area is a separate geographic object.

The local-government structure and relevant tier depend on nation and date. A council and a local authority district are not interchangeable identities.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[ONS administrative geographies](https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography)

Source-stated forms: LA (abbreviation; language unknown).

Project search variants: council (search-variant; language en-GB).
