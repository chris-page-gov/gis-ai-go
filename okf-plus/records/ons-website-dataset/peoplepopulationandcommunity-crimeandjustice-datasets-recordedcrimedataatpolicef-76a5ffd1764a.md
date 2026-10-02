---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fpeoplepopulationandcommunity%2Fcrimeandjustice%2Fdatasets%2Frecordedcrimedataatpoliceforcearealevelincludingpivottable%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Recorded Crime Data at Police Force Area Level (including pivot table)",
  "description": "Recorded crime for police force areas, including a pivot table. The data are rolling 12 month totals, with data points shown at the end of each financial year between year ending March 2003 and year ending March 2007 and at the end of each quarter from June 2007.",
  "nativeIdentifier": "/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current",
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
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "responseSha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "sourcePointer": "/items/367",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1367",
      "normalisedRecordSha256": "11a59a11cb3ca6308daee8739fce25165a8d0560c8101d933414704e3802a799",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current"
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
    "releaseVersion": "Current"
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
    "edition": "Current",
    "id": "/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current",
    "keywords": [
      "criminal activity",
      "personal experience",
      "victims",
      "offence"
    ],
    "meta_description": "Recorded crime for police force areas, including a pivot table. The data are rolling 12 month totals, with data points shown at the end of each financial year between year ending March 2003 and year ending March 2007 and at the end of each quarter from June 2007.",
    "nativeIdentityField": "uri",
    "release_date": "2015-10-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current",
    "sourceEvidence": {
      "pointer": "/items/367",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Recorded crime for police force areas, including a pivot table. The data are rolling 12 month totals, with data points shown at the end of each financial year between year ending March 2003 and year ending March 2007 and at the end of each quarter from June 2007.",
    "title": "Recorded Crime Data at Police Force Area Level (including pivot table)",
    "topics": [
      "9581",
      "2668"
    ],
    "type": "dataset",
    "uri": "/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current"
  }
}
---

# Recorded Crime Data at Police Force Area Level (including pivot table)

Recorded crime for police force areas, including a pivot table. The data are rolling 12 month totals, with data points shown at the end of each financial year between year ending March 2003 and year ending March 2007 and at the end of each quarter from June 2007.

Native identifier: `/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/recordedcrimedataatpoliceforcearealevelincludingpivottable/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
