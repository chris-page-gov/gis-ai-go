# SITES-218: private Sites MCP pilot

Started: 1 October 2026. Updated: 2 October 2026. Status: private version 7
deployed; smoke, five-repeat evaluation, three protocol checks, stop/reinstatement
and receipt-retention checks passed; code rollback and final restoration verified.
Database recovery and wider acceptance remain incomplete.

Public work item: [issue #138](https://github.com/chris-page-gov/gis-ai-go/issues/138).

## Authority and outcome

The owner authorised unattended implementation of the recommended private Sites
MCP experiment, with live OS and ONS APIs, common questions, performance assessment
and a repeatable evaluation harness. Entitlement and credential details are held
in the private working record. Use existing included allowances only: no new paid
services, chargeable overage, new provider terms or wider audience. Replacement
of the private Sites API test token is authorised only if required for testing.
An ingress token is not proof of authenticated end-user identity.

Retain the existing owner-private Site and its captured-CPIH demonstration. Use
a separately named live pilot and evidence contract. Do not alter the supported
v0.1.0 release, exact-five v0.2.0 boundary, immutable research or earlier evidence.
The owner has separately authorised bounded PSGA validation, including NGD.
Admission still needs the recorded product, hosting, purpose and recipient
conditions; the observed deployed tools remain the open-data fallback.

## Baseline and current checkpoint

- Initial canonical baseline: `7496595a1c09f3cac7ca9da2bef69a25443516a9`.
- Deployed public runtime source: `8ab0f592ce949f136501122f93bb81becbeb1af1`.
- Implementation branch: `codex/sites-mcp-pilot`.
- Existing Site: version 7, owner-private, successful deployment, `has_mcp: false`.
- Hosted D1 contains the legacy `web216_cpih_snapshot` plus the separately named
  `sites_pilot_allowance_v1` and `sites_pilot_receipts_v1` tables. The later checkpoint
  contains 33 pilot receipts, all inspected into a complete application checkpoint.
  All 33 records matched the pre-stop checkpoint after final rollback/restoration,
  with every content binding verified and zero provider requests; a full database
  backup/restore remains unproved.
- The signed-in owner browser successfully called capabilities without another
  sign-in or an application test token. The deterministic harness separately
  passed nine enabled cases over 13 wire exchanges and eight upstream attempts.
  The owner-browser geography query returned five Warwick MSOA codes with
  explicit partial coverage and a receipt.
- Five repetitions of five cases all passed: 25 case calls, 45 wire exchanges,
  25 upstream attempts and 20 new receipts. Separate June 2025 and July 2026
  protocol preflight/denial runs passed with zero upstream attempts.
- Removing the pilot origin and redeploying version 7 produced `503`; restoring
  the origin and redeploying restored access without allowance refill. An
  immediate post-deployment `500` remains unexplained despite later success.
- Code rollback to version 5 passed pilot-route absence and the complete legacy
  redirect/demo sequence. Final version 7 restoration passed comparison of all
  33 checkpoint receipts and retained the owner-only audience; the two earlier
  incorrect route expectations remain in the record.
- The [separate NGD validation](SITES-218_NGD_VALIDATION.md) passed bounded local
  Building v4 and Road Link v5 structural checks. Full feature-schema conformance
  and hosted admission remain open; no protected tool was added to version 7.
- Required Repository assurance, Gateway image and CodeQL pull-request checks
  passed for runtime revision `8ab0f592`; final exact-revision integration and
  protected-main evidence are tracked in [PR #139](https://github.com/chris-page-gov/gis-ai-go/pull/139).
- Exact supported native MCP build declaration: blocked in available guidance. The live
  connector exposes connection metadata, but generic Sites prose does not supply
  the declaration schema. The current official build package also contains no
  declaration schema. Do not invent it. The authorised private test-token route
  can exercise the separately guarded `/pilot/mcp` endpoint with native OAuth
  acceptance still pending.
- See the [hosted observation](SITES-218_HOSTED_OBSERVATION.md) for public results,
  per-case performance, packaging lessons, stop/reinstatement results and pending
  rollback/restoration results and remaining database-recovery limits.
  Exact private source/deployment identities and raw observations remain private.

## Work and acceptance

| Work | Status | Acceptance evidence |
| --- | --- | --- |
| Current capability and focused repository review | Documented; all 11 reported GitHub alerts classified, complete registry audit still unavailable | Versioned matrix, dependency reachability limits and architectural decision |
| PSGA/open-data rights and account assessment | Open-data admission documented; authorised local NGD structural checks passed | [Rights assessment](../operations/SITES_MCP_RIGHTS_ASSESSMENT.md) and [NGD validation](SITES-218_NGD_VALIDATION.md); full-schema and hosted admission remain open |
| Supported native MCP declaration and OAuth | Blocked: exact declaration unavailable | Published `has_mcp: true`, returned connection metadata and actual authenticated calls |
| Bounded OS Names, OS product metadata, MSOA names/codes and maintained ONS CPIH | Live smoke passed | Six provider cases passed; protected capabilities remain disabled |
| Distributed provider allowance and evidence persistence | Local failure/concurrency tests pass; all 33 checkpoint receipts independently verified and unchanged after final rollback/restoration | Four allowance rows remain at 41 cumulative attempts; final receipt comparison made zero provider requests; cloud concurrency and full database restore remain separate |
| Common-question corpus and evaluation harness | Nine smoke cases and 25 repeated case calls passed on version 7 | [Runbook](../operations/SITES_MCP_PILOT_EVALUATION.md); full selected corpus on `2025-11-25`, preflight/denial checks on `2025-06-18` and `2026-07-28`; four conditional cases unadmitted |
| Private deployment | Version 7 live verified | Successful deployment, owner-only audience, three application tables, owner-browser capabilities and bounded ONS geography query |
| Deployed correctness and exploratory performance | Smoke and five-repeat evaluation passed | Five samples per selected case; per-case median/range only, no pooled p95, load or service-level claim |
| Operator stop and receipt retention | Passed within the bounded observations | Origin removal produced `503`; reinstatement restored access and two byte-equal checkpoint receipts; unexplained transient `500` retained |
| Application rollback and data restoration | Four rollback route assertions and final version 7 all-33-receipt comparison passed; database restore unproved | Failed redirect expectations and transient `500` retained; application checkpoint is not a SQL/schema backup |
| Protected-main assurance and hand-off | Runtime-revision PR checks passed; exact final acceptance tracked separately | Repository assurance, Gateway image and CodeQL passed for `8ab0f592`; see PR #139 for final integration/protected-main evidence |

## Proposed initial questions

1. Which named places match Warwick, and which is the town rather than station?
2. Where is the selected place's representative point, in which CRS?
3. Which OS open products and versions support place or identifier discovery?
4. What CPIH index is available for a specified month, with source and release?
5. How did the index change between two specified months?
6. Which MSOA 2021 names and codes match a specified name prefix?
7. What evidence supports the previous result?
8. Why can this open-data pilot not return every address or infer occupants?

Population, Census households and point-to-MSOA joins are candidate extensions,
not advertised capabilities until their actual sources and contracts pass.
The full evaluation corpus will retain both supported and conditional questions.

## Usage and reporting

Record provider attempts centrally before egress, including failed attempts. Keep
provider limits separate from Codex account usage and Sites storage/hosting
allowances. Use small declared request/concurrency bounds; never claim an
unverified billing stop. Codex observations remain in the private working record.
They reflect account-wide usage, not this task's token or money cost.
Do not redeem the available reset without a separate explicit request.

Detailed live runs, authentication material, source credentials and account
identifiers remain private and ignored. Public documents contain only cleared
capability facts, aggregate observations, source hashes and limitations.

## Continuation

Continue independent implementation while platform/rights prerequisites are
resolved. Update this checkpoint after tests and each material deployment event.
The separate [OS/ONS-to-OKF feasibility proposal](OS_ONS_OKF_FEASIBILITY.md)
describes catalogue/specification modelling and indicative effort; it activates
no roadmap stage or spending authority.
Do not restart preservation or unrelated historical reviews. A complete repository
rewrite is not indicated by the focused review; assess the deployed dependency
closure, authentication, providers, storage and harness before expanding scope.
