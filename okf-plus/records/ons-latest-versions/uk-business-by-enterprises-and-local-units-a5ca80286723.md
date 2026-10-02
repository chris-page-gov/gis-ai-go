---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/uk-business-by-enterprises-and-local-units",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Business: Activity, Size and Location",
  "description": "The data contained in these tables are numbers of enterprises and local units produced from a snapshot of the Inter-Departmental Business Register (IDBR) taken on 12 March 2021. This dataset contains details of the number of VAT and/or PAYE based enterprises and local units in districts, counties and unitary authorities within region and country by broad industry group.",
  "nativeIdentifier": "uk-business-by-enterprises-and-local-units",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:30:29.935906Z",
      "responseSha256": "017f6fe435e6a37522ca581c9d8aa4bd3dd4f9eb884594bda218f603e54cc444",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/7",
      "normalisedRecordSha256": "948a8595226b2b182986eabf9ca50e87c4d40201f0e63e25b87dff1d1dfaf664",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2022",
    "end": "2022",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Annual",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-A",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "To be announced",
    "metadataModified": "2022-11-03T09:50:09.932Z",
    "releaseVersion": "1"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "dimensions": [
      {
        "id": "calendar-years",
        "label": "Time",
        "name": "time"
      },
      {
        "id": "administrative-geography",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "sic-unofficial",
        "label": "Standard Industrial Classification",
        "name": "unofficialstandardindustrialclassification"
      },
      {
        "id": "enterprises-and-local-units",
        "label": "Enterprises and local units",
        "name": "enterprisesandlocalunits"
      }
    ],
    "edition": "2022",
    "id": "uk-business-by-enterprises-and-local-units",
    "metadata": {
      "description": "The data contained in these tables are numbers of enterprises and local units produced from a snapshot of the Inter-Departmental Business Register (IDBR) taken on 12 March 2021. This dataset contains details of the number of VAT and/or PAYE based enterprises and local units in districts, counties and unitary authorities within region and country by broad industry group.",
      "last_updated": "2022-11-03T09:50:09.932Z",
      "next_release": "To be announced",
      "release_date": "2022-09-28T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "UK Business: Activity, Size and Location",
      "type": "filterable",
      "unit_of_measure": "Count"
    },
    "metadataContract": {
      "catalogueType": "filterable",
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "2022",
        "id": "uk-business-by-enterprises-and-local-units",
        "version": 1
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:29.935906Z",
      "sha256": "017f6fe435e6a37522ca581c9d8aa4bd3dd4f9eb884594bda218f603e54cc444",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2022",
        "minimumNative": "2022",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2022",
          "option": "2022"
        }
      ],
      "reportedTotal": 1,
      "retrievedUnique": 1,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "1",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2022",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# UK Business: Activity, Size and Location

The data contained in these tables are numbers of enterprises and local units produced from a snapshot of the Inter-Departmental Business Register (IDBR) taken on 12 March 2021. This dataset contains details of the number of VAT and/or PAYE based enterprises and local units in districts, counties and unitary authorities within region and country by broad industry group.

Native identifier: `uk-business-by-enterprises-and-local-units`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/uk-business-by-enterprises-and-local-units/editions/2022/versions/1)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2022, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
