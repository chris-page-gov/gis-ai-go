"""Controlled failures for the private execution boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

ExecutionProblemCode = Literal[
    "INVALID_REQUEST",
    "NOT_FOUND",
    "METHOD_NOT_ALLOWED",
    "UNKNOWN_OPERATION",
    "SOURCE_MISMATCH",
    "INVALID_CRS",
    "INVALID_AXIS_ORDER",
    "INVALID_GEOMETRY",
    "LIMIT_EXCEEDED",
    "DEADLINE_EXCEEDED",
    "EXECUTION_CANCELLED",
    "OUTPUT_LIMIT_EXCEEDED",
    "CAPACITY_EXCEEDED",
    "INTERNAL_ERROR",
]


@dataclass(frozen=True, slots=True)
class ExecutionFailure(Exception):
    """A bounded error that is safe to return across the private interface."""

    status: int
    code: ExecutionProblemCode
    title: str
    detail: str
    retryable: bool = False

    def __str__(self) -> str:
        """Avoid reflecting request, path or provider material through exceptions."""

        return self.code

    def as_problem(
        self,
        *,
        request_id: str | None = None,
        trace: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Return the closed execution-problem envelope."""

        return {
            "schema": "gis-ai-go.execution-problem.v1",
            "request_id": request_id,
            "trace": trace,
            "status": self.status,
            "code": self.code,
            "title": self.title,
            "detail": self.detail,
            "retryable": self.retryable,
        }


INVALID_REQUEST = ExecutionFailure(
    400,
    "INVALID_REQUEST",
    "Invalid execution request",
    "The request does not match the closed execution contract.",
)
UNKNOWN_OPERATION = ExecutionFailure(
    422,
    "UNKNOWN_OPERATION",
    "Unknown operation",
    "The requested operation is not allowlisted by this service.",
)
SOURCE_MISMATCH = ExecutionFailure(
    422,
    "SOURCE_MISMATCH",
    "Source mismatch",
    "The source selection does not match the allowlisted fixture.",
)
INVALID_CRS = ExecutionFailure(
    422,
    "INVALID_CRS",
    "Invalid coordinate reference system",
    "The fixture operation accepts EPSG 4326 only.",
)
INVALID_AXIS_ORDER = ExecutionFailure(
    422,
    "INVALID_AXIS_ORDER",
    "Invalid axis order",
    "The fixture operation accepts longitude latitude order only.",
)
INVALID_GEOMETRY = ExecutionFailure(
    422,
    "INVALID_GEOMETRY",
    "Invalid geometry",
    "The geometry is not a valid bounded single ring polygon.",
)
LIMIT_EXCEEDED = ExecutionFailure(
    413,
    "LIMIT_EXCEEDED",
    "Execution limit exceeded",
    "The request exceeds a service or gateway supplied execution limit.",
)
DEADLINE_EXCEEDED = ExecutionFailure(
    408,
    "DEADLINE_EXCEEDED",
    "Execution deadline exceeded",
    "The bounded execution deadline has been exceeded.",
    True,
)
EXECUTION_CANCELLED = ExecutionFailure(
    409,
    "EXECUTION_CANCELLED",
    "Execution cancelled",
    "The private gateway cancelled this execution.",
    True,
)
OUTPUT_LIMIT_EXCEEDED = ExecutionFailure(
    413,
    "OUTPUT_LIMIT_EXCEEDED",
    "Execution output limit exceeded",
    "The canonical result exceeds the permitted output size.",
)
INTERNAL_ERROR = ExecutionFailure(
    500,
    "INTERNAL_ERROR",
    "Execution failed",
    "The execution service could not complete the request safely.",
    True,
)
