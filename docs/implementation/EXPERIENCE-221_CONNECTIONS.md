# EXPERIENCE-221: available facilities and AI connections

Reviewed: 2 October 2026. Baseline: `387e86695e7002e78f005e972703f5c5e51fa546`.
The tables describe the baseline before this increment's deployment acceptance.
Later acceptance must name the deployed version and tested client; a new route
or an installed plugin is not evidence of a successful authenticated tool call.

## What works, and where

There are several separate products and experiments. The public Explorer finds
and explains catalogue records. The accepted local MCP edition uses approved
cached data. The private Sites pilot queries a small, explicit set of live OS and
ONS services. OKF+ searches a much broader local collection of descriptions and
schemas. These scopes are not interchangeable.

| Surface | Available facility | Current boundary |
| --- | --- | --- |
| [Public Explorer](https://chris-page-gov.github.io/gis-ai-go/) | Public catalogue search, source/rights information, cards, graph, timeline, map and downloads. | Supported `v0.1.0` static product. Its map displays catalogue geography; it is not a general uploaded-data analysis map. |
| LOCAL-212/214 | Five MCP tools and three resource interfaces at `http://127.0.0.1:8787/mcp`. | Accepted local runtime; approved cache only, no provider egress. A cloud connector cannot reach this loopback address. |
| WEB-216 local workbench | Manual journey, four page tools and three captured-CPIH MCP tools at `http://127.0.0.1:8788/mcp`. | A separately launched experiment with January/July 2026 captured values and durable local receipts. |
| WebMCP Explorer candidate | Two page-scoped metadata tools plus their manual controls. | Requires a capable browser/host for AI calls. It is distinct from remote MCP and from the supported Pages artefact. |
| [Private Sites pilot](https://gis-ai-go-webmcp-explorer.crpage.chatgpt.site/pilot) | Six live-data/profile/evidence tools behind the owner-private Site; manual page at `/pilot`, guarded MCP at `/pilot/mcp`. | Version 7. Prior direct-wire and owner-browser observations passed; native plugin/OAuth and Claude acceptance remain unproved. |
| OKF+ | Local metadata/schema search, concept and lifecycle discovery, evidence projection, coverage and export. | 30,833 retained records. Catalogue completeness is not established; broader metadata does not add live tools. No accepted installed Ask OKF route. |

The [hosted observation](SITES-218_HOSTED_OBSERVATION.md) retains the version 7
provider, protocol, performance and rollback evidence. The
[local workbench README](../../apps/public-data-workbench/README.md),
[WebMCP README](../../apps/webmcp-explorer/README.md),
[local launcher](../../apps/mcp-gateway/src/local-candidate-main.ts) and
[OKF+ integration boundary](OKF-220_ASK_OKF_INTEGRATION.md) define the other scopes.

## Exact callable feature denominator

Count each advertised operation once within its profile. There are **20 tool
entries across five profiles and three local resource interfaces** in this
baseline. Reusing an operation through a manual control or adding `/mcp` as a
second mount does not create another tool. Resource templates are interfaces,
not counts of every possible returned record. Do not add these counts together
and advertise a single 23-operation hosted server.

| Profile | Exact operation | Source or data | User-facing purpose and limit |
| --- | --- | --- | --- |
| Local five-tool MCP | `catalogue.search` | Checksum-verified public OKF catalogue | Find candidate sources; a catalogue match is not retrieved data. |
| Local five-tool MCP | `catalogue.describe` | One public catalogue record and linked metadata | Explain source, rights, access and limitations. |
| Local five-tool MCP | `selection.resolve` | Closed reviewed ONS selection contract | Review exactly what will be requested; a plan is not permission. |
| Local five-tool MCP | `data.query` | Approved `weekly-deaths-region`, `time-series`, version `121` cache | Read the admitted aggregate observation; it does not query arbitrary ONS datasets. |
| Local five-tool MCP | `evidence.inspect` | Local evidence ledger | Inspect the retained receipt, including recovery by request key; original result material is not replayed. |
| Local resource | `gis-ai-go://catalogue/public` | Public OKF catalogue | Read the available catalogue. |
| Local resource | `gis-ai-go://catalogue/records/{record_id}` | Public catalogue record | Read a known source record. |
| Local resource | `gis-ai-go://evidence/receipts/{receipt_id}` | Local public evidence record | Read evidence for a known completed request. |
| Captured-CPIH MCP | `web216_cpih_select` | Fixed L522/MM23 January/July 2026 capture contract | Review the selected month. |
| Captured-CPIH MCP | `web216_cpih_query` | Validated ONS capture | Return one captured index level and persist evidence; no live refresh. |
| Captured-CPIH MCP | `web216_cpih_inspect` | Captured-CPIH evidence store | Return the stored result and receipt. |
| WebMCP Explorer | `explorer_search_catalogue` | Public catalogue metadata | Update visible search results using validated text/facets. |
| WebMCP Explorer | `explorer_describe_record` | Public catalogue metadata | Open a source record on the page; no durable gateway receipt. |
| Workbench page | `workbench_find_data` | Seven frozen OKF-led metadata projections | Find and display candidates from bounded English keywords. |
| Workbench page | `workbench_review_cpih_selection` | Captured-CPIH MCP | Stage the reviewed January/July plan on the page. |
| Workbench page | `workbench_retrieve_cpih_and_store_receipt` | Captured-CPIH MCP | Display the captured observation and its new stored receipt. |
| Workbench page | `workbench_inspect_receipt` | Captured-CPIH MCP | Display existing evidence, including after restart. |
| Private Sites MCP | `sites_capabilities` | Server-authored profile and limits | Explain what is available and unsupported; no provider call. |
| Private Sites MCP | `sites_os_names` | OS Names API, `/search/names/v1/find` | Up to five Great Britain named-place candidates. Points are not addresses or boundaries; preserve ambiguity. |
| Private Sites MCP | `sites_os_open_product` | OS Downloads API, `/downloads/v1/products/{product}` | Product metadata for `OpenNames`, `OpenUPRN` or `LIDS`; no dataset download. |
| Private Sites MCP | `sites_ons_areas` | ONS ArcGIS `MSOA_DEC_2021_EW_NC_v3`, layer 0 | Up to five England/Wales MSOA 2021 names and codes by prefix; no point containment or population. |
| Private Sites MCP | `sites_ons_cpih` | Maintained ONS L522/MM23 discovery and data endpoints | One or two monthly CPIH index levels; index-point difference and relative change are not automatically published inflation rates. |
| Private Sites MCP | `sites_evidence_inspect` | Pilot D1 evidence store | Read a saved successful result by receipt ID; no provider refresh or new receipt. |

Executable definitions:
[local tools/resources](../../apps/mcp-gateway/src/mcp-server.ts),
[local approved cache](../../providers/ons/data-query-approved-cache.v1.json),
[captured-CPIH MCP](../../apps/mcp-gateway/src/web216-cpih-mcp.ts),
[Explorer page tools](../../apps/webmcp-explorer/src/webmcp-adapter.ts),
[workbench page tools](../../apps/public-data-workbench/src/webmcp.ts),
[Sites inputs and limits](../../apps/mcp-gateway/src/sites-pilot-http.ts),
[Sites provider requests](../../packages/provider-adapter-sdk/src/sites-pilot-providers.ts).

## UI and local knowledge facilities to include in coverage

Tool coverage alone is insufficient. The experience inventory must also cover:

- Public Explorer: text search; six facet groups (type, authority, access, rights,
  freshness, tags); clear/reset; card list and record detail; related-record graph;
  dated-event timeline; catalogue map; source links and limitations; URL-linked
  selected state/back navigation; catalogue/provenance downloads; empty, invalid
  route and failed-load states. These are implemented in
  [the Explorer controller](../../apps/public-explorer/src/main.ts) and its views.
- Private pilot: operation selection; operation-specific inputs; run/cancel and
  busy/error states; bounded candidate tables; source dates and attribution;
  evidence inspection; machine-readable result details. The
  [manual pilot page](../../sites/private-pilot/app/pilot/page.tsx) calls the same
  six operations; it does not register page tools or embed a voice model.
- Captured workbench: discovery cards, selection review, retrieval, receipt
  inspection and result download. Capture date, index units, changed selection
  and an unavailable server require explicit explanations.
- OKF+: metadata search; bounded context projection; schema fields and native
  codes; concept definitions; temporal coverage; update/release locations;
  source provenance and rights; explicit coverage gaps; verification and
  reproducible exports. See [OKF+ usage](../../okf-plus/README.md) and
  [search](../../scripts/okf_plus/search.py). These are local knowledge facilities,
  not newly advertised MCP tools or proof of complete OS/ONS inventory.

The new experience catalogue should identify each UI function and its error and
unsupported states separately. A percentage is meaningful only against its
versioned list; language/persona examples, execution results and independent
human evaluation are separate coverage measures.

## Can Claude connect?

**Claude supports this type of remote MCP server. A working Claude connection to
this private Site has not yet been demonstrated.** Claude's custom connectors
originate in Anthropic's cloud, including when configured in its desktop app.
Consequently the local `127.0.0.1` endpoint and a successful owner-browser login
do not prove remote reachability or OAuth compatibility.
[Claude connection guidance](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

Claude documents Streamable HTTP, OAuth, tools/resources/prompts and optional MCP
Apps. Its documented OAuth versions include `2025-06-18` and `2025-11-25`, which
overlap the pilot's recorded protocol checks. Its hosted tool-result limit is
approximately 150,000 characters, below this server's one-megabyte wire ceiling;
real responses must therefore be measured. Compatibility still needs actual
discovery, authentication and a tool call. The existing pilot offers JSON/text
results and no MCP App UI resource.
[Claude server requirements](https://claude.com/docs/connectors/building).

### Fresh platform observation

A read-only `get_site` call on 2 October returned active version 7, custom access
and zero external visitors. Requesting `include_mcp_connection: true` returned:
“The published Site does not declare an MCP server. Enable MCP and republish it.”
No token, identity, audience, connection or deployment was changed by this check.
The previous missing-declaration diagnosis is therefore still true for version 7.

The installed official Sites MCP skill, bundle `0.1.75`, now specifies the missing
contract: add `mcp` to `.openai/hosting.json` capabilities and expose stateless
HTTP `POST /mcp`. Sites supplies OAuth and trusted identity headers. This is new
documented implementation guidance; it does not retroactively validate version 7.

### Minimal native registration increment

The [private pilot overlay](../../sites/private-pilot/README.md) now adds an exact
`/mcp` mount beside `/pilot/mcp`. Both use the same six-tool application, D1 store,
provider admission and receipts. The native mount accepts only Sites-authenticated
identity; it does not turn a private application test token into a user. The
ordinary pilot route retains its explicitly authorised test mechanism. Paths are
authored in the wrapper and checked by the existing handler, never rewritten from
untrusted input. The two mounts share one two-request isolate limit; durable provider and
receipt ceilings remain shared.

Acceptance steps are sequential:

1. Build and test the exact overlay with the preserved audience, source binding,
   SQL history and merged hosting capability. Verify both routes and shared
   evidence/allowance state using the built Worker probe.
2. Publish the saved exact private version. Retrieve the native connection
   settings using `get_site(include_mcp_connection: true)` and preserve returned
   values verbatim.
3. Reuse the Sites-provisioned App/plugin. Offer its returned plugin ID through
   `plugin_management.suggest_plugins`; after connection, call
   `sites_capabilities` before any live provider operation. Do not create a second
   App, invent OAuth or configure a replacement local MCP integration.
4. Separately verify Claude's supported OAuth discovery and client registration,
   then its actual read-only capability call and bounded provider/evidence journey.
   Record client/version, consent and result limits. If Sites does not admit
   Claude's client, retain this as an interoperability gap; do not remove access
   control or distribute the test token to make the demonstration appear to pass.

The seven tests in
[`test_sites_native_mount.mjs`](../../tests/interoperability/test_sites_native_mount.mjs)
passed locally against the real compiled MCP handler with synthetic identity.
They check tool parity, native test-token refusal, identity/origin/method guards,
exact paths, binding conflict and disabled/mismatched configuration without a
provider or database call. The expanded
[built Worker probe](../../scripts/test_sites_pilot_built_worker.mjs) additionally
requires both mounts to inspect identical receipts and honour the same stopped
allowance across restart. Its execution belongs to assembled-build acceptance;
neither test establishes hosted OAuth or Claude use.

## Proposed facilities are not current capabilities

Voice-driven selection and presentation, persistent JIT explanations, general
file/folder/archive/URL ingestion, arbitrary spatial analysis, uploaded office
documents, general ONS retrieval, hosted NGD and interactive MCP App views need
their own admitted schemas, implementation, examples and acceptance. Existing
metadata about a file format or NGD collection does not implement its parser or
authorise its contents. Keep these entries visible as proposed or blocked until
their exact working scope is proved.
