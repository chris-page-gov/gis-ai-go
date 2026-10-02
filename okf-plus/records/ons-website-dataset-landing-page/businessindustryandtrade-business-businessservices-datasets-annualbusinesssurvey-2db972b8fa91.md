---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fbusiness%2Fbusinessservices%2Fdatasets%2Fannualbusinesssurveyimportersandexportersregionalbreakdown",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Exporters and importers by regional breakdown (Annual Business Survey)",
  "description": "Exporters and importers of goods and services in Great Britain by region.",
  "nativeIdentifier": "/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "export",
    "import",
    "regional",
    "ABS",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/297",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1297",
      "normalisedRecordSha256": "00b2342577cd43ae6f05e8ede3ea2d36274ad0047c6cb2566d709f310920ae56",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown"
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
    "id": "/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown",
    "keywords": [
      "export",
      "import",
      "regional",
      "ABS"
    ],
    "meta_description": "Exporters and importers of goods and services in Great Britain by region.",
    "nativeIdentityField": "uri",
    "release_date": "2026-06-11T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown",
    "sourceEvidence": {
      "pointer": "/items/297",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Exporters and importers of goods and services in Great Britain by region.",
    "title": "Exporters and importers by regional breakdown (Annual Business Survey)",
    "topics": [
      "9658",
      "5132",
      "1198"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown"
  }
}
---

# Exporters and importers by regional breakdown (Annual Business Survey)

Exporters and importers of goods and services in Great Britain by region.

Native identifier: `/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/annualbusinesssurveyimportersandexportersregionalbreakdown)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
