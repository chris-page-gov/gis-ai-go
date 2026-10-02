---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/ons-releases",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "ONS release catalogue and feeds",
  "description": "Publication events include announced, published, revised, cancelled and postponed releases. RSS is a recent change signal; historical coverage requires an explicit calendar interval.",
  "nativeIdentifier": "ons-releases",
  "sourceFamily": "source-families",
  "resource": "https://developer.ons.gov.uk/search/search-releases/",
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
      "resource": "https://developer.ons.gov.uk/search/search-releases/",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://developer.ons.gov.uk/search/search-releases/"
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
      "https://www.ons.gov.uk/releasecalendar"
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
    "inventoryStatus": "captured-explicit-2026-window",
    "sourceLane": "ons-releases",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "ons-releases-published",
      "ons-releases-upcoming",
      "ons-releases-cancelled"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ons.gov.uk/"
  },
  "okfp:machineImported": false
}
---

# ONS release catalogue and feeds

Publication events include announced, published, revised, cancelled and postponed releases. RSS is a recent change signal; historical coverage requires an explicit calendar interval.

Inventory state: `captured-explicit-2026-window`.

[Official source](https://developer.ons.gov.uk/search/search-releases/)

[Update and release discovery](https://www.ons.gov.uk/releasecalendar)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.
