---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/os-ngd-downloads",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "OS NGD Select+Build and nine theme documentation",
  "description": "All indexed NGD documentation pages are captured with bounded structural projections. Download feature types and code lists extend beyond the API collection surface; full field semantics and controlled-value coverage remain unproved.",
  "nativeIdentifier": "os-ngd-downloads",
  "sourceFamily": "source-families",
  "resource": "https://docs.os.uk/osngd",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-review-recorded",
  "tags": [
    "os",
    "catalogue",
    "coverage",
    "updates"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/osngd",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/osngd"
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
      "https://docs.os.uk/osngd/os-ngd-news/change-log"
    ],
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
    "Source-family coverage status is separate from product count, schema coverage, semantic curation and live Ask OKF admission.",
    "All 478 indexed pages were captured; six bounded structural projections are truncated.",
    "Captured code-list pages do not establish a complete normalised vocabulary, field semantics or current feature conformance."
  ],
  "details": {
    "inventoryStatus": "captured-indexed-pages-structural-projection",
    "sourceLane": "os-ngd-downloads",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "osngd-documentation",
      "osngd-documentation-pages"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ordnancesurvey.co.uk/"
  },
  "okfp:machineImported": false
}
---

# OS NGD Select+Build and nine theme documentation

All indexed NGD documentation pages are captured with bounded structural projections. Download feature types and code lists extend beyond the API collection surface; full field semantics and controlled-value coverage remain unproved.

Inventory state: `captured-indexed-pages-structural-projection`.

[Official source](https://docs.os.uk/osngd)

[Update and release discovery](https://docs.os.uk/osngd/os-ngd-news/change-log)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.

The captured navigation cohort contains 478 distinct URLs; all 478 pages returned successfully and have structural projections. This closes page acquisition against that frozen index, not all NGD schema semantics or controlled values. Six page projections are explicitly truncated. The public projection retains table shapes and selected native labels; it does not yet provide a complete normalised code-list/value inventory. The nine documented themes and the versioned live API collection catalogue remain different denominators.
