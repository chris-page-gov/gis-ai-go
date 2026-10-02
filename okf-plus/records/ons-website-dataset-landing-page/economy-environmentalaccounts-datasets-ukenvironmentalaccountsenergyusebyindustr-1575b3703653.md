---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fenvironmentalaccounts%2Fdatasets%2Fukenvironmentalaccountsenergyusebyindustrysourceandfuel",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Energy use: by industry, source and fuel",
  "description": "The UK's energy use by industry (SIC 2007 group - around 130 categories), source (for example, industrial and domestic combustion, aircraft, road transport and so on - around 80 categories) and fuel (for example, anthracite, peat, natural gas and so on - around 20 categories), 1990 to 2024.",
  "nativeIdentifier": "/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "environment",
    "pollution",
    "ghg",
    "emissions",
    "climate",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/124",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1124",
      "normalisedRecordSha256": "88a3a906e1105e1f5a90c3c60dbe5d89b179bea738d20ce7b04f8229ef3c6341",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel"
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
    "id": "/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel",
    "keywords": [
      "environment",
      "pollution",
      "ghg",
      "emissions",
      "climate"
    ],
    "meta_description": "The UK's energy use by industry (SIC 2007 group - around 130 categories), source (for example, industrial and domestic combustion, aircraft, road transport and so on - around 80 categories) and fuel (for example, anthracite, peat, natural gas and so on - around 20 categories), 1990 to 2024.",
    "nativeIdentityField": "uri",
    "release_date": "2026-06-04T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel",
    "sourceEvidence": {
      "pointer": "/items/124",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "The UK's energy use by industry (SIC 2007 group - around 130 categories), source (for example, industrial and domestic combustion, aircraft, road transport and so on - around 80 categories) and fuel (for example, anthracite, peat, natural gas and so on - around 20 categories), 1990 to 2024.",
    "title": "Energy use: by industry, source and fuel",
    "topics": [
      "1245",
      "3322"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel"
  }
}
---

# Energy use: by industry, source and fuel

The UK's energy use by industry (SIC 2007 group - around 130 categories), source (for example, industrial and domestic combustion, aircraft, road transport and so on - around 80 categories) and fuel (for example, anthracite, peat, natural gas and so on - around 20 categories), 1990 to 2024.

Native identifier: `/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsenergyusebyindustrysourceandfuel)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
