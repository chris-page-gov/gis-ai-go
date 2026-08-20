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

## ADAPT-203 provider preflight scope

| Risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| Caller-controlled egress or redirect SSRF | Exact HTTPS origin, method, path and query allowlist; credentials, ports, fragments, wildcards, duplicate parameters and redirects fail closed. | A live adapter must reuse accepted EXEC-202 typed identifiers and add DNS, connection and cancellation controls. |
| Provider overload and response amplification | Recorded provider limits, a lower local ceiling, bounded attempts, deadlines and compressed/decompressed byte ceilings. | No live HTTP client or shared durable rate service exists yet. |
| Version, dimension or rights drift | Exact dataset, edition, version, native dimension order, source date, official URIs and OGL evidence are schema-locked. Unknown or changed rights must fail closed. | Source and rights need revalidation before activation and after provider change. |
| Error and payload leakage | Closed safe error vocabulary; fixture tests reject hostile structures and prove raw exception details are not reflected. No live payload is committed. Accepted EXEC-202 supplies the generic safe-error and log boundary. | Provider-specific live response parsing and redaction must be implemented and tested in the later live-adapter slice. |
| Partial provider suspension | Discovery and invocation lifecycle planes are independent and suspended by default. | Gateway registry and execution dispatch must enforce the same state after integration. |

## TOOLS-205 non-activating registry scope

| Research risk | Control in this slice | Residual boundary |
| --- | --- | --- |
| RK02 tool poisoning and RK24 model/tool hallucination | Closed schema and runtime validation require the exact 12 IDs and names in deterministic ADR-0009 order. Planned profiles cannot enter the current callable helper. | Future descriptions and implementation-specific schemas still need adversarial review before activation. |
| RK03 confused deputy and RK08 policy bypass | Current implementation, lifecycle, discovery and seven assurance gates are separate from explicitly non-runtime `v02Target` metadata. All current gates are false and the callable set is empty. | The gateway remains the sole runtime authority; any later activation must enforce policy on discovery and invocation. |
| RK11 licence/data exfiltration and RK30 operational drift | Every profile records provider dependencies, access tiers, policy attributes, controlled errors, provenance and fallback requirements. Mutating `workflow.execute` is explicitly deferred to `v0.3.0`. | Provider, entitlement and cross-tier enforcement are metadata only until their operation slices are implemented and tested. |
| RK20 provenance spoofing and RK21 audit tampering | The profile binds the immutable research path, SHA-256, Git blob and per-tool JSON pointers; Python tests compare every mirrored research field. Runtime documents and helper results are recursively frozen. | The profile is unsigned repository data; release provenance and protected-main controls remain necessary. |
| RK23 supply-chain compromise | The private package has no dependency and its identity is locked and included in the SBOM. It has no environment override or gateway import. | Existing Node.js, package-manager and CI supply-chain controls remain release gates. |
