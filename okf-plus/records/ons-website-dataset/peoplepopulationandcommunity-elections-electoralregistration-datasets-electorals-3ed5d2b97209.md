---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fpeoplepopulationandcommunity%2Felections%2Felectoralregistration%2Fdatasets%2Felectoralstatisticsforuk%2F2013unformatted",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Electoral Statistics for UK",
  "description": "Total number of local government and parliamentary electors (including the number of attainers) registered to vote in the UK.",
  "nativeIdentifier": "/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "00curres",
    "Electoral",
    "local government",
    "parliamentary constituencies",
    "00curres",
    "electoral",
    "local government",
    "parliamentary constituencies",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/425",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/425",
      "normalisedRecordSha256": "66f33a714a27da02a5136b1bc6e9013cf356e7352645669a7e5b5877fb247ffd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted"
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
    "releaseVersion": "2013 Unformatted"
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
    "edition": "2013 Unformatted",
    "id": "/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted",
    "keywords": [
      "00curres",
      "Electoral",
      "local government",
      "parliamentary constituencies",
      "00curres",
      "electoral",
      "local government",
      "parliamentary constituencies"
    ],
    "meta_description": "Total number of local government and parliamentary electors (including the number of attainers) registered to vote in the UK.",
    "nativeIdentityField": "uri",
    "release_date": "2015-04-15T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted",
    "sourceEvidence": {
      "pointer": "/items/425",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Total number of local government and parliamentary electors (including the number of attainers) registered to vote in the UK.",
    "title": "Electoral Statistics for UK",
    "topics": [
      "9581",
      "9421",
      "4629"
    ],
    "type": "dataset",
    "uri": "/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted"
  }
}
---

# Electoral Statistics for UK

Total number of local government and parliamentary electors (including the number of attainers) registered to vote in the UK.

Native identifier: `/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/elections/electoralregistration/datasets/electoralstatisticsforuk/2013unformatted)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
