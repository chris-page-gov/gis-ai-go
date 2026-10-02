# Sites MCP capability and acceptance matrix

Assessment started: 1 October 2026. Hosted checkpoint: 2 October 2026.
Owner: Chris Page.

This is the evidence register for the **private live-data pilot** proposed in
[ADR-0018](../decisions/ADR-0018-private-sites-live-pilot.md). It does not accept
the supported public gateway, close DEPLOY-207 or change the supported release.
The initial public repository baseline is
`7496595a1c09f3cac7ca9da2bef69a25443516a9`. Private Site identities, source
revisions and account observations are retained in the private deployment record.
Track this increment in [issue #138](https://github.com/chris-page-gov/gis-ai-go/issues/138).

## Evidence labels

- **Live verified** means a current platform readback or retained deployed
  observation establishes the specific fact stated. It does not imply adjacent
  controls passed.
- **Documented** means current official documentation or a callable tool schema
  describes the capability; the pilot has not necessarily exercised it.
- **Source verified** means inspected source establishes configuration or code,
  not deployed behaviour.
- **Untested** means the next observation is required before the claim is made.
- **Blocked** identifies the missing prerequisite. Continue independent work.

The rows below include the [version 7 hosted smoke](../implementation/SITES-218_HOSTED_OBSERVATION.md)
against public runtime revision `8ab0f592ce949f136501122f93bb81becbeb1af1`.
They are not an automatically refreshed status page. Attach dated, source-bound
run evidence when a row changes. Preserve failed
and unavailable observations; do not replace them with a green summary.

## Platform, publication and client contract

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| Site identity and audience | **Live verified:** version 7 was active after final restoration with the owner-only audience and no group/external access. Private identifiers remain in the deployment record. | Re-read owner-only access before and after each future deployment, stop and rollback. Do not broaden access. |
| Existing source | **Source verified:** recovered source matches its private provenance record. Its manifest contains only `project_id`, `d1: "DB"` and `r2: null`; its build uses the pinned `@openai/sites-vite-plugin` `0.2.0`. | Bind the pilot package to exact reviewed source, lockfile, dependencies and archive hashes in private evidence. Verify the pushed source branch before saving. |
| Native MCP declaration | **Blocked:** current publication reports `has_mcp: false`. Requesting MCP connection metadata returns the missing-MCP-declaration error. The official Sites guide and available connector schemas do not specify the build-time declaration. **Source verified:** the current official build plugin, `0.2.0`, contains no MCP declaration schema or implementation. | Obtain the exact supported declaration from current official implementation or documentation; do not invent a manifest field or infer declaration from an HTTP route. |
| Packaging | **Live verified:** version 7 accepted the archive retaining root hosting metadata and `dist/server`, `dist/client` and generated migration trees. Local and platform-returned archive digests are distinct observations. | Follow the [assembly instructions](../../sites/private-pilot/README.md). Do not flatten the layout; verify archive contents and exact returned source/version metadata. A successful archive does not establish a native MCP declaration. |
| Publication | **Live verified:** version 7 completed deployment. Saving and deployment remain separate operations; a repeated save for one source revision can return an existing version. | Preserve each attempted archive and returned metadata. A corrected local archive alone does not prove new bytes were accepted. Verify actual schema and runtime behaviour after each publication. |
| HTTPS and domains | **Live verified:** the existing generated HTTPS Site URL is deployed. **Documented:** custom domains exist where enabled. This is not a negative-case TLS or Host/Origin test. | Use the current generated hostname. Check canonical authority, unauthenticated responses, redirects, certificate and hostile Host/Origin cases against the actual deployment. |
| MCP transport | **Live verified:** ordinary guarded `/pilot/mcp`, finite JSON, passed the smoke and repeated provider corpus on `2025-11-25`; `2025-06-18` and `2026-07-28` passed preflight and two denial cases each, with no provider attempts. | Provider success under the other revisions and independent clients need separate tests. Native acceptance requires `has_mcp: true` and returned connection metadata; the ordinary route is not native registration. |
| OAuth and client setup | **Documented:** `get_site` with `include_mcp_connection: true` returns the exact `mcp_url`, `oauth_resource` and optional provisioned `plugin_id` when ready. The local Codex CLI supports `--oauth-resource`. | Preserve returned values unchanged. Exercise metadata discovery, valid owner login, invalid/expired token, wrong resource and revoked access. Provisioning a plugin does not prove installation or a successful call. |
| Independent clients | **Untested:** direct authenticated Codex and independent Claude connections to the native Site service. Browser sign-in succeeded on 19 September and is a separate observation. | Capture exact-version client discovery and a bounded successful call with matching receipt; compare server output. Record an unavailable client honestly. Do not repeat the completed browser sign-in prerequisite without a new failure. |
| Browser and WebMCP | **Live verified:** the signed-in owner browser called capabilities and retrieved five Warwick MSOA codes with explicit partial coverage and a receipt, without another sign-in or test token. **Source verified:** the pilot page adds no WebMCP registration. | Exercise other provider journeys, accessible failure states and genuine page-tool invocation separately. The prior workbench is a distinct surface. |

## Identity, rights, network and provider controls

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| Platform identity | **Live verified:** ordinary signed-in owner-browser capability access works on version 7. **Documented:** Sites forwards authenticated visitor identity. **Untested:** equivalent owner identity on native MCP requests. | Keep spoofing, unauthorised access and native OAuth tests separate. Reject missing/untrusted identity and retain no personal identity in public evidence. |
| Workload identity | **Unestablished:** visitor authentication does not establish workload identity or provider entitlement. | Record the actual provider credential mechanism and its limitation. Do not claim it satisfies DEPLOY-207's non-static workload-identity requirement. |
| OS entitlement | **Private assessment:** bounded PSGA/NGD validation was authorised. **Locally observed:** Building v4 and Road Link v5 access and limited structural checks passed in the [separate report](../implementation/SITES-218_NGD_VALIDATION.md). Version 7 remains open-data only. | Complete feature-schema and product/recipient admission gates in the [rights assessment](SITES_MCP_RIGHTS_ASSESSMENT.md). A successful credential request alone does not prove its plan or hosted recipient arrangements. |
| Open-data fallback | **Live verified:** six provider cases passed for OS Open Names, admitted OS product metadata, ONS MSOA 2021 names/codes and maintained CPIH L522/MM23. Native fields and attribution were checked. | Extend only through explicit source/rights admission. A named place is not a protected address lookup; MSOA name matching is not containment. |
| Licensed output | **Pending hosted admission:** local NGD access/structural checks passed; full feature-schema validation remains blocked by source-schema and validator gaps. Protected bodies were not retained, and no protected tool was added to version 7. | Resolve the Road Link required-field case mismatch, pin geometry references and enforce temporal formats. Keep protected output out of public artefacts and admit a profile only after rights/technical review. |
| Provider selection | **Source/local verified:** fixed server-authored routes, closed inputs and bounded outputs. **Live verified:** six admitted provider cases succeeded and protected/extra-entitlement cases were denied. | Keep hostile destination, redirect, input and provider-failure tests in the local injected suite. Discovery is not execution authority. |
| Egress | **Live verified:** the Worker completed eight upstream attempts across the admitted OS/ONS routes during the smoke. **Documented:** HTTP/HTTPS/WebSockets are supported; raw TCP is excluded. | Retain fixed destinations, redirect rejection and body/time bounds. This is application allowlisting, not platform-wide deny-default networking or pinned-address TLS. |
| Secrets | **Documented:** hosted environment values are separate from source and manifest and require redeployment to take effect. | Put only the necessary OS credential in server runtime secret storage. Check built browser assets, logs, errors and receipts for absence of credentials; verify rotation/removal and missing-key refusal. |
| Test ingress credential | **Live verified:** the smoke harness passed through private platform ingress and the separate `x-sites-pilot-test-token` gate, checked against a server-configured digest. Ordinary owner-browser access was verified separately. | Test revocation/removal and retain no token values. Neither test-token success nor browser success completes native OAuth acceptance. |
| Provider allowance | **Source/local verified:** shared D1 admission, failure/cancellation accounting and no-refill migration; two per-isolate slots. **Live verified:** four complete rows total 41 attempts and remained unchanged through observed stop, restoration and rollback comparisons. | Hosted overlapping-isolate exhaustion remains unproved. Application counters are not provider account totals or a financial billing stop; no chargeable overage or new paid service is authorised. |
| Response interpretation | **Live verified:** admitted smoke outputs passed native identity, unit, period, source and receipt-binding assertions. **Source verified:** deterministic processing with no embedded LLM. | Add natural-language host evaluation separately. CPIH index levels are not published inflation rates; ambiguous or absent coverage must not produce invented results. |

## Persistence, operation and performance

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| D1 | **Live verified:** three application tables, 33 fully inspected pilot receipts and all four allowance rows captured. Every receipt matched the pre-stop checkpoint after final rollback/restoration; legacy table had zero rows before/after. **Documented:** 10 GB per Site. | Hosted concurrency and full database restore remain unproved. Connector projections truncate large cells; they are not complete SQL/schema exports. |
| R2 | **Documented:** object storage is available and has no fixed storage limit stated; account limits still apply. **Source verified:** the existing Site has no R2 binding. | Do not provision R2 unless an accepted use needs it. No R2 backup claim follows from the platform offering the service. |
| Evidence receipts | **Live verified:** all 33 checkpoint records were exported via MCP inspection; after final version 7 restoration every content binding verified and every record matched the independent pre-stop checkpoint. The comparison made zero provider requests. | This proves all-record retention for the observed transitions, not independent provider authenticity, full database restoration or detection of arbitrary whole-database rollback. |
| Retention | **Unaccepted:** retention metadata is not an implemented retention operation. | Define actual pilot retention and deletion, including logs, request identifiers and provider-derived data. Prefer permitted metadata/digests; test expiry/deletion. Record any platform-managed copies that cannot be independently verified. |
| Backup and restoration | **Application checkpoint verified:** 33 complete receipt records and four allowance rows retained independently. **Unproved:** full database/schema snapshot and restore. Connector cell truncation prevents treating its projection as a backup. | Use a supported full export/restore operation when available; prove restoration separately. No accepted RPO/RTO follows from a checkpoint or code rollback. |
| Operator stop | **Live verified:** removing the admitted origin and redeploying version 7 produced `503`; origin restoration and redeployment restored receipt access without allowance refill. | This does not cancel requests already issued. Test-token revocation is a separate operation; retain the private configuration/recovery record. |
| Code rollback | **Live verified:** version 5 passed pilot `404`, root/demo redirects and final demo `200`; final version 7 restoration passed all 33 retained-receipt comparisons and owner-only audience readback. | Preserve the first two failed route expectations and an unexplained immediate post-deployment `500`. Code rollback is not data restoration or a clean-transition SLA. |
| Data rollback detection | **Proposed:** retain an independent latest checkpoint outside the database being checked. | Demonstrate detection of an older internally valid snapshot. A same-database hash chain cannot independently detect restoration of the whole database. |
| Concurrency and cancellation | **Source verified:** legacy wrapper has per-isolate capacity and cancellation controls; this is not a global quota. | Test the pilot under overlapping clients, multiple isolates where observable, client cancellation and provider timeout. Hold capacity until work settles; an aborted response is not proof that no request or write occurred. |
| Observability | **Live verified:** the harness retains wire/case counts, safe errors, receipt/digest references and separate client, server and provider timing fields without provider payloads. **Documented:** Worker logs and deployment status are available. | This does not establish platform-log redaction or a separate D1-write metric. Keep private identifiers and credentials out of public summaries. |
| Performance | **Live verified, exploratory:** five repeats of five cases all passed at concurrency one; per-case medians range from 1,658 to 2,230 ms. The [hosted observation](../implementation/SITES-218_HOSTED_OBSERVATION.md) gives each case's median/range. | Five samples per case support no p95; do not pool different operations. Concurrency-two/load, cold/warm status, throughput and service objectives remain unproved. |
| Dependencies and assurance | **Verified within scope:** runtime `8ab0f592` passed PR Repository assurance, Gateway image and CodeQL; 63 affected local contracts passed. All 11 reported GitHub alerts were classified as Undici development dependency findings; the Worker bundle excludes it. **Partial:** no complete registry audit. | Final exact-source/protected-main evidence is tracked in [PR #139](https://github.com/chris-page-gov/gis-ai-go/pull/139). Maintain affected tooling separately. The unchanged macOS executable pin still blocks that historical lane; Linux checks cannot prove it. |
| Budget and usage | **Documented:** Sites has plan-specific limits. **Owner boundary:** no new paid service or chargeable overage. Codex usage resets are separate from provider and hosting quotas. | Record Codex usage snapshots, Sites limits when exposed, OS transaction usage and application allowance separately. An application counter limits outbound attempts; it is not proof of a platform billing hard stop. Stop affected provider calls if zero-overage operation cannot be established. |
| Residency | **Documented:** Sites does not currently support data/inference residency guarantees for code, D1/R2, artefacts or logs. | Include this fact in protected-data admission. Do not infer UK-only storage from a UK owner or provider. |
| Support and recovery ownership | **Proposed:** Chris Page owns pilot stop, credential revocation, data removal and acceptance. No production SLA is established. | Provide executable stop and recovery instructions, named platform support route and exact failure evidence. Retain existing private support correspondence privately. |
| Supported release | **Unchanged:** the supported public product remains `v0.1.0`; full DEPLOY-207 binds a different OCI/POSIX/identity/networking contract. | Run required repository assurance for accepted changes. Report private experimental deployment separately from canonical acceptance, public interoperability and release. |

## Minimum deployment evidence record

Each run must identify the repository and Site-source commits, dependency lock,
deployment archive digest, Site version and deployment identifier, endpoint and
audience, protocol and client versions, provider policy and allowance, fixture
corpus identity, checks actually run, failures, and timestamped receipt references.
Do not include private credentials, personal identifiers or restricted payloads.
For each skipped gate, record its failed prerequisite and the independent work
that remains possible. An evaluation result is evidence of that run, not a new
grant of execution authority.

## Offline implementation checkpoint

The 1 October working-tree implementation passes 33 focused gateway tests in
[`sites-pilot.test.ts`](../../apps/mcp-gateway/test/sites-pilot.test.ts), after
building the evidence, provider-adapter and gateway packages. These use the
official MCP SDK with legacy `2025-11-25` and modern `2026-07-28` wire exchanges,
injected provider responses and real SQLite execution of the D1 statements.
They cover independent database connections sharing allowance, minute/lifetime
limits, full-store refusal, restart inspection, receipt tampering, closed inputs,
authentication and HTTP guards, failed receipt writes, no-refund cancellation,
and request capacity. Cancellation during admission, append and inspection keeps
capacity occupied until the actual application promise settles in both protocol
eras. Finite-method admission blocks subscriptions; an independent response guard
cancels unexpected SSE. The legacy path uses the SDK's explicit JSON transport
because its default stateless fallback does not apply the modern JSON setting.
Tests also assert source-native OS/ONS results and explicit incomplete geography
coverage.

This paragraph records local working-tree evidence with synthetic credentials
and identity. The separate version 7 hosted observation now establishes the live
facts explicitly labelled above. Neither observation establishes cloud D1
concurrency, native OAuth, throughput, database recovery or protected-main acceptance.

## Sources checked

- [Sites guide](https://learn.chatgpt.com/docs/sites), fetched 1 October 2026:
  supported shapes, authentication, storage, publication, secrets and limits.
- Current Sites connector schemas, inspected 1 October 2026: source-bound version
  saving, owner-private deployment, deployment status, database inspection and
  MCP connection metadata. These are callable-surface evidence, not a published
  build-time MCP schema.
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)
  and [MCP commands](https://learn.chatgpt.com/docs/developer-commands#codex-mcp),
  checked 1 October 2026; local `codex mcp add --help` confirms the URL and OAuth
  resource options.
- [Generic MCP authentication guidance](https://developers.openai.com/plugins/build/auth#triggering-authentication-ui):
  resource metadata, tool policy and challenges. Do not infer which parts Sites
  provisions without a deployed observation.
- [Official Sites Vite plugin package](https://www.npmjs.com/package/@openai/sites-vite-plugin),
  queried and inspected 1 October 2026. Registry `latest` resolves to `0.2.0`,
  matching the recovered Site lockfile. Its README, declarations and JavaScript
  export `sites(): Plugin`, copy hosting metadata/migrations and implement
  simulated local sign-in; they contain no native MCP declaration contract.
  The retrieved archive SHA-256 is
  `efad8b273a3f7eb43b8fecebf1cde16338684f9cda602c67492903b6127c2a70`;
  its SHA-512 integrity matches the pinned lockfile. Local simulated identities
  are development fixtures, not hosted authentication evidence.
- [Existing hosted experiment](../implementation/WEB-216_HOSTED_STORAGE_EXPERIMENT.md)
  and [DEPLOY-207 admission](DEPLOY-207_PROVIDER_NEUTRAL_ADMISSION.md).

The official pages describe capabilities at the assessment date. Pin or record
the implementation version used for every later build and recheck changed
contracts before deployment.
