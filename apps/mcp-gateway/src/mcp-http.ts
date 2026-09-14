import type { McpHttpHandler } from "@modelcontextprotocol/server";
import { createCatalogueMcpServerFactory, createGovernedCandidateMcpServerFactory, type CatalogueMcpOptions, type GovernedCandidateMcpOptions } from "./mcp-server.js";
import { snapshotGovernedCandidateOptions, type GovernedCandidateAssembly } from "./governed-assembly.js";
import type { Web216CpihApplication } from "./web216-cpih-application.js";
import { createWeb216CpihMcpServerFactory } from "./web216-cpih-mcp.js";
import { createBoundedMcpHttpHandler, errorResponse } from "./mcp-http-core.js";
export { MCP_HTTP_MAX_STANDALONE_BODY_BYTES } from "./mcp-http-core.js";

const TRANSPORT_ERROR = -32_000;

/**
 * Create the modern-only fetch face. Host, Origin, route, body-size,
 * concurrency and timeout controls belong to the Node ingress that mounts it.
 */
export function createCatalogueMcpHttpHandler(
  options: CatalogueMcpOptions,
): McpHttpHandler {
  return createBoundedMcpHttpHandler(
    createCatalogueMcpServerFactory(options),
    options.onerror,
  );
}

/** Create modern MCP HTTP from the same candidate-unregistered assembly. */
export function createGovernedCandidateMcpHttpHandler(
  assembly: GovernedCandidateAssembly,
  options: GovernedCandidateMcpOptions = {},
): McpHttpHandler {
  const exactOptions = snapshotGovernedCandidateOptions(
    options,
    ["createRequestContext", "onerror"],
    "Governed candidate MCP HTTP options",
  ) as GovernedCandidateMcpOptions;
  return createBoundedMcpHttpHandler(
    createGovernedCandidateMcpServerFactory(assembly, exactOptions),
    exactOptions.onerror,
  );
}

/**
 * Inactive loopback-only Fetch face for the separately branded CPIH experiment.
 * This opens no port. A future Node listener still owns concurrency, timeouts and
 * socket-level Host validation; it cannot infer activation from this constructor.
 */
export function createWeb216CpihMcpHttpHandler(
  application: Web216CpihApplication,
): McpHttpHandler {
  const handler = createBoundedMcpHttpHandler(createWeb216CpihMcpServerFactory(application), undefined);
  return {
    ...handler,
    fetch: (request) => {
      const url = new URL(request.url);
      const host = request.headers.get("host");
      const origin = request.headers.get("origin");
      if (url.protocol !== "http:" || url.host !== "127.0.0.1:8788" ||
          url.username !== "" || url.password !== "" || url.pathname !== "/mcp" ||
          url.search !== "" || url.hash !== "" ||
          (host !== null && host !== url.host) || (origin !== null && origin !== url.origin)) {
        return Promise.resolve(errorResponse(403, TRANSPORT_ERROR, "Experimental MCP ingress rejected", {
          reason: "experimental_loopback_boundary",
        }));
      }
      // Always parse the actual bounded wire bytes; no caller-supplied parsed body.
      return handler.fetch(request);
    },
  };
}
