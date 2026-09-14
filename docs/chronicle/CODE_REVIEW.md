# Assessment of the code produced by this process

Review baseline: `6c76c92a18da779766f8d49acbbd7dbbd31abb97`.
Review date: 14 September 2026. Two delegated reviews examine runtime and
provider code, and assurance/tooling/interfaces respectively. Their source coverage
registers distinguish complete reading, targeted tracing and structural inspection.
This is a repository code assessment; it is not an external security certification.

## Judgement

The code expresses its governance model through executable boundaries. Shared
contracts, one governed assembly, fixed provider profiles and receipt verification
make important decisions inspectable. This is a sound foundation for an exemplar.
The review also finds real maintainability and reliability work. The quantity of
tests and the presence of agent reviews did not remove all defects or prevent
large modules and repeated verification from accumulating.

The main outcome of the review is a staged plan that preserves the useful controls
while reducing their operating cost. File length indicates where review and change
are difficult; it is not itself proof of poor code. Similarly, canonical hashing
proves byte relationships, not that all underlying claims are true.

## What is working well

- The same application assembly supplies direct API and MCP operations, reducing
  semantic disagreement between interfaces.
- Authority is constructed by the service and evaluated against explicit policy;
  caller-supplied assertions cannot create entitlement.
- Provider requests have fixed targets, bounds and result validation. Source-native
  identifiers, rights and vintage remain visible.
- Receipt persistence, query reconciliation and inspection are explicit operations
  with failure tests; a lost response does not silently authorise a second query.
- The web applications keep manual interaction useful and separate experimental
  host support from deterministic application behaviour.
- Publication and image workflows tie accepted artefacts to source and independent
  verification, with a defined rollback route.

The detailed reports link each assessment to the relevant source.

## Priority findings

| Area | Finding | Intended response |
| --- | --- | --- |
| Local longevity | The approved cache expires; readiness does not assess its freshness | Define a visible data-validity contract and expiry regression |
| Readiness cost | One ready assessment repeats complete linked evidence replay | Reuse one verified result within the same assessment, with corruption tests |
| Execution control | Saturated work slots can reject cancellation traffic | Reserve bounded control capacity before broader execution workloads |
| Provider deadlines | Preparation and actual transport start need separate deadline checks | Test delayed lease start and preserve absolute caller deadlines |
| Failure evidence | CI omits the WebMCP browser failure directory from its upload | Retain both application failure artefacts |
| Dependency advisories | Three existing medium-severity alerts match locked Hono 4.13.3 | Record per-advisory reachability and a tested update/disposition before local-edition acceptance |
| Public scanning | Baseline credential signatures and excluded-tree traversal are limited | Strengthen publication checks and prune traversal without losing intended files |
| Ordinary builds | Test commands rebuild common dependencies repeatedly | Build once for ordinary tests, preserve independent clean-build phases |
| Modularity | Evidence, image and host-assurance modules combine many responsibilities | Extract one cohesive responsibility per reviewed change |
| Guidance | Several component documents still described Stage 0 or inactive states | Corrections included in this documentation work package |

These are priorities and observations, not a claim that the proposed runtime fixes
have already been implemented. The detailed reports distinguish source deductions
from executed reproductions and the effect on today's small local profile from
future expanded workloads.

## Review coverage and reproducibility

Read [the runtime review](reviews/RUNTIME_REVIEW.md) for gateway, shared packages,
provider adapter and Python execution coverage. Read
[the assurance and UI review](reviews/ASSURANCE_AND_UI_REVIEW.md) for scripts,
workflows, test patterns and both Explorers. Generated files and third-party vendor
code are outside source authorship review; pinned dependency and image scanning
are separate checks. Large assurance modules need their recorded depth to remain
visible; an inventory is not silently promoted into complete line-by-line review.

Historical protected-main CI is evidence for the baseline. Focused tests run during
the review are identified in the detailed reports. The whole suite is not rerun
merely to make a read-only finding sound stronger. Any implemented fix requires an
appropriate regression and the mandatory integration checks.

## What the review says about the development method

Contract-first implementation made intended behaviour visible and supplied useful
negative tests. Repeated independent reviews exposed defects before several
integrations. However, the same model family can share assumptions, and a producer
and verifier can share a bug if too much high-level logic is reused. Verification
independence must be designed and tested, not inferred from the number of agents.

The resulting code shows a preference for explicit small authority boundaries but
not consistently small modules. That trade-off deserves a measured second pass.
The [improvement stage](IMPROVEMENT_PLAN.md) makes this a separate implementation
programme with baselines, acceptance and rollback, rather than an unreviewed
refactor mixed into the retrospective.
