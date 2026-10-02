---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fculturalidentity%2Freligion%2Fdatasets%2Fjewishidentitydatahousing",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Jewish identity data: housing",
  "description": "People who identified as Jewish and Jewish identity groups by housing outcomes in England and Wales, Census 2021.",
  "nativeIdentifier": "/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "jewish identity",
    "housing",
    "household size",
    "occupancy rating of bedrooms",
    "ethnicity",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/997",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1997",
      "normalisedRecordSha256": "5d55287c175db2378b763805dd5cd44c5606e799bbe073e12bb4e7a55f43afd3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing"
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
    "id": "/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing",
    "keywords": [
      "jewish identity",
      "housing",
      "household size",
      "occupancy rating of bedrooms",
      "ethnicity"
    ],
    "meta_description": "People who identified as Jewish and Jewish identity groups by housing outcomes in England and Wales, Census 2021.",
    "nativeIdentityField": "uri",
    "release_date": "2023-12-18T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing",
    "sourceEvidence": {
      "pointer": "/items/997",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "People who identified as Jewish and Jewish identity groups by housing outcomes in England and Wales, Census 2021.",
    "title": "Jewish identity data: housing",
    "topics": [
      "9581",
      "4931",
      "2996"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing"
  }
}
---

# Jewish identity data: housing

People who identified as Jewish and Jewish identity groups by housing outcomes in England and Wales, Census 2021.

Native identifier: `/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/datasets/jewishidentitydatahousing)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
