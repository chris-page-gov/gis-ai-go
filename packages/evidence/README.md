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

The optional public ledger stores only verified anonymous-open v1 or v2 receipts. It uses
exclusive content-addressed files and a hash-chained event sequence, re-verifies the
complete directory after restart, rejects replay and private fields, and returns a
durable reference only after the record and event are synchronised. Its retention
date is a minimum; the package implements no deletion.

The ledger is an application-level integrity control, not a signature, attestation,
WORM medium or malicious-operator defence. `evidence.inspect` is supplied as a
transport-neutral application in the gateway. This package provides no public
transport, identity integration, policy decision point, backup or multi-writer
coordination.

The v1 receipt, durable-record and event content-address domains are unchanged.
V2 receipts use `gis-ai-go.public-evidence-record.v2` and a separate record domain;
the descriptor, event chain, replay key and inspection request remain compatible.
The gateway returns the unchanged v1 inspection-result discriminator for v1
records and a separate v2 discriminator for v2 records; its operation contract is
an explicit closed dispatcher rather than a widening of the v1 result schema.
