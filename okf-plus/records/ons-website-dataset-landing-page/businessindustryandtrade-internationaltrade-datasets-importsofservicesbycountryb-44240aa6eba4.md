---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Finternationaltrade%2Fdatasets%2Fimportsofservicesbycountrybymodesofsupply",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Imports and exports of services by country, by modes of supply, UK",
  "description": "The table provides a breakdown of Trade in Services values by modes of supply for imports and exports. Mode 1 is remote trade, mode 2 is commercial Presence and mode 4 is presence of natural persons. Countries include only total services data by mode, while regions include top-level extended balance of payments (EBOPS) breakdown.",
  "nativeIdentifier": "/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "trade in services",
    "country",
    "imports",
    "mode",
    "EBOPS",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/815",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1815",
      "normalisedRecordSha256": "fc85560a3eac15a56ae23abfee22215fd367792aa08792b18b2fb2c705c4a8f7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply"
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
    "id": "/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply",
    "keywords": [
      "trade in services",
      "country",
      "imports",
      "mode",
      "EBOPS"
    ],
    "meta_description": "The table provides a breakdown of Trade in Services values by modes of supply for imports and exports. Mode 1 is remote trade, mode 2 is commercial Presence and mode 4 is presence of natural persons. Countries include only total services data by mode, while regions include top-level extended balance of payments (EBOPS) breakdown.",
    "nativeIdentityField": "uri",
    "release_date": "2025-12-10T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply",
    "sourceEvidence": {
      "pointer": "/items/815",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Country breakdown of trade in services values by mode of supply (imports and exports). Countries include only total services data, while regions include top-level Extended Balance of Payments Services (EBOPS) breakdown.",
    "title": "Imports and exports of services by country, by modes of supply, UK",
    "topics": [
      "9658",
      "5631"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply"
  }
}
---

# Imports and exports of services by country, by modes of supply, UK

The table provides a breakdown of Trade in Services values by modes of supply for imports and exports. Mode 1 is remote trade, mode 2 is commercial Presence and mode 4 is presence of natural persons. Countries include only total services data by mode, while regions include top-level extended balance of payments (EBOPS) breakdown.

Native identifier: `/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/importsofservicesbycountrybymodesofsupply)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
