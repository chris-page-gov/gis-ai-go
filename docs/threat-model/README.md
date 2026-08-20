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

## EXEC-202 private execution scope

[`EXEC-202.md`](EXEC-202.md) records the private synthetic execution trust boundary,
controls and residual risks. It does not approve a public listener, live provider or
production deployment.
