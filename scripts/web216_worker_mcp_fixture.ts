// Local compatibility fixture only. Never deploy or mount its provisioning routes.
import { createMcpHandler } from "@modelcontextprotocol/server";
import {
  canonicalJson, createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot,
  WEB216_D1_SCHEMA_SQL, type Web216D1Database,
} from "../packages/evidence/dist/src/index.js";
import { createWeb216HostedCpihApplication } from "../apps/mcp-gateway/src/web216-hosted-cpih-application.js";
import { createWeb216HostedCpihMcpServerFactory } from "../apps/mcp-gateway/src/web216-hosted-cpih-mcp.js";
import { withMcpHttpDataQuerySignal } from "../apps/mcp-gateway/src/mcp-request-signal.js";
import projection from "../tests/fixtures/web216/current-cpih-projection.json";

// Fixed synthetic software/request time; not accepted-build or source-time proof.
const software = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) };
const now = () => new Date("2026-09-14T18:00:00.000Z");
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
      const handler = createMcpHandler(createWeb216HostedCpihMcpServerFactory(application), {
        legacy: "reject", responseMode: "json",
      });
      try {
        const response = await withMcpHttpDataQuerySignal(request.signal, () => handler.fetch(request));
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
