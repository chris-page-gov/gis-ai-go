---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/labour-market",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Labour Market",
  "description": "The LFS is a data source compiled from a survey of the UK population. It uses internationally recognised definitions of employment, unemployment and economic activity. It also captures other personal characteristics of household members over the age of 16 such as occupation, education and training. The LFS reflects only a sample of the total population. All cases are therefore weighted on the basis of sub-national population totals by age and sex to give estimates for the entire UK household population. Labour Force Survey estimates have been reweighted for periods from January to March 2019; headline UK seasonally adjusted series prior to this have been modelled, but other series have a discontinuity at this point. The current edition is PWT24, all previous editions have been discontinued.",
  "nativeIdentifier": "labour-market",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:06.199910Z",
      "responseSha256": "b6f46b589138a9c93339c22c50cb14106441f4bf08a0398584a481e01ebe7735",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/29",
      "normalisedRecordSha256": "5fac33834685ae11490109c18654b783eb7b5c1e1a53b2298145ad6d626a9b70",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1"
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
      "label": " ",
      "iri": null,
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "TBD",
    "metadataModified": "2025-06-30T13:14:21.035Z",
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
        "id": "mmm-mmm-yyyy",
        "name": "time"
      },
      {
        "id": "uk-only",
        "name": "geography"
      },
      {
        "id": "unit-of-measure",
        "label": "Unit of measure",
        "name": "unitofmeasure"
      },
      {
        "id": "economic-activity",
        "label": "Economic activity",
        "name": "economicactivity"
      },
      {
        "id": "age-groups",
        "label": "Age groups",
        "name": "agegroups"
      },
      {
        "id": "sex",
        "name": "sex"
      },
      {
        "id": "seasonal-adjustment",
        "label": "Seasonal adjustment",
        "name": "seasonaladjustment"
      }
    ],
    "edition": "PWT24",
    "id": "labour-market",
    "metadata": {
      "description": "The LFS is a data source compiled from a survey of the UK population. It uses internationally recognised definitions of employment, unemployment and economic activity. It also captures other personal characteristics of household members over the age of 16 such as occupation, education and training. The LFS reflects only a sample of the total population. All cases are therefore weighted on the basis of sub-national population totals by age and sex to give estimates for the entire UK household population. Labour Force Survey estimates have been reweighted for periods from January to March 2019; headline UK seasonally adjusted series prior to this have been modelled, but other series have a discontinuity at this point. The current edition is PWT24, all previous editions have been discontinued.",
      "last_updated": "2025-06-30T13:14:21.035Z",
      "next_release": "TBD",
      "release_date": "2025-06-13T00:00:00.000Z",
      "release_frequency": " ",
      "state": "published",
      "title": "UK Labour Market"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "PWT24",
        "id": "labour-market",
        "version": 1
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:06.199910Z",
      "sha256": "b6f46b589138a9c93339c22c50cb14106441f4bf08a0398584a481e01ebe7735",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1/metadata"
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
          "label": "Feb-Apr 2025",
          "option": "feb-apr-2025"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2025",
          "option": "jan-mar-2025"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2025",
          "option": "dec-feb-2025"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2025",
          "option": "nov-jan-2025"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2024",
          "option": "oct-dec-2024"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2024",
          "option": "sep-nov-2024"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2024",
          "option": "aug-oct-2024"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2024",
          "option": "jul-sep-2024"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2024",
          "option": "jun-aug-2024"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2024",
          "option": "may-jul-2024"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2024",
          "option": "apr-jun-2024"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2024",
          "option": "mar-may-2024"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2024",
          "option": "feb-apr-2024"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2024",
          "option": "jan-mar-2024"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2024",
          "option": "dec-feb-2024"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2024",
          "option": "nov-jan-2024"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2023",
          "option": "oct-dec-2023"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2023",
          "option": "sep-nov-2023"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2023",
          "option": "aug-oct-2023"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2023",
          "option": "jul-sep-2023"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2023",
          "option": "jun-aug-2023"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2023",
          "option": "may-jul-2023"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2023",
          "option": "apr-jun-2023"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2023",
          "option": "mar-may-2023"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2023",
          "option": "feb-apr-2023"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2023",
          "option": "jan-mar-2023"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2023",
          "option": "dec-feb-2023"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2023",
          "option": "nov-jan-2023"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2022",
          "option": "oct-dec-2022"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2022",
          "option": "sep-nov-2022"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2022",
          "option": "aug-oct-2022"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2022",
          "option": "jul-sep-2022"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2022",
          "option": "jun-aug-2022"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2022",
          "option": "may-jul-2022"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2022",
          "option": "apr-jun-2022"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2022",
          "option": "mar-may-2022"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2022",
          "option": "feb-apr-2022"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2022",
          "option": "jan-mar-2022"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2022",
          "option": "dec-feb-2022"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2022",
          "option": "nov-jan-2022"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2021",
          "option": "oct-dec-2021"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2021",
          "option": "sep-nov-2021"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2021",
          "option": "aug-oct-2021"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2021",
          "option": "jul-sep-2021"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2021",
          "option": "jun-aug-2021"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2021",
          "option": "may-jul-2021"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2021",
          "option": "apr-jun-2021"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2021",
          "option": "mar-may-2021"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2021",
          "option": "feb-apr-2021"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2021",
          "option": "jan-mar-2021"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2021",
          "option": "dec-feb-2021"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2021",
          "option": "nov-jan-2021"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2020",
          "option": "oct-dec-2020"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2020",
          "option": "sep-nov-2020"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2020",
          "option": "aug-oct-2020"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2020",
          "option": "jul-sep-2020"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2020",
          "option": "jun-aug-2020"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2020",
          "option": "may-jul-2020"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2020",
          "option": "apr-jun-2020"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2020",
          "option": "mar-may-2020"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2020",
          "option": "feb-apr-2020"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2020",
          "option": "jan-mar-2020"
        },
        {
          "dimension": "time",
          "label": "Dec-Feb 2020",
          "option": "dec-feb-2020"
        },
        {
          "dimension": "time",
          "label": "Nov-Jan 2020",
          "option": "nov-jan-2020"
        },
        {
          "dimension": "time",
          "label": "Oct-Dec 2019",
          "option": "oct-dec-2019"
        },
        {
          "dimension": "time",
          "label": "Sep-Nov 2019",
          "option": "sep-nov-2019"
        },
        {
          "dimension": "time",
          "label": "Aug-Oct 2019",
          "option": "aug-oct-2019"
        },
        {
          "dimension": "time",
          "label": "Jul-Sep 2019",
          "option": "jul-sep-2019"
        },
        {
          "dimension": "time",
          "label": "Jun-Aug 2019",
          "option": "jun-aug-2019"
        },
        {
          "dimension": "time",
          "label": "May-Jul 2019",
          "option": "may-jul-2019"
        },
        {
          "dimension": "time",
          "label": "Apr-Jun 2019",
          "option": "apr-jun-2019"
        },
        {
          "dimension": "time",
          "label": "Mar-May 2019",
          "option": "mar-may-2019"
        },
        {
          "dimension": "time",
          "label": "Feb-Apr 2019",
          "option": "feb-apr-2019"
        },
        {
          "dimension": "time",
          "label": "Jan-Mar 2019",
          "option": "jan-mar-2019"
        }
      ],
      "reportedTotal": 74,
      "retrievedUnique": 74,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "1",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1"
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": " "
  }
}
---

# UK Labour Market

The LFS is a data source compiled from a survey of the UK population. It uses internationally recognised definitions of employment, unemployment and economic activity. It also captures other personal characteristics of household members over the age of 16 such as occupation, education and training. The LFS reflects only a sample of the total population. All cases are therefore weighted on the basis of sub-national population totals by age and sex to give estimates for the entire UK household population. Labour Force Survey estimates have been reweighted for periods from January to March 2019; headline UK seasonally adjusted series prior to this have been modelled, but other series have a discontinuity at this point. The current edition is PWT24, all previous editions have been discontinued.

Native identifier: `labour-market`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/labour-market/editions/PWT24/versions/1)

Update cadence:  .
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
