---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Standardised illness ratios by National Statistics Socio-economic Classification, England and Wales",
  "description": "Standardised illness ratios by personal socio-economic position using the National Statistics Socio-economic Classification based on occupation.",
  "nativeIdentifier": "standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "health, socioeconomic, ratios"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/12",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/12",
      "normalisedRecordSha256": "f91dc58c4375a5c9bc1e105931e32550e2aa2b4e4da7e0579be18b9bbf292c51",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions/1981-to-2011/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:30:38.302298Z",
      "responseSha256": "70af3397b714c1e8a522eef86eeb70cb5c2c02601ca53ea4d9a89d07ba26b71c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/12",
      "normalisedRecordSha256": "0ba0ee9ad24fecaaf866efe28535aa46ef641e8739ced8ef760c544c887775ff",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew"
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
    "nextRelease": "To be announced",
    "metadataModified": "2026-09-15T09:20:40.617Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "ONS published-data terms apply; dataset-specific notices and third-party rights must be checked.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Time-option extrema describe available native codes; continuity and populated observation cells have not been established."
  ],
  "details": {
    "description": "Standardised illness ratios by personal socio-economic position using the National Statistics Socio-economic Classification based on occupation.",
    "id": "standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
    "keywords": [
      "health, socioeconomic, ratios"
    ],
    "last_updated": "2026-09-15T09:20:40.617Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions/1981-to-2011/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew"
      }
    },
    "next_release": "To be announced",
    "qmi": {},
    "state": "published",
    "title": "Standardised illness ratios by National Statistics Socio-economic Classification, England and Wales",
    "type": "static",
    "timeMetadata": {
      "dimensions": [],
      "edition": "1981-to-2011",
      "id": "standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
      "metadata": {
        "description": "Standardised illness ratios by personal socio-economic position using the National Statistics Socio-economic Classification based on occupation.",
        "last_updated": "2026-09-15T09:20:40.617Z",
        "next_release": "To be announced",
        "release_date": "2022-08-26T08:30:00.000Z",
        "state": "published",
        "title": "Standardised illness ratios by National Statistics Socio-economic Classification, England and Wales",
        "type": "static"
      },
      "metadataContract": {
        "catalogueType": "static",
        "dimensionListPresent": false,
        "identityEvidence": {
          "edition": "1981-to-2011",
          "id": "standardised-illness-ratios-national-statistics-socio-economic-classification-ew",
          "version": 1
        },
        "variant": "static-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:38.302298Z",
        "sha256": "70af3397b714c1e8a522eef86eeb70cb5c2c02601ca53ea4d9a89d07ba26b71c",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions/1981-to-2011/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions/1981-to-2011/versions/1"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew/editions"
  }
}
---

# Standardised illness ratios by National Statistics Socio-economic Classification, England and Wales

Standardised illness ratios by personal socio-economic position using the National Statistics Socio-economic Classification based on occupation.

Native identifier: `standardised-illness-ratios-national-statistics-socio-economic-classification-ew`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/standardised-illness-ratios-national-statistics-socio-economic-classification-ew)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
