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

For Chrome 152's experimental native WebMCP page API, run the read-only profile
preflight:

```bash
pnpm --filter @gis-ai-go/webmcp-explorer run preflight:chrome
```

It reads Chrome's profile `Last Version` breadcrumb and persisted experiment
overrides. It requires the WebMCP testing opt-in and detects an explicit DevTools
WebMCP disable override; [Chromium enables the DevTools feature by default][1] in
Chrome 152. It reports the native page API and DevTools panel as separate planes,
and recognises Chrome 152 only until another major version has its own observation.
It exits with status 0 when both persisted states are suitable for the full
procedure, 2 when action or version review is required, and 1 when the Chrome state
cannot be read. It does not inspect the running binary, change settings, prove a
relaunch or prove either live surface; those validations remain separate steps.

Manual native-API validation does not need remote debugging. Connecting an external
DevTools or browser-automation agent is a separate integration with access to the
selected browser context. Use a dedicated validation profile or close sensitive
tabs, review its URL and telemetry controls, and grant any connection prompt only
for the bounded test. This preflight neither configures nor proves that integration.

Do not use **Gemini in Chrome** as a substitute for that native-API validation.
[Chrome's WebMCP documentation][2] treats the Model Context Tool Inspector's test agent
as a separate feature from Gemini in Chrome. A Gemini response that can read the
tab but reports no page-tool declarations, followed by no observed tool invocation,
should be recorded as **AI-host bridge not observed** for that session. It does not
disprove the independently verified page registration. Likewise, the presence of a
WebMCP item in DevTools is not evidence of discovery when its content pane is empty.
Record the native `document.modelContext.getTools()` result and an actual bounded
`executeTool()` result independently.

Google's May 2026 announcement says Gemini in Chrome "will soon support" WebMCP
APIs.[3] The current Google help reviewed on 29 August 2026 documents tab sharing
and auto browse, but identifies no WebMCP switch.[4] Do not present the WebMCP
testing flag, tab sharing or **Let Gemini browse for you** as a Gemini-to-WebMCP
switch.

This candidate is not part of the supported GitHub Pages artefact. It uses no model
API key, provider credential, cookie, browser storage, analytics or external runtime
request. The user's supported AI host performs the probabilistic question-to-tool
translation; the page performs deterministic validation and catalogue lookup only.

[1]: https://chromium.googlesource.com/chromium/src/+/1ddb706a3498463d86d39257c243367b2f34947f
[2]: https://developer.chrome.com/docs/ai/webmcp
[3]: https://developer.chrome.com/blog/chrome-at-io26
[4]: https://support.google.com/chrome/answer/16283624?hl=en-GB
