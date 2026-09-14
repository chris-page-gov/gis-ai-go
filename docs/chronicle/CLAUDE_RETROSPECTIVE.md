# The Claude interoperability investigation

Claude Code interoperability was not one failed test repeated until it passed. The
work moved through distinct layers: legacy transport, current protocol negotiation,
authentication, permission-name translation, extensible metadata, turn-count
semantics, model-facing schema presentation and structured-output completion.
That explains part of the elapsed effort. The sequence also exposes avoidable
rework: turn ceilings were changed before the missing fifth tool and the SDK’s
terminal-result contract had been fully reconciled.

The strongest public result is narrow. Claude Code `2.1.245`, reporting
`claude-sonnet-5`, completed the five ordered deterministic operations through
local MCP `2026-07-28` STDIO. The verifier independently checked all five results,
receipts, presentation parity and the search-to-inspection relationship. This does
not prove remote HTTP interoperability, a live geospatial provider, registry
publication, activation, deployment or release.

## Reconstructable observation chronology

The table records a **documented minimum of 12 observation outcomes**. It is not an
exhaustive attempt count. An exact timestamp is shown only when a committed public
projection provides one; otherwise only the documented calendar date is used.
The same rows are available as [JSON](data/claude-observations.json) and
[CSV](data/claude-observations.csv).
The same bounded rows are available as
[machine-readable JSON](data/claude-observations.json) and
[CSV](data/claude-observations.csv).

| Ref | Time evidence | Bounded observation and outcome | Public source |
| --- | --- | --- | --- |
| C01 | 23 August 2026, 21:41:20.640 UTC | Claude Code `2.1.204` completed legacy initialisation and `tools/list`; no model task or tool call, so capability remained unscored. | [Legacy readiness projection](../../tests/interoperability/evidence/claude-code-legacy-stdio-readiness-2026-08-23.json) |
| C02 | 24 August 2026; exact time unavailable | Claude Code `2.1.241` offered MCP `2025-11-25` to the strict `2026-07-28` surface and was correctly rejected. | [Two-attempt protocol projection](../../tests/interoperability/evidence/claude-code-2.1.241-stdio-observation-2026-08-24.json) |
| C03 | 24 August 2026; exact time unavailable | Its constructor-only fallback negotiated `2025-06-18` and completed `tools/list`; capability still unscored. | [Two-attempt protocol projection](../../tests/interoperability/evidence/claude-code-2.1.241-stdio-observation-2026-08-24.json) |
| C04 | 25 August 2026, 06:11:58.916–06:11:59.889 UTC | With v2 automatic negotiation, `2.1.241` completed `server/discover` and a separate modern `tools/list` session. | [`2.1.241` modern readiness projection](../../tests/interoperability/evidence/claude-code-2.1.241-modern-stdio-readiness-2026-08-25.json) |
| C05 | 25 August 2026, 16:12:36.853–16:12:37.921 UTC | The upgraded `2.1.245` client repeated the strict-modern transport pass; no model task was requested. | [`2.1.245` modern readiness projection](../../tests/interoperability/evidence/claude-code-2.1.245-modern-stdio-readiness-2026-08-25.json) |
| C06 | 26 August 2026; exact time unavailable | The first HOST-002 model observation used a one-agentic-turn ceiling. It returned a valid MCP result but ended `error_max_turns` before the required structured final response. | [HOST-002 runbook](../operations/QUAL-206_CLAUDE_CAPABILITY.md) |
| C07 | 26 August 2026, 07:11:24.404 UTC | A two-agentic-turn ceiling allowed the final response. One canonical `catalogue.search` call and its receipt passed independent verification. | [Accepted HOST-002 projection](../../tests/interoperability/evidence/claude-code-2.1.245-host-002-capability-2026-08-26.json) |
| C08 | 27 August 2026; exact time unavailable | The first exact-five observation, bounded at seven turns, stopped after four calls and never called `evidence.inspect`. | [Exact-five runbook](../operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md) |
| C09 | 27 August 2026; exact time unavailable | An eight-turn bound produced the same four-call result. | [Exact-five runbook](../operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md) |
| C10 | 27 August 2026; exact time unavailable | A ten-turn bound ended normally at reported turn 7 but still exposed only four model-facing tools and made four calls. | [Exact-five runbook](../operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md) |
| C11 | 27 August 2026; exact time unavailable | After an observer-only `evidence.inspect` schema projection, Claude made all five calls. Publication was withheld because the verifier incorrectly required `stop_reason: end_turn`, although the successful structured result reported `stop_reason: tool_use` and `terminal_reason: completed`. | [Exact-five runbook](../operations/QUAL-206_CLAUDE_EXACT_FIVE_CAPABILITY.md) |
| C12 | 27 August 2026, 20:55:58.173 UTC | A fresh run after the terminal predicate correction completed all five calls at reported turn 7 and passed independent verification. | [Accepted exact-five projection](../../tests/interoperability/evidence/claude-code-2.1.245-exact-five-capability-2026-08-27.json) |

C02 and C03 are two attempts inside one public observation. C11 is a real
successful five-call observation whose public projection was correctly withheld
under the then-current verifier. Only C07 and C12 are accepted model-capability
projections.

## What changed in GIS AI GO

The repository history records a chain of narrow fixes rather than hiding the
failed hypotheses:

| Pull request | Change | Why it mattered |
| --- | --- | --- |
| [#70](https://github.com/chris-page-gov/gis-ai-go/pull/70) | Bounded capability harness | Made a model-mediated call observable and fail-closed. |
| [#71](https://github.com/chris-page-gov/gis-ai-go/pull/71) | First-party keychain login | Preserved the authorised authentication route without publishing credentials. |
| [#72](https://github.com/chris-page-gov/gis-ai-go/pull/72) | Modern MCP negotiation | Selected Claude’s v2 runtime and automatic negotiation for MCP `2026-07-28`. |
| [#73](https://github.com/chris-page-gov/gis-ai-go/pull/73) | Permission alias | Allowed Claude’s observed dot-to-underscore tool name while preserving canonical dotted MCP names and rejecting collisions. |
| [#74](https://github.com/chris-page-gov/gis-ai-go/pull/74) | Extensible request metadata | Accepted valid namespaced `_meta` extensions without treating them as identity. |
| [#75](https://github.com/chris-page-gov/gis-ai-go/pull/75) and [#76](https://github.com/chris-page-gov/gis-ai-go/pull/76) | Completion turn and counter semantics | Distinguished the configured agentic ceiling from Claude’s reported `num_turns`. |
| [#79](https://github.com/chris-page-gov/gis-ai-go/pull/79) | Exact-five pack | Added the closed five-operation profile, isolation, receipts and adversarial verifier tests. |
| [#83](https://github.com/chris-page-gov/gis-ai-go/pull/83) and [#84](https://github.com/chris-page-gov/gis-ai-go/pull/84) | Higher bounded ceilings | Demonstrated that more turns alone did not restore the missing fifth tool. |
| [#85](https://github.com/chris-page-gov/gis-ai-go/pull/85) | Observer-only schema projection | Presented a compatible closed v1 `evidence.inspect` input while leaving the canonical production contract unchanged. |
| [#87](https://github.com/chris-page-gov/gis-ai-go/pull/87) | Structured terminal predicate | Aligned success with `subtype: success`, valid `structured_output` and `terminal_reason: completed`; `tool_use` alone still fails. |
| [#77](https://github.com/chris-page-gov/gis-ai-go/pull/77) and [#88](https://github.com/chris-page-gov/gis-ai-go/pull/88) | Minimised public evidence | Published only independently verified HOST-002 and exact-five projections. |

The result is stronger than a client-specific workaround. Canonical MCP names and
schemas remain authoritative; compatibility transformations are explicit,
collision-checked, observation-scoped and provenance-bound. Authentication,
network isolation, deterministic fixtures, output contracts and receipt checks
remain separate controls.

## Time and cost boundaries

The interval from the earliest precisely timed retained observation, C01, to the
accepted exact-five result, C12, is **3 days, 23 hours, 14 minutes and 38 seconds**
(rounded). This is an observation window, not continuous labour, model execution
time or the full project duration. It includes gaps whose causes and length cannot
be allocated reliably from this evidence alone.

Git timestamps establish when changes were recorded, not how long each diagnosis
took. The public projections establish only some observation times. The preserved
safe conversation projections contain no trustworthy provider-charge field, and
the public evidence intentionally excludes costs. Absence of a billing field is
not evidence of zero cost. Subscription allowance, tokens, provider charges,
elapsed wall time, CI waiting and operator time must not be merged into one figure.

The private retrospective keeps source-linked candidates for later reconciliation,
but the original programme-root projection was rejected by the safety filter in
every retained generation. That prevents a defensible claim that C01 was the very
first informal attempt, or that the table contains every authentication retry,
command rerun or model call. Issue
[#86](https://github.com/chris-page-gov/gis-ai-go/issues/86) therefore remains open
for the “all attempts with timestamps, duration and cost” requirement.

## Process lessons

1. Read and encode the client SDK’s result contract before the first live
   capability run; keep transport, tool-call and structured-completion predicates
   distinct.
2. Inspect both canonical `tools/list` and the model-facing tool presentation
   before changing turn ceilings.
3. Treat client aliases as a presentation layer. Preserve canonical protocol names
   and test normalisation collisions.
4. Run one bounded observation per explicit hypothesis, write its expected
   discriminator first, and retain failed outcomes in the private journal.
5. Capture start/end time, client and model identity, hypothesis, call count,
   terminal result, measured usage and accepted evidence link at observation time.
6. Publish only a fresh protected-main run after the relevant fix and independent
   verifier have passed.

This turns the expensive investigation into a reusable compatibility method: a
small deterministic case, a closed observer, adversarial offline verification and
a minimised public claim whose limitations are part of the result.
