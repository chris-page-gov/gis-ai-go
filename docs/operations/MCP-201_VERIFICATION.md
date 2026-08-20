# MCP-201 shared catalogue contract verification record

- status: complete local candidate gate passed; commit, pull request and
  protected-main verification pending
- reviewed on: 20 August 2026
- work item: [MCP-201](https://github.com/chris-page-gov/gis-ai-go/issues/19)
- protected-main base: `80ac89d89e04751045693cecff4a3a714d121ebe`
- candidate commit: pending
- pull request: pending
- pull-request assurance and CodeQL: pending
- protected-main merge and post-merge assurance: pending

## Outcome

This first MCP-201 slice establishes a shared catalogue contract over the existing
checksum-verified public catalogue. The Explorer adopts that shared core through
thin compatibility adapters, while the candidate request and result schemas define
a bounded foundation for later read-only catalogue delivery.

This candidate does not provide an MCP listener, direct API, provider adapter,
execution path or evidence store. `catalogue.search` and `catalogue.describe` are
not registered, advertised or active. EVID-204 must add and review canonical inline
evidence before either tool can be activated; the candidate result schema therefore
rejects an opaque evidence reference rather than implying persistence or
attestation that does not exist.

## Candidate scope

- the catalogue parser, search, facet, graph, timeline and link helpers are owned by
  the shared contracts package and consumed by the existing Explorer;
- query analysis exposes the 256-code-point and 10-normalised-term boundaries so a
  later network surface can reject over-limit input consistently;
- closed request, result and problem schemas bound catalogue search and description
  inputs, source-native detail values and public record provenance; and
- repository contract validation checks every schema against JSON Schema Draft
  2020-12 and the GIS AI GO URN namespace.

## Complete local candidate evidence

The current working-tree bytes passed the complete locked `pnpm run check` on
20 August 2026. The gate included:

- 19 of 19 shared catalogue contract tests;
- 4 of 4 existing non-networked gateway boundary tests;
- 6 of 6 catalogue API schema tests;
- 16 of 16 Explorer build-policy tests and 42 of 42 Explorer unit and component
  tests;
- 88 of 88 repository Python tests and 2 of 2 execution-boundary tests;
- 27 of 27 real-browser tests;
- two clean locked builds with byte-identical Pages archives, checksum files and
  archive receipts;
- validation of the product version across 8 manifests and locks, 12 schemas and
  53 evaluation records;
- 300 local Markdown links, 183 immutable research hashes, 2 ledger snapshots and
  71 source identifiers;
- a 461-file baseline secret and machine-path scan, 9 rendered diagrams and a
  146-component CycloneDX SBOM;
- the Explorer production build and built ESM contracts-package runtime import;
- confirmation that the immutable research tree is unchanged from the protected-main
  base; and
- an independent current-byte review with a `SHIP` verdict and no P0, P1 or P2
  finding.

These local results do not replace pull-request checks, CodeQL, protected-main
merge or post-merge assurance. Those remote evidence gates remain pending and must
pass before this record can be promoted from a local candidate.

## Activation and publication boundary

No service or new public endpoint is published by this slice. The supported public
product remains the static `v0.1.0` Explorer. A later MCP-201 slice must implement
and test the listener and direct API, while EVID-204 must supply reviewed inline
evidence. Tool advertisement and activation can follow only after those controls
and the applicable security and interoperability gates pass.
