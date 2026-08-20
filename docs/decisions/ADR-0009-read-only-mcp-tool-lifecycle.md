# ADR-0009: Read-only MCP tool lifecycle

- status: accepted
- decided on: 20 August 2026
- work item: MCP-201
- release target: `v0.2.0`

## Context

The research defines 12 canonical tool profiles. Eleven are described as read-only,
while `workflow.execute` is explicitly mutating. The live roadmap also defines
`v0.2.0` as an open, read-only MCP and direct-API release. Treating every profile as
an advertised runtime tool would therefore contradict the release boundary.

An MCP profile is useful design and governance information even when its
implementation has not passed its activation gate. Advertising that profile as an
available tool is a materially different claim: clients may select and call it.
Returning a routine "not implemented" result from an advertised tool would make
discovery misleading and increase tool-confusion and tool-poisoning risk.

The supported public catalogue from `v0.1.0` is the shared source for the first
runtime slice. The existing static Explorer must remain independently useful and
must not become dependent on the MCP service.

## Decision

Maintain all 12 canonical profiles, with an explicit lifecycle state such as
`active`, `planned`, `suspended` or `retired`. The existence of a profile does not
make its tool available.

MCP discovery and the equivalent direct API may expose a tool only when all of the
following are true:

- its implementation exists;
- it is enabled for the deployed release;
- the current public policy permits discovery and invocation;
- it is read-only; and
- its schema, threat, policy, evidence, interoperability and fallback tests pass.

Never advertise a tool whose implementation is absent. A suspended or planned
profile may remain available as governed catalogue information, but it must not
appear in the callable tool list or an equivalent direct-API capability list.

The supported `v0.2.0` target active set is exactly:

- `catalogue.search`;
- `catalogue.describe`;
- `evidence.inspect`;
- `selection.resolve`; and
- `data.query`.

The MCP-201 contract change establishes a shared catalogue foundation over the
existing checksum-verified bundle, adopted by the static Explorer. The next
end-to-end slice will implement `catalogue.search` and `catalogue.describe` through
the same application path for MCP and direct API consumers. `evidence.inspect`,
`selection.resolve` and
`data.query` become active only after their later evidence gates pass, but all five
must be active for the supported `v0.2.0` release.

The other seven canonical profiles remain planned and non-active throughout
`v0.2.0`:

- `spatial.locate`;
- `spatial.analyse`;
- `statistics.compare`;
- `route.plan`;
- `map.render`;
- `artefact.export`; and
- `workflow.execute`.

`workflow.execute` is deferred to `v0.3.0` because it creates or changes workflow
state and therefore cannot form part of the read-only release. The other planned
tools require their own provider, complexity, non-App fallback and evidence gates
before a later decision can activate them.

This decision and shared catalogue foundation do not claim that an MCP listener,
direct API, provider adapter, policy engine or evidence store is currently running.

## Consequences

- Tool discovery remains deterministic, honest and policy-filtered.
- Clients never need to call a tool to discover that its implementation is absent.
- The 12-profile catalogue can evolve without expanding the callable attack
  surface.
- Direct API and MCP capability lists must agree on the active set.
- Every advertised result must remain complete without an MCP App; a map or
  artefact tool needs its tested non-App fallback before activation.
- The static Explorer and canonical OKF publication remain usable when the service
  is unavailable, suspended or rolled back.
- Activating any of the seven planned profiles requires a later reviewed change;
  activating `workflow.execute` also requires the `v0.3.0` workflow and policy
  boundary.
