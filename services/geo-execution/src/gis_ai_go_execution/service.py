"""Typed, allowlisted and deterministic private execution service."""

from __future__ import annotations

import copy
import re
import threading
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Any

from .canonical import (
    EXECUTION_PARAMETERS_DOMAIN,
    EXECUTION_RESULT_DATA_DOMAIN,
    StrictJsonError,
    canonical_json_bytes,
    sha256_identity,
)
from .errors import (
    DEADLINE_EXCEEDED,
    EXECUTION_CANCELLED,
    INTERNAL_ERROR,
    INVALID_AXIS_ORDER,
    INVALID_CRS,
    INVALID_GEOMETRY,
    INVALID_REQUEST,
    LIMIT_EXCEEDED,
    OUTPUT_LIMIT_EXCEEDED,
    SOURCE_MISMATCH,
    UNKNOWN_OPERATION,
    ExecutionFailure,
)
from .fixtures import FEATURES, FIXTURE_ID, SOURCE
from .geometry import point_in_polygon, validate_polygon

REQUEST_SCHEMA = "gis-ai-go.execution-request.v1"
RESULT_SCHEMA = "gis-ai-go.execution-result.v1"
OPERATION = "fixture.features.query"
AUTHORISATION_SCHEMA = "gis-ai-go.gateway-authorisation.v1"

MAX_REQUEST_BYTES = 65_536
MAX_OUTPUT_BYTES = 262_144
MAX_FEATURES = 100
MAX_COORDINATES = 128
MAX_COMPLEXITY = 20_000
MAX_DEADLINE = timedelta(seconds=30)
MAX_TRACESTATE_CHARACTERS = 512

IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,127}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}$")
TRACESTATE_KEY = re.compile(r"^[a-z0-9][a-z0-9_\-*/@]{0,255}$")
RFC3339 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)

Clock = Callable[[], datetime]
Checkpoint = Callable[[str, int], None]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _object(value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise INVALID_REQUEST
    return value


def _identifier(value: Any) -> str:
    if not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None:
        raise INVALID_REQUEST
    return value


def _integer(value: Any, *, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise INVALID_REQUEST
    if not minimum <= value <= maximum:
        raise LIMIT_EXCEEDED
    return value


def _trace(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or not {"traceparent"} <= set(value) <= {
        "traceparent",
        "tracestate",
    }:
        raise INVALID_REQUEST
    traceparent = value.get("traceparent")
    if not isinstance(traceparent, str):
        raise INVALID_REQUEST
    match = TRACEPARENT.fullmatch(traceparent)
    if match is None or match.group(1) == "0" * 32 or match.group(2) == "0" * 16:
        raise INVALID_REQUEST
    result = {"traceparent": traceparent}
    if "tracestate" in value:
        tracestate = value["tracestate"]
        if (
            not isinstance(tracestate, str)
            or len(tracestate) > MAX_TRACESTATE_CHARACTERS
        ):
            raise INVALID_REQUEST
        members = tracestate.split(",")
        if len(members) > 32:
            raise INVALID_REQUEST
        keys: set[str] = set()
        for raw_member in members:
            member = raw_member.strip(" \t")
            if member == "":
                continue
            if member.count("=") != 1:
                raise INVALID_REQUEST
            key, member_value = member.split("=", maxsplit=1)
            if (
                TRACESTATE_KEY.fullmatch(key) is None
                or key in keys
                or not 1 <= len(member_value) <= 256
                or member_value.endswith(" ")
                or any(
                    not (
                        0x20 <= ord(character) <= 0x2B
                        or 0x2D <= ord(character) <= 0x3C
                        or 0x3E <= ord(character) <= 0x7E
                    )
                    for character in member_value
                )
            ):
                raise INVALID_REQUEST
            keys.add(key)
        result["tracestate"] = tracestate
    return result


def _deadline(value: Any, now: datetime) -> datetime:
    if (
        not isinstance(value, str)
        or not 1 <= len(value) <= 64
        or RFC3339.fullmatch(value) is None
    ):
        raise INVALID_REQUEST
    try:
        deadline = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise INVALID_REQUEST from None
    if deadline.tzinfo is None or deadline.utcoffset() is None:
        raise INVALID_REQUEST
    deadline = deadline.astimezone(timezone.utc)
    if deadline <= now:
        raise DEADLINE_EXCEEDED
    if deadline - now > MAX_DEADLINE:
        raise LIMIT_EXCEEDED
    return deadline


class CancellationToken:
    """Thread-safe cooperative cancellation checked at bounded work checkpoints."""

    def __init__(self) -> None:
        self._cancelled = threading.Event()

    def cancel(self) -> None:
        self._cancelled.set()

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set()


class CancellationRegistry:
    """Track only currently executing request identifiers in memory."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._active: dict[str, CancellationToken] = {}

    def register(self, request_id: str, token: CancellationToken) -> None:
        with self._lock:
            if request_id in self._active:
                raise INVALID_REQUEST
            self._active[request_id] = token

    def remove(self, request_id: str, token: CancellationToken) -> None:
        with self._lock:
            if self._active.get(request_id) is token:
                self._active.pop(request_id, None)

    def cancel(self, request_id: str) -> bool:
        with self._lock:
            token = self._active.get(request_id)
            if token is None:
                return False
            token.cancel()
            return True


class ExecutionService:
    """Execute the single reviewed synthetic operation and nothing else."""

    def __init__(
        self,
        *,
        clock: Clock = _utc_now,
        checkpoint: Checkpoint | None = None,
        registry: CancellationRegistry | None = None,
    ) -> None:
        self._clock = clock
        self._checkpoint_hook = checkpoint
        self._registry = registry or CancellationRegistry()
        self._validate_fixture()

    @property
    def ready(self) -> bool:
        """The synthetic fixture is loaded and passed its closed startup checks."""

        return True

    def cancel(self, request_id: str) -> bool:
        """Cooperatively cancel one active private execution, if present."""

        if IDENTIFIER.fullmatch(request_id) is None:
            return False
        return self._registry.cancel(request_id)

    def execute(
        self,
        request: Any,
        *,
        raw_size: int | None = None,
        cancellation: CancellationToken | None = None,
    ) -> dict[str, Any]:
        """Validate and execute one closed gateway-authorised envelope."""

        request_id: str | None = None
        token = cancellation or CancellationToken()
        registered = False
        try:
            validated = self._validate_request(request, raw_size=raw_size)
            request_id = validated["request_id"]
            self._registry.register(request_id, token)
            registered = True
            return self._execute_fixture(validated, token)
        except ExecutionFailure:
            raise
        except (StrictJsonError, RecursionError, ValueError, TypeError):
            raise INVALID_REQUEST from None
        except Exception:
            raise INTERNAL_ERROR from None
        finally:
            if registered and request_id is not None:
                self._registry.remove(request_id, token)

    def _validate_fixture(self) -> None:
        if len(FEATURES) > MAX_FEATURES:
            raise RuntimeError("synthetic fixture exceeds the service feature limit")
        identifiers: set[str] = set()
        for feature in FEATURES:
            if set(feature) != {"type", "id", "geometry", "properties"}:
                raise RuntimeError("synthetic fixture has an invalid closed feature")
            identifier = feature.get("id")
            if not isinstance(identifier, str) or identifier in identifiers:
                raise RuntimeError("synthetic fixture identifiers are invalid")
            identifiers.add(identifier)
            geometry = feature.get("geometry")
            if (
                not isinstance(geometry, dict)
                or set(geometry) != {"type", "coordinates"}
                or geometry.get("type") != "Point"
                or not isinstance(geometry.get("coordinates"), list)
                or len(geometry["coordinates"]) != 2
            ):
                raise RuntimeError("synthetic fixture geometry is invalid")
        canonical_json_bytes(list(FEATURES))

    def _validate_request(self, request: Any, *, raw_size: int | None) -> dict[str, Any]:
        root = _object(
            request,
            {
                "schema",
                "request_id",
                "operation",
                "trace",
                "gateway_authorisation",
                "deadline",
                "limits",
                "parameters",
            },
        )
        if root["schema"] != REQUEST_SCHEMA:
            raise INVALID_REQUEST
        request_id = _identifier(root["request_id"])
        operation = root["operation"]
        if not isinstance(operation, str) or operation != OPERATION:
            raise UNKNOWN_OPERATION
        trace = _trace(root["trace"])

        authorisation = _object(
            root["gateway_authorisation"],
            {"schema", "decision_id", "decision_digest", "permitted_operation"},
        )
        if authorisation["schema"] != AUTHORISATION_SCHEMA:
            raise INVALID_REQUEST
        _identifier(authorisation["decision_id"])
        if (
            not isinstance(authorisation["decision_digest"], str)
            or SHA256.fullmatch(authorisation["decision_digest"]) is None
            or authorisation["permitted_operation"] != operation
        ):
            raise INVALID_REQUEST

        limits = _object(
            root["limits"],
            {
                "max_features",
                "max_coordinates",
                "max_input_bytes",
                "max_output_bytes",
                "max_complexity",
            },
        )
        validated_limits = {
            "max_features": _integer(limits["max_features"], minimum=1, maximum=MAX_FEATURES),
            "max_coordinates": _integer(
                limits["max_coordinates"], minimum=4, maximum=MAX_COORDINATES
            ),
            "max_input_bytes": _integer(
                limits["max_input_bytes"], minimum=1024, maximum=MAX_REQUEST_BYTES
            ),
            "max_output_bytes": _integer(
                limits["max_output_bytes"], minimum=1024, maximum=MAX_OUTPUT_BYTES
            ),
            "max_complexity": _integer(
                limits["max_complexity"], minimum=16, maximum=MAX_COMPLEXITY
            ),
        }
        observed_size = raw_size if raw_size is not None else len(canonical_json_bytes(root))
        if observed_size > validated_limits["max_input_bytes"]:
            raise LIMIT_EXCEEDED

        parameters = _object(
            root["parameters"],
            {"fixture_id", "source", "crs", "axis_order", "geometry", "limit"},
        )
        if parameters["fixture_id"] != FIXTURE_ID:
            raise SOURCE_MISMATCH
        if not isinstance(parameters["source"], dict) or parameters["source"] != dict(SOURCE):
            raise SOURCE_MISMATCH
        if parameters["crs"] != "EPSG:4326":
            raise INVALID_CRS
        if parameters["axis_order"] != "longitude-latitude":
            raise INVALID_AXIS_ORDER
        limit = _integer(parameters["limit"], minimum=1, maximum=MAX_FEATURES)
        if limit > validated_limits["max_features"]:
            raise LIMIT_EXCEEDED
        ring = validate_polygon(
            parameters["geometry"],
            max_coordinates=validated_limits["max_coordinates"],
        )
        complexity = (len(ring) - 1) ** 2 + len(FEATURES)
        if complexity > validated_limits["max_complexity"]:
            raise LIMIT_EXCEEDED
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise INTERNAL_ERROR
        deadline = _deadline(root["deadline"], now.astimezone(timezone.utc))

        return {
            "request_id": request_id,
            "operation": operation,
            "trace": trace,
            "deadline": deadline,
            "limits": validated_limits,
            "parameters": parameters,
            "ring": ring,
        }

    def _checkpoint(
        self,
        request_id: str,
        index: int,
        token: CancellationToken,
        deadline: datetime,
    ) -> None:
        if token.cancelled:
            raise EXECUTION_CANCELLED
        if self._clock().astimezone(timezone.utc) >= deadline:
            raise DEADLINE_EXCEEDED
        if self._checkpoint_hook is not None:
            self._checkpoint_hook(request_id, index)
        if token.cancelled:
            raise EXECUTION_CANCELLED

    def _execute_fixture(
        self,
        request: dict[str, Any],
        token: CancellationToken,
    ) -> dict[str, Any]:
        parameters = request["parameters"]
        selected: list[dict[str, Any]] = []
        for index, feature in enumerate(sorted(FEATURES, key=lambda item: item["id"])):
            self._checkpoint(
                request["request_id"],
                index,
                token,
                request["deadline"],
            )
            coordinates = feature["geometry"]["coordinates"]
            point = (float(coordinates[0]), float(coordinates[1]))
            if point_in_polygon(point, request["ring"]):
                selected.append(copy.deepcopy(feature))
            if len(selected) >= parameters["limit"]:
                break

        data = {
            "type": "FeatureCollection",
            "crs": "EPSG:4326",
            "axis_order": "longitude-latitude",
            "features": selected,
        }
        source = copy.deepcopy(dict(SOURCE))
        result = {
            "schema": RESULT_SCHEMA,
            "request_id": request["request_id"],
            "operation": request["operation"],
            "status": "succeeded",
            "trace": copy.deepcopy(request["trace"]),
            "data": data,
            "evidence": {
                "schema": "gis-ai-go.execution-evidence.v1",
                "input_sha256": sha256_identity(EXECUTION_PARAMETERS_DOMAIN, parameters),
                "output_sha256": sha256_identity(EXECUTION_RESULT_DATA_DOMAIN, data),
                "feature_count": len(selected),
                "source": source,
                "transformation": {
                    "operation": "synthetic-point-in-polygon-v1",
                    "source_crs": "EPSG:4326",
                    "source_axis_order": "longitude-latitude",
                    "output_crs": "EPSG:4326",
                    "output_axis_order": "longitude-latitude",
                    "geometry_repair": "none",
                    "geometry_simplification": "none",
                },
                "software": {
                    "name": "gis-ai-go-execution",
                    "version": "0.1.0",
                    "algorithm": "synthetic-point-in-polygon-v1",
                },
            },
        }
        if len(canonical_json_bytes(result)) > request["limits"]["max_output_bytes"]:
            raise OUTPUT_LIMIT_EXCEEDED
        return result


def safe_request_context(value: Any) -> tuple[str | None, dict[str, str] | None]:
    """Extract only already-safe identifiers for a controlled problem response."""

    if not isinstance(value, dict):
        return (None, None)
    request_id = value.get("request_id")
    if not isinstance(request_id, str) or IDENTIFIER.fullmatch(request_id) is None:
        request_id = None
    try:
        trace = _trace(value.get("trace"))
    except ExecutionFailure:
        trace = None
    return (request_id, trace)
