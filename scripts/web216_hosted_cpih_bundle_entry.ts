/** Explicit inactive hosted bundle surface; never import the gateway root barrel. */
export {
  canonicalJson, createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot,
  verifyWeb216TransactionalSnapshot,
} from "../packages/evidence/src/web216-pure.js";
export { createWeb216HostedCpihApplication } from "../apps/mcp-gateway/src/web216-hosted-cpih-application.js";
export { createWeb216HostedCpihMcpHttpHandler } from "../apps/mcp-gateway/src/web216-hosted-cpih-http.js";
export { default as cpihProjection } from "../tests/fixtures/web216/current-cpih-projection.json";
