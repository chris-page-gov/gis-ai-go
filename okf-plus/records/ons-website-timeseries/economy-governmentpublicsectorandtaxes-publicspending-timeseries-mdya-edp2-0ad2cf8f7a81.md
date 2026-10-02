---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicspending%2Ftimeseries%2Fmdya%2Fedp2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "CG: Change in CG consolidated gross debt (EDP)",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "timeseries"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "responseSha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "sourcePointer": "/items/12",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/9012",
      "normalisedRecordSha256": "160ebce66801046933208b96a7405eb2e6bfebf810f5382a2b230f22565adf7e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2"
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
    "cdid": "MDYA",
    "dataset_id": "EDP2",
    "edition": "",
    "id": "/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2021-10-26T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2",
    "sourceEvidence": {
      "pointer": "/items/12",
      "retrievedAt": "2026-10-02T07:59:06.843700Z",
      "sha256": "6d8ab7f5f86bb0f3de34ba6fcf69f527f416a21581a98001137c517ab167edb4",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=9000"
    },
    "summary": "",
    "title": "CG: Change in CG consolidated gross debt (EDP)",
    "topics": [
      "9828",
      "8233",
      "1245"
    ],
    "type": "timeseries",
    "uri": "/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2"
  }
}
---

# CG: Change in CG consolidated gross debt (EDP)

ONS website catalogue metadata.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicspending/timeseries/mdya/edp2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
