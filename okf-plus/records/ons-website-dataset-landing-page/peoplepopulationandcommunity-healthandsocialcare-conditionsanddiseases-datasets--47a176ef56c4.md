---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fconditionsanddiseases%2Fdatasets%2Fcoronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Coronavirus and the social impacts on Great Britain: attitudes towards compliance behaviours",
  "description": "Data on adult's compliance behaviours (hand washing or sanitising, face coverings and social distancing), perception of the importance of these, and other people's compliance behaviours to slow down the spread of coronavirus and adults planned behaviours and attitudes towards the ending of COVID-19 restrictions.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "handwashing",
    "wearing masks",
    "ventilation",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/699",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/699",
      "normalisedRecordSha256": "dc9e66e8479d2669790796a06d8bda1889d589a99f2aa0178faaa3a7b63a0090",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend",
    "keywords": [
      "handwashing",
      "wearing masks",
      "ventilation"
    ],
    "meta_description": "Data on adult's compliance behaviours (hand washing or sanitising, face coverings and social distancing), perception of the importance of these, and other people's compliance behaviours to slow down the spread of coronavirus and adults planned behaviours and attitudes towards the ending of COVID-19 restrictions.",
    "nativeIdentityField": "uri",
    "release_date": "2021-08-26T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend",
    "sourceEvidence": {
      "pointer": "/items/699",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Data on adult's perception of the importance of compliance behaviours (hand washing or sanitising, social distancing, face coverings and ventilation) to slow the spread of coronavirus (COVID-19) and actions taken during home visits. Data from the Opinions and Lifestyle Survey.",
    "title": "Coronavirus and the social impacts on Great Britain: attitudes towards compliance behaviours",
    "topics": [
      "3434",
      "8171",
      "9581"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend"
  }
}
---

# Coronavirus and the social impacts on Great Britain: attitudes towards compliance behaviours

Data on adult's compliance behaviours (hand washing or sanitising, face coverings and social distancing), perception of the importance of these, and other people's compliance behaviours to slow down the spread of coronavirus and adults planned behaviours and attitudes towards the ending of COVID-19 restrictions.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronavirusandthesocialimpactsongreatbritainperceptionsofcompliancebehavioursandplannedbehaviourswhenrestrictionsend)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
