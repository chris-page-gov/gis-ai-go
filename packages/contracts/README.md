# Shared contracts

This private workspace package is the shared implementation boundary for GIS AI GO
contracts. It currently provides:

- the defensive public-catalogue parser;
- controlled search, facet, graph and timeline semantics;
- the navigation-link policy used by catalogue consumers; and
- TypeScript types corresponding to the canonical public OKF publication.

The static Explorer imports this package through a compatibility adapter. Future
MCP and direct-API transports must use the same functions rather than copy or
reinterpret catalogue fields.

JSON Schema files under [`../../schemas`](../../schemas/) remain the machine-readable
authority for transport requests and responses. The checksum-verified OKF bundle is
the authority for catalogue records; TypeScript types do not create new records or
provider capabilities.

The candidate catalogue result schema deliberately omits a receipt. `EVID-204` must
add and verify the canonical inline evidence contract before any public catalogue
tool is activated; an opaque reference must not imply an evidence store that does
not exist.

The package does not start a listener, fetch a provider, execute Python, decide
policy or persist evidence.
