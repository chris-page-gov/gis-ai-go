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
30 process-shared actual attempt starts per minute, a 20-second total deadline
exported as `ONS_CALL_DEADLINE_MS`, two
attempts, at most five seconds of usable `Retry-After`, bounded cancellable gzip,
strict UTF-8 and JSON, closed response shape and a 256 KiB canonical result ceiling.

`ApprovedOnsDataQueryCache` is a separate, non-network fallback reader for the one
checked-in ONS v121 cache record. Construction verifies its content and rebuild
identities, accepted probe and provider-result hashes, complete one-shard coverage,
rights, query, resource, policy approval and freshness contract. A read succeeds
only for that exact query, the current allowed public policy decision and an
internally classified network failure or HTTP 500 to 599 response, and only from
the approval time until (but not including) `stale_after`. A 3xx or 4xx response,
local timeout, unsafe address, malformed response, opaque error or externally
constructed fault cannot use it. It is never constructed by default and accepts
no file path, URL, credential, environment value or mutable cache entry.

Cache-eligible network provenance originates only inside the module-owned fixed HTTPS
transport and can be carried only through an exact, pristine ONS adapter execution.
The private transport factory classifies recognised socket, DNS and TLS failures as
`network`; proxies, accessors and unknown error shapes are classified as
`unclassified`. A caller-constructed transport error can describe a failure from an
injected conformance transport, but it cannot authorise cache use. The eligibility
check consumes each module-owned outage proof once, from the exact error caught in
that same application invocation; a replayed proof cannot authorise a later cache
read. Resolver failures are never relabelled as unsafe addresses.

Run the opt-in live probe only when current public-provider evidence is wanted:

```bash
GIS_AI_GO_ONS_LIVE_PROBE=1 \
  pnpm --filter @gis-ai-go/provider-adapter-sdk run probe:ons-live
```

It outputs only version, rights, status, domain-separated result hash and size, and
safe timing/TLS/byte metadata. It does not output the observation or response body.
