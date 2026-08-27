# QUAL-206 Claude exact-five capability pack

## Status

This additive pack prepares a bounded Claude Code `2.1.245` observation of the
complete deterministic exact-five journey over local MCP `2026-07-28` STDIO. It
now includes closed private-run, per-session and minimised public-evidence schemas,
plus an offline verifier and adversarial regression coverage. Two bounded
protected-main observations on 27 August 2026 completed the first four operations
but produced the final structured answer before calling `evidence.inspect`. Both
private runs were rejected because Claude reused the inspected search receipt as
if it were the inspection call's own receipt. No public projection was written and
there is no accepted public exact-five capability evidence yet.

The existing QUAL-206-HOST-002 schemas, verifier and evidence remain unchanged.
That accepted one-tool observation continues to prove only `catalogue.search`.

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
- permits at most seven agentic turns; and
- rejects missing, duplicated, reordered or altered calls, including inspection
  of any receipt other than the search receipt.

The CLI's `--max-turns 7` ceiling allows the fifth call after the observed
four-call cut-off. Anthropic [defines that ceiling](https://code.claude.com/docs/en/agent-sdk/agent-loop)
as a maximum number of tool-use round trips, while `num_turns` reports the total
actually taken and includes a final no-tool turn. The verifier therefore accepts
between three and eight reported turns rather than treating the ceiling as a
target. The lower bound follows from the search-to-inspection dependency plus the
final no-tool turn. It also requires an `end_turn` terminal state, so a
success-shaped `tool_use` result cannot be accepted. It accepts only one closed
call session and the observed bounded negotiation variants. This includes the
accepted two-session shape in which the first session performs `server/discover`
and the second performs `tools/list` then the five ordered calls.

Each exact-five observer session retains one canonical, owner-only and size-bounded
result file locally. The offline Node verifier rechecks the discovery and listing
surface, full structured response bodies, plain-text parity, output contracts and
all five operation-specific cryptographic receipts. It also proves that the
inspection target is the search receipt while the inspection call has its own
distinct receipt. The Python verifier independently binds that result verification
to the request-event chain, source/runtime closure, final Claude structured output,
process cleanup and provider audit.

The fake-client suites exercise the complete one-session and two-session success
paths, the observed four-call `tool_use` termination, wrong order, wrong arguments,
a duplicate call, a substituted inspection receipt and a cryptographically
invalid receipt. Offline projection tests additionally reject result reordering,
duplication, body-parity failure, inspection-relationship substitution, extra
protocol methods, changed request digests, out-of-bound turn counts,
non-`end_turn` results, inflated claims and private-data leakage.

## Publication boundary

Do not treat the private harness result as evidence. Only after this verifier slice
has merged and passed protected-main checks may one separately authorised live
observation be run from exact protected `main`. Raw prompts, responses, paths,
process details, costs, identifiers and private logs must remain local. Only a
successful, schema-valid and minimised verifier projection may enter the public
evidence directory. Failed or incomplete projections are not publishable.

This pack does not establish remote HTTP interoperability, live provider use,
registry publication, activation, deployment or release.
