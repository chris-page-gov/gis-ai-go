---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fexpenditure%2Fdatasets%2Fhouseholdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Household expenditure by equivalised disposable income quintile group where the household reference person is aged under 30 years: Table A12DE",
  "description": "Average weekly household expenditure on goods and services in the UK, by region, age, income, economic status, socio-economic class and household composition.",
  "nativeIdentifier": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "living costs",
    "expenditure",
    "families",
    "purchases",
    "what are households buying",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/716",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1716",
      "normalisedRecordSha256": "1bc4efd2a060615ec5dae47bc04381f98aedf4ad18006e702cde92f1e2784671",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de"
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
    "id": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de",
    "keywords": [
      "living costs",
      "expenditure",
      "families",
      "purchases",
      "what are households buying"
    ],
    "meta_description": "Average weekly household expenditure on goods and services in the UK, by region, age, income, economic status, socio-economic class and household composition.",
    "nativeIdentityField": "uri",
    "release_date": "2019-01-24T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de",
    "sourceEvidence": {
      "pointer": "/items/716",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Average weekly household expenditure on goods and services in the UK. Data are shown by region, age, income (including equivalised) group (deciles and quintiles), economic status, socio-economic class, housing tenure, output area classification, urban and rural areas (Great Britain only), place of purchase and household composition.",
    "title": "Household expenditure by equivalised disposable income quintile group where the household reference person is aged under 30 years: Table A12DE",
    "topics": [
      "9581",
      "2627",
      "5876"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de"
  }
}
---

# Household expenditure by equivalised disposable income quintile group where the household reference person is aged under 30 years: Table A12DE

Average weekly household expenditure on goods and services in the UK, by region, age, income, economic status, socio-economic class and household composition.

Native identifier: `/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/householdexpenditurebyequivaliseddisposableincomequintilegroupwherethehouseholdreferencepersonisagedunder30uktablea12de)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
