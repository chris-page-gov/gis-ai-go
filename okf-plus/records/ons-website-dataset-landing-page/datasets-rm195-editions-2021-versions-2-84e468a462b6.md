---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2FRM195%2Feditions%2F2021%2Fversions%2F2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of households in houses in multiple occupation (HMO) by type of occupancy rating (bedrooms)",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/RM195/editions/2021/versions/2",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/RM195/editions/2021/versions/2",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "dwelling_hmo_unrelated,occupancy_rating_bedrooms_5a",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/525",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2525",
      "normalisedRecordSha256": "ef2a136cc1eb4ae716c6dc8ad36c700634bbe6c58869cedb405f832ad584bcbf",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/RM195/editions/2021/versions/2"
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
    "releaseVersion": "2021"
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
    "canonical_topic": "7779",
    "cdid": "",
    "dataset_id": "RM195",
    "dimensions": [
      {
        "label": "Households of multiple occupancy (HMO)",
        "name": "dwelling_hmo_unrelated",
        "raw_label": "Households of multiple occupancy (HMO) (3 categories)"
      },
      {
        "label": "Occupancy rating for bedrooms",
        "name": "occupancy_rating_bedrooms_5a",
        "raw_label": "Occupancy rating for bedrooms (5 categories)"
      }
    ],
    "edition": "2021",
    "id": "/datasets/RM195/editions/2021/versions/2",
    "keywords": [
      "ltla",
      "dwelling_hmo_unrelated,occupancy_rating_bedrooms_5a"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2023-04-28T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/RM195/editions/2021/versions/2",
    "sourceEvidence": {
      "pointer": "/items/525",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "This dataset provides Census 2021 estimates that classify households in England and Wales by number that are HMOs by occupancy rating (bedrooms). The estimates are as at Census Day, 21 March 2021.",
    "title": "Number of households in houses in multiple occupation (HMO) by type of occupancy rating (bedrooms)",
    "topics": [
      "5586"
    ],
    "type": "dataset_landing_page",
    "uri": "/datasets/RM195/editions/2021/versions/2"
  }
}
---

# Number of households in houses in multiple occupation (HMO) by type of occupancy rating (bedrooms)

ONS website catalogue metadata.

Native identifier: `/datasets/RM195/editions/2021/versions/2`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/RM195/editions/2021/versions/2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
