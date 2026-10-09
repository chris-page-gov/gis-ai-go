"""Socket tests of the private access proxy; no GCP access or real credentials."""
import http.client
import hashlib
import importlib.util
import json
from pathlib import Path
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("gcp_access_proxy", ROOT / "scripts/gcp/access_proxy.py")
PROXY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROXY)


class PrivateProxyTests(unittest.TestCase):
    def setUp(self):
        self.observed = []
        observed = self.observed

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
            connection_factory=lambda: http.client.HTTPConnection(*self.upstream.server_address, timeout=2))
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
