# Provider-adapter SDK

This private workspace package defines the transport-neutral provider-adapter
contract, a byte-deterministic synthetic adapter and one bounded ONS Data API
adapter. The reviewed operations are
`describe`, `health`, `estimate`, `execute`, `normalise_error`,
`licence_evidence` and `provenance`.

The synthetic adapter is suspended for both discovery and invocation by default.
Tests must explicitly activate either plane, which allows independent suspension.
Its provider, dataset, edition, version, dimension and option identifiers are
fixture-native and its values are clearly synthetic. Canonical bytes use the shared
RFC 8785 implementation rather than an adapter-specific serialiser.

The ONS adapter is suspended on both lifecycle planes by default. Its only accepted
request is dataset `weekly-deaths-region`, edition `time-series`, version `121` and
the native ordered selection `time=2026`, `geography=E92000001`, `week=week-24`,
`causeofdeath=all-causes`. It constructs the URL internally, sends no credential,
does not follow redirects and never follows provider links. It is not registered in
the gateway or execution service.

Fixed-egress routes bind the exact ordered decoded name/value pairs and the exact
raw query bytes. Equivalent alternate encodings, substitutions, duplicates,
wildcards and reordering are rejected. Estimates are discriminated: the synthetic
fixture reports exact observations and canonical bytes, while the live adapter
reports conservative upper bounds for observations, attempts and compressed,
decompressed and canonical response bytes. The live adapter also enforces public
DNS answers, pinned TLS hostname verification, one process-shared call in flight,
30 process-shared actual attempt starts per minute, a 20-second total deadline, two
attempts, at most five seconds of usable `Retry-After`, bounded cancellable gzip,
strict UTF-8 and JSON, closed response shape and a 256 KiB canonical result ceiling.

Run the opt-in live probe only when current public-provider evidence is wanted:

```bash
GIS_AI_GO_ONS_LIVE_PROBE=1 \
  pnpm --filter @gis-ai-go/provider-adapter-sdk run probe:ons-live
```

It outputs only version, rights, status, domain-separated result hash and size, and
safe timing/TLS/byte metadata. It does not output the observation or response body.
