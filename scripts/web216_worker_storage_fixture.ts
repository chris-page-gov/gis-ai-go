// Development experiment only: never deploy or mount this fixture as a product route.
// Prerequisite: pnpm --filter @gis-ai-go/evidence run build
import {
  canonicalJson, createWeb216TransactionalSnapshot, createWeb216D1SnapshotStore,
  buildWeb216CpihReceipt, planWeb216TransactionalAppend, WEB216_D1_SCHEMA_SQL,
  type Web216D1Database,
} from "../packages/evidence/dist/src/index.js";
import projection from "../tests/fixtures/web216/current-cpih-projection.json";

// Fixed synthetic provenance, not an accepted-build revision or real request time.
const software = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) };
export default {
  async fetch(request: Request, env: { DB: Web216D1Database }): Promise<Response> {
    try {
      const initialSnapshot = createWeb216TransactionalSnapshot({
        projection, software, createdAt: "2026-09-14T18:00:00.000Z",
        storeNonce: "1".repeat(32), maximumRecords: 32,
      });
      const material = { projection, expectedSoftware: software, expectedStoreId: initialSnapshot.descriptor.store_id };
      const store = createWeb216D1SnapshotStore({ database: env.DB, initialSnapshot, material });
      if (new URL(request.url).pathname === "/exercise") {
        // Explicit test-owned provisioning. The application adapter never runs DDL.
        await env.DB.prepare(WEB216_D1_SCHEMA_SQL).run();
        let snapshot = await store.initialiseIfAbsent();
        const measurements = [];
        for (const [index, period] of [[1, "2026-01"], [2, "2026-07"]] as const) {
          const started = performance.now();
          const proposal = planWeb216TransactionalAppend(snapshot, {
            idempotencyKey: ["gis-ai-go", "ik", "v1", index.toString(16).padStart(64, "0")].join(":"),
            recordedAt: "2026-09-14T18:01:00.000Z",
            receipt: buildWeb216CpihReceipt({
              projection, software, period, requestId: `worker-probe-${index}`,
              traceId: "2".repeat(32), createdAt: "2026-09-14T18:01:00.000Z",
            }),
          }, material);
          if (proposal.status !== "append-plan-not-committed") throw Error("Unexpected existing test data");
          const result = await store.publish(proposal.plan);
          if (result.status !== "published-and-verified") throw Error("Expected a verified test write");
          snapshot = result.snapshot;
          measurements.push({ period, elapsed_ms: performance.now() - started, storage: result.observation });
        }
        return Response.json({ snapshot, canonical: canonicalJson(snapshot), measurements,
          live_provider: false, hosted_deployment: false });
      }
      if (new URL(request.url).pathname === "/inspect") {
        const snapshot = await store.readSnapshot();
        return Response.json({ snapshot, canonical: canonicalJson(snapshot),
          live_provider: false, hosted_deployment: false });
      }
      return new Response("Not found", { status: 404 });
    } catch (error) {
      return Response.json({ probe_failure: true,
        name: error instanceof Error ? error.name : "unknown",
        message: error instanceof Error ? error.message : "unknown" }, { status: 500 });
    }
  },
};
