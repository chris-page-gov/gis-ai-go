---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/usrn",
  "@type": [
    "skos:Concept",
    "okfp:MetadataRecord"
  ],
  "type": "Concept",
  "title": "Unique Street Reference Number",
  "description": "A numerical identifier for a street in Great Britain.",
  "nativeIdentifier": "usrn",
  "sourceFamily": "geospatial-concepts",
  "resource": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-reviewed",
  "tags": [
    "UK identifiers",
    "Unique Street Reference Number",
    "usrn"
  ],
  "sources": [
    {
      "resource": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information",
      "evidenceKind": "official-reference",
      "referenceTitle": "Government property and street identifier standard",
      "reviewedOn": "2026-10-02",
      "reviewMethod": "agent-read-primary-source"
    },
    {
      "resource": "https://docs.os.uk/osngd/data-structure/address",
      "evidenceKind": "official-reference",
      "referenceTitle": "OS NGD Address theme",
      "reviewedOn": "2026-10-21",
      "reviewMethod": "official-search-result-extract-reviewed"
    }
  ],
  "prov:wasDerivedFrom": [
    {
      "@id": "https://docs.os.uk/osngd/data-structure/address"
    },
    {
      "@id": "https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information"
    }
  ],
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "concept-record",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
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
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "The concept scheme is extensible and does not claim exhaustive geospatial coverage.",
    "Agent source review is not independent human acceptance."
  ],
  "details": {
    "scopeBoundary": "A simplified street line is not its complete physical extent.",
    "topic": "UK identifiers",
    "mappingInterpretation": "Associative link to a standard term; no identity or conformance claim.",
    "reviewedOn": "2026-10-02",
    "learningGlossary": {
      "termId": "usrn",
      "definition": "A persistent identifier for a street curated by local-authority custodians.",
      "scopeNote": "A street record is not the same object as a Road Link or Path Link.",
      "definitionAuthority": "project-paraphrase",
      "reviewedOn": "2026-10-21",
      "currentSchemeCoverageComplete": false
    }
  },
  "skos:prefLabel": {
    "@value": "Unique Street Reference Number",
    "@language": "en-GB"
  },
  "skos:scopeNote": {
    "@value": "A simplified street line is not its complete physical extent.",
    "@language": "en-GB"
  },
  "skos:relatedMatch": {
    "@id": "http://purl.org/dc/terms/identifier"
  },
  "skos:related": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/uprn"
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/line-string"
    }
  ],
  "okfp:machineImported": false,
  "okfp:lexicalForm": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/usrn/lexical-form/1",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "USRN"
      },
      "okfp:formKind": "abbreviation",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/data-structure/address"
        }
      ]
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/geospatial-concepts/usrn/lexical-form/2",
      "@type": "okfp:LexicalForm",
      "rdf:value": {
        "@value": "usrn"
      },
      "okfp:formKind": "native-field-form",
      "okfp:authority": "source-stated",
      "prov:wasDerivedFrom": [
        {
          "@id": "https://docs.os.uk/osngd/data-structure/address"
        }
      ]
    }
  ],
  "skos:altLabel": [
    {
      "@value": "USRN"
    }
  ]
}
---

# Unique Street Reference Number

The definition and interpretation boundary are in the inspectable front matter.

[Official reference](https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information) · reviewed 2 October 2026.

Related concept records: [uprn](uprn.md), [line string](line-string.md).

## Learning terms and search forms

A persistent identifier for a street curated by local-authority custodians.

A street record is not the same object as a Road Link or Path Link.

Definitions are project paraphrases. Native forms, source abbreviations and project search variants retain separate authority. No equivalence is inferred.

[OS NGD Address theme](https://docs.os.uk/osngd/data-structure/address)

Source-stated forms: USRN (abbreviation; language unknown); usrn (native-field-form; language unknown).
