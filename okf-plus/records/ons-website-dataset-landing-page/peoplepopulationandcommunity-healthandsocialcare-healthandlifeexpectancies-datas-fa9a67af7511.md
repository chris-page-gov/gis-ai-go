---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fhealthandlifeexpectancies%2Fdatasets%2Fhealthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Health state life expectancies (activity limitation) for Wales by country, decile and unitary authority (UA) for males and females at birth and men and women at age 65, 2010 to 2012",
  "description": "General health expectancy estimates by sex, at birth and age 65, for Wales by country, national deciles of area deprivation and unitary authorities.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "2011 Census",
    "Wales",
    "Activity limitation",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/558",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1558",
      "normalisedRecordSha256": "26d72ccbe95ee81c1eb6bd17ecd861cd203e7243496d3a60efb1b691f0cb3b9d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012",
    "keywords": [
      "2011 Census",
      "Wales",
      "Activity limitation"
    ],
    "meta_description": "General health expectancy estimates by sex, at birth and age 65, for Wales by country, national deciles of area deprivation and unitary authorities.",
    "nativeIdentityField": "uri",
    "release_date": "2016-10-10T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012",
    "sourceEvidence": {
      "pointer": "/items/558",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Activity limitation expectancy estimates by sex, at birth and age 65, for Wales by country, national deciles of area deprivation and unitary authorities.",
    "title": "Health state life expectancies (activity limitation) for Wales by country, decile and unitary authority (UA) for males and females at birth and men and women at age 65, 2010 to 2012",
    "topics": [
      "9581",
      "3434",
      "1167"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012"
  }
}
---

# Health state life expectancies (activity limitation) for Wales by country, decile and unitary authority (UA) for males and females at birth and men and women at age 65, 2010 to 2012

General health expectancy estimates by sex, at birth and age 65, for Wales by country, national deciles of area deprivation and unitary authorities.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/healthstatelifeexpectanciesactivitylimitationforwalesbycountrydecileandunitaryauthorityuaformalesandfemalesatbirthandmenandwomenatage652010to2012)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
