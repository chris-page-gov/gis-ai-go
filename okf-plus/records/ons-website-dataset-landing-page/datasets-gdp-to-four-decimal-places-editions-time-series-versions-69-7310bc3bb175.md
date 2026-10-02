---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2Fgdp-to-four-decimal-places%2Feditions%2Ftime-series%2Fversions%2F69",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GDP monthly estimate (incorporating the Index of Services and Index of Production)",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "GDP",
    "economy",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/385",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1385",
      "normalisedRecordSha256": "b993932bad0ac9515019e7f4d2ed66331c43852b7e6a783937d08e668f1ef30b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69"
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
    "releaseVersion": "time-series"
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
    "dataset_id": "gdp-to-four-decimal-places",
    "edition": "time-series",
    "id": "/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69",
    "keywords": [
      "GDP",
      "economy"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-24T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69",
    "sourceEvidence": {
      "pointer": "/items/385",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Gross domestic product (GDP) measures the value of goods and services produced in the UK. It estimates the size of and growth in the economy. This dataset also contains the Index of Services (monthly movements in output for the services industries) and the Index of Production (movements in the volume of production for the UK production industries: manufacturing, mining and quarrying, energy supply, and water and waste management). Figures are seasonally adjusted.",
    "title": "GDP monthly estimate (incorporating the Index of Services and Index of Production)",
    "type": "dataset_landing_page",
    "uri": "/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69"
  }
}
---

# GDP monthly estimate (incorporating the Index of Services and Index of Production)

ONS website catalogue metadata.

Native identifier: `/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/gdp-to-four-decimal-places/editions/time-series/versions/69)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
