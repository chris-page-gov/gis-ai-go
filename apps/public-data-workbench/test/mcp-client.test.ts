import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createHostedMcpCall, createMcpCall, type Operation } from "../src/mcp-client";

const sdk = vi.hoisted(() => ({
  connect: vi.fn(), callTool: vi.fn(), close: vi.fn(), client: vi.fn(), transport: vi.fn(),
}));
vi.mock("@modelcontextprotocol/client", () => ({
  Client: class {
    constructor(...args: unknown[]) { sdk.client(...args); }
    connect = sdk.connect; callTool = sdk.callTool; close = sdk.close;
  },
  StreamableHTTPClientTransport: class {
    constructor(...args: unknown[]) { sdk.transport(...args); }
  },
}));
const local = "http://127.0.0.1:8788";
const hosted = "https://gis-ai-go-webmcp-explorer.crpage.chatgpt.site";
const locationAt = (origin: string) => ({ origin }) as Location;
type FetchOptions = { fetch: typeof fetch };

beforeEach(() => {
  vi.clearAllMocks();
  sdk.connect.mockResolvedValue(undefined); sdk.close.mockResolvedValue(undefined);
  sdk.callTool.mockResolvedValue({ structuredContent: { example: "controller validates this" } });
});
afterEach(() => vi.unstubAllGlobals());

describe.each([
  ["local", createMcpCall, local, "/mcp", "omit"],
  ["hosted", createHostedMcpCall, hosted, "/workbench/mcp", "same-origin"],
] as const)("%s pinned browser MCP transport", (_label, create, origin, path, credentials) => {
  it("pins the endpoint and protocol, then closes the client", async () => {
    const result = await create(locationAt(origin))("web216_cpih_select", { period: "2026-07" });
    expect(result).toEqual({ example: "controller validates this" });
    expect(sdk.transport.mock.calls[0]![0].href).toBe(origin + path);
    expect(sdk.client.mock.calls[0]![1]).toEqual({ capabilities: {}, versionNegotiation: { mode: { pin: "2026-07-28" } } });
    expect(sdk.close).toHaveBeenCalledOnce();
  });

  it("refuses other origins and tool names before connecting", async () => {
    for (const wrong of [origin === local ? hosted : local, "https://example.invalid", origin + ".invalid"]) {
      await expect(create(locationAt(wrong))("web216_cpih_select", {})).rejects.toThrow(/discovery/);
    }
    await expect(create(locationAt(origin))("other" as Operation, {})).rejects.toThrow(/Unknown/);
    expect(sdk.client).not.toHaveBeenCalled();
  });

  it("overrides credential, redirect and cache options and refuses destination substitution", async () => {
    await create(locationAt(origin))("web216_cpih_select", {});
    const configured = sdk.transport.mock.calls[0]![1] as FetchOptions;
    const fetchMock = vi.fn().mockResolvedValue(new Response("{}")); vi.stubGlobal("fetch", fetchMock);
    await configured.fetch(origin + path, { credentials: "include", redirect: "follow", cache: "force-cache" });
    expect(fetchMock.mock.calls[0]![1]).toMatchObject({ credentials, redirect: "error", cache: "no-store" });
    expect(fetchMock.mock.calls[0]![1].signal).toBeInstanceOf(AbortSignal);
    for (const target of ["https://example.invalid/mcp", origin + path + "?other=1", origin + "/other", origin + path + "#fragment"]) {
      expect(() => configured.fetch(target)).toThrow(/unapproved destination/);
    }
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it("honours prior cancellation and closes after failed or malformed responses", async () => {
    await expect(create(locationAt(origin))("web216_cpih_select", {}, AbortSignal.abort())).rejects.toThrow();
    expect(sdk.client).not.toHaveBeenCalled();
    for (const result of [{ isError: true }, {}, { structuredContent: [] }]) {
      sdk.callTool.mockResolvedValueOnce(result);
      await expect(create(locationAt(origin))("web216_cpih_select", {})).rejects.toThrow();
    }
    expect(sdk.close).toHaveBeenCalledTimes(3);
  });
});
