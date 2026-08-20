# ADAPT-203 provider contract and ONS preflight

Reviewed on 20 August 2026.

## Outcome

This dependency-safe slice implements the seven-operation provider-adapter
contract and a deterministic synthetic statistics adapter. It also records the
current official source, version, rights and fixed-egress evidence needed for the
first ONS Data API adapter.

It does **not** implement or activate the live ONS adapter. Accepted EXEC-202 commit
`6837af6eaa01ffb45e7da08d6a9131cedd1b1a0b` owns the private typed request, result
and error schemas plus the authorised operation, complexity budget, deadline,
cancellation and trace context. This slice records that exact dependency rather than
creating a competing gateway-to-execution envelope.

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
length. A future live adapter must return `confidence: upper-bound` with ceilings
for observations, attempts and compressed, decompressed and canonical response
bytes; it must not claim the byte length of a response that has not been received.

The fixture adapter defaults to suspended discovery and suspended invocation. Each
plane can be activated or suspended independently in tests. Expected failures use a
closed code vocabulary and safe messages; unknown exceptions cannot reflect a raw
provider message, path, stack or token.

The fixture preserves its own provider, dataset, edition, version, dimension and
option identifiers. Arrays preserve provider-native dimension order. Results and
provenance contain no clock reading and are serialised with the shared RFC 8785
implementation, so equivalent inputs produce byte-identical UTF-8 output. The
values are invented and explicitly labelled as synthetic, not official statistics.

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
200. No observation value or response payload is stored in the repository.

The edition endpoint identified `121` as its latest API version during the review.
The wider ONS dataset page had a newer publication date, 19 August 2026. The
candidate is therefore an exact version-bound integration, not a claim that version
`121` is the newest ONS publication outside this beta API edition.

The [observation guide](https://developer.ons.gov.uk/observations/) documents one
option per dimension, one possible wildcard dimension and a provider ceiling of
10,000 observations. This preflight rejects wildcards and permits one observation
only. The [rate-limit guide](https://developer.ons.gov.uk/bots/) states 120 requests
per 10 seconds and 200 per minute for all assets, plus 15 per 10 seconds for
high-demand assets. It requires clients to honour `429` and `Retry-After`. The
candidate ceiling is deliberately lower: one in flight, 30 per minute and no more
than two attempts.

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
  result serialisation; and
- at most two attempts for the recorded retryable statuses, bounded by a 60-second
  `Retry-After` ceiling.

Provider response links are untrusted data and are never followed. This matters
because the observed ONS observation response included `http://` link values even
though the fixed request used HTTPS.

## Dependency and activation boundary

The ONS record and both of its lifecycle planes remain suspended. A later live
adapter slice must reuse the accepted EXEC-202 envelope and cancellation model, add
route-specific parsing, response validation, decompression limits, retry/rate
enforcement and gateway-to-execution round-trip tests. No MCP tool, direct API
operation, gateway capability list, public listener or deployment is changed by
this slice.
