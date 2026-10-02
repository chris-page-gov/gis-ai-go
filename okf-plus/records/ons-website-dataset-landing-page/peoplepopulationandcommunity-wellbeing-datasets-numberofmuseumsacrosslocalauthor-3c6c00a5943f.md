---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fwellbeing%2Fdatasets%2Fnumberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Number of museums across Local Authority Districts (LAD) in the United Kingdom",
  "description": "Counts of museums and counts grouped by size band and type of museum across Local Authority Districts (LAD) In the United Kingdom. Counts of museums per 100,000 people are also provided.",
  "nativeIdentifier": "/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "museums",
    "access to amenities",
    "Local Authority Disctricts",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/530",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2530",
      "normalisedRecordSha256": "d1bfff549394c1fca91a576f6250e30c78a3c0821dda01d681cc49c691b74016",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom"
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
    "id": "/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom",
    "keywords": [
      "museums",
      "access to amenities",
      "Local Authority Disctricts"
    ],
    "meta_description": "Counts of museums and counts grouped by size band and type of museum across Local Authority Districts (LAD) In the United Kingdom. Counts of museums per 100,000 people are also provided.",
    "nativeIdentityField": "uri",
    "release_date": "2024-03-07T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom",
    "sourceEvidence": {
      "pointer": "/items/530",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Counts of museums and counts grouped by size band and type of museum across Local Authority Districts (LAD) in the United Kingdom. Counts of museums per 100,000 people are also provided.",
    "title": "Number of museums across Local Authority Districts (LAD) in the United Kingdom",
    "topics": [
      "9581",
      "2456"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom"
  }
}
---

# Number of museums across Local Authority Districts (LAD) in the United Kingdom

Counts of museums and counts grouped by size band and type of museum across Local Authority Districts (LAD) In the United Kingdom. Counts of museums per 100,000 people are also provided.

Native identifier: `/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/numberofmuseumsacrosslocalauthoritydistrictsladintheunitedkingdom)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
