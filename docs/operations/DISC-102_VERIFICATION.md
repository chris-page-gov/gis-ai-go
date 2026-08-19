# DISC-102 Explorer verification record

Verified locally on 19 August 2026. The pull request and squash merge identify the
exact source revision; embedding that future identifier in this change would be
self-referential.

## Outcome

The static public Explorer implements the issue 4 acceptance journey without an
account, provider request, MCP host or WebMCP implementation. Its default route
answers “INSPIRE polygon: indicative or legal boundary?” and states that the
polygons are indicative and do not establish the exact legal extent of a title.

The Explorer publishes metadata only. It contains no property record, address,
real geometry, credential, protected data or legal boundary assertion.

## Source and build integrity

- the only runtime corpus is the deterministic 18-record DISC-101 OKF bundle;
- the build verifies the canonical checksum ledger, complete inventory, regular
  files and byte-for-byte parity before publishing the catalogue projections;
- JSON and JSON-LD expose the same source-native record identifiers;
- production assets use relative paths, contain no source maps or historical
  research pack, and pass a strict static Content Security Policy check;
- the deployed candidate makes same-origin catalogue requests only and has no
  analytics, remote font, tile, service-worker or provider dependency.

## Functional and accessibility assurance

The Explorer package passed TypeScript checking, 16 build-policy tests, 36 unit
and component tests and 18 Chrome browser journeys. The browser suite covers:

- the focused default answer and operation without WebMCP;
- search, six facet groups, direct routes, canonical URLs and browser history;
- keyboard, touch and skip-link operation;
- axe checks on catalogue, graph, timeline and schematic-map views;
- a 320 CSS-pixel reflow viewport, representing a 1,280-pixel layout at 400%
  zoom;
- forced colours and reduced motion;
- graph adjacency, timeline semantics and complete schematic-map text
  alternatives;
- hostile URL and catalogue values, 44-pixel target sizes and the no-JavaScript
  fallback;
- local-only network traffic, a clean browser console and downloadable checksum
  parity.

A separate Playwright CLI review inspected the built default and schematic-map
views at 1,440 by 1,000 CSS pixels. The visual hierarchy, legal caveat, authority
boundary and non-property-map labelling were clear and no layout blocker was
found.

The repository-wide `pnpm run check` gate also passed unchanged after security
remediation. In addition to the Explorer checks, it ran 4 gateway tests, 23
repository tests, 2 execution boundary tests, validation of 8 schemas and 53
records, 279 local Markdown links, 183 immutable research hashes, 2 source-ledger
snapshots and 71 source identifiers.
The baseline secret scan checked 405 text files, 9 diagrams rendered, and the
CycloneDX generator recorded 145 components.

## Security and privacy boundary

Runtime parsing limits input size, depth, record count and string length; rejects
unexpected fields, controls, HTML-like content, unsafe object keys and
non-public classifications; and checks source-reference closure. Search and URL
state are allowlisted, bounded and canonicalised. Dynamic DOM content is created
with text nodes and typed properties, while navigable links must be confined
relative paths or credential-free HTTPS URLs.

The repository security diff review covered every changed runtime, user-interface
and build-assurance file. Its isolated validation initially confirmed one Low
publication-assurance finding: a weakened CSP and different loopback origin could
pass both automated gates. The owner authorised remediation. The final build now
requires the exact CSP and distribution inventory, validates browser-parsed HTML
attribute semantics, compares browser requests with the exact configured origin,
and always starts a fresh candidate preview for browser assurance.

The same review proved two filesystem footguns that were not reportable under the
current attacker model but were still hardened: public and distribution trees must
be regular, symlink-free allowlisted inputs before Vite runs. All local Python
entrypoints also enforce the reviewed `uv.lock`. Sixteen regression tests cover the
validated build patterns, and the complete post-remediation gate passes. This is a
bounded review of DISC-102, not a guarantee that future code or third-party content
is vulnerability-free.

## Publication and rollback

This record verifies a local candidate only. GitHub Pages remains disabled until
DISC-103 source-family review and the DISC-104 immutable deployment gate pass.
Before deployment, rollback is ordinary pull-request reversion. After deployment,
DISC-104 must retain and be able to redeploy the previous checksum-bound build.
