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

The `@gis-ai-go/provider-adapter-sdk` package supplies a frozen statistics fixture
with fixture-native dataset, version, dimension and option identifiers. Both its
discovery and invocation planes are suspended unless a test activates them
explicitly. It performs no egress and labels every result as synthetic.
`provider-adapter-result.example.json` is the closed contract projection of that
synthetic result; it is not an ONS payload or live evidence.
