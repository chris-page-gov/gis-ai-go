from __future__ import annotations

import http.client
import json
import sys
import threading
import unittest
from pathlib import Path
from typing import Any

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from gis_ai_go_execution import (  # noqa: E402
    ExecutionService,
    canonical_json_bytes,
    create_http_server,
)

from fixtures import FIXED_NOW, expected_result, valid_request  # noqa: E402


class PrivateHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_http_server(
            port=0,
            service=ExecutionService(clock=lambda: FIXED_NOW),
        )
        self.port = self.server.server_address[1]
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=2)

    def request(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, Any], http.client.HTTPResponse]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        request_headers = dict(headers or {})
        if body is not None:
            request_headers.setdefault("Content-Type", "application/json")
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        payload = response.read()
        value = json.loads(payload) if payload else {}
        connection.close()
        return response.status, value, response

    def test_private_health_readiness_and_openapi_are_complete(self) -> None:
        health_status, health, _ = self.request("GET", "/internal/health")
        ready_status, ready, _ = self.request("GET", "/internal/readiness")
        openapi_status, openapi, _ = self.request("GET", "/internal/openapi.json")
        self.assertEqual(200, health_status)
        self.assertEqual(200, ready_status)
        self.assertEqual(200, openapi_status)
        self.assertTrue(health["private"])
        self.assertFalse(health["live_provider_calls"])
        self.assertEqual("ready", ready["status"])
        self.assertEqual("3.1.0", openapi["openapi"])
        self.assertEqual(
            {
                "/internal/health",
                "/internal/readiness",
                "/internal/openapi.json",
                "/internal/v1/execute",
                "/internal/v1/executions/{request_id}",
            },
            set(openapi["paths"]),
        )
        self.assertNotIn("securitySchemes", openapi["components"])
        expected_schema_ids = {
            "ExecutionRequest": "urn:gis-ai-go:schema:execution-request:1",
            "ExecutionResult": "urn:gis-ai-go:schema:execution-result:1",
            "ExecutionProblem": "urn:gis-ai-go:schema:execution-problem:1",
        }
        for component, schema_id in expected_schema_ids.items():
            schema = openapi["components"]["schemas"][component]
            self.assertEqual(schema_id, schema["x-canonical-schema-id"])
            self.assertNotIn("$id", schema)
        self.assertEqual(
            "#/components/schemas/Health",
            openapi["paths"]["/internal/health"]["get"]["responses"]["200"]
            ["content"]["application/json"]["schema"]["$ref"],
        )
        self.assertEqual(
            "#/components/schemas/Readiness",
            openapi["paths"]["/internal/readiness"]["get"]["responses"]["200"]
            ["content"]["application/json"]["schema"]["$ref"],
        )
        for reference in self._references(openapi):
            self.assertTrue(reference.startswith("#/"), reference)
            self._resolve_pointer(openapi, reference)

    def test_private_post_returns_the_canonical_fixture_result(self) -> None:
        status, result, response = self.request(
            "POST",
            "/internal/v1/execute",
            canonical_json_bytes(valid_request()),
        )
        self.assertEqual(200, status)
        self.assertEqual(expected_result(), result)
        self.assertEqual("no-store", response.getheader("Cache-Control"))
        self.assertEqual("nosniff", response.getheader("X-Content-Type-Options"))

    def test_host_content_encoding_compressed_size_and_json_are_fail_closed(self) -> None:
        cases = (
            ({"Host": "example.com", "Content-Type": "application/json"}, b"{}", 400),
            ({"Content-Encoding": "gzip", "Content-Type": "application/json"}, b"{}", 400),
            ({"Content-Type": "text/plain"}, b"{}", 400),
            ({"Content-Type": "application/json"}, b'{"a":1,"a":2}', 400),
            ({"Content-Type": "application/json"}, b"{" + b"a" * 65_536 + b"}", 413),
        )
        for headers, body, expected_status in cases:
            with self.subTest(headers=headers, size=len(body)):
                status, problem, _ = self.request(
                    "POST", "/internal/v1/execute", body, headers
                )
                self.assertEqual(expected_status, status)
                self.assertIn(problem["code"], {"INVALID_REQUEST", "LIMIT_EXCEEDED"})
                self.assertNotIn("Traceback", canonical_json_bytes(problem).decode())

    def test_unknown_routes_methods_and_cancellation_are_bounded_json(self) -> None:
        missing_status, missing, _ = self.request("GET", "/tmp/private")
        method_status, method, method_response = self.request("PUT", "/internal/health")
        cancel_status, cancel, _ = self.request(
            "DELETE", "/internal/v1/executions/exec-202-example"
        )
        self.assertEqual((404, "NOT_FOUND"), (missing_status, missing["code"]))
        self.assertEqual((405, "METHOD_NOT_ALLOWED"), (method_status, method["code"]))
        self.assertEqual("GET, POST, DELETE", method_response.getheader("Allow"))
        self.assertEqual(200, cancel_status)
        self.assertEqual("not-active", cancel["status"])

    def test_http_cancellation_interrupts_the_active_private_request(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=2)
        started = threading.Event()
        resume = threading.Event()

        def pause(_request_id: str, index: int) -> None:
            if index == 0:
                started.set()
                self.assertTrue(resume.wait(timeout=2))

        self.server = create_http_server(
            port=0,
            service=ExecutionService(clock=lambda: FIXED_NOW, checkpoint=pause),
        )
        self.port = self.server.server_address[1]
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        execution_response: list[tuple[int, dict[str, Any], http.client.HTTPResponse]] = []

        def execute() -> None:
            execution_response.append(
                self.request(
                    "POST",
                    "/internal/v1/execute",
                    canonical_json_bytes(valid_request()),
                )
            )

        execution = threading.Thread(target=execute)
        execution.start()
        self.assertTrue(started.wait(timeout=2))
        cancel_status, cancel, _ = self.request(
            "DELETE", "/internal/v1/executions/exec-202-example"
        )
        resume.set()
        execution.join(timeout=2)
        self.assertEqual((200, "accepted"), (cancel_status, cancel["status"]))
        self.assertEqual(409, execution_response[0][0])
        self.assertEqual("EXECUTION_CANCELLED", execution_response[0][1]["code"])

    def test_ninth_concurrent_request_is_rejected_before_another_handler_thread(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=2)
        lock = threading.Lock()
        started = 0
        all_started = threading.Event()
        resume = threading.Event()

        def pause(_request_id: str, index: int) -> None:
            nonlocal started
            if index != 0:
                return
            with lock:
                started += 1
                if started == 8:
                    all_started.set()
            self.assertTrue(resume.wait(timeout=3))

        self.server = create_http_server(
            port=0,
            service=ExecutionService(clock=lambda: FIXED_NOW, checkpoint=pause),
        )
        self.port = self.server.server_address[1]
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        responses: list[tuple[int, dict[str, Any], http.client.HTTPResponse]] = []

        def execute(index: int) -> None:
            request = valid_request()
            request["request_id"] = f"exec-202-concurrent-{index}"
            responses.append(
                self.request(
                    "POST",
                    "/internal/v1/execute",
                    canonical_json_bytes(request),
                )
            )

        executions = [threading.Thread(target=execute, args=(index,)) for index in range(8)]
        for execution in executions:
            execution.start()
        self.assertTrue(all_started.wait(timeout=3))

        overflow = valid_request()
        overflow["request_id"] = "exec-202-concurrent-overflow"
        status, problem, response = self.request(
            "POST",
            "/internal/v1/execute",
            canonical_json_bytes(overflow),
        )
        self.assertEqual((429, "CAPACITY_EXCEEDED"), (status, problem["code"]))
        self.assertEqual("1", response.getheader("Retry-After"))

        resume.set()
        for execution in executions:
            execution.join(timeout=3)
            self.assertFalse(execution.is_alive())
        self.assertEqual([200] * 8, sorted(item[0] for item in responses))

    def test_unexpected_runtime_error_is_normalised_without_stack_or_path(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=2)

        def fail(_request_id: str, _index: int) -> None:
            raise RuntimeError("/tmp/secret provider failed SELECT * FROM credentials")

        self.server = create_http_server(
            port=0,
            service=ExecutionService(clock=lambda: FIXED_NOW, checkpoint=fail),
        )
        self.port = self.server.server_address[1]
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        status, problem, _ = self.request(
            "POST",
            "/internal/v1/execute",
            canonical_json_bytes(valid_request()),
        )
        encoded = canonical_json_bytes(problem).decode()
        self.assertEqual((500, "INTERNAL_ERROR"), (status, problem["code"]))
        for forbidden in ("/tmp/secret", "SELECT", "credentials", "Traceback"):
            self.assertNotIn(forbidden, encoded)

    @staticmethod
    def _references(value: object) -> list[str]:
        references: list[str] = []
        if isinstance(value, dict):
            for key, nested in value.items():
                if key == "$ref" and isinstance(nested, str):
                    references.append(nested)
                else:
                    references.extend(PrivateHttpTests._references(nested))
        elif isinstance(value, list):
            for nested in value:
                references.extend(PrivateHttpTests._references(nested))
        return references

    @staticmethod
    def _resolve_pointer(document: object, pointer: str) -> object:
        current = document
        for token in pointer[2:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if not isinstance(current, dict):
                raise AssertionError(f"Unresolved OpenAPI reference: {pointer}")
            current = current[token]
        return current


if __name__ == "__main__":
    unittest.main()
