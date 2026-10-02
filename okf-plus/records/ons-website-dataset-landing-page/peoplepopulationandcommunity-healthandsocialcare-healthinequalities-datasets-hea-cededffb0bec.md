---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fhealthinequalities%2Fdatasets%2Fhealthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Health state life expectancies by national deprivation deciles, England: 2018 to 2020",
  "description": "Life expectancy (LE), healthy life expectancy (HLE), disability-free life expectancy (DFLE), Slope Index of Inequality (SII) and range by national deprivation deciles (IMD 2019), England, 2015 to 2017 and 2018 to 2020.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Life expectancy",
    "SII",
    "Disability-free",
    "Inequality",
    "Good health",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/573",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1573",
      "normalisedRecordSha256": "1e9b37625209cff77a8b639b2a64c0425698ea5c39254d211bc85fa91d76057b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020",
    "keywords": [
      "Life expectancy",
      "SII",
      "Disability-free",
      "Inequality",
      "Good health"
    ],
    "meta_description": "Life expectancy (LE), healthy life expectancy (HLE), disability-free life expectancy (DFLE), Slope Index of Inequality (SII) and range by national deprivation deciles (IMD 2019), England, 2015 to 2017 and 2018 to 2020.",
    "nativeIdentityField": "uri",
    "release_date": "2022-04-24T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020",
    "sourceEvidence": {
      "pointer": "/items/573",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Life expectancy (LE), healthy life expectancy (HLE), disability-free life expectancy (DFLE), Slope Index of Inequality (SII) and range by national deprivation deciles using the Index of Multiple Deprivation 2015 for data periods from 2011 to 2013 to 2015 to 2017, and the Index of Multiple Deprivation 2019 for data periods from 2016 to 2018 to 2018 to 2020: England, 2011 to 2013 to 2018 to 2020.",
    "title": "Health state life expectancies by national deprivation deciles, England: 2018 to 2020",
    "topics": [
      "9581",
      "3434",
      "6261"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020"
  }
}
---

# Health state life expectancies by national deprivation deciles, England: 2018 to 2020

Life expectancy (LE), healthy life expectancy (HLE), disability-free life expectancy (DFLE), Slope Index of Inequality (SII) and range by national deprivation deciles (IMD 2019), England, 2015 to 2017 and 2018 to 2020.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthinequalities/datasets/healthstatelifeexpectanciesbynationaldeprivationdecilesengland2018to2020)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
