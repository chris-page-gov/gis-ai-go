"""Reject live execution until a later stage is explicitly approved."""

from dataclasses import dataclass
from typing import NoReturn


class StageZeroBoundaryError(RuntimeError):
    """Raised when execution is attempted during Stage 0."""


@dataclass(frozen=True, slots=True)
class ExecutionBoundary:
    """Metadata and fail-closed execution boundary for the Stage 0 scaffold."""

    product: str = "GIS AI GO"
    service: str = "gis-ai-go-execution"
    stage: int = 0
    live_provider_calls: bool = False

    def execute(self, operation: str) -> NoReturn:
        """Reject every operation until deterministic execution is implemented."""

        raise StageZeroBoundaryError(
            f"Stage 0 cannot execute {operation!r}; live execution is not authorised"
        )
