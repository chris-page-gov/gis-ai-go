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

[`data-api-adapter-preflight.v1.json`](data-api-adapter-preflight.v1.json) is a new,
current source and rights review for a potential no-credential ONS Data API adapter.
It binds the candidate to `weekly-deaths-region`, edition `time-series`, version
`121`; records the provider-native dimension order; and fixes the only permitted
origin, paths, method, ordered query name/value pairs, canonical raw query, redirects
and byte/time/retry limits. Its estimate is explicitly an upper bound rather than a
claim about bytes not yet produced by the unimplemented adapter. The record contains
no observation value or live response payload.

Both lifecycle planes remain suspended. Live implementation must reuse the accepted
EXEC-202 typed request, result, error, deadline, cancellation and trace boundary;
this folder does not invent a substitute envelope.
