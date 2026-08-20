# TOOLS-205 non-activating tool registry candidate

- status: local candidate; not activated, advertised or deployed
- work item: `TOOLS-205`
- decision: [ADR-0009](../decisions/ADR-0009-read-only-mcp-tool-lifecycle.md)
- base: protected `main` commit `364c8680ad11399e0547a843be2a04da7a737301`

## Implemented boundary

The candidate adds a closed
[`tool-registry.v1.json`](../../profiles/tool-registry.v1.json) profile, its Draft
2020-12 [schema](../../schemas/tool-registry.schema.json) and the private,
zero-third-party-dependency `@gis-ai-go/tool-registry` package. The registry has
exactly 12 unique IDs and names in ADR-0009 order. Every profile records lifecycle,
mutability, release target, implementation and discovery state, runtime schema
references, provider and operation support, controlled errors, cursor and artefact
status, CRS requirements, provenance, fallback, threats and immutable research
provenance.

| ID | Profile | Current implementation | Current lifecycle | `v0.2.0` target | Release target | Effect |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | `catalogue.search` | implemented | suspended | active | `v0.2.0` | read-only |
| T02 | `catalogue.describe` | implemented | suspended | active | `v0.2.0` | read-only |
| T03 | `selection.resolve` | not implemented | planned | active | `v0.2.0` | read-only |
| T04 | `data.query` | not implemented | planned | active | `v0.2.0` | read-only |
| T05 | `spatial.locate` | not implemented | planned | planned | later reviewed release | read-only |
| T06 | `spatial.analyse` | not implemented | planned | planned | later reviewed release | read-only |
| T07 | `statistics.compare` | not implemented | planned | planned | later reviewed release | read-only |
| T08 | `route.plan` | not implemented | planned | planned | later reviewed release | read-only |
| T09 | `map.render` | not implemented | planned | planned | later reviewed release | read-only |
| T10 | `artefact.export` | not implemented | planned | planned | later reviewed release | read-only |
| T11 | `evidence.inspect` | implemented | suspended | active | `v0.2.0` | read-only |
| T12 | `workflow.execute` | not implemented | planned | planned | `v0.3.0` | mutating |

All current discovery flags and activation gates are false. The v0.2 target is
explicitly marked as having no runtime authority. In particular,
`selection.resolve` and `data.query` are target-active governance requirements, not
implemented or callable tools.

## Runtime API and fail-closed rules

The package exposes:

- `listToolProfiles()` for a frozen copy of the canonical ordered list;
- `getToolProfile(name)` for an exact-name lookup with a controlled unknown-profile
  error;
- `filterToolProfiles(filter)` for a closed metadata filter which preserves
  canonical order; and
- `listCurrentCallableTools()` for the set which passes every current ADR-0009
  condition.

The current callable result is an empty frozen array. The helper considers only
`current` state and accepted runtime input, output and problem schema references;
it never reads `v02Target`. `evidence.inspect` intentionally has no accepted
runtime problem schema reference yet, although its transport-neutral application,
request and result contracts exist.

`controlledErrors` preserves the governance vocabulary from the research profile;
it is not by itself a runtime error contract. Runtime error availability is
declared separately by `runtimeSchemas.problem`, preventing a planned source field
from being mistaken for an implemented transport guarantee.

Registry construction clones caller data, rejects unknown or missing fields,
wrong order, duplicate or substituted IDs, lifecycle contradictions, inappropriate
mutability, incomplete schema state and target metadata presented as runtime
authority. Returned documents, profiles and arrays are recursively frozen. Safe
errors do not reflect rejected input.

## Provenance and dependency boundary

The source research remains byte-for-byte unchanged. The registry binds:

- path `docs/research/2026-08-19/research-pack/data/tool-catalogue.json`;
- SHA-256 `851f626bae4d63e8355ff9ca4021b56041ffa7e432d41f7f682c214151b5a8c3`;
- Git blob `0514fba4ff4765c951c632f6a1c122fe02b1d178`; and
- exact `/tools/0` to `/tools/11` source and research-schema pointers.

Research pointers are provenance only and are never dereferenced as runtime
schemas. The Python contract test compares every mirrored purpose, provider,
access, policy, cost, error, cursor, provenance, fallback and threat field with the
immutable source.

The new package has no dependency. A root development-only workspace link makes
the first-party component explicit in `pnpm-lock.yaml` and the dependency SBOM;
the release-metadata test verifies its product version and exact npm package URL.

## Non-activation and residual boundary

No gateway source, activation array, provider adapter, execution operation, route,
listener or deployment is changed. The registry never reads environment variables.
Production activation remains solely in
`apps/mcp-gateway/src/activation.ts`, whose tool and API arrays remain empty.

This slice does not implement `selection.resolve`, `data.query` or any other
planned operation. It does not complete provider, schema, policy, evidence,
interoperability or fallback gates, and it does not authorise the mutating
`workflow.execute` profile. A later activation change must supply its own reviewed
contracts, threat evidence and lifecycle decision.

## Verification

Focused verification commands are:

```bash
pnpm --filter @gis-ai-go/tool-registry run typecheck
pnpm --filter @gis-ai-go/tool-registry run test
uv run --locked --cache-dir .uv-cache python -m unittest tests.contract.test_tool_registry
pnpm run build:okf
pnpm run validate:contracts
pnpm run validate:versions
uv run --locked --cache-dir .uv-cache python -m unittest tests.contract.test_release_metadata
```

The full repository gate remains required before integration. Activation,
deployment, release, GitHub and live-provider checks are deliberately outside this
candidate.
