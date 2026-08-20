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

This package does not provide a ledger, evidence lookup, persistence, signing,
attestation, identity integration, policy decision point or public transport.
