# Providers

The private provider-adapter package contains the deterministic synthetic fixture
and one exact-selection ONS Data API adapter. Both are suspended by default. The
fixture performs no network request and contains no official statistic. The ONS
adapter can make one fixed-selection bounded public call only when explicitly
activated in a test; no shipped runtime registers it.

The ONS folder includes the version-bound source and rights preflight plus a
privacy-safe successful live-probe record and the one exact content-addressed T04
cache fallback derived from that accepted result identity. Neither record activates
the adapter or configures a runtime; later
gateway-to-execution integration must reuse the accepted EXEC-202 service envelope
rather than define another.
