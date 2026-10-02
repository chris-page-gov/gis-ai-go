---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fwellbeing%2Fdatasets%2F1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of chain supermarkets across Local Authority Districts (LAD) and smaller geographical areas in the UK",
  "description": "Counts of supermarkets and counts grouped by size band and type of retailer, across various geographical areas. Geographies include Local Authority Districts (LAD) in the UK, Middle Layer Super Output Area (MSOA) in England and Wales, Intermediate Zones in Scotland, and Super Data Zones in Northern Ireland. Counts of supermarkets per 10,000 people are also provided for LAD level.",
  "nativeIdentifier": "/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "supermarkets",
    "subnational statistics",
    "access to amenities",
    "local authority districts",
    "MSOA",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/512",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2512",
      "normalisedRecordSha256": "6a253eeeb5ad898e2761ce49ab25d3c00d072b7fe3fe938c1149d0c00d7d1d4d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk"
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
    "id": "/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk",
    "keywords": [
      "supermarkets",
      "subnational statistics",
      "access to amenities",
      "local authority districts",
      "MSOA"
    ],
    "meta_description": "Counts of supermarkets and counts grouped by size band and type of retailer, across various geographical areas. Geographies include Local Authority Districts (LAD) in the UK, Middle Layer Super Output Area (MSOA) in England and Wales, Intermediate Zones in Scotland, and Super Data Zones in Northern Ireland. Counts of supermarkets per 10,000 people are also provided for LAD level.",
    "nativeIdentityField": "uri",
    "release_date": "2024-03-07T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk",
    "sourceEvidence": {
      "pointer": "/items/512",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Counts of supermarkets and counts grouped by size band and type of retailer, across various geographical areas. Geographies include Local Authority Districts (LAD) in the UK, Middle Layer Super Output Area (MSOA) in England and Wales, Intermediate Zones in Scotland, and Super Data Zones in Northern Ireland. Counts of supermarkets per 10,000 people are also provided for LAD level.",
    "title": "Number of chain supermarkets across Local Authority Districts (LAD) and smaller geographical areas in the UK",
    "topics": [
      "9581",
      "2456"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk"
  }
}
---

# Number of chain supermarkets across Local Authority Districts (LAD) and smaller geographical areas in the UK

Counts of supermarkets and counts grouped by size band and type of retailer, across various geographical areas. Geographies include Local Authority Districts (LAD) in the UK, Middle Layer Super Output Area (MSOA) in England and Wales, Intermediate Zones in Scotland, and Super Data Zones in Northern Ireland. Counts of supermarkets per 10,000 people are also provided for LAD level.

Native identifier: `/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/1numberofchainsupermarketsacrosslocalauthoritydistrictsladandsmallergeographicalareasintheuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
