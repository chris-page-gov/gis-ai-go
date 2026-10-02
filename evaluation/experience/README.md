# Experience examples and evaluation

This is the authored learning and evaluation contract for the current product
surfaces. It supports the local learning page, a facilitator, an AI client or an
independent evaluator. It does not grant provider access or run the questions.

[`catalogue.v1.json`](catalogue.v1.json) is authoritative. It contains 74 current
user facilities: 45 source declarations at accepted baseline
`387e86695e7002e78f005e972703f5c5e51fa546` and 29 separately labelled new local
learning facilities. Eight planned facilities are outside that denominator.
There are nine persona hypotheses, 74 stories, 222 questions and 904 prompt
variants. Every current facility has positive, clarification and negative cases;
every positive case has a variant for every persona. Clarification and negative
cases use one or two role variants; all nine roles are not separately assessed
for every refusal or clarification. The 21 named intake child facilities separate
preview formats, entry routes, component checks, format guidance, clear/cancel
and input-limit behaviour instead of hiding them within one upload feature. This is **100% authored
coverage of the declared facilities**, not 100% successful answers, exhaustive
source-data coverage or acceptance by every client.

The baseline includes public Explorer search, all six filters, cards, graph,
timeline, schematic map, downloads, shareable state and publication context;
five local MCP tools and three resource classes; six private Sites tools; two
Explorer page tools; four captured-CPIH workbench page tools; three captured-CPIH MCP tools; and eight local
OKF+ discovery/package facilities. Page tools, remote MCP, local MCP and an
installed AI connector remain distinct surfaces. The source validator checks
exact tool/resource sets and all public Explorer facets, so an added or removed
operation cannot silently retain a 100% label. The remaining user-facility
inventory is an explicit reviewed decomposition of the cited source, not an
automated claim to detect every future control or internal function.

## Use the contract in an interface

Each `feature` declares its surface, operation, maturity, source IDs, concept IDs,
presentation forms, boundary and short `jitSummary`. `current` means present in
the cited implementation; it does not mean available to every visitor or accepted
in every host. `local-increment-unaccepted` explicitly identifies new local work.

Each story states a user goal, component needs and completion criteria. Each
question has a primary `prompt`, `variants` with exact persona IDs, `expected`
checks, structured `assertions` and a plain-language learning summary. Questions
remain `not-run` in the source; execution evidence belongs in a separate report.
Source entries identify the actual API/data grain, repository evidence and rights
boundary. Concept definitions are short, project-authored explanations for user
testing; no certified reading age or proven comprehension is claimed.

Keep the learning panel available next to the task. Make its explanations usable
by keyboard, touch and screen reader. Keep the short explanation visible, then
allow the user to inspect the full technical wording. Never replace source-native
labels with a simpler term that changes their meaning. Show a source and a limit
beside the result, and keep a complete text alternative for every visual form.
A `planned` presentation form is a design requirement, not an available export.

Language style is independent of intelligence, age and subject expertise. The
additional-English variants deliberately use short or incomplete phrasing without
ridicule. Evaluate meaning and task completion; do not score grammar. An expert
may prefer a short spoken request, and a novice may type a long request.
The nine roles are hypotheses for testing, not demographic research findings.

The optional `typedCall` on five positive Site examples is a bounded, existing
recipe. The learning page must not automatically execute it. Before a separate
live run, use the authorised client, inspect current capabilities and retain its
provider-call and time budget. `sites_evidence_inspect` requires a receipt from an
actual successful request, so it has no fabricated static receipt recipe.
The source corpus does not authorise new paid calls, wider queries or protected
data access.

## Run offline coverage checks

From the repository root:

```sh
node scripts/experience_evaluate.mjs --check \
  --output artifacts/experience/coverage.json
node --test tests/test_experience_evaluate.mjs
```

The validator checks identifiers, references, source paths, exact operation
inventories, persona coverage, concept and JIT coverage, case kinds, outcome
assertions and existing typed-call anchors. It performs no network, provider or
model call. The report binds the catalogue SHA-256, baseline, declared denominator
and separately labelled new-local count. With no observation file, all 222
natural-language questions remain unobserved even when authored coverage is 100%.

Existing Sites Q01–Q13, the independent local typed client and OKF+ K01–K40 are
cross-referenced evidence anchors. They are not copied into a new pass count.
A typed operation passing does not show that an AI chose it correctly from a
natural-language question. Four OKF+ context cases remain unassessed.

## Record an actual evaluation

Select a feature, persona variant, client and execution plane. Record the exact
runtime revision and catalogue digest before starting. Keep setup failures,
unsupported capabilities, clarification, safe refusal and wrong answers distinct.
Use the question's assertions unchanged for the first run. A reviewer should
inspect each assertion against the retained evidence; do not mark every check true
because a tool returned HTTP 200 or the screen looked plausible.

Retain observations under the ignored `artifacts/experience/` directory. Use
pseudonymous activity IDs, never names, email addresses, tokens or credentials.
Prefer a sanitised result/receipt to a full transcript. Do not retain children's
voice recordings, personal files or identifiable feedback by default. Local file
preview is not permission to distribute the file or add it to an AI prompt.

An observation file has this structure (placeholders must be replaced with real
values; this example is not a pass receipt):

```json
{
  "schema": "gis-ai-go.experience-observations.v1",
  "catalogueSha256": "<actual catalogue SHA-256>",
  "runtimeRevision": "<actual 40-character runtime Git revision>",
  "observations": [{
    "questionId": "EX-Q001-positive",
    "variantId": "public-search-teen-explorer",
    "plane": "participant",
    "reviewerRole": "facilitator",
    "client": "local learning page and keyboard",
    "observedAt": "2026-10-07T10:45:00+01:00",
    "evidencePath": "artifacts/experience/session-01/result.json",
    "evidenceSha256": "<actual retained file SHA-256>",
    "assertionResults": [
      {"id": "task-outcome", "passed": false, "evidencePointer": "result.json: outcome"},
      {"id": "source-binding", "passed": false, "evidencePointer": "result.json: source"},
      {"id": "boundary", "passed": false, "evidencePointer": "result.json: limits"},
      {"id": "accessible-equivalence", "passed": false, "evidencePointer": "result.json: text"}
    ]
  }]
}
```

Run:

```sh
node scripts/experience_evaluate.mjs \
  --observations artifacts/experience/session-01/observations.json \
  --output artifacts/experience/session-01/report.json
```

The aggregator validates the exact catalogue binding, all expected assertions,
variant IDs, observation plane and retained evidence hash. It reports
**reviewer-reported** outcomes and unobserved questions. It does not independently
judge answer meaning, reviewer independence or factual correctness. A supplied
`typed-client` observation stays separate from `ai-text`, `ai-voice` and
`participant` observations. A file hash verifies integrity, not truth.

All cases are developer-authored. Reserve participant discoveries and independently
authored questions as a later hold-out set, labelled before tuning. Record
latency, task completion, clarification, misconceptions, assistance required and
accessibility problems separately from factual correctness. Do not use a single
score that hides rights, privacy or source failures.

## Architects of Tomorrow: 7 October 2026

The catalogue includes five short activities for novice participants aged 13–14
at the Swansea event. They suit the Hello World and Reimagining DVLA Services
themes: choose a user need, find a source, explain a word, try an invented file,
choose an accessible view and prepare a five-minute presentation. They do not
claim a connection to DVLA systems. Do not use real driver, vehicle, account or
other personal records.

The activities total 65 minutes and can sit within the two-hour build period.
Leave the remaining time for the team's own idea, making and rehearsal. They are
an optional evaluation route, not a replacement for the event's instructions.
Use the owner-selected facilitator-led shared screen and offline activities.
The plan does not require participant AI accounts; table sizes and local device
arrangements still need event coordination. Participants can speak, type, point or ask a
volunteer to operate the interface; the evaluation is about the design, not a
test of the participant.

For the five-minute presentation, show who the idea helps, one working example,
one source, one limitation and one improvement. A small webpage or a clear sketch
can be a valid outcome. A safe refusal with a useful next step can also be a
successful evaluation result.

## Planned intake and voice boundaries

The planned feature rows cover Shapefile folders/component files/ZIPs and links,
GeoJSON, GeoPackage, GeoParquet, text, CSV, spreadsheets, presentations, remote
files/folders, deterministic joins and evidence-bearing output. Each needs its
own parser, limits, rights/provenance handling and failure examples. Naming a
format is not support for every variant or the other files it references.

The new local preview is a narrower facility with an explicit support table in
its interface. It does not fetch remote URLs, upload the selected contents or
turn documents into instructions. Full spatial import, formula/macro execution,
map calculation and hosted PSGA access are not admitted by this corpus.

Voice-driven page tools can select a fixed example, presentation or explanation.
Native host voice routing, reliable transcription, cancellation, turn-taking,
correction and use by actual participants require separate observed tests.
An available microphone or registered page tool is not a voice acceptance result.

## Run the concrete local intake fixtures

[`local-fixtures.v1.json`](local-fixtures.v1.json) contains 30 concrete synthetic
GeoJSON/table/text, Shapefile companion, ZIP, URL and recognised-format cases.
Each names its child facility, teaching question, specification and exact
structured result checks. The classifier's guidance for unsupported binary
formats is evaluated as guidance, never as successful data import.

Build the intake package immediately before execution:

```sh
pnpm --filter @gis-ai-go/experience-intake run build
node scripts/experience_evaluate.mjs --run-local-fixtures \
  --output artifacts/experience/local-fixtures.json
```

The report retains fixture, source and executed-module digests, each actual check
and its result. It reports those deterministic executions separately from all
222 natural-language questions. Folder browser callbacks and page-state actions
have their separate Vitest tests; this runner does not claim to operate the
browser, drop a physical folder, interpret speech or test a participant.

For a blocked evaluation attempt, set `status` to `blocked`, use an empty
`assertionResults` array and set `blockReasonCode` to one of `authentication`,
`client-unavailable`, `unsupported`, `input-not-available`, `timeout`, `permission`
or `other-reviewed`. Retain the same minimal, sanitised evidence binding.
A blocked attempt stays unassessed and cannot carry assertion passes. Omitted
`status` means `completed` for existing observation files.

Optional `rubric` fields make facilitator observations comparable without scoring
a participant: `taskCompletion` is `independent`, `one-hint`, `repeated-help`,
`not-completed` or `not-assessed`; `comprehension` is `own-words`, `partial`,
`not-yet` or `not-assessed`; `sourceCorrectness` is `correct`, `incorrect` or
`not-assessed`. Optional `latencyMs` records an observed non-negative whole number
up to one hour. Keep these dimensions separate from the assertion verdicts and
from each other. They are supplied reviewer observations, not automated judgements.
