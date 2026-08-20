# Public authority context

This package constructs the one authority context available to the first public
catalogue slice: an anonymous, open, read-only context owned by the gateway. The
context is content-addressed using RFC 8785 JSON canonicalisation and is
recursively frozen before it is exported.

`getPublicAuthorityContext()` accepts no caller input. In particular, this
package does not consume or infer a user, organisation, role, client, device,
credential, token, entitlement or request time. Authentication and identity
integration are outside this slice.

The context permits only `catalogue.search` and `catalogue.describe`. Both
operations require an inline receipt that is explicitly not persisted and not
attested.
