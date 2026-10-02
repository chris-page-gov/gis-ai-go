---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fenvironmentalaccounts%2Fdatasets%2Fmaterialconsumptionintheunitedkingdom2000to2013",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Material consumption in the UK",
  "description": "Domestic extraction, imports and exports, domestic material consumption, raw material consumption and resource productivity from the material flow accounts, 2000 to 2013.",
  "nativeIdentifier": "/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "resource efficiency",
    "environmental accounts",
    "biomass",
    "ores",
    "minerals",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/230",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2230",
      "normalisedRecordSha256": "bfcc9ad62d23373bef3b2eecdfb744afbbf610e7a44110a3ab345e16d4ee8bef",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013"
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
    "id": "/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013",
    "keywords": [
      "resource efficiency",
      "environmental accounts",
      "biomass",
      "ores",
      "minerals"
    ],
    "meta_description": "Domestic extraction, imports and exports, domestic material consumption, raw material consumption and resource productivity from the material flow accounts, 2000 to 2013.",
    "nativeIdentityField": "uri",
    "release_date": "2016-02-29T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013",
    "sourceEvidence": {
      "pointer": "/items/230",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Domestic extraction, imports and exports, domestic material consumption, raw material consumption and resource productivity from the material flow accounts, 2000 to 2013.",
    "title": "Material consumption in the UK",
    "topics": [
      "1245",
      "3322"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013"
  }
}
---

# Material consumption in the UK

Domestic extraction, imports and exports, domestic material consumption, raw material consumption and resource productivity from the material flow accounts, 2000 to 2013.

Native identifier: `/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/environmentalaccounts/datasets/materialconsumptionintheunitedkingdom2000to2013)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
