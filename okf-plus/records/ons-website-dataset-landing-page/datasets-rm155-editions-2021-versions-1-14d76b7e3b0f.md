---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2FRM155%2Feditions%2F2021%2Fversions%2F1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Family type by parents' ability to speak Welsh by age and ability to speak Welsh of dependent child",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/RM155/editions/2021/versions/1",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/RM155/editions/2021/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "families_and_children_welsh_speaker_parents_9a,welsh_skills_speak,dependent_child_age_4a",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/322",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1322",
      "normalisedRecordSha256": "037d1132ba37240c4f78cb531c8504dd0ff1254b3d29f21bfec2c90ddb9e18bd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/RM155/editions/2021/versions/1"
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
    "releaseVersion": "2021"
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
    "canonical_topic": "7779",
    "cdid": "",
    "dataset_id": "RM155",
    "dimensions": [
      {
        "label": "Welsh speaking ability",
        "name": "welsh_skills_speak",
        "raw_label": "Welsh speaking ability (3 categories)"
      },
      {
        "label": "Dependent child age",
        "name": "dependent_child_age_4a",
        "raw_label": "Dependent child age (4 categories)"
      },
      {
        "label": "Family type and Welsh-speaking adults",
        "name": "families_and_children_welsh_speaker_parents_9a",
        "raw_label": "Family type and Welsh-speaking adults (9 categories)"
      }
    ],
    "edition": "2021",
    "id": "/datasets/RM155/editions/2021/versions/1",
    "keywords": [
      "ltla",
      "families_and_children_welsh_speaker_parents_9a,welsh_skills_speak,dependent_child_age_4a"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2023-04-25T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/RM155/editions/2021/versions/1",
    "sourceEvidence": {
      "pointer": "/items/322",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "This dataset provides Census 2021 estimates that classify usually resident dependent children aged 3 years and over in families in Wales by family type, by the parents' ability to speak Welsh, by age, and by the ability to speak Welsh. The estimates are as at Census Day, 21 March 2021.",
    "title": "Family type by parents' ability to speak Welsh by age and ability to speak Welsh of dependent child",
    "topics": [
      "9497"
    ],
    "type": "dataset_landing_page",
    "uri": "/datasets/RM155/editions/2021/versions/1"
  }
}
---

# Family type by parents' ability to speak Welsh by age and ability to speak Welsh of dependent child

ONS website catalogue metadata.

Native identifier: `/datasets/RM155/editions/2021/versions/1`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/RM155/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
