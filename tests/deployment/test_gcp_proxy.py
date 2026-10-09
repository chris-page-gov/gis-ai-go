"""Socket tests of the private access proxy; no GCP access or real credentials."""
import http.client
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import threading
import time
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("gcp_access_proxy", ROOT / "scripts/gcp/access_proxy.py")
PROXY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROXY)


class PrivateProxyTests(unittest.TestCase):
    def setUp(self):
        self.observed = []
        self.response_headers = None
        self.override_connection = None
        observed = self.observed
        fixture = self

        class Upstream(PROXY.BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                observed.append((self.path, dict(self.headers), body))
                result = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"ok": True}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(result)))
                self.end_headers()
                self.wfile.write(result)

            def do_GET(self):
                observed.append((self.path, dict(self.headers), b""))
                if fixture.response_headers is not None:
                    self.wfile.write(b"HTTP/1.1 200 OK\r\n" + fixture.response_headers
                        + b"\r\nContent-Length: 20\r\nConnection: close\r\n\r\nupstream-body-marker")
                    self.close_connection = True
                    return
                if self.path == "/exports/bundles/okf-plus/okf-bundle.json":
                    chunk = b"x" * 16_384
                    repeats = 17 * 1024 * 1024 // len(chunk)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(repeats * len(chunk)))
                    self.send_header("X-Gis-Content-Sha256", hashlib.sha256(chunk * repeats).hexdigest())
                    self.end_headers()
                    for _ in range(repeats):
                        self.wfile.write(chunk)
                    return
                if self.path in ("/oversized-api", "/exports/bundles/okf-plus/unhashed.json", "/exports/bundles/okf-plus/too-large.json"):
                    self.send_response(200)
                    self.send_header("Content-Length", str(PROXY.MAX_EXPORT + 1 if self.path.endswith("too-large.json") else PROXY.MAX_RESPONSE + 1))
                    if self.path.endswith("too-large.json"):
                        self.send_header("X-Gis-Content-Sha256", "a" * 64)
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                self.wfile.write(b"data: first\n\n")
                self.wfile.flush()
                time.sleep(0.15)
                self.wfile.write(b"data: second\n\n")

            def log_message(self, *args):
                pass

        self.upstream = PROXY.ThreadingHTTPServer(("127.0.0.1", 0), Upstream)
        self.proxy = PROXY.create_server("https://pilot.example.run.app", "http://127.0.0.1:8789", 0,
            token_provider=lambda: "synthetic-google-transport-token",
            connection_factory=lambda: self.override_connection or http.client.HTTPConnection(*self.upstream.server_address, timeout=2))
        self.threads = [threading.Thread(target=s.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
            for s in [self.upstream, self.proxy]]
        for thread in self.threads:
            thread.start()
        self.addCleanup(self.cleanup_servers)

    def cleanup_servers(self):
        for server in [self.proxy, self.upstream]:
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(timeout=2)

    def exchange(self, path="/mcp", method="POST", headers=None, body=b"{}"):
        connection = http.client.HTTPConnection(*self.proxy.server_address, timeout=3)
        connection.request(method, path, body=body,
            headers={"Host": "127.0.0.1:8789", "Origin": "http://127.0.0.1:8789", **(headers or {})})
        response = connection.getresponse()
        result = response.status, response.read()
        connection.close()
        return result

    def wire_exchange(self):
        with socket.create_connection(self.proxy.server_address, timeout=3) as connection:
            connection.sendall(b"GET /mcp HTTP/1.1\r\nHost: 127.0.0.1:8789\r\nConnection: close\r\n\r\n")
            chunks = []
            while chunk := connection.recv(16_384):
                chunks.append(chunk)
        return b"".join(chunks)

    def assert_empty_gateway_error(self, wire):
        headers, body = wire.split(b"\r\n\r\n", 1)
        self.assertTrue(headers.startswith(b"HTTP/1.1 502 "), wire)
        self.assertEqual(wire.count(b"HTTP/1.1 "), 1, wire)
        self.assertIn(b"Content-Length: 0\r\n", headers + b"\r\n")
        self.assertIn(b"Connection: close\r\n", headers + b"\r\n")
        self.assertNotIn(b"upstream-marker", wire)
        self.assertEqual(body, b"")

    def test_parser_reachable_invalid_response_values_fail_before_status(self):
        for value in (b"upstream-marker\r\n folded", b"upstream-marker\r\n\tfolded",
                      b"upstream-marker\x00suffix", b"upstream-marker\x7fsuffix"):
            with self.subTest(value=value):
                self.response_headers = b"X-Safe: upstream-marker\r\nX-Invalid: " + value
                self.assert_empty_gateway_error(self.wire_exchange())

    def test_invalid_response_headers_fail_before_any_upstream_output(self):
        invalid_headers = [("X-Invalid", value) for value in
            ("upstream-marker\rinjected", "upstream-marker\ninjected", "\x01", "\x0b", "\x1f", "\x7f", "\u0100")]
        invalid_headers += [(name, "upstream-marker") for name in
            ("", "X:Invalid", "X Invalid", "X\tInvalid", "X\rInvalid", "X\nInvalid", "X-\u00e9")]
        # Even fields that would be filtered need validation before the status
        # and previous valid fields can enter BaseHTTPRequestHandler's buffer.
        invalid_headers += [("Server", "upstream-marker\r\ninjected")]
        for header in invalid_headers:
            with self.subTest(header=header):
                response = Mock(status=200)
                response.getheaders.return_value = [("X-Safe", "upstream-marker"), header]
                response.getheader.return_value = None
                upstream = Mock()
                upstream.getresponse.return_value = response
                # Replace only the injected test factory; production has no CLI
                # option for an alternate origin, header source or identity.
                self.override_connection = upstream
                self.assert_empty_gateway_error(self.wire_exchange())
                upstream.close.assert_called_once()
                response.read1.assert_not_called()

    def test_repeated_cookies_and_valid_field_values_remain_independent(self):
        self.response_headers = (b"Set-Cookie: session=synthetic; HttpOnly; SameSite=Lax\r\n"
            b"Set-Cookie: flow=; Max-Age=0; HttpOnly\r\nX-Ordinary: space\ttab\xe9")
        wire = self.wire_exchange()
        headers, body = wire.split(b"\r\n\r\n", 1)
        self.assertTrue(headers.startswith(b"HTTP/1.1 200 "), wire)
        self.assertEqual([line for line in headers.split(b"\r\n") if line.startswith(b"Set-Cookie:")],
            [b"Set-Cookie: session=synthetic; HttpOnly; SameSite=Lax",
             b"Set-Cookie: flow=; Max-Age=0; HttpOnly"])
        self.assertIn(b"X-Ordinary: space\ttab\xe9\r\n", headers + b"\r\n")
        self.assertEqual(body, b"upstream-body-marker")

    def test_separates_application_bearer_from_google_invocation_proof(self):
        status, material = self.exchange(headers={"Authorization": "Bearer synthetic-okta-token"})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(material)["result"]["ok"])
        path, headers, body = self.observed[0]
        self.assertEqual(path, "/mcp")
        self.assertEqual(headers["Host"], "pilot.example.run.app")
        self.assertEqual(headers["Authorization"], "Bearer synthetic-okta-token")
        self.assertEqual(headers["X-Serverless-Authorization"], "Bearer synthetic-google-transport-token")
        self.assertEqual(headers["X-Gis-Invocation-Proof"], "synthetic-google-transport-token")
        self.assertEqual(body, b"{}")
        self.assertEqual(self.proxy.server_address[0], "127.0.0.1")

    def test_rejects_spoofed_identity_and_forwarding_headers(self):
        for name in ["X-Gis-Invocation-Proof", "X-Serverless-Authorization", "X-Role",
                     "X-User-Email", "X-Forwarded-Host", "Forwarded"]:
            with self.subTest(name=name):
                self.assertEqual(self.exchange(headers={name: "spoofed"})[0], 400)
        self.assertEqual(self.observed, [])

    def test_rejects_dns_rebinding_cross_origin_and_absolute_proxy_targets(self):
        self.assertEqual(self.exchange(headers={"Host": "attacker.example"})[0], 403)
        self.assertEqual(self.exchange(headers={"Origin": "https://attacker.example"})[0], 403)
        self.assertEqual(self.exchange(path="https://attacker.example/")[0], 400)
        self.assertEqual(self.exchange(path="//attacker.example/")[0], 400)
        self.assertEqual(self.observed, [])

    def test_bounds_requests_and_rejects_transfer_encoding(self):
        self.assertEqual(self.exchange(headers={"Transfer-Encoding": "chunked"})[0], 400)
        self.assertEqual(self.exchange(headers={"Content-Length": str(PROXY.MAX_BODY + 1)})[0], 413)
        self.assertEqual(self.observed, [])

    def test_streams_without_buffering_whole_response(self):
        connection = http.client.HTTPConnection(*self.proxy.server_address, timeout=3)
        connection.request("GET", "/mcp", headers={"Host": "127.0.0.1:8789"})
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader("Content-Type"), "text/event-stream")
        first = response.read1(13)
        self.assertEqual(first, b"data: first\n\n")
        self.assertEqual(response.read(), b"data: second\n\n")
        connection.close()

    def test_upstream_failure_has_no_token_or_private_diagnostics(self):
        self.proxy.shutdown()
        self.proxy.server_close()
        self.proxy = PROXY.create_server("https://pilot.example.run.app", "http://127.0.0.1:8789", 0,
            token_provider=lambda: (_ for _ in ()).throw(RuntimeError("secret-token-value")))
        thread = threading.Thread(target=self.proxy.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self.threads.append(thread)
        thread.start()
        status, body = self.exchange()
        self.assertEqual(status, 502)
        self.assertEqual(body, b"")

    def test_manifest_hashed_public_exports_stream_beyond_the_api_limit(self):
        status, material = self.exchange(path="/exports/bundles/okf-plus/okf-bundle.json", method="GET", body=None)
        self.assertEqual(status, 200)
        self.assertEqual(len(material), 17 * 1024 * 1024)
        self.assertEqual(hashlib.sha256(material).digest(), hashlib.sha256(b"x" * len(material)).digest())
        for path in ("/oversized-api", "/exports/bundles/okf-plus/unhashed.json", "/exports/bundles/okf-plus/too-large.json"):
            with self.subTest(path=path):
                self.assertEqual(self.exchange(path=path, method="GET", body=None), (502, b""))

    def test_only_canonical_run_upstream_and_loopback_client_origin_are_accepted(self):
        for target in ["http://pilot.run.app", "https://x.run.app/other", "https://a@x.run.app",
                       "https://x.run.app:443", "https://x.run.app.evil", "https://x.run.app?q=1"]:
            with self.subTest(target=target), self.assertRaises(ValueError):
                PROXY.validate_upstream(target)
        for origin in ["http://localhost:8789", "http://0.0.0.0:8789", "https://127.0.0.1:8789",
                       "http://127.0.0.1:8789/"]:
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                PROXY.validate_origin(origin)


if __name__ == "__main__":
    unittest.main()
