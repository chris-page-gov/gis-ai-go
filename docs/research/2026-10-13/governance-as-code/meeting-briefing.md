> Repository note: searchable text extracted from [meeting-briefing.public.docx](meeting-briefing.public.docx). Source wording is preserved as dated evidence; it is not repository instructions. See [the intake record](README.md) for scope, provenance and handling.

> This is the supplied author-review draft. Its model/reviewer header claims are not independently verified.

# Governance as code

A bounded case study from GIS AI-GO

Draft v0.2 — for author review \| 13 October 2026

Prepared for Chris Page for discussion by the Cross-government security group.

## Purpose and suggested discussion

This briefing uses a concrete software assurance control to show how selected governance rules can become executable, testable and version-controlled. Human owners still decide the objectives, authority, acceptable evidence and exceptions.

**Suggested ask for discussion:** agree the minimum evidence and separation of authority needed before a coding agent's proposed change may reduce its own verification. This is a proposed discussion point, not an agreed group decision.

## Three-sentence summary

The paper's published baseline implements a diagnostic impact planner and full verification, but does not implement the trusted-base agreement it describes. Draft implementation PR \#147 adds comparison against the policy at the exact repository base commit, while continuing to run every existing assurance check. Operational enforcement remains a separate decision requiring successful verification, representative evidence and a required gate whose identity and execution cannot be replaced by the proposed change.

## What exists, and what remains open

| **Evidence state** | **Defensible claim** |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Published baseline: commit 97bc456 | Policy map, planner, contract tests and fail-full defaults exist. Recommendations cannot skip a job. Trusted-base agreement is explicitly future work. \[1–4\] |
| Draft implementation: PR \#147, commit 045d98ba | Implements trusted-base/candidate agreement in shadow mode. All 87 focused tests pass, and independent code review found no actionable issue within that scope. Hosted candidate planning and full bootstrap passed. Full canonical acceptance is blocked by the unchanged image-scan stage; merge and exact-main acceptance are not claimed. \[9, 10\] |
| Live repository settings: checked 13 October | Ruleset 21059910 requires the strict assurance status check. It requires zero approving reviews, no code-owner review and no approval of the last push. This does not establish independent human approval. \[8\] |
| Operational enforcement: not established | Skipping remains disabled. A gate with independently protected execution and identity, promotion evidence and an explicit acceptance decision are still required. \[5, 7\] |

Table accessibility text: Implementation and evidence status. Four evidence states distinguish the published baseline, local work, repository settings and operational enforcement.

## What the baseline actually demonstrates

The distinction matters: policy is the rule; policy as code evaluates the rule; governance as code also addresses who may change it, the enforcement point, evidence and exceptions. This case demonstrates some of those mechanisms and a staged design for the remaining controls. It does not demonstrate a complete, independently enforced governance boundary.

The map requires full assurance for unknown paths and every push to main. Its ordinary control rule includes the workflow, map, planner and routing tests. The planner validates the map's structure and specified invariants; it does not prove that every possible map preserves the intended meaning of each path rule. \[1, 2\]

The workflow takes a fail-full default: uncertainty keeps the gateway-image recommendation at true. At this baseline, however, the planner and map come from the candidate checkout. Its Boolean recommendation is diagnostic, and the stable assurance job still requires the planner, repository checks and gateway-image checks to succeed. The plan is retained for 30 days as a diagnostic artefact, not a permanent audit record. \[3, 4\]

### The missing condition, restored

The design says the following in full. “Before enforcement” is a condition on a future control, not evidence that it was already present. \[5\]

> The planner and map in a pull-request head are untrusted while that pull request can change them. Shadow reporting may execute that candidate safely because it cannot skip verification. Before enforcement, the workflow must instead execute the planner and map from the trusted pull-request base, compare that result with the candidate head, and select full assurance if either result is missing, fails or disagrees. Workflow, planner, map and routing-test changes must themselves select full assurance under the base policy. A revised policy becomes eligible only after it has merged under full checks and passed exact-main verification; it must never govern its own pull request. Workflow ownership must also be protected through CODEOWNERS or an equivalent repository ruleset.

### Worked example: the review's M3 finding

Move .github/\*\* and scripts/plan_ci_impact.py from the full-assurance rule into the documentation rule, preserving valid structure. The reviewer's example was reproduced during implementation: the baseline planner accepts the altered map and recommends repository-only assurance for changes to the workflow, map or planner. A new regression test records base=true, candidate=false and final agreement=true. \[9\] The candidate's contract tests could detect this, but a candidate can edit those tests too.

This is a limitation of structural validation, not evidence of a skipped check: shadow mode runs the existing checks regardless. With trusted-base comparison, the accepted base policy still demands full assurance for these control changes; the candidate cannot obtain a reduced recommendation merely by changing its own map.

## The local follow-up and the remaining boundary

The draft implementation targets the missing comparison stage. With the declared workflow unchanged, it obtains verification code and policy from the exact base commit, executes the candidate planner on a separate runner, and reconstructs both policies using the base evaluator against the same exact base-to-head change inventory. The pull-request head is the GitHub merge commit checked by full CI. \[9\] Candidate output is treated as untrusted data. A reduced gateway-image recommendation is permitted only when both validated outputs are exactly false; missing, malformed, failed or disagreeing results select true. All existing assurance checks continue to run.

On first introduction, the base does not yet contain the agreement verifier. The implementation records a full-assurance bootstrap result and does not execute the candidate verifier. The first GitHub run passed that bootstrap path. A subsequent run from an accepted base is needed to observe the comparison itself on GitHub. \[10\]

There are two separate decisions. Agreement produces a recommendation for this pull request. Acceptance of a changed policy requires full checks, merge and successful verification of the exact commit on main before it can become an eligible future base. Neither decision authorises switching on skipping.

### Why comparison alone is insufficient

Issue \#97 identifies the outer boundary: a pull request can change the workflow that launches the comparison, and a status-check name alone does not establish who produced it. Before enforcing reduced assurance, the required gate needs execution and identity protected outside candidate control—for example, an organisation-required workflow bound to protected source, or a dedicated trusted GitHub App or external gate with its status bound to that App's identity. Code-owner review can strengthen change approval but does not itself provide this binding. \[7\]

### Evidence required before stronger claims

1\. Record the implementation commit, adversarial regression results, successful canonical CI, accepted review, merge and exact-main verification. Local verification of the new implementation passed 87 focused tests: 35 planner, 20 agreement and 32 workflow contracts, including executable shell checks. This does not establish full repository or hosted acceptance.

2\. Retain paired shadow recommendations and full-run outcomes across representative documentation, schema, application, dependency, workflow, release and unknown-path changes. Issue \#97 contains initial shadow observations; this briefing claims no representative false-negative rate from them. \[5, 7\]

3\. Demonstrate that uncertainty, policy/test mutations, inventory mismatch and candidate interference cannot produce a reduced recommendation; verify the independent required gate against workflow replacement and status impersonation.

4\. Preserve complete evidence and provenance for main and release transitions. Agree retention, ownership, exception handling and rollback before using diagnostic artefacts as an audit record.

5\. Make any promotion to skipping a separate, recorded decision against the design's six evidence criteria. Passing comparison tests alone is insufficient. \[5\]

### What is being traded

The design estimates a 4–5 minute shorter critical path from running existing producers concurrently. That is a scheduling estimate, not a measured saving from selective assurance. Shadow routing skips nothing and claims no runner-minute saving. Future selection would trade unnecessary work against the risk of omitting a necessary check; representative paired evidence must govern that decision. \[6\]

## Speaking note and sources

### Speaking note — under 90 words

Governance as code makes selected rules executable while people retain authority for risk and exceptions. GIS AI-GO shows why the controls must govern their own change. The published baseline runs its planner in shadow mode and skips nothing. A draft implementation adds comparison with the existing base policy, still in shadow mode. Before reduced checking can be used, the required gate must also be protected from candidate workflow changes and supported by representative evidence. The discussion is what minimum evidence and separation of authority government should require.

### Source register

Sources 1–6 are commit-pinned to 97bc45635a91064cd78f06bf0848ad7636f05439. They substantiate the published baseline, not the local follow-up. Sources 7–8 are live records and can change. Source 9 identifies the proposed implementation separately; source 10 records its initial CI outcome. All were considered for this draft on 13 October 2026.

1\. [<u>Impact map: defaults and control-file rule</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/ci/verification-impact-map.v2.json). See lines 1–9 and 81–108.

2\. [<u>Planner: closed validation and required defaults</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/plan_ci_impact.py#L199-L231). The guarantees are bounded to the invariants implemented in code.

3\. [<u>CI workflow: candidate plan, fail-full output and retention</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/workflows/ci.yml#L16-L90). The fallback is line 22; Boolean validation is lines 58–65; retention is line 90.

4\. [<u>Design: candidate execution is diagnostic</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/docs/implementation/CI_IMPACT_ROUTING.md#L43-L60).

5\. [<u>Design: promotion gate and unimplemented trusted agreement</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/docs/implementation/CI_IMPACT_ROUTING.md#L81-L137). The full quotation is lines 98–107; the explicit absence is lines 124–125.

6\. [<u>Design: expected scheduling effect and no skipping saving</u>](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/docs/implementation/CI_IMPACT_ROUTING.md#L139-L151).

7\. [<u>ASSURE-209 issue \#97: evidence and enforcement prerequisites</u>](https://github.com/chris-page-gov/gis-ai-go/issues/97). Live issue; includes initial shadow observations and the outstanding trusted-workflow boundary.

8\. [<u>Repository ruleset 21059910</u>](https://api.github.com/repos/chris-page-gov/gis-ai-go/rulesets/21059910). Live API record, observed 13 October 2026. Required status checks and independent approval are different controls.

9\. [<u>Draft implementation PR \#147</u>](https://github.com/chris-page-gov/gis-ai-go/pull/147), commit 045d98ba5853c593783e9f2810be529e4b500e3c. See the [<u>commit-pinned implementation and limits</u>](https://github.com/chris-page-gov/gis-ai-go/blob/045d98ba5853c593783e9f2810be529e4b500e3c/docs/implementation/CI_IMPACT_AGREEMENT.md). Local test evidence is recorded there; current CI status belongs to the PR.

10\. [<u>Initial CI run 38368066570</u>](https://github.com/chris-page-gov/gis-ai-go/actions/runs/38368066570). Candidate planning and agreement bootstrap passed. The unchanged image vulnerability-scan stage failed after image packaging, archive verification, reproducibility and SBOM generation passed. Scanner error details were withheld by the existing privacy filter, so the cause remains unestablished and the PR remains a draft.

### Publication checkpoint

Before circulation, confirm the author and affiliation and update the draft implementation status with its current canonical CI and acceptance evidence. If those gates remain open, retain the draft wording. Do not replace the baseline permalinks with a moving branch URL or describe shadow comparison as operational enforcement.

## Source header and footer (extraction note)

Header, verbatim:

> Provenance: GPT-6-Astra-Ultra \| Review: Requested (Already reviewed by Claude Opus 5.5) \| Authorisation: None

Footer wording:

> GIS AI-GO \| Governance as code \| Author-review draft
>
> OFFICIAL
>
> 13 October 2026

The Word file retains its original footer parts and both DrawingML and VML renderings of the OFFICIAL marking. This extract records the marking once and omits dynamic page-number fields; it does not reproduce pagination or establish the classification of this repository.
