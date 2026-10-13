# CI impact routing

Status: shadow evaluation; no assurance check is skipped.

## Safe first slice

The complete repository gate, primary gateway-image gate and protected-main
independent gateway derivation still run for every event on which they previously
ran. Their producers now start independently instead of waiting for repository
assurance. The stable required `assurance` job still fails unless:

- the repository gate succeeds;
- the primary gateway-image gate succeeds; and
- the candidate shadow impact planner succeeds; and
- the separate trusted-base shadow agreement job succeeds.

Protected-main Pages and gateway provenance keep their existing downstream evidence
requirements. The independent gateway derivation has no producer input, so it also
starts independently on protected main. No required-check name changes.

Superseded runs for the same pull request are cancelled. Push runs use the unique
GitHub run identity as their concurrency key, so this policy neither cancels nor
coalesces protected-main runs.

## Shadow planner contract

The versioned map at
`.github/ci/verification-impact-map.v2.json` declares selectable lanes, their
dependencies and repository-path rules. `scripts/plan_ci_impact.py` reads the exact
event-base-to-head Git change inventory, filters recommendations to lanes that run
for that pull-request or protected-main event, and emits canonical JSON. The output
records:

- both exact commits and the map SHA-256;
- every changed path and matching rule;
- dependency-expanded lane decisions;
- unmatched paths; and
- whether a full plan was selected; and
- the closed Boolean `gateway_image_required` decision.

The Boolean remains a Boolean in the canonical plan. Only the workflow output
boundary converts it to the exact string `true` or `false`. Both candidate and
agreement jobs start with `true` as their fail-full default. The agreement job
replaces its default only after the base-owned verifier produces a valid receipt.
Both routing Booleans are checked at the output boundary. A missing planner
result, missing field or any other scalar cannot become a skip recommendation.

The planner accepts an explicit `--repository-root`. Its script bytes can therefore
come from a separately checked-out policy source while the Git inventory, map and
new output remain bounded to the named worktree. The root must be a real directory
and the exact Git top level; nested directories and symbolic-link aliases fail
closed. The candidate job runs this interface against the candidate checkout. On a
separate runner, the agreement job extracts its verifier and planner from exact
base Git blobs and treats candidate policy and output as data. Both outputs remain
diagnostic and do not control which assurance jobs run.

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
| Locked OKF research input | Repository and gateway derivation chain | All existing checks run |
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

The planner and map in a pull-request head are untrusted while that pull request
can change them. Shadow reporting executes that candidate on a separate runner and
cannot skip verification. The agreement stage compares the base policy with the
candidate policy and selects full assurance if either result is missing, fails or
disagrees. Workflow, planner, map and routing-test changes select full assurance.
A revised policy is eligible for future enforcement only after it has merged under
full checks and passed exact-main verification; it must never authorise a reduction
of its own checks. The current diagnostic workflow does not verify that historical
acceptance itself.

Before enforcement, the outer workflow also needs protection. As recorded in
[ASSURE-209 #97](https://github.com/chris-page-gov/gis-ai-go/issues/97), requiring a
status name alone does not bind the check to trusted workflow code. Enforcement
needs an organisation required workflow bound to a protected source, or an external
gate whose required status is bound to a trusted GitHub App. CODEOWNERS declarations
alone do not establish enforced review or independent approval.

The OKF source lock is part of the dependency contract. Its three research-pack
JSON inputs are not ordinary documentation: `scripts/build_okf.py` consumes them
to create the deterministic projection used by Explorer and the gateway image.
Contract tests therefore require every path in `okf/source-lock.json` to select
both repository and gateway-image assurance, including rename handling and a
mutation test which removes a mapping entry.

The v2 contract test evaluates every path tracked at its introduction: all 832 had
an explicit rule, and each of the 235 tracked files admitted to the gateway build
context required gateway-image assurance. The assertions retain those baseline
lower bounds and automatically evaluate newly tracked paths, so an unmapped new path
or an image-context omission fails before routing can be promoted.

## Trusted agreement stage

The v2 baseline at `97bc45635a91064cd78f06bf0848ad7636f05439` did not implement
agreement. The October increment implements a **shadow comparison**, with separate
candidate and agreement runners. It does not establish the external enforcement
boundary described above. Implementation and acceptance evidence is recorded in
[CI impact agreement](CI_IMPACT_AGREEMENT.md).

The agreement job obtains both verifier and planner from the exact event base,
without running candidate preparation. The trusted planner reads both maps from
Git objects and evaluates the same base-to-head inventory. On pull requests, head
means the exact GitHub merge commit also checked by the existing assurance jobs;
it is deliberately not just the source-branch tip. A candidate artefact must match
the base evaluator's reconstruction of that candidate policy, including identities,
paths, map digest and strictly typed decisions. Incompatible planner changes are
conservative full recommendations.

Only two valid, agreeing `false` recommendations can produce `false`. Missing,
malformed, failed, stale or disagreeing results produce `true`; protected-main
pushes and control changes also remain full. If the verifier does not yet exist
in the base, the workflow records a full bootstrap decision instead of trusting the
new verifier to approve its own introduction.

The workflow still does not use `gateway_image_required` in an assurance job
condition. The stable aggregator requires the candidate planner, agreement job,
repository and gateway-image producers to succeed. Receipts are diagnostic
artefacts retained for 30 days, not a permanent or signed audit trail.

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
