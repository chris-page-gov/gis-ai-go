---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Fworkplacedisputesandworkingconditions%2Fdatasets%2Flabourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Working days lost, workers involved and stoppages in progress by main cause and industry group, UK",
  "description": "Working days lost, workers involved and stoppages in progress by main cause and industry group",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "strikes",
    "working days lost",
    "industrial action",
    "stoppages",
    "WDL",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/874",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3874",
      "normalisedRecordSha256": "d84304085a4168c2bca5943d3678bcc4b440bcf1f1b1a5fc80ec40f084b5fe00",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014"
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
    "id": "/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014",
    "keywords": [
      "strikes",
      "working days lost",
      "industrial action",
      "stoppages",
      "WDL"
    ],
    "meta_description": "Working days lost, workers involved and stoppages in progress by main cause and industry group",
    "nativeIdentityField": "uri",
    "release_date": "2019-05-16T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014",
    "sourceEvidence": {
      "pointer": "/items/874",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Annual estimates of working days lost, workers involved and stoppages in the UK, by industry group and main cause, including wage rates and earnings, working patterns and conditions, redundancy and dismissal, staffing and trade union matters.",
    "title": "Working days lost, workers involved and stoppages in progress by main cause and industry group, UK",
    "topics": [
      "6461",
      "5687",
      "2114"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014"
  }
}
---

# Working days lost, workers involved and stoppages in progress by main cause and industry group, UK

Working days lost, workers involved and stoppages in progress by main cause and industry group

Native identifier: `/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/workplacedisputesandworkingconditions/datasets/labourdisputestable5workingdayslostwdlworkersinvolvedandstoppagesinprogressbymaincauseandindustrygroupunitedkingdom2014)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
