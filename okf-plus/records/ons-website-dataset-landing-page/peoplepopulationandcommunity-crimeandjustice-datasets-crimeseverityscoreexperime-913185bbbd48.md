---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fcrimeandjustice%2Fdatasets%2Fcrimeseverityscoreexperimentalstatistics",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Crime Severity Score: Year ending March 2025",
  "description": "Crime Severity Score (CSS) data for police force areas and community safety partnerships, which equate in the majority of instances to local authorities. Includes a data tool to enable production of summary charts on trends and comparisons between areas.",
  "nativeIdentifier": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "offence",
    "harm",
    "police",
    "criminal activity",
    "victims",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/749",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/749",
      "normalisedRecordSha256": "f0631b94a457334f80b096f13c70e3126f3a97a197c28535b78a0410f7a79682",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics"
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
    "id": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics",
    "keywords": [
      "offence",
      "harm",
      "police",
      "criminal activity",
      "victims"
    ],
    "meta_description": "Crime Severity Score (CSS) data for police force areas and community safety partnerships, which equate in the majority of instances to local authorities. Includes a data tool to enable production of summary charts on trends and comparisons between areas.",
    "nativeIdentityField": "uri",
    "release_date": "2025-12-09T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics",
    "sourceEvidence": {
      "pointer": "/items/749",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Crime Severity Score (CSS) data for police force areas and community safety partnerships, which equate in the majority of instances to local authorities. Includes a data tool to enable production of summary charts on trends and comparisons between areas.",
    "title": "Crime Severity Score: Year ending March 2025",
    "topics": [
      "9581",
      "2668"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics"
  }
}
---

# Crime Severity Score: Year ending March 2025

Crime Severity Score (CSS) data for police force areas and community safety partnerships, which equate in the majority of instances to local authorities. Includes a data tool to enable production of summary charts on trends and comparisons between areas.

Native identifier: `/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/datasets/crimeseverityscoreexperimentalstatistics)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
