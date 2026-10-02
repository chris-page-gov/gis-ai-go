---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fconditionsanddiseases%2Fdatasets%2Fdifferencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Differences in time use between lockdowns, by vaccine status and other demographics, Great Britain",
  "description": "Time Use Survey data show changes in how people spent their time during coronavirus (COVID-19) restrictions in March and April 2020, September to October 2020 and March 2021, as well as before the pandemic. It also includes Opinions and Lifestyle Survey data on behaviours following vaccination in Great Britain from 19 May to 13 June 2021.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "time use",
    "coronavirus",
    "vaccine",
    "lockdown",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/867",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/867",
      "normalisedRecordSha256": "b1d98c198935cad75e1866412da57b706772d43ccbfba10aaa71512ffbc5263e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain",
    "keywords": [
      "time use",
      "coronavirus",
      "vaccine",
      "lockdown"
    ],
    "meta_description": "Time Use Survey data show changes in how people spent their time during coronavirus (COVID-19) restrictions in March and April 2020, September to October 2020 and March 2021, as well as before the pandemic. It also includes Opinions and Lifestyle Survey data on behaviours following vaccination in Great Britain from 19 May to 13 June 2021.",
    "nativeIdentityField": "uri",
    "release_date": "2021-06-22T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain",
    "sourceEvidence": {
      "pointer": "/items/867",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Time Use Survey data show changes in how people spent their time during coronavirus (COVID-19) restrictions in March and April 2020, September to October 2020 and March 2021, as well as before the pandemic. It also includes Opinions and Lifestyle Survey data on behaviours following vaccination in Great Britain from 19 May to 13 June 2021.",
    "title": "Differences in time use between lockdowns, by vaccine status and other demographics, Great Britain",
    "topics": [
      "9581",
      "3434",
      "8171"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain"
  }
}
---

# Differences in time use between lockdowns, by vaccine status and other demographics, Great Britain

Time Use Survey data show changes in how people spent their time during coronavirus (COVID-19) restrictions in March and April 2020, September to October 2020 and March 2021, as well as before the pandemic. It also includes Opinions and Lifestyle Survey data on behaviours following vaccination in Great Britain from 19 May to 13 June 2021.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/differencesintimeusebetweenlockdownsbyvaccinestatusandotherdemographicsgreatbritain)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
