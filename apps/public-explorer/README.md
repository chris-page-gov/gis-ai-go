# Public Explorer

The Explorer is a static, progressively enhanced view of the generated public OKF
bundle. It makes no provider request and needs no account, credential, MCP host or
WebMCP implementation.

Build from the repository root so the checksum-verified catalogue is generated and
copied into the static application:

```bash
pnpm run build:explorer
```

Generated catalogue files and browser reports are ignored. The GitHub Pages
publication gate packages only the checked `dist/` tree with deterministic
provenance, receipt, checksums and SBOM. It never publishes the repository root or
immutable research viewer, and deployment verifies and reuses that exact artefact
without rebuilding it.

Before Vite runs, the build rejects symlinked or special-file public and distribution
trees and requires the exact checksum-derived public inventory. The finished
distribution must contain only referenced assets and the byte-identical catalogue,
and its Content Security Policy must match the reviewed directive set exactly.

## Runtime and URL boundary

The application has no production runtime dependency and makes only same-origin
requests for its static assets and verified catalogue. It does not use cookies,
browser storage, analytics, map tiles, provider APIs or WebMCP.

Search and selected facets use the query string. The selected view uses `view`, and
the source-native record identifier uses `#record=…`. Supported facets are `type`,
`authority`, `access`, `rights`, `freshness` and `tag`; unknown or oversized state is
discarded with a visible warning. Search is limited to the governed record fields and
an explicit allowlist of question and provider-capability details. It does not index
arbitrary nested details, rights conditions or forbidden-target notes. The graph
contains only explicit `sourceRefs`, and the coverage schematic contains no real
geometry or legal boundary.

Run the focused checks with:

```bash
pnpm --filter @gis-ai-go/public-explorer run typecheck
pnpm --filter @gis-ai-go/public-explorer run test:unit
pnpm run test:browser
```

After an accepted Pages deployment, the separate live suite uses explicit expected
publication identities:

```bash
PUBLIC_BASE_URL=https://chris-page-gov.github.io/gis-ai-go/ \
EXPECTED_SOURCE_COMMIT=SOURCE_COMMIT \
EXPECTED_ARCHIVE_SHA256=ARCHIVE_SHA256 \
EXPECTED_OKF_CONTENT_ROOT=OKF_CONTENT_ROOT \
EXPECTED_PAYLOAD_ROOT=PAYLOAD_ROOT \
EXPECTED_PUBLIC_CHECKSUMS_SHA256=PUBLIC_CHECKSUMS_SHA256 \
EXPECTED_VERSION=VERSION \
pnpm --filter @gis-ai-go/public-explorer run test:public
```
