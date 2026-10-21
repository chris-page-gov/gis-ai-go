---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/nsul",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "National Statistics UPRN Lookup",
  "description": "A lookup allocating source UPRNs to Output Areas and higher statistical geographies by best fit.",
  "nativeIdentifier": "nsul",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "National Statistics UPRN Lookup"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts",
      "evidenceKind": "official-reference",
      "referenceTitle": "ONS National Statistics UPRN Products",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts"
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
      "termId": "nsul",
      "definition": "A lookup allocating source UPRNs to Output Areas and higher statistical geographies by best fit.",
      "scopeNote": "The higher-area assignment is an OA-based statistical method, not necessarily direct point-in-polygon membership. Check the edition and lifecycle scope; this explanation does not establish counts of current or terminated properties in a retained selection.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "National Statistics UPRN Lookup",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "The higher-area assignment is an OA-based statistical method, not necessarily direct point-in-polygon membership. Check the edition and lifecycle scope; this explanation does not establish counts of current or terminated properties in a retained selection.",
    "@language": "en-GB"
  },
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/nsul/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "NSUL"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "NSUL"
    }
  ]
}
---

# National Statistics UPRN Lookup

A lookup allocating source UPRNs to Output Areas and higher statistical geographies by best fit.

The higher-area assignment is an OA-based statistical method, not necessarily direct point-in-polygon membership. Check the edition and lifecycle scope; this explanation does not establish counts of current or terminated properties in a retained selection.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[ONS National Statistics UPRN Products](https://www.ons.gov.uk/methodology/geography/geographicalproducts/nationalstatisticsaddressproducts)

Source-stated forms: NSUL (abbreviation; language unknown).
