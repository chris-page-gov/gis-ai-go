---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Femploymentandemployeetypes%2Fdatasets%2Fworkingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Households with and without dependent children by type of household and combined economic activity status of household members: Table B",
  "description": "Quarterly and historical data on UK households with and without dependent children by type of household and combined economic activity status of household members.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "worklessness",
    "inactivity",
    "inactive",
    "unemployment",
    "unemployed",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/758",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1758",
      "normalisedRecordSha256": "71f73e86fe47a1176c4a2301b7c921b35c29a16b36e4ebd20c2a3dfd17dc1c3c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers"
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
    "id": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers",
    "keywords": [
      "worklessness",
      "inactivity",
      "inactive",
      "unemployment",
      "unemployed"
    ],
    "meta_description": "Quarterly and historical data on UK households with and without dependent children by type of household and combined economic activity status of household members.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-01T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers",
    "sourceEvidence": {
      "pointer": "/items/758",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Quarterly and historical data on UK households with and without dependent children by type of household and combined economic activity status of household members.",
    "title": "Households with and without dependent children by type of household and combined economic activity status of household members: Table B",
    "topics": [
      "2114",
      "9243",
      "5687"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers"
  }
}
---

# Households with and without dependent children by type of household and combined economic activity status of household members: Table B

Quarterly and historical data on UK households with and without dependent children by type of household and combined economic activity status of household members.

Native identifier: `/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/workingandworklesshouseholdstablebhouseholdswithandwithoutdependentchildrenbytypeofhouseholdandcombinedeconomicactivitystatusofhouseholdmembers)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
