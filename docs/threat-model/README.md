# Threat-model baseline

The research threat register is preserved as
[`evaluation/threat-risks.json`](../../evaluation/threat-risks.json), with its full
context in the immutable research report. Stage 0 exercises repository, dependency,
secret, malformed-contract and live-execution boundaries only. It does not claim that
future identity, policy, provider or hosting risks are controlled.

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
| Lifecycle confusion | Discovery and invocation remain independently suspended by default. The accepted public-read application takes an explicitly injected adapter and its local direct/MCP transports are separately explicit and empty by default; no shipped listener, deployment or Python dispatch configures it. | Registry, policy and local round-trip evidence now exist, but activation, independent-host, approved fallback, deployment and rollback evidence remain separate gates. The synthetic EXEC-202 allowlist is unchanged. |

## TOOLS-205 non-activating registry scope

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK02 tool poisoning and RK24 model/tool hallucination | Closed schema and runtime validation require the exact 12 IDs and names in deterministic ADR-0009 order. Planned profiles cannot enter the current callable helper. | Future descriptions and implementation-specific schemas still need adversarial review before activation. |
| RK03 confused deputy and RK08 policy bypass | Current implementation, lifecycle, discovery and seven assurance gates are separate from explicitly non-runtime `v02Target` metadata. All current gates are false and the callable set is empty. | The gateway remains the sole runtime authority; any later activation must enforce policy on discovery and invocation. |
| RK11 licence/data exfiltration and RK30 operational drift | Every profile records provider dependencies, access tiers, policy attributes, controlled errors, provenance and fallback requirements. Mutating `workflow.execute` is explicitly deferred to `v0.3.0`. | Provider, entitlement and cross-tier enforcement are metadata only until their operation slices are implemented and tested. |
| RK20 provenance spoofing and RK21 audit tampering | The profile binds the immutable research path, SHA-256, Git blob and per-tool JSON pointers; Python tests compare every mirrored research field. Runtime documents and helper results are recursively frozen. | The profile is unsigned repository data; release provenance and protected-main controls remain necessary. |
| RK23 supply-chain compromise | The private package has no dependency and its identity is locked and included in the SBOM. It has no environment override or gateway import. | Existing Node.js, package-manager and CI supply-chain controls remain release gates. |

## TOOLS-205 inactive public-read transport scope

The direct and modern MCP faces for `selection.resolve` and `data.query` are
explicit local-conformance seams. They do not activate or publish a service.

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK02 tool poisoning and RK24 model/tool hallucination | Tools are registered only from exact explicit operation arrays. Closed schemas, exact MCP method/name headers and the modern protocol metadata are checked independently. The legacy seam rejects selection, data and evidence registration. | Independent-host discovery, instruction following and repair-hint behaviour remain release evidence gates. |
| RK08 policy bypass | Direct, MCP HTTP and MCP STDIO faces call the same accepted application instances. Success and problems have byte-equivalent structured/text projections, and every success independently verifies policy and evidence. | Deployment identity, network policy and a production activation decision remain outside this candidate. |
| RK17 provider exhaustion | The Node ingress propagates direct and MCP disconnects to the adapter, uses 5-second ingress controls and 25-second socket-inactivity headroom around the adapter's lower absolute 20-second complete ceiling, and writes no evidence after cancellation. | The adapter limiter is still process-local; no deployed shared limiter or approved cache fallback exists. |
| RK20 provenance spoofing and RK21 audit tampering | Selection and data receipts are inspected through the same durable ledger, tool and receipt resource with exact JSON parity. Corruption and problem paths return no partial evidence. | The ledger is not signed, WORM or externally checkpointed. `HOST-015` remains unresolved: a receipt ID lost with the response cannot be recovered or replayed. |
| RK25 query-history exposure | Inputs and bodies are bounded; problems do not reflect hostile values, abort reasons, provider payloads, credentials or ledger paths. Tests use fixed fake transports rather than live ONS traffic. | Production logs, proxy telemetry, retention and backup controls need a separate privacy review. |
| RK30 operational drift | T03 and T04 are implemented but suspended, undiscoverable, with every activation gate false and no environment override. Registry substitutions, zero-default capabilities and unchanged readiness are tested. | T04 fallback, release, interoperability, accessibility, deployment and rollback evidence remain required before activation. |

`data.query` deliberately advertises `idempotentHint: false`. Repeating a request
can make another provider attempt and persist another ledger event. There is no
idempotency key, result store or receipt lookup by request, and `evidence.inspect`
requires the receipt ID that a lost response would have contained. No exactly-once
or at-most-once reconciliation claim is made.
