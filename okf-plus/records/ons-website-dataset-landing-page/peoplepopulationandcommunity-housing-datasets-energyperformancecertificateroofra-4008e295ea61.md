---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fpeoplepopulationandcommunity%2Fhousing%2Fdatasets%2Fenergyperformancecertificateroofratingsenglandandwales",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Energy Performance Certificate roof ratings, England and Wales",
  "description": "Roof insulation ratings in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
  "nativeIdentifier": "/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/114",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1114",
      "normalisedRecordSha256": "47568b4b773680b2031f1ef9a36a06c533024b380052d45341f4b0e46c243e38",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales"
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
    "id": "/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales",
    "keywords": [
      "energy performance",
      "EPC",
      "dwellings",
      "potential"
    ],
    "meta_description": "Roof insulation ratings in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
    "nativeIdentityField": "uri",
    "release_date": "2023-05-02T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales",
    "sourceEvidence": {
      "pointer": "/items/114",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Roof insulation ratings in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.",
    "title": "Energy Performance Certificate roof ratings, England and Wales",
    "topics": [
      "9581",
      "5586"
    ],
    "type": "dataset_landing_page",
    "uri": "/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales"
  }
}
---

# Energy Performance Certificate roof ratings, England and Wales

Roof insulation ratings in England and Wales at the country and subnational level and for five-year groups. These are broken down by property type, tenure, and property age.

Native identifier: `/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateroofratingsenglandandwales)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
