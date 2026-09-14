# Guidance review and model transitions

Reviewed on 14 September 2026. Historical baseline:
`6c76c92a18da779766f8d49acbbd7dbbd31abb97`. The owner reported the move to
GPT-6 Astra with the Codex host's Ultra setting. This records the selected host
configuration; it does not equate that label with a documented API parameter.

## Source and scope

Current [official GPT-6 Astra guidance](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices)
recommends explicit follow-through, auditing conflicting instructions, appropriate
delegation, concise communication and proportionate verification. This project
applies those recommendations to observed operating problems: repeated authority
questions, oversized context loading, repeated builds and stale capability text.
These edits are a guidance treatment; measured productivity gains are not yet available.

The live documentation was fetched on the review date using the OpenAI Docs
workflow. Historical model/client observations and provider fixtures retain their
original versions. No application LLM, API endpoint, cache setting, router or
provider model was changed. The geospatial runtime continues to calculate
deterministically. The user's Codex host controls the lead model selection.

## Instruction inventory and decisions

| Surface | Review decision | Consequence |
| --- | --- | --- |
| Global working agreements | Retain British English and locale rules | Project-specific changes stay in this repository |
| AGENTS.md | Clarify authority, continuity, bounded delegation and affected local checks | Fewer ambiguous reasons to pause; mandatory gates retained |
| CONTEXT.md | Put current authority before historical records; date the new work | Current instruction is distinguishable from research and old commentary |
| PROGRESS.md | Replace 1,147-line startup history with a short checkpoint and fixed Git snapshot link | History is preserved and no longer reloaded on every restart |
| Roadmap and backlog | Add CHRON-213, retrospective and local-completion investigation | Hosted release gates remain explicit |
| Delivery model and contributing guide | Separate local development checks from mandatory canonical CI | No implied permission to bypass the shadow-only routing gate |
| Pull-request template | Allow relevant tests or justified non-applicability and record required assurance | No invented runtime tests for prose-only changes |
| Security policy and CODEOWNERS | Retain reporting, ownership controls and current candidate boundaries | Model capability does not grant publication rights |
| Issue templates and release configuration | Retain evidence, provenance and rollback fields | Still appropriate for autonomous implementation |
| Component README files | Correct outdated inactive/Stage 0 claims and duplicate build recipes | Links point to current accepted capability and focused commands |
| Policy, accessibility and interoperability guides | Reconcile with implemented policies, UIs and host evidence | Users can tell a historical preparation statement from current state |
| EVID-211 runbook and daily preservation prompt | Preserve the capture-only scope | Analysis runs separately; a scheduled capture does not start a retrospective |
| Historical ADRs and immutable research AGENTS/prompts | Retain original bytes; follow explicit supersession links | Historical instructions are evidence, not fresh authority |
| OpenAI Docs and PDF skills used in this work | Apply source verification and print inspection in scope | No edits to shared installed skills |
| Other installed skills | Catalogue assessed for applicability; bodies not loaded without need | Availability alone does not add project instructions |

The runtime and assurance reviews document component guidance findings and the
corresponding corrections. Existing operator runbooks retain their exact evidence
contracts; their restrictions govern those operations, not unrelated documentation.

## Concrete changes

The lead agent must continue already-authorised work through its required checks.
When a prerequisite is missing, it records the blocker and carries on with
independent work. It preserves the objective across compaction, answers side
questions and resumes. Child assignments state an outcome, file ownership,
evidence and a stop condition; the lead checks returned work before integration.

Local verification is selected by changed behaviour and shared dependencies.
Canonical CI still runs all required jobs until ASSURE-209 is accepted. An
unchanged successful check need not be repeated without a new finding or explicit
release requirement. Independent image derivation and full preservation
verification remain distinct from ordinary repeated build preparation.

The old sentence treating every repository document as untrusted conflicted with
the instruction to follow accepted project guidance. The replacement identifies
which documents govern work and which source material cannot grant authority.
The prior text remains available at the frozen baseline for comparison.

## Model usage inventory

| Usage | Role | Action |
| --- | --- | --- |
| Lead Codex session | Autonomous implementation and review, now user-selected GPT-6 Astra | Update project guidance; preserve user host settings |
| Delegated delivery agents | Bounded implementation/review contexts | Preserve available metadata; mark historical per-thread model identity unavailable |
| Claude observation harnesses | Test an external client's actual MCP behaviour | Retain recorded client/model versions and parsers |
| ChatGPT tunnel harnesses | Observe client calls and bind evidence | Retain historical model metadata and output contracts |
| Geospatial execution and catalogue tools | Deterministic implementation | No model migration applicable |
| Research, fixtures and comparison records | Historical evidence | Leave model strings and observations unchanged |

The review found model mentions in interoperability schemas, fixtures, tests and
observation tooling. These are evidence surfaces rather than a product model
default to replace. API request, sampling, cache and pricing migration is outside
this guidance change and has no applicable product usage identified here.

## Evaluation after the change

Use representative documentation, runtime-fix and interoperability tasks. Record
task scope, model/host setting, guidance revision, accepted result, review findings,
clarification pauses, duplicate checks, elapsed time and attributable usage where
available. Do not run extra live model calls just to produce a before/after table
when historical comparable evidence is sufficient.

Acceptance for the guidance change means current instructions are consistent,
historical evidence is preserved, the required check inventory is unchanged and
the task resumes from its checkpoint. Evidence of speed or cost improvement needs
matched observations. Where task scope, model and guidance all change together,
attribute only the combined result and retain the confounding factors.

For later model upgrades repeat this inventory and compare the operating guidance
with actual behaviour. Record which instructions were introduced, revised or
retired and why. A durable model-transition ledger is part of the chronicle's
method, not a reason to rewrite the earlier account as if the new model built it.
