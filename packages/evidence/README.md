# Evidence package boundary

This package supplies deterministic canonical JSON, domain-separated SHA-256
content identities and closed inline catalogue evidence receipts.

It also supplies a parallel inactive public-read v2 receipt contract for
`selection.resolve` and the exact bounded public ONS `data.query`. The v2 receipt
binds the reviewed profile, provider, adapter, dataset version, fixed selections,
rights evidence, operation-specific parameters and successful result core. A
denial, ambiguous selection or failed query cannot be passed to the success-receipt
builder.

The selection contract also exports the exact reviewed selection profile and its
content-addressed non-executable plan. Successful selection result cores must bind
that plan and the deterministic ranking which selected it. These additive plan and
profile domains do not change the accepted receipt, record, event or replay domains.

Canonical JSON follows the JSON Canonicalization Scheme rules used by RFC 8785 for
the supported JSON data model: object keys are ordered by UTF-16 code units,
strings and numbers use ECMAScript JSON serialisation, and the resulting text is
encoded as UTF-8. Inputs outside the interoperable JSON model fail closed. This
includes cycles, sparse arrays, accessors, non-plain objects, `undefined`, `bigint`,
non-finite numbers and unpaired Unicode surrogates.

Inline receipts bind the normalised request parameters, result core, exact
catalogue publication, authority context, policy decision, software revision and
trace identifiers. Raw query text is not retained in a receipt. Every receipt
states that delivery is inline-only, persistence is absent and attestation is
absent.

The optional public ledger stores only verified anonymous-open v1 or v2 receipts. It
uses exclusive content-addressed files and a hash-chained event sequence, re-verifies
the complete directory after restart, rejects replay and private fields, and returns
a durable reference only after the record and event are synchronised. Directories
must have mode `0700` and files mode `0600` on POSIX systems. Its retention date is a
minimum; the package implements no deletion.
The accepted one-million-event ceiling is enforced before either record or event
publication for a new receipt. Replay detection and inspection still work at the
ceiling. This is a single-writer file-store safety bound, not a deployment quota.

The optional receipt-only reconciliation index binds a caller-generated
`gis-ai-go:ik:v1` identity to the semantic fingerprint of one `data.query`, then to
the resulting receipt. It retains only operation-scoped digests and evidence
identities: the raw key, parameters, observation and result are never stored. A
content-free exclusive ownership marker prevents a second execution for the same
key; complete canonical claim and resolution documents are published before their
ready markers. An interrupted publication remains pending and cannot authorise
another provider execution. The resolution is published before the exact linked ledger accepts
the receipt, and completion is returned only after both stores verify the same
receipt, record, event and storage identities.
Only a genuinely new key is subject to a fixed 4,096-claim local admission ceiling,
checked before ownership publication. Existing pending, completed and conflicting
keys remain available at the ceiling. Verification is linear but reuses its loaded
state and linked-ledger snapshot within each steady operation, so work is bounded by
the local ceiling. This is not cluster admission or an activation-safe quota.
Ownership is immutable: the package supplies no pending-claim expiry, reclamation,
operator override or deletion process. A new attempt requires a new key.

The ledger and index are application-level integrity controls, not signatures,
attestations, WORM media or malicious-operator defences. `evidence.inspect` is
supplied as a transport-neutral application in the gateway. This package provides
no public transport, identity integration, policy decision point, backup or general
multi-writer ledger coordination. Same-key exclusion is scoped to processes sharing
one governed index; one writer must still own the linked ledger.

The v1 receipt, inspection request, durable-record and event content-address domains
are unchanged.
V2 receipts use `gis-ai-go.public-evidence-record.v2` and a separate record domain;
the descriptor, event chain and replay key remain compatible.
The historical v1 and v2 inspection-result schemas remain unchanged. The gateway's
current operation contract returns `gis-ai-go.evidence-inspect-result.v3` for either
lookup with a dedicated current-call receipt. That receipt binds a safe normalised
lookup digest, exact stored evidence identities and the receipt-free result core.
It is inline-only, not persisted or attested and creates no ledger event. V1 and v2
request, receipt, durable-record and event bytes remain unchanged.
