# Bounded Linked Identifiers evidence

Owner: repository owner. Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Method version: 1, authored 20 October 2026. This local candidate adds no hosted
MCP tool, deployment, entitlement decision or live acceptance claim.

`linked_identifiers.py` captures explicitly selected typed identifier or feature
lookups and product-version metadata. `relationship_plan.py` compares supplied
source-backed relationship candidates before considering a separately justified
spatial fallback. Both Linked Identifiers and native references can contribute;
no automatic preference for a native reference can replace investigation of a
missing API relationship. The planner does not execute either route.

## Source and relationship boundaries

The [capability profile](../../okf-plus/profile/os-linked-identifiers-capabilities.json)
binds current official documentation and the official example that establishes
the literal API base. The shared authentication guide permits a `key` HTTP header;
the operation OpenAPI declares query authentication instead. This implementation
uses the header only, without a query-key fallback. Its successful runtime use
requires a separately recorded bounded observation.

Typed nodes retain the native identifier string, identifier type and feature type.
The untyped endpoint remains unadmitted because UPRN and USRN namespaces overlap.
Returned groups and arrays are set-valued: preserve zero, one or many links,
direction, method, correlation identifier, native confidence and both endpoints'
version fields. There is no global one-to-one promise. Confidence concerns source
version alignment, not probability or positional accuracy. Dates retain their
native strings; retrieval time is not feature validity or a source edition.

Method 2 links Road Links to road-surface Topographic Areas, not buildings.
Method 5 links BLPUs to Topographic Areas through the published cross-reference;
that association alone does not classify a polygon as a building. Method 9 relates BLPUs to the
published closest-road association; it is not verified access or serving-road
topology. Methods 5, 9 and 11 include live, provisional and historic BLPUs.
Method 13 uses non-persistent Open Roads node identifiers. Every method keeps its
own source and limitations in the profile. Chaining methods 9 and 5 preserves
two associations; it does not establish transitive identity or access.

The planner currently supports only the API's identifier/feature namespaces,
including native-reference candidates expressed in those same namespaces.
NGD Building/OSID, PathLink and ONS GSS/area comparisons are unsupported and need
separate source-bound bridge contracts. An NGD identifier is not silently changed
into a TOID. This increment does not implement the authority-to-small-area-to-road,
building and UPRN map journey. Geometry, heights and rendering remain separate.

## Policy, transport and durable state

Selections are closed and bind the capability-profile SHA-256, explicit operations,
immutable limits and an absolute UTC `deadlineUtc`. The client constructs only
three fixed GET route families on `api.os.uk`: typed identifiers, typed features
and product-version information. No source URL, returned link or response text
can extend the selection. No paging parameters are invented, no relationships
are recursively followed and no provider script is executed.

The credential is read from `OS_API_KEY` only at execution. It is never put in a
URL, log, receipt or exception message. The client disables environment proxies,
rejects redirects, requests identity-encoded JSON and rejects unsupported media
or compression. A declared Content-Length must be a single bounded decimal and
match the complete body. Conflicting length/transfer headers are refused; chunked
bodies require their terminating framing, and unframed bodies must reach EOF
within the byte/deadline bounds. TLS uses the standard verified HTTPS transport; this is not an
independent pinned-DNS transport. Provider error bodies and headers are not saved.
Raw or JSON-escaped credential reflections prevent response retention.

Hard ceilings are 20 cumulative attempts, 8 MiB of charged body bytes, 300 seconds,
1 MiB per response and at least 2.05 seconds between sequential starts. A concrete
selection may lower those bounds. Other callers can still consume the same
provider-project allowance; these local limits are not an account-wide financial
stop. The absolute UTC deadline is rechecked after durable reservation and bounds
each request, including DNS and body reading through a POSIX wall timer.

Each attempt reserves its maximum body and remaining request-time allowance in a
synchronised private receipt before network access. Successful verified responses
replace reservations with measured body bytes and elapsed time. Failed or pending
attempts retain conservative charges and stop automatic continuation; HTTP 429,
authentication failure and redirects never trigger automatic retry. An ordinary
resume replays and independently validates every retained successful response and
observation. It cannot change the selection, replenish limits or hide an uncertain
attempt. A separately reviewed new selection is needed after a failed attempt.

The output directory must be new or carry the exact existing selection. It is
owner-only, uses a single regular-file lock and refuses symbolic links, linked
files, unmarked contents and overwrites of response files. File and directory
synchronisation does not establish hardware durability, rollback protection,
independent attestation or safety against a hostile local owner. Use the tested
local filesystem and independent backup procedure.

## Contracts and completion

The [capture schema](../../okf-plus/schemas/linked-identifiers.schema.json) closes
selection, observation and receipt fields. The
[planner schema](../../okf-plus/schemas/relationship-plan.schema.json) closes its
input and result. Runtime checks additionally enforce source-profile identity,
request/response binding, method endpoint pairs, checksums and aggregate limits.
The upstream OpenAPI's misspelt `methodIdentfier` requirement is recorded; only its
declared `methodIdentifier` property is admitted. Correlated identifier items
require their documented fields despite the misplaced array-level requirement.
The source permits optional `productPublicationName` strings to be empty; present
empty strings remain distinct from absent fields. Null and non-string values fail.
An unexpected shape fails rather than receiving an invented alias. A bounded,
strictly parsed JSON response that passes recursive credential-reflection checks
but violates the response contract is retained privately as a diagnostic, with its
hash and byte count. It cannot produce a graph or successful completion. Malformed
or reflected data is not retained. Diagnostic attempts keep their original
conservative charges, verify their retained checksum on resume and never retry
automatically; no additional provider call is needed to inspect the mismatch.

A complete capture means all selected operations returned complete, bounded,
validated JSON. It does not mean national coverage or an atomic snapshot. Limits
are 32 correlation groups and 1,000 edges per response, JSON depth 24 and 2 MiB
per observation. Exact-cap responses fail conservatively because truncation is
not ruled out. Missing versions stay missing. Raw responses remain private and
retained; this client neither disposes of them nor builds a permanent graph.
A separate reviewed retention/disposal procedure remains necessary.

Planner candidates require source references and hashes, compatible scope and
version assessments. These are supplied evidence assertions, not independently
verified source contents or execution authority. Native and API candidates remain
separate. Optional `targetSemantics` distinguishes a building outline from a road
surface; method 2 cannot satisfy a building-outline request, and method 5 alone leaves
building classification unresolved. Empty responses,
denials and incomplete observations do not prove absence. Spatial fallback is
always marked as requiring separate review, even if explicitly requested.

## Use and verification

Prepare a private selection conforming to the schema, with a deadline and explicit
limits; never include credentials in that file. Then, only within existing
specific provider authority:

```sh
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.linked_identifiers \
  --selection artifacts/private-linked/selection.json \
  --output artifacts/private-linked/new-capture
```

The parent directory must already exist. Standard output contains only completion,
a fixed reason and attempt count. The planner is offline; its result can contain
private identifiers, so direct its output to private storage:

```sh
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.relationship_plan \
  --input artifacts/private-linked/plan-input.json \
  > artifacts/private-linked/plan.json
```

Synthetic contract tests cover credential destinations/reflection, route injection,
redirect/proxy rejection, deadlines, immutable budgets, interrupted reservations,
concurrent writers, filesystem refusal, checksum replay, namespace collisions,
version types, zero/many links, source schema defects and false relationship or
spatial equivalence. No test requires a key or live provider.
