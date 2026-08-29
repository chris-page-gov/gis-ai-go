# WebMCP Explorer candidate

This standalone static application demonstrates how a supported browser-hosted AI
can translate a person's question into two bounded page-tool calls over the same
generated public OKF catalogue used by GIS AI GO:

- `explorer_search_catalogue` maps to the shared `catalogue.search` semantics; and
- `explorer_describe_record` maps to the shared `catalogue.describe` intent.

The WebMCP names are deliberately different from the canonical MCP operations. A
page result has no gateway policy decision, durable receipt, provider execution or
lost-response reconciliation and must not be presented as the MCP 2026-07-28
gateway result contract.

The application feature-detects `document.modelContext.registerTool` and registers
only after the same checksum-copied catalogue passes the shared bounded parser. The
complete manual demonstration remains available when WebMCP is unsupported. Tool
metadata is static; inputs are validated again in executable code; results are
compact structured public metadata and are marked read-only and untrusted.

Build and test from the repository root:

```bash
pnpm run build:webmcp-explorer
pnpm run test:webmcp-explorer
pnpm run test:webmcp-browser
```

This candidate is not part of the supported GitHub Pages artefact. It uses no model
API key, provider credential, cookie, browser storage, analytics or external runtime
request. The user's supported AI host performs the probabilistic question-to-tool
translation; the page performs deterministic validation and catalogue lookup only.
