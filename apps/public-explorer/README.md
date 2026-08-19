# Public Explorer

The Explorer is a static, progressively enhanced view of the generated public OKF
bundle. It makes no provider request and needs no account, credential, MCP host or
WebMCP implementation.

Build from the repository root so the checksum-verified catalogue is generated and
copied into the static application:

```bash
pnpm run build:explorer
```

Generated catalogue files and browser reports are ignored. The eventual GitHub Pages
workflow publishes only `dist/`, never the repository root or immutable research
viewer. Deployment remains outside DISC-102.

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
discarded with a visible warning. The graph contains only explicit `sourceRefs`, and
the coverage schematic contains no real geometry or legal boundary.

Run the focused checks with:

```bash
pnpm --filter @gis-ai-go/public-explorer run typecheck
pnpm --filter @gis-ai-go/public-explorer run test:unit
pnpm run test:browser
```
