---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fbusiness%2Fbusinessservices%2Fdatasets%2Fproportionofproductgroupintermediateconsumptionbyindustrygroup",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Proportion of product group intermediate consumption by industry group",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "sector",
    "SUT",
    "proportion",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/882",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2882",
      "normalisedRecordSha256": "8480ff7ec140aee60d037f70379e04d8d7f4c0a2f455ca75fc06333f36bd3f9c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup"
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
    "id": "/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup",
    "keywords": [
      "sector",
      "SUT",
      "proportion"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2018-07-25T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup",
    "sourceEvidence": {
      "pointer": "/items/882",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "High level table of Intermediate consumption by industry group",
    "title": "Proportion of product group intermediate consumption by industry group",
    "topics": [
      "9658",
      "5132",
      "1198"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup"
  }
}
---

# Proportion of product group intermediate consumption by industry group

ONS website catalogue metadata.

Native identifier: `/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/proportionofproductgroupintermediateconsumptionbyindustrygroup)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
