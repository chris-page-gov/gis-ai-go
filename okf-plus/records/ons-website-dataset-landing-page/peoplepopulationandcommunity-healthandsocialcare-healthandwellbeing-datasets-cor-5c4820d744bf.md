---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fhealthandwellbeing%2Fdatasets%2Fcoronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Coronavirus and behaviour of the vaccinated population after being in contact with a positive case in England",
  "description": "Behaviour of fully vaccinated individuals not required to self-isolate after being in contact with a positive case of COVID-19, from the COVID Test and Trace Contacts Behavioural Insights Survey. Experimental Statistics.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "self-isolation",
    "vaccinated",
    "covid",
    "covid contact",
    "covid app",
    "lateral flow tests",
    "covid vaccines",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/659",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/659",
      "normalisedRecordSha256": "b94e82eb157f8a12a9e8e32d271cb711e2e62f22b116924a3c1977835397bc0f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland",
    "keywords": [
      "self-isolation",
      "vaccinated",
      "covid",
      "covid contact",
      "covid app",
      "lateral flow tests",
      "covid vaccines"
    ],
    "meta_description": "Behaviour of fully vaccinated individuals not required to self-isolate after being in contact with a positive case of COVID-19, from the COVID Test and Trace Contacts Behavioural Insights Survey. Experimental Statistics.",
    "nativeIdentityField": "uri",
    "release_date": "2022-03-14T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland",
    "sourceEvidence": {
      "pointer": "/items/659",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Behaviour of fully vaccinated individuals not required to self-isolate after being in contact with a positive case of COVID-19, from the COVID Test and Trace Contacts Behavioural Insights Survey. Experimental Statistics.",
    "title": "Coronavirus and behaviour of the vaccinated population after being in contact with a positive case in England",
    "topics": [
      "9581",
      "3434",
      "6378"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland"
  }
}
---

# Coronavirus and behaviour of the vaccinated population after being in contact with a positive case in England

Behaviour of fully vaccinated individuals not required to self-isolate after being in contact with a positive case of COVID-19, from the COVID Test and Trace Contacts Behavioural Insights Survey. Experimental Statistics.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandbehaviourofthevaccinatedpopulationafterbeingincontactwithapositivecaseinengland)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
