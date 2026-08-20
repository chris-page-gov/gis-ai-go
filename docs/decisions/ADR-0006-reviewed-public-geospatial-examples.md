# ADR-0006: Reviewed public geospatial examples

- status: accepted
- decided on: 20 August 2026
- work item: DISC-103

## Context

The public discovery product needs useful examples from HM Land Registry, the
Office for National Statistics and LandIS without importing provider payloads or
repeating the completed research. Rights, access and dates differ by source. A
public landing page does not make every described service or dataset open.

The research pack records an unresolved HM Land Registry commit prefix. The local
source repository contains an approved immutable `v0.3.0` release with a verified
tag, commit, tree and release-root digest.

## Decision

Generate the examples only from checksum-locked research snapshots and selected
files from HM Land Registry OKF release `v0.3.0`. Record that release as the
superseding source identity; do not import mutable repository branches.

Represent LR-Q003, LR-Q006 and LR-Q012 as non-executing discovery workflows. They
preserve source-native identifiers, positive official sources, expected
propositions and mandatory caveats, but do not expose or invoke their negative
operational targets. Provider records describe capabilities only.

Treat the published catalogue records as public metadata. Preserve described-source
access and rights separately:

- paid, authenticated and professional HM Land Registry services remain restricted;
- selected HMLR datasets retain their per-record licence and attribution;
- ONS products use the Open Government Licence only where the product says so and
  retain named third-party conditions;
- LandIS remains mixed access with rights determined per record and no blanket open
  assertion.

Keep source observation, upstream release, retrieval, GIS AI GO review and eventual
deployment dates distinct. The Explorer remains a discovery aid and must never
present indicative geometry as an exact legal boundary.

## Consequences

- source locks, record digests, rights review and forbidden-target checks are part
  of deterministic build assurance;
- the output contains no property, address, transaction, credential, service
  response, provider dataset or real geometry payload;
- provider names and source citations do not imply endorsement;
- live provider adapters remain outside `v0.1.0`;
- GitHub Pages remains disabled until DISC-104 verifies and deploys an immutable
  artefact.
