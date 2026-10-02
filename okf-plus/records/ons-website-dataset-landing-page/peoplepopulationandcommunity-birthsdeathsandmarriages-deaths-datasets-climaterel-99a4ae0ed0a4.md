---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Fdeaths%2Fdatasets%2Fclimaterelatedmortalityenglandandwales",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Climate-related mortality, England and Wales",
  "description": "Results from modelled analysis of mortality attributable to the hottest and coldest 2.5% of ambient outdoor temperatures, using daily mean temperatures for regions of England, and for Wales. Includes detailed results for controlling for coronavirus (COVID-19), demographic breakdowns, underlying cause of death, and guidance for interpreting and using the results.",
  "nativeIdentifier": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "heat",
    "cold",
    "death",
    "health",
    "temperatures",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/519",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/519",
      "normalisedRecordSha256": "5cc301aa2441f77cb91d52a3e081b0483d0b3dd2a569902e5bb1d12b619373b2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales"
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
    "id": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales",
    "keywords": [
      "heat",
      "cold",
      "death",
      "health",
      "temperatures"
    ],
    "meta_description": "Results from modelled analysis of mortality attributable to the hottest and coldest 2.5% of ambient outdoor temperatures, using daily mean temperatures for regions of England, and for Wales. Includes detailed results for controlling for coronavirus (COVID-19), demographic breakdowns, underlying cause of death, and guidance for interpreting and using the results.",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-25T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales",
    "sourceEvidence": {
      "pointer": "/items/519",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Results from modelled analysis of mortality attributable to the hottest and coldest 2.5% of ambient outdoor temperatures, using daily mean temperatures for regions of England, and for Wales. Includes detailed results for controlling for coronavirus (COVID-19), demographic breakdowns, underlying cause of death, and guidance for interpreting and using the results.",
    "title": "Climate-related mortality, England and Wales",
    "topics": [
      "9581",
      "7131",
      "2998"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales"
  }
}
---

# Climate-related mortality, England and Wales

Results from modelled analysis of mortality attributable to the hottest and coldest 2.5% of ambient outdoor temperatures, using daily mean temperatures for regions of England, and for Wales. Includes detailed results for controlling for coronavirus (COVID-19), demographic breakdowns, underlying cause of death, and guidance for interpreting and using the results.

Native identifier: `/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/climaterelatedmortalityenglandandwales)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
