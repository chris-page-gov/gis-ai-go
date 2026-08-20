# Compiled public catalogue policy

This package evaluates one checked-in, content-addressed policy document for the
anonymous public catalogue. It is a local compiled JSON allow-list with a
default-deny outcome. Only `catalogue.search` and `catalogue.describe` can be
allowed, and both carry all six inline evidence and licence obligations.

Before allowing either operation, the evaluator checks that the catalogue is a
bounded, metadata-only publication whose records are public, open, read-only and
contain neither personal nor protected data. Other governed operations receive a
hashed deny decision. An operation outside the governed vocabulary receives an
explicit deny result without manufacturing a schema-invalid decision.

The authority context is constructed inside the server package; callers cannot
supply identity, role, device or entitlement claims. This package has no OPA
client, remote policy decision point, authentication, identity integration or
entitlement logic. Policy changes require a new checked-in document and content
identity.
