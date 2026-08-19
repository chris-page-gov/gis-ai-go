# ADR-0005: Static public Explorer

- status: accepted
- decided on: 19 August 2026
- work item: DISC-102

## Context

The first public product must let people inspect the governed catalogue without an
account, MCP host, provider credential or optional browser integration. The
checksum-verified OKF bundle is the canonical discovery source. The historical
research viewer is immutable evidence and is not suitable for deployment.

## Decision

Build the Explorer as a progressively enhanced static TypeScript application. Its
production runtime has no third-party JavaScript dependency and makes no provider,
analytics, font, tile or other external request. The build copies the complete,
checksum-verified OKF output without transforming it and fails closed when its
inventory, hashes or public-data envelope are invalid.

Use ordinary query parameters for search, facets and the selected view, and the
source-native record identifier in the URL fragment. Canonicalisation uses browser
history replacement; committed navigation uses history entries. All core journeys
work without WebMCP, storage, cookies or JavaScript-only visual meaning.

The graph derives edges only from explicit `sourceRefs`. Timeline dates retain their
source meaning. The map is a coverage schematic with a complete text alternative,
not real property geometry or a legal boundary. Catalogue values are rendered as
text, and navigable links are limited to HTTPS or safe same-publication paths.

Use a relative application base so the same artefact can be verified locally and
later mounted at the GitHub Pages project path. Publication, hosting headers and the
immutable deployment receipt remain the separate DISC-104 gate.

## Consequences

- the Explorer can be built, tested and archived independently of a server;
- JSON and JSON-LD downloads remain byte-for-byte projections of the canonical OKF
  build;
- visual graph, timeline and schematic views need complete semantic alternatives;
- browser, accessibility, malicious-input, network and built-artefact checks are
  mandatory repository assurance;
- GitHub Pages remains disabled until the publication gate passes.
