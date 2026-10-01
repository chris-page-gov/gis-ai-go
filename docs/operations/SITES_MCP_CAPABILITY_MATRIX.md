# Sites MCP capability and acceptance matrix

Assessment date: 1 October 2026. Owner: Chris Page.

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

The rows below are the initial assessment, not an automatically refreshed status
page. Attach dated, source-bound run evidence when a row changes. Preserve failed
and unavailable observations; do not replace them with a green summary.

## Platform, publication and client contract

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| Site identity and audience | **Live verified:** the existing GIS AI GO WebMCP Explorer is active and owner-private. Public access is an available setting, not the selected audience. Private identifiers remain in the deployment record. | Re-read owner-only access before and after each deployment. Do not create a replacement project or broaden access. |
| Existing source | **Source verified:** recovered source matches its private provenance record. Its manifest contains only `project_id`, `d1: "DB"` and `r2: null`; its build uses the pinned `@openai/sites-vite-plugin` `0.2.0`. | Bind the pilot package to exact reviewed source, lockfile, dependencies and archive hashes in private evidence. Verify the pushed source branch before saving. |
| Native MCP declaration | **Blocked:** current publication reports `has_mcp: false`. Requesting MCP connection metadata returns the missing-MCP-declaration error. The official Sites guide and available connector schemas do not specify the build-time declaration. **Source verified:** the current official build plugin, `0.2.0`, contains no MCP declaration schema or implementation. | Obtain the exact supported declaration from current official implementation or documentation; do not invent a manifest field or infer declaration from an HTTP route. |
| Packaging | **Documented:** save accepts an archive of build output from the exact pushed source SHA. The archive must contain `.openai/hosting.json` and a supported Worker entrypoint, or `index.html` in the declared static directory. | Inspect the final archive for required files, integrity, unintended source maps, secrets and private data. Build and run that exact artefact locally. |
| Publication | **Documented:** saving and deployment are distinct; each deployed URL is production. The owner-private combined operation saves the exact pushed version and deploys it without changing access. | Record version number, source SHA, archive hash, deployment identifier, terminal status and audience readback. Do not save a duplicate version when retrying an already-saved deployment. |
| HTTPS and domains | **Live verified:** the existing generated HTTPS Site URL is deployed. **Documented:** custom domains exist where enabled. This is not a negative-case TLS or Host/Origin test. | Use the current generated hostname. Check canonical authority, unauthenticated responses, redirects, certificate and hostile Host/Origin cases against the actual deployment. |
| MCP transport | **Documented:** connection metadata exposes a Streamable HTTP URL. Existing captured-data code uses a separate browser-facing endpoint. **Untested:** native direct-client transport for this Site. | After `has_mcp: true`, use the exact returned URL; test initialisation, negotiated protocol, tool listing, calls, notifications, cancellation, errors and unsupported streaming. Record exact SDK and client versions. |
| OAuth and client setup | **Documented:** `get_site` with `include_mcp_connection: true` returns the exact `mcp_url`, `oauth_resource` and optional provisioned `plugin_id` when ready. The local Codex CLI supports `--oauth-resource`. | Preserve returned values unchanged. Exercise metadata discovery, valid owner login, invalid/expired token, wrong resource and revoked access. Provisioning a plugin does not prove installation or a successful call. |
| Independent clients | **Untested:** direct authenticated Codex and independent Claude connections to the native Site service. Browser sign-in succeeded on 19 September and is a separate observation. | Capture exact-version client discovery and a bounded successful call with matching receipt; compare server output. Record an unavailable client honestly. Do not repeat the completed browser sign-in prerequisite without a new failure. |
| Browser and WebMCP | **Source verified:** the prior workbench has manual and page-tool paths. Earlier local tests used synthetic identity. Registration alone does not prove host invocation. | Exercise the deployed manual path and genuine page-tool invocation; verify visible result/provenance parity and accessible failure states. |

## Identity, rights, network and provider controls

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| Platform identity | **Documented:** Sites forwards authenticated visitor email and optional full name to server code. Browser sign-in paths are platform-managed. **Untested:** equivalent owner identity on native MCP requests. | Verify which identity reaches the Worker after supported MCP OAuth. Reject missing/untrusted identity. Test that caller-supplied identity headers cannot grant owner access. Keep personal identity out of public evidence. |
| Workload identity | **Unestablished:** visitor authentication does not establish workload identity or provider entitlement. | Record the actual provider credential mechanism and its limitation. Do not claim it satisfies DEPLOY-207's non-static workload-identity requirement. |
| OS entitlement | **Private assessment:** the owner has supplied entitlement context for review. The organisation, account and credential details are not publication material or blanket rights clearance. | Record exact product, member/contractor capacity, permitted purpose and current terms privately. Admit a protected route only after checking third-party hosting, storage and client/model transmission against that authority. Never publish a credential location or value. |
| Open-data fallback | **Proposed initial scope:** OS Open Names, admitted OS open-product metadata, ONS MSOA 2021 name/code lookup and maintained ONS CPIH L522/MM23, using source-native fields and current licence attribution. Availability is explicit per provider. | Verify actual API, key requirements, bounded request, response identity and licence. A blocked protected request may offer an explicitly different open-data capability; never label an approximation as the same answer. |
| Licensed output | **Blocked pending rights evidence:** owner-only access is an audience control, not proof that processing by Sites or an AI client is allowed. | Keep protected outputs out of fixtures, source, public receipts, logs and retained evaluation payloads. If rights are unresolved, leave the capability disabled and continue open data. |
| Provider selection | **Proposed:** fixed server-authored OS and ONS routes; no arbitrary URL, SQL, callback or dataset execution. Discovery is not execution authority. | Test exact host/path and parameter allowlists, redirects, encoded bypasses, unknown fields, excessive result limits and unsupported datasets. |
| Egress | **Documented:** Sites supports HTTP/HTTPS/WebSockets and excludes raw inbound/outbound TCP. **Untested:** provider access and application restrictions in the deployed Worker. | Use Fetch with fixed destinations and redirect rejection; bound bodies and time. Exercise blocked destinations without disclosing credentials. Application allowlisting is not platform-wide deny-default networking or pinned-address TLS. |
| Secrets | **Documented:** hosted environment values are separate from source and manifest and require redeployment to take effect. | Put only the necessary OS credential in server runtime secret storage. Check built browser assets, logs, errors and receipts for absence of credentials; verify rotation/removal and missing-key refusal. |
| Test ingress credential | **Authorised if needed:** ordinary guarded MCP at `/pilot/mcp` may use `x-sites-pilot-test-token`, checked against a server-configured SHA-256 value, behind the private Sites audience. This is a separate test-authentication mode, not a signed-in owner or native Sites OAuth. | Record token type without value, minimise lifetime, keep it out of arguments/logs/source and test rejection after removal. Preserve Sites ingress checks. Do not use it to mark OAuth or owner-identity acceptance passed. |
| Provider allowance | **Proposed:** one D1-backed allowance shared by browser, MCP, evaluation and all Worker instances, plus bounded per-request concurrency and deadlines. No chargeable overage or new paid service is authorised. | Atomically reserve before each outbound attempt, including retries; deny when exhausted or accounting is unavailable. Verify concurrent exhaustion, restart, cancellation, provider error and no-refund behaviour. Record a separate OS and ONS request count. |
| Response interpretation | **Proposed:** deterministic schema/geometry/time-series processing; the MCP server embeds no LLM. | Test native identifier, unit, geography and period preservation; distinguish CPIH index from percentage change. Missing/ambiguous place or statistical coverage must produce clarification/refusal rather than invented results. |

## Persistence, operation and performance

| Aspect | Evidence and current status | Next test or prerequisite |
| --- | --- | --- |
| D1 | **Live verified:** `DB` and legacy `web216_cpih_snapshot` exist. No row content or successful hosted receipt write was established by the October structure readback. **Documented:** 10 GB per Site. | Add only separately named pilot tables. Exercise atomic allowance and receipt operations against real local D1 and hosted D1. Preserve the legacy table and its capture-backed semantics. |
| R2 | **Documented:** object storage is available and has no fixed storage limit stated; account limits still apply. **Source verified:** the existing Site has no R2 binding. | Do not provision R2 unless an accepted use needs it. No R2 backup claim follows from the platform offering the service. |
| Evidence receipts | **Proposed:** a distinct pilot family with source/deployment identity, bounded input, provider provenance, timestamps, response digest, licence and measured phases. | Reject data success when required receipt persistence fails. Test concurrent writes, duplicate request handling, inspection, hash mismatch and lost-response uncertainty. A hash is not independent source authenticity. |
| Retention | **Unaccepted:** retention metadata is not an implemented retention operation. | Define actual pilot retention and deletion, including logs, request identifiers and provider-derived data. Prefer permitted metadata/digests; test expiry/deletion. Record any platform-managed copies that cannot be independently verified. |
| Backup and restoration | **Untested:** a database's existence is not a backup. Version rollback does not imply data rollback. | Export a permitted checkpoint, retain its digest independently, restore only into a separately approved pilot target and compare every required field. Record RPO/RTO observations and limits; do not reset legacy data. |
| Code rollback | **Live verified:** prior saved Site versions exist. **Untested:** a pilot rollback rehearsal. | Record the baseline, deploy a compatible candidate, restore the baseline version and confirm behaviour and database compatibility. Disable provider use before rollback if the old version lacks current controls. |
| Data rollback detection | **Proposed:** retain an independent latest checkpoint outside the database being checked. | Demonstrate detection of an older internally valid snapshot. A same-database hash chain cannot independently detect restoration of the whole database. |
| Concurrency and cancellation | **Source verified:** legacy wrapper has per-isolate capacity and cancellation controls; this is not a global quota. | Test the pilot under overlapping clients, multiple isolates where observable, client cancellation and provider timeout. Hold capacity until work settles; an aborted response is not proof that no request or write occurred. |
| Observability | **Documented:** connector exposes Worker logs and deployment status; Site analytics are not MCP/provider metrics. | Retain redacted request/receipt identifiers, phase timings, provider counts and failure classifications. Test that keys, tokens, prompts, emails and protected response bodies do not enter retained logs. |
| Performance | **Untested:** no live pilot latency or throughput baseline yet. | Run a fixed bounded corpus. Report sample count, success/refusal/error counts, p50/p95/max end-to-end and provider timings, bytes, concurrency, warm/cold conditions and observation time. Do not attribute client/model latency to Sites alone. |
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

This is local working-tree evidence with synthetic credentials and identity. It
is not cloud D1 concurrency, genuine provider egress, Sites identity, native OAuth,
deployment, throughput or protected-main acceptance evidence. The live rows above
remain unproved until the corresponding deployment observations are retained.

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
