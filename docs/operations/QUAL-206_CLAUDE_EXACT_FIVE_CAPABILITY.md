# QUAL-206 Claude exact-five capability pack

## Status

This additive pack prepares a bounded Claude Code `2.1.245` observation of the
complete deterministic exact-five journey over local MCP `2026-07-28` STDIO. It
has regression coverage but has not been used for a live Claude observation.
There is no accepted public exact-five capability evidence yet.

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
- permits at most six agentic turns; and
- rejects missing, duplicated, reordered or altered calls, including inspection
  of any receipt other than the search receipt.

The fake-client suite exercises one complete success path and four adversarial
paths: wrong order, wrong arguments, a duplicate call and a substituted inspection
receipt. Each adversarial path is classified as
`capability-evidence-request-invalid` by the observer.

## Publication boundary

Do not treat the private harness result as evidence. A further additive slice
must supply closed exact-five private-run, session and public-projection schemas,
an offline verifier and projection regression tests. Only after that slice has
merged and passed protected-main checks may one separately authorised live
observation be run from exact protected `main`. Raw prompts, responses, paths,
process details and private logs must remain local; only a successful minimised
verifier projection may enter the public evidence directory.

This pack does not establish remote HTTP interoperability, live provider use,
registry publication, activation, deployment or release.
