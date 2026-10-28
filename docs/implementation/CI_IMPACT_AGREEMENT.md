# ASSURE-209: trusted-base shadow agreement

Date: 13 October 2026. Scope: implementation of the missing comparison in
[issue #97](https://github.com/chris-page-gov/gis-ai-go/issues/97). This increment
does not enable selective checks or close that issue's external trusted-gate work.

## Why the change is needed

At the case study's pinned baseline,
`97bc45635a91064cd78f06bf0848ad7636f05439`, the workflow ran the candidate planner
and map only. Its own design explicitly said that trusted agreement was not
implemented. The peer review's principal criticism is correct for that baseline.

The [source-document intake](../research/2026-10-13/governance-as-code/README.md)
preserves the owner-supplied revised meeting briefing and peer review as public
DOCX derivatives and Markdown extracts. The review assessed an earlier 11-page
case study, not the revised briefing or [PR #147](https://github.com/chris-page-gov/gis-ai-go/pull/147).
The briefing remains a dated draft; its header claims about models and reviewers
are unverified. These documents provide evidence for discussion, not operational
authority or endorsement, and retain their source rights.

The reported mutation is reproducible: moving `.github/**` and
`scripts/plan_ci_impact.py` from `global-assurance-control` into the documentation
rule leaves a structurally valid map, but makes those paths recommend repository
assurance without gateway-image assurance. Candidate-owned tests can also be
changed. Structural validation alone therefore cannot establish policy authority.
All existing assurance jobs still ran at that baseline; the mutation did not
actually skip them.

## Implemented comparison

1. `ci_impact_candidate` runs the existing candidate planner with read-only contents
   permission and no persisted checkout credential. Its artefact is untrusted data.
2. `ci_impact_shadow` runs on a fresh runner. It obtains the agreement verifier and
   evaluator from exact base Git blobs. No candidate package installation or Python
   preparation runs there. Isolated Python loads only the extracted base evaluator.
3. The base evaluator reads base and candidate maps as bounded regular Git blobs
   and uses the same exact event-base-to-CI-head inventory. Renames include both
   paths. The pull-request head is the checked GitHub merge commit, matching the
   full assurance jobs.
4. A candidate plan must match a reconstruction by the base evaluator. This binds
   the entire closed schema, exact commits, event, paths, map digest and decision
   types. Duplicate keys, non-finite numbers and Boolean substitutes are rejected.
5. Only agreement on two valid `false` decisions can recommend omitting the image.
   Control changes, protected-main pushes, failed jobs, absent or malformed data,
   incompatible output and disagreement retain full assurance.
6. When the verifier is absent from the base, a bootstrap receipt records full
   assurance. The newly introduced verifier never approves its own introduction.

`assurance` requires both planning jobs and both existing assurance producers to
succeed. No assurance job consumes the new routing decision. Diagnostic receipts
are retained for 30 days; they are not signed attestations or a durable audit archive.

## What this does and does not establish

| Claim | Evidence and limit |
| --- | --- |
| The baseline review identified a real gap | Candidate-only workflow and explicit future-stage design at the pinned baseline; reproduced re-routing mutation. |
| A base-owned comparison can be implemented | New verifier, separate workflow job and regression tests. First introduction deliberately uses full bootstrap. |
| With the declared workflow unchanged, candidate Python cannot change the comparison process on its runner | Separate jobs; comparison imports only extracted base code and reads candidate maps/plans as data. |
| The entire GitHub gate is independent of the candidate | **Not established.** The workflow definition remains in the pull-request tree. |
| Workflow changes require independent approval | **Not established.** The observed personal-repository ruleset does not require code-owner or other approval. |
| Selective routing is ready for enforcement | **Not established.** External gate identity, policy acceptance history and the promotion evidence remain prerequisites. |
| The new comparison reduces runner time | **Not claimed.** It adds diagnostic work while full checks continue. |

On 13 October, a read-only inspection of
[Protect main ruleset 21059910](https://github.com/chris-page-gov/gis-ai-go/rules/21059910)
found active strict `assurance` requirements and no bypass actors, but zero required
approving reviews and no required code-owner or last-push approval. These are
time-specific observations of external settings, not properties proved by the
versioned CODEOWNERS file. Settings may change independently of this document.

## Acceptance and remaining gates

Local checks cover the original planner and workflow contracts plus the new
agreement's real-Git scenarios: valid omission, runtime/full routing, changed
controls, the reported weakened map, rename/delete, malformed and substituted
plans, stale identities, missing/failed candidates and protected-main pushes.
The focused suite passed 87 tests: 35 planner, 20 agreement and 32 workflow
contracts. Workflow tests execute the extraction, bootstrap and scalar-publication
shell blocks. Independent code review found no actionable issue within the stated
shadow scope. Changelog, local-link and baseline secret checks also passed.
The current change's PR and CI runs are the authority for canonical acceptance;
local success does not imply a merged or deployed control.

The document intake also updates the packaged source-rights notice, its exact
publication/image hashes and the affected deterministic local evaluation receipts.
Receipt outcomes remain non-live and unscored; historical acceptance pins are
unchanged. The regenerated receipts passed their existing runner and 33 contract
tests; the publication build and 110 bundle/image contracts passed.

Repeated image-scan failures exposed an observability gap: the existing privacy
filter correctly withheld raw exception output but could not identify the failing
scanner stage. Closed stage exit codes now identify that stage without publishing
exception text or altering scanner pins, vulnerability policy, evidence checks or
quarantine handling. The diagnostic increment passed 149 focused tests and an
independent review. A stage label is diagnostic evidence, not a successful scan.

Before describing this as an enforced protection against a change author:

- bind the required workflow to a protected organisation source, or bind an
  external required status to its trusted GitHub App identity, as specified in #97;
- verify that the selected base policy has passed its required exact-main checks;
- retain representative full-run comparisons and dependency-mutation evidence with
  no false-negative routing decisions;
- check cancellation, skipped-job and escalation behaviour against the selected
  lanes, preserving full main/release assurance; and
- agree review ownership and durable evidence retention for the deployment context.

The initial implementation PR can demonstrate bootstrap only. A subsequent
documentation-only PR and a control-changing PR are needed to observe the
base-owned agreement in GitHub once its source exists in the accepted base.
The [routing promotion gate](CI_IMPACT_ROUTING.md#promotion-gate) remains in force.

Rollback is to revert this increment through the existing full assurance workflow.
It removes diagnostics; it does not restore checks that were skipped, because none
are skipped by this change.

## Wording for the meeting paper

The pinned baseline demonstrates versioned policy, validation, full defaults and
shadow evaluation. A subsequent implementation adds isolated comparison against
the existing base policy. It remains diagnostic: all checks still run. Promotion
requires evidence of safe selection and an externally protected enforcement point.
The case therefore demonstrates both executable governance mechanisms and the
explicit limits of what repository code alone can establish.

Do not replace the baseline paper's links with claims about a future revision.
Cite the implementation PR for proposed code, and cite the accepted commit and
observed runs only after those exist. This also preserves the distinction between
per-change agreement and the later acceptance of a revised policy.
