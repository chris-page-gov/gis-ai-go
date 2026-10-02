---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhousing%2Fdatasets%2Fcurrentandpotentialenergyefficiencyofhousingenglandandwales",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Current and potential energy efficiency of housing, England and Wales",
  "description": "Energy efficiency in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
  "nativeIdentifier": "/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "energy performance",
    "EPC",
    "dwellings",
    "potential",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/769",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/769",
      "normalisedRecordSha256": "c5b6935e2af39367f8379308be42162914be343220e5f06072d9724614c6974f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales"
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
    "id": "/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales",
    "keywords": [
      "energy performance",
      "EPC",
      "dwellings",
      "potential"
    ],
    "meta_description": "Energy efficiency in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
    "nativeIdentityField": "uri",
    "release_date": "2023-05-02T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales",
    "sourceEvidence": {
      "pointer": "/items/769",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Energy efficiency in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
    "title": "Current and potential energy efficiency of housing, England and Wales",
    "topics": [
      "9581",
      "5586"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales"
  }
}
---

# Current and potential energy efficiency of housing, England and Wales

Energy efficiency in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.

Native identifier: `/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/currentandpotentialenergyefficiencyofhousingenglandandwales)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
