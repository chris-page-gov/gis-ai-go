# MCP server input limits and request isolation

Review date: 21 October 2026. Work item: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).

The gateway pins `@modelcontextprotocol/server` and its required core to `2.3.0`.
The existing Node adapter `2.0.0` admits this server through its `^2.0.0` peer
range, so no adapter update is needed. Client and unrelated build dependencies
remain at their separately reviewed versions. The lockfile records exact package
integrities; the earlier [17 October disposition](DEPENDENCY_SECURITY_2026-10-17.md)
remains a historical assessment.

## Required controls

[GHSA-46jr-4wx8-v453](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-46jr-4wx8-v453)
requires more than an upgrade: the SDK's argument element limit is disabled by
default. All four authored server constructors now set `maxToolInputElements`
to 1,024. This counts combined object members and array entries before tool schema
validation. The test derives conservative structural maxima from every registered
input schema, resolving local references, constants, closed objects, bounded arrays
and alternatives. The largest is catalogue search: 76 elements (four top-level
keys, six facet keys and 66 array entries). Selection resolution has at most 53,
data query 23 and catalogue description four. Evidence inspection, each local
or hosted CPIH input, and each pilot input have at most three. A maximum-sized
76-element catalogue fixture also passes its actual advertised schema. The
1,024 ceiling therefore preserves every currently schema-valid input; a new
unbounded or unsupported schema construct fails the bound test and needs review.
It is an operational ceiling, not an increase to any individual tool's schema limit.
Synthetic tests exercise the exact boundary and nested array/record refusal.

The common HTTP handler also sets the SDK body limit to the existing 65,536-byte
application limit. The private pilot uses its existing 16,384-byte ceiling on
both modern and legacy SDK transports. The host parsers retain their earlier
strict byte, Unicode, duplicate-key and nesting checks. Parsed-body entry points
are internal composition seams whose callers already enforce these byte limits.
The argument bound also applies to the shared STDIO constructor; this does not
imply that the HTTP advisory affects STDIO.

[GHSA-jm63-cq47-j5jp](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-jm63-cq47-j5jp)
requires separate server/transport instances for distinct HTTP requests or
sessions. The inspected code already constructs a fresh server in each factory
call. The pilot's legacy branch also constructs a fresh transport per request.
This structure is preserved. An overlapping two-request test uses the same
JSON-RPC ID and verifies that each caller receives its own result; normal
sequential requests continue to use fresh instances.

## Acceptance limits

Gateway regression tests and the pinned dependency assertions are required locally.
Fresh canonical assurance, independent image derivation and the unchanged
vulnerability-policy gate remain required before merge. This source repair does
not prove that any previously deployed private Site or service contains these
bytes. It changes no tool registration, provider authority, entitlement, retry
policy or deployment state.
