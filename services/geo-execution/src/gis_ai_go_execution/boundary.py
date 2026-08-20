"""Public metadata for the closed private execution boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .service import ExecutionService


@dataclass(slots=True)
class ExecutionBoundary:
    """A private synthetic-only boundary with no identity or policy authority."""

    product: str = "GIS AI GO"
    service: str = "gis-ai-go-execution"
    stage: int = 2
    live_provider_calls: bool = False
    end_user_authentication: bool = False
    policy_authority: bool = False
    public_ingress: bool = False
    operations: tuple[str, ...] = ("fixture.features.query",)
    _executor: ExecutionService = field(default_factory=ExecutionService, repr=False)

    def execute(self, request: Any, *, raw_size: int | None = None) -> dict[str, Any]:
        """Execute one validated gateway envelope through the allowlisted service."""

        return self._executor.execute(request, raw_size=raw_size)

    def cancel(self, request_id: str) -> bool:
        """Cancel one active private execution."""

        return self._executor.cancel(request_id)
