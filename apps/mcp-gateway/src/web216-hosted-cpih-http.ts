/** Inactive hosted Fetch face. Mounting ingress owns identity, Host/Origin, route,
 * concurrency, deadlines and response limits. This constructor opens no listener. */
import type { McpHttpHandler } from "@modelcontextprotocol/server";
import type { Web216HostedCpihApplication } from "./web216-hosted-cpih-application.js";
import { createWeb216HostedCpihMcpServerFactory } from "./web216-hosted-cpih-mcp.js";
import { createBoundedJsonOnlyMcpHttpHandler } from "./mcp-http-core.js";

export function createWeb216HostedCpihMcpHttpHandler(
  application: Web216HostedCpihApplication,
): McpHttpHandler {
  const handler = createBoundedJsonOnlyMcpHttpHandler(createWeb216HostedCpihMcpServerFactory(application));
  return {
    ...handler,
    // Discard fabricated parsedBody and other per-request overrides. Only actual
    // bounded request bytes enter the hosted application.
    fetch: (request) => handler.fetch(request),
  };
}
