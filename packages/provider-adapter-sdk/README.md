# Provider-adapter SDK

This private workspace package defines the transport-neutral provider-adapter
contract and a byte-deterministic synthetic adapter. The reviewed operations are
`describe`, `health`, `estimate`, `execute`, `normalise_error`,
`licence_evidence` and `provenance`.

The synthetic adapter is suspended for both discovery and invocation by default.
Tests must explicitly activate either plane, which allows independent suspension.
Its provider, dataset, edition, version, dimension and option identifiers are
fixture-native and its values are clearly synthetic. Canonical bytes use the shared
RFC 8785 implementation rather than an adapter-specific serialiser.

The package also validates fixed egress targets. It does not fetch a URL, follow a
redirect, accept credentials, choose policy, authenticate a user, start a listener
or define the gateway-to-execution envelope. Any live ONS integration must reuse
EXEC-202's accepted typed request, result and error boundary.

Fixed-egress routes bind the exact ordered decoded name/value pairs and the exact
raw query bytes. Equivalent alternate encodings, substitutions, duplicates,
wildcards and reordering are rejected. Estimates are discriminated: the synthetic
fixture reports exact observations and canonical bytes, while a future live adapter
must report conservative upper bounds for observations, attempts and compressed,
decompressed and canonical response bytes.
