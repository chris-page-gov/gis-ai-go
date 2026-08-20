# Governed profiles

Profiles in this directory are checked-in governance data. They do not register,
advertise or activate a runtime capability.

[`tool-registry.v1.json`](tool-registry.v1.json) contains exactly the 12 canonical
tool profiles accepted by ADR-0009. Its `current` fields describe the repository
candidate, while `v02Target` records a non-runtime release objective. Only the
gateway activation document can authorise production registration, and the
registry package has no environment override or gateway integration.

The profile is validated by
[`tool-registry.schema.json`](../schemas/tool-registry.schema.json), the repository
contract validator, Python source-provenance tests and the private
`@gis-ai-go/tool-registry` TypeScript package.
