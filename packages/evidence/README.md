# Evidence package boundary

This package supplies deterministic canonical JSON, domain-separated SHA-256
content identities and closed inline catalogue evidence receipts.

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

The optional public ledger stores only verified anonymous-open receipts. It uses
exclusive content-addressed files and a hash-chained event sequence, re-verifies the
complete directory after restart, rejects replay and private fields, and returns a
durable reference only after the record and event are synchronised. Its retention
date is a minimum; the package implements no deletion.

The ledger is an application-level integrity control, not a signature, attestation,
WORM medium or malicious-operator defence. `evidence.inspect` is supplied as a
transport-neutral application in the gateway. This package provides no public
transport, identity integration, policy decision point, backup or multi-writer
coordination.
