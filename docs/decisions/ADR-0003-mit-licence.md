# ADR-0003: MIT licence

- status: accepted
- decided on: 19 August 2026
- decision maker and copyright holder: Chris Page

## Context

The repository was created locally without a reuse grant while ownership and the
scope of the supplied research pack were confirmed. Chris Page has confirmed that
the code, documentation, schemas and research were produced personally, on personal
time and equipment, and that no employer or other organisation has a copyright claim.
The intent is to allow broad reuse with minimal conditions through a familiar
open-source licence.

## Decision

License all original GIS AI GO code and associated documentation under the MIT
licence, copyright © 2026 Chris Page. This grant includes the original research ZIP,
its checksum-bound extracted copy and live adaptations in this repository.

The root `LICENSE` file is the authoritative licence text. The historical research
pack remains byte-for-byte unchanged; an external grant can license that content
without rewriting or invalidating its evidence files.

## Boundaries

- The MIT licence does not relicense third-party dependencies or material reached
  through external source links.
- Source names, trade marks, provider data and separately licensed material retain
  their own rights and conditions.
- The licence grants copyright permission and disclaims warranty; it does not
  represent name or trade mark clearance.
- Selecting a licence does not itself authorise remote publication or Stage 1.

## Consequences

Repository and package metadata use the SPDX identifier `MIT`. Contributors provide
their submissions under the same licence. The open-source licence gate is resolved;
the publication, name-clearance and later-stage gates remain separate decisions.
