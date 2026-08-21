# Synthetic fixtures

The `execution-*.example.json` records form one gateway-to-Python acceptance
round trip for EXEC-202. They contain only fictional point records and a synthetic
source identity. The request carries a gateway assertion, not an end-user identity
or reusable credential; the Python service validates its closed shape but does not
make an authentication or policy decision.

These examples contain invented identities, catalogue values and results. The public
authority, policy-decision and inline-receipt examples have reproducible canonical
content identities, but remain synthetic contract fixtures rather than evidence of
real access. They contain no licensed provider feature data.

The older authority, policy and receipt examples were adapted from the 19 August
2026 research pack and remain candidate fixtures for deferred protected workflows.

The `public-read-resource`, `public-authority-context-v2`,
`public-policy-decision-v2` and `evidence-receipt-v2` examples reproduce the exact
inactive public ONS prerequisite identities. They contain profile, provider,
dataset-version and licence evidence but no provider observation, raw query,
credential, personal data or protected data. They do not show a live call or an
activated tool. Denied and ambiguous operations deliberately have no success
receipt fixture.

`selection-plan.example.json`, the selection request and the unresolved problem
fixture cover the deterministic inactive resolver. The plan is an exact
non-executable projection; it contains no observation and is not evidence of a
provider call. Problem fixtures deliberately contain no receipt.

The `data-query-parameters`, `data-query-result` and `data-query-problem` examples
exercise the later inactive application-only seam. The successful fixture retains
the already documented public aggregate scalar `10471` to reproduce its complete
result-core and receipt digests; it is not a fresh live query or stored provider
response. The provider, caller-cancelled and caller-deadline problem fixtures are
deliberately receipt-free and cannot retain an abort reason, deadline, adapter
message, provider status, payload, credential, path or stack.

The `data-query-request` fixture wraps those unchanged parameters with a synthetic
caller-generated 256-bit idempotency key. The three reconciliation-problem fixtures
are closed, receipt-free 409 responses for pending, completed and conflicting use of
that key. The public correlation key must be random and must not encode personal or
secret material. `evidence-inspect-request-v2` demonstrates the separate receipt-only
lookup; the key is input material and is never a resource URI.

The reconciliation index, claim and resolution examples are deterministic synthetic
storage documents. The claim retains only domain-separated digests and bounded public
identifiers; the resolution retains only the receipt identity. They contain neither
the raw idempotency key nor query or result material, and do not demonstrate an
activated transport or provider call.

The `@gis-ai-go/provider-adapter-sdk` package supplies a frozen statistics fixture
with fixture-native dataset, version, dimension and option identifiers. Both its
discovery and invocation planes are suspended unless a test activates them
explicitly. It performs no egress and labels every result as synthetic.
`provider-adapter-result.example.json` is the closed contract projection of that
synthetic result; it is not an ONS payload or live evidence.
