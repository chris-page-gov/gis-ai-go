# QUAL-206 local demonstration

This short demonstration lets a colleague inspect the inactive exact-five gateway
candidate without deploying, registering or activating it. The supported public
product remains the static `v0.1.0` Explorer.

## Current state and direction

- `v0.1.0`: the static Explorer is the supported public product.
- `v0.2.0`: the exact-five MCP candidate is local and unregistered. Its next gates
  are a strict-modern independent host, remote HTTP evidence and deployment to an
  agreed runtime and hostname boundary.
- `v0.3.0`: the roadmap adds replayable policy, governance and explicit workflows.
- `v1.0.0`: the goal is an owned, supportable public service boundary.

## Prerequisites

- Use a complete checkout and run the command from the repository root.
- Use Node.js `24.19.0` and pnpm `10.33.2`, as pinned by the repository.
- Install dependencies in advance with `pnpm install --frozen-lockfile`. This may
  need package-registry access; the demonstration itself does not need network
  access.
- Do not provide an API key or provider credential. None is required or used.

## Run it

```bash
pnpm run demo:local
```

The command builds the verified local prerequisites, then runs
`scripts/qual_206_local_demo.mjs`. That driver starts the existing strictly gated
exact-five fixture as a child process over real operating-system STDIO pipes. It
passes only two fixture controls and three parent-owned temporary-path variables to
that child, reports whether the checkout is clean and exits with an error if the
expected journey or safety boundary is not met. The parent removes the temporary
root after all child pipes close, escalating from EOF to `SIGTERM` and then
`SIGKILL` if required.

## Colleague-facing run-of-show

1. Explain that this is an unregistered local candidate, not the supported service.
2. Run the command and show discovery of the five candidate operations:
   `catalogue.search`, `catalogue.describe`, `selection.resolve`, `data.query` and
   `evidence.inspect`.
3. Point out the catalogue, record and evidence resources, then follow the journey
   from catalogue discovery and deterministic selection through the fixed fixture data
   query to receipt inspection.
4. Close on the reported boundary: real STDIO transport, temporary local state, an
   injected fixed provider response, zero guarded provider-egress calls and
   `production_registration: false`. Point out that operating-system network
   isolation is not enforced by this demonstration.

## Concepts demonstrated

- the research-highlighted combination of a portable OKF discovery plane with MCP
  tools and resources;
- governance as code: one immutable assembly, policy-bounded discovery, explicit
  lifecycle state and evidence receipts;
- strict MCP `2026-07-28` negotiation, with no silent downgrade to a legacy protocol;
- MCP discovery, tool calls and resource reads across real STDIO pipes;
- structured results with equivalent plain-text fallbacks;
- deterministic selection without an LLM performing geospatial calculation;
- material results carrying evidence receipts that can be inspected; and
- a data-query path exercised with an injected, fixed ONS-shaped fixture response.

## Safety and evidence boundary

The active journey is deterministic. The provider adapter receives one injected
fixed response in process. A tested preload guard covers the DNS and HTTPS APIs used
by the live provider transport; the private audit proves the injected transport ran
once and no guarded provider-egress API ran. Treat the displayed value as fixture
evidence, not as a current ONS statistic.

This is a provider-path assertion, not an operating-system network sandbox. The
child retains normal host networking, and the report says that OS isolation is not
enforced. The fixture creates its ledger and reconciliation index beneath a private,
parent-owned operating-system temporary directory. The parent removes that entire
root only after the child closes, including after forced termination. It does not
write demonstration state to a persistent service.

The fixture can start only when the driver supplies its exact enable flag, full
source-commit value, authority argument, closed scenario and private audit pipe. Its
assembly identifies itself as `candidate-unregistered`, reports production
registration as false and is not exposed by a shipped HTTP or STDIO entry point.

## What this does not prove

This demonstration does not prove:

- a live-provider call, current provider data or provider availability;
- an independent desktop host, remote HTTP interoperability or a public HTTPS
  endpoint;
- production identity, egress, persistent storage, backup, monitoring or rollback;
- deployment, MCP Registry publication, production activation or a `v0.2.0`
  release;
- model judgement, end-user answer quality or a user-interface journey; or
- the full QUAL-206 acceptance matrix. Run the repository assurance and
  interoperability suites for those broader local checks, then collect the
  separately governed external evidence where required.
