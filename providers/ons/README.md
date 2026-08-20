# Office for National Statistics public discovery metadata

The public OKF bundle describes two non-executing capability families: ONS data APIs
and ONS geography products. The records are dated metadata from checksum-locked
research inputs; they do not call an API or contain observations, postcode or UPRN
rows, boundaries or other dataset payloads.

The Open Government Licence applies only where the named product says it does.
Ordnance Survey, Royal Mail and other third-party conditions remain
product-specific. Release or product vintage must not be inferred from the GIS AI
GO review or publication date. See the
[source review](../../docs/source-ledger/reviewed-public-examples-2026-08-20.md).

[`data-api-adapter-preflight.v1.json`](data-api-adapter-preflight.v1.json) is the
current source, rights, bounds and inactive-lifecycle review for the no-credential
ONS Data API adapter.
It binds the candidate to `weekly-deaths-region`, edition `time-series`, version
`121`; records the provider-native dimension order; and fixes the only permitted
origin, paths, method, ordered query name/value pairs, canonical raw query, redirects
and byte/time/retry limits. Its estimate remains an upper bound rather than a claim
about future response bytes. The record contains no observation value or response
payload.

[`data-api-adapter-live-probe.v1.json`](data-api-adapter-live-probe.v1.json) records
one successful opt-in request through the implemented hardened path. It contains
only status, versions, rights, result hash and size, and safe timing/TLS/byte
metadata. It contains no response payload, observation, IP address or credential.

Both lifecycle planes remain suspended. Runtime integration must reuse the accepted
EXEC-202 typed request, result, error, deadline, cancellation and trace boundary;
this folder and adapter do not invent or activate a substitute gateway envelope.
