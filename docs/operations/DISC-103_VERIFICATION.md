# DISC-103 verification record

- status: implementation candidate
- reviewed on: 20 August 2026
- work item: DISC-103
- publication: none; GitHub Pages remains disabled

## Outcome

DISC-103 adds checksum-locked, metadata-only HM Land Registry, ONS and LandIS
examples to the canonical OKF build and Explorer. It adds no live provider adapter,
credential, property record, transaction, dataset payload or real geometry.

## Source and rights gate

The exact inputs, immutable HMLR release, date meanings, rights treatment and
excluded fields are recorded in the
[reviewed source ledger](../source-ledger/reviewed-public-examples-2026-08-20.md).
The deterministic builder must fail on a digest mismatch, unknown or mixed rights
presented as open, unresolved source, missing mandatory caveat or forbidden target.
The four upstream HMLR files used by the projection or copied into its rights
notices are bound to builder-owned v0.3.0 digests as well as the complete editable
source-lock inventory.

## Functional gate

The final candidate must prove:

- LR-Q003 retrieves the online-copy versus official-copy distinction and correct
  public guidance without invoking a restricted ordering route;
- LR-Q006 retrieves the documented index-map recovery route without treating source
  code or address retrying as the official process;
- LR-Q012 retains the indicative, non-legal conclusion and source evidence;
- Price Paid displays its date, licence, attribution and address-field conditions
  without publishing a row or address;
- ONS exposes two non-executing capability records;
- LandIS visibly retains mixed access and per-record rights;
- the existing accessibility, security, clean-console and no-external-request
  journeys continue to pass.

## Local candidate evidence

The complete `pnpm run check` gate passed on 20 August 2026 against the uncommitted
candidate based on protected `main` at
`6984f3097cff578f0d22088ca8582ebe55725115`:

- 36 deterministic records: 1 bundle, 3 datasets, 4 providers, 24 sources and
  4 workflows;
- 4 gateway tests, 16 Explorer build-policy tests, 39 Explorer unit and component
  tests, 31 repository Python tests and 2 execution-boundary tests;
- 25 real-browser journeys, including 7 reviewed-example journeys and the existing
  WCAG, keyboard, touch, forced-colour, reduced-motion and clean-console coverage;
- 8 schemas and 53 evaluation records validated;
- 286 local links, 183 immutable research hashes, 2 source-ledger snapshots and
  71 source identifiers checked;
- 429 text files scanned without a baseline secret or machine-path match;
- 9 diagrams rendered and a 145-component CycloneDX SBOM generated.

The final security diff scan covered all six changed runtime and source surfaces.
It dynamically confirmed one low-severity provenance weakness: coordinated edits
to upstream HMLR files and the editable source lock could retain the asserted
v0.3.0 identity. Builder-owned release digests and coordinated source, rights,
licence and lock mutation regressions now close that path; the complete gate above
passed after the fix.

A fixed-revision determinism probe produced content root
`b47c97efdb8efe9b3782244406eba32a8b0b765b0df7aef943b0e6fc1c2a305d`.
The release content root is intentionally not claimed here: the build receipt binds
the Git revision, so DISC-104 and the release gate must record the exact merged
revision and its corresponding artefact root.

The pull-request head, remote assurance and CodeQL evidence must be added before
merge. This candidate has not been deployed or released.

## Rollback

Before deployment, rollback is an ordinary reversion of the DISC-103 pull request.
DISC-104 must publish only a checksum-bound artefact built after this gate and retain
the prior deployable Explorer candidate.
