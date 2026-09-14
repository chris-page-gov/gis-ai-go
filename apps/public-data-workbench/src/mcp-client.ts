import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

export type Operation = "web216_cpih_select" | "web216_cpih_query" | "web216_cpih_inspect";
export type McpCall = (name: Operation, input: Record<string, unknown>, signal?: AbortSignal) => Promise<Record<string, unknown>>;

/** Browser cannot choose another server, origin, credentials or protocol. */
export function createMcpCall(location: Location): McpCall {
  return createPinnedMcpCall(location, false);
}

/** Separate private-Site route; never a proxy to the visitor's laptop. */
export function createHostedMcpCall(location: Location): McpCall {
  return createPinnedMcpCall(location, true);
}

function createPinnedMcpCall(location: Location, hosted: boolean): McpCall {
  const origin = hosted ? "https://gis-ai-go-webmcp-explorer.crpage.chatgpt.site" : "http://127.0.0.1:8788";
  const endpoint = new URL(hosted ? "/workbench/mcp" : "/mcp", origin);
  return async (name, input, signal) => {
    if (location.origin !== origin) {
      throw new Error(hosted ? "Retrieval is available only on the approved private Site. This preview only supports discovery."
        : "Retrieval needs the local workbench at http://127.0.0.1:8788. This preview only supports discovery.");
    }
    if (!["web216_cpih_select", "web216_cpih_query", "web216_cpih_inspect"].includes(name)) throw new Error("Unknown workbench operation.");
    signal?.throwIfAborted();
    const boundedSignal = AbortSignal.any([AbortSignal.timeout(15_000), ...(signal ? [signal] : [])]);
    const client = new Client({ name: "gis-ai-go-public-data-workbench", version: "0.1.0" }, {
      capabilities: {}, versionNegotiation: { mode: { pin: "2026-07-28" } },
    });
    const transport = new StreamableHTTPClientTransport(endpoint, {
      fetch: (url, init) => {
        const target = new URL(url instanceof Request ? url.url : String(url));
        if (target.href !== endpoint.href) throw new Error("The MCP transport attempted an unapproved destination.");
        return fetch(url, { ...init, credentials: hosted ? "same-origin" : "omit", redirect: "error", cache: "no-store", signal: boundedSignal });
      },
    });
    try {
      await client.connect(transport);
      const result = await client.callTool({ name, arguments: input }, { signal: boundedSignal });
      boundedSignal.throwIfAborted();
      if (result.isError) throw new Error("The MCP server declined this operation. No success is claimed; retry uses the same request key.");
      if (!result.structuredContent || typeof result.structuredContent !== "object" || Array.isArray(result.structuredContent)) throw new Error("The MCP server returned no structured evidence.");
      return result.structuredContent as Record<string, unknown>;
    } finally { await client.close(); }
  };
}
