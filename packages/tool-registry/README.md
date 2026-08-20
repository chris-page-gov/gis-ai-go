# Tool registry package boundary

This private first-party package reads the checked-in
[`tool-registry.v1.json`](../../profiles/tool-registry.v1.json) profile, validates
its closed structure and lifecycle invariants, and exposes frozen list, get and
filter helpers. It has no third-party or workspace runtime dependency.

The registry contains exactly the 12 ADR-0009 canonical profiles. Profile
existence is governance information, not a runtime availability claim. The
`v02Target` field is explicitly non-runtime metadata and is never used by
`listCurrentCallableTools`. A profile can appear in that helper only when its
current implementation, lifecycle, discovery, release, policy, read-only,
schema, threat, evidence, interoperability and fallback conditions all pass,
including accepted input, output and problem schema references. The current
result is an empty frozen array.

`catalogue.search`, `catalogue.describe` and `evidence.inspect` are implemented
but suspended. `selection.resolve` and `data.query` are required for the
`v0.2.0` target but are not implemented. The other profiles remain planned;
mutating `workflow.execute` is a `v0.3.0` target only.

The suspended `evidence.inspect` profile references a closed operation-result
dispatcher over distinct v1 and v2 result schemas. The original v1 result schema
is not widened, and this governance reference does not make the profile callable.

The package does not import the gateway, register a tool, inspect environment
variables or provide an activation override. Production activation remains
owned solely by `apps/mcp-gateway/src/activation.ts`, which this slice does not
change.
