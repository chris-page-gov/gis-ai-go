---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/vocabulary-learning/epoch",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Epoch",
  "description": "A time reference whose meaning depends on the source system.",
  "nativeIdentifier": "epoch",
  "sourceFamily": "vocabulary-learning",
  "resource": "https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go authored vocabulary research"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "learning vocabulary",
    "Epoch"
  ],
  "sources": [
    {
      "resource": "https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS guide to coordinate systems in Great Britain",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    },
    {
      "resource": "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/release-notes/addressbase-products-november-2025-epoch-123",
      "evidenceKind": "official-reference",
      "referenceTitle": "AddressBase products November 2025 – Epoch 123",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/release-notes/addressbase-products-november-2025-epoch-123"
    },
    {
      "@id": "https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf"
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
      "termId": "epoch",
      "definition": "A time reference whose meaning depends on the source system.",
      "scopeNote": "A geodetic reference epoch and an AddressBase numbered release epoch are different roles. Never merge them merely because the word matches.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "okfp:machineImported": false,
  "skos:prefLabel": {
    "@value": "Epoch",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A geodetic reference epoch and an AddressBase numbered release epoch are different roles. Never merge them merely because the word matches.",
    "@language": "en-GB"
  }
}
---

# Epoch

A time reference whose meaning depends on the source system.

A geodetic reference epoch and an AddressBase numbered release epoch are different roles. Never merge them merely because the word matches.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS guide to coordinate systems in Great Britain](https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf) · [AddressBase products November 2025 – Epoch 123](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/release-notes/addressbase-products-november-2025-epoch-123)
