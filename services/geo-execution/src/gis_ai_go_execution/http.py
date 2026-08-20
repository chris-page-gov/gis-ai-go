"""Loopback-only HTTP adapter for private container and gateway acceptance."""

from __future__ import annotations

import copy
import ipaddress
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, NoReturn

from .canonical import StrictJsonError, canonical_json_bytes, strict_json_loads
from .errors import INTERNAL_ERROR, INVALID_REQUEST, ExecutionFailure
from .service import MAX_REQUEST_BYTES, ExecutionService, safe_request_context

LOOPBACK_HOST = "127.0.0.1"
DEFAULT_PORT = 8091
MAX_CONCURRENT_REQUESTS = 8
HOST_HEADER = re.compile(r"^(?:localhost|127\.0\.0\.1|\[::1\])(?::[0-9]{1,5})?$")
CANCEL_PATH = re.compile(r"^/internal/v1/executions/([a-z0-9][a-z0-9._:-]{0,127})$")
CONTENT_TYPE = re.compile(r"^application/json(?:\s*;\s*charset=utf-8)?$", re.IGNORECASE)


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _load_schema(name: str) -> dict[str, Any]:
    path = _repository_root() / "schemas" / name
    return json.loads(path.read_text(encoding="utf-8"))


def _localise_schema_refs(value: Any, component: str) -> Any:
    """Make repository schema references self-contained inside OpenAPI components."""

    if isinstance(value, list):
        return [_localise_schema_refs(item, component) for item in value]
    if not isinstance(value, dict):
        return value
    result: dict[str, Any] = {}
    for key, item in value.items():
        if key == "$ref" and isinstance(item, str):
            if item.startswith("#/"):
                item = f"#/components/schemas/{component}/{item[2:]}"
            elif item.startswith("urn:gis-ai-go:schema:execution-request:1#/"):
                suffix = item.split("#/", 1)[1]
                item = f"#/components/schemas/ExecutionRequest/{suffix}"
            elif item.startswith("urn:gis-ai-go:schema:execution-result:1#/"):
                suffix = item.split("#/", 1)[1]
                item = f"#/components/schemas/ExecutionResult/{suffix}"
        result[key] = _localise_schema_refs(item, component)
    return result


def _openapi_component(name: str, component: str) -> dict[str, Any]:
    schema = _localise_schema_refs(_load_schema(name), component)
    schema.pop("$schema", None)
    schema_id = schema.pop("$id")
    schema["x-canonical-schema-id"] = schema_id
    return schema


def openapi_document() -> dict[str, Any]:
    """Return the complete private OpenAPI 3.1 contract."""

    request_schema = _openapi_component(
        "execution-request.schema.json", "ExecutionRequest"
    )
    result_schema = _openapi_component(
        "execution-result.schema.json", "ExecutionResult"
    )
    problem_schema = _openapi_component(
        "execution-problem.schema.json", "ExecutionProblem"
    )

    def status_schema(schema: str, status: str) -> dict[str, Any]:
        return {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "schema",
                "service",
                "status",
                "private",
                "live_provider_calls",
            ],
            "properties": {
                "schema": {"const": schema},
                "service": {"const": "gis-ai-go-execution"},
                "status": {"const": status},
                "private": {"const": True},
                "live_provider_calls": {"const": False},
            },
        }
    health_schema = status_schema("gis-ai-go.execution-health.v1", "ok")
    readiness_schema = status_schema("gis-ai-go.execution-ready.v1", "ready")
    cancel_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["schema", "request_id", "status"],
        "properties": {
            "schema": {"const": "gis-ai-go.execution-cancellation.v1"},
            "request_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9._:-]{0,127}$"},
            "status": {"enum": ["accepted", "not-active"]},
        },
    }
    problem_response = {
        "description": "Controlled non-reflective execution problem",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ExecutionProblem"}
            }
        },
    }
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "GIS AI GO private execution service",
            "version": "0.1.0",
            "description": (
                "Loopback-only synthetic execution boundary. This service does not authenticate "
                "end users, decide policy, fetch providers or expose a public route."
            ),
        },
        "servers": [
            {
                "url": f"http://{LOOPBACK_HOST}:{DEFAULT_PORT}",
                "description": "Private loopback acceptance only",
            }
        ],
        "security": [],
        "paths": {
            "/internal/health": {
                "get": {
                    "operationId": "executionHealth",
                    "responses": {
                        "200": {
                            "description": "Process health",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Health"}
                                }
                            },
                        }
                    },
                }
            },
            "/internal/readiness": {
                "get": {
                    "operationId": "executionReadiness",
                    "responses": {
                        "200": {
                            "description": "Validated synthetic fixture readiness",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Readiness"}
                                }
                            },
                        }
                    },
                }
            },
            "/internal/openapi.json": {
                "get": {
                    "operationId": "executionOpenApi",
                    "responses": {"200": {"description": "Private OpenAPI 3.1 document"}},
                }
            },
            "/internal/v1/execute": {
                "post": {
                    "operationId": "executeSyntheticFixture",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ExecutionRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Deterministic synthetic result",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ExecutionResult"}
                                }
                            },
                        },
                        "400": problem_response,
                        "408": problem_response,
                        "409": problem_response,
                        "413": problem_response,
                        "422": problem_response,
                        "429": problem_response,
                        "500": problem_response,
                    },
                }
            },
            "/internal/v1/executions/{request_id}": {
                "delete": {
                    "operationId": "cancelPrivateExecution",
                    "parameters": [
                        {
                            "name": "request_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string",
                                "pattern": "^[a-z0-9][a-z0-9._:-]{0,127}$",
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Cancellation state",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Cancellation"}
                                }
                            },
                        },
                        "400": problem_response,
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "ExecutionRequest": copy.deepcopy(request_schema),
                "ExecutionResult": copy.deepcopy(result_schema),
                "ExecutionProblem": copy.deepcopy(problem_schema),
                "Health": health_schema,
                "Readiness": readiness_schema,
                "Cancellation": cancel_schema,
            }
        },
    }


class PrivateExecutionServer(ThreadingHTTPServer):
    """A loopback-only concurrent server carrying one execution service."""

    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, address: tuple[str, int], service: ExecutionService) -> None:
        self.execution_service = service
        self.openapi = openapi_document()
        self._capacity = threading.BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
        super().__init__(address, PrivateExecutionHandler)

    def get_request(self) -> tuple[Any, Any]:
        """Bound slow or abandoned private connections before handler dispatch."""

        request, address = super().get_request()
        request.settimeout(5.0)
        return request, address

    def process_request(self, request: Any, client_address: Any) -> None:
        """Reject excess connections before allocating another handler thread."""

        if not self._capacity.acquire(blocking=False):
            problem = ExecutionFailure(
                429,
                "CAPACITY_EXCEEDED",
                "Execution capacity exceeded",
                "The private execution service has reached its concurrency limit.",
                True,
            ).as_problem()
            body = canonical_json_bytes(problem)
            response = (
                b"HTTP/1.1 429 Too Many Requests\r\n"
                b"Content-Type: application/json; charset=utf-8\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Cache-Control: no-store\r\n"
                + b"X-Content-Type-Options: nosniff\r\n"
                + b"Retry-After: 1\r\n"
                + b"Connection: close\r\n\r\n"
                + body
            )
            try:
                request.sendall(response)
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._capacity.release()
            raise

    def process_request_thread(self, request: Any, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._capacity.release()


class PrivateExecutionHandler(BaseHTTPRequestHandler):
    """Strict JSON-only adapter with no public or end-user identity surface."""

    protocol_version = "HTTP/1.1"
    server_version = "gis-ai-go-execution"
    sys_version = ""

    @property
    def execution_server(self) -> PrivateExecutionServer:
        return self.server  # type: ignore[return-value]

    def log_message(self, _format: str, *_arguments: object) -> None:
        """Do not reflect private request paths or bodies through default logs."""

    def send_error(
        self,
        code: int,
        message: str | None = None,
        explain: str | None = None,
    ) -> None:
        """Replace BaseHTTPRequestHandler HTML and version disclosure."""

        del code, message, explain
        self._problem(
            ExecutionFailure(
                405,
                "METHOD_NOT_ALLOWED",
                "Method not allowed",
                "The private execution route does not accept this method.",
            )
        )

    def _private_request(self) -> bool:
        try:
            if not ipaddress.ip_address(self.client_address[0]).is_loopback:
                return False
        except ValueError:
            return False
        hosts = self.headers.get_all("Host", failobj=[])
        return len(hosts) == 1 and HOST_HEADER.fullmatch(hosts[0]) is not None

    def _write(self, status: int, value: Any, *, allow: str | None = None) -> None:
        body = canonical_json_bytes(value)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Connection", "close")
        if allow is not None:
            self.send_header("Allow", allow)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        self.close_connection = True

    def _problem(
        self,
        failure: ExecutionFailure,
        *,
        request_id: str | None = None,
        trace: dict[str, str] | None = None,
        allow: str | None = None,
    ) -> None:
        self._write(
            failure.status,
            failure.as_problem(request_id=request_id, trace=trace),
            allow=allow,
        )

    def _guard(self) -> bool:
        if self._private_request():
            return True
        self._problem(
            ExecutionFailure(
                400,
                "INVALID_REQUEST",
                "Invalid private request",
                "The request does not match the private loopback boundary.",
            )
        )
        return False

    def _read_json(self) -> tuple[Any, int]:
        encodings = self.headers.get_all("Content-Encoding", failobj=[])
        if len(encodings) > 1 or (encodings and encodings[0].lower() != "identity"):
            raise INVALID_REQUEST
        if self.headers.get_all("Transfer-Encoding", failobj=[]):
            raise INVALID_REQUEST
        content_types = self.headers.get_all("Content-Type", failobj=[])
        if len(content_types) != 1 or CONTENT_TYPE.fullmatch(content_types[0]) is None:
            raise INVALID_REQUEST
        lengths = self.headers.get_all("Content-Length", failobj=[])
        if len(lengths) != 1 or not lengths[0].isdigit():
            raise INVALID_REQUEST
        length = int(lengths[0])
        if length < 2:
            raise INVALID_REQUEST
        if length > MAX_REQUEST_BYTES:
            raise ExecutionFailure(
                413,
                "LIMIT_EXCEEDED",
                "Execution limit exceeded",
                "The request exceeds the private transport byte limit.",
            )
        payload = self.rfile.read(length)
        if len(payload) != length:
            raise INVALID_REQUEST
        return strict_json_loads(payload), length

    def do_GET(self) -> None:
        if not self._guard():
            return
        if self.path == "/internal/health":
            self._write(
                200,
                {
                    "schema": "gis-ai-go.execution-health.v1",
                    "service": "gis-ai-go-execution",
                    "status": "ok",
                    "private": True,
                    "live_provider_calls": False,
                },
            )
            return
        if self.path == "/internal/readiness":
            self._write(
                200,
                {
                    "schema": "gis-ai-go.execution-ready.v1",
                    "service": "gis-ai-go-execution",
                    "status": "ready",
                    "private": True,
                    "live_provider_calls": False,
                },
            )
            return
        if self.path == "/internal/openapi.json":
            self._write(200, self.execution_server.openapi)
            return
        self._problem(
            ExecutionFailure(
                404,
                "NOT_FOUND",
                "Route not found",
                "The private execution route does not exist.",
            )
        )

    def do_POST(self) -> None:
        if not self._guard():
            return
        if self.path != "/internal/v1/execute":
            self._problem(
                ExecutionFailure(
                    404,
                    "NOT_FOUND",
                    "Route not found",
                    "The private execution route does not exist.",
                )
            )
            return
        request: Any = None
        try:
            request, raw_size = self._read_json()
            result = self.execution_server.execution_service.execute(
                request,
                raw_size=raw_size,
            )
            self._write(200, result)
        except StrictJsonError:
            self._problem(INVALID_REQUEST)
        except ExecutionFailure as failure:
            request_id, trace = safe_request_context(request)
            self._problem(failure, request_id=request_id, trace=trace)
        except Exception:
            request_id, trace = safe_request_context(request)
            self._problem(INTERNAL_ERROR, request_id=request_id, trace=trace)

    def do_DELETE(self) -> None:
        if not self._guard():
            return
        if self.headers.get("Content-Length") not in (None, "0"):
            self._problem(INVALID_REQUEST)
            return
        match = CANCEL_PATH.fullmatch(self.path)
        if match is None:
            self._problem(
                ExecutionFailure(
                    404,
                    "NOT_FOUND",
                    "Route not found",
                    "The private execution route does not exist.",
                )
            )
            return
        request_id = match.group(1)
        accepted = self.execution_server.execution_service.cancel(request_id)
        self._write(
            200,
            {
                "schema": "gis-ai-go.execution-cancellation.v1",
                "request_id": request_id,
                "status": "accepted" if accepted else "not-active",
            },
        )

    def _method_not_allowed(self) -> None:
        if not self._guard():
            return
        self._problem(
            ExecutionFailure(
                405,
                "METHOD_NOT_ALLOWED",
                "Method not allowed",
                "The private execution route does not accept this method.",
            ),
            allow="GET, POST, DELETE",
        )

    do_CONNECT = _method_not_allowed
    do_HEAD = _method_not_allowed
    do_OPTIONS = _method_not_allowed
    do_PATCH = _method_not_allowed
    do_PUT = _method_not_allowed
    do_TRACE = _method_not_allowed


def create_http_server(
    *,
    port: int = DEFAULT_PORT,
    service: ExecutionService | None = None,
) -> PrivateExecutionServer:
    """Create but do not start the fixed-loopback private server."""

    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65_535:
        raise ValueError("port must be an integer from 0 to 65535")
    return PrivateExecutionServer((LOOPBACK_HOST, port), service or ExecutionService())


def serve(*, port: int = DEFAULT_PORT) -> NoReturn:
    """Run the explicit private process entry point on loopback only."""

    server = create_http_server(port=port)
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        server.server_close()
    raise SystemExit(0)
