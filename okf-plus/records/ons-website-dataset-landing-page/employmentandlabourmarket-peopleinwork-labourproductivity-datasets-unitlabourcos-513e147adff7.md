---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Flabourproductivity%2Fdatasets%2Funitlabourcostandunitwagecosttimeseries",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Unit labour cost and unit wage cost time series",
  "description": "Unit labour cost, average labour compensation per hour worked, labour share and unit wage cost for the whole UK economy, unit wage cost for manufacturing.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "labour",
    "wage",
    "quarterly",
    "industries",
    "manufacturing",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/767",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3767",
      "normalisedRecordSha256": "1d8aed5dbdf3cb4de05ce6589bacda66f6c0507a31145cdf853f640aaa769cd4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries"
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
    "dataset_id": "UCST",
    "edition": "",
    "id": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries",
    "keywords": [
      "labour",
      "wage",
      "quarterly",
      "industries",
      "manufacturing"
    ],
    "meta_description": "Unit labour cost, average labour compensation per hour worked, labour share and unit wage cost for the whole UK economy, unit wage cost for manufacturing.",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-17T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries",
    "sourceEvidence": {
      "pointer": "/items/767",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Unit labour cost, average labour compensation per hour worked, labour share and unit wage cost for the whole UK economy, unit wage cost for manufacturing.",
    "title": "Unit labour cost and unit wage cost time series",
    "topics": [
      "6663",
      "5687",
      "2114"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries"
  }
}
---

# Unit labour cost and unit wage cost time series

Unit labour cost, average labour compensation per hour worked, labour share and unit wage cost for the whole UK economy, unit wage cost for manufacturing.

Native identifier: `/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/unitlabourcostandunitwagecosttimeseries)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
