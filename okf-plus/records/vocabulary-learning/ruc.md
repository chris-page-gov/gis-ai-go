---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ruc",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Rural Urban Classification",
  "description": "A statistical classification of areas by settlement and accessibility characteristics.",
  "nativeIdentifier": "ruc",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Rural Urban Classification"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS 2021 Rural Urban Classification",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    },
    {
      "resource": "https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/",
      "evidenceKind": "official-reference",
      "referenceTitle": "Scottish Government Urban Rural Classification 2022",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    },
    {
      "resource": "https://www.nisra.gov.uk/support/geography/urban-rural-classification",
      "evidenceKind": "official-reference",
      "referenceTitle": "NISRA Urban – Rural Classification",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-page-opened-text-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/"
    },
    {
      "@id": "https://www.nisra.gov.uk/support/geography/urban-rural-classification"
    },
    {
      "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification"
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
      "termId": "ruc",
      "definition": "A statistical classification of areas by settlement and accessibility characteristics.",
      "scopeNote": "England/Wales, Scotland and Northern Ireland use distinct products, editions and geographic units. Codes and labels are not shared aliases across these schemes.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Rural Urban Classification",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "England/Wales, Scotland and Northern Ireland use distinct products, editions and geographic units. Codes and labels are not shared aliases across these schemes.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ruc/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "RUC"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification"
        },
        {
          "@id": "https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/"
        },
        {
          "@id": "https://www.nisra.gov.uk/support/geography/urban-rural-classification"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/ruc/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "rural–urban classification",
        "@language": "en-GB"
      },
      "okfp:formKind": "search-variant",
      "okfp:authority": "project-search-variant",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification"
        },
        {
          "@id": "https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/"
        },
        {
          "@id": "https://www.nisra.gov.uk/support/geography/urban-rural-classification"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "RUC"
    }
  ]
}
---

# Rural Urban Classification

A statistical classification of areas by settlement and accessibility characteristics.

England/Wales, Scotland and Northern Ireland use distinct products, editions and geographic units. Codes and labels are not shared aliases across these schemes.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[ONS 2021 Rural Urban Classification](https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification) · [Scottish Government Urban Rural Classification 2022](https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/) · [NISRA Urban – Rural Classification](https://www.nisra.gov.uk/support/geography/urban-rural-classification)

Source-stated forms: RUC (abbreviation; language unknown).

Project search variants: rural–urban classification (search-variant; language en-GB).
