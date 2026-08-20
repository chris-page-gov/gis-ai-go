import assert from "node:assert/strict";
import { request as nodeRequest } from "node:http";
import test from "node:test";

import type { CatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createGatewayNodeServer } from "../src/http-server.js";

const snapshot = {
  bundle: { records: [] },
  recordsById: new Map(),
  version: "0.1.0",
  revision: "a".repeat(40),
  contentRootSha256: "b".repeat(64),
  manifestSha256: "c".repeat(64),
  recordCount: 36,
  stale: false,
  warnings: Object.freeze([]),
  root: "/verified/catalogue",
} as unknown as CatalogueSnapshot;

interface ReceivedResponse {
  readonly status: number;
  readonly headers: Readonly<Record<string, string | string[] | undefined>>;
  readonly body: string;
}

test("the bounded Node adapter serves health and rejects request bodies", async () => {
  const server = createGatewayNodeServer(snapshot);
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve());
  });
  const address = server.address();
  assert.ok(address !== null && typeof address === "object");

  const send = (
    method: string,
    body?: string,
    path = "/healthz",
  ): Promise<ReceivedResponse> =>
    new Promise((resolve, reject) => {
      const request = nodeRequest(
        {
          hostname: "127.0.0.1",
          port: address.port,
          path,
          method,
          headers: {
            accept: "application/json",
            host: "127.0.0.1:8787",
            ...(body === undefined ? {} : { "content-length": Buffer.byteLength(body) }),
          },
        },
        (response) => {
          const chunks: Buffer[] = [];
          response.on("data", (chunk: Buffer) => chunks.push(chunk));
          response.on("end", () => {
            resolve({
              status: response.statusCode ?? 0,
              headers: response.headers,
              body: Buffer.concat(chunks).toString("utf8"),
            });
          });
        },
      );
      request.once("error", reject);
      request.end(body);
    });

  try {
    const health = await send("GET");
    assert.equal(health.status, 200);
    assert.equal(health.headers["cache-control"], "no-store");
    assert.equal(JSON.parse(health.body).lifecycle, "candidate-blocked");

    const bodyRejected = await send("POST", "{}");
    assert.equal(bodyRejected.status, 400);
    assert.equal(bodyRejected.body, "");

    const absoluteTargetRejected = await send(
      "GET",
      undefined,
      "http://attacker.invalid/healthz",
    );
    assert.equal(absoluteTargetRejected.status, 400);

    const nonCanonicalPath = await send("GET", undefined, "/%41");
    assert.equal(nonCanonicalPath.status, 400);
    assert.equal(
      nonCanonicalPath.headers["content-type"],
      "application/problem+json; charset=utf-8",
    );
    assert.equal(JSON.parse(nonCanonicalPath.body).code, "invalid_request");
  } finally {
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error === undefined ? resolve() : reject(error));
    });
  }
});
