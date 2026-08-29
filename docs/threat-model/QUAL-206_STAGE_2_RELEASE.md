# QUAL-206 Stage 2 release threat record

Status: repository preflight accepted on protected `main`; activation and release
are not accepted.

Threat review date: 22 August 2026. Protected-main acceptance recorded on
23 August 2026.

Protected-main review starting point: commit
[`e65071dc1f1bb0baab852bbf8218f9b5f953ad02`](https://github.com/chris-page-gov/gis-ai-go/commit/e65071dc1f1bb0baab852bbf8218f9b5f953ad02),
merged through [pull request 48](https://github.com/chris-page-gov/gis-ai-go/pull/48).
The completed record and exact reviewed implementation merged through
[pull request 49](https://github.com/chris-page-gov/gis-ai-go/pull/49) as protected-main
commit
[`f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`](https://github.com/chris-page-gov/gis-ai-go/commit/f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a),
with passing protected-main CI, provenance and CodeQL.

## Decision boundary

This record integrates all 30 risks in the promoted
[`evaluation/threat-risks.json`](../../evaluation/threat-risks.json) baseline against
the controls implemented for the inactive open read-only `v0.2.0` repository
preflight, which starts from the protected-main commit above. It does not change the
baseline likelihood, impact or residual-risk judgements, and it does not edit the
immutable research evidence.

The reviewed generic production defaults still expose no tool or direct API
operation. The separate local container candidate now reports exact-five readiness
with production registration false; no provider call, public MCP service, registry
entry, tag or `v0.2.0` release exists. A repository control is evidence that a
specific implementation or denial path has been tested. It is not evidence that a
future public ingress, identity, storage, network or operating process supplies the
same control.

The preflight outcome is **hold for activation and release**. In particular:

- the historical protected-main Debian image retained three High findings without
  owner risk acceptance. The accepted protected-main UBI baseline removed those
  package instances in exact attested bytes. The later public-ingress source change
  changes image bytes and therefore needs fresh pull-request and protected-main
  image checks and attestations; owner acceptance remains necessary for any High or
  Critical finding that remains;
- the exact `data.query` approved-cache fallback is admitted only to the fixed local
  container and constructed by a closed builder; stale use is forbidden and no
  alternate-provider fallback exists;
- independent live-host, public-ingress, workload-identity, admitted persistent
  storage, externally retained checkpoint, scheduled backup, retention, disposal,
  shared-admission and real rollback evidence is absent;
  and
- the seven applicable local QUAL-206 receipts are non-live, unscored and explicitly
  incomplete; scored release-candidate and independent-host evidence remains absent.

The exact image finding status and exit conditions are in the
[QUAL-206 gateway image vulnerability disposition](../operations/QUAL-206_IMAGE_VULNERABILITY_DISPOSITION.md).

## Control evidence

The matrix below uses these repository evidence sources. Each keeps its recorded
boundary; inclusion here does not promote repository evidence to live evidence or a
release decision:

- [MCP-201 gateway candidate](../operations/MCP-201_GATEWAY_CANDIDATE.md) and
  [verification record](../operations/MCP-201_VERIFICATION.md);
- [EVID-204 inline evidence](../operations/EVID-204_INLINE_EVIDENCE.md),
  [durable ledger](../operations/EVID-204_DURABLE_LEDGER.md) and
  [provider-independent checkpoint and recovery](../operations/EVID-204_CHECKPOINT_RECOVERY.md),
  plus the
  [inspection transport](../operations/EVID-204_INSPECT_TRANSPORT.md);
- [EXEC-202 execution service](../operations/EXEC-202_EXECUTION_SERVICE.md) and its
  [focused threat notes](EXEC-202.md);
- [ADAPT-203 provider boundary](../operations/ADAPT-203_PROVIDER_PREFLIGHT.md);
- [TOOLS-205 registry](../operations/TOOLS-205_TOOL_REGISTRY.md),
  [selection](../operations/TOOLS-205_SELECTION_RESOLVE.md),
  [data query](../operations/TOOLS-205_DATA_QUERY_APPLICATION.md) and
  [transport](../operations/TOOLS-205_PUBLIC_READ_TRANSPORT.md);
- [QUAL-206 interoperability evidence](../operations/QUAL-206_INTEROPERABILITY.md);
- the
  [repository-only local evaluation receipt set](../../evaluation/qual-206-local-evaluation-receipts.v1.json);
  and
- [DEPLOY-207 blocked container assurance](../operations/DEPLOY-207_GATEWAY_CONTAINER.md).

The state labels mean:

- **controlled, activation gated** — a repository implementation and negative path
  exist, but deployment evidence remains necessary;
- **excluded, deny preserved** — the threat-bearing capability is outside the open
  `v0.2.0` scope and must remain inaccessible; and
- **unresolved release gate** — the repository evidence is insufficient for an
  activation or release decision.

## Integrated risk matrix

| Risk | Implemented repository control | State | Residual activation or release gate |
| --- | --- | --- | --- |
| RK01 — Prompt injection through metadata | Catalogue fields remain schema-bound quoted data; transport instructions explicitly say that returned metadata is never authority, and hostile instruction-like fixtures preserve it only as data. The local E17 receipt is repository-only, unscored and incomplete. | Controlled, activation gated | Repeat E17 as a scored release-candidate evaluation and complete `HOST-017` in independent hosts; retain suspension and record quarantine procedures for any poisoned source. |
| RK02 — Tool poisoning | The closed registry validates the exact 12 identifiers, names and lifecycle order; only explicit operation arrays can register a tool, planned profiles cannot become callable, and production arrays are empty. | Controlled, activation gated | Re-run discovery, schema-drift, repair-hint and emergency-suspension evidence against the exact activated assembly and public host. |
| RK03 — Confused deputy | Server-built anonymous-open authority, compiled public policy and module-private application identities prevent callers from supplying authority. A reconciled `data.query` face must use the exact linked evidence inspector. | Controlled, activation gated | The current gateway assertion is not workload authentication. Public deployment needs an admitted service identity and network policy; protected or delegated authority remains outside `v0.2.0`. |
| RK04 — Agent identity substitution | The open release does not accept a claimed agent, user, organisation or device identity as authority; client metadata is descriptive only. | Excluded, deny preserved | Do not add identity-derived access. Any later protected tier needs verified identity, audience and replay controls under a separate release decision. |
| RK05 — Token theft or replay | The ONS adapter uses no credential, gateway inputs accept no provider token, shipped activation is empty, and telemetry and evidence reject credential material. | Excluded, deny preserved | A public runtime still needs secret isolation and workload-credential rotation evidence. Tunnel or enterprise credentials cannot become service authority without a separate owner decision. |
| RK06 — Overbroad scopes | The candidate has one anonymous-open policy boundary, one fixed public ONS operation and an exact five-tool target; it exposes no OAuth scope or protected operation. | Excluded, deny preserved | Public workload permissions must be least-privilege and evidenced. Protected scopes, transaction permits and resource indicators belong to a later governed release. |
| RK07 — False device posture | Device posture is not an input to the anonymous-open policy, so a client cannot gain capability by asserting that it is managed or compliant. | Excluded, deny preserved | Keep protected and device-dependent routes absent. A future protected tier requires trusted posture evidence and freshness checks. |
| RK08 — Policy bypass | Direct, modern MCP HTTP and STDIO faces share the same application policy and receipt paths. Generic production capability lists remain empty. The container reasserts those defaults, then mounts only the branded exact-five assembly from fixed verified inputs with production registration false. | Controlled, activation gated | Protected integration must retain parity and the no-bypass construction. Public proxy, workload identity and policy-decision correlation remain unevidenced. |
| RK09 — Provider credential misuse | The fixed ONS Data API selection is anonymous, rejects credentials and proxies, and has no caller-controlled provider or URL. Production provider dispatch remains absent. | Excluded, deny preserved | Keep the open adapter credential-free. Protected providers, enterprise credentials and brokered identities require separate owner authority and isolated infrastructure. |
| RK10 — SSRF/arbitrary URL fetch | The adapter constructs one exact HTTPS origin, path and ordered query; it rejects caller URLs, ports, credentials, redirects, proxies and special DNS answers, and pins an accepted public address while retaining TLS hostname verification. | Controlled, activation gated | The authorised runtime must independently enforce domain-aware egress to the accepted ONS origin and paths. No public network policy exists yet. |
| RK11 — Licence/data exfiltration | The supported bundle and fixed ONS observation are public-only and preserve source-native rights and licence obligations. No export, protected cache or caller-selected destination is active. | Controlled, activation gated | Revalidate source rights and an empty ONS `Data Marking` immediately before activation. Keep PSGA, commercial and export paths absent. |
| RK12 — Cross-tenant/tier leakage | `v0.2.0` has one anonymous-open tier, no tenant context, no protected dataset and no dynamic shared result cache. Its approved fallback contains one public scalar only; protected and commercial profiles remain metadata. | Excluded, deny preserved | Do not introduce cross-tier storage or reuse. Any later tier needs physically isolated identities, storage, caches and conformance evidence. |
| RK13 — Cache poisoning | Catalogue, evidence and the one approved ONS fallback are checksum- or content-addressed and verified before use. The image admits only the exact T04 record; the container verifies its path, bytes and semantic identity before the closed builder constructs the branded cache internally. It remains usable only after exact policy approval and an eligible current failure from the pristine fixed adapter. | Controlled, activation gated | No default loader or environment override exists. Refresh the source and freshness decision, and retain forgery, replay, substitution, corruption, incomplete-coverage and stale-cache tests on the final candidate. |
| RK14 — Stale or revoked entitlement | No entitlement is used in the open release. Dataset edition, version, native dimensions, rights and public policy version are fixed and independently validated on success; the approved fallback has a fixed stale-after boundary and rejects stale reads. | Excluded, deny preserved | Revalidate version, rights and fallback freshness before activation and suspend on drift. Long-running protected entitlements remain outside this release. |
| RK15 — Malicious geometry | The private EXEC operation accepts one closed Polygon shape with explicit limits, finite-coordinate checks, self-intersection rejection and no silent repair; active `v0.2.0` operations accept no geometry. | Excluded, deny preserved | Keep spatial tools planned. Any later geometry type, transformation or spatial provider requires new parser, correctness and resource evidence. |
| RK16 — Archive/decompression bomb | Provider gzip input has independent compressed, expanded, JSON and output bounds with cancellation. The container verifier bounds and checks every OCI tar and layer; no user archive route exists. | Controlled, activation gated | Preserve the exact encoding allowlist and prove platform resource limits on the active candidate. Any new archive or encoding needs separate streamed limits. |
| RK17 — Expensive-query denial of service | `data.query` is fixed to one observation, two attempts and a 20-second ceiling; process-wide admission, response bounds, cancellation and the finite ledger/index ceilings fail closed. Container CPU, memory, process and descriptor limits are asserted. | Unresolved release gate | Public use needs shared admission and an operator decision for permanently pending claims, capacity exhaustion and reclamation. Local ceilings are not deployment quotas. |
| RK18 — Map/tile abuse | `map.render` remains planned and undiscoverable; no tile route, map token or map provider exists in the service candidate. | Excluded, deny preserved | Keep the profile non-active until a later release supplies rate, cost, rights, generalisation and complete non-App fallback evidence. |
| RK19 — Widget/WebMCP origin attack | HTTP rejects disallowed or ambiguous Host and Origin values before dispatch. One strict provider-neutral public HTTPS origin can derive exact direct and MCP authority lists; forwarded headers cannot substitute for them. The separate experimental WebMCP page tools remain presentation-only under ADR-0013. | Controlled, activation gated | Exercise the exact configured authority through an authorised TLS ingress and prove certificate, SNI, private-listener and proxy behaviour independently. Configuration and local socket tests are not public-endpoint evidence. |
| RK20 — Provenance spoofing | Server-built canonical decisions and receipts bind parameters, source/version, transformations, software, rights and output digest. Content-addressed ledger inspection re-verifies records, while protected-main source and image subjects have separate attestations. The inactive checkpoint manifest binds both evidence roots but is not a receipt attestation. | Controlled, activation gated | The application ledger is not signed or WORM, and its external checkpoint is not admitted to an independently administered store. Live runtime/image identity and receipt parity must be evidenced on the deployed candidate. |
| RK21 — Audit tampering | Exclusive append-only ledger writes, hash-linked events, restart verification and corruption failure prevent mutable overwrite and partial results. A provider-independent stopped-writer checkpoint binds the complete ledger/index pair in one content-addressed path-free manifest, requires private modes and no links, restores only to empty roots, completes both post-restore verifiers and rejects incomplete, cross-paired or tampered backups. A separately retained checkpoint binds both roots and the ledger tail so a structurally valid tail deletion is detectable. | Unresolved release gate | The stop is an operator assertion and file-system operators remain trusted. No admitted external checkpoint store, schedule, access-control evidence, deployment recovery exercise, RPO/RTO, retention or disposal decision exists; the mechanism is not signed, WORM or deployed. |
| RK22 — Derived-data inference | The only provider result candidate is one reviewed public aggregate scalar; no protected inputs, joins, fine-grained geometry or arbitrary dimensions are reachable. | Excluded, deny preserved | Do not expand dimensions or combine tiers. Any later derived or protected output needs thresholds, inference review and new policy evidence. |
| RK23 — Supply-chain compromise | Dependencies, Actions, base image, BuildKit, Syft and Trivy are pinned; installs are locked and script-disabled; source admission, two-build OCI identity, full SBOM, retained scan replay, CodeQL and protected-main attestations are enforced. The accepted protected-main UBI baseline removed the historical Debian package instances. | Unresolved release gate | The later public-ingress source change produces different image bytes and needs fresh exact pull-request and protected-main image checks and attestations. Explicit owner acceptance is required only for any High or Critical finding that remains. Registry and public-runtime provenance are also absent. |
| RK24 — Model/tool hallucination | Deterministic selection never uses an LLM; schemas and the exact registry prevent invented tools, providers or parameters, and every MCP result includes a complete plain-text representation. The local E13 receipt is repository-only, unscored and incomplete. | Controlled, activation gated | Repeat E13 as a scored release-candidate evaluation and complete `HOST-017` and `HOST-018` in an independent supported host; no web, plug-in or external-service substitution is permitted. |
| RK25 — Sensitive query-history exposure | Receipts retain semantic digests rather than raw queries; reconciliation stores no raw key or result; controlled errors, logs and retained host/image evidence reject prompts, credentials, provider bodies and machine paths. | Controlled, activation gated | Public ingress, proxy, platform, backup and audit retention need a separate privacy review and checked log-minimisation evidence. |
| RK26 — CRS/axis-order error | EXEC schemas require explicit EPSG:4326 longitude-latitude and test invalid order and ranges. Selection and the fixed ONS query are explicitly non-spatial. | Excluded, deny preserved | Keep CRS-bearing tools planned until transformation libraries, gold fixtures and round-trip evidence pass. |
| RK27 — Temporal geography mismatch | The fixed provider selection binds dataset, edition, version `121`, dimension order, release date and source URI; near-match and unreviewed `latest` selections fail closed. | Controlled, activation gated | Revalidate provider metadata at activation and block incompatible versions. No general temporal-geography join is supported. |
| RK28 — Provider outage | The fixed container builder creates the active pristine adapter and exact approved cache without an override seam. The fallback may answer only after exact policy approval and a current internally classified network or HTTP 500 to 599 failure; all forbidden classes remain closed. | Controlled, activation gated | Prove currentness, live eligible-outage behaviour, replay resistance and operational suspension on the final deployed candidate; no alternate provider is permitted. |
| RK29 — Licence withdrawal/change | Catalogue locks, adapter responses and the approved fallback bind reviewed rights, source date, OGL evidence and an empty `Data Marking`; drift and stale fallback use fail closed, and lifecycle planes can be suspended. | Controlled, activation gated | Establish a live review cadence and emergency suspension/republication procedure before activation; provider rights are not signed assertions. |
| RK30 — Operational drift across tiers | One source builds the closed registry, schemas, unregistered exact-five image and evidence manifest. Stable CI requires repository and gateway-image assurance; exact-image suspension and local restore are rehearsed without changing the static Explorer. | Unresolved release gate | No public runtime admission, drift monitor or previous accepted service digest exists. Real TLS, deployment configuration, rollback and open-tier controls must be proved after deployment; protected tiers remain separate. |

## Release hold and next evidence

This record closes only the missing integrated repository threat mapping. It does not
close QUAL-206 or any individual residual gate. Before activation or release, the
exact candidate must still provide:

1. protected integration of the closed container activation builder with its no-path,
   no-command-line and no-environment-based activation boundary intact; the sole
   public-origin setting may change only ingress authority;
2. scored release-candidate evaluation receipts and independent live-host results;
3. current source and freshness evidence, live eligible-outage evidence and a
   provider-suspension procedure for the now-fixed T04 injection;
4. an authorised public runtime with TLS ingress, exact Host and Origin policy,
   workload identity, domain-aware egress, shared admission and governed persistent
   storage;
5. admitted backup and external-checkpoint storage, operator fencing, schedule,
   RPO/RTO, retention, disposal, incident, real restore and rollback evidence; and
6. closure of the [image vulnerability disposition](../operations/QUAL-206_IMAGE_VULNERABILITY_DISPOSITION.md)
   through exact attested protected replacement bytes, or separately recorded owner
   acceptance for any High or Critical finding that remains.

If any control, provider, tier, route or tool changes, review all affected rows again
against the exact candidate bytes. A passing repository check or scan policy cannot
substitute for that review.
