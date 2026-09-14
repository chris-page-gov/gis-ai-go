// Local compatibility fixture only. Never deploy or mount its provisioning routes.
import {
  canonicalJson, createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot,
  WEB216_D1_SCHEMA_SQL, type Web216D1Database,
} from "@gis-ai-go/evidence/web216-pure";
import { createWeb216HostedCpihApplication } from "../apps/mcp-gateway/src/web216-hosted-cpih-application.js";
import { createWeb216HostedCpihMcpHttpHandler } from "../apps/mcp-gateway/src/web216-hosted-cpih-http.js";
import { resolveWeb216CpihSelection } from "../apps/mcp-gateway/src/web216-cpih-selection.js";
import projection from "../tests/fixtures/web216/current-cpih-projection.json";

// Fixed synthetic software/request time; not accepted-build or source-time proof.
const software = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) };
const now = () => new Date("2026-09-14T18:00:00.000Z");
const protocol = "2026-07-28";
const syntheticKey = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const fabricatedParsedBody = {
  jsonrpc: "2.0",
  id: "fabricated-parsed-body",
  method: "tools/call",
  params: {
    name: "web216_cpih_query",
    arguments: {
      period: "2026-01",
      selection_plan_id: resolveWeb216CpihSelection({ period: "2026-01" }).plan_id,
      idempotency_key: syntheticKey,
    },
    _meta: {
      "io.modelcontextprotocol/protocolVersion": protocol,
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        name: "web216-local-worker-probe",
        version: "1.0.0",
      },
    },
  },
} as const;

export default {
  async fetch(request: Request, env: { DB: Web216D1Database }): Promise<Response> {
    try {
      const url = new URL(request.url);
      if (url.origin !== "http://localhost" || url.search !== "") return new Response("Not found", { status: 404 });
      const initialSnapshot = createWeb216TransactionalSnapshot({ projection, software,
        createdAt: now().toISOString(), storeNonce: "1".repeat(32), maximumRecords: 32 });
      const store = createWeb216D1SnapshotStore({ database: env.DB, initialSnapshot,
        material: { projection, expectedSoftware: software, expectedStoreId: initialSnapshot.descriptor.store_id } });
      if (url.pathname === "/provision" && request.method === "POST") {
        // Explicit test-owned DDL only. Normal MCP operations never provision.
        await env.DB.prepare(WEB216_D1_SCHEMA_SQL).run();
        const snapshot = await store.initialiseIfAbsent();
        return Response.json({ schema: "web216-local-worker-mcp-provision.v1",
          record_count: snapshot.records.length, store_id: snapshot.descriptor.store_id });
      }
      if (url.pathname === "/state" && request.method === "GET") {
        const snapshot = await store.readSnapshot();
        return Response.json({ canonical: canonicalJson(snapshot), record_count: snapshot.records.length,
          event_count: snapshot.events.length, checkpoint_id: snapshot.head.checkpoint_id });
      }
      if (url.pathname !== "/mcp") return new Response("Not found", { status: 404 });
      const application = createWeb216HostedCpihApplication({ store, projection, software,
        expectedStoreId: initialSnapshot.descriptor.store_id, now });
      const handler = createWeb216HostedCpihMcpHttpHandler(application);
      try {
        // The probe-only header supplies a fabricated second-argument body to
        // prove the hosted wrapper still parses the exact bytes on the wire.
        const response = request.headers.get("x-web216-probe-parsed-body-bypass") === "1"
          ? await handler.fetch(request, { parsedBody: fabricatedParsedBody })
          : await handler.fetch(request);
        // Complete this finite JSON response before closing the per-request fixture.
        const bytes = await response.arrayBuffer();
        if (bytes.byteLength > 1_048_576) throw new Error("Fixture response exceeds bound");
        return new Response(bytes.byteLength === 0 ? null : bytes, { status: response.status, headers: response.headers });
      } finally { await handler.close(); }
    } catch (error) {
      return Response.json({ probe_failure: true, name: error instanceof Error ? error.name : "unknown",
        message: error instanceof Error ? error.message : "unknown" }, { status: 500 });
    }
  },
};
