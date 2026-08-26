# CI impact routing

Status: shadow evaluation; no assurance check is skipped.

## Safe first slice

The complete repository gate, primary gateway-image gate and protected-main
independent gateway derivation still run for every event on which they previously
ran. Their producers now start independently instead of waiting for repository
assurance. The stable required `assurance` job still fails unless:

- the repository gate succeeds;
- the primary gateway-image gate succeeds; and
- the shadow impact planner succeeds.

Protected-main Pages and gateway provenance keep their existing downstream evidence
requirements. The independent gateway derivation has no producer input, so it also
starts independently on protected main. No required-check name changes.

Superseded runs for the same pull request are cancelled. Push runs use the unique
GitHub run identity as their concurrency key, so this policy neither cancels nor
coalesces protected-main runs.

## Shadow planner contract

The versioned map at
`.github/ci/verification-impact-map.v1.json` declares selectable lanes, their
dependencies and repository-path rules. `scripts/plan_ci_impact.py` reads the exact
event-base-to-head Git change inventory, filters recommendations to lanes that run
for that pull-request or protected-main event, and emits canonical JSON. The output
records:

- both exact commits and the map SHA-256;
- every changed path and matching rule;
- dependency-expanded lane decisions;
- unmatched paths; and
- whether a full plan was selected.

The planner is fail closed. An invalid map, missing commit, malformed or unsafe
path, unknown Git status, empty change set or unmatched path selects full assurance
or stops the stable gate. Rules cannot enable skipping because the workflow does
not consume lane outputs in a job condition. The plan is uploaded only as a
30-day diagnostic artefact.

Every protected-main push selects all lanes, regardless of its paths. The current
Pages and gateway artefacts bind the exact source commit, and `main` remains
releasable, so path routing cannot omit that evidence chain.

Representative current decisions are:

| Change | Shadow recommendation | Current execution |
| --- | --- | --- |
| QUAL-206 harness or fixture | Repository assurance | All existing checks run |
| QUAL-206 schema | Repository and gateway derivation chain | All existing checks run |
| Documentation | Repository assurance | All existing checks run |
| Workflow, lock or toolchain | Full assurance | All existing checks run |
| Unknown path | Full assurance | All existing checks run |
| Any protected-main push | Full exact-commit assurance | All existing checks run |

Gateway runtime and contract paths expand through the independent derivation,
cross-verification and provenance dependencies. Canonical OKF changes additionally
select Pages provenance because they affect both published products.

## Promotion gate

Do not use the plan to skip a check until shadow evidence demonstrates all of the
following:

1. representative documentation, QUAL-206, Explorer, OKF, gateway, execution,
   schema, workflow, dependency and release changes are covered;
2. every unmatched or ambiguous path selects full assurance;
3. recommended lanes have no false negative against the complete checks;
4. dependency-map and workflow-contract mutations select full assurance;
5. protected-main and release transitions retain complete evidence and provenance;
   and
6. branch protection continues to require the stable fail-closed `assurance` job.

The next optimisation decision should use retained shadow plans and full-run
outcomes, not assumptions about filenames alone.

## Expected time effect

Recent full runs show roughly 4 to 5 minutes of repository work and roughly 7
minutes of primary gateway-image work in a previously serial pull-request path.
Running those producers together should reduce an unchanged successful pull-request
critical path by about 4 to 5 minutes. Starting the independent derivation at the
same time should reduce protected-main completion by a similar order, subject to
runner allocation and network variance. Pull-request cancellation additionally
avoids completing obsolete runs; its saving is the remaining duration of each
superseded run.

Shadow planning itself adds one small checkout and a dependency-free Python pass.
It does not yet save runner minutes because skipping remains disabled.
