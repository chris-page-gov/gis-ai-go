---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/ons-classifications",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "ONS statistical classifications and standards",
  "description": "SIC, SOC, NS-SEC and correspondence tables have distinct versions and adoption schedules; preserve the version actually used by each dataset.",
  "nativeIdentifier": "ons-classifications",
  "sourceFamily": "source-families",
  "resource": "https://www.ons.gov.uk/methodology/classificationsandstandards",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-review-recorded",
  "tags": [
    "ons",
    "catalogue",
    "coverage",
    "updates"
  ],
  "sources": [
    {
      "resource": "https://www.ons.gov.uk/methodology/classificationsandstandards",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/methodology/classificationsandstandards"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "dataset-reference-period",
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
    "releaseCatalogue": [
      "https://www.ons.gov.uk/methodology/classificationsandstandards"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
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
    "Source-family coverage status is separate from product count, schema coverage, semantic curation and live Ask OKF admission."
  ],
  "details": {
    "inventoryStatus": "reviewed-reference-unenumerated",
    "sourceLane": "ons-classifications",
    "globalDenominator": "not-established"
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  },
  "okfp:machineImported": false
}
---

# ONS statistical classifications and standards

SIC, SOC, NS-SEC and correspondence tables have distinct versions and adoption schedules; preserve the version actually used by each dataset.

Inventory state: `reviewed-reference-unenumerated`.

[Official source](https://www.ons.gov.uk/methodology/classificationsandstandards)

[Update and release discovery](https://www.ons.gov.uk/methodology/classificationsandstandards)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.
