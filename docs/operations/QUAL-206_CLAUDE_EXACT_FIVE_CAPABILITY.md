# QUAL-206 Claude exact-five capability pack

## Status

This additive pack prepares a bounded Claude Code `2.1.245` observation of the
complete deterministic exact-five journey over local MCP `2026-07-28` STDIO. It
now includes closed private-run, per-session and minimised public-evidence schemas,
plus an offline verifier and adversarial regression coverage. Bounded
protected-main observations on 27 August 2026 with configured maximums of seven
and eight turns still stopped after four calls, before `evidence.inspect`. A later
observation with a ten-turn ceiling completed at reported turn 7 with an `end_turn`
terminal state, but again made only the first four calls. The MCP wire-level
`tools/list` response contained all five tools, while Claude's model-facing set
contained only four and omitted `evidence.inspect`.

Of the five canonical input schemas, `evidence.inspect` alone uses the existing
v1/v2 top-level `oneOf` and `$defs` structure. That is an observed compatibility
correlation and the basis of a narrowly testable hypothesis; it does not prove
that Claude's schema parser caused the omission. Independent result verification
rejected every incomplete observation. No public projection was written and there
is no accepted public exact-five capability evidence yet.

The dedicated QUAL-206-HOST-002 capability schemas, verifier outcome and evidence
remain unchanged. The shared composite event schema and verifier gain only optional
presented-response fields, which remain forbidden for HOST-002. That accepted
one-tool observation continues to prove only `catalogue.search`.

## Closed profile

The versioned `exact-five-v1` profile fixes one ordered call to each canonical
operation:

1. `catalogue.search`
2. `catalogue.describe`
3. `selection.resolve`
4. `data.query`
5. `evidence.inspect`

The first four calls use committed deterministic arguments. The fifth must
inspect the unchanged inline receipt returned by the first call. Every operation
must return a valid inline receipt, match its closed output contract and retain
structured-content and plain-text parity.

Claude's permission surface uses the five observed underscore aliases, such as
`mcp__gis-ai-go-qual-206-exact-five-v1__catalogue_search`. The MCP wire protocol
continues to use the canonical dotted names. Alias generation rejects invalid MCP
names and any collision caused by the dot-to-underscore conversion.

The model instruction now makes the final dependency explicit: after `data.query`,
Claude must call `evidence.inspect`, wait for its response and copy the inspection
call's own distinct receipt before producing structured output. The search receipt
may be reused only as the inspection input and `inspected_search_receipt_id`; it
must not be substituted for the inspection call's receipt. No receipt may be
inferred, invented or calculated. The existing five-call evidence predicates remain
unchanged and fail closed; the independent verifier additionally rejects a
non-`end_turn` terminal state.

## Isolation and fail-closed behaviour

The separate launcher:

- requires `GIS_AI_GO_QUAL_206_CLAUDE_EXACT_FIVE_CAPABILITY=1` and its dedicated
  authority argument;
- advertises exactly the five profile tools, no resources and no built-in Claude
  tools;
- binds the committed profile, observer, launcher, fixture and generated runtime
  closure before execution;
- retains the existing MCP-subtree Seatbelt network denial and credential
  removal;
- permits at most ten bounded agentic turns; and
- rejects missing, duplicated, reordered or altered calls, including inspection
  of any receipt other than the search receipt.

The exact protected-main observations above establish that both `--max-turns 7`
and `--max-turns 8` can stop in `tool_use` state after the first four calls. The
later `--max-turns 10` observation completed at reported turn 7 with `end_turn`,
but still exposed only four model-facing tools and made only those four calls. The
turn boundary is therefore retained as a conservative bound, not treated as the
current explanation for the missing fifth call. Anthropic
[documents `max_turns`](https://code.claude.com/docs/en/agent-sdk/agent-loop) as a
maximum number of tool-use round trips and describes the final no-tool response as
an additional turn. However, the exact native CLI observations at configured
ceilings of seven and eight each reported the configured ceiling while the observer
recorded only four calls. Configured `max_turns` and reported `num_turns` are
therefore bounded metadata here, not evidence of how many MCP calls occurred. The
observer's request-result trace remains authoritative. The accepted one-tool
observation used a ceiling of two and reported three turns after its final response,
so the verifier accepts between three and 11 reported turns rather than treating
the ceiling as a target. It still requires an `end_turn` terminal state, so a
success-shaped `tool_use` result cannot be accepted. It accepts only one closed call
session and the observed bounded negotiation variants. This includes the accepted
two-session shape in which the first session performs `server/discover` and the
second performs `tools/list` then the five ordered calls.

## Observer-only compatibility projection

The `exact-five-v1` observer now validates the complete canonical five-tool
`tools/list` response before deriving a fresh, model-facing presentation. That
presentation changes only the `evidence.inspect` input schema: it uses the existing
closed v1 branch, which requires `receipt_id` and rejects additional properties,
instead of presenting the canonical top-level v1/v2 union. The five canonical tool
names and the other four complete tool definitions remain unchanged. Any missing,
additional, duplicated or input/output-schema-changed tool fails closed. Independent
verification also proves that every field outside the single projected
`evidence.inspect` input schema is identical to the captured canonical listing.

This projection is confined to the bounded Claude exact-five observer. It does not
change the canonical gateway, OpenAPI, direct HTTP, MCP HTTP, ordinary MCP STDIO or
the v2 reconciliation contract. The observer binds separate, domain-separated
digests for the complete canonical tool set and the complete presented tool set,
without mutating the captured canonical response. Its private event trace records
separate byte counts and digests for the canonical fixture output and host-facing
projection, and binds a reproducible digest of the exact presented result. This
keeps both forms attributable and prevents a presentation-only compatibility
measure from being mistaken for a production contract change.

Each exact-five observer session retains one canonical, owner-only and size-bounded
result file locally. The offline Node verifier rechecks the discovery and listing
surface, both full tool-set digests, full structured response bodies, plain-text
parity, output contracts and all five operation-specific cryptographic receipts. It
also proves that the
inspection target is the search receipt while the inspection call has its own
distinct receipt. The Python verifier independently binds that result verification
to the request-event chain, source/runtime closure, final Claude structured output,
process cleanup and provider audit.

The fake-client suites exercise the complete one-session and two-session success
paths, both observed turn-7 and turn-8 four-call `tool_use` terminations, the
observer-only v1 presentation and separate domain-separated canonical and presented
tool-set digests, wrong order, wrong arguments,
a duplicate call, a substituted inspection receipt and a cryptographically
invalid receipt. Offline projection tests additionally reject result reordering,
duplication, body-parity failure, inspection-relationship substitution, extra
protocol methods, changed request digests, out-of-bound turn counts,
non-`end_turn` results, inflated claims and private-data leakage.

## Publication boundary

Do not treat the private harness result as evidence. No public capability projection
may be written until this observer projection has merged and passed protected-main
checks and a new bounded observation from exact protected `main` completes all five
calls and every independent verifier gate. Raw prompts, responses, paths, process
details, costs, identifiers and private logs must remain local. Only a successful,
schema-valid and minimised verifier projection may enter the public evidence
directory. Failed or incomplete projections are not publishable.

This pack does not establish remote HTTP interoperability, live provider use,
registry publication, activation, deployment or release.
