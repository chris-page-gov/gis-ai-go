# Live-host evidence boundary

This directory contains reviewed, public-safe summaries of bounded interoperability
sessions. A summary may contain non-secret tunnel and app identifiers, public query
terms, result identities, timings, byte counts and SHA-256 digests.

It must not contain raw prompts, complete tool arguments or results, credentials,
headers, environment values, personal data, local absolute paths, conversation URLs
or licensed feature payloads. Detailed JSONL and tunnel-client logs remain local and
operator-controlled. ChatGPT and Codex session summaries bind the exact runtime
harness files used for their runs. An earlier readiness-only summary may instead
identify its pre-final wrapper generation and must not imply that current harness
bytes were exercised. A separately labelled evaluation-corpus digest may identify
the current reviewed case set, but must state that the corpus was not a live-session
runtime input.

Independent-host readiness summaries may preserve versions, bounded classifications,
event counts, timings and digests after disposable profiles are removed. They must
distinguish readiness from capability, record zero-traffic outcomes honestly and state
whether the exact current telemetry wrapper was exercised.

The [`Codex CLI readiness summary`](codex-cli-2026-08-20.json) records the isolated
non-interactive host attempt separately from the earlier three-host readiness summary.
It binds the exact corpus case and current wrapper bytes, but remains `not_ready` and
unscored because protocol negotiation stopped before a task-level tool call.

The
[`Claude Code protected-main legacy STDIO readiness summary`](claude-code-legacy-stdio-readiness-2026-08-23.json)
is a later, separately source-bound record. It captures a clean, detached checkout
of protected-main commit `30b575beb27ff805745a2864c1acf44392774046` and the
current telemetry wrapper. Claude Code `2.1.204` completed legacy STDIO
initialisation and `tools/list` through the constructor-only two-tool conformance
launcher. The result is transport `ready` and capability `unscored`: no
model authentication, model task, tool call, resource read, live provider, remote HTTP
host, exact-five production assembly, registration, activation, deployment or
release was exercised. It does not alter the earlier modern-only `not_ready` record
or upgrade the uncommitted exploratory fallback record.

The later
[`Claude Code 2.1.241 STDIO observation`](claude-code-2.1.241-stdio-observation-2026-08-24.json)
preserves that historical record and binds two new credential-free `mcp list`
attempts to exact protected-main commit
`dda0eb9f776e64bcd45069e77b4acbcd4d495e01`. The current client offered MCP
`2025-11-25`, so the canonical `2026-07-28` surface correctly returned `-32022`.
The separately named constructor-only fallback completed initialisation and
`tools/list`. This establishes only fallback transport readiness: the strict modern
path is not ready, capability is unscored and the independent-host gate remains
incomplete. Raw telemetry and disposable profiles remain private and local.

The subsequent
[`Claude Code 2.1.241 strict-modern STDIO readiness summary`](claude-code-2.1.241-modern-stdio-readiness-2026-08-25.json)
records a fresh, credential-free `mcp list` observation from clean, detached,
protected-main commit `c679b6fd8fb702572da11043d492c3e9e953ad7a`. With the
documented v2 runtime and automatic STDIO negotiation selected, Claude completed a
contract-valid MCP `2026-07-28` `server/discover` probe and a separate successful
`tools/list` session. Both sessions passed independent offline replay with zero
provider calls, pending requests, anomalies or stderr, and no observer or fixture
process remained. This establishes strict-modern transport readiness only:
capability is unscored, the exact-five operation journey was not exercised and no
model, provider, remote HTTP host, registration, activation, deployment or release
was used. The 24 August default-negotiation observation remains byte-exact and is
not relabelled; raw logs, profile data and process identities remain private and
local.

The additive
[`Claude Code 2.1.245 strict-modern STDIO readiness summary`](claude-code-2.1.245-modern-stdio-readiness-2026-08-25.json)
records a fresh observation after the macOS parent-executable binding repair reached
protected `main` at commit `e905c632724ecc9d13b13452fee37328e75cc2a4`, tree
`c611ba2d86dcefb541814e5cd4ab3345dd8745b6`. The exact installed binary reported
`2.1.245 (Claude Code)` and `Connected`. The same two-session MCP `2026-07-28`
journey passed independent replay with zero provider traffic, pending requests,
anomalies or stderr. Repository, gateway-image and provenance assurance passed in
[run 32868256571](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32868256571),
and all CodeQL analyses passed in
[run 32868252219](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32868252219).
The public projection is path-free and preserves the 2.1.241 schema and evidence
digests as historical lineage. It proves transport readiness only: capability,
the exact-five journey, remote HTTP evidence, provider use, registration,
activation, deployment and release remain incomplete or unexercised. Raw capture,
client output, profile data and local identities remain owner-only and unpublished.

The separate
[`Claude Code 2.1.245 HOST-002 capability projection`](claude-code-2.1.245-host-002-capability-2026-08-26.json)
is a verifier-produced, path-free pass from exact protected-main commit
`5837bd65a482e90238c466673318f007e305c744`, tree
`d68d0cdb12fd555fbb41da0d6d4aba23a69ef44f`, with projection SHA-256
`558a2a5a337dc2c601b982c11e644390e68c858342b0fe28f9b40bf68d740ebb`.
Every exact-main CI job passed in
[run 32941380816](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32941380816),
and every analysis passed in
[CodeQL run 32941380576](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32941380576).
Claude Code `2.1.245`, reporting model `claude-sonnet-5`, completed MCP
`2026-07-28` case `QUAL-206-HOST-002` with exactly one canonical
`catalogue.search` call and a valid independently checked receipt. The CLI ceiling
was two agentic turns while the exact final host report was `num_turns: 3`; these
are distinct counters. This closes only that one bounded capability case. The
projection explicitly keeps exact-five model capability, remote HTTP
interoperability, live geospatial-provider use, registry publication, activation,
deployment and release false. Raw Claude and MCP capture remains owner-only and
local.

The later
[`Claude Code 2.1.245 exact-five capability projection`](claude-code-2.1.245-exact-five-capability-2026-08-27.json)
is a fresh verifier-produced pass from exact protected-main commit
`029a9d5c7efcafcd45941194394384ee6c578fe9`, tree
`96f75d96b1e0680465494834ddad8661539cbd62`, with projection SHA-256
`06311b896963503bd7f6f88d32d34edfda52afb49b3d9e5b6c05eaed3230f0a6`.
Every exact-main CI job passed in
[run 33114396425](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33114396425),
and every analysis passed in
[CodeQL run 33114396546](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33114396546).
Claude Code `2.1.245`, reporting model `claude-sonnet-5`, completed the five ordered
MCP `2026-07-28` calls over local STDIO. The verifier accepted all five distinct
receipts, every result contract, structured/plain-text parity, the inspection
relationship and the documented `tool_use` plus `completed` terminal form at
reported turn 7. The deterministic fixture made one synthetic provider transport
call and zero guarded live-provider API invocations. This closes local STDIO
exact-five model capability only. Remote HTTP interoperability, a live geospatial
provider, registry publication, activation, deployment and release remain false.
Raw capture remains owner-only and local.

The
[`protected-main local HTTP transport preflight`](local-http-transport-preflight-2026-08-25.json)
is a separate path-free projection from exact protected-main commit
`066a9cb22f719d22e29c95cd99857ddf694c878e`, tree
`43116491557d53c4c0ad2d3a6768761ccf873df4`. A deterministic synthetic client
completed 14 requests and received 13 responses over one ephemeral IPv4 loopback
listener, covering the exact five operations and three resource classes; the one
response-free request is the deliberately aborted second `data.query`. The
projection SHA-256 is
`c227791068c662c64e14fa9ec354d8d8030e5cc2e3d64b0d8ff93101e1b67274`.
Every protected-main CI job passed in
[run 32851616717](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32851616717),
including repository, image, independent-derivation, attestation and provenance
assurance. Every analysis in
[CodeQL run 32851615811](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32851615811)
also passed for Actions, JavaScript/TypeScript and Python. The owner-only private
capture remains local and unpublished. This is loopback HTTP transport preflight
only: remote-host acceptance remains false, Claude Code and model capability remain
unscored, and no live provider, registration, activation, deployment or release was
exercised.

The historical records continue to bind the unchanged ten-case
[`qual_206_cases.json`](../qual_206_cases.json) bytes. The separate
[`qual_206_cases_expansion.json`](../qual_206_cases_expansion.json) is design-time,
non-live and unscored; it is not a runtime input to those sessions and does not
upgrade, relabel or replace their results.

The additive strict-modern capture and public-evidence contracts are described in
the
[`QUAL-206 strict-modern evidence preparation` runbook](../../../docs/operations/QUAL-206_STRICT_MODERN_EVIDENCE.md).
They retain private telemetry locally and compile only a minimised projection. The
current summary-level contract cannot score a real host capability pass; that
requires the separately versioned event-level collector described in the runbook.
