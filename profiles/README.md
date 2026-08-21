# Governed profiles

Profiles in this directory are checked-in governance data. They do not register,
advertise or activate a runtime capability.

[`tool-registry.v1.json`](tool-registry.v1.json) contains exactly the 12 canonical
tool profiles accepted by ADR-0009. Its `current` fields describe the repository
candidate, while `v02Target` records a non-runtime release objective. Only the
gateway activation document can authorise production registration, and the
registry package has no environment override or gateway integration.

[`public-selection-profile.v1.json`](public-selection-profile.v1.json) contains
the single reviewed `PV-ONS-DATA` candidate, finite constraint grammar, exact
ranking weights and content-addressed non-executable plan used by the inactive
`selection.resolve` application. It does not grant execution authority or call a
provider.

The profiles are validated by
[`tool-registry.schema.json`](../schemas/tool-registry.schema.json), the repository
contract validator, operation-specific checkers and their private TypeScript
packages.
