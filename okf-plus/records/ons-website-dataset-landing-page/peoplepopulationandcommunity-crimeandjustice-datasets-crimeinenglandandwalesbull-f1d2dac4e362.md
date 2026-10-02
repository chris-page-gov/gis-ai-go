---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fcrimeandjustice%2Fdatasets%2Fcrimeinenglandandwalesbulletintables",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Crime in England and Wales: Bulletin Tables",
  "description": "Data tables and figures from the statistical bulletin in excel format. The data contained in these tables are from four sources: Crime Survey for England and Wales, Home Office police recorded crime, the National Fraud Intelligence Bureau and the Ministry of Justice Criminal Justice Statistics Quarterly Update.",
  "nativeIdentifier": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "criminal activity",
    "personal experience",
    "victims",
    "offence",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/758",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/758",
      "normalisedRecordSha256": "6700791937684e5a91832a2edbe4647df21b557d87ddf0788d2a41da49ac6d53",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables"
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
    "id": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables",
    "keywords": [
      "criminal activity",
      "personal experience",
      "victims",
      "offence"
    ],
    "meta_description": "Data tables and figures from the statistical bulletin in excel format. The data contained in these tables are from four sources: Crime Survey for England and Wales, Home Office police recorded crime, the National Fraud Intelligence Bureau and the Ministry of Justice Criminal Justice Statistics Quarterly Update.",
    "nativeIdentityField": "uri",
    "release_date": "2017-10-18T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables",
    "sourceEvidence": {
      "pointer": "/items/758",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Data tables and figures from the statistical bulletin in excel format. The data contained in these tables are from four sources: Crime Survey for England and Wales, Home Office police recorded crime, the National Fraud Intelligence Bureau and the Ministry of Justice Criminal Justice Statistics Quarterly Update. Please note: The methodology by which the CSEW calculates its incidents of crime changed in December 2018. Incident numbers and rates published in the Bulletin Tables prior to the year ending September 2018 dataset are not comparable with those currently published.",
    "title": "Crime in England and Wales: Bulletin Tables",
    "topics": [
      "9581",
      "2668"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables"
  }
}
---

# Crime in England and Wales: Bulletin Tables

Data tables and figures from the statistical bulletin in excel format. The data contained in these tables are from four sources: Crime Survey for England and Wales, Home Office police recorded crime, the National Fraud Intelligence Bureau and the Ministry of Justice Criminal Justice Statistics Quarterly Update.

Native identifier: `/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeinenglandandwalesbulletintables)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
