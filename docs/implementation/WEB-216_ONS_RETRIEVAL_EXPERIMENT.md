# WEB-216 X03: metadata to a maintained CPIH observation

Protocol date: 14 September 2026. This is a bounded research probe, not a new
gateway adapter, MCP operation, activation or provider-admission receipt.
It follows the [foundation experiment](WEB-216_EXPERIMENTS.md), whose frozen
metadata is not proof of current provider behaviour.

## An important source correction

The [ONS version 67 page](https://www.ons.gov.uk/datasets/cpih01/editions/time-series/versions/67)
has a notice dated 7 July 2026: the page is no longer updated and holds data only
through January 2026. Its version being labelled “latest” does not make its data
current. Preserve the frozen source record unchanged and attach a separately
dated [lifecycle notice](../../tests/fixtures/web216/lifecycle-notices.json).

The prototype must distinguish latest **within a retired dataset** from the
latest published measure. A request for current CPIH must not silently return this
source. The discovery correction below identifies and tests a maintained API
route separately; neither a publication page nor an HTTP success proves an MCP
integration.

## Maintained route and actual bounded observation

The first-party [ONS API migration guide](https://developer.ons.gov.uk/retirement/v0api/)
describes search followed by retrieval through `/v1/data`. The maintained
[L522/MM23 series page](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l522/mm23)
identifies the overall CPIH index with base year 2015. The bounded probe therefore:

1. requested `/v1/search?content_type=timeseries&cdids=L522` from the fixed ONS
   HTTPS origin;
2. required one exact time-series match, with `cdid=L522`, `dataset_id=MM23` and
   the source-native URI corresponding to that official page;
3. requested `/v1/data` using that returned URI, never an arbitrary supplied URL;
4. retained both responses before separately validating their content.

The actual run on 14 September 2026 took place from 15:42:57.497076 to
15:42:57.906633 UTC. Both GET requests returned HTTP 200: 3,070 bytes for search
and 125,682 bytes for data. These are captured response sizes, not tool-output
sizes. The probe allowed at most two requests, one MiB per response, ten seconds
per request and thirty seconds overall, with no redirects, retries, credentials
or cookies. There was no model or MCP call. Its source-time outcome was
`raw-responses-collected-pending-schema-validation`; that original record is not
rewritten to claim a later validation had already happened.

The pure [validator](../../scripts/web216_current_cpih.py) performs no network
request. It binds the complete captured bytes to the source-time manifest, checks
identity, unit, release alignment and monthly chronology, and selects the exact
requested month or the latest month in that captured response. It refuses duplicate
periods, unknown suppression fields, invalid decimal strings, future observations,
missing requested months and a search/data release mismatch. Dates retain their
original source strings. The 23:00 UTC release timestamp maps to the following
calendar date in London; neither is silently discarded.

The fixture is an explicitly labelled
[two-month redacted projection](../../tests/fixtures/web216/current-cpih-projection.json),
not the complete 463-month response. Its projection hash differs from the original
response hashes, and it excludes contact metadata. Clone-local tests use this
small projection; full-response validation uses the preserved original capture.
An index value is not an inflation percentage. The base year comes from the exact
series title, not from a generic unit string that omits the year.

```bash
python3 -m unittest tests.test_web216_current_cpih -v
python3 scripts/web216_current_cpih.py \
  --capture-directory <preserved-public-response-directory> \
  --period latest --output <fresh-result-file>
```

“Latest” here means latest at the recorded retrieval, not always current. A future
retrieval must revalidate the source; the next-release date is provider metadata,
not a guarantee. Hash binding detects inconsistency with this capture, not
independent authentication, timestamp attestation or provider-admission authority.

## Earlier historical protocol, not executed against the provider

The earlier candidate would demonstrate only the UK CPIH overall index for
January 2026, with base 2015=100.
Discover edition-local version metadata, then require the independently identified
historical version 67. Resolve and validate the time, geography and aggregate
options before fetching one cell. Fail rather than silently follow version drift
or substitute another inflation measure. A historical probe draft passed eighteen
mocked tests but was rejected before integration: its assumed observation shape
did not match the [first-party example](https://developer.ons.gov.uk/observations/).
The draft and its tests are preserved as rejected research evidence, not shipped
as a usable provider implementation. It was never run against ONS. The maintained
route supplied both the historical and latest months, so another eight or nine
requests would not help the current story. Mocked success is not a provider
observation or evidence that an assumed response contract is correct.

The [CMD observation guide](https://developer.ons.gov.uk/observations/cmd/)
uses a time label, unlike the other dimension option identifiers. The
[options endpoint](https://developer.ons.gov.uk/dataset/datasets-id-editions-edition-versions-version-dimensions-dimension-options/)
supplies the labels and code/version links needed to check that proposal. The
candidate inputs `Jan-26`, `K02000001` and `cpih1dim1A0` are not accepted until
matched against the returned option metadata.

Accept exactly one decimal-string observation and its declared index unit,
retaining the original lexical value rather than coercing it to an integer or
binary float. Unknown missing-value or suppression semantics are failures, not
zeroes. Response links and dimensions must reconcile with the selected version
and options. An independent published value may cross-check the result but must
never be substituted when the API response is absent or invalid.

## Historical probe request and evidence bounds

- Fixed ONS HTTPS origin and constructed `cpih01` metadata/option/observation paths.
- At most ten serial GET requests, one MiB per response, ten-second request
  timeout and a bounded overall run; no wildcard, POST, download, credentials,
  cookies, arbitrary URL, redirect or automatic retry.
- On HTTP 429 or another failure, record the failure and stop this attempt.
  The [ONS bot guidance](https://developer.ons.gov.uk/bots/) and
  [fair-use policy](https://www.ons.gov.uk/help/fair-use-policy) apply.
- Use an identifying project User-Agent without personal details. This probe
  uses the operating system HTTPS stack; it does **not** claim the reviewed
  gateway's pinned-address/socket transport, admission or persistence guarantees.
- Save each step's permitted public response, request identity, status, digest,
  byte count and timing, together with code/configuration identity and final
  outcome. Failed and partial attempts remain evidence. Use fresh output paths.
- Make no model call. Keep observed provider requests separate from mocked tests,
  and an empirical API success separate from an actual MCP-client success.

## Consequence for implementation

The existing fixed weekly-deaths adapter stays unchanged. Its integer parsing,
four selected dimensions and provider evidence are not the CPIH contract. A
future CPIH profile needs its own version/option binding, decimal and unit
semantics, lifecycle warnings and missing-value policy before gateway integration.
No browser tool is added by this probe. The provider-backed page-tool decision,
threat review and result contracts remain prerequisites in the
[work package](WEB-216_PUBLIC_DATA_WORKBENCH.md).

The empirical run tests one maintained ONS time-series route. The historical CMD
draft was rejected after mock-only testing. Neither establishes Census/Nomis parity or completion
of all X03 negative and live recovery cases. Those limits remain visible in the
[continuing journal](../chronicle/WEB-216_JOURNAL.md).
