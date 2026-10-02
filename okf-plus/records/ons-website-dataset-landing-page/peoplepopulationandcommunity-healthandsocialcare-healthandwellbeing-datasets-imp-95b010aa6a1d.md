---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fhealthandwellbeing%2Fdatasets%2Fimpactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Impact of multiple cardiometabolic conditions requiring hospitalisation on monthly employee earnings and employment status, England, main analysis",
  "description": "Descriptive data and model estimates for the change in monthly employee earnings and probability of being a paid employee following hospital admission for one, two or three cardiometabolic long-term conditions. Main analysis, aggregating CVD subtypes. This work was commissioned by NHS England.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "cardiometabolic disease",
    "long term conditions",
    "multiple long term conditions",
    "pay",
    "paid work",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/801",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1801",
      "normalisedRecordSha256": "a3674f6b65b795e6ce264285706c3c8ff7256754fce1afbdf93b12a809d92eb4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis",
    "keywords": [
      "cardiometabolic disease",
      "long term conditions",
      "multiple long term conditions",
      "pay",
      "paid work"
    ],
    "meta_description": "Descriptive data and model estimates for the change in monthly employee earnings and probability of being a paid employee following hospital admission for one, two or three cardiometabolic long-term conditions. Main analysis, aggregating CVD subtypes. This work was commissioned by NHS England.",
    "nativeIdentityField": "uri",
    "release_date": "2026-06-28T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis",
    "sourceEvidence": {
      "pointer": "/items/801",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Descriptive data and model estimates for the change in monthly employee earnings and probability of being a paid employee following hospital admission for one, two or three cardiometabolic long-term conditions. Main analysis, aggregating CVD subtypes. This work was commissioned by NHS England.",
    "title": "Impact of multiple cardiometabolic conditions requiring hospitalisation on monthly employee earnings and employment status, England, main analysis",
    "topics": [
      "9581",
      "3434",
      "6378"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis"
  }
}
---

# Impact of multiple cardiometabolic conditions requiring hospitalisation on monthly employee earnings and employment status, England, main analysis

Descriptive data and model estimates for the change in monthly employee earnings and probability of being a paid employee following hospital admission for one, two or three cardiometabolic long-term conditions. Main analysis, aggregating CVD subtypes. This work was commissioned by NHS England.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/impactofmultiplecardiometabolicconditionsrequiringhospitalisationonmonthlyemployeeearningsandemploymentstatusenglandmainanalysis)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
