---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2FRM202%2Feditions%2F2021%2Fversions%2F1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Household size by number of rooms",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/RM202/editions/2021/versions/1",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/RM202/editions/2021/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "voa_number_of_rooms_6a,hh_size_5a",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/739",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1739",
      "normalisedRecordSha256": "7681a347fadfaf3cb3016754a9bf644d34f3c4740ef8d348f1500102bfa76d8b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/RM202/editions/2021/versions/1"
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
    "dataset_id": "RM202",
    "dimensions": [
      {
        "label": "Number of rooms (Valuation Office Agency)",
        "name": "voa_number_of_rooms_6a",
        "raw_label": "Number of rooms (Valuation Office Agency) (6 categories)"
      },
      {
        "label": "Household size",
        "name": "hh_size_5a",
        "raw_label": "Household size (5 categories)"
      }
    ],
    "edition": "2021",
    "id": "/datasets/RM202/editions/2021/versions/1",
    "keywords": [
      "ltla",
      "voa_number_of_rooms_6a,hh_size_5a"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2023-03-28T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/RM202/editions/2021/versions/1",
    "sourceEvidence": {
      "pointer": "/items/739",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "This dataset provides Census 2021 estimates that classify households in England and Wales by household size and by number of rooms. The estimates are as at Census Day, 21 March 2021.",
    "title": "Household size by number of rooms",
    "topics": [
      "4128"
    ],
    "type": "dataset_landing_page",
    "uri": "/datasets/RM202/editions/2021/versions/1"
  }
}
---

# Household size by number of rooms

ONS website catalogue metadata.

Native identifier: `/datasets/RM202/editions/2021/versions/1`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/RM202/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
