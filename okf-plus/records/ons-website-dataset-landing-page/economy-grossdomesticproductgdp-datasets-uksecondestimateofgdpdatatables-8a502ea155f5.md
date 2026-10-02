---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossdomesticproductgdp%2Fdatasets%2Fuksecondestimateofgdpdatatables",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GDP – data tables",
  "description": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "national accounts",
    "GVA",
    "economy",
    "output",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/392",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1392",
      "normalisedRecordSha256": "163a0c352f00bde67ccd516f02c0590dae42dc7dac87783c443b3ccbd4a22409",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
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
    "releaseVersion": ""
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Website and API representations are retained separately; matching titles do not prove equivalence.",
    "Release dates do not establish the period covered by statistical observations."
  ],
  "details": {
    "canonical_topic": "",
    "cdid": "",
    "dataset_id": "",
    "edition": "",
    "id": "/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables",
    "keywords": [
      "national accounts",
      "GVA",
      "economy",
      "output"
    ],
    "meta_description": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-29T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables",
    "sourceEvidence": {
      "pointer": "/items/392",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
    "title": "GDP – data tables",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables"
  }
}
---

# GDP – data tables

Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.

Native identifier: `/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
