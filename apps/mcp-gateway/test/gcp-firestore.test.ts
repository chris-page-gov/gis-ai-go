import assert from "node:assert/strict";
import test from "node:test";
import { createGcpFirestoreRestStore, createGcpMetadataAccessToken } from "../src/gcp-firestore.js";
const CONFIG = { projectId: "synthetic-project", databaseId: "(default)", collection: "gis_evidence" };
const ID = "a".repeat(64);
const ROOT = "projects/synthetic-project/databases/(default)";

test("Firestore REST sends IAM bearer, strong document read and all-or-none updateTime precondition", async () => {
  const requests: { url: string; init: RequestInit | undefined }[] = [];
  const fetcher: typeof fetch = async (input, init) => {
    requests.push({ url: String(input), init });
    if (init?.method === "POST") return new Response(JSON.stringify({ writeResults: [{ updateTime: "2026-10-05T12:00:01Z" }], commitTime: "2026-10-05T12:00:01Z" }));
    return new Response(JSON.stringify({ name: `${ROOT}/documents/gis_evidence/${ID}`, updateTime: "2026-10-05T12:00:00Z", fields: { snapshot_json: { stringValue: "synthetic snapshot" } } }));
  };
  const store = createGcpFirestoreRestStore(CONFIG, { fetch: fetcher, accessToken: async () => "synthetic-access-not-a-real-credential" });
  const read = await store.read(ID); assert.equal(read!.version, "2026-10-05T12:00:00Z");
  assert.equal(requests[0]!.url, `https://firestore.googleapis.com/v1/${ROOT}/documents/gis_evidence/${ID}`);
  assert.equal(await store.compareAndSet(ID, read!.version, { snapshot_json: "next" }), true);
  const request = requests[1]!;
  assert.equal(request.init!.redirect, "error");
  assert.equal(new Headers(request.init!.headers).get("authorization"), "Bearer synthetic-access-not-a-real-credential");
  const body = JSON.parse(request.init!.body as string);
  assert.equal(body.writes.length, 1); assert.deepEqual(body.writes[0].currentDocument, { updateTime: read!.version });
  assert.deepEqual(body.writes[0].update.fields.snapshot_json, { stringValue: "next" });
});

test("Firestore absence/known CAS failures are distinguished from permission/outcome failures; oversize stops before network", async () => {
  let status = 404; let errorStatus = "NOT_FOUND"; let calls = 0;
  const store = createGcpFirestoreRestStore(CONFIG, { accessToken: async () => "synthetic", fetch: async () => {
    calls += 1; return new Response(JSON.stringify({ error: { status: errorStatus } }), { status });
  } });
  assert.equal(await store.read(ID), null);
  for (const tuple of [[400, "FAILED_PRECONDITION"], [409, "ALREADY_EXISTS"], [409, "ABORTED"], [412, "FAILED_PRECONDITION"]] as const) {
    [status, errorStatus] = tuple; assert.equal(await store.compareAndSet(ID, null, { field: "synthetic" }), false);
  }
  status = 403; errorStatus = "PERMISSION_DENIED";
  await assert.rejects(store.compareAndSet(ID, null, { field: "synthetic" }), /uncertain/u);
  const before = calls; await assert.rejects(store.compareAndSet(ID, null, { snapshot_json: "x".repeat(900_001) }), /capacity/u); assert.equal(calls, before);
  await assert.rejects(store.read("../other"), /scope/u);
});

test("short-lived metadata credentials use fixed endpoint, header, verified metadata response and bounded refresh", async () => {
  let clock = 0; let calls = 0;
  const credential = createGcpMetadataAccessToken({ now: () => clock, fetch: async (input, init) => {
    calls += 1; assert.equal(String(input), "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token");
    assert.equal(new Headers(init?.headers).get("metadata-flavor"), "Google"); assert.equal(init?.redirect, "error");
    return new Response(JSON.stringify({ access_token: "test", token_type: "Bearer", expires_in: 3_600 }), { headers: { "metadata-flavor": "Google" } });
  } });
  await credential(); await credential(); assert.equal(calls, 1); clock = 3_571_000; await credential(); assert.equal(calls, 2);
  const invalid = createGcpMetadataAccessToken({ fetch: async () => new Response('{}') }); await assert.rejects(invalid(), /credentials/u);
});
