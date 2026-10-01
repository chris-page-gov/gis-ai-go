# SITES-218: private Sites MCP pilot

Started: 1 October 2026. Status: implementation and local assurance, not deployed.

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
PSGA data use remains conditional on rights for the actual hosting, purpose,
contractors and AI recipients; open-data operation is the fallback.

## Baseline and current checkpoint

- Canonical source: `7496595a1c09f3cac7ca9da2bef69a25443516a9`.
- Implementation branch: `codex/sites-mcp-pilot`.
- Existing Site: version 5, owner-private, successful deployment, `has_mcp: false`.
- D1 `DB` and `web216_cpih_snapshot` table exist; contents were not read during
  the capability assessment.
- Exact supported native MCP build declaration: blocked in available guidance. The live
  connector exposes connection metadata, but generic Sites prose does not supply
  the declaration schema. The current official build package also contains no
  declaration schema. Do not invent it. The authorised private test-token route
  can exercise the separately guarded `/pilot/mcp` endpoint with native OAuth
  acceptance still pending.
- Existing source has been recovered into an ignored local working copy.

## Work and acceptance

| Work | Status | Acceptance evidence |
| --- | --- | --- |
| Current capability and focused repository review | Documented, review fixes under test | Versioned matrix, findings and architectural decision |
| PSGA/open-data rights and account assessment | Open-data admission documented; protected use conditional | [Rights assessment](../operations/SITES_MCP_RIGHTS_ASSESSMENT.md) |
| Supported native MCP declaration and OAuth | Blocked: exact declaration unavailable | Published `has_mcp: true`, returned connection metadata and actual authenticated calls |
| Bounded OS Names, OS product metadata, MSOA names/codes and maintained ONS CPIH | Implemented; deployed checks pending | Synthetic hostile tests; direct upstream CPIH and area-name success; OS format-label mismatch corrected |
| Distributed provider allowance and evidence persistence | Implemented; 33 focused gateway tests pass | Atomic SQLite multi-connection allowance, receipt bounds, restart, tamper and cancellation tests across both protocol eras |
| Common-question corpus and evaluation harness | Implemented; deployed run pending | [Runbook](../operations/SITES_MCP_PILOT_EVALUATION.md), three protocol revisions and independently recomputed receipt hashes |
| Private deployment | Pending | Exact source/archive/version/configuration and access read-back |
| Deployed correctness and exploratory performance | Pending | Bounded run, failures retained, server/provider/client timings distinguished |
| Persistence, application rollback and data restoration | Pending | Independent checkpoint and observed restore; application rollback alone insufficient |
| Protected-main assurance and hand-off | Pending | Required CI, provenance, review and reconciled status |

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
Do not restart preservation or unrelated historical reviews. A complete repository
rewrite is not indicated by the focused review; assess the deployed dependency
closure, authentication, providers, storage and harness before expanding scope.
