---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fexpenditure%2Fdatasets%2Fexpenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Expenditure of one person retired households not mainly dependent on state pensions by equivalised disposable income quintile group (OECD-modified scale), UK: Table 3.4E",
  "description": "Part of a series of tables relating to household expenditure categorised by Classification Of Individual Consumption by Purpose (COICOP). Estimates are drawn from the Living Costs and Food Survey",
  "nativeIdentifier": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "living costs",
    "pensioner",
    "quantile",
    "category",
    "spending",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/250",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1250",
      "normalisedRecordSha256": "7fea6be14b6b9de97174f97fbd2e311b5366fcd44a54cd068487b10e1fd9f06c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e"
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
    "id": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e",
    "keywords": [
      "living costs",
      "pensioner",
      "quantile",
      "category",
      "spending"
    ],
    "meta_description": "Part of a series of tables relating to household expenditure categorised by Classification Of Individual Consumption by Purpose (COICOP). Estimates are drawn from the Living Costs and Food Survey",
    "nativeIdentityField": "uri",
    "release_date": "2017-02-16T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e",
    "sourceEvidence": {
      "pointer": "/items/250",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Part of a series of tables relating to household expenditure categorised by Classification Of Individual Consumption by Purpose (COICOP). Estimates are drawn from the Living Costs and Food Survey",
    "title": "Expenditure of one person retired households not mainly dependent on state pensions by equivalised disposable income quintile group (OECD-modified scale), UK: Table 3.4E",
    "topics": [
      "9581",
      "2627",
      "5876"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e"
  }
}
---

# Expenditure of one person retired households not mainly dependent on state pensions by equivalised disposable income quintile group (OECD-modified scale), UK: Table 3.4E

Part of a series of tables relating to household expenditure categorised by Classification Of Individual Consumption by Purpose (COICOP). Estimates are drawn from the Living Costs and Food Survey

Native identifier: `/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/datasets/expenditureofonepersonretiredhouseholdsnotmainlydependentonstatepensionsbyequivaliseddisposableincomequintilegroupoecdmodifiedscaleuktable34e)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
