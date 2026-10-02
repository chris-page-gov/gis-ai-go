---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Ffamilies%2Fdatasets%2Ffamiliesbyfamilytyperegionsofenglandandukconstituentcountries",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Families by family type, regions of England and UK constituent countries",
  "description": "Labour force survey (LFS) estimates including measures of uncertainty of the number of families by specific family types, for regions of England, and also Scotland, Wales and Northern Ireland.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "families",
    "married",
    "cohabiting",
    "dependent",
    "children",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/315",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1315",
      "normalisedRecordSha256": "20d2b27e1246a45cb6b25ab82ac88e923a5eb1983d9c808a8f585d87a541b942",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries",
    "keywords": [
      "families",
      "married",
      "cohabiting",
      "dependent",
      "children"
    ],
    "meta_description": "Labour force survey (LFS) estimates including measures of uncertainty of the number of families by specific family types, for regions of England, and also Scotland, Wales and Northern Ireland.",
    "nativeIdentityField": "uri",
    "release_date": "2022-03-09T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries",
    "sourceEvidence": {
      "pointer": "/items/315",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Labour Force Survey (LFS) estimates including measures of uncertainty of the number of families by specific family types, for regions of England and also Scotland, Wales and Northern Ireland.",
    "title": "Families by family type, regions of England and UK constituent countries",
    "topics": [
      "7131",
      "1426",
      "9581"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries"
  }
}
---

# Families by family type, regions of England and UK constituent countries

Labour force survey (LFS) estimates including measures of uncertainty of the number of families by specific family types, for regions of England, and also Scotland, Wales and Northern Ireland.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesbyfamilytyperegionsofenglandandukconstituentcountries)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
