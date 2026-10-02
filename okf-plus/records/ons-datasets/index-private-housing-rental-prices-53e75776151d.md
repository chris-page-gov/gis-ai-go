---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/index-private-housing-rental-prices",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Index of Private Housing Rental Prices",
  "description": "An experimental price index tracking the prices paid for renting property from private landlords in the United Kingdom",
  "nativeIdentifier": "index-private-housing-rental-prices",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "private renting",
    "regions,IPHRP,rent,inflation"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/30",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/30",
      "normalisedRecordSha256": "3d38a1705b6366d159020649c33c1ca86e530dd77ca9d28cc19fa6231ca92ac3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions/time-series/versions/41/metadata",
      "retrievedAt": "2026-10-02T01:31:07.865713Z",
      "responseSha256": "bf8269e9f97ba94e434c2ed3178f35f5593a99ef40c68c5c3e07045199f3592a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/30",
      "normalisedRecordSha256": "b9cc128c167651052840ea602698aeb100430c96a522120b61cb88d4199800f6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices"
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
      "status": "source-stated",
      "label": "Monthly",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-M",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "TBC",
    "metadataModified": "2024-02-14T09:54:29.063Z",
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
    "description": "An experimental price index tracking the prices paid for renting property from private landlords in the United Kingdom",
    "id": "index-private-housing-rental-prices",
    "keywords": [
      "private renting",
      "regions,IPHRP,rent,inflation"
    ],
    "last_updated": "2024-02-14T09:54:29.063Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions/time-series/versions/41",
        "id": "41"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/housing"
      }
    },
    "national_statistic": false,
    "next_release": "TBC",
    "qmi": {
      "href": "https://www.ons.gov.uk/economy/inflationandpriceindices/methodologies/indexofprivatehousingrentalpricesqmi"
    },
    "release_frequency": "Monthly",
    "state": "published",
    "title": "Index of Private Housing Rental Prices",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "mmm-yy",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "index-and-year-change",
          "label": "Variable",
          "name": "indexandyearchange"
        }
      ],
      "edition": "time-series",
      "id": "index-private-housing-rental-prices",
      "metadata": {
        "description": "An experimental price index tracking the prices paid for renting property from private landlords in the United Kingdom",
        "last_updated": "2024-02-14T09:54:29.063Z",
        "next_release": "TBC",
        "release_date": "2024-02-14T00:00:00.000Z",
        "release_frequency": "Monthly",
        "state": "published",
        "title": "Index of Private Housing Rental Prices"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "index-private-housing-rental-prices",
          "version": 41
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:07.865713Z",
        "sha256": "bf8269e9f97ba94e434c2ed3178f35f5593a99ef40c68c5c3e07045199f3592a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions/time-series/versions/41/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "continuityEstablished": false,
          "maximumNative": null,
          "minimumNative": null,
          "status": "unknown-unrecognised-or-mixed-period-codes"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "Jan-24",
            "option": "Jan-24"
          },
          {
            "dimension": "time",
            "label": "Dec-23",
            "option": "Dec-23"
          },
          {
            "dimension": "time",
            "label": "Nov-23",
            "option": "Nov-23"
          },
          {
            "dimension": "time",
            "label": "Oct-23",
            "option": "Oct-23"
          },
          {
            "dimension": "time",
            "label": "Sep-23",
            "option": "Sep-23"
          },
          {
            "dimension": "time",
            "label": "Aug-23",
            "option": "Aug-23"
          },
          {
            "dimension": "time",
            "label": "Jul-23",
            "option": "Jul-23"
          },
          {
            "dimension": "time",
            "label": "Jun-23",
            "option": "Jun-23"
          },
          {
            "dimension": "time",
            "label": "May-23",
            "option": "May-23"
          },
          {
            "dimension": "time",
            "label": "Apr-23",
            "option": "Apr-23"
          },
          {
            "dimension": "time",
            "label": "Mar-23",
            "option": "Mar-23"
          },
          {
            "dimension": "time",
            "label": "Feb-23",
            "option": "Feb-23"
          },
          {
            "dimension": "time",
            "label": "Jan-23",
            "option": "Jan-23"
          },
          {
            "dimension": "time",
            "label": "Dec-22",
            "option": "Dec-22"
          },
          {
            "dimension": "time",
            "label": "Nov-22",
            "option": "Nov-22"
          },
          {
            "dimension": "time",
            "label": "Oct-22",
            "option": "Oct-22"
          },
          {
            "dimension": "time",
            "label": "Sep-22",
            "option": "Sep-22"
          },
          {
            "dimension": "time",
            "label": "Aug-22",
            "option": "Aug-22"
          },
          {
            "dimension": "time",
            "label": "Jul-22",
            "option": "Jul-22"
          },
          {
            "dimension": "time",
            "label": "Jun-22",
            "option": "Jun-22"
          },
          {
            "dimension": "time",
            "label": "May-22",
            "option": "May-22"
          },
          {
            "dimension": "time",
            "label": "Apr-22",
            "option": "Apr-22"
          },
          {
            "dimension": "time",
            "label": "Mar-22",
            "option": "Mar-22"
          },
          {
            "dimension": "time",
            "label": "Feb-22",
            "option": "Feb-22"
          },
          {
            "dimension": "time",
            "label": "Jan-22",
            "option": "Jan-22"
          },
          {
            "dimension": "time",
            "label": "Dec-21",
            "option": "Dec-21"
          },
          {
            "dimension": "time",
            "label": "Nov-21",
            "option": "Nov-21"
          },
          {
            "dimension": "time",
            "label": "Oct-21",
            "option": "Oct-21"
          },
          {
            "dimension": "time",
            "label": "Sep-21",
            "option": "Sep-21"
          },
          {
            "dimension": "time",
            "label": "Aug-21",
            "option": "Aug-21"
          },
          {
            "dimension": "time",
            "label": "Jul-21",
            "option": "Jul-21"
          },
          {
            "dimension": "time",
            "label": "Jun-21",
            "option": "Jun-21"
          },
          {
            "dimension": "time",
            "label": "May-21",
            "option": "May-21"
          },
          {
            "dimension": "time",
            "label": "Apr-21",
            "option": "Apr-21"
          },
          {
            "dimension": "time",
            "label": "Mar-21",
            "option": "Mar-21"
          },
          {
            "dimension": "time",
            "label": "Feb-21",
            "option": "Feb-21"
          },
          {
            "dimension": "time",
            "label": "Jan-21",
            "option": "Jan-21"
          },
          {
            "dimension": "time",
            "label": "Dec-20",
            "option": "Dec-20"
          },
          {
            "dimension": "time",
            "label": "Nov-20",
            "option": "Nov-20"
          },
          {
            "dimension": "time",
            "label": "Oct-20",
            "option": "Oct-20"
          },
          {
            "dimension": "time",
            "label": "Sep-20",
            "option": "Sep-20"
          },
          {
            "dimension": "time",
            "label": "Aug-20",
            "option": "Aug-20"
          },
          {
            "dimension": "time",
            "label": "Jul-20",
            "option": "Jul-20"
          },
          {
            "dimension": "time",
            "label": "Jun-20",
            "option": "Jun-20"
          },
          {
            "dimension": "time",
            "label": "May-20",
            "option": "May-20"
          },
          {
            "dimension": "time",
            "label": "Apr-20",
            "option": "Apr-20"
          },
          {
            "dimension": "time",
            "label": "Mar-20",
            "option": "Mar-20"
          },
          {
            "dimension": "time",
            "label": "Feb-20",
            "option": "Feb-20"
          },
          {
            "dimension": "time",
            "label": "Jan-20",
            "option": "Jan-20"
          },
          {
            "dimension": "time",
            "label": "Dec-19",
            "option": "Dec-19"
          },
          {
            "dimension": "time",
            "label": "Nov-19",
            "option": "Nov-19"
          },
          {
            "dimension": "time",
            "label": "Oct-19",
            "option": "Oct-19"
          },
          {
            "dimension": "time",
            "label": "Sep-19",
            "option": "Sep-19"
          },
          {
            "dimension": "time",
            "label": "Aug-19",
            "option": "Aug-19"
          },
          {
            "dimension": "time",
            "label": "Jul-19",
            "option": "Jul-19"
          },
          {
            "dimension": "time",
            "label": "Jun-19",
            "option": "Jun-19"
          },
          {
            "dimension": "time",
            "label": "May-19",
            "option": "May-19"
          },
          {
            "dimension": "time",
            "label": "Apr-19",
            "option": "Apr-19"
          },
          {
            "dimension": "time",
            "label": "Mar-19",
            "option": "Mar-19"
          },
          {
            "dimension": "time",
            "label": "Feb-19",
            "option": "Feb-19"
          },
          {
            "dimension": "time",
            "label": "Jan-19",
            "option": "Jan-19"
          },
          {
            "dimension": "time",
            "label": "Dec-18",
            "option": "Dec-18"
          },
          {
            "dimension": "time",
            "label": "Nov-18",
            "option": "Nov-18"
          },
          {
            "dimension": "time",
            "label": "Oct-18",
            "option": "Oct-18"
          },
          {
            "dimension": "time",
            "label": "Sep-18",
            "option": "Sep-18"
          },
          {
            "dimension": "time",
            "label": "Aug-18",
            "option": "Aug-18"
          },
          {
            "dimension": "time",
            "label": "Jul-18",
            "option": "Jul-18"
          },
          {
            "dimension": "time",
            "label": "Jun-18",
            "option": "Jun-18"
          },
          {
            "dimension": "time",
            "label": "May-18",
            "option": "May-18"
          },
          {
            "dimension": "time",
            "label": "Apr-18",
            "option": "Apr-18"
          },
          {
            "dimension": "time",
            "label": "Mar-18",
            "option": "Mar-18"
          },
          {
            "dimension": "time",
            "label": "Feb-18",
            "option": "Feb-18"
          },
          {
            "dimension": "time",
            "label": "Jan-18",
            "option": "Jan-18"
          },
          {
            "dimension": "time",
            "label": "Dec-17",
            "option": "Dec-17"
          },
          {
            "dimension": "time",
            "label": "Nov-17",
            "option": "Nov-17"
          },
          {
            "dimension": "time",
            "label": "Oct-17",
            "option": "Oct-17"
          },
          {
            "dimension": "time",
            "label": "Sep-17",
            "option": "Sep-17"
          },
          {
            "dimension": "time",
            "label": "Aug-17",
            "option": "Aug-17"
          },
          {
            "dimension": "time",
            "label": "Jul-17",
            "option": "Jul-17"
          },
          {
            "dimension": "time",
            "label": "Jun-17",
            "option": "Jun-17"
          },
          {
            "dimension": "time",
            "label": "May-17",
            "option": "May-17"
          },
          {
            "dimension": "time",
            "label": "Apr-17",
            "option": "Apr-17"
          },
          {
            "dimension": "time",
            "label": "Mar-17",
            "option": "Mar-17"
          },
          {
            "dimension": "time",
            "label": "Feb-17",
            "option": "Feb-17"
          },
          {
            "dimension": "time",
            "label": "Jan-17",
            "option": "Jan-17"
          },
          {
            "dimension": "time",
            "label": "Dec-16",
            "option": "Dec-16"
          },
          {
            "dimension": "time",
            "label": "Nov-16",
            "option": "Nov-16"
          },
          {
            "dimension": "time",
            "label": "Oct-16",
            "option": "Oct-16"
          },
          {
            "dimension": "time",
            "label": "Sep-16",
            "option": "Sep-16"
          },
          {
            "dimension": "time",
            "label": "Aug-16",
            "option": "Aug-16"
          },
          {
            "dimension": "time",
            "label": "Jul-16",
            "option": "Jul-16"
          },
          {
            "dimension": "time",
            "label": "Jun-16",
            "option": "Jun-16"
          },
          {
            "dimension": "time",
            "label": "May-16",
            "option": "May-16"
          },
          {
            "dimension": "time",
            "label": "Apr-16",
            "option": "Apr-16"
          },
          {
            "dimension": "time",
            "label": "Mar-16",
            "option": "Mar-16"
          },
          {
            "dimension": "time",
            "label": "Feb-16",
            "option": "Feb-16"
          },
          {
            "dimension": "time",
            "label": "Jan-16",
            "option": "Jan-16"
          },
          {
            "dimension": "time",
            "label": "Dec-15",
            "option": "Dec-15"
          },
          {
            "dimension": "time",
            "label": "Nov-15",
            "option": "Nov-15"
          },
          {
            "dimension": "time",
            "label": "Oct-15",
            "option": "Oct-15"
          },
          {
            "dimension": "time",
            "label": "Sep-15",
            "option": "Sep-15"
          },
          {
            "dimension": "time",
            "label": "Aug-15",
            "option": "Aug-15"
          },
          {
            "dimension": "time",
            "label": "Jul-15",
            "option": "Jul-15"
          },
          {
            "dimension": "time",
            "label": "Jun-15",
            "option": "Jun-15"
          },
          {
            "dimension": "time",
            "label": "May-15",
            "option": "May-15"
          },
          {
            "dimension": "time",
            "label": "Apr-15",
            "option": "Apr-15"
          },
          {
            "dimension": "time",
            "label": "Mar-15",
            "option": "Mar-15"
          },
          {
            "dimension": "time",
            "label": "Feb-15",
            "option": "Feb-15"
          },
          {
            "dimension": "time",
            "label": "Jan-15",
            "option": "Jan-15"
          },
          {
            "dimension": "time",
            "label": "Dec-14",
            "option": "Dec-14"
          },
          {
            "dimension": "time",
            "label": "Nov-14",
            "option": "Nov-14"
          },
          {
            "dimension": "time",
            "label": "Oct-14",
            "option": "Oct-14"
          },
          {
            "dimension": "time",
            "label": "Sep-14",
            "option": "Sep-14"
          },
          {
            "dimension": "time",
            "label": "Aug-14",
            "option": "Aug-14"
          },
          {
            "dimension": "time",
            "label": "Jul-14",
            "option": "Jul-14"
          },
          {
            "dimension": "time",
            "label": "Jun-14",
            "option": "Jun-14"
          },
          {
            "dimension": "time",
            "label": "May-14",
            "option": "May-14"
          },
          {
            "dimension": "time",
            "label": "Apr-14",
            "option": "Apr-14"
          },
          {
            "dimension": "time",
            "label": "Mar-14",
            "option": "Mar-14"
          },
          {
            "dimension": "time",
            "label": "Feb-14",
            "option": "Feb-14"
          },
          {
            "dimension": "time",
            "label": "Jan-14",
            "option": "Jan-14"
          },
          {
            "dimension": "time",
            "label": "Dec-13",
            "option": "Dec-13"
          },
          {
            "dimension": "time",
            "label": "Nov-13",
            "option": "Nov-13"
          },
          {
            "dimension": "time",
            "label": "Oct-13",
            "option": "Oct-13"
          },
          {
            "dimension": "time",
            "label": "Sep-13",
            "option": "Sep-13"
          },
          {
            "dimension": "time",
            "label": "Aug-13",
            "option": "Aug-13"
          },
          {
            "dimension": "time",
            "label": "Jul-13",
            "option": "Jul-13"
          },
          {
            "dimension": "time",
            "label": "Jun-13",
            "option": "Jun-13"
          },
          {
            "dimension": "time",
            "label": "May-13",
            "option": "May-13"
          },
          {
            "dimension": "time",
            "label": "Apr-13",
            "option": "Apr-13"
          },
          {
            "dimension": "time",
            "label": "Mar-13",
            "option": "Mar-13"
          },
          {
            "dimension": "time",
            "label": "Feb-13",
            "option": "Feb-13"
          },
          {
            "dimension": "time",
            "label": "Jan-13",
            "option": "Jan-13"
          },
          {
            "dimension": "time",
            "label": "Dec-12",
            "option": "Dec-12"
          },
          {
            "dimension": "time",
            "label": "Nov-12",
            "option": "Nov-12"
          },
          {
            "dimension": "time",
            "label": "Oct-12",
            "option": "Oct-12"
          },
          {
            "dimension": "time",
            "label": "Sep-12",
            "option": "Sep-12"
          },
          {
            "dimension": "time",
            "label": "Aug-12",
            "option": "Aug-12"
          },
          {
            "dimension": "time",
            "label": "Jul-12",
            "option": "Jul-12"
          },
          {
            "dimension": "time",
            "label": "Jun-12",
            "option": "Jun-12"
          },
          {
            "dimension": "time",
            "label": "May-12",
            "option": "May-12"
          },
          {
            "dimension": "time",
            "label": "Apr-12",
            "option": "Apr-12"
          },
          {
            "dimension": "time",
            "label": "Mar-12",
            "option": "Mar-12"
          },
          {
            "dimension": "time",
            "label": "Feb-12",
            "option": "Feb-12"
          },
          {
            "dimension": "time",
            "label": "Jan-12",
            "option": "Jan-12"
          },
          {
            "dimension": "time",
            "label": "Dec-11",
            "option": "Dec-11"
          },
          {
            "dimension": "time",
            "label": "Nov-11",
            "option": "Nov-11"
          },
          {
            "dimension": "time",
            "label": "Oct-11",
            "option": "Oct-11"
          },
          {
            "dimension": "time",
            "label": "Sep-11",
            "option": "Sep-11"
          },
          {
            "dimension": "time",
            "label": "Aug-11",
            "option": "Aug-11"
          },
          {
            "dimension": "time",
            "label": "Jul-11",
            "option": "Jul-11"
          },
          {
            "dimension": "time",
            "label": "Jun-11",
            "option": "Jun-11"
          },
          {
            "dimension": "time",
            "label": "May-11",
            "option": "May-11"
          },
          {
            "dimension": "time",
            "label": "Apr-11",
            "option": "Apr-11"
          },
          {
            "dimension": "time",
            "label": "Mar-11",
            "option": "Mar-11"
          },
          {
            "dimension": "time",
            "label": "Feb-11",
            "option": "Feb-11"
          },
          {
            "dimension": "time",
            "label": "Jan-11",
            "option": "Jan-11"
          },
          {
            "dimension": "time",
            "label": "Dec-10",
            "option": "Dec-10"
          },
          {
            "dimension": "time",
            "label": "Nov-10",
            "option": "Nov-10"
          },
          {
            "dimension": "time",
            "label": "Oct-10",
            "option": "Oct-10"
          },
          {
            "dimension": "time",
            "label": "Sep-10",
            "option": "Sep-10"
          },
          {
            "dimension": "time",
            "label": "Aug-10",
            "option": "Aug-10"
          },
          {
            "dimension": "time",
            "label": "Jul-10",
            "option": "Jul-10"
          },
          {
            "dimension": "time",
            "label": "Jun-10",
            "option": "Jun-10"
          },
          {
            "dimension": "time",
            "label": "May-10",
            "option": "May-10"
          },
          {
            "dimension": "time",
            "label": "Apr-10",
            "option": "Apr-10"
          },
          {
            "dimension": "time",
            "label": "Mar-10",
            "option": "Mar-10"
          },
          {
            "dimension": "time",
            "label": "Feb-10",
            "option": "Feb-10"
          },
          {
            "dimension": "time",
            "label": "Jan-10",
            "option": "Jan-10"
          },
          {
            "dimension": "time",
            "label": "Dec-09",
            "option": "Dec-09"
          },
          {
            "dimension": "time",
            "label": "Nov-09",
            "option": "Nov-09"
          },
          {
            "dimension": "time",
            "label": "Oct-09",
            "option": "Oct-09"
          },
          {
            "dimension": "time",
            "label": "Sep-09",
            "option": "Sep-09"
          },
          {
            "dimension": "time",
            "label": "Aug-09",
            "option": "Aug-09"
          },
          {
            "dimension": "time",
            "label": "Jul-09",
            "option": "Jul-09"
          },
          {
            "dimension": "time",
            "label": "Jun-09",
            "option": "Jun-09"
          },
          {
            "dimension": "time",
            "label": "May-09",
            "option": "May-09"
          },
          {
            "dimension": "time",
            "label": "Apr-09",
            "option": "Apr-09"
          },
          {
            "dimension": "time",
            "label": "Mar-09",
            "option": "Mar-09"
          },
          {
            "dimension": "time",
            "label": "Feb-09",
            "option": "Feb-09"
          },
          {
            "dimension": "time",
            "label": "Jan-09",
            "option": "Jan-09"
          },
          {
            "dimension": "time",
            "label": "Dec-08",
            "option": "Dec-08"
          },
          {
            "dimension": "time",
            "label": "Nov-08",
            "option": "Nov-08"
          },
          {
            "dimension": "time",
            "label": "Oct-08",
            "option": "Oct-08"
          },
          {
            "dimension": "time",
            "label": "Sep-08",
            "option": "Sep-08"
          },
          {
            "dimension": "time",
            "label": "Aug-08",
            "option": "Aug-08"
          },
          {
            "dimension": "time",
            "label": "Jul-08",
            "option": "Jul-08"
          },
          {
            "dimension": "time",
            "label": "Jun-08",
            "option": "Jun-08"
          },
          {
            "dimension": "time",
            "label": "May-08",
            "option": "May-08"
          },
          {
            "dimension": "time",
            "label": "Apr-08",
            "option": "Apr-08"
          },
          {
            "dimension": "time",
            "label": "Mar-08",
            "option": "Mar-08"
          },
          {
            "dimension": "time",
            "label": "Feb-08",
            "option": "Feb-08"
          },
          {
            "dimension": "time",
            "label": "Jan-08",
            "option": "Jan-08"
          },
          {
            "dimension": "time",
            "label": "Dec-07",
            "option": "Dec-07"
          },
          {
            "dimension": "time",
            "label": "Nov-07",
            "option": "Nov-07"
          },
          {
            "dimension": "time",
            "label": "Oct-07",
            "option": "Oct-07"
          },
          {
            "dimension": "time",
            "label": "Sep-07",
            "option": "Sep-07"
          },
          {
            "dimension": "time",
            "label": "Aug-07",
            "option": "Aug-07"
          },
          {
            "dimension": "time",
            "label": "Jul-07",
            "option": "Jul-07"
          },
          {
            "dimension": "time",
            "label": "Jun-07",
            "option": "Jun-07"
          },
          {
            "dimension": "time",
            "label": "May-07",
            "option": "May-07"
          },
          {
            "dimension": "time",
            "label": "Apr-07",
            "option": "Apr-07"
          },
          {
            "dimension": "time",
            "label": "Mar-07",
            "option": "Mar-07"
          },
          {
            "dimension": "time",
            "label": "Feb-07",
            "option": "Feb-07"
          },
          {
            "dimension": "time",
            "label": "Jan-07",
            "option": "Jan-07"
          },
          {
            "dimension": "time",
            "label": "Dec-06",
            "option": "Dec-06"
          },
          {
            "dimension": "time",
            "label": "Nov-06",
            "option": "Nov-06"
          },
          {
            "dimension": "time",
            "label": "Oct-06",
            "option": "Oct-06"
          },
          {
            "dimension": "time",
            "label": "Sep-06",
            "option": "Sep-06"
          },
          {
            "dimension": "time",
            "label": "Aug-06",
            "option": "Aug-06"
          },
          {
            "dimension": "time",
            "label": "Jul-06",
            "option": "Jul-06"
          },
          {
            "dimension": "time",
            "label": "Jun-06",
            "option": "Jun-06"
          },
          {
            "dimension": "time",
            "label": "May-06",
            "option": "May-06"
          },
          {
            "dimension": "time",
            "label": "Apr-06",
            "option": "Apr-06"
          },
          {
            "dimension": "time",
            "label": "Mar-06",
            "option": "Mar-06"
          },
          {
            "dimension": "time",
            "label": "Feb-06",
            "option": "Feb-06"
          },
          {
            "dimension": "time",
            "label": "Jan-06",
            "option": "Jan-06"
          },
          {
            "dimension": "time",
            "label": "Dec-05",
            "option": "Dec-05"
          },
          {
            "dimension": "time",
            "label": "Nov-05",
            "option": "Nov-05"
          },
          {
            "dimension": "time",
            "label": "Oct-05",
            "option": "Oct-05"
          },
          {
            "dimension": "time",
            "label": "Sep-05",
            "option": "Sep-05"
          },
          {
            "dimension": "time",
            "label": "Aug-05",
            "option": "Aug-05"
          },
          {
            "dimension": "time",
            "label": "Jul-05",
            "option": "Jul-05"
          },
          {
            "dimension": "time",
            "label": "Jun-05",
            "option": "Jun-05"
          },
          {
            "dimension": "time",
            "label": "May-05",
            "option": "May-05"
          },
          {
            "dimension": "time",
            "label": "Apr-05",
            "option": "Apr-05"
          },
          {
            "dimension": "time",
            "label": "Mar-05",
            "option": "Mar-05"
          },
          {
            "dimension": "time",
            "label": "Feb-05",
            "option": "Feb-05"
          },
          {
            "dimension": "time",
            "label": "Jan-05",
            "option": "Jan-05"
          }
        ],
        "reportedTotal": 229,
        "retrievedUnique": 229,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "41",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions/time-series/versions/41"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-M"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices/editions"
  }
}
---

# Index of Private Housing Rental Prices

An experimental price index tracking the prices paid for renting property from private landlords in the United Kingdom

Native identifier: `index-private-housing-rental-prices`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/index-private-housing-rental-prices)

Update cadence: Monthly.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
