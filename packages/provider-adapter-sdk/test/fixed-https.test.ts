import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { Resolver } from "node:dns/promises";
import { Agent, request as httpRequest } from "node:http";
import { Duplex } from "node:stream";
import test from "node:test";

import {
  FixedHttpsTransportError,
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  assertPublicProviderAddress,
  fixedHttpsGet,
} from "../src/index.js";
import {
  isExactFixedHttpsTransportError,
  normaliseFixedHttpsRequestError,
} from "../src/fixed-https.js";

class ParserProbeSocket extends Duplex {
  readonly #response: string;
  #sent = false;

  constructor(response: string) {
    super();
    this.#response = response;
  }

  override _read(): void {
    if (this.#sent) return;
    this.#sent = true;
    queueMicrotask(() => {
      this.push(Buffer.from(this.#response, "latin1"));
      this.push(null);
    });
  }

  override _write(
    _chunk: Buffer | string,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    callback();
  }
}

async function nodeParserError(response: string): Promise<Error> {
  return await new Promise<Error>((resolve, reject) => {
    const socket = new ParserProbeSocket(response);
    const agent = new Agent();
    agent.createConnection = (() => socket) as typeof agent.createConnection;
    const request = httpRequest(
      {
        hostname: "example.invalid",
        path: "/",
        agent,
        maxHeaderSize: 16_384,
      },
      (incoming) => {
        incoming.resume();
        incoming.once("end", () => reject(new Error("expected an HTTP parser failure")));
      },
    );
    request.once("error", resolve);
    request.end();
  });
}

test("accepts only ordinary public resolver answers", () => {
  assert.doesNotThrow(() => assertPublicProviderAddress("1.1.1.1", 4));
  assert.doesNotThrow(() => assertPublicProviderAddress("8.8.8.8", 4));
  assert.doesNotThrow(() => assertPublicProviderAddress("2606:4700:4700::1111", 6));

  const blocked: readonly [string, number][] = [
    ["0.0.0.0", 4],
    ["10.0.0.1", 4],
    ["100.64.0.1", 4],
    ["127.0.0.1", 4],
    ["169.254.169.254", 4],
    ["172.16.0.1", 4],
    ["192.168.1.1", 4],
    ["198.18.0.1", 4],
    ["192.0.2.1", 4],
    ["192.88.99.1", 4],
    ["224.0.0.1", 4],
    ["255.255.255.255", 4],
    ["::", 6],
    ["::1", 6],
    ["::ffff:127.0.0.1", 6],
    ["64:ff9b::7f00:1", 6],
    ["2001:30::1", 6],
    ["2001:db8::1", 6],
    ["2620:4f:8000::1", 6],
    ["3fff::1", 6],
    ["5f00::1", 6],
    ["fc00::1", 6],
    ["fe80::1", 6],
    ["ff02::1", 6],
    ["not-an-address", 4],
    ["1.1.1.1", 6],
  ];
  for (const [address, family] of blocked) {
    assert.throws(
      () => assertPublicProviderAddress(address, family),
      (error: unknown) =>
        error instanceof FixedHttpsTransportError && error.kind === "unsafe-address",
    );
  }
});

test("classifies real Node parser and DNS failures at the fixed transport boundary", async (t) => {
  const responses = [
    ["HPE_INVALID_HEADER_TOKEN", "HTTP/1.1 200 OK\r\nBad Header\r\n\r\n"],
    [
      "HPE_HEADER_OVERFLOW",
      `HTTP/1.1 200 OK\r\nX-Large: ${"a".repeat(17_000)}\r\nContent-Length: 0\r\n\r\n`,
    ],
    [
      "HPE_INVALID_CHUNK_SIZE",
      "HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\nZ\r\nx\r\n0\r\n\r\n",
    ],
    [
      "HPE_STRICT",
      "HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n1\r\nxX\r\n0\r\n\r\n",
    ],
  ] as const;
  for (const [expectedCode, response] of responses) {
    const error = await nodeParserError(response);
    assert.equal(Object.getOwnPropertyDescriptor(error, "code")?.value, expectedCode);
    assert.equal(
      normaliseFixedHttpsRequestError(error).kind,
      "invalid-response-framing",
    );
  }

  const moduleUrl = new URL("../src/index.js", import.meta.url).href;
  const probe = spawnSync(
    process.execPath,
    [
      "--input-type=module",
      "-e",
      `
        import https from "node:https";
        import http from "node:http";
        import dns from "node:dns/promises";
        import { syncBuiltinESMExports } from "node:module";
        import { Duplex } from "node:stream";

        class ResponseSocket extends Duplex {
          sent = false;
          authorized = true;
          connecting = false;
          constructor(response) {
            super();
            this.response = response;
            Object.defineProperty(this, "remoteAddress", { value: "93.184.216.34" });
          }
          _read() {
            if (this.sent) return;
            this.sent = true;
            queueMicrotask(() => {
              if (this.response.length > 0) {
                this.push(Buffer.from(this.response, "latin1"));
              }
              this.push(null);
            });
          }
          _write(_chunk, _encoding, callback) { callback(); }
          setTimeout() { return this; }
          setNoDelay() { return this; }
          setKeepAlive() { return this; }
          getProtocol() { return "TLSv1.3"; }
          getCipher() { return { name: "TLS_AES_256_GCM_SHA384" }; }
        }

        dns.Resolver.prototype.resolve4 = async function () { return ["93.184.216.34"]; };
        dns.Resolver.prototype.resolve6 = async function () { throw new Error("no IPv6"); };
        let wireResponse = "";
        https.request = function (options, callback) {
          const socket = new ResponseSocket(wireResponse);
          const agent = new http.Agent();
          agent.createConnection = () => socket;
          const request = http.request({ ...options, protocol: "http:", agent }, callback);
          request.once("socket", () => queueMicrotask(() => socket.emit("secureConnect")));
          return request;
        };
        syncBuiltinESMExports();

        const sdk = await import(${JSON.stringify(moduleUrl)});
        async function classify(response) {
          wireResponse = response;
          const adapter = new sdk.OnsDataApiAdapter({
            lifecycle: {
              discovery: "suspended",
              invocation: "active",
              reason: "Offline response-boundary probe.",
            },
            transport: sdk.fixedHttpsGet,
            sleep: async () => undefined,
          });
          const execution = sdk.executePristineOnsDataApiAdapter(
            adapter,
            sdk.ONS_ADAPTER_REQUEST,
            {},
          );
          try {
            await execution.result;
            throw new Error("expected fixed HTTPS failure");
          } catch (error) {
            const normalised = adapter.normalise_error(error);
            return {
              normalised,
              cacheEligible: execution.approvedCacheOutage(error, normalised),
            };
          }
        }
        const results = {};
        for (const [name, response] of [
          ["bad-header", "HTTP/1.1 200 OK\\r\\nBad Header\\r\\n\\r\\n"],
          ["short-content-length", "HTTP/1.1 200 OK\\r\\nContent-Length: 10\\r\\n\\r\\nabc"],
          ["short-chunked", "HTTP/1.1 200 OK\\r\\nTransfer-Encoding: chunked\\r\\n\\r\\n3\\r\\nabc\\r\\n"],
          ["short-redirect", "HTTP/1.1 302 Found\\r\\nLocation: https://evil.invalid/\\r\\nContent-Length: 10\\r\\n\\r\\nabc"],
          ["pre-response-reset", ""],
        ]) {
          results[name] = await classify(response);
        }
        process.stdout.write(JSON.stringify(results));
      `,
    ],
    { encoding: "utf8", timeout: 5_000 },
  );
  assert.equal(probe.status, 0, probe.stderr);
  const malformed = {
    normalised: {
      code: "MALFORMED_PROVIDER_RESPONSE",
      message: "The provider returned a response that failed validation.",
      providerStatus: null,
      retryable: false,
    },
    cacheEligible: null,
  };
  assert.deepEqual(JSON.parse(probe.stdout), {
    "bad-header": malformed,
    "short-content-length": malformed,
    "short-chunked": malformed,
    "short-redirect": malformed,
    "pre-response-reset": {
      normalised: {
        code: "PROVIDER_OUTAGE",
        message: "The provider is unavailable.",
        providerStatus: null,
        retryable: true,
      },
      cacheEligible: {
        source: "network",
        providerStatus: null,
        retryable: true,
      },
    },
  });

  let ipv4Failure: unknown = Object.assign(new Error("offline DNS failure"), {
    code: "ENOTFOUND",
  });
  let ipv6Failure: unknown = Object.assign(new Error("offline DNS failure"), {
    code: "ENOTFOUND",
  });
  t.mock.method(Resolver.prototype, "resolve4", async () => {
    throw ipv4Failure;
  });
  t.mock.method(Resolver.prototype, "resolve6", async () => {
    throw ipv6Failure;
  });

  const expectKind = async (kind: "network" | "unclassified"): Promise<void> => {
    await assert.rejects(
      () => fixedHttpsGet({ policy: ONS_EGRESS_POLICY, url: ONS_OBSERVATION_URI }),
      (error: unknown) =>
        isExactFixedHttpsTransportError(error) && error.kind === kind,
    );
  };

  await expectKind("network");
  ipv4Failure = Object.assign(new Error("offline DNS failure"), { code: "EAI_AGAIN" });
  ipv6Failure = Object.assign(new Error("offline DNS failure"), { code: "EAI_AGAIN" });
  await expectKind("network");

  let accessorReads = 0;
  const accessorFailure = new Error("opaque DNS failure");
  Object.defineProperty(accessorFailure, "code", {
    get: () => {
      accessorReads += 1;
      return "ENOTFOUND";
    },
  });
  ipv4Failure = Object.assign(new Error("offline DNS failure"), { code: "ENOTFOUND" });
  ipv6Failure = accessorFailure;
  await expectKind("unclassified");
  assert.equal(accessorReads, 0);

  let descriptorTraps = 0;
  const proxyFailure = new Proxy(
    Object.assign(new Error("proxied DNS failure"), { code: "ENOTFOUND" }),
    {
      getOwnPropertyDescriptor: () => {
        descriptorTraps += 1;
        throw new Error("DNS error proxy must not be inspected");
      },
    },
  );
  ipv4Failure = proxyFailure;
  ipv6Failure = proxyFailure;
  await expectKind("unclassified");
  assert.equal(descriptorTraps, 0);
});

test("stops before DNS when the fixed request is already cancelled", async () => {
  const controller = new AbortController();
  controller.abort();
  await assert.rejects(
    () =>
      fixedHttpsGet({
        policy: ONS_EGRESS_POLICY,
        url: ONS_OBSERVATION_URI,
        signal: controller.signal,
      }),
    (error: unknown) =>
      error instanceof FixedHttpsTransportError && error.kind === "aborted",
  );
});
