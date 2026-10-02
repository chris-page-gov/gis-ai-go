---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhealthandsocialcare%2Fhealthandwellbeing%2Fdatasets%2Frelationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Relationship between the NHS Diabetes Prevention Programme and monthly earnings, employee status and unplanned hospital admissions, England",
  "description": "Descriptive statistics and model estimates for the change in monthly employee earnings, employee status and probability of unplanned hospital admissions after participation in the NHS Diabetes Prevention Programme, compared with six months before the initial assessment. Includes breakdowns by sex, age group, ethnic group, area deprivation, and body mass index category.",
  "nativeIdentifier": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "healthcare",
    "type 2",
    "weight",
    "fitness",
    "health",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/126",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3126",
      "normalisedRecordSha256": "182f8fd61f24086da64d09fb04c031a06288c276f5fc2abd56c28825924302b3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland"
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
    "id": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland",
    "keywords": [
      "healthcare",
      "type 2",
      "weight",
      "fitness",
      "health"
    ],
    "meta_description": "Descriptive statistics and model estimates for the change in monthly employee earnings, employee status and probability of unplanned hospital admissions after participation in the NHS Diabetes Prevention Programme, compared with six months before the initial assessment. Includes breakdowns by sex, age group, ethnic group, area deprivation, and body mass index category.",
    "nativeIdentityField": "uri",
    "release_date": "2025-11-05T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland",
    "sourceEvidence": {
      "pointer": "/items/126",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Descriptive statistics and model estimates for the change in monthly employee earnings, employee status and probability of unplanned hospital admissions after participation in the NHS Diabetes Prevention Programme, compared with six months before the initial assessment. Includes breakdowns by sex, age group, ethnic group, area deprivation, and body mass index category.",
    "title": "Relationship between the NHS Diabetes Prevention Programme and monthly earnings, employee status and unplanned hospital admissions, England",
    "topics": [
      "9581",
      "3434",
      "6378"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland"
  }
}
---

# Relationship between the NHS Diabetes Prevention Programme and monthly earnings, employee status and unplanned hospital admissions, England

Descriptive statistics and model estimates for the change in monthly employee earnings, employee status and probability of unplanned hospital admissions after participation in the NHS Diabetes Prevention Programme, compared with six months before the initial assessment. Includes breakdowns by sex, age group, ethnic group, area deprivation, and body mass index category.

Native identifier: `/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/relationshipbetweenthenhsdiabetespreventionprogrammeandmonthlyearningsemployeestatusandunplannedhospitaladmissionsengland)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
