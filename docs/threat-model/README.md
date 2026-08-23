# Threat-model baseline

The research threat register is preserved as
[`evaluation/threat-risks.json`](../../evaluation/threat-risks.json), with its full
context in the immutable research report. Stage 0 exercises repository, dependency,
secret, malformed-contract and live-execution boundaries only. It does not claim that
future identity, policy, provider or hosting risks are controlled.

The qualified
[23 August 2026 external incident crosswalk](../research/2026-08-23/agentic-ai-governance-review/THREAT_EVIDENCE_CROSSWALK.md)
maps respondent-reported industry categories to the existing register and current
negative-assurance evidence. It does not re-rate risks or turn survey findings into
control evidence.

## QUAL-206 integrated Stage 2 release record

The
[QUAL-206 Stage 2 release threat record](QUAL-206_STAGE_2_RELEASE.md) maps all 30
baseline risks to the controls implemented for the inactive `v0.2.0` candidate and
the exact residual activation or release gate. Its outcome is hold for activation
and release. It does not re-rate the research risks, accept the retained image
vulnerabilities or claim that repository assurance proves a public deployment.

## EVID-204A public inline-evidence scope

ADR-0010 adds a bounded anonymous-public evidence path for the inactive catalogue
application. It does not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK08 policy bypass | One application success path constructs server authority, evaluates default-deny policy and requires an inline receipt. | Transport registration and every future operation need separate enforcement tests. |
| RK20 provenance spoofing | Domain-separated identities bind policy, authority, catalogue, parameters, result core, software and record-specific rights. | No signature or computation attestation is claimed. |
| RK21 audit tampering | Inline receipt mutation and truncation fail verification. | No ledger exists; deletion, overwrite, restart and recovery controls remain open. |
| RK25 query-history exposure | Receipts retain a semantic-parameter digest rather than raw query or cursor text. | Future operational logs and persistent evidence need separate privacy and retention review. |

The public policy is a compiled checked-in JSON document. It is not OPA, protected
identity, authentication or an enterprise entitlement decision.

## EVID-204B durable public-evidence candidate

ADR-0011 adds an inactive portable store and transport-neutral inspection
application. It does not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK08 policy bypass | Persistence accepts only a receipt that passes full independent material verification. Inspection returns only records whose embedded decision is anonymous-open and allowed. | `evidence.inspect` has no public route or tool. Any later activation needs its own policy and interoperability evidence. |
| RK20 provenance spoofing | Content-addressed records and events bind the exact receipt, ledger, retention and sequence. | No signature, attestation or independent computation replay is claimed. |
| RK21 audit tampering | Exclusive writes prevent API overwrite. Restart checks canonical bytes, identities, event order, hash links, missing or orphan records, replay and truncation. | Direct file-system writers remain trusted. Complete unanchored tail deletion needs an external checkpoint; this is not WORM storage. |
| RK25 query-history exposure | The ledger retains only the receipt's semantic digests and explicitly rejects raw-query, cursor, prompt, geometry, credential and machine-path fields. | Operational logs, backups and future protected evidence need separate privacy review. |

One writer owns a ledger root. Contention fails closed rather than merging events.
Corrupt stores are quarantined and restored from a separately verified complete
copy; there is no silent or in-place repair.
The immutable descriptor also fixes a bounded minimum retention period and each
record exposes `retain_until`. No deletion is implemented; production disposal
policy and evidence remain open.

## EVID-204C evidence inspection transport candidate

The direct and MCP faces are explicit local-conformance seams over the accepted
transport-neutral inspector. They do not change production activation or publish a
service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK08 policy bypass | Every face calls one inspector, which re-verifies the ledger and permits only embedded anonymous-open public decisions. Tool, resource and direct registration are separately explicit and empty by default. | Host interoperability, deployment identity, network policy and a reviewed production activation decision remain release gates. |
| RK20 provenance spoofing | Direct, MCP structured, MCP text, MCP resource and STDIO results are byte-equivalent projections of one verified record and event. Shared closed schemas are advertised on both operation faces. | The event chain is not a signature, attestation, WORM store or external checkpoint. |
| RK21 audit tampering | A verification or corruption failure becomes one controlled unavailable problem and returns no partial record. Tests truncate an event after restart and prove fail-closed behaviour. | File-system operators remain trusted; complete unanchored tail deletion and disaster recovery need external controls. |
| RK25 query-history exposure | Lookups accept one content identity. Problems do not reflect receipt text or ledger paths, and stored records retain digests rather than query, prompt, geometry, credentials or original result material. | Operational hosting logs, backups and future protected evidence require a separate privacy and retention review. |

The bounded resource and duplicated tool representations share a narrower result
ceiling than the direct HTTP response. Oversize evidence therefore fails closed in
the application rather than creating transport-specific truncation.

## EVID-204D receipt-only reconciliation scope

ADR-0012 adds a ledger-linked index and key lookup for the inactive `data.query`
application. It does not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK03 confused deputy and RK08 policy bypass | Module-private identities require every mounted data-query face to mount `evidence.inspect` over the exact same ledger/index. Legacy, mismatched and proxy-wrapped applications fail construction. | Production identity, entitlement and activation remain separate. The trusted application context and explicit request-context factories must remain server-owned. |
| RK17 provider and storage exhaustion | A durable exclusive ownership marker prevents the same key from causing a second provider execution. Pending/completed retries return before provider preflight. A new key is refused before publication once the verified index has 4,096 owned claims, bounding local storage growth and linear verification work. The linked ledger likewise refuses a new receipt before either write at its accepted event ceiling while replay and inspection remain available. | Claims are immutable. Cancellation, pre-egress rejection or uncertain post-ownership failure can leave a key permanently pending. The fixed local bounds are not cluster admission, a rate quota, reclamation, operator resolution or disposal, and do not permit activation. |
| RK20 provenance spoofing and RK21 audit tampering | Domain-separated key and semantic fingerprints, complete-JSON-before-ready publication, resolution-before-ledger ordering and completed re-read bind one key to one verified receipt, record and event. | One writer still owns the ledger. The index coordinates only the same key for processes sharing one filesystem and is not cluster-wide exactly-once execution. |
| RK25 query-history and identity exposure | The ledger/index reject the complete raw key and result material. Direct data queries ignore `x-request-id` and generate opaque server identities; MCP does the same by default. Shared HTTP and STDIO ingress rejects a raw, prefixed, percent-encoded or multiply encoded complete key in JSON-RPC request IDs, methods, tool names and protocol-version claims before SDK dispatch; HTTP also checks its parity headers. Requests receive a fixed `id: null` error and notifications remain silent. Problems, inspection results and resource URIs contain no key. | The caller-generated key is a public correlation label and must contain no personal or secret material. Host, proxy and operational telemetry must keep the digest-only contract; backups need a separate privacy review. |

## EVID-204E trace and readiness completion scope

The final repository-only slice adds internal trace correlation and repeated storage
integrity checks. It does not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK03 confused deputy and RK08 policy bypass | Direct and MCP request contexts construct server-owned values against the W3C Trace Context Level 2 Candidate Recommendation Draft within a 512-character `tracestate` ceiling. `data.query` passes only that closed typed value to the exact adapter, which validates it again. Caller `traceparent`, `tracestate`, baggage, authorisation and arbitrary header maps are ignored; the fixed ONS request still has only its four reviewed headers. | Level 2 remains work in progress. No provider trace header or telemetry exporter is activated. Any future cross-service propagation needs a separate standards-refresh, trust, sampling, privacy and egress review. |
| RK17 provider and storage exhaustion | The blocked container re-verifies the complete linked ledger and reconciliation index on every `/readyz` evaluation while readiness stays `503`. | Both checks are linear in retained events and claims. Before any public readiness ingress or activation, governed request admission, rate limiting, capacity evidence and monitoring are required. |
| RK21 audit tampering | A privately branded seam accepts one exact linked pair, uses captured verification methods, rejects nested receipt-inspection substitution and rechecks the link around reconciliation verification. Post-start corruption cannot make readiness pass and emits the fixed `gateway_readiness_integrity_failed` lifecycle event. | The event needs integration with an authorised operator response. Existing single-writer, non-WORM, checkpoint, backup and disaster-recovery residuals remain. |
| RK25 query-history and identity exposure | Full Trace Context and caller baggage are absent from results, receipts and ONS egress. Readiness failures return the unchanged path-free blocked document and the container sink maps errors to fixed event names without paths, credentials or raw identifiers. | Future tracing backends, proxies, logs and retention need a separate privacy review before trace state or span material is exported. |

## EXEC-202 private execution scope

[`EXEC-202.md`](EXEC-202.md) records the private synthetic execution trust boundary,
controls and residual risks. It does not approve a public listener, live provider or
production deployment.

## ADAPT-203A accepted provider-preflight boundary

| Risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| Caller-controlled egress or redirect SSRF | Exact HTTPS origin, method, path and query allowlist; credentials, ports, fragments, wildcards, duplicate parameters and redirects fail closed. | The inactive adapter below adds DNS, connection and cancellation controls. The accepted public-read application injects it directly and independently validates the exact data-query contract; the separate synthetic EXEC-202 operation allowlist remains unchanged. |
| Provider overload and response amplification | Recorded provider limits, a lower local ceiling, bounded attempts, deadlines and compressed/decompressed byte ceilings. | The adapter below implements process-local admission only; no shared durable rate service exists. |
| Version, dimension or rights drift | Exact dataset, edition, version, native dimension order, source date, official URIs and OGL evidence are schema-locked. Unknown or changed rights must fail closed. | Source and rights need revalidation before activation and after provider change. |
| Error and payload leakage | Closed safe error vocabulary; fixture tests reject hostile structures and prove raw exception details are not reflected. No raw live response body is committed; one public aggregate scalar is retained only in a deterministic test fixture to reproduce the live result digest. Accepted EXEC-202 supplies the generic safe-error and log boundary. | The adapter below adds closed provider-specific live-response parsing; deployed provider-specific log redaction remains a later integration gate. |
| Partial provider suspension | Discovery and invocation lifecycle planes are independent and suspended by default. | The accepted public-read application requires an explicitly injected invocation-active adapter, while the gateway registry and every production transport remain suspended and unactivated. |

## ADAPT-203 inactive live-adapter scope

| Risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK10 SSRF and DNS rebinding | The adapter constructs one exact HTTPS path and ordered raw query. Every attempt resolves the fixed hostname, rejects any special/non-public answer, pins one validated address and retains the hostname for TLS SNI and certificate verification. Redirects, proxies, credentials, cookies, caller URLs and provider links are unused. | There is no deployed egress policy or service integration; any later runtime must enforce the same origin independently at the network plane. |
| RK16 decompression bomb and malformed payload | Compressed input is capped while reading; cancellable gzip expansion is capped separately; media type, encoding and fatal UTF-8 checks precede a bounded duplicate-key-rejecting JSON parser and exact response validation. Canonical output has its own lower cap. | Only identity and gzip are supported. A future encoding or larger response requires a new reviewed bound. |
| RK17 provider exhaustion | One process-shared call is admitted at a time across all adapter instances, with 30 process-shared actual attempt starts per rolling minute, two attempts, 2-second DNS/connect and 5-second response limits, at most 5 seconds of usable `Retry-After`, and a 20-second absolute call deadline reduced by the EXEC deadline. Cancellation reaches DNS, socket, body, decompressor and backoff. | Rate state is process-local and intentionally not represented as a durable distributed limiter. The adapter is therefore not activated. |
| RK20 provenance or rights spoofing | Closed validation binds dataset, edition, version, native dimension order/options, exact constructed source URI, release date, empty ONS `Data Marking`, OGL evidence and deterministic transformations. The canonical result uses its own domain-separated digest. | Rights are a dated public review, not a provider-signed assertion. Any changed or non-empty marking fails closed pending review. |
| RK25 payload or operational leakage | The opt-in evidence record and probe output retain only versions, rights, status, result hash/size and safe timings/TLS/byte counts. They exclude response bodies, observation values, IP addresses, credentials and paths. A deterministic test separately retains the public aggregate scalar needed to reproduce the digest. Controlled errors do not reflect provider content. | A deployed logging and retention policy remains a separate gate. |
| Lifecycle confusion | Discovery and invocation remain independently suspended by default. The accepted public-read application takes an explicitly injected adapter and optional exact approved cache. One repository-only governed candidate now binds these dependencies at compile time, but no shipped listener, deployment or Python dispatch constructs it. | Production registration, independent-host, live cache-eligible network/HTTP 500 to 599 failure evidence, forbidden-class denial evidence, deployment and rollback remain separate gates. The synthetic EXEC-202 allowlist is unchanged. |

## TOOLS-205 non-activating registry scope

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK02 tool poisoning and RK24 model/tool hallucination | Closed schema and runtime validation require the exact 12 IDs and names in deterministic ADR-0009 order. Planned profiles cannot enter the current callable helper. | Future descriptions and implementation-specific schemas still need adversarial review before activation. |
| RK03 confused deputy and RK08 policy bypass | Current implementation, lifecycle, discovery and seven assurance gates remain separate from the exact `candidate-unregistered` projection. All current gates and the production callable set remain empty; the gateway candidate consumes only the exact five read-only profiles with production registration false. | The gateway remains the sole runtime authority; protected integration and any later production activation must independently enforce policy on discovery and invocation. |
| RK11 licence/data exfiltration and RK30 operational drift | Every profile records provider dependencies, access tiers, policy attributes, controlled errors, provenance and fallback requirements. Mutating `workflow.execute` is explicitly deferred to `v0.3.0`. | Provider, entitlement and cross-tier enforcement are metadata only until their operation slices are implemented and tested. |
| RK20 provenance spoofing and RK21 audit tampering | The profile binds the immutable research path, SHA-256, Git blob and per-tool JSON pointers; Python tests compare every mirrored research field. Runtime documents and helper results are recursively frozen. | The profile is unsigned repository data; release provenance and protected-main controls remain necessary. |
| RK23 supply-chain compromise | The private package has no third-party runtime dependency, reads no environment state and is identity-locked in the SBOM. The gateway now imports its exact candidate projection through a frozen workspace dependency; the lockfile and closed container context include the package and exact profile. | Existing Node.js, package-manager, clean-image and CI supply-chain controls remain release gates. |

## TOOLS-205 governed candidate assembly scope

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK03 confused deputy and RK08 policy bypass | One branded compile-time assembly derives direct API, MCP HTTP, MCP STDIO and combined Node discovery from the same exact registry, frozen policies, verified catalogue, provider lifecycle and linked evidence pair. Descriptor-safe constructors reject application, operation and activation replacement; provider and explicit suspension can only remove operations and equivalent resources. | The constructor is repository-only and unregistered. Shipped entrypoints and production arrays remain empty; activation, deployment and rollback need separate authority. |
| RK20 provenance spoofing and RK21 audit tampering | Only loader-branded checksum-verified catalogue snapshots, pristine exact adapters and exact linked evidence stores are admitted. Runtime-dispatched store methods and prototypes are locked; every advertised operation re-verifies membership, provider integrity and evidence integrity before dispatch. | The ledger remains unsigned, non-WORM and locally retained. Provider and evidence alerts, external checkpoints and operator response remain release gates. |
| RK24 model/tool hallucination and lifecycle confusion | Planned and mutating profiles cannot enter the exact-five candidate. OpenAPI, MCP tools and MCP resources apply the same subtractive lifecycle; the full catalogue resource requires both search and describe. Whole-candidate readiness remains `503` for any reduced set and always reports production registration false. Every successful `evidence.inspect` projection now includes a verifiable, inline-only current-call receipt without a ledger write. | Independent-host interoperability and protected integration remain open before issue closure or activation. |

## TOOLS-205 inactive public-read transport scope

The direct and modern MCP faces for `selection.resolve` and `data.query` are
explicit local-conformance seams. They do not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK02 tool poisoning and RK24 model/tool hallucination | Tools are registered only from exact explicit operation arrays. Closed schemas, exact MCP method/name headers and the modern protocol metadata are checked independently. The legacy seam rejects selection, data and evidence registration. | Independent-host discovery, instruction following and repair-hint behaviour remain release evidence gates. |
| RK08 policy bypass | Direct, MCP HTTP and MCP STDIO faces call the same accepted application instances. Success and problems have byte-equivalent structured/text projections, and every success independently verifies policy and evidence. | Deployment identity, network policy and a production activation decision remain outside this candidate. |
| RK17 provider exhaustion | The Node ingress propagates direct and MCP disconnects to the adapter and uses 5-second ingress controls with 25-second socket-inactivity headroom around the adapter's lower absolute 20-second complete ceiling. Cancellation produces no receipt, ledger record or event. The local index refuses new ownership before publication at 4,096 claims. | Once key ownership exists, cancellation can leave an immutable pending claim. The adapter limiter and index bound are still local; the exact approved cache is injection-only and does not provide a deployed shared limiter or governed cluster admission. |
| RK20 provenance spoofing and RK21 audit tampering | Selection and data receipts are inspected through the same durable ledger, tool and receipt resource with exact JSON parity. Reconciled data faces structurally require the exact linked inspector; corruption and problem paths return no partial evidence. | The ledger is not signed, WORM or externally checkpointed. Lost-response recovery returns only the receipt; no result replay is implemented. |
| RK25 query-history exposure | Inputs and bodies are bounded; problems do not reflect hostile values, abort reasons, provider payloads, credentials or ledger paths. Tests use deterministic fake provider responses and mocked resolver failures rather than live ONS traffic. | Production logs, proxy telemetry, retention and backup controls need a separate privacy review. |
| RK30 operational drift | T03 and T04, including the exact current T04 cache fallback, are implemented but suspended and undiscoverable in production, with every current activation gate false and no environment override. Registry substitutions, zero-default capabilities and the separately unregistered compile-time assembly are tested. | Live cache-eligible network/HTTP 500 to 599 failure and forbidden-class denial evidence, release-candidate interoperability, accessibility, deployment and rollback evidence remain required before activation. |

`data.query` advertises `idempotentHint: true` only for the complete arguments,
including the mandatory caller key. A repeat returns a receipt-free pending,
completed or conflict `409`; it does not replay success. `evidence.inspect` v2 can
recover the verified receipt by key after restart. The narrow claim is same-key
at-most-once provider execution through one governed shared index and a single-writer
ledger, not general or cluster-wide exactly-once processing.

## DEPLOY-207 blocked gateway container scope

The repository-only image and local Compose harness do not activate or deploy the
service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK08 policy bypass and lifecycle confusion | The fixed entrypoint asserts empty production arrays, supplies no operation/resource/application/provider override, and keeps readiness at `503`. Container and HTTP acceptance independently prove zero direct and MCP capability. The repository candidate assembly is not referenced by that entrypoint. | Production registration still requires all lifecycle gates and separate reviewed authority. Environment or command-line activation remains forbidden. |
| RK10 SSRF and RK17 exhaustion | The default Compose network is internal, has one replica and no operator-supplied environment or provider. It declares only `127.0.0.1:8787`; acceptance records the realised mapping separately and permits either that exact host loopback or no host port on the verified internal bridge. The full route matrix still runs on container loopback in the fallback. Process, CPU, memory, swap, descriptor and existing request bounds are inspected on the running container. | A no-port receipt is not host-ingress evidence. An active ONS candidate requires domain-aware egress, shared admission and an operator response to permanently pending reconciliation claims. |
| RK21 evidence loss or tampering | Separate private ledger and reconciliation volumes are opened and fully verified before listening. Descriptor modes and hashes survive restart and exact-image restore. Closed canonical schemas cover the image receipt, scan, acceptance and final manifest; exactly 11 evidence subjects plus the manifest are allowed, and protected-main provenance can attest that manifest after complete re-verification. | The store remains single writer, non-WORM and without backup, external checkpoint, disposal or disaster-recovery evidence. No attestation exists for an unmerged local candidate. |
| RK23 supply-chain compromise | The build materialises only Git-tracked allowlisted source plus the checksum-verified closed OKF projection; `.env` files are rejected and ignored. Pinned dependency fetching precedes broad source copies, after which install, compilation and runtime mutation use no BuildKit network. Node, pnpm, BuildKit, Syft and Trivy identities are immutable; the canonical verifier binds source, context, OCI blobs and the closed runtime. Two builds compare canonical OCI bytes. The full Syft SBOM is unfiltered. All High and Critical Trivy findings remain in evidence, the gate blocks the fixable subset, and a deterministic retained database bundle proves offline replay. | Registry publication and public-runtime provenance are absent. Vulnerability knowledge changes over time and must be rescanned; an unfixed finding is retained risk, not proof of safety. |
| RK25 telemetry leakage | No request logger is added. Acceptance sends a raw-key sentinel and rejects its appearance, machine paths and bearer material in bounded logs and artefacts. | TLS proxy, platform, backup and host telemetry require a separate privacy and retention review. |
| RK30 operational drift | The stable final `assurance` job requires both repository and image producers. The image aggregator recreates one closed evidence directory and records changing engine/tool versions and phase timings outside the reproducible OCI. Compose consumes a preloaded exact image with no build or pull, proves suspension and restores the saved image identity without rebuilding. The static Explorer is not a service dependency. | This is a local mechanism rehearsal. Production rollback needs an authorised runtime and a previous accepted digest. |
