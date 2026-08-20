# ADAPT-203 provider contract and inactive ONS adapter

Reviewed on 20 August 2026.

## Outcome

This slice implements the seven-operation provider-adapter contract, deterministic
synthetic statistics adapter and first fixed-selection ONS Data API adapter. The ONS
adapter is no-credential, asynchronous, separately suspendable for discovery and
invocation, and suspended on both planes by default.

It does **not** register or activate the ONS adapter in the gateway, MCP, direct API,
Python execution service, capability list or deployment. Accepted EXEC-202 commit
`6837af6eaa01ffb45e7da08d6a9131cedd1b1a0b` remains the only gateway-to-execution
envelope. The adapter accepts its validated RFC 3339 deadline and cancellation
signal as execution controls rather than inventing another transport envelope.

## Implemented contract

`@gis-ai-go/provider-adapter-sdk` exposes exactly:

- `describe`;
- `health`;
- `estimate`;
- `execute`;
- `normalise_error`;
- `licence_evidence`; and
- `provenance`.

`estimate` is a discriminated contract. The deterministic fixture returns
`confidence: exact` with the observed result count and canonical response byte
length. The live adapter returns `confidence: upper-bound` with ceilings
for observations, attempts and compressed, decompressed and canonical response
bytes; it must not claim the byte length of a response that has not been received.

Both adapters default to suspended discovery and suspended invocation. Each plane
can be activated or suspended independently in tests. Expected failures use a
closed code vocabulary and safe messages; unknown exceptions cannot reflect a raw
provider message, path, stack or token.

The fixture preserves its own provider, dataset, edition, version, dimension and
option identifiers. Arrays preserve provider-native dimension order. Results and
provenance contain no clock reading and are serialised with the shared RFC 8785
implementation, so equivalent inputs produce byte-identical UTF-8 output. The
values are invented and explicitly labelled as synthetic, not official statistics.
The live result uses the same RFC 8785 implementation and a separate
`gis-ai-go.provider-adapter-result.v1` SHA-256 domain.

## Current ONS evidence

The [ONS Developer Hub](https://developer.ons.gov.uk/) confirmed on 20 August 2026
that the beta API base remains `https://api.beta.ons.gov.uk/v1`, is open and needs
no API key. The same page warns that beta development may introduce breaking
changes.

The bounded preflight selected the aggregate dataset
`weekly-deaths-region`, edition `time-series`, version `121`. The exact
[version URI](https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121)
reported a published release dated 1 July 2026 and provider-native dimension order
`time`, `geography`, `week`, `causeofdeath`. A no-credential single-observation
probe used options `2026`, `E92000001`, `week-24` and `all-causes`; it returned HTTP
200. The implemented adapter repeated that exact request successfully at
20:21:08 UTC on 20 August 2026. Its closed evidence record retains only status,
provider and adapter versions, rights, a domain-separated result hash and size,
safe timing/TLS/byte counters and the statement that no payload was stored. No
observation value, response body, IP address or credential is retained.

The edition endpoint identified `121` as its latest API version during the review.
The wider ONS dataset page had a newer publication date, 19 August 2026. The
candidate is therefore an exact version-bound integration, not a claim that version
`121` is the newest ONS publication outside this beta API edition.

The [CMD observation guide](https://developer.ons.gov.uk/observations/cmd/) documents one
option per dimension, one possible wildcard dimension and a provider ceiling of
10,000 observations. This preflight rejects wildcards and permits one observation
only. The [rate-limit guide](https://developer.ons.gov.uk/bots/) states 120 requests
per 10 seconds and 200 per minute for all assets, plus 15 per 10 seconds for
high-demand assets. It requires clients to honour `429` and `Retry-After`. The
candidate ceiling is deliberately lower: one process-shared call in flight, 30
process-shared attempts per minute and no more than two attempts.

The selected [ONS dataset page](https://www.ons.gov.uk/datasets/weekly-deaths-region/editions/time-series/versions/121)
and current [ONS terms](https://www.ons.gov.uk/help/terms-conditions) publish the
content under the
[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/),
except where otherwise stated. The reviewed dataset page stated no additional
exception. The candidate must preserve the exact dataset version and source date,
provide ONS attribution, exclude the ONS logo, avoid endorsement claims and fail
closed if a later record states different or third-party terms.

## Fixed egress and response boundary

The machine-readable preflight allows only:

- credential-free HTTPS to the exact `api.beta.ons.gov.uk` origin;
- `GET` on the exact selected edition, version and observation paths;
- the four exact native observation query name/value pairs in provider order and
  their canonical unescaped raw query bytes;
- no caller URL, credentials, non-default port, fragment, wildcard or redirect;
- a 2-second connection timeout and 5-second response timeout;
- at most 256 KiB compressed, 1 MiB decompressed and 256 KiB after canonical
  result serialisation;
- one complete call deadline of at most 20 seconds, further reduced by an accepted
  EXEC-202 deadline;
- one process-shared call in flight and no more than 30 process-shared actual
  attempt starts in a rolling minute across all adapter instances;
  an already cancelled or expired call consumes no attempt; and
- at most two attempts for the recorded retryable statuses. `Retry-After` is used
  only when it is valid, no more than 5 seconds and leaves a complete second
  attempt inside the remaining call deadline.

Provider response links are untrusted data and are never followed. This matters
because the observed ONS observation response included `http://` link values even
though the fixed request used HTTPS.

Immediately before each attempt, the transport resolves only the fixed hostname,
rejects the whole answer set if it contains local, private, documentation,
transition, multicast or reserved address space, then pins one validated public
address for the TLS connection while retaining the original hostname for SNI and
certificate verification. It does not consult proxy environment variables, send
cookies or credentials, or reuse a provider-returned link.

The response boundary accepts only JSON with UTF-8 or no charset and identity or
gzip content encoding. It enforces compressed bytes while reading, performs bounded
cancellable streaming decompression, decodes UTF-8 fatally, rejects duplicate
decoded object keys, unsafe numbers, malformed syntax and excess depth, and checks
the exact version, dimensions, native option IDs, one observation and empty ONS
`Data Marking`. Unknown data marking fails as unknown rights. The upstream response
does not supply a unit, so the normalised result preserves `unit: null` rather than
inventing one.

## Repeat the bounded probe

The normal test suite skips live access. To run the one-call probe, with at most
two attempts, explicitly:

```bash
GIS_AI_GO_ONS_LIVE_PROBE=1 \
  pnpm --filter @gis-ai-go/provider-adapter-sdk run probe:ons-live
```

The command has a 20-second absolute adapter deadline. Its standard output is the
closed privacy-safe evidence shape described above; it never prints the observation
value or response payload. The checked-in example is
[`data-api-adapter-live-probe.v1.json`](../../providers/ons/data-api-adapter-live-probe.v1.json).

## Dependency and activation boundary

The ONS record and both lifecycle planes remain suspended. The implementation adds
the route-specific parser, DNS/TLS transport, response and decompression limits,
retry/rate admission and execution-control hooks, but it is not dispatched by
EXEC-202. A later reviewed integration must join it to that exact boundary and add
gateway-to-execution round-trip tests. No MCP tool, direct API operation, gateway
capability list, public listener or deployment is changed by this slice.
