#!/usr/bin/env python3
"""Fixed-target Cloud Run authentication proxy for an approved private access VM.

No token or forward-proxy endpoint is exposed. The production command only uses
the VM metadata identity; test connection/token factories are not CLI options.
"""
from __future__ import annotations

import argparse
import base64
import http.client
import json
import re
import ssl
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, urlsplit

MAX_BODY = 1_048_576
MAX_RESPONSE = 16_777_216
MAX_EXPORT = 268_435_456  # The admitted public exporter limits each file to 256 MiB.
HOP_HEADERS = frozenset({"connection", "keep-alive", "proxy-authenticate",
    "proxy-authorization", "te", "trailer", "transfer-encoding", "upgrade"})
UNTRUSTED_IDENTITY = frozenset({"x-gis-invocation-proof", "x-serverless-authorization",
    "x-goog-iap-jwt-assertion", "x-user-email", "x-user-id", "x-role", "x-roles",
    "x-authenticated-user", "forwarded"})


def validate_upstream(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.username is not None or parsed.password is not None
        or parsed.port is not None or parsed.path not in ("", "/") or parsed.query or parsed.fragment
        or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*\.run\.app", parsed.hostname or "")
        or ".." in (parsed.hostname or "")):
        raise ValueError("upstream-must-be-one-canonical-https-cloud-run-origin")
    return "https://" + parsed.hostname


def validate_origin(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.port is None
        or parsed.username is not None or parsed.password is not None or parsed.path or parsed.query
        or parsed.fragment or value != f"http://127.0.0.1:{parsed.port}"):
        raise ValueError("client-origin-must-be-an-exact-ipv4-loopback-origin")
    return value


def validate_response_headers(headers):
    result = []
    for key, value in headers:
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("upstream-response-header-invalid")
        clean_key = key.replace("\r", "").replace("\n", "")
        clean_value = value.replace("\r", "").replace("\n", "")
        if (clean_key != key or clean_value != value
            or not re.fullmatch(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+", clean_key)
            or re.search(r"[\x00-\x08\x0b-\x1f\x7f]", clean_value)):
            raise ValueError("upstream-response-header-invalid")
        # send_header encodes Latin-1. Check before any status/header enters its
        # buffer so a later encoding failure cannot append 502 to a buffered 200.
        clean_value.encode("latin-1")
        result.append((clean_key, clean_value))
    return result


class MetadataIdentity:
    def __init__(self, audience: str):
        self.audience = validate_upstream(audience)
        self.token = ""
        self.refresh_at = 0.0
        self.lock = threading.Lock()

    def __call__(self) -> str:
        with self.lock:
            if self.token and time.time() < self.refresh_at:
                return self.token
            connection = http.client.HTTPConnection("metadata.google.internal", timeout=5)
            try:
                connection.request("GET", "/computeMetadata/v1/instance/service-accounts/default/identity?"
                    + "audience=" + quote(self.audience, safe="") + "&format=full",
                    headers={"Metadata-Flavor": "Google"})
                response = connection.getresponse()
                material = response.read(65_537)
                if response.status != 200 or response.getheader("Metadata-Flavor") != "Google" or len(material) > 65_536:
                    raise RuntimeError("metadata-identity-unavailable")
                token = material.decode("ascii")
                if not re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", token):
                    raise RuntimeError("metadata-identity-invalid")
                # Used only to refresh a trusted metadata response. The application
                # separately verifies the complete signature, issuer and audience.
                payload = token.split(".")[1]
                claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
                expiry = claims.get("exp")
                if not isinstance(expiry, int) or expiry <= time.time() + 60 or claims.get("aud") != self.audience:
                    raise RuntimeError("metadata-identity-invalid")
                self.token, self.refresh_at = token, min(expiry - 60, time.time() + 300)
                return token
            finally:
                connection.close()


class BoundedServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, address, handler):
        self.slots = threading.BoundedSemaphore(16)
        super().__init__(address, handler)

    def get_request(self):
        sock, address = super().get_request()
        sock.settimeout(60)
        return sock, address

    def process_request(self, request, address):
        if not self.slots.acquire(blocking=False):
            try:
                request.sendall(b"HTTP/1.1 503 Service Unavailable\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.slots.release()

    def handle_error(self, request, client_address):
        # Never print request headers, upstream token or response body.
        print('{"event":"private-proxy-request-error"}', flush=True)


def create_server(upstream: str, allowed_origin: str, port: int = 8081,
                  token_provider=None, connection_factory=None) -> BoundedServer:
    upstream = validate_upstream(upstream)
    allowed_origin = validate_origin(allowed_origin)
    host = urlsplit(upstream).hostname
    client_host = urlsplit(allowed_origin).netloc
    identity = token_provider if token_provider is not None else MetadataIdentity(upstream)
    tls = ssl.create_default_context()
    connect = connection_factory if connection_factory is not None else (
        lambda: http.client.HTTPSConnection(host, timeout=120, context=tls))

    class Proxy(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "GISPrivateAccess/1"
        sys_version = ""

        def log_message(self, format, *args):
            pass

        def reject(self, status):
            self.send_response(status)
            self.send_header("Content-Length", "0")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True

        def relay(self):
            self.close_connection = True
            raw_target = self.requestline.split(" ")[1]
            parsed = urlsplit(self.path)
            if (parsed.scheme or parsed.netloc or not self.path.startswith("/") or raw_target.startswith("//")
                or "\\" in self.path or any(ord(c) < 32 for c in self.path)
                or len(self.path) > 8192):
                return self.reject(400)
            if len(self.headers.get_all("Host", [])) != 1 or self.headers.get("Host") != client_host:
                return self.reject(403)
            if (self.headers.get("Origin") is not None and self.headers["Origin"] != allowed_origin):
                return self.reject(403)
            for key in self.headers:
                lower = key.lower()
                if lower in UNTRUSTED_IDENTITY or lower.startswith("x-forwarded-"):
                    return self.reject(400)
            if self.headers.get("Transfer-Encoding") is not None:
                return self.reject(400)
            lengths = self.headers.get_all("Content-Length", [])
            if len(lengths) > 1 or len(self.headers.get_all("Authorization", [])) > 1:
                return self.reject(400)
            if lengths and not re.fullmatch(r"[0-9]{1,8}", lengths[0]):
                return self.reject(400)
            length = int(lengths[0]) if lengths else 0
            if length > MAX_BODY:
                return self.reject(413)
            if self.command == "POST" and not lengths:
                return self.reject(411)
            body = self.rfile.read(length) if length else None
            if body is not None and len(body) != length:
                return self.reject(400)
            headers = {key: value for key, value in self.headers.items()
                if key.lower() not in HOP_HEADERS | {"host", "content-length"}}
            response_started = False
            try:
                token = identity()
                headers.update({"Host": host, "X-Serverless-Authorization": "Bearer " + token,
                    "X-Gis-Invocation-Proof": token})
                connection = connect()
                try:
                    connection.request(self.command, self.path, body=body, headers=headers)
                    response = connection.getresponse()
                    # Validate the complete list, including filtered fields,
                    # before buffering a response. Preserve repeated Set-Cookie.
                    response_headers = validate_response_headers(response.getheaders())
                    response_length = response.getheader("Content-Length")
                    # The full OKF+ JSON/JSON-LD exports exceed the ordinary API
                    # limit. Only a bounded, manifest-hashed file from the fixed
                    # authenticated TLS upstream receives the larger streaming
                    # allowance. The application still enforces the export grant.
                    export = (self.command in ("GET", "HEAD") and response.status == 200
                        and re.fullmatch(r"/exports/bundles/(?:okf|okf-plus|okf-plus-context)/[A-Za-z0-9/_.-]+", self.path)
                        and re.fullmatch(r"[0-9a-f]{64}", response.getheader("X-Gis-Content-Sha256") or "")
                        and response_length is not None)
                    response_limit = MAX_EXPORT if export else MAX_RESPONSE
                    if response_length is not None and (not response_length.isdigit() or int(response_length) > response_limit):
                        return self.reject(502)
                    self.send_response(response.status)
                    for key, value in response_headers:
                        if key.lower() not in HOP_HEADERS | {"content-length", "server", "date"}:
                            self.send_header(key, value)
                    self.send_header("Connection", "close")
                    self.end_headers()
                    response_started = True
                    total = 0
                    while self.command != "HEAD":
                        data = response.read1(16_384)
                        if not data:
                            break
                        total += len(data)
                        if total > response_limit:
                            break
                        self.wfile.write(data)
                        self.wfile.flush()
                finally:
                    connection.close()
            except (OSError, RuntimeError, ValueError, http.client.HTTPException):
                # The client reconciles any uncertain query through its durable key.
                if not response_started and not self.wfile.closed:
                    try:
                        self.reject(502)
                    except OSError:
                        pass

        do_GET = relay
        do_HEAD = relay
        do_POST = relay
        do_DELETE = relay

    return BoundedServer(("127.0.0.1", port), Proxy)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", required=True)
    parser.add_argument("--allowed-origin", default="http://127.0.0.1:8789")
    parser.add_argument("--port", type=int, default=8081)
    parser.add_argument("--check-config", action="store_true")
    options = parser.parse_args()
    validate_upstream(options.upstream)
    validate_origin(options.allowed_origin)
    if not 1024 <= options.port <= 65535:
        parser.error("port must be an unprivileged local port")
    if options.check_config:
        print('{"status":"valid","listen_host":"127.0.0.1"}')
        return
    server = create_server(options.upstream, options.allowed_origin, options.port)
    print('{"event":"private-proxy-started","listen_host":"127.0.0.1"}', flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
