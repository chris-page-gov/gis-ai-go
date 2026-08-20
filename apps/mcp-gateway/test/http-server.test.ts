import assert from "node:assert/strict";
import { request as nodeRequest } from "node:http";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createGatewayNodeServer } from "../src/http-server.js";

const snapshot = await loadCatalogueSnapshot(
  fileURLToPath(new URL("../../../../artifacts/okf/", import.meta.url)),
  { now: new Date("2026-08-20T12:00:00Z") },
);

interface ReceivedResponse {
  readonly status: number;
  readonly headers: Readonly<Record<string, string | string[] | undefined>>;
  readonly body: string;
}

test("the bounded Node adapter serves health and rejects invalid routes", async () => {
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
    assert.equal(
      bodyRejected.headers["content-type"],
      "application/problem+json; charset=utf-8",
    );
    assert.equal(JSON.parse(bodyRejected.body).code, "invalid_request");

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
