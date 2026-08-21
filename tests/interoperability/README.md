# Interoperability-test boundary

The supported public product remains the static `v0.1.0` Explorer. The accepted MCP
gateway has empty production activation arrays and readiness remains `503`.

QUAL-206 may exercise the explicit local conformance seam with exactly
`catalogue.search`, `catalogue.describe`, the public catalogue resource and the
record resource. This is test evidence, not production activation or a public MCP
service.

Run the deterministic, minimised-telemetry harness with:

```bash
pnpm run test:interoperability
```

The [evaluation corpus](qual_206_cases.json) distinguishes public-safe behaviours
derived from the exact source-hashed `mcp-geo` archive from candidate-specific
assurance cases. Every historical case cites its source paths; current-candidate
cases state their basis without claiming historical provenance. Raw chats, secrets,
personal data and licensed payloads are deliberately excluded.
Reviewed live-host summaries are stored under [`evidence/`](evidence/) and bind
their claims to exact harness bytes without retaining raw prompt or result content.
The same directory preserves path-free independent-host readiness summaries without
publishing disposable profiles, raw host logs or device identifiers.
The Codex CLI row uses the exact `QUAL-206-HOST-002` corpus prompt and records a
protocol-negotiation `not_ready` result separately from capability scoring.

The later legacy-host fallback candidate does not rewrite those retained results.
Its separately named launcher supports only isolated STDIO conformance, requires
an exact constructor authority and explicit test argument, and keeps the shipped
HTTP and STDIO entrypoints modern-only with empty production activation. The
interoperability harness verifies the full legacy initialise, list, call and
resource journey through the unchanged minimised-telemetry proxy. Any new host
observation must bind a committed fallback checkout and new telemetry rather than
being added to an older evidence record.
The current [legacy fallback exploratory summary](evidence/legacy-fallback-exploratory-2026-08-20.json)
records a credential-stripped Claude health connection and a Codex
configuration-only check against exact uncommitted runtime hashes. It is explicitly
not accepted host evidence and requires repetition from a reviewed commit.

See the [QUAL-206 interoperability runbook](../../docs/operations/QUAL-206_INTEROPERABILITY.md)
for repeatable ChatGPT secure-tunnel and independent-host procedures.
