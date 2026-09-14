# The Claude interoperability investigation

Editorial recovery revision: 14 September 2026. This chapter corrects the first
12-outcome edition using additional public records and a separately admitted
private projection supplement. Original captures and accepted runtime evidence
remain unchanged.

Claude Code eventually completed the five-operation demonstration, but reaching
that point involved avoidable rework. The public record shows several different
problems, not one failure repeated unchanged: protocol negotiation, process
lifecycle, authentication, permission aliases, request metadata, turn counters,
model-facing schemas and final-result verification. Some fixes addressed genuine
client differences; others corrected assumptions in GIS AI GO's own observation
harness.

The accepted result remains narrow. Claude Code `2.1.245`, reporting
`claude-sonnet-5`, completed the ordered deterministic operations through local
MCP `2026-07-28` STDIO. Independent verification checked the five results and
receipts, agreement between structured and text responses, and the dependency
between searching and inspecting that search's receipt. This establishes neither
remote HTTP interoperability nor live geospatial-provider use, registry
publication, activation, deployment or release. The versions and documentation
below describe the historical investigation, not a claim about today's clients.

## Reconstructable observation chronology

Public files and their history support a **documented minimum of 23 outcomes**:
9 readiness or exploratory checks, 12 capability-lane invocations and 2 preflight
stops. This is not an exhaustive attempt count or a count of paid model requests.
A capability-lane invocation can fail before a model performs useful work;
conversely, one successful tool lifecycle can involve several provider requests.

After crosswalking the recovered records, the combined reviewed minimum is
**31 outcomes**, not 23 plus the raw number of command matches. Sixteen recovered
harness launches map to existing public rows or additional failures; four direct
client diagnostics and one non-live diagnostic are counted separately. The table
below retains the public-source sequence; the recovery additions follow it.

The compact table uses dates in August 2026. Exact timestamps, timing semantics,
turn counts, source anchors and the crosswalk from the first edition's `Cxx`
references are retained in [JSON](data/claude-observations.json) and
[CSV](data/claude-observations.csv). Same-day ordering follows the documented
observation-and-fix sequence where exact times are unavailable. PC17 and PC18 are
explicitly two earlier runs, but their individual identities cannot be separated
from the public summary alone.

| Ref | August date | Concise outcome | Source |
| --- | --- | --- | --- |
| PC01 | 20 | Unauthenticated probe: initialise request, no response. | [Probe](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/independent-host-readiness-2026-08-20.json#L27-L42) |
| PC02 | 20 | Separate health check: legacy opening rejected. | [Health](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/independent-host-readiness-2026-08-20.json#L43-L65) |
| PC03 | 20 | Uncommitted fallback connected; exploratory only. | [Fallback](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/legacy-fallback-exploratory-2026-08-20.json#L1-L56) |
| PC04 | 23 | Protected-main legacy readiness passed. | [Readiness](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-legacy-stdio-readiness-2026-08-23.json#L7-L77) |
| PC05 | 24 | Updated client's old protocol rejected by modern surface. | [Strict check](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.241-stdio-observation-2026-08-24.json#L88-L142) |
| PC06 | 24 | Updated client's constructor fallback connected. | [Fallback check](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.241-stdio-observation-2026-08-24.json#L143-L211) |
| PC07 | 25 | Modern exchange passed; shutdown signal rejected. | [Lifecycle](https://github.com/chris-page-gov/gis-ai-go/commit/c679b6fd8fb702572da11043d492c3e9e953ad7a) |
| PC08 | 25 | Claude 2.1.241 modern readiness accepted. | [Readiness](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.241-modern-stdio-readiness-2026-08-25.json#L7-L65) |
| PC09 | 25 | Upgraded-client identity preflight stopped before capture. | [Identity](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/docs/operations/QUAL-206_CLAUDE_COMPOSITE_OBSERVATION.md#L36-L48) |
| PC10 | 25 | Claude 2.1.245 modern readiness accepted. | [Readiness](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.245-modern-stdio-readiness-2026-08-25.json#L7-L65) |
| PC11 | 25 | Authentication preflight failed; model not started. | [Login](https://github.com/chris-page-gov/gis-ai-go/commit/20a4c9779992826c85ce3229585ef296c19ceb2b) |
| PC12 | 25 | First documented HOST-002 model task used wrong negotiation mode. | [Negotiation](https://github.com/chris-page-gov/gis-ai-go/commit/2edf26238b20eb87d5ba5b24fdec0fda63876bd8) |
| PC13 | 25–26 | Permission alias mismatch prevented the tool call. | [Alias](https://github.com/chris-page-gov/gis-ai-go/commit/10368f73bd612b6aff5e4bc8524d331ede8e5d5e) |
| PC14 | 26 | One valid call; turn limit prevented final response. | [Turn limit](https://github.com/chris-page-gov/gis-ai-go/commit/0eaf430f1d9420db956fd66b359ea06adbfd7018) |
| PC15 | 26 | One-call success withheld for unexpected turn count. | [Counter](https://github.com/chris-page-gov/gis-ai-go/commit/5837bd65a482e90238c466673318f007e305c744) |
| PC16 | 26 | Fresh one-tool capability observation accepted. | [HOST-002](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.245-host-002-capability-2026-08-26.json#L1-L65) |
| PC17 | 27 | Earlier exact-five run A: four calls; receipt reused. | [Earlier pair](https://github.com/chris-page-gov/gis-ai-go/blob/d2f3e72858272dbfe3f79a83d290d622977c65e6/docs/operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md#L5-L13) |
| PC18 | 27 | Earlier exact-five run B: same documented failure. | [Earlier pair](https://github.com/chris-page-gov/gis-ai-go/blob/d2f3e72858272dbfe3f79a83d290d622977c65e6/docs/operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md#L5-L13) |
| PC19 | 27 | Seven-turn bound: still only four calls. | [Seven turns](https://github.com/chris-page-gov/gis-ai-go/commit/b9e777a9ed3744dd7291c0cd69347dd07aab2672) |
| PC20 | 27 | Eight-turn bound: still only four calls. | [Eight turns](https://github.com/chris-page-gov/gis-ai-go/commit/5645c8467133c1d3c2883e084d5f5e1d3792f9bb) |
| PC21 | 27 | Normal completion, but fifth model-facing tool missing. | [Tool visibility](https://github.com/chris-page-gov/gis-ai-go/commit/235b08109bbd6a8e7d2dd4a4635544f6c8bb3c15) |
| PC22 | 27 | Five calls succeeded; terminal predicate withheld projection. | [Terminal check](https://github.com/chris-page-gov/gis-ai-go/commit/029a9d5c7efcafcd45941194394384ee6c578fe9) |
| PC23 | 27 | Fresh exact-five capability observation accepted. | [Exact five](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/tests/interoperability/evidence/claude-code-2.1.245-exact-five-capability-2026-08-27.json#L1-L140) |

Only PC16 and PC23 are accepted model-capability projections. PC15 and PC22
completed their required calls but were withheld by erroneous verifier
assumptions. Refusing to publish an unverified result was the intended safety
behaviour; the predicates themselves still needed correction and a fresh run.

### Additional outcomes recovered from the permitted private projection

These are reviewed paraphrases, not raw private logs. The private matrix retains
the exact launch/output references and timestamps. The public source for the
recovery method is [the accepted preservation repair #121](https://github.com/chris-page-gov/gis-ai-go/pull/121)
and its [aggregate admission note](https://github.com/chris-page-gov/gis-ai-go/issues/86#issuecomment-5664179767).
Unlike the PC rows, these additional outcomes cannot be independently reproduced
from public captures alone. Their evidence-access limit is part of the claim.

| Ref | August date | Classification | Retained outcome |
| --- | --- | --- | --- |
| RC01 | 26 | Capability-lane failure | A further launch after the alias fix returned child exit 1. The precise failing boundary remains unresolved. |
| RC02 | 26 | Direct diagnostic | The client described a catalogue call; an actual MCP call was not established. |
| RC03 | 26 | Direct diagnostic | The client reported that the requested tool was unavailable. |
| RC04 | 26 | Direct diagnostic | The client reached its turn ceiling while requesting tool use. |
| RC05 | 26 | Direct diagnostic | A separate diagnostic also reached its turn ceiling. |
| RC06 | 27 | Unresolved harness failure | A ten-turn launch returned exit 2. It is not the later retry that supports PC21; model contact is unproven. |
| RC07 | 27 | Preflight failure | A fresh launch failed closed with no capture before the final accepted retry. |
| RC08 | 27 | Non-live diagnostic | A deliberately pre-spawn check identified conflicting credential-variable presence. No model was requested. |

The combined categories reconcile to 9 readiness outcomes, 13 capability-lane
outcomes, 4 direct diagnostics, 3 preflight stops, 1 non-live diagnostic and
1 unresolved harness failure. Only two remain accepted capability projections.
Help/version/authentication preparation and offline tests are retained in the
source inventory, not mislabelled as model or MCP attempts. One read of a saved
SDK result is explicitly excluded as a new attempt; its originating launch is
not established by chronological proximity alone.

Two corrections matter for interpreting the first edition. Its seven-turn C08
was the **third**, not the first, documented exact-five attempt. Its C07 and C12
timestamps—now PC16 and PC23—are **completion times**, not start times. Both
verifiers populate `observed_at` from `execution.finished_at`:
[HOST-002 mapping](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/scripts/verify_qual_206_claude_capability.py#L1232-L1235)
and
[exact-five mapping](https://github.com/chris-page-gov/gis-ai-go/blob/a25f4dee9c84369328f52563a2b907bc4aa216c3/scripts/verify_qual_206_claude_exact_five_capability.py#L1203-L1206).

## What changed in GIS AI GO

### 1. Connection was not capability

A readiness check asks whether a client can open a connection and list tools.
It does not prove that a model can choose a tool, supply valid arguments or use
its result. Claude's legacy opening failed against the modern-only surface on
20 August. The constructor-only fallback introduced in
[#40](https://github.com/chris-page-gov/gis-ai-go/commit/e1fc1cbe69ea72c9aa310607d80f392ef56b0d58)
provided a separate conformance route; it did not silently downgrade the canonical
modern interface.

For modern negotiation, Claude first started a disposable discovery process and
then a separate session. The collector had to represent both. The
[composite-observation design](https://github.com/chris-page-gov/gis-ai-go/blob/42f050b/docs/operations/QUAL-206_CLAUDE_COMPOSITE_OBSERVATION.md#L3-L20)
recorded that behaviour and the first-party runtime controls. Subsequent fixes
recognised a safe shutdown signal after a completed response (PC07) and changed
how the upgraded client's executable identity was checked (PC09). These were
bounded observer/lifecycle repairs, not evidence of geospatial functionality.

### 2. Known readiness behaviour did not all reach the model-task harness

The bounded capability harness added in
[#70](https://github.com/chris-page-gov/gis-ai-go/pull/70) made one exact
`catalogue.search` call observable. Its first-party-login environment initially
hid the valid Keychain login; PC11 stopped before the model started. After that
repair, the model-task path still omitted the v2/automatic-negotiation controls
already used by readiness, producing PC12. The next mismatch was a permission
name: Claude selected `catalogue_search`, while the allowlist used the canonical
`catalogue.search` spelling. PC13 therefore made no MCP tool call.

The fixes preserved the login route, transferred the invocation-local runtime
controls and matched the exact host permission alias. Canonical dotted MCP names
remained unchanged. The later
[#74 metadata change](https://github.com/chris-page-gov/gis-ai-go/commit/add17192faec9ce8bdce962bacdce812a213330b)
also checked naming collisions and accepted valid namespaced `_meta` extensions.
Optional client information remained attribution, not trusted identity. A patch
alone does not prove another attempted invocation, so this change is not counted
as an extra observation without independent evidence.

### 3. Two counters were mistaken for one

`--max-turns` configures a ceiling for the client's agent loop. `num_turns` is a
field in its final report. Neither counts independently observed MCP calls.
For this historical client, a ceiling of one returned the required tool result
but stopped before the final structured answer (PC14). Raising the ceiling to
two allowed completion, yet the client reported `num_turns: 3`; the verifier
rejected it because it expected the counters to agree (PC15). The fresh PC16 run
passed after that assumption was corrected.

The distinction is practical: the configured limit bounds exposure, the reported
counter describes client behaviour, and the observer's request/result trace proves
which tools actually ran. The
[recorded counter correction](https://github.com/chris-page-gov/gis-ai-go/commit/5837bd65a482e90238c466673318f007e305c744)
preserved exactly one allowed MCP call and its independently checked receipt.

### 4. Listing a tool did not mean the model could call it

The exact-five profile required, in order, `catalogue.search`,
`catalogue.describe`, `selection.resolve`, `data.query` and `evidence.inspect`.
The last call had to inspect the unchanged receipt from the first, and return
its own distinct receipt. Returning five plausible receipt values was not proof
that five operations had run.

Two early runs stopped after four calls and substituted the search receipt for
the missing inspection receipt. The
[#82 correction](https://github.com/chris-page-gov/gis-ai-go/commit/d2f3e72858272dbfe3f79a83d290d622977c65e6)
made that dependency explicit, raised the committed ceiling from six to seven
and tightened completion checks. Further seven- and eight-turn runs still stopped
after four calls. At a ten-turn ceiling, PC21 ended normally at reported turn 7
but still lacked the fifth tool. More turns alone had not solved the problem.

Three different surfaces must therefore be inspected:

| Surface | What it establishes | What it does not establish |
| --- | --- | --- |
| MCP wire listing | What the server advertised. | What reached the model. |
| Model-facing tool set | What the client made available to the model. | Whether a tool actually ran. |
| Independent observer and verifier | Which calls and valid results occurred. | Whether an unrelated host or deployment works. |

**Observed fact:** the wire listing contained all five tools, but the model-facing
set omitted `evidence.inspect`. **Correlation:** that tool alone used the
top-level `oneOf`/`$defs` schema combination. **Hypothesis:** a narrower schema
presentation might restore compatibility. The historical evidence does not expose
Claude's internal parser, so it cannot establish that parser as the root cause.

[#85](https://github.com/chris-page-gov/gis-ai-go/commit/235b08109bbd6a8e7d2dd4a4635544f6c8bb3c15)
tested that hypothesis with an observer-only projection of the existing closed
v1 inspection input. It retained all canonical tools and separately bound the
canonical and presented forms to digests. The following observation completed
all five calls. This was evidence for the bounded compatibility measure, not a
reason to rewrite the production gateway, HTTP API or canonical v1/v2 contract.

### 5. Successful calls could still fail the final-result check

PC22 completed the calls, receipt checks and inspection relationship. Its final
result nevertheless retained `stop_reason: "tool_use"`, while the agent loop
reported `terminal_reason: "completed"`, `subtype: "success"` and valid structured
output. The verifier incorrectly insisted on `stop_reason: "end_turn"`.

`stop_reason` describes an underlying model response; `terminal_reason` describes
why the agent loop ended. Treating them as interchangeable created a second
kind of false negative. The
[#87 correction](https://github.com/chris-page-gov/gis-ai-go/commit/029a9d5c7efcafcd45941194394384ee6c578fe9)
required completed, successful, schema-valid structured output and clean process
closure, while retaining every call and receipt check. `tool_use` by itself
remained insufficient. PC22 was not retrospectively promoted: a fresh run from
the corrected protected-main source produced PC23, published through
[#88](https://github.com/chris-page-gov/gis-ai-go/commit/80c55d1c5817adee67052ef8be6d99d5efcceb52).

## When the documentation was used

The public record does **not** support the claim that #87 was the first time
first-party documentation had been consulted. The 25 August composite design
already cited
[Claude MCP runtimes](https://code.claude.com/docs/en/mcp#MCP-client-runtimes),
[environment controls](https://code.claude.com/docs/en/env-vars) and the
[MCP release](https://blog.modelcontextprotocol.io/posts/2026-07-28/).
The historical source anchors are in the
[original decision matrix](https://github.com/chris-page-gov/gis-ai-go/blob/42f050b/docs/operations/QUAL-206_CLAUDE_COMPOSITE_OBSERVATION.md#L14-L20).

The naming/metadata correction cited
[MCP tool-name guidance](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
and [metadata rules](https://modelcontextprotocol.io/specification/2026-07-28/basic#_meta).
The earlier completion work cited the
[CLI turn limit](https://code.claude.com/docs/en/cli-usage) and
[Agent SDK loop](https://code.claude.com/docs/en/agent-sdk/agent-loop).
The narrower
[structured-output success](https://code.claude.com/docs/en/agent-sdk/structured-outputs)
and [TypeScript result-contract](https://code.claude.com/docs/en/agent-sdk/typescript)
predicates were reconciled in
[#87's terminal section](https://github.com/chris-page-gov/gis-ai-go/blob/029a9d5c7efcafcd45941194394384ee6c578fe9/docs/operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md#L145-L165).
These are references recorded during the investigation, not a fresh validation
of their present-day contents.

The supported criticism is more specific: known readiness configuration was not
fully carried into the capability harness, and the relevant result predicates
and model-facing tool visibility were reconciled too late. Reading documentation
is not enough; the assumptions it supports must reach the launcher, fake client,
verifier and regression tests together.

## Time and cost boundaries

The earliest precisely timed public attempt starts at
**20 August 2026, 18:12:18.064 UTC**. The accepted exact-five run completed at
**27 August 2026, 20:55:58.173 UTC**. The resulting public observation window is
**7 days, 2 hours, 43 minutes and 40.109 seconds**. This is not continuous labour,
cumulative model execution or the full project duration. The first edition's
shorter window omitted the earlier public records.

The first probe's very short interval records telemetry, not complete client
startup. Similarly, the accepted readiness intervals cover observer sessions.
PC03 and PC04 have observation instants whose start/end meaning is not established;
PC16 and PC23 have confirmed completion instants. Git commit times record changes,
not the duration of the diagnoses that preceded them.

The public evidence intentionally excludes billing details. Unknown cost is not
zero cost. Subscription allowance, token use, provider charges, elapsed time, CI
waiting and human intervention are different measures and must remain separate.
The private CSV and JSON include per-attempt and cumulative covered timing/cost
columns; unavailable values remain null rather than invented estimates.

| Measure | Evidence available | Interpretation |
| --- | --- | --- |
| Public observation window | 7 days, 2 hours, 43 minutes, 40.109 seconds | Calendar span from first retained public probe to accepted exact-five completion; not active work. |
| Recovered collection envelopes | 21 non-overlapping intervals; 627.237 seconds in total | Launch-record-to-terminal-collection subtotal, including startup, waiting and reporting overhead; not complete investigation runtime. |
| Direct diagnostic SDK duration | Four paired result records; 12.208 seconds in total | Small, separate SDK-reported subset; do not add it to overlapping command envelopes. |
| Client-reported cost | Four directly paired totals retained privately | Not invoices or total Claude spend. A fifth saved-result total is excluded because its originating attempt is unproven. |
| Full active work, actual charges, Codex allocation and human time | Unavailable or not attributable | No conversion from elapsed time, no pricing of historical tokens at current rates, no implied zero. |

The large difference between collection envelopes and calendar span is not a measured
waste total: implementation, tests, reviews, other work, human availability and
unrecorded waits share that span. The records do not support a complete allocation
between them. Likewise, repeated compaction or malformed-command reports do not
by themselves establish how much delay each caused.

### Completion and remaining evidence gap

The recovery now reconciles the identified launch records, delayed terminal
outputs, earlier public chronology and directly paired cost records. The private
and public products preserve the unresolved boundaries, rather than simply adding
the original ten launch candidates to the twelve-row table. Two independent
candidate sweeps also examined earlier preparation and later redacted launch names.

This does **not** establish the first-ever informal attempt or a globally exhaustive
count: some source records remain omitted or quarantined, and RC01/RC06 retain
classification uncertainty. The earliest retained probe and final accepted result
are anchored; missing records cannot prove that nothing preceded or fell between
them. [RETRO-208 #86](https://github.com/chris-page-gov/gis-ai-go/issues/86) must not be
closed as exhaustive on the strength of this minimum. Closing on a recoverable-
evidence basis requires an explicit owner decision; it is not a silent change to
the acceptance criteria.

## Process lessons

These are recommendations derived from the observed failures, not claims that
every improvement has already been implemented:

1. **Carry the accepted configuration forward.** Share or contract-test the
   readiness and capability launch settings. Test login mode, runtime selection
   and permission aliases before spending a model run on a known prerequisite.
2. **Define success before the live call.** Encode the versioned final-result
   contract in both successful and hostile fixtures. Keep client counters,
   observed calls, structured completion and process cleanup separate.
3. **Locate a missing call before changing budgets.** Compare server listing,
   model-facing tools, permission decision and observer trace. State the specific
   evidence that would support or reject each hypothesis.
4. **Change one material hypothesis at a time.** Record the expected result,
   bounded authority and stopping rule. After a failed hypothesis, inspect the
   new evidence before increasing the same limit again.
5. **Preserve failures as well as passes.** Capture native start/end fields,
   client/model versions, limits, exit status, call counts and available usage.
   Separate preflight, diagnostic and capability attempts; deduplicate reruns and
   repeated reporting of the same event.
6. **Make verification proportionate, not optional.** Use affected offline tests
   while developing a fix, reuse passing checks for unchanged inputs, and retain
   mandatory canonical CI. Prefer event-driven waits over repetitive polling.
   No retry or local optimisation should weaken the independent receipt gate.
7. **Publish the smallest demonstrated claim.** Obtain a fresh protected-main
   observation after a verifier correction. Keep compatibility projections
   explicit and preserve the distinction between local STDIO, remote HTTP and a
   deployed service.

The useful exemplar is not that autonomous coding made no mistakes. It is that
the mistakes, rejected hypotheses and safeguards can be inspected, and that the
method can improve without rewriting its evidence or expanding its claims.

The two P1 follow-ons are [client-contract preflight #122](https://github.com/chris-page-gov/gis-ai-go/issues/122)
and [source-time attempt journalling #123](https://github.com/chris-page-gov/gis-ai-go/issues/123).
CI selection remains [#97](https://github.com/chris-page-gov/gis-ai-go/issues/97),
archive throughput [#116](https://github.com/chris-page-gov/gis-ai-go/issues/116),
and modularisation [#119](https://github.com/chris-page-gov/gis-ai-go/issues/119).
Each has separate acceptance evidence; none is claimed implemented by this report.
