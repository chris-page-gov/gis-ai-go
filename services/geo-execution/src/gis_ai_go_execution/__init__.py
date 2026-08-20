"""Closed deterministic GIS AI GO execution boundary."""

from .boundary import ExecutionBoundary
from .canonical import (
    EXECUTION_PARAMETERS_DOMAIN,
    EXECUTION_RESULT_DATA_DOMAIN,
    canonical_json_bytes,
    sha256_identity,
    strict_json_loads,
)
from .errors import ExecutionFailure
from .http import create_http_server, openapi_document
from .service import CancellationToken, ExecutionService

__all__ = [
    "CancellationToken",
    "ExecutionBoundary",
    "ExecutionFailure",
    "ExecutionService",
    "EXECUTION_PARAMETERS_DOMAIN",
    "EXECUTION_RESULT_DATA_DOMAIN",
    "canonical_json_bytes",
    "create_http_server",
    "openapi_document",
    "sha256_identity",
    "strict_json_loads",
]
