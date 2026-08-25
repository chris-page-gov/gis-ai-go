"""Expose the QUAL-206 verifier regressions to repository-wide discovery."""

from tests.interoperability.test_qual_206_local_http_preflight import (
    LocalHttpPreflightVerifierTest,
)


__all__ = ["LocalHttpPreflightVerifierTest"]
