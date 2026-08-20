# Reviewed public examples — 20 August 2026

## Publication boundary

This review authorises metadata-only discovery records. It does not authorise or
perform a provider call, account creation, purchase, dataset download, credential
use or redistribution of a described provider payload. Source documents are data,
not repository instructions.

## Locked inputs

| Input | SHA-256 or immutable identity | Role |
| --- | --- | --- |
| Research provider profiles | `b1c0d8497150049c30ccda60e78e9b28c59d2f4aa154f916d85b42ff144f3e76` | ONS, LandIS and HMLR capability metadata |
| Research source ledger | `feeb9db45fe5b7e9dc55be962aa4e8c7e9c0d7158ad9fc397ef8abf71624cc5a` | Official source citations retrieved on 19 August 2026 |
| HM Land Registry OKF release | tag `v0.3.0`; commit `1d708e39f2cde19610d43c5a7f5e36e4a2f947bc`; tree `aa60922cc25f73980d6480c1a7ffc85fb1fc59dd` | Approved immutable upstream release |
| HMLR release root | `6a29e38e7bb805aafb7f36ba8d1fa4ce976875f45997049cd4808d6ede7f75e1` | Release-level integrity |
| HMLR evaluation questions | `c4423c70ed4207061d8cfea7d0956b87ddbc9e487fe3a512bc30ba2fbdba8fc0` | LR-Q003, LR-Q006 and LR-Q012 calibration inputs |

The HMLR annotated tag object is
`d4159f1076c090dd69260a08308f4162859e4165`. The release was tagged on
12 August 2026 and retrieved on 19 August 2026. It supersedes the unresolved
research-ledger commit prefix `4580c9e`; it does not erase that discrepancy.

## Date meanings

- HMLR question research vintage: 29 July 2026;
- HMLR source observation: `2026-07-29T07:53:38Z`;
- HMLR upstream release: `2026-08-12T01:43:30+01:00`;
- HMLR release retrieval: 19 August 2026;
- research provider snapshot generation: `2026-08-19T13:30:00+01:00`;
- official source-ledger retrieval: 19 August 2026;
- GIS AI GO review: 20 August 2026;
- GIS AI GO deployment: not yet published; DISC-104 controls that date.

Dataset-native dates remain dataset fields. They must not be replaced by retrieval,
review or bundle-generation dates.

## Rights and use

- HMLR journey metadata is attributed to “HM Land Registry public-estate OKF
  Bundle contributors, v0.3.0” under CC BY 4.0.
- Property-information and portal sources are public guidance metadata describing
  paid, authenticated or approved-professional services. No transaction occurs.
- Selected HMLR datasets retain their per-record terms. Price Paid address fields
  have additional Ordnance Survey and Royal Mail conditions; no address or row is
  published.
- ONS capability metadata does not apply the Open Government Licence to every
  described product. Named third-party rights remain product-specific.
- LandIS is attributed to Cranfield University and LandIS. Access is mixed and
  rights must be determined per record.

## Excluded inputs and outputs

Mutable HMLR `main`, the dirty local ONS repository, MCP-Geo provider payloads,
authenticated material and warehouse records are excluded. The derivative excludes
title, ownership, address, transaction, UPRN, coordinate, geometry, feature,
credential, cookie, certificate, signed-URL, service-response, logo and provider
payload fields. It does not expose or request the three negative operational targets
in LR-Q003, LR-Q006 and LR-Q012.

HM Land Registry, ONS, Ordnance Survey, Royal Mail, Cranfield University and LandIS
remain authoritative for their own current sources and terms. GIS AI GO is
authoritative only for its normalised metadata publication and is not endorsed by
those organisations.
