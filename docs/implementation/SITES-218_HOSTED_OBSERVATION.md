# SITES-218: private hosted observation

Observed on 2 October 2026. Status: bounded open-data smoke, repeated evaluation
and three protocol checks passed on private Site version 7. Operator stop,
reinstatement, receipt-retention and code rollback checks passed; database recovery
and wider operational acceptance remain incomplete.

This records the separate [private pilot](SITES-218_PRIVATE_MCP_PILOT.md), not
acceptance of the public gateway, DEPLOY-207 or a supported release. The packaged
public runtime revision is `8ab0f592ce949f136501122f93bb81becbeb1af1`.
Private Site identity, origin, source repository revision, archive/deployment
identifiers, credentials and raw observations remain in the private operating
record. A returned source revision is a binding checked by this experiment, not
independent build attestation or protected-main acceptance.

## What the deployment proves

The platform reported a successful version 7 deployment with the existing
owner-private audience. Hosted D1 inspection established three application
tables: the existing legacy `web216_cpih_snapshot`, plus
`sites_pilot_allowance_v1` and `sites_pilot_receipts_v1`. The new tables are separately
named; successful deployment status alone was not accepted as migration proof.

The existing signed-in owner browser successfully called the pilot capability
tool without an additional sign-in or application test token. Its ONS geography
query also returned five Warwick MSOA codes with explicit partial coverage and a
retained receipt. These prove those browser journeys, not every manual provider
path, accessibility acceptance, WebMCP invocation or independent AI-client
authentication. The new `/pilot` page does not register WebMCP tools.

The deterministic harness used the ordinary guarded `/pilot/mcp` route with the
authorised private test credential. The platform ingress and application test
gate are separate controls. This observation is not a native MCP OAuth exchange.
The publication still reports `has_mcp: false`, and the exact supported build-time
native MCP declaration remains unavailable. An HTTP route must not be presented
as platform-native MCP registration.

## Bounded smoke results

The retained run covered 00:38:52–00:39:17 BST on 2 October 2026
(23:38:52–23:39:17 UTC on 1 October). It used the pinned MCP client `2.0.0`,
protocol `2025-11-25`, one repetition and concurrency one. Preflight passed and
the run completed. All nine enabled cases passed their typed assertions:

| Cases | Observed result | New upstream attempts | New receipts |
| --- | --- | ---: | ---: |
| Q01–Q02 | OS named-place candidates and representative points | 2 | 2 |
| Q03 | OS Open Names product metadata | 1 | 1 |
| Q04–Q05 | Maintained ONS CPIH L522/MM23 index observations | 4 | 2 |
| Q10 | Inspection of an earlier result's matching receipt | 0 | 0 |
| Q11–Q12 | Protected capability disabled; extra entitlement input rejected | 0 | 0 |
| Q13 | Bounded ONS MSOA 2021 name/code matching | 1 | 1 |
| Total | Nine enabled cases passed | 8 | 6 |

There were 13 wire exchanges, including initialisation, the initialised
notification, discovery and SDK transport traffic. The SDK's GET received the
expected `405` for this finite POST-only service; it is not a failed question.
The four conditional corpus cases Q06–Q09 were not admitted or executed. This
does not establish population, Census overcrowding or point-to-MSOA containment.

The harness checked the expected six tools, source revision, result semantics,
licence/source metadata and independently recomputed receipt content bindings.
Q10 proves same-deployment inspection of a persisted result; persistence across
restart or redeployment needs the separate observation below. Reported provider
attempts and receipt inspection support this bounded run, not a hosted concurrency or
disaster-recovery claim. The report retains digests and measurements without
provider payloads. No model calls or protected PSGA queries were part of the run.

## Repeated evaluation and protocol coverage

The five-repeat run completed at 00:44:06–00:45:21 BST on 2 October, holding
version 7, protocol `2025-11-25` and concurrency one constant. All 25 case calls
passed. Its 45 wire exchanges produced 25 upstream attempts and 20 new receipts;
five receipt inspections produced no new provider request or receipt.

| Case and operation | Successful samples | Client median, ms | Client range, ms |
| --- | ---: | ---: | ---: |
| Q01: OS named places | 5 | 2,165 | 2,108–2,326 |
| Q03: OS product metadata | 5 | 2,193 | 1,919–3,363 |
| Q04: maintained ONS CPIH | 5 | 2,230 | 2,079–2,412 |
| Q13: ONS MSOA names/codes | 5 | 1,932 | 1,753–2,158 |
| Q10: preceding receipt inspection | 5 | 1,658 | 1,501–1,946 |

These rounded per-case measurements are exploratory. Five samples per case do
not support a p95; heterogeneous cases are not pooled to create one. There was
no load or concurrency-two trial, no demonstrated cold/warm Worker classification
and no model call. The timings do not establish throughput or a service objective.
Provider timing, server timing and end-to-end client timing remain separate
measurements; server timing does not isolate D1 writes. See the
[evaluation method](../operations/SITES_MCP_PILOT_EVALUATION.md) for the fixed
corpus, reporting rules and bounds.

Two further runs proved preflight, discovery and the Q11/Q12 denial cases with
protocols `2025-06-18` and `2026-07-28`. Both completed with two passing cases and
zero provider attempts; the June 2025 run used six wire exchanges and the July
2026 run used four. This is bounded protocol/denial coverage, not a repeat of the
successful provider corpus under those revisions, native OAuth or an independent
client implementation.

At the later database checkpoint, 33 pilot receipts existed. Cumulative attempt
counters were CPIH 16, geography 8, OS Names 8 and OS product metadata 9. These are
application counters, not provider account or billing totals. They include
browser activity beyond the harness's 33 smoke-plus-repeat upstream attempts.
A CPIH query uses two upstream attempts. The retained totals must not be presented as
one harness run or used to infer every query from one combined counter.

## Checkpoint, operator stop and deployment transitions

A complete application-receipt checkpoint was collected through 33 MCP inspection
calls, with every record's content binding checked. The private retained file is
116,108 bytes and has an independently recorded SHA-256 digest. All four allowance
rows were captured separately. The complete receipt collection and allowance
records are an application checkpoint, not a full SQL/schema snapshot or an
exercised database restore. The database connector's projections truncate large
cells; its tabular response cannot substitute for the complete receipt export.

Removing `SITES_PILOT_ORIGIN` and redeploying the saved version 7 produced the
expected `503` pilot refusal. Reinstating the exact origin and redeploying version
7 restored access. The first and last checkpoint receipts were inspected and
matched the retained records. The four allowance rows remained unchanged
at 41 cumulative attempts through these stop/restoration observations. This
establishes a working operator stop and sampled receipt retention across a real
deployment transition, not cancellation of an already issued upstream request.

The final rollback check successfully deployed the retained version 5 and passed
all four wire assertions: the pilot route returned `404`, `/` returned `307` to
`/demo.html`, that path returned `307` to `/demo`, and `/demo` returned `200`.
The first two test attempts had incorrect expectations about the static/demo
routes; those failures remain in the evidence and were not runtime fixes.
Version 7 restoration after the first two rehearsals passed two checkpoint-receipt
comparisons. The final version 7 restoration completed at 00:07:56 UTC on
2 October. Its two-receipt probe passed, followed by inspection of all 33 original
receipts: every content binding verified and every record was deeply equal to the
complete pre-stop checkpoint. This final comparison made zero provider requests.
Version 7 remained active with the owner-only audience and no group or external
access. The legacy capture table had zero rows before and after the observed
comparisons; no legacy content was overwritten or reset.

One immediate request after deployment returned an unexplained HTTP `500`.
The available Worker log readback showed no corresponding error, and a later
manual diagnostic passed two receipt checks. This does not establish the failure's
cause or prove a clean transition. Retain the failed response alongside subsequent
success; no zero-downtime, recovery-time or service-level claim follows. A rollback
changes code, while the additive pilot tables and allowance remain; it does not
restore earlier data.

## Packaging and migration findings

The accepted archive retains `.openai/hosting.json`, `dist/server/**`,
`dist/client/**` and the generated `dist/.openai/drizzle/**` tree. Do not flatten
the Worker output or relocate migration metadata. The source manifest and
generated hosting manifest must agree. The
[assembly instructions](../../sites/private-pilot/README.md) record the exact
layout, source binding and local built-Worker probe.

Record the local archive digest and the platform-returned digest separately;
platform normalisation can make them different. A repeated save for one source
revision can return an earlier saved version, so a corrected local archive is
not proof that the platform accepted new bytes. Preserve failed attempts and
inspect the returned version/archive record before deploying.

SQL, typed schema, journal and generated Drizzle snapshot must describe the same
additive migration, including SQLite primary-key nullability. The initial
provider rows are fixed operational configuration. Migration replay must not
refill or re-enable an existing allowance; ordinary HTTP requests must never
create tables or seed allowance. Hosted table inspection and actual receipt
writes now prove that the version 7 path works. They do not independently explain
every earlier packaging or migration failure, nor prove future platform
migration behaviour. Do not generalise the successful archive into an undocumented
native MCP manifest schema.

## Assurance and data boundaries

Focused gateway, provider and evaluation checks, plus the assembled Worker
experiment, cover synthetic failure, cancellation, receipt and allowance paths.
The current local assurance record also includes 63 passing impact-map and
evaluation-receipt contracts after canonical receipt regeneration. Sites paths
retain an explicit full-assurance route; the impact planner remains shadow-only.
Required pull-request Repository assurance, Gateway image and CodeQL checks
passed for public runtime revision `8ab0f592ce949f136501122f93bb81becbeb1af1`.
Final integration, exact-revision checks and protected-main acceptance are tracked
separately in [PR #139](https://github.com/chris-page-gov/gis-ai-go/pull/139);
the runtime-revision result must not be substituted for those checks.

The historical macOS capture lane is blocked by a changed `sandbox-exec` binary
identity. Its reviewed pin has not been weakened or refreshed in this pilot.
The earlier uv lock warning was a stale temporary symlink and was repaired;
the targeted HTTP capture/verifier regression then passed. Neither condition is
a live provider result. Linux CI cannot establish the blocked macOS-specific
observation, even if its applicable checks pass.

All 11 reported open GitHub default-branch dependency alerts were obtained and
classified: they concern development dependency Undici `8.10.0` through the
three Explorer/workbench applications. The runtime bundle excludes that package
and uses Workers native Fetch. The private Site's tooling separately contains
Undici `7.29.0`; these are not patched-tooling claims. The reviewed harness does
not exercise the affected WebSocket/interceptor features, but this does not clear
unrelated tooling paths or remove the need for dependency maintenance.

Dependency assessment therefore remains partial: classification of those alerts
is not a complete current registry audit of every transitive dependency or the
exact deployed archive. No alert was dismissed and no dependency upgraded by
that classification. Future OAuth-client adoption needs its own dependency and
issuer-binding review. The private Site's framework/build closure remains distinct
from the packaged MCP server/core and Zod closure.

The observed pilot uses only the admitted open-data capabilities. The owner has
separately authorised bounded PSGA validation, including NGD. The
[local NGD observation](SITES-218_NGD_VALIDATION.md) passed limited Building v4
and Road Link v5 structural checks and retrieved their public schemas/queryables.
It did not establish full feature-schema conformance: the Road Link schema has
inconsistent required-field casing, external geometry references were not
resolved, and strict date-time validation needs an explicit checker. Protected
routes remain disabled in this hosted version pending those technical gates and
the admission record in the [rights assessment](../operations/SITES_MCP_RIGHTS_ASSESSMENT.md).
Private access and a working credential alone do not establish product/recipient
conditions. The MCP
runtime embeds no LLM. Names are representative points, MSOA name matches are not
containment, and CPIH index levels are not separately published inflation rates.

## Pending observations

The following were still being tested when this checkpoint was written.
Replace each status only with its retained, source-bound observation:

| Observation | Current boundary |
| --- | --- |
| Full database backup and restore | Application checkpoint complete, but no complete SQL/schema snapshot or exercised database restore. Connector cell truncation prevents treating its projection as a backup. |
| Data restore and retention deletion | Unavailable through the currently exposed connector operations; no unreviewed administrative endpoint has been added. |
| Native MCP and independent clients | Blocked on the exact supported declaration and authentication contract. The successful test route does not close this gate. |
| Manual, accessibility and WebMCP journeys | Owner capability and bounded ONS geography requests verified; other provider journeys, accessibility and page-tool invocation remain separate. |
| PSGA and NGD validation | Local bounded access and structural checks passed; full feature-schema conformance and hosted rights/technical admission remain open in the separate report. |
| Dependency and canonical acceptance | All 11 reported GitHub alerts classified and runtime-revision PR checks passed; complete registry audit and final exact-revision acceptance remain separate, tracked in PR #139. |

The [capability matrix](../operations/SITES_MCP_CAPABILITY_MATRIX.md) remains the
dimension-by-dimension acceptance record. Retain both successful and failed
observations, without publishing private configuration, account records or
credential material.
